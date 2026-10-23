---
term: I2C
created: 2026-02-25
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# I2C

> **See also:** [[quick-context/pupper-bom-control-board]] | [[quick-context/can-bus]] | [[quick-context/embedded-communication-protocols]] | pull-up-pull-down-resistors

**[[learning/notes/quick-context/capacitance|Definition]]:** Inter-[[learning/notes/quick-context/playbook-main|Integrated]] Circuit — a 2-wire [[learning/notes/quick-context/data-bus-and-arbitration|serial protocol]] ([[learning/notes/quick-context/qwiic-stemma-qt-i2c|SDA]] for data, [[learning/notes/quick-context/qwiic-stemma-qt-i2c|SCL]] for [[learning/notes/quick-context/bare-minimal-data-storage-circuit|clock]]) that lets a [[learning/notes/quick-context/data-bus-and-arbitration|master]] chip talk to many peripheral chips on [[learning/notes/quick-context/capacitance|the]] same [[learning/notes/quick-context/data-bus-and-arbitration|bus]]. Each device has a unique 7-bit [[learning/notes/quick-context/how-source-code-is-stored|address]], so the master selects who to talk to. Runs at 100 kHz (standard) or 400 kHz ([[learning/notes/quick-context/comparator|fast]] mode). Used in [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] Pupper for the [[quick-context/pupper-brain|BNO086 IMU and ADS1110 ADC]] communicating with the main STM32.

## How It Works

- The master sends a START condition (SDA goes low while SCL is high), then clocks [[learning/notes/micro-context/push-pull-vs-open-drain|out]] the 7-bit slave address plus a read/[[learning/notes/quick-context/d-flip-flop|write]] bit.
- The addressed slave acknowledges (pulls SDA low during the ACK clock pulse), [[learning/notes/micro-context/push-pull-vs-open-drain|and]] data [[learning/notes/quick-context/how-source-code-is-stored|bytes]] follow in the same clocked fashion.
- [[learning/notes/quick-context/bjt-specifications|Both]] SDA and SCL are [[learning/notes/micro-context/push-pull-vs-open-drain|open-drain]] lines — devices [[learning/notes/quick-context/embedded-communication-protocols|can]] [[learning/notes/quick-context/comparator-specification|only]] [[learning/notes/micro-context/push-pull-vs-open-drain|pull LOW]], and external pull-up resistors [[learning/notes/quick-context/d-flip-flop|hold]] the lines HIGH by default.
- A [[learning/notes/quick-context/camera-fundamentals|STOP]] condition (SDA goes high while SCL is high) releases the bus for the next transaction.

```
          VCC
           │          │
          ┌┴┐        ┌┴┐    ← [[micro-context/smd-resistor|Pull-up resistors]]
          │R│        │R│       (typically 4.7kΩ)
          └┬┘        └┬┘
  SDA ─────┼──────────┼─────────┼───
  SCL ─────┼──────────┼─────────┼───
           │          │         │
      ┌────┴────┐ ┌───┴───┐ ┌──┴────┐
      │ Master  │ │ Slave │ │ Slave │
      │ (STM32) │ │ 0x4A  │ │ 0x48  │
      └─────────┘ └───────┘ └───────┘

  START → [Address + R/W] → ACK → [Data] → ACK → STOP
```

**Key insight:** [[learning/notes/quick-context/embedded-communication-protocols|I2C]] lines are open-[[learning/notes/quick-context/differential-pair|drain]] — devices can only pull the line LOW, never drive it HIGH. The [[quick-context/resistor|pull-up resistors]] passively hold lines HIGH, which is [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] every I2C bus needs them and why getting the pull-up value wrong causes intermittent failures. The I2C spec limits [[learning/notes/quick-context/similarity-transform|total]] bus [[quick-context/capacitance|capacitance]] to [[learning/notes/quick-context/capacitance|400 pF]] because each device adds ~10 pF in [[learning/notes/quick-context/parallel-vs-series-voltage|parallel]] — exceed this and the pull-up can't [[learning/notes/quick-context/cations-and-reduction|charge]] the line fast enough for [[learning/notes/quick-context/ros2-architecture|reliable]] communication.
