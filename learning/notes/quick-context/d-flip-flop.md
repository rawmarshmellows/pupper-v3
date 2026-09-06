---
topic: D Flip-Flop — The Atom of Digital Memory
created: 2026-04-08
---

> **Related:** [[learning/notes/quick-context/transistor-analog-to-digital|Transistors - From Imperfect Analog Devices to Digital Switches]] | [[learning/notes/micro-context/sram|SRAM]] | [[learning/notes/quick-context/physics-of-writing-data-to-memory|Physics of Writing Data to Memory — How Bits Become Charges, Voltages, and Trapped Electrons]] | [[learning/notes/quick-context/how-source-code-is-stored|How Source Code Is Stored — Text, Encoding, and Bytes in Memory]] | [[learning/notes/quick-context/flip-chip|Flip-Chip Packaging]]

# D Flip-Flop — The Atom of Digital Memory


> **TL;DR:** A D flip-flop (DFF) is a circuit that stores exactly one bit. It has one data input (D), one output (Q), and a clock input. On each [[micro-context/clock-edges|clock edge]], it captures whatever value is on D and holds it at Q until the next clock edge — ignoring all input changes in between. This "sample once per tick" behavior is what makes digital systems work: it gives combinational logic a fixed window to settle before results are captured. Everything that stores state in a computer — registers, counters, shift registers, SRAM — is built from D flip-flops or their close relatives. In the [Nand2Tetris Python implementation](learning/references/courses/python-nand-to-tetris-part-1/src/hardware/sequential_chips/data_flip_flop_chip.py), each function call represents one clock tick: `out(t) = in(t-1)`.

## The Core Problem

Combinational logic (AND, OR, NOT gates) can compute any function, but it has no memory — the output changes the instant the inputs change. To build anything useful (a counter, a register, a CPU), you need circuits that can **remember** a value and only update it at controlled moments. The D flip-flop solves this: it samples its input once per [[learning/notes/micro-context/clock-edges|clock edge]] and holds the result stable, giving the rest of the circuit a reliable, unchanging value to work with until the next tick.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **D (Data) Input** | The single data input to the flip-flop. Whatever binary value (0 or 1) is present here at the moment of the clock edge gets captured. |
| **Q (Output)** | The stored value. After a clock edge, Q holds the value that D had at that edge. Q stays stable until the next clock edge, regardless of what D does in between. |
| **Clock (CLK)** | A continuous square wave that drives all flip-flops in a synchronous circuit. The flip-flop only "looks" at D during the clock edge (rising or falling, depending on design). Between edges, input changes are ignored. See [[micro-context/clock-edges]]. |
| **Latch vs. Flip-Flop** | A **latch** is level-sensitive: it passes input to output whenever the enable signal is HIGH (transparent). A **flip-flop** is edge-sensitive: it captures input only at the clock transition instant. Flip-flops are preferred in synchronous design because they avoid race conditions. |
| **Setup & Hold Time** | The data input must be stable for a minimum time *before* the clock edge (**setup time**, $t_{su}$) and *after* (**hold time**, $t_h$). Violating these causes **metastability** — the flip-flop enters an undefined state between 0 and 1. |

<details>
<summary><strong>How It Works</strong> — From cross-coupled gates to edge-triggered memory</summary>

### The Core Idea: Feedback Creates Memory

Memory in digital circuits comes from **feedback loops**. If you connect two gates so that each one's output feeds the other's input, the circuit has two stable states — it "remembers" which state it was pushed into. This is identical to the [[quick-context/physics-of-writing-data-to-memory|cross-coupled inverters in SRAM]].

### Level 1: The SR Latch (2 NAND gates — the simplest memory)

The most primitive memory element. Two NAND gates cross-coupled:

```
SR LATCH FROM 2 NAND GATES
================================================================================

  S̄ (active low) ───┐
                    ├── NAND ──┬──── Q
              ┌────►┘          │
              │                │
              │    ┌───────────┘
              │    │
              │    └──►┐
              │        ├── NAND ──┬──── Q̄
  R̄ (active low) ───┘          │
              ▲                │
              └────────────────┘

  Truth table (active-low inputs):
  ┌─────┬─────┬───────┬──────────────────────────┐
  │  S̄  │  R̄  │   Q   │  Meaning                 │
  ├─────┼─────┼───────┼──────────────────────────┤
  │  0  │  1  │   1   │  SET (Q = 1)             │
  │  1  │  0  │   0   │  RESET (Q = 0)           │
  │  1  │  1  │  Q_prev│  HOLD (no change)       │
  │  0  │  0  │  ??   │  FORBIDDEN (both outputs │
  │     │     │       │  go HIGH — undefined)     │
  └─────┴─────┴───────┴──────────────────────────┘

  The feedback is the key: each gate's output loops back to the
  other gate's input. Once pushed into a state (SET or RESET),
  the loop reinforces itself — the latch remembers.
```

**Problem:** Two separate inputs (S, R) and a forbidden state. We want one data input and controlled timing.

### Level 2: The Gated D Latch (4 NAND gates — adding a clock)

Add an **enable** signal (which in practice is the clock) and merge S/R into a single D input:

```
GATED D LATCH — ADDING CLOCK CONTROL
================================================================================

                   ┌────────────────────────────┐
                   │                            │
  D ──────┬───────►├── NAND ──► S̄ ──┐          │
          │        │                 │  SR      │
  EN ─────┤        │                 │  Latch   ├──► Q
  (clock) │        │                 │  (2 NAND │
          │  ┌─►NOT┤                 │   gates) │
          │  │     ├── NAND ──► R̄ ──┘          ├──► Q̄
          └──┘     │                            │
                   └────────────────────────────┘

  When EN = 1 ("transparent"):
    D = 1 → S̄ = 0, R̄ = 1 → Q = 1  (passes through)
    D = 0 → S̄ = 1, R̄ = 0 → Q = 0  (passes through)

  When EN = 0 ("opaque"):
    Both NAND outputs go HIGH → S̄ = R̄ = 1 → HOLD state
    Q keeps whatever value it had when EN went low.

  Total: 4 NAND gates + 1 NOT gate
```

**Problem:** While EN is HIGH, the output tracks the input continuously ("transparent"). Changes to D ripple through instantly. This causes race conditions in synchronous circuits where multiple latches feed each other.

### Level 3: The Edge-Triggered D Flip-Flop (Master-Slave, ~6 NAND gates)

The solution: chain two D latches with **opposite enable signals**. The first (master) is transparent when the clock is LOW; the second (slave) is transparent when the clock is HIGH. Data can never pass through both at the same time.

```
MASTER-SLAVE D FLIP-FLOP (POSITIVE EDGE-TRIGGERED)
================================================================================

  CLK ──────────┬───────────────────────────────────┐
                │                                   │
         ┌──────┤                            ┌──────┤
         │ NOT  │                            │      │
         v      │                            v      │
  ┌──────────────────┐              ┌──────────────────┐
  │   MASTER LATCH   │              │   SLAVE LATCH    │
  │                  │              │                  │
  │  D latch         │              │  D latch         │
  │  EN = NOT(CLK)   │   Q_master   │  EN = CLK        │
  │                  ├─────────────►│                  ├──── Q (output)
  D ────────────────►│              │                  │
  │                  │              │                  │
  └──────────────────┘              └──────────────────┘
    Transparent when                  Transparent when
    CLK = 0 (LOW)                     CLK = 1 (HIGH)

  TIMING — WHY ONLY THE EDGE MATTERS:

  CLK:    ─────┐     ┌─────┐     ┌─────
               └─────┘     └─────┘
                ↑           ↑
            rising edge  rising edge

  Phase 1 (CLK = 0):
    Master is TRANSPARENT → captures D
    Slave is OPAQUE → holds previous Q

  Phase 2 (CLK = 0→1, the rising edge):
    Master goes OPAQUE → locks in whatever D was
    Slave goes TRANSPARENT → passes master's value to Q

  Phase 3 (CLK = 1):
    Master is OPAQUE → D changes are ignored
    Slave is TRANSPARENT → but its input (master Q) is frozen

  Net effect: Q changes ONLY at the rising edge of CLK,
  capturing whatever D was just before the edge.

  SETUP TIME (tsu): D must be stable BEFORE the rising edge
  ──────────────────┼──────────────────
                 tsu↔│←th
  D:  ════════════X STABLE X════════════
                      ↑
  CLK:  ──────────────┘ (rising edge)
  HOLD TIME (th):  D must stay stable AFTER the rising edge
```

### The Clock: The Heartbeat of Synchronous Design

The clock is a square wave that coordinates every flip-flop in the circuit. Without it, logic gates would produce glitchy intermediate values as signals propagate at different speeds through different paths. The clock says: "everyone update NOW, then hold still until I tick again."

```
THE CLOCK'S ROLE IN A SYNCHRONOUS CIRCUIT
================================================================================

  Clock:  ───┐   ┌───┐   ┌───┐   ┌───┐   ┌───
             └───┘   └───┘   └───┘   └───┘
              ↑       ↑       ↑       ↑
              │       │       │       │
         ┌────┴───────┴───────┴───────┴────┐
         │  All flip-flops in the circuit   │
         │  sample their inputs at these    │
         │  edges SIMULTANEOUSLY            │
         └─────────────────────────────────┘

  Between edges:
  ┌─────────────────────────────────────────────────┐
  │  Combinational logic computes new values        │
  │  Signals propagate through gates at different   │
  │  speeds (some paths are longer than others)     │
  │  Intermediate values may be WRONG (glitches)    │
  │  BUT NOBODY IS LOOKING — all flip-flops are     │
  │  holding their previous values, ignoring inputs │
  └─────────────────────────────────────────────────┘

  At the next edge:
  ┌─────────────────────────────────────────────────┐
  │  All signals have settled (if clock is slow     │
  │  enough — this constraint sets max clock speed) │
  │  Every flip-flop captures its D input           │
  │  New stable values propagate into the next      │
  │  round of combinational logic                   │
  └─────────────────────────────────────────────────┘

  Clock period must be ≥ longest combinational delay + tsu
  This is what determines the maximum clock frequency.
```

### How Flip-Flops Compose Into Larger Structures

A single DFF stores 1 bit. Everything larger is just arrays or chains of DFFs:

```
BUILDING BLOCKS FROM D FLIP-FLOPS
================================================================================

  1 BIT REGISTER (DFF + MUX):
     Store or hold. MUX selects: load new value, or feed back
     the current output (hold). This is exactly the Nand2Tetris
     BitRegisterChip.

     load ────────► MUX ──► DFF ──┬──► Q
                    ▲  ▲         │
     D (new) ──────┘  │         │
                      └─────────┘  (feedback: hold current value)

  N-BIT REGISTER (N parallel DFFs):
     16 BitRegisterChips side by side, all sharing the same
     clock and load signal. Stores a 16-bit word.

  SHIFT REGISTER (N chained DFFs):
     Q of each DFF feeds D of the next. On each clock tick,
     every bit moves one position. This is the core of the
     UART receive path — see [[quick-context/uart]].

     serial  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
     input──►│D   Q├─►│D   Q├─►│D   Q├─►│D   Q├──►
             │ FF3 │  │ FF2 │  │ FF1 │  │ FF0 │
             └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘
                │        │        │        │
                CLK      CLK      CLK      CLK
                (all share the same clock)

  COUNTER (DFFs with adder feedback):
     Output feeds back through an incrementer to the input.
     Each tick: Q(t+1) = Q(t) + 1.
     This is the Nand2Tetris ProgramCounterChip.

  RAM (array of registers + address decoder):
     DMUX routes the write signal to one register;
     MUX selects one register's output for reading.
     8 registers → RAM8. 8×RAM8 → RAM64. And so on.
```

</details>

<details>
<summary><strong>The Key Tension</strong> — Speed vs. reliability (the clock constraint)</summary>

The fundamental tension in synchronous design is **[[learning/notes/micro-context/clock-speed|clock speed]] vs. correctness**.

Every combinational logic path between two flip-flops has a **propagation delay** — the time for a signal to ripple through all the gates. The clock period must be long enough for the slowest path (the "critical path") to settle before the next clock edge samples the result. Too fast → signals haven't settled → flip-flops capture wrong values → the circuit produces garbage.

```
THE CRITICAL PATH CONSTRAINT
================================================================================

  DFF_A ──► [combinational logic] ──► DFF_B
         │                          │
         │◄──── propagation delay ──►│
         │      (longest path)       │
         │                           │
         │◄── tsu ──┤                │
  Clock period ≥ propagation delay + setup time + clock skew

  If you violate this:
    DFF_B samples while signals are still changing
    → captures a metastable or incorrect value
    → error propagates through the entire circuit
```

| Choice | Faster Clock | Slower Clock |
|--------|-------------|-------------|
| **Performance** | More operations/sec | Fewer operations/sec |
| **Power** | Higher (more switching/sec) | Lower |
| **Reliability** | Risk of timing violations | Safe margins |
| **Design effort** | Must optimize critical path | More relaxed |

This is why CPU clock speeds plateaued around 4-5 GHz (~2005). The causes are intertwined: higher frequency means shorter clock periods, leaving less time for signals to settle (timing), *and* power consumption grows super-linearly with frequency ($P \propto fCV^2$), making thermal dissipation unsustainable (Dennard scaling breakdown). The solution was going multi-core — more flip-flops running in parallel at a manageable speed — rather than faster clocks.

**Metastability** — the worst failure mode: if setup/hold times are violated, the flip-flop can enter a state that is neither 0 nor 1, hovering at a [[learning/notes/quick-context/voltage|voltage]] in the "forbidden zone" between logic levels. This metastable state eventually resolves to 0 or 1, but it takes an unpredictable amount of time. This is a real problem at clock domain boundaries (e.g., data crossing from a [[quick-context/uart|UART's]] baud rate clock to the CPU's system clock), and is typically solved with synchronizer chains (2-3 flip-flops in series).

</details>

<details>
<summary><strong>Concrete Example</strong> — The Nand2Tetris DFF in Python</summary>

Your [Nand2Tetris implementation](learning/references/courses/python-nand-to-tetris-part-1/src/hardware/sequential_chips/data_flip_flop_chip.py) models the DFF beautifully. The key insight: **each function call = one clock tick**.

### The DFF: `out(t) = in(t-1)`

```python
# From: learning/references/courses/python-nand-to-tetris-part-1/
#       src/hardware/sequential_chips/data_flip_flop_chip.py

class DataFlipFlopChip:
    def __init__(self):
        self.to_return = Bit(0)       # Q output (what we return THIS tick)
        self.current_value = Bit(0)   # what was input LAST tick
        self.is_first_call = True

    def __call__(self, in_bit: Bit) -> Bit:
        if self.is_first_call:
            self.current_value = in_bit   # store input
            self.is_first_call = False
            return self.to_return         # return initial 0

        self.to_return = self.current_value   # output = PREVIOUS input
        self.current_value = in_bit           # store CURRENT input for next tick
        return self.to_return
```

The clock is **implicit** — in real hardware it's an explicit electrical signal, but in this simulation each `__call__` represents one rising clock edge. The behavior is exactly `out(t) = in(t-1)`: what you get out is what you put in *last tick*.

### The Bit Register: DFF + MUX = Loadable Storage

```python
# From: learning/references/courses/python-nand-to-tetris-part-1/
#       src/hardware/sequential_chips/bit_register_chip.py

class BitRegisterChip:
    def __init__(self):
        self.data_flip_flop_chip = DataFlipFlopChip()
        self.mux_gate = MuxGate()

    def __call__(self, in_bit: Bit, load: Bit) -> Bit:
        previous = self.to_return                         # DFF's current output
        mux_output = self.mux_gate(previous, in_bit, load)  # load=0: hold, load=1: new
        return self.data_flip_flop_chip(mux_output)       # feed MUX result to DFF
```

When `load=0`: the MUX selects `previous` (the DFF's own output) and feeds it back as input → the DFF stores the same value again → **hold**.

When `load=1`: the MUX selects `in_bit` (new data) → the DFF stores the new value → **write**.

This is the fundamental building block. The [16-bit RegisterChip](learning/references/courses/python-nand-to-tetris-part-1/src/hardware/sequential_chips/register_chip.py) is just 16 of these in parallel, and the RAM chips are arrays of registers with address decoding.

### Tracing Three Clock Ticks

```
TRACING THE BIT REGISTER — 3 TICKS
================================================================================

  Tick 1: load=1, in_bit=1
    MUX(previous=0, in_bit=1, load=1) → selects in_bit → 1
    DFF input = 1, DFF output = 0 (returns PREVIOUS input)
    → Q = 0 (the "1" is captured but won't appear until next tick)

  Tick 2: load=0, in_bit=X (don't care)
    MUX(previous=1, in_bit=X, load=0) → selects previous → 1
    DFF input = 1, DFF output = 1 (returns what was input last tick)
    → Q = 1 ← the stored value appears!

  Tick 3: load=0, in_bit=X
    MUX(previous=1, in_bit=X, load=0) → selects previous → 1
    DFF input = 1, DFF output = 1
    → Q = 1 ← still holding, no change
```

### Why the DFF Is Treated as a Primitive in Nand2Tetris

In the course, the DFF is given as a built-in primitive (not built from NAND gates). This is a deliberate abstraction: in real hardware, a DFF requires ~6 NAND gates (master-slave configuration), but its behavior is simple enough to treat as an atom. The course focuses on what you can *build with* flip-flops (registers, RAM, CPU) rather than how flip-flops are built *from* gates. See "How It Works" above for the full gate-level construction.

**The one thing most outsiders get wrong about this is...** thinking the clock is just "there" as some abstract timing concept. The clock is a **physical electrical signal** — a square wave generated by a [[micro-context/crystal-oscillator|crystal oscillator]] that is routed as a wire to every single flip-flop in the chip. On a modern CPU with billions of flip-flops, distributing this clock signal so that it arrives at all flip-flops within picoseconds of each other ("clock skew") is one of the hardest physical design challenges. Clock distribution networks consume ~30-40% of a chip's total power. In the Nand2Tetris simulation, `__call__` hides all of this — but in the real [[micro-context/stm32-microcontroller|STM32]], there's a [[micro-context/clock-source|clock tree]] that physically routes the oscillator signal to every peripheral.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **How a Computer Works — Index-Spine** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/code-to-gates-and-bootstrapping]]** — The full compilation chain from code to logic gates. Layer 2 shows how registers are built from "MUX + Data Flip-Flop" — the exact pattern in the Nand2Tetris BitRegisterChip.

- **[[quick-context/uart]]** — The [[learning/notes/quick-context/uart|UART]]'s receive shift register is a chain of 8 D flip-flops where each Q feeds the next D. On each baud clock tick, bits shift through the chain. The flip-flop is the hardware atom that makes serial-to-parallel conversion possible.

- **[[quick-context/physics-of-writing-data-to-memory]]** — The cross-coupled inverters in [[learning/notes/micro-context/sram|SRAM]] are the continuous-time analog of a flip-flop's feedback loop. Both use feedback to create bistable states, but SRAM cells are optimized for density (6 transistors) while flip-flops are optimized for speed and clean edge-triggered behavior.

- **[[quick-context/transistor-analog-to-digital]]** — How imperfect analog transistors are forced to behave as digital switches. The flip-flop's edge-triggered discipline is one of the key engineering tricks: by only sampling at [[learning/notes/micro-context/clock-edges|clock edges]], the circuit ignores the messy analog transitions between them.

- **[[micro-context/clock-edges]]** — The precise definition of rising and falling clock edges, and why edge-triggered sampling is the foundation of synchronous digital design.

- **[[micro-context/clock-source]]** — Where the clock signal comes from: crystal oscillators, ceramic resonators, internal RC oscillators. The clock tree routes this signal to every flip-flop in the system.

- **[[micro-context/crystal-oscillator]]** — The physical component that generates the precise square wave driving all flip-flops. Crystal accuracy (~50 ppm) matters for UART baud rate generation.

- **[[quick-context/switches-to-registers-storing-data]]** — A hands-on breadboard circuit showing how a physical switch, clock button, and D flip-flop chip (74HC74/74HC574) store data — and how this minimal setup scales to build every register, RAM, and CPU.

- **[[quick-context/bare-minimal-data-storage-circuit]]** — Adds the analog front-end to the picture: how a power supply, [[micro-context/crystal-oscillator|quartz crystal]], [[learning/notes/quick-context/comparator|comparator]], and the register's `in_bit`/`load` signals fit together physically, and how each block maps to a line in the Nand2Tetris `BitRegisterChip`.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What's the fundamental difference between a latch and a flip-flop?
<details>
<summary>Answer</summary>
A **latch** is **level-sensitive** — it passes input to output whenever the enable signal is HIGH (transparent mode). A **flip-flop** is **edge-sensitive** — it captures input only at the clock transition (rising or falling edge) and holds it stable the rest of the time. Flip-flops are preferred because level-sensitive latches can cause race conditions when multiple latches feed each other in a loop — a change can ripple through multiple latches in a single clock period. See: Level 2 (Gated D Latch) vs. Level 3 (Edge-Triggered) in How It Works.
</details>

**Q2:** In the Nand2Tetris `DataFlipFlopChip`, why does the first call return 0 instead of the input value?
<details>
<summary>Answer</summary>
Because the DFF's contract is `out(t) = in(t-1)` — the output at time t equals the input at time t-1. On the very first tick (t=0), there is no t-1 input, so the output is the initial value (0). The input provided at t=0 will appear at the output on t=1. This one-tick delay is the entire point of the flip-flop — it creates a boundary between "now" and "one clock ago," which is what makes sequential logic possible. See: Concrete Example.
</details>

**Q3:** Why does the `BitRegisterChip` feed the DFF's *own output* back through a MUX?
<details>
<summary>Answer</summary>
To implement **hold** behavior. A bare DFF always captures whatever is on D at each clock edge — it can't "choose" to keep its current value. The MUX adds that choice: when `load=0`, the MUX routes the DFF's current output back to its input, so the DFF re-stores the same value. When `load=1`, the MUX routes the new input data instead. Without the feedback MUX, you'd need to continuously drive the correct value on D every tick, which is impractical when you want to "set and forget" a register value. See: Concrete Example (BitRegisterChip).
</details>

**Q4:** If flip-flops only sample at clock edges, what happens if you chain the output of one flip-flop into the input of another?
<details>
<summary>Answer</summary>
This is exactly how **shift registers** and **pipelines** work. On each clock edge, flip-flop B captures the value that flip-flop A had been *holding* (not the value A is about to capture). This works because the propagation delay through a flip-flop is much shorter than the clock period — by the time A's output changes to its new value, B has already captured A's old value. The one-tick delay per flip-flop is what makes pipelining possible: data moves one stage per clock tick, like items on a conveyor belt. The [[quick-context/uart|UART shift register]] uses exactly this pattern — 8 DFFs chained together, each bit shifting one position per baud clock tick.
</details>

**Q5:** The clock is described as arriving at all flip-flops "simultaneously," but signals travel at finite speed. What happens when the clock arrives at different flip-flops at slightly different times?
<details>
<summary>Answer</summary>
This is **clock skew** — the difference in arrival time of the clock signal at different flip-flops. If flip-flop A's clock edge arrives 100 ps before flip-flop B's, there's a 100 ps window where A has updated but B hasn't yet — B might see A's *new* value instead of the old one, violating the pipeline assumption. The critical path timing constraint becomes: clock period ≥ propagation delay + setup time + **clock skew**. On modern chips, clock distribution networks (H-trees, clock meshes) keep skew under ~50 ps. This is one of the hardest physical design challenges — clock buffers and balanced routing consume 30-40% of a chip's power. The Nand2Tetris simulation avoids this entirely because `__call__` provides perfectly synchronous ticks.
</details>

</details>
