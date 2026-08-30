---
topic: Pupper Lab 2 — Forward Kinematics (3-DOF Leg)
created: 2026-03-10
---

# Pupper Lab 2 — Forward Kinematics (3-DOF Leg)

> **Related:** [[learning/notes/quick-context/pupper-lab3-inverse-kinematics]]

> **TL;DR:** Forward kinematics computes where the foot ends up in 3D space given three joint angles, by chaining 4x4 homogeneous transformation matrices along the leg's kinematic chain. This is the mathematical foundation reused in every subsequent Pupper lab.

## The Core Problem

A quadruped robot leg has three revolute joints — hip abduction (swing out/in), hip flexion (forward/backward), and knee flexion. When these joints rotate by angles $\theta_1, \theta_2, \theta_3$, the foot moves to some position $(x, y, z)$ in 3D space. Forward kinematics (FK) answers the question: *given the joint angles, where is the foot?* This is the foundational "forward" direction of the kinematics problem; Lab 3 tackles the harder "inverse" direction (given a foot position, what joint angles produce it).

The naive approach would be to derive trigonometric formulas by hand — for a 3-DOF leg you could write out $x = L_1 \cos\theta_1 + L_2 \cos(\theta_1 + \theta_2) + \ldots$ — but this gets unwieldy fast and is error-prone when axes are not all parallel. Instead, Lab 2 uses **4x4 homogeneous transformation matrices**, a systematic framework where each joint-link pair is encoded as a single matrix, and the full chain is computed by multiplying them together. The approach scales cleanly: whether you have 3 joints or 30, the procedure is the same.

Each transformation matrix encodes two things simultaneously: a rotation (what direction the next link points) and a translation (where the next joint is located relative to the current one). By using 4x4 matrices instead of 3x3, rotations and translations can be combined into a single matrix multiplication — this is the "homogeneous" trick. The final matrix product $T_{0 \to ee}$ contains the foot's 3D position directly in its last column, ready to be extracted and visualized as a green sphere in RViz.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Homogeneous Transform** | A 4x4 matrix that encodes both rotation and translation in a single representation, enabling chained spatial transformations via matrix multiplication |
| **Rotation Matrix** | A 3x3 orthonormal matrix (embedded in the upper-left of the 4x4) that rotates vectors about an axis — Lab 2 implements `rotation_y()` and `rotation_z()` plus a rotation about x for hip abduction |
| **Translation** | A displacement vector $(d_x, d_y, d_z)$ placed in the rightmost column of the 4x4 matrix — represents the offset along a link from one joint to the next |
| **Kinematic Chain** | The sequence of joints and rigid links from the robot's body frame to the end-effector; for Pupper's front-left leg: body $\to$ hip $\to$ upper leg $\to$ lower leg $\to$ foot |
| **End-Effector** | The "tool" at the end of the chain — in this case the foot contact point, whose 3D position is the output of the FK computation |

<details>
<summary><strong>How It Works</strong> — Chaining transformation matrices</summary>

### The 4x4 Homogeneous Transform

A [[learning/notes/micro-context/homogeneous-transformation-matrix|homogeneous transformation matrix]] packs a 3x3 rotation and a 3x1 translation into one 4x4 matrix:

$$T = \begin{bmatrix} R_{3 \times 3} & \mathbf{d}_{3 \times 1} \\ \mathbf{0}_{1 \times 3} & 1 \end{bmatrix} = \begin{bmatrix} r_{11} & r_{12} & r_{13} & d_x \\ r_{21} & r_{22} & r_{23} & d_y \\ r_{31} & r_{32} & r_{33} & d_z \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

The upper-left 3x3 block is the rotation matrix $R$. The right column $(d_x, d_y, d_z)$ is the translation. The bottom row is always $[0 \; 0 \; 0 \; 1]$.

When you multiply two transforms, $T_A \cdot T_B$, the result applies $B$'s rotation and translation *within* $A$'s coordinate frame — this is exactly what "chaining" means.

### The 3-Joint Kinematic Chain

Pupper's front-left leg has three joints. Each joint introduces a rotation, and the rigid link after it introduces a translation:

```
PUPPER FRONT-LEFT LEG — Kinematic Chain
================================================================

  Body Frame (0)
       │
       │  T_{0→1}: rotate about x-axis (hip abduction, θ₁)
       │           + translate along link to upper leg joint
       ▼
  Joint 1 (Hip Abduction)
       │
       │  T_{1→2}: rotate about y-axis (hip flexion, θ₂)
       │           + translate along upper leg length
       ▼
  Joint 2 (Hip Flexion / Upper Leg)
       │
       │  T_{2→3}: rotate about y-axis (knee flexion, θ₃)
       │           + translate along lower leg length
       ▼
  Joint 3 (Knee)
       │
       │  T_{3→ee}: translate along remaining link to foot
       │            (no rotation — just an offset)
       ▼
  End-Effector (Foot)
```

The complete forward kinematics is a single matrix product:

$$T_{0 \to ee} = T_{0 \to 1}(\theta_1) \cdot T_{1 \to 2}(\theta_2) \cdot T_{2 \to 3}(\theta_3) \cdot T_{3 \to ee}$$

### Building Each Transform

Each $T_{i \to i+1}$ is constructed by combining a rotation matrix with a translation matrix. For example, $T_{1 \to 2}$ for the hip flexion joint (rotation about the y-axis by $\theta_2$, followed by a translation along the upper leg):

$$T_{1 \to 2} = \text{rotation\_y}(\theta_2) \cdot \text{translation}(L_{upper}, 0, 0)$$

where:

$$\text{rotation\_y}(\theta) = \begin{bmatrix} \cos\theta & 0 & \sin\theta & 0 \\ 0 & 1 & 0 & 0 \\ -\sin\theta & 0 & \cos\theta & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

$$\text{translation}(x, y, z) = \begin{bmatrix} 1 & 0 & 0 & x \\ 0 & 1 & 0 & y \\ 0 & 0 & 1 & z \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

### Extracting the Foot Position

After computing the full chain product $T_{0 \to ee}$, the foot position in the body frame is simply the translation column:

$$\mathbf{p}_{foot} = \begin{bmatrix} T_{0 \to ee}[0, 3] \\ T_{0 \to ee}[1, 3] \\ T_{0 \to ee}[2, 3] \end{bmatrix}$$

This position is published as an RViz `Marker` (green sphere) so students can visually verify their FK against the robot's actual foot location.

</details>

<details>
<summary><strong>The Key Tension</strong> — Why matrices instead of trig</summary>

### Direct Trigonometry: Simple but Fragile

For a planar 2-link arm, you can write the end-effector position directly:

$$x = L_1 \cos\theta_1 + L_2 \cos(\theta_1 + \theta_2)$$
$$y = L_1 \sin\theta_1 + L_2 \sin(\theta_1 + \theta_2)$$

This is fast and transparent. But it has serious limitations:

1. **Non-parallel axes break the pattern.** Pupper's first joint rotates about the x-axis (hip abduction) while the next two rotate about y-axes. Writing a single trig expression that handles the frame change between x-rotation and y-rotation is messy and error-prone.

2. **It doesn't compose.** Adding a 4th joint means re-deriving the entire formula, not just appending one more term. For a 6-DOF arm, the trig expressions become pages long.

3. **No orientation information.** Trig gives you the position, but the matrix approach also gives you the orientation of the end-effector (the 3x3 rotation block) — essential for tasks like grasping or knowing which direction the foot pushes against the ground.

### Matrix Multiplication: Systematic and General

The matrix approach treats every joint identically:

1. Write the rotation matrix for the joint's axis and angle.
2. Write the translation matrix for the link length.
3. Multiply them together to get $T_{i \to i+1}$.
4. Chain all $T$ matrices together.

Adding a joint means multiplying in one more matrix. Changing a rotation axis means swapping `rotation_y` for `rotation_x` or `rotation_z`. The procedure is mechanical and the same for any robot geometry.

The tradeoff is computational cost: matrix multiplication requires more operations than a direct trig formula. But for a 3-DOF leg at 200 Hz, the cost is negligible — and the clarity of the systematic approach prevents the kinds of sign errors and frame confusion bugs that plague hand-derived trig solutions.

### The Deeper Insight

Matrix chaining is really about **composing coordinate frame transformations**. Each matrix $T_{i \to i+1}$ says: "here is how to convert a point expressed in frame $i+1$'s coordinates into frame $i$'s coordinates." The full product $T_{0 \to ee}$ converts the foot's position (which is trivially $\mathbf{0}$ in its own frame) into the body's coordinate frame. This frame-thinking generalizes to any spatial relationship in robotics — not just serial chains but also [[quick-context/camera-fundamentals|camera-to-world transforms]] (where the extrinsic matrix is exactly a homogeneous transform), sensor fusion, and multi-robot coordination.

</details>

<details>
<summary><strong>Concrete Example</strong> — Computing foot position from joint angles</summary>

Suppose the front-left leg has:
- Link lengths: $L_{hip} = 0.05$ m (hip offset), $L_{upper} = 0.08$ m (upper leg), $L_{lower} = 0.11$ m (lower leg), $L_{foot} = 0.02$ m (foot offset)
- Joint angles: $\theta_1 = 0$ (no abduction), $\theta_2 = -30°$ (hip flexed back), $\theta_3 = 60°$ (knee bent)

### Step 1: Build $T_{0 \to 1}$ (hip abduction about x-axis)

With $\theta_1 = 0$, the rotation is identity, plus a translation for the hip offset along the y-axis:

$$T_{0 \to 1} = \text{rotation\_x}(0) \cdot \text{translation}(0, L_{hip}, 0) = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0.05 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

### Step 2: Build $T_{1 \to 2}$ (hip flexion about y-axis)

With $\theta_2 = -30°$, $\cos(-30°) \approx 0.866$, $\sin(-30°) = -0.5$:

$$T_{1 \to 2} = \text{rotation\_y}(-30°) \cdot \text{translation}(0, 0, -L_{upper})$$

$$= \begin{bmatrix} 0.866 & 0 & -0.5 & 0 \\ 0 & 1 & 0 & 0 \\ 0.5 & 0 & 0.866 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} \cdot \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -0.08 \\ 0 & 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} 0.866 & 0 & -0.5 & 0.04 \\ 0 & 1 & 0 & 0 \\ 0.5 & 0 & 0.866 & -0.069 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

### Step 3: Build $T_{2 \to 3}$ (knee flexion about y-axis)

With $\theta_3 = 60°$, $\cos(60°) = 0.5$, $\sin(60°) \approx 0.866$:

$$T_{2 \to 3} = \text{rotation\_y}(60°) \cdot \text{translation}(0, 0, -L_{lower})$$

$$= \begin{bmatrix} 0.5 & 0 & 0.866 & 0 \\ 0 & 1 & 0 & 0 \\ -0.866 & 0 & 0.5 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} \cdot \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -0.11 \\ 0 & 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} 0.5 & 0 & 0.866 & -0.095 \\ 0 & 1 & 0 & 0 \\ -0.866 & 0 & 0.5 & -0.055 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

### Step 4: Build $T_{3 \to ee}$ (foot offset, no rotation)

$$T_{3 \to ee} = \text{translation}(0, 0, -L_{foot}) = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -0.02 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

### Step 5: Chain them all

$$T_{0 \to ee} = T_{0 \to 1} \cdot T_{1 \to 2} \cdot T_{2 \to 3} \cdot T_{3 \to ee}$$

The foot position is the last column of $T_{0 \to ee}$. For these angles, the foot ends up roughly at:

$$\mathbf{p}_{foot} \approx \begin{bmatrix} 0.007 \\ 0.05 \\ -0.174 \end{bmatrix} \text{ meters}$$

This means: nearly directly below the hip (x close to 0), offset laterally by the hip width (y = 0.05 m), and about 17.4 cm below the body frame origin — which makes physical sense for a leg that is mostly pointing downward with a moderate knee bend.

**The one thing most outsiders get wrong about this is...** thinking the matrices multiply left-to-right in the order you "walk" along the chain. They do — but the reason is subtle. Each matrix transforms *from* the next frame *into* the current frame. So $T_{0 \to 1} \cdot T_{1 \to 2}$ first expresses frame-2 coordinates in frame-1, then expresses frame-1 coordinates in frame-0. The foot position in its own frame is just the origin $(0, 0, 0, 1)^T$, and the full chain "carries" that origin all the way back to the body frame.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/pupper-v3-labs]]** — The full 7-lab progression. Lab 2 FK is reused directly in Lab 3 (IK via gradient descent on FK), Lab 4 (FK for all 4 legs), and conceptually underpins Lab 5's neural controller.
- **[[quick-context/pupper-brain]]** — The hardware that executes FK computations at 200 Hz. Joint angles come from motor encoders via CAN bus; computed foot positions can be published as ROS2 topics.
- **Denavit-Hartenberg (DH) Parameters** — A standardized convention for assigning coordinate frames to each joint, reducing any serial chain to a table of 4 parameters per joint ($\theta$, $d$, $a$, $\alpha$). Lab 2 uses a slightly simplified approach, but DH is the industry standard for complex manipulators.
- **RViz Visualization** — ROS2's 3D visualization tool. Lab 2 publishes a `visualization_msgs/Marker` (green sphere, type `SPHERE`) at the computed foot position so students can visually debug their FK against the URDF model.
- **Rotation Conventions** — Lab 2 uses intrinsic rotations (each rotation is about the *current* frame's axis, not the fixed world axis). The distinction between intrinsic and extrinsic rotations matters when chaining: intrinsic rotations multiply right-to-left if you think in fixed-frame terms, but left-to-right if you think in body-frame terms (which is what the matrix chain does).
- **URDF (Unified Robot Description Format)** — The XML file that defines Pupper's link lengths, joint axes, and visual meshes. The constants used in FK (link lengths, axis directions) must match the URDF for the RViz visualization to align.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does Lab 2 use 4x4 matrices instead of 3x3 rotation matrices plus separate translation vectors?

<details>
<summary>Answer</summary>

With 3x3 rotation matrices, you would need to apply rotation and translation separately at each step: $\mathbf{p}_{i} = R_{i} \mathbf{p}_{i+1} + \mathbf{d}_{i}$. This means two operations per joint and does not compose cleanly — you cannot simply multiply all the transforms together in one expression. The 4x4 homogeneous form embeds both rotation and translation into a single matrix, so the entire chain reduces to one matrix product $T_{0 \to ee} = T_{0 \to 1} \cdot T_{1 \to 2} \cdot \ldots$, and the foot position is extracted from a single column. This also makes the math uniform: every spatial relationship (joint transforms, sensor mounts, camera frames) is a 4x4 matrix with the same structure.
</details>

**Q2:** The first joint rotates about the x-axis while joints 2 and 3 rotate about y-axes. What would go wrong if you accidentally used `rotation_y` for all three joints?

<details>
<summary>Answer</summary>

The hip abduction joint swings the leg laterally (in/out from the body). It must rotate about the x-axis (the axis pointing forward along the body) to produce lateral motion. If you used `rotation_y` instead, the first joint would swing the leg forward/backward — the same direction as the hip flexion joint. The leg would have no ability to move sideways, effectively collapsing from 3-DOF to a planar 2-DOF mechanism. The FK would produce foot positions only in the x-z plane, never offset in the y-direction (except by the fixed hip link length), and the robot would be unable to adjust its stance width.
</details>

**Q3:** After computing $T_{0 \to ee}$, you extract the foot position from column index 3 (the last column). What information is contained in the upper-left 3x3 block of $T_{0 \to ee}$, and when would you need it?

<details>
<summary>Answer</summary>

The upper-left 3x3 block is the cumulative rotation matrix $R_{0 \to ee}$, representing the orientation of the end-effector frame relative to the body frame. For Pupper's foot, orientation is less critical (the foot is roughly a point contact), but it becomes essential for tasks like: (1) computing the Jacobian for inverse kinematics, where you need to know how the end-effector frame is oriented to map joint velocities to Cartesian velocities; (2) ground contact normal estimation, determining the angle at which the foot contacts the terrain; (3) manipulators with grippers, where the tool orientation (not just position) must be controlled. In Lab 3, the cost function only uses position, but a full 6-DOF IK formulation would also penalize orientation error using this rotation block.
</details>

</details>
