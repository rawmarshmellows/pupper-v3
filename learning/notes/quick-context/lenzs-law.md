---
topic: Lenz's Law
created: 2026-02-17
---

# Lenz's Law

> **Related:** [[learning/notes/quick-context/coil-magnetic-field]] | [[learning/notes/quick-context/electric-magnetic-field-unification]] | [[learning/notes/micro-context/electromagnetic-induction]] | [[learning/notes/quick-context/electromagnetism]] | [[learning/notes/quick-context/faraday-tensor]]

> **TL;DR:** Lenz's Law is the minus sign in Faraday's Law (EMF = -N × dΦ/dt) — it states that any induced [[learning/notes/quick-context/electric-current|current]] creates a magnetic field that opposes the change in flux that caused it. This isn't arbitrary; it's conservation of energy enforced at the electromagnetic level. Without this opposition, you could extract infinite energy from nothing.

## The Core Problem: Why the Minus Sign?

Faraday discovered that changing magnetic flux through a coil induces [[learning/notes/quick-context/voltage|voltage]]. But in which direction? If the induced current reinforced the flux change, it would create a positive feedback loop: more flux → more current → even more flux → infinite energy from nothing. This would violate the first law of thermodynamics. Lenz's Law prevents this: the induced EMF always creates effects that oppose the change. Push a magnet toward a coil, and the coil becomes a magnet that pushes back. Try to stop current through an [[learning/notes/quick-context/inductor|inductor]], and it generates voltage that tries to keep current flowing. Nature resists change, and Lenz's Law is how [[learning/notes/quick-context/electromagnetism|electromagnetism]] enforces that resistance.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Lenz's Law** | The direction of induced EMF opposes the change in magnetic flux that produced it. Named after Heinrich Lenz (1834). The minus sign in EMF = -N × dΦ/dt. |
| **Magnetic Flux (Φ)** | The "amount" of magnetic field passing through a surface: Φ = B × A × cos(θ). Measured in webers (Wb). Changes in flux induce EMF. |
| **Faraday's Law** | EMF = -N × dΦ/dt. The magnitude of induced voltage equals the rate of flux change times the number of turns. Lenz's Law determines the sign. |
| **Back-EMF** | The voltage an [[learning/notes/quick-context/inductor|inductor]] generates to oppose current changes. When you try to increase current, back-EMF pushes against you. When current decreases, back-EMF tries to maintain it. |
| **Magnetic Braking** | The slowing force on conductors moving through magnetic fields. Induced currents create opposing magnetic fields that resist motion. Used in roller coasters, trains, and gym equipment. |

<details>
<summary><strong>How It Works</strong> — The physics of opposition</summary>

## Why Opposition is Inevitable: Energy Conservation

The deep reason for Lenz's Law is conservation of energy. Consider what would happen without opposition:

```
WHY THE INDUCED CURRENT MUST OPPOSE THE CHANGE
══════════════════════════════════════════════════════════════════════════════

SCENARIO: You push a magnet toward a coil

         ┌──────────────────────────────────────────────────────────────────┐
         │  MAGNET         COIL                                             │
         │                                                                  │
         │     N ═══ S  ──▶   ⊃⊃⊃⊃⊃⊃⊃⊃⊃                                   │
         │                        │                                         │
         │   (moving right)       │                                         │
         │                        ▼                                         │
         │                   WHAT HAPPENS?                                  │
         └──────────────────────────────────────────────────────────────────┘

HYPOTHESIS A: Induced current REINFORCES the field (wrong!)
──────────────────────────────────────────────────────────────────────────────

    1. Magnet approaches → flux through coil increases
    2. Induced current creates field that ADDS to magnet's field
    3. This increases flux even more
    4. More flux change → more induced current → even stronger field
    5. Positive feedback → infinite energy from nothing!

    ✗ VIOLATES CONSERVATION OF ENERGY


HYPOTHESIS B: Induced current OPPOSES the field (Lenz's Law — correct!)
──────────────────────────────────────────────────────────────────────────────

    1. Magnet approaches → flux through coil increases
    2. Induced current creates field that OPPOSES the increase
    3. The coil acts like a magnet with N pole facing the incoming N pole
    4. This creates a REPULSIVE FORCE on the magnet
    5. You must do WORK to push the magnet against this force
    6. That work is converted to electrical energy in the coil

    ✓ ENERGY IS CONSERVED: Mechanical work in → Electrical energy out


              YOU                MAGNETIC
              DO                 BRAKING          ELECTRICAL
              WORK    ────────▶  FORCE    ────▶   ENERGY
                │                  │                 │
                │  Push magnet     │   Opposes       │  Powers
                │  against         │   motion        │  circuit
                │  resistance      │                 │
                └──────────────────┴─────────────────┘

    Conservation of energy: Work you do = Energy delivered to circuit
```

## What Is Magnetic Flux? (And What Does "Decreasing" Mean?)

Before understanding Lenz's Law, you need to understand what flux actually is:

```
MAGNETIC FLUX: How Much Field Passes Through a Surface
══════════════════════════════════════════════════════════════════════════════

    Flux (Φ) = B × A × cos(θ)

    Where:
    • B = magnetic field strength (how strong the field is)
    • A = area of the loop/coil
    • θ = angle between field and the surface normal

    Think of it like water flow through a hoop:

        STRONG FLUX                    WEAK FLUX                 ZERO FLUX
        (lots of field               (less field               (field parallel
         through loop)                through loop)             to loop)

         ║║║║║║║║║║                    ║  ║  ║                   ══════════
         ║║║║║║║║║║                    ║  ║  ║                   ══════════
        ┌──────────┐                 ┌──────────┐               ┌──────────┐
        │          │                 │          │               │          │
        │   LOOP   │                 │   LOOP   │               │   LOOP   │
        │          │                 │          │               │          │
        └──────────┘                 └──────────┘               └──────────┘
         ║║║║║║║║║║                    ║  ║  ║
         ▼▼▼▼▼▼▼▼▼▼                    ▼  ▼  ▼

        Many field lines              Fewer field               No field lines
        pass through                  lines through             pass through


WHAT DOES "FLUX CHANGING" MEAN?
──────────────────────────────────────────────────────────────────────────────

    INCREASING FLUX: More field lines passing through the loop over time

        Time 1              Time 2              Time 3
        ║  ║                ║║║║║║              ║║║║║║║║║║
        ║  ║                ║║║║║║              ║║║║║║║║║║
       ┌────┐              ┌────┐              ┌────┐
       │    │      →       │    │      →       │    │
       └────┘              └────┘              └────┘
        ▼  ▼                ▼▼▼▼▼▼              ▼▼▼▼▼▼▼▼▼▼

        Φ = small          Φ = medium          Φ = large
                  dΦ/dt > 0 (positive, increasing)

        This happens when:
        • A magnet approaches the coil
        • Current in a nearby coil increases
        • In an inductor: current is increasing (field building up)


    DECREASING FLUX: Fewer field lines passing through the loop over time

        Time 1              Time 2              Time 3
        ║║║║║║║║║║          ║║║║║║              ║  ║
        ║║║║║║║║║║          ║║║║║║              ║  ║
       ┌────┐              ┌────┐              ┌────┐
       │    │      →       │    │      →       │    │
       └────┘              └────┘              └────┘
        ▼▼▼▼▼▼▼▼▼▼          ▼▼▼▼▼▼              ▼  ▼

        Φ = large          Φ = medium          Φ = small
                  dΦ/dt < 0 (negative, decreasing)

        This happens when:
        • A magnet moves away from the coil
        • Current in a nearby coil decreases
        • In an inductor: current is decreasing (field collapsing)
```

## Why Does the Induced EMF Oppose the Change?

This is the heart of Lenz's Law. The induced current creates a magnetic field that **fights against whatever is happening to the flux**.

```
THE LOGIC OF OPPOSITION
══════════════════════════════════════════════════════════════════════════════

CASE 1: FLUX IS INCREASING
──────────────────────────────────────────────────────────────────────────────

    Situation: External field through coil is getting stronger

        External field (increasing)
              ║║║║║║
              ║║║║║║
              ▼▼▼▼▼▼
            ┌────────┐
            │  COIL  │ ←── What does the coil do?
            └────────┘

    What the induced current does:

        External field         Induced field
        (increasing ↓)         (opposing ↑)
              ║║║║║║                ▲▲▲▲
              ║║║║║║                ││││
              ▼▼▼▼▼▼                ││││
            ┌────────┐
            │ ←──────│←── Current flows THIS direction
            └────────┘    (creates field pointing UP)

    WHY? The induced current creates a field that points OPPOSITE to the
    external field. This REDUCES the net flux increase.

    • External field adds flux (pointing down)
    • Induced field subtracts flux (pointing up)
    • Net effect: flux still increases, but slower than it would otherwise

    If the induced field HELPED the increase, you'd get:
    More flux → more induced current → even more flux → runaway!
    This would violate energy conservation (free energy from nothing).


CASE 2: FLUX IS DECREASING
──────────────────────────────────────────────────────────────────────────────

    Situation: External field through coil is getting weaker

        External field (decreasing)
              ║    ║
              ║    ║
              ▼    ▼
            ┌────────┐
            │  COIL  │ ←── What does the coil do?
            └────────┘

    What the induced current does:

        External field         Induced field
        (decreasing ↓)         (supporting ↓)
              ║    ║               ║║║║
              ║    ║               ║║║║
              ▼    ▼               ▼▼▼▼
            ┌────────┐
            │ ──────→│←── Current flows THIS direction (opposite to Case 1!)
            └────────┘    (creates field pointing DOWN)

    WHY? The induced current creates a field that points the SAME direction
    as the external field. This REDUCES the net flux decrease.

    • External field is weakening (less flux pointing down)
    • Induced field adds flux (also pointing down)
    • Net effect: flux still decreases, but slower than it would otherwise

    The coil is trying to MAINTAIN the flux it had.
    It can't stop the decrease, but it fights against it.


THE PATTERN: ALWAYS OPPOSE THE CHANGE
──────────────────────────────────────────────────────────────────────────────

    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │   FLUX INCREASING?                                                    │
    │   → Induced field points OPPOSITE to external field                   │
    │   → Tries to REDUCE the increase                                      │
    │   → "Stop adding more!"                                               │
    │                                                                        │
    │   FLUX DECREASING?                                                    │
    │   → Induced field points SAME direction as external field             │
    │   → Tries to REDUCE the decrease                                      │
    │   → "Don't take it away!"                                             │
    │                                                                        │
    │   In BOTH cases: the induced effect opposes the CHANGE.              │
    │   Not the field itself—the CHANGE in the field.                       │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘


WHY MUST IT OPPOSE? (Energy Conservation)
──────────────────────────────────────────────────────────────────────────────

    The opposition isn't arbitrary—it's required by conservation of energy.

    THOUGHT EXPERIMENT: What if induced current HELPED the change?

    Flux increasing scenario (with wrong physics):
    1. Flux increases slightly
    2. This induces current
    3. Induced current creates field that ADDS to external field
    4. More flux → more induced current → more field → even more flux
    5. Positive feedback → infinite energy from nothing!

    Flux decreasing scenario (with wrong physics):
    1. Flux decreases slightly
    2. This induces current
    3. Induced current creates field that SUBTRACTS from remaining field
    4. Less flux → different induced current → less field → even less flux
    5. Field collapses instantly, releasing energy infinitely fast!

    BOTH scenarios violate conservation of energy.

    By OPPOSING the change:
    • Energy must be PUT IN to increase flux (work against opposition)
    • Energy is RELEASED when flux decreases (opposition slows release)
    • Energy is always conserved, transferred at finite rates
```

## The Magnetic Field Direction

When flux through a coil changes, the induced current creates its own magnetic field. Lenz's Law determines this field's direction:

```
LENZ'S LAW IN ACTION — Two Scenarios
══════════════════════════════════════════════════════════════════════════════

SCENARIO 1: FLUX INCREASING (magnet approaching)
──────────────────────────────────────────────────────────────────────────────

         External field           Induced field
         (from magnet)            (from coil current)
              │                        │
              ▼                        ▼

         N ═══ S  ────▶        S ═══ N
         magnet      │         │
         approaching │         └── Coil becomes a magnet
                     │             with N pole facing OUT
                     │             (repels incoming magnet)
                     │
                     └── Flux increasing (more field lines through coil)

    Induced current flows in direction that creates OPPOSING field
    (Right-hand rule: curl fingers with current, thumb points to N pole)

    Result: Coil pushes back against magnet. You must do work to approach.


SCENARIO 2: FLUX DECREASING (magnet withdrawing)
──────────────────────────────────────────────────────────────────────────────

         External field           Induced field
         (from magnet)            (from coil current)
              │                        │
              ▼                        ▼

         ◀──── N ═══ S           N ═══ S
               magnet            │
               withdrawing       └── Coil becomes a magnet
                     │               with S pole facing OUT
                     │               (attracts departing magnet)
                     │
                     └── Flux decreasing (fewer field lines through coil)

    Induced current now flows OPPOSITE direction
    Creates field that tries to MAINTAIN the flux

    Result: Coil pulls magnet back. You must do work to withdraw.


THE UNIVERSAL PATTERN:
══════════════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   FLUX INCREASING  →  Induced field OPPOSES external field         │
    │                        (tries to reduce the increase)              │
    │                                                                     │
    │   FLUX DECREASING  →  Induced field SUPPORTS external field        │
    │                        (tries to reduce the decrease)              │
    │                                                                     │
    │   In both cases: the induced effect OPPOSES THE CHANGE             │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
```

## Application to Inductors

An [[learning/notes/quick-context/inductor|inductor]] applies Lenz's Law to itself. When [[learning/notes/quick-context/electric-current|current]] changes, the flux through its own coils changes:

```
SELF-INDUCTION: Lenz's Law in Inductors
══════════════════════════════════════════════════════════════════════════════

    Current through inductor creates magnetic flux:  Φ = L × I
    Changing current means changing flux:            dΦ/dt = L × dI/dt
    Changing flux induces voltage:                   V = -L × dI/dt

    The minus sign IS Lenz's Law!


CURRENT INCREASING (dI/dt > 0):
──────────────────────────────────────────────────────────────────────────────

    ┌───┐                     ╭────────╮
    │ + ├───────────────────⊃⊃⊃⊃⊃⊃⊃⊃⊃├────┐
    │   │     I (increasing)  ╰────────╯    │
    │   │     ═══════▶        ║══════════   │
    │ − ├─────════════════════╨═════════════┘
    └───┘                     B (increasing)

    • Current rising → magnetic field building
    • Increasing flux induces EMF that OPPOSES the increase
    • V_L = -L × dI/dt is NEGATIVE (opposes positive dI/dt)
    • The inductor "pushes back" against the current rise
    • Energy is stored in the magnetic field: E = ½LI²


CURRENT DECREASING (dI/dt < 0):
──────────────────────────────────────────────────────────────────────────────

    ┌───┐                     ╭────────╮
    │   ├───────────────────⊃⊃⊃⊃⊃⊃⊃⊃⊃├────┐
    │   │     I (decreasing)  ╰────────╯    │
    │   │     ═════▶          ║══════════   │
    │   ├─────════════════════╨═════════════┘
    └───┘                     B (decreasing)

    • Current falling → magnetic field collapsing
    • Decreasing flux induces EMF that OPPOSES the decrease
    • V_L = -L × dI/dt is POSITIVE (opposes negative dI/dt)
    • The inductor tries to MAINTAIN the current
    • Stored energy releases back into the circuit


SUDDEN DISCONNECT: Lenz's Law Creates Voltage Spikes
──────────────────────────────────────────────────────────────────────────────

    If you try to instantly stop current (dI/dt → -∞):

    V_L = -L × dI/dt → +∞

    The inductor will generate whatever voltage is needed to keep
    current flowing! This can be hundreds or thousands of volts,
    enough to arc across switch contacts or destroy transistors.

    This is Lenz's Law taken to the extreme: the inductor REFUSES
    to allow its current to change instantly.

    Solution: Flyback diode provides a safe path for the current.


WHY VOLTAGE "SHIFTS" FROM INDUCTOR TO LOAD OVER TIME
──────────────────────────────────────────────────────────────────────────────

A common confusion: when you connect a battery to a coil with a load, the load
initially sees 0V, but eventually sees the full source voltage. Lenz's Law
explains exactly why this happens.

    CIRCUIT: Battery (Vs) → Inductor (L) → Load (R)

         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │           L                 R       │
      Vs │                                     │
         └─────────────────────────────────────┘

    Kirchhoff's Law always applies: Vs = V_L + V_R


THE KEY INSIGHT: Opposition is proportional to RATE OF CHANGE
──────────────────────────────────────────────────────────────────────────────

    V_L = L × dI/dt    (voltage across inductor = inductance × current change rate)

    AT t=0 (moment of connection):
    ─────────────────────────────
    • Current is zero, but WANTS to become non-zero
    • This "want" means dI/dt is LARGE (current trying to change fast)
    • Large dI/dt → Large V_L (Lenz's Law opposition!)
    • Since V_R = I×R and I=0 → V_R = 0
    • Result: V_L = Vs (all voltage absorbed by opposition)

                  ↓ All opposition here
         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │         Vs                 0        │
         └─────────────────────────────────────┘


    AS TIME PASSES:
    ─────────────────────────────
    • Current builds up (Lenz's Law loses the battle gradually)
    • As I increases, it's closer to its final value
    • Being closer means dI/dt decreases (less "urgency" to change)
    • Smaller dI/dt → Smaller V_L (less opposition needed!)
    • V_R = I×R grows as I grows
    • Result: voltage transfers from L to R

                  ↓ Less opposition         ↓ More here
         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │         ½Vs               ½Vs       │
         └─────────────────────────────────────┘


    AT t=∞ (steady state):
    ─────────────────────────────
    • Current has reached its limit: I = Vs/R
    • Current is CONSTANT (no longer changing)
    • dI/dt = 0 → V_L = L × 0 = 0
    • Nothing to oppose → no opposition voltage
    • Result: V_L = 0, V_R = Vs (all voltage at load)

                  ↓ No opposition           ↓ All here now
         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │          0                 Vs       │
         └─────────────────────────────────────┘


    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │  Lenz's Law opposes CHANGE, not steady state.                         │
    │                                                                        │
    │  • While current is changing: opposition (V_L > 0)                    │
    │  • When current is stable: no opposition (V_L = 0)                    │
    │                                                                        │
    │  The "voltage transfer" from inductor to load is just the             │
    │  opposition fading as there's less and less change to oppose.         │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘

    See RL Time Constant for the
    mathematics: the time constant τ = L/R determines how fast this happens.
```

</details>

<details>
<summary><strong>The Key Tension</strong> — Opposition vs. useful work</summary>

## Lenz's Law Is Both a Limitation and the Mechanism for Energy Transfer

The opposition described by Lenz's Law might seem like a nuisance — it's why generators require mechanical force to turn, and why inductors resist current changes. But this opposition is exactly what allows energy conversion:

```
LENZ'S LAW: LIMITATION AND ENABLER
══════════════════════════════════════════════════════════════════════════════

THE APPARENT LIMITATION:
────────────────────────────────────────────────────────────────────────────

    • Generators: Spinning the coil induces current, but that current
      creates magnetic braking that resists rotation. You must supply
      mechanical force to overcome it.

    • Inductors: Trying to increase current is opposed by back-EMF.
      Current can only rise at rate dI/dt = V/L, not instantly.

    • Transformers: The secondary current creates fields that oppose
      the primary's field changes, loading the primary circuit.


THE HIDDEN ENABLER:
────────────────────────────────────────────────────────────────────────────

    Without Lenz's Law, NO energy could transfer!

    GENERATOR without opposition:
    • Coil spins freely (no magnetic braking)
    • Induced current creates field that... helps rotation?
    • Free energy from nothing → impossible

    GENERATOR with opposition:
    • Magnetic braking requires work to overcome
    • That work = electrical energy delivered to circuit
    • Energy is conserved: mechanical in → electrical out


    INDUCTOR without opposition:
    • Apply voltage → current jumps instantly to any value
    • No energy stored in magnetic field
    • Infinite power transfer in zero time → impossible

    INDUCTOR with opposition:
    • Back-EMF limits dI/dt
    • Energy gradually stored in field: E = ½LI²
    • Power = V × I is finite and manageable


THE DEEP INSIGHT:
────────────────────────────────────────────────────────────────────────────

    Lenz's Law = Conservation of Energy, electromagnetically expressed

    ┌──────────────────────────────────────────────────────────────────────┐
    │                                                                      │
    │   The opposition isn't a bug — it's the mechanism by which          │
    │   energy transfers from one form to another.                        │
    │                                                                      │
    │   • Generator: opposition = how mechanical → electrical             │
    │   • Motor: opposition = how electrical → mechanical                 │
    │   • Inductor: opposition = how energy enters/exits the field        │
    │   • Transformer: opposition = how power couples between coils       │
    │                                                                      │
    │   Without opposition, there would be no energy transfer at all.     │
    │                                                                      │
    └──────────────────────────────────────────────────────────────────────┘
```

| System | What Lenz's Law Opposes | What This Enables |
|--------|------------------------|-------------------|
| Generator | Rotation of coil | Mechanical → electrical conversion |
| Motor | Current flow | Electrical → mechanical conversion |
| [[learning/notes/quick-context/inductor|Inductor]] | Current changes | Energy storage in magnetic field |
| Transformer | Flux changes in primary | Power transfer to secondary |
| Eddy current brake | Motion of conductor | Magnetic braking (no friction wear) |

</details>

<details>
<summary><strong>Concrete Example</strong> — Dropping a magnet through a copper tube</summary>

## The Falling Magnet Demonstration

One of the most striking demonstrations of Lenz's Law: drop a strong magnet through a copper tube, and it falls slowly — as if moving through thick honey.

```
MAGNET FALLING THROUGH COPPER TUBE
══════════════════════════════════════════════════════════════════════════════

SETUP:
────────────────────────────────────────────────────────────────────────────

    Copper tube           Neodymium magnet
    (non-magnetic!)       (strong!)

    ┌───────────┐
    │███████████│         ╔═══╗
    │███     ███│         ║ N ║
    │███     ███│         ╠═══╣
    │███     ███│         ║ S ║
    │███     ███│         ╚═══╝
    │███     ███│           │
    │███     ███│           │ gravity
    │███     ███│           ▼
    │███     ███│
    │███████████│
    └───────────┘

    Note: Copper is NOT magnetic! It doesn't attract magnets.
    But something dramatic happens when the magnet falls through...


WHAT HAPPENS (Lenz's Law):
────────────────────────────────────────────────────────────────────────────

    As the magnet approaches a section of tube:

           ┌──────────────────────────────────────┐
           │  Magnet approaching → flux increases │
           │                                      │
           │      ╔═══╗                           │
           │      ║ N ║ ↓                         │
           │      ╠═══╣                           │
           │      ║ S ║                           │
           │      ╚═══╝                           │
           │        │                             │
           │        ▼                             │
           │  ┌─────────────┐                     │
           │  │             │ ← eddy currents     │
           │  │    TUBE     │   circulate here    │
           │  │   SECTION   │   creating field    │
           │  │             │   that REPELS N     │
           │  └─────────────┘                     │
           │                                      │
           │  Induced currents create S pole      │
           │  facing up → repels falling magnet   │
           └──────────────────────────────────────┘

    As the magnet leaves a section of tube:

           ┌──────────────────────────────────────┐
           │  Magnet leaving → flux decreases     │
           │                                      │
           │  ┌─────────────┐                     │
           │  │             │ ← eddy currents     │
           │  │    TUBE     │   now flow OPPOSITE │
           │  │   SECTION   │   direction, create │
           │  │             │   field that        │
           │  └─────────────┘   ATTRACTS S        │
           │        │                             │
           │        │                             │
           │      ╔═══╗                           │
           │      ║ N ║                           │
           │      ╠═══╣ ↓                         │
           │      ║ S ║                           │
           │      ╚═══╝                           │
           │                                      │
           │  Induced currents create N pole      │
           │  facing down → attracts departing    │
           │  magnet, slowing it                  │
           └──────────────────────────────────────┘


COMBINED EFFECT:
────────────────────────────────────────────────────────────────────────────

    Section above magnet: attracts it (opposes downward motion)
    Section below magnet: repels it (opposes downward motion)

                ↑ attraction
                │
           ─────┼─────  tube section
                │
              ╔═══╗
              ║ N ║
              ╠═══╣
              ║ S ║
              ╚═══╝
                │
           ─────┼─────  tube section
                │
                ↑ repulsion

    Both effects OPPOSE the motion (Lenz's Law).
    The magnet falls slowly, as if braked.

    WHERE DOES THE ENERGY GO?
    ────────────────────────────────────────────────────────────────────────────

    • Gravitational potential energy decreases (magnet falls)
    • Kinetic energy stays nearly constant (slow, steady descent)
    • Electrical energy appears as eddy currents in copper
    • Currents dissipate as heat (copper warms up!)

    Energy: Gravitational PE → Electrical (eddy currents) → Heat

    Touch the tube after dropping the magnet through several times
    — it's measurably warmer!
```

**The one thing most outsiders get wrong about this is...** thinking copper is somehow magnetic. It isn't — copper has no magnetic attraction to stationary magnets. The effect only occurs when the magnet is *moving*, because movement creates changing flux, which induces currents, which create magnetic fields that oppose the motion. A stationary magnet inside a copper tube experiences no force. The moment it moves, opposition appears. This is pure Lenz's Law: no change, no opposition; change creates opposition.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/quick-context/electromagnetism]]** — Lenz's Law is part of Faraday's Law (the minus sign), which is one of [[learning/notes/quick-context/maxwell-equations|Maxwell's four equations]]. Understanding the full electromagnetic framework shows how electric and magnetic fields create each other.

- **[[learning/notes/quick-context/inductor]]** — Inductors are the primary application of Lenz's Law in circuits. The back-EMF that opposes current changes (V = -L × dI/dt) is a direct consequence of Lenz's Law applied to self-induction.

- **[[learning/notes/quick-context/self-induction]]** — Complete walkthrough of the self-induction cycle: current creates flux, changing flux creates back-EMF, and what happens during charging, steady state, and field collapse. Includes voltages across both inductor and load at each phase.

- **[[learning/notes/quick-context/electricity-generation]]** — Generators convert mechanical energy to electrical energy through Lenz's Law: the induced current creates magnetic braking that requires work to overcome, and that work becomes electrical energy.

- **[[learning/notes/quick-context/coil-magnetic-field]]** — Why [[learning/notes/quick-context/electric-current|current]] through a coil creates a magnetic field (B = μ₀nI). This field is what changes when current changes, triggering Lenz's Law effects.

- **[[learning/notes/quick-context/power-watts-joules]]** — The energy perspective on Lenz's Law: the work done against magnetic opposition equals the electrical energy generated. Power = work/time connects mechanical and electrical domains.

- **[[learning/notes/micro-context/electromagnetic-induction]]** — Brief definition of Faraday's Law and [[learning/notes/micro-context/electromagnetic-induction|electromagnetic induction]], of which Lenz's Law specifies the direction.

- **[[learning/notes/quick-context/coil-magnetic-field]]** — Step-by-step walkthrough of how inductors work, with detailed treatment of how Lenz's Law causes back-EMF and voltage spikes.

- **Eddy Currents** — Induced currents in bulk conductors (not wires). Used in induction heating, magnetic braking, and metal detectors. Lenz's Law determines their direction and explains why they oppose motion.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A magnet approaches a coil. Does the coil attract or repel the magnet? Why?
<details>
<summary>Answer</summary>
**The coil repels the magnet.** As the magnet approaches, flux through the coil increases. Lenz's Law says the induced current must create a field that opposes this increase. The coil becomes an electromagnet with its like pole facing the incoming magnet (N facing N, or S facing S), creating repulsion. You must do work to push the magnet closer. See: How It Works — Scenario 1.
</details>

**Q2:** If Lenz's Law didn't exist (no opposition), what would happen when you tried to spin a generator?
<details>
<summary>Answer</summary>
**The generator would spin freely and produce no useful energy.** Without opposition, there would be no magnetic braking. The coil would spin with no resistance, but also no energy transfer. Current might flow, but it wouldn't come from your mechanical work — it would be "free energy" from nothing, violating conservation of energy. Lenz's Law ensures that the mechanical work you do against magnetic braking equals the electrical energy produced. See: Why Opposition is Inevitable.
</details>

**Q3:** An inductor carries steady DC current. Is Lenz's Law active?
<details>
<summary>Answer</summary>
**No, Lenz's Law requires change.** With steady DC, dI/dt = 0, so there's no changing flux, so no induced EMF. The inductor acts like a simple wire (just its DC resistance). Lenz's Law only activates when current changes — during turn-on, turn-off, or AC operation. At steady state, all the "opposition" has already happened, and the inductor is doing nothing but maintaining its magnetic field.
</details>

**Q4:** You drop two identical magnets: one through air, one through a copper tube. Both start at the same height. Which hits the ground first, and why?
<details>
<summary>Answer</summary>
**The one through air hits first.** The magnet in the copper tube experiences Lenz's Law braking: as it falls, it induces eddy currents in the copper that create magnetic fields opposing its motion. Both sections above and below the magnet oppose downward motion. The tube-dropped magnet falls slowly, while the air-dropped one accelerates freely under gravity. See: Concrete Example (Falling Magnet).
</details>

**Q5:** A transformer works by changing current in the primary coil to induce voltage in the secondary. The secondary current creates its own magnetic field. Does this help or oppose the primary's field?
<details>
<summary>Answer</summary>
**It opposes the primary's field (Lenz's Law).** When primary current increases, it increases flux through both coils. The secondary's induced current must create a field that opposes this increase — it flows in the direction that creates a field opposing the primary's field. This is why loading a transformer (drawing current from secondary) causes more current to flow in the primary: the secondary's opposing field reduces net flux, requiring the primary to work harder to maintain the same flux change. This is the mechanism by which power transfers from primary to secondary.
</details>

</details>
