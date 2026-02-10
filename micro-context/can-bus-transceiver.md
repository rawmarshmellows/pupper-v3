---
term: CAN Bus Transceiver
created: 2026-01-27
---

# CAN Bus Transceiver

> **See also:** [[quick-context/pcb-printed-circuit-board]] | [[quick-context/electric-current]]

**Definition:** A chip that converts the microcontroller's digital TX/RX signals into differential voltage signals for the CAN bus (and vice versa). CAN bus is a robust 2-wire communication protocol used in cars and robots where multiple devices share the same wire pair. The MAX3051 handles the electrical interface so the MCU only deals with data.

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
