---
topic: BJT (Bipolar Junction Transistor)
created: 2026-02-06
---

> **Related:** [[quick-context/bjt-specifications|BJT Specifications]] | [[quick-context/transistor]] | [[quick-context/doped-silicon]] | [[quick-context/transistor-design-history]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]

> **TL;DR:** A BJT is a current-controlled [[quick-context/transistor|transistor]] made from three layers of [[quick-context/doped-silicon|doped silicon]] (NPN or PNP) where a small base current controls a much larger collector-emitter current—still widely used in analog amplification, power switching, and current mirrors despite MOSFETs dominating digital electronics.

# BJT (Bipolar Junction Transistor)

## The Core Problem: Amplifying Signals With Current

MOSFETs are [[quick-context/voltage|voltage]]-controlled switches that dominate digital electronics (billions per chip). But BJTs—current-controlled amplifiers—still matter. When you need to amplify a weak analog signal (microphone, sensor), drive a relay or motor from a [[micro-context/microcontroller|microcontroller]] pin, or build a precise current reference, BJTs are often simpler and cheaper. A tiny current into the base (microamps) controls a much larger current through the collector (milliamps)—that's amplification. The [[quick-context/transistor-design-history|history of transistors]] started with BJTs in the 1950s, and while MOSFETs took over for digital, BJTs remain essential in analog and discrete power circuits.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **NPN / PNP** | The two BJT types. NPN: current flows collector→emitter when base current flows in. PNP: current flows emitter→collector when base current flows out. NPN is more common. |
| **Base (B)** | The control terminal. A small current into the base (for NPN) turns the [[quick-context/transistor|transistor]] on. Unlike a [[micro-context/mosfet|MOSFET]] gate, the base draws continuous current. |
| **Collector (C) / Emitter (E)** | The high-current terminals. Current flows from collector to emitter (NPN) when the transistor is on. The emitter has the arrow in the schematic symbol. |
| **Current Gain (β / hFE)** | Ic = β × Ib. Typical β = 50-300. A BJT with β=100 and Ib=100μA passes Ic=10mA. β varies with temperature and current—not a precision parameter, so designs use the *minimum* guaranteed value (see [[quick-context/bjt-specifications|BJT specifications]]). |
| **Saturation** | When the BJT is fully "on" (both junctions forward biased). Vce drops to ~0.1-0.3V. Used for switching. Contrast with the "active" region used for linear amplification. |

<details>
<summary><strong>How It Works</strong></summary>

An NPN BJT is a sandwich: N-type collector, thin P-type base, N-type emitter. It contains two PN junctions (like two [[quick-context/diode|diodes]] back-to-back), but the key is that the base layer is extremely thin—electrons injected from the emitter mostly shoot through the base into the collector instead of exiting through the base terminal.

```
NPN BJT STRUCTURE
══════════════════════════════════════════════════════════════════════════════

    Collector (C)
        │
    ┌───┴───┐
    │N-type │  ← Many electrons available
    ├───────┤
    │P-type │  ← Very thin! (~1μm)      ← Base (B)
    ├───────┤     Most electrons shoot through
    │N-type │  ← Electron source
    └───┬───┘
        │
    Emitter (E)


    SCHEMATIC SYMBOLS
    ═════════════════

         C                    C
         │                    │
    B ───┤               B ───┤
         │ →                  │ ←
         E                    E
        NPN                  PNP
    (arrow out             (arrow in
     of emitter)            to emitter)


THREE OPERATING REGIONS
══════════════════════════════════════════════════════════════════════════════

    CUTOFF (OFF):
    • Base-Emitter junction reverse biased (Vbe < 0.7V)
    • No base current → No collector current
    • Transistor acts like open switch
    • Vce ≈ Vcc (supply voltage)

    ACTIVE (LINEAR AMPLIFICATION):
    • Base-Emitter forward biased (Vbe ≈ 0.7V)
    • Collector-Base reverse biased
    • Ic = β × Ib (current amplification)
    • Used for analog circuits (amplifiers, filters)

    SATURATION (FULLY ON):
    • Both junctions forward biased
    • Vce ≈ 0.1-0.3V (nearly a short circuit)
    • Ic limited by external circuit, NOT by β × Ib
    • Used for switching (on/off, not linear)


    Ic
    ▲
    │         Saturation    ╱ Active region
    │        ┌─────────────╱   (Ic = β × Ib)
    │        │            ╱
    │   Ib3 ─┤───────────╱──────────────
    │        │          ╱
    │   Ib2 ─┤─────────╱───────────────
    │        │        ╱
    │   Ib1 ─┤───────╱────────────────
    │        │      ╱
    │        │     ╱  Cutoff (Ib = 0)
    └────────┴────╱─────────────────── Vce
               0.3V


BJT vs MOSFET COMPARISON
══════════════════════════════════════════════════════════════════════════════

    Property           │ BJT                    │ MOSFET
    ───────────────────┼────────────────────────┼──────────────────────
    Control            │ Current (Ib)           │ Voltage (Vgs)
    Input impedance    │ Low (draws current)    │ Nearly infinite
    Switching speed    │ Moderate               │ Fast
    Scalability        │ Hard to shrink         │ Billions per chip
    Analog precision   │ Higher transconductance│ Lower gm
    Power switching    │ Good for linear        │ Better for on/off
    Digital logic      │ Possible but wasteful  │ CMOS dominates
    Noise              │ Lower 1/f noise        │ Higher 1/f noise
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## When to Use BJT vs. MOSFET

```
USE A BJT WHEN:                        USE A MOSFET WHEN:
────────────────────                   ─────────────────────
• Driving small loads (<1A)            • Digital logic (always)
  from a microcontroller pin           • High-current switching (>1A)
• Analog amplification                 • Battery-powered (no gate current)
• Current mirrors/references           • High-speed switching
• You need cheap, simple,              • You need billions of them
  SOT-23 packages                        on a chip
• Low-noise analog front-ends          • Power MOSFETs have lower Rds(on)
```
 
The base current requirement is the BJT's biggest drawback for digital: in TTL logic, every gate draws continuous current from the previous stage. CMOS ([[quick-context/transistor|MOSFET-based]]) gates draw essentially zero static current, which is why CMOS won the digital war.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## BJT as a Switch: Driving a Motor from a Microcontroller

A microcontroller GPIO pin can only source ~20 mA. A small motor needs 200 mA. A BJT bridges the gap.

```
MOTOR DRIVER CIRCUIT
══════════════════════════════════════════════════════════════════════════════

                        +12V ──────────┐
                         │            │
                    ┌────┴────┐       │
                    │  MOTOR  │       ├┤◄── Flyback diode
                    │    M    │       │     (1N4001)
                    └────┬────┘       │
                         │            │
              C ─────────┴────────────┘
              │
    MCU Pin ──╱╱╱╱──┤►  NPN (2N2222)
               Rb   │
                    E
                    │
                   GND

    DESIGN CALCULATION:
    ────────────────────

    Motor current (Ic) = 200 mA
    BJT β (minimum guaranteed) = 100
    Required base current: Ib = Ic / β = 200mA / 100 = 2 mA

    But for reliable saturation, use 2-5x more base current:
    Ib_design = 5 mA

    MCU output = 3.3V, Vbe = 0.7V
    Rb = (3.3V - 0.7V) / 5mA = 520Ω → use standard 470Ω

    Power dissipated in BJT (saturated):
    P = Vce_sat × Ic = 0.2V × 200mA = 40 mW  (negligible)

    MCU pin sources only 5 mA but controls 200 mA → 40x amplification


    WHY THE FLYBACK DIODE?
    ──────────────────────

    Motors are inductive loads. When the BJT turns off,
    the motor's inductance tries to keep current flowing
    (V = L × dI/dt, with dt→0, V→huge).

    Without diode: voltage spike destroys the BJT
    With diode: current circulates safely through the diode
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/bjt-specifications]]** — The buyer's checklist: the five datasheet numbers (type, V_CEO, I_C, P_C, β) you verify before dropping a BJT into a circuit, with a worked 2N2222 relay-driver example. This note is the *physics*; that one is the *selection*.

- **[[quick-context/transistor]]** — The MOSFET is the BJT's sibling. Understanding one helps understand the other. MOSFETs are voltage-controlled; BJTs are current-controlled. Same purpose (switching/amplification), different physics.

- **[[quick-context/doped-silicon]]** — BJTs are built from three alternating layers of N-type and P-type silicon. The thin base region is what makes amplification possible.

- **[[quick-context/transistor-design-history]]** — BJTs were the dominant transistor from the 1950s through 1980s. The shift to CMOS (MOSFET-based) digital logic happened because MOSFETs don't draw static current and scale better.

- **[[quick-context/diode]]** — A BJT contains two PN junctions. The base-emitter junction behaves like a [[quick-context/diode|diode]] (0.7V forward drop). You can even use the B-E junction as a temperature sensor.

- **[[quick-context/resistor]]** — Base resistors are essential for BJT circuits. They set the bias current and prevent excessive base current from damaging the transistor or the driving circuit.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** An NPN BJT has β = 150 and Ib = 100μA. What is Ic (in the active region)?
<details>
<summary>Answer</summary>
**15 mA.** Ic = β × Ib = 150 × 100μA = 15,000μA = 15 mA. This is only valid in the active region—if the load resistance limits current below this, the BJT is in saturation and Ic < β × Ib.
</details>

**Q2:** Why does a BJT base always draw current, but a MOSFET gate doesn't?
<details>
<summary>Answer</summary>
**The BJT base-emitter junction is a forward-biased diode.** Current must flow through this junction to inject carriers into the base that get swept to the collector. A MOSFET gate is separated from the channel by an insulating oxide layer—it's a [[quick-context/capacitor|capacitor]], not a diode. Charge flows to charge/discharge the gate [[quick-context/capacitance|capacitance]], but no DC current flows through it.
</details>

**Q3:** What does "saturation" mean for a BJT, and how is it different from MOSFET saturation?
<details>
<summary>Answer</summary>
**Confusingly, they mean opposite things.** BJT saturation = fully ON (both junctions forward biased, Vce ≈ 0.2V, maximum current). MOSFET saturation = the region where drain current is relatively constant regardless of Vds (used for amplification). BJT saturation is like MOSFET "linear/triode" region. This naming inconsistency is a historical accident.
</details>

**Q4:** Why is a flyback diode necessary when switching an inductive load with a BJT?
<details>
<summary>Answer</summary>
**Inductors generate voltage spikes when current is interrupted.** V = L × dI/dt. When the BJT turns off, the motor's inductance tries to maintain current flow by generating a large reverse voltage—potentially hundreds of volts. This exceeds the BJT's collector-emitter breakdown voltage and destroys it. The flyback diode provides a path for the inductive current to circulate safely as the magnetic field collapses.
</details>

**Q5:** A digital circuit needs 50 million transistors. Why can't you build it with BJTs?
<details>
<summary>Answer</summary>
**Power consumption.** Each BJT gate draws continuous base current, even when idle. With 50 million gates, the total idle power would be enormous—and the heat would be unmanageable. CMOS (complementary MOSFETs) draws essentially zero static power because MOSFET gates don't need DC current. CMOS only draws current during switching transitions, making billion-transistor chips thermally feasible.
</details>

</details>
