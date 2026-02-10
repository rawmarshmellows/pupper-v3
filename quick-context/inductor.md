---
topic: Inductor
created: 2026-02-06
---

> **Related:** [[quick-context/electric-magnetic-field-unification|Field Unification]] | [[quick-context/electromagnetism]] | [[quick-context/electric-current]] | [[quick-context/electricity-generation]] | [[quick-context/capacitor]] | [[quick-context/resistor]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]

> **TL;DR:** An inductor stores energy in a magnetic field created by current flowing through a coil of wire, opposing any change in current—it's the magnetic counterpart to a [[quick-context/capacitor|capacitor]] (which stores energy in an electric field) and is essential for power supplies, filters, and energy conversion.

# Inductor

## The Core Problem: Smoothing and Converting Power

A switching power supply chops a DC voltage on and off millions of times per second. Without an inductor, you'd just get violent pulses of current. The inductor smooths these pulses into steady current by storing energy in its magnetic field during the "on" phase and releasing it during the "off" phase. Every phone charger, laptop adapter, and voltage regulator on every [[quick-context/pcb-printed-circuit-board|PCB]] depends on inductors to efficiently convert one voltage to another. They're also half of the LC resonant circuits used in radio tuning, and they form filters that block high-frequency noise while passing DC.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Inductance (L)** | The ability to store energy in a magnetic field per unit current change, measured in henrys (H). Most practical inductors are microhenrys (μH) to millihenrys (mH). |
| **Back-EMF** | The voltage an inductor generates to oppose changes in current: V = L × dI/dt. Try to suddenly stop current through an inductor and it generates a voltage spike (potentially destructive). |
| **Saturation Current** | The current at which the core's magnetic material can't hold any more flux—inductance drops sharply and the inductor stops working properly. Exceeding this is a common design mistake. |
| **DCR (DC Resistance)** | The resistance of the wire in the coil. Lower is better—DCR wastes power as heat. Thicker wire = lower DCR but larger inductor. |
| **Core Material** | What the coil is wound around. Air (no saturation, low inductance), ferrite (high inductance, saturates), powdered iron (good for power, gradual saturation). |

<details>
<summary><strong>How It Works</strong></summary>

When [[quick-context/electric-current|current]] flows through a wire, it creates a magnetic field around the wire (see [[quick-context/electromagnetism]]). Coiling the wire concentrates the field. The key behavior: an inductor resists changes to the current flowing through it—the exact opposite of a [[quick-context/capacitor|capacitor]], which resists changes in voltage.

```
INDUCTOR FUNDAMENTALS
══════════════════════════════════════════════════════════════════════════════

    Current flowing through a coil creates a magnetic field:

         ┌──⊃⊃⊃⊃⊃⊃⊃⊃──┐
    I →  │   ══════════  │  → I
         │   Magnetic    │
         │   field lines │
         └──────────────┘

    V = L × dI/dt    (voltage across inductor = inductance × rate of
                       current change)

    Key behaviors:
    • Constant current → V = 0  (inductor acts like a wire)
    • Increasing current → inductor opposes, generates negative voltage
    • Decreasing current → inductor opposes, generates positive voltage
    • Sudden current cutoff → HUGE voltage spike (V = L × dI/dt, dt≈0)


ENERGY STORAGE
══════════════════════════════════════════════════════════════════════════════

    E = ½ × L × I²

    Compare with capacitor: E = ½ × C × V²

    INDUCTOR                        CAPACITOR
    ────────                        ─────────
    Stores energy in magnetic       Stores energy in electric field
    field
    Opposes current changes         Opposes voltage changes
    Blocks AC, passes DC            Blocks DC, passes AC
    V = L × dI/dt                   I = C × dV/dt
    Series: L_total = L1 + L2       Series: 1/C = 1/C1 + 1/C2
    Parallel: 1/L = 1/L1 + 1/L2    Parallel: C_total = C1 + C2

    They're exact duals of each other!


RL TIME CONSTANT
══════════════════════════════════════════════════════════════════════════════

    τ = L / R    (compare with RC: τ = R × C)

       ┌───╱╱╱╱───⊃⊃⊃⊃───┐
       │     R       L     │
    Vs ┤                   │
       │                   │
       └───────────────────┘

    Current builds up exponentially:
    I(t) = (Vs/R) × (1 - e^(-t/τ))

    I                                    V across inductor
    ▲                                    ▲
    │            ─────────────          Vs│─┐
    │       ────                         │  └──
    │    ──                              │     ───
    │  ─                                 │        ────
    │─                                   │            ──────────
    └──┬──┬──┬──┬──► t                  └──┬──┬──┬──┬──► t
       1τ 2τ 3τ 5τ                        1τ 2τ 3τ 5τ

    At t=0: inductor blocks all current (acts like open circuit)
    At t=∞: inductor passes all current (acts like short circuit)
    Exactly opposite of a capacitor!
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Inductance vs. Size vs. Saturation vs. Loss

```
THE CORE TRADEOFFS
══════════════════════════════════════════════════════════════════════════════

    Want more inductance?  → More turns or bigger core → Larger size
    Want higher current?   → Bigger core (avoid saturation) → Larger size
    Want lower DCR?        → Thicker wire → Larger size
    Want higher frequency? → Fewer turns (lower inductance) → Core losses

    Everything pushes toward BIGGER. Inductors are usually the largest
    component on a power supply PCB.
```

| Type | Inductance | Current | Frequency | Best For |
|------|-----------|---------|-----------|----------|
| **Air core** | Very low (nH) | Unlimited (no saturation) | GHz | RF circuits, antennas |
| **Ferrite core** | High (μH-mH) | Limited by saturation | kHz-MHz | Power supplies, filters |
| **Powdered iron** | Medium (μH) | High (gradual saturation) | kHz-MHz | High-current power |
| **Toroidal** | High (contained field) | Medium-high | kHz-MHz | Low EMI, audio |
| **SMD power** | Low-medium (μH) | Medium | MHz | Compact DC-DC converters |
| **Molded/shielded** | Low-medium (μH) | Medium | MHz | Dense PCBs, low EMI |

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Buck Converter: Stepping Voltage Down Efficiently

The most common inductor application. A buck converter uses a switch, diode, inductor, and [[quick-context/capacitor|capacitor]] to step voltage down (e.g., 12V → 3.3V) at 85-95% efficiency—far better than a resistor voltage divider, which wastes the excess as heat.

```
BUCK CONVERTER OPERATION
══════════════════════════════════════════════════════════════════════════════

    Vin (12V) ──┬──╥──⊃⊃⊃⊃──┬─── Vout (3.3V)
                │  ║    L     │
              [SW] ║         ═╪═ C (output cap)
                │  ║          │
                ▼  ║         GND
              [D]  ║
                │  ║
               GND ║
                   ║
              Controller sets duty cycle: D = Vout/Vin = 3.3/12 = 27.5%


    PHASE 1: Switch ON (27.5% of cycle)
    ────────────────────────────────────
    Vin ──[ON]──⊃⊃⊃⊃──┬── Vout
                  L      │
         Current  ↑     ═╪═ C
         ramps UP        │
                        GND

    • Current flows from Vin through L to load
    • L stores energy in magnetic field (current increasing)
    • V_L = Vin - Vout = 8.7V (positive, current ramps up)


    PHASE 2: Switch OFF (72.5% of cycle)
    ─────────────────────────────────────
          [OFF]  ⊃⊃⊃⊃──┬── Vout
                  L      │
    GND ──[D]───┘       ═╪═ C
         Current  ↑      │
         ramps DOWN     GND

    • Switch opens, but inductor FORCES current to keep flowing
    • Current freewheels through diode
    • L releases stored energy (current decreasing)
    • V_L = -Vout = -3.3V (negative, current ramps down)


    INDUCTOR CURRENT WAVEFORM
    ─────────────────────────────────────
    I_L
     ▲    ╱╲      ╱╲      ╱╲
     │   ╱  ╲    ╱  ╲    ╱  ╲      ← "ripple" around average
     │──╱────╲──╱────╲──╱────╲──   ← average = load current
     │ ╱      ╲╱      ╲╱      ╲
     └──────────────────────────► t
       ON OFF  ON OFF  ON OFF

    The output capacitor smooths this ripple into steady DC.
```

**Why not just use a resistor to drop voltage?** A resistor dropping 12V to 3.3V at 1A would waste P = 8.7V × 1A = 8.7W as heat. The buck converter wastes only ~0.5W for the same job. At scale (millions of devices, 24/7 operation), this efficiency difference is enormous.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/capacitor]]** — Inductors and capacitors are exact duals: one stores energy in magnetic fields, the other in electric fields. Together they form LC resonant circuits (f = 1/(2π√LC)) and second-order filters.

- **[[quick-context/electric-current]]** — The inductor equation V = L×dI/dt means inductors care about current changes. Understanding current as charge flow is essential.

- **[[quick-context/resistor]]** — RL circuits (inductor + resistor) have a time constant τ = L/R, analogous to RC circuits. Real inductors always have parasitic resistance (DCR).

- **[[quick-context/pcb-printed-circuit-board]]** — Inductor placement matters: magnetic fields can couple into nearby traces. Power inductor layout is critical for switching power supply performance.

- **[[quick-context/thermal-noise-electronics]]** — Inductors don't generate thermal noise themselves (only resistive elements do), but their DCR contributes noise in sensitive circuits.

- **[[quick-context/electricity-generation]]** — Inductors are fundamental to electromagnetic generators. Faraday's law (EMF = -N × dΦ/dt) describes how changing magnetic flux through a coil induces voltage—the operating principle of virtually all grid electricity generation.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does an inductor generate a voltage spike when you suddenly interrupt its current?
<details>
<summary>Answer</summary>
**V = L × dI/dt. If dt approaches zero (instant cutoff), the voltage approaches infinity.** The inductor's magnetic field is collapsing and it will do whatever it takes to keep current flowing—even generating hundreds of volts across a small inductor. This is why flyback diodes are placed across inductive loads like motors and relays: they give the current a safe path to flow during turn-off.
</details>

**Q2:** An inductor and a capacitor are "duals." What does this mean practically?
<details>
<summary>Answer</summary>
**They have opposite behaviors in every way.** Capacitors block DC and pass AC; inductors pass DC and block AC. Capacitors oppose voltage changes; inductors oppose current changes. Their series/parallel formulas are swapped. Their time constant formulas are inverted (τ = RC vs τ = L/R). Together they create resonance at f = 1/(2π√LC).
</details>

**Q3:** A buck converter has Vin = 5V and needs Vout = 1.8V. What duty cycle is needed?
<details>
<summary>Answer</summary>
**36%.** Duty cycle D = Vout/Vin = 1.8/5 = 0.36 = 36%. The switch is ON for 36% of each cycle, during which the inductor charges, and OFF for 64%, during which it discharges.
</details>

**Q4:** Why are inductors typically the largest component on a power supply PCB?
<details>
<summary>Answer</summary>
**Magnetic energy storage requires physical volume.** More inductance needs more turns of wire. Higher current needs a larger core to avoid saturation. Lower losses need thicker wire (lower DCR). All of these push toward larger size. Unlike capacitors (which can be made very thin with ceramic layers), inductors fundamentally need 3D volume for their magnetic field.
</details>

**Q5:** What happens if you exceed an inductor's saturation current?
<details>
<summary>Answer</summary>
**Inductance drops sharply and current spikes uncontrollably.** The core material can't support any more magnetic flux, so the inductor stops opposing current changes and acts more like a short circuit (just its DCR). In a switching power supply, this means current shoots up, the switch transistor may overheat or blow, and output voltage regulation is lost. Always pick an inductor with saturation current above your maximum expected current.
</details>

</details>
