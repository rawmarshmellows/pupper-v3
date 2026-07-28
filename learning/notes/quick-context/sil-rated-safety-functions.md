---
topic: SIL-Rated Safety Functions
created: 2026-01-17
---

> **Related:** [[quick-context/preempt-rt]] | [[micro-context/plc-programmable-logic-controller]] | [[quick-context/plc-vs-software-control]]

> **TL;DR:** Safety Integrity Levels (SIL 1-4) quantify how reliably a safety function will prevent harm when demanded, requiring redundant hardware, certified components, and rigorous process—not just careful code.

# SIL-Rated Safety Functions

## The Core Problem

Industrial machinery can maim and kill. A robotic arm moving at speed has the kinetic energy to crush a skull; a valve failing open can cause a chemical release; a conveyor that doesn't stop when someone falls on it will drag them into a pinch point.

**Safety Integrity Level (SIL)** is a quantified measure of how reliably a safety function will work when demanded—not "will this code crash?" but "what's the probability this emergency stop fails to stop the machine before the operator dies?"

The IEC 61508 standard defines four levels (SIL 1-4), each representing an order of magnitude improvement in reliability. SIL 1 requires a probability of failure on demand (PFD) of 10^-1 to 10^-2, meaning the safety function can fail once in 10-100 demands. SIL 3 requires 10^-3 to 10^-4—fail once in 1,000-10,000 demands.

Without this framework, there's no way to systematically design, verify, and certify that a safety system is actually safe. Engineers would just write code and hope; regulators would have no basis to approve equipment; and when failures occurred, there'd be no way to determine if the design was negligent or merely unlucky.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **PFD (Probability of Failure on Demand)** | The likelihood the safety function fails to act when triggered—SIL levels are defined by PFD ranges (SIL 3 = 10^-4 to 10^-3). |
| **Safe Failure Fraction (SFF)** | The proportion of failures that leave the system in a safe state (e.g., valve fails closed)—higher SFF allows higher SIL with less redundancy. |
| **Dual-Channel Architecture (1oo2)** | Two independent systems that must both agree to allow operation; either can independently trigger shutdown—the standard pattern for SIL 2/3. |
| **Diagnostic Coverage (DC)** | The percentage of dangerous failures detectable by automatic diagnostics—higher DC reduces the "undetected dangerous failure" rate that drives PFD. |
| **Safety PLC** | A PLC certified to execute safety functions (Siemens F-CPU, Allen-Bradley GuardLogix, Pilz)—internally redundant with self-monitoring, certified to IEC 61508. |

<details>
<summary><strong>How It Works</strong></summary>

SIL certification requires proving statistical reliability of the entire hardware/software/human system against specific failure modes:

```
                        SIL CERTIFICATION COMPONENTS
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │   ┌───────────────┐    ┌───────────────┐    ┌───────────┐  │
    │   │   Hardware    │    │   Software    │    │  Process  │  │
    │   │  Architecture │    │   Lifecycle   │    │   Rigor   │  │
    │   └───────┬───────┘    └───────┬───────┘    └─────┬─────┘  │
    │           │                    │                  │        │
    │           v                    v                  v        │
    │   ┌─────────────────────────────────────────────────────┐  │
    │   │              PFD Calculation (Target SIL)           │  │
    │   │   SIL 1: 10^-1 to 10^-2  (1 in 10-100 demands)      │  │
    │   │   SIL 2: 10^-2 to 10^-3  (1 in 100-1,000 demands)   │  │
    │   │   SIL 3: 10^-3 to 10^-4  (1 in 1,000-10,000 demands)│  │
    │   │   SIL 4: 10^-4 to 10^-5  (1 in 10,000-100,000)      │  │
    │   └─────────────────────────────────────────────────────┘  │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘

           REDUNDANCY ARCHITECTURES (Hardware Fault Tolerance)

    1oo1 (Single Channel)          1oo2 (Dual Channel - Either Trips)
    ┌─────────┐                    ┌─────────┐
    │ Sensor  │───> Output         │Sensor A │───┐
    └─────────┘                    └─────────┘   │  OR  ───> Safe Output
                                   ┌─────────┐   │      (Either can stop)
                                   │Sensor B │───┘
                                   └─────────┘

    2oo3 (Triple Modular - Majority Voting)
    ┌─────────┐
    │Sensor A │───┐
    └─────────┘   │
    ┌─────────┐   │  VOTING  ───> Output
    │Sensor B │───┤  (2 of 3)     (Tolerates 1 failure)
    └─────────┘   │
    ┌─────────┐   │
    │Sensor C │───┘
    └─────────┘
```

1. **Hardware Architecture**: Redundancy patterns (1oo1, 1oo2, 2oo3) determine base failure rates
2. **Diagnostic Coverage**: Self-testing detects failures before they're demanded
3. **Safe Failure Fraction**: Failures should fail-safe, not fail-dangerous
4. **Process Rigor**: Formal requirements, design reviews, testing, and change control throughout lifecycle

The PFD calculation aggregates all failure rates and diagnostic coverages to prove the system achieves the target SIL level. This data comes from component manufacturers' "safety manuals" with certified MTTF (mean time to failure) values.

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The fundamental tradeoff is **safety assurance vs. development cost and flexibility**. Achieving SIL 2 or SIL 3 certification isn't about writing careful code—it's about proving, through rigorous process, that the entire lifecycle (requirements, design, implementation, testing, operation, modification) meets statistical reliability targets.

This means: redundant hardware (dual-channel sensors, cross-monitoring CPUs), diagnostic coverage calculations for every failure mode, formal methods or extensive testing to demonstrate software correctness, third-party audits, and strict change control. A SIL 3 safety PLC costs 10x a standard PLC; the engineering process costs 5-20x normal development.

Practitioners constantly argue about where to draw the safety boundary—what functions genuinely need SIL rating vs. what can be "standard" with operational controls? There's also tension between the functional safety world (IEC 61508 and sector standards like 62443 for cybersecurity, 61511 for process, 62061 for machinery) and the software world's move-fast culture. You cannot iterate your way to SIL 3; you must specify correctly upfront, because every change triggers revalidation.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## SIL 2 Light Curtain Implementation

A light curtain protects a robot cell: break the beam, robot stops. Here's what SIL 2 requires versus a naive implementation:

**Naive (Non-SIL) Approach:**
```
Light Curtain -> Single Input -> Standard PLC -> Robot Stop Command
```
Problem: Single-point failures everywhere. PLC input fails shorted? Robot doesn't stop. Output relay welds closed? Robot doesn't stop. No certification, no reliability data.

**SIL 2 Architecture:**
```
+------------------------------------------------------------------+
|   Light Curtain (Type 4, SIL 2 rated, e.g., SICK deTec4)         |
|   - Dual internal channels with cross-monitoring                  |
|   - OSSD outputs (self-testing every 50ms)                        |
|         |              |                                          |
|         v              v                                          |
|   +---------+    +---------+                                      |
|   | Input A |    | Input B |  <- Safety PLC F-CPU (dual internal) |
|   +----+----+    +----+----+                                      |
|        |              |                                           |
|        +------+-------+                                           |
|               v                                                   |
|   Safety Program: Both inputs must be TRUE to allow run           |
|               |                                                   |
|               v                                                   |
|   +---------+    +---------+                                      |
|   |Output Q1|    |Output Q2|  <- Dual safety relay channels       |
|   +----+----+    +----+----+                                      |
|        |              |                                           |
|        v              v                                           |
|   Contactor K1     Contactor K2  <- Series configuration          |
|        |              |           (either opens = robot stops)    |
|        +------+-------+                                           |
|               v                                                   |
|          Robot Drive Enable                                       |
+------------------------------------------------------------------+
```

**Safety PLC Program (Siemens F-CPU, Safety LAD):**
```
// SAFETY PROGRAM - Certified logic, change triggers re-validation
// This runs in the F-CPU's isolated safety partition

NETWORK 1: Light Curtain Dual-Channel Evaluation
      LightCurtain_A    LightCurtain_B
           |                  |
           +------------------+
           |      AND         |
           v                  v
      +-------------------------+
      |   SF_ESTOP1 Function    |  // Certified safety function block
      |   Block (SIL 2 rated)   |
      |   - Input: Both channels|
      |   - Discrepancy time:   |
      |     500ms max           |
      |   - Output: Safe state  |
      +-----------+-------------+
                  v
             Q_Robot_Safe  ->  Output to dual contactors

// Discrepancy check: if channels disagree for >500ms,
// system latches to safe state and requires manual reset
```

**Failure Mode Analysis (excerpt):**

| Failure Mode | Detection | Safe State? | Mitigation |
|--------------|-----------|-------------|------------|
| Input A wire break | Cross-check with B | Yes (stops) | - |
| Input A shorted high | Cross-check with B | Yes (discrepancy -> stop) | - |
| Both inputs shorted | OSSD self-test | Yes (curtain detects) | Certified curtain |
| Output relay welded | K1/K2 feedback monitoring | Yes (PLC detects, prevents restart) | Dual contactors |
| F-CPU CPU failure | Dual-CPU cross-check | Yes (watchdog -> safe) | Safety PLC architecture |

**The one thing most outsiders get wrong about this is...** thinking SIL is about writing better code. It's not—it's about proving statistical reliability of the entire hardware/software/human system against specific failure modes. You can have perfect code and still fail SIL certification because your sensor has insufficient diagnostic coverage, or your change management process isn't documented. Conversely, a SIL 3 system might use trivially simple logic (light curtain breaks -> motor stops) that any junior engineer could write. The complexity isn't in the algorithm; it's in the assurance case.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/plc-vs-software-control]]** - Understanding why safety functions must run on certified PLCs, not general-purpose software
- **[[quick-context/preempt-rt]]** - Real-time Linux limitations that explain why ROS2 cannot replace safety PLCs
- **[[quick-context/preempt-rt-ros2-plc-replacement]]** — The 2025-2026 push to replace PLCs with PREEMPT_RT + ROS2, and why SIL certification remains the last hard barrier (Codethink CTRL OS achieved SIL-3 baseline assessment in May 2025, but no full product cert yet)
- **[[quick-context/integration-failure-modes-solutions]]** - Non-safety failure modes where standard (non-SIL) solutions apply

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why can't you achieve SIL 3 certification through careful coding and extensive testing alone?
<details>
<summary>Answer</summary>
SIL certification requires proving statistical reliability of the entire hardware/software/human system, not just software quality. You need redundant hardware (dual-channel sensors, cross-monitoring CPUs), certified components with known failure rates (MTTF data), diagnostic coverage calculations for every failure mode, and a rigorous lifecycle process with change control. Perfect code running on non-redundant hardware with unknown failure characteristics cannot meet the PFD requirements.
</details>

**Q2:** What is the purpose of OSSD (Output Signal Switching Device) outputs on safety sensors, and how often do they self-test?
<details>
<summary>Answer</summary>
OSSD outputs are self-testing safety outputs that verify the entire signal path is functioning. They pulse the output and verify the signal propagates correctly, detecting failures like welded contacts or shorted wiring. In the light curtain example, OSSD outputs self-test every 50ms, ensuring that a failure is detected within that window rather than remaining undetected until the safety function is actually demanded.
</details>

**Q3:** Why does a SIL 2 light curtain implementation use two contactors (K1 and K2) in series rather than just one?
<details>
<summary>Answer</summary>
Series dual contactors eliminate single-point failures at the final control element. If K1 welds closed (a common failure mode), K2 can still open to stop the robot. The PLC monitors feedback from both contactors—if one fails to open when commanded, the system detects the fault and prevents restart. This redundancy is essential for achieving the PFD targets required for SIL 2.
</details>

**Q4:** What is the difference between SFF (Safe Failure Fraction) and DC (Diagnostic Coverage), and how do they both contribute to achieving a target SIL?
<details>
<summary>Answer</summary>
SFF measures what proportion of all possible failures leave the system in a safe state (e.g., a valve failing closed when closed is safe). DC measures what proportion of dangerous failures can be detected by automatic diagnostics before the safety function is demanded. Both reduce effective dangerous failure rates: high SFF means fewer failures are dangerous in the first place, while high DC means dangerous failures are caught and addressed before they matter. Together, they allow achieving higher SIL levels with less hardware redundancy.
</details>

**Q5:** Why does every change to a SIL-rated safety function trigger revalidation, and what does this mean for "iterate and improve" development approaches?
<details>
<summary>Answer</summary>
SIL certification proves that a specific configuration of hardware, software, and processes meets reliability targets. Any change—even a "minor" software fix—could introduce new failure modes, alter timing characteristics, or invalidate the statistical analysis. Revalidation ensures the modified system still meets the SIL requirements. This fundamentally conflicts with iterative development: you cannot "move fast and break things" when breaking things means someone dies. Requirements must be correct upfront, and changes must go through formal change control with full impact analysis.
</details>

</details>
