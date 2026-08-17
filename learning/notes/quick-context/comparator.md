---
topic: Comparator
created: 2026-04-01
---

# Comparator

> **Related:** [[quick-context/differential-pair]] | [[quick-context/high-gain-amplifier-stage]] | [[quick-context/inside-the-triangle|All Stages Together]] | [[quick-context/op-amp]] | [[quick-context/transistor]] | [[quick-context/pwm-controller-circuit]] | [[quick-context/comparator-specification|Datasheet Specs]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]

> **TL;DR:** A comparator is a circuit that takes two analog voltages as input and outputs a digital HIGH or LOW depending on which input is larger---it's the bridge between the analog and digital worlds, built from the same [[quick-context/transistor|transistor]] differential pairs as an [[quick-context/op-amp|op-amp]] but optimized for speed and clean digital output rather than linear amplification.

## The Core Problem: Making a Yes/No Decision from Analog Voltages

A battery monitor needs to answer a simple question: "Is the battery [[learning/notes/quick-context/voltage|voltage]] above 3.0V or below?" A thermostat needs to know: "Is the temperature above the setpoint?" A [[quick-context/pwm-controller-circuit|PWM controller]] needs to determine, every nanosecond: "Is the error signal above or below the sawtooth ramp?" These are all binary decisions made from continuous analog signals. You need a circuit that cleanly converts "voltage A is greater than voltage B" into a crisp digital 1 or 0---with no in-between, no ambiguity, and ideally no delay. That circuit is a comparator.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Non-inverting (+) / Inverting (-) inputs** | The two input pins. Output goes HIGH when V(+) > V(-), LOW when V(+) < V(-). Same pin naming as an op-amp, but no feedback loop. |
| **Propagation delay ($t_{pd}$)** | The time from when the input crosses the threshold until the output changes state. Fast comparators achieve 1--10 ns; general-purpose ones are 200--500 ns. |
| **Hysteresis** | A deliberate voltage gap between the rising and falling thresholds (e.g., trip HIGH at 3.0V, trip LOW at 2.9V). Prevents rapid oscillation ("chatter") when the input hovers near the threshold. Created by positive feedback. |
| **Open-drain / open-collector output** | Many comparators have an output that can only pull LOW (sink current to ground). A pull-up resistor provides the HIGH level. This lets you wire-OR multiple comparators and interface to any voltage logic level. |
| **Reference voltage ($V_{REF}$)** | The fixed voltage applied to one input, against which the signal is compared. Can come from a voltage divider, a bandgap reference IC, or a precision voltage source. |

<details>
<summary><strong>How It Works</strong> --- From transistor pairs to digital output</summary>

### The Functional View: What a Comparator Does

A comparator is the simplest possible analog-to-digital converter: 1-bit resolution, no clock needed, continuous output.

```
COMPARATOR FUNCTION
==============================================================================

                V(+) ───┤+  ╲
                        │    ╲
                        │     ╲──── Vout
                        │     ╱
                V(-) ───┤-  ╱
                        │  ╱

    If V(+) > V(-):  Vout = HIGH  (Vdd or open-drain pulled up)
    If V(+) < V(-):  Vout = LOW   (Vss or 0V)

    Same triangle symbol as an op-amp, but:
    • No feedback resistor (operates open-loop)
    • Output is digital (slams to rail), not analog
    • Optimized for speed, not gain precision


TRANSFER CHARACTERISTIC (Comparator vs Op-Amp)
==============================================================================

    Op-amp (with feedback):              Comparator (no feedback):

    Vout                                 Vout
    ▲                                    ▲
    │            ╱                        │         ┌──────── HIGH
    │         ╱                           │         │
    │      ╱     LINEAR                   │         │
    │   ╱        REGION                   │         │  NO linear
    │╱                                    │         │  region
    └──────────────────► Vdiff            └─────────┴────────► Vdiff
                                                    0
                                              V(+) - V(-)

    Op-amp + feedback: smooth, proportional    Comparator: binary snap
    output that tracks input linearly          HIGH or LOW, nothing between
```

### The Two Inputs: Non-Inverting (+) and Inverting (−)

Every comparator has exactly two analog inputs, and their names describe how each one steers the output. The **non-inverting input** `V(+)` pushes the output the *same* direction it moves; the **inverting input** `V(−)` pushes it the *opposite* direction.

```
THE TWO INPUTS AND HOW THEY STEER THE OUTPUT
==============================================================================

    NON-INVERTING INPUT   V(+) ───┤+  ╲
                                  │    ╲
                                  │     ╲──── Vout
                                  │     ╱
    INVERTING INPUT       V(-) ───┤-  ╱
                                  │  ╱

    Decision rule:   Vout = HIGH   when  V(+) > V(-)
                     Vout = LOW    when  V(+) < V(-)

    NON-INVERTING (+):  output moves the SAME way as this input.
                        Push V(+) up → output heads toward HIGH.

    INVERTING (-):      output moves the OPPOSITE way.
                        Push V(-) up → output heads toward LOW.

    Only the SIGN of V(+) - V(-) matters, never the size. 1 mV past
    the crossover gives the same full HIGH/LOW as 1 V past it.
```

Which pin gets the **signal** and which gets the **reference** is a free design choice---and swapping them flips the output logic. Put the reference on the inverting input and the comparator answers "is the signal *above* the reference?" (output HIGH = yes). Put the reference on the non-inverting input instead and you get the inverted question: "is the signal *below* the reference?"

**Real pinout --- TI LMC7211-N** (a tiny CMOS rail-to-rail comparator). The two inputs carry exactly these names on the physical package:

```
LMC7211-N PIN ASSIGNMENTS (same die, two packages)
==============================================================================

    8-Pin SOIC-8                       5-Pin SOT23-5
    ─────────────                      ──────────────
    Pin 1   NC                         Pin 1   OUTPUT
    Pin 2   INVERTING INPUT (-)        Pin 2   V+   (positive supply)
    Pin 3   NON-INVERTING INPUT (+)    Pin 3   NON-INVERTING INPUT (+)
    Pin 4   V-   (negative supply)     Pin 4   INVERTING INPUT (-)
    Pin 5   NC                         Pin 5   V-   (negative supply)
    Pin 6   OUTPUT
    Pin 7   V+   (positive supply)
    Pin 8   NC
```

See [[quick-context/comparator-specification]] for how to read this part's full datasheet---supply range, input offset, propagation delay, and the rest.

### How It's Built Inside: The Transistor-Level Circuit

A comparator IC contains three main stages, all built from [[quick-context/transistor|transistors]]:

```
INTERNAL BLOCK DIAGRAM
==============================================================================

    V(+) ──┐     ┌─────────────┐     ┌───────────────┐     ┌──────────┐
           ├────►│ DIFFERENTIAL ├────►│  HIGH-GAIN     ├────►│  OUTPUT  ├──► Vout
    V(-) ──┘     │    PAIR      │     │  AMPLIFIER     │     │  STAGE   │
                 └─────────────┘     └───────────────┘     └──────────┘
                      ▲                     ▲                    ▲
                      │                     │                    │
                 Senses the            Amplifies tiny        Converts to
                 difference            difference to         clean digital
                 between inputs        full swing            output levels


TRANSISTOR-LEVEL SCHEMATIC (all stages in one view)
══════════════════════════════════════════════════════════════════════════════

    Same transistor building blocks as an op-amp, minus the compensation
    capacitor — that's the key structural difference that makes it fast.
    See [[quick-context/differential-pair]] and
    [[quick-context/high-gain-amplifier-stage]] for deep dives on each.

                                Vdd
                                │
           ┌────────────────────┼──────────────────┐
           │                    │                  │
        ┌──┴──┐              ┌──┴──┐               │
        │ Q3  │──────────────│ Q4  │               │
        │PMOS │  current     │PMOS │               │        Vdd
        └──┬──┘  mirror      └──┬──┘               │         │
           │    (active          │                  │    ┌────┴────┐
           │     load)           ├── high-Z node    │    │ Rpull-up│
           │                     │   (gain happens  │    │  10kΩ  │
        ┌──┴──┐              ┌──┴──┐  here)        │    └────┬────┘
   V(+)►│ Q1  │              │ Q2  │◄── V(-)      │         │
        │NMOS │              │NMOS │               │         ├──── Vout
        └──┬──┘              └──┬──┘               │         │
           │                    │       no Cc!     │    ┌────┴────┐
           └─────────┬──────────┘      (no comp.   │    │   Q6   │
                     │                  cap — fast) │    │  NMOS  │
                ┌────┴────┐                        │    └────┬────┘
                │   Q5    │  tail current          │    (open-drain
                │  NMOS   │  source (100 μA)       │     output)
                └────┬────┘                        │         │
                     │                             │         │
                  [Rbias]  (sets bias current)     │         │
                     │                             │         │
           ──────────┴─────────────────────────────┴─────────┘
                                GND

    ┌──────────────────────────────────────────────────────────────┐
    │  Compare to op-amp (same diff pair, different output path):  │
    │  • Same Q1–Q5 differential pair + current mirror             │
    │  • NO compensation capacitor — nothing slows the gain node   │
    │  • Output is digital (open-drain Q6), not linear push-pull   │
    └──────────────────────────────────────────────────────────────┘


WHAT EACH PART DOES
══════════════════════════════════════════════════════════════════════════════

    Part             Transistors          Function
    ────             ───────────          ────────
    Differential     Q1, Q2 (NMOS)        Converts V(+) − V(-) into a
    Input Pair                            current difference. Higher Vgs
                                          = more current through that side.

    Current Mirror   Q3, Q4 (PMOS,        Active load. Copies Q1's current
    Active Load      gates tied)          to Q4, where it fights Q2's
                                          current. The mismatch × high
                                          impedance = huge voltage swing.

    Tail Current     Q5 (NMOS) +          Fixes total current (e.g. 100 μA)
    Source           Rbias (resistor)     shared by Q1 + Q2. Rejects
                                          common-mode noise on both inputs.

    Output Stage     Q6 (NMOS,            Open-drain: Q6 ON → Vout = GND.
                     open-drain)          Q6 OFF → pull-up sets HIGH level.
                                          Can also be push-pull (add PMOS
                                          above Q6) for faster transitions.


SIGNAL FLOW
══════════════════════════════════════════════════════════════════════════════

    1. V(+) and V(-) each drive one transistor's gate (Q1, Q2)
    2. Q5 + Rbias force Q1 + Q2 to share a fixed 100 μA:
       if V(+) > V(-) → Q1 takes 60 μA, Q2 gets 40 μA
    3. Mirror (Q3) copies Q1's 60 μA and forces it into Q4
    4. Q4 pushes 60 μA down, but Q2 only pulls 40 μA
       → 20 μA mismatch at the high-impedance node
       → V = I × R → 20 μA × 2 MΩ = huge voltage swing → rail
    5. That rail-level voltage drives Q6 fully ON or OFF → digital output
    6. No compensation cap → this all happens in nanoseconds
       (an op-amp's Cc would slow step 4 to microseconds)
```

### What Makes It Different from an Op-Amp

An [[quick-context/op-amp|op-amp]] and a comparator have the same input stage (differential pair), but everything after that is optimized differently:

```
OP-AMP vs COMPARATOR: Same Input, Different Optimization
==============================================================================

    Feature              │ Op-Amp                    │ Comparator
    ═════════════════════╪═══════════════════════════╪══════════════════════════
    Feedback             │ Negative (always)         │ None, or positive
                         │                           │   (for hysteresis)
    Output type          │ Analog (proportional)     │ Digital (binary)
    Output stage         │ Push-pull, linear         │ Push-pull or open-drain
    Speed (slew rate)    │ 1-50 V/μs typical        │ Output in 1-500 ns
    Compensation         │ Internal cap slows it     │ No compensation cap
                         │ for stability             │ (speed is the priority)
    Output swing         │ Limited by supply rails   │ Full rail-to-rail or
                         │                           │   logic-level compatible
    Input overdrive      │ Kept near zero by         │ Can be volts apart
                         │ negative feedback         │   (open-loop operation)

    KEY: The compensation capacitor inside an op-amp deliberately slows
    the response to prevent oscillation in feedback circuits. A comparator
    removes this cap because it WANTS fast transitions---it's not in a
    feedback loop (or only has positive feedback for hysteresis).
```

</details>

<details>
<summary><strong>The Key Tension</strong> --- Speed vs. noise immunity</summary>

The fundamental tradeoff in comparator design: **faster response** vs. **resistance to false triggering**.

```
THE HYSTERESIS DILEMMA
==============================================================================

WITHOUT HYSTERESIS (bare comparator):
──────────────────────────────────────────────────────────────────────────────

    Input signal with noise:

                  noise
    Vref ─ ─ ─ ─╱╲╱╲╱╲─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ threshold
              ╱╲╱      ╲╱╲
            ╱╱              ╲╲
          ╱╱                  ╲╲

    Output:
    HIGH ─┐ ┌┐ ┌┐ ┌─────────────────────────────
          └─┘└─┘└─┘                              ← CHATTER!
    LOW

    Problem: Every time noise causes the input to cross the threshold,
    the output toggles. A slowly-changing signal + noise = rapid oscillation.


WITH HYSTERESIS (Schmitt trigger comparator):
──────────────────────────────────────────────────────────────────────────────

    Input signal with noise:

    V_high ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ rising threshold
                  noise
    V_low  ─ ─ ─╱╲╱╲╱╲─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ falling threshold
              ╱╲╱      ╲╱╲
            ╱╱              ╲╲
          ╱╱                  ╲╲

    Output:
    HIGH ──────────────────────────────────────────
                                                   ← CLEAN!
    LOW  ─────┘

    The noise wiggles never cross BOTH thresholds, so the output
    doesn't chatter. The price: you lose precision about exactly
    where the transition happens (it's somewhere in the hysteresis band).


HOW POSITIVE FEEDBACK CREATES HYSTERESIS:
──────────────────────────────────────────────────────────────────────────────

              R1                    R2
    Vin ────╱╱╱╱────┬────────────╱╱╱╱──── Vout
                    │                       │
                    │                       │
             V(+) ─┘                        │
                   ╲                        │
            V(-) ───╲                       │
                     ╲──────────────────────┘
                     ╱
             Vref ──╱

    A fraction of the output is fed back to the non-inverting input.
    When output is HIGH, V(+) shifts up → input must go LOWER to flip.
    When output is LOW, V(+) shifts down → input must go HIGHER to flip.

    Hysteresis band ≈ Vout_swing × R1 / R2
```

| Comparator Type | Propagation Delay | Use Case |
|----------------|-------------------|----------|
| **Ultra-fast** (ADCMP601) | 3.5 ns | High-speed data, clock recovery |
| **Fast** (LM393) | 300 ns | General purpose, motor control |
| **With built-in hysteresis** (LM311) | 200 ns | Noisy environments, threshold detection |
| **Schmitt trigger IC** (74HC14) | 15 ns | Digital signal cleaning, debouncing |
| **Window comparator** (LM339 pair) | 300 ns | "Is voltage between A and B?" |

The other key tension is **dedicated comparator vs. op-amp used as a comparator**:

| Factor | Dedicated Comparator | Op-Amp as Comparator |
|--------|---------------------|---------------------|
| Speed | 1-500 ns | 1-50 $\mu$s (compensation cap slows it) |
| Output | Logic-compatible or open-drain | Analog (may not reach rails) |
| Recovery | Fast (designed for overdrive) | Slow (input stage saturates) |
| Hysteresis | Often built-in or easy to add | Must add external positive feedback |
| Cost | Cheap ($0.10-$1.00) | Often already on the board |

**Bottom line:** Never use an op-amp as a comparator in production designs---it works on the bench but fails in noisy, fast, or temperature-varying real-world conditions. Use a real comparator.

</details>

<details>
<summary><strong>Concrete Example</strong> --- Battery voltage monitor</summary>

A lithium battery must not discharge below 3.0V or it suffers permanent damage. You need a circuit that pulls a "low battery" warning pin LOW when $V_{BAT}$ drops below 3.0V.

```
BATTERY UNDERVOLTAGE DETECTOR
==============================================================================

CIRCUIT:
──────────────────────────────────────────────────────────────────────────────

                 VBAT (3.0V - 4.2V)
                    │
                  ┌─┴─┐
                  │   │ R1 = 100kΩ
                  │   │
                  └─┬─┘
                    │
                    ├──── V(+) on comparator
                    │
                  ┌─┴─┐
                  │   │ R2 = 100kΩ
                  │   │
                  └─┬─┘
                    │
                   GND

    V(+) = VBAT × R2 / (R1 + R2) = VBAT / 2

    At VBAT = 3.0V:  V(+) = 1.50V
    At VBAT = 4.2V:  V(+) = 2.10V
    At VBAT = 3.5V:  V(+) = 1.75V


                                                 Vdd (3.3V)
    VBAT                                          │
      │                                     ┌─────┴─────┐
      │                                     │  10kΩ     │
      │                                     │ (pull-up) │
      ├─── divider ──► V(+) ─┤+  ╲         └─────┬─────┘
      │                      │    ╲               │
      │              Vref ───┤-    ╲──────────────┤
      │             (1.50V)  │     ╱              │
      │                      │    ╱               ├──── VBAT_OK
      │                      └──╱                 │    (to MCU GPIO)
      │                     (open-drain)          │
     GND


DESIGN:
──────────────────────────────────────────────────────────────────────────────

    Target trip point: VBAT = 3.0V → V(+) = 1.50V
    Reference: 1.50V (from a bandgap reference or second divider)

    When VBAT > 3.0V: V(+) > Vref → output HIGH (open-drain OFF)
                       Pull-up holds VBAT_OK = HIGH → battery OK

    When VBAT < 3.0V: V(+) < Vref → output LOW (open-drain ON)
                       VBAT_OK pulled to GND → MCU sees LOW → warning!


ADDING HYSTERESIS (prevent chatter at 3.0V boundary):
──────────────────────────────────────────────────────────────────────────────

    Add R3 = 10MΩ from output to V(+) input.

    When output is HIGH (3.3V):
        V(+) shifts up slightly via R3 → effective threshold drops to ~2.97V

    When output is LOW (0V):
        V(+) shifts down slightly via R3 → effective threshold rises to ~3.03V

    Hysteresis band: ~60mV → battery must recover to 3.03V before
    the warning clears. Prevents chattering when battery sits at 3.0V.


CURRENT CONSUMPTION:
──────────────────────────────────────────────────────────────────────────────

    Divider: I = VBAT / (R1 + R2) = 4.2V / 200kΩ = 21 μA
    Comparator (TLV3691): ~0.75 μA quiescent
    Total: ~23 μA — negligible for a battery that holds 2000+ mAh
```

**The one thing most outsiders get wrong about this is...** thinking a comparator is just a "degraded op-amp" that happens to be used without feedback. In reality, a comparator is a deliberately different design. The internal compensation [[learning/notes/quick-context/capacitor|capacitor]] that makes op-amps stable in feedback loops is exactly what makes them terrible comparators---it slows down the output transition, causes the output to ring or latch up when overdriven, and the output stage may not reach logic-compatible voltage levels. Comparator ICs are designed from the ground up for fast overdrive recovery, clean rail-to-rail digital output, and operation without negative feedback.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> --- Related topics to explore</summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/comparator-specification]]** --- How to read a real comparator datasheet (the TI LMC7211-N): what each spec section (Absolute Maximum Ratings, Operating Ratings, DC/AC Electrical Characteristics, Typical Characteristics) actually means, and which numbers are guaranteed versus typical.

- **[[quick-context/op-amp]]** --- Shares the same differential-pair input stage. Understanding the [[quick-context/op-amp|op-amp's]] golden rules (virtual short, no input current) explains what happens when you remove the negative feedback: the virtual short breaks, and the output slams to the rails---which is exactly what a comparator does intentionally.

- **[[quick-context/transistor]]** --- Comparators are built from [[quick-context/transistor|transistors]] at every stage: differential pair for sensing, current mirrors for biasing, output transistors for driving. The differential pair is the same circuit used in op-amps, ADCs, and voltage regulators.

- **[[quick-context/pwm-controller-circuit]]** --- The comparator inside a [[quick-context/pwm-controller-circuit|buck converter IC]] intersects the error amplifier's output with the sawtooth ramp to produce the [[learning/notes/micro-context/pwm-pulse-width-modulation|PWM]] pulse. This is the comparator's most common industrial application.

- **[[quick-context/rc-oscillator]]** --- Every [[quick-context/rc-oscillator|relaxation oscillator]] uses a comparator (or transistor acting as one) to detect when the capacitor voltage hits the threshold. The comparator triggers the reset that starts the next cycle.

- **[[quick-context/transistor-analog-to-digital]]** --- A comparator is the simplest possible 1-bit ADC---it makes a binary decision from an analog input. Flash ADCs use $2^n - 1$ comparators in parallel to get n-bit conversion in a single clock cycle.

- **[[quick-context/resistor]]** --- [[quick-context/resistor|Resistor]] dividers create both the reference voltage and the scaled feedback signal. Divider accuracy directly determines threshold accuracy.

- **[[micro-context/adc-analog-to-digital-converter]]** --- ADCs are built from comparators. A successive-approximation ADC uses one comparator with a DAC; a flash ADC uses many comparators in parallel.

- **[[learning/notes/small-context/pull-up-pull-down-resistors]]** --- Every MCU GPIO input is a comparator (typically a Schmitt trigger) deciding HIGH vs LOW. Pull-up/pull-down resistors define the "rest" voltage that comparator sees when nothing else is driving the pin.

- **[[learning/notes/quick-context/bare-minimal-data-storage-circuit]]** --- Where the comparator earns its place as a 1-bit ADC inside a minimal data-storage circuit: it converts the analog input voltage into the clean `in_bit` signal that a [[learning/notes/quick-context/d-flip-flop|register]] can capture on each [[learning/notes/micro-context/clock-edges|clock edge]].

</details>

<details>
<summary><strong>Test Your Understanding</strong> --- 5 progressive questions</summary>

**Q1:** What is the output of a comparator when V(+) = 2.5V and V(-) = 2.3V?
<details>
<summary>Answer</summary>
**HIGH.** V(+) > V(-), so the output goes to the positive rail (or the pull-up voltage for open-drain outputs). The magnitude of the difference (0.2V) doesn't matter---any positive difference produces the same HIGH output. See: How It Works (Comparator Function).
</details>

**Q2:** Why does a comparator's output "chatter" when the input signal slowly crosses the threshold in a noisy environment?
<details>
<summary>Answer</summary>
**Noise causes the input to repeatedly cross the single threshold.** If the input is hovering near $V_{REF}$ and noise adds even a few millivolts of oscillation, the signal crosses back and forth across the threshold rapidly. Each crossing triggers an output transition, producing a burst of rapid toggling. The solution is hysteresis: two separate thresholds (one for rising, one for falling) so that small noise excursions can't cause re-crossing. See: The Key Tension (The Hysteresis Dilemma).
</details>

**Q3:** An engineer uses an op-amp (LM358, GBW = 1 MHz) as a comparator in a prototype and it works fine. When they deploy it in a factory with noisy power lines, it fails. Why?
<details>
<summary>Answer</summary>
**Three problems compound in the noisy environment:** (1) The LM358's internal compensation capacitor limits its slew rate, so the output takes microseconds to transition---during which time noise can cause multiple crossings. (2) When the input difference is large, the op-amp's input stage saturates, and recovery from saturation takes additional microseconds (poor overdrive recovery). (3) The output may not reach clean logic levels (the LM358 can't swing to the positive rail with a resistive load), so the receiving logic sees ambiguous voltage levels. A dedicated comparator (e.g., LM393) has none of these problems: no compensation cap, designed for overdrive, and open-drain output that swings to clean GND. See: The Key Tension (Op-Amp as Comparator table).
</details>

**Q4:** In a flash ADC, why do you need $2^n - 1$ comparators for n bits of resolution?
<details>
<summary>Answer</summary>
**Each comparator represents one possible threshold level.** An n-bit ADC must distinguish $2^n$ voltage levels. The boundaries between adjacent levels require $2^n - 1$ comparators, each with its reference voltage set to a different point on a resistor ladder. All comparators fire simultaneously---those whose reference is below the input output HIGH, those above output LOW. A priority encoder then converts this "thermometer code" (a string of 1s followed by 0s) into a binary number. For example, an 8-bit flash ADC needs 255 comparators. This is why flash ADCs are fast (one clock cycle) but expensive (exponential hardware). See: Peripheral Knowledge (ADC connection).
</details>

**Q5:** A window comparator uses two comparators to detect whether a voltage is between two limits (e.g., 2.5V < Vin < 3.5V). Draw the logic: how do you combine two comparator outputs to get a single "in range" signal?
<details>
<summary>Answer</summary>
**Use two comparators with open-drain outputs wired together (wire-AND):**

Comparator A: V(+) = Vin, V(-) = 2.5V (lower limit). Output HIGH when Vin > 2.5V.
Comparator B: V(+) = 3.5V (upper limit), V(-) = Vin. Output HIGH when Vin < 3.5V.

Both outputs are open-drain, tied together with a single pull-up resistor. The combined output is HIGH only when BOTH comparators output HIGH (neither pulls LOW)---meaning Vin is above 2.5V AND below 3.5V. If Vin goes outside either limit, the corresponding comparator pulls the line LOW.

This is why open-drain outputs exist on comparators: wire-AND logic with no additional gate needed. See: 5 Essential Terms (Open-drain output).
</details>

</details>
