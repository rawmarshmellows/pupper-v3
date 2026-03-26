---
term: I2C
created: 2026-02-25
---

# I2C

**Definition:** Inter-Integrated Circuit — a 2-wire serial protocol (SDA for data, SCL for clock) that lets a master chip talk to many peripheral chips on the same bus. Each device has a unique 7-bit address, so the master selects who to talk to. Runs at 100 kHz (standard) or 400 kHz (fast mode). Used in your Pupper for the [[quick-context/pupper-brain|BNO086 IMU and ADS1110 ADC]] communicating with the main STM32.

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

**Key insight:** I2C lines are open-drain — devices can only pull the line LOW, never drive it HIGH. The [[quick-context/resistor|pull-up resistors]] passively hold lines HIGH, which is why every I2C bus needs them and why getting the pull-up value wrong causes intermittent failures.
