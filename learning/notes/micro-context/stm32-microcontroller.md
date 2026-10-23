---
term: STM32 Microcontroller
created: 2026-01-27
updated: 2026-04-05
---

> **Related:** [[learning/notes/micro-context/microcontroller]] | [[learning/notes/micro-context/st-link-v2-programmer]] | [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]]

# STM32 Microcontroller

> **See also:** [[quick-context/transistor]] | [[quick-context/pcb-chip-transistor-hierarchy]] | [[quick-context/silicon-die]] | [[quick-context/raspberry-pi-5-components]] | [[quick-context/esp32]]

**[[learning/notes/quick-context/capacitance|Definition]]:** A family of 32-bit ARM Cortex-M microcontrollers made by STMicroelectronics. They're [[learning/notes/quick-context/capacitance|the]] "brain" of embedded systems—running code, reading sensors, [[learning/notes/micro-context/push-pull-vs-open-drain|and]] controlling outputs. The Pupper v3 uses [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] STM32 MCUs in LQFP64 packages (64-pin, low-profile quad flat [[learning/notes/quick-context/silicon-die|package]]) on its custom PCB. They run at up to 180MHz with [[learning/notes/quick-context/code-to-gates-and-bootstrapping|hardware]] support for [[quick-context/can-bus|CAN bus]], [[micro-context/i2c|I2C]], [[micro-context/spi|SPI]], USART, and USB.

## How It Works

- The ARM Cortex-M4 core fetches instructions from on-chip flash, executes them in a pipelined architecture at up to 180MHz, and stores working data in [[learning/notes/quick-context/ram-addressing-decoder|SRAM]].
- Built-in hardware peripherals ([[learning/notes/quick-context/embedded-communication-protocols|CAN]], [[learning/notes/micro-context/spi|SPI]], [[learning/notes/micro-context/i2c|I2C]], USART, ADC, PWM timers) offload communication and I/O tasks so the CPU can focus on control algorithms.
- [[learning/notes/quick-context/firmware|Firmware]] runs bare-metal or under an RTOS, with microsecond-level [[learning/notes/quick-context/keypress-to-pixel-pipeline|interrupt]] response times essential for real-time motor control.

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

The Pupper PCB has two STM32 MCUs, each with a 7-pin [[learning/notes/quick-context/dupont-jumper-wires|JST SH]] [[learning/notes/quick-context/qwiic-stemma-qt-i2c|connector]] (CN1) exposing the SWD debug/programming interface plus [[learning/notes/quick-context/data-bus-and-arbitration|serial]]. You flash firmware using an **ST-Link V2** programmer.

### 7-Pin Connector Pinout

```
  JST SH 7-Pin Connector
  ┌───┬───┬──────┬──────────┬──────────┬─────┬─────┐
  │ 1 │ 2 │  3   │    4     │    5     │  6  │  7  │
  │TCK│TMS│ NRST │ USART TX │ USART RX │ VCC │ GND │
  └───┴───┴──────┴──────────┴──────────┴─────┴─────┘
```

### Pin Definitions

| Pin | Name     | [[learning/notes/quick-context/singular-value-decomposition|Full]] Name                        | [[learning/notes/quick-context/bare-minimal-data-storage-circuit|What]] It Does                                                     |
|-----|----------|----------------------------------|------------------------------------------------------------------|
| 1   | TCK      | Test [[learning/notes/quick-context/bare-minimal-data-storage-circuit|Clock]]                       | [[learning/notes/quick-context/switches-to-registers-storing-data|Clock signal]] for the SWD/JTAG debug interface (= [[learning/notes/micro-context/swd-serial-wire-debug|SWCLK]] on ST-Link) |
| 2   | TMS      | Test Mode Select                 | [[learning/notes/quick-context/data-bus-and-arbitration|Bidirectional]] data line for SWD (= [[learning/notes/micro-context/swd-serial-wire-debug|SWDIO]] on ST-Link)            |
| 3   | NRST     | Negative Reset (active-low)      | Resets the MCU [[learning/notes/quick-context/bare-minimal-data-storage-circuit|when]] pulled low; the programmer can force a reset |
| 4   | USART TX | USART Transmit                   | Serial output from MCU — for debug [[learning/notes/quick-context/pupper-lab5-neural-controller|logging]] or communication     |
| 5   | USART RX | USART Receive                    | Serial input to MCU — for receiving commands or data             |
| 6   | [[learning/notes/quick-context/qwiic-stemma-qt-i2c|VCC]]      | [[learning/notes/quick-context/voltage|Voltage]] Common Collector         | Positive supply voltage (3.3V) — powers the MCU and provides voltage [[learning/notes/quick-context/comparator|reference]] to programmer |
| 7   | [[learning/notes/quick-context/qwiic-stemma-qt-i2c|GND]]      | Ground                           | 0V reference — completes the circuit                             |

### Programming with ST-Link V2

To flash firmware, [[learning/notes/quick-context/comparator-specification|only]] **4 [[learning/notes/quick-context/uart|wires]]** are needed from the 7-pin cable to the ST-Link:

```
  7-Pin Cable              ST-Link V2 (20-pin header)
  ─────────                ─────────────────────────
  TCK (pin 1)  ──────────  TCK  (pin 9)  aka SWCLK
  TMS (pin 2)  ──────────  TMS  (pin 7)  aka SWDIO
  VCC (pin 6)  ──────────  VCC  (pin 1 or 2)
  GND (pin 7)  ──────────  GND  (any even pin)
```

The remaining pins (NRST, USART TX, USART RX) are [[learning/notes/micro-context/can-bus-termination|not]] required for [[learning/notes/quick-context/playbook-main|basic]] SWD programming but are useful for resetting the chip and serial [[learning/notes/quick-context/firmware|debugging]].

**Key insight:** Unlike a Raspberry Pi (which runs Linux), microcontrollers run [[micro-context/plc-programmable-logic-controller|"bare metal" or RTOS]] code with microsecond-level [[learning/notes/quick-context/comparator-specification|timing]] precision—essential for real-time motor control in robots.
