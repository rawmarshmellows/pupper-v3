---
term: SPI
created: 2026-02-25
updated: 2026-03-27
---

# SPI

> **See also:** [[quick-context/pupper-bom-control-board]] | [[quick-context/can-bus]] | [[quick-context/embedded-communication-protocols]]

**Definition:** Serial Peripheral Interface — a 4-wire full-duplex serial protocol where a master clocks data in and out of peripherals simultaneously. Unlike [[micro-context/i2c|I2C]] which uses addresses on a shared bus, SPI selects each device with a dedicated chip-select (CS) line. Runs at 1-50+ MHz — much faster than [[micro-context/i2c|I2C]], but costs an extra pin per device. In your [[quick-context/pupper-brain|Pupper]], U1 sends joint targets to U5 over SPI.

## How It Works

- The master asserts chip-select (CS) low to activate the target peripheral, then drives the clock (SCLK).
- On each clock edge, the master shifts one bit out on MOSI while simultaneously reading one bit in from MISO.
- After all bits are clocked, the master de-asserts CS to end the transaction.
- Because data flows in both directions simultaneously, SPI is full-duplex — reads and writes happen in the same clock cycle.

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
