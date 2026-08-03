---
topic: The CPU Fetch-Execute Cycle — How a Machine Runs Instructions
created: 2026-06-07
---

# The CPU Fetch-Execute Cycle — How a Machine Runs Instructions

> **Related:** [[learning/notes/micro-context/clock-edges]] | [[learning/notes/micro-context/clock-source]] | [[learning/notes/micro-context/clock-speed-vs-temperature]] | [[learning/notes/micro-context/clock-speed-vs-temperature]] | [[learning/notes/quick-context/switches-to-registers-storing-data]]

> **TL;DR:** A CPU does one stupid thing, billions of times a second: read a number from memory, treat that number's bits as switch settings, let those switches steer data through an [[learning/notes/quick-context/code-to-gates-and-bootstrapping|ALU and registers]], save the result, then read the next number. That's it. "Running a program" is nothing more than this loop — fetch, decode, execute, write back, advance — repeated forever. The huge "aha" is that **code is not magic: it is a list of numbers sitting in [[learning/notes/quick-context/ram-addressing-decoder|RAM]], and each number's bits are physically wired to mux-select lines, ALU controls, and register load-enables**. "Decoding" an instruction is just routing those bits to the wires they were always destined for.

## The Core Problem

You've built [[learning/notes/quick-context/switches-to-registers-storing-data|registers]] (things that store bits) and an ALU (a thing that computes on bits). But a pile of registers and an ALU just sits there — it does nothing until someone, every clock tick, decides *which* registers to read, *what* the ALU should compute, and *where* to put the answer. The fetch-execute cycle is the mechanism that makes those decisions automatically, by reading them out of memory one number at a time. Without it, you have a calculator with no one pressing the buttons. With it, you have a computer that presses its own buttons forever — and the list of button-presses is your program.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Program Counter (PC)** | A [[learning/notes/quick-context/switches-to-registers-storing-data|register]] that holds the memory address of the next instruction. It's just a register wired to a `+1` incrementer with feedback — each clock tick it advances by one (or loads a jump target). |
| **Instruction** | A single number (16 bits on the Hack CPU, 32 on ARM) stored in memory. Its individual bit-fields *are* control signals — they directly drive mux selects, ALU operation bits, and register load-enables. An instruction is a list of switch settings. |
| **Fetch** | Use the PC as an address to read RAM, pulling the instruction number into the CPU so its bits are available as control wires. |
| **Decode** | There is no separate "decoder brain" — decode is just *wiring*. The instruction's bits are fed straight to the control inputs of the muxes, ALU, and registers. Routing, not interpreting. |
| **Execute / Write-back** | The ALU computes (steered by the instruction's bits), and on the [[learning/notes/micro-context/clock-edges|clock edge]] a register or RAM cell captures the result. Then the PC advances and the loop repeats. |

<details>
<summary><strong>How It Works</strong> — The essential mechanism</summary>

### One loop, forever

A CPU is a loop with five steps. One full pass = roughly one or a few clock ticks. Each [[learning/notes/micro-context/clock-edges|clock edge]] is the "do it now" pulse that lets registers capture their new values.

```
THE FETCH-EXECUTE CYCLE
================================================================================

      ┌───────────────────────────────────────────────────────────────┐
      │                                                               │
      ▼                                                               │
  ┌────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐  │
  │ FETCH  │───►│   DECODE     │───►│  EXECUTE     │───►│WRITE-BACK│  │
  │        │    │              │    │              │    │          │  │
  │ PC ──► │    │ instruction  │    │ ALU computes │    │ result   │  │
  │ address│    │ bits become  │    │ / RAM r/w /  │    │ captured │  │
  │ RAM,   │    │ control      │    │ register     │    │ in reg   │  │
  │ read   │    │ signals      │    │ feeds ALU    │    │ or RAM   │  │
  │ instr  │    │ (just wires) │    │              │    │ at edge  │  │
  └────────┘    └──────────────┘    └──────────────┘    └────┬─────┘  │
                                                             │        │
                                            ┌────────────────┘        │
                                            ▼                         │
                                     ┌──────────────┐                 │
                                     │ PC ADVANCES  │                 │
                                     │ +1, or load  │─────────────────┘
                                     │ jump target  │
                                     └──────────────┘

  Repeat ~10^9 times per second. That repetition IS "running a program."
```

### The Program Counter is just a register with feedback

You already know a [[learning/notes/quick-context/switches-to-registers-storing-data|register]] captures a value at the clock edge. Take that register, wire its output through a `+1` incrementer, and feed the incremented value back into its own input. Now every clock tick it counts up by one. Bolt on two muxes so you can *override* the count with a jump address (or with zero on reset), and you have a full Program Counter:

```
PROGRAM COUNTER = REGISTER + INCREMENTER + FEEDBACK + MUXES
================================================================================

  Three muxes pick the next value; one register captures it each clock edge.

  Inputs to choose from                            The chain
  ──────────────────────────────                   ──────────────────────────

  current value ────────────────────►┐  (sel=inc)
  current + 1 ──[ +1 ]──────────────►┴──► MUX 1 ──┐
                                                  │  (MUX 1 out)
  jump address ─────────────────────►┐  (sel=load)│
                       MUX 1 out ────┴──► MUX 2 ──┤
                                                  │  (MUX 2 out)
  0 (zero) ─────────────────────────►┐ (sel=reset)│
                       MUX 2 out ────┴──► MUX 3 ──┤
                                                  │  (MUX 3 out = next PC value)
   ┌──────────────┐                               │
   │  PC Register │◄──── clock edge ◄─────────────┘
   │  (holds addr)│──┐
   └──────────────┘  │
          ▲          │
          └──────────┘  PC Register's output is the "current value" at the top,
                        and is ALSO the address sent out to fetch the instruction.

  MUX 1: if inc=1   pick PC+1, else pick current value
  MUX 2: if load=1  pick jump address, else pass MUX 1's output
  MUX 3: if reset=1 pick 0,            else pass MUX 2's output
```

This is exactly the real Nand2Tetris implementation in
`learning/references/courses/python-nand-to-tetris-part-1/src/hardware/sequential_chips/program_counter_chip.py`
— three chained `mux16_gate` calls (pick incremented value if `inc`, else jump
input if `load`, else zero if `reset`) feeding one `register_chip`. The PC is
not special hardware; it is a register you already understand, plus a counter.

### The KEY INSIGHT: an instruction's bits ARE the control wires

This is the whole leap. Here is the Hack ALU's control interface — six bits named
`zx, nx, zy, ny, f, no`. From
`learning/references/courses/python-nand-to-tetris-part-1/src/hardware/combinational_chips/alu_chip.py`:

```
zx: if 1, force x to 0          ny: if 1, invert y
nx: if 1, invert x             f:  if 1, compute x+y ; if 0, compute x AND y
zy: if 1, force y to 0         no: if 1, invert the result
```

Look at how each of those bits is *used* inside the ALU — every one is just a
mux-select line choosing between "raw value" and "modified value":

```python
# from alu_chip.py (ALUChip.__call__) — the bit literally IS the sel line:
x = self.mux16_gate(x, Bits16.from_string("0000000000000000"), sel=zx)  # zx forces x=0
x = self.mux16_gate(x, self.not16_gate(x), sel=nx)                       # nx inverts x
y = self.mux16_gate(y, Bits16.from_string("0000000000000000"), sel=zy)  # zy forces y=0
y = self.mux16_gate(y, self.not16_gate(y), sel=ny)                       # ny inverts y
out = self.mux16_gate(self.and16_gate(x, y), self.add16_chip(x, y), sel=f)  # f picks +/AND
out = self.mux16_gate(out, self.not16_gate(out), sel=no)                 # no inverts result
```

There is no `if opcode == "ADD"` anywhere. The bit `f` is *physically the wire*
that decides whether the output mux passes the AND result or the ADD result.
"Decoding ADD" means: the bit that happened to be 1 in that position steers the
mux. That's it. **Decode = routing bits to the selects they're wired to.**

So now the chain closes:

```
WHY "CODE = INSTRUCTIONS" IS LITERALLY TRUE
================================================================================

  a program  =  a list of numbers in RAM
       ↓
  each number =  16 bits
       ↓
  those bits  =  control-wire settings (which mux path, which ALU op,
                 which register loads, whether to jump)
       ↓
  over time   =  a sequence of switch settings, one per clock tick
       ↓
  the result  =  the machine "does something" — i.e. runs the program

  Code is not instructions to a clever interpreter. Code is the
  configuration of the switches, frame by frame.
```

</details>

<details>
<summary><strong>The Key Tension</strong> — What practitioners argue about</summary>

### Do more in one instruction, or do simpler instructions faster?

Every CPU designer fights the same tradeoff: how much should a single instruction
*do*, and how literally should the fetch-execute loop run?

| Axis | Simple loop (RISC / Hack-like) | Complex loop (CISC / modern x86) |
|------|-------------------------------|-----------------------------------|
| Instruction does | One small thing (add, load, jump) | Possibly a lot (string copy, multiply-add) |
| Decode | Pure wiring — bits go straight to selects | Often a tiny program (microcode) that emits simpler micro-ops |
| Clock ticks/instr | ~1, predictable | Variable; some instructions take many cycles |
| Hardware cost | Small, easy to pipeline | Large decoder, but fewer instructions fetched |
| Who picks up slack | The compiler emits more instructions | The hardware does more per instruction |

The deeper tension is **transparency vs. throughput**. The pure "fetch one, do
one, advance" model (what the Hack CPU and this note describe) is beautifully
literal — but a real CPU that did *only* that, one instruction fully finished
before starting the next, would waste most of its silicon idling. So designers
break the loop into overlapping stages (pipelining), guess which way branches go
(speculation), and cache memory locally — all to keep more of the machine busy.
None of this changes the *meaning* of the loop; it only changes how many copies
of each stage run at once. The mental model "code is a list of switch settings
executed in order" stays exactly correct.

</details>

<details>
<summary><strong>Concrete Example</strong> — A tiny program traced tick-by-tick</summary>

### The program: compute 2 + 3 and store it

Here is a real Hack assembly program and the exact 16-bit numbers it becomes
(these encodings come straight from
[[learning/notes/quick-context/code-to-gates-and-bootstrapping|the compilation-chain note]]):

```
ADDRESS   ASSEMBLY      MACHINE CODE (the bits)   MEANING
─────────────────────────────────────────────────────────────────────────────
  0       @2            0000000000000010          A-instruction: load 2 into A
  1       D=A           1110110000010000          C-instruction: D ← A   (D=2)
  2       @3            0000000000000011          A-instruction: load 3 into A
  3       D=D+A         1110000010010000          C-instruction: D ← D+A  (D=5)
  4       @0            0000000000000000          A-instruction: load 0 into A
  5       M=D           1110001100001000          C-instruction: RAM[0] ← D (store 5)
```

The leading bit tells the two instruction types apart: `0...` is an
A-instruction (just "put this number in the A register"), `1...` is a
C-instruction (a compute instruction whose [[learning/notes/quick-context/ram-addressing-decoder|lower bits]] are the ALU controls
`a c1..c6 d1..d3 j1..j3`). In the real CPU,
`learning/references/courses/python-nand-to-tetris-part-1/src/hardware/computer/cpu.py`
does this split with literally one NOT gate:

```python
is_compute_instruction = op_code          # the top bit
is_address_instruction = self.not_gate(op_code)
```

### Tick by tick

Let `D`, `A` be CPU registers and `RAM[0]` a memory cell. Watch the PC drive
everything. Each row is one fetch-execute pass:

```
TRACE: running 2 + 3, store in RAM[0]
================================================================================
tick  PC  FETCHED INSTR        WHAT THE BITS STEER                  AFTER: D   A   RAM[0]
────────────────────────────────────────────────────────────────────────────────────
  0    0  0000000000000010     A-instr: route number → A register          ?   2   ?
                               PC +1 → 1
  1    1  1110110000010000     C-instr: ALU outputs A (zx..no pick         2   2   ?
                               "pass y=A"), load_d=1 → D captures it
                               PC +1 → 2
  2    2  0000000000000011     A-instr: route number → A register          2   3   ?
                               PC +1 → 3
  3    3  1110000010010000     C-instr: ALU bits f=1 → compute D+A,        5   3   ?
                               load_d=1 → D captures 5
                               PC +1 → 4
  4    4  0000000000000000     A-instr: route 0 → A (A is now the          5   0   ?
                               *address* 0)  PC +1 → 5
  5    5  1110001100001000     C-instr: ALU outputs D, write_m=1 →         5   0   5
                               RAM[A]=RAM[0] captures 5
                               PC +1 → 6
────────────────────────────────────────────────────────────────────────────────────
Result: RAM[0] = 5. The machine never "understood" addition — bit f=1 just
        steered the output mux to the adder. The program ran.
```

The dual role of the A register is worth pausing on: in tick 0 it holds an
*operand* (the number 2); in tick 4 it holds an *address* (where to store). Same
register, different bits routing it. In `cpu.py`, the mux that feeds the ALU's
`y` input is selected by [[learning/notes/quick-context/ram-addressing-decoder|exactly one]] bit of the instruction (`a_flag`): it picks
between "the A register's value" and "the value read from RAM." One instruction
bit, one mux — decode as routing, again.

### How fetch actually reads RAM

Fetching is just an addressed read. `memory.py`
(`learning/references/courses/python-nand-to-tetris-part-1/src/hardware/computer/memory.py`)
takes the address bits, uses a `dmux_gate` to pick which RAM bank to talk to, and
a `mux16_gate` to select that bank's output back out — the same address-decode
pattern from [[learning/notes/quick-context/ram-addressing-decoder|RAM addressing]].
The PC's value goes in as the address; the instruction number comes out. Nothing
more mysterious than looking up an array element.

**The one thing most outsiders get wrong about this is...** imagining a little
homunculus inside the CPU that *reads* each instruction, *understands* what "ADD"
means, and then *decides* to add. There is no reader and no understanding. The
instruction's bits are copper wires carrying 1s and 0s straight into the select
lines of multiplexers. Bit `f` doesn't *mean* "add" — bit `f` *is the wire* that,
when high, makes the output mux pass the adder's result. The CPU is a player
piano: the instruction is the punched roll, and the music is whatever the holes
happen to play.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[learning/notes/quick-context/switches-to-registers-storing-data]]** — Where the PC, instruction register, and data registers come from: 8 D flip-flops capturing at a clock edge. The fetch-execute loop is just "register → logic → register" running forever; this note builds that on a breadboard.

- **[[learning/notes/quick-context/ram-addressing-decoder]]** — How "PC points to an address in RAM" physically works: an [[learning/notes/quick-context/ram-addressing-decoder|address decoder]] ([[learning/notes/quick-context/ram-addressing-decoder|DMUX]] in, MUX out) selecting one cell among thousands. Fetch is one read from this structure. *(sibling note — may not exist yet.)*

- **[[learning/notes/quick-context/code-to-gates-and-bootstrapping]]** — The upstream chain: how source code becomes the exact 16-bit numbers traced above, including the Hack C-instruction bit-field layout and how the ALU is built from NAND gates.

- **[[learning/notes/micro-context/clock-edges]]** — The "do it now" pulse. Each fetch-execute step is gated by a clock edge so every register captures consistent, settled values at the same instant.

- **[[learning/notes/quick-context/d-flip-flop]]** — The 1-bit memory cell underneath every register, the PC, and the instruction register. Edge-triggering is why the loop advances in clean discrete steps.

- **[[learning/notes/quick-context/firmware]]** — What the program *is* on a real chip: instructions sitting in flash that the CPU fetch-executes straight from non-volatile memory at power-on.

- **[[learning/notes/quick-context/from-code-to-running-firmware]]** — How those instruction numbers get placed at real addresses (linker), written to the chip (flash), and reached ([[learning/notes/quick-context/firmware|reset vector]] → first fetch). Picks up where this loop starts.

- **Von Neumann architecture** — Why instructions and data share one memory (so the PC's "address" and an operand's "address" index the same RAM), and what the alternative (Harvard, separate instruction/data memory) buys you.

- **Pipelining / caches / microcode** — The same loop, scaled: overlapping stages, fast local copies of memory, and a tiny program inside the decoder. More machinery, identical meaning.

- **how-a-computer-works-index** — The hub: the full ladder from electricity up to running code. This note is rung L8, the rung where "registers + ALU + RAM" becomes "a running program."

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** What are the (up to) five things that happen in one pass of the fetch-execute cycle?
<details>
<summary>Answer</summary>
FETCH (use the PC as an address to read the instruction out of RAM), DECODE (the instruction's bits become control signals — really just wiring them to mux selects, ALU control bits, and register load-enables), EXECUTE (the ALU computes and/or RAM is read/written, steered by those bits), WRITE-BACK (a register or RAM cell captures the result at the clock edge), and PC ADVANCE (PC += 1, or load a jump target). See: How It Works (THE FETCH-EXECUTE CYCLE diagram).
</details>

**Q2:** The Program Counter sounds like special hardware. What is it actually made of?
<details>
<summary>Answer</summary>
Just a register plus a `+1` incrementer with the output fed back to the input, so it counts up one per clock tick. Two extra muxes let a jump address or zero (reset) override the count. That's the whole thing — see `program_counter_chip.py`, which is three chained `mux16_gate` calls feeding one register. See: How It Works (PROGRAM COUNTER diagram).
</details>

**Q3:** In the trace, the A register holds the *number 2* at tick 0 but an *address (0)* at tick 4. How can one register mean two different things?
<details>
<summary>Answer</summary>
Because "meaning" lives in how the *other* instructions route the register, not in the register itself. An A-instruction just dumps a number into A. A later C-instruction's bits decide whether A's value is fed to the ALU as an operand (via the `a_flag` mux) or used as the RAM address for a store (`write_m`). The same bits in A get steered to different destinations by different instructions. See: Concrete Example (dual role of the A register).
</details>

**Q4:** Someone says "the decoder reads the opcode, figures out it's an ADD, and tells the ALU to add." What's wrong with that description?
<details>
<summary>Answer</summary>
It smuggles in a thinking agent. Nothing "reads" or "figures out" anything. The instruction's bits are physically wired to the ALU's control inputs; in the Hack ALU, bit `f` *is* the select line of the output mux that chooses between the AND result and the ADD result. When `f` is 1, the adder's output is passed — not because anything decided to add, but because that's where the wire goes. Decode is routing, not interpreting. See: How It Works (the `sel=` excerpt from alu_chip.py) and Concrete Example (player-piano misconception).
</details>

**Q5:** If the entire model is "fetch one number, route its bits, advance," how does a modern multi-GHz CPU with pipelines and caches still fit it — and what would break if you took the loop too literally?
<details>
<summary>Answer</summary>
A modern CPU runs the *same* loop but overlaps it: while one instruction executes, the next is being fetched and another decoded (pipelining), with caches keeping hot memory close and microcode cracking complex instructions into simpler internal steps. The meaning is unchanged — it's still "a list of numbers whose bits steer the datapath, in program order." Taking the loop too literally — fully finishing each instruction before starting the next — is correct but wasteful: most of the chip would idle every cycle, which is exactly why the overlapping tricks exist. The abstraction "code = ordered switch settings" never breaks; only the number of stages running at once changes. See: The Key Tension (transparency vs. throughput) and Peripheral Knowledge (Pipelining/caches/microcode).
</details>

</details>
