---
term: Ceramic Resonator
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# Ceramic Resonator[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[micro-context/stm32-microcontroller]] | [[quick-context/pupper-bom-control-board]] | [[quick-context/clock-sources-and-timing|Clock Sources and Timing]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] [[learning/notes/quick-context/meddpicc-qualification-framework|3]]-pin [[learning/notes/quick-context/comparator-specification|timing]] [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|component]] that uses [[learning/notes/quick-context/capacitance|the]] [[micro-context/piezoelectric-effect|piezoelectric effect]] in ceramic material to vibrate at a precise frequency, providing the [[learning/notes/quick-context/bare-minimal-data-storage-circuit|clock]] [[learning/notes/quick-context/comparator|reference]] for [[micro-context/stm32-microcontroller|microcontrollers]]. On the Pupper v3 board, [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] muRata CSTNE8M00G55A000R0 resonators (X1, X2) provide [[learning/notes/quick-context/comparator-specification|8]] MHz references that the STM32's internal PLL multiplies to 180 MHz: $f_{CPU} = 8\[[learning/notes/quick-context/how-source-code-is-stored|text]]{ MHz} \times \frac{180}{8} = 180\text{ MHz}$. Less accurate than quartz crystals (±[[learning/notes/quick-context/meddpicc-qualification-framework|0]].5% vs ±0.002%) but cheaper [[learning/notes/micro-context/push-pull-vs-open-drain|and]] includes built-in 33 pF load [[learning/notes/quick-context/voltage|capacitors]] — [[learning/notes/micro-context/capacitive-voltage-sensing|no]] external caps needed.

## How It Works

- An AC [[learning/notes/quick-context/comparator|signal]] applied to the ceramic element excites mechanical vibrations at its natural resonant frequency [[learning/notes/quick-context/metal-interconnect-layers|via]] the [[learning/notes/micro-context/piezoelectric-effect|piezoelectric effect]].
- The vibrating ceramic feeds back a stable oscillating signal to the MCU's oscillator circuit, locking it to the resonant frequency (8 MHz).
- The STM32's internal PLL multiplies this 8 MHz reference up to the operating frequency (180 MHz).
- Built-in load capacitors (33 pF) eliminate the need for external [[learning/notes/quick-context/tensor|components]], unlike quartz crystals which require two external caps.

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

**Key insight:** The Pupper [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|BOM]] uses ceramic resonators instead of quartz crystals because [[learning/notes/quick-context/embedded-communication-protocols|CAN]] [[learning/notes/quick-context/data-bus-and-arbitration|bus]] tolerates ±0.5% clock error — the built-in load capacitors save two external components per MCU for no practical [[learning/notes/quick-context/rc-oscillator|accuracy]] tradeoff in this application.
