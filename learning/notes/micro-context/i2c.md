---
term: I2C
created: 2026-02-25
updated: 2026-03-27
---

# I2C

> **Related:** [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]] | [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/ads1110-battery-adc]] | [[micro-context/bjt-mosfet-igbt]]

**[[quick-context/capacitance|Definition]]:** Inter-Integrated Circuit — a 2-wire serial protocol (SDA for data, SCL for [[quick-context/bare-minimal-data-storage-circuit|clock]]) that lets a master chip talk to many peripheral chips on the same bus. Each device has a unique 7-bit address, so the master selects who to talk to. Runs at 100 kHz (standard) or 400 kHz ([[quick-context/comparator|fast]] mode). Used in [[quick-context/mcp6541-as-lmc7211-replacement|your]] Pupper for the [[quick-context/pupper-brain|BNO086 IMU and ADS1110 ADC]] communicating with the main STM32.

## How It Works

- The master sends a START condition (SDA goes low while SCL is high), then clocks out the 7-bit slave address plus a read/write bit.
- The addressed slave acknowledges (pulls SDA low during the ACK clock pulse), and data bytes follow in the same clocked fashion.
- [[quick-context/bjt-specifications|Both]] SDA and SCL are [[micro-context/push-pull-vs-open-drain|open-drain]] lines — devices [[quick-context/embedded-communication-protocols|can]] [[quick-context/comparator-specification|only]] pull LOW, and external pull-up resistors hold the lines HIGH by default.
- A [[quick-context/camera-fundamentals|STOP]] condition (SDA goes high while SCL is high) releases the bus for the next transaction.

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

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** I2C lines are open-[[quick-context/differential-pair|drain]] — devices can only pull the line LOW, never drive it HIGH. The [[quick-context/resistor|pull-up resistors]] passively hold lines HIGH, which is why every I2C bus needs them and why getting the pull-up value wrong causes intermittent failures. The I2C spec limits total bus [[quick-context/capacitance|capacitance]] to 400 pF because each device adds ~10 pF in [[quick-context/parallel-vs-series-voltage|parallel]] — exceed this and the pull-up can't charge the line fast enough for reliable communication.
