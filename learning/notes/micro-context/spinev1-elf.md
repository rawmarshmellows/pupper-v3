---
term: SPIneV1.elf
created: 2026-03-26
updated: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/microcontroller]] | [[learning/notes/micro-context/scan-loop]] | [[learning/notes/micro-context/st-link-v2-programmer]]


# SPIneV1.elf

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** The compiled [[learning/notes/quick-context/firmware|firmware]] binary for the Pupper v3's motor control [[micro-context/stm32-microcontroller|STM32F446]] (U5). It receives joint angle targets from the main MCU (U1) over [[micro-context/spi|SPI]], translates them into [[micro-context/can-bus-transceiver|CAN bus]] [[learning/notes/quick-context/ros2-architecture|messages]], and sends position commands to all 12 servo motors at 1 kHz. The name "SPIne" likely reflects [[learning/notes/micro-context/spi|SPI]] + CAN interface (the "spine" connecting brain to legs).

## How It Works

- At boot, U5's Cortex-M4 core begins executing SPIneV1 code from flash, initializing SPI (slave to U1) and [[learning/notes/quick-context/ram-addressing-decoder|four]] CAN bus interfaces.
- U1 sends 12 joint angle targets over SPI at 1 kHz; SPIneV1 unpacks them into individual motor commands.
- Each motor command is formatted as a CAN [[learning/notes/quick-context/can-bus|frame]] and dispatched to the correct bus (one bus per leg, 3 motors each).
- The servo motors receive their CAN position commands and close their own internal PID loops to reach the target angles.

```
SPIneV1 FIRMWARE — WHAT IT DOES ON U5:

  U1 (Main MCU)         U5 (Motor MCU)         Servos
  ┌──────────┐   SPI    ┌──────────────┐  CAN   ┌─────┐
  │ IMU read │─────────►│  SPIneV1.elf │──Bus1─►│ x3  │
  │ Control  │  joint   │              │──Bus2─►│ x3  │
  │ calc     │  targets │ SPI → CAN    │──Bus3─►│ x3  │
  └──────────┘          │ translation  │──Bus4─►│ x3  │
                        └──────────────┘        └─────┘
                                              12 motors
```

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** The `.elf` format contains [[learning/notes/quick-context/bjt-specifications|both]] [[learning/notes/quick-context/python-to-machine-code-pipeline|machine code]] and debug symbols — it gets [[quick-context/firmware|flashed]] onto U5's 512KB flash via [[micro-context/swd-serial-wire-debug|SWD]], but unlike a stripped `.bin`, you can also use it for step-through [[learning/notes/quick-context/firmware|debugging]] in STM32CubeIDE.
