---
term: CAN Bus Termination
created: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/can-bus-transceiver]] | [[learning/notes/quick-context/can-bus]] | [[learning/notes/quick-context/data-bus-and-arbitration]]

# CAN Bus Termination[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[quick-context/can-bus]] | [[quick-context/embedded-communication-protocols]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] 120Ω [[quick-context/resistor|resistor]] placed at each end of a [[quick-context/can-bus|CAN bus]] to match [[learning/notes/quick-context/capacitance|the]] cable's characteristic [[quick-context/impedance-and-reactance|impedance]] [[learning/notes/micro-context/push-pull-vs-open-drain|and]] prevent [[learning/notes/quick-context/comparator|signal]] reflections. On the Pupper v3 control board, R1–R4 are the termination resistors for the [[learning/notes/quick-context/similarity-transform|4]] [[learning/notes/quick-context/embedded-communication-protocols|CAN]] buses connecting to 12 servo motors.

## How It Works

- A CAN [[learning/notes/quick-context/data-bus-and-arbitration|bus]] is a [[learning/notes/quick-context/differential-pair|differential pair]] (CANH/CANL) [[learning/notes/quick-context/breaking-elongation-rate|with]] ~120Ω characteristic impedance set by the wire geometry.
- [[learning/notes/quick-context/bare-minimal-data-storage-circuit|When]] a signal reaches an unterminated end, the impedance mismatch causes it to bounce back as a reflection, corrupting data.
- A 120Ω [[learning/notes/quick-context/fundamental-electronic-parts-index|resistor]] across CANH and CANL at each bus end absorbs the signal energy, eliminating reflections.
- [[learning/notes/quick-context/comparator-specification|Only]] the [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] endpoints need termination — nodes in the middle of the bus [[learning/notes/quick-context/ros2-architecture|must]] **[[learning/notes/micro-context/jst-connector-families|not]]** add termination resistors, [[learning/notes/micro-context/push-pull-vs-open-drain|or]] they'll reduce the bus impedance and distort signals.

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

**Key insight:** Without termination, CAN may work on very short buses at low speeds — but at [[learning/notes/quick-context/meddpicc-qualification-framework|1]] Mbps, reflected signals overlap with subsequent bits and distort [[learning/notes/quick-context/voltage|voltage]] levels during sampling, causing data corruption. The 120Ω value isn't arbitrary; it matches the physical impedance of a twisted wire pair.
