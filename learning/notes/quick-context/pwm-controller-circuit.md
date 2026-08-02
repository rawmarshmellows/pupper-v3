---
topic: PWM Controller Circuit
created: 2026-03-27
---

# PWM Controller Circuit

> **Related:** [[micro-context/buck-converter]] | [[micro-context/pwm-pulse-width-modulation]] | [[quick-context/op-amp]] | [[quick-context/transistor]] | [[quick-context/pupper-bom-control-board]]

> **TL;DR:** Inside every buck converter IC is a tiny analog feedback loop: an oscillator generates a sawtooth wave, an error amplifier compares the output [[quick-context/voltage|voltage]] to a reference, and a comparator intersects the two signals to produce the PWM pulse that drives the [[micro-context/mosfet|MOSFET]] gate. The whole loop runs autonomously at hundreds of kHz with no software involvement.

## The Core Problem

Without a feedback-controlled PWM, the output voltage of a [[micro-context/buck-converter|buck converter]] would drift with every change in load current or input voltage. You need a circuit that continuously senses the output, decides how long to keep the switch ON, and adjusts on a cycle-by-cycle basis — all in microseconds. This is too fast for a [[micro-context/stm32-microcontroller|microcontroller]]; it requires dedicated analog hardware running in a tight loop.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Sawtooth oscillator** | Internal [[quick-context/rc-oscillator|RC oscillator]] clock that generates a repeating ramp waveform (0V → peak → reset), setting the switching frequency (e.g., 500kHz) |
| **Error amplifier** | An [[quick-context/op-amp\|op-amp]] inside the IC that outputs a voltage proportional to how far $V_{OUT}$ is from the target — the "error signal" |
| **[[quick-context/comparator\|Comparator]]** | Compares the error signal to the sawtooth ramp; output goes HIGH when error > ramp, LOW when error < ramp — this IS the PWM pulse |
| **Voltage reference ($V_{REF}$)** | A precision internal voltage (typically 0.6–0.8V) that the error amplifier uses as its target — the "setpoint" |
| **Feedback divider** | Two [[quick-context/resistor\|resistors]] from $V_{OUT}$ to GND that scale the output down to match $V_{REF}$ (e.g., 5V → 0.8V), so the IC can regulate any voltage |

<details>
<summary><strong>How It Works</strong> — The complete PWM generation circuit</summary>

### The Full Circuit (IC + External Power Stage)

```
                                                   VIN
                                                    │
                     BUCK CONVERTER IC              │D
    ┌────────────────────────────────────────┐  ┌───┴───┐
    │                                        │  │       │
    │  ┌──────┐  ┌──────────┐  ┌──────┐     │  │  Q1   │ MOSFET
    │  │ VREF ├►(+) ERROR  ├►(+)     │     │  │       │
    │  │ 0.8V │  │  AMP    │  │ COMP │GATE │  │       │
    │  └──────┘  │         │  │      │ DRV ├──►G       │
    │            └───▲─────┘┌►(−)    │     │  └───┬───┘
    │                │      │ └──────┘     │      │S (SW node)
    │            FB pin  ┌──┴────────┐     │  ┌───┴───┐
    │                │   │ SAWTOOTH  │    │  │   L   │ Inductor
    │                │   │    OSC    │    │  └───┬───┘
    │                │   └───────────┘    │      │
    └────────────────┼────────────────────┘      ├──── VOUT
                     │                           │
                     │◄──────────────────────────┤ ← feedback path
                     │                           │
                ┌────┴────┐                  ┌───┴───┐
                │   R1    │                  │ C_OUT │ Output Cap
                ├─────────┤                  └───┬───┘
                │   R2    │                      │
                └────┬────┘                      │
                     │                           │
                    GND ─────────────────────────┘

    Complete loop: GATE DRV → Q1 gate → Q1 switches VIN through
    → L stores/releases energy → VOUT → R1/R2 divides down → FB pin
    → error amp compares to VREF → adjusts PWM → loop repeats
```

### Why R1 and R2? — Programming the Output Voltage

The error amplifier has a fixed internal reference ($V_{REF}$, typically 0.8V). It regulates whatever appears at the FB pin to equal $V_{REF}$ — that's the only thing it knows how to do. But you want 5V or 3.3V out, not 0.8V.

R1 and R2 solve this by forming a **voltage divider** that scales $V_{OUT}$ down to $V_{REF}$ level:

$$V_{FB} = V_{OUT} \times \frac{R_2}{R_1 + R_2} \quad \xrightarrow{\text{IC regulates } V_{FB} = V_{REF}} \quad V_{OUT} = V_{REF} \times \frac{R_1 + R_2}{R_2}$$

**Without R1 and R2**, you'd connect $V_{OUT}$ directly to the FB pin, and the IC would regulate the output to 0.8V — too low for almost anything. The divider lets a single IC design with one fixed reference regulate to *any* output voltage just by choosing resistor values.

**Why two resistors, not one?** A single resistor wouldn't create a defined division ratio. You need two resistors to form a ratio that depends *only* on R1 and R2, not on the IC's internals. The FB pin has extremely high input impedance (megaohms), so it draws negligible current and doesn't disturb the divider — the voltage at FB is determined purely by the R1/R2 ratio and $V_{OUT}$.

**R1 and R2 are the converter's "programming interface."** Changing the output voltage means changing one resistor. The IC, MOSFET, inductor, and capacitor can all stay the same — only the feedback divider ratio determines $V_{OUT}$.

### Step-by-Step: How One PWM Cycle Happens

**Step 1 — Oscillator generates the ramp.** The internal [[quick-context/rc-oscillator|RC oscillator]] produces a sawtooth wave that ramps linearly from 0V to a peak (say 1.5V), then snaps back to 0V. Each ramp-and-reset is one switching period $T$. At 500kHz, that's $T = 2\mu s$.

**Step 2 — Error amplifier measures the "mistake."** The [[quick-context/resistor|resistor]] divider scales $V_{OUT}$ down to $V_{FB}$. The error amplifier computes $V_{ERR} = A \times (V_{REF} - V_{FB})$, where $A$ is high gain (~60–80dB). If output is too low, $V_{ERR}$ rises; if too high, $V_{ERR}$ falls. The error amp has a compensation network (R-C) on its output that controls how fast it responds — too fast causes oscillation, too slow causes poor transient response.

**Step 3 — Comparator intersects ramp and error.** The comparator outputs HIGH when $V_{ERR} > V_{RAMP}$ and LOW when $V_{ERR} < V_{RAMP}$. Because the ramp is a linearly rising signal, a higher $V_{ERR}$ means the ramp takes longer to "catch up" — producing a wider pulse (longer ON time, higher [[micro-context/pwm-pulse-width-modulation|duty cycle]]).

**Step 4 — Gate driver amplifies the pulse.** The comparator output is a weak logic signal. The gate driver (a push-pull buffer) amplifies it to charge/discharge the [[micro-context/mosfet|MOSFET]] gate [[quick-context/capacitance|capacitance]] fast enough for clean switching transitions (nanoseconds).

### The Comparator Intersection — This IS How PWM Width Is Set

```
    Voltage
    ▲
    │
1.5V├ · · · · · · · · · · · · · · · · · · · · · · · · peak
    │        ╱│       ╱│       ╱│       ╱│       ╱│
    │       ╱ │      ╱ │      ╱ │      ╱ │      ╱ │
    │      ╱  │     ╱  │     ╱  │     ╱  │     ╱  │
    │  ●──╱──●│ ●──╱──●│    ╱   │    ╱   │    ╱   │
    │  │ ╱  │ │ │ ╱  │ │   ╱    │   ╱    │   ╱    │
1.0V├──┼╱───┼─┼─┼╱───┼─┼──╱─────┼──╱─────┼──╱─────┼─ Verr (HIGH = output too low)
    │  ╱    │ │ ╱    │ │ ╱      │ ╱      │ ╱      │
    │ ╱│    │ │╱│    │ │╱│      │╱│      │╱│      │
    │╱ │    │ ╱ │    │ ╱ │      ╱ │      ╱ │      │
    ╱  │    │╱  │    │╱  │     ╱│ │     ╱│ │      │
0.6V├──┼────┼───┼────┼───┼──●╱─┼─●───●╱─┼─●──────┼─ Verr (LOW = output recovered)
    │  │    │   │    │   │ ╱│  │    ╱│  │         │
    │  │    │   │    │   │╱ │  │   ╱ │  │         │
    │  │    │   │    │   ╱  │  │  ╱  │  │         │
0V  ├──┴────┴───┴────┴──╱┴──┴──┴─╱┴──┴──┴─────────┴─►
    │  t1   t2  t3   t4 t5  t6  t7  t8              time
    │
    │   ╱ = sawtooth ramp     ● = intersection point
    │   ── = Verr level       ── = Verr level

    PWM output (comparator result: HIGH when Verr > ramp):
    ├──────┤    ├──────┤    ├───┤    ├───┤
    │██████│    │██████│    │███│    │███│
    │██████│    │██████│    │███│    │███│
    └──────┴────┴──────┴────┴───┴────┴───┴────────────►
    ├─ wide pulse ─┤         ├narrow┤
      (high Verr)            (low Verr = output OK)

    Higher Verr → ramp takes longer to reach it → wider pulse → more ON time → more power
    Lower  Verr → ramp reaches it sooner       → narrow pulse → less ON time → less power
```

### The Closed Feedback Loop (Why It Self-Corrects)

```
    Load increases (draws more current)
           │
           ▼
    VOUT drops slightly (capacitor discharges faster)
           │
           ▼
    V_FB drops below Vref
           │
           ▼
    Error amplifier output (Verr) RISES
           │
           ▼
    Comparator intersection moves later → WIDER pulse
           │
           ▼
    MOSFET stays ON longer → more energy into inductor
           │
           ▼
    VOUT recovers back to target ──────────────────┐
           │                                        │
           └──── loop repeats every cycle ◄─────────┘
                 (self-correcting in microseconds)
```

This is a **negative feedback loop**: any deviation from the target is opposed. The error amplifier's compensation network (typically a series R-C from its output to the inverting input) controls the loop's speed and stability — this is where most of the IC designer's effort goes.

</details>

<details>
<summary><strong>The Key Tension</strong> — Switching speed vs. stability</summary>

The central tradeoff in PWM controller design is **loop bandwidth vs. stability**:

| Want | Problem |
|------|---------|
| **Fast response** (high bandwidth) | Error amplifier reacts to noise, overshoots, oscillates — the output rings |
| **Stable output** (low bandwidth) | Slow to respond to load transients — output dips/spikes before loop corrects |

This is tuned by the **compensation network** — a small R-C circuit on the error amplifier. It's the same stability problem as any negative feedback system (gain margin, phase margin). IC datasheets specify recommended compensation values for different inductor/capacitor combinations.

**Another tension: switching frequency**

| Higher frequency (1–2MHz) | Lower frequency (100–300kHz) |
|---|---|
| Smaller [[quick-context/inductor\|inductor]] and [[quick-context/capacitor\|capacitor]] needed (smaller board area) | Larger L and C needed (bigger board) |
| More switching losses ($P_{sw} \propto f$) — MOSFET turns on/off more often | Less switching loss |
| Gate driver must charge MOSFET capacitance faster | Easier gate driving |

Modern buck ICs typically run at 400kHz–2MHz, optimizing for small size. The TPS54302 on the Pupper control board, for example, uses a fixed 400kHz switching frequency.

</details>

<details>
<summary><strong>Concrete Example</strong> — Designing the feedback divider for 5V output</summary>

A buck converter IC has $V_{REF} = 0.8V$ internally. You want $V_{OUT} = 5V$. The feedback divider must scale 5V down to 0.8V:

$$V_{FB} = V_{OUT} \times \frac{R_2}{R_1 + R_2} = V_{REF}$$

$$\frac{R_2}{R_1 + R_2} = \frac{0.8}{5} = 0.16$$

Choose $R_2 = 10k\Omega$, then:

$$R_1 = R_2 \times \left(\frac{V_{OUT}}{V_{REF}} - 1\right) = 10k \times \left(\frac{5}{0.8} - 1\right) = 10k \times 5.25 = 52.5k\Omega$$

Use nearest standard value: $R_1 = 52.3k\Omega$ (E96 series) or $51k\Omega$ (E24).

```
    VOUT (5V) ────┬────
                  │
                ┌─┴─┐
                │   │ R1 = 52.3kΩ
                │   │
                └─┬─┘
                  ├──── FB pin → to error amplifier (sees ~0.8V here)
                ┌─┴─┐
                │   │ R2 = 10kΩ
                │   │
                └─┬─┘
                  │
    GND ──────────┘

    When VOUT = 5.0V:  V_FB = 5.0 × 10k/(52.3k+10k) = 0.803V ≈ Vref  ✓
    When VOUT = 4.8V:  V_FB = 4.8 × 10k/(52.3k+10k) = 0.771V < Vref  → duty cycle ↑
    When VOUT = 5.2V:  V_FB = 5.2 × 10k/(52.3k+10k) = 0.835V > Vref  → duty cycle ↓
```

**Changing VOUT is just changing R1.** Want 3.3V instead? $R_1 = 10k \times (3.3/0.8 - 1) = 31.25k\Omega$. The IC doesn't know or care what the output voltage is — it just regulates the FB pin to equal $V_{REF}$.

**The one thing most outsiders get wrong about this is...** thinking the [[micro-context/stm32-microcontroller|microcontroller]] or software generates the PWM for power conversion. In reality, the buck converter IC is a fully autonomous analog control system — it has its own oscillator, error amplifier, comparator, and gate driver on a single chip. The MCU doesn't even know the PWM exists. Software-generated PWM (from timer peripherals) is used for different things: [[micro-context/pwm-pulse-width-modulation|motor speed control]], LED dimming, and servo positioning — not power supply regulation, which requires the nanosecond-precision analog loop described here.

### Real Example on the Pupper v3 Control Board

The TPS54561 at **U8** on the Pupper v3 control board is exactly this circuit in silicon. Open [pupper-control-board-interactive.html](pupper-control-board-interactive.html) and hover U8 / R5 / R6 to see the feedback divider.

| Generic part above | Pupper board part |
|---|---|
| "Buck converter IC" (oscillator + error amp + comparator + gate driver) | **U8** — TPS54561DPRR (WSON-10) |
| High-side MOSFET (Q1) | **integrated inside U8** |
| $V_{REF}$ | 0.8V internal bandgap |
| R1 (top of feedback divider) | **R5** — 60.4kΩ (E96) |
| R2 (bottom of feedback divider) | **R6** — 11.5kΩ (E96) |
| External inductor | **L1** — 10µH |
| Catch/freewheeling [[quick-context/diode|diode]] | **D1** — SS56 Schottky |
| Output caps | **C18, C19** — 2× 47µF |

$V_{OUT} = 0.8\text{V} \times (1 + 60.4\text{k}/11.5\text{k}) \approx 5.0\text{V}$. R5 and R6 aren't some separate "PWM-setting" resistors — they are literally the feedback divider that programs the setpoint of the analog loop inside U8. The PWM itself never leaves U8; the only externally visible power-loop signals are SW (switching node, at L1), FB (the divider midpoint), and VOUT.

See [[micro-context/buck-converter#real-example-pupper-v3-control-board]] for the full Pupper buck topology.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[micro-context/buck-converter]]** — The power stage (MOSFET + diode + inductor + capacitor) that this controller drives
- **[[micro-context/pwm-pulse-width-modulation]]** — The PWM signal itself — what it is, duty cycle math, and applications beyond power conversion
- **[[quick-context/op-amp]]** — The error amplifier IS an op-amp; understanding virtual short and negative feedback is key to understanding the control loop
- **[[quick-context/frequency-and-filtering]]** — The output LC filter is a 2nd-order low-pass filter; the compensation network shapes the loop's frequency response
- **[[quick-context/capacitor]]** — Output capacitor smoothing and the MOSFET gate capacitance that the driver must charge
- **[[quick-context/inductor]]** — Energy storage element; its $V = L \times dI/dt$ relationship determines the current ramp rate
- **[[quick-context/resistor]]** — Feedback divider resistors set the output voltage; compensation network uses R-C
- **[[micro-context/mosfet]]** — The power switch being controlled; gate capacitance affects switching speed
- **[[quick-context/self-induction]]** — Why the inductor's collapsing field drives current through the freewheeling diode in Phase 2
- **[[micro-context/decoupling-capacitor]]** — Related concept: local charge reservoirs near ICs, same principle as output capacitor filtering

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** What happens to the PWM duty cycle if the load suddenly draws more current?
<details>
<summary>Answer</summary>
VOUT drops → V_FB drops below Vref → error amplifier output rises → comparator intersection moves later in the ramp → wider pulse → higher duty cycle → more energy delivered → VOUT recovers. See: The Closed Feedback Loop diagram.
</details>

**Q2:** If you want to change a buck converter's output from 5V to 3.3V, what do you physically change on the board?
<details>
<summary>Answer</summary>
Change R1 in the feedback divider (the resistor between VOUT and the FB pin). A smaller R1 means V_FB reaches Vref at a lower VOUT, so the controller regulates to a lower voltage. See: Concrete Example.
</details>

**Q3:** Why can't you just use a microcontroller's PWM output to regulate a buck converter?
<details>
<summary>Answer</summary>
A microcontroller's PWM timer typically runs at kHz rates with microsecond resolution, but a buck converter needs cycle-by-cycle correction at 500kHz+ with nanosecond switching transitions. Even though hardware interrupt latency is fast (~12 cycles, ~71ns on a 168MHz Cortex-M4), the total response time including ISR entry, ADC sampling, and computation pushes practical latency to ~1μs — comparable to an entire switching period. The analog comparator inside the IC responds in nanoseconds with no software overhead. Also, the gate driver needs to source/sink amps of current to charge the MOSFET gate capacitance — an MCU GPIO pin can't do that.
</details>

**Q4:** What goes wrong if the error amplifier's compensation network makes the loop respond too fast?
<details>
<summary>Answer</summary>
The loop oscillates. A too-fast error amplifier overreacts to every small perturbation — by the time the power stage responds, the error amp has already swung the other way, creating ringing on the output. This is the classic stability problem in any negative feedback system: too much gain at high frequencies causes the phase to shift past 180°, turning negative feedback into positive feedback. See: The Key Tension.
</details>

**Q5:** In the comparator waveform diagram, the sawtooth ramp resets instantly to 0V. What would happen if the ramp were a triangle wave (ramp up then ramp down) instead of a sawtooth?
<details>
<summary>Answer</summary>
With a triangle wave, you'd get two intersection points per cycle — one on the rising edge and one on the falling edge — producing a pulse centered in the middle of the period rather than aligned to the start. This is actually used in some controllers (called "naturally sampled PWM") and produces lower harmonic distortion. Sawtooth (leading-edge or trailing-edge modulation) is simpler to implement and more common in power converters because it gives a single, unambiguous intersection point per cycle.
</details>

</details>
