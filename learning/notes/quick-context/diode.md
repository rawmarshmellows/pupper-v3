---
topic: Diode
created: 2026-02-06
updated: 2026-02-25
---

> **Related:** [[quick-context/doped-silicon]] | [[quick-context/transistor]] | [[quick-context/electric-current]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]

> **TL;DR:** A diode is a one-way valve for [[quick-context/electric-current|electric current]]—built from a PN junction in [[quick-context/doped-silicon|doped silicon]], it conducts in one direction (with a ~0.7V drop) and blocks in the other, enabling AC-to-DC conversion, [[quick-context/voltage|voltage]] protection, and light emission (LEDs).

# Diode

## Human notes

The collapsing [[quick-context/inductor|inductor]] field pulls the switch node below GND — the inductor generates a voltage fighting the current decrease ([[quick-context/self-induction|self-induction]]). This is what forward-biases the freewheeling [[quick-context/diode|diode]] in a [[micro-context/buck-converter|buck converter]]: the [[micro-context/cathode|cathode]] (at the switch node) drops below the [[micro-context/anode|anode]] (at GND), so the diode conducts and provides the return path for the inductor current. This "freewheeling" use case is one of the most important diode applications in switching power supplies — the diode exists specifically to give the inductor somewhere to push current when the [[micro-context/mosfet|MOSFET]] turns off.

## The Core Problem: Making Current Flow Only One Way

Wall outlets provide AC power that alternates direction 50-60 times per second, but every electronic device needs DC (current flowing in one direction). The diode solves this: it conducts current in one direction and blocks it in the other. This simple behavior enables rectifiers that convert AC to DC, protection circuits that prevent reverse-polarity damage, and LEDs that convert current to light. Diodes are the simplest semiconductor device—just a single PN junction—making them the gateway to understanding how [[quick-context/transistor|transistors]] work (a transistor is essentially two PN junctions back-to-back).

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **PN Junction** | The boundary where P-type silicon (holes) meets N-type silicon (electrons). A depletion zone forms at the boundary, creating a natural barrier to current flow. |
| **Forward Bias** | Applying voltage in the "easy" direction (positive to P-side, negative to N-side). Overcomes the depletion zone; current flows. Requires ~0.7V for silicon, ~0.3V for Schottky, ~2V for LEDs. |
| **Reverse Bias** | Applying voltage in the "blocking" direction. Widens the depletion zone; essentially no current flows (only tiny leakage). |
| **Forward Voltage Drop (Vf)** | The voltage "consumed" by the diode when conducting. Always present—a silicon diode always drops ~0.7V regardless of current (within limits). |
| **Breakdown Voltage** | The reverse voltage at which the diode can no longer block current and conducts in reverse. Destructive for normal diodes; intentionally exploited in Zener diodes for voltage regulation. |

<details>
<summary><strong>How It Works</strong></summary>

A diode is a piece of silicon with one half [[quick-context/doped-silicon|doped]] P-type (excess holes) and the other half N-type (excess electrons). At the junction, electrons and holes recombine, creating a depletion zone—a region with no free carriers that acts as an insulating barrier.

```
PN JUNCTION AND DEPLETION ZONE
══════════════════════════════════════════════════════════════════════════════

    P-TYPE              │         N-TYPE
    (excess holes ⊕)    │         (excess electrons ⊖)
                        │
    ⊕ ⊕ ⊕ ⊕ ⊕ ⊕   ░░░░░░░░░░   ⊖ ⊖ ⊖ ⊖ ⊖ ⊖
    ⊕ ⊕ ⊕ ⊕ ⊕ ⊕   ░░░░░░░░░░   ⊖ ⊖ ⊖ ⊖ ⊖ ⊖
    ⊕ ⊕ ⊕ ⊕ ⊕ ⊕   ░░░░░░░░░░   ⊖ ⊖ ⊖ ⊖ ⊖ ⊖
                    ^^^^^^^^^^^^
                    Depletion zone
                    (no free carriers)
                    Built-in voltage ~0.7V


FORWARD BIAS: Current flows
══════════════════════════════════════════════════════════════════════════════

    (+) ──── P │░░│ N ──── (-)
              ←narrowed→
              depletion zone

    • External voltage pushes holes toward junction from P-side
    • External voltage pushes electrons toward junction from N-side
    • Depletion zone narrows and collapses → current flows
    • Requires ~0.7V to overcome the built-in barrier (silicon)


REVERSE BIAS: No current
══════════════════════════════════════════════════════════════════════════════

    (-) ──── P │░░░░░░░░░░│ N ──── (+)
              ←──── widened ────→
                depletion zone

    • External voltage pulls holes AWAY from junction
    • External voltage pulls electrons AWAY from junction
    • Depletion zone widens → no current flows (only nanoamps of leakage)
    • Until breakdown voltage is reached → catastrophic reverse conduction


DIODE I-V CURVE
══════════════════════════════════════════════════════════════════════════════

    Current (I)
        ▲
        │              ╱
        │             ╱    Forward: exponential rise
        │            ╱     after ~0.7V threshold
        │           ╱
        │         ╱
    ────┼────────╱────────────── Voltage (V)
        │       0.7V
   ─────┤
   Break│←── Reverse: tiny leakage until
   down │     breakdown voltage (destructive
        │     for normal diodes)
        │


HOW LEDs WORK
══════════════════════════════════════════════════════════════════════════════

    Same PN junction, but made from special semiconductors
    (GaAs, GaN, InGaN) instead of pure silicon:

    electron ⊖ ──→ recombines with hole ⊕ ──→ releases PHOTON (light)

    The semiconductor's band gap energy determines the color:
    • Red: GaAsP (Vf ≈ 1.8V)     • Low energy photon
    • Green: GaP (Vf ≈ 2.1V)     • Medium energy
    • Blue: GaN (Vf ≈ 3.0V)      • High energy photon
    • White: Blue LED + phosphor coating

    Silicon diodes also release energy during recombination,
    but as heat (infrared) instead of visible light.
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Speed vs. Forward Drop vs. Current Capacity

| Type | Vf | Speed | Max Current | Best For |
|------|-----|-------|------------|----------|
| **Silicon rectifier (1N400x)** | 0.7-1.1V | Slow (μs) | 1-50A | Power supply rectification |
| **Schottky** | 0.15-0.45V | Very fast (ns) | 1-30A | Switching power supplies, OR-ing |
| **Zener** | Specified reverse breakdown | N/A | mA-A | Voltage references, clamping |
| **LED** | 1.8-3.3V (color-dependent) | Fast (ns) | 20 mA typical | Indicators, lighting |
| **TVS (Transient Voltage Suppressor)** | High | Very fast (ps) | High (surge) | ESD and surge protection |
| **[[quick-context/camera-fundamentals|Photodiode]]** | ~0.5V | Very fast (ns) | μA (generated) | Light detection, [[quick-context/camera-fundamentals|image sensors]], solar cells |

```
THE FORWARD DROP TRADEOFF
══════════════════════════════════════════════════════════════════════════════

    Silicon rectifier: Vf = 0.7V, cheap, robust, slow
                       At 10A: wastes 7W as heat!

    Schottky:          Vf = 0.3V, faster, lower loss, costs more
                       At 10A: wastes only 3W

    In a 5V/10A power supply, the diode choice determines
    whether you waste 6% or 14% of your total power budget
    just in the rectifier diode.
```

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Full-Wave Bridge Rectifier: AC to DC

The most common diode application—four diodes converting AC (from a wall transformer) to pulsating DC, which a [[quick-context/capacitor|capacitor]] then smooths.

```
BRIDGE RECTIFIER CIRCUIT
══════════════════════════════════════════════════════════════════════════════

    AC Input         Bridge           Smoothing        DC Output
    (transformer)    Rectifier        Capacitor

                    D1    D2
      ~  ───────┬──►├──┬──►├──┬──────┬──────────── (+) DC out
                │       │       │      │
                │       │       │     ═╪═ C
                │       │       │      │
      ~  ───────┼──►├──┘──►├──┘      │
                │  D3       D4        │
                │                      │
                └──────────────────────┴──── (-) DC out


    POSITIVE HALF CYCLE:                NEGATIVE HALF CYCLE:
    AC top is (+)                       AC top is (-)

    (+)──→──D1──→──(+out)              (+out)──→──D2──→──(+)
               │                                  │
            (load)                              (load)
               │                                  │
    (-)──←──D4──←──(-out)              (-out)──←──D3──←──(-)

    Current flows through the load in the SAME direction
    during both halves of the AC cycle!


    OUTPUT WAVEFORM
    ═══════════════

    AC Input (alternates positive and negative):
         ╱╲      ╱╲      ╱╲
        ╱  ╲    ╱  ╲    ╱  ╲
    ───╱────╲──╱────╲──╱────╲─── ← zero line
              ╲╱      ╲╱      ╲╱
               (negative half)

    After bridge (full-wave rectified):
       ╱╲    ╱╲    ╱╲    ╱╲    ╱╲
      ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲
    ─╱────╲╱────╲╱────╲╱────╲╱────╲─ ← all above zero

    After smoothing capacitor:
    ────────────────────────────── ← nearly flat DC
       ~~~ (small ripple) ~~~

    The capacitor fills in the valleys between the humps,
    providing near-constant DC voltage to the load.
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/doped-silicon]]** — The PN junction that makes diodes work is created by doping silicon with different impurities on each side. Understanding N-type and P-type silicon explains why diodes conduct in only one direction.

- **[[quick-context/transistor]]** — A MOSFET contains a built-in "body diode." A [[quick-context/bjt|BJT]] is essentially two PN junctions. Understanding diodes is prerequisite to understanding transistors.

- **[[quick-context/electric-current]]** — Diodes control current direction. The forward voltage drop means diodes always consume some power (P = Vf × I).

- **[[quick-context/ac-to-dc-rectification|AC-to-DC Rectification]]** — The full story: AC from the grid, forward/reverse bias, half-wave vs full-bridge rectification, smoothing capacitors, and the complete conversion chain inside every power supply.

- **[[quick-context/capacitor]]** — After rectification, capacitors smooth the pulsating DC into steady DC. The ripple voltage depends on [[quick-context/capacitance|capacitance]], load current, and frequency.

- **[[quick-context/resistor]]** — LEDs always need a current-limiting resistor (R = (Vsupply - Vf) / I_desired). Without one, the LED draws too much current and burns out.

- **[[quick-context/inductor]] / [[micro-context/buck-converter|Buck Converter]]** — Freewheeling (flyback) diodes provide a current path for inductors when a switch opens. The inductor's [[quick-context/self-induction|self-induction]] pulls the switch node below GND, forward-biasing the diode. This is why every buck converter needs a diode (or synchronous MOSFET) — without it, the inductor's voltage spike destroys the switch.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does a silicon diode always drop ~0.7V when conducting, regardless of the current?
<details>
<summary>Answer</summary>
**The 0.7V is the built-in potential of the PN junction.** It's the voltage needed to overcome the depletion zone's electric field and push carriers across the junction. The I-V curve is exponential (Shockley equation), so voltage changes very slowly with current—from ~0.6V at low current to ~0.8V at high current. It's approximately constant, not exactly.
</details>

**Q2:** What's the advantage of a Schottky diode over a standard silicon diode?
<details>
<summary>Answer</summary>
**Lower forward voltage (~0.3V vs ~0.7V) and faster switching.** Schottky diodes use a metal-semiconductor junction instead of a PN junction, so there's no minority carrier storage and no reverse recovery time. This makes them ideal for switching power supplies where efficiency and speed matter. The tradeoff: higher reverse leakage current and lower breakdown voltage.
</details>

**Q3:** A Zener diode is rated at 5.1V. How is it used differently from a normal diode?
<details>
<summary>Answer</summary>
**It's operated in reverse bias, intentionally at its breakdown voltage.** Normal diodes are destroyed by reverse breakdown. Zener diodes are designed to break down at a precise, repeatable voltage. Connected in reverse with a series resistor from a higher voltage, the Zener clamps the output to its rated voltage (5.1V), acting as a simple voltage regulator or reference.
</details>

**Q4:** Why does an LED need a current-limiting resistor but a regular diode in a rectifier doesn't?
<details>
<summary>Answer</summary>
**In a rectifier, the load itself limits the current.** The load resistance determines how much current flows. An LED has very low dynamic resistance once conducting—without an external resistor, the current is limited only by the source's ability to deliver it, which is usually far more than the 20 mA an LED can handle. The resistor acts as the current-controlling element: R = (Vsupply - Vf_LED) / I_desired.
</details>

**Q5:** In a [[micro-context/buck-converter|buck converter]], the MOSFET turns off and the inductor's current must keep flowing. Why does the freewheeling diode conduct, and what would happen without it?
<details>
<summary>Answer</summary>
**The inductor's collapsing magnetic field pulls the switch node voltage below GND.** An [[quick-context/inductor|inductor]] resists changes in current ([[quick-context/self-induction|self-induction]]) — when the MOSFET opens, the inductor generates whatever voltage is needed to keep current flowing. The switch node drops below GND by ~0.7V, forward-biasing the diode (cathode at the switch node is now more negative than the anode at GND). Current flows: GND → anode → cathode → inductor → load → GND. Without the diode, the inductor's voltage spike would have no safe path — the switch node voltage would shoot to hundreds of volts, destroying the MOSFET. The freewheeling diode is there to protect the circuit by absorbing the inductor's stored energy.
</details>

</details>
