---
topic: Why Current Through a Coil Creates a Magnetic Field
created: 2026-02-14
---

> **Related:** [[learning/notes/quick-context/electric-magnetic-field-unification|Electric and Magnetic Field Unification]] | [[learning/notes/quick-context/voltage-current-causality|Voltage-Current Causality]] | [[learning/notes/micro-context/tail-current|Tail Current]] | [[learning/notes/micro-context/quiescent-supply-current|Quiescent Supply Current]] | [[learning/notes/micro-context/mosfet|MOSFET]]

# Why Current Through a Coil Creates a Magnetic Field


> **TL;DR:** Moving electric charges create magnetic fields—this is a fundamental law of nature confirmed by Maxwell's equations and explained by special relativity. When you coil a wire, you concentrate and align the circular magnetic fields from each turn, creating a strong, uniform field inside the coil whose strength is calculated by B = μ₀nI (field = permeability × turns per length × current).

## The Core Problem

You've wrapped wire into a coil and run [[quick-context/electric-current|current]] through it. Suddenly it acts like a magnet—attracting iron, deflecting compasses, storing energy. But *why* does moving charge create magnetism at all? And once you accept that it does, how do you calculate the resulting field strength? These questions sit at the heart of [[quick-context/electromagnetism|electromagnetism]]: understanding them unlocks motors, generators, [[quick-context/inductor|inductors]], transformers, MRI machines, and the physics of how all wireless communication works.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Ampère's Law** | A circulating current creates a magnetic field that curls around the current. Mathematically: ∮B·dl = μ₀I (the line integral of B around any closed loop equals μ₀ times the enclosed current). |
| **Permeability (μ₀)** | The fundamental constant relating current to magnetic field in a vacuum: μ₀ = 4π × 10⁻⁷ T·m/A. In magnetic materials like iron, effective permeability μ can be 1000-100,000× higher. |
| **Solenoid** | A coil of wire wound in a helix. When current flows, it creates a nearly uniform magnetic field inside and near-zero field outside—an ideal electromagnet geometry. |
| **Magnetic Field (B)** | The vector field created by moving charges. Measured in tesla (T). Earth's field: ~50 μT. Strong permanent magnet: ~1 T. MRI machine: 1.5-7 T. |
| **Right-Hand Rule** | Point thumb in current direction; fingers curl in direction of magnetic field. For a coil: curl fingers in current direction; thumb points to north pole (field direction inside). |

<details>
<summary><strong>How It Works</strong> — From single wire to powerful electromagnet</summary>

## The Fundamental Fact: Moving Charges Create Magnetic Fields

This isn't derived from something more basic—it's a law of nature. Experiments show it. [[learning/notes/quick-context/maxwell-equations|Maxwell's equations]] encode it. Special relativity explains it as a consequence of how electric fields transform between reference frames. But at the practical level: **any moving electric charge creates a magnetic field that circles around its direction of motion.**

```
WHY MOVING CHARGES CREATE MAGNETIC FIELDS — The Deep Answer
══════════════════════════════════════════════════════════════════════════════

THE EXPERIMENTAL FACT (Oersted, 1820):
──────────────────────────────────────────────────────────────────────────────

    A compass needle deflects when placed near a wire carrying current.

              Before                          After (current ON)
              ──────                          ─────────────────

         N ←───────── S                            ↑
              ↑                                    │
           Compass                            N ───┼─── S
           points                                  │
           to Earth's                         Compass deflected
           magnetic north                     by wire's field


    This was the first evidence that electricity and magnetism are related.
    It led directly to Maxwell's equations and our modern understanding.


THE RELATIVISTIC EXPLANATION (Einstein, 1905):
──────────────────────────────────────────────────────────────────────────────

    The magnetic field is the ELECTRIC field as seen from a moving frame.

    Imagine you're stationary next to a wire with current flowing:
    • You see moving electrons (negative) and stationary protons (positive)
    • The wire is electrically neutral (same number of + and - charges)
    • But you also observe a MAGNETIC field around the wire

    Now imagine you're moving WITH the electrons:
    • You see the electrons as stationary
    • You see the protons moving backward
    • Due to length contraction (special relativity), the proton
      spacing appears different than electron spacing
    • The wire is NO LONGER NEUTRAL in your frame—it has net charge!
    • That net charge creates an ELECTRIC field

    What one observer calls a "magnetic field," another calls an "electric
    field." They're the same phenomenon viewed from different velocities.

    This is why we say "electromagnetism"—they're fundamentally ONE thing.


THE PRACTICAL ANSWER (What to remember):
──────────────────────────────────────────────────────────────────────────────

    Moving charges create magnetic fields. That's the rule.

    WHY? Because that's how spacetime and charge behave at the deepest level.
    Maxwell encoded this as one of his four equations (Ampère's Law).
    Einstein showed it's inevitable once you accept special relativity.

    For engineering purposes: accept the fact, learn to calculate with it.
```

## Single Wire: The Starting Point

When [[quick-context/electric-current|current]] flows through a straight wire, the magnetic field forms concentric circles around the wire:

```
MAGNETIC FIELD AROUND A STRAIGHT WIRE — Biot-Savart Law
══════════════════════════════════════════════════════════════════════════════

    SIDE VIEW                              END VIEW (looking along wire)
    ─────────                              ─────────────────────────────

         │ I                                      ┌───╮
         │ ↓                                    ╱  ╭───╮ ╲
         │                                    ╱  ╱     ╲  ╲
         │     B field                       │  │   ⊗   │  │  ← current INTO page
         │   ╭───────╮                       │  │  wire │  │
         │  ╱         ╲                       ╲  ╲     ╱  ╱
         │ │           │                       ╲  ╰───╯ ╱
         │  ╲         ╱                          ╰───╯
         │   ╰───────╯
         │                                    B field circles CLOCKWISE
         │                                    (when current goes INTO page)
         ▼


    FORMULA FOR FIELD STRENGTH:
    ──────────────────────────────────────────────────────────────────────────

        B = μ₀I / (2πr)

        B  = magnetic field strength (tesla)
        μ₀ = 4π × 10⁻⁷ T·m/A (permeability of free space)
        I  = current (amperes)
        r  = distance from wire (meters)

    EXAMPLE: 10 amps through a wire, at 1 cm distance:

        B = (4π × 10⁻⁷) × 10 / (2π × 0.01)
        B = (4 × 10⁻⁶) / 0.02
        B = 2 × 10⁻⁴ T = 200 μT

        That's about 4× Earth's magnetic field—enough to deflect a compass!


THE RIGHT-HAND RULE:
──────────────────────────────────────────────────────────────────────────────

    Point THUMB in direction of current (conventional: + to -)
    FINGERS curl in direction of magnetic field

            Thumb → I (current direction)
              │
              │     ╭───╮
              │    ╱     ╲
              ▼   │   ⊗   │   ← B field circles around wire
                   ╲     ╱
                    ╰───╯

    Current into page (⊗): field circles clockwise
    Current out of page (⊙): field circles counter-clockwise
```

## Why Coiling the Wire Amplifies the Field

A single loop of wire creates a magnetic field, but most of it spreads out into space. When you wind many turns close together, something powerful happens:

```
FROM SINGLE LOOP TO SOLENOID — Field Amplification
══════════════════════════════════════════════════════════════════════════════

SINGLE LOOP:
──────────────────────────────────────────────────────────────────────────────

                ─────→ B ─────→
               ╱               ╲
              ╱                 ╲
             │    ┌───────┐      │
             │    │       │      │    Field spreads out
             ↑    │ LOOP  │      ↓    Not very concentrated
             │    │       │      │
              ╲   └───────┘     ╱
               ╲               ╱
                ←─────────────←

    Each segment of the loop creates its own circular field.
    Inside the loop, all these fields ADD UP (same direction).
    Outside the loop, they partially CANCEL.


MULTIPLE LOOPS (SOLENOID):
──────────────────────────────────────────────────────────────────────────────

    Side view of a solenoid (coil with N turns):

              I →                             → I
        ┌────────────────────────────────────────┐
        │ ⊗  ⊗  ⊗  ⊗  ⊗  ⊗  ⊗  ⊗  ⊗  ⊗  ⊗  ⊗ │  ← wire going INTO page
        │                                        │
        │  ══════════════════════════════════    │  ← B field INSIDE (uniform)
        │  ══════════════════════════════════    │     (strong, parallel)
        │  ══════════════════════════════════    │
        │                                        │
        │ ⊙  ⊙  ⊙  ⊙  ⊙  ⊙  ⊙  ⊙  ⊙  ⊙  ⊙  ⊙ │  ← wire coming OUT of page
        └────────────────────────────────────────┘
          S                                    N
        South pole                         North pole


    WHY THIS WORKS:
    ─────────────────────────────────────────────────────────────────────────

    1. Each loop creates a field that goes THROUGH the center of the loop

    2. Loops are stacked so all their fields point the SAME direction

    3. Inside the solenoid: fields from all N turns ADD together
       B_total = N × B_single_loop

    4. Outside the solenoid: fields from opposite sides CANCEL
       (One side has current going left, other side has current going right)

    5. Result: Strong, uniform field INSIDE. Nearly zero field OUTSIDE.


                    Outside: B ≈ 0                Outside: B ≈ 0
                         │                              │
                         ▼                              ▼
            ═══ ← ═══ ═══════════════════════════ ═══ → ═══
                    │                              │
                    │         INSIDE:              │
                    │      B = μ₀ × n × I          │
                    │     (strong, uniform)        │
                    │                              │
            ═══ ← ═══ ═══════════════════════════ ═══ → ═══

    The field lines form closed loops (required by Maxwell's equations).
    They exit the N pole, curve around outside, re-enter at S pole.
    But outside the coil, they're spread over a huge volume → weak.
    Inside the coil, they're concentrated → strong.
```

## Calculating Solenoid Field Strength

The formula for the magnetic field inside a solenoid is elegantly simple:

```
SOLENOID FIELD FORMULA
══════════════════════════════════════════════════════════════════════════════

        B = μ₀ × n × I

    WHERE:
    ─────────────────────────────────────────────────────────────────────────

    B  = magnetic field strength inside the solenoid (tesla)

    μ₀ = permeability of free space = 4π × 10⁻⁷ T·m/A
         (This is a fundamental constant of nature)

    n  = number of turns per unit length (turns/meter)
         If you have N total turns over length L: n = N/L

    I  = current through the wire (amperes)


    ALTERNATIVE FORM:
    ─────────────────────────────────────────────────────────────────────────

        B = μ₀ × N × I / L

    WHERE:
        N = total number of turns
        L = length of solenoid (meters)


WHY THIS FORMULA WORKS (Ampère's Law derivation):
══════════════════════════════════════════════════════════════════════════════

    Ampère's Law states: ∮ B · dl = μ₀ × I_enclosed

    "The line integral of B around any closed path equals μ₀ times
     the total current passing through the area enclosed by that path"

    Apply this to a rectangular path through a solenoid:

                 b ─────────────────────────── c
                 │                             │
        OUTSIDE  │           INSIDE            │  OUTSIDE
        B ≈ 0    │         B = strong          │  B ≈ 0
                 │                             │
                 a ─────────────────────────── d


    Path a→b: Outside solenoid, B ≈ 0, contributes ~0
    Path b→c: Inside solenoid, B parallel to path, contributes B × L
    Path c→d: Outside solenoid, B ≈ 0, contributes ~0
    Path d→a: Perpendicular to B, contributes 0

    Total: ∮ B · dl = B × L

    Current enclosed: If path encloses n × L turns, each carrying I:
    I_enclosed = n × L × I

    Setting them equal (Ampère's Law):
    B × L = μ₀ × n × L × I

    Solving for B:
    B = μ₀ × n × I  ✓


PRACTICAL CALCULATIONS:
══════════════════════════════════════════════════════════════════════════════

    EXAMPLE 1: Simple electromagnet
    ─────────────────────────────────────────────────────────────────────────

    Coil specifications:
    • 500 turns (N = 500)
    • 10 cm long (L = 0.1 m)
    • 2 amps current (I = 2 A)

    Turns per meter: n = 500 / 0.1 = 5000 turns/m

    Field strength:
    B = μ₀ × n × I
    B = (4π × 10⁻⁷) × 5000 × 2
    B = (1.257 × 10⁻⁶) × 10000
    B = 0.01257 T ≈ 12.6 mT

    That's about 250× Earth's field! Strong enough to attract iron.


    EXAMPLE 2: MRI machine
    ─────────────────────────────────────────────────────────────────────────

    Target: B = 3 T (typical clinical MRI)

    Rearranging: I = B / (μ₀ × n)

    If n = 10,000 turns/m (reasonable for superconducting coil):
    I = 3 / (4π × 10⁻⁷ × 10000)
    I = 3 / 0.01257
    I ≈ 239 Amps

    This is why MRI machines use superconducting coils—regular copper
    would melt at these currents. Superconductors have zero resistance,
    so no heating occurs.


    EXAMPLE 3: Magnetizer (from permanent magnet creation)
    ─────────────────────────────────────────────────────────────────────────

    Industrial magnetizers need B > 1 T for a few milliseconds.

    If n = 2000 turns/m:
    I = 1 / (4π × 10⁻⁷ × 2000)
    I = 1 / 0.00251
    I ≈ 398 Amps

    Achieved via capacitor discharge—charge slowly, release all at once.
```

## Adding a Magnetic Core: Massive Amplification

Air-core solenoids are limited. Wrapping the coil around iron or ferrite dramatically increases the field:

```
EFFECT OF MAGNETIC CORE MATERIAL
══════════════════════════════════════════════════════════════════════════════

    WITH AIR CORE:              WITH IRON CORE:
    ──────────────              ───────────────

    B = μ₀ × n × I              B = μ × n × I = μᵣ × μ₀ × n × I

    μ₀ ≈ 1.257 × 10⁻⁶           μᵣ (relative permeability):
                                • Pure iron: 4,000 - 5,000
                                • Silicon steel: 7,000
                                • Permalloy: 100,000
                                • Supermalloy: 800,000


    AMPLIFICATION FACTOR:
    ─────────────────────────────────────────────────────────────────────────

    Same coil with iron core vs air core:

    If μᵣ = 5000 (typical iron):
    B_iron = 5000 × B_air

    Your 12.6 mT air-core electromagnet becomes 63 T with iron!
    (In reality, iron saturates around 2 T, limiting this)


    WHY IRON WORKS — Domain Alignment:
    ─────────────────────────────────────────────────────────────────────────

    Iron has magnetic domains (see permanent magnet creation).
    The external field from your coil aligns these domains.
    The aligned domains produce their OWN field that adds to the coil's field.

    It's like having a crowd of people pushing:
    • Air core: just you pushing
    • Iron core: you + 5000 helpers all pushing together


    CORE MATERIALS COMPARISON:
    ─────────────────────────────────────────────────────────────────────────

    Material          │ μᵣ          │ Best For
    ══════════════════╪═════════════╪════════════════════════════════════
    Air               │ 1           │ High-frequency, no saturation
    Ferrite           │ 1000-3000   │ High-frequency (low losses)
    Powdered iron     │ 10-100      │ High current (gradual saturation)
    Silicon steel     │ 5000-7000   │ Transformers, motors
    Pure iron         │ 4000-5000   │ DC electromagnets
    Mumetal           │ 80,000-100,000 │ Magnetic shielding


    SATURATION — The Limit:
    ─────────────────────────────────────────────────────────────────────────

    Iron can only amplify so much. Once ALL domains are aligned,
    adding more current doesn't help—the core is "saturated."

    B
    ▲
    │                    ___________
    │                 __/
    │              __/
    │           __/  ← Saturation point
    │         _/       (all domains aligned)
    │       _/
    │     _/
    │   _/
    │  /  ← Linear region (B ∝ H)
    │ /
    │/
    └──────────────────────────────────────► H (magnetic field intensity = nI)

    For iron: saturation ≈ 2 T
    For ferrite: saturation ≈ 0.4 T

    This is why inductors have "saturation current" ratings.
    (See [[quick-context/inductor]])
```

</details>

<details>
<summary><strong>The Key Tension</strong> — Field strength vs. practical limits</summary>

## More Current = Stronger Field... Until Reality Intervenes

The formula B = μ₀nI seems to promise unlimited field strength: just add more turns or more current. In practice, several factors limit what's achievable:

```
THE ENGINEERING TRADEOFFS
══════════════════════════════════════════════════════════════════════════════

WANT STRONGER FIELD?         REALITY CHECK
═══════════════════════════════════════════════════════════════════════════════

Add more turns (↑ n)    →    More wire = more resistance = more heat
                             More wire = more inductance = slower response
                             More wire = larger, heavier coil

Increase current (↑ I) →    I²R heating (power loss scales with I²!)
                             Thicker wire needed (larger coil)
                             Power supply requirements increase

Use magnetic core      →    Core saturates at ~2T (iron)
                             Core has losses at AC frequencies
                             Core adds weight and cost

Go superconducting     →    Requires cryogenic cooling (-269°C)
                             Expensive infrastructure
                             Limited to specialized applications


THE HEAT PROBLEM IN DETAIL:
──────────────────────────────────────────────────────────────────────────────

    Power dissipated = I² × R

    If you double current:
    • Field doubles (B ∝ I)
    • Power dissipation QUADRUPLES (P ∝ I²)

    Example:
    • 100-turn coil, 10Ω total resistance
    • At 1A: P = 1² × 10 = 10W (warm)
    • At 2A: P = 2² × 10 = 40W (hot!)
    • At 5A: P = 5² × 10 = 250W (melting wire)

    This is why high-field magnets use:
    • Thick wire (low R) — but increases size/weight
    • Active cooling (water, oil) — adds complexity
    • Pulsed operation (brief current) — only for specialized uses
    • Superconductors (R = 0) — expensive, needs cryogenics
```

| Application | Field Needed | Solution |
|-------------|-------------|----------|
| Door electromagnet | 0.01-0.1 T | Air gap, iron core, modest current |
| Inductor in power supply | Specified inductance, not field | Ferrite or powdered iron core |
| Motor/Generator | 0.5-2 T | Laminated steel core, optimized geometry |
| MRI machine | 1.5-7 T | Superconducting coil |
| Research magnets | 10-45 T | Hybrid superconducting + resistive |
| Pulsed magnets | 100+ T | [[learning/notes/quick-context/capacitor|Capacitor]] discharge, coil often destroyed |

</details>

<details>
<summary><strong>Concrete Example</strong> — Designing a simple electromagnet</summary>

## Example: Building an Electromagnet to Lift Iron

Let's design a practical electromagnet and calculate its performance.

```
ELECTROMAGNET DESIGN WALKTHROUGH
══════════════════════════════════════════════════════════════════════════════

GOAL: Lift a 1 kg piece of iron

CONSTRAINTS:
• Power supply: 12V
• Maximum continuous current: 2A (24W power budget)
• Wire: 22 AWG copper (0.644 mm diameter, 52.9 mΩ/m)


STEP 1: Choose a Core
──────────────────────────────────────────────────────────────────────────────

    Using a soft iron bolt, 8mm diameter, 50mm long
    Relative permeability: μᵣ ≈ 4000 (typical soft iron)


STEP 2: Determine Wire Length from Resistance Constraint
──────────────────────────────────────────────────────────────────────────────

    At 2A from 12V: R = V/I = 12/2 = 6Ω maximum

    Wire resistance: 52.9 mΩ/m = 0.0529 Ω/m

    Maximum wire length: L_wire = 6 / 0.0529 = 113 meters

    (We'll use ~100m to leave some margin)


STEP 3: Calculate Number of Turns
──────────────────────────────────────────────────────────────────────────────

    Each turn wraps around the 8mm bolt.
    Circumference per turn ≈ π × 8mm = 25mm = 0.025m

    Number of turns from 100m wire:
    N = 100 / 0.025 = 4000 turns

    That's a LOT of turns! But with thin wire, they'll fit.

    With 0.644mm wire, each layer ≈ 50mm / 0.7mm ≈ 70 turns
    Number of layers needed: 4000 / 70 ≈ 57 layers
    Coil thickness: 57 × 0.7mm ≈ 40mm outer radius

    This is getting bulky. Let's use 500 turns as a practical compromise.


STEP 4: Recalculate with 500 Turns
──────────────────────────────────────────────────────────────────────────────

    Wire length: 500 × 0.025m = 12.5m
    Resistance: 12.5 × 0.0529 = 0.66Ω

    At 12V: I = V/R = 12/0.66 = 18A  (way too high!)

    We need to add resistance. Use 6Ω total (includes coil):
    I = 12/6 = 2A (within budget)
    External resistor needed: 6 - 0.66 = 5.34Ω (use 5Ω + wire resistance)


STEP 5: Calculate Magnetic Field
──────────────────────────────────────────────────────────────────────────────

    With iron core (μᵣ = 4000):

    n = N/L = 500 / 0.05 = 10,000 turns/m

    B = μᵣ × μ₀ × n × I
    B = 4000 × (4π × 10⁻⁷) × 10,000 × 2
    B = 4000 × 1.257 × 10⁻⁶ × 20,000
    B = 100.5 T  (theoretical!)

    BUT iron saturates at ~2T, so actual field ≈ 1.5-2 T


STEP 6: Estimate Lifting Force
──────────────────────────────────────────────────────────────────────────────

    Approximate formula for electromagnet force:

    F = B² × A / (2 × μ₀)

    Where A = pole area = π × (4mm)² = 50 mm² = 50 × 10⁻⁶ m²

    At B = 1.5 T:
    F = (1.5)² × (50 × 10⁻⁶) / (2 × 4π × 10⁻⁷)
    F = 2.25 × 50 × 10⁻⁶ / (2.51 × 10⁻⁶)
    F = 44.8 N ≈ 45 N

    That's enough to lift 4.5 kg! Our 1 kg target is easily met.


FINAL DESIGN:
──────────────────────────────────────────────────────────────────────────────

    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │     12V DC ───┬──────────────────────────────────────┬──── GND     │
    │               │                                      │              │
    │          [5Ω resistor]                               │              │
    │               │                                      │              │
    │               └──────────⊃⊃⊃⊃⊃⊃⊃⊃⊃⊃⊃⊃⊃⊃⊃⊃──────────┘              │
    │                         ║          ║                                │
    │                     ════╬══════════╬════                            │
    │                         ║ IRON BOLT║                                │
    │                     ════╬══════════╬════                            │
    │                         ║    ↑N    ║                                │
    │                              │                                      │
    │                        Lifting force ~45N                           │
    │                                                                     │
    │     Specifications:                                                 │
    │     • 500 turns of 22 AWG wire                                      │
    │     • 8mm × 50mm soft iron core                                     │
    │     • Operating current: 2A at 12V                                  │
    │     • Power consumption: 24W                                        │
    │     • Field at pole: ~1.5 T                                         │
    │     • Lift capacity: ~4 kg                                          │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
```

**The one thing most outsiders get wrong about this is...** assuming more wire always means a stronger magnet. More turns increase n (turns per length), which increases B—but more wire also increases resistance R. With a fixed [[learning/notes/quick-context/voltage|voltage]] supply, higher R means *less* current (I = V/R). Since B depends on both n and I, there's an optimum point. You can have a coil with thousands of turns that produces a weak field because the current is tiny. The art of electromagnet design is balancing turns, current, resistance, heat dissipation, and core saturation. Simply wrapping more wire isn't the answer.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/electromagnetism]]** — The full picture of how electric and magnetic fields interact, including [[quick-context/maxwell-equations|Maxwell's equations]] and electromagnetic waves. This document explains the specific case; [[learning/notes/quick-context/electromagnetism|electromagnetism]] covers the universal principles.

- **[[quick-context/inductor]]** — An [[learning/notes/quick-context/inductor|inductor]] is a coil designed to store energy in its magnetic field. The inductor equation V = L×dI/dt comes directly from how changing current changes the magnetic flux through the coil (Faraday's Law).

- **[[quick-context/electric-current]]** — Current is moving charge, and moving charge is what creates the magnetic field. Understanding current as "coulombs per second" connects to calculating the field strength.

- **[[quick-context/electric-magnetic-field-unification|Field Unification]]** — Explains why moving charges create magnetic fields from first principles: electric and magnetic fields are two aspects of one electromagnetic field, transformed by relative motion.

- **[[quick-context/electricity-generation]]** — Generators use the reverse principle: moving a coil through a magnetic field induces current. Same physics, different application.

- **permanent magnet creation** — Shows a practical application: using a high-current coil to magnetize iron. The magnetizer is just a solenoid optimized for maximum field strength during a brief pulse.

- **Helmholtz Coils** — Two identical coils separated by their radius create a very uniform field in the region between them. Used for calibration and research.

- **Superconducting Magnets** — At very low temperatures, some materials have zero electrical resistance. Coils made from these can carry enormous currents without heating, enabling MRI machines and particle accelerators.

- **[[quick-context/faraday-tensor]]** — The relativistic explanation for why moving charges create magnetic fields is made mathematically precise by the [[learning/notes/quick-context/faraday-tensor|Faraday tensor]]. What one observer sees as a pure electric field, another moving observer sees as a mix of E and B—the [[learning/notes/quick-context/tensor|tensor]] transforms correctly between frames.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A compass needle deflects when placed near a wire carrying DC current. What would happen if you reversed the current direction?
<details>
<summary>Answer</summary>
**The compass would deflect in the opposite direction.** The magnetic field direction follows the right-hand rule: thumb points in current direction, fingers curl in field direction. Reverse the current, and the field circles the other way. The compass needle (a small magnet) aligns with this field, so it deflects opposite to before.
</details>

**Q2:** You have a solenoid with 1000 turns over 10 cm carrying 3 amps. Calculate the magnetic field inside (air core).
<details>
<summary>Answer</summary>
**B = 0.0377 T = 37.7 mT.** Using B = μ₀nI: n = 1000/0.1 = 10,000 turns/m. B = (4π × 10⁻⁷) × 10,000 × 3 = 1.257 × 10⁻⁶ × 30,000 = 0.0377 T. This is about 750× Earth's field.
</details>

**Q3:** You add an iron core (μᵣ = 4000) to the solenoid from Q2. What's the new field strength?
<details>
<summary>Answer</summary>
**Approximately 2 T (limited by saturation).** Theoretically, B = μᵣ × B_air = 4000 × 0.0377 = 151 T. But iron saturates around 2 T—once all magnetic domains are aligned, no further increase is possible. The actual field would be close to the saturation value of the specific iron used, typically 1.5-2 T.
</details>

**Q4:** Why does wrapping wire into a coil create a stronger field than a straight wire carrying the same current?
<details>
<summary>Answer</summary>
**Concentration and alignment of field contributions.** Each turn of wire creates a magnetic field. In a coil, the fields from each turn pass through the same central region and all point in the same direction—they add constructively. Meanwhile, the fields outside the coil point in opposite directions from adjacent turns and partially cancel. The result: strong, uniform field inside; weak, spread-out field outside. See: "Why Coiling the Wire Amplifies the Field" diagram.
</details>

**Q5:** An electromagnet runs at 2A and gets warm. To get a stronger field, you double the current to 4A. How much more heat does it generate?
<details>
<summary>Answer</summary>
**4× more heat (quadruple).** Power dissipation P = I²R. When you double I, P increases by 2² = 4. The field only doubles, but heat generation quadruples. This is the fundamental challenge of high-field electromagnets—you hit thermal limits before you hit magnetic limits. See: "The Heat Problem" in The Key Tension.
</details>

</details>
