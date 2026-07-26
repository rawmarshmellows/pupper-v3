---
term: Ceramic Resonator
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/clock-edges|Clock Edge]] | [[learning/notes/micro-context/clock-source]] | [[learning/notes/micro-context/clock-speed-vs-temperature]] | [[learning/notes/micro-context/clock-speed]] | [[learning/notes/quick-context/clock-sources-and-timing]]

# Ceramic Resonator

> **See also:** [[micro-context/stm32-microcontroller]] | [[quick-context/pupper-bom-control-board]] | [[quick-context/clock-sources-and-timing|Clock Sources and Timing]]

**Definition:** A 3-pin timing component that uses the [[micro-context/piezoelectric-effect|piezoelectric effect]] in ceramic material to vibrate at a precise frequency, providing the clock reference for [[micro-context/stm32-microcontroller|microcontrollers]]. On the Pupper v3 board, two muRata CSTNE8M00G55A000R0 resonators (X1, X2) provide 8 MHz references that the STM32's internal PLL multiplies to 180 MHz: $f_{CPU} = 8\text{ MHz} \times \frac{180}{8} = 180\text{ MHz}$. Less accurate than quartz crystals (±0.5% vs ±0.002%) but cheaper and includes built-in 33 pF load capacitors — no external caps needed.

## How It Works

- An AC signal applied to the ceramic element excites mechanical vibrations at its natural resonant frequency via the [[learning/notes/micro-context/piezoelectric-effect|piezoelectric effect]].
- The vibrating ceramic feeds back a stable oscillating signal to the MCU's oscillator circuit, locking it to the resonant frequency (8 MHz).
- The STM32's internal PLL multiplies this 8 MHz reference up to the operating frequency (180 MHz).
- Built-in load capacitors (33 pF) eliminate the need for external components, unlike quartz crystals which require two external caps.

```
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
  │ Type             │ Accuracy  │ Use case         │
  ├──────────────────┼───────────┼──────────────────┤
  │ Ceramic resonator│ ±0.5%    │ CAN, UART, I2C   │
  │ Quartz crystal   │ ±0.002%  │ USB, precision   │
  │ TCXO             │ ±0.0001% │ GPS, RF, timing  │
  └──────────────────┴───────────┴──────────────────┘
```

**Key insight:** The Pupper BOM uses ceramic resonators instead of quartz crystals because [[learning/notes/quick-context/can-bus|CAN bus]] tolerates ±0.5% clock error — the built-in load capacitors save two external components per MCU for no practical accuracy tradeoff in this application.
