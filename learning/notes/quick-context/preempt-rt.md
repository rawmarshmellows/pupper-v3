---
topic: PREEMPT_RT
created: 2026-01-17
---

> **Related:** [[quick-context/plc-vs-software-control]] | [[quick-context/preempt-rt-ros2-plc-replacement]] | [[quick-context/plc-vs-software]] | [[quick-context/sil-rated-safety-functions]]

> **TL;DR:** PREEMPT_RT patches the Linux kernel to provide bounded worst-case latency (~50-100us), enabling soft real-time control loops in userspace - but it's not a replacement for safety-certified PLCs.

# PREEMPT_RT: Real-Time Linux for Industrial Control

## The Core Problem: Linux Doesn't Care About Your Deadlines

Standard Linux is a time-sharing system optimized for throughput, not response time. When your Python program asks the kernel to do something, it might wait microseconds—or it might wait 10 milliseconds while the kernel services disk I/O, runs another process, or handles network interrupts. For web servers, this is fine. For servo motor control, it's catastrophic.

If you're interpolating trajectory waypoints at 1kHz and one cycle takes 15ms instead of 1ms, your robot arm doesn't smoothly trace an arc—it jerks, overshoots, or faults the drive. PREEMPT_RT patches the Linux kernel to make nearly all kernel code preemptible, meaning your real-time task can interrupt almost anything the kernel is doing.

The result is bounded worst-case latency (typically under 100us on good hardware) instead of unbounded spikes. Without it, you cannot run a motion control loop in userspace Linux and expect it to behave like a PLC. With it, you can build "soft PLCs" on commodity x86 hardware that achieve 1ms cycle times reliably enough for many industrial applications—though not for SIL-rated safety functions.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Jitter** | The variation in cycle timing—if your loop runs at 1ms +/- 5us, jitter is 5us; if it's 1ms +/- 2ms, you have a problem that PREEMPT_RT exists to solve. |
| **Latency** | The time from when an event occurs (e.g., encoder pulse) to when your code responds—PREEMPT_RT bounds this; stock Linux does not. |
| **SCHED_FIFO** | The Linux scheduler policy for real-time tasks—first-in-first-out at a given priority, with no time-slicing; your RT thread runs until it blocks or yields. |
| **Cyclictest** | The standard tool for measuring real-time latency in Linux—it spawns a thread, sleeps for a fixed interval, measures how late it wakes up, and reports statistics. |
| **IRQ Threading** | PREEMPT_RT's technique of running interrupt handlers as kernel threads instead of in "hard IRQ" context, making them preemptible by higher-priority tasks. |

<details>
<summary><strong>How It Works</strong></summary>

PREEMPT_RT modifies the Linux kernel in several key ways:

1. **Threaded Interrupts**: Hardware interrupt handlers run as schedulable kernel threads, not in hard IRQ context
2. **Preemptible Spinlocks**: Most spinlocks become mutexes that can be preempted
3. **Priority Inheritance**: Prevents priority inversion where a low-priority task blocks a high-priority one
4. **High-Resolution Timers**: Enables microsecond-precision sleep and wake-up

First, verify your kernel has PREEMPT_RT and measure baseline latency:

```bash
# Check kernel config
uname -a  # Should show "PREEMPT_RT" or "PREEMPT RT"
# e.g.: Linux rt-controller 6.6.0-rt14 #1 SMP PREEMPT_RT x86_64

# Run cyclictest under load (stress simulates real workload)
sudo stress --cpu 4 --io 2 --vm 2 &
sudo cyclictest -m -Sp90 -i1000 -h400 -q -l10000

# Output interpretation:
# T: 0 ( 1234) P:90 I:1000 C:  10000 Min:      3 Act:    7 Avg:    5 Max:   47
#                                                                    ^^^^
# Max latency of 47us under load - acceptable for 1ms control loop
```

A minimal real-time control loop in C:

```c
// rt_control_loop.c - 1kHz control loop with bounded jitter
#define _GNU_SOURCE
#include <sched.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

#define NSEC_PER_SEC 1000000000L
#define CYCLE_NS     1000000L  // 1ms cycle time

static inline void timespec_add_ns(struct timespec *t, long ns) {
    t->tv_nsec += ns;
    while (t->tv_nsec >= NSEC_PER_SEC) {
        t->tv_nsec -= NSEC_PER_SEC;
        t->tv_sec++;
    }
}

int main() {
    struct sched_param param = { .sched_priority = 90 };
    struct timespec next_cycle;

    // Lock memory - prevents page faults during RT operation
    mlockall(MCL_CURRENT | MCL_FUTURE);

    // Set SCHED_FIFO with priority 90 (high, but below kernel threads)
    if (sched_setscheduler(0, SCHED_FIFO, &param) == -1) {
        perror("sched_setscheduler failed - are you root?");
        exit(1);
    }

    clock_gettime(CLOCK_MONOTONIC, &next_cycle);

    while (1) {
        // === Your control code here ===
        // Read encoders, compute PID, write to DAC
        // This MUST complete in <1ms
        do_control_iteration();
        // ===============================

        // Sleep until next cycle - this is where PREEMPT_RT matters
        // On stock Linux: might wake up 5ms late
        // On PREEMPT_RT:  wakes up within ~50us of target
        timespec_add_ns(&next_cycle, CYCLE_NS);
        clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next_cycle, NULL);
    }
}
```

Compile and run:
```bash
gcc -O2 -o rt_control rt_control_loop.c -lrt
sudo ./rt_control  # Requires root for SCHED_FIFO
```

The difference: on stock Linux under load, `clock_nanosleep` might return anywhere from on-time to 10ms late. With PREEMPT_RT, worst-case is typically 50-100us late—well within tolerance for a 1ms control loop.

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The core tradeoff is **latency vs. throughput and ecosystem**. A fully preemptible kernel means the scheduler can yank control away from almost any code path, which requires:
- Replacing spinlocks with mutexes (adding overhead)
- Carefully auditing drivers
- Accepting that some hardware simply won't work well

You also give up most of Linux's power management and some security features.

Practitioners argue about where the acceptable latency boundary lies:
- Some say PREEMPT_RT's ~50-100us worst-case is fine for 1ms control loops
- Others insist you need a dual-kernel architecture (Xenomai, RTLinux) that runs your real-time code in a separate domain where Linux can't interfere at all

The 2024 mainlining of PREEMPT_RT into the official kernel (after 20 years as an out-of-tree patch) settled the "will this exist long-term?" question, but the "is soft real-time good enough for my application?" debate remains application-specific. If you need sub-10us jitter or safety certification, PREEMPT_RT is a starting point, not a destination.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Consider a CNC machine controller running on Linux:

**Without PREEMPT_RT:**
- You set up a 1ms timer for trajectory interpolation
- Under normal conditions, it runs fine
- Then someone starts a file copy in the background
- The kernel services disk I/O, your timer callback is delayed 8ms
- The tool path suddenly has an 8mm gap, ruining the part (or worse, crashing the tool)

**With PREEMPT_RT:**
- Same 1ms timer for trajectory interpolation
- File copy starts in the background
- Your RT thread (priority 90) preempts the disk I/O handler
- Timer callback runs within 50us of schedule
- Tool path remains smooth, part comes out correctly

This is why LinuxCNC (an open-source CNC controller) requires PREEMPT_RT. It's also why projects like ROS2's real-time capabilities and CODESYS-on-Linux depend on it.

**The one thing most outsiders get wrong about this is...** assuming PREEMPT_RT turns Linux into a PLC. It doesn't. It gives you *bounded* latency, not *zero* latency—and those bounds (50-100us typical, potentially worse with bad drivers or hardware) aren't certified or guaranteed. A SIL-rated safety function still needs a proper safety PLC. What PREEMPT_RT actually enables is running the "soft" parts of automation—trajectory interpolation, sensor fusion, high-level coordination—in userspace Linux at 1kHz without random multi-millisecond stalls.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/plc-vs-software-control]]** - How PREEMPT_RT-enabled systems divide work with traditional PLCs
- **[[quick-context/plc-vs-software]]** - Why PLCs exist and what guarantees they provide that PREEMPT_RT cannot match
- **[[quick-context/sil-rated-safety-functions]]** - The certification requirements that still mandate hardware PLCs for safety
- **[[quick-context/preempt-rt-ros2-plc-replacement]]** — The current state of using PREEMPT_RT + ROS2 to replace PLCs entirely, including production hardware (Bosch ctrlX, ADLINK ROScube, Beckhoff TwinCAT on Linux) and the remaining safety certification gap
- **Xenomai** - A dual-kernel alternative providing harder real-time guarantees than PREEMPT_RT
- **LinuxCNC** - The canonical example of PREEMPT_RT enabling industrial control in userspace

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does PREEMPT_RT convert spinlocks to mutexes, and what's the tradeoff?
<details>
<summary>Answer</summary>
Spinlocks disable preemption while held—if a low-priority task holds a spinlock, a high-priority RT task can't preempt it, causing unbounded latency. Converting to mutexes (with priority inheritance) lets the RT task preempt and, if needed, boost the lock holder's priority to release it faster. The tradeoff is overhead: mutex operations are slower than spinlocks, reducing overall throughput for non-RT workloads.
</details>

**Q2:** Your cyclictest shows 47us max latency. Is this system suitable for a 100us control loop?
<details>
<summary>Answer</summary>
Probably not. The max latency of 47us is already half your cycle budget. Cyclictest measures scheduling latency, not your actual control code execution time. If your control iteration takes 30us and scheduling adds 47us, you're already at 77us—leaving only 23us margin. You'd want max latency under 20us for a 100us loop, or need to move to a dual-kernel solution like Xenomai.
</details>

**Q3:** Why can't PREEMPT_RT be used for SIL-rated safety functions?
<details>
<summary>Answer</summary>
SIL (Safety Integrity Level) certification requires formal proof of bounded behavior, extensive testing, and hardware-level fail-safes. PREEMPT_RT provides probabilistic guarantees ("typically under 100us") not formal ones—a misbehaving driver or hardware issue could still cause an unbounded delay. Additionally, the complexity of the Linux kernel makes formal verification effectively impossible. Safety PLCs have certified hardware watchdogs, redundant processors, and audited code paths that Linux cannot match.
</details>

**Q4:** What is the difference between jitter and latency in the context of real-time systems?
<details>
<summary>Answer</summary>
Latency is the time from when an event occurs (e.g., a timer expiring or sensor signal arriving) to when your code responds. Jitter is the variation in that timing—if your loop runs at 1ms +/- 5us, jitter is 5us. Both matter: high latency means slow response, and high jitter means unpredictable timing that can cause motion irregularities or control instability.
</details>

**Q5:** What does cyclictest measure, and why is it not sufficient to validate a real-time control system?
<details>
<summary>Answer</summary>
Cyclictest measures scheduling latency—how late a thread wakes up compared to when it asked to wake. This is useful for characterizing kernel behavior, but it doesn't account for your actual control code execution time, I/O latency, or application-specific timing requirements. A system passing cyclictest can still fail in production if the control loop itself is too slow or if hardware introduces additional delays.
</details>

</details>
