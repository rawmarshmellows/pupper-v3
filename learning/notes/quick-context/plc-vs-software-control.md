---
topic: PLC vs Software Control for Robotic Arms
created: 2026-01-16
---

> **Related:** [[quick-context/plc-vs-software|PLC and why it's different to software and how it's implemented]] | [[quick-context/preempt-rt|PREEMPT_RT]] | [[quick-context/robotic-arm-api-levels|Different Levels of APIs for Controlling Robotic Arms]] | [[quick-context/sil-rated-safety-functions|SIL-Rated Safety Functions]] | [[quick-context/preempt-rt-ros2-plc-replacement|PREEMPT_RT + ROS2 as PLC Replacement]]

> **TL;DR:** PLCs handle deterministic real-time motion and safety, while software handles complex planning and intelligence - modern robotic systems need both working together.

# PLC vs Software Control in Robotic Arm Systems

## The Core Problem: Who Executes the Motion Control Loop?

The robotic arm API stack described in [[quick-context/robotic-arm-api-levels]] glosses over a critical architectural question: who actually executes the motion control loop? For PLC fundamentals (scan cycle, ladder logic, fail-safe behavior, and why PLCs exist), see [[quick-context/plc-vs-software]]. This article focuses on how modern robotic systems split work between PLC hardware and software.

The problem is that manufacturing demands both: PLCs excel at discrete I/O coordination (conveyors, safety interlocks, sequencing) but are terrible at complex math and high-level logic, while software excels at trajectory planning and integration but can't guarantee hard real-time response. If you put motion control in software without real-time guarantees, a garbage collection pause or kernel interrupt causes the arm to jerk or fault. If you try to do everything in the PLC, you end up writing inverse kinematics in Structured Text and praying.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Scan Cycle** | See [[quick-context/plc-vs-software]] — the PLC's deterministic read-execute-write loop (1–10ms for motion, 10–50ms for discrete I/O). |
| **Structured Text (ST)** | The IEC 61131-3 programming language that looks like Pascal and runs on PLCs—the closest thing to "real programming" in PLC-land. |
| **[[quick-context/preempt-rt|PREEMPT_RT]]** | A Linux kernel patch that makes the kernel preemptible, enabling soft real-time performance—the bridge that lets software pretend to be a PLC. |
| **Soft PLC** | Software that implements PLC runtime semantics on commodity hardware (Beckhoff TwinCAT, CODESYS)—looks like a PLC to the plant, runs on a PC. |
| **Fieldbus** | The industrial network (PROFINET, EtherNet/IP, EtherCAT) connecting PLCs to I/O, drives, and robots—the nervous system of the automation cell. |

<details>
<summary><strong>How It Works</strong></summary>

Here's how a real system divides responsibility between a Siemens S7-1500 PLC and a ROS2-based vision/planning system:

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│  Linux IPC (ROS2)                                           │
│  ├── Camera driver (30 fps)                                 │
│  ├── Object detection (ML model)                            │
│  ├── Pick pose computation                                  │
│  └── MoveIt trajectory planning                             │
│           │                                                 │
│           │ Trajectory waypoints via OPC-UA                 │
│           ▼                                                 │
├─────────────────────────────────────────────────────────────┤
│  Siemens S7-1500 PLC (2ms scan)                             │
│  ├── Safety monitoring (E-stop, light curtains)             │
│  ├── Conveyor control (start/stop/speed)                    │
│  ├── Robot motion execution (interpolated waypoints)        │
│  └── Gripper I/O, sensor interlocks                         │
│           │                                                 │
│           │ PROFINET IRT (250μs cycle)                      │
│           ▼                                                 │
│  Servo Drives + Robot                                       │
└─────────────────────────────────────────────────────────────┘
```

**PLC Side (Structured Text) - Receiving and executing trajectory:**
```iecst
// S7-1500: Receive waypoints from ROS, execute with interpolation
PROGRAM ExecuteTrajectory
VAR
    waypoints : ARRAY[0..99] OF RobotPose;  // from OPC-UA
    currentIdx : INT := 0;
    interpFactor : REAL := 0.0;
    cmdPose : RobotPose;
END_VAR

// 2ms scan cycle - interpolate between waypoints
IF trajectoryActive THEN
    interpFactor := interpFactor + 0.02;  // 50ms between waypoints
    IF interpFactor >= 1.0 THEN
        currentIdx := currentIdx + 1;
        interpFactor := 0.0;
    END_IF;

    // Linear interpolation - PLC handles the real-time part
    cmdPose := Interpolate(waypoints[currentIdx],
                           waypoints[currentIdx + 1],
                           interpFactor);

    // Safety check runs EVERY scan - non-negotiable
    IF SafetyOK() THEN
        DriveOutputs := PoseToJoints(cmdPose);
    ELSE
        DriveOutputs := HOLD_POSITION;
        trajectoryActive := FALSE;
    END_IF;
END_IF;
```

**Software Side (ROS2 Python) - Computing and sending trajectory:**
```python
# ROS2 node: compute trajectory, hand off to PLC for execution
class TrajectoryPlanner(Node):
    def __init__(self):
        super().__init__('trajectory_planner')
        self.opcua_client = Client("opc.tcp://plc-ip:4840")
        self.moveit = MoveGroupInterface("manipulator")

    def pick_object(self, detected_pose: Pose):
        # This part is NOT real-time - we're just planning
        pick_trajectory = self.moveit.plan(detected_pose)

        if pick_trajectory.success:
            # Convert to simple waypoint list PLC can consume
            waypoints = self.downsample_trajectory(pick_trajectory, hz=20)

            # Hand off to PLC - it handles the hard real-time execution
            self.opcua_client.write("ns=2;s=Robot.Waypoints", waypoints)
            self.opcua_client.write("ns=2;s=Robot.StartTrajectory", True)

            # PLC takes over here - we just monitor
            while not self.opcua_client.read("ns=2;s=Robot.TrajectoryComplete"):
                time.sleep(0.05)  # Non-RT polling is fine
```

The key insight: ROS does the smart stuff (vision, planning) on commodity hardware without real-time constraints, then throws a simplified trajectory over the fence to the PLC which handles the microsecond-level servo control and safety monitoring. Neither system could do the other's job well.

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The fundamental argument is **determinism vs. capability**. PLC vendors (Siemens, Rockwell, Beckhoff) have spent decades building certified, safety-rated, industrially-hardened systems with SIL-rated emergency stop handling and 20-year part availability. Software ecosystems (ROS, custom stacks) offer modern programming paradigms, rich libraries, machine learning integration, and escape from vendor lock-in—but achieving hard real-time in software requires specialized kernels (PREEMPT_RT, Xenomai), careful architecture, and loses most safety certifications.

The industry is slowly converging: Beckhoff's TwinCAT runs PLC runtime on Windows with a real-time hypervisor, ROS2 added deterministic DDS transports, and "soft PLCs" blur the line entirely. But in regulated industries (automotive, pharma, food), auditors still want to see traditional PLC programs for anything safety-related, regardless of technical capability.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

The architecture diagram above shows a real-world split: the Linux IPC running ROS2 handles vision processing at 30fps, ML-based object detection, and MoveIt trajectory planning. None of this needs real-time guarantees. The computed trajectory waypoints are sent via OPC-UA to the Siemens S7-1500 PLC, which runs a 2ms scan cycle handling safety monitoring, conveyor control, and the actual motion interpolation. The PLC then commands servo drives over PROFINET IRT at 250 microsecond cycles.

This division means: software does the "thinking" (where to move, what to pick up), PLC does the "doing" (actually moving safely and precisely). The PLC code is deliberately simple—interpolate waypoints, check safety every scan, command drives. The software code can be arbitrarily complex without risking motion quality.

**The one thing most outsiders get wrong about this is...** thinking the PLC is "dumb" legacy tech being replaced by software. The PLC isn't handling motion because engineers don't know Python—it's there because when the light curtain trips, the arm must stop within 50ms regardless of what your ML model is doing. The "dumb" scan cycle that runs the same 2000 lines of ladder logic forever is a feature, not a bug. Software replaces the PLC for flexibility; it doesn't replace it for reliability.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/robotic-arm-api-levels]]** - The full API stack from high-level task planning down to servo control
- **[[quick-context/preempt-rt]]** - The Linux kernel patch that enables soft real-time, bridging the gap between software and PLC
- **[[quick-context/preempt-rt-ros2-plc-replacement]]** — The emerging hardware platforms (Bosch ctrlX, ADLINK ROScube, Beckhoff TwinCAT on Linux) that collapse the PLC/software split onto a single PREEMPT_RT + ROS2 device
- **[[quick-context/plc-vs-software]]** - Deeper dive into PLC architecture and why it differs fundamentally from software
- **[[quick-context/sil-rated-safety-functions]]** - Why safety-critical functions still require certified hardware

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why can't you just run trajectory interpolation in a ROS2 node with a 1ms timer callback?
<details>
<summary>Answer</summary>
Because Linux (without PREEMPT_RT) provides no guarantees about when your callback will actually run. A garbage collection pause, kernel interrupt, or disk I/O could delay your "1ms" callback by 10-50ms, causing the robot arm to jerk, overshoot, or fault the servo drive. The PLC's scan cycle is deterministic—it runs every 2ms regardless of what else is happening.
</details>

**Q2:** If PREEMPT_RT gives Linux soft real-time capabilities, why not move everything to software?
<details>
<summary>Answer</summary>
Two reasons: (1) PREEMPT_RT provides bounded latency (~50-100μs worst case), not the sub-microsecond determinism of dedicated hardware—fine for 1ms loops but not for [[quick-context/sil-rated-safety-functions|SIL-rated safety functions]]. (2) Safety certifications (SIL, PLe) require certified hardware and auditable, simple code. Even if your software is technically capable, regulators in automotive, pharma, and food industries won't accept it for safety-critical functions.
</details>

**Q3:** What's the role of OPC-UA in this architecture?
<details>
<summary>Answer</summary>
OPC-UA serves as the bridge between the non-real-time software world and the real-time PLC world. It's an industry-standard protocol for exchanging data (like trajectory waypoints) between systems. The software side writes waypoints to OPC-UA variables; the PLC reads them and executes. OPC-UA itself isn't real-time, but it doesn't need to be—it just transfers the plan, not the execution.
</details>

**Q4:** What is a "Soft PLC" and why is it blurring the line between PLC and software control?
<details>
<summary>Answer</summary>
A Soft PLC (like Beckhoff TwinCAT or CODESYS) implements PLC runtime semantics on commodity PC hardware, often using a real-time hypervisor to guarantee scan cycle timing. To the plant floor, it looks like a PLC (same programming languages, same I/O interfaces); to IT, it's a Windows or Linux PC. This enables running PLC logic and high-level software on the same hardware, reducing integration complexity—though safety certification remains more challenging than traditional PLCs.
</details>

**Q5:** Why do regulated industries (pharma, automotive, food) still insist on traditional PLCs for safety functions despite software capabilities?
<details>
<summary>Answer</summary>
Safety certifications (SIL, PLe) require auditable, deterministic systems with proven track records. Traditional PLCs have decades of certification history, simple architectures that auditors understand, and guaranteed long-term part availability. Software-based safety requires proving the entire stack (OS, runtime, application) meets certification requirements—possible but expensive and scrutinized heavily. The regulatory burden, not technical capability, drives the choice.
</details>

</details>
