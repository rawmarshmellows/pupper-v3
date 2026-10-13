---
topic: Fundamental Electronic Parts — Index
created: 2026-02-06
updated: 2026-02-07
---
> **Related:** [[learning/notes/quick-context/melt-index]]


> **[[learning/notes/quick-context/3d-printer-hotends|Related:]]** [[quick-context/pcb-chip-transistor-hierarchy]] | [[quick-context/transistor]] | [[quick-context/capacitor]] | [[quick-context/electric-current]]

> **[[learning/notes/quick-context/3d-printer-hotends|TL;DR:]]** This is a navigational index of all fundamental electronic [[learning/notes/quick-context/tensor|components]]—from passive parts (resistors, [[learning/notes/quick-context/voltage|capacitors]], inductors) through active devices (transistors, diodes) to the physical hierarchy that connects them (dies, substrates, packages, PCBs). Use it as a map to find existing quick-context files and spot gaps in coverage.

# Fundamental Electronic Parts — Index

## The Core Problem: Electronics Has Too Many Pieces to Hold in Your Head

A modern electronic system spans nine orders of magnitude (5 nm transistors to 5 mm connectors) and involves dozens of distinct [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|component]] types, each governed by different physics. Beginners drown in vocabulary; experienced engineers forget where one abstraction [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|layer]] ends and the next begins. This index organizes every fundamental electronic part into a coherent hierarchy so you can find the concept you need and understand how it relates to everything else.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Passive component** | A part that cannot amplify or [[learning/notes/quick-context/switches-to-registers-storing-data|switch]] signals—it can [[learning/notes/quick-context/comparator-specification|only]] store or dissipate energy. Resistors, capacitors, and inductors are the three fundamental passives. |
| **Active component** | A part that can amplify or switch—it adds energy from a [[learning/notes/quick-context/d-flip-flop|power]] supply into a [[learning/notes/quick-context/comparator|signal]] path. Transistors and diodes are the primary examples. |
| **Discrete component** | A single part in its own [[learning/notes/quick-context/silicon-die|package]] soldered to a PCB (a standalone [[learning/notes/quick-context/resistor|resistor]], a single [[learning/notes/quick-context/transistor|transistor]]). Contrast with "[[learning/notes/quick-context/playbook-main|integrated]]," where billions of components are fabricated together on one die. |
| **Integrated circuit (IC)** | [[learning/notes/quick-context/bond-pad|Billions of transistors]] (plus resistors, capacitors, and wiring) fabricated together on a single [[quick-context/silicon-die|silicon die]]—a complete functional block like a CPU, [[learning/notes/quick-context/bare-minimal-data-storage-circuit|memory]] chip, or sensor. |
| **Packaging hierarchy** | The chain of physical structures (die → [[learning/notes/quick-context/flip-chip|substrate]] → package → PCB) that connects nanometer-[[learning/notes/quick-context/absolute-orientation|scale]] transistors to the centimeter-scale world. See [[quick-context/pcb-chip-transistor-hierarchy|PCB-Chip-Transistor Hierarchy]]. |

<details>
<summary><strong>How It Works — The [[learning/notes/quick-context/singular-value-decomposition|Full]] Parts Map</strong></summary>

## 1. Passive Components — Store or Dissipate Energy

These are the simplest building blocks. They obey linear equations (mostly) and appear [[learning/notes/quick-context/bjt-specifications|both]] as discrete parts on PCBs and as structures inside ICs.

```
THE THREE FUNDAMENTAL PASSIVES
══════════════════════════════════════════════════════════════════════════════

  RESISTOR (R)              CAPACITOR (C)              INDUCTOR (L)
  ─────╱╱╱╱─────           ─────┤├─────               ─────⊃⊃⊃⊃─────

  Dissipates energy         Stores energy in           Stores energy in
  as heat                   an electric field          a magnetic field

  V = I × R                 Q = C × V                  V = L × dI/dt
  (Ohm's law)              I = C × dV/dt              E = ½LI²

  Unit: Ohm (Ω)            Unit: Farad (F)             Unit: Henry (H)

  Resists current flow      Blocks DC, passes AC       Blocks AC, passes DC
  Converts electrical       Charges/discharges         Opposes changes
  energy → heat             in nanoseconds             in current


  VARIABLE KEY
  ─────────────────────────────────────────────────────────────────
  V = voltage (volts)              I = current (amps)
  R = resistance (ohms)            C = capacitance (farads)
  L = inductance (henrys)          Q = charge (coulombs)
  E = energy (joules)              t = time (seconds)
  dI/dt = rate of current change   dV/dt = rate of voltage change
  P = power (watts)
```

| Part | Existing Quick-Context? | Key Concept |
|------|------------------------|-------------|
| **[[quick-context/capacitor\|Capacitor]]** | Yes | Q=CV ([[learning/notes/quick-context/cations-and-reduction|charge]] = [[learning/notes/quick-context/capacitance|capacitance]] × [[learning/notes/quick-context/voltage|voltage]]), dielectrics, RC time constants, decoupling |
| **[[quick-context/resistor\|Resistor]]** | Yes | [[learning/notes/quick-context/resistor|Ohm's law]] (V=IR: voltage = [[learning/notes/quick-context/capacitance|current]] × resistance), [[learning/notes/quick-context/resistor|power dissipation]] (P=I²R: power = current² × resistance), voltage dividers, pull-up/pull-down |
| **[[quick-context/inductor\|Inductor]]** | Yes | Magnetic energy [[learning/notes/quick-context/3d-printing-filament-refill-vs-spool|storage]] (E=½LI²: energy = ½ × inductance × current²), opposes current changes, used in filters/power supplies |

## 2. Active Components — Amplify and Switch

These are the parts that make electronics "smart." They use energy from a power supply to control signals.

```
ACTIVE COMPONENT FAMILY TREE
══════════════════════════════════════════════════════════════════════════════

  DIODE                          TRANSISTOR
  ─►├─                           (three terminals)

  One-way valve for current      Electrically-controlled switch/amplifier

  Two types:                     Two major families:
  • PN junction diode            • BJT (Bipolar Junction Transistor)
  • LED (Light Emitting Diode)   • MOSFET (Metal-Oxide-Semiconductor FET)
  • Zener (voltage reference)        └── The one that matters for digital
  • Schottky (fast switching)             electronics (billions per chip)
```

| Part | Existing Quick-Context? | Key Concept |
|------|------------------------|-------------|
| **[[quick-context/transistor\|Transistor (MOSFET)]]** | Yes | [[learning/notes/quick-context/transistor|Gate]]-controlled switch, [[learning/notes/quick-context/transistor|MOS capacitor]], NAND gates, CMOS |
| **[[quick-context/transistor-analog-to-digital\|Transistor: Analog → Digital]]** | Yes | Leakage, noise margins, [[learning/notes/quick-context/transistor-analog-to-digital|regenerative logic]], clocking |
| **[[quick-context/transistor-design-history\|Transistor: Design History]]** | Yes | [[learning/notes/quick-context/epson-rc-plus-programming|Point]]-contact → BJT → [[learning/notes/quick-context/transistor-design-history|planar MOSFET]] → [[learning/notes/quick-context/transistor-design-history|FinFET]] → GAA |
| **[[quick-context/diode\|Diode]]** | Yes | [[learning/notes/quick-context/diode|PN junction]], forward/reverse bias, rectification, LEDs |
| **[[quick-context/bjt\|BJT (Bipolar Junction Transistor)]]** | Yes | Current-controlled amplifier, NPN/PNP, base/collector/emitter |
| **[[quick-context/bjt-specifications\|BJT Specifications]]** | Yes | The 5 datasheet numbers to check: [[learning/notes/quick-context/bjt-specifications|type]], V_CEO, I_C, P_C, β/hFE |
| **[[quick-context/op-amp\|Op-Amp]]** | Yes | Differential amplifier IC, [[learning/notes/quick-context/op-amp|negative feedback]], gain = Rf/Rin (feedback resistor / input resistor) |
| **[[quick-context/comparator\|Comparator]]** | Yes | Op-amp's sibling optimized for binary output; bridges analog signals to digital logic |
| **[[quick-context/differential-pair\|Differential Pair]]** | Yes | Two matched transistors + [[learning/notes/quick-context/differential-pair|tail current source]]; the universal input stage of op-amps, comparators, and ADCs |
| **[[quick-context/high-gain-amplifier-stage\|High-Gain Amplifier Stage]]** | Yes | [[learning/notes/micro-context/current-mirror|Current mirror]] [[learning/notes/quick-context/high-gain-amplifier-stage|active load]] on a [[learning/notes/quick-context/differential-pair|differential pair]]; converts μA current difference into full-rail voltage swing |

## 3. Semiconductor Materials — What Parts Are Made Of

```
FROM SAND TO SWITCH
══════════════════════════════════════════════════════════════════════════════

  Sand (SiO₂) → Purified Silicon → Doped Silicon → Transistors
                 (intrinsic)        (n-type/p-type)  (billions per die)
```

| [[learning/notes/quick-context/ros2-architecture|Topic]] | Existing Quick-Context? | Key Concept |
|-------|------------------------|-------------|
| **[[quick-context/doped-silicon\|Doped Silicon]]** | Yes | N-type/P-type, PN junctions, [[learning/notes/quick-context/semiconductor-fabrication|ion implantation]] |
| **[[quick-context/semiconductor-fabrication\|Semiconductor Fabrication]]** | Yes | [[learning/notes/quick-context/metal-interconnect-layers|Photolithography]], CVD/PVD/ALD ([[learning/notes/quick-context/semiconductor-fabrication|deposition]] methods), [[learning/notes/quick-context/semiconductor-fabrication|etching]], CMP (chemical-mechanical polishing), EUV (extreme ultraviolet lithography) |
| **[[quick-context/silicon-die\|Silicon Die]]** | Yes | FEOL (front-end: transistors) + BEOL (back-end: metal wiring layers), [[learning/notes/quick-context/silicon-die|wafer]] [[learning/notes/quick-context/silicon-die|dicing]], [[learning/notes/quick-context/silicon-die|yield]] |

## 4. Circuit Fundamentals — How Parts Behave Together

| Topic | Existing Quick-Context? | Key Concept |
|-------|------------------------|-------------|
| **[[quick-context/electric-current\|Electric Current]]** | Yes | Amperes, coulombs, DC/AC, [[learning/notes/quick-context/lenzs-law|Faraday's law]] |
| **[[quick-context/parallel-vs-series-voltage\|Parallel vs. Series Voltage]]** | Yes | Why billions of transistors share ~0.65V, [[learning/notes/quick-context/voltage-current-causality|Kirchhoff's laws]] |
| **[[quick-context/thermal-noise-electronics\|Thermal Noise]]** | Yes | Johnson-Nyquist noise, kT energy scale, noise margins |
| **[[quick-context/impedance-and-reactance\|Impedance and Reactance]]** | Yes | Z = R + jX (impedance = resistance + imaginary unit × reactance), capacitive/inductive reactance, [[learning/notes/quick-context/impedance-and-reactance|phase angle]] |
| **[[quick-context/frequency-and-filtering\|Frequency and Filtering]]** | Yes | Cutoff frequency, dB (decibels), low-pass/high-pass, filter [[learning/notes/quick-context/frequency-and-filtering|order]] |
| **[[quick-context/power-watts-joules\|Electrical Power]]** | Yes | P = VI (power = voltage × current), watts, joules, efficiency, [[learning/notes/quick-context/power-watts-joules|thermal dissipation]] |
| **[[quick-context/electromagnetism\|Electromagnetism]]** | Yes | [[learning/notes/quick-context/maxwell-equations|Maxwell's equations]], magnetic [[learning/notes/quick-context/code-to-gates-and-bootstrapping|fields]], Faraday's law, EM waves |
| **[[quick-context/electric-magnetic-field-unification\|Field Unification]]** | Yes | How V, I, E, B connect—the conceptual map |
| **[[quick-context/grounding-and-return-paths\|Grounding and Return Paths]]** | Yes | Return paths, ground planes, ground loops, star grounding |

## 5. IC Packaging Hierarchy — Connecting Nano to Macro

The [[quick-context/pcb-chip-transistor-hierarchy|master hierarchy document]] covers the full chain. Individual files go deep on each level:

```
PACKAGING HIERARCHY (nano → macro)
══════════════════════════════════════════════════════════════════════════════

  TRANSISTORS (5 nm)
       │
  METAL INTERCONNECTS (M1-M10+)  ← wiring inside the die
       │
  BOND PADS (~50 μm)            ← connection points on die surface
       │
  ┌────┴────┐
  │         │
  WIRE     FLIP-CHIP             ← die-to-substrate connection method
  BOND     (C4 bumps)
  │         │
  └────┬────┘
       │
  SUBSTRATE (RDL fan-out)        ← redistributes fine pitch → coarse pitch
       │
  BGA BALLS (~0.5 mm)           ← package-to-PCB connection
       │
  PCB TRACES/VIAS               ← board-level wiring
       │
  CONNECTORS (~5 mm)            ← to the outside world
```

| Level | Existing Quick-Context? | Key Concept |
|-------|------------------------|-------------|
| **[[quick-context/pcb-chip-transistor-hierarchy\|Full Hierarchy]]** | Yes | 9 orders of magnitude, progressive fan-out |
| **[[quick-context/metal-interconnect-layers\|Metal Interconnect Layers]]** | Yes | M1-M10+ wiring, vias, signal routing, power delivery |
| **[[quick-context/bond-pad\|Bond Pads]]** | Yes | ~50 μm connection points, edge vs. area array |
| **[[quick-context/wire-bonding\|Wire Bonding]]** | Yes | Ball/wedge bond, [[learning/notes/quick-context/wire-bonding|ultrasonic welding]], [[learning/notes/quick-context/wire-bonding|loop height]] |
| **[[quick-context/flip-chip\|Flip-Chip (C4)]]** | Yes | [[learning/notes/quick-context/soldering|Solder]] bumps, [[learning/notes/quick-context/flip-chip|underfill]], CTE mismatch |
| **[[quick-context/substrate-ic-packaging\|Substrate / IC Packaging]]** | Yes | RDL (redistribution layer), organic vs. ceramic, FOWLP ([[learning/notes/quick-context/substrate-ic-packaging|fan-out wafer-level packaging]]) |
| **[[quick-context/bga-ball-grid-array\|BGA (Ball Grid Array)]]** | Yes | Solder balls, [[learning/notes/quick-context/bga-ball-grid-array|pitch]], [[learning/notes/quick-context/bga-ball-grid-array|reflow]], [[learning/notes/quick-context/bga-ball-grid-array|X-ray inspection]] |
| **[[quick-context/pcb-printed-circuit-board\|PCB]]** | Yes | Traces, vias, pads, layers, [[learning/notes/quick-context/pcb-layers|soldermask]] |

## 6. Failure Modes — How Parts Break

| Topic | Existing Quick-Context? | Key Concept |
|-------|------------------------|-------------|
| **[[quick-context/electromigration\|Electromigration]]** | Yes | [[learning/notes/quick-context/electromigration|Electron wind]], voids/hillocks, Black's Law |

## 7. Practical Skills — Tools and Techniques

| Topic | Existing Quick-Context? | Key Concept |
|-------|------------------------|-------------|
| **[[quick-context/soldering\|Soldering]]** | Yes | Solder alloys, [[learning/notes/quick-context/soldering|flux]], [[learning/notes/quick-context/soldering|wetting]], reflow, hand vs machine |
| **[[quick-context/oscilloscope-and-multimeter\|Oscilloscope and Multimeter]]** | Yes | DMM for static values, scope for time-domain waveforms |
| **[[quick-context/schematic-reading\|Schematic Reading]]** | Yes | Symbols, [[learning/notes/quick-context/comparator|reference]] designators, nets, signal tracing |
| **[[quick-context/common-ic-packages\|Common IC Packages]]** | Yes | DIP, [[learning/notes/quick-context/common-ic-packages|SOIC]], QFP, QFN, BGA—size/pin/thermal tradeoffs |

</details>

<details>
<summary><strong>[[learning/notes/quick-context/3d-printing-filament-types|The Key Tension]]: Coverage Map</strong></summary>

## Full Coverage

```
COVERAGE MAP
══════════════════════════════════════════════════════════════════════════════

  PASSIVES               ACTIVES                CIRCUIT CONCEPTS
  ────────────────       ────────────────       ─────────────────────
  ✅ Resistor            ✅ Transistor (MOSFET)  ✅ Electric current
  ✅ Capacitor           ✅ Diode / LED          ✅ Parallel vs. series
  ✅ Inductor            ✅ BJT                  ✅ Thermal noise
                         ✅ Op-amp               ✅ Impedance / reactance
                         ✅ Comparator
                                                 ✅ Frequency / filtering
  IC PACKAGING           MATERIALS               ✅ Power (watts, joules)
  ────────────────       ────────────────        ✅ Electromagnetism
  ────────────────       ────────────────        ✅ Grounding / return paths
  ✅ Full hierarchy      ✅ Doped silicon
  ✅ Metal interconnects ✅ Semiconductor fab    PRACTICAL
  ✅ Bond pads           ✅ Silicon die          ─────────────────────
  ✅ Wire bonding                                ✅ Soldering
  ✅ Flip-chip                                   ✅ Oscilloscope / DMM
  ✅ Substrate                                   ✅ Schematic reading
  ✅ BGA                                         ✅ Common IC packages
  ✅ PCB                                           (DIP, QFP, QFN, SOT)
```

All fundamental electronic parts now have quick-context files. [[learning/notes/quick-context/similarity-transform|Total]]: 34 electronics-related files in the knowledge graph.

</details>

<details>
<summary><strong>Concrete [[learning/notes/quick-context/teep|Example:]] Reading a Schematic</strong></summary>

## Tracing a Signal Through Fundamental Parts

Here's a simplified path from a sensor to a [[learning/notes/micro-context/microcontroller|microcontroller]], showing which parts you'd encounter and which quick-context files explain them:

```
SENSOR SIGNAL PATH
══════════════════════════════════════════════════════════════════════════════

  SENSOR OUTPUT (analog voltage)
       │
       ▼
  ┌──────────┐
  │ RESISTOR │  Voltage divider to scale signal ← resistor.md
  │  10 kΩ   │
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │ CAPACITOR│  Filter out high-frequency noise  ← capacitor.md
  │  100 nF  │
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │  DIODE   │  Protect against negative voltage ← diode.md
  │  1N4148  │
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │   MCU    │  ADC pin reads voltage            ← transistor.md (inside)
  │  (IC)    │  Billions of transistors             pcb-chip-transistor-
  │          │  on a silicon die                     hierarchy.md
  └────┬─────┘
       │
       ▼
  ┌──────────┐
  │   PCB    │  Traces connect everything         ← pcb-printed-circuit-
  │          │  Vias route between layers            board.md
  └──────────┘


  POWER SUPPLY PATH (separate but critical)
  ──────────────────────────────────────────

  Wall adapter → Voltage regulator → Bulk caps → Decoupling caps → IC
                  (inductor inside)   (electrolytic)  (ceramic, 100nF)
                  ← inductor.md       ← capacitor.md  ← capacitor.md
```

Every signal in every electronic device passes through some combination of these fundamental parts. The index above tells you which ones have deep-dive explanations available and which are still gaps.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/transistor]]** — The most important active component. Understanding the MOSFET is the gateway to understanding all digital electronics, from logic gates to CPUs.

- **[[quick-context/capacitor]]** — The most important passive for digital electronics. Decoupling capacitors are on every board; the MOS capacitor is inside every transistor.

- **[[quick-context/electric-current]]** — The foundational concept that connects all components. Current flows through resistors, charges capacitors, creates magnetic fields in inductors, and drives transistor switching.

- **[[quick-context/pcb-chip-transistor-hierarchy]]** — The [[learning/notes/quick-context/data-bus-and-arbitration|master]] document for understanding how components at different scales connect together, from 5 nm transistors to 5 mm connectors.

- **[[quick-context/doped-silicon]]** — Why [[learning/notes/quick-context/transistor|silicon]] is special: not a conductor, not an insulator, but controllable. [[learning/notes/quick-context/doped-silicon|Doping]] creates the PN junctions that make transistors and diodes possible.

- **[[quick-context/semiconductor-fabrication]]** — How all of these components get manufactured at nanometer scales on silicon wafers.

- **[[quick-context/thermal-noise-electronics]]** — The fundamental physical limit on how small and quiet electronic components can be: thermal energy (kT, where k = Boltzmann's constant and T = temperature in kelvins) sets a [[learning/notes/quick-context/thermal-noise-electronics|noise floor]] that constrains circuit design.

- **[[quick-context/galvanic-cells-batteries]]** — Batteries and capacitors are both energy storage, but through completely different mechanisms. Understanding the contrast clarifies [[learning/notes/quick-context/bare-minimal-data-storage-circuit|what]] capacitors actually do.

</details>

<details>
<summary><strong>Test [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|Your]] Understanding</strong></summary>

**Q1:** What are the three fundamental passive components, and what [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|form]] of energy does each store or dissipate?
<details>
<summary>Answer</summary>
**Resistor** dissipates energy as heat. **Capacitor** stores energy in an [[learning/notes/quick-context/voltage-current-causality|electric field]] (E = ½CV²: energy = ½ × capacitance × voltage²). **[[learning/notes/quick-context/inductor|Inductor]]** stores energy in a magnetic field (E = ½LI²: energy = ½ × inductance × current²). Resistors are the only passive that converts electrical energy into a non-electrical form; capacitors and inductors store energy temporarily and can return it to the circuit.
</details>

**Q2:** What is the difference between a passive and an active component?
<details>
<summary>Answer</summary>
A **passive component** can only store or dissipate energy—it cannot amplify a signal. Resistors, capacitors, and inductors are passive. An **active component** can amplify or switch signals by drawing energy from a power supply and injecting it into the signal path. Transistors are the primary example: a small voltage on the gate controls a much larger current between source and [[learning/notes/quick-context/differential-pair|drain]].
</details>

**Q3:** A capacitor "blocks DC but passes AC" and an inductor "blocks AC but passes DC." Why are these behaviors exactly opposite?
<details>
<summary>Answer</summary>
They store energy in [[learning/notes/quick-context/comparator-specification|dual]] forms: capacitors in electric fields (voltage-dependent), inductors in magnetic fields (current-dependent). A capacitor opposes voltage changes (I = C × dV/dt: current = capacitance × rate of voltage change)—DC has no voltage change, so no current passes. An inductor opposes current changes (V = L × dI/dt: voltage = inductance × rate of current change)—DC has no current change, so the inductor acts like a wire. At higher frequencies, voltage and current change faster, amplifying these opposing behaviors. This duality is why LC combinations create resonance and second-order [[learning/notes/quick-context/pupper-lab7-vision-tracking|filters]].
</details>

**Q4:** In the packaging hierarchy, why are there multiple connection technologies ([[learning/notes/quick-context/wire-bonding|wire bonding]] vs. [[learning/notes/quick-context/flip-chip|flip-chip]]) rather than just one?
<details>
<summary>Answer</summary>
They serve different tradeoffs. **Wire bonding** is cheap, flexible, and well-understood, but limited in [[learning/notes/quick-context/bond-pad|density]] and adds inductance ([[learning/notes/quick-context/uart|wires]] are long). **Flip-chip** offers higher density and [[learning/notes/quick-context/pcb-printed-circuit-board|lower inductance]] (shorter connections), but requires more complex manufacturing and underfill to handle thermal stress. [[learning/notes/quick-context/bond-pad|Cost]]-sensitive, low-pin-[[learning/notes/quick-context/switches-to-registers-storing-data|count]] chips use wire bonding; high-[[learning/notes/quick-context/bond-pad|performance]] processors use flip-chip. See [[quick-context/wire-bonding]] and [[quick-context/flip-chip]].
</details>

**Q5:** If you had to explain to someone the purpose of the entire packaging hierarchy in one sentence, what would it be?
<details>
<summary>Answer</summary>
The packaging hierarchy is a chain of progressively coarser "adapters" that bridge nine orders of magnitude in scale—from 5 nm transistors on a [[learning/notes/quick-context/silicon-die|silicon die]] to 5 mm connectors on a PCB—so that nanometer-scale computation can connect to the human-scale world with [[learning/notes/quick-context/ros2-architecture|reliable]] electrical and thermal paths. See [[quick-context/pcb-chip-transistor-hierarchy]].
</details>

</details>
