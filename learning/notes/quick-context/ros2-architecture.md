---
topic: ROS2 Architecture — Robot Operating System 2 for Pupper v3
created: 2026-03-10
---

# ROS2 Architecture — Robot Operating System 2 for Pupper v3

> **Related:** [[quick-context/pupper-v3-labs]] | [[quick-context/pupper-brain]] | [[quick-context/pupper-bom-control-board]]

> **TL;DR:** ROS2 is the middleware framework that connects every software component on the Pupper v3 — from motor PD controllers to neural network policies to LLM voice agents — through a publish/subscribe messaging system where nodes communicate over named topics, allowing each of the 7 CS123 labs to add new capabilities without modifying existing code.

## The Core Problem

A walking robot that sees, talks, and tracks objects is not one program — it is dozens of programs running simultaneously. The PD controller needs joint positions at 200 Hz. The [[quick-context/pupper-lab3-inverse-kinematics|inverse kinematics]] solver runs at 20 Hz. The neural locomotion policy updates at 50 Hz. The vision detector processes frames at 5 Hz. The [[quick-context/pupper-lab6-llm-voice-control|LLM]] voice agent responds in seconds. These processes have wildly different rates, different programming languages, and different computational requirements (some run on the Pi's ARM cores, others could run on edge accelerators). Without a communication framework, you would spend more time writing socket code, serialization formats, and synchronization logic than writing actual robotics algorithms.

ROS2 (Robot Operating System 2) solves this by providing a standardized publish/subscribe middleware built on DDS (Data Distribution Service). Each software component runs as an independent **node**. Nodes communicate by publishing **messages** to named **topics** — any node [[micro-context/can-bus-termination|can]] subscribe to any topic, and ROS2 handles the serialization, transport, and delivery. This decouples producers from consumers: the PD controller doesn't know or care whether its joint commands came from a hand-tuned IK solver (Lab 3), a gait generator (Lab 4), or a neural network (Lab 5). It just reads from the same topic.

This architecture is what makes the 7-lab progression possible. Each lab adds new nodes and topics to the graph without touching the nodes from previous labs. Lab 1 creates the PD controller node. Lab 2 adds an FK visualization node. Lab 3 adds an IK node that publishes to the same joint target topic. Lab 5 swaps in a [[quick-context/pupper-lab5-neural-controller|neural controller]] node. Lab 6 adds a voice node. Lab 7 adds a vision node and state machine. At every stage, the existing infrastructure keeps working — you are composing a robot from modular building blocks, not rewriting a monolith.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Node** | An independent process that performs one task — e.g., `pd_controller_node`, `neural_controller`, `hailo_detection`, `realtime_voice`. Each node has its own update rate and lifecycle. Nodes are the unit of modularity in ROS2. |
| **Topic** | A named communication channel — e.g., `/joint_states`, `/cmd_vel`, `/detections`. Topics are typed: only messages of the declared type can be published. Topics decouple publishers from subscribers; neither needs to know the other exists. |
| **Publisher / Subscriber** | The two ends of a topic connection. A publisher sends messages (e.g., the vision node publishes `Detection2DArray` to `/detections`). A subscriber receives them (e.g., the state machine subscribes to `/detections`). One topic can have multiple publishers and multiple subscribers simultaneously. |
| **Message Type** | A structured data format defined in `.msg` files — e.g., `sensor_msgs/JointState` contains `name[]`, `position[]`, `velocity[]`, `effort[]` fields. Common types on Pupper: `JointState`, `Float64MultiArray`, `Twist`, `Detection2DArray`, `String`. |
| **Launch File** | A Python script (`.launch.py`) that starts multiple nodes with configured parameters in one command. Launch files specify which nodes to run, remap topic names, load YAML config files, and set ROS2 parameters — they are the "recipe" for bringing up an entire lab's node graph. |

<details>
<summary><strong>How It Works</strong> — ROS2 communication model</summary>

### The Publish/Subscribe Pattern

ROS2 uses anonymous publish/subscribe: publishers push messages to topics, subscribers pull from topics, and neither side knows who is on the other end. The DDS middleware layer handles discovery (finding who's publishing what), serialization (converting structs to bytes), and transport (shared memory on one machine, UDP across a network).

```
PUBLISH / SUBSCRIBE MODEL
================================================================

  Publisher Node                          Subscriber Node(s)
  ┌──────────────┐                        ┌──────────────┐
  │ hailo_       │   Detection2DArray     │ lab_7 state  │
  │ detection    │──── /detections ──────>│ machine      │
  └──────────────┘                        └──────────────┘
                                          ┌──────────────┐
                           (same topic)──>│ RViz (debug) │
                                          └──────────────┘

  One publisher, many subscribers — all decoupled.
  Adding RViz for debugging doesn't change hailo_detection at all.
```

### The Full Pupper v3 Node Graph (All 7 Labs)

Here is the complete ROS2 node and topic graph when all systems are active (Lab 7 full stack). Each lab adds new nodes incrementally — the graph grows but never breaks:

```
PUPPER v3 COMPLETE ROS2 NODE GRAPH
================================================================

  ┌─────────────────────────────────────────────────────────────────┐
  │                    HARDWARE LAYER                               │
  │  Motors (12× servos via CAN)    IMU (BNO086)    Camera (USB)   │
  │  Microphone (USB)               Speaker (I2S)                  │
  └──────┬──────────────────────────┬──────────────────┬───────────┘
         │                          │                  │
         ▼                          ▼                  ▼
  ┌──────────────┐          ┌──────────────┐   ┌──────────────────┐
  │ ros2_control │          │forward_command│   │ camera_driver    │
  │ hardware     │          │_controller   │   │ (v4l2)           │
  │ interface    │          │              │   │                  │
  └──────┬───────┘          └──────┬───────┘   └────────┬─────────┘
         │                         │                    │
         │ /joint_states           │ effort commands    │ /camera/image_raw
         │ (JointState)            │ (Float64Multi      │ (Image)
         │ 200 Hz                  │  Array)            │ 30 Hz
         ▼                         │                    ▼
  ┌──────────────────┐             │            ┌──────────────────┐
  │                  │◄────────────┘            │  hailo_detection │
  │  PD Controller   │                          │  (Lab 7)         │
  │  Node (Lab 1)    │                          │  YOLOv5 on Hailo │
  │                  │                          │  AI accelerator  │
  │  200 Hz loop     │                          │  ~5 Hz           │
  │  τ = Kp(e) +     │                          └──┬──────────┬────┘
  │      Kd(ė)       │                             │          │
  └──────────────────┘                             │          │
         ▲                                         │          │
         │ /joint_position_targets                 │          │
         │ (Float64MultiArray)                     │          │
         │                                         │          │
    ┌────┴────────────────────────────┐            │          │
    │         SOURCES OF JOINT TARGETS│            │          │
    │  (only one active at a time)    │            │          │
    │                                 │            │          │
    │  ┌──────────────┐               │            │          │
    │  │ IK Node      │ Lab 3: 20 Hz  │            │          │
    │  │ gradient     │ FK+IK         │            │          │
    │  │ descent      │               │            │          │
    │  └──────────────┘               │            │          │
    │                                 │            │          │
    │  ┌──────────────┐               │            │          │
    │  │ Gait Node    │ Lab 4: 20 Hz  │            │          │
    │  │ trot pattern │ FK+IK all legs│            │          │
    │  └──────────────┘               │            │          │
    │                                 │            │          │
    │  ┌──────────────┐               │            │          │
    │  │ Neural       │ Lab 5: ~50 Hz │            │          │
    │  │ Controller   │◄──────────────┼────────────┼──────┐   │
    │  │ (RL policy)  │  /cmd_vel     │            │      │   │
    │  └──────────────┘  (Twist)      │            │      │   │
    └─────────────────────────────────┘            │      │   │
                                                   │      │   │
                                                   │      │   │
         /detections (Detection2DArray) ◄──────────┘      │   │
         ~5 Hz                                            │   │
         │                                                │   │
         ▼                                                │   │
  ┌──────────────────┐     /cmd_vel (Twist)               │   │
  │  Lab 7 State     │────────────────────────────────────┘   │
  │  Machine         │     20 Hz                              │
  │                  │                                        │
  │  IDLE → SEARCH   │                                        │
  │  → TRACK         │     /tracking_control (String)         │
  │                  │◄───────────────────────────────────┐   │
  └──────────────────┘                                    │   │
                                                          │   │
  ┌──────────────────┐     /gpt4_response_topic (String)  │   │
  │  realtime_voice  │─────────────────────────────┐      │   │
  │  (Lab 6)         │                             │      │   │
  │  OpenAI WebSocket│     /tracking_control  ─────┼──────┘   │
  │  24kHz audio     │─────  (String)              │          │
  └──────────────────┘                             ▼          │
                                            ┌──────────────┐  │
                                            │ Karel        │  │
                                            │ Command      │  │
                                            │ Parser       │  │
                                            │ (Labs 6-7)   │──┘
                                            │              │ /annotated_image
                                            └──────────────┘   (Image, debug)
```

### Topic Reference Table

| Topic | Message Type | Publisher(s) | Subscriber(s) | Rate | Lab |
|-------|-------------|-------------|---------------|------|-----|
| `/joint_states` | `sensor_msgs/JointState` | ros2_control hardware interface | PD controller, FK node | 200 Hz | 1+ |
| `/joint_position_targets` | `std_msgs/Float64MultiArray` | IK node, Gait node, Neural controller | PD controller (forward_command_controller) | 20-50 Hz | 1+ |
| `/cmd_vel` | `geometry_msgs/Twist` | Lab 7 state machine, Karel parser, teleop | Neural controller | 20 Hz | 5+ |
| `/detections` | `vision_msgs/Detection2DArray` | hailo_detection | Lab 7 state machine | ~5 Hz | 7 |
| `/tracking_control` | `std_msgs/String` | realtime_voice / Karel | hailo_detection (filter), Lab 7 state machine | event | 7 |
| `/gpt4_response_topic` | `std_msgs/String` | realtime_voice | Karel command parser | event | 6+ |
| `/camera/image_raw` | `sensor_msgs/Image` | [[quick-context/camera-fundamentals|camera]] driver | hailo_detection | 30 Hz | 7 |
| `/annotated_image` | `sensor_msgs/Image` | hailo_detection | RViz (debug) | ~5 Hz | 7 |
| RViz marker topic | `visualization_msgs/Marker` | FK node (green sphere) | RViz | 20 Hz | 2 |

### YAML Configuration and ros2_control

The `forward_command_controller` from the ros2_control framework is the bridge between ROS2 topics and the actual motor hardware. It is configured via YAML files that define:

```yaml
# Simplified example from Lab 1 config
controller_manager:
  ros__parameters:
    update_rate: 200  # Hz — PD loop rate

forward_command_controller:
  ros__parameters:
    joints:
      - leg_front_l_1
      - leg_front_l_2
      - leg_front_l_3
      # ... all 12 joints
    interface_name: effort   # torque control mode
    kp: [5.0, 5.0, 5.0]     # proportional gains
    kd: [0.1, 0.1, 0.1]     # derivative gains
```

This config tells ros2_control which joints exist, what command interface to use (effort = torque, position = angle), and what PD gains to apply. The controller reads `Float64MultiArray` messages from a topic and writes effort commands to the hardware interface, which sends them over CAN to the servos.

</details>

<details>
<summary><strong>The Key Tension</strong> — Real-time vs. flexibility</summary>

ROS2 provides extraordinary flexibility — any node can talk to any other node, you can add or remove nodes at runtime, and the same code runs on a laptop or an embedded Pi. But this flexibility comes at a cost: **DDS middleware introduces non-deterministic latency** that makes it unsuitable for hard real-time control.

### The Latency Problem

Every ROS2 message traverses a stack of software layers:

```
MESSAGE LATENCY BREAKDOWN (approximate)
================================================================

  User code: serialize message           ~5 μs
  ROS2 middleware: rmw layer             ~10 μs
  DDS implementation: discovery/routing  ~20-100 μs
  Transport: shared memory or UDP        ~5-50 μs
  DDS on receiver: deserialize           ~20-100 μs
  ROS2 middleware: callback dispatch     ~10 μs
  ──────────────────────────────────────────────
  Total: ~70-300 μs typical
  Worst case (GC, context switch): 1-5 ms

  For 200 Hz control (5 ms period): usually fine
  For 1000 Hz motor loop (1 ms period): UNACCEPTABLE
```

A 1-5 ms spike might seem small, but at a 1 kHz control loop, a single late message means the motor holds its previous command for an extra millisecond. For a balancing robot, this causes jitter that accumulates into oscillation and falling.

### The Pupper Solution: Split the Architecture

This is why the Pupper v3 uses a **two-tier architecture** that assigns each control loop to the right layer:

```
CONTROL FREQUENCY TIERS
================================================================

  TIER 1: STM32 Bare-Metal         TIER 2: ROS2 on Raspberry Pi
  (No OS, no middleware)            (Linux + DDS middleware)
  ──────────────────────           ──────────────────────────────
  1000 Hz motor current loop       200 Hz PD joint controller
  1000 Hz CAN bus TX/RX            50 Hz neural policy inference
  1000 Hz IMU read                 20 Hz IK solver
                                   5 Hz vision detection
  Latency: <10 μs                  Latency: ~100 μs–5 ms
  Jitter: <1 μs                    Jitter: ~50 μs–2 ms

  HARD REAL-TIME                   SOFT REAL-TIME
  "never miss a deadline"          "usually meets deadlines"
```

The [[micro-context/stm32-microcontroller|STM32]] microcontrollers handle everything that must happen every millisecond without exception — current regulation, encoder reading, CAN communication. ROS2 on the Pi handles everything above 5 ms period — joint-level PD control, trajectory planning, neural network inference, vision, voice. The ros2_control `forward_command_controller` sits at the boundary: it runs as a ROS2 node but communicates with the STM32 hardware interface over [[micro-context/spi|SPI]] at a fixed rate.

This split explains a recurring pattern in the labs: **you never write code that directly talks to motors**. Your ROS2 nodes publish joint targets or velocity commands, and the ros2_control + STM32 stack translates those into actual motor current at rates your ROS2 node could never sustain reliably.

### Why Not ROS1?

ROS2 replaced ROS1 specifically to improve real-time capabilities. ROS1 used a centralized `roscore` master — if it crashed, the entire robot went down. ROS2's DDS layer is fully distributed with no single point of failure. ROS2 also adds QoS (Quality of Service) profiles that let you choose between reliable delivery (every message arrives, possibly late) and best-effort delivery (messages may drop, but never stale). The neural controller uses best-effort QoS because a dropped velocity command is better than a stale one.

</details>

<details>
<summary><strong>Concrete Example</strong> — Message flow for a velocity command</summary>

Here's the exact sequence of events when you publish a `Twist` message to make Pupper walk forward. This traces through the full Lab 5+ stack, showing every topic and message type at each hop.

### Step-by-Step Trace

```
VELOCITY COMMAND → MOTOR TORQUE (Full Message Trace)
================================================================

  STEP 1: ORIGIN — User or state machine publishes Twist
  ─────────────────────────────────────────────────────

  Source: Lab 7 state machine (or teleop keyboard, or Karel)

  Topic: /cmd_vel
  Type:  geometry_msgs/msg/Twist
  Content:
    linear:
      x: 0.3    # forward velocity (m/s)
      y: 0.0
      z: 0.0
    angular:
      x: 0.0
      y: 0.0
      z: 0.0    # no turning
  Rate: 20 Hz


  STEP 2: NEURAL CONTROLLER — Policy network inference
  ─────────────────────────────────────────────────────

  Node: neural_controller (Lab 5)
  Subscribes to: /cmd_vel (Twist)
  Also reads:    /joint_states (JointState) — current positions/velocities

  Processing:
    1. Construct observation vector:
       obs = [cmd_vel.linear.x,       # commanded forward speed
              cmd_vel.linear.y,       # commanded lateral speed
              cmd_vel.angular.z,      # commanded yaw rate
              joint_positions[0:12],  # current joint angles
              joint_velocities[0:12], # current joint velocities
              imu_orientation[0:4],   # quaternion from IMU
              gravity_vector[0:3]]    # projected gravity
    2. Feed through neural network (MLP, ~50 μs inference)
    3. Output: 12 joint position targets (radians)

  Publishes to: /joint_position_targets
  Type: std_msgs/msg/Float64MultiArray
  Content:
    data: [0.1, -0.4, 0.8,    # front-left hip, thigh, calf
           0.1,  0.4, -0.8,   # front-right
          -0.1, -0.4, 0.8,    # back-left
          -0.1,  0.4, -0.8]   # back-right
  Rate: ~50 Hz (520 Hz / repeat_action=10)


  STEP 3: FORWARD COMMAND CONTROLLER — ros2_control bridge
  ─────────────────────────────────────────────────────────

  Node: forward_command_controller (ros2_control)
  Subscribes to: /joint_position_targets (Float64MultiArray)
  Reads config: YAML (kp, kd, joint names, interfaces)

  Processing:
    For each joint i:
      error     = target[i] - current_position[i]
      error_dot = 0 - current_velocity[i]
      torque[i] = kp[i] * error + kd[i] * error_dot
      torque[i] = clamp(torque[i], -3.0, 3.0)  # safety limit

  Writes to: ros2_control hardware interface
  Rate: 200 Hz


  STEP 4: HARDWARE INTERFACE → STM32 → CAN → MOTORS
  ──────────────────────────────────────────────────

  The ros2_control hardware interface sends torque commands
  over SPI to the STM32 Motor MCU (U5), which packages
  them into CAN messages for each servo.

  ┌────────────┐  SPI   ┌────────┐  CAN   ┌─────────┐
  │ Raspberry  │───────>│ STM32  │───────>│ Servo   │
  │ Pi (ROS2)  │  1MHz  │ U5     │  1Mbps │ Motors  │
  │            │        │ 1kHz   │        │ ×12     │
  └────────────┘        └────────┘        └─────────┘

  The STM32 runs its own 1 kHz current control loop
  on top of the position targets — this is below the
  ROS2 abstraction layer.
```

### Why This Layering Matters

Notice how the `Twist` message (a human-readable velocity in m/s) gets progressively transformed:

```
ABSTRACTION LAYERS
================================================================

  /cmd_vel              Twist        "walk forward at 0.3 m/s"
      │                              (semantic intent)
      ▼
  neural_controller     inference    obs → policy(obs) → actions
      │                              (learned mapping)
      ▼
  /joint_position_      Float64      [0.1, -0.4, 0.8, ...]
  targets               MultiArray   (12 joint angles in radians)
      │                              (geometric configuration)
      ▼
  PD controller         torque calc  τ = Kp·e + Kd·ė
      │                              (control law)
      ▼
  hardware interface    SPI bytes    raw register writes
      │                              (protocol encoding)
      ▼
  STM32 + CAN          PWM current  milliamp-level commands
                                     (electrical actuation)
```

Each layer only knows about its immediate inputs and outputs. The neural controller doesn't know about CAN buses. The STM32 doesn't know about Twist messages. This separation is what makes the system maintainable — you can swap the neural controller for a hand-tuned gait (Lab 4) or an IK solver (Lab 3) by changing which node publishes to `/joint_position_targets`, and nothing downstream changes.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **DDS (Data Distribution Service)** — The underlying communication standard ROS2 is built on. DDS provides automatic peer discovery, configurable QoS policies, and supports both shared-memory (same machine) and UDP (network) transport. The default DDS implementation on the Pi is Fast-DDS (eProsima). You rarely interact with DDS directly — ROS2 wraps it — but understanding DDS explains why ROS2 can discover nodes without a central server.

- **QoS Profiles (Quality of Service)** — ROS2 lets you configure reliability, durability, and history depth per topic. The two most common profiles on Pupper: **best-effort** (used for `/cmd_vel`, `/joint_states` — drop stale messages rather than queue them) and **reliable** (used for `/tracking_control` — ensure every command arrives). Mismatched QoS between publisher and subscriber is the #1 cause of "my subscriber never receives messages" bugs.

- **ros2_control Framework** — The standardized interface between ROS2 nodes and robot hardware. Defines `HardwareInterface` (reads/writes to physical actuators), `Controller` (implements control laws), and `ControllerManager` (loads and switches controllers at runtime). Pupper uses `forward_command_controller` to bridge ROS2 topics to motor commands. See the YAML config files in each lab for interface definitions.

- **colcon Build System** — The build tool for ROS2 workspaces. `colcon build` compiles all packages in a workspace, resolving dependencies automatically. `source install/setup.bash` loads the built packages into your environment. Most lab code is Python (no compilation needed), but the ros2_control hardware interface and C++ nodes require building.

- **Launch Files** — Python scripts (`.launch.py`) that orchestrate multi-node startup. A typical lab launch file: loads YAML parameters, starts the controller manager, spawns the forward_command_controller, starts the student's node, and optionally starts RViz. Lab 7's launch file starts 5+ nodes simultaneously.

- **RViz** — ROS2's 3D visualization tool. Lab 2 uses it to display a green sphere marker at the FK-computed foot position. Lab 7 can display annotated camera images and detection bounding boxes. RViz subscribes to standard message types (`Marker`, `Image`, `PointCloud2`) and renders them in a 3D viewport — useful for debugging without physical hardware.

- **rosbag** — Records and replays ROS2 topic data. `ros2 bag record /joint_states /cmd_vel` captures all messages with timestamps; `ros2 bag play` replays them. Essential for debugging: record a failed walking attempt, then replay the data through your analysis nodes offline without needing the physical robot.

- **[[quick-context/pupper-brain]]** — The dual-STM32 + Raspberry Pi hardware architecture. The STM32s handle the 1 kHz loops below the ROS2 layer; the Pi runs ROS2 nodes for everything above. Understanding the hardware split explains why certain control loops are in ROS2 and others are not.

- **[[quick-context/pupper-v3-labs]]** — The 7-lab CS123 curriculum. Each lab adds ROS2 nodes to the graph: Lab 1 (PD controller), Lab 2 (FK + RViz marker), Lab 3 (IK node), Lab 4 (gait node), Lab 5 (neural controller subscribing to `/cmd_vel`), Lab 6 (realtime_voice publishing to `/gpt4_response_topic`), Lab 7 (hailo_detection + state machine + `/tracking_control`).

- **[[quick-context/pupper-bom-control-board]]** — The physical hardware that ros2_control's hardware interface talks to. The SPI connection to the STM32, the CAN transceivers to the servos, and the IMU that provides orientation data to `/joint_states` are all components on this board.

</details>

<details>
<summary><strong>Deep Dive: All 6 Node Communication Interfaces</strong></summary>

ROS 2 provides six distinct communication mechanisms, each optimized for different interaction patterns. The Pupper labs primarily use Topics (pub/sub), but the full set gives you the vocabulary for any distributed robotics system.

### 1. Topics — Pub/Sub for Continuous Data Streams

Topics provide **asynchronous, one-to-many message broadcasting**. This is the backbone of the Pupper system — `/joint_states`, `/cmd_vel`, `/detections` are all topics.

**Quality of Service (QoS) profiles** control delivery across six dimensions:

| QoS Policy | Options | Pupper Usage |
|------------|---------|-------------|
| **Reliability** | RELIABLE (retransmit) / BEST_EFFORT (drop) | `/cmd_vel` uses BEST_EFFORT — stale commands are worse than dropped ones |
| **Durability** | TRANSIENT_LOCAL (late joiners get last msg) / VOLATILE | Map data uses TRANSIENT_LOCAL |
| **History** | KEEP_LAST(N) / KEEP_ALL | Sensor topics use KEEP_LAST(5) |
| **Deadline** | Max period between messages | Safety-critical topics set deadlines |
| **Lifespan** | Max message age before expiry | Prevents processing stale detections |
| **Liveliness** | AUTOMATIC / MANUAL_BY_TOPIC | Detects crashed publishers |

QoS compatibility follows a "request vs offered" model — connections form only when subscriber requirements are met by publisher offerings. **Mismatched QoS is the #1 cause of "my subscriber never receives messages" bugs.**

**QoS recipe cheat sheet:** sensor data → BEST_EFFORT + VOLATILE + KEEP_LAST(5); map/latched data → RELIABLE + TRANSIENT_LOCAL + KEEP_LAST(1); safety-critical → RELIABLE + deadline + liveliness configured.

**Publisher with full QoS configuration:**
```python
from rclpy.qos import (
    QoSProfile, ReliabilityPolicy, DurabilityPolicy,
    HistoryPolicy, LivelinessPolicy,
)
from rclpy.duration import Duration

qos_profile = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    history=HistoryPolicy.KEEP_LAST,
    depth=10,
    deadline=Duration(seconds=1),
    lifespan=Duration(seconds=5),
    liveliness=LivelinessPolicy.AUTOMATIC,
    liveliness_lease_duration=Duration(seconds=10),
)
self.publisher_ = self.create_publisher(String, 'sensor_topic', qos_profile)
```

**Subscriber with QoS event callbacks** (detect deadline misses, liveliness changes, incompatible QoS):
```python
from rclpy.event_handler import (
    QoSRequestedDeadlineMissedInfo,
    QoSLivelinessChangedInfo,
    QoSRequestedIncompatibleQoSInfo,
    SubscriptionEventCallbacks,
)

event_callbacks = SubscriptionEventCallbacks(
    deadline=self.on_deadline_missed,
    liveliness=self.on_liveliness_changed,
    incompatible_qos=self.on_incompatible_qos,
)
self.subscription = self.create_subscription(
    String, 'sensor_topic', self.listener_callback,
    qos_profile, event_callbacks=event_callbacks,
)

def on_deadline_missed(self, event: QoSRequestedDeadlineMissedInfo):
    self.get_logger().warn(f'Deadline missed! total={event.total_count}')

def on_incompatible_qos(self, event: QoSRequestedIncompatibleQoSInfo):
    self.get_logger().error(f'Incompatible QoS! policy_kind={event.last_policy_kind}')
```

**Custom message definition** (`my_robot_interfaces/msg/SensorData.msg`):
```
std_msgs/Header header
float64 temperature
float64 humidity
float64[3] acceleration
string sensor_id
bool is_valid
```

### 2. Services — Synchronous Request/Reply for Quick Operations

Services provide **1-to-1 request/response RPC** with guaranteed delivery. Use for short-lived operations under ~1 second: parameter queries, mode changes, triggering computations.

```python
# Server
from example_interfaces.srv import AddTwoInts

class AddServer(Node):
    def __init__(self):
        super().__init__('add_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.callback)

    def callback(self, request, response):
        response.sum = request.a + request.b
        return response
```

```python
# Async client (recommended — synchronous call() deadlocks without separate spin thread!)
class AddClientAsync(Node):
    def __init__(self):
        super().__init__('add_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

    def send_request(self, a: int, b: int):
        request = AddTwoInts.Request()
        request.a, request.b = a, b
        self.future = self.cli.call_async(request)
        self.future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        self.get_logger().info(f'Result: {future.result().sum}')
```

**Critical warning:** The synchronous `client.call()` method will **silently deadlock** unless `rclpy.spin()` runs on a separate thread. Always prefer `call_async()`.

### 3. Actions — Long-Running Tasks with Feedback and Cancellation

Actions combine services and topics for tasks taking >1 second. They provide **progress feedback**, **cancellation**, and a **goal state machine** (ACCEPTED → EXECUTING → SUCCEEDED/CANCELED/ABORTED). Under the hood: 3 services + 2 topics.

```python
# Action server with goal acceptance, cancellation, and feedback
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from action_tutorials_interfaces.action import Fibonacci

class FibonacciServer(Node):
    def __init__(self):
        super().__init__('fibonacci_server')
        self._action_server = ActionServer(
            self, Fibonacci, 'fibonacci',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=ReentrantCallbackGroup(),
        )

    def goal_callback(self, goal_request):
        return GoalResponse.REJECT if goal_request.order < 0 else GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        return CancelResponse.ACCEPT  # Default is REJECT!

    def execute_callback(self, goal_handle):
        feedback = Fibonacci.Feedback()
        feedback.partial_sequence = [0, 1]
        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = Fibonacci.Result()
                result.sequence = feedback.partial_sequence
                return result
            feedback.partial_sequence.append(
                feedback.partial_sequence[i] + feedback.partial_sequence[i - 1])
            goal_handle.publish_feedback(feedback)
            time.sleep(1)
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback.partial_sequence
        return result
```

```python
# Action client with feedback and cancellation
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus

class FibonacciClient(Node):
    def __init__(self):
        super().__init__('fibonacci_client')
        self._client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order: int):
        self._client.wait_for_server()
        goal = Fibonacci.Goal()
        goal.order = order
        future = self._client.send_goal_async(
            goal, feedback_callback=self.feedback_cb)
        future.add_done_callback(self.goal_response_cb)

    def goal_response_cb(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            return
        self._goal_handle = goal_handle
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_cb)

    def feedback_cb(self, feedback_msg):
        self.get_logger().info(f'Feedback: {list(feedback_msg.feedback.partial_sequence)}')

    def result_cb(self, future):
        status = future.result().status
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f'Succeeded: {list(future.result().result.sequence)}')
```

### 4. Parameters — Dynamic Node Configuration

Parameters expose named, typed configuration values that can be queried, set, and monitored at runtime. They support descriptors with value ranges and validation callbacks.

```python
from rcl_interfaces.msg import (
    ParameterDescriptor, SetParametersResult, FloatingPointRange,
)

class ParameterNode(Node):
    def __init__(self):
        super().__init__('param_node')
        self.declare_parameter('max_speed', 2.0, ParameterDescriptor(
            description='Maximum speed in m/s',
            floating_point_range=[FloatingPointRange(
                from_value=0.0, to_value=10.0, step=0.1)]))
        self._max_speed = self.get_parameter('max_speed').value
        self.add_on_set_parameters_callback(self._validate)

    def _validate(self, params: list) -> SetParametersResult:
        for p in params:
            if p.name == 'max_speed' and p.value < 0.0:
                return SetParametersResult(
                    successful=False, reason='max_speed must be >= 0')
            if p.name == 'max_speed':
                self._max_speed = p.value
        return SetParametersResult(successful=True)
```

Set at runtime: `ros2 param set /param_node max_speed 5.0`

### 5. Component Composition — Multiple Nodes in One Process

Python nodes can share a process with a common executor, avoiding inter-process network overhead. FastDDS automatically uses **shared memory transport** for same-host communication. True **zero-copy intra-process** communication (pointer passing without serialization) is a **C++ rclcpp-only feature** via `NodeOptions().use_intra_process_comms(true)`. Python always serializes through DDS.

```python
from rclpy.executors import MultiThreadedExecutor

def main():
    rclpy.init()
    executor = MultiThreadedExecutor(num_threads=4)
    nodes = [ProducerNode(), ProcessorNode(), SinkNode()]
    for n in nodes:
        executor.add_node(n)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        for n in nodes:
            n.destroy_node()
        rclpy.shutdown()
```

### 6. Lifecycle Nodes — Managed State Transitions

Lifecycle nodes add a state machine (**Unconfigured → Inactive → Active → Finalized**) with transition callbacks. `LifecyclePublisher` automatically enables/disables with state transitions.

```python
from rclpy.lifecycle import LifecycleNode, LifecycleState, TransitionCallbackReturn

class MyLifecycleNode(LifecycleNode):
    def __init__(self):
        super().__init__('my_lifecycle_node')
        self._pub = None

    def on_configure(self, state: LifecycleState) -> TransitionCallbackReturn:
        self._pub = self.create_lifecycle_publisher(String, 'lifecycle_chatter', 10)
        self._timer = self.create_timer(1.0, self._publish, autostart=False)
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: LifecycleState) -> TransitionCallbackReturn:
        if self._timer:
            self._timer.reset()
        return super().on_activate(state)

    def on_deactivate(self, state: LifecycleState) -> TransitionCallbackReturn:
        if self._timer:
            self._timer.cancel()
        return super().on_deactivate(state)

    def on_cleanup(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.destroy_timer(self._timer)
        self.destroy_lifecycle_publisher(self._pub)
        return TransitionCallbackReturn.SUCCESS
```

### When to Choose Each Mechanism

| Feature | Topic | Service | Action |
|---------|-------|---------|--------|
| Direction | 1→N broadcast | 1↔1 RPC | 1↔1 + feedback stream |
| Blocking? | No | Client waits | Non-blocking (async) |
| Feedback? | N/A | No | Yes |
| Cancellable? | N/A | No | Yes |
| QoS tuning? | Full 6-policy | Limited | Internal defaults |
| Typical duration | Continuous | < 1 second | Seconds to minutes |

**Decision rule:** continuous data → Topic; quick request/reply → Service; long-running cancellable task → Action; runtime config → Parameters; performance-critical same-process → Composition; coordinated startup → Lifecycle.

</details>

<details>
<summary><strong>Deep Dive: The Launch System</strong></summary>

The launch system orchestrates multi-node deployments with namespacing, remapping, parameter injection, conditional logic, and lifecycle management — all from Python launch files.

### Groups and Namespaces

`GroupAction` creates scoped contexts where `PushRosNamespace` applies only within the group. This enables clean multi-robot or multi-subsystem deployments:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushRosNamespace

def generate_launch_description():
    robot_ns_arg = DeclareLaunchArgument(
        'robot_ns', default_value='robot1')

    sensor_group = GroupAction(actions=[
        PushRosNamespace(LaunchConfiguration('robot_ns')),
        PushRosNamespace('sensors'),
        Node(package='demo_nodes_cpp', executable='talker',
             name='camera_node', output='screen',
             parameters=[{'frame_rate': 30.0}],
             remappings=[('chatter', 'image_raw')]),
        Node(package='demo_nodes_cpp', executable='talker',
             name='lidar_node', output='screen',
             remappings=[('chatter', 'scan')]),
    ])

    return LaunchDescription([robot_ns_arg, sensor_group])
```

Run with `robot_ns:=my_robot` → creates nodes at `/my_robot/sensors/camera_node`, `/my_robot/sensors/lidar_node`.

### Topic Remapping

```python
# The first element is the node's internal topic name; the second is the runtime name
talker = Node(
    package='demo_nodes_cpp', executable='talker', name='my_talker',
    remappings=[('chatter', 'my_chatter')])
```

Use relative names (`'chatter'`) for relative remapping and absolute names (`'/input/pose'`) for fully-qualified remapping. `SetRemap` applies global remaps to all nodes within a `GroupAction`.

### Setting Parameters at Launch

The `parameters` argument accepts dictionaries (inline) and/or file paths (YAML). Later values override earlier ones:

```python
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

node = Node(
    package='turtlesim', executable='turtlesim_node',
    parameters=[
        PathJoinSubstitution([
            FindPackageShare('launch_tutorial'), 'config', 'turtlesim.yaml']),
        {'background_r': 255, 'background_g': 0},  # overrides YAML values
    ])
```

**YAML parameter file format:**
```yaml
/turtlesim1/sim:
  ros__parameters:         # double underscore is mandatory
    background_r: 150
    camera:
      width: 640           # accessed as camera.width
      height: 480

/**:                       # wildcard — applies to any node loading this file
  ros__parameters:
    use_sim_time: false
```

### Conditional Logic

`IfCondition`, `UnlessCondition`, and `PythonExpression` control which nodes launch:

```python
from launch.conditions import IfCondition, UnlessCondition, LaunchConfigurationEquals
from launch.substitutions import LaunchConfiguration, PythonExpression

rviz = Node(package='rviz2', executable='rviz2',
            condition=IfCondition(LaunchConfiguration('use_rviz')))

hw_driver = Node(package='my_pkg', executable='hw_driver',
                 condition=UnlessCondition(LaunchConfiguration('use_sim_time')))

camera3 = Node(package='my_pkg', executable='cam3',
               condition=IfCondition(PythonExpression([
                   LaunchConfiguration('num_cameras'), ' >= 3'])))

diff_ctrl = Node(package='my_pkg', executable='diff_ctrl',
                 condition=LaunchConfigurationEquals('robot_type', 'differential'))
```

### Lifecycle Orchestration with Chained Event Handlers

The most powerful launch pattern: lifecycle nodes are sequentially configured and activated using `OnStateTransition` event handlers. Node B activates only after Node A reaches `active`:

```python
import lifecycle_msgs.msg
from launch.actions import EmitEvent, RegisterEventHandler
from launch.events import matches_action
from launch_ros.actions import LifecycleNode
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState

node_a = LifecycleNode(name='talker', namespace='', package='lifecycle',
                        executable='lifecycle_talker')

# node_a reaches inactive → activate it
on_a_inactive = RegisterEventHandler(OnStateTransition(
    target_lifecycle_node=node_a, goal_state='inactive',
    entities=[
        EmitEvent(event=ChangeState(
            lifecycle_node_matcher=matches_action(node_a),
            transition_id=lifecycle_msgs.msg.Transition.TRANSITION_ACTIVATE))]))

# node_a reaches active → launch and configure node_b
on_a_active = RegisterEventHandler(OnStateTransition(
    target_lifecycle_node=node_a, goal_state='active',
    entities=[
        node_b,
        EmitEvent(event=ChangeState(
            lifecycle_node_matcher=matches_action(node_b),
            transition_id=lifecycle_msgs.msg.Transition.TRANSITION_CONFIGURE))]))

# Start the chain: configure node_a
configure_a = EmitEvent(event=ChangeState(
    lifecycle_node_matcher=matches_action(node_a),
    transition_id=lifecycle_msgs.msg.Transition.TRANSITION_CONFIGURE))

# Register handlers BEFORE the triggers that produce events
return LaunchDescription([on_a_inactive, on_a_active, node_a, configure_a])
```

Sequence: node_a launches → configure → inactive → activate → active → node_b launches → configure → inactive → activate → active.

</details>

<details>
<summary><strong>Deep Dive: Concurrency, Executors & Race Conditions</strong></summary>

ROS 2's concurrency model revolves around **executors** and **callback groups**. Understanding these is essential to avoiding race conditions.

### Executors Control Callback Scheduling

```
EXECUTOR TYPES
================================================================

  SingleThreadedExecutor (default with rclpy.spin())
  ├── All callbacks serialized — never overlap
  ├── No thread-safety concerns
  └── A long callback blocks EVERYTHING

  MultiThreadedExecutor
  ├── Configurable thread pool
  ├── Callbacks run concurrently, governed by callback groups
  └── Required when a callback must wait for another callback

  EventsExecutor (Rolling, experimental)
  ├── Event-driven instead of polling
  └── ~1/10th CPU usage for idle nodes
```

```python
from rclpy.executors import MultiThreadedExecutor

executor = MultiThreadedExecutor(num_threads=4)
executor.add_node(my_node)
executor.spin()
```

### Callback Groups — The Primary Concurrency Control

**MutuallyExclusiveCallbackGroup** (the default): at most **one** callback from the group runs at any time. No locking needed for shared state within the group.

**ReentrantCallbackGroup**: **any number** of callbacks run simultaneously. You **must** use explicit locks for shared state.

**Critical rule:** mutual exclusion is *within* a group only. Callbacks in *different* MutuallyExclusiveCallbackGroups **can** run in parallel with each other.

```python
import threading
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup

class SharedStateNode(Node):
    def __init__(self):
        super().__init__('shared_state_node')
        self.counter = 0
        self.lock = threading.Lock()

        # Approach 1: MutuallyExclusive — no lock needed
        self.mutex_group = MutuallyExclusiveCallbackGroup()
        self.create_subscription(Int32, 'input_a', self.mutex_cb, 10,
                                 callback_group=self.mutex_group)
        self.create_timer(2.0, self.mutex_timer, callback_group=self.mutex_group)

        # Approach 2: Reentrant — lock required
        self.reentrant_group = ReentrantCallbackGroup()
        self.create_subscription(Int32, 'input_b', self.reentrant_cb, 10,
                                 callback_group=self.reentrant_group)

    def mutex_cb(self, msg):
        self.counter += msg.data  # safe: serialized by group

    def reentrant_cb(self, msg):
        with self.lock:
            self.counter += msg.data  # must lock: concurrent execution possible
```

### Message Filters — Synchronize Data Across Topics

When processing data from multiple sensors, messages arrive at different times:

```python
import message_filters
from sensor_msgs.msg import Image, PointCloud2

class SyncNode(Node):
    def __init__(self):
        super().__init__('sync_node')

        # Exact sync: identical timestamps only
        self.img_sub = message_filters.Subscriber(self, Image, '/camera/image_raw')
        self.info_sub = message_filters.Subscriber(self, CameraInfo, '/camera/camera_info')
        self.exact_sync = message_filters.TimeSynchronizer(
            [self.img_sub, self.info_sub], queue_size=10)
        self.exact_sync.registerCallback(self.exact_cb)

        # Approximate sync: tolerates up to 100ms difference
        self.cloud_sub = message_filters.Subscriber(self, PointCloud2, '/lidar/points')
        self.approx_sync = message_filters.ApproximateTimeSynchronizer(
            [self.img_sub, self.cloud_sub],
            queue_size=10, slop=0.1)  # 100ms tolerance
        self.approx_sync.registerCallback(self.approx_cb)
```

### The Fundamental Gap: No Global Ordering

ROS 2 provides **per-publisher FIFO ordering** within a single topic but **no global ordering across topics or nodes**. No distributed transactions, no two-phase commit, no vector clocks. Multi-node coordination requiring atomicity must be built at the application level.

**Pattern 1: Chain-of-services** — sequential pipeline where each node calls the next:

```python
class NodeB(Node):
    """Receives request, chains to NodeC, returns combined result."""
    def __init__(self):
        super().__init__('node_b')
        self.group = ReentrantCallbackGroup()
        self.create_service(AddTwoInts, '/service_b', self.handle,
                            callback_group=self.group)
        self.client_c = self.create_client(AddTwoInts, '/service_c',
                                           callback_group=self.group)

    def handle(self, req, resp):
        req_c = AddTwoInts.Request()
        req_c.a, req_c.b = req.a + 10, req.b + 10
        done = Event()
        future = self.client_c.call_async(req_c)
        future.add_done_callback(lambda _: done.set())
        done.wait()
        resp.sum = future.result().sum + 1
        return resp
```

**Pattern 2: Centralized orchestrator** with rollback on failure:

```python
class Orchestrator(Node):
    def run_workflow(self):
        completed = []
        for worker in self.workers:
            result = self.call_sync(self.exec_clients[worker], req)
            if not result or not result.success:
                self.get_logger().error(f'{worker} failed! Rolling back...')
                for rw in reversed(completed):
                    self.call_sync(self.roll_clients[rw], SetBool.Request())
                return
            completed.append(worker)
```

### Priority-Based Execution

For priority differentiation: place high-priority callbacks on a dedicated executor in an OS thread with elevated scheduling priority:

```python
import threading

ctrl = ControlNode()   # 100 Hz control loop
log = LoggingNode()    # 1 Hz logging

hi_exec = SingleThreadedExecutor()
lo_exec = SingleThreadedExecutor()
hi_exec.add_node(ctrl)
lo_exec.add_node(log)

t_hi = threading.Thread(target=hi_exec.spin, daemon=True)
t_lo = threading.Thread(target=lo_exec.spin, daemon=True)
t_hi.start()
t_lo.start()
```

**Real-time limitations in Python:** The GIL prevents true parallel execution. Python's garbage collector introduces non-deterministic latency. For hard real-time, use **rclcpp** with the TLSF allocator for O(1) bounded-time allocation. Python is fine for soft real-time paths: planning, logging, visualization — which is why the Pupper's 1 kHz motor loop runs on bare-metal STM32, not in ROS2 Python.

</details>

<details>
<summary><strong>Deep Dive: Architectural Patterns & Extensibility</strong></summary>

### pluginlib — Runtime Extensibility

ROS 2's `pluginlib` uses `dlopen` to load plugin classes from shared libraries at runtime. Plugins are registered via `PLUGINLIB_EXPORT_CLASS`, declared in XML manifests, and discovered through the ament resource index. The loading application only needs the abstract base class — concrete implementations are resolved at runtime by string name.

The `rclcpp_components` system extends this for entire nodes. Component nodes are built as shared libraries with `RCLCPP_COMPONENTS_REGISTER_NODE`, loaded into a **ComponentManager** container that exposes `load_node`/`unload_node`/`list_nodes` services. Components sharing a process get automatic shared memory transport and, with `use_intra_process_comms: true`, **zero-copy message passing** in C++.

### rosidl — The Type System as Contract

Every `.msg`, `.srv`, `.action` definition acts as a **typed contract** between nodes. The `rosidl` pipeline generates language-specific code (Python classes, C++ structs) and DDS-vendor-specific serialization. Supports:
- Primitives: `bool`, `float64`, `string`
- Fixed arrays: `int32[5]`
- Bounded sequences: `int32[<=5]`
- Bounded strings: `string<=10`
- Nested types, constants, default values

Type compatibility is enforced at the DDS layer through type hashing — a subscriber expecting `sensor_msgs/msg/LaserScan` cannot accidentally receive `geometry_msgs/msg/Twist`.

### Mapping ROS 2 Patterns to Web Platform Design

These patterns transfer directly to web architectures:

| ROS 2 Pattern | Web Equivalent |
|---------------|---------------|
| Topics (pub/sub) | WebSocket channels, RxJS Observables, EventEmitter |
| QoS: TRANSIENT_LOCAL | `shareReplay(1)` in RxJS |
| QoS: deadline | `timeout()` operator |
| QoS: RELIABLE | `retry()` operator |
| `.msg` definitions | TypeScript interfaces, JSON Schema, Protobuf |
| `rosidl` codegen | `protoc`, `json-schema-to-typescript`, OpenAPI codegen |
| Lifecycle nodes | React `constructor` → `componentDidMount` → `componentWillUnmount` |
| `pluginlib` / `dlopen` | Dynamic `import()`, React.lazy + Suspense, Module Federation |
| Namespace isolation | Shadow DOM, CSS modules, scoped state stores |

A web-platform lifecycle manager inspired by ROS 2:

```typescript
abstract class ManagedComponent {
  state: 'unconfigured' | 'inactive' | 'active' | 'finalized' = 'unconfigured';

  abstract onConfigure(): Promise<boolean>;
  abstract onActivate(): Promise<boolean>;
  abstract onDeactivate(): Promise<boolean>;
  abstract onCleanup(): Promise<boolean>;
  abstract onShutdown(): Promise<void>;

  async configure() {
    if (this.state === 'unconfigured' && await this.onConfigure())
      this.state = 'inactive';
  }
  async activate() {
    if (this.state === 'inactive' && await this.onActivate())
      this.state = 'active';
  }
}
```

### Foxglove — ROS 2 Patterns in a Web Visualization Platform

Foxglove Studio implements several ROS 2 architectural patterns in a web context. It connects via **Foxglove Bridge** (`foxglove_bridge`), a C++ node exposing a WebSocket server with binary message streaming — architecturally superior to rosbridge due to binary encoding and lower overhead.

**Extensions** are TypeScript packages compiled as `.foxe` files (ZIP archives), loaded at runtime — directly analogous to ROS 2 component loading. The extension entry point registers panels via `extensionContext.registerPanel()`, mirroring `RCLCPP_COMPONENTS_REGISTER_NODE`.

```typescript
function initMyPanel(context: PanelExtensionContext) {
  context.watch("topics");
  context.watch("currentFrame");
  context.subscribe([{ topic: "/camera/image" }]);

  context.onRender = (renderState, done) => {
    const messages = renderState.currentFrame;
    context.panelElement.innerHTML = `<div>${messages?.length} messages</div>`;
    done();  // MUST call done() to signal render complete
  };

  return () => { /* cleanup */ };
}
```

The pattern correspondence: `create_subscription()` → `context.subscribe()`, `REGISTER_NODE` → `registerPanel()`, lifecycle transitions → `initPanel()` → `onRender` loop → cleanup return, parameters → `context.saveState()`.

### The Transferable Insight

ROS 2's **separation of concerns across three axes** is the most transferable design principle:
1. **Typed contracts** (rosidl) decouple data format from processing logic
2. **Pub/sub topics** decouple producers from consumers
3. **Lifecycle management** decouples component initialization from activation

This combination — typed message bus + managed component lifecycle + dynamic loading via registry + namespace isolation — provides the architectural foundation that scales from simple panels to complex multi-component systems, whether in robotics or web platforms.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** In Lab 5, the neural controller subscribes to `/cmd_vel` (Twist) and `/joint_states` (JointState), then publishes to `/joint_position_targets` (Float64MultiArray). Why does it need both inputs — couldn't it work with just `/cmd_vel`?

<details>
<summary>Answer</summary>

The neural controller needs `/cmd_vel` to know *what* the robot should do (walk forward, turn left) and `/joint_states` to know *what the robot is currently doing* (current joint angles, velocities, body orientation from IMU). A velocity command alone is meaningless without knowing the current state — "walk forward at 0.3 m/s" requires different joint targets depending on whether the robot is mid-stride with the left legs forward or standing still. The RL policy was trained on state-action pairs: the observation vector includes both the command and the full proprioceptive state (12 joint positions, 12 joint velocities, IMU quaternion, projected gravity). Without `/joint_states`, the policy has no feedback and would output open-loop commands that diverge from reality within seconds.
</details>

**Q2:** The Lab 7 state machine publishes `Twist` messages to `/cmd_vel`, and the Karel command parser also publishes `Twist` messages to `/cmd_vel`. What happens if both publish simultaneously, and how does ROS2 handle this?

<details>
<summary>Answer</summary>

ROS2 topics support multiple publishers — the subscriber (neural controller) receives messages from *both* publishers interleaved by arrival time. This means the robot would receive conflicting velocity commands: the state machine might say "rotate to search" while Karel says "move forward." The result is erratic behavior as the neural controller alternates between contradictory commands. In practice, the labs are designed so only one high-level controller is active at a time — the state machine only publishes when tracking is active, and Karel publishes discrete motion commands that complete before the next one starts. But this is a convention, not an enforcement. In production systems, you would use a **cmd_vel_mux** (velocity multiplexer) node that accepts commands from multiple sources with priorities and only forwards the highest-priority active source.
</details>

**Q3:** The PD controller runs at 200 Hz, but the neural controller only publishes new joint targets at ~50 Hz. What does the PD controller do during the 3 out of every 4 cycles when no new target arrives?

<details>
<summary>Answer</summary>

The PD controller holds the last received target and continues applying the PD control law against it. This is a key design pattern in ROS2 robotics: the **high-frequency controller** (200 Hz PD) interpolates between **low-frequency commands** (50 Hz neural policy) by continuously driving the joints toward the most recent target. Each 200 Hz cycle, the PD controller reads fresh joint positions/velocities from `/joint_states` (which updates at 200 Hz from the hardware) and computes $\tau = K_p(q_{target} - q) + K_d(\dot{q}_{target} - \dot{q})$ using the stale target but fresh sensor data. This is why the system stays smooth even though the neural controller is 4x slower — the PD controller acts as a servo loop that tracks whatever target it was last given, rejecting disturbances and maintaining stiffness between neural network updates.
</details>

**Q4:** You create two `MutuallyExclusiveCallbackGroup`s in a node running under `MultiThreadedExecutor`. Callback A is in group 1, callback B is in group 2, and both modify `self.counter`. Is `self.counter` thread-safe? Why or why not?

<details>
<summary>Answer</summary>

**No, it is not thread-safe.** Mutual exclusion is *within* a group only. Callbacks in *different* MutuallyExclusiveCallbackGroups can run in parallel with each other under a MultiThreadedExecutor. So callback A and callback B could execute simultaneously on different threads and race on `self.counter`. You need either: (1) put both callbacks in the *same* MutuallyExclusiveCallbackGroup, or (2) use a `threading.Lock()` to protect the shared state, or (3) use a ReentrantCallbackGroup with explicit locking. This is one of the most common concurrency bugs in ROS 2 — assuming "mutually exclusive" means node-wide when it actually means group-wide.
</details>

**Q5:** Why does `client.call()` (synchronous service call) deadlock under a `SingleThreadedExecutor`, and how does `call_async()` avoid this?

<details>
<summary>Answer</summary>

`client.call()` blocks the calling thread until the response arrives. But under a `SingleThreadedExecutor`, that same thread is the *only* thread processing callbacks — including the callback that would handle the incoming response. The thread is blocked waiting for a response that can never be delivered because the thread that would deliver it is blocked. `call_async()` avoids this by returning a `Future` immediately, allowing `spin()` to continue processing callbacks. When the response arrives, the executor dispatches the done callback. Alternatively, you can use a `MultiThreadedExecutor` where the response can be processed on a different thread than the one blocking on `call()`.
</details>

**Q6:** A publisher uses `RELIABLE` reliability and a subscriber uses `BEST_EFFORT`. Will the connection form? What about the reverse?

<details>
<summary>Answer</summary>

**RELIABLE publisher + BEST_EFFORT subscriber: YES**, the connection forms. The subscriber is requesting less than what the publisher offers — BEST_EFFORT is a weaker requirement that RELIABLE satisfies. **BEST_EFFORT publisher + RELIABLE subscriber: NO**, the connection does NOT form. The subscriber demands guaranteed delivery, but the publisher only offers best-effort. QoS follows a "request vs offered" compatibility model — the subscriber's requirements must be met by the publisher's offerings. This mismatch is the #1 cause of "my subscriber never receives messages" bugs in ROS 2, and `ros2 doctor` or QoS event callbacks (`on_incompatible_qos`) help diagnose it.
</details>

</details>
