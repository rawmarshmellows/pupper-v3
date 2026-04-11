---
term: CAN Bus Transceiver
created: 2026-01-27
updated: 2026-03-27
---

# CAN Bus Transceiver
> **Related:** [[quick-context/can-bus]] | [[quick-context/electric-current]] | [[quick-context/embedded-communication-protocols]] | [[quick-context/pcb-printed-circuit-board]] | [[quick-context/pupper-bom-control-board]]

> **See also:** [[quick-context/can-bus]] | [[quick-context/pcb-printed-circuit-board]] | [[quick-context/electric-current]] | [[quick-context/pupper-bom-control-board]] | [[quick-context/embedded-communication-protocols]]

**Definition:** A chip that converts the [[micro-context/microcontroller|microcontroller]]'s digital TX/RX signals into differential voltage signals for the CAN bus (and vice versa). CAN bus is a robust 2-wire communication protocol used in cars and robots where multiple devices share the same wire pair. The MAX3051 handles the electrical interface so the MCU only deals with data.

## How It Works

- The MCU's CAN peripheral generates a serial data stream (TX) using the CAN protocol's bit timing and arbitration rules.
- The transceiver converts this single-ended TX signal into a [[quick-context/differential-pair|differential pair]] (CANH and CANL) with opposite voltage swings.
- On receive, the transceiver subtracts CANL from CANH, canceling any common-mode noise picked up on the wire pair.
- This differential signaling allows reliable multi-drop communication over long cables in electrically noisy environments.

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

**Key insight:** CAN transceivers are why robots can communicate reliably over long cables in electrically noisy environments—the differential signaling rejects interference that would corrupt single-wire connections.
