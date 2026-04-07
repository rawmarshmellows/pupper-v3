---
topic: Electricity Generation (How Electricity is Created)
created: 2026-02-06
---

> **Related:** [[quick-context/electromagnetism]] | [[quick-context/electric-current]] | [[quick-context/inductor]] | [[quick-context/galvanic-cells-batteries]] | [[quick-context/power-watts-joules]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]

> **TL;DR:** Electricity is created by converting other forms of energy into the directed flow of electrons—whether through chemical reactions (batteries), changing magnetic fields (generators), or photon absorption (solar cells). Over 99% of grid electricity comes from [[learning/notes/micro-context/electromagnetic-induction|electromagnetic induction]]: spin a coil in a magnetic field and electrons are forced to move.

# How Electricity is Created

## The Core Problem: Energy Conversion

Electricity doesn't exist freely in nature in a useful form. Lightning is too brief and uncontrollable. Static electricity dissipates instantly. To power civilization, we must *continuously convert* other energy forms into the sustained, controllable flow of electrons through circuits.

There are fundamentally three ways to force electrons to move:

1. **Chemical reactions** — Batteries exploit spontaneous redox reactions where certain atoms "want" to give up electrons while others "want" to accept them. See [[quick-context/galvanic-cells-batteries]].

2. **[[quick-context/electromagnetism|Electromagnetic induction]]** — Moving a conductor through a magnetic field (or changing the field around a conductor) forces electrons to flow. This powers 99%+ of grid electricity.

3. **Photovoltaic effect** — Photons knock electrons loose in semiconductor materials, creating current. Solar panels work this way.

Every power plant, battery, and solar panel is fundamentally an energy converter. Coal plants convert chemical energy → heat → mechanical motion → electricity. Hydroelectric dams convert gravitational potential → mechanical motion → electricity. The final step is almost always electromagnetic induction.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Electromagnetic Induction** | A changing magnetic field through a conductor induces [[learning/notes/quick-context/voltage|voltage]] and current. Discovered by Faraday (1831). The equation: EMF = -N × dΦ/dt (voltage equals turns times rate of magnetic flux change). This is how generators work. |
| **Generator** | A machine that converts mechanical rotation into electricity via electromagnetic induction. A coil spins inside a magnetic field (or magnets spin around a coil), inducing alternating current. |
| **Photovoltaic Effect** | When photons strike certain semiconductors, they knock electrons loose, creating current. Silicon solar cells achieve 20-25% efficiency; the theoretical maximum is ~33% (Shockley-Queisser limit). |
| **Turbine** | A rotary mechanical device that extracts energy from fluid flow (steam, water, wind) and converts it to rotation. The turbine spins the generator. |
| **Primary Energy Source** | The original energy form before conversion: coal, natural gas, nuclear fuel, sunlight, wind, falling water. Each gets converted through various steps into electricity. |

<details>
<summary><strong>How It Works</strong></summary>

```
THE THREE MECHANISMS FOR CREATING ELECTRICITY
══════════════════════════════════════════════════════════════════════════════

1. ELECTROMAGNETIC INDUCTION (Generators)
─────────────────────────────────────────
   Faraday's Law: EMF = -N × dΦ/dt

   "A changing magnetic flux through a coil induces a voltage."

         ┌─────────────────────────────────────┐
         │           GENERATOR                  │
         │                                      │
         │    N ══════════════════════ S       │
         │         ↑    COIL    ↑              │
         │         │  ┌──────┐  │              │
         │         │  │ ~~~~ │  │  ROTATION    │
         │         │  │ ~~~~ │◄─┼──────────    │
         │         │  │ ~~~~ │  │              │
         │         │  └──┬───┘  │              │
         │              │                      │
         │         ┌────┴────┐                 │
         │         │   AC    │                 │
         │         │ OUTPUT  │                 │
         │         └─────────┘                 │
         └─────────────────────────────────────┘

   As the coil rotates:
   • Magnetic flux through coil changes continuously
   • Changing flux induces voltage (Faraday's Law)
   • Voltage pushes electrons → current flows
   • One full rotation = one AC cycle

   WHAT SPINS THE GENERATOR?
   ┌────────────────────┬─────────────────────────────────┐
   │ Energy Source      │ What provides the rotation      │
   ├────────────────────┼─────────────────────────────────┤
   │ Coal/Gas/Nuclear   │ Heat → Steam → Steam turbine    │
   │ Hydroelectric      │ Falling water → Water turbine   │
   │ Wind               │ Moving air → Wind turbine       │
   │ Geothermal         │ Earth's heat → Steam turbine    │
   └────────────────────┴─────────────────────────────────┘


2. CHEMICAL (Batteries/Galvanic Cells)
──────────────────────────────────────
   See [[quick-context/galvanic-cells-batteries]] for full details.

         ANODE (-)              CATHODE (+)
            │                       │
            │    ←── e⁻ ←── e⁻ ←──  │
            │    ═══════════════    │
            │         WIRE          │
            │                       │
       ┌────┴────┐             ┌────┴────┐
       │   Zn    │             │   Cu    │
       │ oxidizes│             │ reduces │
       │ Zn→Zn²⁺ │             │ Cu²⁺→Cu │
       └─────────┘             └─────────┘
              ↑                     ↑
              └───── ELECTROLYTE ───┘
                    (ion pathway)

   • Oxidation at anode releases electrons
   • Electrons flow through external circuit (doing work)
   • Reduction at cathode consumes electrons
   • Ions flow through electrolyte to complete circuit

   Battery voltage = E°cathode - E°anode
   (Determined by electrode materials)


3. PHOTOVOLTAIC (Solar Cells)
─────────────────────────────
   Photon energy → Electron-hole pairs → Current

         SUNLIGHT (photons)
              │ │ │
              ▼ ▼ ▼
       ┌─────────────────────┐
       │ Anti-reflective     │
       │ coating             │
       ├─────────────────────┤  ← Metal contacts (collect e⁻)
       │ N-type silicon      │  ← Extra electrons (phosphorus doped)
       │ (negative)          │
       ├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┤  ← P-N JUNCTION (electric field)
       │ P-type silicon      │  ← Electron holes (boron doped)
       │ (positive)          │
       ├─────────────────────┤  ← Metal back contact
       └─────────────────────┘
              │
              ▼
         DC OUTPUT

   Step by step:
   1. Photon hits silicon, transfers energy to electron
   2. Electron knocked loose, leaves behind a "hole"
   3. Built-in electric field at P-N junction sweeps
      electrons toward N-side, holes toward P-side
   4. Metal contacts collect electrons → external circuit
   5. Electrons flow through circuit, return via back contact

   Efficiency limits:
   • Photons below bandgap energy: not absorbed (wasted)
   • Photons above bandgap: excess energy becomes heat
   • Theoretical max (single junction): ~33%
   • Practical silicon cells: 20-25%
```

</details>

<details>
<summary><strong>Generators and Inductors: The Same Physics</strong></summary>

## Faraday's Law Unifies Everything

Generators and [[quick-context/inductor|inductors]] are governed by the **exact same equation**—Faraday's Law. The difference is only what causes the magnetic flux to change:

```
FARADAY'S LAW: THE UNIVERSAL PRINCIPLE
══════════════════════════════════════════════════════════════════════════════

    EMF = -N × dΦ/dt

    EMF = induced voltage (volts)
    N   = number of turns in the coil
    Φ   = magnetic flux through the coil (webers)
    dΦ/dt = rate of change of flux

    The minus sign ([[quick-context/lenzs-law|Lenz's Law]]): induced voltage OPPOSES the change
    that created it. This is why inductors resist current changes
    and why generators require mechanical force to turn.


TWO APPLICATIONS OF THE SAME LAW:
══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────┐    ┌─────────────────────────────────┐
│         GENERATOR               │    │         INDUCTOR                │
├─────────────────────────────────┤    ├─────────────────────────────────┤
│                                 │    │                                 │
│  WHAT CHANGES THE FLUX?         │    │  WHAT CHANGES THE FLUX?         │
│  ─────────────────────────      │    │  ─────────────────────────      │
│  Mechanical rotation moves      │    │  Changing current through       │
│  the coil through a fixed       │    │  the coil changes the           │
│  magnetic field.                │    │  magnetic field it creates.     │
│                                 │    │                                 │
│       N ════════════ S          │    │      I(t) ──⊃⊃⊃⊃⊃⊃── I(t)      │
│          ┌──────┐               │    │              ║                  │
│          │ COIL │ ← rotates     │    │         Φ = L × I               │
│          │~~~~~~│               │    │              ║                  │
│          └──────┘               │    │         dΦ/dt = L × dI/dt       │
│                                 │    │                                 │
│  Φ changes because coil         │    │  Φ changes because current      │
│  orientation changes            │    │  magnitude changes              │
│                                 │    │                                 │
│  EMF = -N × dΦ/dt               │    │  V = -L × dI/dt                 │
│        ↓                        │    │      ↓                          │
│  OUTPUT: Electricity!           │    │  OUTPUT: Back-EMF               │
│  (converts motion → current)    │    │  (opposes current change)       │
│                                 │    │                                 │
└─────────────────────────────────┘    └─────────────────────────────────┘

    SAME EQUATION, DIFFERENT SOURCE OF dΦ/dt:
    • Generator: mechanical motion → dΦ/dt → EMF → current out
    • Inductor: current change → dΦ/dt → back-EMF → opposes the change


THE DEEP CONNECTION:
══════════════════════════════════════════════════════════════════════════════

    An inductor IS a generator where the "motion" is electrical, not mechanical.

    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │   GENERATOR                        INDUCTOR                            │
    │   ─────────                        ────────                            │
    │   Input: Mechanical work           Input: Changing current             │
    │          (turbine spinning)               (from power supply)          │
    │                 │                              │                       │
    │                 ▼                              ▼                       │
    │          ┌───────────┐                  ┌───────────┐                  │
    │          │ Faraday's │                  │ Faraday's │                  │
    │          │    Law    │                  │    Law    │                  │
    │          │ EMF=-NdΦ/dt                  │ V=-LdI/dt │                  │
    │          └───────────┘                  └───────────┘                  │
    │                 │                              │                       │
    │                 ▼                              ▼                       │
    │   Output: Electrical current           Output: Voltage that            │
    │           (powers the grid)                    opposes change          │
    │                                                (stores energy)         │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘


WHY THIS MATTERS FOR POWER SYSTEMS:
══════════════════════════════════════════════════════════════════════════════

    1. GENERATORS create electricity using Faraday's Law
       • Turbine spins coil in magnetic field
       • Changing flux induces voltage
       • Voltage drives current through the grid

    2. TRANSFORMERS transfer electricity using Faraday's Law
       • AC current in primary coil creates changing magnetic field
       • Changing field induces voltage in secondary coil
       • Allows stepping voltage up/down for efficient transmission
       • Only works with AC (needs dΦ/dt ≠ 0)

       Primary coil          Secondary coil
       ⊃⊃⊃⊃⊃⊃⊃              ⊃⊃⊃⊃⊃⊃⊃⊃⊃⊃⊃⊃
           ║ ══════════════════ ║
           ║   SHARED CORE      ║
           ║   (iron)           ║

       V₂/V₁ = N₂/N₁  (voltage ratio = turns ratio)

    3. INDUCTORS in power supplies use Faraday's Law
       • Buck/boost converters rely on inductor's back-EMF
       • When switch opens, inductor's collapsing field
         maintains current flow (energy release)
       • Smooths pulsed DC into steady DC

    4. MOTORS are generators in reverse
       • Current through coil in magnetic field → force
       • Force causes rotation (opposite of generator)
       • Same components, energy flows opposite direction


THE LENZ'S LAW INSIGHT:
══════════════════════════════════════════════════════════════════════════════

    The minus sign in EMF = -N × dΦ/dt is Lenz's Law:
    "The induced EMF opposes the change that caused it."

    In a GENERATOR:
    • Turning the shaft induces current
    • That current creates its own magnetic field
    • That field opposes the rotation (magnetic braking)
    • You must do WORK to overcome this opposition
    • This is how mechanical energy converts to electrical!

    In an INDUCTOR:
    • Increasing current tries to build magnetic field
    • Inductor generates back-EMF opposing the increase
    • This is why current rises slowly (τ = L/R)
    • Decreasing current releases stored magnetic energy
    • Inductor generates EMF trying to maintain current

    Conservation of energy enforced by Lenz's Law:
    • You can't get electrical energy without putting in mechanical work
    • You can't instantly change current without infinite voltage
    • Energy is stored in the magnetic field, not created or destroyed
```

**The one thing most outsiders get wrong about generators vs inductors:** They seem like completely different devices—one makes electricity, the other is a passive component. But they're both coils of wire exploiting the same physics. A generator has an *external* source of changing flux (mechanical rotation). An inductor creates its *own* flux from current, so changing the current changes the flux, inducing back-EMF. The "inductance" L is just a measure of how much flux a coil creates per amp of current (L = NΦ/I), which then determines how much voltage appears when current changes (V = L × dI/dt). Understanding this unity reveals why transformers work (mutual inductance between two coils), why motors and generators are reversible, and why inductors are essential in switching power supplies.

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Dispatchability vs. Sustainability

```
THE ENERGY TRILEMMA
══════════════════════════════════════════════════════════════════════════════

Every electricity source trades off between three goals:

                    RELIABLE
                   (on-demand)
                       ▲
                      /│\
                     / │ \
                    /  │  \
                   /   │   \
          Coal ●  /    │    \  ● Natural Gas
                 /     │     \
                /      │      \
               /       │       \
              /    Nuclear ●    \
             /         │         \
            /          │          \
           ▼───────────┴───────────▼
       CHEAP                    CLEAN
    (affordable)            (sustainable)

   Wind/Solar ● ─────────────────────→ Clean + increasingly cheap
                                       BUT intermittent

   Nuclear    ● ─────────────────────→ Clean + reliable
                                       BUT expensive, slow to build

   Natural Gas● ─────────────────────→ Reliable + cheaper than nuclear
                                       BUT CO₂ emissions

   Coal       ● ─────────────────────→ Cheap + reliable
                                       BUT high emissions
```

**The storage problem:** Solar produces peak power at noon; demand peaks in evening. Wind is unpredictable. Without massive energy storage (batteries, pumped hydro, hydrogen), renewables can't provide baseload power. This is why the grid still needs "dispatchable" sources (gas, nuclear, hydro) that can ramp up on demand.

| Source | Dispatchable? | Capacity Factor | CO₂ (g/kWh) |
|--------|---------------|-----------------|-------------|
| Coal | Yes | 40-50% | 820-1200 |
| Natural Gas | Yes | 40-60% | 410-520 |
| Nuclear | Yes (baseload) | 90%+ | 5-20 |
| Hydro | Yes | 30-50% | 4-30 |
| Wind | No | 25-45% | 7-15 |
| Solar PV | No | 15-25% | 20-50 |

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Following Electricity from Coal to Light Bulb

```
COAL POWER PLANT → YOUR LIGHT BULB
══════════════════════════════════════════════════════════════════════════════

1. CHEMICAL ENERGY (Coal)
─────────────────────────
   Coal = ancient plant matter, mostly carbon
   Energy stored in C-C and C-H bonds

   C + O₂ → CO₂ + HEAT (393 kJ/mol)

   1 kg of coal ≈ 24 MJ of chemical energy


2. THERMAL ENERGY (Boiler)
──────────────────────────
   ┌─────────────────────────────────┐
   │         BOILER                  │
   │   ┌─────────────────────┐       │
   │   │ Water tubes         │       │
   │   │    ○ ○ ○ ○ ○        │       │
   │   │      │ │ │          │ ← Heat from burning coal
   │   │    ○ ○ ○ ○ ○        │       │
   │   └─────────────────────┘       │
   │             │                   │
   │             ▼                   │
   │      HIGH-PRESSURE STEAM        │
   │      (540°C, 170 bar)           │
   └─────────────────────────────────┘

   η ≈ 90% (most heat transferred to steam)


3. MECHANICAL ENERGY (Turbine)
──────────────────────────────
   Steam expands through turbine blades
   Pressure drop → blade rotation

   ┌─────────────────────────────────────┐
   │              TURBINE                │
   │                                     │
   │   Steam →  ╱│╲  ╱│╲  ╱│╲  → Exhaust │
   │   (high P) ╲│╱  ╲│╱  ╲│╱   (low P)  │
   │              │    │    │            │
   │              └────┼────┘            │
   │                   │                 │
   │                   │ SHAFT           │
   │                   │ (3600 RPM)      │
   │                   ▼                 │
   └─────────────────────────────────────┘

   η ≈ 45% (Carnot limit for these temps)


4. ELECTRICAL ENERGY (Generator)
────────────────────────────────
   Shaft spins generator rotor
   Changing magnetic field induces current in stator

   ┌─────────────────────────────────────┐
   │            GENERATOR                │
   │                                     │
   │    ┌─────────────────────┐         │
   │    │ STATOR (stationary) │         │
   │    │  ┌───────────────┐  │         │
   │    │  │ ROTOR (spins) │  │ ← From turbine shaft
   │    │  │   N     S     │  │         │
   │    │  └───────────────┘  │         │
   │    └──────────┬──────────┘         │
   │               │                    │
   │          AC OUTPUT                 │
   │     (13.8 kV, 3-phase, 60 Hz)     │
   └─────────────────────────────────────┘

   η ≈ 98% (generators are very efficient)


5. TRANSMISSION
───────────────
   Step up → 345 kV (reduce I²R losses)
   Hundreds of miles of transmission lines
   Step down → 120V at your outlet

   η ≈ 93% (7% lost in transmission)


OVERALL EFFICIENCY:
───────────────────
   Coal → Heat:       90%
   Heat → Rotation:   45%
   Rotation → Elec:   98%
   Transmission:      93%
   ─────────────────────
   Total:             90% × 45% × 98% × 93% ≈ 37%

   For every 100 J of coal energy, ~37 J reaches your outlet.
   The rest is waste heat (mostly at the turbine stage).
```

**Comparison of generation methods:**

| Method | Energy Conversions | Overall Efficiency |
|--------|-------------------|-------------------|
| Coal/Gas | Chemical → Heat → Mechanical → Electrical | 33-45% |
| Nuclear | Nuclear → Heat → Mechanical → Electrical | 33-37% |
| Hydro | Gravitational → Mechanical → Electrical | 85-90% |
| Wind | Kinetic → Mechanical → Electrical | 35-45% (of wind energy) |
| Solar PV | Light → Electrical (direct!) | 20-25% |

Solar PV is unique: no moving parts, no intermediate conversions. Light directly creates electron flow. This simplicity is why solar costs have dropped 99% since 1976.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/electric-current]]** — Electricity generation creates current: the directed flow of electrons. Understanding current (I = Q/t) is essential for understanding what generators, batteries, and solar cells actually produce.

- **[[quick-context/galvanic-cells-batteries]]** — The chemistry of how batteries convert chemical potential energy to electrical energy. Batteries are the portable alternative to grid generation.

- **[[quick-context/electrolysis]]** — The reverse of batteries and a potential storage mechanism. Excess renewable electricity can electrolyze water into hydrogen, which can later be burned or run through fuel cells.

- **[[quick-context/power-watts-joules]]** — [[learning/notes/quick-context/power-watts-joules|Power (watts)]] is the rate of energy transfer. A 1 GW power plant generates 1 billion joules per second. Understanding power helps connect generation capacity to energy consumption.

- **[[quick-context/inductor]]** — Inductors are the key component in generators and transformers. They store energy in magnetic fields and are central to electromagnetic induction.

- **[[quick-context/capacitor]]** — Capacitors store energy in electric fields. Combined with inductors, they form the basis of AC power systems and grid stabilization.

- **[[quick-context/lenzs-law]]** — Why generators require mechanical work: the induced current creates magnetic fields that oppose the rotation, and overcoming this opposition is how mechanical energy converts to electrical.

- **[[quick-context/maxwell-equations]]** — The four equations that govern all electromagnetic phenomena, including Faraday's law of induction (which explains generators) and Ampère's law (which explains electromagnets).

- **[[quick-context/coil-magnetic-field]]** — Explains why current through a generator's coils creates magnetic fields, and how to calculate field strength. The B = μ₀nI formula governs electromagnet and generator design.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A wind turbine and a coal plant both use generators. What's fundamentally different about how they spin the generator?
<details>
<summary>Answer</summary>
**The energy source and conversion chain.** Coal burns to heat water into steam, which expands through a steam turbine connected to the generator (chemical → thermal → mechanical → electrical). Wind directly pushes turbine blades connected to the generator (kinetic → mechanical → electrical). The generator itself works identically in both cases—electromagnetic induction converts rotation to electricity. The difference is what provides the rotation.
</details>

**Q2:** Solar panels produce DC electricity, but the grid runs on AC. Why do we use AC for the grid instead of DC?
<details>
<summary>Answer</summary>
**AC can be easily transformed to different voltages.** Transformers only work with AC (they rely on changing magnetic fields). To minimize transmission losses (P = I²R), we step voltage up to hundreds of thousands of volts for long-distance transmission, then step it down for distribution and household use. With DC, voltage conversion requires expensive power electronics. Historically, AC won because transformers were cheap and efficient. Modern HVDC (high-voltage DC) is now used for very long distances and undersea cables, but the grid remains predominantly AC.
</details>

**Q3:** A nuclear plant and a coal plant have similar overall efficiencies (33-37%), yet nuclear produces almost no CO₂. Why the similar efficiency if the fuel is so different?
<details>
<summary>Answer</summary>
**Both are limited by the Carnot efficiency of their steam turbines.** Whether heat comes from burning coal or nuclear fission, both use that heat to boil water and spin a steam turbine. Carnot efficiency depends only on temperature difference: η = 1 - T_cold/T_hot. Both operate with similar steam temperatures (~300-550°C) and similar cold reservoir temperatures (cooling water ~30°C). The nuclear fuel is irrelevant to turbine efficiency—what matters is steam temperature. The CO₂ difference comes from the fuel: coal is carbon that becomes CO₂; uranium fission produces no carbon compounds.
</details>

**Q4:** Why can't we simply store solar electricity in giant capacitors instead of batteries?
<details>
<summary>Answer</summary>
**Capacitors have far lower energy density than batteries.** Energy stored in a [[learning/notes/quick-context/capacitor|capacitor]] is E = ½CV². Even supercapacitors store only ~5-10 Wh/kg, while lithium-ion batteries store 150-260 Wh/kg. To store a day's worth of solar production for a home (~30 kWh), you'd need 3-6 tons of supercapacitors vs. ~120 kg of lithium batteries. Capacitors excel at rapid charge/discharge (high power density) but can't hold much total energy. Batteries are the opposite: high energy density but slower charge/discharge. Grid storage needs energy density, so batteries win.
</details>

**Q5:** Hydroelectric dams achieve 85-90% efficiency while coal plants achieve only 33-37%. What's the fundamental reason for this difference?
<details>
<summary>Answer</summary>
**Hydro skips the thermal conversion step.** Coal plants must convert chemical energy to heat, then heat to mechanical motion. This thermal step is limited by Carnot efficiency (typically 40-45% for steam turbines). Hydro converts gravitational potential energy directly to mechanical rotation—water falling through turbines spins them directly. No heat engines means no Carnot limit. The only losses are friction in the turbines and generator inefficiency, both small. This is why hydro is the most efficient large-scale generation technology.
</details>

**Q6:** A generator and an [[learning/notes/quick-context/inductor|inductor]] both use coils of wire and both involve Faraday's Law. What's the fundamental difference in how they use the law?
<details>
<summary>Answer</summary>
**The source of the changing magnetic flux is different.** In a generator, mechanical rotation moves the coil through an external magnetic field—the flux changes because the coil's orientation changes. In an inductor, the coil creates its own magnetic field from the current flowing through it—the flux changes because the current changes (Φ = L × I, so dΦ/dt = L × dI/dt). Same equation (EMF = -N × dΦ/dt), but generator converts mechanical motion to electricity, while inductor opposes changes in current by generating back-EMF. See: Generators and Inductors section.
</details>

**Q7:** Transformers only work with AC, not DC. Using Faraday's Law, explain why.
<details>
<summary>Answer</summary>
**DC creates constant flux, and dΦ/dt = 0 means EMF = 0.** A transformer works by the primary coil creating a changing magnetic field that induces voltage in the secondary coil (EMF = -N × dΦ/dt). With AC, current continuously alternates, so flux continuously changes, so voltage is continuously induced. With DC, once current stabilizes, it creates a constant magnetic field—no change means no induced voltage in the secondary. You'd only get a brief pulse when DC is first applied (while current is rising). This is also why inductors "pass DC" after the initial transient—at steady state, dI/dt = 0, so V = L × dI/dt = 0.
</details>

</details>
