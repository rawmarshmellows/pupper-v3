---
topic: Oscilloscope and Multimeter
created: 2026-02-06
---

> **Related:** [[quick-context/fundamental-electronic-parts-index|Fundamental Electronic Parts — Index]] | [[quick-context/resistor|Resistor]] | [[quick-context/can-bus|CAN Bus]] | [[quick-context/capacitance|Capacitance]] | [[quick-context/uart|UART — Universal Asynchronous Receiver/Transmitter]]

> **TL;DR:** A multimeter measures [[quick-context/voltage|voltage]], current, and resistance as single numbers (good for DC and slow checks), while an oscilloscope shows how voltage changes over time (essential for debugging signals, timing, noise, and anything that happens faster than your eye can see)—together they are the two fundamental tools for understanding what's actually happening in a circuit.

# Oscilloscope and Multimeter

## The Core Problem: You Can't Debug What You Can't See

A circuit doesn't work. Is the power supply providing 3.3V? Is the clock signal actually toggling? Is there noise on the data line? Is the signal arriving 100 ns too late? Without instruments, you're guessing. A **multimeter** gives you steady-state readings (DC voltage, resistance, continuity). An **oscilloscope** shows you the time-domain waveform—the actual shape of a signal as it changes over nanoseconds to seconds. Most debugging starts with "what voltage is on this pin?" (multimeter) and escalates to "what does the signal look like?" (oscilloscope).

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **DMM (Digital Multimeter)** | Measures V, I, R, continuity, and sometimes [[quick-context/capacitance|capacitance]]/frequency. Displays a single number. Every electronics bench has one. |
| **Oscilloscope** | Displays voltage vs. time on a screen. Shows signal shape, frequency, rise time, noise, glitches. Modern scopes are digital (DSO) with memory and measurement functions. |
| **Probe** | The cable connecting the instrument to the circuit. Oscilloscope probes have a 10:1 divider (10× probe) that reduces loading on the circuit and extends voltage range. |
| **Trigger** | The oscilloscope feature that stabilizes the display by starting each sweep at the same point on the waveform. Without triggering, signals appear to drift across the screen. |
| **Bandwidth** | The maximum frequency an oscilloscope can accurately measure (-3 dB point). A 100 MHz scope can measure signals up to ~100 MHz. Rule of thumb: scope bandwidth should be 5× the signal frequency. |

<details>
<summary><strong>How It Works</strong></summary>

```
MULTIMETER: SINGLE-NUMBER MEASUREMENTS
══════════════════════════════════════════════════════════════════════════════

    VOLTAGE (V):  Place probes across component (in parallel)
    ─────────────────────────────────────────────────────────

        ┌──component──┐
    ────┤             ├────
        │    ┌───┐    │
        └────┤ V ├────┘     DMM shows: 3.31V
             └───┘
             (high impedance: ~10MΩ, draws almost no current)


    CURRENT (A):  Break circuit, insert meter in series
    ─────────────────────────────────────────────────────

    ────┬────── ──┬──component──────
        │         │
        └───┤A├───┘     DMM shows: 47.2 mA
            └─┘
            (low impedance: meter is in the current path)
            WARNING: connecting ammeter in parallel = short circuit = blown fuse


    RESISTANCE (Ω):  Component must be UNPOWERED and DISCONNECTED
    ────────────────────────────────────────────────────────────

    DMM sends a small test current and measures voltage drop.
    R = V/I (Ohm's law internally)

    CONTINUITY: Beeps if resistance < ~50Ω
    The most-used multimeter function: "are these two points connected?"


OSCILLOSCOPE: VOLTAGE vs TIME
══════════════════════════════════════════════════════════════════════════════

    ┌────────────────────────────────────────────────────────────┐
    │      ╱╲      ╱╲      ╱╲      ╱╲      ╱╲      ╱╲           │
    │     ╱  ╲    ╱  ╲    ╱  ╲    ╱  ╲    ╱  ╲    ╱  ╲          │
    │────╱────╲──╱────╲──╱────╲──╱────╲──╱────╲──╱────╲── 0V    │
    │   ╱      ╲╱      ╲╱      ╲╱      ╲╱      ╲╱      ╲        │
    │  ╱                                                 ╲       │
    │                                                            │
    │  Volts/div: 1V     Time/div: 1μs     Trigger: rising, 0V  │
    │  Freq: 500 kHz     Vpp: 3.3V         Rise time: 50ns      │
    └────────────────────────────────────────────────────────────┘

    Key controls:
    • Volts/div: vertical scale (zoom in/out on amplitude)
    • Time/div: horizontal scale (zoom in/out on time)
    • Trigger level: voltage at which scope starts capturing
    • Trigger edge: rising or falling


WHEN TO USE WHICH
══════════════════════════════════════════════════════════════════════════════

    Multimeter                        Oscilloscope
    ──────────                        ────────────
    "Is the power supply 5V?"         "Is the power supply noisy?"
    "Is this wire broken?"            "What does the clock signal look like?"
    "What's the resistance?"          "Is there ringing on this trace?"
    "How much current?"               "Is the I2C timing correct?"
    Static / DC values                Dynamic / time-varying signals
    $20-200                           $300-10,000+


10x PROBE: WHY AND HOW
══════════════════════════════════════════════════════════════════════════════

    1× probe:                    10× probe:
    Everything the scope sees    Divides signal by 10 at the probe tip

    • Full signal amplitude      • 1/10 signal (scope compensates in display)
    • Higher capacitive loading  • 10× less loading on circuit
      (~100 pF)                    (~10-15 pF)
    • Limited bandwidth          • Higher usable bandwidth
    • Disturbs fast signals      • Accurate for fast signals

    Always use 10× for signals faster than ~1 MHz.
    The scope has a "10×" setting that multiplies readings back up.
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Bandwidth vs. Cost, and What You Actually Need

| Bandwidth | Price Range | Good For |
|-----------|-----------|----------|
| 50 MHz | $300-500 | Arduino, slow digital, audio, power supplies |
| 100 MHz | $400-800 | SPI, I2C, [[quick-context/uart|UART]], most embedded work |
| 200 MHz | $800-2000 | Faster SPI, [[quick-context/can-bus|CAN bus]], switching supply debug |
| 500 MHz | $2000-5000 | USB, Ethernet PHY, DDR memory |
| 1+ GHz | $5000-50000 | PCIe, high-speed serial, RF |

Rule of thumb: scope bandwidth should be 5× the highest frequency in your signal. A 3.3V square wave at 10 MHz has significant energy at 50 MHz (5th harmonic), so a 50 MHz scope shows rounded edges. A 100 MHz scope shows it more accurately.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Debugging a Failing I2C Bus

```
SCENARIO: I2C communication between MCU and sensor is intermittent
══════════════════════════════════════════════════════════════════════════════

    Step 1: MULTIMETER CHECK
    ─────────────────────────
    • Is 3.3V present on sensor VCC? → Yes (3.28V)
    • Are pull-up resistors installed? → Continuity from SDA/SCL to 3.3V: beep!
    • Multimeter says everything looks fine. But I2C still fails.

    Step 2: OSCILLOSCOPE REVEALS THE TRUTH
    ──────────────────────────────────────

    SDA line on scope:

    3.3V ─────╲              ╱─────          ╱───
              ╲            ╱              ╱
              ╲     ╱╲   ╱    ← Slow rise time!
              ╲   ╱  ╲ ╱       The signal doesn't reach 3.3V
    0V   ──────╲─╱    ╲╱────── before the next transition

    DIAGNOSIS: Pull-up resistors are too high (100kΩ instead of 4.7kΩ).
    The RC time constant (R_pullup × C_bus) is too long for 400 kHz I2C.

    • Bus capacitance: ~50 pF
    • With 100kΩ: τ = 100k × 50p = 5 μs (way too slow for 2.5μs period)
    • With 4.7kΩ: τ = 4.7k × 50p = 235 ns (fast enough)

    FIX: Replace 100kΩ pull-ups with 4.7kΩ → I2C works perfectly.

    The multimeter showed 3.3V because it measures the AVERAGE.
    The oscilloscope showed the signal never actually reached 3.3V
    during the short high periods.
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/electric-current]]** — Multimeters measure current by inserting a known resistance (shunt) and measuring voltage drop. Understanding I = V/R explains how current measurement works internally.

- **[[quick-context/impedance-and-reactance]]** — Oscilloscope probes have capacitance that loads the circuit. At high frequencies, this loading changes the signal you're trying to measure. The 10× probe reduces this by 10×.

- **[[quick-context/resistor]]** — Multimeter resistance measurement works by injecting a known current and measuring voltage (R = V/I). Always disconnect power before measuring resistance, or you'll get wrong readings.

- **[[quick-context/frequency-and-filtering]]** — Oscilloscope bandwidth is itself a low-pass filter. A 100 MHz scope attenuates signal components above 100 MHz by -3 dB, rounding sharp edges.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** You connect a multimeter set to "amps" in parallel across a component. What happens?
<details>
<summary>Answer</summary>
**You create a near-[[micro-context/short-circuit|short circuit]] and blow the multimeter's fuse (or worse).** An ammeter has very low internal resistance (~0.1Ω) to minimize voltage drop. Connecting it in parallel puts that low resistance across the component, creating a short circuit with potentially very high current. Always connect ammeters in SERIES (break the circuit and insert the meter in the current path).
</details>

**Q2:** A 50 MHz oscilloscope is displaying a 10 MHz square wave that looks like a sine wave. Why?
<details>
<summary>Answer</summary>
**The scope's bandwidth is filtering out the harmonics that make a square wave square.** A square wave is composed of its fundamental frequency plus odd harmonics (3rd, 5th, 7th...). A 10 MHz square wave has significant energy at 30 MHz (3rd harmonic) and 50 MHz (5th harmonic). A 50 MHz scope attenuates the 5th harmonic by -3 dB and higher harmonics even more, rounding the square wave into something approaching a sine wave. A 200 MHz scope would show it properly.
</details>

**Q3:** Why should you use a 10× probe instead of a 1× probe for most measurements?
<details>
<summary>Answer</summary>
**Lower capacitive loading and higher bandwidth.** A 1× probe presents ~100 pF of capacitance to the circuit, which can change the behavior of high-impedance or high-frequency signals. A 10× probe reduces this to ~10-15 pF. The tradeoff is 10× less signal amplitude, but the scope compensates by multiplying the display. Always use 10× for signals above ~1 MHz.
</details>

**Q4:** What does the trigger do on an oscilloscope?
<details>
<summary>Answer</summary>
**It synchronizes the display so the waveform appears stationary.** Without triggering, each sweep starts at an arbitrary point on the waveform, and the signal appears to drift or jump across the screen. The trigger waits for the signal to cross a specified voltage level on a specified edge (rising or falling), then starts the sweep. This ensures every sweep begins at the same phase of the waveform, creating a stable display.
</details>

**Q5:** Your multimeter reads 3.3V on a digital signal pin, but the circuit isn't working. What might be wrong?
<details>
<summary>Answer</summary>
**The multimeter shows the average (DC) value, not what's happening dynamically.** The signal could be oscillating, have slow rise/fall times, excessive noise, glitches, or incorrect timing—none of which a multimeter reveals. An oscilloscope would show the actual waveform in time. Common issues invisible to a multimeter: signal not reaching full logic levels, ringing after edges, noise spikes crossing thresholds, or timing violations between clock and data.
</details>

</details>
