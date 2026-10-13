---
term: CAN Bus Transceiver
created: 2026-01-27
updated: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/can-bus-termination]] | [[learning/notes/quick-context/can-bus]] | [[learning/notes/quick-context/data-bus-and-arbitration]] | [[learning/notes/micro-context/i2c]] | [[learning/notes/micro-context/i2s-audio-amplifier]]


# CAN Bus Transceiver

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[quick-context/can-bus]] | [[quick-context/pcb-printed-circuit-board]] | [[quick-context/electric-current]] | [[quick-context/pupper-bom-control-board]] | [[quick-context/embedded-communication-protocols]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** A chip that converts the [[learning/notes/micro-context/microcontroller|microcontroller]]'s digital TX/RX signals into differential [[learning/notes/quick-context/voltage|voltage]] signals for the CAN bus (and vice versa). CAN bus is a robust 2-wire communication protocol used in cars and robots where multiple devices share the same wire pair. The MAX3051 handles the electrical interface so the MCU [[learning/notes/quick-context/comparator-specification|only]] deals with data.

## How It Works

- The MCU's CAN peripheral generates a [[learning/notes/quick-context/data-bus-and-arbitration|serial]] data stream (TX) using the CAN protocol's bit [[learning/notes/quick-context/comparator-specification|timing]] and [[learning/notes/quick-context/can-bus|arbitration]] rules.
- The transceiver converts this single-ended TX [[learning/notes/quick-context/comparator|signal]] into a [[learning/notes/quick-context/differential-pair|differential pair]] (CANH and CANL) with opposite voltage swings.
- On receive, the transceiver subtracts CANL from CANH, canceling any common-mode noise picked up on the wire pair.
- This [[learning/notes/quick-context/embedded-communication-protocols|differential signaling]] allows [[learning/notes/quick-context/ros2-architecture|reliable]] multi-drop communication over long cables in electrically noisy environments.

```
MCU to CAN BUS signal conversion:

  MCU                 MAX3051              CAN BUS (to motors)
  ┌───┐              ┌───────┐             ════════════════
  │   │───TX────────►│       │───CANH──────►  Differential
  │   │              │       │               pair (twisted)
  │   │◄──RX─────────│       │◄──CANL──────►  ±2V swing
  └───┘              └───────┘             ════════════════
    │                    │
   3.3V               5V logic            Noise-immune
  logic              + ESD protection     long-distance

  Why differential?
  ──────────────────
  CANH: ──┐  ┌──┐  ┌──       Noise hits BOTH wires equally
          └──┘  └──┘
  CANL: ──┘  └──┘  └──       Receiver subtracts → noise cancels
          ┌──┐  ┌──┐
          (inverted)
```

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** CAN transceivers are why robots can communicate reliably over long cables in electrically noisy environments—the differential signaling rejects interference that would corrupt single-wire connections.
