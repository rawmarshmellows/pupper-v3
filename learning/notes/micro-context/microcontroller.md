---
term: Microcontroller
created: 2026-03-26
updated: 2026-03-27
---

# Microcontroller

> **See also:** [[quick-context/embedded-communication-protocols]]

> **Related:** [[micro-context/stm32-microcontroller]]

**Definition:** A complete computer on a single chip — CPU, memory (RAM + flash), and I/O peripherals all integrated into one package. Unlike a general-purpose CPU that needs external RAM, storage, and a motherboard, a microcontroller is self-contained and runs a single dedicated program. Common families include [[micro-context/stm32-microcontroller|STM32]] (ARM), [[quick-context/esp32|ESP32]] (Xtensa/RISC-V + integrated WiFi/BLE radio), ATmega (AVR/Arduino), and PIC.

## How It Works

- On power-up, the CPU core begins fetching instructions from a fixed address in on-chip flash memory (the reset vector).
- The program runs in a loop, reading sensor data through peripheral interfaces ([[micro-context/adc-analog-to-digital-converter|ADC]], [[micro-context/i2c|I2C]], [[micro-context/spi|SPI]]), processing it, and driving outputs ([[micro-context/pwm-pulse-width-modulation|PWM]], GPIO, CAN).
- Hardware interrupts allow the MCU to respond to external events (timer tick, incoming data, pin change) within microseconds, pausing the main loop and jumping to a handler.
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

**Key insight:** A microcontroller trades raw power for integration and real-time determinism — it runs [[micro-context/plc-programmable-logic-controller|bare metal or RTOS]] code with microsecond timing, which is why robots, cars, and appliances use them instead of full computers for control tasks.
