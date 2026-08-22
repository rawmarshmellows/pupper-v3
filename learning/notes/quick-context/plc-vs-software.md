---
topic: PLC and why it's different to software and how it's implemented
created: 2026-01-14
---

> **Related:** [[quick-context/plc-vs-software-control]] | [[quick-context/preempt-rt]] | [[quick-context/sil-rated-safety-functions]]

> **TL;DR:** PLCs are purpose-built for deterministic, fail-safe control in harsh industrial environments where general-purpose computers would crash, freeze, or get people killed.

# PLC: Why It's Different From Software

## The Core Problem: When Computers Crash, People Die

A **[[micro-context/plc-programmable-logic-controller|Programmable Logic Controller]] ([[micro-context/plc-programmable-logic-controller|PLC]])** exists because general-purpose computers fail catastrophically in industrial environments—they crash, they need reboots, they have non-deterministic timing, and when they freeze, people die or million-dollar equipment destroys itself. PLCs solve the problem of executing control logic with absolute determinism and reliability in harsh conditions (vibration, temperature extremes, electrical noise).

Before PLCs, factories used massive relay panels with hundreds of physical switches wired together; changing the logic meant rewiring. PLCs replaced that with programmable logic while keeping the same deterministic, fail-safe behavior. If a PLC stops running, a conveyor might crush someone, a chemical reactor might overheat, or a robot arm might swing into a human. The failure mode isn't "restart the app"—it's "call the coroner."

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Scan Cycle** | The fixed-interval loop where a PLC reads inputs, runs logic, and writes outputs—typically 10-50ms, absolutely predictable. |
| **Ladder Logic** | Visual programming language resembling electrical relay diagrams, designed for electricians who understood relays, not programmers. |
| **I/O Modules** | Hardware cards that connect PLCs to real-world sensors and actuators—the physical interface to the plant. |
| **HMI** | Human-Machine Interface—the touchscreen operators use to monitor and control the process. |
| **Fail-safe** | The designed behavior when something goes wrong, always defaulting to the safest state (usually: stop everything). |

<details>
<summary><strong>How It Works</strong></summary>

The PLC executes in a **scan cycle**: read all inputs, execute all logic top-to-bottom, write all outputs, repeat forever at a predictable interval (often 10-50ms). This makes timing behavior absolutely predictable.

```
┌─────────────────────────────────────────┐
│           PLC SCAN CYCLE                │
│                                         │
│  1. READ ALL INPUTS (sensors, switches) │
│              ↓                          │
│  2. EXECUTE ALL LOGIC (top to bottom)   │
│              ↓                          │
│  3. WRITE ALL OUTPUTS (motors, valves)  │
│              ↓                          │
│  4. REPEAT (every 10-50ms, guaranteed)  │
└─────────────────────────────────────────┘
```

Modern PLCs support IEC 61131-3 languages:
- **Ladder Logic** - Visual, looks like relay circuits
- **Structured Text (ST)** - Looks like Pascal, closest to "real programming"
- **Function Block Diagram (FBD)** - Visual dataflow

The key difference from software: a PLC doesn't "crash" in the traditional sense. If the program has a bug, the scan cycle still runs. If hardware fails, the system goes to a defined fail-safe state. There's no blue screen, no segfault, no "application not responding."

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The central tension in PLC work is **determinism vs. flexibility**. Traditional PLC programming uses Ladder Logic, which executes in a fixed scan cycle making timing behavior absolutely predictable—but makes complex algorithms painful.

Modern practitioners argue constantly about:
- When to use IEC 61131-3 languages (Structured Text looks like Pascal) versus sticking with ladder logic that any maintenance electrician can troubleshoot at 3am
- Whether to stay in proprietary vendor ecosystems (Allen-Bradley, Siemens, Mitsubishi all have incompatible tooling) versus pushing toward more open, software-like approaches

The industry philosophy is inverted from software: in software, you optimize for features and fix bugs with patches; in PLC programming, you optimize for *never needing to change it* and for *any failure to be obvious and recoverable*. The code isn't clever—it's deliberately simple, because cleverness kills people when a maintenance tech has to debug it during an emergency at 2am with the plant manager screaming.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

A simple safety interlock in ladder logic vs. Python:

**Ladder Logic (PLC):**
```
     |  GUARD_CLOSED    MOTOR_RUNNING    ESTOP_NOT_PRESSED  |
-----|-------] [------------] [---------------] [-----------|----( )--- ALLOW_MOTION
     |                                                      |
```

**Python equivalent (conceptually):**
```python
# This looks simpler but hides the critical difference
allow_motion = guard_closed and motor_running and not estop_pressed
```

The ladder logic version:
- Executes every scan cycle (10ms), guaranteed
- If any input fails (wire breaks), defaults to FALSE (safe)
- Any electrician can read it and verify the logic
- Has been running unchanged for 15 years

The Python version:
- Might not run if the OS is busy
- If the sensor library crashes, the whole program crashes
- Requires a software engineer to debug
- Needs updates for security patches, dependency changes

**The one thing most outsiders get wrong about this is...** thinking PLCs are just "embedded systems" or "slow computers running simple code." The entire paradigm is inverted: in software, you optimize for features and fix bugs with patches; in PLC programming, you optimize for *never needing to change it* and for *any failure to be obvious and recoverable*. The code isn't clever—it's deliberately simple, because cleverness kills people when a maintenance tech has to debug it during an emergency at 2am with the plant manager screaming.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/plc-vs-software-control]]** - How PLCs and software divide responsibilities in modern robotic systems
- **[[quick-context/preempt-rt]]** - Linux kernel patches that let software approach (but not match) PLC determinism
- **[[quick-context/preempt-rt-ros2-plc-replacement]]** — The 2025-2026 state of replacing PLCs entirely with PREEMPT_RT + ROS2, including production hardware and real factory deployments
- **[[quick-context/sil-rated-safety-functions]]** - The certification framework that makes PLCs mandatory for safety-critical functions
- **[[quick-context/isa-95-levels]]** - Where PLCs fit in the automation hierarchy (Level 1-2)

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why do PLCs use ladder logic instead of a "normal" programming language?
<details>
<summary>Answer</summary>
Ladder logic was designed for electricians who understood relay circuits, not programmers. It visually resembles the relay panels it replaced, making it readable by maintenance technicians who need to troubleshoot at 3am without software engineering training. The visual format also makes it easy to verify safety interlocks by inspection.
</details>

**Q2:** What happens if a PLC program has an infinite loop?
<details>
<summary>Answer</summary>
The PLC's watchdog timer detects that the scan cycle exceeded its maximum allowed time and forces the system into a fail-safe state (usually stopping all outputs). Unlike a computer that would freeze, the PLC has hardware-level protection against runaway code. This is why scan cycle time is monitored and bounded.
</details>

**Q3:** Why can't you just run PLC logic on a Raspberry Pi with careful programming?
<details>
<summary>Answer</summary>
Three reasons: (1) Linux on a Pi has non-deterministic timing—garbage collection, kernel interrupts, or SD card writes can cause multi-millisecond delays. (2) A Pi lacks the electrical hardening (noise immunity, wide temperature range, vibration resistance) for industrial environments. (3) No safety certification—regulators won't accept it for safety-critical functions regardless of how well it works in testing.
</details>

**Q4:** What is the scan cycle, and why is its predictability important?
<details>
<summary>Answer</summary>
The scan cycle is the fixed-interval loop where a PLC reads all inputs, executes all logic top-to-bottom, and writes all outputs—typically every 10-50ms. Its predictability is critical because industrial processes depend on knowing exactly when actions will occur. If timing varies unpredictably, a conveyor might start before a part is in position, or a safety interlock might not trigger in time.
</details>

**Q5:** Why do PLCs default to a "fail-safe" state rather than trying to recover automatically?
<details>
<summary>Answer</summary>
In safety-critical systems, an unknown state is more dangerous than a stopped state. If a PLC loses communication with a sensor or detects an error, it cannot safely assume what the correct action should be. Stopping everything (the fail-safe state) ensures that no dangerous motion occurs while humans assess and correct the situation. Automatic recovery could mask the root cause or take action based on incorrect assumptions.
</details>

</details>
