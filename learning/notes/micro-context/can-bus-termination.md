---
term: CAN Bus Termination
created: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]


# CAN Bus Termination

> **See also:** [[learning/notes/quick-context/can-bus]] | [[learning/notes/quick-context/embedded-communication-protocols]]

**Definition:** A 120Ω [[learning/notes/quick-context/resistor|resistor]] placed at each end of a [[learning/notes/quick-context/can-bus|CAN bus]] to match the cable's characteristic [[learning/notes/quick-context/impedance-and-reactance|impedance]] and prevent signal reflections. On the Pupper v3 control board, R1–R4 are the termination resistors for the 4 CAN buses connecting to 12 servo motors.

## How It Works

- A CAN bus is a [[learning/notes/quick-context/differential-pair|differential pair]] (CANH/CANL) with ~120Ω characteristic impedance set by the wire geometry.
- When a signal reaches an unterminated end, the impedance mismatch causes it to bounce back as a reflection, corrupting data.
- A 120Ω [[learning/notes/quick-context/resistor|resistor]] across CANH and CANL at each bus end absorbs the signal energy, eliminating reflections.
- Only the two endpoints need termination — nodes in the middle of the bus must **not** add termination resistors, or they'll reduce the bus impedance and distort signals.

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

**Key insight:** Without termination, CAN may work on very short buses at low speeds — but at 1 Mbps, reflected signals overlap with subsequent bits and distort [[learning/notes/quick-context/voltage|voltage]] levels during sampling, causing data corruption. The 120Ω value isn't arbitrary; it matches the physical impedance of a twisted wire pair.
