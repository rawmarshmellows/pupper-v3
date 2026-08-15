---
topic: RAM — Addressing an Array of Registers
created: 2026-06-07
---

# RAM — Addressing an Array of Registers

> **Related:** [[learning/notes/quick-context/switches-to-registers-storing-data]] | [[learning/notes/quick-context/d-flip-flop]] | [[learning/notes/quick-context/cpu-fetch-execute-cycle]] | 

> **TL;DR:** A [[learning/notes/quick-context/switches-to-registers-storing-data|register]] stores exactly one word. RAM (Random-Access Memory) is just an **array of those registers** plus a way to pick **exactly one of them by a number — its address**. Two switching circuits do the picking: a **DMUX** routes the "write now" signal to the one register you want to change, and a **MUX** selects the one register's value you want to read. With $n$ address bits you can name $2^n$ words, and you build big RAM by stacking eight small RAMs and gluing on three more address bits — over and over.

## The Core Problem

A single register can hold one word, but a useful program needs thousands or millions of words and must be able to grab **any one of them at random**, instantly, by name. If you wired every register's output together you'd get a [[learning/notes/micro-context/short-circuit|short circuit]], and if you pulsed every register's clock at once you'd overwrite all of them. RAM solves both: an **address decoder** guarantees that on any given operation, exactly **one** register is written and exactly **one** register is read — chosen by a plain binary number.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Word** | The fixed-size chunk RAM stores and returns per address — one register's worth of bits. In the Nand-to-Tetris machine modeled here a word is 16 bits (`Bits16`); on a PC it is usually 8, 32, or 64. |
| **Address** | A binary number that names one word in the array. With $n$ address bits there are $2^n$ distinct addresses, so an $n$-bit address selects one of $2^n$ words. |
| **DMUX (demultiplexer)** | A 1-to-many router on the **write path**. It takes the single `load` ("write now") signal and forwards it to **exactly one** register's load pin, chosen by the address. All other registers get `load = 0` and ignore the clock edge. |
| **MUX (multiplexer)** | A many-to-1 selector on the **read path**. Every register is always outputting its stored value; the MUX picks **exactly one** of those outputs to pass through, chosen by the address. |
| **Load / clock-enable** | The gate that decides whether a register captures new data on the next [[learning/notes/micro-context/clock-edges|clock edge]]. If `load = 1` the register overwrites itself at the edge; if `load = 0` it holds. The DMUX sets exactly one register's `load` to 1. |

<details>
<summary><strong>How It Works</strong> — The essential mechanism</summary>

### One register, then many

Start from one register. It has three things going in — the data word `in`, a `load` bit (write or hold), and a clock — and one thing coming out: the stored word `out`. (See [[learning/notes/quick-context/switches-to-registers-storing-data|switches to registers]] for how that one register is built from [[learning/notes/quick-context/d-flip-flop|D flip-flops]].)

```
            in[16] ─────────────►┌───────────┐
                                  │  REGISTER │────► out[16]
   load ───────────────────────► │  (1 word) │
   clock ──────────────────────► └───────────┘
```

Now line up eight of them. The data word `in` is broadcast to **all eight** registers at once — that part is just parallel wires, no decision. The clever bit is the two circuits that turn "all eight" into "exactly one".

```
RAM8 = 8 registers + a 3-bit address + a DMUX (write) + a MUX (read)
================================================================================

  in[16] (broadcast to ALL) ──┬────┬────┬────┬────┬────┬────┬────┬
                              ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼
                            ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐
                            │ R0││ R1││ R2││ R3││ R4││ R5││ R6││ R7│  ← the array
                            └─┬─┘└─┬─┘└─┬─┘└─┬─┘└─┬─┘└─┬─┘└─┬─┘└─┬─┘
   WRITE PATH:                │    │    │    │    │    │    │    │
   load ──►┌──────┐           l0   l1   l2   l3   l4   l5   l6   l7
           │ DMUX │──► (one-hot: exactly ONE of l0..l7 = 1, the rest = 0)
           └──────┘
              ▲
              └── address[3] picks which register's load goes high

   READ PATH:                 │    │    │    │    │    │    │    │
                              ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼
                            ┌─────────────────────────────────────┐
                            │                 MUX                 │──► out[16]
                            └─────────────────────────────────────┘
                              ▲
                              └── address[3] picks which output passes through
```

### Write path vs read path — two independent jobs

The two paths use the **same address** but do opposite-shaped jobs:

```
WRITE (1 → many):   load=1 enters → DMUX fans it out → only addressed reg's
                    load becomes 1 → at the next clock edge that ONE register
                    captures `in`; the other seven hold (their load is 0).

READ (many → 1):    all 8 registers continuously output their stored words →
                    MUX funnels them down → only the addressed reg's word
                    leaves as `out`. (Reading is combinational — no clock needed.)
```

The asymmetry is the whole trick. Writing must be **gated by the clock** so data is captured at a precise, glitch-free instant — that is the `load`/clock-enable gating. Reading is just selection; the value is already sitting there, so the MUX can present it immediately.

### Why the DMUX prevents clobbering

Every register shares the same clock. If you simply let all of them capture on every edge, one write would overwrite all eight. The DMUX is what makes the array behave like memory instead of a broadcast: it converts a single `load` into a **one-hot** vector (exactly one wire high) so the clock edge only "lands" on the addressed register.

```
address = 5 (binary 101)        load = 1
                │                   │
                ▼                   ▼
        ┌───────────────── DMUX ───────────────┐
        l0 l1 l2 l3 l4 l5 l6 l7
         0  0  0  0  0  1  0  0   ← only R5 is armed; clock edge writes R5 only
```

</details>

<details>
<summary><strong>The Key Tension</strong> — What practitioners argue about</summary>

The central design tension in real RAM is **speed vs. density vs. cost**, and it shows up as the SRAM-vs-DRAM split.

The Nand-to-Tetris model in this note treats each cell as a full register (a bundle of flip-flops). That is essentially **SRAM**: fast, holds its value as long as power is on, but expensive because every bit costs roughly six transistors. Real **DRAM** stores each bit as a tiny charge on a [[learning/notes/quick-context/capacitor|capacitor]] — one [[learning/notes/quick-context/transistor|transistor]] plus one capacitor — so it is far denser and cheaper per bit, but the charge leaks and must be **refreshed** thousands of times per second, and reads are destructive (you have to write the value back). DRAM is also slower to access.

| | SRAM (register-like) | DRAM (capacitor) |
|---|---|---|
| Cell | ~6 transistors (flip-flop) | 1 transistor + 1 capacitor |
| Speed | Fastest (<1 ns) | Slower |
| Density / cost | Low density, expensive | High density, cheap |
| Needs refresh? | No (static while powered) | Yes (charge leaks) |
| Typical use | CPU registers, cache | Main memory (the GBs of "RAM") |

So a machine uses **both**: a little fast SRAM right next to the CPU (registers and cache) and a lot of cheap DRAM as main memory. See [[learning/notes/micro-context/sram|SRAM]] for the cross-coupled-inverter cell and [[learning/notes/quick-context/physics-of-writing-data-to-memory|the physics of writing data to memory]] for why the capacitor approach leaks. The decoder/MUX/DMUX addressing logic in this note is **identical** for both — it is independent of how each cell physically stores its bit.

The other recurring argument is **decoder cost as $n$ grows**. A flat decoder for $2^n$ words needs a fan-out that grows exponentially, which is why real chips (and the recursive build below) decompose the address into stages — a few bits per level — rather than one giant decoder.

</details>

<details>
<summary><strong>Concrete Example</strong> — The recursive build, as real runnable code</summary>

This repository contains a working Python model of exactly this hierarchy in
`learning/references/courses/python-nand-to-tetris-part-1/src/hardware/sequential_chips/`.
The pattern is **recursive**: each bigger RAM is *eight copies of the next smaller RAM* with **three more address bits** layered on top — the top 3 bits pick which sub-RAM, the remaining bits are handed down inside it.

### The scaling table

```
Chip      Words   Built from        Address bits   New bits added
---------------------------------------------------------------------------
RAM8         8    8 × Register        3 (2^3 = 8)   3  (top decoder)
RAM64       64    8 × RAM8            6 (2^6 = 64)  3  (3 here + 3 inside)
RAM512     512    8 × RAM64           9 (2^9 = 512) 3
RAM4K     4096    8 × RAM512         12 (2^12)      3
RAM16K   16384    4 × RAM4K          14 (2^14)      2  (uses a 4-way decoder)
```

Each level: the **top bits** drive a DMUX (route the write) and a MUX (route the read) across the eight sub-units; the **lower bits** ride along into whichever sub-unit was selected. Note the last step, `ram16K_chip.py`, breaks the "8×" rhythm: $16384 / 4096 = 4$, so it stacks only **four** RAM4Ks and uses a **4-way** DMUX/MUX with a **2-bit** top field instead of 3.

### RAM8: the base case, in real code

From `ram8_chip.py` — eight `RegisterChip`s, one `Dmux8WayGate`, one `Mux8Way16Gate`:

```python
class Ram8Chip:
    def __init__(self):
        self.register_a = RegisterChip()   # the array:
        self.register_b = RegisterChip()   #   eight registers,
        self.register_c = RegisterChip()   #   each holds one 16-bit word
        self.register_d = RegisterChip()
        self.register_e = RegisterChip()
        self.register_f = RegisterChip()
        self.register_g = RegisterChip()
        self.register_h = RegisterChip()
        self.dmux8way_gate = Dmux8WayGate()   # write-path router
        self.mux8way16_gate = Mux8Way16Gate() # read-path selector

    def __call__(self, in_bits: Bits16, load: Bit, address: Bits3) -> Bits16:
        # WRITE PATH: split the single `load` into 8 one-hot enables.
        # Only the addressed register gets load=1; the rest get 0.
        a, b, c, d, e, f, g, h = self.dmux8way_gate(load, address)
        # READ PATH: every register is fed the SAME in_bits (broadcast) but its
        # own load enable, then the MUX selects ONE output by the same address.
        return self.mux8way16_gate(
            self.register_a(in_bits, a),   # in_bits broadcast to all 8;
            self.register_b(in_bits, b),   # `a..h` are the gated load bits
            self.register_c(in_bits, c),
            self.register_d(in_bits, d),
            self.register_e(in_bits, e),
            self.register_f(in_bits, f),
            self.register_g(in_bits, g),
            self.register_h(in_bits, h),
            address,                        # MUX picks which output to return
        )
```

Read that carefully — it *is* the diagram above, line for line:
`dmux8way_gate(load, address)` is the write router that arms one register, and
`mux8way16_gate(..., address)` is the read selector that returns one word.

The DMUX itself (`dmux8way_gate.py`) is just a tree of 1-to-2 demuxes that turns 3 select bits into 8 one-hot lines:

```python
def dmux8way_gate(a, sel0, sel1, sel2):
    x0, x1 = dmux_gate(a, sel0)        # split on bit 0
    x2, x3 = dmux_gate(x0, sel1)       # split on bit 1
    x4, x5 = dmux_gate(x1, sel1)
    a, b = dmux_gate(x2, sel2)         # split on bit 2 -> 8 outputs
    c, d = dmux_gate(x3, sel2)
    e, f = dmux_gate(x4, sel2)
    g, h = dmux_gate(x5, sel2)
    return a, b, c, d, e, f, g, h      # exactly one of these is 1
```

### RAM64: the recursion, in real code

From `ram64_chip.py` — now the eight cells are themselves `Ram8Chip`s, and the 6-bit address is split: top 3 bits (`address[:3]`) pick the sub-RAM, bottom 3 bits (`address[3:]`) are passed down:

```python
def __call__(self, in_bits: Bits16, load: Bit, address: Bits6) -> Bits16:
    a, b, c, d, e, f, g, h = self.dmux8way_gate(load, address[:3])  # top 3 bits
    return self.mux8way16_gate(
        self.ram8_a(in_bits, a, address[3:]),   # bottom 3 bits ride along
        self.ram8_b(in_bits, b, address[3:]),
        self.ram8_c(in_bits, c, address[3:]),
        self.ram8_d(in_bits, d, address[3:]),
        self.ram8_e(in_bits, e, address[3:]),
        self.ram8_f(in_bits, f, address[3:]),
        self.ram8_g(in_bits, g, address[3:]),
        self.ram8_h(in_bits, h, address[3:]),
        address[:3],                            # MUX selects sub-RAM by top 3
    )
```

`ram512_chip.py` and `ram4K_chip.py` are the **identical** pattern with `Ram64Chip` and `Ram512Chip` as the cells and 9- and 12-bit addresses. `ram16K_chip.py` is the same idea but with `Dmux4WayGate`/`Mux4Way16Gate` and `address[:2]` because it only needs four RAM4Ks.

**The one thing most outsiders get wrong about this is...** thinking RAM "searches" for the address, like flipping through a notebook to find the right page — so they assume bigger memory is slower to find a word in. It does not search at all. The address is fed straight into the decoder, which is pure combinational logic, and the selected register is reached in essentially constant time no matter how big the array is. That is the whole meaning of **"random access"**: every address costs the same, in any order. (The recursive tree adds a few gate delays per level, but it is still constant for a fixed size — not a scan.)

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[learning/notes/quick-context/switches-to-registers-storing-data]]** — The rung below this one: how a single register (one word) is built from switches, a clock, and flip-flops. RAM is just an array of these.
- **[[learning/notes/quick-context/d-flip-flop]]** — The 1-bit storage element underneath every register; the `load`/clock-edge behavior of a whole register comes straight from the DFF.
- **[[learning/notes/micro-context/sram]]** — How a real fast memory cell stores a bit with six cross-coupled transistors. The "register per word" model in this note is essentially SRAM.
- **[[learning/notes/quick-context/physics-of-writing-data-to-memory]]** — The other side of the SRAM-vs-DRAM split: why a capacitor-based cell is dense and cheap but leaks and needs refresh.
- **[[learning/notes/quick-context/cpu-fetch-execute-cycle]]** — The rung above this one: the CPU repeatedly reads instructions and data from RAM by address, then writes results back — it is the main "customer" of this addressing machinery.
- **** — The spine hub: the full ladder from electricity up to running code. RAM is rung L7, sitting above the register and below the CPU.

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** What two switching circuits turn an array of registers into addressable RAM, and which path (read or write) does each serve?
<details>
<summary>Answer</summary>
A **DMUX** serves the **write path** — it routes the single `load` signal to exactly one register's load pin. A **MUX** serves the **read path** — it selects exactly one register's output to pass through as `out`. Both use the same address. See "How It Works."
</details>

**Q2:** With a 10-bit address, how many distinct words can RAM hold, and why?
<details>
<summary>Answer</summary>
$2^{10} = 1024$ words. Each address bit doubles the number of distinguishable addresses, so $n$ bits name $2^n$ words. (3 bits -> 8, the RAM8 case.)
</details>

**Q3:** All eight registers in a RAM8 share the same clock line. Why doesn't a single write overwrite all eight registers at once?
<details>
<summary>Answer</summary>
Because each register only captures new data when its own `load` (clock-enable) is 1. The DMUX converts the single incoming `load` into a one-hot vector — exactly one of the eight load lines is high — so when the clock edge arrives, only the addressed register captures `in`; the other seven have `load = 0` and simply hold. See "Why the DMUX prevents clobbering."
</details>

**Q4:** Someone says "a 16K RAM must be built from 8 RAM4Ks, because that's the recursive rule." What's wrong with that claim?
<details>
<summary>Answer</summary>
$16384 / 4096 = 4$, not 8 — so RAM16K is built from **four** RAM4Ks, not eight. The "8×" rhythm of RAM8 -> RAM64 -> RAM512 -> RAM4K breaks at the top level. Accordingly, `ram16K_chip.py` uses a **4-way** DMUX/MUX and a **2-bit** top address field (`address[:2]`) instead of the 3-bit 8-way decoder used at the lower levels.
</details>

**Q5:** Reading from RAM is described as combinational (no clock needed) while writing requires a clock edge. Why the asymmetry, and what would go wrong if writes weren't clock-gated?
<details>
<summary>Answer</summary>
Reading is pure selection: every register is already holding a stable value and continuously outputting it, so the MUX can route the chosen one out immediately. Writing changes stored state, which must happen at a single, well-defined instant. If a write weren't gated to the clock edge, the register could capture transient, mid-settling "glitch" values as the address and data lines change, corrupting memory. The clock edge (plus the DMUX picking one register) guarantees the addressed cell latches a clean value at one precise moment. This is the same edge-triggered discipline the [[learning/notes/quick-context/d-flip-flop|D flip-flop]] provides at the single-bit level.
</details>

</details>
