---
topic: Resistor
created: 2026-02-06
---

> **Related:** [[micro-context/smd-resistor]]

> **TL;DR:** A resistor opposes the flow of [[quick-context/electric-current|electric current]], converting electrical energy into heat according to Ohm's law (V = IR)—it's the simplest and most ubiquitous electronic component, used to limit current, divide voltages, set bias points, and terminate signals in virtually every circuit ever built.

# Resistor

## The Core Problem: Controlling How Much Current Flows

Imagine connecting an LED directly to a 9V battery. The LED wants about 20 mA at 2V. Without anything limiting the current, the battery pushes as much as it can—hundreds of milliamps—and the LED burns out instantly. You need something that "uses up" the extra 7V and limits current to 20 mA. That's a resistor: it opposes current flow, and the harder current pushes through it, the more [[quick-context/voltage|voltage]] it "drops" across itself. Ohm's law (V = IR) is the single most-used equation in electronics. Every [[quick-context/capacitor|capacitor]] charging circuit, every [[quick-context/transistor|transistor]] bias network, every sensor interface uses resistors. They're the glue that makes all other components work together at the right voltage and current levels.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Resistance (R)** | The opposition to current flow, measured in ohms (Ω). Higher resistance = less current for a given voltage. |
| **Ohm's Law** | V = I × R. The voltage across a resistor equals the current through it times its resistance. The most fundamental equation in electronics. |
| **Power Dissipation** | P = I²R = V²/R = IV. Resistors convert electrical energy to heat. Every resistor has a maximum power rating (commonly 1/8W, 1/4W, 1/2W). Exceed it and the resistor burns. |
| **Tolerance** | How close the actual resistance is to the labeled value. A 1kΩ resistor at ±5% could be 950Ω to 1050Ω. Precision circuits need ±1% or better. |
| **Voltage Divider** | Two resistors in series that split a voltage proportionally: Vout = Vin × R2/(R1+R2). The most common resistor circuit after simple current limiting. |

<details>
<summary><strong>How It Works</strong></summary>

At the atomic level, resistance comes from electrons colliding with atoms as they flow through a material. Metals have lots of free electrons but the atoms still get in the way—each collision transfers energy from the electron to the atom, which vibrates more (heat). Longer, thinner wires have more resistance; shorter, thicker wires have less.

```
OHM'S LAW: THE FOUNDATION
══════════════════════════════════════════════════════════════════════════════

    V = I × R          I = V / R          R = V / I

    ┌──────────────────────────────────────────────────────────────────────┐
    │                                                                      │
    │   Voltage (V)          ┌───────────┐          Current (I)            │
    │   "Pressure"    ──────►│  RESISTOR  │──────►   "Flow"                │
    │   in volts             │    R Ω     │          in amps               │
    │                        └───────────┘                                 │
    │                                                                      │
    │   Higher voltage = more current (for same R)                         │
    │   Higher resistance = less current (for same V)                      │
    │                                                                      │
    └──────────────────────────────────────────────────────────────────────┘

    EXAMPLE: 9V battery, 1kΩ resistor
    I = V/R = 9 / 1000 = 0.009A = 9 mA
    P = V × I = 9 × 0.009 = 0.081W = 81 mW  (well under 1/4W rating)


POWER DISSIPATION
══════════════════════════════════════════════════════════════════════════════

    Three equivalent formulas:

    P = V × I       P = I² × R       P = V² / R

    EXAMPLE: 12V across a 10Ω resistor

    I = 12 / 10 = 1.2A
    P = 12 × 1.2 = 14.4 WATTS  ← A 1/4W resistor would catch fire!


SERIES AND PARALLEL
══════════════════════════════════════════════════════════════════════════════

    SERIES: Resistances ADD
    ───╱╱╱╱───╱╱╱╱───╱╱╱╱───
       R1      R2      R3         R_total = R1 + R2 + R3


    PARALLEL: Reciprocals ADD
       ┌───╱╱╱╱───┐
    ───┤───╱╱╱╱───├───
       └───╱╱╱╱───┘              1/R_total = 1/R1 + 1/R2 + 1/R3
          R1, R2, R3
                                  Two equal R in parallel = R/2


VOLTAGE DIVIDER
══════════════════════════════════════════════════════════════════════════════

    Vin ───╱╱╱╱───┬───╱╱╱╱─── GND
             R1    │    R2
                 [Vout]

    Vout = Vin × R2 / (R1 + R2)

    5V in, R1=R2=10kΩ  →  Vout = 2.5V
    12V in, R1=22kΩ, R2=10kΩ  →  Vout = 3.75V
```

### Resistor Color Code

```
READING COLOR CODES (4-band)
══════════════════════════════════════════════════════════════════════════════

    Color       │ Digit │ Multiplier │ Tolerance
    ────────────┼───────┼────────────┼──────────
    Black       │   0   │  ×1        │
    Brown       │   1   │  ×10       │  ±1%
    Red         │   2   │  ×100      │  ±2%
    Orange      │   3   │  ×1k       │
    Yellow      │   4   │  ×10k      │
    Green       │   5   │  ×100k     │  ±0.5%
    Blue        │   6   │  ×1M       │
    Violet      │   7   │            │
    Grey        │   8   │            │
    White       │   9   │            │
    Gold        │       │  ×0.1      │  ±5%
    Silver      │       │  ×0.01     │  ±10%

    Example: Brown Red Orange Gold = 12 × 1000 = 12kΩ ±5%

    SMD codes: "472" = 47 × 10² = 4.7kΩ
               "1001" = 100 × 10¹ = 1kΩ (4-digit)
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Precision vs. Cost vs. Power vs. Size

| Type | Tolerance | Power | Cost | Best For |
|------|-----------|-------|------|----------|
| **Carbon film** | ±5% | 1/8-1/2W | Lowest | Hobby, general purpose |
| **Metal film** | ±1%, ±0.1% | 1/8-1W | Low | Precision, most production |
| **Wirewound** | ±0.01% | 1-100W+ | High | Power resistors, precision refs |
| **SMD thick film** | ±1-5% | 1/16-1W | Very low | Production PCBs |
| **SMD thin film** | ±0.1% | 1/16-1/4W | Medium | Precision SMD |

```
SIZE VS. POWER RATING
══════════════════════════════════════════════════════════════════════════════

    SMD Package    Size (mm)      Max Power
    ───────────    ────────────   ─────────
    0201           0.6 × 0.3     1/20 W      ← needs microscope
    0402           1.0 × 0.5     1/16 W
    0603           1.6 × 0.8     1/10 W
    0805           2.0 × 1.25    1/8 W       ← hand-solderable
    1206           3.2 × 1.6     1/4 W
    Through-hole   ~6 × 2        1/4 - 2W    ← prototyping

    Smaller = less surface area = less heat escape = lower power rating
```

### E-Series: Why Resistor Values Seem Weird

Values like 4.7kΩ and 2.2kΩ come from the E12/E24 series—logarithmically spaced so every possible resistance falls within tolerance of at least one standard value:

```
    E12 series (per decade): 10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82
    Then × 10: 100, 120, 150...    × 100: 1k, 1.2k, 1.5k...
```

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Pull-Up Resistors: Making Digital Signals Reliable

Every [[micro-context/i2c|I2C]] bus, every button input, every open-drain output needs pull-up resistors. Without them, the signal floats at an undefined voltage and [[quick-context/transistor|transistor]] inputs reading it go haywire.

```
THE PROBLEM: FLOATING INPUTS
══════════════════════════════════════════════════════════════════════════════

    WITHOUT PULL-UP:                    WITH PULL-UP:

    3.3V                                3.3V ──╱╱╱╱──┬─── MCU reads HIGH
                                               10kΩ   │
    Button ──┤ ├──── MCU Pin            Button ──┤ ├──┘
                      │                               │
    GND               [???]             GND ──────────┘   MCU reads LOW
                   random garbage!                        when pressed


I2C BUS PULL-UPS
══════════════════════════════════════════════════════════════════════════════

    3.3V ──┬──╱╱╱╱──┬──╱╱╱╱──┐
           │  4.7kΩ  │  4.7kΩ  │
           │   SDA   │   SCL   │
     ┌─────┴──┐            ┌───┴──────┐
     │ Master │            │ Sensor   │
     │ (MCU)  │            │ (Slave)  │
     └────────┘            └──────────┘

    Why 4.7kΩ?
    • Too low (1kΩ): wastes power, devices can't pull line LOW
    • Too high (100kΩ): RC time constant too slow for bus speed
    • 4.7kΩ: sweet spot for 100-400 kHz I2C
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/electric-current]]** — Ohm's law (V = IR) is the direct relationship between resistance and current. Understanding current flow is prerequisite to understanding resistors.

- **[[quick-context/voltage-current-causality]]** — V = IR is a *constraint*, not a causal arrow. Whether voltage causes current or current causes voltage depends on what's driving the circuit (voltage source vs. current source).

- **[[quick-context/capacitor]]** — Resistors and capacitors form RC circuits: the most common filter and timing element. The time constant tau = RC governs charging, discharging, and frequency response.

- **[[quick-context/parallel-vs-series-voltage]]** — Series resistors divide voltage; parallel resistors divide current. Same Kirchhoff's laws that govern transistor power delivery.

- **[[quick-context/transistor]]** — Resistors set bias points for transistors, limit base/gate current, and form loads in amplifier circuits.

- **[[quick-context/thermal-noise-electronics]]** — Every resistor generates thermal noise: V_noise = sqrt(4kTRB). Higher resistance = more noise, setting fundamental limits on sensitive analog circuits.

- **[[learning/notes/small-context/pull-up-pull-down-resistors]]** — How a single resistor plus a button turns a floating GPIO into a deterministic digital input. Walks through pull-up vs pull-down and how to pick the resistor value.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** You have a 5V supply and an LED that needs 20 mA at 2V forward drop. What resistor value do you need?
<details>
<summary>Answer</summary>
**150Ω.** The resistor must drop 5V - 2V = 3V. R = V/I = 3V / 0.020A = 150Ω. Power: P = 3V × 20mA = 60 mW—well within a 1/8W rating.
</details>

**Q2:** Two 10kΩ resistors in series? In parallel?
<details>
<summary>Answer</summary>
**Series: 20kΩ. Parallel: 5kΩ.** Series adds directly. Parallel: (10k × 10k)/(10k + 10k) = 5kΩ. Parallel is always less than the smallest individual resistor.
</details>

**Q3:** What resistor values create a voltage divider that converts 12V to ~3.3V?
<details>
<summary>Answer</summary>
**R1 = 27kΩ, R2 = 10kΩ → Vout = 3.24V.** Need R1/R2 = (12-3.3)/3.3 ≈ 2.64. With R2 = 10kΩ, R1 = 26.4kΩ. Nearest standard value is 27kΩ, giving 3.24V.
</details>

**Q4:** A resistor is marked Brown, Black, Red, Gold. What is its value?
<details>
<summary>Answer</summary>
**1kΩ ±5%.** Brown=1, Black=0, Red=×100, Gold=±5%. So 10 × 100 = 1000Ω = 1kΩ.
</details>

**Q5:** Why can't you use a very high-value pull-up resistor (e.g., 10MΩ) on a digital input?
<details>
<summary>Answer</summary>
**The RC time constant becomes too large.** Every wire has parasitic [[quick-context/capacitance|capacitance]]. With 10MΩ and even 10 pF of stray capacitance, tau = 10M × 10p = 100 μs. The signal would take hundreds of microseconds to rise, far too slow for any reasonable digital communication. Also, the tiny current (0.33 μA at 3.3V) would be overwhelmed by leakage currents and noise.
</details>

</details>
