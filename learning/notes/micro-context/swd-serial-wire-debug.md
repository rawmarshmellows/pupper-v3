---
term: SWD (Serial Wire Debug)
created: 2026-03-25
updated: 2026-03-27
---

# SWD (Serial Wire Debug)

> **See also:** [[micro-context/st-link-v2-programmer|ST-Link V2]] | [[micro-context/stm32-microcontroller|STM32]] | [[micro-context/i2c|I2C]] | [[micro-context/spi|SPI]]

**Definition:** A 2-signal debug protocol designed by ARM for Cortex-M microcontrollers. It replaces the older 4+ wire JTAG interface with just **SWDIO** (bidirectional data) and **SWCLK** (clock), providing the same core debug features: flash programming, breakpoints, single-stepping, and live memory/register inspection. A typical SWD cable adds 3.3V power and GND for a 4-wire connection total.

## How It Works

- The debugger drives SWCLK and exchanges data bidirectionally on SWDIO using a rigid request→ACK→data packet protocol.
- Each SWD transaction accesses the chip's Debug Access Port (DAP), which bridges to the internal bus — giving the debugger the same memory access as the CPU.
- Through this bus access, the debugger can erase and write flash (programming), set hardware breakpoints, single-step instructions, and inspect registers/memory in real time.
- All of this happens over just 2 signal wires (plus power and ground), replacing the older 4+ wire JTAG interface.

## Physical Connection

```
Debugger                         Target MCU
┌────────┐                       ┌──────────┐
│        │── SWDIO (data) ──────►│          │
│ ST-Link│◄── SWDIO (data) ──────│  STM32   │
│   V2   │── SWCLK (clock) ─────►│  Debug   │
│        │                       │  Port    │
│        │── 3.3V ──────────────►│          │
│        │── GND ────────────────│          │
└────────┘                       └──────────┘
             ◄── 4-pin cable ──►

SWDIO is bidirectional: debugger and target take turns
SWCLK is always driven by the debugger (typically 1-4 MHz)
```

## How SWD Fits Into the ARM Debug Architecture

SWD isn't just a wire protocol — it's the transport layer for ARM's **CoreSight** debug architecture. Understanding the layers helps you know what's happening when you click "Debug" in your IDE.

```
YOUR PC                     DEBUG PROBE              TARGET MCU
┌──────────────┐           ┌──────────┐           ┌─────────────────────┐
│  GDB / IDE   │           │          │           │  ┌───────────────┐  │
│  (OpenOCD,   │◄── USB ──►│ ST-Link  │◄── SWD ──►│  │      DP       │  │
│   pyOCD,     │           │          │           │  │ (Debug Port)  │  │
│   STM32Cube) │           └──────────┘           │  └───────┬───────┘  │
└──────────────┘                                  │          │          │
                                                  │  ┌───────▼───────┐  │
  Software layer            Physical layer        │  │   MEM-AP      │  │
  sends commands            converts USB          │  │ (Access Port) │  │
  like "read 0x2000"        to SWD signals        │  └───────┬───────┘  │
                                                  │          │          │
                                                  │  ┌───────▼───────┐  │
                                                  │  │  AHB Bus      │  │
                                                  │  │  (system bus)  │  │
                                                  │  └──┬─────┬──┬───┘  │
                                                  │     │     │  │      │
                                                  │   Flash SRAM CPU    │
                                                  │              Regs   │
                                                  └─────────────────────┘

DP  = Debug Port — the SWD endpoint on the chip. Handles the wire protocol.
AP  = Access Port — bridges from the debug port to the chip's internal buses.
DAP = Debug Access Port = DP + AP together. Every Cortex-M has one.
```

**Key terminology:**
- **DP (Debug Port):** The SWD-facing side. Manages the wire protocol, handshake, and error detection. Every SWD transaction talks to the DP first.
- **MEM-AP (Memory Access Port):** Bridges the DP to the chip's AHB/APB bus. This is what lets an external debugger read/write any memory address — flash, SRAM, peripheral registers — as if it were the CPU itself.
- **DAP (Debug Access Port):** The DP + AP(s) together. The ARM spec name for the whole debug subsystem.

## The SWD Protocol: What Happens on the Wire

Every SWD transaction follows a rigid 3-phase pattern. This is a synchronous protocol — all transitions happen on SWCLK edges, driven by the debugger.

```
        Phase 1          Phase 2        Phase 3
       REQUEST            ACK            DATA
    (8 bits, host→)   (3 bits, ←target) (33 bits, direction varies)
    ┌─┬─┬─┬──┬─┬─┬─┬─┐ ┌─┬─┬─┐ ┌──────────────────────────────────┐
    │1│A│R│A │0│P│S│P│ │O│F│W│ │  32 data bits + 1 parity bit     │
    │ │P│n│ 2│ │a│t│a│ │K│A│A│ │  (host→target for WRITE,         │
    │ │ │W│  │ │r│o│r│ │ │U│I│ │   target→host for READ)          │
    └─┴─┴─┴──┴─┴─┴─┴─┘ └─┴─┴─┘ └──────────────────────────────────┘
     ▲                   ▲
     Start bit = 1       OK  = 001 (success)
     APnDP = 0:DP 1:AP   FAULT = 010 (error)
     RnW = 0:Write 1:Read WAIT = 100 (busy, retry)
     A[1:0] = register
     Parity = even parity of {APnDP, RnW, A[1:0]}
     Stop = 0, Park = 1

TURNAROUND: Between phases where direction changes (host→target or
target→host), there is a 1-cycle "turnaround" period where SWDIO
is tristated. This prevents bus contention — both sides driving
the line simultaneously.

Timing example (Read from DP register):
SWCLK: ⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍⎍
SWDIO: [--8-bit request-->][T][ACK][T][---32-bit data + parity---]
        host drives          ^^      ^^   target drives
                          turnaround    turnaround
                          (host→tgt)    (tgt→host... actually same
                                         direction, so no turn needed
                                         on reads — turn only on
                                         direction changes)
```

**Why this matters practically:** When you see "SWD communication failed" errors in OpenOCD, it usually means the ACK phase returned FAULT or WAIT instead of OK, or the parity check failed (noise on the wire, bad connection). The protocol's built-in error detection is why SWD works reliably with cheap jumper wires at short distances.

## What You Can Do Through SWD

SWD gives the debugger the same bus access as the CPU. Here's what that enables:

| Capability | How it works via SWD |
|---|---|
| **Flash programming** | Write to flash controller registers to unlock flash, erase sectors, then write 32-bit words. The debug probe's software (OpenOCD, STM32CubeProgrammer) automates this sequence. |
| **Hardware breakpoints** | Write a target address into one of the CPU's FPB (Flash Patch and Breakpoint) [[learning/notes/quick-context/comparator|comparator]] registers. Cortex-M4 has 6 hardware breakpoints. When the PC matches, the CPU halts. |
| **Software breakpoints** | Replace an instruction with `BKPT` (0xBExx). Unlimited count but only works in RAM, not flash (without erasing). |
| **Single-stepping** | Set the STEP bit in the Debug Halting Control register (DHCSR). CPU executes one instruction then halts again. |
| **Register inspection** | Read/write all CPU registers (R0-R15, PSR, etc.) through the DCRSR/DCRDR register pair while the CPU is halted. |
| **Live memory view** | Read any address in the memory map without halting the CPU. This is how "live watch" works in IDEs — it polls memory via SWD while the program runs. |
| **SWO trace (optional)** | A third wire (not part of SWD itself) that streams `printf`-style trace data from the ITM (Instrumentation Trace Macrocell). Requires hardware support — official [[micro-context/st-link-v2-programmer|ST-Link V2]] has it, most clones don't. |

## SWD vs JTAG: When Each Wins

```
                          SWD                    JTAG
                    ┌──────────────┐       ┌──────────────┐
  Signal count:     │ 2 (+ pwr/gnd)│       │ 4-5 (+ pwr)  │
  Signals:          │ SWDIO, SWCLK │       │ TDI, TDO,    │
                    │              │       │ TCK, TMS,    │
                    │              │       │ (nTRST opt)  │
  Connector:        │ 4-pin header │       │ 20-pin (std) │
  Daisy-chain:      │ No — 1 device│       │ Yes — scan   │
                    │   per port   │       │   chain      │
  Boundary scan:    │ No           │       │ Yes (IEEE    │
                    │              │       │   1149.1)    │
  Debug features:   │ Same as JTAG │       │ Same as SWD  │
  Speed:            │ ~4 MHz typ   │       │ ~4 MHz typ   │
  Board space:      │ Minimal      │       │ Large header │
  Cortex-M support: │ All          │       │ All          │
  Cortex-A support: │ Some (newer) │       │ All          │
                    └──────────────┘       └──────────────┘

Use SWD when: Single MCU, space-constrained board, Cortex-M
              → This is the Pupper's case (STM32F446, single chip)

Use JTAG when: Multiple devices on one debug chain, need boundary
               scan for board-level testing, or targeting Cortex-A/R
```

**Why SWD won for Cortex-M:** ARM designed SWD specifically for the [[learning/notes/micro-context/microcontroller|microcontroller]] market where boards are small, there's only one debug target, and boundary scan is overkill. The 2-wire protocol reuses the same DAP architecture as JTAG internally — the silicon is almost identical — so there's no feature penalty for the simpler wiring.

## SWD in the Pupper

On the Pupper V3 control board, the [[micro-context/stm32-microcontroller|STM32F446]] exposes SWD on a pin header. The workflow:

```
1. Connect ST-Link clone to SWD header (verify pinout with multimeter!)
2. OpenOCD discovers the DAP and identifies the chip:
     Info : SWD DPIDR 0x2ba01477   ← Cortex-M4 debug port ID
     Info : stm32f4x.cpu: hardware has 6 breakpoints, 4 watchpoints
3. Flash firmware:
     openocd -f interface/stlink.cfg -f target/stm32f4x.cfg \
       -c "program firmware.bin verify reset exit 0x08000000"
4. Or attach GDB for live debugging:
     arm-none-eabi-gdb firmware.elf
     (gdb) target remote :3333
     (gdb) break main
     (gdb) continue
```

The `DPIDR` register (Debug Port ID Register) is the first thing read over SWD — it confirms the target is alive and identifies the ARM core variant. If you see `Error: SWD DPIDR 0x00000000`, the target isn't powered or the wires are wrong.

**Key insight:** SWD gives you god-mode access to the chip's entire memory map through just 2 wires. The protocol is simple enough that a $10 clone programmer running open-source software provides the same flash/debug experience as a $500 J-Link for hobby and coursework use. JTAG only becomes necessary when you're debugging multiple chips on one board or need IEEE boundary scan for manufacturing test.
