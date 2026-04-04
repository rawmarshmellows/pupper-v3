---
topic: PREEMPT_RT + ROS2 as PLC Replacement
created: 2026-03-13
---

# PREEMPT_RT + ROS2 as PLC Replacement

> **Related:** [[quick-context/preempt-rt]] | [[quick-context/plc-vs-software-control]] | [[quick-context/sil-rated-safety-functions]] | [[quick-context/ros2-architecture]]

> **TL;DR:** A growing ecosystem of industrial hardware (Bosch ctrlX CORE, Phoenix Contact PLCnext, ADLINK ROScube, Beckhoff TwinCAT on Linux) now runs [[quick-context/preempt-rt|PREEMPT_RT]] Linux with ROS2 to handle motion control, EtherCAT fieldbus communication, and AI/perception on a single platform — replacing the traditional split between [[quick-context/plc-vs-software-control|PLCs and software]]. The remaining hard gap is [[quick-context/sil-rated-safety-functions|SIL-rated safety certification]]: no PREEMPT_RT + ROS2 stack has achieved SIL-2/SIL-3, so safety-critical functions still require dedicated safety PLCs.

## The Core Problem

Industrial automation has historically required two separate worlds: [[quick-context/plc-vs-software|PLCs]] for deterministic real-time control (motor loops, safety interlocks, fieldbus I/O) and general-purpose computers for intelligence (vision, path planning, AI). Integrating them means OPC-UA bridges, data format translations, and duplicate hardware — a tax on every project. The promise of [[quick-context/preempt-rt|PREEMPT_RT]] + ROS2 is collapsing these into one platform: a Linux system deterministic enough for 1 ms servo loops *and* capable enough for neural networks and SLAM. As of 2025-2026, this is no longer theoretical — production hardware exists and real factories are running it — but the safety certification gap means the PLC isn't dead yet.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Soft [[micro-context/plc-programmable-logic-controller|PLC]]** | Software implementing PLC runtime semantics (scan cycle, IEC 61131-3 languages, fieldbus I/O) on commodity Linux/PC hardware instead of dedicated PLC hardware — e.g., CODESYS, Beckhoff TwinCAT, Bosch ctrlX. |
| **Virtual PLC** | A soft PLC running in a container or VM, enabling multiple "PLC instances" on shared server infrastructure — Audi's EC4P runs Siemens S7-1500V in Docker containers replacing floor-level hardware PLCs. |
| **EtherCAT on ROS2** | Integration of EtherCAT fieldbus (the dominant industrial real-time network) directly into the [[quick-context/ros2-architecture|ROS2]] control stack via drivers like `ethercat_driver_ros2` or ADLINK's software-defined EtherCAT — eliminating the need for a separate PLC to talk to servo drives. |
| **ros2_control** | The ROS2 framework for real-time hardware abstraction — provides a controller manager that ticks hardware interfaces at fixed rates (up to 2000 Hz demonstrated by PAL Robotics), with pluggable controllers for PD, trajectory tracking, etc. |
| **Codethink CTRL OS** | The world's first Linux-based OS to receive a baseline safety assessment to SIL-3/ASIL-D (May 2025, validated by exida) — a landmark that opens a path toward safety-certifiable Linux, though not yet a full product certification. |

<details>
<summary><strong>How It Works</strong> — The converging architecture</summary>

### The Traditional Split (What We're Replacing)

The [[quick-context/plc-vs-software-control|traditional architecture]] uses two separate hardware platforms connected by a bridge protocol:

```
TRADITIONAL ARCHITECTURE
================================================================

  ┌──────────────────────────────┐     ┌──────────────────────────┐
  │  LINUX PC (Non-Real-Time)    │     │  PLC (Hard Real-Time)    │
  │                              │     │                          │
  │  ROS2 nodes:                 │     │  Scan cycle (1-10 ms):   │
  │   - Camera / vision          │     │   - Read fieldbus I/O    │
  │   - SLAM / navigation        │     │   - Safety interlocks    │
  │   - MoveIt path planning     │     │   - Motion interpolation │
  │   - ML inference             │     │   - Servo loop control   │
  │                              │     │                          │
  │  Languages: Python, C++      │     │  Languages: Ladder, ST   │
  │  Timing: best-effort         │     │  Timing: deterministic   │
  └──────────────┬───────────────┘     └──────────┬───────────────┘
                 │                                 │
                 │         OPC-UA bridge            │
                 │  (waypoints, status, commands)   │
                 └────────────────┬────────────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │  EtherCAT / PROF- │
                        │  INET fieldbus    │
                        │  → Servo drives   │
                        │  → Sensors / I/O  │
                        └──────────────────┘

  Two platforms, two languages, two toolchains, one bridge.
```

### The Converging Architecture (What's Emerging)

PREEMPT_RT + ROS2 enables a single platform running both real-time control and AI/perception. The key enablers: PREEMPT_RT merged into mainline Linux kernel v6.12 (September 2024), `ros2_control` providing deterministic hardware-interface ticking, and EtherCAT drivers bringing fieldbus I/O directly into ROS2.

```
CONVERGING ARCHITECTURE (Bosch ctrlX / PLCnext / ROScube model)
================================================================

  ┌──────────────────────────────────────────────────────────────┐
  │  SINGLE LINUX PLATFORM (PREEMPT_RT kernel)                   │
  │                                                              │
  │  ┌────────────────────┐    ┌─────────────────────────────┐   │
  │  │  Real-Time Domain  │    │  Non-Real-Time Domain       │   │
  │  │  (SCHED_FIFO,      │    │  (standard processes)       │   │
  │  │   pinned cores)    │    │                             │   │
  │  │                    │    │  ROS2 nodes:                │   │
  │  │  ros2_control:     │    │   - Camera / vision         │   │
  │  │   - 1 kHz tick     │    │   - SLAM / navigation       │   │
  │  │   - PD controller  │    │   - MoveIt planning         │   │
  │  │   - EtherCAT I/O   │    │   - ML inference            │   │
  │  │                    │    │   - LLM / voice             │   │
  │  │  Soft PLC runtime  │    │                             │   │
  │  │  (optional):       │    │  Languages: Python, C++     │   │
  │  │   - IEC 61131-3    │    │  Timing: best-effort        │   │
  │  │   - Safety logic   │    │                             │   │
  │  └────────┬───────────┘    └──────────────┬──────────────┘   │
  │           │                               │                  │
  │           │    Shared memory / DDS        │                  │
  │           └───────────────┬───────────────┘                  │
  │                           │                                  │
  └───────────────────────────┼──────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  EtherCAT / CAN  │
                    │  → Servo drives  │
                    │  → Sensors / I/O │
                    └──────────────────┘

  One platform. Real-time and AI share data via shared memory.
  No OPC-UA bridge. No separate PLC hardware.
```

### Timing Performance: Can It Actually Match a PLC?

[[quick-context/preempt-rt|PREEMPT_RT]] on tuned hardware achieves latency that meets most industrial control requirements:

| Metric | PREEMPT_RT (tuned) | Typical PLC | Verdict |
|--------|-------------------|-------------|---------|
| Achievable cycle time | 250 us - 1 ms | 1-50 ms | PREEMPT_RT can run *faster* |
| Worst-case jitter at 1 ms cycle | +/- 4 us (with EtherCAT) | < 1 us (hardware) | PLC still wins on jitter |
| Worst-case latency | 20-100 us | < 1 us | PLC wins, but 100 us is fine for 1 ms loops |

For context: industrial robots typically require timing jitter under 200 us for a 1 ms control cycle. PREEMPT_RT comfortably meets this. The gap only matters for sub-microsecond synchronization needs (e.g., multi-axis CNC interpolation at very high speeds).

### The Hardware Landscape (2025-2026)

**Tier 1 — Explicitly marketed as PLC replacements with ROS2:**

| Platform | Key Feature | Real-Time Approach | Fieldbus |
|----------|-------------|-------------------|----------|
| **Bosch Rexroth ctrlX CORE** | Shared memory between ROS2, PLC, and Datalayer | ctrlX OS (RT Linux) | EtherCAT, PROFINET, Sercos |
| **b-robotized b-controlled box** | One-click sim-to-real deployment | ROS2 + ros2_control | EtherCAT, ProfiNET, CAN, Modbus |
| **Phoenix Contact PLCnext** | IEC 61131-3 alongside Docker + ROS2 | PREEMPT_RT (Yocto) | PROFINET, EtherCAT (modules) |

**Tier 2 — Industrial platforms with ROS2 integration:**

| Platform | Key Feature | ROS2 Integration |
|----------|-------------|-----------------|
| **ADLINK ROScube** | Software-defined EtherCAT eliminates separate controllers | Built-in ROS2 SDK |
| **Beckhoff TwinCAT on Linux** (Sept 2025) | Containerized PLC runtime + GPU access | ros2_control via ADS |
| **Intel Embodied Intelligence SDK** | IgH EtherCAT Master + PLCopen motion library | DDS gateway bridge |
| **Siemens ROSie** | SIMATIC software PLC + ROS2 shared memory | Code-gen connector |

**EtherCAT integration** — the critical piece for PLC replacement — is available now via:
- **ICube-Robotics `ethercat_driver_ros2`** — integrates EtherCAT modules with ros2_control using the IgH EtherCAT Master
- **acontis EC-Master ROS2 Node** — standalone EtherCAT master as a ROS2 node (expected Q1 2026)
- **ADLINK Software-defined EtherCAT** — EtherCAT master integrated directly into ROS2 controller stack

</details>

<details>
<summary><strong>The Key Tension</strong> — Safety certification is the last moat</summary>

The technical capability gap between PREEMPT_RT + ROS2 and PLCs has mostly closed. The remaining gap is institutional: [[quick-context/sil-rated-safety-functions|safety certification]].

### What's Already Achievable

For **non-safety** real-time control — servo loops, motion interpolation, fieldbus I/O, trajectory tracking — PREEMPT_RT + ROS2 is production-ready. Audi runs virtual PLCs (Siemens S7-1500V in Docker) at their e-tron GT plant. PAL Robotics runs ros2_control at 2000 Hz on production humanoids. Panasonic built an AMR in 2 months using ADLINK's ROS2 + EtherCAT stack with 30% cost reduction.

### What's Still Blocked

For **safety-critical functions** — e-stops, light curtain interlocks, anything requiring [[quick-context/sil-rated-safety-functions|SIL-2/SIL-3]] certification — dedicated safety PLCs remain mandatory. The reason isn't performance; it's provability:

| Requirement | Safety PLC (Pilz, Siemens F-CPU) | PREEMPT_RT + ROS2 |
|-------------|----------------------------------|-------------------|
| Deterministic I/O scan | Hardware-guaranteed, < 1 us | Software-bounded, ~20-100 us |
| Hardware watchdog | Independent of CPU, triggers fail-safe on overrun | Depends on software cooperation |
| Power-failure resilience | Battery-backed state, deterministic resume | Filesystem corruption possible |
| Formal safety certification | Decades of SIL-2/SIL-3 certified products | No integrated product certification yet |
| Dual-channel redundancy | Built into F-CPU architecture | Must be designed at application level |

### The Breakthrough Progress (2024-2025)

- **PREEMPT_RT merged into mainline** (kernel 6.12, September 2024) — eliminates the 20-year maintenance burden of out-of-tree patches, making it viable for long-lifecycle industrial products.
- **Codethink CTRL OS** (May 2025) — first Linux-based OS with a SIL-3/ASIL-D baseline safety assessment validated by exida. This is a *pathfinder*, not a product cert, but it demonstrates the methodology exists.
- **CODESYS Virtual Control SL** (June 2024) — IEC 61508 SIL-3 certified soft PLC runtime on generic Linux hardware. Not ROS2, but proves Linux + soft PLC can achieve SIL-3.
- **ELISA Project** (Linux Foundation) — building tools and processes for certifying Linux in safety-critical applications. No concrete SIL milestone yet, but active working groups through 2026.

### The Emerging Hybrid: Soft PLC + ROS2 on One Box

The industry isn't choosing between PLC and ROS2 — it's converging them onto shared hardware:

```
HYBRID ARCHITECTURE (e.g., ctrlX CORE, TwinCAT on Linux)
================================================================

  ┌──────────────────────────────────────────────────────────┐
  │  Single Industrial PC / Edge Controller                   │
  │                                                          │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
  │  │  Safety PLC   │  │  Soft PLC    │  │  ROS2        │   │
  │  │  (SIL-rated,  │  │  (IEC 61131, │  │  (AI, SLAM,  │   │
  │  │   certified   │  │   real-time  │  │   planning,  │   │
  │  │   runtime)    │  │   control)   │  │   vision)    │   │
  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
  │         │                 │                  │           │
  │         │    Shared memory / Datalayer       │           │
  │         └─────────────────┼──────────────────┘           │
  │                           │                              │
  └───────────────────────────┼──────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Fieldbus (Ether-│
                    │  CAT / PROFINET) │
                    │  → Drives, I/O   │
                    └──────────────────┘

  Safety PLC handles certified safety functions.
  Soft PLC handles deterministic motion control.
  ROS2 handles intelligence. All on one box.
```

This is the architecture Bosch ctrlX CORE, Beckhoff TwinCAT on Linux, and Phoenix Contact PLCnext are converging toward. The PLC isn't eliminated — it's virtualized and colocated with ROS2.

</details>

<details>
<summary><strong>Concrete Example</strong> — Panasonic AMR with ADLINK ROS2 + EtherCAT</summary>

Panasonic developed an Autonomous Mobile Robot (AMR) using ADLINK's ROScube platform, replacing the traditional architecture of separate PLC + separate ROS2 PC with a single integrated controller.

### Traditional AMR Architecture (What They Replaced)

```
BEFORE: Three separate controllers
================================================================

  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
  │  Linux PC   │    │  Motor       │    │  Safety PLC     │
  │  (ROS2)     │    │  Controller  │    │  (E-stop,       │
  │             │    │  (EtherCAT   │    │   bumper)       │
  │  - SLAM     │    │   master)    │    │                 │
  │  - Nav2     │    │             │    │                 │
  │  - Fleet    │    │  - Servo    │    │                 │
  │    mgmt     │    │    loops    │    │                 │
  └──────┬──────┘    └──────┬──────┘    └────────┬────────┘
         │                  │                     │
         └──── Ethernet ────┴──── Safety bus ─────┘

  Cost: 3 controllers + 2 communication bridges
  Development time: 6+ months
  Integration complexity: high
```

### New Architecture (ROS2 + Software-Defined EtherCAT)

```
AFTER: Single ROScube controller
================================================================

  ┌──────────────────────────────────────────────────────────┐
  │  ADLINK ROScube (PREEMPT_RT Linux)                       │
  │                                                          │
  │  ros2_control stack:                                     │
  │   ┌───────────────┐    ┌────────────────────────────┐    │
  │   │ Nav2 + SLAM   │    │ EtherCAT hardware interface│    │
  │   │ (non-RT)      │    │ (RT, SCHED_FIFO)           │    │
  │   │               │    │                            │    │
  │   │ Publishes     │    │ 1 kHz servo loop:          │    │
  │   │ /cmd_vel      │──>│  - Read motor encoders     │    │
  │   │               │    │  - Compute PD torque       │    │
  │   │               │    │  - Write drive commands    │    │
  │   └───────────────┘    └─────────────┬──────────────┘    │
  │                                      │                   │
  └──────────────────────────────────────┼───────────────────┘
                                         │
                                         ▼
                               ┌──────────────────┐
                               │  EtherCAT bus     │
                               │  → Wheel drives   │
                               │  → Lidar          │
                               │  → Safety I/O     │
                               └──────────────────┘

  Cost: 1 controller (30% reduction)
  Development time: 2 months
  Integration: ROS2 topics connect everything natively
```

### What Changed

| Aspect | Before (3 controllers) | After (ROScube) |
|--------|----------------------|-----------------|
| Hardware cost | 3 separate units + cabling | 1 unit |
| Development time | 6+ months | 2 months |
| Motor control | Separate EtherCAT master box | `ethercat_driver_ros2` in ros2_control |
| SLAM → motor path | Ethernet bridge, format conversion | ROS2 topic (`/cmd_vel`) directly |
| Software stack | 3 toolchains (ROS2, vendor motor IDE, PLC IDE) | 1 toolchain (ROS2) |
| Simulation | Separate sim for each subsystem | Single Gazebo sim for entire robot |

### Other Production Deployments

- **Audi e-tron GT plant** (announced March 2025, commissioning underway) — Virtual PLCs (Siemens S7-1500V in Docker containers) replace floor-level hardware PLCs for body-shop welding at Bollinger Hofe, Neckarsulm. TUV-certified safety. Plans to expand across the facility.
- **PAL Robotics TALOS humanoid** — ros_control/ros2_control running at up to 2000 Hz for whole-body locomotion. PAL has used ros_control in production humanoids since ~2013, with ongoing migration to ros2_control.
- **b-robotized GmbH** — Production deployments using ros2_control with EtherCAT, CANopen, and Modbus, presented at ROS-Industrial Conference 2025.
- **Volvo Trucks** — Collaborative robot assembly at engine manufacturing in Skovde, Sweden, using ROS/ROS2 with a "Sequence Planner" bridging high-level route planning to low-level motion control.

**The one thing most outsiders get wrong about this is...** thinking you need to choose between PLC and ROS2. The winning architecture in 2025-2026 is both on one box: a soft PLC runtime handles deterministic control and safety (in IEC 61131-3 languages the plant electrician can maintain), while ROS2 handles perception, planning, and AI (in Python/C++ the robotics engineer prefers). They share data through shared memory, not a network bridge. The question isn't "can ROS2 replace PLCs?" — it's "can they run on the same hardware?" And the answer is increasingly yes.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/preempt-rt]]** — The kernel patches that make this possible. Covers PREEMPT_RT's mechanism (threaded interrupts, preemptible spinlocks, priority inheritance), cyclictest benchmarking, and the fundamental limitations vs. dual-kernel approaches like Xenomai.
- **[[quick-context/plc-vs-software-control]]** — The traditional architecture this topic is disrupting. Details the PLC/software responsibility split, OPC-UA bridging, and why the "PLC does motion, software does planning" pattern exists.
- **[[quick-context/plc-vs-software]]** — Why PLCs exist in the first place: deterministic scan cycles, fail-safe behavior, ladder logic. Essential context for understanding what "replacing a PLC" actually means.
- **[[quick-context/sil-rated-safety-functions]]** — The certification framework (IEC 61508, SIL 1-4) that remains the last hard barrier to full PLC replacement. Covers PFD calculations, dual-channel architectures, and why safety certification requires more than good code.
- **[[quick-context/ros2-architecture]]** — The ROS2 middleware (nodes, topics, DDS) that provides the software framework. The `ros2_control` subsystem described here is the specific ROS2 component that enables real-time hardware interfacing.
- **[[quick-context/isa-95-levels]]** — Where this fits in the automation hierarchy: PREEMPT_RT + ROS2 targets [[quick-context/isa-95-levels|ISA-95 Levels]] 1-2 (sensing/control), while also reaching up to Level 3 (MES integration via ROS2's networking capabilities).
- **[[quick-context/robotic-arm-api-levels]]** — The API stack from high-level planning to raw servo control. PREEMPT_RT + ROS2 platforms like ctrlX CORE span multiple levels of this stack on a single device.
- **CODESYS Virtual Control SL** — IEC 61508 SIL-3 certified soft PLC on Linux (June 2024). Proves the soft PLC + Linux model can achieve safety certification, though it's a proprietary runtime, not ROS2.
- **EtherCAT** — The dominant real-time industrial fieldbus. Direct ROS2 integration (via `ethercat_driver_ros2` or ADLINK's software-defined EtherCAT) is the key enabler that lets ROS2 talk to servo drives without a PLC intermediary.
- **Xenomai** — Dual-kernel alternative to PREEMPT_RT offering lower worst-case latencies. Still used where sub-10 us jitter is required, but PREEMPT_RT's mainline merge makes it the preferred choice for most new designs.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** PREEMPT_RT achieves worst-case jitter of +/- 4 us at a 1 ms cycle with EtherCAT. A typical PLC achieves < 1 us. Does this gap matter for most industrial robot control?

<details>
<summary>Answer</summary>

No. Industrial robots typically require timing jitter under 200 us for a 1 ms control cycle. PREEMPT_RT's +/- 4 us is 50x better than this requirement. The gap only matters for extremely high-precision applications like multi-axis CNC interpolation at very high feed rates, or semiconductor lithography — not for typical robotic arm or AMR control. For the vast majority of industrial automation, PREEMPT_RT's timing is more than adequate.
</details>

**Q2:** Audi runs virtual PLCs in Docker containers at their e-tron GT plant. Why Docker containers for PLC runtime instead of bare-metal Linux processes?

<details>
<summary>Answer</summary>

Containerization enables several things that traditional PLCs can't do: (1) multiple independent PLC instances on shared server infrastructure, reducing per-station hardware costs, (2) rapid deployment and rollback — a new PLC program is a container image push, not a [[quick-context/firmware|firmware]] flash, (3) centralized management — IT teams manage PLC infrastructure with the same tools they use for other services, (4) resource isolation — one PLC instance crashing doesn't affect others. The real-time scheduling still happens at the kernel level (PREEMPT_RT), so containerization doesn't compromise timing. Audi's system is TUV-certified, validating that the container approach meets safety requirements.
</details>

**Q3:** The Panasonic AMR replaced 3 separate controllers with 1 ROScube. What happens to the safety PLC functions (e-stop, bumper) in this architecture?

<details>
<summary>Answer</summary>

Safety I/O (e-stop buttons, safety bumpers) connects to safety-rated EtherCAT modules on the fieldbus. The safety logic still runs in a certified safety runtime — either a dedicated safety module on the EtherCAT bus (like a Pilz safety module) or a soft safety PLC partition on the ROScube. The key point: safety functions are not handled by ROS2 nodes. They run in an isolated, certified domain that can halt the robot independently of whatever the ROS2 stack is doing. Eliminating the separate motor controller doesn't mean eliminating safety certification — it means relocating where the safety logic executes.
</details>

**Q4:** A startup claims their PREEMPT_RT + ROS2 system "replaces PLCs entirely" for a pharmaceutical filling line. What critical gap should you flag?

<details>
<summary>Answer</summary>

Pharmaceutical manufacturing is heavily regulated (FDA 21 CFR Part 11, EU GMP Annex 11). Filling lines handling sterile products require SIL-2 or SIL-3 rated safety functions for dose accuracy, contamination prevention, and operator protection. No PREEMPT_RT + ROS2 stack has SIL-2/SIL-3 certification as an integrated system. The Codethink CTRL OS baseline assessment (May 2025) is a pathfinder, not a product cert. CODESYS has SIL-3 on Linux, but that's a proprietary runtime, not ROS2. A safety auditor in pharma would reject the system for safety-critical functions. The startup would still need dedicated safety PLCs for interlocks and safety I/O, making the claim of "entirely" replacing PLCs misleading. See: "The Key Tension" section.
</details>

**Q5:** The Pupper v3 uses an [[micro-context/stm32-microcontroller|STM32 microcontroller]] for 1 kHz motor control and a Raspberry Pi for ROS2. If PREEMPT_RT + ROS2 can run servo loops at 1 kHz on a single platform, why does the Pupper still use this dual-processor architecture?

<details>
<summary>Answer</summary>

Several reasons: (1) The Pupper is a teaching platform designed before PREEMPT_RT's mainline merge — the dual architecture is a pragmatic design choice, not a fundamental requirement. (2) The Raspberry Pi's ARM SoC doesn't have the same real-time guarantees as a purpose-built industrial controller (ROScube, ctrlX CORE); even with PREEMPT_RT, SD card I/O and GPU thermal throttling can cause latency spikes. (3) The STM32 provides bare-metal [[quick-context/can-bus|CAN bus]] communication with 12 servos — handling the electrical-level protocol is simpler and more reliable on a dedicated [[micro-context/microcontroller|microcontroller]] than through Linux kernel drivers. (4) Cost: the dual STM32 + Pi architecture is cheaper for a student robot than an industrial PREEMPT_RT controller. However, if you were building a production Pupper, a single PREEMPT_RT platform with EtherCAT servos could absolutely collapse the architecture — exactly what PAL Robotics does with their production humanoids running ros2_control at 2000 Hz.
</details>

</details>
