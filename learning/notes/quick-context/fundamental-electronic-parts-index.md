---
topic: Fundamental Electronic Parts — Index
created: 2026-02-06
updated: 2026-02-07
---

> **Related:** [[learning/notes/quick-context/melt-index]]

> **TL;DR:** This is a navigational index of all fundamental electronic components—from passive parts (resistors, capacitors, inductors) through active devices (transistors, diodes) to the physical hierarchy that connects them (dies, substrates, packages, PCBs). Use it as a map to find existing quick-context files and spot gaps in coverage.

# Fundamental Electronic Parts — Index

## The Core Problem: Electronics Has Too Many Pieces to Hold in Your Head

A modern electronic system spans nine orders of magnitude (5 nm transistors to 5 mm connectors) and involves dozens of distinct component types, each governed by different physics. Beginners drown in vocabulary; experienced engineers forget where one abstraction layer ends and the next begins. This index organizes every fundamental electronic part into a coherent hierarchy so you can find the concept you need and understand how it relates to everything else.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Passive component** | A part that cannot amplify or switch signals—it can only store or dissipate energy. Resistors, capacitors, and inductors are the three fundamental passives. |
| **Active component** | A part that can amplify or switch—it adds energy from a power supply into a signal path. Transistors and diodes are the primary examples. |
| **Discrete component** | A single part in its own package soldered to a PCB (a standalone resistor, a single transistor). Contrast with "integrated," where billions of components are fabricated together on one die. |
| **Integrated circuit (IC)** | Billions of transistors (plus resistors, capacitors, and wiring) fabricated together on a single [[quick-context/silicon-die|silicon die]]—a complete functional block like a CPU, memory chip, or sensor. |
| **Packaging hierarchy** | The chain of physical structures (die → substrate → package → PCB) that connects nanometer-scale transistors to the centimeter-scale world. See [[quick-context/pcb-chip-transistor-hierarchy|PCB-Chip-Transistor Hierarchy]]. |

<details>
<summary><strong>How It Works — The Full Parts Map</strong></summary>

## 1. Passive Components — Store or Dissipate Energy

These are the simplest building blocks. They obey linear equations (mostly) and appear both as discrete parts on PCBs and as structures inside ICs.

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
| **[[quick-context/capacitor\|Capacitor]]** | Yes | Q=CV (charge = capacitance × voltage), dielectrics, RC time constants, decoupling |
| **[[quick-context/resistor\|Resistor]]** | Yes | Ohm's law (V=IR: voltage = current × resistance), power dissipation (P=I²R: power = current² × resistance), voltage dividers, pull-up/pull-down |
| **[[quick-context/inductor\|Inductor]]** | Yes | Magnetic energy storage (E=½LI²: energy = ½ × inductance × current²), opposes current changes, used in filters/power supplies |

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
| **[[quick-context/transistor\|Transistor (MOSFET)]]** | Yes | Gate-controlled switch, MOS capacitor, NAND gates, CMOS |
| **[[quick-context/transistor-analog-to-digital\|Transistor: Analog → Digital]]** | Yes | Leakage, noise margins, regenerative logic, clocking |
| **[[quick-context/transistor-design-history\|Transistor: Design History]]** | Yes | Point-contact → BJT → planar MOSFET → FinFET → GAA |
| **[[quick-context/diode\|Diode]]** | Yes | PN junction, forward/reverse bias, rectification, LEDs |
| **[[quick-context/bjt\|BJT (Bipolar Junction Transistor)]]** | Yes | Current-controlled amplifier, NPN/PNP, base/collector/emitter |
| **[[quick-context/bjt-specifications\|BJT Specifications]]** | Yes | The 5 datasheet numbers to check: type, V_CEO, I_C, P_C, β/hFE |
| **[[quick-context/op-amp\|Op-Amp]]** | Yes | Differential amplifier IC, negative feedback, gain = Rf/Rin (feedback resistor / input resistor) |
| **[[quick-context/comparator\|Comparator]]** | Yes | Op-amp's sibling optimized for binary output; bridges analog signals to digital logic |
| **[[quick-context/differential-pair\|Differential Pair]]** | Yes | Two matched transistors + tail current source; the universal input stage of op-amps, comparators, and ADCs |
| **[[quick-context/high-gain-amplifier-stage\|High-Gain Amplifier Stage]]** | Yes | Current mirror active load on a differential pair; converts μA current difference into full-rail voltage swing |

## 3. Semiconductor Materials — What Parts Are Made Of

```
FROM SAND TO SWITCH
══════════════════════════════════════════════════════════════════════════════

  Sand (SiO₂) → Purified Silicon → Doped Silicon → Transistors
                 (intrinsic)        (n-type/p-type)  (billions per die)
```

| Topic | Existing Quick-Context? | Key Concept |
|-------|------------------------|-------------|
| **[[quick-context/doped-silicon\|Doped Silicon]]** | Yes | N-type/P-type, PN junctions, ion implantation |
| **[[quick-context/semiconductor-fabrication\|Semiconductor Fabrication]]** | Yes | Photolithography, CVD/PVD/ALD (deposition methods), etching, CMP (chemical-mechanical polishing), EUV (extreme ultraviolet lithography) |
| **[[quick-context/silicon-die\|Silicon Die]]** | Yes | FEOL (front-end: transistors) + BEOL (back-end: metal wiring layers), wafer dicing, yield |

## 4. Circuit Fundamentals — How Parts Behave Together

| Topic | Existing Quick-Context? | Key Concept |
|-------|------------------------|-------------|
| **[[quick-context/electric-current\|Electric Current]]** | Yes | Amperes, coulombs, DC/AC, Faraday's law |
| **[[quick-context/parallel-vs-series-voltage\|Parallel vs. Series Voltage]]** | Yes | Why billions of transistors share ~0.65V, Kirchhoff's laws |
| **[[quick-context/thermal-noise-electronics\|Thermal Noise]]** | Yes | Johnson-Nyquist noise, kT energy scale, noise margins |
| **[[quick-context/impedance-and-reactance\|Impedance and Reactance]]** | Yes | Z = R + jX (impedance = resistance + imaginary unit × reactance), capacitive/inductive reactance, phase angle |
| **[[quick-context/frequency-and-filtering\|Frequency and Filtering]]** | Yes | Cutoff frequency, dB (decibels), low-pass/high-pass, filter order |
| **[[quick-context/power-watts-joules\|Electrical Power]]** | Yes | P = VI (power = voltage × current), watts, joules, efficiency, thermal dissipation |
| **[[quick-context/electromagnetism\|Electromagnetism]]** | Yes | Maxwell's equations, magnetic fields, Faraday's law, EM waves |
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
| **[[quick-context/wire-bonding\|Wire Bonding]]** | Yes | Ball/wedge bond, ultrasonic welding, loop height |
| **[[quick-context/flip-chip\|Flip-Chip (C4)]]** | Yes | Solder bumps, underfill, CTE mismatch |
| **[[quick-context/substrate-ic-packaging\|Substrate / IC Packaging]]** | Yes | RDL (redistribution layer), organic vs. ceramic, FOWLP (fan-out wafer-level packaging) |
| **[[quick-context/bga-ball-grid-array\|BGA (Ball Grid Array)]]** | Yes | Solder balls, pitch, reflow, X-ray inspection |
| **[[quick-context/pcb-printed-circuit-board\|PCB]]** | Yes | Traces, vias, pads, layers, soldermask |

## 6. Failure Modes — How Parts Break

| Topic | Existing Quick-Context? | Key Concept |
|-------|------------------------|-------------|
| **[[quick-context/electromigration\|Electromigration]]** | Yes | Electron wind, voids/hillocks, Black's Law |

## 7. Practical Skills — Tools and Techniques

| Topic | Existing Quick-Context? | Key Concept |
|-------|------------------------|-------------|
| **[[quick-context/soldering\|Soldering]]** | Yes | Solder alloys, flux, wetting, reflow, hand vs machine |
| **[[quick-context/oscilloscope-and-multimeter\|Oscilloscope and Multimeter]]** | Yes | DMM for static values, scope for time-domain waveforms |
| **[[quick-context/schematic-reading\|Schematic Reading]]** | Yes | Symbols, reference designators, nets, signal tracing |
| **[[quick-context/common-ic-packages\|Common IC Packages]]** | Yes | DIP, SOIC, QFP, QFN, BGA—size/pin/thermal tradeoffs |

</details>

<details>
<summary><strong>The Key Tension: Coverage Map</strong></summary>

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

All fundamental electronic parts now have quick-context files. Total: 34 electronics-related files in the knowledge graph.

</details>

<details>
<summary><strong>Concrete Example: Reading a Schematic</strong></summary>

## Tracing a Signal Through Fundamental Parts

Here's a simplified path from a sensor to a microcontroller, showing which parts you'd encounter and which quick-context files explain them:

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

- **[[quick-context/pcb-chip-transistor-hierarchy]]** — The master document for understanding how components at different scales connect together, from 5 nm transistors to 5 mm connectors.

- **[[quick-context/doped-silicon]]** — Why silicon is special: not a conductor, not an insulator, but controllable. Doping creates the PN junctions that make transistors and diodes possible.

- **[[quick-context/semiconductor-fabrication]]** — How all of these components get manufactured at nanometer scales on silicon wafers.

- **[[quick-context/thermal-noise-electronics]]** — The fundamental physical limit on how small and quiet electronic components can be: thermal energy (kT, where k = Boltzmann's constant and T = temperature in kelvins) sets a noise floor that constrains circuit design.

- **[[quick-context/galvanic-cells-batteries]]** — Batteries and capacitors are both energy storage, but through completely different mechanisms. Understanding the contrast clarifies what capacitors actually do.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What are the three fundamental passive components, and what form of energy does each store or dissipate?
<details>
<summary>Answer</summary>
**Resistor** dissipates energy as heat. **Capacitor** stores energy in an electric field (E = ½CV²: energy = ½ × capacitance × voltage²). **Inductor** stores energy in a magnetic field (E = ½LI²: energy = ½ × inductance × current²). Resistors are the only passive that converts electrical energy into a non-electrical form; capacitors and inductors store energy temporarily and can return it to the circuit.
</details>

**Q2:** What is the difference between a passive and an active component?
<details>
<summary>Answer</summary>
A **passive component** can only store or dissipate energy—it cannot amplify a signal. Resistors, capacitors, and inductors are passive. An **active component** can amplify or switch signals by drawing energy from a power supply and injecting it into the signal path. Transistors are the primary example: a small voltage on the gate controls a much larger current between source and drain.
</details>

**Q3:** A capacitor "blocks DC but passes AC" and an inductor "blocks AC but passes DC." Why are these behaviors exactly opposite?
<details>
<summary>Answer</summary>
They store energy in dual forms: capacitors in electric fields (voltage-dependent), inductors in magnetic fields (current-dependent). A capacitor opposes voltage changes (I = C × dV/dt: current = capacitance × rate of voltage change)—DC has no voltage change, so no current passes. An inductor opposes current changes (V = L × dI/dt: voltage = inductance × rate of current change)—DC has no current change, so the inductor acts like a wire. At higher frequencies, voltage and current change faster, amplifying these opposing behaviors. This duality is why LC combinations create resonance and second-order filters.
</details>

**Q4:** In the packaging hierarchy, why are there multiple connection technologies (wire bonding vs. flip-chip) rather than just one?
<details>
<summary>Answer</summary>
They serve different tradeoffs. **Wire bonding** is cheap, flexible, and well-understood, but limited in density and adds inductance (wires are long). **Flip-chip** offers higher density and lower inductance (shorter connections), but requires more complex manufacturing and underfill to handle thermal stress. Cost-sensitive, low-pin-count chips use wire bonding; high-performance processors use flip-chip. See [[quick-context/wire-bonding]] and [[quick-context/flip-chip]].
</details>

**Q5:** If you had to explain to someone the purpose of the entire packaging hierarchy in one sentence, what would it be?
<details>
<summary>Answer</summary>
The packaging hierarchy is a chain of progressively coarser "adapters" that bridge nine orders of magnitude in scale—from 5 nm transistors on a silicon die to 5 mm connectors on a PCB—so that nanometer-scale computation can connect to the human-scale world with reliable electrical and thermal paths. See [[quick-context/pcb-chip-transistor-hierarchy]].
</details>

</details>
