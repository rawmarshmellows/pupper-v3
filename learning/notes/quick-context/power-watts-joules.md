---
topic: Electrical Power (Watts, Joules, Energy)
created: 2026-02-06
---

> **Related:** [[learning/notes/micro-context/buck-converter]] | [[learning/notes/micro-context/power-inductor]] | [[learning/notes/micro-context/pwm-pulse-width-modulation]] | [[learning/notes/micro-context/decoupling-capacitor]] | [[learning/notes/micro-context/short-circuit]]

> **TL;DR:** Power (watts) is the rate at which energy (joules) is transferred or converted—P = V × I tells you how much work a circuit does per second, and understanding power is essential because every watt not delivered to the load becomes heat that must be managed, making thermal design the central constraint of modern electronics.

# Electrical Power

## The Core Problem: Where Does the Energy Go?

A phone charger pulls 10W from the wall but delivers only 8W to the battery. The missing 2W becomes heat—which is why chargers get warm. A CPU runs at 150W, and every watt not doing useful computation heats the chip. If the chip can't dissipate that heat, it throttles or dies. [[quick-context/electric-current|Current]] and [[learning/notes/quick-context/voltage|voltage]] alone don't tell you how much work is being done or how much heat is being generated. Power (P = V × I) answers both questions, and energy (E = P × t) tells you the total accumulated cost. Every electronic design is ultimately a thermal management problem.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Power (P)** | Rate of energy transfer, measured in watts (W). P = V × I = I²R = V²/R. One watt = one joule per second. |
| **Energy (E)** | Total work done, measured in joules (J). E = P × t. Your electricity bill is in kilowatt-hours (1 kWh = 3,600,000 J). |
| **Watt-hour (Wh)** | A practical energy unit: 1 Wh = 3600 J. A phone battery holds ~15 Wh. A laptop battery ~50 Wh. |
| **Efficiency (η)** | Pout / Pin × 100%. A 90%-efficient power supply converts 90W of input to useful output and wastes 10W as heat. |
| **Thermal Dissipation** | The process of removing waste heat. Every watt of loss must be carried away by conduction, convection, or radiation—or the temperature rises until something breaks. |

<details>
<summary><strong>How It Works</strong></summary>

```
THE POWER EQUATIONS
══════════════════════════════════════════════════════════════════════════════

    P = V × I         (fundamental: power = voltage × current)
    P = I² × R        (useful when you know current and resistance)
    P = V² / R        (useful when you know voltage and resistance)

    Energy = Power × Time
    E = P × t         (joules = watts × seconds)
    E = V × I × t     (joules = volts × amps × seconds)


WHERE POWER GOES IN A CIRCUIT
══════════════════════════════════════════════════════════════════════════════

    Power In (Pin)
        │
        ├──► Useful Work (Pout)
        │    • Motor spinning
        │    • LED emitting light
        │    • CPU computing
        │    • Radio transmitting
        │
        └──► Waste Heat (Ploss = Pin - Pout)
             • Resistive losses (I²R in wires, traces, switches)
             • Switching losses (transistors transitioning)
             • Quiescent current (circuits doing nothing but still drawing power)

    Efficiency: η = Pout / Pin × 100%


POWER RATINGS: WHY THEY MATTER
══════════════════════════════════════════════════════════════════════════════

    Component              │ Typical Rating  │ If Exceeded
    ───────────────────────┼─────────────────┼──────────────────
    SMD Resistor (0603)    │ 1/10 W          │ Burns/opens
    SMD Resistor (0805)    │ 1/8 W           │ Burns/opens
    Through-hole resistor  │ 1/4 W           │ Burns/opens
    LED                    │ 60-100 mW       │ Dims then dies
    Small transistor       │ 0.3-1 W         │ Overheats/shorts
    Voltage regulator      │ 1-15 W          │ Thermal shutdown
    CPU                    │ 15-300 W        │ Throttles then shuts down

    EXAMPLE: Linear voltage regulator dropping 12V to 5V at 1A

    Pin = 12V × 1A = 12W
    Pout = 5V × 1A = 5W
    Ploss = 12W - 5W = 7W → ALL becomes heat in the regulator!
    Efficiency = 5/12 = 42% → terrible

    This is why switching power supplies (using inductors) replaced
    linear regulators for most applications: 85-95% efficiency vs 42%.
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Power vs. Efficiency vs. Size (The Thermal Wall)

```
THE THERMAL CONSTRAINT
══════════════════════════════════════════════════════════════════════════════

    Temperature Rise = Power Dissipated × Thermal Resistance

    ΔT = P × Rθ

    Rθ (°C/W) depends on:
    • Package type (bare die, heatsink, fan)
    • Airflow (still air vs forced cooling)
    • PCB copper area (acts as a heatsink)

    EXAMPLE: IC dissipating 2W in a package with Rθ = 50°C/W
    ΔT = 2W × 50°C/W = 100°C above ambient
    If ambient = 25°C → chip runs at 125°C → near maximum!

    To run cooler: reduce power OR reduce thermal resistance
    (bigger heatsink, more airflow, better package)
```

| Power Source | Efficiency | Waste Heat | Use Case |
|-------------|-----------|-----------|----------|
| **Linear regulator** | 30-60% | High | Low-noise analog, <500 mA |
| **Buck converter** | 85-95% | Low | Step-down, most digital |
| **Boost converter** | 80-92% | Low | Step-up, battery-powered |
| **Class D amplifier** | 85-93% | Low | Audio amplification |
| **Class AB amplifier** | 50-70% | Medium-high | High-fidelity audio |

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Phone Charger: Tracing Power from Wall to Battery

```
POWER FLOW: WALL OUTLET → PHONE BATTERY
══════════════════════════════════════════════════════════════════════════════

    Wall Outlet (120V AC, 60Hz)
         │
         │  P = 12W from wall
         ▼
    ┌──────────────────┐
    │  Charger (AC→DC)  │  η = 88%
    │  120V AC → 5V DC  │  Ploss = 1.4W (charger gets warm)
    └────────┬─────────┘
             │  P = 10.6W on USB cable (5V × 2.1A)
             ▼
    ┌──────────────────┐
    │  USB Cable        │  Resistance: ~0.3Ω
    │  (1m, 28AWG)     │  Ploss = I²R = 2.1² × 0.3 = 1.3W
    └────────┬─────────┘   (cable gets warm at high current!)
             │  P = 9.3W reaching phone
             ▼
    ┌──────────────────┐
    │  Phone Charge IC  │  η = 92%
    │  (buck to 4.2V)  │  Ploss = 0.7W
    └────────┬─────────┘
             │  P = 8.6W into battery (4.2V × 2.0A)
             ▼
    ┌──────────────────┐
    │  Battery          │  15 Wh capacity
    │  (Li-ion)        │  Charge time ≈ 15Wh / 8.6W ≈ 1.7 hours
    └──────────────────┘

    Total efficiency: 8.6 / 12 = 72%
    Total waste heat: 3.4W spread across charger, cable, and phone

    This is why fast chargers use higher voltage (9V, 12V, 20V):
    same power at lower current → less I²R cable loss.
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/electric-current]]** — Power is the product of voltage and current (P = VI). Understanding current flow is prerequisite to understanding where power is consumed.

- **[[quick-context/resistor]]** — Every resistor in a circuit converts power to heat (P = I²R). Power ratings determine how much current a resistor can safely carry.

- **[[quick-context/inductor]]** — Switching power supplies use inductors to convert voltage efficiently. The inductor stores and releases energy each switching cycle, achieving 85-95% efficiency vs. 30-60% for linear regulators.

- **[[quick-context/capacitor]]** — Energy stored in a capacitor is E = ½CV². This is usually very small compared to batteries, but the power (rate of delivery) can be enormous because capacitors charge/discharge in nanoseconds.

- **[[quick-context/transistor]]** — CPU power consumption is dominated by switching power (P = C×V²×f) and leakage power. Both increase as transistors shrink, driving the "power wall" that ended single-core frequency scaling.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A USB device draws 500 mA at 5V. How much power does it consume?
<details>
<summary>Answer</summary>
**2.5W.** P = V × I = 5V × 0.5A = 2.5W. This is the standard USB 2.0 power budget per port.
</details>

**Q2:** A linear regulator converts 12V to 3.3V at 200 mA. How much power is wasted as heat?
<details>
<summary>Answer</summary>
**1.74W.** Pin = 12V × 0.2A = 2.4W. Pout = 3.3V × 0.2A = 0.66W. Ploss = 2.4 - 0.66 = 1.74W. Efficiency = 0.66/2.4 = 27.5%. This is why a buck converter (90%+ efficient) is preferred for large voltage drops.
</details>

**Q3:** Your phone battery is 15 Wh. At 4W average power consumption, how long does it last?
<details>
<summary>Answer</summary>
**3.75 hours.** Time = Energy / Power = 15 Wh / 4W = 3.75 hours. In practice it varies because power consumption fluctuates (screen brightness, radio activity, CPU load).
</details>

**Q4:** A [[learning/notes/quick-context/pcb-printed-circuit-board|PCB]] trace has 50 milliohms of resistance and carries 3A. How much power is wasted in the trace?
<details>
<summary>Answer</summary>
**0.45W.** P = I²R = 3² × 0.05 = 0.45W. This heats the trace. For a thin trace on FR-4, 0.45W could raise the temperature significantly. This is why high-current traces are made wider (lower resistance) or use multiple layers.
</details>

**Q5:** Why did fast charging standards move to higher voltages (9V, 12V, 20V) instead of higher current?
<details>
<summary>Answer</summary>
**To reduce I²R losses in the cable.** For the same power, doubling voltage halves current, which reduces cable heating by 4× (since P_loss = I²R). Delivering 60W at 5V requires 12A (massive cable losses), but 60W at 20V requires only 3A (manageable losses with standard cables). The phone internally converts the high voltage down to battery voltage using an efficient buck converter.
</details>

</details>
