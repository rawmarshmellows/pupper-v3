---
topic: Pupper Lab 5 — Neural Controller (Reinforcement Learning)
created: 2026-03-10
updated: 2026-03-12
---

> **Related:** [[learning/notes/micro-context/coriolis-effect]] | [[learning/notes/micro-context/homogeneous-transformation-matrix]] | [[learning/notes/micro-context/spinev1-elf]] | [[learning/notes/quick-context/absolute-orientation]]

# Pupper Lab 5 — Neural Controller (Reinforcement Learning)


> **TL;DR:** Lab 5 replaces the entire hand-tuned PD + FK/IK + gait pipeline from Labs 1-4 with a single neural network policy trained via reinforcement learning in MuJoCo simulation, then deployed to the real Pupper at ~52 Hz to directly output 12 joint position targets — achieving robust locomotion (including three-legged walking and parkour) that would be nearly impossible to hand-engineer.

## Human notes

What are the current best practices in the industry for RL-based robot locomotion? How does Lab 5's approach compare to what production teams and research labs are doing now (2025-2026)?

Expand on: what is the neural network actually trying to predict? What do the tuples $(o_t, a_t, r_t, o_{t+1})$ mean? What are the concrete variables in the observation and action space?

## The Core Problem

Labs 1-4 build a classical robotics stack: PD control drives individual joints (Lab 1), [[learning/notes/quick-context/pupper-lab2-forward-kinematics|forward kinematics]] maps joint angles to foot positions (Lab 2), [[learning/notes/quick-context/pupper-lab3-inverse-kinematics|inverse kinematics]] solves for joint angles given desired foot positions (Lab 3), and a gait controller coordinates all four legs into a trotting pattern (Lab 4). This pipeline works, but it is brittle. Every parameter — step height, stride length, phase offsets, PD gains — is hand-tuned for flat ground. Push the robot, change the surface friction, or remove a leg, and the entire stack breaks down because no part of the pipeline was designed to adapt.

Reinforcement learning offers a fundamentally different approach. Instead of manually specifying *how* the robot should move, you specify *what* good movement looks like (a reward function) and let an optimization algorithm discover the control policy through millions of simulated trials. The policy — a small neural network — learns to map sensor observations (IMU orientation, joint positions, joint velocities, velocity commands) directly to joint position targets. Because training happens in simulation with randomized physics parameters (friction, mass, motor delays), the resulting policy generalizes to conditions it has never explicitly seen, including the real robot.

The sim-to-real gap is the central challenge. A policy that works perfectly in MuJoCo can fail on the real Pupper because simulation never perfectly captures motor dynamics, sensor noise, communication delays, or floor surfaces. Lab 5's approach mitigates this through domain randomization during training — deliberately varying simulation parameters so the policy learns to be robust rather than optimal for any single configuration. The `config.yaml` on the real robot then provides the bridge: PD gains ($K_p = 7.5$, $K_d = 0.25$ for all joints), default joint poses, and timing parameters that match the assumptions baked into the trained policy.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Reinforcement Learning Policy** | A neural network $\pi_\theta(a \mid o)$ that maps an observation vector $o$ to an action vector $a$ (12 joint position targets). Trained by maximizing cumulative reward in simulation using [[quick-context/ppo-proximal-policy-optimization|PPO]]. |
| **Sim-to-Real Transfer** | Deploying a policy trained entirely in simulation to a physical robot. Bridged by domain randomization (varying sim physics) and careful config matching (`config.yaml` gains, timing). |
| **MuJoCo** | Multi-Joint dynamics with Contact — the physics simulator used for training. Provides fast, differentiable contact dynamics essential for generating the millions of rollouts RL requires. |
| **Observation Space** | The vector of sensor readings fed to the policy each inference step: body orientation (from BNO086 IMU), angular velocity, joint positions, joint velocities, and commanded velocity — everything the network needs to decide what to do next. |
| **Action Space** | The 12-dimensional output vector: one position target per joint. These are *not* torques — the lower-level PD controller on the STM32 tracks these targets at the full 520 Hz update rate. |

<details>
<summary><strong>How It Works</strong> — RL policy deployment pipeline</summary>

The pipeline spans two phases: offline training (simulation) and online deployment (real robot).

### What the Neural Network Learns

The neural network is **not** predicting what will happen (that's a dynamics model). It is learning a **policy** — a function that says "given what I currently sense about the world, what joint positions should I command *right now* to maximize long-term walking quality?" Formally, the network $\pi_\theta(a \mid o)$ maps an observation $o$ (what the robot senses) to an action $a$ (12 joint position targets). The "learning" is adjusting the weights $\theta$ so that the actions the policy chooses lead to high cumulative reward over time.

This is fundamentally different from supervised learning. There is no "correct answer" dataset of observation→action pairs. Instead, the robot discovers good actions through trial and error: try something, see how much reward you get, adjust the policy to do more of what worked and less of what didn't.

### The Experience Tuple $(o_t, a_t, r_t, o_{t+1})$

During training, the simulated robot collects **experience tuples** — each one is a single timestep of interaction:

$$\underbrace{(o_t,}_{\text{what I sensed}} \quad \underbrace{a_t,}_{\text{what I did}} \quad \underbrace{r_t,}_{\text{how good it was}} \quad \underbrace{o_{t+1})}_{\text{what happened next}}$$

| Symbol | Meaning | Concrete Pupper Example |
|--------|---------|------------------------|
| $o_t$ | **Observation** at time $t$ — everything the robot can sense | IMU orientation, angular velocity, 12 joint positions, 12 joint velocities, velocity command, previous action |
| $a_t$ | **Action** taken at time $t$ — the policy's output | 12 joint position offsets from default pose (e.g., $[+0.05, -0.02, +0.08, \ldots]$ rad) |
| $r_t$ | **Reward** received for this transition — a scalar score | e.g., $r_t = 0.85$ (good forward tracking) or $r_t = -0.3$ (fell over, energy wasted) |
| $o_{t+1}$ | **Next observation** — the world's response to your action | Updated joint positions/velocities after physics simulation stepped forward |

**How [[learning/notes/quick-context/ppo-proximal-policy-optimization|PPO]] uses these tuples:** Thousands of tuples are collected across parallel simulated robots. PPO estimates the *advantage* — "was this action better or worse than average for this observation?" — and adjusts the policy weights to increase the probability of above-average actions and decrease below-average ones. The clipped surrogate objective prevents any single update from changing the policy too drastically.

```
ONE TRAINING EPISODE (simplified)
================================================================

  t=0         t=1         t=2         t=3      ...  t=T (fell)
  │           │           │           │              │
  o₀──→π──→a₀  o₁──→π──→a₁  o₂──→π──→a₂            │
  │     │      │     │      │     │                  │
  │  physics   │  physics   │  physics               │
  │  step      │  step      │  step                  │
  │     │      │     │      │     │                  │
  └──→r₀,o₁   └──→r₁,o₂   └──→r₂,o₃               │
                                                     │
  Collected: [(o₀,a₀,r₀,o₁), (o₁,a₁,r₁,o₂), ...]  │
                                                     │
  PPO asks: for each tuple, was aₜ better than       │
  average? If yes → increase π(aₜ|oₜ).              │
  If no → decrease it. Repeat for millions of tuples.│
```

### Observation Space — What the Robot Senses

The observation vector $o_t$ is a flat array of floats concatenated in this order:

```
OBSERVATION VECTOR BREAKDOWN (~48 dimensions)
================================================================

  Index   Variable              Dims  Source           Units
  ─────────────────────────────────────────────────────────────
  [0:3]   velocity command      3     joystick/cmd_vel  m/s, m/s, rad/s
          (vx, vy, yaw_rate)          via /cmd_vel

  [3:6]   angular velocity      3     BNO086 IMU        rad/s
          (ωx, ωy, ωz)               body frame

  [6:9]   projected gravity     3     BNO086 IMU        unitless
          (gx, gy, gz)               direction of gravity
                                      in body frame
                                      (≈[0,0,-1] when upright)

  [9:21]  joint position        12    CAN bus encoders   rad
          offsets                     q - q_default
          (q₁-q₁ᵈ, q₂-q₂ᵈ,...)     (centered around 0)

  [21:33] joint velocities      12    CAN bus encoders   rad/s
          (q̇₁, q̇₂, ...)

  [33:45] previous action       12    from last NN       rad
          (aₜ₋₁)                     inference
                                      (helps temporal
                                       smoothness)
```

**Why these specific variables?**
- **Velocity command** tells the policy *what* to do (walk forward, turn left)
- **Angular velocity + projected gravity** tell the policy the body's orientation and how fast it's rotating — essential for balance
- **Joint position offsets** (not raw positions) are centered near zero, which helps the neural network learn faster. The offset from the default standing pose is more informative than the raw angle
- **Joint velocities** tell the policy how fast each joint is currently moving — needed to predict where the joint will be next
- **Previous action** provides temporal context so the policy can produce smooth, continuous motions rather than jerky independent decisions

**What's NOT in the observation (and why):** foot contact sensors (not available on Pupper hardware), terrain heightmap (not available without cameras — this is what the teacher-student pipeline adds via privileged learning), and absolute position/velocity (not available without external tracking). The policy must infer ground contact and terrain from the *pattern* of joint positions and IMU readings.

### Action Space — What the Robot Commands

The action vector $a_t$ is 12 floats — one position offset per joint:

```
ACTION VECTOR BREAKDOWN (12 dimensions)
================================================================

  Index  Joint Name            Leg          Joint Type
  ──────────────────────────────────────────────────────
  [0]    leg_front_r_1        Front-Right   Hip abduction
  [1]    leg_front_r_2        Front-Right   Hip flexion
  [2]    leg_front_r_3        Front-Right   Knee flexion
  [3]    leg_front_l_1        Front-Left    Hip abduction
  [4]    leg_front_l_2        Front-Left    Hip flexion
  [5]    leg_front_l_3        Front-Left    Knee flexion
  [6]    leg_back_r_1         Back-Right    Hip abduction
  [7]    leg_back_r_2         Back-Right    Hip flexion
  [8]    leg_back_r_3         Back-Right    Knee flexion
  [9]    leg_back_l_1         Back-Left     Hip abduction
  [10]   leg_back_l_2         Back-Left     Hip flexion
  [11]   leg_back_l_3         Back-Left     Knee flexion

  Each value is a POSITION OFFSET (radians) from default pose.
  Actual target sent to PD controller:

    q_target[i] = q_default[i] + a_t[i]

  Typical range: aₜ ∈ [-0.5, +0.5] rad per joint
  (policy learns to stay within useful range)
```

**Crucially, these are NOT:**
- Torques (that's the PD controller's job: $\tau = K_p(q_{target} - q) + K_d(0 - \dot{q})$)
- Absolute angles (they're offsets from the default standing pose)
- Velocities (the action is held constant for 10 PD ticks until the next NN inference)

### Training Phase (Offline, GPU Cluster)

1. **Environment setup**: A MuJoCo model of Pupper is loaded with randomized physics — friction coefficients, link masses, motor strength, observation noise, and communication delays are sampled from distributions each episode.
2. **Rollout collection**: The current policy $\pi_\theta$ controls the simulated robot for thousands of parallel episodes. At each timestep, the simulator records the experience tuple $(o_t, a_t, r_t, o_{t+1})$ — what was observed, what action the policy chose, how much reward that transition earned, and what the world looked like after. A single training batch might contain 100,000+ tuples from thousands of parallel robots.
3. **Reward shaping**: The reward $r_t$ typically includes terms for:
   - Forward velocity tracking: $r_{vel} = \exp(-\|v_{cmd} - v_{actual}\|^2)$
   - Energy penalty: $r_{energy} = -\sum_i |\tau_i \cdot \dot{q}_i|$
   - Smoothness: $r_{smooth} = -\|a_t - a_{t-1}\|^2$
   - Orientation: $r_{orient} = -\|\text{projected gravity} - [0, 0, -1]\|^2$
4. **Policy update**: PPO uses the collected tuples to estimate which actions were better than average (positive advantage) and updates the network weights $\theta$ to make good actions more likely. The clipped surrogate objective prevents the policy from changing too drastically in any single update.
5. **Logging**: Weights & Biases (wandb) tracks reward curves, episode lengths, and periodically saves policy checkpoints as `.json` files (project: `pupperv3-mjx-rl`).

### Deployment Phase (Real Robot, Raspberry Pi)

```
DEPLOYMENT PIPELINE
================================================================

  TRAINING (GPU)                    DEPLOYMENT (Pi)
  ┌──────────────┐                 ┌──────────────────────────┐
  │   MuJoCo     │   wandb         │  download_latest_policy  │
  │   + PPO      │──────────────-->│  .py                     │
  │   training   │   policy.json   │                          │
  └──────────────┘                 └───────────┬──────────────┘
                                               │
                                               ▼
                                   ┌──────────────────────────┐
                                   │  neural_controller       │
                                   │  (ROS2 controller)       │
                                   │                          │
                              ┌────│  Every 10th update tick:  │
                              │    │  1. Read IMU + joints     │
                              │    │  2. Build observation     │
                              │    │  3. Forward pass (NN)     │
                              │    │  4. Output 12 positions   │
                              │    └──────────────────────────┘
                              │
                520 Hz         │    ┌──────────────────────────┐
              update rate      └───>│  PD Controller (HW)      │
              (repeat_action=10     │  τ = Kp(q_target - q)    │
               → ~52 Hz NN)        │    + Kd(dq_target - dq)  │
                                   │  Kp=7.5, Kd=0.25         │
                                   └───────────┬──────────────┘
                                               │
                                               ▼
                                   ┌──────────────────────────┐
                                   │  CAN Bus → 12 Servos     │
                                   │  3 joints × 4 legs       │
                                   └──────────────────────────┘
```

### Key Numbers

- **Update rate**: 520 Hz (set slightly above 500 Hz to achieve exactly ~52 Hz for the neural network with `repeat_action: 10`)
- **Neural network inference**: $520 / 10 = 52$ Hz — each action is held for 10 control ticks
- **PD tracking**: Runs at the full 520 Hz between neural network updates
- **Init sequence**: 2.0s ramp to default pose (`init_duration`) + 2.0s fade-in to policy control (`fade_in_duration`)
- **Safety threshold**: `max_body_angle: 1.5` rad (~86 degrees) — if exceeded, the controller triggers e-stop

### Downloading a Policy

Students train policies in simulation and log them to wandb. The `download_latest_policy.py` script pulls a specific run's policy:

```bash
# Auto-detects your wandb entity from login session
python3 download_latest_policy.py --run_number 42

# Or use the interactive deploy script
python3 deploy.py
# → Enter run number (or press Enter to keep current policy)
# → Automatically launches: ros2 launch neural_controller launch.py
```

The downloaded `.json` file is copied to `policy_latest.json` in the neural_controller launch directory.

</details>

<details>
<summary><strong>The Key Tension</strong> — Classical vs. learned control</summary>

Lab 5 sits at the inflection point of the CS123 curriculum: everything before it is classical robotics, everything after it builds on top of the neural policy. This transition exposes a fundamental tradeoff that the entire field of robotics grapples with.

### The Classical Stack (Labs 1-4)

Every equation is visible. You can prove that the FK chain $T_{0 \to ee} = T_{0 \to 1} \cdot T_{1 \to 2} \cdot T_{2 \to 3} \cdot T_{3 \to ee}$ correctly maps joint angles to foot positions. You can verify the IK gradient $\nabla_\theta C = \nabla_\theta \|FK(\theta) - p_{target}\|^2$ converges. You can trace exactly why the robot stumbles — a gain too high, a phase offset wrong, a step height insufficient. But you pay for this transparency with rigidity: the gait works on flat carpet and fails on gravel, works with four legs and breaks with three.

### The Learned Stack (Lab 5)

A single policy file (`policy_latest.json`) replaces hundreds of lines of FK/IK/gait code. It handles terrain variation, perturbations, missing legs, and velocity commands — behaviors that would each require a separate engineering effort in the classical stack. The parkour policy navigates obstacles that no reasonable hand-tuned gait could handle. But the policy is a black box: when the robot falls, you cannot point to a specific weight or neuron and say "that's the bug."

| Aspect | Classical (Labs 1-4) | Learned (Lab 5) |
|--------|---------------------|-----------------|
| **Interpretability** | Full — every matrix, gain, and equation is visible | Low — weights are opaque, behavior is emergent |
| **Robustness** | Fragile — tuned for specific conditions | Robust — domain randomization covers a distribution |
| **Development cost** | Weeks of hand-tuning per behavior | Hours of training (but weeks of reward engineering + sim setup) |
| **Failure mode** | Predictable, traceable to a specific parameter | Sudden, catastrophic, hard to reproduce |
| **Generalization** | Manual: each new behavior requires new code | Emergent: reshape reward to get new behavior |
| **Safety guarantees** | Can prove joint limits, torque bounds | Statistical — works 99% of the time is not 100% |
| **Compute requirement** | Runs on bare-metal STM32 | Needs Pi-level compute for inference |

### The Hybrid Reality

In practice, Lab 5 does not fully abandon classical control. The neural network outputs *position targets*, not torques. The PD controller from Lab 1 — $\tau = K_p(q_{target} - q) + K_d(\dot{q}_{target} - \dot{q})$ — still runs at every tick to track those targets. This is a deliberate design choice: letting the RL policy output torques directly would require much more training data and be far less safe. The classical PD layer provides a safety floor — even if the neural network outputs a bad target, the PD controller limits how fast the joints can move to reach it.

The e-stop controller (`estop_controller.cpp`) provides another classical safety layer: a C++ node that monitors joystick buttons and can instantly deactivate all neural controllers, publishing to `/emergency_stop` and commanding zero gains. This layered architecture — learned policy for behavior, classical PD for tracking, hardcoded safety for emergencies — is how production robot systems actually work.

</details>

<details>
<summary><strong>Concrete Example</strong> — One inference cycle at t = 3.14 seconds</summary>

The robot has been walking for about 1 second (after the 2.0s init + 2.0s fade-in). The joystick is commanding forward velocity $v_x = 0.5$ m/s and zero yaw. Here is what happens during one neural network inference tick:

### Step 1: Sensor Read (tick 163 of the 520 Hz loop)

The controller reads from the [[learning/notes/quick-context/ros2-architecture|ROS2]] hardware interface:

```
IMU (BNO086 via I2C):
  orientation quaternion:  [0.998, 0.02, -0.01, 0.05]
  angular velocity:        [0.1, -0.05, 0.02] rad/s
  projected gravity:       [0.02, -0.01, -0.98]

Joint States (12 joints via CAN bus):
  positions:  [0.28, 0.15, -0.48, -0.24, 0.12, 0.55,
               0.25, -0.08, -0.50, -0.27, 0.03, 0.49]
  velocities: [0.5, -1.2, 0.8, -0.3, 1.1, -0.6,
               0.2, -0.9, 0.4, -0.1, 0.7, -0.3]
```

### Step 2: Build Observation Vector

The neural network receives a single flat vector combining:

$$o_t = [\underbrace{q_{cmd}}_{\text{velocity cmd}}, \underbrace{\omega}_{\text{angular vel}}, \underbrace{g_{proj}}_{\text{gravity}}, \underbrace{q - q_{default}}_{\text{joint pos offset}}, \underbrace{\dot{q}}_{\text{joint vel}}, \underbrace{a_{t-1}}_{\text{prev action}}]$$

The joint positions are expressed as offsets from the default standing pose (`default_joint_pos` in config.yaml: `[0.26, 0.0, -0.52, -0.26, 0.0, 0.52, ...]`). This centering helps the network — deviations from nominal are small numbers near zero.

### Step 3: Neural Network Forward Pass

The policy network (loaded from `policy_latest.json`) performs a forward pass:

$$h_1 = \text{ELU}(W_1 \cdot o_t + b_1)$$
$$h_2 = \text{ELU}(W_2 \cdot h_1 + b_2)$$
$$a_t = W_3 \cdot h_2 + b_3$$

The output $a_t$ is a 12-dimensional vector of position *offsets* from the default pose. Adding these to `default_joint_pos` yields the actual target:

$$q_{target} = q_{default} + a_t$$

For example, if $a_t[0] = 0.05$, then the target for `leg_front_r_1` is $0.26 + 0.05 = 0.31$ rad.

### Step 4: Action Hold (repeat_action = 10)

This target vector is held constant for the next 10 ticks of the 520 Hz loop. During each of those ticks, the PD controller computes torques:

$$\tau_i = 7.5 \cdot (q_{target,i} - q_i) + 0.25 \cdot (0 - \dot{q}_i)$$

The $K_p = 7.5$ and $K_d = 0.25$ gains (from `init_kps` and `init_kds` in config) provide compliant tracking — stiff enough to follow the target but soft enough that the robot doesn't fight perturbations rigidly.

### Step 5: Motor Execution

The torque commands travel: ROS2 controller manager $\to$ hardware interface $\to$ [[learning/notes/quick-context/can-bus|CAN bus]] (via MAX3051 transceivers) $\to$ 12 servo motors. Each servo's internal encoder reports back position and velocity for the next observation.

```
ONE FULL INFERENCE CYCLE (out of ~52 per second)
================================================================

  tick 160 ──────────────── tick 163 ──────────────── tick 170
  (prev NN inference)       (this NN inference)       (next)
       │                         │                         │
       │  PD tracks prev target  │  PD tracks new target   │
       │  for 10 ticks           │  for 10 ticks           │
       ▼                         ▼                         ▼
  ┌─────────┐              ┌─────────┐              ┌─────────┐
  │ Read    │              │ Read    │              │ Read    │
  │ sensors │              │ sensors │              │ sensors │
  │         │              │         │              │         │
  │ Build   │              │ Build   │              │ Build   │
  │ obs     │              │ obs     │              │ obs     │
  │         │              │         │              │         │
  │ NN fwd  │              │ NN fwd  │              │ NN fwd  │
  │ pass    │              │ pass    │              │ pass    │
  │         │              │         │              │         │
  │ Output  │              │ Output  │              │ Output  │
  │ 12 pos  │              │ 12 pos  │              │ 12 pos  │
  └─────────┘              └─────────┘              └─────────┘
       │                         │
       └── 10 PD ticks @ 520Hz ──┘
           ~19.2ms between NN inferences
```

**The one thing most outsiders get wrong about this is...** assuming the neural network directly outputs motor torques. It does not. It outputs *position targets* that the classical PD controller from Lab 1 tracks at full rate. This separation is critical: the RL policy only needs to run at 52 Hz (deciding *where* joints should go), while the PD controller handles the fast, reactive torque computation at 520 Hz (deciding *how hard* to push to get there). This makes training easier, deployment safer, and the system more robust to timing jitter on the [[learning/notes/quick-context/raspberry-pi-5-components|Raspberry Pi]].

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/ppo-proximal-policy-optimization|PPO (Proximal Policy Optimization)]]** — The RL algorithm used to train the policy. PPO constrains each gradient update to stay close to the previous policy (via a clipped surrogate objective), preventing catastrophic policy collapse. It is the standard algorithm for continuous control tasks like locomotion because it balances training stability with simplicity.
- **Domain Randomization** — During training, simulation parameters (friction $\mu \in [0.3, 1.5]$, link masses $\pm 20\%$, motor strength, observation delay) are randomized each episode. The policy cannot overfit to any single configuration, forcing it to learn robust strategies that transfer to the real robot's unknown true parameters.
- **Reward Shaping** — The art of designing $r_t$ to elicit desired behavior. Naive rewards (e.g., just forward velocity) produce degenerate gaits — the robot may learn to fall forward. Careful penalty terms for energy, joint acceleration, body orientation, and foot contact patterns guide the optimizer toward natural locomotion.
- **[[quick-context/pupper-brain]]** — The dual-[[learning/notes/micro-context/stm32-microcontroller|STM32]] + Raspberry Pi hardware architecture. The STM32 motor [[learning/notes/micro-context/microcontroller|MCU]] (U5) executes PD tracking at 1 kHz on the CAN bus; the Pi runs the neural network inference. The 520 Hz update rate in `config.yaml` is the rate at which the ROS2 controller manager ticks the hardware interface.
- **[[quick-context/pupper-v3-labs]]** — The full 7-lab CS123 curriculum. Lab 5 is the pivot point: Labs 1-4 build understanding of what the neural network replaces, Labs 6-7 build on top of the neural controller for voice control and vision tracking.
- **Emergency Stop System** — The `estop_controller.cpp` node (C++) subscribes to `/joy` and monitors PS4 controller buttons. Pressing the right joystick (button 12) instantly deactivates all neural controllers and publishes to `/emergency_stop`. The start button (button 9) reactivates the last-used controller. Buttons X/O/Triangle/Square switch between the four controller modes (normal, three-legged, parkour, test).
- **Weights & Biases (wandb)** — MLOps platform used for experiment tracking. Each training run logs reward curves, episode statistics, and policy checkpoints to the `pupperv3-mjx-rl` project. Students download specific runs by number: `python3 download_latest_policy.py --run_number 42`. The script auto-detects the logged-in user's wandb entity.

</details>

<details>
<summary><strong>Industry Best Practices (2025-2026)</strong> — How Lab 5 compares to the state of the art</summary>

Lab 5's approach — PPO + MuJoCo + domain randomization + position-target actions with PD tracking — is the pedagogical core of what production teams use, but the industry has moved significantly beyond it in several dimensions. Here's where things stand now and what Lab 5 gets right vs. what real systems do differently.

### What Lab 5 Gets Right (Still Best Practice)

**Position targets + PD tracking.** Lab 5 outputs joint position targets, not torques. This remains the industry standard. NVIDIA's Isaac Lab locomotion examples, ETH Zurich's ANYmal controllers, and virtually all deployed quadruped policies use the same pattern: NN outputs positions at 50-100 Hz, PD controller tracks at 200-1000 Hz. The reason hasn't changed — it's safer, trains faster, and transfers better to real hardware.

**PPO as the RL algorithm.** PPO (specifically the RSL-RL implementation) remains the dominant algorithm for locomotion. Despite advances in off-policy methods and diffusion-based policies, PPO's stability and simplicity make it the default choice. NVIDIA's Isaac Lab uses PPO with RSL-RL for all their locomotion benchmarks across 11 different robot morphologies (A1, Go1/2, Spot, ANYmal-B/C/D, Cassie, etc.).

**Domain randomization for sim-to-real.** Still essential. Every production pipeline randomizes friction, masses, motor delays, and sensor noise. The only change is that some teams now use **Automatic Domain Randomization (ADR)**, which adaptively expands randomization ranges during training rather than hand-picking distributions.

### Where Industry Has Moved Beyond Lab 5

**1. Teacher-Student Policy Distillation (Privileged Learning)**

This is the single biggest gap between Lab 5 and current best practice. The standard pipeline is now two-stage:

```
TEACHER-STUDENT PIPELINE (industry standard since ~2023)
================================================================

  Stage 1: TEACHER (privileged)
  ┌────────────────────────────────────────────┐
  │ Train with privileged information:          │
  │  - exact terrain heightmap under robot     │
  │  - true friction coefficients              │
  │  - true motor models                       │
  │  - contact forces at each foot             │
  │                                             │
  │ Teacher policy: π_teacher(a | o_priv)      │
  │ Learns near-optimal behavior (easy task)    │
  └─────────────────────┬──────────────────────┘
                        │ distillation
                        ▼
  Stage 2: STUDENT (deployable)
  ┌────────────────────────────────────────────┐
  │ Train to match teacher using only           │
  │ real-sensor observations:                   │
  │  - proprioception (joint pos/vel, IMU)     │
  │  - short history of past observations      │
  │                                             │
  │ Student policy: π_student(a | o_real)      │
  │ Learns to infer hidden terrain/friction     │
  │ from proprioceptive history                 │
  └────────────────────────────────────────────┘
```

**Why this matters:** The teacher has access to information (terrain shape, true friction) that makes the RL problem much easier — it just needs to learn the right foot placement for known conditions. The student then learns to *infer* these hidden variables from the pattern of joint positions and IMU readings over time. This two-stage approach converges faster, produces more robust policies, and handles terrain variation far better than end-to-end training with domain randomization alone. Lab 5's single-stage approach is simpler but leaves performance on the table.

Recent variants include Concurrent Teacher-Student (CTS) learning where both are trained simultaneously, and Generative Adversarial Distillation (GAD) which uses adversarial training to transfer the teacher's motion distribution to the student while preserving naturalness from human motion-capture data.

**2. GPU-Parallel Simulation (Isaac Lab / Isaac Gym)**

Lab 5 uses MuJoCo, which is excellent for accuracy but runs environments sequentially (or with limited parallelism via MJX on GPU). Current best practice uses NVIDIA Isaac Lab (successor to Isaac Gym), which runs **thousands of environments in parallel on GPU**:

| Aspect | MuJoCo (Lab 5) | Isaac Lab (Industry) |
|--------|----------------|---------------------|
| Parallelism | Tens of envs (CPU) or hundreds (MJX/GPU) | 4,096-8,192 parallel envs (GPU) |
| Throughput | ~10K steps/sec | ~90K frames/sec (RTX A6000) |
| Training time | Hours to days | Minutes to hours |
| Tensor pipeline | Numpy → PyTorch | Pure PyTorch (zero copy) |
| Physics fidelity | Excellent (MuJoCo gold standard) | Good (PhysX-based, improving) |

Isaac Lab exposes physics results directly as PyTorch tensors, eliminating CPU-GPU data transfer. Training a locomotion policy for ANYmal or Spot typically takes 30-60 minutes on a single GPU. Lab 5's MuJoCo approach is pedagogically clearer (easier to understand one environment) but wouldn't scale to the thousands of terrain variations that production systems train on.

**3. Terrain Curriculum Learning**

Lab 5 trains on flat ground (or simple terrains) with domain randomization. Production systems use **progressive terrain curricula** that automatically increase difficulty:

```
TERRAIN CURRICULUM (progressive difficulty)
================================================================

  Level 0         Level 1         Level 2         Level 3
  flat ground     gentle slopes   stairs + gaps   rough rubble
  ┌─────────┐    ┌─/──\────┐    ┌─┐ ┌─┐ ┌─┐    ┌/\─/\─┐
  │         │    │/    \   │    │ │ │ │ │ │    │\/  \/\│
  └─────────┘    └──────\──┘    └─┘ └─┘ └─┘    └──────┘

  Robot advances to harder terrain only when
  it achieves a reward threshold on current level.
  Poor performance → moved back to easier terrain.
```

ETH Zurich's ANYmal team and NVIDIA's Spot training both use automatic curricula where the system estimates the agent's learning progress and adaptively adjusts terrain sampling. Learning Progress-based Automatic Curriculum RL (LP-ACRL) enables stable locomotion at 2.5 m/s across stairs, slopes, gravel, and low-friction surfaces — without manually designing the difficulty progression.

**4. Emerging: Diffusion Policies and VLA Models**

Two newer trends are beginning to influence locomotion, though PPO remains dominant:

**Diffusion policies** (DPPO — Diffusion Policy Policy Optimization) use denoising diffusion models as policy representations instead of MLPs. They handle multimodal action distributions gracefully — useful when multiple valid gaits exist for the same command. Still mostly used in manipulation; locomotion adoption is early.

**Vision-Language-Action (VLA) models** are the frontier for combining locomotion with semantic understanding. Figure AI's Helix model controls entire humanoid bodies from vision + language inputs. WholeBodyVLA (ICLR 2026) learns locomotion + manipulation jointly from egocentric video. These don't replace low-level RL locomotion policies — they sit *above* them as high-level controllers, similar to how Lab 6-7's LLM sits above Lab 5's neural policy. The layered architecture Lab 5 teaches (NN → PD → motors) is exactly how these systems work at the bottom of the stack.

### Summary: Where Lab 5 Sits

```
MATURITY SPECTRUM
================================================================

  Lab 5                    Industry Standard           Frontier
  (Pedagogical)            (Production 2025)           (Research 2026)
  ─────────────────────────────────────────────────────────────────
  Single-stage PPO         Teacher-student distill.    VLA models
  MuJoCo (serial)          Isaac Lab (GPU parallel)    Diffusion policies
  Flat + domain rand.      Terrain curriculum + ADR    Foundation models
  Simple MLP               MLP + history encoder       Transformers
  Position targets + PD    Position targets + PD ✓     Same ✓
  wandb logging            wandb/Neptune logging ✓     Same ✓
```

Lab 5 nails the architectural foundation (position targets, PD tracking, PPO, domain randomization) that every production system builds on. The main gaps — teacher-student distillation, GPU-parallel training, and terrain curricula — are engineering scale-ups rather than conceptual changes. Understanding Lab 5 is sufficient to read and implement any of the industry-standard approaches.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** The neural network outputs 12 values, one per joint. Are these torques, velocities, or position targets? Why does this choice matter for safety?

<details>
<summary>Answer</summary>

They are **position targets** (joint angles in radians), added as offsets to the default standing pose. This matters for safety because the PD controller acts as a low-pass [[learning/notes/quick-context/frequency-and-filtering|filter]] between the NN and the motors: even if the NN outputs a sudden, large position jump, the PD controller smoothly drives toward it at a rate limited by $K_p = 7.5$ and $K_d = 0.25$. If the NN output torques directly, a single bad inference could instantly command maximum current to a motor, potentially damaging hardware or injuring a nearby person. Position targets give the classical PD layer a chance to limit force.
</details>

**Q2:** Why does Lab 5 use uniform PD gains ($K_p = 7.5$, $K_d = 0.25$) across all 12 joints, even though hip abduction and knee flexion have very different mechanical loads?

<details>
<summary>Answer</summary>

The RL policy is trained with these exact gains in simulation — they are part of the simulated actuator model. The policy implicitly learns to compensate for per-joint differences by commanding different position offsets: a heavily loaded joint gets a larger offset to generate more torque through the PD law. Changing gains per joint after training would break this learned compensation. Uniform gains also simplify sim-to-real transfer — one fewer thing to match between simulation and reality.
</details>

**Q3:** Domain randomization varies friction, masses, and motor delays during training. Why not just make the simulation as accurate as possible instead?

<details>
<summary>Answer</summary>

Because you can never make simulation perfectly accurate — there will always be a gap (unmodeled motor dynamics, cable stiffness, floor texture). A policy optimized for a single "perfect" simulation overfits to that simulation's specific parameters and fails when reality inevitably differs. Domain randomization forces the policy to be robust across a *distribution* of physics parameters, so the real robot's true parameters are likely somewhere within that distribution. It's the difference between memorizing one exam vs. studying broadly — the randomized policy sacrifices peak performance in any single environment for reliable performance across all of them.
</details>

**Q4:** The teacher-student distillation pipeline (industry standard) trains a teacher with privileged information (true terrain, friction), then distills to a student using only real-sensor observations. Why not just train the student directly with domain randomization, as Lab 5 does? What specific failure mode does the teacher avoid?

<details>
<summary>Answer</summary>

The core problem is that without privileged information, the RL optimization must simultaneously learn two things: (1) how to *infer* hidden environment properties (terrain shape, friction) from proprioceptive history, and (2) how to *act optimally* given those properties. This joint optimization is much harder and often converges to suboptimal policies that are "cautious everywhere" rather than terrain-adaptive. The teacher-student split separates these concerns: the teacher only learns optimal behavior (easy, because it sees the terrain), and the student only learns to *predict* what the teacher would do from limited sensor data (a supervised learning problem, which is well-understood). The result is a student that implicitly infers terrain and adapts its gait, rather than Lab 5's approach of learning a single "average" policy that works acceptably on all terrains but optimally on none.
</details>

**Q5:** VLA models (Helix, WholeBodyVLA) and diffusion policies are emerging trends. Where do they sit relative to Lab 5's neural controller in the control stack — do they replace it, or layer on top of it? What architectural principle from the Pupper labs predicts this?

<details>
<summary>Answer</summary>

They layer **on top** of it, not replace it. VLA models operate at the semantic level ("pick up the cup on the table") and output high-level commands (velocity targets, waypoints, or task-space goals). These get translated into joint-level actions by a low-level locomotion policy — exactly Lab 5's neural controller. The Pupper labs already demonstrate this architecture: Lab 6-7's LLM outputs text commands → Karel translates to Twist messages → Lab 5's neural controller converts to joint positions → PD tracks at full rate. VLA models are a more capable version of the LLM layer, and diffusion policies are an alternative policy *representation* (replacing Lab 5's MLP) but still output position targets tracked by PD control. The architectural principle is **separation of timescales**: slow deliberation (LLM/VLA at ~1 Hz) → fast reactive locomotion (NN at ~50 Hz) → fastest motor tracking (PD at ~500 Hz). Each layer only talks to its neighbors, not to hardware directly.
</details>

</details>
