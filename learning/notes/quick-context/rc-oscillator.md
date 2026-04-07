---
topic: RC Oscillator
created: 2026-03-28
---

# RC Oscillator

> **Related:** [[quick-context/resistor]] | [[quick-context/capacitor]] | [[quick-context/frequency-and-filtering]] | [[quick-context/pwm-controller-circuit]]

> **TL;DR:** An RC oscillator generates a repeating waveform (sawtooth, square, or triangle) using only [[quick-context/resistor|resistors]] and [[quick-context/capacitor|capacitors]] -- no quartz crystal or resonator needed. It's the cheap, "good enough" [[learning/notes/micro-context/clock-source|clock source]] inside [[learning/notes/micro-context/pwm-pulse-width-modulation|PWM]] controller ICs, 555 timers, and [[learning/notes/micro-context/microcontroller|microcontroller]] internal oscillators (like the [[learning/notes/micro-context/stm32-microcontroller|STM32]]'s HSI), where ±1-5% frequency accuracy is acceptable because a feedback loop or protocol tolerance compensates for drift.

## The Core Problem

Many circuits need a periodic signal -- a clock, a ramp, a trigger -- but don't need the ±0.002% precision of a [[micro-context/crystal-oscillator|crystal oscillator]]. Crystals are external components that cost board space, money, and design complexity. An RC oscillator can be built entirely on-chip from standard transistors, resistors, and capacitors already available in the IC fabrication process. This makes it the default choice whenever "roughly the right frequency" is good enough: [[quick-context/pwm-controller-circuit|PWM controllers]] switching at ~500 kHz, [[micro-context/clock-source|microcontroller fallback clocks]], and timing circuits where a feedback loop corrects for frequency error.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **RC Time Constant ($\tau = RC$)** | The time it takes a [[quick-context/capacitor\|capacitor]] charging through a [[quick-context/resistor\|resistor]] to reach ~63% of its final [[learning/notes/quick-context/voltage|voltage]]. This is the fundamental timing element -- $R$ and $C$ values set the oscillation frequency. |
| **Threshold / Trip Point** | A voltage level (set by a [[quick-context/comparator\|comparator]] or [[quick-context/transistor\|transistor]] switch) at which the circuit changes state -- triggering a reset, discharge, or direction change in the waveform. |
| **Sawtooth Wave** | A waveform that ramps linearly from low to high, then snaps back to zero. Produced when a constant current charges a [[learning/notes/quick-context/capacitor|capacitor]], then a switch discharges it instantly. This is the waveform inside [[quick-context/pwm-controller-circuit\|PWM controller ICs]]. |
| **Relaxation Oscillator** | The general class of oscillator that works by charging a capacitor to a threshold, then rapidly discharging it and repeating. The 555 timer and the sawtooth generator inside [[learning/notes/micro-context/buck-converter|buck converter]] ICs are both relaxation oscillators. |
| **Frequency Accuracy** | How close the actual output frequency is to the target. RC oscillators are typically ±1-5% due to component tolerances and temperature drift, vs. ±0.002% for [[micro-context/crystal-oscillator\|crystals]] and ±0.5% for [[micro-context/ceramic-resonator\|ceramic resonators]]. |

<details>
<summary><strong>How It Works</strong> -- Charge, compare, reset, repeat</summary>

Every RC oscillator follows the same core loop: charge a capacitor through a [[learning/notes/quick-context/resistor|resistor]], detect when the voltage crosses a threshold, then reset the capacitor and start over. The time to charge from 0V to the threshold voltage determines the period.

### The Basic Relaxation Oscillator

```
RC RELAXATION OSCILLATOR (simplified)
==============================================================================

    VCC ────────────────────────────────────────────────────
                │
              ┌─┴─┐
              │   │  R (charging resistor)
              │   │
              └─┬─┘
                │
                ├──────────────── to comparator (+) input
                │
              ┌─┴─┐
              │   │  C (timing capacitor)
              │   │
              └─┬─┘
                │
    GND ──────┬─┘
              │
           [SWITCH]  ◄── comparator output controls this
              │           (resets C when threshold reached)
    GND ──────┘


    The cycle:

    1. CHARGE: Current flows through R into C
       V_cap rises exponentially: V(t) = VCC × (1 - e^(-t/RC))

    2. COMPARE: When V_cap reaches threshold V_TH...

    3. RESET: Switch closes, discharging C to ~0V almost instantly

    4. REPEAT: Switch opens, charging begins again
```

### Sawtooth Waveform Generation (What's Inside a PWM IC)

The [[quick-context/pwm-controller-circuit|sawtooth oscillator inside a buck converter IC]] uses a constant current source instead of a resistor, which produces a perfectly linear ramp rather than an exponential curve. This matters because a linear ramp gives a linear relationship between the error voltage and the [[micro-context/pwm-pulse-width-modulation|duty cycle]].

```
SAWTOOTH GENERATOR (constant-current variant used in PWM ICs)
==============================================================================

    ┌──────────────────┐
    │ Constant Current │
    │ Source (I)       │        With constant current:
    └────────┬─────────┘        V_cap = (I/C) × t  (LINEAR ramp!)
             │
             │                  vs. resistor charging:
             ├──────► to comparator     V_cap = VCC(1-e^(-t/RC))  (exponential)
             │
           ┌─┴─┐
           │   │ C
           └─┬─┘
             │
          [SWITCH] ◄── reset when V_cap hits V_TH
             │
            GND


    Voltage across C
    ▲
    │
V_TH├ · · · ·╱│· · · ·╱│· · · ·╱│· · · ·╱│
    │        ╱ │      ╱ │      ╱ │      ╱ │
    │       ╱  │     ╱  │     ╱  │     ╱  │
    │      ╱   │    ╱   │    ╱   │    ╱   │
    │     ╱    │   ╱    │   ╱    │   ╱    │
    │    ╱     │  ╱     │  ╱     │  ╱     │
    │   ╱      │ ╱      │ ╱      │ ╱      │
    │  ╱       │╱       │╱       │╱       │╱
 0V ├──────────┴────────┴────────┴────────┴──────► time
    │          T        2T       3T       4T
    │
    │   T = (C × V_TH) / I
    │
    │   At 500 kHz:  T = 2 μs
    │   With C = 10 pF, V_TH = 1.5V:
    │   I = C × V_TH / T = 10e-12 × 1.5 / 2e-6 = 7.5 μA
```

### Square Wave Generation (555 Timer Style)

A square wave oscillator charges *and* discharges through resistors, toggling between two thresholds:

```
SQUARE WAVE OSCILLATOR (two-threshold relaxation)
==============================================================================

    Voltage across C
    ▲
    │
V_H ├ · · · · ╱─────╲ · · · · · ╱─────╲ · · · ·
    │        ╱       ╲         ╱       ╲
    │       ╱         ╲       ╱         ╲
    │      ╱           ╲     ╱           ╲
V_L ├ ───╱· · · · · · · ╲───╱ · · · · · · ╲────
    │
 0V ├──────────────────────────────────────────► time
    │    charge    discharge   charge   discharge
    │   (through   (through   (through  (through
    │    R1+R2)      R2)       R1+R2)     R2)
    │
    │   V_H = 2/3 VCC  (upper threshold)
    │   V_L = 1/3 VCC  (lower threshold)
    │
    │   f = 1.44 / ((R1 + 2×R2) × C)    (555 timer formula)
```

### Why RC Oscillators Drift

The frequency depends on $R$, $C$, and threshold voltages -- all of which vary with temperature:

```
FREQUENCY DRIFT SOURCES
==============================================================================

    Component        │ Temperature Effect         │ Typical Drift
    ═════════════════╪════════════════════════════╪═══════════════
    Resistor (R)     │ Shifts with temperature    │ ±50 to ±200 ppm/°C
    Capacitor (C)    │ Varies by type (ceramic    │ ±30 to ±1000 ppm/°C
                     │ caps are worst offenders)  │
    Threshold (V_TH) │ Transistor Vbe shifts      │ -2 mV/°C
                     │ ~-2mV/°C                   │
    ─────────────────┼────────────────────────────┼───────────────
    Total RC osc.    │ Combined drift             │ ±1-5% over temp
    Crystal          │ Quartz is mechanically     │ ±20 ppm (0.002%)
                     │ stable                     │

    EXAMPLE: STM32F4 internal RC oscillator (HSI)
    Nominal: 16 MHz
    At 25°C: 16 MHz ±1% (15.84 - 16.16 MHz)
    At -40 to +105°C: -8% to +4.5% (per datasheet)

    For CAN bus (requires ≤1.58% clock accuracy):
    HSI alone FAILS the spec at temperature extremes →
    that's why the Pupper uses external ceramic
    resonators (±0.5%) instead
```

</details>

<details>
<summary><strong>The Key Tension</strong> -- Accuracy vs. cost and integration</summary>

The core tradeoff is between frequency precision and the ability to integrate everything on-chip:

| | RC Oscillator | [[micro-context/ceramic-resonator\|Ceramic Resonator]] | [[micro-context/crystal-oscillator\|Crystal Oscillator]] |
|---|---|---|---|
| **Accuracy** | ±1-5% | ±0.5% | ±0.002% (20 ppm) |
| **External parts** | None (on-chip) | 1 component (3-pin) | 1 crystal + 2 caps |
| **Cost** | Free (built into IC) | ~$0.10-0.30 | ~$0.20-1.00 + caps |
| **Board space** | Zero | Small | Medium |
| **Startup time** | Microseconds | ~0.1-0.5 ms | ~1-10 ms |
| **Good enough for** | PWM switching, fallback clock, timing delays | CAN, UART, I2C, SPI | USB, Ethernet, RF, precision timing |

**When RC is fine:**
- [[quick-context/pwm-controller-circuit|PWM controllers]] in buck converters -- the feedback loop compensates for switching frequency drift. Whether it's 480 kHz or 520 kHz, the output voltage is the same.
- Internal MCU clock for bootup -- the STM32 starts on its 16 MHz HSI (RC), then switches to the external [[micro-context/ceramic-resonator|resonator]] once the PLL locks.
- 555-style timers, LED blinkers, debounce circuits -- anywhere ±5% is "close enough."

**When RC is NOT fine:**
- USB requires ±0.25% clock accuracy -- RC oscillators can't guarantee this over temperature.
- [[quick-context/can-bus|CAN bus]] needs ≤1.58% -- RC is marginal; the Pupper v3 uses ceramic resonators.
- RF communication -- even ±0.1% frequency error would shift the carrier off-channel.

</details>

<details>
<summary><strong>Concrete Example</strong> -- The 555 timer as an RC oscillator</summary>

The 555 timer is the most famous RC oscillator IC ever made (over a billion sold per year). It contains exactly the building blocks described above: two comparators, a flip-flop, a discharge transistor, and a [[quick-context/resistor|resistor]] voltage divider that sets the thresholds at $\frac{1}{3}V_{CC}$ and $\frac{2}{3}V_{CC}$.

```
555 TIMER IN ASTABLE (FREE-RUNNING) MODE
==============================================================================

    VCC ──────┬──────────────────────────────┬─────
              │                              │
            ┌─┴─┐                     ┌──────┴──────┐
            │   │ R1                  │   555 IC    │
            │   │                     │              │
            └─┬─┘                     │  ┌───────┐  │
              ├──────────────────────►│  │2/3 VCC│  │
              │                       │  │ COMP  ├──┤►S  Q ──► OUTPUT
            ┌─┴─┐                     │  └───────┘  │  FLIP
            │   │ R2                  │             │  FLOP
            │   │                     │  ┌───────┐  │
            └─┬─┘                     │  │1/3 VCC│  │
              ├──────────────────────►│  │ COMP  ├──┤►R  Q̄
              │                       │  └───────┘  │   │
            ┌─┴─┐                     │             │   │
            │   │ C                   │  DISCHARGE ◄─┘   │
            │   │                     │  TRANSISTOR      │
            └─┬─┘                     └──────┬──────┘   │
              │                              │           │
    GND ──────┴──────────────────────────────┴───────────┘


    DESIGN EXAMPLE: 1 kHz square wave

    Want f = 1 kHz.  Choose C = 100 nF.

    f = 1.44 / ((R1 + 2×R2) × C)

    1000 = 1.44 / ((R1 + 2×R2) × 100e-9)

    R1 + 2×R2 = 1.44 / (1000 × 100e-9) = 14.4 kΩ

    Choose R1 = 4.7 kΩ, R2 = 4.7 kΩ:
    R1 + 2×R2 = 4.7k + 9.4k = 14.1 kΩ  ← close enough

    Actual f = 1.44 / (14,100 × 100e-9) = 1021 Hz  (~2% off target)

    Duty cycle = (R1 + R2) / (R1 + 2×R2) = 9.4k/14.1k = 66.7%
    (not 50% because charge path includes R1+R2 but discharge only uses R2)
```

**The one thing most outsiders get wrong about this is...** assuming that the "oscillator" inside a [[quick-context/pwm-controller-circuit|PWM controller IC]] or [[micro-context/stm32-microcontroller|microcontroller]] is a crystal. The internal oscillators in these chips are almost always RC-based -- they're built from the same transistors and passive components already in the silicon. A crystal is an *external* component that provides better accuracy when needed. The STM32, for example, has *both*: an internal 16 MHz RC oscillator (HSI) for quick startup, and pins for an external crystal or [[micro-context/ceramic-resonator|ceramic resonator]] (HSE) for precision. The chip boots on the RC oscillator and optionally switches to the crystal-referenced PLL once it stabilizes.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> -- Related topics to explore</summary>

- **[[quick-context/resistor]]** -- The R in RC. Resistor tolerance and temperature coefficient directly affect oscillator frequency accuracy.

- **[[quick-context/capacitor]]** -- The C in RC. Capacitor type matters enormously: ceramic caps have voltage-dependent [[learning/notes/quick-context/capacitance|capacitance]] that shifts frequency under load; film caps are more stable but larger.

- **[[quick-context/capacitance]]** -- Capacitance as a geometric property. Parasitic capacitance on [[learning/notes/quick-context/pcb-printed-circuit-board|PCB]] traces or IC pins adds to the timing capacitor, shifting frequency from the calculated value.

- **[[quick-context/frequency-and-filtering]]** -- RC circuits are the foundation of passive filters. The same $f_c = 1/(2\pi RC)$ equation that sets a filter's cutoff frequency also governs the oscillator's timing.

- **[[quick-context/pwm-controller-circuit]]** -- The sawtooth oscillator inside a buck converter IC is an RC relaxation oscillator (constant-current variant). It sets the switching frequency that the error amplifier and [[learning/notes/quick-context/comparator|comparator]] modulate into PWM.

- **[[micro-context/crystal-oscillator]]** -- The high-precision alternative. Uses mechanical resonance of quartz instead of RC charging, achieving 100-1000x better frequency accuracy.

- **[[micro-context/ceramic-resonator]]** -- A middle ground between RC and crystal: piezoelectric resonance gives ±0.5% accuracy, cheaper and simpler than a crystal but still an external component.

- **[[micro-context/clock-source]]** -- How the STM32 selects between its internal RC oscillator (HSI) and external resonator (HSE), and how the PLL multiplies either to operating frequency.

- **[[quick-context/clock-sources-and-timing|Clock Sources and Timing]]** -- The companion quick-context covering the OTHER clock source types (crystal, [[learning/notes/micro-context/ceramic-resonator|ceramic resonator]]) and the full chain from source to PLL to system clock to edge-triggered computation to thermal limits.

- **[[quick-context/comparator]]** -- The [[quick-context/comparator|comparator]] that detects the threshold crossing is the key active element in every relaxation oscillator. It's what converts the capacitor's smooth charging curve into a sharp trigger event.

- **[[quick-context/op-amp]]** -- Comparators (which trigger the oscillator's reset) are essentially op-amps without feedback, driven into saturation to produce digital-like HIGH/LOW outputs.

- **[[quick-context/impedance-and-reactance]]** -- The capacitor's [[quick-context/impedance-and-reactance|reactance]] ($X_C = 1/(2\pi fC)$) is what makes RC timing frequency-dependent: at the oscillation frequency, the capacitor's [[learning/notes/quick-context/impedance-and-reactance|impedance]] interacts with the resistor to set the charge/discharge rate.

- **[[quick-context/capacitive-sensing-measurement]]** -- The same RC timing principle used in oscillators is repurposed for sensing: charge an unknown capacitance through a known resistor, time the result, and the count is proportional to $C_x$. An RC oscillator is essentially a capacitive sensor that continuously measures its own capacitance.

</details>

<details>
<summary><strong>Test Your Understanding</strong> -- 5 progressive questions</summary>

**Q1:** Why is an RC oscillator less accurate than a [[learning/notes/micro-context/crystal-oscillator|crystal oscillator]]?
<details>
<summary>Answer</summary>
An RC oscillator's frequency depends on resistor and capacitor values, which drift ±1-5% with temperature, manufacturing tolerance, and aging. A crystal oscillator's frequency is set by the mechanical dimensions of a quartz crystal, which is inherently stable (±20 ppm). The crystal vibrates at a precise resonant frequency determined by physics; the RC circuit charges at a rate determined by component values that change with conditions. See: How It Works (Frequency Drift Sources).
</details>

**Q2:** A buck converter IC has an internal oscillator running at 500 kHz ±5%. Does this 5% frequency error affect the output voltage?
<details>
<summary>Answer</summary>
**No.** The output voltage is set by the feedback loop, not the switching frequency. If the oscillator runs at 475 kHz instead of 500 kHz, the error amplifier simply adjusts the duty cycle to maintain $V_{OUT} = V_{IN} \times D$. The frequency changes how often the [[learning/notes/micro-context/mosfet|MOSFET]] switches, but the feedback loop ensures the correct duty cycle regardless. This is exactly why an RC oscillator is "good enough" for PWM controllers. See: The Key Tension.
</details>

**Q3:** You want to build a 555 timer oscillator at 10 kHz with C = 10 nF. What values of R1 and R2 should you choose?
<details>
<summary>Answer</summary>
Using $f = 1.44 / ((R1 + 2 \times R2) \times C)$:

$R1 + 2 \times R2 = 1.44 / (10{,}000 \times 10 \times 10^{-9}) = 14.4\text{ k}\Omega$

Choose $R1 = R2 = 4.7\text{ k}\Omega$: $4.7\text{k} + 2 \times 4.7\text{k} = 14.1\text{ k}\Omega$, giving $f \approx 10.2\text{ kHz}$. Or for closer to 50% duty cycle, use $R1 = 1\text{ k}\Omega$, $R2 = 6.8\text{ k}\Omega$: $1\text{k} + 13.6\text{k} = 14.6\text{ k}\Omega$, giving $f \approx 9.86\text{ kHz}$ with duty cycle = 53%. See: Concrete Example.
</details>

**Q4:** The STM32 boots on its internal 16 MHz RC oscillator (HSI), then switches to an external 8 MHz ceramic resonator. Why start on the less accurate clock?
<details>
<summary>Answer</summary>
**Startup speed.** The internal RC oscillator is ready in microseconds because it's just transistors switching -- no external component needs to stabilize. An external crystal or resonator needs milliseconds to reach stable oscillation (the mechanical/piezoelectric element must build up energy). The MCU boots on HSI immediately, runs its startup code, configures the PLL to lock onto the external resonator, and then switches over. If the external oscillator fails, the MCU can fall back to HSI and keep running (at reduced accuracy). See: The Key Tension (startup time row).
</details>

**Q5:** An RC oscillator's capacitor has a ceramic dielectric whose capacitance drops 20% when the DC bias voltage across it equals its rated voltage. How does this affect the oscillator?
<details>
<summary>Answer</summary>
**The frequency increases.** With $f \propto 1/(RC)$, a 20% decrease in effective capacitance means the capacitor charges to the threshold voltage faster (less charge storage capacity). So the oscillation frequency rises by roughly 25% ($1/0.8 = 1.25$). This is a real problem with ceramic capacitors (especially X5R and Y5R types in small packages): their capacitance depends on applied voltage. This "DC bias derating" is a major reason why RC oscillators using ceramic caps have poor frequency stability -- the frequency shifts depending on supply voltage. Film capacitors or NP0/C0G ceramics have negligible voltage dependence and are preferred for precision timing. See: Peripheral Knowledge (capacitor link).
</details>

</details>
