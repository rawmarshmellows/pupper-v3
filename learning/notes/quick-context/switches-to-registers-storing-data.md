---
topic: Switches to Registers — Storing Data with Real Hardware
created: 2026-04-09
---

# Switches to Registers — Storing Data with Real Hardware

> **Related:** [[learning/notes/quick-context/d-flip-flop]] | [[learning/notes/quick-context/physics-of-writing-data-to-memory]] | [[learning/notes/quick-context/code-to-gates-and-bootstrapping]] | [[learning/notes/quick-context/ram-addressing-decoder]] | [[learning/notes/quick-context/data-bus-and-arbitration]]

> **TL;DR:** A physical switch provides a 1 or 0, a clock signal says "capture NOW," and a [[learning/notes/quick-context/d-flip-flop|D flip-flop]] stores the bit at the clock edge. Chain eight flip-flops into a register (a real chip: the 74HC574), connect eight switches and eight LEDs, and you've built the fundamental unit of all computing memory. Every register in every CPU, every byte in every [[learning/notes/micro-context/sram|SRAM]] cache, and every address in every RAM chip is just a scaled-up version of this exact circuit.

## The Core Problem

Combinational logic (AND, OR, NOT gates built from [[learning/notes/quick-context/transistor|transistors]]) can *compute* — but it can't *remember*. The instant you remove the inputs, the outputs vanish. To do anything useful — count, accumulate, follow a sequence of instructions — a circuit needs to **store a value and hold it stable** until deliberately changed. The D flip-flop solves this: it captures one bit at a [[learning/notes/micro-context/clock-edges|clock edge]] and holds it until the next edge. An 8-bit register is just eight of these in parallel, and from registers you can build RAM, CPUs, and every digital system that has ever existed.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Physical Switch** | A mechanical device (toggle switch, DIP switch) that connects a wire to either Vcc (HIGH / 1) or GND (LOW / 0). This is the simplest way a human provides a binary input to a circuit. |
| **Clock Signal** | A square wave that alternates between HIGH and LOW at a fixed rate. In this circuit, even a push button can serve as a manual clock — each press creates one rising edge that tells the flip-flop "capture now." See [[learning/notes/micro-context/clock-edges]]. |
| **D Flip-Flop (DFF)** | A circuit that stores one bit. On the rising [[learning/notes/micro-context/clock-edges|clock edge]], it captures whatever value is on its D input and holds it at Q until the next clock edge. The 74HC74 chip contains two independent DFFs. See [[learning/notes/quick-context/d-flip-flop]]. |
| **8-Bit Register** | Eight D flip-flops sharing a single clock line. On one clock edge, all eight capture their D inputs simultaneously — storing a full byte. The 74HC574 is a real chip that does exactly this. |
| **Output Enable (OE)** | A control pin on the 74HC574 that connects or disconnects the outputs from the rest of the circuit (tri-state). When OE is LOW, outputs are active. When HIGH, they go high-impedance — as if the chip isn't there. This lets multiple registers share one data bus. |

<details>
<summary><strong>How It Works</strong> — The bare minimal circuit</summary>

### Experiment 1: Storing a Single Bit

The simplest possible data storage circuit uses three components:

```
SINGLE-BIT STORAGE: Switch + Clock + D Flip-Flop
================================================================================

Parts: 1x toggle switch, 1x push button, 1x 74HC74 (dual D flip-flop), 1x LED

              Vcc (+5V)
               │
         ┌─────┤
         │     │
    TOGGLE     ├── 10kΩ ──┐
    SWITCH     │          │
         │     │          │          74HC74
         └──┬──┘          │    ┌──────────────────┐
            │              │    │                  │
            └── D input ──────►│ 1D          1Q ──├──── LED ──┬── 330Ω ── GND
                               │                  │           │
    PUSH      ┌── 10kΩ ──┐    │                  │           │
    BUTTON ───┤          ├───►│ 1CP (clock)      │           │
              │          │    │                  │
              └── GND    │    │ 1S̄D ── Vcc       │  (preset/clear
                              │ 1R̄D ── Vcc       │   tied inactive)
                              │                  │
                              │ Vcc (pin 14)     │
                              │ GND (pin 7)      │
                              └──────────────────┘

WHAT HAPPENS:
═════════════
  1. Flip switch UP (D = HIGH = 1)
  2. Press the button (rising clock edge)
  3. LED turns ON — the flip-flop captured the 1

  4. Flip switch DOWN (D = LOW = 0)
  5. LED is STILL ON — the flip-flop is HOLDING the old value
     (this is the key insight: memory!)

  6. Press the button again (another rising clock edge)
  7. NOW the LED turns OFF — it captured the new 0

  The flip-flop only "looks" at the switch when you press the button.
  Between presses, it ignores the switch completely.
```

This is the fundamental act of digital memory: **capture on command, hold until told otherwise.**

### Experiment 2: Storing a Full Byte (8 Bits)

Scale up to eight switches and a single register chip:

```
8-BIT REGISTER: 8 Switches + Clock + 74HC574
================================================================================

Parts: 8x DIP switches, 1x push button, 1x 74HC574 (octal D flip-flop),
       8x LEDs, 8x 330Ω resistors, 2x 10kΩ resistors, 0.1µF decoupling cap

                    Vcc (+5V)
                     │
              ┌──────┴──────────────────────────────────────┐
              │      │                                      │
              │    0.1µF (decoupling cap between Vcc & GND) │
              │      │                                      │
              │    GND                                      │
              │                                             │
    8 DIP SWITCHES          74HC574 (20-pin)            8 LEDs
    ┌─┬─┬─┬─┬─┬─┬─┬─┐    ┌──────────────────┐    ┌─┬─┬─┬─┬─┬─┬─┬─┐
    │0│1│2│3│4│5│6│7│    │                  │    │0│1│2│3│4│5│6│7│
    └┬┴┬┴┬┴┬┴┬┴┬┴┬┴┬┘    │ D0  ────────  Q0 │    └┬┴┬┴┬┴┬┴┬┴┬┴┬┴┬┘
     │ │ │ │ │ │ │ │──────►│ D1  ────────  Q1 │────►│ │ │ │ │ │ │ │
     │ │ │ │ │ │ │ │      │ D2  ────────  Q2 │    │ │ │ │ │ │ │ │
     │ │ │ │ │ │ │ │      │ D3  ────────  Q3 │    │ │ │ │ │ │ │ │
     └─┴─┴─┴─┴─┴─┴─┘      │ D4  ────────  Q4 │    └─┴─┴─┴─┴─┴─┴─┘
     (each switch to        │ D5  ────────  Q5 │    (each Q to LED
      Vcc via 10kΩ          │ D6  ────────  Q6 │     via 330Ω to GND)
      pullup, or to         │ D7  ────────  Q7 │
      GND when OFF)         │                  │
                            │ CP (clock) ◄─────┼──── PUSH BUTTON
                            │ OE̅ ── GND        │    (with 10kΩ pulldown)
                            │                  │
                            │ Vcc (pin 20)     │
                            │ GND (pin 10)     │
                            └──────────────────┘

STORING THE LETTER "A" (ASCII 65 = 0b01000001):
════════════════════════════════════════════════
  1. Set DIP switches to: OFF ON OFF OFF OFF OFF OFF ON
                          (0   1   0   0   0   0   0   1)

  2. Press the clock button — one rising edge

  3. LEDs show:  ○ ● ○ ○ ○ ○ ○ ●   ← "A" is now STORED

  4. Change switches to anything else — LEDs DON'T CHANGE
     The register is holding the byte until the next clock edge

  5. Set switches to 0b01000010 (66 = "B"), press clock again
     LEDs update to: ○ ● ○ ○ ○ ○ ● ○   ← now storing "B"
```

**What's inside the 74HC574?** Eight [[learning/notes/quick-context/d-flip-flop|D flip-flops]], all wired to the same clock pin. Each flip-flop is built from ~6 NAND gates, each NAND gate from 4 [[learning/notes/micro-context/mosfet|MOSFETs]]. So the chip contains roughly $8 \times 6 \times 4 = 192$ transistors — all working together to store 8 bits.

### Timing: Why the Clock Matters

The clock is what transforms a chaotic mess of switch bounces into clean, reliable data capture:

```
WHY THE CLOCK MAKES DIGITAL STORAGE WORK
================================================================================

Without a clock (transparent latch):
  Switch bounces:  ─┐┌─┐┌─┐┌──────────────────
                    └┘ └┘ └┘
  Output follows:  ─┐┌─┐┌─┐┌──────────────────
  every glitch!     └┘ └┘ └┘
  → Garbage. The output sees every bounce as a new value.


With a clock (edge-triggered flip-flop):
  Switch bounces:  ─┐┌─┐┌─┐┌──────────────────
                    └┘ └┘ └┘
  Clock:           ───────────────┘
                                  ┌────────────
                                  ↑
                             SAMPLE HERE
                             (rising edge, bouncing has stopped)
  Output:          ───────────────┘
                                  ┌──── stable ──
  → Clean. The flip-flop only looks at the switch at the rising
    clock edge, after the bouncing has settled.
```

This is why [[learning/notes/micro-context/clock-edges|clock edges]] are the heartbeat of digital systems. The [[learning/notes/quick-context/d-flip-flop|D flip-flop]] article explains the full gate-level mechanism (master-slave latch pair) that makes edge-triggering work.

</details>

<details>
<summary><strong>The Key Tension</strong> — Why this tiny circuit is the foundation of ALL computing</summary>

### The Leap from Storage to Computation

The switch-clock-register circuit stores data. That alone sounds trivial. But here's the insight that makes it the foundation of all computing:

**Computation = logic + memory + a clock to coordinate them.**

Combinational logic (AND, OR, NOT gates) can compute any function, but only in the present instant — it has no concept of "before" or "after." Add a register (flip-flops + clock), and suddenly you can:

1. **Store results** — compute something, capture the result, use it later
2. **Create sequences** — feed a register's output back through logic to its input, and each clock tick advances one step (this is a state machine)
3. **Count** — a register feeding through an incrementer is a counter
4. **Execute instructions** — a Program Counter (register + incrementer) fetches the next instruction each tick

```
FROM REGISTER TO COMPUTER — THE SAME PATTERN SCALES UP
================================================================================

YOUR BREADBOARD CIRCUIT:
  8 switches ──► 74HC574 register ──► 8 LEDs
                      ▲
                      │
                  clock button

A CPU's REGISTER FILE (same pattern, more registers):
  ALU output ──► Register R0 ──► ALU input
  ALU output ──► Register R1 ──► ALU input
  ...            Register R15
                      ▲
                      │
               180 MHz clock (instead of a button)

A CPU's PROGRAM COUNTER (register + feedback):
               ┌──────────────────────┐
               │                      │
               ▼                      │
  ┌────────────────┐    ┌──────────┐  │
  │ PC Register    │───►│   +1     │──┘
  │ (stores current│    │(increment│
  │  address)      │    │ er)      │
  └────────────────┘    └──────────┘
         │         ▲
         │     clock edge
         ▼
  Fetch instruction at this address from memory

RAM (array of registers + address decoder):
  Address ──► DMUX ──► selects which register to write
  Data ──► all registers' D inputs (but only selected one captures)
  Clock ──► all registers' clock (gated by DMUX selection)
  Read: MUX selects one register's Q output

  RAM8  = 8 registers + 3-bit address DMUX/MUX
  RAM64 = 8 × RAM8
  RAM4K = 8 × RAM512 ... and so on

ENTIRE COMPUTER (registers everywhere):
  ┌─────────────────────────────────────────────────┐
  │ CPU                                             │
  │  ┌──────────────┐    ┌────────────────────┐     │
  │  │ Instruction  │───►│ Control Unit        │     │
  │  │ Register     │    │ (decodes opcode,    │     │
  │  │ (a register!)│    │  generates control  │     │
  │  └──────────────┘    │  signals)           │     │
  │                      └────────────────────┘     │
  │  ┌──────────────┐    ┌────────────────────┐     │
  │  │ Program      │───►│ ALU                 │     │
  │  │ Counter      │    │ (combinational     │     │
  │  │ (a register!)│    │  logic — adds,     │     │
  │  └──────────────┘    │  compares, etc.)   │     │
  │                      └────────────────────┘     │
  │  ┌──────────────┐                               │
  │  │ Data         │  Every box labeled "register" │
  │  │ Registers    │  is your 74HC574 circuit,     │
  │  │ R0..R15      │  just running at GHz speed    │
  │  │ (registers!) │  instead of button presses.   │
  │  └──────────────┘                               │
  └─────────────────────────────────────────────────┘
         │
         ▼
  ┌──────────────────┐
  │ RAM              │
  │ (thousands of    │
  │  registers with  │  ← Same 74HC574 pattern, but
  │  address decoder)│    as SRAM cells (6T per bit)
  └──────────────────┘
```

### The Three Ingredients and Why Each Is Necessary

| Ingredient | What it provides | Without it |
|-----------|-----------------|------------|
| **Switch** (data input) | A way to set a bit to 0 or 1 | No way to get information into the system |
| **Clock** (timing) | A coordinated "capture now" signal | Chaos — outputs change whenever inputs change, race conditions everywhere |
| **Flip-flop / Register** (memory) | Captures and holds a value | No memory — computation is stateless, can't build sequences or programs |

Remove any one of these and digital computing is impossible. The [[learning/notes/quick-context/code-to-gates-and-bootstrapping|full compilation chain from code to gates]] bottoms out at exactly these three things: data flowing into [[learning/notes/quick-context/transistor|transistor]]-based logic, captured into registers at [[learning/notes/micro-context/clock-edges|clock edges]], fed back through more logic, captured again, billions of times per second.

### Is This *Really* the Foundation of ALL Computing?

Yes — with one caveat. The flip-flop-based register is the foundation of **synchronous digital computing**, which covers essentially all modern computers, phones, embedded controllers, GPUs, and FPGAs. There are alternative computing paradigms (analog computers, asynchronous logic, quantum computers, neuromorphic chips) that don't use clocked registers, but they represent a tiny fraction of computing today.

Every [[learning/notes/micro-context/stm32-microcontroller|STM32 microcontroller]] on the Pupper robot, every Intel CPU, every GPU rendering your screen — they all work by clocking data through registers billions of times per second. Your breadboard circuit with 8 switches and a 74HC574 is doing the *exact same thing*, just once per button press instead of 180 million times per second.

</details>

<details>
<summary><strong>Concrete Example</strong> — Building a 2-stage pipeline on a breadboard</summary>

### Beyond Storage: Register-to-Register Computation

The real power emerges when you chain registers with logic between them. Here's a breadboard circuit that adds two 4-bit numbers using registers — the same pattern a CPU uses for every instruction:

```
TWO-STAGE REGISTER PIPELINE (simplified to 4 bits)
================================================================================

Stage 1: INPUT REGISTERS (capture operands)

  4 switches ──► 74HC574A (register A) ──┐
                      ▲                   │
                  clock button            ├──► 74HC283 (4-bit adder)
                                          │        │
  4 switches ──► 74HC574B (register B) ──┘         │
                      ▲                            │
                  clock button                     │
                                                   ▼
Stage 2: RESULT REGISTER (capture sum)

                 74HC574C (result register) ──► 4 LEDs
                      ▲
                  clock button

HOW IT WORKS:
═════════════
  1. Set switch bank A to 0101 (5), press clock → register A holds 5
  2. Set switch bank B to 0011 (3), press clock → register B holds 3
  3. The 74HC283 adder (pure combinational logic, no clock needed)
     continuously outputs A + B = 1000 (8)
  4. Press clock for register C → result register captures 8
  5. LEDs show: ● ○ ○ ○ = 8

  Change the input switches — the adder output changes immediately,
  but register C still shows 8 until you press the clock again.
  THIS IS A PIPELINE STAGE — the same pattern the CPU uses to
  fetch, decode, and execute instructions.
```

### The Mental Model

```
EVERY CPU INSTRUCTION FOLLOWS THIS PATTERN
================================================================================

  ┌───────────┐    ┌───────────────────┐    ┌───────────┐
  │ Register  │───►│  Combinational    │───►│ Register  │
  │ (holds    │    │  Logic            │    │ (captures │
  │  inputs)  │    │  (computes in     │    │  result)  │
  └───────────┘    │   zero "time")    │    └───────────┘
       ▲           └───────────────────┘         ▲
       │                                         │
       └────── CLOCK EDGE ───────────────────────┘
       (both registers capture simultaneously)

  Your breadboard: switches → adder → LEDs (with registers)
  CPU instruction: register file → ALU → register file
  Same pattern. Different scale.
```

This is the [[learning/notes/quick-context/code-to-gates-and-bootstrapping|fetch-execute cycle]] at its most fundamental: read from registers, compute through logic, write to registers, repeat. The 74HC574 on your breadboard is the same functional unit as the register file inside an ARM Cortex-M4 — the [[learning/notes/micro-context/stm32-microcontroller|STM32]] just has more registers, a more complex ALU, and a [[learning/notes/micro-context/clock-source|180 MHz clock]] instead of a push button.

**The one thing most outsiders get wrong about this is...** thinking that "memory" and "computation" are separate concepts. In reality, computation IS memory updating over time. An ALU without registers is just a fancy truth table — it can't count, can't loop, can't follow a program. The register is what turns static logic into dynamic computation. The moment you wire a register's output back through an adder to its own input, you've created a counter — and from counters and state machines, you can build anything. The [[learning/notes/quick-context/physics-of-writing-data-to-memory|physics beneath it all]] is just cross-coupled transistors holding voltages stable — the same [[learning/notes/micro-context/sram|SRAM cell]] pattern, whether it's in a $2 breadboard chip or a billion-transistor CPU.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[learning/notes/quick-context/d-flip-flop]]** — Deep dive into the D flip-flop itself: how it's built from NAND gates (SR latch → gated latch → master-slave edge-triggered), the Nand2Tetris Python implementation, and how flip-flops compose into registers, shift registers, and counters.

- **[[learning/notes/quick-context/physics-of-writing-data-to-memory]]** — The physics beneath this circuit: how bits are physically stored as voltages in [[learning/notes/micro-context/sram|SRAM]] (cross-coupled transistors), charge on [[learning/notes/quick-context/capacitor|capacitors]] (DRAM), and trapped electrons on floating gates (flash). The 74HC574's internal flip-flops use the SRAM-like cross-coupled inverter pattern.

- **[[learning/notes/quick-context/code-to-gates-and-bootstrapping]]** — The upstream story: how source code compiles down through 7 layers of abstraction to the logic gates and registers described here. Layer 2 of that document shows "Registers = MUX + Data Flip-Flop" — exactly the 74HC574 pattern.

- **[[learning/notes/quick-context/transistor]]** — The physical switch that makes all of this possible. Each NAND gate inside the 74HC574 is built from 4 [[learning/notes/micro-context/mosfet|MOSFETs]]. The entire register chip is ~192 transistors implementing 8 one-bit memories.

- **[[learning/notes/quick-context/transistor-analog-to-digital]]** — How the imperfect analog behavior of real transistors is forced to behave as clean digital switches. The clock-and-register discipline is one of the key tricks: by only sampling at edges, the circuit ignores messy analog transitions.

- **[[learning/notes/micro-context/clock-edges]]** — The precise definition of rising/falling clock edges and why edge-triggered sampling is the foundation of synchronous digital design.

- **[[learning/notes/micro-context/clock-source]]** — Where clock signals come from in real systems: crystal oscillators, [[learning/notes/micro-context/ceramic-resonator|ceramic resonators]], [[learning/notes/quick-context/rc-oscillator|RC oscillators]]. The push button in the breadboard circuit is the simplest possible "clock source."

- **[[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens]]** — Historical context: the earliest computers used vacuum tubes as switches and magnetic core memory (tiny ferrite rings) as registers. The 74HC574 on your breadboard does what a room-sized relay rack did in 1945.

- **[[learning/notes/quick-context/bare-minimal-data-storage-circuit]]** — A variant of the same circuit where the digital switch is replaced by an *analog* source plus a [[learning/notes/quick-context/comparator|comparator]], and the manual button clock is replaced by a [[learning/notes/micro-context/crystal-oscillator|quartz crystal oscillator]]. Maps each block back to one line of the Nand2Tetris `BitRegisterChip`.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does the LED stay on after you flip the switch back to LOW (before pressing the clock button again)?
<details>
<summary>Answer</summary>
The D flip-flop is **edge-triggered** — it only samples its D input at the rising edge of the clock. Between clock edges, it ignores all changes on D and holds its stored value at Q. The LED reflects Q (the stored value), not D (the current switch position). This is the fundamental property that makes it memory: capture once, hold until told otherwise. See: How It Works (Experiment 1).
</details>

**Q2:** The 74HC574 has an Output Enable (OE) pin. What would happen if you connected OE to HIGH instead of GND?
<details>
<summary>Answer</summary>
The outputs would go to a **high-impedance (tri-state)** condition — electrically disconnected from the circuit. The LEDs would turn off, but the flip-flops inside are still holding their data. Pulling OE back to LOW would make the outputs reappear with the stored values intact. This feature lets multiple registers share a single data bus: only one register drives the bus at a time (OE = LOW), while others disconnect (OE = HIGH), preventing voltage conflicts. See: 5 Essential Terms (Output Enable).
</details>

**Q3:** How is the 74HC574 register on your breadboard related to the register file inside an ARM CPU?
<details>
<summary>Answer</summary>
They are functionally identical — both are arrays of D flip-flops that capture data on a clock edge. The ARM register file has 16 registers of 32 bits each (16 × 32 = 512 flip-flops), while the 74HC574 has 1 register of 8 bits (8 flip-flops). The ARM register file also has more complex addressing (a MUX selects which register to read/write) and runs at MHz-to-GHz [[learning/notes/micro-context/clock-speed|clock speeds]] instead of button presses. But the core mechanism — "capture D at clock edge, hold at Q" — is identical. See: The Key Tension (FROM REGISTER TO COMPUTER diagram).
</details>

**Q4:** If you removed the clock entirely and connected the switch directly to a latch (level-sensitive) instead of a flip-flop (edge-sensitive), what would go wrong?
<details>
<summary>Answer</summary>
A latch is **transparent** while its enable is HIGH — the output follows the input continuously. Every mechanical switch bounce (the contact physically bouncing open and closed for milliseconds) would appear at the output as rapid 0/1 toggling. Worse, in a multi-stage circuit, a change could ripple through multiple latches in a single clock period, causing race conditions where the output depends on which path is physically faster. The edge-triggered flip-flop solves both problems: it only samples at the clock transition instant, ignoring all input changes before and after. See: How It Works (Timing: Why the Clock Matters) and the [[learning/notes/quick-context/d-flip-flop|D Flip-Flop]] article's Level 2 vs. Level 3 explanation.
</details>

**Q5:** You claim that registers are the foundation of ALL computing. But neural networks and analog computers don't seem to use registers. Are they truly universal?
<details>
<summary>Answer</summary>
The claim is specifically about **synchronous digital computing**, which is how neural networks are actually *implemented* today. When you train a neural network on a GPU, the GPU is a synchronous digital chip with billions of registers clocking data through multiply-accumulate units. The "neurons" and "weights" exist as binary values in registers and SRAM, not as analog signals. True analog computers and neuromorphic chips (like Intel's Loihi) do exist and don't use clocked registers — they process information as continuous voltages or spike timings. But they represent a tiny fraction of computing. Quantum computers also don't use registers (they use qubits). The register-based model dominates because it's robust, scalable, and — thanks to [[learning/notes/quick-context/transistor-analog-to-digital|noise margins and regenerative logic]] — tolerates the messy analog reality of transistors. See: The Key Tension (Is This Really the Foundation of ALL Computing?).
</details>

</details>
