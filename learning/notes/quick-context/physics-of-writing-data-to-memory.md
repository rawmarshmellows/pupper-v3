---
topic: Physics of Writing Data to Memory — How Bits Become Charges, Voltages, and Trapped Electrons
created: 2026-04-07
---
> **Related:** [[learning/notes/micro-context/microcontroller]] | [[learning/notes/micro-context/reverse-and-forward-bias]] | [[learning/notes/micro-context/scan-loop]] | [[learning/notes/micro-context/st-link-v2-programmer]] | [[learning/notes/micro-context/stm32-microcontroller]]

> **TL;DR:** Every bit stored in a computer is a physical thing — a [[learning/notes/quick-context/voltage|voltage]] held stable by cross-coupled [[learning/notes/micro-context/mosfet|transistors]] (SRAM), a tiny charge on a ~10-30 femtofarad [[learning/notes/quick-context/capacitor|capacitor]] that leaks away in milliseconds (DRAM), or electrons trapped on a floating gate surrounded by insulating oxide that holds them for decades without power (flash). Writing a bit means physically moving charge: SRAM flips [[learning/notes/quick-context/transistor|transistor]] states in <1 ns, DRAM dumps charge onto a capacitor through an access transistor, and flash forces electrons through an oxide barrier using 15-20V pulses via Fowler-Nordheim tunneling. When you type `x = 5` in a `.py` file, the letter `x` exists as a voltage pattern in DRAM, a trapped-electron pattern on your SSD, and — if it's machine code being [[learning/notes/quick-context/from-code-to-running-firmware|flashed to an MCU]] — electrons jammed onto floating gates inside the chip's flash memory by a debug probe.

## The Core Problem

The [[learning/notes/quick-context/code-to-gates-and-bootstrapping|compilation chain]] explains how source code becomes binary instructions, and the [[learning/notes/quick-context/from-code-to-running-firmware|firmware pipeline]] explains how those instructions reach the chip. But neither explains the *physics* of the final step: how a `1` or `0` actually gets written into a physical memory cell. What voltage is applied? What moves? What holds the bit in place? This matters because the three main memory technologies (SRAM, DRAM, flash) use fundamentally different physical mechanisms, and their tradeoffs — speed, density, volatility, endurance — all trace back to the physics of how they store charge.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Floating Gate** | An electrically isolated polysilicon layer inside a flash memory [[learning/notes/micro-context/mosfet|MOSFET]], surrounded by oxide insulation. Electrons trapped here shift the transistor's threshold voltage, encoding a bit that persists without power for 10+ years. |
| **Fowler-Nordheim Tunneling** | The quantum-mechanical process used to program/erase flash memory. A strong electric field (15-20V) gives electrons enough energy to tunnel through the ~7-10 nm oxide barrier onto or off of the floating gate. |
| **Sense Amplifier** | A circuit that detects the tiny voltage difference on a bitline during a DRAM/flash read and amplifies it to a full logic level. In DRAM, the stored charge is so small (~10-30 fF) that reading it requires destroying and rewriting the cell. |
| **Cross-Coupled Inverters** | The core of an SRAM cell — two CMOS inverters connected output-to-input in a loop. Each inverter reinforces the other's state, creating two stable voltage configurations (bit = 0 or 1) that persist as long as power is on. This is the same feedback principle that gives [[quick-context/d-flip-flop|D flip-flops]] their memory. |
| **Wordline / Bitline** | The row and column wires in a memory array. The **wordline** activates a row of cells (turns on access transistors), and the **bitline** carries the data in or out. Writing = drive the bitline to the desired voltage, then pulse the wordline to connect the cell. |

<details>
<summary><strong>How It Works</strong> — Three ways to physically store a bit</summary>

### The Three Memory Technologies

Every memory cell stores a bit as some form of electrical charge or voltage. The three dominant technologies differ in *how* they hold that charge:

```
THREE WAYS TO STORE A BIT
================================================================================

SRAM (Static RAM) — Stable voltage on cross-coupled transistors
─────────────────────────────────────────────────────────────────
  Used in: CPU registers, L1/L2/L3 cache, MCU SRAM

  6 transistors per bit. Two cross-coupled CMOS inverters hold a
  stable HIGH or LOW voltage. Two access transistors gate read/write.

       Vdd ─────┬──────────────┬───── Vdd
                 │              │
              ┌──┴──┐        ┌──┴──┐
              │PMOS │        │PMOS │
              └──┬──┘        └──┬──┘
     Q ─────────┤├──────────────┤├──────── Q̄
              ┌──┴──┐        ┌──┴──┐
              │NMOS │        │NMOS │
              └──┬──┘        └──┬──┘
                 │              │
       GND ─────┴──────────────┴───── GND

  Inverter A's output drives Inverter B's input, and vice versa.
  If Q = HIGH → Q̄ = LOW → Inverter A's input is LOW → Q stays HIGH.
  Self-reinforcing. Noise nudges the voltage? The loop corrects it.

  Write: drive the bitline to desired value, pulse wordline to open
         access transistors. The bitline overwhelms the cell's state.
  Speed: <1 ns. No charge transfer — just transistor switching.
  Volatile: loses state when power is removed.
  Density: poor (6 transistors per bit).


DRAM (Dynamic RAM) — Charge on a tiny capacitor
─────────────────────────────────────────────────────────────────
  Used in: main system memory (DDR4, DDR5, LPDDR)

  1 transistor + 1 capacitor per bit.

       Wordline
          │
     ┌────┴────┐
     │  Access  │
     │Transistor│
     └────┬────┘
          │
  Bitline─┤
          │
     ┌────┴────┐
     │Capacitor│  ~10-30 fF (femtofarads)
     │  ┌──┐   │  Stores ~40,000-200,000 electrons for a "1"
     │  │▓▓│   │
     └──┴──┴───┘
          │
        GND

  "1" = capacitor charged (electrons stored)
  "0" = capacitor discharged (no charge)

  Write: drive bitline to Vdd (for 1) or GND (for 0), pulse wordline
         to Vcc + Vth to fully open access transistor. Charge flows
         onto capacitor through the transistor channel.
  Read: precharge bitline to Vdd/2, pulse wordline. Stored charge
         shifts bitline voltage slightly. Sense amplifier detects
         the difference and amplifies to full logic level. Reading
         DESTROYS the stored charge — the cell must be rewritten.
  Refresh: every 32-64 ms, every row must be read and rewritten
           because charge leaks through the transistor junction
           and oxide (~1 fA leakage current). Without refresh,
           data disappears in milliseconds.
  Density: excellent (1T + 1C per bit).
  Volatile: loses data when power is removed OR refresh stops.


FLASH MEMORY — Electrons trapped on a floating gate
─────────────────────────────────────────────────────────────────
  Used in: SSDs, USB drives, MCU program memory, SD cards

  1 floating-gate transistor per bit (SLC). The transistor has
  TWO gates stacked vertically:

       Control Gate  ← connected to wordline
     ┌─────────────┐
     │ Oxide (ONO)  │  ~15 nm insulating layer
     ├─────────────┤
     │ FLOATING GATE│  ← polysilicon, COMPLETELY surrounded
     │ (electrons   │     by oxide. Electrically isolated.
     │  trapped     │     Electrons stay here for 10+ years.
     │  here)       │
     ├─────────────┤
     │ Tunnel Oxide │  ~7-10 nm SiO₂ — the barrier electrons
     ├─────────────┤     must tunnel through
     │   Channel    │
     └──┬───────┬──┘
      Source   Drain

  No electrons on floating gate → low threshold voltage → "1" (erased)
  Electrons on floating gate → high threshold voltage → "0" (programmed)

  Program (write "0"):
    Apply ~15-20V to control gate, 0V to source.
    Electric field across tunnel oxide is enormous:
    $E = V / d \approx 20V / 8nm = 2.5 \times 10^9 \text{ V/m}$
    Fowler-Nordheim tunneling: electrons quantum-tunnel through
    the oxide barrier and get trapped on the floating gate.
    Takes ~200-500 μs per page.

  Erase (restore to "1"):
    Apply ~20V to source (or substrate), 0V to control gate.
    Field reverses. Electrons tunnel OFF the floating gate.
    Erase happens per BLOCK (many pages at once), ~2-5 ms.

  Read:
    Apply intermediate voltage to control gate (between the
    threshold of a programmed and erased cell).
    If current flows → cell is erased → "1"
    If no current → cell is programmed → "0"

  Non-volatile: trapped electrons persist without power.
  Endurance: oxide degrades with each tunnel event.
    SLC: ~100,000 program/erase cycles. TLC: ~1,000-3,000.
  Density: excellent (1 transistor per bit, or 2-4 bits per
           cell in MLC/TLC/QLC using multiple voltage levels).
```

### Speed Comparison

| Operation | SRAM | DRAM | Flash (NAND) |
|-----------|------|------|-------------|
| Read | <1 ns | ~10-20 ns | ~25-50 $\mu$s |
| Write | <1 ns | ~10-20 ns | ~200-500 $\mu$s (page) |
| Erase | N/A | N/A | ~2-5 ms (block) |
| Volatile? | Yes | Yes (needs refresh) | No |
| Bits/cell | 1 (6 transistors) | 1 (1T + 1C) | 1-4 (1 transistor) |

The speed difference is physical: SRAM just flips transistor states (fast), DRAM transfers charge through a channel (medium), and flash forces electrons through an oxide barrier via quantum tunneling (slow, requires high voltage).

</details>

<details>
<summary><strong>The Key Tension</strong> — Speed vs. density vs. persistence</summary>

### The Memory Hierarchy Tradeoff

No single memory technology is best at everything. The physics forces a three-way tradeoff:

| Property | SRAM | DRAM | Flash |
|----------|------|------|-------|
| **Speed** | Fastest (<1 ns) | Fast (~15 ns) | Slowest (~200 $\mu$s write) |
| **Density** | Worst (6T/bit) | Good (1T+1C/bit) | Best (1T/bit, multi-level) |
| **Persistence** | Volatile | Volatile + refresh | Non-volatile |
| **Endurance** | Unlimited writes | Unlimited writes | Limited P/E cycles |
| **Cost/bit** | $$$$ | $$ | $ |
| **Power** | High (leakage in 6T) | Medium (refresh circuits) | Low (no power to retain) |

**Why not just use the fastest?** SRAM needs 6 transistors per bit. A 16 GB SRAM module would need $16 \times 10^9 \times 8 \times 6 = 768 \times 10^9$ transistors just for storage — physically enormous and prohibitively expensive. DRAM gets the same capacity with $128 \times 10^9$ transistors + capacitors.

**Why not just use the densest?** Flash writes are 1000x slower than DRAM and degrade the oxide with every write. Running a program from flash (as MCUs do) is fine for reads, but you can't use flash as working memory — the write speed and endurance would be catastrophic.

**The physical root cause:** Storing a bit more *permanently* requires moving charge through a stronger barrier, which takes more energy and time. SRAM holds bits as voltages on transistor gates (fast to change, gone without power). DRAM holds charge on a capacitor (slightly harder to change, leaks away). Flash traps electrons behind an oxide wall (hard to change, stays for years). The tradeoff is inescapable because it's rooted in the physics of charge storage.

This is why computers use a **memory hierarchy**: SRAM for registers/cache (tiny, fast), DRAM for main memory (big, fast enough), flash/SSD for storage (massive, persistent). Each level exploits a different point on the speed-density-persistence curve.

</details>

<details>
<summary><strong>Concrete Example</strong> — From keypress to stored bit: what happens physically when you type "x" in a .py file</summary>

### The Physical Journey of the Letter "x"

When you type the letter `x` into a Python file, the ASCII byte `0x78` (binary `01111000`) must be physically written into memory at every level of the hierarchy. Here's what happens at the hardware level:

```
THE PHYSICAL JOURNEY OF A KEYPRESS → STORED BIT
================================================================================

STEP 1: KEYBOARD → SCAN CODE → USB → PC (mechanical → electrical)
─────────────────────────────────────────────────────────────────

  Your finger presses the "x" key. A mechanical switch closes.

  Inside the keyboard is a small MCU (often a CH552 or 8051)
  whose firmware exists as trapped electrons on floating gates
  in flash — [[learning/notes/quick-context/from-code-to-running-
  firmware|programmed at the factory]] via the same Fowler-
  Nordheim tunneling physics described in STEP 5 below.

  The MCU's [[learning/notes/quick-context/code-to-gates-and-
  bootstrapping|fetch-execute cycle]] runs a scan loop:
  drive each matrix row LOW, read columns. Row 2, Col 1 reads
  LOW → "x" detected → firmware looks up the USB HID scan
  code (0x1B) from a table in flash → packages an 8-byte HID
  report → writes it to the USB endpoint buffer (SRAM inside
  the USB peripheral).

  The [[learning/notes/quick-context/usb-peripheral-hardware|
  USB peripheral's Serial Interface Engine (SIE)]] takes over:
  it serializes the bytes, NRZI-encodes them, appends CRC,
  and drives push-pull MOSFET pairs to toggle D+/D- between
  3.3V and 0V at 12 MHz. The scan code travels to the PC as
  voltage transitions on the USB cable.

  (See [[learning/notes/quick-context/usb-peripheral-hardware|
  USB Peripheral Hardware]] for the full Phase 0→5 breakdown
  of how the SIE turns buffer bytes into voltage on the wire.)


STEP 2: PC USB CONTROLLER → CPU INTERRUPT (serial → parallel)
─────────────────────────────────────────────────────────────────

  The PC's USB host controller receives the differential
  voltage transitions, NRZI-decodes them, checks the CRC, and
  assembles the 8-byte HID report in its buffer (SRAM inside
  the USB controller chip).

  The USB controller raises an INTERRUPT signal — a voltage
  change on a dedicated CPU pin. The CPU's interrupt controller
  notices and redirects the Program Counter to the interrupt
  handler address from the vector table.


STEP 3: CPU PROCESSES SCAN CODE → ASCII (registers = SRAM)
─────────────────────────────────────────────────────────────────

  The CPU reads the scan code from the USB controller's I/O port
  into a register. The register is SRAM — 6 cross-coupled
  transistors per bit, flipping state in <1 ns.

  The keyboard driver (software) translates the scan code to
  ASCII: "x" → 0x78 → binary 01111000.

  At this moment, the byte 0x78 exists as 8 voltage states
  across 48 transistors (6 per bit) in a CPU register:

    Bit 7: 0 → Q = LOW,  Q̄ = HIGH  (inverter pair stable at "0")
    Bit 6: 1 → Q = HIGH, Q̄ = LOW   (inverter pair stable at "1")
    Bit 5: 1 → Q = HIGH, Q̄ = LOW
    Bit 4: 1 → Q = HIGH, Q̄ = LOW
    Bit 3: 1 → Q = HIGH, Q̄ = LOW
    Bit 2: 0 → Q = LOW,  Q̄ = HIGH
    Bit 1: 0 → Q = LOW,  Q̄ = HIGH
    Bit 0: 0 → Q = LOW,  Q̄ = HIGH


STEP 4: CPU → DRAM (register → main memory)
─────────────────────────────────────────────────────────────────

  The OS text editor writes the character to a buffer in DRAM.
  The CPU issues a memory write: the memory controller selects
  the target row and column in the DRAM chip.

  For each bit of 0x78 (01111000):

    WRITE A "1" (e.g., bit 6):
    1. Memory controller drives the bitline to Vdd (~1.2V for DDR4)
    2. Wordline voltage rises to Vdd + Vth (~2V) to fully open
       the access transistor
    3. Charge flows through the transistor channel onto the
       storage capacitor (~10-30 fF fills with tens of thousands of electrons)
    4. Wordline drops → transistor closes → charge trapped

    WRITE A "0" (e.g., bit 7):
    1. Memory controller drives bitline to GND (0V)
    2. Wordline opens the access transistor
    3. Any existing charge drains off the capacitor
    4. Wordline drops → capacitor stays discharged

  Every 32-64 ms, a refresh circuit re-reads and re-writes
  every row to replace charge that leaked away. If your
  computer loses power right now, the capacitors discharge
  in milliseconds and the "x" is gone.


STEP 5: DRAM → SSD FLASH (when you hit Ctrl+S)
─────────────────────────────────────────────────────────────────

  The filesystem tells the SSD controller to write the file.
  The SSD controller finds a free page (4 KB) in a NAND flash
  block and programs it.

  For each bit of 0x78 (01111000):

    PROGRAM A "0" (e.g., bit 7 — flash "0" means electrons stored):
    1. SSD controller applies ~15-20V to the control gate
       via the wordline
    2. Source held at 0V → enormous electric field across
       the 7-10 nm tunnel oxide:
       $E \approx 20V / 8nm = 2.5 \times 10^9 \text{ V/m}$
    3. Fowler-Nordheim tunneling: electrons quantum-tunnel
       through the oxide barrier and land on the floating gate
    4. Voltage removed → electrons are TRAPPED — oxide
       insulation holds them in place for 10+ years
    5. Threshold voltage of the transistor has shifted upward

    LEAVE A "1" (e.g., bit 6 — flash "1" means erased, no electrons):
    1. The cell was already erased (block erase clears all cells)
    2. No programming pulse applied → floating gate stays empty
    3. Threshold voltage remains low

  Now the letter "x" exists as a pattern of trapped electrons
  and empty floating gates on a silicon chip inside your SSD.
  Power off the computer — the electrons stay. Come back in a
  year — the electrons are still there.
```

### What about machine code on an MCU?

When you [[learning/notes/quick-context/from-code-to-running-firmware|flash firmware]] to an [[learning/notes/micro-context/stm32-microcontroller|STM32]], the same floating-gate physics applies, but the path is different:

1. The [[learning/notes/micro-context/st-link-v2-programmer|ST-Link]] debug probe sends the machine code bytes over [[learning/notes/micro-context/swd-serial-wire-debug|SWD]] (2 wires: SWDIO + SWCLK)
2. The SWD protocol writes to the MCU's flash controller registers via the AHB bus
3. The flash controller's internal charge pump generates the ~15-20V programming voltage from the 3.3V supply
4. The charge pump drives the wordlines while the data is placed on bitlines
5. Fowler-Nordheim tunneling traps electrons on floating gates — same physics as an SSD, but the flash cells are NOR-type (individually addressable) rather than NAND-type (page-addressable)
6. After programming, the controller reads back and verifies each word

The entire process — erase block, program page, verify — takes ~100-500 ms for the full firmware image. After that, the machine code exists as trapped electrons on the [[learning/notes/quick-context/silicon-die|silicon die]], persisting without power until intentionally erased.

**The one thing most outsiders get wrong about this is...** thinking that bits are somehow "magnetic" or "electrical" in a vague hand-wavy sense. They're not vague at all. A bit in DRAM is literally tens of thousands of electrons sitting on a capacitor plate. A bit in flash is literally electrons trapped behind an 8-nanometer oxide wall by quantum tunneling. A bit in SRAM is literally two transistor pairs holding each other's voltages stable. Every `0` and `1` in your computer is a concrete physical arrangement of electrons — and the differences between memory technologies come down to *how hard it is to put those electrons there* and *how hard it is for them to escape*.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[learning/notes/quick-context/code-to-gates-and-bootstrapping]]** — The upstream story: how source code becomes the machine code binary patterns that ultimately get written into memory. This document explains *what* those patterns are; the current document explains *how* they get physically stored.

- **[[learning/notes/quick-context/from-code-to-running-firmware]]** — The linking and flashing pipeline: how compiled code goes from an ELF file on your PC to bytes in an MCU's flash memory. Covers the software toolchain (linker, flash programmer) that drives the physical write process described here.

- **[[learning/notes/quick-context/transistor]]** — The [[learning/notes/micro-context/mosfet|MOSFET]] switch that is the foundation of all three memory types. SRAM uses 6 MOSFETs per bit, DRAM uses 1 [[learning/notes/micro-context/mosfet|MOSFET]] + 1 capacitor, and flash uses a modified MOSFET with a floating gate.

- **[[learning/notes/quick-context/transistor-analog-to-digital]]** — How the analog voltage on a DRAM capacitor or flash floating gate gets interpreted as a clean digital 0 or 1. Noise margins and sense amplifiers are what make this work.

- **[[learning/notes/quick-context/doped-silicon]]** — The [[learning/notes/micro-context/reverse-and-forward-bias|PN junctions]] that make charge storage possible. The DRAM access transistor and the flash floating-gate transistor both rely on doped regions to control current flow.

- **[[learning/notes/quick-context/silicon-die]]** — Where the memory cells physically live. Flash memory on an SSD die, SRAM in a CPU cache die, DRAM on a separate die — all manufactured via [[learning/notes/quick-context/semiconductor-fabrication|photolithography]].

- **Charge Trap Flash (CTF)** — Modern 3D NAND (Samsung V-NAND, Micron 3D NAND) replaces the polysilicon floating gate with a silicon nitride charge-trap layer. Same tunneling physics, but the trap layer is more compatible with vertical stacking (100+ layers).

- **Multi-Level Cells (MLC/TLC/QLC)** — Store 2/3/4 bits per flash cell by distinguishing multiple threshold voltage levels. Each additional bit doubles the voltage precision needed, reducing endurance and read speed. QLC distinguishes 16 voltage levels per cell.

- **Wear Leveling** — SSD controller firmware that distributes writes evenly across flash blocks to prevent any single block from hitting its P/E cycle limit before others. Without it, frequently-written blocks would die early.

- **[[learning/notes/quick-context/usb-peripheral-hardware]]** — Deep dive into STEP 1/STEP 4 of the keypress journey: how the keyboard MCU's Serial Interface Engine (SIE) autonomously serializes bytes from the endpoint buffer into NRZI-encoded voltage transitions on the USB data lines, using MOSFET push-pull drivers switching at 12 MHz.

- **[[learning/notes/quick-context/switches-to-registers-storing-data]]** — A breadboard-level circuit (switches + clock button + 74HC574) that demonstrates data storage with real chips, and explains how this minimal pattern scales to build every register and RAM in a computer. The 74HC574's internal flip-flops use the same cross-coupled inverter pattern described here.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does DRAM need to be refreshed every 32-64 ms, while SRAM does not?
<details>
<summary>Answer</summary>
DRAM stores bits as charge on a capacitor, and that charge leaks away through the access transistor's junction and oxide (leakage current ~1 fA). Without refresh, the capacitor discharges and the bit is lost. SRAM stores bits as stable voltage states in cross-coupled inverters — the transistors actively reinforce each other's states through feedback, so small perturbations are corrected rather than accumulated. SRAM doesn't leak *data* (though it does draw leakage *current*). See: How It Works (DRAM vs. SRAM sections)
</details>

**Q2:** What physical mechanism makes flash memory non-volatile?
<details>
<summary>Answer</summary>
The floating gate is completely surrounded by insulating oxide (SiO$_2$). Once electrons are tunneled onto the floating gate during programming, the oxide barrier prevents them from escaping. There is no leakage path — the electrons are trapped by the insulating layer, not held by an applied voltage. They persist for 10+ years without power. This is fundamentally different from SRAM (which needs power to maintain transistor states) and DRAM (which needs refresh to replace leaked charge). See: How It Works (FLASH MEMORY section)
</details>

**Q3:** Reading a DRAM cell destroys its contents. Why doesn't reading a flash cell destroy its contents?
<details>
<summary>Answer</summary>
In DRAM, reading works by connecting the tiny storage capacitor to the long bitline — charge redistributes between them, destroying the original voltage on the capacitor. The sense amplifier must then rewrite the cell. In flash, reading works by applying an intermediate voltage to the control gate and checking if current flows through the channel. The floating gate's trapped electrons are never disturbed — the read voltage is far too low to cause tunneling. The electrons stay put because the oxide barrier is only penetrable at the much higher programming voltages (15-20V). See: How It Works (DRAM read vs. FLASH read)
</details>

**Q4:** An MCU's flash is NOR-type while an SSD uses NAND-type flash. Both use floating-gate transistors and Fowler-Nordheim tunneling. What's the architectural difference, and why does it matter for machine code execution?
<details>
<summary>Answer</summary>
In NOR flash, each cell has its own connection to a bitline — cells are wired in parallel, allowing random byte-level access. This lets the CPU fetch individual instructions directly from flash (execute-in-place / XIP). In NAND flash, cells are wired in series (strings of 32-128 cells), which increases density but means you can only read/write entire pages (4-8 KB) at once. NAND can't support XIP because the CPU needs to fetch individual 2-4 byte instructions at arbitrary addresses. This is why MCUs use NOR flash for code storage (direct execution) while SSDs use NAND flash for data storage (page-level I/O is fine for file operations). See: Concrete Example (What about machine code on an MCU?)
</details>

**Q5:** Flash endurance is limited (SLC ~100K cycles, TLC ~3K cycles) because the tunnel oxide degrades with each program/erase. SRAM and DRAM have unlimited write endurance. Trace this difference back to the physics: what exactly degrades, and why don't SRAM/DRAM have the same problem?
<details>
<summary>Answer</summary>
Each time electrons tunnel through the oxide in flash, some get trapped *inside* the oxide itself (not on the floating gate) — these are called "oxide trap charges." Over thousands of P/E cycles, trapped charges accumulate and weaken the oxide's insulating ability, shifting the threshold voltage window and eventually making it impossible to distinguish programmed from erased states. The oxide physically degrades because it's being subjected to extreme electric fields ($\sim 2.5 \times 10^9$ V/m) that force quantum tunneling. SRAM doesn't have this problem because it stores bits as transistor voltage states — no charge is forced through any oxide barrier during writes. DRAM doesn't have this problem because charge flows through the access transistor's *channel* (a conductive path), not through insulating oxide — the write mechanism is conventional current flow, not tunneling. The unlimited endurance of SRAM and DRAM comes from the fact that their write mechanisms don't damage any material. See: How It Works (Flash endurance) and The Key Tension
</details>

</details>
