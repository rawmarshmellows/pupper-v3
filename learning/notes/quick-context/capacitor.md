---
topic: Capacitor
created: 2026-01-30
---

# Capacitor

> **Related:** [[learning/notes/micro-context/decoupling-capacitor]]

> **TL;DR:** A capacitor stores energy in an electric field between two conductive plates separated by an insulator; unlike batteries that store chemical energy and release it slowly, capacitors store electrical energy directly and can charge/discharge almost instantly, making them essential for stabilizing power supplies, filtering signals, and enabling [[learning/notes/quick-context/transistor|transistor]] switching.

## The Core Problem

Electronics need stable voltage to operate correctly, but power supplies fluctuate, digital circuits draw sudden bursts of [[quick-context/electric-current|current]], and signals contain unwanted noise. Capacitors solve these problems by acting as tiny, fast-responding energy reservoirs. When voltage rises, capacitors absorb excess charge; when voltage dips, they release stored charge to fill the gap. This happens in nanoseconds - far faster than any battery or power supply can respond. Without capacitors, your computer's CPU would crash from voltage fluctuations every time millions of [[quick-context/transistor|transistors]] switched simultaneously. The humble capacitor is what keeps digital circuits from descending into electrical chaos.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **[[quick-context/capacitance|Capacitance]] (C)** | The ability to store charge per unit voltage, measured in farads (F). C = Q/V. A 1-farad capacitor stores 1 coulomb of charge at 1 volt. Most capacitors are microfarads (uF) to picofarads (pF). |
| **Dielectric** | The insulating material between the capacitor's plates that determines [[learning/notes/quick-context/capacitance|capacitance]] and voltage rating. Common dielectrics: ceramic, tantalum, aluminum oxide, silicon dioxide (in [[quick-context/transistor|transistors]]). |
| **Charge (Q)** | The amount of electrical charge stored, measured in coulombs. Q = C x V. More capacitance or higher voltage means more stored charge. |
| **Time Constant (RC)** | The product of resistance and capacitance that determines how fast a capacitor charges/discharges. After one time constant (tau = RC), a capacitor reaches ~63% of its final voltage. |
| **Decoupling/Bypass Capacitor** | A capacitor placed near an IC to provide instant current during switching and filter high-frequency noise from the power supply - the most common capacitor application in digital electronics. |

<details>
<summary><strong>How It Works</strong></summary>

A capacitor consists of two conductive plates separated by an insulator (dielectric). When you apply voltage across the plates, electrons accumulate on one plate (making it negative) and are depleted from the other plate (making it positive). This charge separation creates an electric field stored in the dielectric. The field itself holds energy - no chemical reaction needed, unlike [[quick-context/galvanic-cells-batteries|batteries]].

```
BASIC CAPACITOR STRUCTURE AND OPERATION
================================================================================

                         NO VOLTAGE APPLIED
                    ──────────────────────────────

                    ┌─────────────────────────────┐
                    │    PLATE A (conductor)      │  No charge buildup
                    └─────────────────────────────┘
                    ╔═════════════════════════════╗
                    ║     DIELECTRIC (insulator)  ║  No electric field
                    ╚═════════════════════════════╝
                    ┌─────────────────────────────┐
                    │    PLATE B (conductor)      │  No charge buildup
                    └─────────────────────────────┘


                         VOLTAGE APPLIED (+V on A, 0V on B)
                    ──────────────────────────────────────────

                        (+) Terminal connected ────┐
                                                   │
                    ┌─────────────────────────────┐│
                    │+ + + + + + + + + + + + + + +││  Electrons pulled away
                    │    PLATE A (positive)       ││  (net positive charge)
                    └─────────────────────────────┘│
                    ╔═════════════════════════════╗│
                    ║  ↓ ↓ ↓ ELECTRIC FIELD ↓ ↓ ↓ ║│  Energy stored HERE
                    ╚═════════════════════════════╝│  in the field
                    ┌─────────────────────────────┐│
                    │- - - - - - - - - - - - - - -││  Electrons accumulate
                    │    PLATE B (negative)       ││  (net negative charge)
                    └─────────────────────────────┘│
                                                   │
                        (-) Terminal connected ────┘


KEY INSIGHT: The dielectric BLOCKS electron flow between plates, but the
electric field passes through it. Charge can't cross - it just accumulates.


ENERGY STORAGE COMPARISON:
══════════════════════════════════════════════════════════════════════════════

              CAPACITOR                         BATTERY
              ─────────                         ───────
              Energy in electric field          Energy in chemical bonds

              ┌───┐   ←Field→   ┌───┐          ┌─────────────────────┐
              │ + │             │ - │          │ Chemical reactions  │
              │ + │   electric field   │ - │          │ slowly release      │
              │ + │  ═══════════│ - │          │ electrons           │
              └───┘             └───┘          └─────────────────────┘

              Charge/discharge:                 Charge/discharge:
              Nanoseconds to milliseconds       Minutes to hours

              Energy density:                   Energy density:
              Low (0.01-0.1 Wh/kg)             High (100-250 Wh/kg)

              Power density:                    Power density:
              Very high (instant delivery)      Limited by reaction rate

              Cycle life:                       Cycle life:
              Millions of cycles                Hundreds to thousands
```

### The Fundamental Equation: Q = CV

Everything about capacitors flows from one equation: **Q = C × V**

- **Q** (charge in coulombs) = how many electrons have accumulated
- **C** (capacitance in farads) = the capacitor's "size" for storing charge
- **V** (voltage in volts) = the electrical pressure across the plates

```
THE CAPACITOR EQUATION AND ITS IMPLICATIONS
══════════════════════════════════════════════════════════════════════════════

BASIC FORM:     Q = C × V        (Charge = Capacitance × Voltage)

REARRANGED:     C = Q/V          (Capacitance = Charge per Volt)
                V = Q/C          (Voltage = Charge divided by Capacitance)


WHAT DETERMINES CAPACITANCE:
────────────────────────────────────────────────────────────────────────────

                        ε × A
                C  =  ─────────
                          d

    Where:
    • ε = dielectric constant (permittivity) of insulator material
    • A = plate area (larger plates = more capacitance)
    • d = plate separation (closer plates = more capacitance)

    ┌───────────────────────────────────────────────────────────────────────┐
    │                                                                       │
    │   SMALL CAPACITANCE           LARGE CAPACITANCE                       │
    │                                                                       │
    │   ┌────┐     Small A          ┌──────────────────┐  Large A           │
    │   │    │                      │                  │                    │
    │   └────┘     Large d          └──────────────────┘  Small d           │
    │      ↕                              ↕                                 │
    │   ╔════╗                      ╔══════════════════╗                    │
    │      ↕                              ↕                                 │
    │   ┌────┐                      ┌──────────────────┐                    │
    │   │    │                      │                  │                    │
    │   └────┘                      └──────────────────┘                    │
    │                                                                       │
    │   C = small                   C = large                               │
    │                                                                       │
    └───────────────────────────────────────────────────────────────────────┘


ENERGY STORED IN A CAPACITOR:
────────────────────────────────────────────────────────────────────────────

                    1           1   Q²
    Energy  =  ─── C V²  =  ─── ────
                    2           2   C

    EXAMPLE: 100 μF capacitor at 5V

    E = 0.5 × (100 × 10⁻⁶) × 5² = 0.00125 J = 1.25 mJ

    That's tiny! This is why capacitors can't replace batteries for
    bulk energy storage - but they're perfect for brief current bursts.
```

### Current Flow: Charging and Discharging

Capacitors don't pass DC current (the dielectric blocks it), but they appear to conduct during voltage changes. When voltage rises, current flows IN to deposit charge. When voltage falls, current flows OUT as charge leaves.

```
CHARGING AND DISCHARGING THROUGH A RESISTOR
══════════════════════════════════════════════════════════════════════════════

                    ┌────╱╱╱╱────┐
                    │      R     │
        Vs ─────────┤            ├─────── GND
                    │    ┌──┐    │
                    └────┤  ├────┘
                         │C │
                         └──┘

    Time constant: τ = R × C


CHARGING (switch to Vs):
─────────────────────────────────────────────────────────────────────────────

    Voltage across capacitor              Current into capacitor

    V                                     I
    ▲                                     ▲
    │                                     │
 Vs │........................─────────    │I₀ ─┐
    │              ───────               │    │
    │         ────                        │    └───
    │      ──                             │        ───
    │    ─                                │           ────
    │  ─                                  │              ─────
    │ ─                                   │                   ────────────
    │─                                    │
    └──┬──┬──┬──┬──┬──┬──┬──► t          └──┬──┬──┬──┬──┬──┬──► t
       1τ 2τ 3τ 4τ 5τ                       1τ 2τ 3τ 4τ 5τ

    V(t) = Vs × (1 - e^(-t/RC))          I(t) = (Vs/R) × e^(-t/RC)

    At t = 1τ: V = 63.2% of Vs            At t = 1τ: I = 36.8% of I₀
    At t = 3τ: V = 95% of Vs              At t = 3τ: I = 5% of I₀
    At t = 5τ: V = 99.3% of Vs            At t = 5τ: I = 0.7% of I₀


DISCHARGING (switch to GND):
─────────────────────────────────────────────────────────────────────────────

    Voltage across capacitor              Current out of capacitor

    V                                     I
    ▲                                     ▲
    │                                     │
 Vs │─┐                                 0 ├────────────────────────────────
    │  └──                                │             ────────────
    │     ───                             │         ────
    │        ────                         │     ────
    │            ─────                    │────
    │                 ──────              │ ───┐
    │                       ───────────   │    │
    │                                     │    └─ -I₀ (negative = flowing out)
    └──┬──┬──┬──┬──┬──┬──┬──► t          └──┬──┬──┬──┬──┬──┬──► t
       1τ 2τ 3τ 4τ 5τ                       1τ 2τ 3τ 4τ 5τ

    V(t) = Vs × e^(-t/RC)                I(t) = -(Vs/R) × e^(-t/RC)


PRACTICAL EXAMPLE:
─────────────────────────────────────────────────────────────────────────────

    R = 10 kΩ, C = 100 μF, Vs = 5V

    τ = 10,000 × 0.0001 = 1 second

    Charging from 0V to 5V:
    • After 1 second: 3.16V (63%)
    • After 3 seconds: 4.75V (95%)
    • After 5 seconds: 4.97V (99.3%)

    Initial charging current: I₀ = 5V / 10kΩ = 0.5 mA
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Size vs. Speed vs. Voltage Rating

Capacitor design involves fundamental tradeoffs that practitioners constantly navigate:

```
THE THREE-WAY TRADEOFF
══════════════════════════════════════════════════════════════════════════════

                         CAPACITANCE
                              ▲
                             /│\
                            / │ \
                           /  │  \
                          /   │   \
                         /    │    \
                        /     │     \
                       /      │      \
                      /       │       \
                     /        │        \
            SPEED ◄──────────────────────► SIZE/COST
                    \         │         /
                     \        │        /
                      \       │       /
                       \      │      /
                        \     │     /
                         \    │    /
                          \   │   /
                           \  │  /
                            \ │ /
                             \│/
                         VOLTAGE
                         RATING


WANT MORE CAPACITANCE?
──────────────────────────────────────────────────────────────────────────────
• Increase plate area → Larger physical size, higher cost
• Decrease plate separation → Lower voltage rating (dielectric breakdown)
• Use higher-ε dielectric → Often worse temperature stability, more leakage


WANT FASTER RESPONSE (lower ESR/ESL)?
──────────────────────────────────────────────────────────────────────────────
• Use ceramic instead of electrolytic → Smaller capacitance per volume
• Shorter internal connections → More expensive construction
• Multiple small caps in parallel → Takes more PCB space


WANT HIGHER VOLTAGE RATING?
──────────────────────────────────────────────────────────────────────────────
• Thicker dielectric → Lower capacitance for same size
• Better dielectric material → Higher cost
```

### Capacitor Types and Their Tradeoffs

| Type | Capacitance Range | Voltage Range | Speed (ESR) | Best Use Case |
|------|------------------|---------------|-------------|---------------|
| **Ceramic (MLCC)** | 1 pF - 100 uF | 6V - 100V | Excellent (<10 mOhm) | Decoupling, high-frequency filtering |
| **Aluminum Electrolytic** | 1 uF - 10,000 uF | 6V - 450V | Poor (10-1000 mOhm) | Bulk energy storage, power supply filtering |
| **Tantalum** | 100 nF - 1000 uF | 2V - 50V | Good (10-100 mOhm) | Medium density where size matters |
| **Film** | 100 pF - 10 uF | 50V - 2000V | Good | Audio, high-voltage, precision |
| **Supercapacitor** | 0.1 F - 1000+ F | 2.5V - 5V | Poor | Energy storage, backup power |

```
WHY YOU CAN'T HAVE IT ALL: The Electrolytic vs. Ceramic Example
══════════════════════════════════════════════════════════════════════════════

    ELECTROLYTIC CAPACITOR              CERAMIC CAPACITOR (MLCC)
    (Aluminum foil + oxide layer)       (Ceramic layers + metal electrodes)

    ┌─────────────────────────────┐     ┌─────────────────────────────┐
    │  Aluminum foil (etched for  │     │═══════════════════════════  │
    │  surface area)              │     │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
    │  ░░░░░░░░░░░░░░░░░░░░░░░░░  │     │═══════════════════════════  │
    │  Aluminum oxide (dielectric)│     │  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
    │  ░░░░░░░░░░░░░░░░░░░░░░░░░  │     │═══════════════════════════  │
    │  Electrolyte (conductor)    │     │                             │
    │  ░░░░░░░░░░░░░░░░░░░░░░░░░  │     │  ═══ = ceramic dielectric   │
    │  Aluminum foil              │     │  ─ ─ = metal electrode      │
    │                             │     │                             │
    │  Rolled into cylinder       │     │  Flat chip package          │
    └─────────────────────────────┘     └─────────────────────────────┘

    ✓ High capacitance (1000s μF)       ✓ Low ESR (fast response)
    ✓ High voltage (up to 450V)         ✓ Small size
    ✗ High ESR (slow, lossy)            ✓ No polarity concerns
    ✗ Polarity sensitive                ✗ Limited capacitance (<100μF)
    ✗ Large size                        ✗ Capacitance varies with voltage!
    ✗ Liquid dries out over time        ✗ Can crack from thermal stress


TYPICAL PCB POWER SUPPLY FILTERING:
══════════════════════════════════════════════════════════════════════════════

    Power    Bulk         Local Decoupling
    Input    Storage      (next to each IC)
      │        │               │
      ▼        ▼               ▼
    ─┬─      ─┬──┬─          ─┬──┬──┬─
     │        │  │            │  │  │
    ═╪═      ═╪══╪═          ═╪══╪══╪═
     │        │  │            │  │  │
    ─┴─      ─┴──┴─          ─┴──┴──┴─

    100-1000μF   10-100μF      0.1μF (100nF)
    Electrolytic Electrolytic  Ceramic

    Handles      Handles       Handles
    low-freq     medium-freq   high-freq
    ripple       transients    noise

    Each stage catches what the previous one can't handle.
    This is why you see BOTH electrolytics AND ceramics on every board.
```

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Decoupling Capacitors: Keeping CPUs from Crashing

Every [[quick-context/pcb-printed-circuit-board|PCB]] with digital ICs is covered in small ceramic capacitors placed next to chip power pins. These "decoupling" or "bypass" capacitors are the unsung heroes preventing circuit chaos.

```
THE PROBLEM: SUDDEN CURRENT DEMANDS
══════════════════════════════════════════════════════════════════════════════

When a transistor switches, it briefly draws a spike of current.
When MILLIONS switch simultaneously, the demand is enormous.

    Without decoupling:

    Power Supply ────────────────────────────── CPU
    (far away)        ~10cm of trace/wire      (needs instant current)
       │                     │
       │    L = ~10nH        │    Millions of transistors
       │    R = ~10mΩ        │    switch in 1 nanosecond
       │                     │
       └─ Slow response!     └─ V = L × di/dt = HUGE voltage drop!

    Example:
    • CPU needs 100A current spike in 1ns
    • Inductance of power trace: 10 nH
    • Voltage drop: V = L × (di/dt) = 10×10⁻⁹ × (100/10⁻⁹) = 1000V !!!

    That's insane! CPU would see 0V or negative voltage → CRASH


THE SOLUTION: LOCAL CHARGE RESERVOIR
══════════════════════════════════════════════════════════════════════════════

    Power Supply ────────╥────────────────────── CPU
                         ║                        │
                         ║                        │
                     ┌───╨───┐                ┌───┴───┐
                     │ 100μF │                │ 0.1μF │
                     │       │                │       │ ← Right next to
                     └───┬───┘                └───┬───┘   CPU power pins
                         │                        │
                        GND                      GND

    Bulk cap              Decoupling caps
    (refills from         (provide INSTANT current)
     power supply)


    How it works:

    1. CPU transistors switch → demand sudden current

    2. Decoupling cap (right next door) provides current INSTANTLY
       - Very low inductance (short path)
       - Voltage drop: V = L × di/dt with L < 0.1nH → millivolts, not kilovolts
       - Cap voltage drops slightly as it discharges

    3. Bulk cap refills decoupling cap over next few nanoseconds

    4. Power supply refills bulk cap over next few microseconds

    Each stage handles a different timescale!


REAL CPU POWER DELIVERY:
══════════════════════════════════════════════════════════════════════════════

    Modern CPUs have HUNDREDS of decoupling capacitors:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                          CPU DIE                                        │
    │                         ┌───────┐                                       │
    │                         │       │                                       │
    │                         │       │                                       │
    │                         └───────┘                                       │
    │    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●       │
    │                                                                         │
    │    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●       │
    │                          PACKAGE                                        │
    │    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●       │
    │                                                                         │
    │    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●       │
    │         ● = decoupling capacitor (inside package AND on PCB!)           │
    └─────────────────────────────────────────────────────────────────────────┘

    Some capacitors are even INSIDE the CPU package, between die and BGA balls.
    Why? Even the ~5mm from PCB to die is too much inductance for fastest
    transients.

    TYPICAL DECOUPLING SCHEME FOR A 100W CPU:

    Location          │ Type      │ Capacitance │ Quantity │ Purpose
    ──────────────────┼───────────┼─────────────┼──────────┼─────────────────
    Inside package    │ Ceramic   │ 10-100 nF   │ 100s     │ Fastest transients
    PCB under CPU     │ Ceramic   │ 100 nF-10μF│ 50-100   │ Fast transients
    Near VRM          │ Ceramic   │ 1-22 μF     │ 10-20    │ Medium transients
    VRM input         │ Electro.  │ 100-1000 μF │ 5-10     │ Bulk storage


DECOUPLING FAILURE - WHAT GOES WRONG:
══════════════════════════════════════════════════════════════════════════════

    Symptom                  │ Likely Cause
    ─────────────────────────┼────────────────────────────────────────────────
    Random crashes/resets    │ Missing or wrong value decoupling caps
    Works at low speed,      │ Inadequate high-frequency decoupling
    crashes at high speed    │
    Intermittent errors      │ Cracked ceramic cap (thermal cycling)
    Gets worse when hot      │ Electrolytic cap ESR increases with temp
    Gets worse when cold     │ Ceramic cap loses capacitance at low temp
```

**The one thing most outsiders get wrong about this is...** thinking capacitors are just "smoothing" or "filtering." In digital circuits, decoupling capacitors are **local energy storage** - they're tiny batteries that can discharge in nanoseconds. The CPU doesn't draw smooth, constant current; it draws violent spikes every time transistors switch. No power supply, no matter how good, can respond fast enough. The capacitors aren't filtering anything out - they're actively injecting current into the circuit to fill demand that the power supply can't meet in time. Without them, every fast digital circuit would fail.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/transistor]]** - The transistor's gate-oxide-semiconductor structure forms a MOS capacitor. Understanding capacitors is essential for understanding how transistors switch: applying gate voltage charges this capacitor, creating the electric field that forms the channel.

- **[[quick-context/electric-current]]** - Current and capacitors are intimately related. Current equals the rate of charge flow: I = dQ/dt = C × dV/dt. A capacitor only "conducts" when voltage is changing.

- **[[quick-context/parallel-vs-series-voltage]]** - Explains why decoupling capacitors are critical for CPU power delivery and how they handle sudden current demands that would otherwise cause voltage drops.

- **[[quick-context/galvanic-cells-batteries]]** - Both store energy, but through fundamentally different mechanisms. Batteries: chemical energy, high density, slow. Capacitors: electric field energy, low density, instant response.

- **[[quick-context/pcb-printed-circuit-board]]** - PCB design heavily revolves around capacitor placement. Power planes act as distributed capacitance, and decoupling cap placement is critical for signal integrity.

- **[[quick-context/thermal-noise-electronics]]** - Capacitors have a fundamental noise floor: V_noise = sqrt(kT/C). This limits how small DRAM storage capacitors can be, because thermal noise would overwhelm the stored signal.

- **[[quick-context/capacitance]]** — Capacitance as a fundamental property of geometry and materials, including parasitic capacitance in PCB traces, transistor gates, and IC packages — the unintended capacitance that limits speed and determines power consumption.

- **[[quick-context/rc-oscillator|RC Oscillator]]** -- [[learning/notes/quick-context/resistor|Resistor]]-capacitor timing circuits generate repeating waveforms (sawtooth, square) by charging C through R to a threshold, then resetting. The same RC time constant that governs filters also sets oscillation frequency.

- **RC Circuits and Filters** - Resistor-capacitor combinations form the basis of analog signal processing: low-pass filters, high-pass filters, integrators, and differentiators.

- **[[small-context/permanent-magnet-creation]]** - Capacitor discharge circuits store energy at high voltage (E = ½CV²) then release it in milliseconds to create 15,000+ amp pulses for magnetizing iron. A practical example of how capacitors enable high-power applications from low-power sources.

- **[[quick-context/capacitive-sensing-measurement]]** -- How capacitive sensors (humidity, MEMS accelerometers, touchscreens) measure capacitance changes using RC timing, sigma-delta CDCs, and AC impedance techniques. The RC charge/discharge curve described above is the mathematical basis of the simplest measurement family.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A 100 uF capacitor and a 10 uF capacitor are both charged to 5V. Which one stores more energy?
<details>
<summary>Answer</summary>
**The 100 uF capacitor stores 10x more energy.** Energy = 0.5 × C × V². For 100 uF at 5V: E = 0.5 × 100×10⁻⁶ × 25 = 1.25 mJ. For 10 uF at 5V: E = 0.5 × 10×10⁻⁶ × 25 = 0.125 mJ. When voltage is the same, energy scales directly with capacitance. See: How It Works (Energy Stored section).
</details>

**Q2:** Why do PCBs have both large electrolytic capacitors and small ceramic capacitors for power supply filtering?
<details>
<summary>Answer</summary>
**They handle different frequency ranges due to different ESR/ESL characteristics.** Electrolytics have high capacitance for bulk energy storage but high ESR/ESL, so they respond slowly (good for low-frequency ripple). Ceramics have low capacitance but very low ESR/ESL, so they respond nearly instantly (good for high-frequency transients). Using both covers the full frequency spectrum. See: The Key Tension (typical PCB power supply filtering diagram).
</details>

**Q3:** A capacitor in an RC circuit has R = 1 kOhm and C = 10 uF. How long does it take to charge to approximately 95% of the supply voltage?
<details>
<summary>Answer</summary>
**About 30 milliseconds (3 time constants).** Time constant tau = RC = 1000 × 10×10⁻⁶ = 0.01 seconds = 10 ms. At t = 3tau = 30 ms, the capacitor reaches 95% of final voltage. At 5tau (50ms), it reaches 99.3%. See: How It Works (Charging and Discharging section).
</details>

**Q4:** An engineer removes all the 0.1 uF ceramic capacitors near a CPU to "simplify the design." What will likely happen?
<details>
<summary>Answer</summary>
**The system will crash, produce errors, or fail to boot.** Without decoupling capacitors, sudden current demands from switching transistors cause massive voltage drops due to power trace inductance (V = L × di/dt). The CPU sees voltage dipping below its minimum operating level, causing logic errors or complete failure. This is especially true at high clock speeds where current transients are faster and more severe. See: Concrete Example (The Problem: Sudden Current Demands).
</details>

**Q5:** Why do DRAM chips need to be "refreshed" periodically, and how do capacitors relate to this requirement?
<details>
<summary>Answer</summary>
**DRAM stores bits as charge on tiny capacitors (~20 fF), and that charge slowly leaks away.** Each memory cell is just a capacitor and a transistor. The capacitor holds charge (bit = 1) or doesn't (bit = 0). But capacitors aren't perfect insulators - small leakage currents drain the charge over milliseconds. Without periodic refresh (reading and rewriting each cell), the stored data would be lost. This is also why DRAM loses all data when power is removed. The [[quick-context/thermal-noise-electronics|thermal noise]] floor (V = sqrt(kT/C)) also limits how small these capacitors can be - shrink them too much and thermal noise overwhelms the signal. See: Peripheral Knowledge (thermal noise link).
</details>

</details>
