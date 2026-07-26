---
term: SPIneV1.elf
created: 2026-03-26
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/i2c]] | [[learning/notes/quick-context/qwiic-stemma-qt-i2c|Qwiic / STEMMA QT — Plug-and-Play I2C Connector Ecosystem]] | [[learning/notes/quick-context/uart|UART — Universal Asynchronous Receiver/Transmitter]] | [[learning/notes/quick-context/embedded-communication-protocols|Embedded Communication Protocols — UART, I2C, SPI, CAN, RS-232, RS-485, 1-Wire, USB, I3C, and When to Use Each]]

# SPIneV1.elf

**Definition:** The compiled [[learning/notes/quick-context/firmware|firmware]] binary for the Pupper v3's motor control [[micro-context/stm32-microcontroller|STM32F446]] (U5). It receives joint angle targets from the main MCU (U1) over [[micro-context/spi|SPI]], translates them into [[micro-context/can-bus-transceiver|CAN bus]] messages, and sends position commands to all 12 servo motors at 1 kHz. The name "SPIne" likely reflects SPI + CAN interface (the "spine" connecting brain to legs).

## How It Works

- At boot, U5's Cortex-M4 core begins executing SPIneV1 code from flash, initializing SPI (slave to U1) and four [[learning/notes/quick-context/can-bus|CAN bus]] interfaces.
- U1 sends 12 joint angle targets over SPI at 1 kHz; SPIneV1 unpacks them into individual motor commands.
- Each motor command is formatted as a CAN frame and dispatched to the correct bus (one bus per leg, 3 motors each).
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

**Key insight:** The `.elf` format contains both machine code and debug symbols — it gets [[quick-context/firmware|flashed]] onto U5's 512KB flash via [[micro-context/swd-serial-wire-debug|SWD]], but unlike a stripped `.bin`, you can also use it for step-through debugging in STM32CubeIDE.
