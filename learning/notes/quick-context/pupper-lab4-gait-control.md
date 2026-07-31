---
topic: Pupper Lab 4 — Gait Control (Trotting Quadruped)
created: 2026-03-10
---

# Pupper Lab 4 — Gait Control (Trotting Quadruped)

> **Related:** [[learning/notes/quick-context/pupper-lab1-pid-control]] | [[learning/notes/quick-context/pupper-lab6-llm-voice-control]] | [[learning/notes/quick-context/pupper-brain]] | [[learning/notes/quick-context/pupper-lab2-forward-kinematics]] | [[learning/notes/quick-context/pupper-lab3-inverse-kinematics]]

> **TL;DR:** Lab 4 extends single-leg FK/IK from Labs 2-3 to all four legs simultaneously, coordinating them into a trotting gait where diagonal leg pairs (FR+BL, FL+BR) move in anti-phase. All target joint positions for one complete gait cycle are pre-cached via IK at startup to avoid real-time computational cost, then the 200 Hz control loop simply indexes into the cached trajectory with per-leg phase offsets.

## The Core Problem

Making a quadruped robot walk requires solving three problems simultaneously: where each foot should be at every instant (trajectory planning), what joint angles achieve those foot positions (inverse kinematics), and how to coordinate four legs so the robot stays balanced (gait timing). Labs 2 and 3 solved the first two problems for a single leg — Lab 2 gave us forward kinematics to know where the foot is, Lab 3 gave us inverse kinematics to command where it should go, and a triangle trajectory to step. Lab 4's challenge is scaling this to four legs that must work in concert.

The trotting gait is the natural starting point for quadruped locomotion because it is the simplest dynamically stable two-phase gait. At any instant during a trot, two diagonally opposite feet are on the ground while the other two are swinging through the air. This diagonal pairing ensures the support polygon — the line connecting the two grounded feet — passes roughly under the robot's center of mass, preventing roll or pitch instability. Compare this to pacing (same-side legs swing together), which causes lateral rocking, or bounding (front pair and rear pair alternate), which causes fore-aft pitching. Trotting minimizes both failure modes, making it the most forgiving gait for a student-built controller.

The computational cost of inverse kinematics is the hidden bottleneck. Lab 3's gradient-descent IK requires many FK evaluations per solve — each evaluation involves multiplying four $4 \times 4$ homogeneous transformation matrices, and convergence may take tens of iterations. Running IK for all four legs at 200 Hz would consume most of the available CPU budget on the Raspberry Pi. Lab 4's elegant solution is pre-caching: before the robot starts walking, compute all IK solutions for every waypoint of every leg for one complete gait cycle, then store the resulting joint angle arrays. At runtime, the control loop simply looks up the correct index in the cache, adds the appropriate phase offset per leg, and sends joint commands. This trades startup time and memory for deterministic, near-zero runtime cost — but it sacrifices the ability to adapt trajectories on the fly, a limitation that Lab 5's neural controller eventually overcomes.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Trotting Gait** | A two-phase quadruped gait where diagonal leg pairs (FR+BL and FL+BR) alternate between swing and stance; the most common gait for medium-speed quadruped locomotion |
| **Phase Offset** | The fractional delay ($\phi \in [0, 1)$) applied to a leg's gait cycle relative to a reference leg; for trotting, diagonal partners share $\phi = 0$ while the other pair has $\phi = 0.5$ |
| **Stance Phase** | The portion of the gait cycle when a foot is on the ground and pushing the body forward; the foot moves backward relative to the body at ground contact speed |
| **Swing Phase** | The portion of the gait cycle when a foot is in the air, traveling from liftoff to the next touchdown position; trajectory must clear the ground to avoid scuffing |
| **Gait Cycle** | One complete period $T$ of a leg's motion, from touchdown through stance, liftoff, swing, and back to the next touchdown; all legs share the same cycle period but differ in phase |

<details>
<summary><strong>How It Works</strong> — Coordinated 4-leg trotting</summary>

### Extending FK to All Four Legs

In Lab 2, FK was implemented for the front-left leg only. Lab 4 requires FK for all four legs, each with different hip offsets from the body center. The transformation chain for each leg is:

$$T_{0 \to \text{foot}}^{(i)} = T_{\text{body} \to \text{hip}}^{(i)} \cdot T_{\text{hip} \to \text{thigh}}^{(i)} \cdot T_{\text{thigh} \to \text{shin}}^{(i)} \cdot T_{\text{shin} \to \text{foot}}^{(i)}$$

The body-to-hip transform $T_{\text{body} \to \text{hip}}^{(i)}$ differs per leg, encoding the $x$ (fore-aft) and $y$ (lateral) offset of each hip from the body center. Front legs have positive $x$ offset, back legs negative. Left legs have positive $y$ offset, right legs negative. The remaining transforms in the chain use the same link lengths and joint-axis definitions as Lab 2, but with sign flips for left vs. right legs on the hip abduction axis.

### Diagonal Pairing and Phase Timing

The trot divides the gait cycle into two halves. During the first half, legs FR and BL are in stance (on the ground) while FL and BR are in swing (in the air). At the halfway point, they swap roles.

```
TROTTING GAIT — Phase Timing for All Four Legs
================================================================

  Phase:    0%        25%        50%        75%       100%
            |          |          |          |          |
  FR  ══════STANCE══════╗         ╔═══SWING═══╗         ╔══
            ████████████║         ║░░░░░░░░░░░║         ║██
  BL  ══════STANCE══════╝         ╚═══SWING═══╝         ╚══
            ████████████           ░░░░░░░░░░░           ██

  FL  ═══SWING═══╗         ╔══════STANCE══════╗         ╔══
            ░░░░░░░░░░░║         ║████████████║         ║░░
  BR  ═══SWING═══╝         ╚══════STANCE══════╝         ╚══
            ░░░░░░░░░░░           ████████████           ░░

  ████ = foot on ground (stance)    ░░░░ = foot in air (swing)

  DIAGONAL PAIRS:
    Pair A: FR + BL  →  phase offset φ = 0.0
    Pair B: FL + BR  →  phase offset φ = 0.5

  At any instant, exactly one diagonal pair supports the robot:

        t = 0.25              t = 0.75
        ┌────────┐            ┌────────┐
    FR ●│  BODY  │○ FL    FR ○│  BODY  │● FL
        │        │            │        │
    BR ○│        │● BL    BR ●│        │○ BL
        └────────┘            └────────┘
    ● = on ground   ○ = in air
```

### The 6-Waypoint Trajectory

Each leg follows a closed trajectory of 6 waypoints per gait cycle. During stance, the foot traces a line on the ground (3 waypoints moving backward relative to the body). During swing, it traces a triangle arc through the air (liftoff, mid-swing apex, touchdown).

```
SINGLE-LEG TRAJECTORY (side view, body frame)
================================================================

  Height (z)
    ▲
    │         (5) Mid-swing
    │          ╱ ╲
    │         ╱   ╲
    │        ╱     ╲
    │   (4) ╱       ╲ (0)
    │  Liftoff       Touchdown
    │───●───────────────●───── Ground level (z = -h)
    │   (3)    (2)    (1)
    │   Stance  Stance  Stance
    │   end     mid     start
    │
    └──────────────────────────► Forward (x)
        ◄── body moves this way

  WAYPOINT TABLE (relative to hip, approximate):
  ┌─────┬──────────────┬────────┬────────────────────────────┐
  │  #  │  Name        │ (x, z) │ Phase in cycle             │
  ├─────┼──────────────┼────────┼────────────────────────────┤
  │  0  │ Touchdown    │ (+d, -h)│ 0.0  — foot contacts ground│
  │  1  │ Stance start │ (+⅔d,-h)│ 0.1  — pushing backward    │
  │  2  │ Stance mid   │ (0, -h) │ 0.25 — directly below hip  │
  │  3  │ Stance end   │ (-d, -h)│ 0.4  — about to lift off   │
  │  4  │ Liftoff      │ (-d,-h+ε)│ 0.5  — foot leaves ground  │
  │  5  │ Mid-swing    │ (0,-h+Δ)│ 0.75 — apex of swing arc   │
  └─────┴──────────────┴────────┴────────────────────────────┘

  d = half stride length    h = nominal leg height
  Δ = swing clearance       ε = small liftoff height
```

### Pre-Caching the Gait

Before the robot begins walking, Lab 4 discretizes one full gait cycle into $N$ timesteps (e.g., $N = 100$). For each timestep $k$ and each leg $i$:

1. Compute the foot target position $\mathbf{p}_k^{(i)}$ by interpolating between waypoints, applying leg $i$'s phase offset $\phi_i$
2. Run gradient-descent IK to solve for joint angles: $\boldsymbol{\theta}_k^{(i)} = \text{IK}(\mathbf{p}_k^{(i)})$
3. Store $\boldsymbol{\theta}_k^{(i)}$ in a lookup table

At runtime, the control loop maintains a single cycle counter $k$ that increments each tick. Each leg reads from the cache at index $(k + \phi_i \cdot N) \mod N$, and the PD controller tracks the retrieved joint angles. The entire walk reduces to a modular array lookup.

```
PRE-CACHE STRUCTURE (conceptual)
================================================================

  cache[leg][timestep] = (θ_hip, θ_thigh, θ_knee)

  Leg:    FR (φ=0.0)    FL (φ=0.5)    BR (φ=0.5)    BL (φ=0.0)
  ──────────────────────────────────────────────────────────────
  k=0     cache[0][0]   cache[1][50]  cache[2][50]  cache[3][0]
  k=1     cache[0][1]   cache[1][51]  cache[2][51]  cache[3][1]
  k=2     cache[0][2]   cache[1][52]  cache[2][52]  cache[3][2]
  ...     ...           ...           ...           ...
  k=49    cache[0][49]  cache[1][99]  cache[2][99]  cache[3][49]
  k=50    cache[0][50]  cache[1][0]   cache[2][0]   cache[3][50]
  ...     (wraps mod N=100)
```

</details>

<details>
<summary><strong>The Key Tension</strong> — Pre-cached vs. real-time IK</summary>

Lab 4's pre-caching strategy is a deliberate engineering tradeoff that reveals a fundamental tension in robot control: **determinism vs. adaptability**.

### Why Pre-Cache?

**Computational cost.** Lab 3's gradient-descent IK solves one leg at ~20 Hz. Scaling to four legs in real time would drop the effective rate to ~5 Hz per leg — far too slow for smooth locomotion. Pre-caching moves all IK computation to a one-time startup phase, leaving the 200 Hz runtime loop free for PD control alone.

**Determinism.** Gradient descent is iterative and its convergence time varies depending on the initial guess and target proximity. In real time, an IK solve that takes 3x longer than average could cause a missed control deadline, producing a visible hitch in the gait. Pre-cached trajectories eliminate this variability entirely — every timestep costs exactly one array lookup.

**Reproducibility.** The same cache produces the same gait every time. This makes debugging straightforward: if the robot stumbles, the problem is in PD tuning or hardware, not in a non-deterministic IK solution that happened to converge to a different local minimum.

### What You Lose

**Terrain adaptation.** If the robot encounters a slope, a step, or an obstacle, the pre-cached trajectory cannot adjust. The feet will follow the same path regardless of ground contact, potentially causing slipping or stumbling.

**Velocity changes.** Changing walking speed requires either recomputing the entire cache (expensive) or interpolating between pre-computed caches at different speeds (complex). A real-time IK system could simply adjust foot targets on the fly.

**Reactive balance.** When the robot is pushed or tilts unexpectedly, the pre-cached gait cannot shift foot placements to recover balance. The PD controller can resist perturbations to some degree, but the foot trajectory itself is fixed.

This is precisely the limitation that motivates Lab 5: a neural network policy trained via reinforcement learning replaces the entire FK + IK + gait pipeline. The RL policy runs at ~52 Hz, outputs joint targets directly (no IK solve needed), and has learned to adapt to perturbations, terrain variation, and even missing legs — capabilities that are effectively impossible with a pre-cached open-loop gait.

| Aspect | Pre-Cached (Lab 4) | Real-Time IK | Neural Policy (Lab 5) |
|--------|--------------------|--------------|-----------------------|
| Runtime cost per leg | $O(1)$ array lookup | $O(n \cdot k)$ per IK solve | $O(1)$ network forward pass |
| Terrain adaptation | None | Possible with sensor feedback | Learned from simulation |
| Velocity changes | Requires re-cache | Adjust targets directly | Commanded via `/cmd_vel` |
| Predictability | Fully deterministic | Varies per solve | Stochastic but robust |
| Setup complexity | Moderate | Low | High (sim training) |

</details>

<details>
<summary><strong>Concrete Example</strong> — One gait cycle traced</summary>

Here is one complete gait cycle ($T = 0.5$ s, i.e., 2 Hz trot) traced through all four legs. The cycle is discretized into $N = 100$ steps at 200 Hz (one step every 5 ms).

```
FULL GAIT CYCLE TRACE — 4 legs, 100 timesteps, T = 0.5s
================================================================

Timestep  Phase   FR (φ=0.0)       BL (φ=0.0)       FL (φ=0.5)       BR (φ=0.5)
────────  ──────  ───────────────  ───────────────  ───────────────  ───────────────
k=0       0.00    TOUCHDOWN        TOUCHDOWN        MID-STANCE       MID-STANCE
                  foot hits ground  foot hits ground  pushing back     pushing back

k=10      0.10    EARLY STANCE     EARLY STANCE     LATE STANCE      LATE STANCE
                  push begins      push begins      approaching lift  approaching lift

k=25      0.25    MID-STANCE       MID-STANCE       STANCE END       STANCE END
                  foot below hip   foot below hip   foot behind hip  foot behind hip

k=40      0.40    LATE STANCE      LATE STANCE      LIFTOFF          LIFTOFF
                  nearing liftoff  nearing liftoff  foot leaves ground foot leaves ground

k=50      0.50    LIFTOFF          LIFTOFF          TOUCHDOWN        TOUCHDOWN
                  *** PHASE SWAP — diagonal pairs exchange roles ***

k=60      0.60    EARLY SWING      EARLY SWING      EARLY STANCE     EARLY STANCE
                  foot rising      foot rising      push begins      push begins

k=75      0.75    MID-SWING        MID-SWING        MID-STANCE       MID-STANCE
                  apex of arc      apex of arc      foot below hip   foot below hip

k=90      0.90    LATE SWING       LATE SWING       LATE STANCE      LATE STANCE
                  foot descending  foot descending  nearing liftoff  nearing liftoff

k=100     1.00    TOUCHDOWN        TOUCHDOWN        LIFTOFF          LIFTOFF
          =0.00   *** CYCLE REPEATS ***
```

**Walking through the phase swap at $k = 50$:**

At $k = 49$, FR and BL are finishing their stance phase — feet are on the ground, behind the hip, having pushed the body forward. FL and BR are finishing their swing — feet are descending toward their touchdown positions ahead of the hip.

At $k = 50$, the swap happens simultaneously:
- FR and BL lift off the ground, beginning their swing arcs
- FL and BR touch down, beginning to support the body

The PD controller sees a smooth transition because the pre-cached trajectory is continuous: the liftoff joint angles at $k = 50$ are very close to the late-stance angles at $k = 49$, with only a slight vertical displacement $\epsilon$ separating them.

**What the joint angles look like** for one leg (FR) through the cycle:

```
FR JOINT ANGLES OVER ONE GAIT CYCLE
================================================================

  θ_hip (abduction)         Mostly constant — slight adjustment
  ────────────────          for lateral foot placement
   5° ─────────────────────────────────────────────────────
   0° ─────────────────────────────────────────────────────

  θ_thigh (shoulder)        Oscillates: forward in stance, backward in swing
  ──────────────────
  20° ─          ──────
      ─        ─      ─
  10° ──      ─        ──
       ──   ─           ──
   0° ───────             ─────
       STANCE              SWING
      0%    25%    50%    75%    100%

  θ_knee (elbow)            Extends in stance, flexes sharply in swing
  ──────────────
 -20° ─────────             ─────
       ──   ─           ──
 -40°   ──      ─        ──
          ─        ─      ─
 -60°      ─          ──────
           STANCE      SWING
      0%    25%    50%    75%    100%
```

**The one thing most outsiders get wrong about this is...** assuming gait control is primarily about leg trajectories. In practice, the hard part is timing coordination. A single leg following a perfect triangle trajectory is easy (Lab 3 already does it). Making four legs share a single clock, maintain precise phase relationships, and transition cleanly between stance and swing without the PD controllers fighting each other — that is where Lab 4's real complexity lives. The pre-caching strategy elegantly sidesteps per-leg IK timing jitter, but the phase offset math and hip offset transforms are where students spend most of their debugging time.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/pupper-v3-labs]]** — The full 7-lab progression. Lab 4 sits at the pivot point between single-leg control (Labs 1-3) and full-system intelligence (Labs 5-7). Everything after Lab 4 assumes a working trotting gait.
- **[[quick-context/pupper-brain]]** — The dual-STM32 + Raspberry Pi hardware that runs this gait. The 200 Hz PD loop executes on the Pi's ROS2 stack, while the 1 kHz motor control loop runs on the STM32, meaning Lab 4's cached joint targets are downsampled and interpolated by the [[learning/notes/micro-context/microcontroller|microcontroller]] firmware.
- **Other quadruped gaits** — Trotting is one of many: *walking* (3 feet always grounded, slowest but most stable), *pacing* (ipsilateral pairs, used by camels), *bounding* (front/back pairs, fast but unstable), *galloping* (asymmetric, fastest). Each has different duty factors and phase relationships.
- **Static vs. dynamic stability** — A statically stable gait keeps the center of mass within the support polygon at all times (requires 3+ feet on the ground). Trotting is only *dynamically* stable — with just 2 feet down, the robot relies on momentum and fast gait cycling to avoid falling. This is why trot speed matters: too slow and the robot tips between steps.
- **Zero Moment Point (ZMP)** — A formal stability criterion used in humanoid and quadruped robotics. The ZMP is the point on the ground where the net moment of inertial and gravitational forces is zero. If the ZMP stays within the support polygon, the robot won't tip. Lab 4's trot doesn't explicitly compute ZMP, but the diagonal pairing implicitly keeps it near the body center.
- **Central Pattern Generators (CPGs)** — Biological approach to gait generation inspired by neural circuits in animal spinal cords. CPGs use coupled oscillators to produce rhythmic leg motion with tunable phase relationships, offering a more biologically plausible alternative to Lab 4's waypoint interpolation.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does the trotting gait pair diagonal legs (FR+BL) rather than same-side legs (FR+BR) or same-end legs (FR+FL)?

<details>
<summary>Answer</summary>
Diagonal pairing maximizes stability by placing the two support points on opposite corners of the body. The line connecting FR and BL passes roughly through the center of mass, preventing both roll and pitch. Same-side pairing (pacing: FR+BR) creates a support line along one side of the body, causing the robot to rock laterally since the CoM is not over the support. Same-end pairing (bounding: FR+FL) places both support points at one end, causing the body to pitch forward or backward. Trotting is the only two-phase gait where the support geometry naturally contains the center of mass projection.
</details>

**Q2:** The pre-cache uses $N = 100$ timesteps at 200 Hz, giving a gait period of $T = 0.5$ s. If you wanted the robot to walk slower (say $T = 1.0$ s) without recomputing IK, could you simply step through the cache at half speed (incrementing $k$ every other control tick)?

<details>
<summary>Answer</summary>
Yes, this works and is a common trick. By incrementing the cache index every 2nd tick instead of every tick, the same 100-waypoint trajectory is played back over 1.0 s instead of 0.5 s. The foot positions remain identical — only the timing changes. However, there are limits: the stance-phase foot velocity relative to the ground must match the body's forward velocity, or the feet will slip. If you halve the playback speed, the body also moves at half speed (since stance pushback is half as fast), so the gait remains self-consistent. But you cannot independently change speed and stride length without recomputing the cache with different waypoint positions.
</details>

**Q3:** Lab 4 pre-caches all IK solutions at startup. What would happen if one leg's IK fails to converge for a particular waypoint, and how might you detect or handle this?

<details>
<summary>Answer</summary>
If gradient-descent IK fails to converge (cost remains above threshold after max iterations), the cached joint angles for that waypoint will be wrong — the foot won't reach its target position. During the gait, this manifests as the leg "missing" a step or jerking to an unexpected pose. Detection strategies: (1) check the final IK cost after each solve during pre-caching and flag waypoints that didn't converge below a threshold, (2) verify that consecutive cached angles don't have discontinuous jumps (which indicate the IK found a different local minimum). Handling strategies: increase iteration count, use the previous waypoint's solution as the initial guess (warm-starting), or reduce the waypoint spacing so targets are closer together and easier to solve.
</details>

</details>
