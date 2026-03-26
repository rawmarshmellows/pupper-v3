---
term: SPI
created: 2026-02-25
---

# SPI

**Definition:** Serial Peripheral Interface — a 4-wire full-duplex serial protocol where a master clocks data in and out of peripherals simultaneously. Unlike [[micro-context/i2c|I2C]] which uses addresses on a shared bus, SPI selects each device with a dedicated chip-select (CS) line. Runs at 1-50+ MHz — much faster than I2C, but costs an extra pin per device. In your [[quick-context/pupper-brain|Pupper]], U1 sends joint targets to U5 over SPI.

```
  Master (STM32)                Peripheral
  ┌───────────┐                ┌──────────┐
  │       SCLK├───────────────→│SCLK      │
  │       MOSI├───────────────→│MOSI (in) │
  │       MISO│←───────────────┤MISO (out)│
  │         CS├───────────────→│CS        │
  └───────────┘                └──────────┘

  CS:   ────┐                                    ┌────
            └────────────────────────────────────┘
  SCLK: ────────┐       ┌───┐       ┌───┐       ┌───
                └───────┘   └───────┘   └───────┘
  MOSI: ════════╪═══════════╪═══════════╪═══════════╪═  →
               b7         b6         b5         b4
  MISO: ════════╪═══════════╪═══════════╪═══════════╪═  ←
               b7         b6         b5         b4
                  (simultaneous both directions)
```

**Key insight:** SPI is full-duplex — the master and peripheral exchange one bit on every clock cycle, so reads and writes happen at the same time. This makes it faster but less pin-efficient than I2C, which is the core tradeoff between the two most common embedded buses.
