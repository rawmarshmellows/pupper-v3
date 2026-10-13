---
term: SPI
created: 2026-02-25
updated: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/can-bus-termination]] | [[learning/notes/micro-context/can-bus-transceiver]] | [[learning/notes/micro-context/i2c]] | [[learning/notes/micro-context/i2s-audio-amplifier]] | [[learning/notes/micro-context/i2s]]


# SPI

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[quick-context/pupper-bom-control-board]] | [[quick-context/can-bus]] | [[quick-context/embedded-communication-protocols]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** [[learning/notes/quick-context/data-bus-and-arbitration|Serial]] Peripheral Interface — a 4-wire [[learning/notes/quick-context/singular-value-decomposition|full]]-duplex [[learning/notes/quick-context/data-bus-and-arbitration|serial protocol]] where a [[learning/notes/quick-context/data-bus-and-arbitration|master]] clocks data in and out of peripherals [[learning/notes/quick-context/bare-minimal-data-storage-circuit|simultaneously]]. Unlike [[micro-context/i2c|I2C]] which uses addresses on a shared bus, SPI selects each device with a dedicated chip-select (CS) line. Runs at 1-50+ MHz — much faster than [[learning/notes/micro-context/i2c|I2C]], but costs an extra pin per device. In [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] [[quick-context/pupper-brain|Pupper]], U1 sends joint targets to U5 over SPI.

## How It Works

- The master asserts chip-select (CS) low to activate the target peripheral, then drives the [[learning/notes/quick-context/bare-minimal-data-storage-circuit|clock]] (SCLK).
- On each [[learning/notes/micro-context/clock-edges|clock edge]], the master shifts one bit out on MOSI while simultaneously reading one bit in from MISO.
- After all bits are clocked, the master de-asserts CS to end the transaction.
- Because data flows in [[learning/notes/quick-context/bjt-specifications|both]] directions simultaneously, SPI is full-duplex — reads and writes happen in the same clock cycle.

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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** SPI is full-duplex — the master and peripheral exchange one bit on every clock cycle, so reads and writes happen at the same time. This makes it faster but less pin-efficient than I2C, which is the core tradeoff between the two most common embedded buses.
