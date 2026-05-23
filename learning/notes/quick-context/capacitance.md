---
topic: Capacitance
created: 2026-03-28
---

# Capacitance

> **Related:** [[quick-context/capacitor]] | [[quick-context/impedance-and-reactance]] | [[quick-context/voltage]] | [[quick-context/electric-current]]

> **TL;DR:** Capacitance is the ability of any two conductors separated by an insulator to store electric charge -- measured in farads ($C = Q/V$) -- and it shows up everywhere in electronics, not just in discrete [[quick-context/capacitor|capacitors]]: [[quick-context/pcb-printed-circuit-board|PCB]] traces, transistor gates, cable shields, and even bare wires all have parasitic capacitance that limits speed, causes crosstalk, and determines how fast signals can switch.

## The Core Problem

Every pair of conductors separated by an insulator has capacitance. Discrete [[quick-context/capacitor|capacitors]] exploit this intentionally, but *parasitic* capacitance -- the unintended capacitance baked into every wire, trace, connector, and [[quick-context/transistor|transistor]] gate -- is what limits how fast digital circuits can switch, how far analog signals can travel without distortion, and how much power a CPU burns. Understanding capacitance as a *property of geometry and materials* (not just a component spec) is the key to understanding signal integrity, switching speed, and power dissipation in modern electronics.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Farad (F)** | The unit of capacitance. 1 farad = 1 coulomb stored per volt applied ($C = Q/V$). Practical values range from femtofarads (fF, transistor gates) through picofarads (pF, PCB traces) to microfarads ($\mu$F, [[micro-context/decoupling-capacitor|decoupling caps]]). |
| **Parasitic Capacitance** | Unintended capacitance between conductors in a circuit -- PCB traces, IC pins, wire bundles. Always present, often dominant at high frequencies, and the primary speed limiter in digital circuits. |
| **Dielectric Constant ($\varepsilon_r$)** | How much a material amplifies capacitance compared to vacuum. Air: ~1. FR-4 ([[quick-context/pcb-printed-circuit-board|PCB]] substrate): ~4.5. Silicon dioxide (transistor gate): ~3.9. Higher $\varepsilon_r$ = more capacitance for same geometry. |
| **$C = \varepsilon A / d$** | The parallel-plate formula: capacitance scales with plate area ($A$) and [[quick-context/voltage|dielectric constant]] ($\varepsilon$), and inversely with plate separation ($d$). This governs both intentional and parasitic capacitance. |
| **Miller Capacitance** | The effective input capacitance of an amplifying stage, multiplied by $(1 + \text{gain})$. A 2 pF drain-gate capacitance in a [[quick-context/transistor|transistor]] with gain of 50 looks like ~102 pF at the input, severely limiting switching speed. |

<details>
<summary><strong>How It Works</strong> -- Capacitance as a geometric property</summary>

Capacitance exists whenever two conductors are separated by an insulator. It doesn't matter whether you intended to create a capacitor -- the physics doesn't care. The key equation is:

$$C = \frac{\varepsilon_0 \cdot \varepsilon_r \cdot A}{d}$$

Where:
- $\varepsilon_0$ = permittivity of free space ($8.85 \times 10^{-12}$ F/m)
- $\varepsilon_r$ = relative permittivity (dielectric constant) of the insulator
- $A$ = overlapping area of the two conductors
- $d$ = distance between them

```
CAPACITANCE IS EVERYWHERE
==============================================================================

INTENTIONAL (discrete capacitors):

    ┌──────────────────┐
    │ Metal plate      │
    ├══════════════════╡  C = εA/d
    │ Dielectric       │  Designed for specific value
    ├══════════════════╡
    │ Metal plate      │
    └──────────────────┘


PARASITIC (unintended, unavoidable):

    1. TWO PCB TRACES RUNNING PARALLEL
    ─────────────────────────────────────────────────────────

         Trace A  ════════════════════════════  signal
                   d (gap)
         Trace B  ════════════════════════════  signal

         Longer traces, closer spacing, higher-ε substrate
         → more coupling capacitance → more crosstalk


    2. PCB TRACE OVER GROUND PLANE
    ─────────────────────────────────────────────────────────

         Signal trace  ════════════════════════
         ─ ─ ─ ─ ─ ─ ─ FR-4 substrate ─ ─ ─ ─  εr ≈ 4.5
         Ground plane   ══════════════════════════════════

         This capacitance is actually useful:
         it sets the trace's characteristic impedance
         (Z₀ depends on L and C per unit length)


    3. TRANSISTOR GATE (the critical one)
    ─────────────────────────────────────────────────────────

              Gate (metal)
         ┌──────────────────────┐
         ├══════════════════════╡  Gate oxide (~1-2 nm!)
         │ Channel (silicon)    │  C_gate = ε × A / d
         └──────────────────────┘
                                   d is nanometers → C is significant
                                   THIS capacitance must charge/discharge
                                   every time the transistor switches

         Switching speed ∝ 1/C_gate
         Power consumption ∝ C_gate × V² × f


    4. IC PIN AND PACKAGE
    ─────────────────────────────────────────────────────────

         ┌──────────────┐
         │     IC       │
         │     die      │    Bond wire + package pin + PCB pad
         │              │    all add parasitic capacitance
         └──┬──┬──┬──┬──┘    Typically 2-15 pF per pin
            │  │  │  │
         ═══╪══╪══╪══╪═══   PCB pads
            │  │  │  │
```

### Why Parasitic Capacitance Limits Speed

To change the [[quick-context/voltage|voltage]] on any node, you must charge or discharge its capacitance. The equation $I = C \times dV/dt$ means:

$$\text{Switching time} \approx \frac{C \times \Delta V}{I_{\text{drive}}}$$

More capacitance on a node means:
- More [[quick-context/electric-current|current]] needed to switch at the same speed, or
- Slower switching with the same drive current, or
- More [[quick-context/power-watts-joules|power]] consumed at the same speed ($P = C V^2 f$)

```
WHY CAPACITANCE = SPEED LIMIT
==============================================================================

    Digital signal switching a node with capacitance C:

    Drive current I ──►┌────────┐
                       │        │───► Output
                       │ Driver │     │
                       │        │    ═╪═ C (parasitic)
                       └────────┘     │
                                      GND

    Time to switch from 0V to VDD:

        t_switch = C × VDD / I

    EXAMPLE: Switching a 10 pF node from 0V to 1V with 1 mA:

        t = 10×10⁻¹² × 1 / 1×10⁻³ = 10 ns

    Double the parasitic C → double the switching time (or double the current)


    THIS IS WHY TRANSISTOR SHRINKING MATTERS:
    ──────────────────────────────────────────────────────────────────────────

    Smaller transistors → smaller gate area → less C_gate → faster switching

    Node       │ Gate Length │ Approx. C_gate │ Relative Speed
    ═══════════╪════════════╪════════════════╪═══════════════
    180 nm     │ 180 nm     │ ~1 fF          │ 1×
    45 nm      │ 45 nm      │ ~0.3 fF        │ ~3×
    7 nm       │ 7 nm       │ ~0.05 fF       │ ~20×
    (FinFET)   │            │                │

    But parasitic capacitance from wires doesn't shrink as fast
    → at small nodes, wire capacitance dominates over gate capacitance
```

### Capacitance in Series and Parallel

Like [[quick-context/resistor|resistors]], capacitances combine -- but with inverted rules:

```
COMBINING CAPACITANCES
==============================================================================

    PARALLEL (most parasitic capacitances add this way):

        ═╪═ C1
         │
    ─────┼──── Node
         │
        ═╪═ C2

        C_total = C1 + C2    (capacitances ADD)

        Every extra trace, pin, or pad on a node adds to its total C.


    SERIES (less common, used in capacitor dividers):

    ──┤├──┤├──
      C1   C2

        1/C_total = 1/C1 + 1/C2

        C_total = (C1 × C2) / (C1 + C2)    (always LESS than smallest)
```

### Why Daisy Chains Have a Device Limit

Every device connected to a shared signal line adds its input capacitance in parallel. This is the direct consequence of the parallel rule above: $C_{\text{total}} = C_1 + C_2 + C_3 + \ldots$. Add enough devices and the total bus capacitance becomes so large that the signal can't transition fast enough to be read correctly.

The clearest real-world example is [[micro-context/i2c|I2C]]. Each device on the bus adds ~10 pF of input capacitance (from its pin, bond wire, ESD protection diode, and PCB pad). The [[micro-context/i2c|I2C]] spec caps total bus capacitance at **400 pF** -- beyond that, the open-drain pull-up [[quick-context/resistor|resistors]] can't charge the line fast enough for the clock to reach a valid HIGH before the next edge.

```
WHY DAISY CHAINS HIT A WALL
==============================================================================

    I2C BUS: open-drain with pull-up resistors
    ──────────────────────────────────────────────────────────────────────────

        VCC
         │
        ┌┴┐  R_pullup (e.g. 4.7 kΩ)
        └┬┘
         │
    SDA ─┼──────┬──────┬──────┬──────┬──────┬─── ...
         │      │      │      │      │      │
        ═╪═    ═╪═    ═╪═    ═╪═    ═╪═    ═╪═   Each device adds
        ~10pF  ~10pF  ~10pF  ~10pF  ~10pF  ~10pF parasitic C to the bus
         │      │      │      │      │      │
        GND    GND    GND    GND    GND    GND

    C_total = N × C_device + C_trace

    With 30 devices: C_total ≈ 30 × 10 pF + 50 pF (traces) = 350 pF  ✓ OK
    With 40 devices: C_total ≈ 40 × 10 pF + 50 pF (traces) = 450 pF  ✗ Over spec!


    THE PHYSICS: Why more capacitance kills the signal
    ──────────────────────────────────────────────────────────────────────────

    I2C uses open-drain drivers: devices pull the line LOW actively,
    but rely on a passive pull-up resistor to bring it back HIGH.

    Pulling LOW (fast):                Pulling HIGH (slow — the bottleneck):

        Device shorts line to GND        Pull-up resistor must charge
        through a transistor (~10Ω)      total bus C through R

        SDA ──┐                              VCC
              │                               │
              └──── GND                     ┌─┴─┐
                                            │ R │ (4.7 kΩ)
        t_fall ≈ tiny                       └─┬─┘
        (low-impedance switch)                │
                                         SDA ─┼── C_total
                                              │
                                             GND

                                         t_rise ≈ 0.85 × R × C_total
                                         (time from 30% to 70% of VDD)

    EXAMPLE:
        R = 4.7 kΩ, C_total = 100 pF  →  t_rise ≈ 400 ns     ✓ Fast enough
        R = 4.7 kΩ, C_total = 400 pF  →  t_rise ≈ 1593 ns    ≈ Limit
        R = 4.7 kΩ, C_total = 800 pF  →  t_rise ≈ 3186 ns    ✗ Too slow

    At 400 kHz (fast mode I2C), the clock period is 2500 ns.
    If rise time eats >1000 ns of that, the receiver can't reliably
    distinguish HIGH from LOW → communication errors.


    THE GENERAL PATTERN (applies to any shared bus):
    ──────────────────────────────────────────────────────────────────────────

    Protocol    │ Bus C limit  │ ~C per device │ Practical device limit
    ════════════╪══════════════╪═══════════════╪════════════════════════
    I2C (std)   │ 400 pF       │ ~10 pF        │ ~30 devices
    I2C (fast+) │ 550 pF       │ ~10 pF        │ ~50 devices
    SPI (MISO)  │ No spec, but │ ~5-15 pF      │ ~10-20 before signal
                │ degrades     │               │ integrity suffers
    UART        │ No spec      │ ~5 pF         │ Usually point-to-point
    CAN bus     │ Driver-      │ ~15 pF        │ ~30-110 nodes
                │ dependent    │ (transceiver) │ (depends on bit rate)

    WORKAROUNDS when you hit the limit:
    • Lower the pull-up resistance (faster charge, but more power)
    • Use a bus buffer/repeater (resets capacitance at each segment)
    • Reduce clock speed (more time for transitions)
    • Switch to a protocol with active drivers (SPI, CAN)
    • Use bus expanders (I2C multiplexers like TCA9548A)
```

The key insight: **the 400 pF I2C limit isn't arbitrary -- it's a direct consequence of $t_{\text{rise}} = RC$.** The pull-up resistor and total bus capacitance form an RC circuit. More devices = more C = slower rise time = eventually the signal can't keep up with the clock. This is parasitic capacitance in parallel, setting a hard ceiling on how many devices can share a wire.

</details>

<details>
<summary><strong>The Key Tension</strong> -- Capacitance you want vs. capacitance you don't</summary>

The fundamental tension in electronics is that the same physical phenomenon -- charge storage between conductors -- is both essential and parasitic:

| You WANT capacitance for... | You DON'T want capacitance because... |
|---|---|
| [[micro-context/decoupling-capacitor|Decoupling]] (local energy storage) | It slows down signal transitions |
| Filtering (frequency selectivity) | It couples noise between traces (crosstalk) |
| Energy storage | It increases dynamic [[quick-context/power-watts-joules|power]] ($P = CV^2f$) |
| Setting [[quick-context/impedance-and-reactance|impedance]] (transmission lines) | Miller effect multiplies it at amplifier inputs |
| Timing circuits ([[quick-context/rc-oscillator|RC oscillators]], time constants) | It limits I/O speed at package pins |

```
THE SPEED-POWER-NOISE TRIANGLE
==============================================================================

    Every parasitic capacitance forces a choice:

                        SPEED
                          ▲
                         / \
                        /   \
                       /     \
                      /       \
                     /  Pick   \
                    /   two     \
                   /             \
            POWER ◄───────────────► NOISE
            (low)                 (low)

    To go FASTER with same C: drive harder → more power
    To use LESS POWER with same C: switch slower → latency
    To reduce CROSSTALK NOISE: space traces apart → larger PCB, longer traces

    The only real win is reducing C itself:
    • Thinner gate oxide (but leakage increases)
    • Low-κ dielectrics between metal layers
    • Shorter interconnects (better floorplanning)
    • Smaller transistors (but wire C eventually dominates)
```

</details>

<details>
<summary><strong>Concrete Example</strong> -- [[micro-context/mosfet|MOSFET]] gate capacitance and dynamic power</summary>

The most consequential capacitance in modern electronics is the gate capacitance of a [[quick-context/transistor|MOSFET transistor]]. Every time a transistor switches, its gate capacitance must be charged (0 → VDD) or discharged (VDD → 0). In a processor with billions of transistors switching billions of times per second, this is where most of the power goes.

```
DYNAMIC POWER IN A CMOS INVERTER
==============================================================================

    VDD ────┬────────────────────
            │
         ┌──┴──┐
         │PMOS │  (pulls output to VDD when input = 0)
         └──┬──┘
            │
    In ─────┤────── Out
            │        │
         ┌──┴──┐    ═╪═ C_load (gate cap of next stage
         │NMOS │     │         + wire parasitic)
         └──┬──┘    GND
            │
    GND ────┴────────────────────


    Every time "In" transitions:

    0→1: NMOS turns on, discharges C_load to GND
         Energy dissipated = ½ × C_load × VDD²

    1→0: PMOS turns on, charges C_load to VDD
         Energy drawn from VDD = C_load × VDD²
         (half stored in C, half dissipated in PMOS resistance)

    Per full cycle: E = C_load × VDD²

    At frequency f:

        P_dynamic = C_load × VDD² × f

    REAL NUMBERS:
    ─────────────────────────────────────────────────────────────────────

    Modern CPU: ~25 billion transistors (e.g. Apple M4, Intel 13th gen)
    Average C_load per gate: ~1 fF (10⁻¹⁵ F)
    Not all switch every cycle. Activity factor α ≈ 0.1
    VDD = 0.8V, f = 4 GHz

    P = α × N × C × VDD² × f
    P = 0.1 × 2.5×10¹⁰ × 10⁻¹⁵ × 0.64 × 4×10⁹
    P = 0.1 × 2.5×10¹⁰ × 10⁻¹⁵ × 2.56×10⁹
    P ≈ 6.4 W  (just for gate switching -- real CPUs have wire C too)

    Total with wire parasitics, leakage, etc.: 50-150W typical


    WHY VOLTAGE REDUCTION MATTERS SO MUCH:
    ─────────────────────────────────────────────────────────────────────

    P ∝ VDD²  (voltage SQUARED!)

    VDD    │ Relative Power │ Why we can't just keep dropping V
    ═══════╪════════════════╪════════════════════════════════════
    1.0V   │ 1.00×          │
    0.8V   │ 0.64×          │ 36% power savings!
    0.6V   │ 0.36×          │ But transistors switch slower
    0.4V   │ 0.16×          │ Noise margins shrink dangerously
    0.2V   │ 0.04×          │ Transistors barely turn on/off

    Capacitance × voltage² is why "voltage scaling" has been
    the #1 trick for reducing chip power for decades.
```

**The one thing most outsiders get wrong about this is...** thinking capacitance only matters when you're using a discrete capacitor component. In reality, the parasitic capacitance of wires, traces, and transistor gates dominates modern circuit behavior. A 5 cm PCB trace can have 2-5 pF of capacitance to the ground plane (depending on trace width and dielectric thickness) -- comparable to a small ceramic capacitor. A CPU's total gate capacitance (summed across billions of transistors) determines its power consumption more than any other single factor. The [[quick-context/capacitor|capacitor components]] on your board are the capacitance you *chose*; the parasitic capacitance is the capacitance physics *imposed* -- and the parasitic kind is usually what limits your design.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/capacitor]]** -- The component that exploits capacitance intentionally. Covers types (ceramic, electrolytic, tantalum), charge/discharge curves, time constants, and the critical role of [[micro-context/decoupling-capacitor|decoupling capacitors]] in digital circuits.

- **[[quick-context/impedance-and-reactance]]** -- Capacitance creates frequency-dependent opposition to current: $X_C = 1/(2\pi fC)$. This is why capacitors pass high frequencies and block low frequencies, and why parasitic capacitance matters more at higher frequencies.

- **[[quick-context/inductor]]** -- The electromagnetic dual of capacitance. Inductance stores energy in magnetic fields and opposes current changes; capacitance stores energy in electric fields and opposes voltage changes. Together they create resonance at $f = 1/(2\pi\sqrt{LC})$.

- **[[quick-context/frequency-and-filtering]]** -- Capacitance is the basis of all passive filters. The cutoff frequency $f_c = 1/(2\pi RC)$ directly depends on capacitance value.

- **[[quick-context/transistor]]** -- Gate capacitance ($C_{gs}$, $C_{gd}$) determines switching speed and dynamic power. Miller capacitance ($C_{gd}$ multiplied by gain) is the dominant speed limiter in analog amplifiers.

- **[[quick-context/pcb-printed-circuit-board]]** -- PCB trace geometry creates parasitic capacitance that sets characteristic impedance, causes crosstalk between traces, and affects signal integrity at high frequencies.

- **[[quick-context/voltage]]** -- [[quick-context/voltage|Voltage]] is what drives charge onto capacitance ($Q = CV$). The energy stored in any capacitance is $E = \frac{1}{2}CV^2$ -- voltage squared makes this highly sensitive to supply voltage.

- **[[quick-context/power-watts-joules]]** -- Dynamic power $P = CV^2f$ directly ties capacitance to energy consumption. Reducing capacitance is one of the few ways to reduce power without sacrificing speed or voltage.

- **[[quick-context/capacitive-sensing-measurement]]** -- How capacitance is actually *measured* in sensors (humidity, accelerometers, touchscreens). Covers the three measurement families: RC timing, sigma-delta charge-balance, and AC impedance.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A PCB trace is 10 cm long, running 0.2 mm above a ground plane on FR-4 (dielectric constant ~4.5). Roughly, does it have more or less capacitance than a trace that's 0.4 mm above the ground plane?
<details>
<summary>Answer</summary>
**More capacitance -- roughly double.** From $C = \varepsilon A / d$, halving the distance $d$ doubles the capacitance. The 0.2 mm trace has about twice the capacitance per unit length as the 0.4 mm trace. This also means lower characteristic impedance (since $Z_0 \propto \sqrt{L/C}$). PCB stackup design is fundamentally about controlling this parasitic capacitance.
</details>

**Q2:** Why does $P = CV^2f$ mean that reducing voltage is more effective than reducing capacitance for power savings?
<details>
<summary>Answer</summary>
**Because voltage is squared.** Cutting voltage in half reduces power by 4x ($0.5^2 = 0.25$), while cutting capacitance in half only reduces power by 2x. That's why voltage scaling has been the dominant power reduction technique in chip design. However, voltage can't drop below the threshold voltage of the transistors, so eventually capacitance reduction (smaller transistors, low-k dielectrics) becomes the only option. See: Concrete Example.
</details>

**Q3:** Two parallel PCB traces each contribute 3 pF of parasitic capacitance to a signal node. A 10 pF decoupling capacitor is also connected. What's the total capacitance the driver must charge?
<details>
<summary>Answer</summary>
**16 pF.** Capacitances in parallel add: 3 + 3 + 10 = 16 pF. The driver must supply $I = C \times dV/dt = 16 \text{ pF} \times dV/dt$ to change the node voltage. This is why parasitic capacitance budgeting matters -- every additional trace, pin, or component on a node adds to the total load. See: How It Works (Combining Capacitances).
</details>

**Q4:** A MOSFET has 2 pF of gate-drain capacitance ($C_{gd}$) and a voltage gain of 100. Why does the input see 200 pF, not 2 pF?
<details>
<summary>Answer</summary>
**Miller effect.** When the gate voltage changes by $\Delta V$, the drain swings by $-100 \times \Delta V$ (inverted by the gain). The voltage across $C_{gd}$ changes by $(1 + 100) \times \Delta V = 101 \times \Delta V$. The current through $C_{gd}$ is therefore 101x what you'd expect from 2 pF alone, making it look like ~200 pF from the input's perspective. This is why high-gain amplifier stages are slower than their raw gate capacitance would suggest. See: 5 Essential Terms (Miller Capacitance).
</details>

**Q5:** As transistors shrink to 3 nm and below, wire (interconnect) capacitance increasingly dominates over gate capacitance. Why doesn't shrinking the transistor also shrink the wire capacitance proportionally?
<details>
<summary>Answer</summary>
**Wires don't scale the same way as transistors.** [[quick-context/transistor|Transistor]] gate area shrinks with the square of the feature size, directly reducing gate capacitance. But interconnect wires must still span the full chip to connect distant blocks -- you can make them thinner, but then resistance increases (more delay, more [[quick-context/electromigration|electromigration]] risk). And thinner wires packed closer together actually *increase* capacitance between neighbors ($C = \varepsilon A / d$ with smaller $d$). The semiconductor industry now spends more effort on "back-end" interconnect optimization (low-k dielectrics, air gaps between wires) than on transistor improvements.
</details>

</details>
