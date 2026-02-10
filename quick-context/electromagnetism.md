---
topic: Electromagnetism
created: 2026-02-09
---

# Electromagnetism

> **Related:** [[quick-context/electric-magnetic-field-unification|Field Unification]] | [[quick-context/electric-current]] | [[quick-context/inductor]] | [[quick-context/electricity-generation]] | [[quick-context/capacitor]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]

> **TL;DR:** Electromagnetism is the unified physics of electric and magnetic fields—moving charges create magnetic fields, changing magnetic fields create electric fields, and this interplay enables motors, generators, transformers, inductors, and all wireless communication. Maxwell unified these phenomena in 1865, revealing that light itself is an electromagnetic wave.

## The Core Problem: Two Forces That Are Really One

Before the 1800s, electricity and magnetism seemed unrelated. Static electricity made sparks; magnets pointed north. But experiments revealed deep connections: [[quick-context/electric-current|current]] flowing through a wire deflects a compass needle (Oersted, 1820), and moving a magnet through a coil induces current (Faraday, 1831). Maxwell realized these weren't separate forces—they're two aspects of a single electromagnetic field. Any change in one creates the other. This unification explains why we can generate electricity by spinning magnets, why [[quick-context/inductor|inductors]] oppose current changes, why transformers transfer power between isolated coils, and why radio waves travel at the speed of light.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Magnetic Field (B)** | A vector field created by moving charges (current) or changing electric fields. Measured in tesla (T). Earth's field: ~50 μT. Strong magnet: 1 T. MRI machine: 1.5-3 T. |
| **Electric Field (E)** | A vector field created by charges or changing magnetic fields. Measured in volts/meter. Pushes charges in the direction of the field (positive charges) or opposite (negative). |
| **Electromagnetic Induction** | A changing magnetic flux through a conductor induces voltage: EMF = -N × dΦ/dt. The minus sign (Lenz's Law) means the induced current opposes the change that caused it. This is how [[quick-context/electricity-generation|generators]] and [[quick-context/inductor|inductors]] work. |
| **Lorentz Force** | The force on a moving charge in electromagnetic fields: F = q(E + v × B). Electric fields push charges; magnetic fields deflect moving charges perpendicular to their velocity. This is how motors and CRT screens work. |
| **Electromagnetic Wave** | Self-propagating oscillations of electric and magnetic fields, traveling at the speed of light (c = 3×10⁸ m/s in vacuum). Radio, microwaves, infrared, visible light, UV, X-rays, and gamma rays are all electromagnetic waves at different frequencies. |

<details>
<summary><strong>How It Works</strong></summary>

## The Four Maxwell Equations (Conceptual)

All of electromagnetism reduces to four equations. You don't need the math to understand what each says:

```
MAXWELL'S EQUATIONS — WHAT THEY MEAN
══════════════════════════════════════════════════════════════════════════════

1. GAUSS'S LAW (Electric)
   ─────────────────────────────────────────────────────────────────────────
   "Electric field lines start on positive charges and end on negative charges"

        (+) ────→ ────→ ────→ ────→ (-)

   The total electric flux out of any closed surface equals the charge inside.
   This is why capacitors work: charges on plates create fields between them.


2. GAUSS'S LAW (Magnetic)
   ─────────────────────────────────────────────────────────────────────────
   "Magnetic field lines have no beginning or end—they always form closed loops"

              ┌──────────────────┐
              │                  │
              ▼                  │
        N ═══════════ S         │
              │                  │
              └──────────────────┘

   There are no magnetic monopoles (no isolated N or S poles).
   Every magnet has both poles; cut it in half and you get two magnets.


3. FARADAY'S LAW
   ─────────────────────────────────────────────────────────────────────────
   "A changing magnetic field creates an electric field"

         ┌─────────────────────────────────────┐
         │  Magnetic flux changing:            │
         │                                      │
         │     B (increasing)                  │
         │         ↓↓↓↓↓                        │
         │      ┌──────┐                        │
         │      │      │ ← induced EMF around   │
         │      │ coil │   the loop             │
         │      └──────┘                        │
         │         ↑                            │
         │     Induced electric field circles         │
         │     around the changing B           │
         └─────────────────────────────────────┘

   EMF = -N × dΦ/dt

   This is electromagnetic induction—the basis of:
   • Generators (motion → electricity)
   • Inductors (opposing current change)
   • Transformers (power transfer between coils)


4. AMPÈRE-MAXWELL LAW
   ─────────────────────────────────────────────────────────────────────────
   "Currents and changing electric fields create magnetic fields"

              Current I
                 │
                 │
                 ▼
        ───────⊗────────  Wire carrying current
                │
           ┌────┴────┐
           │         │
           │   B     │    Magnetic field circles
           │ circles │    around the current
           │         │
           └─────────┘

   • DC current creates steady magnetic field (electromagnets)
   • AC current creates oscillating magnetic field
   • Changing electric field also creates magnetic field (displacement current)
     → This is Maxwell's key addition that predicts electromagnetic waves


PUTTING IT TOGETHER: ELECTROMAGNETIC WAVES
══════════════════════════════════════════════════════════════════════════════

    Changing B creates E (Faraday)
         +
    Changing E creates B (Ampère-Maxwell)
         =
    SELF-SUSTAINING WAVE

              E field                    B field
              ↑                          ↑
       ┌──────┴──────┐            ┌──────┴──────┐
       │     ╱╲     │            │             │
       │    ╱  ╲    │            │   ╱╲   ╱╲   │
       │   ╱    ╲   │ ──────►    │  ╱  ╲ ╱  ╲  │ ──────►
       │  ╱      ╲  │            │ ╱    ╲    ╲ │     c
       │ ╱        ╲ │            │╱           ╲│
       └────────────┘            └─────────────┘

    E and B oscillate perpendicular to each other and to the
    direction of travel. Speed: c = 1/√(ε₀μ₀) = 3×10⁸ m/s

    Maxwell calculated this speed from electric and magnetic
    constants—and found it matched the known speed of light!
    Light is an electromagnetic wave.
```

## The Right-Hand Rules

```
RIGHT-HAND RULES — Predicting Magnetic Field Direction
══════════════════════════════════════════════════════════════════════════════

1. CURRENT → MAGNETIC FIELD (for a straight wire)
   ─────────────────────────────────────────────────────────────────────────

   Point thumb in direction of current (conventional, + to -)
   Fingers curl in direction of magnetic field

         Thumb → I (current direction)
           │
           │     ╭───╮
           │    ╱     ╲
           ▼   │   ⊗   │   ← magnetic field circles around wire
              ╲  │  ╱
               ╰─┴─╯

   Current into page (⊗): magnetic field circles clockwise
   Current out of page (⊙): magnetic field circles counter-clockwise


2. COIL → MAGNETIC FIELD (for a solenoid/inductor)
   ─────────────────────────────────────────────────────────────────────────

   Curl fingers in direction of current through coil
   Thumb points to N pole (direction of magnetic field inside)

         ──⊃⊃⊃⊃⊃⊃⊃⊃──
              ║
         ═════════════ → B (inside coil)
              ║
              N pole

   A coil with current is an electromagnet


3. FORCE ON A MOVING CHARGE (Lorentz force)
   ─────────────────────────────────────────────────────────────────────────

   F = q × v × B

   Point fingers in direction of velocity (v)
   Curl toward magnetic field (B)
   Thumb points to force direction (F) for positive charge
   (Reverse for negative charge)

   This is how:
   • Motors work (current in magnetic field → force → rotation)
   • CRT screens work (electron beam steered by magnets)
   • Particle accelerators steer charged particles
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Fields vs. Forces: The Two Ways to Think About Electromagnetism

**Force-based thinking:** Focus on what charges and currents do to each other. Good for motors, force calculations, simple circuits.

**Field-based thinking:** Focus on the fields that fill space, independent of what created them. Essential for understanding waves, radiation, antennas, and advanced applications.

```
TWO PERSPECTIVES ON THE SAME PHYSICS
══════════════════════════════════════════════════════════════════════════════

    FORCE VIEW                              FIELD VIEW
    ──────────────────────                  ──────────────────────
    "Charges push each other"               "Charges create fields,
                                             fields push charges"

         (+)──────────(-)                        (+)
            attractive                        ────→ E
             force                           ────→ E
                                             ────→ E
                                                 │
                                                 ▼
    Good for:                                (-)  ← feels force from field
    • Simple DC circuits
    • Static problems
    • Intuitive understanding               Good for:
                                            • Electromagnetic waves
                                            • Antennas and radiation
                                            • Time-varying phenomena
                                            • Understanding light

The field view becomes essential when you realize fields carry energy
and momentum themselves—they're not just a mathematical convenience.
Electromagnetic waves are oscillating fields traveling through space,
carrying energy from the sun to Earth across 150 million km of vacuum.
```

| Application | Primary Principle | Key Device |
|-------------|------------------|------------|
| Power generation | Faraday's law (changing B → E) | Generator, alternator |
| Electric motors | Lorentz force (I × B → F) | DC motor, AC motor |
| Transformers | Faraday's law (mutual induction) | Power transformer |
| [[quick-context/inductor|Inductors]] | Faraday's law (self-induction) | Chokes, filter coils |
| Wireless communication | EM wave propagation | Antennas, radio |
| Magnetic storage | Hysteresis in magnetic materials | Hard drives, tape |

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## How a Generator Creates Electricity

A generator converts mechanical rotation into electrical current using electromagnetic induction. This is how 99%+ of grid electricity is produced.

```
GENERATOR OPERATION — Step by Step
══════════════════════════════════════════════════════════════════════════════

    PHYSICAL STRUCTURE
    ─────────────────────────────────────────────────────────────────────────

          N ════════════════════════════════ S
                        ┌──────────┐
                        │          │
                        │   COIL   │ ← rotates on axis
                        │          │
                        └────┬─────┘
                             │
                          SHAFT ← connected to turbine
                             │
                        ┌────┴────┐
                        │ SLIP    │
                        │ RINGS   │ ← connect rotating coil to external circuit
                        └─────────┘
                             │
                             ▼
                        AC OUTPUT


    WHY ROTATION CREATES VOLTAGE (Faraday's Law)
    ─────────────────────────────────────────────────────────────────────────

    EMF = -N × dΦ/dt

    Φ = magnetic flux = B × A × cos(θ)
      where θ = angle between coil and field

    As coil rotates, θ changes continuously:

    Position 1: θ = 0°        Position 2: θ = 90°       Position 3: θ = 180°
    (coil faces field)        (coil edge-on)            (coil faces opposite)

         N ═════ S             N ═════ S                 N ═════ S
            ┌─┐                   │                         ┌─┐
            │ │                   │                         │ │
            └─┘                   │                         └─┘
                                  │
    Φ = maximum               Φ = zero                  Φ = -maximum
    dΦ/dt = 0                 dΦ/dt = maximum           dΦ/dt = 0
    EMF = 0                   EMF = maximum             EMF = 0


    THE RESULTING WAVEFORM
    ─────────────────────────────────────────────────────────────────────────

    EMF (voltage)
         ▲
         │        ╱╲              ╱╲
         │       ╱  ╲            ╱  ╲
     +V  │      ╱    ╲          ╱    ╲
         │     ╱      ╲        ╱      ╲
      0  │────╱────────╲──────╱────────╲──────► rotation angle
         │              ╲    ╱          ╲    ╱
     -V  │               ╲  ╱            ╲  ╱
         │                ╲╱              ╲╱
         │
         └── 0°    90°   180°   270°   360° ──►

    One full rotation = one AC cycle
    60 rotations/second = 60 Hz (US grid frequency)
    3000 RPM = 50 Hz (European grid frequency)


    LENZ'S LAW — Why Generators Require Work
    ─────────────────────────────────────────────────────────────────────────

    The minus sign in EMF = -N × dΦ/dt (Lenz's Law) means:
    "The induced current opposes the change that caused it"

    1. Turbine pushes coil, changing flux
    2. Induced current creates its own magnetic field
    3. That field opposes the rotation (magnetic braking)
    4. You must do WORK to overcome this opposition
    5. That work comes from steam pressure, falling water, or wind

    This is conservation of energy enforced by physics:
    You can't get electrical energy without putting in mechanical work.
```

**The one thing most outsiders get wrong about this is...** thinking generators "create" energy from magnets. They don't. The magnetic field is just a medium for transferring energy from mechanical motion to electrical current. When you spin the generator faster, you don't "get more energy from the magnet"—you're putting in more mechanical work, which becomes electrical energy. Lenz's Law guarantees this: the generator pushes back against you exactly as hard as the electrical load demands. A generator with nothing connected spins freely; connect a heavy load and it becomes hard to turn. The energy always comes from whatever is spinning the shaft.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/electric-current]]** — Current is moving charge, and moving charges create magnetic fields. Understanding current flow is prerequisite to understanding how electromagnets and inductors work.

- **[[quick-context/inductor]]** — An inductor stores energy in a magnetic field created by current through a coil. The inductor equation V = L×dI/dt is a direct application of Faraday's law: changing current changes the magnetic flux, which induces a voltage opposing the change.

- **[[quick-context/electricity-generation]]** — Electromagnetic induction is the dominant method for generating grid electricity. Generators, turbines, and the energy conversion chain all depend on Faraday's law.

- **[[quick-context/capacitor]]** — Capacitors store energy in electric fields; inductors store energy in magnetic fields. They are electromagnetic duals: I = C×dV/dt vs. V = L×dI/dt.

- **[[micro-context/electromagnetic-induction]]** — Glossary-style definition of electromagnetic induction with Faraday's law.

- **Maxwell's Equations** — The complete mathematical formulation of electromagnetism in four equations. All electromagnetic phenomena—from static charges to light—emerge from these equations.

- **Special Relativity** — Einstein showed that electric and magnetic fields are the same phenomenon viewed from different reference frames. A moving charge sees a magnetic field as an electric field, and vice versa. This is why magnetism is sometimes called "relativistic electricity."

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A compass needle deflects when you bring a wire carrying DC current near it. Why?
<details>
<summary>Answer</summary>
**Current creates a magnetic field that surrounds the wire.** According to Ampère's Law, any current (moving charges) creates a magnetic field that circles around the current. The compass needle (itself a small magnet) aligns with this field, deflecting from magnetic north. The right-hand rule predicts the direction: point thumb along current, fingers curl in the direction of the magnetic field.
</details>

**Q2:** Why does an [[quick-context/inductor|inductor]] oppose changes in current?
<details>
<summary>Answer</summary>
**Faraday's Law and Lenz's Law.** When current through an inductor changes, the magnetic field it creates also changes. By Faraday's Law, a changing magnetic field induces a voltage (V = L×dI/dt). By Lenz's Law, this induced voltage opposes the change that caused it—if current is increasing, the induced voltage pushes back against the increase; if decreasing, it tries to maintain the current. This is why inductors "resist" current changes.
</details>

**Q3:** A transformer has 100 turns on the primary coil and 1000 turns on the secondary. If you apply 12V AC to the primary, what voltage appears on the secondary?
<details>
<summary>Answer</summary>
**120V AC.** Transformer voltage ratio equals turns ratio: V₂/V₁ = N₂/N₁. So V₂ = 12V × (1000/100) = 120V. Note this only works with AC—the changing current in the primary creates a changing magnetic field, which induces voltage in the secondary. DC would create a constant field, meaning dΦ/dt = 0, meaning no induced voltage.
</details>

**Q4:** Why doesn't a transformer work with DC?
<details>
<summary>Answer</summary>
**No change in magnetic flux means no induced voltage.** Faraday's Law is EMF = -N×dΦ/dt. With DC, once current reaches steady state, dI/dt = 0, so the magnetic flux is constant, so dΦ/dt = 0, so EMF = 0. You'd only get a brief voltage pulse when DC is first applied (while current is rising). AC continuously alternates, so dΦ/dt is never zero, and voltage is continuously induced.
</details>

**Q5:** Light travels at 3×10⁸ m/s. Maxwell calculated this speed from measurements of electric and magnetic constants made in a laboratory. How did he know these were related?
<details>
<summary>Answer</summary>
**He derived it from his equations.** Maxwell's equations predict that changing electric fields create magnetic fields and vice versa, allowing self-sustaining waves that propagate at speed c = 1/√(ε₀μ₀), where ε₀ (permittivity) and μ₀ (permeability) are the electric and magnetic properties of free space. When he plugged in the measured values, he got c ≈ 3×10⁸ m/s—matching the known speed of light. This was the first clue that light is an electromagnetic wave, not a separate phenomenon.
</details>

</details>
