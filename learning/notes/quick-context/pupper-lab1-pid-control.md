---
topic: Pupper Lab 1 — PID Control (Single Joint)
created: 2026-03-10
---

# Pupper Lab 1 — PID Control (Single Joint)

> **Related:** [[learning/notes/quick-context/pupper-v3-labs]] | [[learning/notes/quick-context/can-bus]]

> **TL;DR:** Lab 1 introduces closed-loop motor control by having students implement and tune a PD controller for a single joint — computing torque from position and velocity error at 200 Hz — which becomes the foundational control primitive reused in every subsequent lab.

## The Core Problem

A robot motor does not move to a desired angle on its own. Given a raw torque command, the motor spins with some force, but nothing inherently drives it toward a target position or prevents it from overshooting. Proportional-Derivative (PD) control solves this by continuously measuring the gap between where the joint *is* and where it *should be*, then applying a corrective torque proportional to that error. The proportional term ($K_p$) pulls the joint toward the target; the derivative term ($K_d$) resists motion that is too fast, damping out oscillation. Together they produce smooth, stable tracking of a desired trajectory.

In this lab, students work with a single joint (`leg_front_l_1`) on the Pupper quadruped. The ROS2 node subscribes to `/joint_states` (which provides the current joint position $q$ and velocity $\dot{q}$) and publishes torque commands through a `forward_command_controller` that exposes effort, kp, and kd interfaces via YAML configuration. Students implement two functions — `get_target_joint_info()`, which returns the desired position and velocity at the current time, and `calculate_torque()`, which applies the PD formula $\tau = K_p(q_{target} - q) + K_d(\dot{q}_{target} - \dot{q})$ — then tune the gains so the joint tracks a sinusoidal or step trajectory without oscillation or sluggishness. All torque output is clamped to $\pm 3.0$ Nm for safety.

This lab is deliberately scoped to one joint so students can build intuition for gain tuning before the complexity of multi-joint kinematics (Lab 2), inverse kinematics (Lab 3), and full-body gait control (Lab 4) enter the picture. The 200 Hz PD loop implemented here reappears in Labs 3 and 4, where it tracks joint angle targets produced by the IK solver and gait planner.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **$K_p$ (Proportional Gain)** | Scalar multiplier on position error — higher $K_p$ means stronger corrective torque toward the target, but too high causes oscillation |
| **$K_d$ (Derivative Gain)** | Scalar multiplier on velocity error — provides damping that resists rapid motion, smoothing out overshoot at the cost of slower response |
| **Torque Clamp** | Hard limit ($\pm 3.0$ Nm) applied to the computed torque before sending it to the motor — prevents damage to gears and protects against runaway commands from bad gains |
| **`/joint_states`** | ROS2 topic of type `sensor_msgs/JointState` carrying each joint's current position (radians), velocity (rad/s), and effort (Nm) — the feedback signal in the control loop |
| **`forward_command_controller`** | ROS2 controller plugin that accepts raw effort (torque) commands and forwards them directly to the motor driver — bypasses any built-in position controller so students implement PD themselves |

<details>
<summary><strong>How It Works</strong> — PD control loop</summary>

The control loop runs at 200 Hz (every 5 ms). Each cycle executes the same sequence:

```
PD CONTROL LOOP — ONE CYCLE (5 ms)
================================================================

  1. READ JOINT STATE
     Subscribe to /joint_states
     → Extract: q (position), q̇ (velocity) for leg_front_l_1

  2. COMPUTE TARGET
     Call get_target_joint_info(current_time)
     → Returns: q_target, q̇_target

  3. COMPUTE ERROR
     position_error = q_target - q
     velocity_error = q̇_target - q̇

  4. APPLY PD FORMULA
     τ = Kp × position_error + Kd × velocity_error

  5. CLAMP TORQUE
     τ = clamp(τ, -3.0, +3.0)

  6. PUBLISH COMMAND
     Publish τ to forward_command_controller
     → Motor applies torque → joint moves → new state at step 1


BLOCK DIAGRAM:
================================================================

  q_target ──┐
             ├─ Σ ─── position_error ─── × Kp ───┐
  q ─────────┘                                     ├─ Σ ─── clamp ─── τ ─── Motor
                                                   │
  q̇_target ──┐                                     │
             ├─ Σ ─── velocity_error ─── × Kd ───┘
  q̇ ─────────┘

                    ┌──────────────────────────────┐
  Motor ──────────> │  /joint_states (q, q̇)        │ ──> back to top
                    │  (sensor feedback @ 200 Hz)   │
                    └──────────────────────────────┘
```

The `get_target_joint_info()` function typically returns a sinusoidal trajectory for testing:
- $q_{target}(t) = A \sin(2\pi f t)$
- $\dot{q}_{target}(t) = 2\pi f A \cos(2\pi f t)$

where $A$ is the amplitude (e.g., 0.5 rad) and $f$ is the frequency (e.g., 0.5 Hz). Providing both position and velocity targets lets the derivative term contribute even during smooth motion — without $\dot{q}_{target}$, the $K_d$ term would always resist motion toward the target, making the response sluggish.

</details>

<details>
<summary><strong>The Key Tension</strong> — Gain tuning tradeoffs</summary>

PD gain tuning is a balancing act between responsiveness and stability. The two gains pull in opposite directions:

**$K_p$ too high:** The motor applies enormous torque for even small position errors. The joint overshoots the target, and the large error on the other side drives it back past the target again — producing oscillation that grows or sustains indefinitely. In a real robot, this causes violent shaking and can strip gears.

**$K_p$ too low:** The corrective torque is weak. The joint drifts slowly toward the target but never quite gets there, especially under gravity or friction. It "sags" below desired positions and can't keep up with fast trajectory changes.

**$K_d$ too high:** The derivative term resists all motion aggressively. Even correct motion toward the target is damped, making the response sluggish and slow to settle. Worse, high $K_d$ amplifies sensor noise — if the velocity measurement has high-frequency noise (common with numerical differentiation of encoder position), the $K_d$ term produces jerky, noisy torque commands.

**$K_d$ too low:** No damping. Overshoots are unchecked, so even moderate $K_p$ produces oscillation. The system rings like a struck bell.

```
GAIN TUNING MAP
================================================================

             High Kd
               │
    SLUGGISH   │   STABLE
    (overdamped│   (critically damped — the goal)
     slow to   │    fast response, minimal overshoot)
     settle)   │
  ─────────────┼─────────────── High Kp
               │
    INERT      │   OSCILLATING
    (barely    │   (underdamped — rings and
     moves)    │    may become unstable)
               │
             Low Kd

    Sweet spot: Kp high enough for fast response,
    Kd just enough to prevent overshoot.
    Start with Kd = 0, increase Kp until oscillation,
    then add Kd until oscillation stops.
```

**Why the torque clamp matters:** Even with perfect gains, transient errors (like startup, when the joint is far from the target) produce huge torques. The 3.0 Nm clamp prevents gear damage during these transients. It also acts as a safety net during tuning — if you accidentally set $K_p = 1000$, the motor hits the clamp instead of destroying itself. The tradeoff: clamping makes the controller nonlinear and can slow convergence from large errors since the motor is torque-limited.

</details>

<details>
<summary><strong>Concrete Example</strong> — Tracing one control cycle</summary>

Suppose the joint is tracking a sinusoidal trajectory with $A = 0.5$ rad, $f = 0.5$ Hz. At $t = 0.25$ s into the trajectory, with gains $K_p = 10.0$, $K_d = 0.5$:

```
ONE CONTROL CYCLE AT t = 0.250 s
================================================================

STEP 1: Read /joint_states
   q       = 0.320 rad     (current position)
   q̇       = 1.400 rad/s   (current velocity)

STEP 2: Compute target (sinusoidal trajectory)
   q_target  = 0.5 × sin(2π × 0.5 × 0.25)
             = 0.5 × sin(π/4)
             = 0.5 × 0.707
             = 0.354 rad

   q̇_target  = 2π × 0.5 × 0.5 × cos(π/4)
             = 1.571 × 0.707
             = 1.111 rad/s

STEP 3: Compute errors
   position_error = 0.354 - 0.320 = +0.034 rad
                    (joint is slightly behind target)

   velocity_error = 1.111 - 1.400 = -0.289 rad/s
                    (joint is moving too fast)

STEP 4: Apply PD formula
   τ = Kp × position_error + Kd × velocity_error
   τ = 10.0 × 0.034  +  0.5 × (-0.289)
   τ = 0.340 + (-0.145)
   τ = 0.195 Nm

   Interpretation:
   • Kp term (+0.340): "Pull toward target" — joint is behind
   • Kd term (-0.145): "Slow down" — joint is moving too fast
   • Net: gentle forward torque, slightly braked

STEP 5: Clamp check
   |0.195| < 3.0   →   no clamping needed
   τ_output = 0.195 Nm

STEP 6: Publish
   → forward_command_controller receives 0.195 Nm
   → Motor applies torque
   → Next cycle in 5 ms (t = 0.255 s)
```

**What if the gains were wrong?**

With $K_p = 100$, $K_d = 0.1$ (too aggressive, underdamped):
```
   τ = 100.0 × 0.034 + 0.1 × (-0.289)
   τ = 3.400 + (-0.029) = 3.371 Nm
   → CLAMPED to 3.0 Nm

   The motor is torque-saturated. The tiny Kd barely contributes.
   On the next cycle, the joint will overshoot the target,
   then the Kp term will slam it back — oscillation.
```

With $K_p = 1.0$, $K_d = 5.0$ (too sluggish, overdamped):
```
   τ = 1.0 × 0.034 + 5.0 × (-0.289)
   τ = 0.034 + (-1.445) = -1.411 Nm

   Net torque is NEGATIVE — the Kd term dominates and
   actively brakes the joint even though it hasn't reached
   the target yet. The joint falls further behind the
   sinusoidal trajectory.
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/pupper-v3-labs]]** — The full 7-lab curriculum overview. Lab 1's PD controller is reused directly in Labs 3 (IK trajectory tracking) and 4 (gait control), and its concepts appear in Lab 7's proportional yaw controller for visual tracking.
- **[[quick-context/pupper-brain]]** — The hardware that executes these commands. The `forward_command_controller` ultimately sends torque values through the STM32 motor MCU over [[learning/notes/quick-context/can-bus|CAN bus]] to the servo motors.
- **ROS2 `sensor_msgs/JointState`** — The message type on `/joint_states`. Fields: `name[]` (joint names), `position[]` (radians), `velocity[]` (rad/s), `effort[]` (Nm). The node must index into these arrays to find the correct joint.
- **`forward_command_controller`** — A ROS2 control plugin from `ros2_controllers`. The YAML config maps joint names to command interfaces (effort) and state interfaces (position, velocity). It bypasses any built-in PID so students implement their own.
- **Torque vs. position control** — Most hobby servos accept position commands. The Pupper's motors accept raw torque commands, giving students direct control over the force applied — essential for learning PD control from first principles.
- **200 Hz control rate** — A tradeoff: fast enough for smooth joint control, slow enough to run comfortably on the Raspberry Pi in Python. Lab 5's neural controller runs at ~50 Hz; the underlying hardware supports up to 1000 Hz via the STM32.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** You set $K_d = 0$ and increase $K_p$ from 1 to 50. At $K_p = 30$, the joint starts oscillating around the target. Why does increasing $K_p$ alone eventually cause oscillation?
<details>
<summary>Answer</summary>
Without derivative damping ($K_d = 0$), there is nothing to slow the joint as it approaches the target. At high $K_p$, the large corrective torque accelerates the joint so aggressively that it overshoots. Once past the target, the position error reverses sign and the motor slams back the other direction — overshooting again. Each cycle feeds the next, producing sustained or growing oscillation. This is a classic underdamped second-order system: the natural frequency increases with $K_p$, and without $K_d$ the damping ratio is effectively zero.
</details>

**Q2:** Why does the controller compute $\dot{q}_{target}$ (target velocity) instead of just using zero as the desired velocity?
<details>
<summary>Answer</summary>
If $\dot{q}_{target} = 0$ always, the derivative term becomes $K_d(0 - \dot{q}) = -K_d \dot{q}$, which opposes ALL motion — including correct motion toward the target. When tracking a moving trajectory (like a sinusoid), the joint needs to be moving at a nonzero speed at most time steps. Setting $\dot{q}_{target}$ to the trajectory's analytical derivative means the $K_d$ term only penalizes deviation from the expected speed, not motion itself. This is the difference between a PD controller (tracks trajectory) and a PD regulator (drives to a fixed setpoint).
</details>

**Q3:** The torque output is clamped to $\pm 3.0$ Nm. What would happen if there were no clamp and a student accidentally set $K_p = 500$?
<details>
<summary>Answer</summary>
With $K_p = 500$ and even a modest position error of 0.1 rad, the computed torque would be 50 Nm — far beyond the motor's rated torque. Three things could happen: (1) the motor driver's own current limit might cap the output, but potentially at a level that still damages the gearbox; (2) the gears could strip or the motor could overheat from sustained stall current; (3) the leg could slam into mechanical hard stops at high speed, damaging the 3D-printed structure. The software clamp at 3.0 Nm is a first line of defense that keeps the motor in a safe operating range regardless of gain values. It also prevents the control board from commanding currents that exceed the motor driver's safe limits.
</details>

</details>
