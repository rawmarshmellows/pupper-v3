---
topic: Impedance and Reactance
created: 2026-02-06
---

> **Related:** [[quick-context/capacitor]] | [[quick-context/inductor]] | [[quick-context/resistor]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]

> **TL;DR:** Impedance extends the concept of [[quick-context/resistor|resistance]] to AC circuits—[[quick-context/capacitor|capacitors]] and [[quick-context/inductor|inductors]] oppose current flow in a frequency-dependent way called reactance, and impedance (Z = R + jX) combines resistance and reactance into a single quantity that describes how any component behaves with AC signals.

# Impedance and Reactance

## The Core Problem: Resistance Alone Can't Describe AC Behavior

Ohm's law (V = IR) works perfectly for resistors with DC. But connect a [[quick-context/capacitor|capacitor]] to an AC signal and something strange happens: it passes high-frequency signals easily but blocks low-frequency signals. An [[quick-context/inductor|inductor]] does the opposite. Neither behaves like a simple resistance—their opposition to current depends on frequency. Impedance is the generalized version of resistance that accounts for this frequency dependence and the fact that voltage and current can be out of phase. Without impedance, you can't design filters, understand signal integrity, or debug transmission line problems.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Impedance (Z)** | The total opposition to AC current flow, measured in ohms. Z = R + jX, where R is resistance and X is reactance. It's the AC generalization of resistance. |
| **Reactance (X)** | The frequency-dependent opposition to current from capacitors or inductors. Unlike resistance, reactance doesn't dissipate energy—it stores and returns it. |
| **Capacitive Reactance (Xc)** | Xc = 1/(2πfC). Decreases with frequency—[[quick-context/capacitance|capacitance]] causes capacitors to pass high frequencies and block low frequencies. |
| **Inductive Reactance (XL)** | XL = 2πfL. Increases with frequency—inductors pass low frequencies and block high frequencies. |
| **Phase Angle** | The time shift between voltage and current waveforms. In a [[learning/notes/quick-context/capacitor|capacitor]], current leads voltage by 90°. In an [[learning/notes/quick-context/inductor|inductor]], voltage leads current by 90°. In a [[learning/notes/quick-context/resistor|resistor]], they're in phase (0°). |

<details>
<summary><strong>How It Works</strong></summary>

```
WHY VOLTAGE AND CURRENT GET OUT OF PHASE
══════════════════════════════════════════════════════════════════════════════

    RESISTOR: V and I are in phase (0° shift)
    ─────────────────────────────────────────

         ╱╲      ╱╲                Voltage and current
    V ──╱──╲────╱──╲────           rise and fall together
           ╲  ╱    ╲  ╱            P = V × I (always positive = heat)
    I ──────╲╱──────╲╱──


    CAPACITOR: Current LEADS voltage by 90° (remember: ICE)
    ────────────────────────────────────────────────────────

          ╱╲      ╱╲               Current peaks BEFORE voltage
    I ───╱──╲────╱──╲────          Because I = C × dV/dt
            ╲  ╱    ╲  ╱           (current depends on voltage CHANGE)
    ─────────╲╱──────╲╱──
               ╱╲      ╱╲
    V ────────╱──╲────╱──╲─        Voltage lags by 90° (1/4 cycle)
                 ╲  ╱    ╲  ╱
    ──────────────╲╱──────╲╱

    When voltage is changing fastest (zero crossing) → max current
    When voltage is at its peak (not changing) → zero current


    INDUCTOR: Voltage LEADS current by 90° (remember: ELI)
    ────────────────────────────────────────────────────────

          ╱╲      ╱╲               Voltage peaks BEFORE current
    V ───╱──╲────╱──╲────          Because V = L × dI/dt
            ╲  ╱    ╲  ╱           (voltage depends on current CHANGE)
    ─────────╲╱──────╲╱──
               ╱╲      ╱╲
    I ────────╱──╲────╱──╲─        Current lags by 90° (1/4 cycle)
                 ╲  ╱    ╲  ╱
    ──────────────╲╱──────╲╱

    Mnemonic: ELI the ICE man
    E leads I in L (inductor)
    I leads E in C (capacitor)


IMPEDANCE AS A COMPLEX NUMBER
══════════════════════════════════════════════════════════════════════════════

    Z = R + jX     (j = imaginary unit, √(-1))

    Magnitude: |Z| = √(R² + X²)     (in ohms)
    Phase:     θ = arctan(X/R)       (in degrees)

    For a series R-C circuit:
    Z = R + 1/(jωC) = R - j/(ωC)

    For a series R-L circuit:
    Z = R + jωL


FREQUENCY DEPENDENCE: THE KEY INSIGHT
══════════════════════════════════════════════════════════════════════════════

    Xc = 1/(2πfC)                    XL = 2πfL

    Xc (Ω)                           XL (Ω)
     ▲                                ▲
     │╲                               │         ╱
     │ ╲                              │        ╱
     │  ╲                             │       ╱
     │   ╲                            │      ╱
     │    ╲───                        │    ╱
     │        ────────                │  ╱
     └──────────────────► f           └╱─────────────► f

    Capacitor: LOW impedance          Inductor: HIGH impedance
    at high frequency                 at high frequency
    → passes HF signals              → blocks HF signals

    EXAMPLE: 100nF capacitor
    At 100 Hz:  Xc = 1/(2π×100×100×10⁻⁹) = 15,900Ω (blocks)
    At 10 kHz:  Xc = 1/(2π×10k×100n) = 159Ω (moderate)
    At 1 MHz:   Xc = 1/(2π×1M×100n) = 1.6Ω (passes easily)

    This is why capacitors work as decoupling: low impedance
    at high frequencies shorts noise to ground.
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Impedance Matching

When a signal travels through a cable or PCB trace, reflections occur at any point where impedance changes. Maximizing power transfer or minimizing reflections requires matching impedances.

```
WHY 50Ω AND 75Ω?
══════════════════════════════════════════════════════════════════════════════

    50Ω = standard for RF, test equipment, antennas
           (optimizes power handling for coaxial cables)

    75Ω = standard for video, cable TV, broadcast
           (optimizes low-loss signal transmission)

    100Ω = standard for differential digital signals
           (Ethernet, USB, HDMI use 90-100Ω differential pairs)

    Impedance mismatch → signal reflections → ringing, overshoot,
    data errors. This is why high-speed PCB design is obsessed with
    controlled-impedance traces.
```

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## RC Low-Pass Filter

The simplest and most common filter: a [[quick-context/resistor|resistor]] and [[quick-context/capacitor|capacitor]] that passes low frequencies and attenuates high frequencies.

```
RC LOW-PASS FILTER
══════════════════════════════════════════════════════════════════════════════

    Vin ───╱╱╱╱───┬─── Vout
             R     │
                  ═╪═ C
                   │
                  GND

    Cutoff frequency: fc = 1 / (2π × R × C)

    Example: R = 10kΩ, C = 100nF
    fc = 1 / (2π × 10000 × 0.0000001) = 159 Hz

    FREQUENCY RESPONSE (Bode plot)
    ────────────────────────────────

    Gain (dB)
     0 ─────────╲
                  ╲
    -3 ──────────╳╲──── fc (cutoff, -3dB = half power)
                    ╲
    -20 ─────────────╲──── -20 dB/decade slope
                      ╲
    -40 ───────────────╲
                        ╲
    └──────┬──────┬──────┬──► f (log scale)
          fc    10fc   100fc

    Below fc: signal passes unchanged
    At fc: signal attenuated to 70.7% (-3dB)
    Above fc: signal drops 20dB per decade (÷10 per 10× frequency)

    HOW IT WORKS:
    • At low frequency: Xc is huge → capacitor is open circuit → Vout ≈ Vin
    • At high frequency: Xc is tiny → capacitor is short circuit → Vout ≈ 0
    • At fc: Xc = R → voltage divides equally → Vout = 0.707 × Vin
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/capacitor]]** — Capacitive reactance (Xc = 1/2πfC) explains why decoupling capacitors work: they have very low impedance at high frequencies, shorting noise to ground while leaving DC unaffected. See also [[quick-context/capacitance]] for how parasitic [[learning/notes/quick-context/capacitance|capacitance]] affects impedance in PCB traces and IC packages.

- **[[quick-context/inductor]]** — Inductive reactance (XL = 2πfL) explains why inductors are used in power supply filters: they have high impedance at switching frequencies, blocking ripple while passing DC.

- **[[quick-context/resistor]]** — Resistance is the real (non-frequency-dependent) part of impedance. A pure resistor has Z = R at all frequencies with zero phase shift.

- **[[quick-context/pcb-printed-circuit-board]]** — At high frequencies, PCB traces behave as transmission lines with characteristic impedance. Controlled-impedance routing (50Ω, 100Ω differential) is essential for signal integrity.

- **[[quick-context/thermal-noise-electronics]]** — Noise power is proportional to bandwidth. Filters reduce noise by limiting bandwidth—understanding impedance is essential for noise analysis.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A 1μF capacitor is in an AC circuit at 1 kHz. What is its reactance?
<details>
<summary>Answer</summary>
**159Ω.** Xc = 1/(2πfC) = 1/(2π × 1000 × 1×10⁻⁶) = 159Ω. At 10 kHz, it would be 15.9Ω. At 100 Hz, it would be 1590Ω. The reactance scales inversely with frequency.
</details>

**Q2:** Why does "ELI the ICE man" help remember phase relationships?
<details>
<summary>Answer</summary>
**ELI: in an inductor (L), voltage (E) leads current (I). ICE: in a capacitor (C), current (I) leads voltage (E).** This comes directly from the fundamental equations: V = L×dI/dt means voltage is proportional to the rate of current change (peaks earlier), and I = C×dV/dt means current is proportional to the rate of voltage change (peaks earlier).
</details>

**Q3:** A series circuit has R = 100Ω and Xc = 100Ω. What is the magnitude of the total impedance?
<details>
<summary>Answer</summary>
**141Ω.** |Z| = √(R² + Xc²) = √(100² + 100²) = √20000 = 141Ω. Note this is NOT simply 200Ω—because resistance and reactance are at 90° to each other, you must use the Pythagorean theorem. The phase angle is arctan(-100/100) = -45°.
</details>

**Q4:** Why do high-speed digital PCBs need "controlled impedance" traces?
<details>
<summary>Answer</summary>
**At high frequencies, PCB traces act as transmission lines.** If the trace impedance doesn't match the driver and receiver impedance, signals reflect back and forth, causing ringing, overshoot, and data errors. A 1 GHz signal has wavelengths comparable to PCB trace lengths (~15 cm), so wave effects dominate. Matching impedances (typically 50Ω single-ended or 100Ω differential) eliminates reflections.
</details>

**Q5:** A [[learning/notes/micro-context/decoupling-capacitor|decoupling capacitor]] has 1.6Ω of reactance at 1 MHz. Is it doing its job?
<details>
<summary>Answer</summary>
**Yes—1.6Ω is low enough to effectively short high-frequency noise to ground.** The power supply rail typically has much higher source impedance at 1 MHz (tens of ohms from trace inductance), so the capacitor provides a much easier path for high-frequency currents. The lower the impedance at the frequency of interest, the better the decoupling. However, every real capacitor also has parasitic inductance (ESL) that increases impedance above its self-resonant frequency.
</details>

</details>
