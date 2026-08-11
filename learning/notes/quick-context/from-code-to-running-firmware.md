---
topic: From Code to Running Firmware — Linking, Flashing, and Booting on an MCU
created: 2026-03-26
---

# From Code to Running Firmware

> **Related:** [[quick-context/code-to-gates-and-bootstrapping]] | [[quick-context/pupper-brain]]

> **TL;DR:** After the compiler produces object files, the **linker** combines them using a **linker script** that maps code and data to physical memory regions (flash at `0x08000000`, RAM at `0x20000000`). The result is an **ELF file** containing machine code, initialized data, and debug symbols. A debug probe [[quick-context/firmware|flashes]] the relevant sections into the MCU's flash memory. On power-up, the CPU loads the stack pointer from address 0x0, jumps to `Reset_Handler`, which copies `.data` from flash to RAM, zeros `.bss`, calls `SystemInit()`, and finally calls `main()`.

## The Core Problem

The [[quick-context/code-to-gates-and-bootstrapping|compilation chain]] explains how source code becomes machine instructions, but it stops at "binary instructions." A real [[micro-context/microcontroller|microcontroller]] has two distinct memories (flash and RAM) at fixed addresses, a vector table the CPU reads on boot, and startup code that must run before your `main()` function. The linker, linker script, ELF format, flash programmer, and startup code are the missing layers between "compiled object files" and "robot legs moving."

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Linker** | The tool (e.g., `arm-none-eabi-ld`) that combines compiled object files (`.o`) into a single executable, resolving symbol references (e.g., connecting a `call motor_update` to the actual function address) and placing everything at the correct memory addresses. |
| **Linker Script** (`.ld`) | A configuration file that tells the linker where physical memory lives — flash origin, RAM origin, their sizes — and which code/data sections go where. It's the bridge between the software world (sections) and the hardware world (memory addresses). |
| **ELF** (Executable and Linkable Format) | The output file format containing machine code (`.text`), initialized data (`.data`), the vector table (`.isr_vector`), debug symbols (DWARF), and a header describing where each section belongs in memory. The flash tool reads the ELF to know what bytes go where. |
| **Vector Table** | An array of 32-bit addresses at the very start of flash. Entry 0 is the initial stack pointer, entry 1 is the `Reset_Handler` address, and entries 2+ are exception/interrupt handler addresses. The CPU reads entries 0 and 1 from hardware on every reset — no software involved. |
| **Startup Code** (`startup_*.s`) | Assembly code that runs before `main()`. It defines the vector table, copies initialized globals from flash to RAM (`.data`), zeros uninitialized globals (`.bss`), calls `SystemInit()` to configure clocks, then calls `main()`. |

<details>
<summary><strong>How It Works</strong> — From object files to running code</summary>

### The Full Pipeline

The [[quick-context/code-to-gates-and-bootstrapping|compilation chain]] gets you from source to object files. This document picks up from there:

```
THE LINK → FLASH → BOOT PIPELINE
================================================================================

  SOURCE CODE          COMPILER             OBJECT FILES
  ┌──────────┐        ┌──────────┐        ┌──────────────┐
  │ main.c   │──gcc──►│ main.o   │        │ .text (code) │
  │ can.c    │──gcc──►│ can.o    │        │ .data (init) │
  │ spi.c    │──gcc──►│ spi.o    │        │ .bss (uninit)│
  │startup.s │──as───►│startup.o │        │ .rodata      │
  └──────────┘        └──────────┘        └──────┬───────┘
                                                 │
                      LINKER + LINKER SCRIPT      │
                      ┌──────────────────────┐   │
                      │ STM32F446RETX_FLASH.ld│◄──┘
                      │                      │
                      │ MEMORY {             │
                      │   FLASH: 0x08000000  │
                      │   RAM:   0x20000000  │
                      │ }                    │
                      └──────────┬───────────┘
                                 │
                            ELF FILE
                      ┌──────────▼───────────┐
                      │   SPIneV1.elf         │
                      │  ┌─────────────────┐  │
                      │  │ .isr_vector     │  │ → flash @ 0x08000000
                      │  │ .text (code)    │  │ → flash
                      │  │ .rodata (const) │  │ → flash
                      │  │ .data (init val)│  │ → flash (copied to RAM at boot)
                      │  │ .bss (zeros)    │  │ → RAM (zeroed at boot)
                      │  │ .debug_* (DWARF)│  │ → not flashed (debug only)
                      │  └─────────────────┘  │
                      └──────────┬────────────┘
                                 │
                      FLASH PROGRAMMER
                      ┌──────────▼────────────┐
                      │ OpenOCD / ST-Link      │
                      │ Reads ELF, extracts    │
                      │ loadable sections,     │
                      │ writes to flash via    │
                      │ SWD debug probe        │
                      └──────────┬────────────┘
                                 │
                      MCU BOOTS
                      ┌──────────▼────────────┐
                      │ CPU reads vector table │
                      │ → Reset_Handler runs   │
                      │ → copies .data to RAM  │
                      │ → zeros .bss in RAM    │
                      │ → SystemInit() (clocks)│
                      │ → main()               │
                      └───────────────────────┘
```

### The Linker Script — Mapping Software to Hardware

The linker script is a short text file that answers two questions: **where is the memory?** and **what goes where?**

```
STM32F446 LINKER SCRIPT (simplified)
================================================================================

/* Question 1: Where is the physical memory? */
MEMORY
{
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
  RAM   (rwx) : ORIGIN = 0x20000000, LENGTH = 128K
}

/* Question 2: What goes where? */
SECTIONS
{
  .isr_vector :          /* Vector table — MUST be first in flash */
  {
    KEEP(*(.isr_vector))
  } > FLASH

  .text :                /* All code — goes in flash (read+execute) */
  {
    *(.text)
    *(.text*)
  } > FLASH

  .rodata :              /* Constants, string literals — flash */
  {
    *(.rodata)
  } > FLASH

  .data :                /* Initialized globals — stored in flash, */
  {                      /* but addressed in RAM                    */
    _sdata = .;          /* ← startup code uses these symbols       */
    *(.data)
    _edata = .;
  } > RAM AT> FLASH      /* ← the magic: lives in RAM, loaded from flash */

  .bss :                 /* Uninitialized globals — RAM only */
  {
    _sbss = .;
    *(.bss)
    _ebss = .;
  } > RAM
}

_estack = ORIGIN(RAM) + LENGTH(RAM);  /* Stack starts at top of RAM */
```

The critical line is `> RAM AT> FLASH`. This tells the linker: "the CPU will access `.data` variables at RAM addresses, but store their initial values in flash." The startup code bridges this gap by copying the data at boot.

### Memory Layout After Flashing

```
FLASH (0x08000000)                    RAM (0x20000000)
┌─────────────────────────┐           ┌──────────────────────┐
│ 0x0800_0000: Vector     │           │ 0x2000_0000:         │
│   Table                 │           │   .data              │
│   [MSP init value]      │           │   (copied from flash │
│   [Reset_Handler addr]  │           │    by startup code)  │
│   [NMI_Handler addr]    │           │                      │
│   [HardFault addr]      │           ├──────────────────────┤
│   [... 80+ vectors]     │           │   .bss               │
├─────────────────────────┤           │   (zeroed by startup │
│ .text                   │           │    code)             │
│   (all compiled code)   │           ├──────────────────────┤
│                         │           │   Heap ↓             │
├─────────────────────────┤           │                      │
│ .rodata                 │           │                      │
│   (const strings, etc)  │           │   (free space)       │
├─────────────────────────┤           │                      │
│ .data (init values)     │           │             ↑ Stack  │
│   (source for RAM copy) │           │ 0x2002_0000: _estack │
└─────────────────────────┘           └──────────────────────┘
  Persists without power               Lost on power-off
  Read + Execute                        Read + Write + Execute
```

### The Boot Sequence — What Happens at Power-On

When the [[micro-context/stm32-microcontroller|STM32]] powers on (or resets), the hardware does two things with zero software involvement:

1. Loads the value at address `0x00000000` into the **Main Stack Pointer** (MSP)
2. Loads the value at address `0x00000004` into the **Program Counter** (PC) — this is the `Reset_Handler` address

On [[learning/notes/micro-context/stm32-microcontroller|STM32]], flash at `0x08000000` is aliased to `0x00000000` by default, so the vector table at the start of flash is what the CPU sees.

Then `Reset_Handler` (assembly code in `startup_stm32f446retx.s`) runs:

```
BOOT SEQUENCE TIMELINE
================================================================================

  Power on / Reset
       │
       ▼
  ┌─ HARDWARE (no software) ──────────────────────────────────┐
  │  1. Load MSP from address 0x00000000 (top of RAM)         │
  │  2. Load PC from address 0x00000004 (Reset_Handler addr)  │
  │  3. Jump to Reset_Handler                                  │
  └───────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─ Reset_Handler (startup_stm32f446retx.s) ─────────────────┐
  │                                                            │
  │  4. Copy .data from flash to RAM:                          │
  │     src = _sidata (flash address of .data init values)     │
  │     dst = _sdata  (RAM start of .data section)             │
  │     end = _edata  (RAM end of .data section)               │
  │     memcpy(dst, src, end - dst)                            │
  │                                                            │
  │  5. Zero .bss in RAM:                                      │
  │     start = _sbss                                          │
  │     end   = _ebss                                          │
  │     memset(start, 0, end - start)                          │
  │                                                            │
  │  6. Call SystemInit()                                      │
  │     → Configures PLL to multiply 8 MHz crystal to 180 MHz │
  │     → Enables FPU (Cortex-M4 has hardware float)           │
  │                                                            │
  │  7. Call __libc_init_array()                               │
  │     → Runs C++ constructors, C init functions              │
  │                                                            │
  │  8. Call main()  ← YOUR CODE STARTS HERE                   │
  └────────────────────────────────────────────────────────────┘
```

Steps 4-5 are why the linker script exports symbols like `_sdata`, `_edata`, `_sbss`, `_ebss`, `_sidata` — the startup assembly code references them to know where to copy and zero.

</details>

<details>
<summary><strong>The Key Tension</strong> — Flash vs. RAM and the .data problem</summary>

The fundamental tension in embedded firmware is: **code and constants can live in flash (cheap, large, persistent), but variables must live in RAM (expensive, small, volatile)**. This creates the `.data` problem.

A global variable like `int speed = 100;` needs to be `100` when your code first reads it. But RAM is empty after power-on. The only persistent storage is flash. So the initial value `100` must be stored in flash, then copied to RAM before `main()` runs. This is why:

- The linker script has the cryptic `> RAM AT> FLASH` directive
- The startup code does a flash-to-RAM copy loop
- The ELF file has *two* addresses for `.data`: the **VMA** (Virtual Memory Address, where the CPU accesses it in RAM) and the **LMA** (Load Memory Address, where the flash programmer writes it)

| Section | Stored in | Accessed from | Why |
|---------|----------|---------------|-----|
| `.text` | Flash | Flash | Code is read-only, executes in place |
| `.rodata` | Flash | Flash | Constants are read-only |
| `.data` | Flash (init values) | RAM (after copy) | Variables need write access |
| `.bss` | Nowhere (just zeroed) | RAM | No initial value to store — just zero it |
| Stack | — | RAM (top-down) | Grows downward from `_estack` |

The `.bss` optimization is elegant: since all uninitialized globals start at zero, there's no point storing thousands of zero bytes in flash. The linker just records the start and end addresses, and the startup code zeroes that range in RAM. This can save significant flash space — a `uint8_t buffer[4096];` takes 0 bytes in flash but 4096 in RAM.

**The tradeoff:** More `.data` = slower boot (more bytes to copy). More `.bss` = negligible boot cost (just zeroing). This is why embedded developers prefer uninitialized globals or explicit initialization in `main()` over initialized globals when boot time matters.

</details>

<details>
<summary><strong>Concrete Example</strong> — Tracing SPIneV1.elf from source to boot</summary>

Here's the exact journey for the Pupper's [[micro-context/spinev1-elf|SPIneV1.elf]] firmware:

### Step 1: Compilation

```c
// can.c — one of the source files
uint32_t can_error_count = 0;        // → goes in .bss (uninitialized, zero)
uint32_t can_baud_rate = 1000000;    // → goes in .data (initialized to 1M)
const char fw_version[] = "V1";      // → goes in .rodata (constant, flash)

void can_transmit(uint32_t id, uint8_t *data) {  // → goes in .text (code)
    // ...
}
```

The compiler produces `can.o` with four sections — but no fixed addresses yet.

### Step 2: Linking

The linker reads `STM32F446RETX_FLASH.ld` and stitches together `main.o`, `can.o`, `spi.o`, `startup_stm32f446retx.o`, and HAL library objects:

```
arm-none-eabi-ld -T STM32F446RETX_FLASH.ld \
  startup_stm32f446retx.o main.o can.o spi.o \
  stm32f4xx_hal_can.o stm32f4xx_hal_spi.o ... \
  -o SPIneV1.elf
```

The linker resolves all cross-references (e.g., `main.o` calls `can_transmit` defined in `can.o`) and assigns final addresses:

```
SYMBOL RESOLUTION EXAMPLE:
================================================================================

  main.o:         BL can_transmit    ← "call can_transmit, address TBD"
  can.o:          can_transmit:      ← "can_transmit starts here"

  After linking:
  main.o @ 0x0800_1234:  BL 0x0800_2000   ← address filled in
  can.o  @ 0x0800_2000:  can_transmit:     ← placed at final address
```

### Step 3: ELF File Contents

The resulting [[micro-context/spinev1-elf|SPIneV1.elf]] contains:

| Section | Address (VMA) | Size | Contents |
|---------|--------------|------|----------|
| `.isr_vector` | `0x0800_0000` | ~400 bytes | Vector table (98 entries: initial SP + 15 system exceptions + 82 IRQs) |
| `.text` | `0x0800_018C` | ~50 KB | All compiled code |
| `.rodata` | (after .text) | ~2 KB | String constants, lookup tables |
| `.data` | `0x2000_0000` (VMA) / flash (LMA) | ~500 bytes | Initialized globals |
| `.bss` | (after .data in RAM) | ~2 KB | Uninitialized globals |
| `.debug_*` | (not loaded) | ~200 KB | DWARF symbols for debugging |

### Step 4: Flashing

OpenOCD reads the ELF, extracts the loadable sections, and writes them to flash via the [[micro-context/st-link-v2-programmer|ST-Link]] over [[micro-context/swd-serial-wire-debug|SWD]]:

```bash
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg \
  -c "program SPIneV1.elf verify reset exit"
```

It only writes `.isr_vector`, `.text`, `.rodata`, and `.data` init values to flash. The `.debug_*` sections stay on your PC for the debugger. The `.bss` section isn't written anywhere — it will be zeroed in RAM at boot.

### Step 5: Boot

Power on → hardware reads vector table from `0x08000000`:
- Word 0 → MSP = `0x20020000` (top of 128KB RAM)
- Word 1 → PC = address of `Reset_Handler`

`Reset_Handler` in `startup_stm32f446retx.s` copies `.data`, zeros `.bss`, calls `SystemInit()` (configures the PLL: $f_{CPU} = 8\text{MHz} \times \frac{180}{8} = 180\text{MHz}$), calls `__libc_init_array()`, and jumps to `main()`.

Your motor control loop starts running. The entire sequence from power-on to `main()` takes roughly 5-10 milliseconds (hardware reset temporization + oscillator startup + software init).

**The one thing most outsiders get wrong about this is...** thinking the ELF file is what runs on the chip. The chip never sees the ELF — the flash programmer extracts the raw binary sections and writes them to specific addresses. The ELF is a *container* with metadata that tells the programmer where each byte belongs. What actually sits in flash is a flat stream of bytes starting with the vector table, followed by code and data — no headers, no file format, just raw instructions the CPU fetches and executes.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/code-to-gates-and-bootstrapping]]** — The upstream story: how source code compiles to machine instructions, and how the CPU's fetch-execute cycle processes them. This document picks up where that one leaves off.

- **[[micro-context/spinev1-elf]]** — The specific ELF firmware for the Pupper's motor control MCU. A concrete instance of everything described here.

- **[[quick-context/firmware|flashing firmware]]** — The physical act of writing firmware to flash via SWD. Focuses on the debug probe side of the process.

- **[[micro-context/swd-serial-wire-debug]]** — The 2-wire debug protocol used to flash firmware and set breakpoints. Explains what happens on the wire when OpenOCD programs the chip.

- **[[micro-context/stm32-microcontroller]]** — The STM32F446 MCU that this whole pipeline targets. Includes the block diagram showing flash, SRAM, and peripherals.

- **[[quick-context/pupper-bom-control-board]]** — The hardware BOM showing the dual STM32s (U1, U5) that each receive their own firmware through this pipeline.

- **Relocatable vs. Position-Independent Code** — Object files (`.o`) contain relocatable code with placeholder addresses. The linker resolves these. Position-independent code (PIC) can run at any address — useful for bootloaders but rarely needed on bare-metal MCUs with fixed memory maps.

- **Bootloaders** — A bootloader is a small program that lives at the start of flash and can reprogram the rest of flash (e.g., over UART or USB), without needing an external debug probe. The STM32 has a factory-programmed bootloader in system memory that can be activated by setting the BOOT0 pin high.

- **[[quick-context/physics-of-writing-data-to-memory]]** — The physics beneath this pipeline: how the flash programmer's bytes actually become trapped electrons on floating gates inside the MCU's flash cells, and why flash has erase-before-write constraints and limited P/E cycles.

- **[[quick-context/from-vacuum-tubes-to-coding-on-screens]]** — The big-picture story: how programming interfaces evolved from plugboards and punch cards to typing code on screens. Explains the historical context for *why* we have compilers, operating systems, and the whole toolchain that produces the ELF files described here.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does the linker script need to know the physical addresses of flash and RAM?
<details>
<summary>Answer</summary>
Because the CPU accesses memory by absolute address. When your code does `can_error_count++`, the machine instruction contains the literal RAM address (e.g., `0x20000004`) where that variable lives. The linker must assign these addresses at link time so every instruction points to the correct physical location. Unlike a desktop OS (which has virtual memory and address space randomization), a bare-metal MCU has no memory management unit to remap addresses — what the linker assigns is what the hardware sees. See: How It Works (The Linker Script)
</details>

**Q2:** What would happen if you skipped the `.data` copy in the startup code?
<details>
<summary>Answer</summary>
All initialized global variables would have garbage values instead of their intended initial values. For example, `uint32_t can_baud_rate = 1000000;` would contain whatever random value was in RAM after power-on instead of 1,000,000. The initial values exist only in flash (at the LMA), and without the copy, the RAM locations (at the VMA) where the code reads them would be uninitialized. This would cause subtle, hard-to-debug failures — the code compiles and links fine, and might even work sometimes if RAM happens to contain useful values from a previous run. See: The Key Tension
</details>

**Q3:** The `.bss` section takes 0 bytes in flash but can use kilobytes of RAM. Why is this an important optimization?
<details>
<summary>Answer</summary>
Flash space is limited (512KB on the STM32F446) and shared between code, constants, and `.data` initial values. A large uninitialized buffer like `uint8_t dma_buffer[4096]` would waste 4KB of flash storing nothing but zeros if `.bss` weren't handled separately. By only recording the start and end addresses, the linker keeps flash usage proportional to *meaningful* data. The startup code then zeros the region in RAM with a fast loop — much more efficient than storing and copying thousands of zero bytes. This is why embedded developers prefer `static uint8_t buf[1024];` (goes in `.bss`, 0 flash bytes) over `static uint8_t buf[1024] = {0};` (compilers may place this in `.data`, costing 1024 flash bytes, though most modern compilers are smart enough to put it in `.bss` anyway). See: The Key Tension
</details>

**Q4:** If the vector table must be at address `0x00000000` but STM32 flash starts at `0x08000000`, how does the CPU find it?
<details>
<summary>Answer</summary>
STM32 uses **memory aliasing**: the flash region at `0x08000000` is also mapped (mirrored) to address `0x00000000` by default. So the CPU reading address `0x00000000` physically accesses `0x08000000`. This aliasing is controlled by the BOOT pins — with BOOT0=0 (default), flash is aliased to 0x0. With BOOT0=1, system memory (containing ST's factory bootloader) is aliased instead, enabling firmware updates over UART/USB without a debug probe. The linker script places the vector table at `0x08000000` (the real flash address), and the aliasing handles the rest. See: How It Works (The Boot Sequence)
</details>

**Q5:** The ELF file for SPIneV1 is ~250KB, but the actual flash usage is ~55KB. Where does the other ~195KB go?
<details>
<summary>Answer</summary>
The extra ~195KB is almost entirely **DWARF debug information** (`.debug_info`, `.debug_line`, `.debug_abbrev`, `.debug_str`, etc.) — the symbol tables, source line mappings, and type information that let you do step-through debugging in STM32CubeIDE or GDB. These sections have no LMA (Load Memory Address) — the flash programmer skips them entirely. They exist only in the ELF file on your PC, where the debugger reads them to map between machine addresses and your source code. A stripped `.bin` file (produced by `arm-none-eabi-objcopy -O binary SPIneV1.elf SPIneV1.bin`) would be ~55KB — just the raw bytes that actually go into flash. See: Concrete Example (Step 3: ELF File Contents)
</details>

</details>
