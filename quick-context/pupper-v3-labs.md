---
topic: Pupper v3 Labs — CS123 Robotics Curriculum (Labs 1-7)
created: 2026-03-10
---

# Pupper v3 Labs — CS123 Robotics Curriculum (Labs 1-7)

> **Related:** [[quick-context/pupper-brain]] | [[quick-context/pupper-bom-control-board]] | [[quick-context/ros2-architecture]]
>
> **Individual Labs:** [[quick-context/pupper-lab1-pid-control]] | [[quick-context/pupper-lab2-forward-kinematics]] | [[quick-context/pupper-lab3-inverse-kinematics]] | [[quick-context/pupper-lab4-gait-control]] | [[quick-context/pupper-lab5-neural-controller]] | [[quick-context/pupper-lab6-llm-voice-control]] | [[quick-context/pupper-lab7-vision-tracking]]

> **TL;DR:** Seven progressive labs that take you from controlling a single motor joint with PID to a fully autonomous voice-controlled quadruped that sees, tracks, and responds to spoken commands. Labs 1-4 build classical robotics foundations (PID, forward kinematics, inverse kinematics, gait control), Lab 5 replaces hand-tuned control with RL-trained neural policies, and Labs 6-7 add LLM voice control and computer vision for a complete autonomy stack.

## The Core Problem

Building a walking, seeing, talking robot requires knowledge spanning control theory, kinematics, machine learning, and systems integration. No single course can teach all of this at once. These 7 labs scaffold the learning: each lab builds on the previous one's code and concepts, progressively unlocking new capabilities while reusing FK/IK/gait code from earlier labs. By Lab 7, every subsystem (motors, IMU, camera, microphone, speaker, neural network, LLM) runs simultaneously on the Pupper.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **PD Control** | Proportional-Derivative controller that computes torque as $\tau = K_p(q_{target} - q) + K_d(\dot{q}_{target} - \dot{q})$ — the foundation of Labs 1, 3, and 4 |
| **Forward Kinematics (FK)** | Computing end-effector (foot) position from joint angles using chained 4x4 homogeneous transformation matrices — Lab 2's core concept, reused in every subsequent lab |
| **Inverse Kinematics (IK)** | Finding joint angles that place the foot at a desired position — Lab 3 solves this via gradient descent on the FK cost function |
| **Karel** | The `KarelPupper` class (Labs 6-7) that wraps ROS2 Twist commands into simple actions (`move_forward`, `bark`, `begin_tracking`) so an LLM can control the robot through function calls |
| **State Machine** | Lab 7's IDLE/SEARCH/TRACK controller that transitions between rotating to find a target, and using proportional control to follow it based on camera detections |

<details>
<summary><strong>How It Works</strong> — The 7-lab progression</summary>

```
LAB PROGRESSION — Each builds on the previous
================================================================

  Lab 1          Lab 2          Lab 3          Lab 4
  PID            FK             IK             Gait
  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
  │ 1 joint│───>│ 3 joint│───>│gradient│───>│ 4 legs │
  │ torque │    │ chain  │    │descent │    │ trot   │
  │ control│    │ matrix │    │ + FK   │    │ +FK+IK │
  └────────┘    └────────┘    └────────┘    └────────┘
       │              │              │              │
       │         reuse FK       reuse FK+IK    reuse all
       │              │              │              │
       ▼              ▼              ▼              ▼
  Lab 5          Lab 6          Lab 7
  RL Policy      LLM Voice      Vision+Track
  ┌────────┐    ┌────────┐    ┌────────┐
  │ neural │    │ OpenAI │    │ Hailo  │
  │ net    │    │Realtime│    │ YOLOv5 │
  │replaces│    │  API   │    │  +LLM  │
  │PD+gait │    │ +Karel │    │ +Karel │
  └────────┘    └────────┘    └────────┘
```

### Lab 1: PID Control (Single Joint)

Students tune $K_p$ and $K_d$ gains for one motor (`leg_front_l_1`). The control loop runs at 200 Hz, reading joint position/velocity from `/joint_states` and publishing torque commands (clamped to 3.0 Nm). Key tasks:

- Implement `get_target_joint_info()` to return desired position and velocity
- Implement `calculate_torque()` using the PD formula
- Tune gains to track a trajectory without oscillation

The YAML config exposes effort, kp, and kd interfaces through ROS2's `forward_command_controller`.

### Lab 2: Forward Kinematics (3-DOF Leg)

Students build 4x4 homogeneous transformation matrices to compute where the front-left foot is in 3D space given three joint angles. Key tasks:

- Implement `rotation_y()`, `rotation_z()`, and `translation()` matrices
- Chain transformations: $T_{0 \to ee} = T_{0 \to 1} \cdot T_{1 \to 2} \cdot T_{2 \to 3} \cdot T_{3 \to ee}$
- Extract 3D position from the final transformation matrix
- Visualize with an RViz marker (green sphere at foot position)

Each transform combines a rotation about a joint axis with a translation along the link. The first joint rotates about the x-axis (hip abduction), subsequent joints about y-axes.

### Lab 3: Inverse Kinematics (Gradient Descent)

Students solve the inverse problem: given a desired foot position, find joint angles. Uses numerical optimization rather than analytical solutions. Key tasks:

- Implement cost function: $C(\theta) = \|FK(\theta) - p_{target}\|^2$
- Compute gradient via finite differences: $\frac{\partial C}{\partial \theta_i} \approx \frac{C(\theta + \epsilon e_i) - C(\theta)}{\epsilon}$
- Gradient descent update: $\theta \leftarrow \theta - \alpha \nabla C(\theta)$
- Interpolate between 3 triangle waypoints (touchdown, liftoff, mid-swing) for a stepping motion

Runs a 200 Hz PD loop for joint tracking and a 20 Hz IK loop for trajectory updates.

### Lab 4: Gait Control (Trotting)

Extends Labs 2-3 to all 4 legs for coordinated walking. Key tasks:

- Implement FK for all 4 legs (front-right, front-left, back-right, back-left) with correct hip offsets
- Define trotting gait: diagonal leg pairs move in sync (FR+BL swing while FL+BR stance)
- Pre-cache all target joint positions for one gait cycle to avoid real-time IK cost
- Interpolate triangle trajectories per leg with phase offsets

The gait uses 6 waypoints per leg (touchdown, 3 stance positions, liftoff, mid-swing) with offsets from body center.

### Lab 5: Neural Controller (Reinforcement Learning)

Replaces the hand-tuned PD + FK/IK + gait pipeline with an RL-trained neural network policy. The neural controller runs at ~52 Hz (via `repeat_action: 10` at 520 Hz update rate) and directly outputs joint position targets. Key concepts:

- Policies trained in simulation (MuJoCo), deployed to real robot (sim-to-real transfer)
- Weights & Biases (wandb) for experiment tracking and policy download
- Multiple modes: normal walk, three-legged, parkour, test
- Emergency stop controller (C++ node) for safety
- Config-driven: `config.yaml` sets gains, joint names, default poses

### Lab 6: LLM Voice Control (Karel + OpenAI Realtime API)

Students program the robot to respond to voice commands through an LLM. Two components:

**KarelPupper class** (`karel.py`): Wraps ROS2 Twist commands into robot actions:
- Implement `move_forward()`, `move_backward()`, `move_left()`, `move_right()`, `turn_left()`, `turn_right()`
- Implement `bob()` animation with alternating forward/backward motion + sound
- Create a `dance()` choreography combining movements

**Realtime Voice** (`realtime_voice.py`): OpenAI WebSocket API for ultra-low-latency voice:
- Write a system prompt that instructs the LLM to output structured commands matching Karel's action functions
- Audio streaming at 24 kHz PCM16 with server-side VAD (voice activity detection)
- Auto-muting during playback to prevent echo loops

### Lab 7: Vision + Tracking (Full System)

Adds computer vision for autonomous object tracking, combining everything from prior labs. Three new components:

**Hailo Detection** (`hailo_detection.py`): YOLOv5 inference on a Hailo AI accelerator:
- Fisheye camera undistortion to equirectangular projection
- COCO 80-class object detection at 5 FPS
- Publishes `Detection2DArray` messages

**State Machine** (`lab_7.py`): Students implement:
- Detection callback: find most central detection, normalize position to [-0.5, 0.5]
- State transitions: IDLE (no tracking), SEARCH (rotate to find target), TRACK (follow with P-controller)
- Proportional yaw control: $\omega = -K_p \cdot x_{normalized}$
- Timeout-based transition back to SEARCH when target lost

**Enhanced Karel** (`karel.py`): Added `begin_tracking(obj)` and `end_tracking()` to let the LLM trigger visual tracking of any COCO object class.

</details>

<details>
<summary><strong>The Key Tension</strong> — Classical control vs. learned control</summary>

The lab sequence reveals a fundamental tension in robotics:

**Labs 1-4 (Classical):** You understand every equation. PD gains are interpretable, FK matrices are derivable, IK convergence is provable. But the pipeline is fragile — hand-tuned gaits don't adapt to terrain, and adding a new behavior (jumping, recovering from a push) requires re-engineering the whole stack.

**Lab 5 (Learned):** The neural network replaces hundreds of lines of FK/IK/gait code with a single policy file. It handles terrain variation, perturbations, and three-legged locomotion that would be extremely difficult to hand-code. But the policy is a black box — when it fails, you can't easily debug which "line" of the neural network went wrong.

| Aspect | Classical (Labs 1-4) | Learned (Lab 5) |
|--------|---------------------|-----------------|
| Interpretability | Full — every equation visible | Low — weights are opaque |
| Robustness | Fragile to unknowns | Handles novel terrain |
| Development time | Weeks of tuning | Hours of training (+ sim setup) |
| Failure mode | Predictable, debuggable | Sudden, hard to diagnose |
| Generalization | Manual per-behavior | Emergent from reward shaping |

**Labs 6-7 add a third layer:** LLM-based high-level control. The LLM doesn't control joints or even gaits — it issues semantic commands ("follow that person", "dance") that get executed by either the classical or neural pipeline underneath. This mirrors real autonomous systems: perception (Lab 7 vision) feeds into planning (LLM reasoning) feeds into control (Lab 5 neural policy or Lab 4 gait).

</details>

<details>
<summary><strong>Concrete Example</strong> — Tracing a command through the full stack</summary>

Here's what happens when you say "follow the dog" to the Lab 7 system:

```
VOICE COMMAND → ROBOT ACTION (Full Stack Trace)
================================================================

  1. AUDIO CAPTURE
     Microphone → 24kHz PCM16 → base64 encode
     → WebSocket send to OpenAI Realtime API

  2. LLM PROCESSING
     OpenAI server: VAD detects speech end
     → Transcription: "follow the dog"
     → System prompt instructs output format
     → Response: "begin_tracking dog"

  3. COMMAND PARSING (realtime_voice.py)
     response.done event → publish to /gpt4_response_topic
     → Karel command parser extracts: begin_tracking("dog")

  4. TRACKING CONTROL (karel.py)
     begin_tracking("dog")
     → Publish String("start:dog") to /tracking_control

  5. DETECTION FILTER (hailo_detection.py)
     /tracking_control callback: self.tracking_class_id = 16  (COCO: "dog")
     → Only publish Detection2D for class_id == 16

  6. STATE MACHINE (lab_7.py)
     /detections callback:
       → Normalize: target_pos = bbox_center_x / 700 - 0.5
       → If detection fresh (< TIMEOUT): state = TRACK
       → If stale: state = SEARCH

  7. MOTOR COMMAND
     TRACK state:
       yaw = -target_pos * KP    (P-controller centers dog)
       forward = TRACK_FORWARD_VEL
     → Publish Twist(linear.x, angular.z) to /cmd_vel

  8. NEURAL CONTROLLER (Lab 5)
     /cmd_vel → neural policy maps velocity command
     → 12 joint position targets at 50Hz
     → CAN bus → servo motors → Pupper walks toward dog
```

The ROS2 topic graph for the full Lab 7 system:

```
  /camera/image_raw ──> hailo_detection ──> /detections
                                       ──> /annotated_image

  microphone ──> realtime_voice ──> /gpt4_response_topic
                                ──> /tracking_control

  /tracking_control ──> hailo_detection (filter by class)
                    ──> lab_7 state machine

  /detections ──> lab_7 state machine ──> /cmd_vel

  /cmd_vel ──> neural_controller ──> joint position targets
                                 ──> CAN bus → motors
```

**The one thing most outsiders get wrong about this is...** thinking the LLM directly controls the motors. It doesn't. The LLM is three abstraction layers removed from the hardware: it outputs text commands → parsed into Karel function calls → which publish ROS2 Twist messages → which the neural controller converts to joint angles. This layering is essential — an LLM operating at ~500ms latency can't control a 1kHz motor loop, but it can make high-level decisions that the real-time layers execute reliably.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/pupper-brain]]** — The [[micro-context/stm32-microcontroller|dual-STM32]] + Raspberry Pi hardware architecture that Labs 1-4 run on directly. The 1kHz control loop described there is what executes the PD control from Lab 1 and the joint targets from Labs 3-5.
- **[[quick-context/pupper-bom-control-board]]** — Every physical component on the board: the [[micro-context/can-bus-transceiver|CAN transceivers]] that carry joint commands, the [[micro-context/imu-inertial-measurement-unit|BNO086 IMU]] that Lab 5's neural policy reads for balance, and the [[micro-context/buck-converter|buck converter]] powering it all.
- **[[quick-context/ros2-architecture|ROS2 (Robot Operating System 2)]]** — The middleware framework all labs use. Nodes communicate via topics (pub/sub), services, and actions. Key message types: `JointState`, `Float64MultiArray`, `Twist`, `Detection2DArray`. See the dedicated quick-context for the full node graph and topic map.
- **MuJoCo** — Physics simulator used in Lab 5 for training RL policies before transferring to the real robot (sim-to-real).
- **Hailo AI Accelerator** — Edge AI chip used in Lab 7 for running YOLOv5 object detection at low power on the robot.
- **OpenAI Realtime API** — WebSocket-based voice API used in Labs 6-7, replacing the traditional Whisper + GPT + TTS pipeline with a single low-latency connection.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does Lab 3 use gradient descent for inverse kinematics instead of an analytical (closed-form) solution?
<details>
<summary>Answer</summary>
Numerical IK via gradient descent generalizes to any robot geometry without requiring derivation of closed-form equations (which may not exist for some configurations). It also naturally handles the cost-function formulation where you can add constraints (joint limits, obstacle avoidance) by adding penalty terms. The tradeoff is speed — gradient descent requires many FK evaluations per IK solve, which is why Lab 3 runs IK at only 20 Hz while the PD loop runs at 200 Hz.
</details>

**Q2:** In Lab 4's trotting gait, why do diagonal leg pairs (FR+BL, FL+BR) swing together rather than adjacent legs?
<details>
<summary>Answer</summary>
Diagonal pairing (trotting) keeps the robot statically stable — at any instant, two diagonally opposite feet are on the ground, forming a support line that passes under the center of mass. If same-side (ipsilateral) legs swung together (pacing), the robot would rock side to side. If both front legs and both hind legs swung together (bounding), the robot would pitch forward and backward. Trotting is the most stable two-phase gait for quadrupeds.
</details>

**Q3:** Lab 5's neural controller uses `repeat_action: 10` at a 520 Hz update rate. What effective control frequency does the neural network run at, and why not run it faster?
<details>
<summary>Answer</summary>
$520 / 10 = 52$ Hz (the config intentionally runs slightly above 500 Hz to land at exactly ~50 Hz for the neural controller). The neural network doesn't run faster because: (1) RL policies are trained at a specific frequency in simulation — running at a different frequency changes the dynamics and the policy may fail, (2) neural network inference has non-trivial compute cost on the Pi, and (3) the policy outputs position targets that the lower-level PD controller tracks at full rate, so ~50 Hz is sufficient for locomotion commands.
</details>

**Q4:** In Lab 7's state machine, why use a timeout-based transition to SEARCH instead of immediately switching when no detection is found in a single frame?
<details>
<summary>Answer</summary>
Object detection is noisy — the detector can miss the target for a few frames even when it's clearly visible (occlusion, motion blur, inference latency). Immediately switching to SEARCH on a single missed frame would cause erratic behavior: the robot would start spinning every time the detector blinks. The timeout (typically 1-2 seconds) provides hysteresis, keeping the robot in TRACK mode through brief detection dropouts and only switching to SEARCH when the target is genuinely lost.
</details>

**Q5:** The system prompt in Lab 6's `realtime_voice.py` must instruct the LLM to output specific action phrases that match Karel's command parser. Why is this prompt engineering critical, and what happens if the LLM outputs free-form text instead?
<details>
<summary>Answer</summary>
The command parser uses string matching to map LLM output to Karel function calls (e.g., "move forward" maps to `move_forward()`). If the LLM outputs "I'll walk ahead now" instead of "move forward", the parser won't recognize it and the robot does nothing. This is a fundamental tension in LLM-controlled systems: natural language is ambiguous but robot APIs need exact commands. The system prompt must enumerate every valid action phrase with examples, essentially constraining the LLM's output space to a controlled vocabulary. This is why structured output formats (JSON, function calling) are increasingly preferred over free-text command parsing.
</details>

</details>
