---
topic: Firmware — Software That Lives on Hardware
created: 2026-03-26
---

# Firmware — Software That Lives on Hardware

> **Related:** [[quick-context/code-to-gates-and-bootstrapping]] | [[quick-context/pupper-brain]] | [[quick-context/pupper-bom-control-board]]

> **TL;DR:** Firmware is software permanently stored in a device's non-volatile memory (typically flash) that runs immediately at power-on without an operating system, bootloader chain, or filesystem. It's the code that makes hardware *be* what it is — the STM32s on the Pupper control board run firmware that turns raw silicon into a motor controller and sensor hub.

## The Core Problem

Hardware alone does nothing. An [[micro-context/stm32-microcontroller|STM32 microcontroller]] fresh from the factory is a general-purpose chip — it could be a motor controller, a thermostat, or a MIDI synthesizer. The firmware is what commits it to a specific job. Without firmware, the Pupper's control board is an inert PCB. With `SPIneV1.elf` [[quick-context/firmware|flashed]] onto the STM32s, it becomes a real-time robot controller reading IMU data, computing joint targets, and driving 12 servos at 1 kHz.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Firmware** | Software stored in non-volatile memory (flash/ROM) that controls hardware directly, typically running bare metal or under an RTOS with no general-purpose OS |
| **Flashing** | Writing compiled firmware into a [[micro-context/microcontroller|microcontroller]]'s flash memory via a debug probe (ST-Link) and debug protocol (SWD) — erases old code, writes new code, resets the chip |
| **ELF file (.elf)** | Executable and Linkable Format — the compiler's output containing machine code, memory layout, and debug symbols; the flash tool extracts the code sections and writes them to the chip |
| **Reset vector** | The hardwired memory address the CPU reads its first instruction from at power-on — on STM32, this is `0x08000000`, the start of flash memory |
| **Bootloader** | Optional firmware that runs before the main firmware, typically to check for updates over USB/[[quick-context/uart|UART]] before jumping to the application code; some STM32 projects skip this and flash the application directly |

<details>
<summary><strong>How It Works</strong></summary>

### From Source Code to Running Robot

Firmware goes through a build-flash-run pipeline that's fundamentally different from desktop software:

```
FIRMWARE PIPELINE (vs. Desktop Software)
================================================================

DESKTOP SOFTWARE:                    FIRMWARE:
  source.py                            main.c, motor.c, imu.c
      │                                    │
  interpreter                          ARM cross-compiler
  or compiler                          (arm-none-eabi-gcc)
      │                                    │
  executable                           SPIneV1.elf
  (.exe, binary)                       (ELF with ARM machine code)
      │                                    │
  OS loads into RAM                    Flash tool extracts code
  from filesystem                      sections from ELF
      │                                    │
  runs under Linux/                    ST-Link writes code to
  macOS/Windows                        STM32's flash via SWD
      │                                    │
  can be stopped,                      Code runs immediately at
  restarted, updated                   power-on, no OS, no
  at any time                          filesystem, no user
                                       intervention
```

### What Happens at Power-On

When the Pupper's battery connects, the STM32 begins executing firmware from flash in microseconds — no boot screen, no kernel, no login:

```
STM32 POWER-ON SEQUENCE:
================================================================

  Power applied
      │
      ▼
  CPU reset: all registers → 0
      │
      ▼
  Read reset vector from 0x08000000
  (first 4 bytes = initial stack pointer)
  (next 4 bytes = address of Reset_Handler function)
      │
      ▼
  Jump to Reset_Handler
      │
      ▼
  ┌─────────────────────────────────┐
  │  SystemInit()                   │  Configure clock tree:
  │  - Enable PLL                   │  8 MHz resonator × PLL
  │  - Set clock to 180 MHz         │  = 180 MHz CPU clock
  │  - Configure flash wait states  │
  └───────────┬─────────────────────┘
              │
              ▼
  ┌─────────────────────────────────┐
  │  Copy .data section             │  Initialized globals
  │  RAM → from flash               │  (e.g., int x = 42)
  │  Zero .bss section              │  Uninitialized globals
  │  (all zero-init globals)        │  (e.g., int count;)
  └───────────┬─────────────────────┘
              │
              ▼
  ┌─────────────────────────────────┐
  │  main()                         │  Your firmware starts:
  │  - Init SPI, CAN, I2C, PWM     │  configure peripherals
  │  - Calibrate IMU                │  set up communication
  │  - Enter 1 kHz control loop     │  begin real-time control
  └─────────────────────────────────┘

  Total time from power-on to main(): ~10-50 milliseconds
  (vs. ~30 seconds for Linux on a Raspberry Pi)
```

### Inside the ELF File

The compiler produces an ELF file that contains more than just code — it's a structured container that the flash tool and debugger both use:

```
SPIneV1.elf STRUCTURE:
================================================================

  ┌─────────────────────────────────────┐
  │  ELF Header                         │  Magic: 7f 45 4c 46
  │  - Architecture: ARM               │  (identifies as ELF)
  │  - Entry point: 0x0800xxxx          │
  ├─────────────────────────────────────┤
  │  .text section                      │  Machine code (ARM
  │  (loaded to 0x0800_0000)            │  Thumb-2 instructions)
  ├─────────────────────────────────────┤
  │  .rodata section                    │  Read-only constants
  │  (loaded to flash, after .text)     │  (lookup tables, strings)
  ├─────────────────────────────────────┤
  │  .data section                      │  Initialized variables
  │  (stored in flash, copied to RAM    │  (copied to SRAM at
  │   at 0x2000_0000 on startup)        │  startup by Reset_Handler)
  ├─────────────────────────────────────┤
  │  .bss section                       │  Zero-initialized vars
  │  (not stored — just a size record;  │  (RAM zeroed at startup)
  │   RAM allocated at 0x2000_xxxx)     │
  ├─────────────────────────────────────┤
  │  .symtab + .strtab                  │  Debug symbols
  │  (NOT flashed to chip — used only   │  (function names,
  │   by GDB for debugging)             │  variable addresses)
  └─────────────────────────────────────┘

  Flash tool: extracts .text + .rodata + .data → writes to flash
  Debugger:   reads .symtab so you can "break main" by name
```

### Linker Script: The Memory Map

The linker script (`.ld` file) tells the compiler where each section goes in the STM32's memory:

```
STM32F446 MEMORY MAP:
================================================================

  0x0800_0000 ┌──────────────────────┐
              │  Vector table        │ ← Reset vector, IRQ handlers
              │  .text (code)        │ ← Your firmware functions
              │  .rodata (constants) │ ← Lookup tables, strings
              │  .data (init values) │ ← Copied to RAM at boot
  0x0807_FFFF └──────────────────────┘
                512 KB Flash (non-volatile)

  0x2000_0000 ┌──────────────────────┐
              │  .data (runtime copy)│ ← Initialized globals
              │  .bss  (zeroed)      │ ← Uninitialized globals
              │  Heap  ↓             │ ← Grows up (rare in firmware)
              │         ...          │
              │  Stack ↓             │ ← Grows down from _estack
  0x2001_FFFF └──────────────────────┘  ← _estack (initial SP)
                128 KB SRAM (volatile)

  0x4000_0000 ┌──────────────────────┐
              │  Peripheral registers│ ← SPI, CAN, I2C, GPIO,
              │  (memory-mapped I/O) │   UART, timers, ADC...
  0x5FFF_FFFF └──────────────────────┘
                Write to address = configure hardware
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

### Firmware vs. Application Software

The fundamental tension is **control vs. convenience**. Firmware gives you direct hardware access and deterministic timing, but you give up everything a general-purpose OS provides:

| | Firmware (STM32) | Application Software (Raspberry Pi) |
|---|---|---|
| **Startup** | ~10 ms to main() | ~30 seconds to shell |
| **Timing** | Deterministic microsecond loops | Non-deterministic (kernel, GC) |
| **Memory** | 128 KB [[micro-context/sram|SRAM]], no virtual memory | 4 GB RAM, full MMU |
| **Storage** | 512 KB flash, no filesystem | 32 GB+ SD card, ext4 |
| **Debugging** | SWD + GDB (hardware breakpoints) | SSH, printf, strace |
| **Updates** | Requires flash tool + physical access | `apt update && apt upgrade` |
| **Languages** | C, C++, Rust (no runtime) | Python, C++, anything |
| **Libraries** | Vendor HAL, hand-rolled drivers | pip, apt, npm |
| **Crash recovery** | Watchdog timer resets chip | systemd restarts process |
| **Concurrency** | Interrupts, DMA, maybe RTOS tasks | Threads, processes, async |

This is exactly why the Pupper uses both — the STM32s run firmware for the 1 kHz motor control loop where a missed deadline means the robot falls, and the Raspberry Pi runs Linux for WiFi, ML inference, voice processing, and everything that doesn't need hard real-time guarantees. See [[quick-context/pupper-brain]] for the full architecture.

### The Update Problem

Desktop software updates are trivial — download, replace, restart. Firmware updates are risky: if power is lost mid-flash, the chip boots into corrupted code and may be unrecoverable ("bricked"). This is why:
- Production devices use **dual-bank flash** (bank A runs while bank B is updated, then swap)
- Bootloaders verify new firmware before committing
- Some systems keep a known-good "golden image" that can't be overwritten
- For the Pupper, you just re-flash via ST-Link — bricking is recoverable because the debug interface bypasses firmware entirely

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

### Flashing SPIneV1.elf onto the Pupper

Here's the actual workflow to get firmware running on the Pupper's control board:

```bash
# 1. Build firmware (or use pre-built .elf)
#    The name "SPIne" = SPI + (Cali)ne — refers to the SPI bridge
#    firmware for motor MCU communication
ls courses/pupper/building/microcontroller-firmware/SPIneV1.elf

# 2. Connect ST-Link to SWD header on control board
#    Pinout: SWDIO, SWCLK, 3.3V, GND
#    ⚠ Verify pinout with multimeter — clone pinouts vary!

# 3. Flash using OpenOCD
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg \
  -c "program SPIneV1.elf verify reset exit"
# OpenOCD reads the ELF, extracts loadable sections,
# erases the required flash sectors, writes the code,
# reads it back to verify, and resets the chip.

# Output you'll see:
# Info : SWD DPIDR 0x2ba01477        ← Cortex-M4 identified
# Info : flash size = 512 kbytes
# Info : erasing sectors 0..4        ← old code wiped
# Info : programming 98304 bytes     ← new code written
# Info : verified 98304 bytes        ← read-back matches
# Info : reset                       ← chip restarts into new firmware

# 4. (Optional) Debug with GDB
arm-none-eabi-gdb SPIneV1.elf
# (gdb) target remote :3333    ← connect to OpenOCD
# (gdb) break main             ← uses .symtab from ELF
# (gdb) continue               ← run until breakpoint
# (gdb) print motor_targets    ← inspect variables by name
```

### Other Common Firmware Formats

```
FILE FORMAT COMPARISON:
================================================================

  Format   │ Contains           │ Used by
  ─────────┼────────────────────┼──────────────────────────
  .elf     │ Code + debug syms  │ GDB, OpenOCD (preferred)
           │ + memory layout    │ Knows WHERE to load code
  ─────────┼────────────────────┼──────────────────────────
  .bin     │ Raw binary image   │ STM32CubeProgrammer
           │ (no metadata)      │ Must specify load address
           │                    │ manually (0x08000000)
  ─────────┼────────────────────┼──────────────────────────
  .hex     │ Intel HEX: ASCII   │ Many flash tools
           │ text with addresses │ Self-describing addresses
           │ encoded per line   │ Human-readable (sort of)
  ─────────┼────────────────────┼──────────────────────────

  .elf → .bin:  arm-none-eabi-objcopy -O binary SPIneV1.elf SPIneV1.bin
  .elf → .hex:  arm-none-eabi-objcopy -O ihex SPIneV1.elf SPIneV1.hex
```

**The one thing most outsiders get wrong about this is...** thinking firmware is just "software for small computers." The difference isn't size — it's the execution model. Desktop software runs *on top of* an operating system that manages memory, schedules tasks, handles crashes, and provides a filesystem. Firmware runs *instead of* an operating system — it IS the lowest layer, talking directly to hardware registers, managing its own interrupts, and executing from the very first instruction at power-on. When your firmware crashes, there's no kernel to catch the exception and restart you — the chip hangs until the watchdog timer fires or someone cycles power.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/code-to-gates-and-bootstrapping]]** — The full compilation chain from source code to logic gates. Firmware lives at layers 4-5 of this chain: compiled to machine code, running directly on the CPU's fetch-execute cycle. The bootstrapping section explains the Reset Vector — the exact mechanism firmware uses to begin executing at power-on.

- **[[quick-context/pupper-brain]]** — The dual-MCU + Raspberry Pi architecture. Explains why Pupper needs firmware on the STM32s (real-time motor control) alongside Linux on the Pi (WiFi, ML, voice). Firmware handles the timing-critical 1 kHz loop; the Pi handles everything else.

- **[[quick-context/pupper-bom-control-board]]** — Every hardware component the firmware interacts with: the STM32F446 MCUs it runs on, the CAN transceivers it drives, the IMU it reads, the audio amplifier it feeds. The BOM is the hardware; the firmware is what makes it move.

- **[[micro-context/stm32-microcontroller]]** — The specific chip this firmware targets. The STM32F446's 512 KB flash, 128 KB SRAM, CAN/SPI/I2C peripherals, and 180 MHz clock define the firmware's constraints.

- **[[quick-context/firmware|flashing firmware]]** — The micro-context companion: a concise definition of the flash process itself (erase → write → verify → reset).

- **[[micro-context/swd-serial-wire-debug]]** — The 2-wire debug protocol used to flash firmware and set breakpoints. Explains the full SWD transaction format, the DAP architecture, and why a $10 clone programmer works for hobbyist use.

- **[[micro-context/plc-programmable-logic-controller]]** — The spectrum of execution environments firmware can target. The Pupper's STM32s run bare metal (no OS), which gives maximum speed but no safety net.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What's the difference between firmware and regular application software?
<details>
<summary>Answer</summary>
Firmware runs directly on hardware with no operating system underneath — it starts at the reset vector on power-on, manages its own memory and interrupts, and talks to hardware registers directly. Application software runs on top of an OS that provides memory management, scheduling, filesystems, and crash recovery. Firmware is stored in non-volatile flash and persists across power cycles without any storage device. See: The Key Tension.
</details>

**Q2:** Why does the flash tool need the `.elf` file rather than just raw machine code?
<details>
<summary>Answer</summary>
The ELF file contains not just machine code but also metadata telling the flash tool *where* to load each section in memory. The `.text` section goes to flash at `0x08000000`, the `.data` section's initial values also go to flash (to be copied to RAM at boot). Without this metadata, the tool wouldn't know the correct load addresses. A raw `.bin` file works too, but you must manually specify the base address. The ELF also contains debug symbols (`.symtab`) that let GDB map addresses to function names. See: How It Works — Inside the ELF File.
</details>

**Q3:** The Pupper has two STM32 MCUs (U1 and U5). Do they run the same firmware?
<details>
<summary>Answer</summary>
No — they run different firmware for different roles. U1 (Main MCU) runs firmware that reads the BNO086 IMU, reads battery [[quick-context/voltage|voltage]], communicates with the Raspberry Pi, and sends audio. U5 (Motor MCU) runs the `SPIneV1` firmware that handles the 1 kHz motor control loop — receiving joint targets from U1 over SPI and commanding all 12 servos via 4 CAN buses. Each MCU is flashed independently. See: [[quick-context/pupper-brain]] and [[quick-context/pupper-bom-control-board]].
</details>

**Q4:** If firmware runs from flash memory, why does the STM32 also need SRAM?
<details>
<summary>Answer</summary>
Code executes from flash, but runtime data needs RAM. The stack (function call frames, local variables), heap (dynamic allocations), `.data` section (initialized global variables copied from flash at boot), and `.bss` section (zero-initialized globals) all live in SRAM. Flash is non-volatile but slow to write and has limited erase cycles (~10,000) — you can't use it as working memory. The CPU reads instructions from flash at full speed (with wait states and cache), but reads/writes data from SRAM at zero wait states. See: How It Works — Linker Script: The Memory Map.
</details>

**Q5:** A firmware update fails halfway — power was lost during the flash erase step. What happens when the chip powers back on, and how would you recover?
<details>
<summary>Answer</summary>
The CPU reads the reset vector from `0x08000000`, but that flash sector was erased and now contains `0xFFFFFFFF` (erased flash reads as all-ones). The CPU attempts to execute at address `0xFFFFFFFF`, which is invalid — the chip immediately hard-faults and hangs. However, it is NOT permanently bricked: the SWD debug interface is implemented in hardware, not firmware, so the ST-Link can still connect, erase the corrupted flash, and write fresh firmware. This is why SWD is the recovery mechanism of last resort — it works regardless of what's in flash. Production devices avoid this with dual-bank flash or bootloaders that verify firmware integrity before jumping to application code. See: [[micro-context/swd-serial-wire-debug]] and The Key Tension — The Update Problem.
</details>

</details>
