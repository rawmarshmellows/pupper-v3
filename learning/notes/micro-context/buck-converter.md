---
term: Buck Converter
created: 2026-01-27
updated: 2026-03-27
---

# Buck Converter

> **Related:** [[micro-context/mosfet]] | [[micro-context/pwm-pulse-width-modulation]] | [[micro-context/stm32-microcontroller]] | [[quick-context/capacitor]] | [[quick-context/diode]]

## Human notes

Make the ASCII diagrams clearer, in particular on the relationship between [[quick-context/transistor|MOSFET]] and [[quick-context/diode|diode]] — what is connected to the source, drain, and gate?

**Why does the [[quick-context/capacitor|output capacitor]] still smooth everything to 5V?** The inductor current has a sawtooth ripple — it ramps up during Phase 1 (switch ON) and ramps down during Phase 2 (switch OFF). The output capacitor acts as a reservoir: when inductor current is above the load's demand, the excess charges the capacitor; when inductor current dips below demand, the capacitor discharges to make up the difference. Because $V = Q/C$ and the capacitor has significant capacitance, these tiny charge/discharge cycles produce only millivolts of ripple around the 5V average. The *average* voltage is set by the [[micro-context/pwm-pulse-width-modulation|duty cycle]] ($V_{OUT} = V_{IN} \times D$) — the capacitor doesn't *create* 5V, it just filters out the switching noise around that average.

**Who controls the [[micro-context/pwm-pulse-width-modulation|PWM]] and how is it connected?** A dedicated buck converter IC (e.g., TPS54302, LM2596, MP1584) contains the PWM controller — it's not the [[micro-context/stm32-microcontroller|MCU]]. The IC connects to VIN for its own power and to drive the [[micro-context/mosfet|MOSFET]] gate (often the MOSFET is integrated *inside* the IC). A [[quick-context/resistor|resistor]] divider from VOUT feeds back to the IC's feedback (FB) pin. The IC compares this to an internal voltage reference (~0.8V) and adjusts the duty cycle: if VOUT drops → longer ON time → more energy → voltage recovers. This closed-loop control runs autonomously at hundreds of kHz — no software involved.

> **See also:** [[quick-context/electric-current]] | [[quick-context/parallel-vs-series-voltage]] | [[quick-context/inductor]] | [[quick-context/capacitor]] | [[quick-context/pupper-bom-control-board]] | [[quick-context/pwm-controller-circuit]]

**Definition:** A switching power supply that efficiently steps down voltage (e.g., 12V battery → 5V for logic). Unlike linear regulators that waste excess voltage as heat, buck converters use rapid switching (100kHz–2MHz) and an inductor to achieve 85–95% efficiency.

---

## Circuit Topology

```
             GATE ◄── PWM controller
               │
          ┌────┴────┐                      INDUCTOR (L)
          │ N-MOSFET│                  ┌──────────────┐
  VIN ────┤D      S ├─────────┬────────┤   ~~~~~~     ├───┬──── VOUT
  (12V)   │         │         │        │   ~~~~~~     │   │     (5V)
          └─────────┘         │        └──────────────┘   │
           drain    source    │                         ┌─┴─┐
                              │  switch node (SW)       │   │ C
                              │                         │   │(output
                           ──┬── K (cathode)            └─┬─┘ cap)
                            ╲│                            │
                             │    DIODE (D)               │
                            ╱│    freewheeling            │
                           ──┴── A (anode)                │
                              │                           │
  GND ────────────────────────┴───────────────────────────┘


  MOSFET pins:                Diode terminals:
  ┌──────────────────────┐    ┌───────────────────────────┐
  │ DRAIN (D)  → VIN     │    │ CATHODE (K) → switch node │
  │ GATE  (G)  → PWM     │    │ ANODE   (A) → GND         │
  │ SOURCE (S) → SW node │    └───────────────────────────┘
  └──────────────────────┘

  The "switch node" — where 3 things meet:

      MOSFET SOURCE ──┬── INDUCTOR input
                      │
                DIODE CATHODE

  This junction swings between VIN (SW on) and ~−0.7V (SW off).
```

---

## How It Works: Two-Phase Operation

### Phase 1: Switch ON (Charging)

```
  GATE = HIGH → MOSFET ON (drain-to-source conducts)

          ┌─────────┐                    INDUCTOR
          │ N-MOSFET│                 ┌────────────┐
  VIN ════╡D═════ S ╞═════════╤═══════╡  ~~~~~~    ╞═══════╗
  (12V)   │  (ON)   │         │       │  ~~~~~~    │       ║
          └─────────┘         │       └────────────┘       ║
                       current║        energy stored       ║
                        ═══▶  ║        in field (↑)      ┌─╨─┐
                              ║                          │   │
                           ──┬── K                       │ L │
                            ╲│                           │ O │ LOAD
                             │  DIODE reverse            │ A │
                            ╱│  biased — OFF             │ D │
                           ──┴── A                       │   │
                              │   K is at ~VIN,          └─╥─┘
                              │   A is at GND →            ║
                              │   reverse biased           ║
  GND ════════════════════════╧════════════════════════════╝
                              ◀═══════════════ current


  Path: VIN → DRAIN → SOURCE → switch node → INDUCTOR → LOAD → GND
```

### Phase 2: Switch OFF (Discharging)

```
  GATE = LOW → MOSFET OFF (drain-to-source open)

          ┌─────────┐                     INDUCTOR
          │ N-MOSFET│                 ┌────────────┐
  VIN ────┤D  ×   S ├ · · · · ╤═══════╡  ~~~~~~    ╞═══════╗
  (12V)   │  (OFF)  │         │       │  ~~~~~~    │       ║
          └─────────┘         │       └────────────┘       ║
                        ═══▶  ║        releases            ║
                       current║        stored energy     ┌─╨─┐
                              ║        (B↓)              │   │
                           ══╤══ K                       │ L │
                            ╲║                           │ O │ LOAD
                             ║  DIODE now conducts       │ A │
                            ╱║  (freewheeling)           │ D │
                           ══╧══ A                       │   │
                              ║                          └─╥─┘
                              ║  SW node drops below       ║
                              ║  GND → forward biases D    ║
  GND ════════════════════════╩════════════════════════════╝
                              ◀═══════════════ current


  Path: switch node → INDUCTOR → LOAD → GND → DIODE (A→K) → switch node

  The inductor REFUSES to let current stop suddenly!
  Its collapsing magnetic field drives current through the diode.

  In Phase 2: can you explain why current flows through the diode now? Here's what's happening: during Phase 1, the [[quick-context/inductor|inductor]] was storing energy in its magnetic field while current flowed through it. When the MOSFET switches OFF, the inductor's current can't stop instantly — that's [[quick-context/self-induction|self-induction]] (a consequence of [[quick-context/lenzs-law|Lenz's law]]). The inductor's collapsing magnetic field generates a voltage that *fights* the current decrease, pulling the switch node voltage *below* GND. Once the switch node drops ~0.7V below GND, the [[quick-context/diode|diode]] becomes forward-biased (its cathode is now more negative than its anode at GND), so current flows: GND → diode anode → diode cathode → switch node → inductor → load → back to GND. The diode provides the return path that the inductor *demands*.
```

---

## Waveforms

```
     SWITCH STATE (GATE signal):
         ON      OFF     ON      OFF     ON
     ├────────┼────────┼────────┼────────┼────────┤
     │████████│        │████████│        │████████│
     │████████│        │████████│        │████████│
     └────────┴────────┴────────┴────────┴────────┘
         ton     toff      ton     toff
     ├─────────────────┤
          T (period)

     INDUCTOR CURRENT (IL):
                 ╱╲          ╱╲          ╱╲
               ╱    ╲      ╱    ╲      ╱    ╲
     ─────────╱────────╲──╱────────╲──╱────────╲───  ← ripple
             ╱          ╲╱          ╲╱          ╲      around
            ╱                                          average
           ramps up    ramps down
          (SW on)      (SW off)

     OUTPUT VOLTAGE (VOUT):
     ────────────────────────────────────────────── 5V (smooth)
          (capacitor filters the ripple)
```

---

## The Math

$$V_{OUT} = V_{IN} \times D$$

where $D = t_{on} / T$ is the duty cycle.

Example: 12V input, want 5V output → $D = 5/12 = 0.417$ (41.7% duty cycle). At 500kHz ($T = 2\mu s$): $t_{on} = 0.83\mu s$, $t_{off} = 1.17\mu s$.

---

## Why It's Efficient

```
     LINEAR REGULATOR:              BUCK CONVERTER:
     ─────────────────              ────────────────

     VIN ──┬── VOUT                 VIN ──[SW]──[INDUCTOR]── VOUT
           │                                │         │
        ┌──┴──┐                            [D]       [C]
        │ΔΔΔΔΔ│  ← transistor               │         │
        │ΔΔΔΔΔ│    always ON               GND       GND
        └──┬──┘    (partial)
           │                        • Switch: fully ON or fully OFF
           ▼                             (no in-between)
        HEAT!                       • INDUCTOR stores/releases energy
                                    • No wasted voltage drop!
     Power wasted = (VIN - VOUT) × I
     Example: (12V - 5V) × 1A = 7W of HEAT!    Power loss ≈ 5-15%
```

---

**Key insight:** The MOSFET's drain connects to VIN and its source connects to the "switch node," where it meets the diode's cathode and the inductor input. This three-way junction is the heart of the converter — it swings between VIN (switch on) and below GND (switch off, diode conducts). The inductor stores energy magnetically when the switch is ON and releases it when OFF, achieving 85–95% efficiency.
