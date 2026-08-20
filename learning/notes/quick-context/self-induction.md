---
topic: Self-Induction
created: 2026-02-17
---

# Self-Induction

> **Related:** [[learning/notes/micro-context/electromagnetic-induction]] | [[learning/notes/quick-context/coil-magnetic-field]] | [[learning/notes/micro-context/coriolis-effect]] | [[learning/notes/micro-context/coulomb-history]] | [[learning/notes/micro-context/current-inductor-capacitor-relationship]]

> **TL;DR:** Self-induction is the phenomenon where a coil's own changing current creates a changing magnetic flux, which induces a voltage (back-EMF) that opposes the current change. The current creates the flux, but it's the *rate of change* of flux that creates the opposition. This explains why current can't change instantly in an [[learning/notes/quick-context/inductor|inductor]], and why the magnetic field "pushes" current when you try to stop it.

## The Core Question

If the magnetic flux is created BY the current, how can the flux oppose the current? Isn't that circular?

The answer: **the flux doesn't oppose the current directly — the *changing* flux creates a [[learning/notes/quick-context/voltage|voltage]] that opposes the *change* in current.** This is self-induction, and understanding it resolves the apparent paradox.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Self-Induction** | When a coil's own changing current induces a voltage in itself. The coil's flux links with its own turns, so any current change creates back-EMF. |
| **Back-EMF** | The voltage induced in a coil that opposes the change in current. Equal to V = L × dI/dt. It's called "back" because it opposes the applied voltage. |
| **Flux Linkage** | The total magnetic flux linking with a coil: Λ = N × Φ = L × I. For a coil, each turn links with flux from all turns, multiplying the effect. |
| **Mutual Induction** | When changing current in one coil induces voltage in a nearby coil. Self-induction is the special case where the coil induces voltage in itself. |
| **Steady State** | When current is constant (dI/dt = 0), so there's no changing flux, no back-EMF, and the inductor acts like a plain wire. |

<details>
<summary><strong>How It Works</strong> — The complete cycle with voltages</summary>

## The Self-Induction Feedback Loop

The key insight: **current creates flux, but changing flux creates back-EMF**.

```
THE CAUSAL CHAIN
══════════════════════════════════════════════════════════════════════════════

    Current (I)  ───creates───▶  Magnetic Flux (Φ = L × I)
                                        │
                                        │ if changing
                                        ▼
                              Changing Flux (dΦ/dt = L × dI/dt)
                                        │
                                        │ induces (Faraday's Law)
                                        ▼
                              Back-EMF (V = -L × dI/dt)
                                        │
                                        │ opposes (Lenz's Law)
                                        ▼
                              Change in Current (dI/dt)


    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │   The flux doesn't "block" current like a wall.                       │
    │   The RATE OF CHANGE of flux creates a voltage that fights            │
    │   against the applied voltage.                                         │
    │                                                                        │
    │   Once current is steady → flux is steady → no back-EMF → no fight.  │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘
```

## Complete Circuit Analysis: Inductor + Load

Let's trace through the COMPLETE cycle with actual voltages, including what happens when you disconnect the battery.

```
THE CIRCUIT
══════════════════════════════════════════════════════════════════════════════

              L (inductor)        R (load)
         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │                                     │
      Vs │ 10V                                 │
         │                                     │
         └─────────────────────────────────────┘

    Kirchhoff's Voltage Law (always true):

        Vs = V_L + V_R

    Where:
    • Vs = source voltage (10V battery)
    • V_L = voltage across inductor = L × dI/dt
    • V_R = voltage across load = I × R

    Assume: L = 1H, R = 10Ω, so final current = Vs/R = 1A


══════════════════════════════════════════════════════════════════════════════
PHASE 1: THE INSTANT YOU CONNECT THE BATTERY (t = 0)
══════════════════════════════════════════════════════════════════════════════

    What's happening:
    • Current was 0, now trying to flow
    • Flux was 0, now trying to build
    • dI/dt is MAXIMUM (current wants to change as fast as possible)

         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │         V_L                V_R      │
      10V│         10V                0V       │
         │                                     │
         └─────────────────────────────────────┘
              I = 0A (just starting)

    The numbers:
    ─────────────────────────────────────────────────────────────────────────
    • Current:           I = 0 A
    • Flux:              Φ = L × I = 1 × 0 = 0 Wb
    • Load voltage:      V_R = I × R = 0 × 10 = 0V
    • Inductor voltage:  V_L = Vs - V_R = 10V - 0V = 10V
    • Rate of change:    dI/dt = V_L / L = 10V / 1H = 10 A/s

    WHY is V_L = 10V?
    ─────────────────────────────────────────────────────────────────────────
    The current is TRYING to increase from 0. This attempt to change creates
    a changing flux, which induces back-EMF equal to 10V. The back-EMF
    absorbs the entire source voltage, leaving nothing for the load.

    But current IS starting to flow — at 10 amps per second initially.


══════════════════════════════════════════════════════════════════════════════
PHASE 2: CURRENT BUILDING UP (t = 0.1 seconds, as example)
══════════════════════════════════════════════════════════════════════════════

    What's happening:
    • Current has been rising, now at some intermediate value
    • Flux has partially built up
    • dI/dt is decreasing (current rising more slowly now)

         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │         V_L                V_R      │
      10V│         6.3V               3.7V     │
         │          ║║║║                       │
         └──────────╨╨╨╨───────────────────────┘
              I ≈ 0.37A, Φ building

    The numbers (at t = τ = L/R = 0.1s):
    ─────────────────────────────────────────────────────────────────────────
    • Current:           I ≈ 0.63 × (Vs/R) = 0.63A  (63% of final)
    • Flux:              Φ = L × I = 1 × 0.63 = 0.63 Wb
    • Load voltage:      V_R = I × R = 0.63 × 10 = 6.3V
    • Inductor voltage:  V_L = Vs - V_R = 10V - 6.3V = 3.7V
    • Rate of change:    dI/dt = V_L / L = 3.7V / 1H = 3.7 A/s

    WHY is V_L decreasing?
    ─────────────────────────────────────────────────────────────────────────
    Current is closer to its final value, so it's changing SLOWER.
    Slower change → less dI/dt → less back-EMF.

    Energy is flowing into the magnetic field (E = ½LI² = 0.2J so far)


══════════════════════════════════════════════════════════════════════════════
PHASE 3: STEADY STATE (t → ∞, practically after ~5τ = 0.5s)
══════════════════════════════════════════════════════════════════════════════

    What's happening:
    • Current has reached maximum (limited by R)
    • Flux is at maximum and STABLE
    • dI/dt = 0 (nothing changing)

         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │         V_L                V_R      │
      10V│         0V                 10V      │
         │        ║║║║║║                       │
         └────────╨╨╨╨╨╨───────────────────────┘
              I = 1A (maximum), Φ = maximum

    The numbers:
    ─────────────────────────────────────────────────────────────────────────
    • Current:           I = Vs/R = 10V/10Ω = 1A
    • Flux:              Φ = L × I = 1 × 1 = 1 Wb (maximum)
    • Load voltage:      V_R = I × R = 1 × 10 = 10V (ALL the source voltage!)
    • Inductor voltage:  V_L = Vs - V_R = 10V - 10V = 0V
    • Rate of change:    dI/dt = 0 (current is constant)
    • Energy stored:     E = ½LI² = ½ × 1 × 1² = 0.5J (in magnetic field)

    WHY is V_L = 0?
    ─────────────────────────────────────────────────────────────────────────
    Current is NOT CHANGING. No change means no changing flux, which means
    no induced EMF. The inductor acts like a plain wire with 0V across it.

    The magnetic field is "full" — holding 0.5 joules of energy.


══════════════════════════════════════════════════════════════════════════════
PHASE 4: BATTERY DISCONNECTED (t = 0⁺ after disconnect)
══════════════════════════════════════════════════════════════════════════════

    NOW THINGS GET INTERESTING.

    You open a switch, removing the battery. What happens?

         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │         V_L                V_R      │
      ╳  │        ??? V              ??? V     │
   (open)│        ║║║║║║                       │
         └────────╨╨╨╨╨╨───────────────────────┘
              I was 1A... what now?

    The magnetic field contains 0.5 joules of energy.
    That energy cannot just disappear!

    What the inductor "wants":
    ─────────────────────────────────────────────────────────────────────────
    • Current was 1A and suddenly has no source
    • Current TRIES to drop to 0 instantly
    • But instant change means dI/dt → -∞
    • Back-EMF = -L × dI/dt → +∞
    • The inductor generates HUGE voltage to keep current flowing!

    What actually happens (with just the load):
    ─────────────────────────────────────────────────────────────────────────
    If the load R is still connected (just battery removed), current flows
    through the load, powered by the collapsing magnetic field.

         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │         V_L                V_R      │
         │        -10V               +10V      │  (signs relative to
         │        ║║║║║║               ↑       │   original current
         │        ║║║║║║               │       │   direction)
         └────────╨╨╨╨╨╨───────┬───────┘
                               │
                          I = 1A (still flowing!)
                          powered by collapsing field

    The inductor has REVERSED its voltage polarity!
    Now it's acting like a SOURCE, pushing current through the load.


══════════════════════════════════════════════════════════════════════════════
PHASE 5: FIELD COLLAPSING (t > 0 after disconnect)
══════════════════════════════════════════════════════════════════════════════

    The magnetic field energy is being converted to heat in the load.

    Just after disconnect:
    ─────────────────────────────────────────────────────────────────────────
    • Current:           I = 1A (can't change instantly)
    • Flux:              Φ = 1 Wb (but starting to collapse)
    • Load voltage:      V_R = I × R = 1 × 10 = 10V
    • Inductor voltage:  V_L = -10V (reversed! now a source)
    • Rate of change:    dI/dt = V_L / L = -10V / 1H = -10 A/s (decreasing)

    The circuit (no battery, just L and R in loop):

         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │   INDUCTOR (source)    LOAD (sink)  │
         │                                     │
         │   V_L = -L(dI/dt)      V_R = IR     │
         │                                     │
         │   ← ← ← ← I ← ← ← ← ← ← ← ← ← ←    │
         └─────────────────────────────────────┘

    KVL: V_L + V_R = 0  (no battery anymore)
         -L(dI/dt) + IR = 0
         dI/dt = -IR/L = -I/τ

    This gives exponential decay: I(t) = I₀ × e^(-t/τ)


    As time passes (field collapsing):
    ─────────────────────────────────────────────────────────────────────────

    t = 0.1s (one time constant):
    • Current:     I = 1A × e^(-1) = 0.37A
    • Flux:        Φ = 0.37 Wb
    • Load voltage: V_R = 3.7V
    • Inductor voltage: V_L = -3.7V
    • Energy remaining: E = ½ × 1 × 0.37² = 0.068J (most dissipated as heat)

    t = 0.5s (five time constants):
    • Current:     I ≈ 0.007A (essentially zero)
    • Flux:        Φ ≈ 0
    • Load voltage: V_R ≈ 0V
    • Inductor voltage: V_L ≈ 0V
    • Energy remaining: ≈ 0J (all dissipated as heat in load)


    WHERE DID THE ENERGY GO?
    ─────────────────────────────────────────────────────────────────────────

    Before disconnect:  E = ½LI² = 0.5J stored in magnetic field

    After collapse:     E = 0J in field

    The energy was converted to HEAT in the resistor:

        E = ∫ I²R dt = ∫ (I₀e^(-t/τ))² R dt = ½LI₀² = 0.5J  ✓

    Energy is conserved. The magnetic field energy became thermal energy.
```

## Summary: The Complete Voltage Story

```
VOLTAGE ACROSS INDUCTOR AND LOAD THROUGH ALL PHASES
══════════════════════════════════════════════════════════════════════════════

    V_L (inductor)                    V_R (load)
    ▲                                 ▲
    │                                 │
 10V│─┐                            10V│            ─────────────┐
    │  ╲                              │       ────              │
    │   ╲                             │    ──                   │
    │    ───                          │  ─                      │
    │       ────                      │─                        │
  0V├──────────────────              0├───────────────────      │
    │              ────               │                   ─     │
    │                  ───            │                    ──   │
    │                     ╲           │                      ───│
-10V│                      ╲─┐        │                         │
    └──┬─────────┬──────────┬──►     └──┬─────────┬──────────┬──►
       │         │          │            │         │          │
    Battery   Steady    Battery       Battery   Steady    Battery
    connected  state   disconnected  connected  state   disconnected

    PHASE 1-2: V_L starts at Vs, decreases to 0 as current builds
               V_R starts at 0, increases to Vs as current builds

    PHASE 3:   V_L = 0 (no change happening)
               V_R = Vs (all voltage across load)

    PHASE 4-5: V_L goes NEGATIVE (inductor becomes source)
               V_R decreases as current decays
               Both approach 0 as field fully collapses


┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  DURING CHARGING:                                                          │
│  • Source provides energy                                                  │
│  • Some energy goes to load (heat)                                        │
│  • Some energy goes to magnetic field (stored)                            │
│  • V_L is POSITIVE (absorbing power from source)                          │
│                                                                            │
│  DURING COLLAPSE:                                                          │
│  • No external source                                                      │
│  • Magnetic field provides energy                                          │
│  • All energy goes to load (heat)                                         │
│  • V_L is NEGATIVE (delivering power to circuit)                          │
│                                                                            │
│  The inductor is like a rechargeable energy reservoir:                    │
│  • Absorbs energy while current increases                                 │
│  • Releases energy while current decreases                                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

</details>

<details>
<summary><strong>The Key Tension</strong> — Self-induction: friend or foe?</summary>

## Self-Induction Creates Both Problems and Solutions

```
THE DUAL NATURE OF SELF-INDUCTION
══════════════════════════════════════════════════════════════════════════════

PROBLEM: You can't switch inductive loads easily
──────────────────────────────────────────────────────────────────────────────

    When you open a switch on an inductive load (motor, relay, solenoid),
    the collapsing field generates voltage spikes that can:

    • Arc across switch contacts (wears them out)
    • Destroy transistors (if using solid-state switching)
    • Create electromagnetic interference (EMI)
    • Damage nearby electronics

    The faster you try to stop the current, the bigger the spike.
    V = L × dI/dt → if dt → 0, then V → ∞


SOLUTION: The same physics enables useful applications
──────────────────────────────────────────────────────────────────────────────

    • SWITCHING POWER SUPPLIES: Inductors store energy during "on" phase,
      release it during "off" phase → efficient voltage conversion

    • SPARK IGNITION: Car ignition coils use self-induction to generate
      40,000V sparks from a 12V battery

    • ENERGY STORAGE: Inductors in power supplies smooth out ripple by
      absorbing and releasing energy each switching cycle

    • CURRENT LIMITING: Inductors prevent current from changing too fast,
      protecting circuits from surge damage
```

</details>

<details>
<summary><strong>Concrete Example</strong> — Why your car needs an ignition coil</summary>

## Ignition Coil: Self-Induction Creates 40,000 Volts

```
HOW A 12V BATTERY CREATES A 40,000V SPARK
══════════════════════════════════════════════════════════════════════════════

    The ignition coil is just an inductor (with a secondary winding).
    Self-induction in the primary creates the high voltage.

    CHARGING PHASE (points closed):
    ─────────────────────────────────────────────────────────────────────────

         12V ────[points]────⊃⊃⊃⊃⊃⊃⊃⊃⊃────┐
                 (closed)   IGNITION COIL  │
                            (L ≈ 5mH)      │
                            ║║║║║║║║║║     │
                            ╨╨╨╨╨╨╨╨╨╨     │
                                           │
         GND ──────────────────────────────┘

         • Current builds up to ~4A over several milliseconds
         • Magnetic field stores energy: E = ½LI² = ½ × 0.005 × 16 = 0.04J
         • This energy will become the spark


    SPARK PHASE (points open):
    ─────────────────────────────────────────────────────────────────────────

         12V ────[points]────⊃⊃⊃⊃⊃⊃⊃⊃⊃────┐
                 (OPEN!)    IGNITION COIL  │
                   ╳        ║║║║║║║║║║     │
                   │        ╨╨╨╨╨╨╨╨╨╨     │
                   │              ⚡        │
                   │        SPARK PLUG     │
         GND ──────┴───────────────────────┘

         • Current TRIES to stop instantly
         • dI/dt = 4A / 0.000001s = 4,000,000 A/s
         • V = L × dI/dt = 0.005 × 4,000,000 = 20,000V (primary)
         • Secondary winding multiplies this to ~40,000V
         • Spark jumps across spark plug gap, igniting fuel

    The 0.04 joules stored in the magnetic field is released in
    microseconds, creating enormous instantaneous power.
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/inductor]]** — Complete treatment of inductors: energy storage, RL time constants, why coils have more inductance than straight wires, and the physics of why current can't change instantly.

- **[[quick-context/lenzs-law]]** — Why the induced EMF always opposes the change: energy conservation requires it. Includes detailed explanation of increasing vs. decreasing flux.

- **[[quick-context/voltage]]** — The electric field perspective on voltage. The back-EMF in an inductor is a real voltage created by the changing magnetic flux.

- **[[quick-context/electromagnetism]]** — The unified picture: changing magnetic fields create electric fields (which is why changing flux induces EMF), and changing electric fields create magnetic fields.

- **[[quick-context/capacitor]]** — The dual of an inductor. Capacitors store energy in electric fields and oppose voltage changes, while inductors store energy in magnetic fields and oppose current changes.

- **[[quick-context/electric-current]]** — Current is the flow of charge. In an inductor, the current creates the magnetic field that stores energy.

- **[[micro-context/buck-converter]]** — Practical application of self-induction: the inductor stores energy when the switch is on and releases it when the switch is off, enabling efficient DC-DC conversion.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Current is flowing steadily through an inductor. Is there any self-induced EMF?
<details>
<summary>Answer</summary>
**No.** Self-induced EMF = L × dI/dt. If current is steady, dI/dt = 0, so EMF = 0. The magnetic flux exists, but it's not changing, so no voltage is induced. The inductor acts like a plain wire. Self-induction only matters when current is *changing*.
</details>

**Q2:** At the instant you connect a battery to an inductor-[[learning/notes/quick-context/resistor|resistor]] circuit, why does the load see 0V even though the battery is 10V?
<details>
<summary>Answer</summary>
**The inductor absorbs all the voltage as back-EMF.** At t=0, current is zero but trying to change rapidly. This rapid change (large dI/dt) creates a large back-EMF (V_L = L × dI/dt = 10V). By KVL, V_R = Vs - V_L = 10V - 10V = 0V. The entire source voltage is "used up" opposing the current change, leaving nothing for the load. As current builds up and dI/dt decreases, V_L drops and V_R rises.
</details>

**Q3:** When you disconnect the battery from an inductor carrying current, the inductor voltage reverses polarity. Why?
<details>
<summary>Answer</summary>
**The inductor switches from absorbing energy to releasing it.** While charging, current was increasing, so the inductor opposed by creating voltage that fought the source (positive V_L, absorbing power). When disconnected, current tries to decrease, so the inductor opposes by creating voltage that *maintains* current flow (negative V_L relative to original, now delivering power). The inductor has become the source, pushing its stored energy through the load.
</details>

**Q4:** An inductor stores 1 joule of energy in its magnetic field. You disconnect it from the source. Where does that 1 joule go?
<details>
<summary>Answer</summary>
**It's converted to heat in whatever the current flows through.** The magnetic field collapses, inducing voltage that drives current through any available path. If a resistor is connected, the current flows through it, dissipating energy as heat (P = I²R). If NO path exists, the inductor generates enough voltage to arc through air or destroy components — the energy still dissipates, just destructively. Energy is always conserved; it transforms from magnetic field energy to thermal energy.
</details>

**Q5:** A coil has inductance L. You wind it with twice as many turns (2N instead of N), keeping everything else the same. How does the self-inductance change?
<details>
<summary>Answer</summary>
**It quadruples (becomes 4L).** Inductance is proportional to N² because: (1) more turns create a stronger magnetic field for the same current, and (2) more turns link with that stronger field. Each turn both contributes to the field and links with flux from all other turns. So doubling turns gives 2× field strength AND 2× flux linkage = 4× total inductance. See [[quick-context/inductor]] for the full explanation of the N² effect.
</details>

</details>
