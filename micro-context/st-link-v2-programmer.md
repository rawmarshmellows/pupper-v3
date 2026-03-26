---
term: ST-Link V2 Programmer
created: 2026-03-25
updated: 2026-03-25
---

# ST-Link V2 Programmer

**Definition:** An in-circuit debugger and programmer for [[micro-context/stm32-microcontroller|STM32]] and STM8 microcontrollers. Connects via USB to your PC and uses a 4-pin [[micro-context/swd-serial-wire-debug|SWD]] cable to flash firmware and set breakpoints on the target chip. The official ST-LINK/V2 (~$22-25, white plastic enclosure) supports SWD + JTAG + SWO trace. Cheap $7-13 clones like the **HiLetgo ST-Link V2** (small aluminum USB stick) use an STM32F103C8T6 internally and support SWD only -- no SWO trace, no JTAG, fixed 3.3V output (the official also outputs at 3.3V but accepts 1.65-3.6V target signals). "Emulator" in clone listings is a translation artifact from Chinese 仿真器 (historically meant in-circuit emulator, now means any debug probe).

```
                 Official (~$25)        Clone (~$10)
                 ┌──────────────┐       ┌──────────────┐
  Protocols:     │ SWD + JTAG   │       │ SWD only     │
  SWO trace:     │ Yes          │       │ No (mod req) │
  Voltage:       │ 1.65-3.6V in │       │ 3.3V fixed   │
  CubeIDE:       │ Full support │       │ Blocked (FW) │
  OpenOCD:       │ Works        │       │ Works        │
  Pinout:        │ Standardized │       │ Varies!      │
                 └──────────────┘       └──────────────┘
  ⚠ NEVER accept firmware upgrade prompts on a clone -- bricks it
```

**Key insight:** HiLetgo and similar clones are functional for hobbyist use with OpenOCD or open-source `stlink` utilities, but ST's official tools (CubeIDE 1.9+) actively block clones via firmware checks. Clones may also contain non-genuine chips (APM32, CKS32) and have inconsistent pinouts between units -- always verify with a multimeter. For hassle-free use, a Nucleo-64 board (~$13-20 depending on variant) includes a detachable genuine ST-Link plus a dev board.
