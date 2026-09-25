---
term: CAN Bus Termination
created: 2026-03-27
---

# CAN Bus Termination

> **Related:** [[micro-context/can-bus-transceiver]] | [[quick-context/can-bus]] | [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]] | [[micro-context/adc-analog-to-digital-converter]]

**[[quick-context/capacitance|Definition]]:** A 120Ω [[quick-context/resistor|resistor]] placed at each end of a [[quick-context/can-bus|CAN bus]] to match the cable's characteristic [[quick-context/impedance-and-reactance|impedance]] and prevent [[quick-context/comparator|signal]] reflections. On the Pupper v3 control board, R1–R4 are the termination resistors for the 4 CAN buses connecting to 12 servo motors.

## How It Works

- A CAN bus is a [[quick-context/can-bus|differential pair (CANH/CANL)]] with ~120Ω characteristic impedance set by the wire geometry.
- [[quick-context/bare-minimal-data-storage-circuit|When]] a signal reaches an unterminated end, the impedance mismatch causes it to bounce back as a reflection, corrupting data.
- A 120Ω [[quick-context/resistor|resistor]] across CANH and CANL at each bus end absorbs the signal energy, eliminating reflections.
- [[quick-context/comparator-specification|Only]] the [[micro-context/schmitt-trigger-hysteresis|two]] endpoints need termination — nodes in the middle of the bus must **not** add termination resistors, or they'll reduce the bus impedance and distort signals.

```
CAN bus with termination (Pupper: one bus of four)

  MCU (U5)
    │
 ┌──┴──┐
 │MAX  │  120Ω        Servo 1    Servo 2    Servo 3
 │3051 │──┤├──┬──────────┬──────────┬──────────┤├── 120Ω
 │     │      │  CANH    │          │          (end
 │     │──────┴──────────┴──────────┴───────── term.)
 └─────┘         CANL
  R1-R4                        No termination
  (board end)                  at middle nodes
```

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** Without termination, CAN may work on very short buses at low speeds — but at 1 Mbps, reflected signals overlap with subsequent bits and distort [[quick-context/voltage|voltage]] levels during sampling, causing data corruption. The 120Ω value isn't arbitrary; it matches the physical impedance of a twisted wire pair.
