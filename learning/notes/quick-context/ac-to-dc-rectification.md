---
topic: AC-to-DC Rectification
created: 2026-03-29
---

# AC-to-DC Rectification

> **Related:** [[micro-context/diode-rectification]]

> **TL;DR:** The power grid delivers AC because transformers make it efficient to transmit, but electronics need DC -- so every power supply uses diodes (one-way valves built from PN junctions) to rectify AC into DC, then smoothing capacitors to flatten the ripple into steady voltage.

## The Core Problem

Wall outlets deliver AC that swings positive and negative 50-60 times per second, but every chip, LED, and motor controller needs DC flowing in one constant direction. Converting AC to DC requires a component that acts as a one-way valve -- the [[quick-context/diode|diode]]. The full conversion chain (transformer, rectifier, filter, regulator) is inside every phone charger, laptop brick, and power supply on earth.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **AC (Alternating Current)** | Current that reverses direction periodically (sinusoidal, typically 50-60 Hz). The grid uses AC because transformers can step [[quick-context/voltage|voltage]] up for efficient long-distance transmission and down for safe household use. |
| **DC (Direct Current)** | Current that flows in one constant direction. Batteries produce DC; electronics require DC internally. |
| **Forward Bias** | Applying positive [[quick-context/voltage|voltage]] to the P-side and negative to the N-side of a PN junction. Shrinks the depletion zone and lets current flow, with a ~0.7V drop for silicon diodes. |
| **Reverse Bias** | Applying voltage in the blocking direction (positive to N-side). Widens the depletion zone and blocks current until breakdown voltage is reached. |
| **Ripple Voltage** | The residual AC variation on top of the DC output after rectification and filtering. Determined by [[quick-context/capacitance|capacitance]], load current, and rectification frequency (RC time constant). |

<details>
<summary><strong>How It Works</strong></summary>

### Step 1: AC from the Grid

AC is produced by rotating a coil in a magnetic field (generator), naturally creating a sinusoidal voltage. Transformers -- which only work with AC -- step voltage up for efficient long-distance transmission (less I^2*R loss) and down for safe household use. This is why AC won the "war of currents."

```
AC from the wall (e.g. 120V, 60 Hz):

  V ▲  /\      /\      /\
  + │ /  \    /  \    /  \
  0─┼/────\──/────\──/────\──► t
  - │      \/      \/      \/

  Swings positive and negative 60 times/second
```

### Step 2: The PN Junction -- Forward and Reverse Bias

A [[quick-context/diode|diode]] is a PN junction: P-type silicon (excess holes) meets N-type (excess electrons). A depletion zone forms at the boundary with a built-in field of ~0.7V.

```
Forward bias: current flows           Reverse bias: current blocked

  (+)── P │░│ N ──(-)                 (-)── P │░░░░░░░░│ N ──(+)
         ←─→                                 ←────────→
       narrow                               widened
    depletion zone                       depletion zone

  Voltage pushes carriers              Voltage pulls carriers
  TOWARD junction → collapse           AWAY from junction → barrier grows
  → current flows (Vf ≈ 0.7V Si)      → no current (until breakdown)
```

This one-way behavior is what makes rectification possible.

### Step 3: Half-Wave Rectification (Single Diode)

The simplest rectifier: one diode passes only the positive half of AC and blocks the negative half.

```
AC input               After single diode

    /\      /\           /\      /\
   /  \    /  \         /  \    /  \
──/────\──/────\──    ─/────────/────────
        \/      \/
                        Negative half is gone (wasted)
                        Output is pulsating, with big gaps
```

Simple but wasteful -- you throw away half the power.

### Step 4: Full-Bridge Rectification (Four Diodes)

Four diodes arranged in a diamond steer current through the load in the same direction during BOTH halves of AC. No wasted energy.

```
THE BRIDGE (diamond shape):

                (+) OUTPUT
                    │
               ┌────┴────┐
               │         │
            ──▶|D1    D2|▶──
           │                 │
      AC ~~●                 ●~~ AC
           │                 │
            ──▶|D3    D4|▶──
               │         │
               └────┬────┘
                    │
                (−) OUTPUT


WHEN AC SWINGS + ON LEFT:        WHEN AC SWINGS − ON LEFT:

    (+)             (−)              (−)             (+)
     ●               ●                ●               ●
     │               │                │               │
     └──▶D1    D4▶───┘                └──▶D2    D3▶───┘
           ↓    ↑                           ↓    ↑
          LOAD                             LOAD
         (+ to −)                         (+ to −)

     ════════════                    ════════════
     SAME DIRECTION THROUGH LOAD BOTH TIMES!
```

Two diodes always conduct at once, so the output is ~1.4V below the AC peak (2 x 0.7V silicon drop). This is why Schottky bridges (lower Vf) are used in low-voltage supplies.

```
After bridge (full-wave rectified):
   ╱╲    ╱╲    ╱╲    ╱╲    ╱╲
  ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲  ╱  ╲
─╱────╲╱────╲╱────╲╱────╲╱────╲─ ← all above zero now

Both halves contribute → double the ripple frequency vs half-wave
```

### Step 5: Smoothing Capacitor -- From Pulsating to Steady DC

A [[quick-context/capacitor|capacitor]] charges during the voltage peaks and discharges through the load during the dips, filling in the valleys.

```
After bridge (bumpy):            + Capacitor (smooth):
   ╱╲    ╱╲    ╱╲
  ╱  ╲  ╱  ╲  ╱  ╲              ════════════════════════
─╱────╲╱────╲╱────╲─               ~~~ (small ripple) ~~~

 still pulsating                  nearly flat DC output
```

The RC time constant (R_load x C) determines how much ripple remains. Bigger [[quick-context/capacitor|capacitor]] or lighter load = smoother DC. Full-wave rectification helps too -- the capacitor only has to bridge half the gap compared to half-wave.

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Efficiency vs. Simplicity vs. Cost

| Approach | Diodes | Pros | Cons |
|----------|--------|------|------|
| **Half-wave** | 1 | Simplest, cheapest | Wastes 50% of AC, more ripple, larger cap needed |
| **Full-bridge** | 4 | Uses both halves, less ripple, smaller cap | 1.4V total drop (2 diodes always in series), more components |
| **Synchronous rectification** | 0 (MOSFETs) | Lowest loss (~50mV drop), highest efficiency | Complex gate drive, expensive, used in modern switch-mode supplies |

The 1.4V drop matters most at low voltages. Rectifying 120V AC? The 1.4V is negligible (1.2%). Rectifying 5V AC for USB? That 1.4V is a 28% loss -- this is why modern USB chargers use switch-mode topologies with synchronous rectification instead of simple bridge rectifiers.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## A USB Phone Charger: Wall to 5V DC

Every phone charger performs this exact conversion chain:

```
120V AC   →   Transformer   →   Bridge    →   Filter   →   Voltage    →   5V DC
wall          (step down        Rectifier      Cap          Regulator      to phone
outlet         to ~7V AC)       (4 diodes)     (smooth)     (steady 5V)
```

1. **120V AC from the wall** -- alternating 60 times/second
2. **Transformer steps down** to ~7V AC (modern chargers use high-frequency switching instead)
3. **Bridge rectifier** flips both halves positive: ~7V pulsating DC, minus 1.4V diode drop = ~5.6V pulsating
4. **Filter capacitor** smooths the pulses into ~5.6V with small ripple
5. **Voltage regulator** (linear or switching) locks the output at exactly 5.0V

**The one thing most outsiders get wrong about this is...** that a "DC adapter" does not just magically change AC to DC. There is real power lost in every stage -- especially the diode drops. Two silicon diodes always in the current path means 1.4V gone as heat before you even start regulating. This is why cheap chargers get warm and why the industry moved to switch-mode power supplies with synchronous rectification (MOSFETs replacing diodes) for better efficiency.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

### Source Micro-Contexts (Glossary Stubs)

- **[[micro-context/ac-dc-current|AC vs DC Current]]** -- Why the grid uses AC (transformers), why electronics need DC, the war of currents.
- **[[micro-context/reverse-and-forward-bias|Reverse and Forward Bias]]** -- PN junction mechanics, depletion zone, forward bias (0.7V), reverse bias, breakdown voltage.
- **[[micro-context/diode-rectification|Diode Rectification]]** -- Half-wave rectification with a single diode, smoothing capacitor basics.
- **[[micro-context/full-bridge-rectifier|Full-Wave Bridge Rectifier]]** -- Four-diode diamond bridge, both halves used, 1.4V total drop, Schottky bridges for low-voltage.

### Related Quick-Contexts

- **[[quick-context/diode]]** -- The component itself: PN junction types, forward voltage drop, Schottky vs silicon, LEDs, Zener, freewheeling diodes.
- **[[quick-context/capacitor]]** -- Smoothing capacitors fill the ripple dips; RC time constant determines ripple voltage.
- **[[quick-context/electric-current]]** -- Fundamental concept: what current is, conventional vs electron flow.
- **[[quick-context/inductor]]** -- Transformers (coupled inductors) are why AC exists on the grid in the first place.
- **[[quick-context/voltage]]** -- Voltage drops across diodes, transformer voltage ratios, why stepping voltage up reduces transmission losses.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does the power grid use AC instead of DC?
<details>
<summary>Answer</summary>
Transformers only work with AC, and transformers allow stepping voltage up for efficient long-distance transmission (high voltage = lower current = less I^2*R loss in the wires) and back down for safe household use. DC could not be efficiently voltage-converted until modern power electronics.
</details>

**Q2:** A silicon diode is forward-biased. What voltage does it drop, and why is this approximately constant regardless of current?
<details>
<summary>Answer</summary>
~0.7V. This is the built-in potential of the PN junction's depletion zone. The I-V curve is exponential (Shockley equation), meaning voltage changes very slowly as current increases -- from ~0.6V at low current to ~0.8V at high current. It appears approximately constant over a wide operating range.
</details>

**Q3:** Half-wave rectification uses one diode. Why is full-bridge (four diodes) worth the extra complexity?
<details>
<summary>Answer</summary>
Half-wave throws away the entire negative half of AC, wasting 50% of the available power and producing large gaps the smoothing capacitor must fill. Full-bridge uses both halves, doubling the ripple frequency (easier to filter), requiring a smaller capacitor for the same ripple, and delivering more average power to the load.
</details>

**Q4:** A full-bridge rectifier outputs ~1.4V less than the AC peak. Where does this voltage go?
<details>
<summary>Answer</summary>
Two diodes are always in the current path (one on each side of the bridge). Each silicon diode drops ~0.7V, so 2 x 0.7V = 1.4V is lost as heat in the diodes. This is why low-voltage supplies use Schottky diodes (~0.3V each, 0.6V total drop) or synchronous rectification with MOSFETs (~50mV drop).
</details>

**Q5:** You have a full-bridge rectifier feeding a smoothing capacitor. The load draws more current. What happens to the DC output quality, and why?
<details>
<summary>Answer</summary>
The ripple voltage increases. Higher load current discharges the capacitor faster between rectified peaks, so the voltage droops more before the next peak recharges it. The ripple is approximately V_ripple = I_load / (f * C), where f is the ripple frequency (2x line frequency for full-wave) and C is the [[quick-context/capacitance|capacitance]]. To reduce ripple under heavier load, you need a larger capacitor.
</details>

</details>

---
> **Human notes:**
> - ElectroBOOM explains the full-bridge rectifier really well: https://www.youtube.com/watch?v=Fwj_d3uO5g8
