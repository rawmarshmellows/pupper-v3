---
term: Microcontroller
created: 2026-03-26
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/stm32-microcontroller]] | [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]]

# Microcontroller

> **See also:** [[quick-context/embedded-communication-protocols]]

**[[learning/notes/quick-context/capacitance|Definition]]:** A complete computer on a single chip — CPU, [[learning/notes/quick-context/bare-minimal-data-storage-circuit|memory]] (RAM + flash), [[learning/notes/micro-context/push-pull-vs-open-drain|and]] I/O peripherals all [[learning/notes/quick-context/playbook-main|integrated]] into [[learning/notes/quick-context/ram-addressing-decoder|one]] [[learning/notes/quick-context/silicon-die|package]]. Unlike a [[learning/notes/quick-context/singular-value-decomposition|general]]-purpose CPU that needs external RAM, [[learning/notes/quick-context/3d-printing-filament-refill-vs-spool|storage]], and a motherboard, a microcontroller is self-contained and runs a single dedicated program. Common families include [[micro-context/stm32-microcontroller|STM32]] (ARM), [[quick-context/esp32|ESP32]] (Xtensa/RISC-V + integrated WiFi/BLE radio), ATmega (AVR/Arduino), and PIC.

## How It Works

- On [[learning/notes/quick-context/d-flip-flop|power]]-up, [[learning/notes/quick-context/capacitance|the]] CPU core begins fetching instructions from a fixed [[learning/notes/quick-context/how-source-code-is-stored|address]] in on-chip flash memory (the [[learning/notes/quick-context/firmware|reset vector]]).
- The program runs in a loop, reading sensor data through peripheral interfaces (ADC, [[learning/notes/micro-context/i2c|I2C]], [[learning/notes/micro-context/spi|SPI]]), processing it, and driving outputs (PWM, [[learning/notes/quick-context/raspberry-pi-5-components|GPIO]], [[learning/notes/quick-context/embedded-communication-protocols|CAN]]).
- [[learning/notes/quick-context/code-to-gates-and-bootstrapping|Hardware]] [[learning/notes/quick-context/keypress-to-pixel-pipeline|interrupts]] allow the MCU to respond to external events (timer tick, incoming data, pin change) within microseconds, pausing the main loop and jumping to a handler.
- All of this — CPU, memory, and peripherals — runs on a single chip costing $0.20–$15, powered by milliwatts.

```
MICROCONTROLLER vs GENERAL-PURPOSE CPU:

  Microcontroller (e.g. STM32)       Desktop CPU (e.g. x86)
  ┌───────────────────────┐          ┌──────────┐
  │  CPU core  ┌───────┐  │          │ CPU core │
  │  ┌──────┐  │ Flash │  │          └────┬─────┘
  │  │ RAM  │  │(program)│ │               │ bus
  │  └──────┘  └───────┘  │          ┌────┴─────┐
  │  GPIO  SPI  I2C  CAN  │          │ External │
  │  UART  ADC  PWM  USB  │          │ RAM, SSD │
  └───────────┬───────────┘          │ GPU, I/O │
         one chip                    └──────────┘
       $0.20 - $15+                     needs a motherboard
```

**Key insight:** A microcontroller trades raw power for integration and real-time determinism — it runs [[micro-context/plc-programmable-logic-controller|bare metal or RTOS]] code with microsecond [[learning/notes/quick-context/comparator-specification|timing]], which is [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] robots, cars, and appliances use them instead of [[learning/notes/quick-context/singular-value-decomposition|full]] computers for control tasks.
