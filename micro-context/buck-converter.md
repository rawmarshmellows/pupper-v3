---
term: Buck Converter
created: 2026-01-27
updated: 2026-02-14
---

# Buck Converter

> **See also:** [[quick-context/electric-current]] | [[quick-context/parallel-vs-series-voltage]] | [[quick-context/inductor]]

**Definition:** A switching power supply that efficiently steps down voltage (e.g., 12V battery → 5V for logic). Unlike linear regulators that waste excess voltage as heat, buck converters use rapid switching (100kHz–2MHz) and an inductor to achieve 85–95% efficiency.

---

## Circuit Topology

```
                                        INDUCTOR (L)
                                    ┌──────────────┐
          SW (MOSFET)               │   ~~~~~~     │
         ┌───────┐                  │   ~~~~~~     │
  VIN ───┤       ├──────────────────┤   ~~~~~~     ├───┬─────── VOUT
  (12V)  └───┬───┘                  │   ~~~~~~     │   │        (5V)
             │       "switch node"  └──────────────┘   │
             │            (SW)                        ┌┴┐
             │             │                          │ │ C
           ──┴──           │                          │ │(output
            ╲│             │                          └┬┘ capacitor)
             ├─────────────┘                           │
            ╱│  D (freewheeling diode)                 │
           ──┴──                                       │
             │                                         │
  GND ───────┴─────────────────────────────────────────┘


  Signal path:  VIN ──▶ SW ──▶ INDUCTOR ──▶ LOAD/VOUT
                              (in series)

  The INDUCTOR sits between the switch output and the load.
  It's the energy reservoir that smooths the chopped voltage.
```

---

## How It Works: Two-Phase Operation

### Phase 1: Switch ON (Charging)

```
                                    INDUCTOR
                  SW CLOSED      ┌────────────┐
                 ┌───────┐       │  ~~~~~~    │
  VIN ═══════════╡ ■■■■■ ╞═══════╡  ~~~~~~    ╞═══════╗
  (12V)          └───────┘       │  ~~~~~~    │       ║
         current ═══════▶        └────────────┘       ║
                                  energy stored       ║
             │                    in magnetic       ┌─╨─┐
           ──┴──                  field (↑)         │   │
            ╲│                                     │ L │ LOAD
             │   (diode reverse                    │ O │
            ╱│    biased - OFF)                    │ A │
           ──┴──                                   │ D │
             │                                      └─╥─┘
             │                                        ║
  GND ═══════╧════════════════════════════════════════╝
                           ◀═══════════ current


     Path: VIN → SWITCH → INDUCTOR → LOAD → GND
                            │
                     stores energy in
                     magnetic field (B↑)
```

### Phase 2: Switch OFF (Discharging)

```
                                    INDUCTOR
                   SW OPEN       ┌────────────┐
                 ┌───────┐       │  ~~~~~~    │
  VIN ───────────┤   ×   ├ · · · ╡  ~~~~~~    ╞═══════╗
  (12V)          └───────┘       │  ~~~~~~    │       ║
         (no current)            └────────────┘       ║
                          ═══════▶  releases          ║
                          current   stored energy   ┌─╨─┐
           ──┬──            ▲       (B↓)            │   │
            ╲│             │                       │ L │ LOAD
             ╞═════════════╝                        │ O │
            ╱│  DIODE now conducts                  │ A │
           ──┴──  (freewheeling)                    │ D │
             ║                                      └─╥─┘
             ║                                        ║
  GND ═══════╩════════════════════════════════════════╝
                           ◀═══════════ current


     Path: INDUCTOR → LOAD → GND → DIODE → back to INDUCTOR
                │                     │
         releases stored         provides return
         magnetic energy         path for current

     The inductor REFUSES to let current stop suddenly!
     Its collapsing magnetic field drives current through the diode.
```

---

## Waveforms

```
     SWITCH STATE:
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

```
     DUTY CYCLE:  D = ton / T

     OUTPUT VOLTAGE:  VOUT = VIN × D

     Example: 12V input, want 5V output
              D = 5V / 12V = 0.417 (41.7% duty cycle)
              If switching at 500kHz (T = 2μs):
              ton = 0.83μs, toff = 1.17μs
```

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
           │                        • Switch: ON or OFF
           ▼                             (no in-between)
        HEAT!                       • INDUCTOR stores/releases energy
                                    • No wasted voltage drop!
     Power wasted = (VIN - VOUT) × I
     Example: (12V - 5V) × 1A = 7W of HEAT!    Power loss ≈ 5-15%
```

---

**Key insight:** The inductor is the magic—it stores energy magnetically when the switch is ON and releases it when OFF. Unlike a linear regulator where excess voltage becomes heat, the buck converter's switching approach only transfers the energy needed, achieving 85-95% efficiency. The output capacitor smooths the inductor's sawtooth current into clean DC.
