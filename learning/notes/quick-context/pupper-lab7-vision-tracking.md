---
topic: Pupper Lab 7 — Vision + Tracking (Full Autonomy Stack)
created: 2026-03-10
---

# Pupper Lab 7 — Vision + Tracking (Full Autonomy Stack)

> **Related:** [[quick-context/pupper-lab1-pid-control]] | [[quick-context/pupper-lab2-forward-kinematics]] | [[quick-context/pupper-lab3-inverse-kinematics]] | [[quick-context/pupper-lab4-gait-control]] | [[quick-context/pupper-lab5-neural-controller]]

> **TL;DR:** Lab 7 closes the autonomy loop by adding camera-based object detection (YOLOv5 on a Hailo edge accelerator) and a three-state tracking controller (IDLE/SEARCH/TRACK) so the Pupper can autonomously find and follow any of the 80 COCO object classes on spoken command, integrating every subsystem from Labs 1-6 into a single perception-planning-control pipeline.

## The Core Problem

A robot that walks and talks is impressive, but it is still blind. Labs 5 and 6 gave the Pupper locomotion and voice understanding, yet every action required an explicit human command — "move forward," "turn left." Real autonomy demands that the robot perceive its environment, decide what to do, and act — the classic **sense-plan-act** loop. Lab 7 fills in the missing "sense" layer with computer vision and replaces open-loop human commands with a closed-loop tracking controller that continuously adjusts behavior based on what the camera sees.

The design centers on a **finite state machine** with three states. In IDLE the robot stands still, awaiting a tracking command. In SEARCH it rotates in place, scanning for the target object. In TRACK it uses a proportional controller to yaw toward the detected object and advance. Transitions between states are driven entirely by the presence or absence of fresh detections: if the detector finds the target, the machine enters TRACK; if detections go stale beyond a timeout threshold, it falls back to SEARCH. This reactive architecture is lightweight enough to run at camera frame rate (~5 Hz) while being robust to the inevitable noise of real-world object detection.

Crucially, Lab 7 does not replace the LLM from Lab 6 — it augments it. The LLM serves as a **deliberative** planner that interprets high-level voice commands ("follow the dog") and translates them into state-machine directives (`begin_tracking("dog")`). The state machine then handles the **reactive**, real-time tracking loop that the LLM's ~500 ms latency could never sustain. This two-tier architecture — slow deliberative reasoning on top, fast reactive control underneath — mirrors how production autonomous systems (self-driving cars, warehouse robots) are built.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **State Machine** | A controller with discrete modes (IDLE, SEARCH, TRACK) and well-defined transitions between them — the decision-making core of Lab 7's tracking behavior |
| **YOLO (You Only Look Once)** | A single-shot object detection architecture that predicts bounding boxes and class labels in one forward pass; Lab 7 uses YOLOv5 trained on the 80-class COCO dataset |
| **[[quick-context/raspberry-pi-ai-hat|Hailo Accelerator]]** | An edge AI inference chip (~26 TOPS) mounted on the Pupper via the [[quick-context/raspberry-pi-ai-hat|AI HAT+]] that runs the YOLOv5 network at low power, enabling on-robot detection without cloud connectivity |
| **Detection2DArray** | A ROS2 message type from `vision_msgs` containing a list of 2D bounding boxes, each with a class ID and confidence score — the output of the Hailo detection node |
| **Proportional Tracking Controller** | A P-controller that converts the horizontal pixel offset of a detected object into a yaw rate command: $\omega = -K_p \cdot x_{\text{normalized}}$, steering the robot to center the target in frame |

<details>
<summary><strong>How It Works</strong> — Perception -> Decision -> Action pipeline</summary>

The Lab 7 system implements a three-stage pipeline that runs continuously once tracking is activated:

### Stage 1: Perception (Hailo Detection Node)

The fisheye camera captures raw frames, which are first **undistorted** from the fisheye projection into an equirectangular image. This matters because fisheye lenses map straight lines to curves, which would distort bounding box geometry and confuse the detector. The undistorted frame is fed to YOLOv5 running on the Hailo accelerator at ~5 FPS. The detector outputs bounding boxes for all recognized objects, but the node **filters** by the currently tracked class ID (set via `/tracking_control`), publishing only relevant detections as `Detection2DArray` messages.

### Stage 2: Decision (State Machine)

The state machine node subscribes to `/detections` and maintains three states:

```
STATE MACHINE — Transitions driven by detection freshness
================================================================

                   begin_tracking(obj)
                          │
                          ▼
                    ┌───────────┐
                    │   IDLE    │
                    │ (standby) │
                    └─────┬─────┘
                          │ tracking_class set
                          ▼
                    ┌───────────┐
          ┌────────│  SEARCH   │◄────────┐
          │        │ (rotate)  │         │
          │        └─────┬─────┘         │
          │              │ detection     │ no detection
          │              │ received      │ for > TIMEOUT
          │              ▼               │
          │        ┌───────────┐         │
          │        │   TRACK   │─────────┘
          │        │ (follow)  │
          │        └─────┬─────┘
          │              │
          │   end_tracking()
          │              │
          └──────────────┘
                  │
                  ▼
            ┌───────────┐
            │   IDLE    │
            └───────────┘
```

**Detection callback logic** (students implement):
1. Receive `Detection2DArray` message
2. Find the detection whose bounding box center is closest to the image center (most central detection)
3. Normalize the horizontal position: $x_{\text{norm}} = \frac{x_{\text{center}}}{\text{image\_width}} - 0.5$, yielding a value in $[-0.5, 0.5]$
4. Update `last_detection_time` to the current timestamp

### Stage 3: Action (Twist Command Generation)

Each state produces a different velocity command published to `/cmd_vel`:

| State | `linear.x` | `angular.z` | Behavior |
|-------|-----------|------------|----------|
| IDLE | 0 | 0 | Stand still |
| SEARCH | 0 | $\omega_{\text{search}}$ (constant) | Rotate in place to scan |
| TRACK | $v_{\text{forward}}$ | $-K_p \cdot x_{\text{norm}}$ | Advance while centering target |

The proportional controller in TRACK mode is elegant in its simplicity: if the target is left of center ($x_{\text{norm}} < 0$), the negative sign produces positive yaw (turn left); if right ($x_{\text{norm}} > 0$), negative yaw (turn right). The gain $K_p$ controls how aggressively the robot corrects — too high and it oscillates, too low and it loses the target on curves.

### Full ROS2 Topic Graph

```
COMPLETE LAB 7 ROS2 ARCHITECTURE
================================================================

  ┌──────────────┐     /camera/image_raw     ┌──────────────────┐
  │  USB Camera  │ ─────────────────────────> │ hailo_detection   │
  │  (fisheye)   │                            │                   │
  └──────────────┘                            │ - undistort       │
                                              │ - YOLOv5 @ 5 FPS │
                      /tracking_control       │ - filter by class │
                 ┌───────────────────────────>│                   │
                 │                            └────────┬──────────┘
                 │                                     │
                 │                          /detections│  /annotated_image
                 │                                     │        │
                 │                                     ▼        ▼
  ┌──────────────┴──┐                         ┌──────────────────┐
  │ realtime_voice   │  /gpt4_response_topic  │   lab_7 state    │
  │                  │ ──────────────────────> │   machine        │
  │ - microphone in  │                        │                  │
  │ - OpenAI WS API  │                        │ - IDLE/SEARCH/   │
  │ - speaker out    │                        │   TRACK          │
  └──────────────────┘                        │ - P-controller   │
                                              └────────┬─────────┘
                                                       │
                                                /cmd_vel
                                                       │
                                                       ▼
                                              ┌──────────────────┐
                                              │ neural_controller │
                                              │ (Lab 5 RL policy)│
                                              │                  │
                                              │ - 12 joint       │
                                              │   targets @ 50Hz │
                                              └────────┬─────────┘
                                                       │
                                                   CAN bus
                                                       │
                                                       ▼
                                              ┌──────────────────┐
                                              │  12 servo motors  │
                                              └──────────────────┘
```

The pipeline latency from photon to motor command is roughly: camera capture (~30 ms) + fisheye undistortion (~10 ms) + Hailo inference (~150 ms) + state machine + ROS2 transport (~5 ms) + neural controller (~20 ms) = **~215 ms**. This is fast enough for tracking walking-speed targets but too slow for catching thrown objects.

</details>

<details>
<summary><strong>The Key Tension</strong> — Reactive vs. deliberative control</summary>

Lab 7 crystallizes a tension that runs through all of robotics: **how much should a robot think vs. react?**

### Reactive Control (State Machine)

The IDLE/SEARCH/TRACK state machine is purely **reactive** — it responds to the current sensor reading with no memory of past observations and no model of the future. If it sees the target, it tracks. If not, it searches. This makes it:

- **Fast:** Decisions happen in microseconds, limited only by detection rate
- **Predictable:** Behavior is fully determined by the current state + input
- **Fragile:** It cannot reason about occlusion ("the dog went behind the couch, I should walk around"), plan paths, or handle ambiguity ("there are two dogs, which one did the human mean?")

The proportional controller $\omega = -K_p \cdot x_{\text{norm}}$ is the simplest possible feedback law. A PD controller adding a derivative term $-K_d \cdot \dot{x}_{\text{norm}}$ would reduce oscillation, and a PID controller with an integral term would eliminate steady-state offset. But at 5 FPS detection rate, derivative estimation is noisy and integral windup is a risk, so pure P-control is a pragmatic choice.

### Deliberative Control (LLM)

The LLM from Lab 6 operates at the opposite extreme — it **reasons** about goals, context, and multi-step plans. When the user says "find my keys and come back," the LLM can decompose this into: (1) `begin_tracking("keyboard")` or perhaps recognize that keys aren't a COCO class and suggest an alternative, (2) wait for tracking to succeed, (3) `end_tracking()`, (4) `turn_around()`, (5) `move_forward()`. No reactive state machine could generate this plan.

But the LLM runs at ~500 ms per response and cannot sustain the tight control loop needed to physically follow a moving target. Hence the layered architecture:

```
CONTROL HIERARCHY — Deliberative on top, reactive below
================================================================

  ┌─────────────────────────────────────────┐  Seconds
  │           LLM (deliberative)            │  timescale
  │  "follow the dog" → begin_tracking()    │
  └─────────────────────┬───────────────────┘
                        │ semantic commands
                        ▼
  ┌─────────────────────────────────────────┐  ~200 ms
  │       State Machine (reactive)          │  timescale
  │  IDLE / SEARCH / TRACK → Twist          │
  └─────────────────────┬───────────────────┘
                        │ velocity commands
                        ▼
  ┌─────────────────────────────────────────┐  ~20 ms
  │       Neural Controller (Lab 5)         │  timescale
  │  Twist → 12 joint position targets      │
  └─────────────────────┬───────────────────┘
                        │ joint targets
                        ▼
  ┌─────────────────────────────────────────┐  1 ms
  │       Motor PD Loop (STM32)             │  timescale
  │  position target → torque → motion      │
  └─────────────────────────────────────────┘
```

Each layer operates at a different timescale and abstraction level. The LLM never touches joint angles. The state machine never interprets speech. The motor loop never reasons about object classes. This **separation of concerns** is what makes the system tractable — and is exactly how industrial autonomous systems (autonomous vehicles, warehouse robots, surgical robots) are structured.

</details>

<details>
<summary><strong>Concrete Example</strong> — "Follow the dog" full stack trace</summary>

Here is the complete trace from a human saying "follow the dog" to the Pupper physically walking after a dog, touching every node and topic in the system:

### Step 1: Voice Capture and LLM Reasoning

```
Human speaks: "Hey Pupper, follow the dog"
    │
    ▼
Microphone → 24 kHz PCM16 audio → base64 encode
    │
    ▼
realtime_voice.py: WebSocket send to OpenAI Realtime API
    │
    ▼
OpenAI server:
  - VAD detects end of speech
  - Transcribes audio
  - System prompt includes Karel action list:
    "begin_tracking(object_name) — track a COCO object"
  - LLM outputs: "I'll track the dog for you. begin_tracking dog"
    │
    ▼
realtime_voice.py: parses response → calls karel.begin_tracking("dog")
```

### Step 2: Karel Sets Up Tracking

```python
# In karel.py
def begin_tracking(self, obj: str):
    msg = String()
    msg.data = f"start:{obj}"
    self.tracking_pub.publish(msg)   # → /tracking_control
```

### Step 3: Hailo Detection Filters by Class

```
/tracking_control receives "start:dog"
    │
    ▼
hailo_detection.py:
  - Maps "dog" → COCO class ID 16
  - self.tracking_class_id = 16
  - Now only publishes Detection2D messages where class_id == 16
```

The COCO dataset defines 80 object classes. Some commonly tracked ones:

| Class ID | Name | Class ID | Name |
|----------|------|----------|------|
| 0 | person | 16 | dog |
| 1 | bicycle | 17 | horse |
| 2 | car | 39 | bottle |
| 15 | cat | 73 | book |

### Step 4: Camera Frame Processing

```
USB fisheye camera captures 700×700 frame
    │
    ▼
Fisheye undistortion:
  - [[quick-context/camera-fundamentals|Camera intrinsics matrix K]] and distortion coefficients D
  - cv2.fisheye.undistortImage() → equirectangular projection
  - Straight lines restored, bounding boxes now geometrically valid
    │
    ▼
Hailo inference (~150 ms):
  - YOLOv5 processes undistorted frame
  - Raw output: 12 detections (3 people, 1 dog, 2 chairs, ...)
  - Filter: only class_id == 16 (dog) passes
  - Result: 1 Detection2D with bbox center at pixel (420, 350)
    │
    ▼
Publish Detection2DArray to /detections
```

### Step 5: State Machine Tracks

```
lab_7.py detection_callback():
    │
    ├─ Find most central detection:
    │    x_center = 420 (out of 700 px width)
    │    x_norm = 420 / 700 - 0.5 = 0.1  (slightly right of center)
    │
    ├─ Update timestamp:
    │    self.last_detection_time = now()
    │
    └─ State transition:
         time_since_detection < TIMEOUT → state = TRACK

TRACK state publishes Twist:
    linear.x  = TRACK_FORWARD_VEL   (e.g., 0.3 m/s)
    angular.z = -Kp * x_norm
              = -2.0 * 0.1
              = -0.2 rad/s  (slight right turn to center dog)
    │
    ▼
Publish Twist to /cmd_vel
```

### Step 6: Neural Controller Executes

```
/cmd_vel: Twist(linear.x=0.3, angular.z=-0.2)
    │
    ▼
neural_controller (Lab 5 RL policy):
  - Observation: [cmd_vel, joint_states, IMU quaternion, ...]
  - Forward pass through trained policy network (~20 ms)
  - Output: 12 joint position targets
    │
    ▼
CAN bus → 12 servo motors → Pupper walks forward-right toward dog
```

### Step 7: The Loop Continues

This entire pipeline repeats at ~5 Hz (camera frame rate). Each cycle:
- If the dog moves left, $x_{\text{norm}}$ becomes negative, yaw goes positive, robot turns left
- If the dog moves far right, $x_{\text{norm}} \approx 0.5$, yaw = $-K_p \times 0.5 = -1.0$ rad/s (sharp right turn)
- If the dog disappears behind furniture, detections stop, timeout elapses, state transitions to SEARCH, robot rotates in place scanning for the dog
- If the human says "stop tracking," LLM calls `end_tracking()`, state returns to IDLE

**The one thing most outsiders get wrong about this is...** assuming the LLM is "controlling" the robot in real time. The LLM fires exactly once — to issue the `begin_tracking("dog")` command. After that, the reactive state machine and proportional controller run the show at 5 Hz with no LLM involvement. The LLM is a goal-setter, not a motor controller.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **COCO Dataset** — "Common Objects in Context," the 80-class benchmark dataset YOLOv5 is trained on. Includes everyday objects (person, car, dog, bottle, chair) but notably lacks many useful categories (keys, phone, specific breeds). This limits what Lab 7 can track out of the box. See: [cocodataset.org](https://cocodataset.org)
- **[[quick-context/raspberry-pi-ai-hat|Raspberry Pi AI HAT+]]** — The full product family of Hailo-based NPU boards for edge AI inference, including the 13T, 26T, and AI HAT+ 2 (with on-board RAM for LLMs). Covers TOPS benchmarks, data flow architecture, and the software stack that Lab 7's Hailo detection node runs on.
- **[[quick-context/camera-fundamentals|Camera Fundamentals]]** — The intrinsic matrix $K$ and distortion coefficients used in `cv2.fisheye.undistortImage()` are explained in detail here, along with sensor physics, focal length/FOV relationships, and the extrinsic transformation that locates the camera in the robot's frame.
- **Fisheye Lens Models** — Fisheye cameras use ultra-wide-angle lenses (>180 FOV) that introduce severe radial distortion modeled by: $r_d = \frac{1}{\omega} \arctan(2r_u \tan(\omega/2))$ (equidistant projection). Undistortion is essential before running detectors trained on rectilinear images. OpenCV's `cv2.fisheye` module handles the calibration and remapping.
- **Hysteresis in Control Systems** — The timeout-based TRACK-to-SEARCH transition is a form of hysteresis: the condition for entering TRACK (any fresh detection) differs from the condition for leaving it (no detection for $> T$ seconds). This asymmetry prevents rapid state oscillation (chattering) when detections are intermittent. Hysteresis appears throughout engineering: thermostats, Schmitt triggers, magnetic materials.
- **[[quick-context/pupper-v3-labs]]** — The full 7-lab curriculum overview showing how Labs 1-6 build the foundation that Lab 7 integrates.
- **[[quick-context/pupper-brain]]** — The hardware architecture (dual STM32 + Raspberry Pi + CAN bus) that executes the motor commands Lab 7's state machine generates.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** The proportional tracking controller uses $\omega = -K_p \cdot x_{\text{normalized}}$. Why is the negative sign necessary, and what would happen without it?

<details>
<summary>Answer</summary>

The negative sign creates **negative feedback** — the controller acts to reduce the error. If the target is to the right of center, $x_{\text{norm}} > 0$, and the robot should turn right (negative $\omega$ in standard ROS convention where positive $\omega$ is counter-clockwise). Without the negative sign, the controller would exhibit **positive feedback**: a target to the right would cause the robot to turn left, moving the target further right, causing even more left turn — the robot would spin away from the target instead of toward it. This is the fundamental difference between a stable and unstable control loop.
</details>

**Q2:** The Hailo detection node runs at ~5 FPS, but the neural locomotion controller runs at ~50 Hz. Why is this mismatch acceptable, and what would break if the detection rate were much lower (say 0.5 FPS)?

<details>
<summary>Answer</summary>

The mismatch is acceptable because the state machine **holds** its last Twist command between detection updates. The locomotion controller receives a steady `/cmd_vel` stream and smoothly executes the velocity — it does not need a new detection every cycle. At 5 FPS, the tracking loop updates yaw correction every 200 ms, which is fast enough to follow walking-speed targets. At 0.5 FPS (2 seconds between updates), two problems emerge: (1) the robot drives in a straight line for 2 seconds between corrections, causing it to overshoot and oscillate, and (2) the detection timeout (typically 1-2 seconds) would fire between nearly every valid frame, causing constant TRACK-to-SEARCH transitions. The 5 FPS rate is a sweet spot between inference cost and control responsiveness.
</details>

**Q3:** The state machine uses timeout-based hysteresis for the TRACK $\to$ SEARCH transition instead of switching immediately on a missed detection. Suppose the timeout is set to 1.5 seconds and the detector runs at 5 FPS. How many consecutive missed frames does this tolerate, and why is this preferable to a frame-count threshold (e.g., "switch after 3 missed frames")?

<details>
<summary>Answer</summary>

At 5 FPS, each frame arrives every 200 ms. A 1.5-second timeout tolerates $1.5 / 0.2 = 7.5$, so approximately **7 consecutive missed frames** before transitioning to SEARCH. A time-based threshold is preferable to a frame-count threshold because the detection frame rate is not guaranteed to be constant — Hailo inference time varies with scene complexity, and frames can be dropped due to USB bandwidth or CPU load. If the detector temporarily slows to 2 FPS, a "3 missed frames" threshold would wait 1.5 seconds, but if it speeds up to 10 FPS, the same threshold would only wait 0.3 seconds — causing premature SEARCH transitions during brief occlusions. A time-based timeout provides consistent behavior regardless of frame rate variation. This is a general principle: time-based thresholds are more robust than count-based thresholds when the event rate is variable.
</details>

</details>
