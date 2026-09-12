---
topic: EPSON RC+ Programming
created: 2026-01-16
---

> **Related:** [[learning/notes/quick-context/can-bus]] | [[learning/notes/quick-context/how-source-code-is-stored]] | [[learning/notes/quick-context/robotic-arm-api-levels]] | [[learning/notes/quick-context/making-electrolytes]] | [[learning/notes/quick-context/pcb-assembly-files-bom-cpl]]

> **TL;DR:** EPSON RC+ is the IDE and SPEL+ programming language for Epson robots, enabling motion control through commands like Go, Move, and Jump with careful tuning of speed, accuracy, and path smoothness tradeoffs.

# EPSON RC+ Programming

## The Core Problem: Translating Intent into Precise, Repeatable Motion

EPSON RC+ is the integrated development environment for programming Epson SCARA and 6-axis robots. It solves the fundamental problem of translating human intent—"pick this part, place it there, don't crash into the fixture"—into precise, repeatable motion that runs on Epson's robot controllers. Without it, you'd be stuck with teach pendants for point-by-point recording (tedious, inflexible) or trying to shoehorn generic PLCs into motion control they weren't designed for.

The IDE bundles simulation, I/O configuration, vision integration, and the SPEL+ programming language into one environment, which matters because industrial robotics lives or dies on the integration between motion planning, sensing, and cell-level logic.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **SPEL+** | Epson's BASIC-like robot programming language; not intuitive if you're expecting Python, but straightforward once you accept the syntax. |
| **Point** | A stored position (X, Y, Z, U, V, W or joint angles) that the robot moves to; points live in a point file, not inline in code. |
| **Go/Move/Jump** | The three motion commands: `Go` for joint interpolation (fastest, but unpredictable path), `Move` for linear interpolation (straight line in Cartesian space), `Jump` for pick-place arcs with Z-axis retract. |
| **Tool** | A coordinate frame offset from the robot's flange to the actual end-effector tip; get this wrong and your positions are all shifted. |
| **CP (Continuous Path)** | A mode where the robot blends through waypoints without stopping, trading positional accuracy for speed. |

<details>
<summary><strong>How It Works</strong></summary>

EPSON RC+ provides a complete workflow for robot programming:

1. **Point Teaching**: Define positions using the teach pendant or 3D simulation, storing them as point numbers (P1, P2, etc.) in a point file separate from code.

2. **Motion Programming**: Write SPEL+ code that references these points using motion commands:
   - `Go` - Joint interpolation (fastest, curved path)
   - `Move` - Linear interpolation (straight Cartesian path)
   - `Jump` - Arc motion with automatic Z-retract for pick-and-place

3. **Tool Definition**: Set coordinate frame offsets from the robot flange to the actual gripper or tool tip, ensuring positions are accurate regardless of end-effector.

4. **Motion Tuning**: Adjust Speed, Accel, and CP (Continuous Path) parameters to balance cycle time against positional accuracy.

5. **I/O Integration**: Control grippers, sensors, and external devices through digital I/O commands integrated into the motion sequence.

6. **Simulation**: Test programs in the built-in simulator before running on hardware.

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The core tension in EPSON robot programming is **cycle time vs. motion smoothness vs. positional accuracy**.

You can move fast with aggressive acceleration (Speed/Accel commands), but the robot will overshoot or vibrate at endpoints. You can hit positions exactly with `Fine` motion termination, but the robot decelerates to zero velocity at every point, killing throughput.

Practitioners spend real effort tuning `CP` (Continuous Path) motion, `Arch` parameters for pick-and-place Z-clearances, and acceleration curves to thread this needle.

The second tension is **hardcoded positions vs. computed coordinates**—novices record every point manually; experienced programmers use pallet functions, coordinate transforms, and vision offsets to make programs that adapt to fixture variation.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Here's a concrete pick-and-place example in SPEL+:

```spel
Function PickAndPlace
    ' Define tool offset for gripper (50mm Z offset from flange)
    Tool 1

    ' Set motion parameters
    Speed 80           ' 80% of max speed
    Accel 70, 70       ' Accel and decel percentages

    ' Move to approach position above pick point
    Jump P1, LimZ(50)  ' Jump to P1 with 50mm Z clearance

    ' Descend and grip
    Go P1              ' Move to exact pick position
    On gripperClose    ' Activate gripper output
    Wait 0.1           ' Dwell for gripper to close

    ' Retract and move to place
    Jump P2, LimZ(50)  ' Arc motion to place position

    ' Place the part
    Go P2
    Off gripperClose
    Wait 0.1

    ' Retract to safe position
    Jump P0            ' Return to home/safe point
Fend
```

The `Jump` command is doing the heavy lifting here—it automatically retracts in Z before moving in X/Y, then descends at the target, creating the "arch" motion that avoids dragging parts across surfaces. `P1`, `P2`, and `P0` are point numbers defined in the Point Editor, not coordinates hardcoded in the program. The `LimZ(50)` parameter overrides the default arch height to 50mm.

**The one thing most outsiders get wrong** is assuming SPEL+ programs run like sequential scripts. They're actually compiled to the controller and run in a real-time environment with multitasking—you can have background tasks monitoring sensors, a main task running motion, and trap handlers for errors, all executing concurrently. The IDE simulation looks like running code on your laptop, but the real execution model is closer to a PLC with motion coprocessors than a Python interpreter.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/quick-context/robotic-arm-api-levels]]** - Understanding where EPSON RC+ fits in the hierarchy from low-level servo control to high-level task planning
- **[[learning/notes/quick-context/robot-cell-integration-best-practices]]** - How to integrate EPSON robots with PLCs, vision systems, and other cell equipment
- **[[learning/notes/quick-context/plc-vs-software-control]]** - When to use PLC logic vs. robot-native programming for cell coordination
- **[[learning/notes/quick-context/sil-rated-safety-functions]]** - Safety considerations for industrial robot programming

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What is the difference between `Go`, `Move`, and `Jump` commands in SPEL+?
<details>
<summary>Answer</summary>
`Go` uses joint interpolation (fastest but curved path), `Move` uses linear interpolation (straight line in Cartesian space), and `Jump` creates arc motion with automatic Z-axis retract for pick-and-place operations.
</details>

**Q2:** Why are points stored in a separate point file rather than hardcoded in the program?
<details>
<summary>Answer</summary>
Separating points from code allows positions to be updated (via teaching or offset adjustments) without modifying the program logic. This makes programs more maintainable and adaptable to fixture variations or mechanical wear.
</details>

**Q3:** What does the `Tool` command configure and why is it important?
<details>
<summary>Answer</summary>
The `Tool` command sets a coordinate frame offset from the robot's flange to the actual end-effector tip. Without the correct tool definition, all programmed positions will be shifted by the difference between the flange and the actual tool center point.
</details>

**Q4:** Why can't you treat SPEL+ like a sequential Python script?
<details>
<summary>Answer</summary>
SPEL+ programs are compiled to the controller and run in a real-time multitasking environment. Multiple tasks can run concurrently (main motion, background sensor monitoring, trap handlers), more like a PLC with motion coprocessors than an interpreted script.
</details>

**Q5:** What is the tradeoff when using `CP` (Continuous Path) motion?
<details>
<summary>Answer</summary>
CP mode allows the robot to blend through waypoints without stopping, which improves cycle time and motion smoothness. However, this trades off positional accuracy—the robot won't hit each waypoint exactly, it will cut corners to maintain velocity.
</details>

</details>
