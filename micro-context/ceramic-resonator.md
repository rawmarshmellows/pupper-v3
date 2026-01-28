---
term: Ceramic Resonator
created: 2026-01-27
---

# Ceramic Resonator

> **See also:** [[quick-context/transistor]] | [[micro-context/stm32-microcontroller]]

**Definition:** A 3-pin timing component that vibrates at a precise frequency (8MHz in your Pupper) to provide the clock signal for microcontrollers. Less accurate than quartz crystals (±0.5% vs ±0.002%) but cheaper and includes built-in load capacitors—good enough for CAN bus and UART communication.

```
CERAMIC RESONATOR vs CRYSTAL:

  Ceramic Resonator (3-pin)      Quartz Crystal (2-pin)
  ┌─────────────────────┐        ┌───────────────┐
  │    ┌───┐            │        │   ┌─────┐     │
  │  ┌─┤ R ├─┐          │        │   │XTAL │     │
  │  │ └───┘ │          │        │   └──┬──┘     │
  │ ═══     ═══  built- │        │      │        │
  │  │       │   in     │        │  needs external
  │  └───┬───┘   caps   │        │  load capacitors
  └──────┼──────────────┘        └──────┼────────┘
     IN GND OUT                     X1    X2

  ACCURACY COMPARISON:
  ┌──────────────────┬───────────┬─────────────────┐
  │ Type             │ Accuracy  │ Use case        │
  ├──────────────────┼───────────┼─────────────────┤
  │ Ceramic resonator│ ±0.5%     │ CAN, UART, I2C  │
  │ Quartz crystal   │ ±0.002%   │ USB, precision  │
  │ TCXO             │ ±0.0001%  │ GPS, RF, timing │
  └──────────────────┴───────────┴─────────────────┘
```

**Key insight:** Your BOM uses ceramic resonators because CAN bus tolerates ±0.5% clock error—crystals would cost more and require extra capacitors for no practical benefit in this application.
