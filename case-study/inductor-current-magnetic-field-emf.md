---
case: Inductor Self-Induction and Energy Storage
components: [inductor, electromagnetism, electric-current]
created: 2026-02-17
---

# Case: Inductor Self-Induction and Energy Storage

> **Components:** [[quick-context/inductor]] | [[quick-context/electromagnetism]] | [[quick-context/electric-current]] | [[quick-context/coil-magnetic-field]]
> **Micro-context:** [[micro-context/electromagnetic-induction]] | [[micro-context/buck-converter]]

> **In brief:** When [[quick-context/electric-current|current]] flows through a coiled wire, it creates a [[quick-context/coil-magnetic-field|magnetic field]] inside the coil. When the current changes, the changing magnetic flux induces an EMF (voltage) that opposes the change—this is [[micro-context/electromagnetic-induction|electromagnetic induction]] applied to the coil itself. When you disconnect the load, the magnetic field doesn't vanish instantly; it collapses and drives current until its stored energy dissipates through resistance.

## The Situation

You have a coil of wire connected to a power source. When you turn on the current, something resists its buildup. When you try to shut off the current, a voltage spike appears. When you disconnect the load entirely, current somehow keeps flowing briefly. What's happening inside the inductor, and why does the magnetic field eventually "die"?

## The Pieces

**Current through wire:** Moving electrons create a magnetic field that circles around the wire. In a coil, these fields from each turn add together inside the coil, creating a concentrated field along the coil's axis. See [[quick-context/coil-magnetic-field]] for the full treatment.

**Magnetic flux (Φ):** The "amount" of magnetic field passing through the coil's cross-section. Flux = B × A (field strength × area). When current changes, B changes, so flux changes.

**Faraday's Law:** A changing magnetic flux through a loop induces a voltage (EMF) around that loop: EMF = -N × dΦ/dt. The minus sign is Lenz's Law—the induced EMF opposes the change that caused it.

**Energy storage:** The magnetic field itself stores energy: E = ½LI². This energy must go somewhere when the field collapses.

## Step by Step: What Happens

### Step 1: Current Starts Flowing (Field Builds Up)

When you first connect a voltage source, current begins to flow through the coil. Each increment of current increases the magnetic field inside:

```
INITIAL STATE: No current, no field
═══════════════════════════════════════════════════════════════════════════════

    Power       Switch
    Supply      (open)         Coil
    ┌───┐         ╱           ╭────────╮
    │ + ├────────○  ○────────⊃⊃⊃⊃⊃⊃⊃⊃⊃├────┐
    │   │                     ╰────────╯    │
    │   │                                   │
    │ − ├───────────────────────────────────┘
    └───┘

    I = 0                     B = 0 (no field inside coil)


SWITCH CLOSES: Current begins to rise
═══════════════════════════════════════════════════════════════════════════════

    ┌───┐                     ╭────────╮
    │ + ├───────────────────⊃⊃⊃⊃⊃⊃⊃⊃⊃├────┐
    │   │          I →        ╰────────╯    │
    │   │          ↑          ║══════════   │
    │ − ├──────────┴──────────╨─────────────┘
    └───┘                     B (building)

    Current starts flowing → magnetic field starts building inside coil
    Each turn adds to the central field (fields align and superimpose)
```

As current increases, the magnetic flux through the coil increases. Faraday's Law says this changing flux induces an EMF:

```
THE INDUCED EMF OPPOSES CURRENT RISE
═══════════════════════════════════════════════════════════════════════════════

    Applied voltage: Vs        Induced EMF: V_L = -L × dI/dt
          │                         │
          ▼                         ▼
    ┌─────┴─────────────────────────┴─────┐
    │                                      │
    │    Vs ──────────→  ←────────── V_L  │
    │    (pushing I up)  (opposing change)│
    │                                      │
    └──────────────────────────────────────┘

    Net effect: Current rises GRADUALLY, not instantly

    • dI/dt is large at first → V_L is large → most of Vs dropped across coil
    • As current approaches final value → dI/dt decreases → V_L decreases
    • At steady state: dI/dt = 0 → V_L = 0 → coil acts like a wire
```

### Step 2: Steady State (Constant Current, Constant Field)

Once the current reaches its final value (determined by V/R of the circuit), it stops changing:

```
STEADY STATE: Constant current, constant field
═══════════════════════════════════════════════════════════════════════════════

    ┌───┐                     ╭────────╮
    │ + ├───────────────────⊃⊃⊃⊃⊃⊃⊃⊃⊃├────┐
    │   │     I (constant)    ╰────────╯    │
    │   │     ═══════════▶    ║══════════   │   ← uniform field inside coil
    │ − ├─────════════════════╨═════════════┘
    └───┘                     B (constant)

    dI/dt = 0  →  V_L = L × dI/dt = 0

    The inductor appears as just its wire resistance (DCR).
    Energy is stored in the magnetic field: E = ½LI²
```

**Magnetic field direction:** Using the right-hand rule, if you curl your fingers in the direction of current flow around the coil, your thumb points in the direction of the magnetic field inside. The field lines form closed loops—they exit one end of the coil (North pole), curve around outside, and re-enter the other end (South pole).

```
FIELD DIRECTION (Right-Hand Rule)
═══════════════════════════════════════════════════════════════════════════════

    Current flow (viewed from right end):

              ↓ (coming down front of coil)
         ┌────┴────┐
        /           \
       │      ⊙      │   ← If current goes counterclockwise (as seen from right),
        \           /        magnetic field points TO THE RIGHT (out of page here)
         └────┬────┘
              ↑ (going up back of coil)

    3D view of field lines:

         Outside: field curves back around
              ╭──────────────────────────╮
             ╱                            ╲
            ╱  ┌──────────────────────┐    ╲
           │   │ ══════════════════▶  │ N   │    Magnetic field lines
           │   │ ══════════════════▶  │     │    form CLOSED LOOPS
           │   │ ══════════════════▶  │     │    (no beginning or end)
            ╲  └──────────────────────┘    ╱
             ╲           S                ╱
              ╰──────────────────────────╯
         Outside: field returns through S pole
```

### Step 3: Current Decreases (Field Collapses, EMF Opposes)

Now suppose you reduce the voltage or add resistance. Current starts to decrease:

```
CURRENT DECREASING: Field collapse induces EMF
═══════════════════════════════════════════════════════════════════════════════

    Before: I = I_max, B = B_max

    ┌───┐                     ╭────────╮
    │ + ├───────────────────⊃⊃⊃⊃⊃⊃⊃⊃⊃├────┐
    │   │     I (decreasing)  ╰────────╯    │
    │   │     ═══════▶        ║══════════   │   ← field collapsing
    │ − ├─────════════════════╨═════════════┘
    └───┘                     B (decreasing)

    dI/dt < 0 (current decreasing)

    V_L = -L × dI/dt = -L × (negative) = POSITIVE

    The induced EMF now ADDS to the current direction!


    Physical interpretation:
    ┌──────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   The magnetic field is collapsing. This changing flux induces an EMF   │
    │   that tries to MAINTAIN the current—opposing the decrease.             │
    │                                                                          │
    │   The collapsing field releases its stored energy by driving current.   │
    │                                                                          │
    └──────────────────────────────────────────────────────────────────────────┘
```

### Step 4: Sudden Disconnection (The Dangerous Case)

What happens if you suddenly open a switch, trying to instantly stop the current?

```
SUDDEN DISCONNECTION: Voltage spike!
═══════════════════════════════════════════════════════════════════════════════

    Before: I = 1A, stored energy E = ½LI²

    ┌───┐       Switch                  ╭────────╮
    │ + ├─────────○/○─────────────────⊃⊃⊃⊃⊃⊃⊃⊃⊃├────┐
    │   │        (opening)              ╰────────╯    │
    │   │                               ║══════════   │
    │ − ├─────────────────────────────────════════════┘
    └───┘

    The switch tries to make dI/dt → -∞ (instant current stop)

    V_L = -L × dI/dt

    If dI/dt → -∞, then V_L → +∞ (huge positive voltage spike!)


    What actually happens:
    ┌──────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    │   1. The inductor generates a voltage spike (can be hundreds of volts)  │
    │   2. This voltage can ARC across the switch contacts                    │
    │   3. The arc provides a path for current to continue briefly            │
    │   4. Energy dissipates as heat/light in the arc                         │
    │   5. Once energy is gone, arc extinguishes, current stops               │
    │                                                                          │
    └──────────────────────────────────────────────────────────────────────────┘

                 VOLTAGE SPIKE
                      │
                      ▼
    V across         ╱╲
    switch          ╱  ╲
                   ╱    ╲
         ────────╱      ╲──────────  ← can be 10-100x the supply voltage
                 │       │
                 │       │
            switch    arc    arc
            opens    forms   dies
```

### Step 5: The Field Dies (Energy Dissipation)

The magnetic field doesn't "die" on its own—the energy stored in it must be converted to another form. Here's how:

```
HOW THE MAGNETIC FIELD "DIES"
═══════════════════════════════════════════════════════════════════════════════

    The field stores energy: E = ½LI²

    This energy cannot vanish—it must go somewhere:


    PATH 1: Dissipation through resistance (normal operation)
    ────────────────────────────────────────────────────────────────────────────

    If there's a closed path with resistance R:

        ┌────────────────────────────────────────┐
        │                                        │
        │     ⊃⊃⊃⊃⊃⊃⊃⊃⊃───────╱╱╱╱╱────────     │
        │         L              R               │
        │                                        │
        └────────────────────────────────────────┘

    The collapsing field drives current through R.
    Current decays exponentially: I(t) = I₀ × e^(-t/τ)  where τ = L/R

    Energy dissipates as heat in the resistor:
    P = I²R → total energy = ∫P dt = ½LI₀² (all the stored energy)


    PATH 2: Arcing (uncontrolled disconnection)
    ────────────────────────────────────────────────────────────────────────────

    The voltage spike ionizes air → arc forms → plasma conducts current
    Energy dissipates as heat and light in the arc
    This damages switch contacts over time


    PATH 3: Flyback/freewheeling diode (controlled dissipation)
    ────────────────────────────────────────────────────────────────────────────

        ┌──────────────▷├────────────────────────┐
        │              Diode                     │
        │     ⊃⊃⊃⊃⊃⊃⊃⊃⊃───────╱╱╱╱╱────────     │
        │         L           Load               │
        │                                        │
        └────────────────────────────────────────┘

    When switch opens:
    • Inductor voltage reverses (trying to maintain current)
    • This forward-biases the diode
    • Current continues through diode + load
    • Energy dissipates safely through load resistance

    This is how [[micro-context/buck-converter|buck converters]] work safely!


    PATH 4: Snubber circuit (RC network absorbs energy)
    ────────────────────────────────────────────────────────────────────────────

    RC network across switch absorbs the spike:
    • Capacitor limits voltage rise rate (dV/dt)
    • Resistor dissipates energy as heat
```

```
EXPONENTIAL DECAY: How current fades
═══════════════════════════════════════════════════════════════════════════════

    With path resistance R and inductance L:

    Time constant: τ = L/R

    I(t) = I₀ × e^(-t/τ)

    I
    ▲
    │
 I₀ ┼───┐
    │   │╲
    │   │  ╲
    │   │    ╲
    │   │      ╲╲
    │   │         ╲╲╲
    │   │             ╲╲╲╲╲──────────
    └───┼───┼───┼───┼───┼───┼────────▶ t
        0   τ  2τ  3τ  4τ  5τ

    At t = τ:  I = 37% of I₀
    At t = 3τ: I ≈ 5% of I₀
    At t = 5τ: I ≈ 0.7% of I₀ (effectively zero)


    Example: L = 100mH, R = 10Ω
    τ = 0.1H / 10Ω = 0.01s = 10ms

    Field is "dead" (< 1% current) after ~50ms
```

## The Result

When you disconnect an inductor:

```
COMPLETE PICTURE: What happens when load disconnects
═══════════════════════════════════════════════════════════════════════════════

    t = 0⁻ (just before disconnect)
    ──────────────────────────────────────────────────────
    • Current I₀ flowing through inductor
    • Magnetic field at full strength: B = μ₀nI₀
    • Energy stored: E = ½LI₀²


    t = 0⁺ (just after disconnect)
    ──────────────────────────────────────────────────────
    • Current CANNOT instantly stop (would require infinite voltage)
    • Inductor generates voltage spike to maintain current
    • Current finds a path: arc, diode, snubber, or parasitic capacitance


    t = several τ (field "dies")
    ──────────────────────────────────────────────────────
    • Current has decayed to near zero
    • Magnetic field has collapsed
    • ALL stored energy has been converted:
      - Heat in resistance
      - Light/heat in arc
      - Or stored briefly in capacitor


    ENERGY ACCOUNTING:
    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │   Energy in magnetic field: E = ½LI²                                  │
    │                                                                        │
    │   This energy CANNOT disappear. It converts to:                       │
    │   • Heat (I²R losses in wire, load, or arc)                           │
    │   • Light (in arc plasma)                                             │
    │   • Electric field energy (if capacitor present)                      │
    │   • Electromagnetic radiation (small amount, especially if fast)      │
    │                                                                        │
    │   Conservation of energy enforces this accounting.                    │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘
```

## Why Each Piece Matters

- **Current → Magnetic field:** Moving charges create magnetic fields. Coiling the wire concentrates and aligns these fields, storing energy in the magnetic field inside the coil.

- **Changing flux → Induced EMF:** Faraday's Law links changing magnetic flux to induced voltage. This is why inductors "resist" current changes—any change in current changes the flux, inducing a voltage that opposes the change.

- **Lenz's Law (the minus sign):** The induced EMF always opposes the change. Current increasing? EMF pushes back. Current decreasing? EMF tries to maintain it. This is nature enforcing energy conservation.

- **Energy must dissipate:** The magnetic field stores real energy (½LI²). When the field collapses, this energy must go somewhere—typically heat in resistance. No resistance = no dissipation = current tries to flow forever (superconductors actually do this).

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/electromagnetic-induction]] — Faraday's Law: changing magnetic flux induces voltage
- [[micro-context/buck-converter]] — Practical application: inductor stores/releases energy in switching power supply

**Full treatment (10 minutes):**
- [[quick-context/inductor]] — Complete inductor physics: L, back-EMF, saturation, applications
- [[quick-context/electromagnetism]] — Maxwell's equations, how E and B fields interact
- [[quick-context/coil-magnetic-field]] — Why coils create magnetic fields, B = μ₀nI derivation
- [[quick-context/electric-current]] — What current actually is, drift velocity, Q = It
- [[quick-context/voltage]] — Electric field as the fundamental driver, EMF as the integral of the field
