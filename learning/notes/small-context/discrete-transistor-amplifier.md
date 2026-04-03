---
case: Discrete Transistor Amplifier Design
components: [bjt, resistor, op-amp]
created: 2026-03-29
---

# Case: Discrete Transistor Amplifier Design

> **Components:** [[quick-context/bjt]] | [[quick-context/resistor]] | [[quick-context/op-amp]]
> **Micro-context:** [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/thermal-runaway]] | [[micro-context/reverse-and-forward-bias]]

> **In brief:** Before [[quick-context/op-amp|op-amps]] existed as ICs, engineers built amplifiers from individual [[quick-context/bjt|BJTs]] and [[quick-context/resistor|resistors]]. This works, but the gain depends on $\beta$ (which varies transistor-to-transistor and drifts with temperature), making precise amplification difficult. Understanding why shows exactly what op-amps solved.

## The Situation

A temperature sensor outputs 10 mV/°C. Your [[micro-context/adc-analog-to-digital-converter|ADC]] reads 0–3.3V. You need a gain of ~330 to fill the ADC range. With an [[quick-context/op-amp|op-amp]], you'd pick two [[quick-context/resistor|resistors]] and be done. But what if you only have discrete [[quick-context/bjt|BJTs]] and resistors?

## The Pieces

**BJT (Common-Emitter Configuration):** A [[quick-context/bjt|BJT]] in the "active" region amplifies signals: a small change in base voltage produces a large change in collector current. The voltage gain depends on the transistor's internal parameters. [[quick-context/bjt|Full treatment →]]

**Resistors (Biasing Network):** [[quick-context/resistor|Resistors]] set the DC operating point (bias) so the BJT sits in its active region, and define the load that converts current changes into voltage changes. [[quick-context/resistor|Full treatment →]]

## Step by Step: What Happens

### Step 1: A Single Common-Emitter Amplifier

The simplest BJT amplifier: signal goes into the base, amplified signal comes out of the collector.

```
COMMON-EMITTER AMPLIFIER (simplest form)
═══════════════════════════════════════════════════════

              +Vcc (5V)
               │
               ╱╱╱╱ Rc (collector resistor)
               │
               ├──────── Vout
               │
          C ───┘
    Vin ──╱╱╱╱──B    NPN (2N2222)
           Rb   E ───┐
                     │
                    GND

    HOW IT AMPLIFIES:
    ─────────────────
    1. Vin rises slightly → more base current Ib
    2. Ic = β × Ib → collector current rises by β×
    3. More current through Rc → bigger voltage drop
    4. Vout = Vcc - Ic×Rc → Vout drops (inverted)

    Voltage gain ≈ -Rc / re
    where re = Vt / Ic ≈ 26Ω at Ic = 1mA (small-signal emitter resistance)
```

This works — but $r_e$ depends on the bias current $I_C$, which itself depends on $\beta$. So the gain is still $\beta$-dependent indirectly. That's the problem.

### Step 2: Why $\beta$ Ruins Precision

$\beta$ (current gain) is not a design parameter — it's a side effect of manufacturing. It varies wildly:

```
THE β PROBLEM
═══════════════════════════════════════════════════════

    Same part number (2N2222), three transistors from the same bag:

    Transistor A:  β = 120
    Transistor B:  β = 220
    Transistor C:  β = 180

    Same transistor at different temperatures:

    25°C:   β = 180
    50°C:   β = 230     (+28%)
    -10°C:  β = 130     (-28%)

    If your gain formula contains β, your gain shifts
    ±28% just from temperature change — useless for
    precision sensor amplification.

    Target gain = 330 but actual gain = 240–420
    depending on which transistor and what temperature.
```

For the sensor scenario: $\pm 28\%$ gain drift means a reading of 25°C could display as 18–32°C. Unusable.

### Step 3: Emitter Degeneration — Trading Gain for Stability

Adding a [[quick-context/resistor|resistor]] $R_E$ between emitter and ground creates **negative feedback** at the transistor level. This stabilizes the gain but reduces it.

```
WITH EMITTER DEGENERATION RESISTOR
═══════════════════════════════════════════════════════

              +Vcc
               │
               ╱╱╱╱ Rc
               │
               ├──────── Vout
               │
          C ───┘
    Vin ──╱╱╱╱──B    NPN
           Rb   E
                │
               ╱╱╱╱ Re  ← emitter degeneration
                │
               GND

    NEW GAIN FORMULA:

    Without Re:   Gain ≈ -Rc / re             (β-dependent via bias!)
    With Re:      Gain ≈ -Rc / Re             (β drops out!)

    WHY β DISAPPEARS:
    ─────────────────
    If Vin rises → Ic rises → voltage across Re rises
    → emitter voltage rises → Vbe DECREASES → Ic drops back

    The Re resistor fights against gain changes.
    As long as β is "large enough" (>50), the gain
    depends almost entirely on the Rc/Re ratio.

    EXAMPLE:  Rc = 10kΩ, Re = 1kΩ  →  Gain ≈ -10
```

**The tradeoff:** without $R_E$, you could get gain of 300+ (but unstable). With $R_E$, gain is stable but limited to $R_C / R_E$. Getting gain of 330 requires $R_C / R_E = 330$, meaning $R_E$ is tiny — so small it stops providing stability. You need **multiple stages**, each with modest gain, cascaded together.

### Step 4: The Differential Pair — The Core of Every Op-Amp

Two matched BJTs with their emitters tied together. This is the topology that eventually became the input stage of every op-amp IC.

```
DIFFERENTIAL PAIR
═══════════════════════════════════════════════════════

         +Vcc              +Vcc
          │                  │
         ╱╱╱╱ Rc1           ╱╱╱╱ Rc2
          │                  │
          ├── Vout-          ├── Vout+
          │                  │
     C ───┘                  └─── C
     B ──── Q1          Q2 ──── B
     E ───┐                  ┌─── E
          │                  │
          └────────┬─────────┘
                   │
                  ╱╱╱╱ Re (or current source)
                   │
                  GND

    Vout = (Vout+) - (Vout-) ≈ -Rc / Re × (Vin+ - Vin-)

    WHAT THIS BUYS YOU:
    ───────────────────
    • Amplifies the DIFFERENCE between two inputs
    • Temperature drift affects BOTH transistors equally
      → drift cancels out in the difference
    • Power supply noise appears on both sides
      → cancels out (common-mode rejection)
    • β mismatch still matters less because of Re
```

This is better — temperature drift largely cancels. But you still need matched transistors (hard with discretes), multiple gain stages, and careful biasing. A real discrete amplifier for gain-of-330 might need 3–4 stages, each with its own bias network: 20+ components, all hand-tuned.

### Step 5: The Op-Amp — All of This on One Chip

An [[quick-context/op-amp|op-amp]] IC packages a differential pair, multiple gain stages, and output buffer into 8 pins. The internal gain is ~100,000×, and **negative feedback** through external resistors sets the gain precisely.

```
DISCRETE vs. OP-AMP: Same Gain-of-330 Amplifier
═══════════════════════════════════════════════════════

    DISCRETE (3+ stages, ~25 components):

         Vcc    Vcc    Vcc    Vcc
          │      │      │      │
    Sensor→[Bias]→[Stage1]→[Stage2]→[Stage3]→ ADC
          │      │      │      │
         GND    GND    GND    GND

    Each stage: 2 resistor voltage divider for bias
                1 collector resistor
                1 emitter resistor
                1 BJT
                1 coupling capacitor
    Total: ~25 parts, all values interdependent
    Gain drifts ~5-15% over temperature
    Requires hand-trimming

    OP-AMP (2 resistors + 1 IC):

                  Rf = 329kΩ
             ┌───────╱╱╱╱───────┐
             │                   │
         ┌───┤-  ╲               │
         │   │    ╲              │
         │   │     ╲─────────────┴── ADC
         │   │     ╱
  Sensor─┼───┤+  ╱
         │   └──╱
        ╱╱╱╱ Rin = 1kΩ
         │
        GND

    Gain = 1 + Rf/Rin = 1 + 329k/1k = 330
    Accuracy: limited by resistor tolerance (±1%)
    Temperature drift: <0.1% (resistors are stable)
    Total: 3 parts, formula is trivial
```

## The Result

| Property | Discrete BJT | Op-Amp IC |
|----------|-------------|-----------|
| Parts count (gain=330) | ~25 | 3 |
| Gain accuracy | $\pm 15\%$ (β-dependent) | $\pm 1\%$ (resistor-dependent) |
| Temperature drift | $\pm 5$–$15\%$ | $< 0.1\%$ |
| Design time | Hours of calculation | Minutes |
| Gain formula | Depends on β, $r_e$, bias point | $1 + R_F / R_{IN}$ |

The op-amp didn't eliminate the transistors — it hid them inside an IC where they're laser-trimmed, thermally coupled on the same die (so drift cancels), and wrapped in enough internal feedback that the external behavior depends only on the resistor ratio you choose.

## Why Each Piece Matters

- **BJTs:** Provide the fundamental current amplification. Every op-amp contains dozens of them internally — the IC just handles all the ugly biasing for you.
- **Resistors:** In discrete designs, they set bias *and* gain (conflicting jobs). In op-amp designs, they set *only* gain — clean separation of concerns.
- **Negative feedback (via $R_E$ or op-amp feedback):** The universal fix for $\beta$ dependence. $R_E$ does it partially at one stage. An op-amp does it globally with 100,000× excess gain, making the result nearly perfect.

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/adc-analog-to-digital-converter]] — What an ADC does and resolution levels
- [[micro-context/thermal-runaway]] — How temperature creates destructive feedback loops in transistors
- [[micro-context/reverse-and-forward-bias]] — Forward/reverse bias at PN junctions (relevant to BJT biasing)

**Full treatment (10 minutes):**
- [[quick-context/bjt]] — BJT operating regions, NPN/PNP, current gain, switching vs. amplification
- [[quick-context/resistor]] — Ohm's law, tolerance, voltage dividers, power dissipation
- [[quick-context/op-amp]] — Golden rules, inverting/non-inverting amplifiers, GBW, signal conditioning
- [[quick-context/transistor]] — MOSFET operation, the oxide capacitor, digital logic from transistors
