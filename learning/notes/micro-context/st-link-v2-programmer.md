---
term: ST-Link V2 Programmer
created: 2026-03-25
updated: 2026-03-27
---

# ST-Link V2 Programmer

> **See also:** [[micro-context/swd-serial-wire-debug|SWD]] | [[quick-context/firmware|Flashing Firmware]] | [[micro-context/stm32-microcontroller|STM32]] | [[micro-context/spinev1-elf|SPIneV1.elf]]

**Definition:** A debug probe — a [[quick-context/usb-peripheral-hardware|USB]] device that acts as a translator between your PC and an [[micro-context/stm32-microcontroller|STM32]] [[micro-context/microcontroller|microcontroller]]. It speaks USB on one side and the [[micro-context/swd-serial-wire-debug|SWD]] protocol (2 wires: SWDIO + SWCLK) on the other. Its primary role is [[quick-context/firmware|flashing firmware]] — getting compiled code like [[micro-context/spinev1-elf|SPIneV1.elf]] from your computer into the STM32's flash memory. It also enables live debugging via GDB: hardware breakpoints (Cortex-M4 has 6), single-stepping, and real-time register/memory inspection — all through the same 2-wire connection. The official ST-LINK/V2 (~$22-25) supports SWD + JTAG + SWO trace. Cheap $7-13 clones like the **HiLetgo ST-Link V2** (aluminum USB stick) use an STM32F103C8T6 internally and support SWD only. "Emulator" in clone listings is a translation artifact from Chinese 仿真器 (historically meant in-circuit emulator, now means any debug probe).

## How It Works

- Your PC runs OpenOCD (or similar), which sends flash/debug commands over USB bulk transfers to the ST-Link probe.
- Inside the probe, an STM32F103 MCU translates USB commands into SWD signals by bit-banging its GPIO pins (toggling SWDIO and SWCLK in the correct protocol sequence).
- The SWD signals reach the target STM32's Debug Port, which routes read/write requests to the chip's internal flash, [[micro-context/sram|SRAM]], and peripheral registers.
- Responses travel back the same path: target → SWD → ST-Link GPIO → USB → OpenOCD → your screen.

```
  HOW IT WORKS (Pupper workflow):

  Your PC                 ST-Link V2              STM32F446
  ┌──────────┐           ┌──────────┐           ┌──────────────┐
  │ OpenOCD  │           │ Converts │           │ Flash Memory │
  │ reads    │───USB────►│ USB cmds │───SWD────►│ 0x0800_0000  │
  │ .elf file│           │ to SWD   │  (2 wire) │ [new code]   │
  └──────────┘           │ signals  │           │ CPU resets → │
  Also: GDB              └──────────┘           │ runs firmware│
  for live debug                                └──────────────┘

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

## What's Inside the ST-Link

The ST-Link isn't magic — it's just another [[micro-context/microcontroller|microcontroller]] acting as a middleman. Crack open a clone and you'll find an **STM32F103C8T6** (a cheaper, smaller STM32) running proprietary firmware. That internal MCU does two jobs: speak USB to your PC and bit-bang the [[micro-context/swd-serial-wire-debug|SWD]] protocol out its GPIO pins to the target chip.

```
INSIDE THE ST-LINK CLONE (HiLetgo):

  USB connector          STM32F103C8T6                  4-pin header
  ┌────┐          ┌─────────────────────────┐          ┌─────────┐
  │    │          │                         │          │         │
  │    │◄──USB──► │  ┌──────────┐  ┌──────┐ │  GPIO    │  SWDIO ─┼──► Target
  │    │  (bulk   │  │ ST-Link  │  │ GPIO │─┼─────────►│  SWCLK ─┼──► STM32F446
  │    │ endpts)  │  │ Firmware │  │ Pins │ │  bit-    │  3.3V  ─┼──► (power)
  │    │          │  │          │  │      │ │  bang    │  GND   ─┼──► (ground)
  │    │          │  └──────────┘  └──────┘ │          │         │
  │    │          │    72MHz MCU            │          └─────────┘
  └────┘          └─────────────────────────┘
                    Also has: 64KB flash (firmware lives here)
                              20KB SRAM, USB peripheral
```

### The signal flow step by step

Here's what happens when you run `openocd -c "program firmware.bin"`:

**1. USB layer — PC to ST-Link**

OpenOCD sends commands over USB **bulk transfers** (not HID, not serial — raw bulk endpoints). The commands are in ST's proprietary protocol: a binary packet saying things like "do an SWD write to register X with value Y." OpenOCD's `stlink.c` driver knows this protocol via reverse-engineering (ST never published it — the open-source community figured it out).

**2. Firmware layer — inside the ST-Link**

The STM32F103's firmware receives the USB packet, parses the command, and translates it into GPIO operations. For an SWD write, the firmware must:
- Drive SWCLK low/high in sequence (the clock)
- Set SWDIO high/low to send each bit of the [[micro-context/swd-serial-wire-debug|SWD packet]] (request phase: 8 bits)
- Release SWDIO and read back the target's ACK (3 bits)
- Drive SWDIO again to send the 32-bit data + parity

This is called **bit-banging** — the firmware manually toggles GPIO pins in the right sequence and timing to implement the SWD protocol. There's no dedicated SWD hardware peripheral; the firmware does it all in a tight loop.

```
WHAT BIT-BANGING LOOKS LIKE (simplified):

  STM32F103 firmware pseudo-code:

  for each bit in swd_packet:
      set_gpio(SWDIO, bit)     // drive data line
      set_gpio(SWCLK, HIGH)    // clock rising edge — target samples SWDIO
      delay_cycles(n)          // hold for timing
      set_gpio(SWCLK, LOW)     // clock falling edge
      delay_cycles(n)

  // Turnaround: release SWDIO, let target drive it
  set_gpio_input(SWDIO)
  for each ack_bit:
      set_gpio(SWCLK, HIGH)
      ack[i] = read_gpio(SWDIO)   // read target's response
      set_gpio(SWCLK, LOW)
```

The firmware runs at 72MHz, which is fast enough to generate SWD clock signals at 1-4MHz (plenty of cycles per [[micro-context/clock-edges|clock edge]] for the bit-bang loop). The official ST-Link uses a similar approach but with more sophisticated firmware that also handles JTAG and SWO trace.

**3. Wire layer — ST-Link to target**

The GPIO toggles appear as [[micro-context/swd-serial-wire-debug|SWD]] signals on the 4-pin cable. The target STM32F446's Debug Port (DP) receives these, interprets the SWD packet, and performs the requested operation — writing to flash controller registers, reading memory, setting breakpoints, etc. The response travels back the same way: target drives SWDIO → ST-Link firmware reads GPIO → firmware packages USB response → OpenOCD gets the result.

```
COMPLETE ROUND-TRIP (e.g., "write 0xDEADBEEF to address 0x20000000"):

  OpenOCD                ST-Link firmware              Target STM32F446
  ┌───────┐             ┌───────────────┐             ┌─────────────────┐
  │ USB   │  bulk xfer  │ Parse cmd     │  SWD write  │ DP receives     │
  │ packet│────────────►│ Bit-bang GPIO │────────────►│ MEM-AP routes   │
  │       │             │ SWDIO/SWCLK   │             │ to AHB bus      │
  │       │             │               │  SWD ACK    │ Write to SRAM   │
  │ Read  │◄────────────│ Read GPIO     │◄────────────│ ACK = OK (001)  │
  │ result│  bulk xfer  │ Package resp  │             │                 │
  └───────┘             └───────────────┘             └─────────────────┘
          ~1ms USB              ~2-10μs SWD                ~ns internal
          latency               per transaction            bus access
```

### Why this matters

The ST-Link's simplicity is the point — it's just a $1 MCU bit-banging GPIOs. That's why clones can cost $7-13 and still work. The intelligence lives in **OpenOCD on your PC** (which knows how to orchestrate flash erase/write sequences, manage breakpoints, etc.) and in the **target chip's CoreSight debug hardware** (which provides the memory-mapped access). The ST-Link in the middle is a relatively dumb USB-to-SWD bridge.

**Key insight:** The ST-Link is the essential bridge for getting code onto the Pupper's brain — without it, there's no way to program the STM32. For hobbyist use, a $10 clone + OpenOCD provides the same flash/debug experience as official tools. ST's CubeIDE (1.9+) actively blocks clones via firmware checks, but open-source `stlink` utilities work fine. Clone pinouts vary between units — always verify with a multimeter.
