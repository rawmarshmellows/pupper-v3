---
case: AC to DC Power Conversion
components: [diode, capacitor]
created: 2026-02-08
---

# Case: AC to DC Power Conversion

> **Components:** [[quick-context/diode]] | [[quick-context/capacitor]]
> **Micro-context:** [[micro-context/ac-dc-current]] | [[micro-context/diode-rectification]]

> **In brief:** Wall power is [[micro-context/ac-dc-current|AC]] (current alternates direction 60 times per second) but electronics need [[micro-context/ac-dc-current|DC]] (current flows one way, steady). Diodes act as one-way valves to block the "backwards" half of AC ([[micro-context/diode-rectification|rectification]]), then capacitors fill in the gaps to make smooth, steady DC.

## The Situation

Every phone charger, laptop adapter, and power supply does this: converts 120V AC from the wall into smooth DC (like 5V or 12V) that electronics can use. Without this conversion, your devices would flicker on and off 60 times per second.

## The Pieces

**Diode:** A one-way valve for current. Current flows easily in one direction but is blocked in the other. For this use case, what matters is: it only lets current through when the AC is swinging in the "right" direction. [[quick-context/diode|Full treatment →]]

**Capacitor:** A tiny energy reservoir that charges and discharges almost instantly. For this use case, what matters is: it stores charge when voltage is high and releases it when voltage dips. [[quick-context/capacitor|Full treatment →]]

## Step by Step: What Happens

### Step 1: AC Input — Current swings positive and negative

Wall power is AC: voltage swings positive, then negative, then positive again—60 complete cycles per second.

```
    Voltage
        ↑
   +170V ┤     ╱╲          ╱╲          ╱╲
        │    ╱  ╲        ╱  ╲        ╱  ╲
     0V ┼───╱────╲──────╱────╲──────╱────╲───
        │        ╲    ╱      ╲    ╱      ╲
  -170V ┤         ╲╱          ╲╱          ╲
        └─────────────────────────────────────→ time

        ←──── one cycle ────→
              (1/60 second)
```

Electronics can't use this—they need current flowing in one direction.

### Step 2: Rectification — Diodes block the negative half

Pass the AC through a diode. The diode only lets current through when voltage is positive. When voltage swings negative, the diode blocks it.

```
        Diode as one-way valve
        ═══════════════════════

    AC ──────►|────── Output
           (diode)

        ► = easy direction (current flows)
        | = blocked direction (no current)


    After half-wave rectification:

        ↑
   +170V┤     ╱╲                ╱╲                ╱╲
        │    ╱  ╲              ╱  ╲              ╱  ╲
     0V ┼───╱────╲────────────╱────╲────────────╱────╲
        │        (blocked)         (blocked)
        └─────────────────────────────────────────────→

    The negative halves are gone—but now we have gaps!
```

**What's happening inside the diode:** The diode is made of two types of silicon joined together (a PN junction). When voltage pushes current the "right" way, carriers flow across the junction. When voltage reverses, a barrier forms that blocks current. It's not mechanical—it's the physics of how electrons and "holes" move in semiconductors.

### Step 3: Smoothing — Capacitor fills the gaps

Add a capacitor after the diode. When voltage rises, the capacitor charges up (stores energy). When voltage drops (during the gaps), the capacitor discharges into the circuit, filling in the dips.

```
        Circuit with smoothing capacitor
        ═════════════════════════════════

    AC ───►|───┬──── DC Output
               │
              ═╪═ Capacitor
               │
              GND


    Waveform with smoothing:

        ↑
   +170V┤───────────────────────────────────────
        │   ╱‾‾‾‾╲   ╱‾‾‾‾╲   ╱‾‾‾‾╲
        │  ╱      ╲_╱      ╲_╱      ╲_╱   ← small ripple
        │ ╱                                  (capacitor
     0V ┼╱                                    can't fill
        └────────────────────────────────→    100%)

    The capacitor smooths the humps into nearly-steady DC.
    Some "ripple" remains—larger capacitor = less ripple.
```

**What's happening inside the capacitor:** Two metal plates separated by insulator. When voltage rises, electrons pile up on one plate (energy stored in the electric field between plates). When voltage drops, those electrons flow out into the circuit. No chemistry involved—just pure electrical charge storage. This happens in nanoseconds, far faster than any battery.

### Step 4: Full-Wave Rectification — Using both halves (real circuits)

Real power supplies use 4 diodes in a "bridge" configuration to use BOTH halves of AC, not just one. This doubles the frequency of humps, making smoothing easier.

```
        Bridge Rectifier (4 diodes)
        ═══════════════════════════

                    D1          D2
        AC+ ──────►|──┬──►|──────┐
                       │          │
                       └──┬───────┤──── DC+
                          │       │
                       ┌──┴───────┤
                       │          │
        AC- ──────►|──┘──►|──────┘
                    D3          D4


    Full-wave rectified output:

        ↑
   +170V┤  ╱╲    ╱╲    ╱╲    ╱╲    ╱╲    ╱╲
        │ ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲
     0V ┼╱────╲╱────╲╱────╲╱────╲╱────╲╱────╲─
        └────────────────────────────────────→

    No gaps! Both halves are "flipped" to positive.
    Twice as many humps = easier to smooth.
```

## The Result

```
    Complete conversion:

    WALL AC              AFTER DIODES         AFTER CAPACITOR

         ╱╲                 ╱╲  ╱╲              ════════════
        ╱  ╲               ╱  ╲╱  ╲             smooth DC
    ───╱────╲───          ╱────────╲            (small ripple)
           ╲╱            ╱          ╲

    Alternating          All positive          Steady
    positive/negative    (still bumpy)         DC output
```

Smooth DC power ready for electronics.

## Why Each Piece Matters

- **Diodes:** Create the one-way flow. Without them, current would still alternate—just capacitors alone can't fix that.
- **Capacitors:** Fill the gaps. Without them, you'd have pulsing DC that would make electronics flicker or malfunction.

Together they solve two different problems: direction (diodes) and steadiness (capacitors).

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/ac-dc-current]] — What AC and DC mean
- [[micro-context/diode-rectification]] — Ultra-brief definition of rectification

**Full treatment (10 minutes):**
- [[quick-context/diode]] — PN junction physics, forward voltage drop, LEDs, Zeners, Schottky diodes
- [[quick-context/capacitor]] — RC time constants, decoupling, different capacitor types and tradeoffs
