---
term: STM32 Microcontroller
created: 2026-01-27
updated: 2026-04-05
---
> **Related:** [[learning/notes/micro-context/microcontroller]] | [[learning/notes/quick-context/uart]] | [[learning/notes/quick-context/firmware]] | [[learning/notes/quick-context/from-code-to-running-firmware]]

# STM32 Microcontroller

> **See also:** [[quick-context/transistor]] | [[quick-context/pcb-chip-transistor-hierarchy]] | [[quick-context/silicon-die]] | [[quick-context/raspberry-pi-5-components]] | [[quick-context/esp32]]

**Definition:** A family of 32-bit ARM Cortex-M microcontrollers made by STMicroelectronics. They're the "brain" of embedded systems—running code, reading sensors, and controlling outputs. The Pupper v3 uses two STM32 MCUs in LQFP64 packages (64-pin, low-profile quad flat package) on its custom PCB. They run at up to 180MHz with hardware support for [[quick-context/can-bus|CAN bus]], [[micro-context/i2c|I2C]], [[micro-context/spi|SPI]], USART, and USB.

## How It Works

- The ARM Cortex-M4 core fetches instructions from on-chip flash, executes them in a pipelined architecture at up to 180MHz, and stores working data in [[learning/notes/micro-context/sram|SRAM]].
- Built-in hardware peripherals (CAN, SPI, I2C, USART, ADC, PWM timers) offload communication and I/O tasks so the CPU can focus on control algorithms.
- Firmware runs bare-metal or under an RTOS, with microsecond-level interrupt response times essential for real-time motor control.

```
STM32 MICROCONTROLLER BLOCK DIAGRAM:

  ┌─────────────────────────────────────────┐
  │              STM32 @ 180MHz             │
  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
  │  │  ARM    │  │  Flash  │  │  SRAM   │  │
  │  │Cortex-M4│  │ (code)  │  │ (data)  │  │
  │  └────┬────┘  └────┬────┘  └────┬────┘  │
  │       └────────────┴───────────┘        │
  │                    │                    │
  │  ┌──────┬──────┬───┴───┬───────┬──────┐  │
  │  │ CAN  │ I2C  │  SPI  │ USART │ GPIO │  │
  │  └──┬───┴──┬───┴───┬───┴───┬───┴──┬───┘  │
  └─────┼──────┼───────┼───────┼──────┼──────┘
        ↓      ↓       ↓       ↓      ↓
     Motors  IMU    Flash   Serial   LEDs
```

## Programming & Debug Interface

The Pupper PCB has two STM32 MCUs, each with a 7-pin [[learning/notes/quick-context/dupont-jumper-wires|JST SH]] connector (CN1) exposing the SWD debug/programming interface plus serial. You flash firmware using an **ST-Link V2** programmer.

### 7-Pin Connector Pinout

```
  JST SH 7-Pin Connector
  ┌───┬───┬──────┬──────────┬──────────┬─────┬─────┐
  │ 1 │ 2 │  3   │    4     │    5     │  6  │  7  │
  │TCK│TMS│ NRST │ USART TX │ USART RX │ VCC │ GND │
  └───┴───┴──────┴──────────┴──────────┴─────┴─────┘
```

### Pin Definitions

| Pin | Name     | Full Name                        | What It Does                                                     |
|-----|----------|----------------------------------|------------------------------------------------------------------|
| 1   | TCK      | Test Clock                       | [[learning/notes/quick-context/switches-to-registers-storing-data|Clock signal]] for the SWD/JTAG debug interface (= [[learning/notes/micro-context/swd-serial-wire-debug|SWCLK]] on ST-Link) |
| 2   | TMS      | Test Mode Select                 | Bidirectional data line for SWD (= [[learning/notes/micro-context/swd-serial-wire-debug|SWDIO]] on ST-Link)            |
| 3   | NRST     | Negative Reset (active-low)      | Resets the MCU when pulled low; the programmer can force a reset |
| 4   | USART TX | USART Transmit                   | Serial output from MCU — for debug logging or communication     |
| 5   | USART RX | USART Receive                    | Serial input to MCU — for receiving commands or data             |
| 6   | VCC      | Voltage Common Collector         | Positive supply voltage (3.3V) — powers the MCU and provides [[learning/notes/quick-context/pwm-controller-circuit|voltage reference]] to programmer |
| 7   | GND      | Ground                           | 0V reference — completes the circuit                             |

### Programming with ST-Link V2

To flash firmware, only **4 wires** are needed from the 7-pin cable to the ST-Link:

```
  7-Pin Cable              ST-Link V2 (20-pin header)
  ─────────                ─────────────────────────
  TCK (pin 1)  ──────────  TCK  (pin 9)  aka SWCLK
  TMS (pin 2)  ──────────  TMS  (pin 7)  aka SWDIO
  VCC (pin 6)  ──────────  VCC  (pin 1 or 2)
  GND (pin 7)  ──────────  GND  (any even pin)
```

The remaining pins (NRST, USART TX, USART RX) are not required for basic SWD programming but are useful for resetting the chip and serial debugging.

**Key insight:** Unlike a Raspberry Pi (which runs Linux), microcontrollers run [[micro-context/plc-programmable-logic-controller|"bare metal" or RTOS]] code with microsecond-level timing precision—essential for real-time motor control in robots.
