---
term: STM32 Microcontroller
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[learning/notes/quick-context/firmware]]

# STM32 Microcontroller

> **See also:** [[learning/notes/quick-context/transistor]] | [[learning/notes/quick-context/pcb-chip-transistor-hierarchy]] | [[learning/notes/quick-context/silicon-die]]

**Definition:** A family of 32-bit ARM Cortex-M microcontrollers made by STMicroelectronics. They're the "brain" of embedded systems—running code, reading sensors, and controlling outputs. The STM32F446 in your Pupper runs at 180MHz with 512KB flash and hardware support for [[learning/notes/quick-context/can-bus|CAN bus]], [[learning/notes/micro-context/i2c|I2C]], [[learning/notes/micro-context/spi|SPI]], and USB.

## How It Works

- The ARM Cortex-M4 core fetches instructions from on-chip flash (512KB), executes them in a pipelined architecture at up to 180MHz, and stores working data in SRAM (128KB).
- Built-in hardware peripherals (CAN, SPI, I2C, UART, ADC, PWM timers) offload communication and I/O tasks so the CPU can focus on control algorithms.
- [[learning/notes/quick-context/firmware|Firmware]] runs bare-metal or under an RTOS, with microsecond-level interrupt response times essential for real-time motor control.

```
STM32 MICROCONTROLLER BLOCK DIAGRAM:

  ┌─────────────────────────────────────────┐
  │            STM32F446 @ 180MHz           │
  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
  │  │  ARM    │  │  Flash  │  │  SRAM   │  │
  │  │Cortex-M4│  │ 512KB   │  │ 128KB   │  │
  │  │  (CPU)  │  │ (code)  │  │ (data)  │  │
  │  └────┬────┘  └────┬────┘  └────┬────┘  │
  │       └────────────┴───────────┘        │
  │                    │                    │
  │  ┌──────┬──────┬───┴───┬──────┬──────┐  │
  │  │ CAN  │ I2C  │  SPI  │ UART │ GPIO │  │
  │  └──┬───┴──┬───┴───┬───┴──┬───┴──┬───┘  │
  └─────┼──────┼───────┼──────┼──────┼──────┘
        ↓      ↓       ↓      ↓      ↓
     Motors  IMU    Flash  Debug   LEDs
```

**Key insight:** Unlike a Raspberry Pi (which runs Linux), microcontrollers run [[learning/notes/micro-context/plc-programmable-logic-controller|"bare metal" or RTOS]] code with microsecond-level timing precision—essential for real-time motor control in robots.
