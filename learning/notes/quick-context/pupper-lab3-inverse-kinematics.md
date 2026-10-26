---
topic: Pupper Lab 3 — Inverse Kinematics (Gradient Descent)
created: 2026-03-10
updated: 2026-03-11
---

# Pupper Lab 3 — Inverse Kinematics (Gradient Descent)

> **Related:** [[learning/notes/quick-context/pupper-lab2-forward-kinematics]]

> **TL;DR:** Lab 3 flips the FK problem: given a desired foot position in 3D space, find the joint angles that reach it by minimizing a cost function via gradient descent, then drives a single leg through a triangle stepping trajectory using a dual-rate architecture (200 Hz PD tracking + 20 Hz IK solving).

## The Core Problem

In Lab 2 you solved forward kinematics: plug in joint angles $\theta_1, \theta_2, \theta_3$, get foot position $p \in \mathbb{R}^3$. That's a clean, closed-form mapping. But a walking robot doesn't think in joint angles — it thinks in foot positions. You want to say "put the foot here" and have the robot figure out which angles achieve that. This is the **inverse kinematics** problem, and for most robots it's far harder than FK because the mapping from Cartesian space back to joint space can be nonlinear, non-unique, or even nonexistent (if the target is out of reach).

Pupper's 3-DOF leg actually does have a closed-form analytical IK solution — you could derive it with trigonometry. But Lab 3 deliberately uses **numerical gradient descent** instead, for two reasons. First, the gradient descent approach generalizes: it works for any robot geometry (6-DOF arms, redundant manipulators, humanoid legs) without rederiving equations. Second, it teaches the optimization-based thinking that underlies modern robotics — trajectory optimization, model-predictive control, and even neural network training all share the same gradient-based core.

The lab also introduces a critical systems concept: **dual-rate control**. The IK solver runs at 20 Hz because each solve requires multiple FK evaluations (one per joint per gradient step), making it computationally expensive. But the motors need smooth, high-frequency commands to avoid jerky motion. So a separate PD control loop runs at 200 Hz, tracking whatever joint targets the IK solver most recently produced. This separation of planning rate from execution rate is standard in real robot architectures — Lab 5's neural controller uses the same pattern at 50 Hz policy / 500 Hz PD.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Inverse Kinematics (IK)** | Finding joint angles $\theta$ such that $FK(\theta) = p_{target}$ — the reverse of forward kinematics. In general, solutions may be non-unique (multiple configurations reach the same point) or nonexistent (target out of workspace). |
| **Cost Function** | $C(\theta) = \|FK(\theta) - p_{target}\|^2$ — the squared Euclidean distance between where the foot actually is and where you want it. IK becomes an optimization problem: minimize $C$ to zero. |
| **Gradient Descent** | Iterative update rule $\theta \leftarrow \theta - \alpha \nabla C(\theta)$ that walks downhill on the cost surface. The learning rate $\alpha$ controls step size: too large overshoots, too small converges slowly. |
| **Finite Differences** | Numerical gradient approximation: $\frac{\partial C}{\partial \theta_i} \approx \frac{C(\theta + \epsilon e_i) - C(\theta)}{\epsilon}$, where $e_i$ is the $i$-th unit vector and $\epsilon$ is a small perturbation (typically $10^{-6}$). Requires one extra FK evaluation per joint. |
| **Triangle Trajectory** | Three waypoints defining a stepping motion — touchdown, liftoff, and mid-swing (apex) — linearly interpolated to create a closed loop. The foot traces a triangle in the sagittal plane: flat along the ground during stance, lifted arc during swing. |

<details>
<summary><strong>How It Works</strong> — Numerical IK via gradient descent</summary>

### The Optimization Loop

Each IK solve takes the current joint angles and a target foot position, then iterates gradient descent until the foot is close enough (or a max iteration count is hit):

```
ONE IK SOLVE (runs at 20 Hz)
================================================================

  Input: θ_current = [θ1, θ2, θ3],  p_target = [x, y, z]

  for step = 1 to max_iterations:
  │
  │  1. EVALUATE COST
  │     p_actual = FK(θ)
  │     C = ‖p_actual - p_target‖²
  │
  │  2. CHECK CONVERGENCE
  │     if C < tolerance:  → done, return θ
  │
  │  3. COMPUTE GRADIENT (finite differences)
  │     for each joint i = 1, 2, 3:
  │     │  θ_perturbed = θ  (copy)
  │     │  θ_perturbed[i] += ε
  │     │  C_perturbed = ‖FK(θ_perturbed) - p_target‖²
  │     │  ∂C/∂θ_i = (C_perturbed - C) / ε
  │     │
  │     ∇C = [∂C/∂θ1, ∂C/∂θ2, ∂C/∂θ3]
  │
  │  4. UPDATE
  │     θ ← θ - α · ∇C
  │
  Output: θ_solution
```

Note that each gradient computation requires 3 additional FK evaluations (one per joint). If you run 10 iterations, that's $10 \times (1 + 3) = 40$ FK calls per solve. At 20 Hz, that's 800 FK evaluations per second — which is why IK can't run at the same rate as the PD loop.

### Dual-Rate Architecture

```
DUAL-RATE CONTROL ARCHITECTURE
================================================================

  20 Hz IK Loop                    200 Hz PD Loop
  ┌──────────────────┐            ┌──────────────────────┐
  │                  │            │                      │
  │  trajectory      │   θ_target │  read joint states   │
  │  interpolation   │──────────>│  (position, velocity)│
  │       │          │            │       │              │
  │       ▼          │            │       ▼              │
  │  IK solve        │            │  τ = Kp(θ_t - θ)    │
  │  (gradient       │            │    + Kd(dθ_t - dθ)  │
  │   descent)       │            │       │              │
  │                  │            │       ▼              │
  └──────────────────┘            │  publish torque      │
                                  │  to motors           │
                                  └──────────────────────┘

  Timeline (50ms window):
  ────────────────────────────────────────────────────────
  0ms    5ms    10ms   15ms   20ms   25ms   30ms   35ms
  │      │      │      │      │      │      │      │
  IK     PD     PD     PD     PD     PD     PD     PD
  +PD    only   only   only   only   only   only   only
                                     IK
                                     +PD

  IK fires every 50ms (20 Hz), sets new θ_target
  PD fires every 5ms (200 Hz), tracks current θ_target
```

The PD loop holds the last θ_target from IK and smoothly drives the motors toward it. When IK produces a new target (every 50ms), the PD loop seamlessly transitions to tracking the updated target. This decoupling means the IK solver can take variable time without causing motor jitter.

### Triangle Trajectory

The foot traces a triangular path defined by three waypoints:

```
TRIANGLE STEPPING TRAJECTORY (sagittal plane, side view)
================================================================

                    mid-swing (apex)
                        *
                       / \
                      /   \
                     /     \
                    /       \
                   /         \
  touchdown ─────*───────────*───── liftoff
                 │  stance   │
                 │  (on ground) │
                 └───────────┘

  Phase:  0.0 ──────── 0.5 ──── 0.75 ──── 1.0
          touchdown    liftoff   apex    touchdown
          (start)                        (repeat)

  Interpolation: linear between consecutive waypoints
  The 20 Hz IK loop advances the phase each tick,
  computes the interpolated 3D target, then solves IK.
```

The trajectory planner linearly interpolates between these waypoints based on a phase variable that advances each IK tick. Each interpolated point becomes $p_{target}$ for the gradient descent solver.

</details>

<details>
<summary><strong>The Key Tension</strong> — Numerical vs. analytical IK</summary>

Pupper's 3-DOF leg is simple enough that you could derive a closed-form IK solution using the law of cosines and some arctangent calls. This would be faster (one evaluation, no iteration) and guaranteed to find a solution if one exists. So why bother with gradient descent?

**Generality vs. speed.** Analytical IK requires a human to derive equations specific to each robot's geometry. Change the link lengths, add a joint, or switch to a different robot, and you re-derive from scratch. Gradient descent works on any robot where you have FK — just swap the FK function and the optimizer doesn't care. For a 6-DOF industrial arm or a humanoid with 30+ joints, closed-form solutions may not even exist.

**Convergence guarantees.** Gradient descent on $C(\theta) = \|FK(\theta) - p_{target}\|^2$ is minimizing a non-convex function. The cost landscape has local minima — configurations where the gradient is zero but the foot isn't at the target (e.g., the elbow is bent the wrong way). Analytical solutions enumerate all valid configurations directly, avoiding this trap. In practice, initializing gradient descent from the current joint angles (which are close to the solution for smooth trajectories) prevents local minima issues for Pupper's simple leg.

**Extensibility.** The cost function formulation lets you add constraints trivially: joint limits become penalty terms $C_{limits}(\theta) = \sum \max(0, \theta_i - \theta_{max})^2$, obstacle avoidance becomes a distance penalty, and you can even add secondary objectives (e.g., minimize joint velocities) as weighted cost terms. Analytical solutions can't absorb these extras without complete re-derivation.

| Aspect | Numerical (Gradient Descent) | Analytical (Closed-Form) |
|--------|------------------------------|--------------------------|
| Speed per solve | Slow (many FK evals) | Fast (one evaluation) |
| Generality | Any robot geometry | Specific to one robot |
| Local minima | Possible (non-convex) | N/A — enumerates all solutions |
| Constraint handling | Add cost terms | Re-derive equations |
| Implementation effort | Low (generic optimizer) | High (geometry-specific algebra) |
| When to prefer | Research, complex robots, prototyping | Production, simple geometry, real-time |

### The Hybrid Approach: Analytical Seed + Numerical Optimization

In practice, production robots often use analytical IK for speed and then layer on numerical optimization for constraint satisfaction — you get the best of both worlds. This is worth understanding in detail because it's how real systems actually work:

**The problem with pure analytical IK:** IKFast (used in MoveIt) can auto-generate C++ analytical solvers that find solutions in microseconds. But these solutions only satisfy the kinematic constraint $FK(\theta) = p_{target}$ — they say nothing about joint limits, self-collisions, obstacle avoidance, or secondary objectives like "keep the elbow away from the table." An analytical solver might return 8 valid configurations for a 6-DOF arm, and all 8 might collide with the environment.

**The problem with pure numerical IK:** Gradient descent (Lab 3's approach) or more advanced optimizers can encode any constraint as a cost term. But numerical solvers need a good starting point — they're slow to converge from far away and can get trapped in local minima that don't satisfy the kinematic constraint at all.

**The hybrid solution:** Use analytical IK to generate a set of candidate joint configurations that exactly reach the target pose (fast, microseconds), then feed each candidate as a seed into a numerical optimizer that minimizes constraint violations (collision distance, joint centering, smoothness). The optimizer starts near a valid IK solution, so it converges quickly and only needs to "nudge" the configuration rather than solve the full nonlinear problem from scratch.

```
HYBRID IK PIPELINE (production systems)
================================================================

  Target pose p_target
        │
        ▼
  ┌──────────────┐
  │ Analytical IK │──→ {θ₁, θ₂, ..., θ_k}  (k candidate solutions,
  │ (IKFast)      │     all exactly satisfy FK(θ) = p_target,
  └──────────────┘     found in ~5 μs)
        │
        ▼
  ┌──────────────────────────────────────────────┐
  │ Numerical Optimizer (per candidate)           │
  │                                               │
  │  min  C_collision(θ) + C_joint_limits(θ)     │
  │       + C_smoothness(θ) + C_joint_centering(θ)│
  │                                               │
  │  starting from each analytical candidate      │
  │  (converges in 1-5 iterations, ~50 μs)        │
  └──────────────────────────────────────────────┘
        │
        ▼
  Best θ that satisfies all constraints
  (or report failure if no candidate works)
```

**Real-world implementations of this pattern:**

- **MoveIt's pick_ik** — Combines a local gradient descent optimizer with a global evolutionary algorithm. In `local` mode it takes a seed (from analytical IK or the current configuration) and optimizes cost functions for joint displacement, joint centering, and avoiding limits. In `global` mode it uses an evolutionary algorithm to escape local minima.

- **TRAC-IK** — Runs two solvers in parallel: a fast KDL-based numerical solver and a sequential quadratic programming (SQP) solver with joint limit constraints. Returns whichever finds a valid solution first.

- **Recent research (Cohn et al., 2026)** — Uses the analytical IK solution as a *change of variables* in the optimization formulation itself, so the optimizer works in a space where the kinematic constraint is automatically satisfied. This achieves higher success rates on problems involving collision avoidance, grasp selection, and humanoid stability than either approach alone.

The key insight: analytical IK solves the hard nonlinear constraint (reaching the target) exactly, and numerical optimization handles the "soft" constraints (collision, smoothness, limits) that are easier to optimize over. Neither alone is sufficient — analytical can't handle constraints, and numerical struggles with the nonlinear FK constraint.

Lab 3 teaches the numerical approach because it's the foundation for more advanced techniques (Jacobian-based IK, trajectory optimization, model-predictive control) encountered in graduate robotics courses. Understanding gradient descent on the IK cost function prepares you for the numerical optimization half of the hybrid pipeline.

</details>

<details>
<summary><strong>Concrete Example</strong> — One IK solve iteration</summary>

Suppose the current joint angles are $\theta = [0.2, -0.5, 0.8]$ radians and we want the foot at $p_{target} = [0.05, -0.10, -0.15]$ meters. Let's walk through one gradient descent step.

**Step 1: Evaluate FK and cost.**

$p_{actual} = FK([0.2, -0.5, 0.8]) = [0.048, -0.095, -0.142]$ m

$C = (0.048 - 0.05)^2 + (-0.095 - (-0.10))^2 + (-0.142 - (-0.15))^2$

$C = (-0.002)^2 + (0.005)^2 + (0.008)^2 = 0.000004 + 0.000025 + 0.000064 = 0.000093$

**Step 2: Compute gradient via finite differences ($\epsilon = 10^{-6}$).**

For joint 1: perturb $\theta_1$ by $\epsilon$:

$\theta_{pert} = [0.200001, -0.5, 0.8]$

$p_{pert} = FK(\theta_{pert}) = [0.04800, -0.09502, -0.14199]$ (small shift)

$C_{pert} = 0.000091$

$\frac{\partial C}{\partial \theta_1} = \frac{0.000091 - 0.000093}{10^{-6}} = -2.0$

Repeat for joints 2 and 3 (each requires one FK call):

$\frac{\partial C}{\partial \theta_2} = -3.8$

$\frac{\partial C}{\partial \theta_3} = -5.1$

$\nabla C = [-2.0, -3.8, -5.1]$

**Step 3: Update with learning rate $\alpha = 0.01$.**

$\theta_{new} = [0.2, -0.5, 0.8] - 0.01 \times [-2.0, -3.8, -5.1]$

$\theta_{new} = [0.2 + 0.02, -0.5 + 0.038, 0.8 + 0.051]$

$\theta_{new} = [0.22, -0.462, 0.851]$

**Step 4: Verify improvement.**

$p_{new} = FK([0.22, -0.462, 0.851]) = [0.0495, -0.0988, -0.1483]$

$C_{new} = (0.0495 - 0.05)^2 + (-0.0988 + 0.10)^2 + (-0.1483 + 0.15)^2 = 0.0000063$

Cost dropped from $0.000093$ to $0.0000063$ — a $93\%$ reduction in one step. A few more iterations and the cost will be below the convergence tolerance, at which point the IK solver returns $\theta_{new}$ as the solution and the 200 Hz PD loop begins driving the motors to these angles.

**Computation cost of this one step:** 4 FK evaluations (1 base + 3 perturbations). A typical solve takes 5-15 steps, so 20-60 FK evaluations total. Each FK evaluation chains three 4x4 matrix multiplications (from Lab 2), which is why this is too expensive to run at 200 Hz.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **Jacobian-based IK** — Instead of finite differences, compute the analytical Jacobian $J = \frac{\partial FK}{\partial \theta}$ and solve $\Delta\theta = J^{\dagger} \Delta p$ (pseudoinverse method). Faster convergence per step, but requires deriving $J$. This is the standard approach in industrial robotics and what most graduate courses teach next after Lab 3's gradient descent introduction.
- **Newton's Method** — Uses second-order information (the Hessian $\nabla^2 C$) for faster convergence: $\theta \leftarrow \theta - (\nabla^2 C)^{-1} \nabla C$. Converges quadratically near the solution vs. gradient descent's linear convergence, but each step is more expensive and the Hessian can be singular.
- **Levenberg-Marquardt Algorithm** — A damped least-squares method that interpolates between gradient descent (far from solution) and Gauss-Newton (near solution). The standard workhorse for nonlinear least-squares problems in robotics, vision, and SLAM.
- **[[quick-context/pupper-v3-labs]]** — The full 7-lab progression. Lab 3 builds directly on Lab 2's FK implementation and feeds into Lab 4's multi-leg gait controller.
- **[[quick-context/pupper-brain]]** — The hardware executing these loops: the STM32 microcontrollers running the 200 Hz PD loop, and the Raspberry Pi running the 20 Hz IK solver in Python via [[quick-context/ros2-architecture|ROS2]].
- **Optimization Theory** — Lab 3's gradient descent is a first-order unconstrained optimizer. The broader field includes constrained optimization (Lagrange multipliers, interior-point methods), stochastic gradient descent (used in ML), and convex optimization (where global minima are guaranteed). Boyd & Vandenberghe's *Convex Optimization* is the standard reference.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What does the cost function $C(\theta) = \|FK(\theta) - p_{target}\|^2$ actually measure, and what does it equal when IK has found a perfect solution?

<details>
<summary>Answer</summary>

It measures the squared Euclidean distance between the foot's actual position (computed by forward kinematics) and the desired target position. When IK finds a perfect solution, $FK(\theta) = p_{target}$ exactly, so $C = 0$. In practice, the solver stops when $C$ drops below a small tolerance (e.g., $10^{-6}$), meaning the foot is within a fraction of a millimeter of the target.
</details>

**Q2:** Why does Lab 3 initialize gradient descent from the current joint angles rather than from zeros or random values?

<details>
<summary>Answer</summary>

Because the foot trajectory changes smoothly between IK ticks (20 Hz is fast enough that consecutive targets are close together), the current joint angles are already a near-optimal solution for the next target. Starting from this warm initialization means gradient descent converges in just a few steps. Starting from zeros or random angles would require many more iterations to converge, might converge to a different local minimum (e.g., elbow-up vs. elbow-down), and could cause discontinuous jumps in joint angles between ticks — which would translate to violent, jerky motor commands. Warm-starting is a general technique used across robotics and optimization.
</details>

**Q3:** The IK cost function $C(\theta) = \|FK(\theta) - p_{target}\|^2$ is described as non-convex. What does this mean concretely for the Pupper leg, and why doesn't it cause problems in practice?

<details>
<summary>Answer</summary>

Non-convex means the cost landscape has multiple local minima — there are joint configurations where the gradient is zero but the foot isn't at the target. For the Pupper leg, this corresponds to "elbow-up" vs. "elbow-down" configurations that represent different ways to reach nearby (but not target) positions. It doesn't cause problems in practice because warm-starting from the current configuration (which is already close to the solution for smooth trajectories) keeps gradient descent in the same local basin. The solver never has to "jump over a hill" to find the right minimum. This would break down if you commanded a sudden large jump in foot position — the solver might converge to the wrong configuration or fail to converge at all.
</details>

**Q4:** If you decreased the IK loop rate from 20 Hz to 5 Hz but kept the PD loop at 200 Hz, what would happen to the robot's motion quality? What if you did the opposite — ran IK at 200 Hz but PD at 20 Hz?

<details>
<summary>Answer</summary>

**Slow IK (5 Hz), fast PD (200 Hz):** The PD loop still smoothly tracks joint targets, so motor commands remain smooth. But the trajectory updates only every 200ms, making the foot path coarser — it "staircases" between waypoints. The robot still functions because the PD loop interpolates between stale targets. Motion quality degrades but doesn't break.

**Fast IK (200 Hz), slow PD (20 Hz):** This is much worse. The IK solver produces beautiful joint targets at 200 Hz, but the PD loop only commands the motors every 50ms. Between PD ticks, the motors hold their last torque command with no feedback correction. External disturbances go uncorrected for 50ms, causing oscillation and potential instability. The lesson: **high-frequency tracking (PD) matters more than high-frequency planning (IK)**. The fast inner loop is what keeps the hardware stable; the slower outer loop just sets goals.
</details>

**Q5:** In the hybrid analytical+numerical IK pipeline, why can't you just run the numerical optimizer from scratch with collision avoidance as a cost term, skipping the analytical seed entirely? What specifically goes wrong?

<details>
<summary>Answer</summary>

The FK constraint ($FK(\theta) = p_{target}$) is highly nonlinear — the mapping from joint angles to Cartesian position involves nested trigonometric functions. When you add collision avoidance (another nonconvex constraint), the optimizer must simultaneously satisfy two hard nonlinear constraints. Starting from a random or distant seed, the optimizer often can't find the narrow feasible region where both constraints are satisfied, and either: (1) converges to a local minimum where the foot doesn't reach the target, (2) reaches the target but in a colliding configuration, or (3) fails to converge entirely. The analytical seed eliminates one constraint entirely — every seed already exactly satisfies $FK(\theta) = p_{target}$ — so the optimizer only needs to handle collision avoidance, a much easier problem. This is the general principle: decompose hard problems by solving the analytically tractable part exactly, then optimize over the remainder.
</details>

</details>
