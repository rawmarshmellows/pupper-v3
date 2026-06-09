---
topic: How a Computer Works — Index-Spine (Electricity → Code Executing)
created: 2026-06-07
updated: 2026-06-09
---

> **Related:** [[learning/notes/quick-context/switches-to-registers-storing-data]] | [[learning/notes/quick-context/cpu-fetch-execute-cycle]] | [[learning/notes/quick-context/python-to-machine-code-pipeline]] | [[learning/notes/quick-context/code-to-gates-and-bootstrapping]] | [[learning/notes/quick-context/keypress-to-pixel-pipeline]] | [[learning/notes/quick-context/semiconductor-fabrication]]

> **TL;DR:** One map of the whole machine, built as **two towers that meet at machine code**, standing on a **fabrication basement**. The **hardware tower** climbs *up* from raw electricity → transistors → gates → flip-flops → registers → RAM → a **CPU that executes machine code**. The **software tower** descends *down* from your **Python source** → bytecode/VM → assembly → the *same* machine code — which is exactly what the CPU eats. Beneath both, the **fabrication basement** shows how the physical parts (transistors, diodes, resistors, capacitors, ICs) are actually manufactured. The one thread tying it all together: *a controlled voltage (a 0 or 1) flows through logic, gets captured into a register at a clock edge, and the captured bits steer the next round of logic.* Code is just a long list of those bit-patterns. Follow the rungs and you can explain a keypress becoming a letter on screen, end to end.

# How a Computer Works — Index-Spine

## The Core Problem: The Abstraction Gap Is Too Wide to Cross in One Jump

"How does a computer work?" spans ~15 layers: from electrons in copper, to a transistor switch, to logic gates, to one-bit memory, to registers, RAM, a CPU executing instructions — and *separately*, from the Python you type, down through a compiler and a virtual machine to the machine code that CPU runs. And beneath all of it: every physical part had to be manufactured atom by atom. Nobody holds all that at once, so explanations either stay shallow ("it's just 1s and 0s") or strand you in one layer with no map. This spine fixes that with a single picture: **two towers meeting at machine code, on a fabrication basement.** Read the hardware tower upward, the software tower downward, watch them meet, then look beneath the parts. Each rung links a deep note for the full story and, where it exists, the **real Nand2Tetris Python chip that implements it** — so you see every idea twice: as intuition and as runnable code.

> **Code path shorthand:** `<course>` = `learning/references/courses/python-nand-to-tetris-part-1/src/hardware`
> (Nand2Tetris **Part 1 = hardware**, present in this repo. The compiler/VM/assembler are Part 2 — referenced conceptually in the software tower.)

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Bit (signal)** | A wire's voltage read as one of two states: HIGH (≈Vcc) = 1, LOW (≈GND) = 0. Everything is built by combining and capturing bits. |
| **Logic gate** | A circuit (made of transistor switches) that computes a boolean function (AND/OR/NOT) *in the present instant only*. All arithmetic and decoding is gates. |
| **Register** | A row of D flip-flops that capture their inputs on the same clock edge and hold them. The unit of memory in a CPU; an array of them is RAM. |
| **Machine code / instruction** | A number in memory whose bits are wired to control lines — they pick the ALU op, which register loads, where to read/write. The CPU executes these directly. "Code" ultimately becomes a list of them. |
| **Virtual machine / bytecode** | An *intermediate* instruction set (e.g. Python bytecode) run by an interpreter program — not the CPU's own machine code, but itself executed by machine code underneath. |

<details>
<summary><strong>PART A — The Hardware Tower (electricity ↑ up to a CPU that runs machine code)</strong></summary>

Each rung: **intuition** → **anchors** (deep note · implementing code) → **bridge** (why the next rung must exist). Read upward.

### A0 — Electricity: what is a signal?
**Intuition.** Voltage is a pressure difference that pushes charge (current) through a wire; power is the rate energy is delivered. "A signal" is just a voltage on a wire we agree to read as 1 or 0.
**Anchors.** [[learning/notes/quick-context/voltage|Voltage]] · [[learning/notes/quick-context/electric-current|Electric Current]] · [[learning/notes/quick-context/voltage-current-causality|Voltage→Current Causality]] · [[learning/notes/quick-context/power-watts-joules|Power, Watts, Joules]]
**Bridge.** A raw voltage is analog and messy — it sags, drifts, picks up noise. Before a wire can reliably mean "1" or "0" we need a stable supply and a way to force wires cleanly to Vcc or GND. → **A1**.

### A1 — Power supply & passives: a clean, stable 0/1
**Intuition.** A power supply gives steady Vcc and GND; resistors and capacitors shape and stabilize it; pull-up/pull-down resistors guarantee a floating wire reads as a definite 1 or 0.
**Anchors.** [[learning/notes/quick-context/resistor|Resistor]] · [[learning/notes/quick-context/capacitor|Capacitor]] · [[learning/notes/quick-context/parallel-vs-series-voltage|Series/Parallel Voltage]] · [[learning/notes/quick-context/ac-to-dc-rectification|AC→DC Rectification]] · [[learning/notes/quick-context/grounding-and-return-paths|Grounding & Return Paths]] · [[learning/notes/small-context/pull-up-pull-down-resistors|Pull-up/Pull-down Resistors]]
**Bridge.** Stable rails hold a clean 1 or 0, but a static voltage can't *decide* anything. To compute we need a part where one voltage switches another: the transistor. → **A2**.

### A2 — The switch → logic gates: computing in the instant
**Intuition.** A transistor is an electrically-controlled switch. Wire a few into a NAND gate; from NAND alone you can build every other gate (NOT/AND/OR/XOR) and the selectors (MUX/DMUX). This is where electricity starts *computing*.
**Anchors.** [[learning/notes/quick-context/transistor|Transistor]] · [[learning/notes/micro-context/mosfet|MOSFET]] · [[learning/notes/quick-context/diode|Diode]] · [[learning/notes/quick-context/doped-silicon|Doped Silicon]] · [[learning/notes/quick-context/transistor-analog-to-digital|Analog Transistors Acting Digital]] · Code: `<course>/elementary_logic_gates/nand_gate.py` → `not_gate.py`, `and_gate.py`, `or_gate.py`, `xor_gate.py`, `mux_gate.py`, `dmux_gate.py`
**Bridge.** Gates compute only *right now* — change inputs, outputs change, result vanishes. A computer must *remember*. To remember we need a heartbeat that says "capture this value and hold it." → **A3**, then **A4**.

### A3 — The clock (piezoelectric source): "capture NOW"
**Intuition.** A clock is a square wave; its rising edge is the universal "capture now" command. The most stable source is a piezoelectric quartz crystal (ceramic resonator = cheaper, RC = crudest). On a breadboard a push button is a one-shot clock.
**Anchors.** [[learning/notes/micro-context/clock-edges|Clock Edges]] · [[learning/notes/micro-context/clock-source|Clock Source]] · [[learning/notes/micro-context/crystal-oscillator|Quartz Crystal Oscillator]] · [[learning/notes/micro-context/ceramic-resonator|Ceramic Resonator]] · [[learning/notes/quick-context/rc-oscillator|RC Oscillator]] · [[learning/notes/quick-context/clock-sources-and-timing|Clock Sources & Timing]]
**Bridge.** Gates (compute) + clock (timing) lets us finally build a circuit that captures one bit and holds it until the next tick — memory. → **A4**.

### A4 — Storing one bit: the D flip-flop
**Intuition.** A D flip-flop captures whatever is on D *at the clock edge* and holds it at Q until the next edge — "capture once, hold until told otherwise," the atom of digital memory. Physically: cross-coupled transistors holding each other's voltage (the SRAM pattern).
**Anchors.** [[learning/notes/quick-context/d-flip-flop|D Flip-Flop]] · [[learning/notes/quick-context/physics-of-writing-data-to-memory|Physics of Writing Data to Memory]] · [[learning/notes/micro-context/sram|SRAM Cell]] · [[learning/notes/quick-context/bare-minimal-data-storage-circuit|Bare-Minimal Data-Storage Circuit]] · [[learning/notes/quick-context/comparator|Comparator]] · Code: `<course>/sequential_chips/data_flip_flop_chip.py`, `bit_register_chip.py`
**Bridge.** One flip-flop = one bit. A useful value is many bits. Wire several to the *same* clock and they capture a whole word at once. → **A5**.

### A5 — The register: storing a whole word (the seed)
**Intuition.** N D flip-flops sharing one clock = a register; one edge captures a whole byte/word. The real breadboard chip (74HC574) and the exact unit inside a CPU's register file.
**Anchors.** [[learning/notes/quick-context/switches-to-registers-storing-data|Switches to Registers — Storing Data]] · Code: `<course>/sequential_chips/register_chip.py`
**Bridge.** Holding data is pointless unless we *do* something with it — add, compare. For that we need combinational logic that turns bits into arithmetic. → **A6**.

### A6 — Arithmetic → the ALU: gates that add and compare
**Intuition.** Gates → half-adder → multi-bit adder; add mode-select lines and you get an ALU: one block that adds/subtracts/ANDs/compares depending on a few control bits. Pure gates, no memory, sandwiched between registers.
**Anchors.** [[learning/notes/quick-context/code-to-gates-and-bootstrapping|Code to Gates & Bootstrapping]] · [[learning/notes/quick-context/transistor-design-history|Transistor Design History]] · Code: `<course>/combinational_chips/half_adder_chip.py`, `full_adder_chip.py`, `add16_chip.py`, `inc16_chip.py`, `alu_chip.py`
**Bridge.** Register → ALU → register is the compute heartbeat, but a few registers can't hold a program's data. We need a large *addressable* store. → **A7**.

### A7 — RAM: an addressable array of registers 🆕
**Intuition.** RAM = many registers + an address decoder. A DMUX routes "load" to one register (write); a MUX selects one register's output (read). `n` address bits pick `2ⁿ` words. Built recursively: RAM8 → RAM64 → … → RAM16K, each 8× the last.
**Anchors.** [[learning/notes/quick-context/ram-addressing-decoder|RAM — Addressing an Array of Registers]] · Code: `<course>/sequential_chips/ram8_chip.py` … `ram16K_chip.py`, `<course>/elementary_logic_gates/dmux8way_gate.py`, `mux8way16_gate.py`
**Bridge.** Now we can store lots of data *and* lots of numbers that happen to be **instructions**. Something must read those instruction-numbers one at a time and let each steer the registers/ALU/RAM. → **A8**.

### A8 — The CPU fetch-execute cycle: executing machine code ⭐ the meeting point
**Intuition.** The Program Counter (a register + incrementer) holds an address; the CPU **fetches** the instruction-number there, **decodes** it — its bits are literally wired to the ALU controls, register load-enables, and MUX selects — **executes** (ALU computes, a register/RAM cell captures the result on the clock edge), then the PC advances or jumps. One tick = one step. **Decoding is just routing bits**, so a program is a list of numbers, each a momentary setting of switches across the machine. *This is where electricity "runs code."*
**Anchors.** [[learning/notes/quick-context/cpu-fetch-execute-cycle|The CPU Fetch-Execute Cycle]] · Code: `<course>/computer/cpu.py`, `computer/memory.py`, `<course>/sequential_chips/program_counter_chip.py`, `<course>/combinational_chips/alu_chip.py`
**Bridge.** The CPU eats *machine code*. But you don't write machine code — you write Python. Where do those instruction-numbers come from? That's the other tower, descending to meet this rung. → **PART B**.

</details>

<details>
<summary><strong>PART B — The Software Tower (your Python ↓ down to that machine code)</strong></summary>

The hardware tower ends at "a CPU that executes machine code." This tower starts at human-written source and descends until it produces exactly that machine code — **the towers meet at the instruction.** Read downward.

### B1 — Source code as stored text & bytes 🆕
**Intuition.** A `.py` file is plain *text* — characters encoded (ASCII/UTF-8) as bytes, stored on disk and loaded into RAM (the same addressable cells from A7). The big reframe: **code is data.** The identical bytes-in-memory mechanism holds your text, the bytecode, and the final machine code; what makes bytes "code" is only how they're later executed.
**Anchors.** [[learning/notes/quick-context/how-source-code-is-stored|How Source Code Is Stored]] · Code: `<course>/computer/memory.py` (everything, including programs, lives in one addressable space)
**Bridge.** Text a human reads can't drive the ALU. It must be translated down toward machine code. The first translation turns source into a portable intermediate. → **B2**.

### B2 — Compile / transpile → bytecode & the VM (Python example) 🆕
**Intuition.** CPython **compiles** `x = 2 + 3` to **bytecode** (`LOAD_CONST … BINARY_OP … STORE_NAME`) for a stack-based **virtual machine** — its interpreter loop. Bytecode isn't CPU machine code; the VM *is* a C program already compiled to machine code that reads bytecode one op at a time. (Contrast: C/Rust compile straight to machine code (AOT); JIT engines compile hot bytecode to machine code at runtime; TypeScript *transpiles* to JavaScript, still needing an engine below.)
**Anchors.** [[learning/notes/quick-context/python-to-machine-code-pipeline|Python to Machine Code]] · [[learning/notes/quick-context/code-to-gates-and-bootstrapping|Code to Gates & Bootstrapping]] (the full 7-layer chain) · Code: `<course>/computer/cpu.py` (the machine that ultimately runs it)
**Bridge.** Whether via interpreter, JIT, or AOT compiler, the bottom of every route is the CPU's own language: assembly, assembled 1:1 into machine code. → **B3**.

### B3 — Assembly → machine code (the assembler)
**Intuition.** Assembly is a human-readable mnemonic for each machine instruction (`@2`, `D=A`, `D=D+A`); the **assembler** maps each line 1:1 to a binary instruction word per the **ISA**. That binary stream is precisely what the CPU at **A8** fetches and executes — **the two towers meet here.**
**Anchors.** [[learning/notes/quick-context/code-to-gates-and-bootstrapping|Code to Gates & Bootstrapping]] (Layers 5→4: assembly → machine code) · meets [[learning/notes/quick-context/cpu-fetch-execute-cycle|CPU Fetch-Execute]]
**Bridge.** We can now turn source into running machine code on a CPU. A full computer wraps that with start-up code, many chips talking, and real I/O. → **PART C**.

</details>

<details>
<summary><strong>PART C — The Running Machine (firmware, buses, keypress→pixel)</strong></summary>

### C1 — Firmware & boot: where the first instructions come from
**Intuition.** At power-on the CPU fetches from a fixed address holding *firmware* — the first code that wakes the chip and loads everything else. A microcontroller (e.g. STM32) packs CPU + RAM + flash + peripherals on one chip.
**Anchors.** [[learning/notes/quick-context/firmware|Firmware]] · [[learning/notes/quick-context/from-code-to-running-firmware|From Code to Running Firmware]] · [[learning/notes/micro-context/stm32-microcontroller|STM32 Microcontroller]]
**Bridge.** A live CPU+RAM still must talk to memory and devices over shared wires without colliding. → **C2**.

### C2 — Buses & communication protocols: chips talk
**Intuition.** A bus is a shared bundle (address/data/control); only one chip drives a wire at a time — others go *tri-state* via Output-Enable (the register's OE pin). Address decoding (chip-select) picks who responds; serial protocols (UART/I²C/SPI/USB/CAN) send bits one-after-another. Memory-mapped I/O = the CPU reaches peripherals through the same address space as RAM.
**Anchors.** [[learning/notes/quick-context/data-bus-and-arbitration|Data Bus & Arbitration]] 🆕 · [[learning/notes/quick-context/embedded-communication-protocols|Embedded Communication Protocols]] · [[learning/notes/quick-context/uart|UART]] · [[learning/notes/micro-context/i2c|I²C]] · [[learning/notes/quick-context/can-bus|CAN Bus]] · [[learning/notes/quick-context/usb-peripheral-hardware|USB Peripheral Hardware]]
**Bridge.** Now walk one concrete signal through every layer of both towers — finger to glowing letter. → **C3**.

### C3 — Keypress → pixel: the whole machine in one trace 🆕 the capstone
**Intuition.** A key is a physical switch (back to A2's 1/0). The keyboard MCU scans the matrix, debounces, sends a scancode over USB/serial (C2) → an **interrupt** hits the CPU → its handler (code from PART B, running fetch-execute at A8) reads the code → the OS keymap turns it into a character → the focused app's code decides to show it → the glyph's pixels are written into a framebuffer (RAM = A7) → the display controller/GPU scans it out and lights the pixels.
**Anchors.** [[learning/notes/quick-context/keypress-to-pixel-pipeline|Keypress to Pixel — Full Path]] · Code: `<course>/computer/memory.py` (memory-mapped Keyboard + Screen — the toy kernel of the real pipeline)
**Bridge.** That's the full climb, both towers, running. One last view: it wasn't always silicon, and every physical part had to be *made*. → **C4**, then **PART D**.

### C4 — Historical grounding
**Intuition.** Early computers used vacuum tubes as switches and magnetic cores as memory — the same logic+memory+clock pattern, room-sized. The through-line makes the abstraction feel inevitable.
**Anchors.** [[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens|From Vacuum Tubes to Coding on Screens]]

</details>

<details>
<summary><strong>PART D — The Fabrication Basement (how the physical parts are made)</strong></summary>

Everything in PART A is built from physical components. This basement shows how those components are manufactured — beneath even "electricity."

### D1 — Doping silicon: making the raw switch material
**Intuition.** Pure silicon is a poor conductor; *doping* it with trace impurities creates n-type and p-type regions whose junctions are the basis of every transistor and diode.
**Anchors.** [[learning/notes/quick-context/doped-silicon|Doped Silicon]] · [[learning/notes/quick-context/semiconductor-fabrication|Semiconductor Fabrication]]
**Bridge.** Doped regions are useless until patterned into billions of precise shapes. That's photolithography. → **D2**.

### D2 — The photolithography cycle: patterning a chip
**Intuition.** Fabs cycle photolithography → deposition → etch → ion-implant → planarize 50–100+ times to build transistors and on-chip wiring layer by layer on a wafer.
**Anchors.** [[learning/notes/quick-context/semiconductor-fabrication|Semiconductor Fabrication]] · [[learning/notes/quick-context/metal-interconnect-layers|Metal Interconnect Layers]] · [[learning/notes/quick-context/transistor-design-history|Transistor Design History]]
**Bridge.** That same process also makes the *other* parts — but resistors, capacitors, diodes, and comparators are made both on-chip and as discrete components. → **D3**.

### D3 — Resistors, capacitors, diodes, comparators 🆕
**Intuition.** **On-chip:** a resistor is a doped/poly strip; a capacitor is MOS or MIM between layers; a diode is a PN junction; a comparator/op-amp is an *IC* — many transistors on a die. **Discrete:** an SMD chip resistor is laser-trimmed thick film on ceramic; an MLCC capacitor is co-fired ceramic+metal layers; a diode is a PN die in a 2-lead package. All patterned in the same fab world as transistors.
**Anchors.** [[learning/notes/quick-context/how-passive-and-discrete-components-are-made|How Resistors, Capacitors, Diodes & Comparators Are Made]] · [[learning/notes/quick-context/resistor|Resistor]] · [[learning/notes/quick-context/capacitor|Capacitor]] · [[learning/notes/quick-context/diode|Diode]] · [[learning/notes/quick-context/comparator|Comparator]] · [[learning/notes/micro-context/smd-resistor|SMD Resistor]]
**Bridge.** A bare die can't be soldered or handled. It must be packaged and mounted onto a board with the other parts. → **D4**.

### D4 — Die → package → PCB → board
**Intuition.** The die is wire-bonded/flip-chipped into a package with external pins; packages and discrete parts are soldered onto a PCB whose copper layers wire them together — the centimeter-scale world your fingers touch.
**Anchors.** [[learning/notes/quick-context/silicon-die|Silicon Die]] · [[learning/notes/quick-context/substrate-ic-packaging|Substrate & IC Packaging]] · [[learning/notes/quick-context/common-ic-packages|Common IC Packages]] · [[learning/notes/quick-context/wire-bonding|Wire Bonding]] · [[learning/notes/quick-context/pcb-printed-circuit-board|PCB]] · [[learning/notes/quick-context/pcb-chip-transistor-hierarchy|PCB-Chip-Transistor Hierarchy]] · [[learning/notes/quick-context/soldering|Soldering]]

</details>

<details>
<summary><strong>The Whole Map at a Glance</strong></summary>

```
HOW A COMPUTER WORKS — TWO TOWERS MEETING AT MACHINE CODE
================================================================================

  PART C — THE RUNNING MACHINE
    keypress → pixel · firmware/boot · buses & protocols · history     ✅ +🆕
                              ▲
  PART B — SOFTWARE TOWER (your code  ↓ descends to machine code)
    B1  source as text/bytes .......................................  🆕
         │  compile
    B2  bytecode + virtual machine  (Python example) ...............  🆕
         │  assemble
    B3  assembly → MACHINE CODE ....................................  ✅
                              │
        ══════════════════════╪═══ THE TWO TOWERS MEET HERE ═══════════
                              ▼  (machine code is fed into the CPU)
  PART A — HARDWARE TOWER (electricity  ↑ climbs to run machine code)
    A8  CPU fetch–execute  ⭐ executes machine code ................  ✅
    A7  RAM (registers + address decoder) ..........................  🆕
    A6  ALU (gates that add/compare) ...............................  ✅
    A5  register (one word) ........................................  ✅
    A4  D flip-flop (one bit) ......................................  ✅
    A3  clock (piezo/quartz) — "capture NOW" .......................  ✅
    A2  switch → gates (transistor → NAND → all) ...................  ✅
    A1  power supply & passives (clean 0/1) ........................  ✅
    A0  electricity (voltage, current, power) ......................  ✅
                              ▲
        every physical part above was MANUFACTURED:
  PART D — FABRICATION BASEMENT
    D4  die → package → PCB → board ................................  ✅
    D3  resistors · capacitors · diodes · comparators ..............  🆕
    D2  photolithography cycle (patterning a chip) .................  ✅
    D1  dope silicon (the raw switch material) .....................  ✅

LEGEND:  ✅ existing note   🆕 created with this spine
```

**Status:** 24 rungs across 4 parts · all have notes · 0 gaps. Created this run (🆕): `ram-addressing-decoder`, `cpu-fetch-execute-cycle`, `data-bus-and-arbitration`, `keypress-to-pixel-pipeline`, `how-source-code-is-stored`, `python-to-machine-code-pipeline`, `how-passive-and-discrete-components-are-made`.

</details>

<details>
<summary><strong>Concrete Example — typing "A" through BOTH towers</strong></summary>

```
ONE KEYSTROKE, BOTH TOWERS, ALL THE WAY
================================================================================

  BEFOREHAND (software tower, PART B):  someone wrote the editor in Python/C →
    [B1] stored as text bytes → [B2] compiled to bytecode/VM (or [B3] to machine
    code) → ends as MACHINE CODE sitting in RAM, ready for the CPU.

  YOU PRESS "A"
        │
  [A2]  the key is a physical SWITCH — contacts close → a wire goes 1
        │
  [A3/A1] keyboard MCU's clocked matrix scan samples + debounces the contact
        │
  [C2]  MCU encodes a scancode → USB/HID packet → host → raises an INTERRUPT
        │
  [A8]  CPU fetch-execute runs the handler (the machine code from PART B):
        │  fetch → decode (bits steer ALU/registers) → execute. Reads the
        │  scancode from a memory-mapped input register.
        │
  [B-stack] OS keymap code (more instructions) translates scancode → 'A' = 65
        │  and delivers it to the focused app
        │
  [A7]  the app's code writes the glyph's pixels into the FRAMEBUFFER (RAM)
        │
  [A5/A4] each word is captured into memory cells on a clock edge
        │
  [C2]  display controller / GPU reads the framebuffer over a bus
        │
        ▼
  THE LETTER "A" LIGHTS UP ON SCREEN

  ── and every chip in that path (CPU, RAM, keyboard MCU, display driver) was
     built in PART D: doped silicon → litho → packaged die → soldered to a PCB.
```

The "code" in the trace is just machine-code numbers in RAM; each, when fetched, momentarily sets switches across the ALU/registers/RAM. That's why "running a program" and "electricity flowing through gates into registers" are the same sentence — and why the software tower had to descend all the way to machine code to meet the hardware.

</details>

<details>
<summary><strong>Concrete Example — storing ONE bit into RAM and DISK</strong></summary>

The trace above moves a keystroke *across* the towers. This one zooms all the way in on the rung where a bit actually *lands* — what physically holds the `1` once a clock edge (A3) captures it into a cell (A4→A7), and what changes when it's saved to disk. Take the letter `x` = ASCII `0x78` = `01111000`, pick **one** bit, and follow it into each storage technology. Same bit, three completely different physical states — and that difference *is* the speed/density/persistence tradeoff of the memory hierarchy.

```
ONE BIT, THREE PLACES IT CAN LIVE   (letter "x" = 0x78 = 0 1 1 1 1 0 0 0)
================================================================================
Pick bit 6 (a "1") and bit 7 (a "0"). Watch where each physically ends up.

  [A4/A5] CPU REGISTER / CACHE — SRAM   volatile · <1 ns · 6 transistors/bit
  ──────────────────────────────────────────────────────────────────────────
    A "1" = two cross-coupled inverters latched HIGH; "0" = latched LOW.
    The clock edge (A3) that loads the register IS this bit being captured.
        bit6 = 1 → Q = HIGH, Q̄ = LOW  ─┐ each inverter drives the other's
        bit7 = 0 → Q = LOW,  Q̄ = HIGH ─┘ input, so the pair holds itself.
    Power off → the voltages collapse → bit gone. (No charge moved; just
    transistors flipping — why registers are the fastest memory there is.)

  [A7] MAIN MEMORY — DRAM   volatile + refresh · ~15 ns · 1 transistor + 1 cap
  ──────────────────────────────────────────────────────────────────────────
    Memory controller addresses the cell via A7's decoder, then per bit:
        WRITE 1 (bit6): drive bitline → Vdd, pulse wordline → charge flows
                        onto a ~10-30 fF capacitor (tens of thousands of e⁻).
        WRITE 0 (bit7): drive bitline → GND, pulse wordline → capacitor drains.
    Charge leaks in ms → every 32-64 ms a refresh re-reads + rewrites the row.
    Power off → capacitors discharge → bit gone.

  [DISK] SSD — NAND FLASH   non-volatile · ~200 µs write · floating gate
  ──────────────────────────────────────────────────────────────────────────
    On Ctrl+S the SSD controller programs a page; per bit:
        WRITE 0 (bit7): ~15-20 V on control gate → field ≈ 2.5×10⁹ V/m across
                        an ~8 nm oxide → electrons Fowler-Nordheim-tunnel onto
                        a floating gate and stay TRAPPED behind the insulator.
        WRITE 1 (bit6): leave the (pre-erased) cell empty — no electrons.
    Power off → electrons stay behind the oxide wall → bit survives 10+ years.
```

The deeper a bit is meant to persist, the harder a barrier its charge must cross to get there: a register just flips a voltage, DRAM pushes charge through a transistor channel, flash forces electrons through an insulating wall by quantum tunneling. Full physics (sense amps, refresh, endurance, the MCU-flash path): [[learning/notes/quick-context/physics-of-writing-data-to-memory|Physics of Writing Data to Memory]] · breadboard version with real chips: [[learning/notes/quick-context/switches-to-registers-storing-data|Switches to Registers]].

</details>

<details>
<summary><strong>Bootstrapping — where the first software came from</strong></summary>

The software tower (PART B) quietly assumes a compiler, an assembler, and an OS loader **already exist**. But each of those is itself a program — so what built the first one? The chicken-and-egg answer is **bootstrapping**: you climb up from bare hardware by hand, each tool building the next better tool. This is the historical origin of the whole tower, and it's also what still happens at every power-on (the reset vector at C1 is the modern punch card — code that needs no loader because it's physically burned into ROM).

```
THE CHICKEN-AND-EGG OF SOFTWARE: HOW THE FIRST TOOLS WERE MADE
================================================================================
PART B assumes a compiler, assembler, and loader already exist. Each is itself
a program — so what built the first? You climb up from bare hardware, by hand.

  STEP 0  NAKED HARDWARE
          A CPU that can fetch-execute (A8) but zero software. At power-on the
          PC jumps to a hardwired RESET VECTOR (C1) — the only "code" needing no
          loader, because it's burned into ROM at the factory.

  STEP 1  HAND-ENCODED BINARY → FIRST ASSEMBLER
          Humans punch instruction words bit-by-bit onto cards (hole = 1):
              ○ ● ○ ○ ○ ● ● ○   ← one instruction per row
          Those bits ARE a tiny program: "read mnemonic text, look up its
          binary, write that binary to memory." The first assembler — by hand.

  STEP 2  ASSEMBLER → BETTER ASSEMBLER
          Now write  @2 / D=A / D=D+A  as text (B3). Feed it through Step 1's
          assembler → binary. Use that to write a richer assembler (labels,
          macros) — in assembly this time, not raw bits.

  STEP 3  ASSEMBLER → FIRST COMPILER
          Write a small high-level compiler in assembly. It turns `x = 2 + 3`
          (B1) into assembly (B3) → machine code — the two towers now meet (A8).

  STEP 4  SELF-HOSTING
          Rewrite the C compiler IN C; compile it with the old one. Now the
          compiler builds itself. Every modern toolchain (GCC, LLVM, rustc, Go)
          descends from this — an unbroken chain back to the punch cards.
```

So the tower wasn't dropped in finished — it was bootstrapped up one rung at a time, hand-encoded binary first. Full chain (encoding details, reset vector, self-hosting): [[learning/notes/quick-context/code-to-gates-and-bootstrapping|Code to Gates & Bootstrapping]] · how the *interface* evolved from punch cards to screens: [[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens|From Vacuum Tubes to Coding on Screens]].

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/quick-context/fundamental-electronic-parts-index|Fundamental Electronic Parts — Index]]** — the component-level companion map (passives → actives → packaging). "What are the parts?" to this spine's "how do the parts become a computer?"
- **[[learning/notes/quick-context/pcb-chip-transistor-hierarchy|PCB-Chip-Transistor Hierarchy]]** — the physical packaging scale from nm transistors to cm boards.
- **[[learning/notes/quick-context/from-code-to-running-firmware|From Code to Running Firmware]]** & **[[learning/notes/quick-context/code-to-gates-and-bootstrapping|Code to Gates & Bootstrapping]]** — the two fuller treatments of the software tower (linking/flashing/booting, and the full 7-layer chain incl. bootstrapping).
- **The Nand2Tetris course** (`learning/references/courses/python-nand-to-tetris-part-1`) — the hardware tower as runnable Python, `nand_gate.py` → `cpu.py`. This spine is a reading guide pairing each chip with its intuition (and the software-tower compiler/VM/assembler are the course's Part 2).

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** The map is "two towers meeting at machine code." What does each tower start from, and what is the meeting point?
<details>
<summary>Answer</summary>
The **hardware tower** starts at raw electricity (A0) and climbs *up* to a CPU that executes machine code (A8). The **software tower** starts at human-written source (B1) and descends *down* through bytecode/VM (B2) and assembly (B3) to produce machine code. They **meet at machine code**: the binary instruction stream the assembler emits is exactly what the CPU fetch-executes. See: PART A8, PART B3, and the at-a-glance map.
</details>

**Q2:** Python "compiles to bytecode," yet Python is called interpreted. How is bytecode different from the machine code the CPU runs?
<details>
<summary>Answer</summary>
Bytecode is instructions for a **virtual machine** (CPython's stack-based interpreter loop), not for the CPU. The CPU can't execute bytecode directly. Instead the CPython interpreter — itself a C program already compiled **ahead-of-time into real machine code** — reads bytecode one op at a time and acts on it. So bytecode is executed *by* machine code. Compiled languages (C/Rust) skip the VM and become machine code directly; JIT engines compile hot bytecode to machine code at runtime. See: B2 and [[learning/notes/quick-context/python-to-machine-code-pipeline|Python to Machine Code]].
</details>

**Q3:** In what concrete sense is "code just a list of instructions," and where does that become physical?
<details>
<summary>Answer</summary>
At A8. A machine instruction is a number in RAM whose bits are physically wired to control lines — ALU op-select, register load-enables, MUX selects. "Decoding" just routes those bits to where they steer hardware. So a program is a list of numbers; fetching each momentarily sets switches across the machine. The whole software tower (B1→B3) exists to turn human source into that list. See: A8, B3, Concrete Example.
</details>

**Q4:** A comparator and a resistor are both "components," but they're manufactured very differently. How?
<details>
<summary>Answer</summary>
A **comparator** is an integrated circuit — many transistors (plus on-chip resistors/caps) fabricated together on a silicon die by photolithography, then packaged. A **resistor** can be *on-chip* (a doped/polysilicon strip whose value comes from geometry+doping, made in the same litho process) or *discrete* (an SMD chip resistor: laser-trimmed thick film on a ceramic body, soldered to a PCB). See: PART D3 and [[learning/notes/quick-context/how-passive-and-discrete-components-are-made|How Components Are Made]].
</details>

**Q5:** Trace the minimum rungs a single keystroke crosses to change one pixel, and name where the *software* tower already did its work.
<details>
<summary>Answer</summary>
The software tower ran *beforehand*: the editor/OS source (B1) was compiled (B2) / assembled (B3) into machine code now sitting in RAM. At keypress: switch closes (A2) → clocked scan+debounce (A3/A1) → protocol+interrupt (C2) → CPU fetch-executes that machine code (A8) → keymap code maps to 'A' → glyph pixels written to framebuffer in RAM (A7) → display controller reads it over the bus (C2) → pixel lights. See: Concrete Example.
</details>

</details>
