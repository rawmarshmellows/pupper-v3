---
topic: Op-Amp (Operational Amplifier)
created: 2026-02-06
---

> **Related:** [[learning/notes/micro-context/common-mode-rejection-ratio]] | [[learning/notes/micro-context/current-mirror]] | [[learning/notes/micro-context/input-bias-current]] | [[learning/notes/micro-context/input-common-mode-range]]

> **TL;DR:** An op-amp is a high-gain differential amplifier IC that, with [[quick-context/resistor|resistor]] feedback networks, becomes a precision building block for amplification, filtering, and signal conditioning—it's the universal analog component, as fundamental to analog circuits as the [[quick-context/transistor|transistor]] is to digital ones.

# Op-Amp (Operational Amplifier)

## The Core Problem: Precise Analog Signal Processing

A sensor outputs 10 mV when it detects something. Your [[learning/notes/micro-context/adc-analog-to-digital-converter|ADC]] needs 0-3.3V input. You need to amplify the signal exactly 330×, without adding noise or distortion, regardless of what's connected to the output. Doing this with discrete [[quick-context/transistor|transistors]] and [[quick-context/resistor|resistors]] requires careful design and the gain drifts with temperature. An op-amp solves this: it has enormous internal gain (100,000× or more), and by wrapping it in a negative feedback loop with resistors, the gain becomes determined entirely by the [[learning/notes/quick-context/resistor|resistor]] ratio—which is stable, predictable, and easy to calculate. Op-amps make analog design almost as straightforward as digital. https://www.youtube.com/watch?v=_ZuJgt4NfFI

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
<summary><strong>Op-Amp Math: The Six Analog Computing Circuits</strong></summary>

Op-amps were literally invented for analog computers—"operational" refers to mathematical operations. The op-amp itself never changes—you change the **feedback network** to select the operation:

```
  ┌───────────────┬──────────────────────────┬────────────────────────────┐
  │   Operation   │         Circuit          │          Key Idea          │
  ├───────────────┼──────────────────────────┼────────────────────────────┤
  │ Add           │ Summing amplifier —      │ Currents sum at virtual    │
  │               │ multiple input resistors │ ground node                │
  ├───────────────┼──────────────────────────┼────────────────────────────┤
  │               │ Difference amplifier —   │ Symmetrical resistor       │
  │ Subtract      │ inputs on both terminals │ network cancels            │
  │               │                          │ common-mode                │
  ├───────────────┼──────────────────────────┼────────────────────────────┤
  │ Multiply ×k   │ Inverting amp with       │ Resistor ratio sets        │
  │               │ Rf = k·Rin               │ constant scale factor      │
  ├───────────────┼──────────────────────────┼────────────────────────────┤
  │ Divide ÷k     │ Inverting amp with       │ Same circuit, just         │
  │               │ Rf = Rin/k               │ Rf < Rin                   │
  ├───────────────┼──────────────────────────┼────────────────────────────┤
  │ Differentiate │ Capacitor input,         │ I = C·dV/dt through cap,   │
  │               │ resistor feedback        │ converted to voltage by Rf │
  ├───────────────┼──────────────────────────┼────────────────────────────┤
  │ Integrate     │ Resistor input,          │ Constant current charges   │
  │               │ capacitor feedback       │ cap: V = (1/C)∫I dt       │
  └───────────────┴──────────────────────────┴────────────────────────────┘

  The pattern: same triangle, different feedback.

       Input element        Feedback element       Operation
       ─────────────        ────────────────       ─────────
       Resistor         →   Resistor           =   Scale (×k or ÷k)
       Multiple R's     →   Resistor           =   Add
       R on both +/−    →   R on both +/−      =   Subtract
       Capacitor        →   Resistor           =   Differentiate
       Resistor         →   Capacitor          =   Integrate
```

```
ADDITION — Summing Amplifier
══════════════════════════════════════════════════════════════════════════════

              R1              Rf
    V1 ──────╱╱╱╱──┐    ┌───╱╱╱╱───┐
              R2    │    │          │
    V2 ──────╱╱╱╱──┼────┘          │
              R3    │               │
    V3 ──────╱╱╱╱──┼───┤-  ╲      │
                    │   │    ╲     │
                    │   │     ╲────┴── Vout
                    │   │     ╱
               ┌────┘───┤+  ╱
               │        └──╱
              GND

    Vout = −(Rf/R1 × V1 + Rf/R2 × V2 + Rf/R3 × V3)

    If R1 = R2 = R3 = Rf = R:
        Vout = −(V1 + V2 + V3)

    Why it works:
    • Virtual ground at (−) input (Rule 2: V− = V+ = 0V)
    • Each input drives current I_n = V_n / R_n independently (Rule 1)
    • All currents sum at the node and flow through Rf
    • Rf converts total current back to voltage: Vout = −Rf × ΣI_n

    Example: V1 = 1V, V2 = 2V, V3 = 0.5V, all R = 10kΩ
             Vout = −(1 + 2 + 0.5) = −3.5V


SUBTRACTION — Difference Amplifier
══════════════════════════════════════════════════════════════════════════════

                  R1            R2
    V1 ──────────╱╱╱╱──┬──────╱╱╱╱────┐
                        │               │
                    ┌───┤-   ╲          │
                    │   │     ╲         │
                    │   │      ╲────────┴── Vout
                    │   │      ╱
    V2 ────╱╱╱╱────┼───┤+   ╱
            R1      │   └───╱
                   ╱╱╱╱
                    R2
                    │
                   GND

    Vout = (R2 / R1) × (V2 − V1)

    Why it works:
    • V2 is divided by R1/R2 network to set V+ voltage
    • V1 drives the inverting side through R1 with Rf = R2
    • The symmetry cancels common-mode signals (noise on both lines)
    • With matched resistors, output is purely the difference

    Example: R1 = 10kΩ, R2 = 47kΩ, V1 = 2.0V, V2 = 2.3V
             Vout = (47/10) × (2.3 − 2.0) = 4.7 × 0.3 = 1.41V

    Real-world use: reading differential sensor signals, bridge circuits


MULTIPLICATION — Scaling Amplifier (multiply by constant k)
══════════════════════════════════════════════════════════════════════════════

                  Rf = k × Rin
             ┌───────╱╱╱╱───────┐
             │                   │
    Vin ─╱╱╱╱─┬──┤-  ╲          │
          Rin  │  │    ╲         │
               │  │     ╲───────┴── Vout = −k × Vin
          ┌────┘  │     ╱
          │   ────┤+  ╱
         GND      └──╱

    Vout = −(Rf / Rin) × Vin = −k × Vin

    This is just the inverting amplifier — "multiply" means scaling
    by a fixed constant set by the resistor ratio.

    To multiply by 5:   Rf = 50kΩ, Rin = 10kΩ
    To multiply by 0.5: Rf = 5kΩ,  Rin = 10kΩ  (also divides by 2)

    For non-inverting (positive k):

                      Rf
                 ┌───────╱╱╱╱───────┐
                 │                   │
             ┌───┤-  ╲              │
             │   │    ╲             │
            ╱╱╱╱ │     ╲────────────┴── Vout = (1 + Rf/Rg) × Vin
             Rg  │     ╱
             │   ┤+  ╱
            GND  └──╱
                  │
    Vin ──────────┘

    Gain = 1 + Rf/Rg

    Note: true multiplication of two variable signals (V1 × V2)
    requires a dedicated analog multiplier IC (e.g., AD633) which
    uses a Gilbert cell internally.


DIVISION — Scaling Amplifier (divide by constant k)
══════════════════════════════════════════════════════════════════════════════

                  Rf = Rin / k
             ┌───────╱╱╱╱───────┐
             │                   │
    Vin ─╱╱╱╱─┬──┤-  ╲          │
          Rin  │  │    ╲         │
               │  │     ╲───────┴── Vout = −Vin / k
          ┌────┘  │     ╱
          │   ────┤+  ╱
         GND      └──╱

    Vout = −(Rf / Rin) × Vin = −(1/k) × Vin

    Division by k is multiplication by 1/k — same circuit,
    just make Rf smaller than Rin.

    To divide by 3:  Rin = 30kΩ, Rf = 10kΩ → gain = −1/3
    To divide by 10: Rin = 100kΩ, Rf = 10kΩ → gain = −1/10

    Example: Vin = 9V, Rin = 30kΩ, Rf = 10kΩ
             Vout = −(10/30) × 9 = −3V  (divided by 3)

    Note: true division of two variable signals (V1 / V2)
    can be done by placing a multiplier IC in the feedback loop.


DIFFERENTIATION — Differentiator
══════════════════════════════════════════════════════════════════════════════

               C             Rf
    Vin ──────||──┬─────────╱╱╱╱────┐
                  │                  │
              ┌───┤-  ╲             │
              │   │    ╲            │
              │   │     ╲───────────┴── Vout
              │   │     ╱
              │───┤+  ╱
              │   └──╱
             GND

    Vout = −Rf × C × dVin/dt

    Why it works:
    • Current through capacitor: I = C × dVin/dt
    • Virtual ground at (−): all that current flows through Rf
    • Vout = −I × Rf = −Rf × C × dVin/dt

    Input → Output behavior:
    ┌─────────────────┬──────────────────────────────┐
    │ Vin waveform    │ Vout waveform                │
    ├─────────────────┼──────────────────────────────┤
    │ Ramp (linearly  │ Constant DC (slope = const)  │
    │ increasing)     │                              │
    │ Sine wave       │ Cosine wave (phase-shifted)  │
    │ Square wave     │ Spikes at each edge           │
    │ Constant DC     │ Zero (no change = no output) │
    └─────────────────┴──────────────────────────────┘

    ⚠ Practical issue: high-frequency noise gets amplified
    (derivative of noise = large). Real differentiators add a
    small resistor in series with C to limit high-freq gain.


INTEGRATION — Integrator
══════════════════════════════════════════════════════════════════════════════

                       Cf
               R    ┌───||───┐
    Vin ──────╱╱╱╱──┤         │
                    │         │
                ┌───┤-  ╲    │
                │   │    ╲   │
                │   │     ╲──┴── Vout
                │   │     ╱
                │───┤+  ╱
                │   └──╱
               GND

    Vout = −(1 / RC) × ∫ Vin dt

    Why it works:
    • Current through R: I = Vin / R  (virtual ground at −)
    • That current charges Cf: V_cap = (1/C) × ∫I dt
    • Vout = −V_cap = −(1/RC) × ∫Vin dt

    Input → Output behavior:
    ┌─────────────────┬──────────────────────────────┐
    │ Vin waveform    │ Vout waveform                │
    ├─────────────────┼──────────────────────────────┤
    │ Constant DC     │ Ramp (accumulating over time) │
    │ Square wave     │ Triangle wave                │
    │ Sine wave       │ Negative cosine              │
    │ Spike / impulse │ Step (holds the area)        │
    └─────────────────┴──────────────────────────────┘

    ⚠ Practical issue: any tiny DC offset on Vin accumulates
    forever, saturating the output. Real integrators add a
    large resistor in parallel with Cf to bleed off DC drift.


SUMMARY — Op-Amp as Analog Computer
══════════════════════════════════════════════════════════════════════════════

    ┌──────────────┬────────────────┬───────────────────────────────┐
    │ Operation    │ Feedback       │ Transfer Function             │
    ├──────────────┼────────────────┼───────────────────────────────┤
    │ Add          │ Rf resistor    │ −(Rf/R₁·V₁ + Rf/R₂·V₂ + …) │
    │ Subtract     │ R2 resistor    │ (R₂/R₁)(V₂ − V₁)            │
    │ Multiply ×k  │ Rf = k·Rin     │ −k · Vin                     │
    │ Divide ÷k    │ Rf = Rin/k     │ −Vin / k                     │
    │ Differentiate│ Rf + C input   │ −RC · dVin/dt                 │
    │ Integrate    │ Cf + R input   │ −(1/RC) · ∫Vin dt            │
    └──────────────┴────────────────┴───────────────────────────────┘

    The pattern: the input element sets how current enters,
    the feedback element sets how current becomes output voltage.
    Resistor→Resistor = scale. Capacitor→Resistor = differentiate.
    Resistor→Capacitor = integrate. Multiple resistors = sum.
```

</details>

<details>
<summary><strong>[[learning/notes/quick-context/inside-the-triangle|Inside the Triangle]]: [[learning/notes/quick-context/transistor|Transistor]]-Level Construction</strong></summary>

An op-amp isn't magic—it's ~20 [[quick-context/transistor|transistors]] and a few [[quick-context/resistor|resistors]] on a single chip. Here's the simplified architecture (based on the classic 741):

```
FUNCTIONAL BLOCK DIAGRAM
═══════════════════════════════════════════════════════════════════════════

  V(+) ──►┌──────────────────┐    ┌───────────────┐    ┌──────────────┐
           │  DIFFERENTIAL    │    │   HIGH-GAIN   │    │    OUTPUT    │
           │  INPUT STAGE     ├───►│   AMPLIFIER   ├───►│    STAGE     ├──► Vout
           │                  │    │   STAGE       │    │  (push-pull) │
  V(-) ──►│  (diff pair +    │    │  (CE amp +    │    │              │
           │   current mirror │    │   active      │    │  drives the  │
           │   active load)   │    │   load)       │    │  load        │
           └────────┬─────────┘    │       ║       │    └──────────────┘
                    │              │    Cc ═══     │
                 ┌──┴──┐          │   (Miller     │
                 │TAIL │          │    comp.)     │
                 │CURR.│          └───────────────┘
                 │SRC  │
                 └──┬──┘
                    │
             Rbias ╱╱╱╱ ─── sets all currents in the chip


TRANSISTOR-LEVEL SCHEMATIC (simplified)
═══════════════════════════════════════════════════════════════════════════

  V+ ───┬───────────────────────────────────────────────────────┐
        │                                                       │
        │      ┌── STAGE 1: Differential Pair ──┐               │
        │      │                                │               │
     ┌──┴──┐   │                             ┌──┴──┐         ┌──┴──┐
     │ Q3  │   │◄── bases tied ─────────────►│ Q4  │         │ Q7  │
     │ PNP │   │    (current mirror)         │ PNP │         │ NPN │──┐
     └──┬──┘   │                             └──┬──┘         └──┬──┘  │
        │      │                                │                │     │
        │      │    STAGE 2 ──┐                 │             Cc ═══   ├── Vout
        │      │              │                 │      (30pF)    │     │
     ┌──┴──┐   │           ┌──┴──┐           ┌──┴──┐         ┌──┴──┐  │
V(+)►│ Q1  │   │           │ Q2  │◄── V(-)  │ Q6  │         │ Q8  │  │
     │ NPN │   │           │ NPN │           │ NPN │         │ PNP │──┘
     └──┬──┘   │           └──┬──┘           └──┬──┘         └──┬──┘
        │      └──────────────┤                  │               │
        └──────────┬──────────┘                  │               │
                ┌──┴──┐                          │               │
                │ Q5  ├──╱╱╱╱── V+ (Rbias)      │               │
                │ NPN │  (tail current source)   │               │
                └──┬──┘                          │               │
                   │                             │               │
  V- ──────────────┴─────────────────────────────┴───────────────┘


WHAT EACH STAGE DOES
═══════════════════════════════════════════════════════════════════════════

  Stage           Components             Function                 Gain
  ─────           ──────────             ────────                 ────
  Differential    Q1, Q2 (NPN pair)      Subtracts V(+) − V(-)   ~100×
  Input Pair      Q3, Q4 (PNP current    Current mirror forces
                  mirror, active load)   equal collector currents
                                         → maximizes diff. gain

  Tail Current    Q5 (NPN) +             Sets stable bias         —
  Source          Rbias (resistor)        current for Q1, Q2.
                                         Rejects common-mode
                                         signals (noise on both
                                         inputs equally)

  High-Gain       Q6 (NPN) +             Common-emitter amp       ~1000×
  Amplifier       active load            with enormous voltage
                                         gain at this node

  Compensation    Cc (30 pF capacitor)   Miller effect slows      —
                                         the gain stage rolloff
                                         to prevent oscillation
                                         under feedback

  Output          Q7 (NPN) + Q8 (PNP)   Push-pull: Q7 sources    ~1×
  Stage                                  current, Q8 sinks it.   (current
                                         Low output impedance     gain)

  ───────────────────────────────────────────────────────────────────────
  Total open-loop gain ≈ 100 × 1000 = 100,000  (that's your A ≈ 10⁵)


SIGNAL FLOW THROUGH THE TRANSISTORS
═══════════════════════════════════════════════════════════════════════════

  1. V(+) and V(-) each drive the base of one transistor (Q1, Q2)
  2. Q1 and Q2 share a tail current from Q5:
     if V(+) rises, Q1 steals more current → Q2 gets less
  3. The current mirror (Q3, Q4) copies Q1's collector current
     and forces it into Q4's side, where it fights Q2's current
     → the DIFFERENCE becomes a large voltage swing at Q4's collector
  4. That voltage drives Q6's base → Q6 amplifies it another ~1000×
  5. Cc (compensation cap) tames the gain vs. frequency so the
     whole thing doesn't oscillate when you add negative feedback
  6. Q7/Q8 push-pull output stage buffers the result:
     Q7 (NPN) pushes current to the load, Q8 (PNP) pulls it away
     → low output impedance, can drive real loads


PARTS LIST (simplified 741-style op-amp)
═══════════════════════════════════════════════════════════════════════════

     Component          Count    Role
     ─────────          ─────    ────
     NPN transistors      4      Q1, Q2 (diff pair), Q5 (tail), Q6 (gain)
     PNP transistors      4      Q3, Q4 (mirror), Q7 (output), Q8 (output)
     Resistors            1-3    Bias current setting
     Capacitors           1      Cc — frequency compensation (30 pF)
     ────────────────────────────────────────────────────────────────────
     Total: ~8 transistors + a few passive components
     (Real 741 has ~20 transistors for protection & better biasing)
```

The key insight: the triangle symbol on schematics hides a **feedback amplifier built from the same [[quick-context/transistor|transistors]] and [[quick-context/resistor|resistors]] you already know**. The [[learning/notes/quick-context/differential-pair|differential pair]] subtracts, the [[learning/notes/micro-context/current-mirror|current mirror]] maximizes gain, and the compensation [[quick-context/capacitor|capacitor]] ensures stability. Everything else is bias circuitry and output buffering.

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

A temperature sensor outputs 10 mV/°C. At room temperature (25°C), it outputs 250 mV. Your [[learning/notes/micro-context/microcontroller|MCU]]'s ADC reads 0-3.3V with 12-bit resolution (0.8 mV/step). To get useful resolution over 0-100°C, you need to amplify and offset the signal.

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

- **[[quick-context/differential-pair]]** — The [[quick-context/differential-pair|differential pair]] is the op-amp's input stage. Two matched transistors sharing a [[learning/notes/micro-context/tail-current|tail current]] source convert V(+) - V(-) into a current difference. Understanding the pair explains the golden rules.

- **[[quick-context/high-gain-amplifier-stage]]** — The [[quick-context/high-gain-amplifier-stage|high-gain amplifier stage]] (current mirror active load) is what gives the op-amp its enormous [[learning/notes/micro-context/open-loop-voltage-gain|open-loop gain]]. The compensation [[learning/notes/quick-context/capacitor|capacitor]] at this stage's output node is what makes op-amps stable in feedback—and what makes them slow as comparators.

- **[[quick-context/transistor]]** — Op-amps are built from dozens of transistors internally. Understanding transistor amplification explains how op-amps achieve their high gain.

- **[[quick-context/resistor]]** — Resistor ratios determine op-amp circuit gain. The precision of your gain depends on resistor tolerance, not the op-amp. Use ±1% metal film resistors for ±1% gain accuracy.

- **[[quick-context/capacitor]]** — Adding capacitors to op-amp feedback networks creates active filters (low-pass, high-pass, band-pass) with better performance than passive RC filters.

- **[[quick-context/electric-current]]** — The golden rule "no current into the inputs" means all current through the input resistor must flow through the feedback resistor—this is how you derive gain formulas using Kirchhoff's current law.

- **[[quick-context/pwm-controller-circuit]]** — Inside every [[learning/notes/micro-context/buck-converter|buck converter]] IC, an op-amp serves as the error amplifier in the [[learning/notes/micro-context/pwm-pulse-width-modulation|PWM]] feedback loop — a real-world application of negative feedback where the op-amp compares output [[learning/notes/quick-context/voltage|voltage]] to a reference and adjusts duty cycle.

- **[[quick-context/comparator]]** — A [[learning/notes/quick-context/comparator|comparator]] shares the same differential-pair input stage as an op-amp but is optimized for speed and digital output. Removing the op-amp's negative feedback and compensation capacitor gives you a comparator—intentionally.

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
**[[learning/notes/quick-context/impedance-and-reactance|Impedance]] transformation.** The input draws essentially zero current (won't load a delicate sensor), while the output can drive significant current into a low-impedance load. Without the buffer, connecting a high-impedance source to a low-impedance load would create a [[learning/notes/quick-context/parallel-vs-series-voltage|voltage divider]] that drops the signal. The buffer isolates them.
</details>

**Q3:** An op-amp has GBW = 10 MHz. What's the maximum [[learning/notes/quick-context/frequency-and-filtering|frequency]] at which it can amplify with a gain of 100?
<details>
<summary>Answer</summary>
**100 kHz.** GBW = Gain × Bandwidth. So Bandwidth = GBW / Gain = 10 MHz / 100 = 100 kHz. Above this frequency, the gain drops below 100. At 1 MHz, the gain would be only 10. At 10 MHz, the gain would be 1 (unity).
</details>

**Q4:** What happens if you connect the output to the non-inverting (+) input instead of the inverting (-) input?
<details>
<summary>Answer</summary>
**Positive feedback—the circuit becomes a [[quick-context/comparator|comparator]] or oscillator, not an amplifier.** Instead of stabilizing, any small difference between inputs gets amplified and fed back to increase the difference further. The output slams to one supply rail or the other. This is intentionally used in [[quick-context/comparator|Schmitt triggers]] and oscillator circuits, but it's a mistake if you wanted linear amplification.
</details>

**Q5:** Why does the gain of an op-amp circuit depend on resistor ratios rather than the op-amp's own gain?
<details>
<summary>Answer</summary>
**Negative feedback.** The open-loop gain is so large (~100,000) that even a tiny difference between V+ and V- produces a huge output. The feedback loop forces V+ ≈ V- by feeding output back to the inverting input. The circuit gain then depends only on how the feedback network divides the output—which is set by resistor ratios. As long as the open-loop gain is much larger than the desired closed-loop gain, the exact op-amp gain doesn't matter.
</details>

</details>
