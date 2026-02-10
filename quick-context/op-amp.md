---
topic: Op-Amp (Operational Amplifier)
created: 2026-02-06
---

> **Related:** [[quick-context/transistor]] | [[quick-context/resistor]] | [[quick-context/capacitor]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]

> **TL;DR:** An op-amp is a high-gain differential amplifier IC that, with [[quick-context/resistor|resistor]] feedback networks, becomes a precision building block for amplification, filtering, and signal conditioning—it's the universal analog component, as fundamental to analog circuits as the [[quick-context/transistor|transistor]] is to digital ones.

# Op-Amp (Operational Amplifier)

## The Core Problem: Precise Analog Signal Processing

A sensor outputs 10 mV when it detects something. Your ADC needs 0-3.3V input. You need to amplify the signal exactly 330×, without adding noise or distortion, regardless of what's connected to the output. Doing this with discrete [[quick-context/transistor|transistors]] and [[quick-context/resistor|resistors]] requires careful design and the gain drifts with temperature. An op-amp solves this: it has enormous internal gain (100,000× or more), and by wrapping it in a negative feedback loop with resistors, the gain becomes determined entirely by the resistor ratio—which is stable, predictable, and easy to calculate. Op-amps make analog design almost as straightforward as digital.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Inverting (-) / Non-inverting (+) inputs** | The two inputs. The op-amp amplifies the difference between them: Vout = A × (V+ - V-), where A is the open-loop gain (~100,000). |
| **Open-loop gain (A)** | The raw gain without feedback. Enormous (10⁵) but useless alone—too high, too variable, too sensitive. Feedback tames it into precise, controlled gain. |
| **Negative feedback** | Connecting the output back to the inverting input through a resistor network. This is what makes op-amp circuits predictable. It trades excess gain for stability and precision. |
| **Virtual short** | With negative feedback, the op-amp drives its output to make V+ ≈ V-. The inputs aren't physically connected, but the voltage difference between them is driven to ~0. This simplifies all op-amp circuit analysis. |
| **Rail-to-rail** | An op-amp whose output can swing to within millivolts of its supply voltages. Standard op-amps can only reach within ~1-2V of the rails, wasting headroom. |

<details>
<summary><strong>How It Works</strong></summary>

```
OP-AMP SYMBOL AND PINS
══════════════════════════════════════════════════════════════════════════════

           V+ (positive supply)
            │
            │
    ───┤+   │╲
       │    │ ╲
       │    │  ╲──── Vout
       │    │  ╱
    ───┤-   │ ╱
            │╱
            │
           V- (negative supply or GND)

    Vout = A × (V+ - V-)    where A ≈ 100,000

    • (+) = non-inverting input
    • (-) = inverting input
    • Two supply pins (often omitted from schematics)


THE TWO GOLDEN RULES (with negative feedback)
══════════════════════════════════════════════════════════════════════════════

    Rule 1: No current flows into the inputs
            (input impedance is essentially infinite)

    Rule 2: V+ = V-
            (the op-amp adjusts its output to make this true)

    These two rules let you analyze ANY op-amp circuit with just
    Ohm's law and Kirchhoff's current law. No calculus needed.


INVERTING AMPLIFIER
══════════════════════════════════════════════════════════════════════════════

              Rf (feedback resistor)
         ┌───────╱╱╱╱───────┐
         │                   │
    Vin ─╱╱╱╱─┬─┤-  ╲       │
          Rin │ │    ╲      │
              │ │     ╲─────┴─── Vout
         ┌────┘ │     ╱
         │   ───┤+  ╱
        GND     └──╱

    Analysis using Golden Rules:
    • V- = V+ = 0V  (Rule 2, since V+ is grounded)
    • Current into Rin: I = Vin / Rin  (Rule 1, no current into op-amp)
    • Same current flows through Rf: I = -Vout / Rf
    • Therefore: Vout = -(Rf / Rin) × Vin

    Gain = -Rf / Rin    (negative = inverts the signal)

    Example: Rf = 100kΩ, Rin = 10kΩ → Gain = -10
             Vin = 0.3V → Vout = -3.0V


NON-INVERTING AMPLIFIER
══════════════════════════════════════════════════════════════════════════════

                  Rf
             ┌───────╱╱╱╱───────┐
             │                   │
         ┌───┤-  ╲              │
         │   │    ╲             │
         │   │     ╲────────────┴─── Vout
         │   │     ╱
    Vin ─┼───┤+  ╱
         │   └──╱
         Rg
         │
        GND

    Gain = 1 + (Rf / Rg)     (always ≥ 1, non-inverting)

    Example: Rf = 9kΩ, Rg = 1kΩ → Gain = 10
             Vin = 0.3V → Vout = 3.0V


VOLTAGE FOLLOWER (BUFFER)
══════════════════════════════════════════════════════════════════════════════

              ┌────────────┐
              │            │
    Vin ──────┤+  ╲        │
              │    ╲       │
              │     ╲──────┴─── Vout = Vin
         ┌────┤-    ╱
         │    │   ╱
         │    └──╱
         │       │
         └───────┘  (output connected directly to inverting input)

    Gain = 1  (Vout = Vin exactly)

    Why bother? IMPEDANCE TRANSFORMATION:
    • Input: draws essentially zero current (won't load the source)
    • Output: can drive significant current (low output impedance)

    Perfect for connecting a high-impedance sensor to a low-impedance ADC
    or load without the signal drooping.
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Ideal vs. Real Op-Amp Limitations

```
IDEAL OP-AMP                    REAL OP-AMP
──────────────                  ──────────────
Infinite gain                   Gain = 100k-10M (but rolls off with freq)
Infinite bandwidth              GBW product = 1-100 MHz
Zero input current              Input bias current = pA to μA
Zero offset voltage             Offset = 0.1-10 mV (needs trimming)
Infinite output current         Output limited to 10-50 mA typically
Rail-to-rail output             Often 1-2V from rails
```

| Op-Amp | GBW (MHz) | Input Type | Cost | Best For |
|--------|----------|------------|------|----------|
| **LM741** | 1 | BJT | $0.30 | Learning, non-critical |
| **LM358** | 1 | BJT | $0.20 | Single-supply, cheap |
| **TL072** | 3 | JFET | $0.50 | Audio, low noise |
| **MCP6002** | 1 | CMOS | $0.40 | Low power, rail-to-rail |
| **OPA2134** | 8 | JFET | $3.00 | High-quality audio |
| **AD8605** | 10 | CMOS | $1.50 | Precision, low noise |

**Gain-Bandwidth Product (GBW):** An op-amp with GBW = 1 MHz can amplify at gain=10 up to 100 kHz, gain=100 up to 10 kHz, or gain=1000 up to 1 kHz. Gain × bandwidth = constant.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Signal Conditioning: Sensor to ADC

A temperature sensor outputs 10 mV/°C. At room temperature (25°C), it outputs 250 mV. Your MCU's ADC reads 0-3.3V with 12-bit resolution (0.8 mV/step). To get useful resolution over 0-100°C, you need to amplify and offset the signal.

```
SIGNAL CONDITIONING CHAIN
══════════════════════════════════════════════════════════════════════════════

    Sensor     Buffer      Amplifier       ADC
    (10mV/°C)  (gain=1)    (gain=3.3)      (12-bit)

    0-1000mV → 0-1000mV → 0-3300mV    →  0-4095 counts
    (0-100°C)                (0-3.3V)

                              Rf=23kΩ
                         ┌────╱╱╱╱────┐
              ┌────┐     │             │
    Sensor ───┤+ ╲ ├─────╱╱╱╱──┤-     │    ┌────────┐
              │  ╱─┘     Rin=10kΩ ╲   │    │  MCU   │
              └──┘              ╱──┴───┤───►│  ADC   │
              Buffer        ┌──╱       │    │  Pin   │
              Stage         │          │    └────────┘
                           GND
                        Amplifier
                        Gain = 1 + 23k/10k = 3.3

    Why the buffer?
    • The sensor has high output impedance (10kΩ+)
    • Without the buffer, the amplifier's input resistor
      forms a voltage divider with the sensor, reducing the signal
    • The buffer draws zero current from the sensor,
      then drives the amplifier from its low-impedance output

    Result: 25°C = 250mV × 3.3 = 825mV → ADC reads 1023
            Each ADC count = 0.024°C resolution
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/transistor]]** — Op-amps are built from dozens of transistors internally. Understanding transistor amplification explains how op-amps achieve their high gain.

- **[[quick-context/resistor]]** — Resistor ratios determine op-amp circuit gain. The precision of your gain depends on resistor tolerance, not the op-amp. Use ±1% metal film resistors for ±1% gain accuracy.

- **[[quick-context/capacitor]]** — Adding capacitors to op-amp feedback networks creates active filters (low-pass, high-pass, band-pass) with better performance than passive RC filters.

- **[[quick-context/electric-current]]** — The golden rule "no current into the inputs" means all current through the input resistor must flow through the feedback resistor—this is how you derive gain formulas using Kirchhoff's current law.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** An inverting amplifier has Rin = 10kΩ and Rf = 47kΩ. What is the gain?
<details>
<summary>Answer</summary>
**-4.7.** Gain = -Rf/Rin = -47k/10k = -4.7. A 1V input produces -4.7V output (inverted). The negative sign means the output is inverted relative to the input.
</details>

**Q2:** Why is a voltage follower (gain = 1) useful if it doesn't amplify?
<details>
<summary>Answer</summary>
**Impedance transformation.** The input draws essentially zero current (won't load a delicate sensor), while the output can drive significant current into a low-impedance load. Without the buffer, connecting a high-impedance source to a low-impedance load would create a voltage divider that drops the signal. The buffer isolates them.
</details>

**Q3:** An op-amp has GBW = 10 MHz. What's the maximum frequency at which it can amplify with a gain of 100?
<details>
<summary>Answer</summary>
**100 kHz.** GBW = Gain × Bandwidth. So Bandwidth = GBW / Gain = 10 MHz / 100 = 100 kHz. Above this frequency, the gain drops below 100. At 1 MHz, the gain would be only 10. At 10 MHz, the gain would be 1 (unity).
</details>

**Q4:** What happens if you connect the output to the non-inverting (+) input instead of the inverting (-) input?
<details>
<summary>Answer</summary>
**Positive feedback—the circuit becomes a comparator or oscillator, not an amplifier.** Instead of stabilizing, any small difference between inputs gets amplified and fed back to increase the difference further. The output slams to one supply rail or the other. This is intentionally used in Schmitt triggers and oscillator circuits, but it's a mistake if you wanted linear amplification.
</details>

**Q5:** Why does the gain of an op-amp circuit depend on resistor ratios rather than the op-amp's own gain?
<details>
<summary>Answer</summary>
**Negative feedback.** The open-loop gain is so large (~100,000) that even a tiny difference between V+ and V- produces a huge output. The feedback loop forces V+ ≈ V- by feeding output back to the inverting input. The circuit gain then depends only on how the feedback network divides the output—which is set by resistor ratios. As long as the open-loop gain is much larger than the desired closed-loop gain, the exact op-amp gain doesn't matter.
</details>

</details>
