---
topic: Electric and Magnetic Field Unification
created: 2026-02-10
---

# Electric and Magnetic Field Unification

> **Related:** [[quick-context/electromagnetism]] | [[quick-context/electric-current]] | [[quick-context/capacitor]] | [[quick-context/inductor]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]

> **TL;DR:** Current, voltage, electric fields, and magnetic fields are four aspects of one underlying reality: charges push through voltage differences, creating current; stationary charges create electric fields, moving charges (current) create magnetic fields; and changes in either field create the other—this chain of causation is why electricity and magnetism are actually "electromagnetism."

## The Core Problem: Four Concepts That Seem Disconnected

Students learn voltage, current, electric fields, and magnetic fields as separate topics—often in different chapters or courses. This makes it hard to see that they're all faces of the same physics. The conceptual chain is: **charges → fields → forces → motion → more fields**. Understanding this chain turns a pile of memorized equations into a coherent mental model you can reason with.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Current (I)** | Moving charges. Measured in amps (A = coulombs/second). Current is the *flow* of charge—the thing actually doing work in circuits. |
| **Voltage (V)** | Energy per unit charge, measured in volts (V = joules/[[micro-context/coulomb-history|coulomb]]). Voltage is the "pressure" that pushes charges. It's a difference in electric potential between two points. |
| **Electric Field (E)** | The force per unit charge at each point in space, measured in V/m or N/C. Created by charges (stationary or moving). Points from + toward -. |
| **Magnetic Field (B)** | A force field created by moving charges (current) or changing electric fields, measured in tesla (T). Exerts forces on other moving charges, perpendicular to their velocity. |
| **Electromagnetic Field** | The unified reality: E and B are two aspects of one thing. A stationary observer sees a magnetic field; an observer moving with the charges sees an electric field. Maxwell unified them; Einstein explained why. |

<details>
<summary><strong>How It Works</strong></summary>

## The Conceptual Chain: Charges → Fields → Everything Else

```
THE COMPLETE PICTURE — How All Four Concepts Connect
══════════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   CHARGES (the source of everything)                                         │
│   ═══════════════════════════════════                                        │
│                                                                              │
│   Charges are the fundamental source. They can be:                           │
│   • Stationary → create ELECTRIC FIELD only                                 │
│   • Moving → create BOTH electric AND magnetic fields                        │
│                                                                              │
│           Stationary charge              Moving charge (current)             │
│                (+)                           (+) ═══►                        │
│              ↗ ↑ ↖                          ↗ ↑ ↖                            │
│            ← (+) →  electric field              ← (+) →  electric field                    │
│              ↙ ↓ ↘  radiates               ↙ ↓ ↘  still there                │
│                                              ⊙ ⊗                              │
│                                          magnetic field circles                     │
│                                          around motion                       │
│                                                                              │
│   This is the first key insight:                                             │
│   CURRENT = MOVING CHARGES = SOURCE OF MAGNETIC FIELD                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   FIELDS (how charges interact at a distance)                                │
│   ═══════════════════════════════════════════                                │
│                                                                              │
│   Fields fill space. They're not just math—they carry real energy.           │
│                                                                              │
│   ELECTRIC FIELD (E)                    MAGNETIC FIELD (B)                   │
│   ──────────────────                    ──────────────────                   │
│   Created by:                           Created by:                          │
│   • Charges (always)                    • Moving charges/current (always)    │
│   • Changing B field                    • Changing E field                   │
│                                                                              │
│   Acts on:                              Acts on:                             │
│   • Any charge (F = qE)                • Only MOVING charges (F = qv × B)   │
│                                                                              │
│   Direction of force:                   Direction of force:                  │
│   • Along the field line               • Perpendicular to motion AND field   │
│                                                                              │
│                                                                              │
│   This is why B doesn't do "work":                                           │
│   Force perpendicular to motion means F·v = 0, so no energy transfer.        │
│   B deflects charges but can't speed them up or slow them down.              │
│   Only E can add or remove energy from charges.                              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   VOLTAGE (connecting electric field to circuits)                                   │
│   ════════════════════════════════════════                                   │
│                                                                              │
│   Voltage IS the electric field, integrated along a path:                    │
│                                                                              │
│         V = ∫ E · dl     (voltage = integral of electric field along path)         │
│                                                                              │
│   In uniform field:  V = E × d    (voltage = field strength × distance)     │
│                                                                              │
│                                                                              │
│        electric field                        In a capacitor:                        │
│        ──────►                                                               │
│        ──────►                           (+) ───────────────                 │
│        ──────►                            │     electric field                      │
│        ──────►                            │  ═══════════════►  d = 1mm       │
│                                           │                                  │
│        d = 1m                            (-) ───────────────                 │
│        E = 5 V/m                          E = 5000 V/m                       │
│        V = 5V                             V = 5V                             │
│                                                                              │
│   Same 5V, but field strength is 1000× higher in the capacitor               │
│   because the distance is 1000× smaller. V = E × d                           │
│                                                                              │
│                                                                              │
│   KEY INSIGHT: Voltage is what you MEASURE in circuits.                      │
│   Electric field is what's PHYSICALLY HAPPENING in space.                    │
│   They're the same thing, just expressed differently.                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   CURRENT (connecting fields to charge motion)                               │
│   ════════════════════════════════════════════                               │
│                                                                              │
│   Current IS charges moving in response to electric field:                   │
│                                                                              │
│        electric field pushes charges → charges move → that's current               │
│                                                                              │
│        ────────────────────────────────────────────────────────              │
│              Wire (conductor)                                                │
│        ────────────────────────────────────────────────────────              │
│        ←───  electric field  ───→              →e⁻ →e⁻ →e⁻ →e⁻ →e⁻                 │
│                                          electrons flow                      │
│                                          (current direction                  │
│                                          is opposite by convention)          │
│                                                                              │
│   In Ohm's Law terms:                                                        │
│                                                                              │
│        I = V / R                                                             │
│          ↑   ↑   ↑                                                           │
│          │   │   └─ Resistance: how hard it is for charges to move           │
│          │   └───── Voltage: the electric field integrated, the "push"              │
│          └───────── Current: the actual charge flow that results             │
│                                                                              │
│   WHY DO MOVING CHARGES CREATE B-FIELD?                                      │
│   This is just a fact of nature (explained by special relativity).           │
│   The moment charges move, they create a magnetic field that circles         │
│   around their direction of motion.                                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## The Complete Causal Chain

```
THE CIRCULAR RELATIONSHIP — Why It's "Electromagnetism"
══════════════════════════════════════════════════════════════════════════════

This is the key to understanding—it's a LOOP:

                    ┌─────────────────────────────────────┐
                    │                                     │
                    ▼                                     │
            ┌───────────────┐                             │
            │   CHARGES     │                             │
            │   (exist)     │                             │
            └───────┬───────┘                             │
                    │ create                              │
                    ▼                                     │
            ┌───────────────┐                             │
            │ ELECTRIC FIELD│ ◄────────────────┐          │
            │     (E)       │                  │          │
            └───────┬───────┘                  │          │
                    │ pushes charges           │          │
                    ▼                          │          │
            ┌───────────────┐           ┌──────┴───────┐  │
            │   CURRENT     │           │   CHANGING   │  │
            │ (moving       │           │   B-FIELD    │  │
            │  charges)     │           │ creates E!   │  │
            └───────┬───────┘           └──────────────┘  │
                    │ creates                  ▲          │
                    ▼                          │          │
            ┌───────────────┐                  │          │
            │ MAGNETIC FIELD│ ─────────────────┘          │
            │     (B)       │                             │
            └───────┬───────┘                             │
                    │                                     │
                    │ if B changes, it creates E          │
                    │ which pushes charges                │
                    │ which creates more B...             │
                    │                                     │
                    └─────────────────────────────────────┘

This self-reinforcing loop is what makes electromagnetic waves possible:
• Changing E creates B
• Changing B creates E
• They bootstrap each other through empty space at the speed of light


IN CIRCUITS (the practical version):
══════════════════════════════════════════════════════════════════════════════

    BATTERY/SUPPLY                           LOAD
    ┌──────────┐                          ┌──────┐
    │          │    I →                   │      │
    │  Creates │──────────────────────────│ Uses │
    │  Voltage │                          │Energy│
    │  (electric field│──────────────────────────│      │
    │  source) │    ← I                   │      │
    └──────────┘                          └──────┘
         │                                    │
         │                                    │
         ▼                                    ▼
    electric field in wire                      electric field does work
    pushes electrons                     on charges passing through

    The VOLTAGE across the load tells you how much electric field energy
    each coulomb of charge delivers to the load.

    V = energy per charge (joules per coulomb)
    I = charge flow rate (coulombs per second)
    P = V × I = energy per second = power (watts)
```

## Where Each Component Stores Energy

```
ENERGY STORAGE — The Link Between Fields and Components
══════════════════════════════════════════════════════════════════════════════

    CAPACITOR                              INDUCTOR
    ════════                               ════════

    Stores energy in                       Stores energy in
    ELECTRIC FIELD                         MAGNETIC FIELD

    ┌─────────────────┐                    ┌──────────────┐
    │ + + + + + + + + │                    │  ⊃⊃⊃⊃⊃⊃⊃⊃   │
    │═════════════════│ ← electric field          │  ══════════  │ ← magnetic field inside
    │ - - - - - - - - │                    │  ⊃⊃⊃⊃⊃⊃⊃⊃   │
    └─────────────────┘                    └──────────────┘

    E = ½CV²                               E = ½LI²

    Energy ∝ V²                            Energy ∝ I²
    (voltage-based storage)                (current-based storage)

    Opposes voltage changes                Opposes current changes
    (can't change E instantly)             (can't change B instantly)


    RESISTOR
    ════════

    Doesn't store energy—                  P = I²R = V²/R
    DISSIPATES it as heat

    ┌───╱╱╱╱───┐
    │    R     │ → heat
    └──────────┘

    electric field inside resistor does work on charges,
    but that energy goes to heating atoms (random motion),
    not to organized motion (current).


WHY CAPACITORS AND INDUCTORS ARE "DUALS"
══════════════════════════════════════════════════════════════════════════════

    They're electromagnetic mirrors of each other:

                        CAPACITOR              INDUCTOR
    ─────────────────────────────────────────────────────────────────────
    Stores energy in     Electric field         Magnetic field
    Energy formula       E = ½CV²               E = ½LI²
    Controlled by        Voltage                Current
    Opposes changes in   Voltage                Current
    Key equation         I = C × dV/dt          V = L × dI/dt
    Blocks               DC (no current)        AC (opposes changes)
    Passes               AC (charges/discharges) DC (steady current OK)
    Series combination   1/C = 1/C₁ + 1/C₂     L = L₁ + L₂
    Parallel combo       C = C₁ + C₂           1/L = 1/L₁ + 1/L₂

    This symmetry exists because E and B fields are symmetric partners
    in Maxwell's equations. Capacitors and inductors are just the
    practical manifestations of electric field and magnetic field energy storage.
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Two Valid Worldviews: Charges vs. Fields

Physicists argued about this for decades. Both views are correct—they're complementary.

```
THE TWO WAYS TO THINK ABOUT ELECTRICITY
══════════════════════════════════════════════════════════════════════════════

VIEW 1: CHARGES ARE FUNDAMENTAL, FIELDS ARE BOOKKEEPING
──────────────────────────────────────────────────────────────────────────────

    "Charges push and pull on each other. Fields are just a convenient
     way to calculate those forces without tracking every charge."

    (+) ────────────────────────────────── (-)
                force between them

    This view works great for:
    • DC circuits
    • Static electricity
    • Simple force calculations
    • Building intuition


VIEW 2: FIELDS ARE FUNDAMENTAL, CHARGES ARE SOURCES
──────────────────────────────────────────────────────────────────────────────

    "Fields fill all of space and carry energy and momentum. Charges
     are just where field lines begin and end."

    (+)                                    (-)
     │                                      │
     └──────→ ──────→ ──────→ ──────→ ─────┘
              electric field exists everywhere

    This view is REQUIRED for:
    • Electromagnetic waves (light, radio)
    • Understanding radiation
    • Antennas and wireless
    • Special relativity


WHICH IS "TRUE"?
──────────────────────────────────────────────────────────────────────────────

    Both! They're different descriptions of the same reality.

    For everyday circuits, "charges push each other" is simpler.
    For advanced physics, "fields carry energy through space" is essential.

    The fact that light (an electromagnetic wave) travels from the sun
    to Earth across 150 million km of vacuum proves that fields are
    real things—they carry energy even where there are no charges.
```

| Situation | Better Mental Model |
|-----------|-------------------|
| DC circuit analysis | Charges flow, voltage pushes |
| AC circuit analysis | Charges flow, but consider reactance |
| Capacitor charging | electric field building between plates |
| Inductor charging | magnetic field building in coil |
| Transformer operation | Changing B creates E in secondary |
| Radio transmission | E and B waves propagating through space |
| Lightning | Charges discharge, massive current, huge magnetic field |

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Tracing the Physics Through a Simple Circuit

Let's follow exactly what happens when you connect a battery to a light bulb:

```
WHAT'S ACTUALLY HAPPENING — Physics Step by Step
══════════════════════════════════════════════════════════════════════════════

    SETUP:
    ────────────────────────────────────────────────────────────────────────

         Battery                Wire              Light Bulb
        ┌──────┐           ───────────           ┌──────┐
        │ (+)  │──────────────────────────────────│      │
        │      │                                  │ 💡   │
        │ (-)  │──────────────────────────────────│      │
        └──────┘           ───────────           └──────┘


    STEP 1: Battery creates electric field
    ────────────────────────────────────────────────────────────────────────

    Chemical reactions in the battery separate charges:
    • (+) terminal has deficit of electrons
    • (-) terminal has excess of electrons

    This charge separation creates an E-FIELD in the wire:

        ┌──────┐
        │ (+)  │←───── electric field points from + to -
        │      │       throughout the entire circuit
        │ (-)  │
        └──────┘

    The electric field exists INSTANTLY (at speed of light) along the whole wire,
    even before any electrons have moved!


    STEP 2: electric field pushes electrons (creating current)
    ────────────────────────────────────────────────────────────────────────

    Free electrons in the wire feel force F = qE:

        Wire interior:
        ─────────────────────────────────────────────────────────
                ←E       ←E       ←E       ←E       ←E
                         ↓        ↓        ↓
                       →e⁻     →e⁻     →e⁻     →e⁻
        ─────────────────────────────────────────────────────────

    electric field points + to - (left)
    Electrons feel force OPPOSITE to E (they're negative!)
    So electrons drift from - to + (right in the wire)

    Conventional current I flows opposite to electron motion (historical accident)


    STEP 3: Current creates magnetic field
    ────────────────────────────────────────────────────────────────────────

    Moving charges create a magnetic field that circles around the current:

        Wire cross-section:
                    ↑ B
               ┌────┼────┐
           B ← │    ⊗    │ → B        (current into page)
               └────┼────┘
                    ↓ B

    If you held a compass near the wire, it would deflect!
    This was Oersted's discovery in 1820.


    STEP 4: Energy transfer in the bulb
    ────────────────────────────────────────────────────────────────────────

    Inside the filament (high resistance):

        ─────╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱─────
              ←E       →e⁻         (electric field still present)
                       →e⁻
                       →e⁻

    The electric field does WORK on each electron as it passes through.
    W = F × d = qE × d = qV  (that's where V = voltage comes from!)

    Where does that energy go?
    • Electrons crash into tungsten atoms
    • Atoms vibrate more → temperature rises
    • At 2500°C, filament glows white → LIGHT

    Power dissipated: P = V × I = I²R = V²/R


    STEP 5: Completing the circuit
    ────────────────────────────────────────────────────────────────────────

    Electrons that gave up energy in the bulb return to the battery
    The battery's chemical reaction re-energizes them (adds potential)
    The cycle repeats continuously as long as the circuit is closed


SUMMARY: The Four Quantities in Action
══════════════════════════════════════════════════════════════════════════════

    VOLTAGE (9V)
    • Created by chemical separation of charges in battery
    • Represents 9 joules of potential energy per coulomb of charge
    • Measured BETWEEN two points (+ and - terminals)

    ELECTRIC FIELD
    • Fills the wire, pointing from + to -
    • Strength varies: strong in filament (high E over short distance)
    • E = V/d in each section

    CURRENT (say, 0.5A)
    • 0.5 coulombs of charge flowing per second
    • Same everywhere in a series circuit (charge is conserved)
    • Actual electrons drift slowly (~mm/s) but the effect is instant

    MAGNETIC FIELD
    • Circles around every current-carrying section
    • Stronger where current is concentrated
    • Does no direct work but can exert forces on other currents/magnets

    POWER
    • P = V × I = 9V × 0.5A = 4.5W
    • 4.5 joules per second converted from chemical → electrical → light + heat
```

**The one thing most outsiders get wrong about this is...** thinking voltage "flows" or gets "used up." Voltage is a *difference*—like altitude. When you hike from 5000 ft to 4000 ft elevation, you don't "use up" altitude; you convert gravitational potential energy to kinetic energy (and heat in your muscles). Similarly, electrons "fall" through voltage, converting electrical potential energy to other forms. The voltage across the battery stays 9V whether the bulb is connected or not. What changes when you connect the bulb is that *current* starts flowing, allowing that potential energy to be converted to light and heat.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/electromagnetism]]** — The detailed physics of how electric and magnetic fields interact, including Maxwell's equations and electromagnetic waves. Read this for the mathematical relationships.

- **[[quick-context/electric-current]]** — Deep dive into current: what it is, how it's measured, the relationship to charge, and practical applications in [[quick-context/electrolysis|electrolysis]] and circuits.

- **[[quick-context/capacitor]]** — How electric fields store energy between conductive plates. Understanding capacitors is understanding electric field energy storage in a practical package.

- **[[quick-context/inductor]]** — How magnetic fields store energy in coils. Understanding inductors is understanding magnetic field energy storage in a practical package.

- **[[quick-context/resistor]]** — Where electrical energy becomes heat. The resistor shows what happens when current flows but the energy isn't stored—it's dissipated.

- **[[quick-context/power-watts-joules]]** — The rate of energy transfer: P = VI. This connects the abstract concepts (voltage, current, fields) to practical concerns (heat, battery life, electrical cost).

- **[[quick-context/voltage]]** — Electric field defines voltage; field strength drives current through materials.

- **[[quick-context/coil-magnetic-field]]** — The practical application of the principle that moving charges create magnetic fields. Explains solenoid field calculations and why coiling concentrates the field.

- **Special Relativity** — Einstein showed that E and B fields are the *same thing* seen from different reference frames. What looks like a magnetic field to a stationary observer looks like an electric field to a moving observer. This is why "electromagnetism" is one word.

- **[[quick-context/faraday-tensor]]** — The mathematical object that makes E/B unification precise: a 4×4 antisymmetric [[quick-context/tensor|tensor]] containing all six field components. Under Lorentz transformations, the tensor components mix E and B together automatically, showing they're aspects of one unified electromagnetic field.

- **[[quick-context/maxwell-equations]]** — The four equations that govern all electromagnetic phenomena. They encode the relationships between charges, currents, and the E and B fields discussed here, and predict that changing E creates B and vice versa.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A wire carries steady DC current. Is there an electric field in the wire? A magnetic field? Both?
<details>
<summary>Answer</summary>
**Both.** There must be an electric field inside the wire—that's what pushes the electrons and creates current (F = qE). Ohm's law in microscopic form is J = σE (current density = conductivity × electric field). The current also creates a magnetic field that circles around the wire. For steady DC, these fields are constant in time.
</details>

**Q2:** Why can a magnetic field deflect an electron but can't change its speed?
<details>
<summary>Answer</summary>
**The Lorentz force from a magnetic field is always perpendicular to velocity.** F = qv × B means the force direction is perpendicular to both v and B. Since F is perpendicular to v, the force does no work: W = F·d, but F ⊥ d (displacement is along velocity), so W = 0. No work means no change in kinetic energy, so speed stays constant. The electron curves but doesn't speed up or slow down. Only electric fields can add or remove energy from charges.
</details>

**Q3:** You measure 5V across a resistor and 5V across a capacitor in the same circuit. Are the electric fields inside them the same strength?
<details>
<summary>Answer</summary>
**Almost certainly not.** Voltage is the integral of electric field over distance: V = E × d (for uniform field). If the resistor is 1 cm long and the capacitor gap is 0.1 mm, then E_resistor = 5V/0.01m = 500 V/m, while E_capacitor = 5V/0.0001m = 50,000 V/m—100× stronger! Same voltage, vastly different field strength, because of different dimensions.
</details>

**Q4:** In a transformer, no current flows between primary and secondary coils (they're electrically isolated). How does energy transfer between them?
<details>
<summary>Answer</summary>
**Through the magnetic field.** Current in the primary creates a magnetic field in the core. When that current changes (AC), the magnetic field changes. By Faraday's law, changing B creates E. That induced electric field exists in the secondary coil and pushes electrons, creating current. Energy flows: electrical (primary) → magnetic (core) → electrical (secondary). The magnetic field is the intermediary that carries energy across the galvanic isolation.
</details>

**Q5:** If electric and magnetic fields are "really the same thing" (as relativity says), why do circuits have separate capacitors (electric field storage) and inductors (magnetic field storage)?
<details>
<summary>Answer</summary>
**They're the same thing at rest in different reference frames, but in our frame (stationary relative to the circuit) they behave differently.** electric fields exert forces on stationary and moving charges alike; magnetic fields only act on moving charges. electric fields can do work; magnetic fields cannot. electric field energy density ∝ E²; magnetic field energy density ∝ B². In practice: to store energy using voltage (charge separation), you use a capacitor. To store energy using current (moving charges), you use an inductor. They're complementary tools for different jobs, even though at the deepest level they're aspects of one unified field.
</details>

</details>
