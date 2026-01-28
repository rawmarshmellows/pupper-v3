---
term: STM32 Microcontroller
created: 2026-01-27
---

# STM32 Microcontroller

> **See also:** [[quick-context/transistor]] | [[quick-context/pcb-chip-transistor-hierarchy]] | [[quick-context/silicon-die]]

**Definition:** A family of 32-bit ARM Cortex-M microcontrollers made by STMicroelectronics. They're the "brain" of embedded systems—running code, reading sensors, and controlling outputs. The STM32F446 in your Pupper runs at 180MHz with 512KB flash and hardware support for CAN bus, I2C, SPI, and USB.

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

**Key insight:** Unlike a Raspberry Pi (which runs Linux), microcontrollers run "bare metal" or RTOS code with microsecond-level timing precision—essential for real-time motor control in robots.
