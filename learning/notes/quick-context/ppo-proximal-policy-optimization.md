---
topic: PPO (Proximal Policy Optimization)
created: 2026-03-13
---

# PPO (Proximal Policy Optimization)

> **Related:** [[quick-context/pupper-lab5-neural-controller]] | [[quick-context/pupper-lab4-gait-control]]

> **TL;DR:** PPO is a reinforcement learning algorithm that trains a neural network policy by collecting batches of experience in the environment, estimating which actions were better than average (advantage), and updating the policy weights — but with a clipping mechanism that prevents any single update from changing the policy too drastically, making training stable enough to work reliably on continuous control tasks like robot locomotion.

## The Core Problem

Policy gradient methods learn by trial and error: try actions, measure how good they were, and adjust the policy to do more of what worked. The problem is sensitivity to step size. Take too large a gradient step and the policy changes drastically — it starts selecting completely different actions, the new experience no longer matches the assumptions of the update, and performance collapses catastrophically (this happened routinely with vanilla policy gradients). TRPO solved this with a hard KL-divergence constraint, but its implementation required conjugate gradient optimization and line searches — complex and computationally expensive. Take too small a step and training takes forever. PPO solves this with a deceptively simple idea: clip the objective [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|function]] so that the policy can't change more than a small amount ($\epsilon$, typically 0.2) in any single update. This eliminates the most common [[learning/notes/quick-context/pupper-lab5-neural-controller|failure mode]] — catastrophic policy collapse — while keeping the algorithm simple enough to implement in ~100 lines of code, which is why PPO has been the default RL algorithm for continuous control since its publication by OpenAI in 2017.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Policy $\pi_\theta(a \mid s)$** | The neural network being trained — maps an observation (state) $s$ to a probability distribution over actions $a$. In Pupper Lab 5, this is a small MLP that outputs 12 joint [[learning/notes/quick-context/pupper-lab5-neural-controller|position targets]]. |
| **Advantage $\hat{A}_t$** | A scalar estimate of "how much better was the action I took compared to what I usually do in this state?" Positive advantage means the action was above average; negative means below. |
| **Clipped Surrogate Objective** | PPO's core innovation: the loss function that limits how much $\pi_\theta$ can change per update by clipping the probability ratio $r_t(\theta)$ to $[1 - \epsilon, 1 + \epsilon]$. |
| **Probability Ratio $r_t(\theta)$** | $\frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{old}}(a_t \mid s_t)}$ — how much more or less likely the new policy is to take the same action as the old policy. A ratio of 1.0 means no change; 1.3 means 30% more likely. |
| **Value Function $V_\phi(s)$** | A second neural network (the "critic") that estimates the expected cumulative reward from state $s$. Used to compute the advantage: $\hat{A}_t \approx r_t + \gamma V(s_{t+1}) - V(s_t)$. |

<details>
<summary><strong>How It Works</strong> — The PPO training loop</summary>

### The Big Picture

PPO alternates between two phases: (1) **rollout** — use the current policy to collect experience by interacting with the environment, and (2) **update** — use that experience to improve the policy. This collect-then-update cycle is the heartbeat of the algorithm.

```
PPO TRAINING LOOP
================================================================

  ┌─────────────────────────────────────────────────────────────┐
  │  PHASE 1: ROLLOUT (collect experience)                      │
  │                                                             │
  │  Run current policy π_θ in N parallel environments          │
  │  for T timesteps each. Collect:                             │
  │                                                             │
  │    (s_t, a_t, r_t, s_{t+1}, log π_θold(a_t|s_t))          │
  │                                                             │
  │  Total: N × T experience tuples per rollout batch           │
  │  (e.g., 4096 envs × 24 steps = 98,304 tuples)              │
  └──────────────────────┬──────────────────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  Compute advantages using GAE (Generalized Advantage        │
  │  Estimation) with the value function V_φ(s):                │
  │                                                             │
  │    δ_t = r_t + γ V(s_{t+1}) - V(s_t)     (TD error)       │
  │    A_t = δ_t + (γλ)δ_{t+1} + (γλ)²δ_{t+2} + ...          │
  │                                                             │
  │  γ = discount factor (~0.99), λ = GAE lambda (~0.95)        │
  └──────────────────────┬──────────────────────────────────────┘
                         │
                         ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  PHASE 2: UPDATE (improve policy)                           │
  │                                                             │
  │  For K epochs (typically 3-10):                             │
  │    Shuffle rollout data into minibatches                    │
  │    For each minibatch:                                      │
  │      1. Compute probability ratio r_t(θ)                    │
  │      2. Compute clipped surrogate loss L^CLIP               │
  │      3. Compute value function loss                         │
  │      4. Backpropagate and update θ, φ                       │
  │                                                             │
  │  Key: the log probabilities from Phase 1 (θ_old) are       │
  │  frozen — only the current θ changes during updates.        │
  └──────────────────────┬──────────────────────────────────────┘
                         │
                         └──── repeat from Phase 1 ────┘
```

### The Clipped Surrogate Objective (The Core Math)

The key question PPO answers at each update step is: "should I make this action more or less likely?" The naive approach would be to just follow the policy gradient — increase the probability of actions that had positive advantage. But large gradient steps can be catastrophic.

PPO's solution is the clipped surrogate objective:

$$L^{CLIP}(\theta) = \mathbb{E}_t \left[ \min \left( r_t(\theta) \hat{A}_t, \; \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$

where $r_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{old}}(a_t \mid s_t)}$ is the probability ratio.

**What this does, intuitively:**

The $\min$ operator selects the *more pessimistic* of two terms:
- The unclipped term $r_t(\theta) \hat{A}_t$ — the standard policy gradient objective
- The clipped term $\text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t$ — same thing but with $r_t$ forced into $[1 - \epsilon, 1 + \epsilon]$

```
HOW CLIPPING WORKS — Positive Advantage Case (A > 0)
================================================================

  Objective
  L^CLIP
    ▲
    │                         ┌──────────── unclipped: r × A
    │                        ╱
    │                       ╱
    │               ┌──────╱── clipped: (1+ε) × A
    │              ╱│     ╱        (flat ceiling)
    │             ╱ │    ╱
    │            ╱  │   ╱
    │           ╱   │  ╱
    │          ╱    │ ╱
    │         ╱     │╱
    │        ╱      │             min() selects the
    │       ╱       │             LOWER of the two curves
    │      ╱        │
    │─────╱─────────┼─────────────────────────► r_t(θ)
    │              1+ε
    │   clipped     │    unclipped (but capped)
    │   = unclipped │
    │               │
    └───────────────┘

  When A > 0 (good action), PPO WANTS to increase r_t.
  But once r_t > 1+ε, there is NO further gradient incentive.
  The policy has moved "far enough" — stop pushing.


HOW CLIPPING WORKS — Negative Advantage Case (A < 0)
================================================================

  Objective
  L^CLIP
    ▲
    │
    │────────────────┐
    │                │        clipped: (1-ε) × A
    │                │             (flat floor)
    │                │╲
    │                │ ╲
    │                │  ╲
    │                │   ╲
    │                │    ╲
    │                │     ╲         unclipped: r × A
    │                │      ╲
    │────────────────┼───────╲────────────────► r_t(θ)
    │               1-ε       ╲
    │  unclipped     │   clipped = unclipped
    │  (but floored) │
    └────────────────┘

  When A < 0 (bad action), PPO WANTS to decrease r_t.
  But once r_t < 1-ε, there is NO further gradient incentive.
  The policy has moved "far enough" — stop pushing.
```

**Why $\epsilon = 0.2$?** This means the policy can only become at most 20% more or less likely to take any given action per update. In practice, $\epsilon \in [0.1, 0.3]$ works well. Smaller $\epsilon$ is more conservative (slower but safer training); larger $\epsilon$ allows faster learning but risks instability.

### The Value Function and Advantage Estimation

PPO uses a separate neural network — the **critic** $V_\phi(s)$ — to estimate how much total future reward to expect from a given state. This baseline is essential: without it, all actions in high-reward states would be reinforced equally, even the bad ones.

The advantage $\hat{A}_t$ tells us how much better (or worse) a specific action was compared to the state's baseline:

$$\hat{A}_t = r_t + \gamma r_{t+1} + \gamma^2 r_{t+2} + \cdots - V_\phi(s_t)$$

In practice, PPO uses **Generalized Advantage Estimation (GAE)** which smoothly interpolates between high-bias/low-variance (1-step TD) and low-bias/high-variance (full Monte Carlo) estimates via a parameter $\lambda$:

$$\hat{A}_t^{GAE} = \sum_{l=0}^{\infty} (\gamma \lambda)^l \delta_{t+l}, \quad \text{where } \delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$$

The value function is trained alongside the policy by minimizing the squared error between its predictions and the actual returns observed during rollouts.

### On-Policy: Why You Throw Away Data

PPO is **on-policy**: after each update, the rollout data is discarded and fresh data is collected with the updated policy. This seems wasteful — off-policy algorithms like SAC reuse old data from a replay buffer. The tradeoff:

- **On-policy (PPO):** Data is always generated by the current policy, so advantage estimates are accurate. But you need lots of environment interactions. GPU-parallel simulators (Isaac Lab running 4096+ envs) make this cheap.
- **Off-policy (SAC, TD3):** Reuses old data, so it's more sample-efficient. But old data was generated by a different policy, requiring importance sampling corrections that can be unstable with large policy changes.

For robotics simulation where environments are cheap to run in parallel, PPO's simplicity and stability outweigh its sample inefficiency. This is why [[quick-context/pupper-lab5-neural-controller|Lab 5]] and virtually all production locomotion pipelines use PPO.

</details>

<details>
<summary><strong>The Key Tension</strong> — Stability vs. sample efficiency</summary>

PPO occupies a specific point in the RL algorithm design space, trading sample efficiency for training stability. Understanding this tradeoff explains why PPO dominates some domains and not others.

### The Algorithm Landscape

| Algorithm | Type | Key Idea | Sample Efficiency | Stability | Best For |
|-----------|------|----------|-------------------|-----------|----------|
| **Vanilla PG (REINFORCE)** | On-policy | Raw policy gradient | Very low | Low (high variance) | Pedagogical |
| **TRPO** | On-policy | KL-constrained update | Low | High | Continuous control (superseded by PPO) |
| **PPO** | On-policy | Clipped surrogate | Low | High | Continuous control, locomotion, RLHF |
| **SAC** | Off-policy | Max-entropy + replay buffer | High | Medium | Sample-limited domains, real-world RL |
| **TD3** | Off-policy | Twin critics + delayed update | High | Medium | Continuous control (alternative to SAC) |

### Why PPO Wins for Robot Locomotion

1. **Parallel simulation is cheap.** GPU-based simulators (Isaac Lab, MJX) run thousands of environments simultaneously. When you can collect 100K transitions per second, sample efficiency barely matters — training takes minutes either way.

2. **Stability matters more than speed.** A locomotion training run that diverges at hour 6 wastes more time than a stable run that takes 8 hours. PPO's clipping makes divergence rare.

3. **Continuous action spaces.** PPO handles continuous actions (joint position targets) naturally by parameterizing $\pi_\theta$ as a Gaussian: the network outputs a mean $\mu$ for each action dimension, and a learned (or fixed) standard deviation $\sigma$ defines exploration.

4. **Compatibility with GAE.** The advantage estimator used by PPO (GAE with $\lambda$) provides a smooth knob between bias and variance, making reward shaping less finicky.

### Where PPO Loses

- **Real-world RL** where each sample requires physical robot interaction: SAC's replay buffer makes every interaction count.
- **Sparse rewards** where millions of random actions are needed before any learning signal: exploration-focused algorithms (RND, Go-Explore) outperform.
- **Offline RL** where you have a fixed dataset and can't collect new data: PPO can't be used at all; algorithms like CQL or IQL are needed.

### PPO for RLHF (Language Models)

PPO's second major application — beyond robotics — is Reinforcement Learning from Human Feedback (RLHF) for training language models. The same clipping mechanism that prevents a robot policy from collapsing also prevents a language model from degenerating into nonsensical text during reward-model-guided fine-tuning. In this context, the "environment" is text generation, the "action" is the next token, and the "reward" comes from a trained reward model reflecting human preferences. The KL penalty between the fine-tuned model and the base model serves a similar purpose to PPO's clipping — preventing the policy from straying too far.

</details>

<details>
<summary><strong>Concrete Example</strong> — One PPO update step for Pupper locomotion</summary>

Here's a concrete walkthrough of one PPO update cycle during [[quick-context/pupper-lab5-neural-controller|Pupper Lab 5]] training in MuJoCo simulation.

### Setup

- 4096 parallel simulated Puppers (via MJX on GPU)
- Rollout length: 24 timesteps per environment
- Total batch: $4096 \times 24 = 98{,}304$ transitions
- $\epsilon = 0.2$, $\gamma = 0.99$, $\lambda = 0.95$
- Update epochs: 5
- Minibatch size: 4096

### Phase 1: Rollout Collection

All 4096 simulated Puppers take 24 steps using the current policy $\pi_{\theta_{old}}$. For each step $t$ and each environment $n$, we record:

```
STORED PER TRANSITION:
================================================================
  s_t       = observation vector (~48 dims: IMU, joint pos/vel, cmd, prev action)
  a_t       = action vector (12 joint position offsets)
  r_t       = scalar reward (velocity tracking + energy penalty + smoothness + ...)
  s_{t+1}   = next observation
  log π_old = log probability of a_t under the OLD policy (frozen)
  V(s_t)    = value function estimate (from critic network)
```

### Phase 2: Advantage Computation

For one specific transition — say environment #1337, timestep $t = 10$:

```
EXAMPLE TRANSITION (env #1337, t=10):
================================================================
  s_10 = [cmd_vel=(0.5,0,0), gyro=(0.1,-0.05,0.02),
          grav=(0.02,-0.01,-0.98), joint_offsets=(...), ...]

  a_10 = [+0.03, -0.01, +0.05, ...]  (12 position offsets)

  r_10 = 0.72  (good forward velocity tracking, moderate energy use)

  V(s_10) = 18.3  (critic estimates ~18.3 total future reward)
  V(s_11) = 18.5

  TD error:
    δ_10 = r_10 + γ V(s_11) - V(s_10)
         = 0.72 + 0.99 × 18.5 - 18.3
         = 0.72 + 18.315 - 18.3
         = 0.735

  GAE advantage (simplified, showing first 3 terms):
    A_10 = δ_10 + (γλ)δ_11 + (γλ)²δ_12 + ...
         = 0.735 + 0.9405 × 0.12 + 0.884 × (-0.08) + ...
         ≈ 0.78

  Interpretation: action a_10 was BETTER than average
  for this state (positive advantage).
```

### Phase 3: Policy Update

For 5 epochs, shuffle all 98,304 transitions into minibatches of 4096 and update:

```
ONE MINIBATCH UPDATE (for the transition above):
================================================================

  1. Compute new log probability of the SAME action under
     the CURRENT (changing) policy:

     log π_θ(a_10 | s_10) = -3.42   (current policy)
     log π_old(a_10 | s_10) = -3.50  (stored from rollout)

  2. Probability ratio:

     r_t(θ) = exp(log π_θ - log π_old)
            = exp(-3.42 - (-3.50))
            = exp(0.08)
            = 1.083

     Interpretation: the updated policy is 8.3% MORE likely
     to take this action than the old policy was.

  3. Clipped surrogate loss (for this single transition):

     unclipped = r_t × A_t = 1.083 × 0.78 = 0.845
     clipped   = clip(1.083, 0.8, 1.2) × 0.78
               = 1.083 × 0.78 = 0.845
               (1.083 is within [0.8, 1.2], so no clipping)

     L = min(0.845, 0.845) = 0.845

     Since A > 0 and r < 1.2, there IS gradient pushing r higher.
     The optimizer will make this good action even more likely.

  4. If instead r_t had grown to 1.25:

     unclipped = 1.25 × 0.78 = 0.975
     clipped   = clip(1.25, 0.8, 1.2) × 0.78
               = 1.2 × 0.78 = 0.936

     L = min(0.975, 0.936) = 0.936

     The min picks the clipped term. Gradient through the
     clipped term is ZERO w.r.t. r_t (it's been clamped at 1.2).
     No further incentive to increase r_t. Policy stops changing.

  5. Value function loss (trained simultaneously):

     L_value = (V_φ(s_10) - R_10^actual)²

     where R_10^actual = r_10 + γr_11 + γ²r_12 + ...
     (actual discounted return observed during rollout)
```

### What Happens Over Many Updates

```
TRAINING PROGRESS (typical Pupper locomotion run)
================================================================

  Iteration    Avg Reward    Avg Episode Length    Policy Change
  ─────────    ──────────    ─────────────────    ─────────────
       0          -2.1         0.3s (falls)       (random)
     100          +3.5         1.2s (stumbles)    large
     500         +12.8         4.0s (walks)       medium
    1000         +18.2         8.0s (stable walk) small
    2000         +22.1        12.0s (robust)      very small
    3000         +23.0        15.0s (converged)   minimal

  Early: large advantages, big policy changes, rapid improvement.
  Late: small advantages, clipping rarely triggers, fine-tuning.
```

**The one thing most outsiders get wrong about this is...** thinking PPO is sample-efficient. It is not — PPO throws away all experience after every update and recollects from scratch. It succeeds in robotics not because it uses data wisely, but because GPU-parallel simulation generates data so cheaply that inefficiency doesn't matter. If you tried to train a Pupper policy with PPO on a physical robot (collecting experience one step at a time), it would take years. The algorithm only works because MuJoCo or Isaac Lab can simulate thousands of Puppers simultaneously at millions of steps per second.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/pupper-lab5-neural-controller]]** — The primary consumer of PPO in this project. Lab 5 trains locomotion policies with PPO in MuJoCo, then deploys them to the real Pupper at ~52 Hz. The observation space, action space, and reward shaping are all detailed there.
- **TRPO (Trust Region Policy Optimization)** — PPO's predecessor by Schulman et al. (2015). TRPO enforces a hard KL-divergence constraint between old and new policies using conjugate gradient optimization — theoretically principled but complex to implement. PPO achieves similar stability with a simple clip, making it the practical successor.
- **GAE (Generalized Advantage Estimation)** — The advantage estimator used by PPO. Introduced by Schulman et al. (2016), GAE interpolates between 1-step TD estimates (high bias, low variance) and full Monte Carlo returns (low bias, high variance) via the $\lambda$ parameter. Almost always used with $\lambda = 0.95$, $\gamma = 0.99$.
- **SAC (Soft Actor-Critic)** — The main alternative to PPO for continuous control. SAC is off-policy (uses a replay buffer), maximizes entropy alongside reward, and is more sample-efficient. Preferred when environment interactions are expensive (real robots), but less stable and harder to tune than PPO.
- **Domain Randomization** — During training, simulation parameters (friction, mass, motor delay) are randomized each episode to prevent overfitting to a single simulator configuration. Combined with PPO, this is the standard recipe for sim-to-real transfer in locomotion.
- **Isaac Lab / Isaac Gym** — NVIDIA's GPU-parallel simulation framework. Runs 4096+ environments simultaneously on a single GPU, making PPO's sample inefficiency irrelevant. The industry standard for training locomotion policies at scale.
- **RLHF (Reinforcement Learning from Human Feedback)** — PPO's other major application domain. Used to fine-tune language models (GPT, Claude) based on human preference rankings. The same clipped objective prevents the language model from degenerating during reward-guided fine-tuning.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** PPO clips the probability ratio $r_t(\theta)$ to $[1 - \epsilon, 1 + \epsilon]$. What does a ratio of 1.0 mean? What does 1.3 mean?

<details>
<summary>Answer</summary>

$r_t = 1.0$ means the new policy assigns exactly the same probability to action $a_t$ as the old policy — no change. $r_t = 1.3$ means the new policy is 30% more likely to take that action. With $\epsilon = 0.2$, a ratio of 1.3 exceeds $1 + \epsilon = 1.2$ and would be clipped, removing the gradient incentive to push the ratio any higher.
</details>

**Q2:** Why does PPO take the $\min$ of the clipped and unclipped objectives? Why not just use the clipped version directly?

<details>
<summary>Answer</summary>

The $\min$ creates a **pessimistic bound**: it only clips in the direction that would make the objective better. For positive advantage (good action), clipping prevents $r_t$ from going above $1 + \epsilon$ (stops over-reinforcing). For negative advantage (bad action), clipping prevents $r_t$ from going below $1 - \epsilon$ (stops over-penalizing). But if the ratio moves in the "wrong" direction (making a good action less likely or a bad action more likely), the unclipped term is smaller and the $\min$ selects it — providing a full gradient signal to correct the mistake. Using only the clipped version would remove this corrective gradient.
</details>

**Q3:** PPO is on-policy and discards data after each update. Why not use an off-policy algorithm like SAC that reuses old experience, especially since RL is notoriously sample-hungry?

<details>
<summary>Answer</summary>

For the robotics simulation setting (MuJoCo, Isaac Lab), PPO's sample inefficiency is irrelevant because parallel simulation generates millions of transitions per second at near-zero cost. The bottleneck is training stability, not data volume. Off-policy methods like SAC reuse old data efficiently but introduce staleness — old transitions were generated by a different policy, requiring importance sampling corrections that can destabilize training. PPO avoids this entirely: every batch is "fresh" and the advantage estimates are accurate. In domains where environment interaction is expensive (real robots, expensive API calls), SAC's sample efficiency is worth the complexity. In cheap-simulation domains, PPO's stability wins. See: "The Key Tension" section.
</details>

**Q4:** The Pupper Lab 5 trains with PPO in MuJoCo using domain randomization. If you doubled $\epsilon$ from 0.2 to 0.4, what would you expect to happen to training?

<details>
<summary>Answer</summary>

With $\epsilon = 0.4$, each update can change action probabilities by up to 40% instead of 20%. This allows faster learning early on (larger policy changes per update), but risks instability: the policy could change so much that the advantage estimates from the rollout batch become stale and misleading, leading to a bad update that tanks performance. In practice, $\epsilon = 0.4$ often causes training to oscillate — reward improves rapidly for a few iterations, then collapses when a too-aggressive update pushes the policy into a bad region. The policy might recover, but the training curve becomes noisy and unreliable compared to $\epsilon = 0.2$.
</details>

**Q5:** PPO is used both for training robot locomotion policies and for RLHF fine-tuning of language models. These seem like very different domains. What structural similarity makes the same algorithm work for both?

<details>
<summary>Answer</summary>

Both are sequential decision problems where a policy (robot controller or language model) produces actions (joint targets or tokens) and receives delayed reward (locomotion quality or human preference score). Both face the same core challenge: updating the policy to improve reward without changing it so drastically that behavior degenerates. For robots, "degeneration" means the policy forgets how to walk and falls over. For language models, it means the model produces incoherent or reward-hacked text that scores high on the reward model but is nonsensical. PPO's clipping prevents both failure modes by bounding the per-update policy change. In both domains, there's also a KL-style regularization toward a "reference" behavior (domain randomization teaches robustness in robotics; a KL penalty toward the base model preserves language coherence in RLHF).
</details>

</details>
