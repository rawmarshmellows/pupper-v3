---
term: I2C
created: 2026-02-25
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/spi]] | [[learning/notes/micro-context/spinev1-elf|SPIneV1.elf]] | [[learning/notes/quick-context/uart|UART — Universal Asynchronous Receiver/Transmitter]] | [[learning/notes/quick-context/qwiic-stemma-qt-i2c|Qwiic / STEMMA QT — Plug-and-Play I2C Connector Ecosystem]] | [[learning/notes/quick-context/embedded-communication-protocols|Embedded Communication Protocols — UART, I2C, SPI, CAN, RS-232, RS-485, 1-Wire, USB, I3C, and When to Use Each]]

# I2C

> **See also:** [[quick-context/pupper-bom-control-board]] | [[quick-context/can-bus]] | [[quick-context/embedded-communication-protocols]] | pull up pull down resistors

**Definition:** Inter-Integrated Circuit — a 2-wire serial protocol (SDA for data, SCL for clock) that lets a master chip talk to many peripheral chips on the same bus. Each device has a unique 7-bit address, so the master selects who to talk to. Runs at 100 kHz (standard) or 400 kHz (fast mode). Used in your Pupper for the [[quick-context/pupper-brain|BNO086 IMU and ADS1110 ADC]] communicating with the main STM32.

## How It Works

- The master sends a START condition (SDA goes low while SCL is high), then clocks out the 7-bit slave address plus a read/write bit.
- The addressed slave acknowledges (pulls SDA low during the ACK clock pulse), and data bytes follow in the same clocked fashion.
- Both SDA and SCL are open-drain lines — devices can only pull LOW, and external pull-up resistors hold the lines HIGH by default.
- A STOP condition (SDA goes high while SCL is high) releases the bus for the next transaction.

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

**Key insight:** I2C lines are open-drain — devices can only pull the line LOW, never drive it HIGH. The [[quick-context/resistor|pull-up resistors]] passively hold lines HIGH, which is why every I2C bus needs them and why getting the pull-up value wrong causes intermittent failures. The I2C spec limits total bus [[quick-context/capacitance|capacitance]] to 400 pF because each device adds ~10 pF in parallel — exceed this and the pull-up can't charge the line fast enough for reliable communication.
