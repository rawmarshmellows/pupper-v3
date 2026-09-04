---
topic: Different Levels of APIs for Controlling Robotic Arms
created: 2026-01-16
---

> **Related:** [[learning/notes/micro-context/plc-programmable-logic-controller]] | [[learning/notes/quick-context/pcb-assembly-files-bom-cpl]]

> **TL;DR:** Robotic arm APIs exist at multiple abstraction levels from raw servo control (1kHz real-time) to high-level task planners, with each level trading control granularity for ease of use.

# Robotic Arm API Levels in Manufacturing

## The Core Problem: Bridging Human Intent to Motor Commands

Robotic arms are fundamentally dumb servo motors arranged in a kinematic chain. Without layered abstractions, every programmer would need to solve inverse kinematics (translating "move the gripper here" into "rotate joint 3 by 47.2 degrees"), handle trajectory planning to avoid collisions, manage real-time motion timing at millisecond precision, and coordinate with sensors and other machines.

The abstraction layers exist because manufacturing needs both determinism (a welding robot must follow the exact same path every cycle) and flexibility (reprogramming for a new product shouldn't require a PhD in control theory). Without these layers, you'd either have unmaintainable low-level code or be locked into vendor-specific high-level tools with no escape hatch.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Inverse Kinematics (IK)** | Math that converts a desired end-effector pose (position + orientation) into the joint angles needed to achieve it—the fundamental translation between "where" and "how." |
| **Teach Pendant** | The handheld device operators use to manually jog the robot and record waypoints; the "no-code" interface to industrial arms. |
| **Motion Primitive** | A reusable building block (linear move, circular arc, spline) that the motion planner stitches together into complete trajectories. |
| **Real-Time Bus** | The deterministic communication layer (EtherCAT, PROFINET IRT, Sercos) that guarantees joint commands arrive within microseconds—lose this timing and the arm stutters or faults. |
| **MoveGroup** | In ROS/MoveIt, the logical grouping of joints that move together (e.g., "arm" vs. "gripper"), the unit of motion planning. |

<details>
<summary><strong>How It Works</strong></summary>

The API stack for robotic arms typically has three main levels:

**Level 1: Vendor High-Level Scripts**
- Languages like KUKA KRL, Fanuc TP, ABB RAPID
- Teach pendant programmable
- Motion primitives like PTP (point-to-point), LIN (linear), CIRC (circular)
- Vendor handles IK, trajectory generation, and safety
- Limited customization but fast deployment

**Level 2: Middleware Abstraction (ROS/MoveIt)**
- Language-agnostic (Python, C++)
- Automatic collision checking and motion planning
- IK solved by configurable solvers
- Works across robot brands with driver plugins
- Higher latency, less deterministic than Level 1

**Level 3: Direct Servo Control**
- Raw joint position/velocity/torque commands
- Real-time loop at 1kHz or faster
- You implement IK, trajectory generation, safety
- Maximum control, maximum responsibility
- Requires EtherCAT, Sercos, or similar real-time bus

Most production systems use multiple levels: high-level for task sequencing, dropping to lower levels for critical timing or custom motion profiles.

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The central tradeoff is **abstraction vs. control latency**.

High-level APIs (like ROS MoveIt or vendor teach pendants) let you say "pick up the widget" but introduce planning latency and hide timing guarantees. Low-level APIs give you direct joint control at 1kHz+ but require you to handle everything—singularities, velocity limits, emergency stops.

Practitioners argue endlessly about where to draw the line: integrators want high-level abstractions for faster deployment, while controls engineers want deterministic real-time access for precision applications like surgical robots or high-speed [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|pick-and-place]].

The rise of "real-time capable" middleware (EtherCAT, ROS2 with DDS) is an attempt to have both, but the impedance mismatch between IT-style APIs and OT-style timing requirements remains a constant source of pain.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Here's what the same "pick and place" operation looks like at different abstraction levels:

**Level 1: Vendor High-Level Script (KUKA KRL)**
```krl
; KUKA Robot Language - pendant-programmable
DEF PickAndPlace()
  PTP Home  ; point-to-point move to home
  LIN PickApproach ; linear move above part
  LIN PickPose ; descend to part
  GripperClose()
  LIN PickApproach ; retract
  LIN PlaceApproach
  LIN PlacePose
  GripperOpen()
  PTP Home
END
```

**Level 2: ROS MoveIt (Python) - Middleware Abstraction**
```python
import moveit_commander

arm = moveit_commander.MoveGroupCommander("manipulator")
gripper = moveit_commander.MoveGroupCommander("gripper")

# Cartesian pose target - MoveIt handles IK + collision checking
pick_pose = Pose(position=Point(0.5, 0.2, 0.1), orientation=...)
arm.set_pose_target(pick_pose)
arm.go(wait=True)  # blocking call, planner runs internally

gripper.set_named_target("closed")
gripper.go(wait=True)

place_pose = Pose(position=Point(0.5, -0.2, 0.1), orientation=...)
arm.set_pose_target(place_pose)
arm.go(wait=True)
```

**Level 3: Direct Joint Control (EtherCAT via SOEM)**
```c
// Real-time loop running at 1kHz - you own everything
void realtime_loop() {
    ec_send_processdata();  // send joint commands over EtherCAT
    ec_receive_processdata();

    for (int j = 0; j < 6; j++) {
        // Raw position command in encoder counts
        // YOU computed these via your own IK + trajectory generator
        slave[j].outputs->target_position = trajectory[cycle][j];

        // Check following error - no safety net
        if (abs(slave[j].inputs->actual_position - trajectory[cycle][j]) > MAX_ERROR) {
            emergency_stop();
        }
    }
    cycle++;
}
```

**The one thing most outsiders get wrong about this is...** assuming these API levels are cleanly separated like a web stack. In practice, they're deeply intertwined—a "high-level" vendor script might need inline low-level overrides for timing-critical sections, and "low-level" EtherCAT applications still rely on vendor-specific motion kernels running on the drive itself. The real skill isn't picking a level, it's knowing when to punch through the abstraction.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/epson-rc-plus-programming]]** - Specific example of a vendor high-level API for SCARA robots
- **[[quick-context/robot-cell-integration-best-practices]]** - How robots at any API level integrate with the broader manufacturing cell
- **[[quick-context/plc-vs-software-control]]** - The [[learning/notes/micro-context/plc-programmable-logic-controller|PLC]] side of the robot-to-cell coordination problem
- **[[quick-context/preempt-rt]]** - Linux real-time extensions for running Level 3 control on commodity hardware

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What problem does inverse kinematics solve?
<details>
<summary>Answer</summary>
Inverse kinematics converts a desired end-effector pose (position and orientation in Cartesian space) into the joint angles required to achieve that pose. It answers "what joint values put the gripper at this location?"
</details>

**Q2:** Why would you choose Level 3 (direct servo control) over Level 1 (vendor scripts)?
<details>
<summary>Answer</summary>
Level 3 gives maximum control over timing and behavior, essential for applications requiring custom motion profiles, sub-millisecond coordination, or integration with non-standard sensors. Examples include surgical robots, high-speed pick-and-place, or research platforms where you need to implement novel control algorithms.
</details>

**Q3:** What is a "real-time bus" and why does it matter for robotic arms?
<details>
<summary>Answer</summary>
A real-time bus (EtherCAT, PROFINET IRT, Sercos) is a deterministic communication layer that guarantees joint commands arrive within microseconds. Without this timing guarantee, the arm would stutter, overshoot, or fault because commands arrive too late for the servo control loop.
</details>

**Q4:** Why might a production system use multiple API levels simultaneously?
<details>
<summary>Answer</summary>
High-level APIs handle task sequencing and general motion efficiently, while low-level access is needed for timing-critical operations or custom motion profiles. For example, a cell might use ROS for task planning but drop to direct servo control for a precision assembly step.
</details>

**Q5:** What is the main tradeoff when choosing higher abstraction levels?
<details>
<summary>Answer</summary>
Higher abstraction levels are easier to program and faster to deploy, but they introduce planning latency and hide timing guarantees. You lose fine-grained control over exactly when and how motion occurs, which matters for precision or high-speed applications.
</details>

</details>
