---
term: SPI
created: 2026-02-25
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# SPI[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[quick-context/pupper-bom-control-board]] | [[quick-context/can-bus]] | [[quick-context/embedded-communication-protocols]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/data-bus-and-arbitration|Serial]] Peripheral Interface — [[learning/notes/quick-context/anions-and-oxidation|a]] [[learning/notes/quick-context/similarity-transform|4]]-wire [[learning/notes/quick-context/singular-value-decomposition|full]]-duplex [[learning/notes/quick-context/data-bus-and-arbitration|serial protocol]] where a [[learning/notes/quick-context/data-bus-and-arbitration|master]] clocks data in [[learning/notes/micro-context/push-pull-vs-open-drain|and]] [[learning/notes/micro-context/push-pull-vs-open-drain|out]] of peripherals [[learning/notes/quick-context/bare-minimal-data-storage-circuit|simultaneously]]. Unlike [[micro-context/i2c|I2C]] which uses addresses on a shared [[learning/notes/quick-context/data-bus-and-arbitration|bus]], [[learning/notes/quick-context/embedded-communication-protocols|SPI]] selects each device [[learning/notes/quick-context/breaking-elongation-rate|with]] a dedicated chip-select (CS) line. Runs at [[learning/notes/quick-context/meddpicc-qualification-framework|1]]-50+ MHz — much faster than [[learning/notes/micro-context/i2c|I2C]], but costs an extra pin per device. In [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] [[quick-context/pupper-brain|Pupper]], U1 sends joint targets to U5 over SPI.

## How It Works

- [[learning/notes/quick-context/capacitance|The]] master asserts chip-select (CS) low to activate the target peripheral, then drives the [[learning/notes/quick-context/bare-minimal-data-storage-circuit|clock]] (SCLK).
- On each [[learning/notes/micro-context/clock-edges|clock edge]], the master shifts [[learning/notes/quick-context/ram-addressing-decoder|one]] bit out on MOSI while simultaneously reading one bit in from MISO.
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

**Key insight:** SPI is full-duplex — the master and peripheral exchange one bit on every clock cycle, so reads and writes happen at the same time. This makes it faster but less pin-efficient than I2C, which is the core tradeoff between the [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] most common embedded buses.
