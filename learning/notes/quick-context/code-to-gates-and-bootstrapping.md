---
topic: Code to Gates - The Full Compilation Chain and Bootstrapping
created: 2026-02-14
updated: 2026-04-07
---

> **Related:** [[quick-context/transistor]] | [[quick-context/transistor-analog-to-digital]] | [[quick-context/pcb-chip-transistor-hierarchy]] | [[quick-context/semiconductor-fabrication]] | [[quick-context/from-code-to-running-firmware]]

> **TL;DR:** Every line of code you write gets transformed through a chain of abstractions—compiler, virtual machine, assembler, machine code—until it becomes binary instructions that a CPU executes by fetching, decoding, and routing signals through logic gates built from [[quick-context/transistor|transistors]]. Machine code is produced by the assembler, which encodes each mnemonic into a fixed-width binary word whose bit fields are defined by the CPU's Instruction Set Architecture (ISA). Those encoded bytes get written into an object file on disk, combined by a [[quick-context/from-code-to-running-firmware|linker]], and ultimately placed at their final destination: loaded into RAM by an OS loader (desktop), flashed to non-volatile memory via a [[micro-context/swd-serial-wire-debug|debug probe]] (embedded), or historically punched onto cards or paper tape. The chicken-and-egg problem of "how do you compile the first compiler?" was solved by bootstrapping: humans hand-encoded binary instructions via punch cards to build the first assembler, then used that assembler to build better tools, all the way up to modern compilers.

# Code to Gates — The Full Compilation Chain and Bootstrapping

## Human notes

How does machine code actually get written — what is the encoding process that turns assembly into binary? And where does the resulting machine code physically end up?

## The Core Problem

You type `x = 2 + 3` in Python. Somehow, billions of [[quick-context/transistor|transistors]] on a [[quick-context/silicon-die|silicon die]] physically switch on and off to make that happen. How? There are roughly **7 layers of abstraction** between your code and the hardware, each translating the layer above into simpler instructions for the layer below. And there's a deeper puzzle: the very first layer (the compiler) is itself a program—so what compiled *it*? The answer is bootstrapping, a process that started with humans manually encoding binary on punch cards.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Compiler** | A program that translates high-level source code (C, Rust) into lower-level code (assembly or machine code). Ahead-of-time compilers do this before execution; JIT compilers do it during. |
| **Assembler** | Translates human-readable assembly mnemonics (`ADD R1, R2`) into binary machine code (`0110001100`). It's a 1-to-1 mapping—each assembly instruction becomes exactly one machine instruction. |
| **Machine Code (Instructions)** | The binary patterns a CPU can directly execute. Each instruction is a fixed-width binary word (16-bit on Hack, 32-bit on ARM) whose bit fields encode the opcode, registers, and operands according to the ISA. |
| **ISA (Instruction Set Architecture)** | The contract between software and hardware. It defines every instruction the CPU supports, its binary encoding (which bits mean what), the available registers, and addressing modes. ARM, x86, RISC-V, and Hack are all different ISAs. |
| **Logic Gate** | A circuit built from [[quick-context/transistor|transistors]] that implements a boolean function (AND, OR, NOT, NAND). All computation ultimately happens here—NAND gates alone can implement any boolean function. |
| **Bootstrapping** | The process of building complex tools from simpler ones, starting from nothing. In computing: hand-coded binary → first assembler → first compiler → better compiler → modern toolchains. |

<details>
<summary><strong>How It Works</strong></summary>

The Full Stack: Code to Gates

The entire chain from high-level code to physical hardware looks like this:

```
THE COMPILATION CHAIN (7 LAYERS OF ABSTRACTION)
================================================================================

LAYER 7: HIGH-LEVEL LANGUAGE          "x = 2 + 3"
         (Python, C, Java, Rust)       Human-readable, abstracts away everything
              │
              │  COMPILER or INTERPRETER
              │  (Tokenizer → Parser → AST → Code Generator)
              ▼
LAYER 6: VIRTUAL MACHINE / IR         "push 2; push 3; add"
         (Python bytecode, LLVM IR,    Stack-based or register-based intermediate
          Java bytecode, .NET CIL)     form. Portable across CPU architectures.
              │
              │  VM EXECUTOR or BACKEND COMPILER
              │  (Translates VM ops to target architecture)
              ▼
LAYER 5: ASSEMBLY LANGUAGE            "@ 2        // load 2 into A register"
         (x86 ASM, ARM ASM,           "D=A        // D = 2"
          RISC-V ASM, Hack ASM)       "@ 3        // load 3"
              │                        "D=D+A      // D = 2 + 3"
              │  ASSEMBLER
              │  (1-to-1 symbol → binary translation)
              ▼
LAYER 4: MACHINE CODE                  0000000000000010    (load 2)
         (Binary instructions)         1110110000010000    (D = A)
              │                        0000000000000011    (load 3)
              │                        1110000010010000    (D = D + A)
              │  CPU FETCH-DECODE-EXECUTE CYCLE
              ▼
LAYER 3: CPU MICROARCHITECTURE         Program Counter → fetch instruction from RAM
         (Fetch-Execute Cycle,         → decode opcode → route to ALU
          Control Unit, Registers)     → write result to register → increment PC
              │
              │  CONTROL SIGNALS route data through...
              ▼
LAYER 2: LOGIC GATES                   ALU is built from: Adders ← Full Adders
         (AND, OR, NOT, NAND,          ← Half Adders ← XOR + AND gates
          XOR, MUX, DMUX)             Registers ← MUX + [[quick-context/d-flip-flop|Data Flip-Flop]]
              │                        RAM ← DMUX + Registers + MUX
              │  GATES ARE BUILT FROM...
              ▼
LAYER 1: TRANSISTORS                   NAND gate = 4 transistors (2 NMOS
         (MOSFET switches on           series + 2 PMOS parallel). Voltage
          doped silicon)               on gate → conducts (ON) or blocks (OFF)
```

The Fetch-Execute Cycle (Layer 3 in detail)

This is the heartbeat of every computer. The CPU repeats this cycle billions of times per second:

```
THE FETCH-EXECUTE CYCLE
================================================================================

    ┌──────────────────────────────────────────────────────────┐
    │                         CPU                              │
    │                                                          │
    │   ┌─────────────┐    ┌──────────────┐    ┌──────────┐   │
    │   │   Program    │    │  Instruction  │    │          │   │
    │   │   Counter    │───→│   Register    │───→│   ALU    │   │
    │   │   (PC)       │    │   (decode)    │    │          │   │
    │   └──────┬──────┘    └──────────────┘    └────┬─────┘   │
    │          │                                     │         │
    │          │ address                      result │         │
    │          ▼                                     ▼         │
    │   ┌─────────────────────────────────────────────────┐   │
    │   │              REGISTERS (D, A, etc.)              │   │
    │   └─────────────────────────────────────────────────┘   │
    └──────────────────────────┬───────────────────────────────┘
                               │ read/write
                               ▼
                    ┌─────────────────────┐
                    │     RAM (Memory)     │
                    │  ┌───┬───┬───┬───┐  │
                    │  │ 0 │ 1 │ 2 │...│  │  ← Instructions AND data live here
                    │  └───┴───┴───┴───┘  │
                    └─────────────────────┘

  CYCLE:
  ══════
  1. FETCH:   PC points to address in RAM → get the instruction
  2. DECODE:  Instruction Register reads the opcode and operands
  3. EXECUTE: ALU performs the operation (add, subtract, compare...)
  4. STORE:   Result written to register or RAM
  5. UPDATE:  PC increments (or jumps if branch instruction)
  6. REPEAT:  Go to step 1
```

How Logic Gates Build an ALU (Layer 2 → Layer 3)

Everything the CPU computes passes through the ALU, which is built entirely from simple gates:

```
FROM NAND GATES TO AN ALU
================================================================================

NAND is the universal gate — every other gate can be built from it:

  NOT(x)    = x NAND x
  AND(x,y)  = NOT(x NAND y)
  OR(x,y)   = NOT(NOT(x) AND NOT(y))
  XOR(x,y)  = (x OR y) AND (NOT(x) OR NOT(y))

These combine into arithmetic circuits:

  HALF ADDER (adds 2 bits):
  ┌─────────────┐
  │  a ──┬──[XOR]──→ sum        XOR gives the sum bit
  │      │           │           AND gives the carry bit
  │  b ──┼──[AND]──→ carry
  └─────────────┘

  FULL ADDER (adds 3 bits — two inputs + carry-in):
  ┌──────────────────────────────────┐
  │  a ───┐                          │
  │       ├─[HALF ADDER]─→ sum1 ─┐  │
  │  b ───┘              → carry1─┤  │
  │                               │  │
  │  carry_in ────────────────────┤  │
  │       ├─[HALF ADDER]─→ sum ──┼──┼──→ sum (output)
  │       └──────────────→ carry2─┤  │
  │                               │  │
  │              [carry1 OR carry2]───┼──→ carry (output)
  └──────────────────────────────────┘

  16-BIT ADDER = 16 full adders chained (carry out → carry in):
  ┌────┐  ┌────┐  ┌────┐       ┌────┐
  │ FA │←─│ FA │←─│ FA │← ... ←│ FA │←─ 0
  │bit15│  │bit14│  │bit13│       │bit0 │
  └────┘  └────┘  └────┘       └────┘

  ALU = adder + control logic that selects which operation to perform
        (add, subtract via two's complement, AND, OR, NOT, etc.)
        Control bits from the instruction's opcode configure which
        gates are active for each operation.
```

How Machine Code Gets Written: The Encoding Process

The assembler's job is to turn human-readable mnemonics into the exact binary patterns the CPU expects. But these patterns aren't arbitrary — they're defined by the CPU's **Instruction Set Architecture (ISA)**, which specifies the bit-field layout of every instruction.

Each machine instruction is a fixed-width binary word (16-bit on Hack, 32-bit on ARM/RISC-V, variable on x86) divided into **fields**:

```
HOW THE ASSEMBLER ENCODES AN INSTRUCTION
================================================================================

Example: ARM Thumb "ADDS R1, R2, R3" (add R2 + R3, store in R1)

The ISA manual says Thumb ADD (register) format is:

  15  14  13  12  11  10   9   8   7   6   5   4   3   2   1   0
 ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 │ 0 │ 0 │ 0 │ 1 │ 1 │ 0 │ 0 │  Rm   │   Rn  │   Rd  │
 └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  └─── opcode (7 bits) ───┘   │Rm=R3│ Rn=R2 │ Rd=R1 │
  "this is an ADD register"    = 011   = 010   = 001

  Assembler output: 0001100 011 010 001 → 0x18D1 (two bytes in flash)

Example: Hack CPU "D=D+A" (add D and A registers, store in D)

The Hack ISA says C-instruction format is:

  15  14  13  12  11  10   9   8   7   6   5   4   3   2   1   0
 ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
 │ 1 │ 1 │ 1 │ a │ c1│ c2│ c3│ c4│ c5│ c6│ d1│ d2│ d3│ j1│ j2│ j3│
 └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  "C-type"   │  a=0    comp=000010    │ d=010 │  j=000  │
              │  (use A, not M)  (D+A) │ (dest │ (no     │
              │                        │  = D) │  jump)  │

  Assembler output: 1110000010010000 → stored as 16 bits in ROM
```

The assembler is essentially a **lookup table + symbol resolver**:

1. **Parse** the mnemonic: split `ADDS R1, R2, R3` into opcode (`ADDS`), destination (`R1`), operands (`R2`, `R3`)
2. **Look up** the opcode in the ISA encoding table → get the bit pattern for the opcode field
3. **Encode** register names as numbers: `R1`=001, `R2`=010, `R3`=011
4. **Pack** the fields into a binary word according to the ISA format
5. **Resolve labels**: if the instruction references a label like `loop:`, substitute the address where that label was defined

For a compiler (not assembler), the process is more complex — one high-level statement may generate many machine instructions, requiring register allocation, instruction selection, and optimization. But every instruction still ends up encoded through the same ISA bit-field rules.

Where Machine Code Ends Up: From Object File to Final Destination

The assembler doesn't write directly to the CPU. The encoded bytes go through several stages before reaching their final home:

```
WHERE MACHINE CODE GETS WRITTEN
================================================================================

STAGE 1: OBJECT FILE (on disk)
─────────────────────────────────────────────────────────
  The assembler (or compiler backend) writes encoded instructions
  into an object file (.o on Unix, .obj on Windows).

  The .o file contains:
  • .text section  — the machine code bytes
  • .data section  — initialized global variables
  • .bss section   — space reserved for uninitialized globals
  • Symbol table   — "function can_transmit starts at offset 0x40"
  • Relocation entries — "at offset 0x0C, insert the address of
                          can_transmit when you know it"

  Addresses are NOT final yet — the object file uses relative
  offsets. The linker assigns real addresses later.


STAGE 2: LINKED EXECUTABLE (on disk)
─────────────────────────────────────────────────────────
  The linker combines multiple .o files into one executable:
  • Resolves cross-references (main.o calling can.o's function)
  • Assigns final memory addresses using a linker script
  • Produces an ELF (Linux), PE (Windows), or Mach-O (macOS) file

  The executable is still on disk. The machine code isn't
  "running" yet — it's just a file with a specific layout.


STAGE 3: FINAL DESTINATION (depends on the target)
─────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────┐
  │  DESKTOP / SERVER (Linux, Windows, macOS)                   │
  │                                                             │
  │  OS Loader reads the executable from disk:                  │
  │  1. Allocates virtual memory pages                          │
  │  2. Copies .text (code) into executable memory pages        │
  │  3. Copies .data into writable memory pages                 │
  │  4. Zeros .bss pages                                        │
  │  5. Resolves dynamic library references (shared .so/.dll)   │
  │  6. Sets Program Counter to the entry point                 │
  │                                                             │
  │  Machine code lives in RAM. Lost on power-off.              │
  │  Reloaded from disk every time you run the program.         │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  EMBEDDED (MCU like STM32, ESP32)                           │
  │                                                             │
  │  Flash programmer (OpenOCD / ST-Link) reads the ELF:        │
  │  1. Extracts loadable sections (.text, .data init values)   │
  │  2. Erases flash memory on the chip                         │
  │  3. Writes bytes to flash via SWD/JTAG debug probe          │
  │  4. Machine code persists without power (flash is NV)       │
  │                                                             │
  │  CPU executes code directly from flash (XIP).               │
  │  Startup code copies .data to RAM, zeros .bss.              │
  │  See: [[quick-context/from-code-to-running-firmware]]       │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │  HISTORICAL (1950s–1970s)                                   │
  │                                                             │
  │  Assembler output written to:                               │
  │  • Punch cards — one instruction per card, holes = bits     │
  │  • Paper tape — continuous roll, holes punched in columns   │
  │  • Magnetic tape — sequential binary on reels               │
  │                                                             │
  │  Card reader or tape reader feeds instructions into memory. │
  │  Machine code lives in core memory (magnetic rings that     │
  │  retain state without power — the original "non-volatile"). │
  └─────────────────────────────────────────────────────────────┘
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

Abstraction vs. Performance

The compilation chain is a tower of abstractions, and the core tension is: **each layer of abstraction trades performance for productivity**.

| Approach | Productivity | Performance | Control |
|----------|-------------|-------------|---------|
| Python (interpreted, Layer 7) | Highest — write fast, debug fast | Slowest — multiple translation layers at runtime | Least — can't control memory layout |
| C (compiled, Layer 5→4) | Medium — manual memory, but fast compilation | Fast — compiles directly to machine code | High — control memory, pointers |
| Assembly (Layer 5) | Low — tedious, architecture-specific | Very fast — 1:1 with machine instructions | Very high — register-level control |
| Hand-coded binary (Layer 4) | Terrible — error-prone, unreadable | Identical to assembly (same output) | Total — but impractical |
| Custom hardware / FPGA (Layer 2) | Lowest — design gates directly in HDL | Fastest — no instruction overhead | Absolute — but weeks of development |

The key insight: **you almost never need to go below your language's abstraction level**. Python's overhead is irrelevant for most applications. When it matters (game engines, OS kernels, real-time systems), you drop to C or Rust. You only write assembly for device drivers, bootloaders, or extreme optimization. And you only touch gates when designing actual hardware.

The other tension is **hardware vs. software implementation**. Any function can be implemented in either:
- **Hardware** (dedicated circuit): faster but fixed, costs die area
- **Software** (sequence of simpler instructions): slower but flexible

For example, a CPU could implement multiplication as a dedicated circuit (fast, expensive) or as repeated addition in software (slow, free). Modern CPUs make different tradeoffs — ARM's RISC philosophy uses simpler hardware with more software, while x86's CISC approach puts more into hardware.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Bootstrapping: From Punch Cards to Modern Compilers

The chicken-and-egg problem: a compiler is a program, so what compiled the first compiler? The answer is **bootstrapping** — building up from nothing, layer by layer.

```
THE BOOTSTRAPPING CHAIN
================================================================================

STEP 0: HARDWARE ONLY (no software exists yet)
────────────────────────────────────────────────────────────────────────────────
  The CPU exists. It can execute binary instructions. But there is NO software.
  No assembler, no compiler, no operating system. Just naked hardware with a
  Reset Vector pointing to some memory address.

  How do you get the first program into memory?


STEP 1: PUNCH CARDS / TOGGLE SWITCHES → FIRST ASSEMBLER
────────────────────────────────────────────────────────────────────────────────
  Humans hand-encode binary instructions onto physical media:

  ┌─────────────────────────────────────────────────────┐
  │  PUNCH CARD                                         │
  │  ○ ● ○ ○ ○ ● ● ○  ← each hole = 1, no hole = 0   │
  │  ○ ○ ● ○ ● ○ ○ ●     represents one instruction    │
  │  ● ○ ○ ● ○ ○ ● ○                                   │
  │  ...hundreds of cards for a simple program...       │
  └─────────────────────────────────────────────────────┘

  These binary instructions define a VERY simple program:
  "Read text input (assembly mnemonics), convert each mnemonic
   to its binary equivalent, output the binary to memory."

  This is the FIRST ASSEMBLER — written entirely in binary by hand.


STEP 2: FIRST ASSEMBLER → BETTER ASSEMBLER
────────────────────────────────────────────────────────────────────────────────
  Now we can write assembly code in human-readable text:

     @2          instead of     0000000000000010
     D=A                        1110110000010000
     @3                         0000000000000011
     D=D+A                      1110000010010000

  Feed this through the assembler from Step 1 → get binary output.
  We use this to write a BETTER assembler (with labels, variables,
  macros) — in assembly language this time, not raw binary.


STEP 3: BETTER ASSEMBLER → FIRST COMPILER
────────────────────────────────────────────────────────────────────────────────
  Using the improved assembler, we write a simple compiler in assembly.
  This compiler can translate a subset of a high-level language (like
  early C) into assembly code.

     int x = 2 + 3;    ──→    assembler   ──→    0000000000000010
                         ↓     from step 2        1110110000010000
                     compiler               ...
                     from step 3


STEP 4: FIRST COMPILER → SELF-HOSTING COMPILER
────────────────────────────────────────────────────────────────────────────────
  The breakthrough: rewrite the compiler IN ITS OWN LANGUAGE.

  The C compiler (written in assembly) can compile C code.
  So... rewrite the C compiler in C. Compile it with the old
  assembly-based compiler. Now you have a C compiler written in C,
  compiled by itself. This is "self-hosting."

  From here: every future version of the compiler is written in C
  and compiled by the previous version.


STEP 5: MODERN TOOLCHAINS
────────────────────────────────────────────────────────────────────────────────
  Self-hosting compilers evolve:
  GCC (C/C++ compiler, now written in C++), LLVM/Clang, rustc (Rust compiler
  bootstraps from a previous rustc version), Go compiler (now in Go,
  originally bootstrapped from C).

  The chain from punch cards is unbroken — every modern compiler
  descends from hand-encoded binary.
```

How the CPU Knows Where to Start: The Reset Vector

Once you have instructions in memory, how does the CPU know where to begin?

```
POWER-ON SEQUENCE
================================================================================

  1. Power applied to CPU
  2. CPU resets all registers to known state
  3. Program Counter (PC) is set to the RESET VECTOR address
     (hardwired into the CPU — e.g., address 0x0000 or 0xFFFF0000)
  4. CPU fetches instruction at that address
  5. Fetch-Execute cycle begins

  ┌──────────────────────────────────────────────────────────────┐
  │  MEMORY MAP                                                  │
  │                                                              │
  │  0x0000  ┌─────────────────────┐  ← Reset Vector points     │
  │          │ First instruction   │     here (ROM/firmware)     │
  │  0x0001  │ Second instruction  │                             │
  │          │ ...                 │  These instructions         │
  │          │ Initialize hardware │  initialize the system      │
  │          │ Load bootloader     │  and load the OS            │
  │          │ Jump to OS entry    │                             │
  │          └─────────────────────┘                             │
  │              ...                                             │
  │  0xFFFF  └─────────────────────┘                             │
  └──────────────────────────────────────────────────────────────┘

  In modern systems:
  Reset Vector → ROM/Firmware (BIOS/UEFI) → Bootloader → OS Kernel

  The firmware at the Reset Vector address is burned into ROM at the
  factory — it's the modern equivalent of the punch cards. It's the
  one piece of software that doesn't need to be "loaded" because
  it's physically part of the hardware.
```

**The one thing most outsiders get wrong about this is...** thinking that "code runs on hardware" means the CPU somehow understands your programming language. The CPU understands *nothing* — it's a machine that reads binary patterns and routes electrical signals through gates. Every abstraction layer (compiler, VM, assembler) exists purely to translate human intent into the specific binary patterns that configure those gates. Python doesn't "run" — it gets translated through 4+ layers until it's just voltages switching [[quick-context/transistor|transistors]] on and off.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/transistor]]** — The physical switch that implements logic gates. Understanding how a [[quick-context/transistor|transistor]] works (voltage on gate controls current flow) is the foundation for understanding how gates compute.

- **[[quick-context/transistor-analog-to-digital]]** — How imperfect analog transistors are engineered to behave as perfect digital switches, using noise margins and CMOS logic. Explains why the gate abstraction works at all.

- **[[quick-context/pcb-chip-transistor-hierarchy]]** — The physical packaging hierarchy from 5nm transistors to millimeter-scale connectors. Where the logic gates physically live on the die.

- **[[quick-context/semiconductor-fabrication]]** — How billions of transistors (and therefore gates) are manufactured on silicon wafers through photolithography.

- **[[quick-context/silicon-die]]** — The actual piece of silicon containing the transistors, ALU, registers, and cache that execute your compiled instructions.

- **Two's Complement** — How negative numbers are represented in binary, enabling the ALU to perform subtraction using only addition circuits. Elegant hack: flip all bits and add 1.

- **Von Neumann Architecture** — The architectural pattern where instructions and data share the same memory, which is why the fetch-execute cycle needs to distinguish between them.

- **HDL (Hardware Description Language)** — Languages like VHDL and Verilog used to design and verify logic gate implementations before manufacturing. The "source code" for hardware.

- **[[quick-context/from-code-to-running-firmware]]** — The downstream story: once machine code exists, how the linker places it at physical memory addresses, the flash programmer writes it to the chip, and the startup code boots to `main()`. Picks up where this document leaves off.

- **[[quick-context/physics-of-writing-data-to-memory]]** — The physical story: how bits actually get written into SRAM, DRAM, and flash at the transistor/charge level. Explains the hardware physics behind "writing to memory" that this document's compilation chain produces.

- **[[quick-context/from-vacuum-tubes-to-coding-on-screens]]** — The upstream story: how programming interfaces evolved from plugboards and punch cards to interactive terminals and modern screens. Explains *how* humans went from hand-coding binary on punch cards (Step 1 of bootstrapping) to typing code in an editor.

- **[[quick-context/switches-to-registers-storing-data]]** — A hands-on breadboard circuit (switches + clock + 74HC574 register chip) that makes Layer 2's "Registers = MUX + Data Flip-Flop" tangible. Demonstrates how the register pattern scales from 8 LEDs to a CPU's register file to RAM.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What does the assembler actually do when it encodes `ADD R1, R2`?
<details>
<summary>Answer</summary>
The assembler looks up the ISA encoding for `ADD` to get the opcode bit pattern, converts register names to their numeric encodings (`R1`=001, `R2`=010), and packs these fields into a fixed-width binary word according to the ISA's instruction format. The result is a sequence of bytes (e.g., 2 bytes for Thumb, 4 bytes for ARM) that gets written into the `.text` section of an object file. It's essentially a lookup table + field packer — no optimization, no interpretation, just 1-to-1 encoding. See: How It Works (How Machine Code Gets Written)
</details>

**Q2:** Where does machine code physically end up on a desktop vs. an embedded MCU?
<details>
<summary>Answer</summary>
On a **desktop**, the OS loader reads the executable from disk, allocates virtual memory pages, and copies the `.text` section into RAM — machine code lives in RAM and is reloaded from disk every time you run the program. On an **embedded MCU**, a flash programmer writes the machine code directly into non-volatile flash memory via a debug probe ([[micro-context/swd-serial-wire-debug|SWD]]/JTAG). The code persists without power and the CPU executes it directly from flash (execute-in-place). See: How It Works (Where Machine Code Ends Up)
</details>

**Q3:** If a CPU only understands binary, how can Python — an interpreted language — run on it?
<details>
<summary>Answer</summary>
**Python never runs directly on the CPU.** The Python interpreter (e.g., CPython) is a C program that was compiled to machine code. When you run Python, the CPU is actually executing the *interpreter's* machine code, which reads your Python source, converts it to bytecode, and then the interpreter's compiled C code handles each bytecode operation by executing the corresponding machine instructions. Your Python code is *data* being processed by the interpreter program, not instructions being executed by the CPU. See: How It Works (THE COMPILATION CHAIN, Layers 7→4)
</details>

**Q4:** Why can't the assembler write machine code directly into the CPU's memory? Why does it go through object files and a linker first?
<details>
<summary>Answer</summary>
Because a real program is split across multiple source files, and the assembler processes them independently. When `main.o` calls a function in `can.o`, the assembler doesn't know that function's final address yet — it leaves a placeholder and a **relocation entry** saying "fill in the address of `can_transmit` here." Only the **linker** can resolve these cross-references, because it sees all object files at once and assigns final memory addresses using the linker script. On embedded targets, the linker also needs to know the physical memory map (flash at `0x08000000`, RAM at `0x20000000`) to place code correctly. See: How It Works (Where Machine Code Ends Up) and [[quick-context/from-code-to-running-firmware|From Code to Running Firmware]]
</details>

**Q5:** The bootstrapping chain starts with humans hand-encoding binary on punch cards. But even that requires knowing the ISA — how did the first CPU designers know what bit patterns to encode, and what would happen if the ISA changed between CPU revisions?
<details>
<summary>Answer</summary>
The ISA is defined *by* the hardware designers — they choose the bit-field layout when they design the CPU's control unit (the decoder circuit). The truth table of the decoder *is* the ISA: input bit pattern X produces control signals Y. So the first programmers didn't "discover" the encoding — they read the hardware specification written by the people who wired the logic gates. If the ISA changes between revisions (new instructions, different encodings), all existing machine code breaks — it would decode to wrong operations or illegal instructions. This is why ISA backward compatibility is sacred: x86 CPUs in 2026 can still run 8086 binary from 1978. ARM maintains compatibility within architecture versions. Breaking the ISA means every assembler, compiler, and existing binary must be rebuilt — essentially restarting the bootstrapping chain. See: Concrete Example (THE BOOTSTRAPPING CHAIN) and 5 Essential Terms (ISA)
</details>

</details>
