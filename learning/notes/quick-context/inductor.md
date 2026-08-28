---
topic: Inductor
created: 2026-02-06
---
> **Related:** [[learning/notes/micro-context/buck-converter]] | [[learning/notes/micro-context/current-inductor-capacitor-relationship]] | [[learning/notes/micro-context/power-inductor]] | [[learning/notes/micro-context/short-circuit]] | [[learning/notes/quick-context/capacitance]]

> **TL;DR:** An inductor stores energy in a magnetic field created by current flowing through a coil of wire, opposing any change in current—it's the magnetic counterpart to a [[quick-context/capacitor|capacitor]] (which stores energy in an electric field) and is essential for power supplies, filters, and energy conversion.

# Inductor

## The Core Problem: Smoothing and Converting Power

A switching power supply chops a DC [[learning/notes/quick-context/voltage|voltage]] on and off millions of times per second. Without an inductor, you'd just get violent pulses of current. The inductor smooths these pulses into steady current by storing energy in its magnetic field during the "on" phase and releasing it during the "off" phase. Every phone charger, laptop adapter, and voltage regulator on every [[quick-context/pcb-printed-circuit-board|PCB]] depends on inductors to efficiently convert one voltage to another. They're also half of the LC resonant circuits used in radio tuning, and they form filters that block high-frequency noise while passing DC.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Inductance (L)** | The ability to store energy in a magnetic field per unit current change, measured in henrys (H). Most practical inductors are microhenrys (μH) to millihenrys (mH). |
| **Back-EMF** | The voltage an inductor generates to oppose changes in current: V = L × dI/dt ([[quick-context/lenzs-law|Lenz's Law]]). Try to suddenly stop current through an inductor and it generates a voltage spike (potentially destructive). |
| **Saturation Current** | The current at which the core's magnetic material can't hold any more flux—inductance drops sharply and the inductor stops working properly. Exceeding this is a common design mistake. |
| **DCR (DC Resistance)** | The resistance of the wire in the coil. Lower is better—DCR wastes power as heat. Thicker wire = lower DCR but larger inductor. |
| **Core Material** | What the coil is wound around. Air (no saturation, low inductance), ferrite (high inductance, saturates), powdered iron (good for power, gradual saturation). |

<details>
<summary><strong>How It Works</strong></summary>

When [[quick-context/electric-current|current]] flows through a wire, it creates a magnetic field around the wire (see [[quick-context/electromagnetism]] and [[quick-context/coil-magnetic-field|coil magnetic field]]). Coiling the wire concentrates the field. The key behavior: an inductor resists changes to the current flowing through it—the exact opposite of a [[quick-context/capacitor|capacitor]], which resists changes in voltage.

```
WHY A COIL, NOT JUST A STRAIGHT WIRE?
══════════════════════════════════════════════════════════════════════════════

A straight wire DOES have a magnetic field when current flows. Every current-
carrying conductor creates a magnetic field — that's fundamental physics.
So why doesn't a straight wire act like an inductor?

It does! But the inductance is tiny. The difference is concentration and
self-linkage.


STRAIGHT WIRE: Field exists, but weak and spread out
──────────────────────────────────────────────────────────────────────────────

    Current through ANY wire creates circular magnetic field:

                    ╭───────╮
                   ╱    ↑    ╲
                  │     │     │
                  │  ───┼───  │  ← Wire (current into page ⊗)
                  │     │     │
                   ╲    ↓    ╱
                    ╰───────╯

                  Field circles around wire (right-hand rule)

    The field exists! But:
    • It spreads out into open space (not concentrated)
    • The wire doesn't "link" with much of its own flux
    • Energy stored is small: E = ½LI², and L is tiny

    A 10cm straight wire has inductance ≈ 100 nH (0.0001 mH)
    That's basically nothing for most purposes.


COILED WIRE: Same physics, but MULTIPLIED
──────────────────────────────────────────────────────────────────────────────

    When you coil the wire, two things happen:

    1. THE FIELD CONCENTRATES (adds up in the center)

        Straight wire:              Coiled wire:

            ○                        →→→→→→→→→→
           ╱│╲                      ║ ⊃⊃⊃⊃⊃⊃ ║
          ╱ │ ╲                     ║ ║║║║║║ ║
            │                       ║ ║║║║║║ ║
        Field spreads              →→→→→→→→→→
        in all directions           ←←←←←←←←←←

                                   Fields from each turn ADD UP
                                   in the center of the coil


    2. EACH TURN LINKS WITH FLUX FROM ALL OTHER TURNS (the key insight!)

        Single turn:
        ┌─────────────────────┐
        │  Flux Φ passes      │
        │  through this loop  │     Inductance ∝ Φ/I
        │        ↓↓↓↓         │
        └─────────────────────┘

        Multiple turns (N turns):
        ┌─────────────────────┐
        │  ╔═══════════════╗  │     Turn 1 links with flux from turns 1,2,3...N
        │  ║ ╔═══════════╗ ║  │     Turn 2 links with flux from turns 1,2,3...N
        │  ║ ║ ╔═══════╗ ║ ║  │     Turn 3 links with flux from turns 1,2,3...N
        │  ║ ║ ║  ↓↓↓  ║ ║ ║  │     ...
        │  ║ ║ ╚═══════╝ ║ ║  │
        │  ║ ╚═══════════╝ ║  │     Total flux linkage = N × Φ
        │  ╚═══════════════╝  │
        └─────────────────────┘

        Inductance L ∝ N² (turns SQUARED!)

        10 turns doesn't give 10× inductance — it gives 100× inductance!


    THE MATH:

        For a coil:  L = (μ₀ × N² × A) / length

        • μ₀ = permeability of free space
        • N = number of turns  ← This is squared!
        • A = cross-sectional area
        • length = coil length

        Example:
        • 1 turn:    L ∝ 1² = 1
        • 10 turns:  L ∝ 10² = 100
        • 100 turns: L ∝ 100² = 10,000


    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │   STRAIGHT WIRE                      COIL                             │
    │   ─────────────                      ────                             │
    │   Has magnetic field: YES            Has magnetic field: YES          │
    │   Has inductance: YES (tiny)         Has inductance: YES (large)      │
    │                                                                        │
    │   Why small?                         Why large?                       │
    │   • Field spreads into space         • Field concentrates in center   │
    │   • Wire doesn't link with           • Each turn links with flux     │
    │     much of its own flux               from ALL turns (N² effect)    │
    │                                                                        │
    │   The physics is IDENTICAL. The geometry makes the difference.       │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘


INDUCTOR FUNDAMENTALS
══════════════════════════════════════════════════════════════════════════════

    Current flowing through a coil creates a magnetic field:

         ┌──⊃⊃⊃⊃⊃⊃⊃⊃──┐
    I →  │   ══════════  │  → I
         │   Magnetic    │
         │   field lines │
         └──────────────┘

    V = L × dI/dt    (voltage across inductor = inductance × rate of
                       current change)

    Key behaviors:
    • Constant current → V = 0  (inductor acts like a wire)
    • Increasing current → inductor opposes, generates negative voltage
    • Decreasing current → inductor opposes, generates positive voltage
    • Sudden current cutoff → HUGE voltage spike (V = L × dI/dt, dt≈0)


ENERGY STORAGE — The Key to Understanding Everything
══════════════════════════════════════════════════════════════════════════════

    E = ½ × L × I²

    This equation is the answer to "why does it take time?" and "why does
    current keep flowing?" Everything about inductor behavior follows from
    the fact that the magnetic field contains real, physical energy.

    Compare with capacitor: E = ½ × C × V²

    INDUCTOR                        CAPACITOR
    ────────                        ─────────
    Stores energy in magnetic       Stores energy in electric field
    field
    Opposes current changes         Opposes voltage changes
    Blocks AC, passes DC            Blocks DC, passes AC
    V = L × dI/dt                   I = C × dV/dt
    Series: L_total = L1 + L2       Series: 1/C = 1/C1 + 1/C2
    Parallel: 1/L = 1/L1 + 1/L2    Parallel: C_total = C1 + C2

    They're exact duals of each other!


RL TIME CONSTANT
══════════════════════════════════════════════════════════════════════════════

    τ = L / R    (compare with RC: τ = R × C)

       ┌───╱╱╱╱───⊃⊃⊃⊃───┐
       │     R       L     │
    Vs ┤                   │
       │                   │
       └───────────────────┘

    Current builds up exponentially:
    I(t) = (Vs/R) × (1 - e^(-t/τ))

    I                                    V across inductor
    ▲                                    ▲
    │            ─────────────          Vs│─┐
    │       ────                         │  └──
    │    ──                              │     ───
    │  ─                                 │        ────
    │─                                   │            ──────────
    └──┬──┬──┬──┬──► t                  └──┬──┬──┬──┬──► t
       1τ 2τ 3τ 5τ                        1τ 2τ 3τ 5τ

    At t=0: inductor blocks all current (acts like open circuit)
    At t=∞: inductor passes all current (acts like short circuit)
    Exactly opposite of a capacitor!


WHY DOES VOLTAGE "APPEAR" ACROSS THE LOAD OVER TIME?
══════════════════════════════════════════════════════════════════════════════

This is a common confusion. Let's trace through what actually happens when you
connect a battery to an inductor with a load (resistor):

    CIRCUIT:
                  L (inductor)        R (load)
         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │                                     │
      Vs │ 10V                                 │
         │                                     │
         └─────────────────────────────────────┘

    Kirchhoff's Voltage Law:   Vs = V_L + V_R
                               10V = V_L + V_R   (always true!)


MOMENT 1: The instant you connect the battery (t = 0)
──────────────────────────────────────────────────────────────────────────────

    Current before:  I = 0 A
    Current now:     I = 0 A  (hasn't had time to change yet!)

    Since I = 0:     V_R = I × R = 0 × R = 0V

    From KVL:        V_L = Vs - V_R = 10V - 0V = 10V

    ALL the source voltage appears across the inductor!

         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │         10V               0V        │
      10V│        (all here!)      (nothing)   │
         └─────────────────────────────────────┘
                  V_L = 10V         V_R = 0V

    WHY? The inductor is OPPOSING the current change.
    • Current wants to go from 0 to something
    • Inductor generates back-EMF: V_L = L × dI/dt
    • This back-EMF is 10V, opposing the battery
    • Net driving force on current = Vs - V_L = 10V - 10V... wait, that's 0?

    Not quite. The 10V across the inductor IS the voltage driving dI/dt:
    V_L = L × dI/dt   →   dI/dt = V_L / L = 10V / L

    So current STARTS to rise at rate 10/L amps per second.


MOMENT 2: A short time later (t = small)
──────────────────────────────────────────────────────────────────────────────

    Current has started flowing:  I = small (say 0.1A if R=100Ω, L=1H)

    Now:             V_R = I × R = 0.1A × 100Ω = 1V

    From KVL:        V_L = Vs - V_R = 10V - 1V = 9V

    Voltage is now SHARED between inductor and load!

         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │          9V                1V       │
      10V│        (most here)      (some now)  │
         └─────────────────────────────────────┘
                  V_L = 9V          V_R = 1V

    WHY is V_L decreasing?
    • Current is now flowing, so it's changing LESS rapidly
    • dI/dt is smaller than before
    • V_L = L × dI/dt → smaller dI/dt means smaller V_L

    The inductor is "giving up" voltage to the load as current builds up.


MOMENT 3: Much later (t → ∞, steady state)
──────────────────────────────────────────────────────────────────────────────

    Current has reached its maximum:  I = Vs/R = 10V/100Ω = 0.1A
    Current is now CONSTANT (not changing)

    Since I is constant:  dI/dt = 0

    Therefore:           V_L = L × dI/dt = L × 0 = 0V

    From KVL:            V_R = Vs - V_L = 10V - 0V = 10V

    ALL the source voltage now appears across the load!

         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │          0V               10V       │
      10V│        (nothing!)      (all here!)  │
         └─────────────────────────────────────┘
                  V_L = 0V          V_R = 10V

    WHY? The inductor is no longer opposing anything.
    • Current is steady—no change to oppose
    • Magnetic field is fully established and stable
    • Inductor acts like a plain wire (just its DCR)


THE PHYSICS SUMMARY:
══════════════════════════════════════════════════════════════════════════════

    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │  V_L = L × dI/dt     ← This equation explains everything!             │
    │                                                                        │
    │  • At t=0: current trying to change fast → dI/dt is large → V_L large │
    │  • As time passes: current approaches limit → dI/dt decreases → V_L ↓ │
    │  • At t=∞: current constant → dI/dt = 0 → V_L = 0                     │
    │                                                                        │
    │  The inductor "uses up" voltage only while current is CHANGING.       │
    │  Once current stabilizes, the inductor becomes invisible (0V drop).   │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘

    This is [[quick-context/lenzs-law|Lenz's Law]] in action:

    • Inductor opposes CHANGE, not current itself
    • Opposition is proportional to rate of change
    • Fast changes → strong opposition (high voltage)
    • Slow/no changes → weak/no opposition (low/zero voltage)

    Energy perspective:
    • While V_L > 0, energy is flowing INTO the magnetic field
    • At steady state, field is "full"—no more energy transfer needed
    • If you then disconnect, stored energy releases (voltage spike!)


THE DEEP PHYSICS: WHY CAN'T CURRENT CHANGE INSTANTLY?
══════════════════════════════════════════════════════════════════════════════

This is the real question. The inductor is just wire—why can't electrons
flow through it immediately?

THE ANSWER: Because the magnetic field requires ENERGY to create.

    When current flows through a coil:
    ─────────────────────────────────────────────────────────────────────────

    Current (I) → Creates magnetic field (B) → Field stores energy (E = ½LI²)

         I ──→ ⊃⊃⊃⊃⊃⊃ ──→
               ║║║║║║
               ║║║║║║  ← Magnetic field lines
               ║║║║║║    (real, physical, contain energy)
               ══════

    The magnetic field isn't just a concept—it's a physical thing that
    exists in space and contains energy. Creating this field requires
    transferring energy from the power source into the field.


    Why instant current change is impossible:
    ─────────────────────────────────────────────────────────────────────────

    Suppose current could jump instantly from 0 to 1 amp:

        Before (t=0⁻):   I = 0 A      →  E = ½L(0)² = 0 J
        After (t=0⁺):    I = 1 A      →  E = ½L(1)² = ½L joules

    Energy changed from 0 to ½L joules in ZERO time.

        Power = Energy / Time = (½L) / 0 = INFINITE POWER

    Infinite power is physically impossible. You cannot transfer a finite
    amount of energy in zero time. Therefore current CANNOT change instantly.

    The math confirms this:

        V = L × dI/dt

    If dI/dt → ∞ (instant change), then V → ∞ (infinite voltage).
    No real power source can provide infinite voltage.


    The mechanical analogy — INERTIA:
    ─────────────────────────────────────────────────────────────────────────

    An inductor has "electrical inertia" just like mass has mechanical inertia.

        MASS                              INDUCTANCE
        ────                              ──────────
        Stores energy in motion:          Stores energy in magnetic field:
        E = ½mv²                          E = ½LI²

        Resists changes in velocity:      Resists changes in current:
        F = m × dv/dt                     V = L × dI/dt

        Can't instantly change speed      Can't instantly change current
        (would require infinite force)    (would require infinite voltage)

    Think of a heavy flywheel:

        ┌─────────────────────────────────────────────────────────────────┐
        │                                                                 │
        │   FLYWHEEL                         INDUCTOR                     │
        │                                                                 │
        │      ╭───╮                            ⊃⊃⊃⊃                     │
        │     ╱     ╲   ← spinning             ════   ← current flowing  │
        │    │       │    (has momentum)       ════     (has "momentum") │
        │     ╲     ╱                          ════                      │
        │      ╰───╯                                                     │
        │                                                                 │
        │   To speed it up:                  To increase current:        │
        │   Apply torque, wait for it        Apply voltage, wait for it  │
        │   to accelerate gradually          to build up gradually       │
        │                                                                 │
        │   To stop it instantly:            To stop current instantly:  │
        │   Would require infinite force     Would require infinite V    │
        │   (impossible)                     (impossible)                │
        │                                                                 │
        └─────────────────────────────────────────────────────────────────┘


THE DEEP PHYSICS: WHY DOES CURRENT KEEP FLOWING WHEN DISCONNECTED?
══════════════════════════════════════════════════════════════════════════════

When you open a switch on an inductor carrying current, the current doesn't
stop. It WILL find a path—arcing across the switch if necessary. Why?

THE ANSWER: The magnetic field contains energy that MUST go somewhere.

    Before disconnection:
    ─────────────────────────────────────────────────────────────────────────

    Current I is flowing, magnetic field is established:

         ┌────────[SW]────⊃⊃⊃⊃⊃⊃────╱╱╱╱╱────┐
         │       (closed)    L         R      │
      Vs │    I →→→→→→→→→→→→→→→→→→→→→→→→→    │
         │                ║║║║║║              │
         └────────────────╨╨╨╨╨╨──────────────┘
                     magnetic field
                     contains E = ½LI²


    The moment you open the switch:
    ─────────────────────────────────────────────────────────────────────────

         ┌────────[SW]────⊃⊃⊃⊃⊃⊃────╱╱╱╱╱────┐
         │       (open!)     L         R      │
      Vs │       ╳                            │
         │     AIR GAP   ║║║║║║               │
         └───────────────╨╨╨╨╨╨───────────────┘
                    field still exists!
                    still contains ½LI² of energy!

    The field cannot just disappear. Energy is conserved.
    That energy MUST be released somehow.


    What happens physically:
    ─────────────────────────────────────────────────────────────────────────

    1. Switch opens, breaking the circuit

    2. Current TRIES to stop (dI/dt becomes very negative)

    3. But V = L × dI/dt means a huge POSITIVE voltage appears across L

    4. This voltage is the field's "attempt" to keep current flowing

    5. The voltage rises until it finds a path:

        • If voltage exceeds air breakdown (~3000V/mm), current ARCS
          across the switch gap

        • Or current flows through parasitic capacitance

        • Or it destroys a transistor that was switching it

    6. Current continues through whatever path exists, dissipating
       the field's energy as heat (in the arc, in components, etc.)


    The field FORCES current to continue:
    ─────────────────────────────────────────────────────────────────────────

         ┌────────[SW]────⊃⊃⊃⊃⊃⊃────╱╱╱╱╱────┐
         │       ╳ ⚡      L         R      │
         │       │ ARC!  ║║║║║║              │
         │       │ (500V)║║║║║║              │
         └───────┴───────╨╨╨╨╨╨──────────────┘

    The inductor generates whatever voltage is necessary to maintain
    current flow. If that means 500V across a 1mm air gap, so be it.

    The energy equation:

        Before: E = ½LI²  (stored in field)
        After:  E = 0     (field collapsed)

        Where did the energy go?
        → Dissipated as heat in the arc
        → Or heat in whatever component absorbed the spike


    This is NOT the inductor "wanting" current to flow—it's simpler:
    ─────────────────────────────────────────────────────────────────────────

    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │   The magnetic field contains real energy.                            │
    │   Energy cannot be created or destroyed.                              │
    │   The field must collapse to release its energy.                      │
    │   A collapsing field (dΦ/dt) induces voltage (Faraday's Law).        │
    │   That voltage drives current through whatever path exists.           │
    │                                                                        │
    │   The current isn't "trying" to flow—the field is collapsing,        │
    │   and a collapsing field ALWAYS induces current. It's physics.        │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘


    The flyback diode solution:
    ─────────────────────────────────────────────────────────────────────────

    Give the current a safe path to flow while the field collapses:

         ┌────────[SW]────⊃⊃⊃⊃⊃⊃────╱╱╱╱╱────┐
         │       (open)     L    │    R      │
         │                  ║║║║ ▼ D         │
         │                  ║║║║ │ (diode)   │
         └──────────────────╨╨╨╨─┴───────────┘

    When switch opens:
    • Voltage across L reverses (tries to keep current going)
    • This forward-biases diode D
    • Current flows through D, gradually decreasing
    • Field energy dissipates safely as heat in R and D
    • No destructive voltage spike
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Inductance vs. Size vs. Saturation vs. Loss

```
THE CORE TRADEOFFS
══════════════════════════════════════════════════════════════════════════════

    Want more inductance?  → More turns or bigger core → Larger size
    Want higher current?   → Bigger core (avoid saturation) → Larger size
    Want lower DCR?        → Thicker wire → Larger size
    Want higher frequency? → Fewer turns (lower inductance) → Core losses

    Everything pushes toward BIGGER. Inductors are usually the largest
    component on a power supply PCB.
```

| Type | Inductance | Current | Frequency | Best For |
|------|-----------|---------|-----------|----------|
| **Air core** | Very low (nH) | Unlimited (no saturation) | GHz | RF circuits, antennas |
| **Ferrite core** | High (μH-mH) | Limited by saturation | kHz-MHz | Power supplies, filters |
| **Powdered iron** | Medium (μH) | High (gradual saturation) | kHz-MHz | High-current power |
| **Toroidal** | High (contained field) | Medium-high | kHz-MHz | Low EMI, audio |
| **SMD power** | Low-medium (μH) | Medium | MHz | Compact DC-DC converters |
| **Molded/shielded** | Low-medium (μH) | Medium | MHz | Dense PCBs, low EMI |

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Buck Converter: Stepping Voltage Down Efficiently

The most common inductor application. A [[learning/notes/micro-context/buck-converter|buck converter]] uses a switch, [[learning/notes/quick-context/diode|diode]], inductor, and [[quick-context/capacitor|capacitor]] to step voltage down (e.g., 12V → 3.3V) at 85-95% efficiency—far better than a [[learning/notes/quick-context/resistor|resistor]] voltage divider, which wastes the excess as heat.

```
BUCK CONVERTER OPERATION
══════════════════════════════════════════════════════════════════════════════

    Vin (12V) ──┬──╥──⊃⊃⊃⊃──┬─── Vout (3.3V)
                │  ║    L     │
              [SW] ║         ═╪═ C (output cap)
                │  ║          │
                ▼  ║         GND
              [D]  ║
                │  ║
               GND ║
                   ║
              Controller sets duty cycle: D = Vout/Vin = 3.3/12 = 27.5%


    PHASE 1: Switch ON (27.5% of cycle)
    ────────────────────────────────────
    Vin ──[ON]──⊃⊃⊃⊃──┬── Vout
                  L      │
         Current  ↑     ═╪═ C
         ramps UP        │
                        GND

    • Current flows from Vin through L to load
    • L stores energy in magnetic field (current increasing)
    • V_L = Vin - Vout = 8.7V (positive, current ramps up)


    PHASE 2: Switch OFF (72.5% of cycle)
    ─────────────────────────────────────
          [OFF]  ⊃⊃⊃⊃──┬── Vout
                  L      │
    GND ──[D]───┘       ═╪═ C
         Current  ↑      │
         ramps DOWN     GND

    • Switch opens, but inductor FORCES current to keep flowing
    • Current freewheels through diode
    • L releases stored energy (current decreasing)
    • V_L = -Vout = -3.3V (negative, current ramps down)


    INDUCTOR CURRENT WAVEFORM
    ─────────────────────────────────────
    I_L
     ▲    ╱╲      ╱╲      ╱╲
     │   ╱  ╲    ╱  ╲    ╱  ╲      ← "ripple" around average
     │──╱────╲──╱────╲──╱────╲──   ← average = load current
     │ ╱      ╲╱      ╲╱      ╲
     └──────────────────────────► t
       ON OFF  ON OFF  ON OFF

    The output capacitor smooths this ripple into steady DC.
```

**Why not just use a resistor to drop voltage?** A resistor dropping 12V to 3.3V at 1A would waste P = 8.7V × 1A = 8.7W as heat. The buck converter wastes only ~0.5W for the same job. At scale (millions of devices, 24/7 operation), this efficiency difference is enormous.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/capacitor]]** — Inductors and capacitors are exact duals: one stores energy in magnetic fields, the other in electric fields. Together they form LC resonant circuits (f = 1/(2π√LC)) and second-order filters. See [[quick-context/capacitance]] for the underlying property and how parasitic [[learning/notes/quick-context/capacitance|capacitance]] interacts with inductance in real circuits.

- **[[quick-context/electric-current]]** — The inductor equation V = L×dI/dt means inductors care about current changes. Understanding current as charge flow is essential.

- **[[quick-context/resistor]]** — RL circuits (inductor + resistor) have a time constant τ = L/R, analogous to RC circuits. Real inductors always have parasitic resistance (DCR).

- **[[quick-context/pcb-printed-circuit-board]]** — Inductor placement matters: magnetic fields can couple into nearby traces. [[learning/notes/micro-context/power-inductor|Power inductor]] layout is critical for switching power supply performance.

- **[[quick-context/thermal-noise-electronics]]** — Inductors don't generate thermal noise themselves (only resistive elements do), but their DCR contributes noise in sensitive circuits.

- **[[quick-context/electricity-generation]]** — Inductors are fundamental to electromagnetic generators. Faraday's law (EMF = -N × dΦ/dt) describes how changing magnetic flux through a coil induces voltage—the operating principle of virtually all grid electricity generation.

- **[[quick-context/coil-magnetic-field]]** — [[learning/notes/quick-context/coil-magnetic-field|Why current through a coil creates a magnetic field]], and how to calculate field strength (B = μ₀nI). The coil field is what inductors store energy in.

- **[[quick-context/lenzs-law]]** — The physics behind back-EMF: why the induced voltage always opposes current changes. This is conservation of energy enforced electromagnetically.

- **[[quick-context/self-induction]]** — The complete cycle: how current creates flux, changing flux creates back-EMF, and what happens when you disconnect the battery (the field collapses, pushing current through the load until all energy is dissipated). Includes voltage across both inductor and load at each phase.

- **[[small-context/permanent-magnet-creation]]** — A magnetizer is essentially a high-current inductor used to align magnetic domains in ferromagnetic materials. The same principle (current creates magnetic field) but applied to create permanent magnets.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does an inductor generate a voltage spike when you suddenly interrupt its current?
<details>
<summary>Answer</summary>
**V = L × dI/dt. If dt approaches zero (instant cutoff), the voltage approaches infinity.** The inductor's magnetic field is collapsing and it will do whatever it takes to keep current flowing—even generating hundreds of volts across a small inductor. This is why flyback diodes are placed across inductive loads like motors and relays: they give the current a safe path to flow during turn-off.
</details>

**Q2:** An inductor and a [[learning/notes/quick-context/capacitor|capacitor]] are "duals." What does this mean practically?
<details>
<summary>Answer</summary>
**They have opposite behaviors in every way.** Capacitors block DC and pass AC; inductors pass DC and block AC. Capacitors oppose voltage changes; inductors oppose current changes. Their series/parallel formulas are swapped. Their time constant formulas are inverted (τ = RC vs τ = L/R). Together they create resonance at f = 1/(2π√LC).
</details>

**Q3:** A buck converter has Vin = 5V and needs Vout = 1.8V. What duty cycle is needed?
<details>
<summary>Answer</summary>
**36%.** Duty cycle D = Vout/Vin = 1.8/5 = 0.36 = 36%. The switch is ON for 36% of each cycle, during which the inductor charges, and OFF for 64%, during which it discharges.
</details>

**Q4:** Why are inductors typically the largest component on a power supply PCB?
<details>
<summary>Answer</summary>
**Magnetic energy storage requires physical volume.** More inductance needs more turns of wire. Higher current needs a larger core to avoid saturation. Lower losses need thicker wire (lower DCR). All of these push toward larger size. Unlike capacitors (which can be made very thin with ceramic layers), inductors fundamentally need 3D volume for their magnetic field.
</details>

**Q5:** What happens if you exceed an inductor's saturation current?
<details>
<summary>Answer</summary>
**Inductance drops sharply and current spikes uncontrollably.** The core material can't support any more magnetic flux, so the inductor stops opposing current changes and acts more like a [[learning/notes/micro-context/short-circuit|short circuit]] (just its DCR). In a switching power supply, this means current shoots up, the switch [[learning/notes/quick-context/transistor|transistor]] may overheat or blow, and output voltage regulation is lost. Always pick an inductor with saturation current above your maximum expected current.
</details>

</details>
