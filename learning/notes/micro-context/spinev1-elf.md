---
term: SPIneV1.elf
created: 2026-03-26
updated: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/quick-context/bare-minimal-data-storage-circuit]] | [[learning/notes/quick-context/code-to-gates-and-bootstrapping]] | [[learning/notes/quick-context/cpu-fetch-execute-cycle]]

# SPIneV1.elf

**Definition:** The compiled firmware binary for the Pupper v3's motor control [[learning/notes/micro-context/microcontroller|STM32F446]] (U5). It receives joint angle targets from the main MCU (U1) over [[micro-context/spi|SPI]], translates them into [[micro-context/can-bus-transceiver|CAN bus]] messages, and sends position commands to all 12 servo motors at 1 kHz. The name "SPIne" likely reflects SPI + CAN interface (the "spine" connecting brain to legs).

## How It Works

- At boot, U5's Cortex-M4 core begins executing SPIneV1 code from flash, initializing SPI (slave to U1) and four [[learning/notes/quick-context/can-bus|CAN bus]] interfaces.
- U1 sends 12 joint angle targets over [[learning/notes/micro-context/spi|SPI]] at 1 kHz; SPIneV1 unpacks them into individual motor commands.
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

**Key insight:** The `.elf` format contains both machine code and debug symbols — it gets [[learning/notes/quick-context/firmware|flashed]] onto U5's 512KB flash via [[micro-context/swd-serial-wire-debug|SWD]], but unlike a stripped `.bin`, you can also use it for step-through debugging in STM32CubeIDE.
