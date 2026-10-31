---
topic: The Data Bus and Bus Arbitration — How Chips Share Wires
created: 2026-06-07
---

# The Data Bus and Bus Arbitration — How Chips Share Wires

> **Related:** [[learning/notes/index/how-a-computer-works-index]] | [[learning/notes/quick-context/switches-to-registers-storing-data]] | [[learning/notes/quick-context/keypress-to-pixel-pipeline]] | [[learning/notes/quick-context/embedded-communication-protocols]]

> **TL;DR:** A **bus** is a single bundle of wires that the CPU, RAM, and every peripheral all share — instead of running a private set of wires from every chip to every other chip. The catch: if two chips try to drive the same wire to opposite voltages, you get a [[learning/notes/micro-context/short-circuit|short circuit]] and garbage data. The fix is **tri-state** outputs (the same Output Enable pin you met on the 74HC574 register) plus **arbitration** — a discipline that guarantees exactly one chip drives the shared wires at any instant, while everyone else stays electrically "invisible."

## The Core Problem

A computer is dozens of chips that all need to exchange bytes: the CPU reads an instruction from RAM, writes a pixel to the display controller, polls a keyboard. Wiring a dedicated set of data lines from every chip to every other chip would need an explosion of traces — for $N$ chips each needing to talk to all others, point-to-point links grow roughly as $N^2$. A shared **bus** collapses that to one set of wires everyone taps into, so wiring grows like $N$. But sharing wires creates a new danger: two chips driving the same wire at once is an electrical short. The whole art of the bus is letting many chips share wires *without ever driving them at the same time.*

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Bus** | A shared bundle of parallel wires that multiple chips connect to. A typical system bus has three parts: an **address bus** (which location?), a **data bus** (what value?), and a **control bus** (read or write? when?). |
| **Tri-state / High-impedance (Hi-Z)** | A third output state beyond HIGH and LOW: electrically *disconnected*. A chip whose output is Hi-Z is "not on the wire" — it neither pulls the line high nor low, letting another chip drive it. Enabled/disabled by the [[learning/notes/quick-context/switches-to-registers-storing-data\|Output Enable (OE)]] pin. |
| **Bus contention** | The fault condition where two chips drive the same wire to opposite voltages (one HIGH, one LOW) simultaneously — a near-short that produces garbage logic levels and can overheat or damage the chips. The thing arbitration exists to prevent. |
| **Address decoding / Chip-select (CS)** | Logic that watches the address bus and activates exactly one device's enable pin when its assigned address range appears. This is how "everyone listens, one responds" is enforced. |
| **Memory-mapped I/O** | Treating peripherals (display, keyboard, timers) as if they were memory: each gets a slice of the address space, and the CPU talks to them with the *same* read/write instructions it uses for RAM. |

<details>
<summary><strong>How It Works</strong> — One wire, many talkers, no shouting</summary>

### The three buses

A "bus" in a computer is actually three cooperating bundles of wires:

```
THE THREE BUSES (a CPU talking to RAM and peripherals)
================================================================================

                 ADDRESS BUS (CPU drives — "WHICH location?")
        ┌───────────────────────────────────────────────────────┐
        │                                                       │
               DATA BUS (bidirectional — "WHAT value?")
        │  ┌─────────────────────────────────────────────────┐  │
        │  │                                                 │  │
                CONTROL BUS (READ / WRITE / CLOCK strobe)
        │  │  ┌───────────────────────────────────────────┐  │  │
        │  │  │                                           │  │  │
   ┌────┴──┴──┴──┐   ┌─────────────┐  ┌──────────┐  ┌────────────┐
   │     CPU     │   │     RAM     │  │ DISPLAY  │  │  KEYBOARD  │
   │(controller) │   │             │  │   CTRL   │  │    CTRL    │
   └─────────────┘   └─────────────┘  └──────────┘  └────────────┘
          │                 │               │              │
          └── address ──────┴─ all taps ────┴── data ──────┘
              (CPU sends)     the SAME     (one device
                               three buses    drives at a time)
```

- **Address bus** — driven by the CPU. An $n$-bit address bus can name $2^n$ distinct locations (a 16-bit address bus reaches $2^{16} = 65{,}536$ locations).
- **Data bus** — the only **bidirectional** bus. On a *read* the selected device drives it; on a *write* the CPU drives it.
- **Control bus** — carries the "verb" and the timing: a READ line, a WRITE line, and a clock/strobe that says "the value on the data bus is valid *now*."

### Why two drivers on one wire is a disaster

A digital output isn't just "a 1 or a 0." It's a tiny pair of transistors: to make HIGH it connects the wire to $V_{cc}$ (+supply); to make LOW it connects the wire to GND. If chip A says HIGH (wire to $V_{cc}$) while chip B says LOW (wire to GND) on the *same* wire, you've connected the power supply straight to ground through two transistors:

```
BUS CONTENTION = A SHORT CIRCUIT
================================================================================

   Chip A output = HIGH        Chip B output = LOW
        Vcc                          (the SAME wire)
         │                                │
       ──┴── transistor ON              ──┴── transistor ON
         │                                │
         └────────── shared wire ─────────┘
                       │
              voltage = undefined (~halfway),
              huge current flows Vcc → GND,
              chips heat up, data is garbage
```

The wire ends up at some undefined middle [[learning/notes/quick-context/voltage|voltage]] that's neither a valid 1 nor a valid 0, large current flows, and over time the output transistors can be damaged. **This is the central problem a bus must prevent.**

### The fix: tri-state and Output Enable

The solution is a **third output state**. Beyond HIGH (connected to $V_{cc}$) and LOW (connected to GND), a tri-state buffer adds **high-impedance (Hi-Z)**: *both* transistors off, so the output is electrically disconnected — as if the chip's pin had been physically unplugged from the wire.

```
NORMAL output: 2 states          TRI-STATE output: 3 states
─────────────────────────        ──────────────────────────────────
  HIGH  → wire to Vcc              HIGH  → wire to Vcc      (OE active)
  LOW   → wire to GND              LOW   → wire to GND      (OE active)
                                   Hi-Z  → DISCONNECTED     (OE inactive)
```

You already met this exact mechanism: the **74HC574** octal register from
[[learning/notes/quick-context/switches-to-registers-storing-data|Switches to Registers]] has an **Output Enable (OE)** pin. When OE is LOW, its eight Q outputs drive the bus; when OE is HIGH, all eight go Hi-Z and the chip "vanishes" from the bus while *still holding its stored byte inside*. Hang several 74HC574s on one 8-wire data bus, and the rule becomes simple and absolute:

> **At most one device may have OE active at any instant. Everyone else is Hi-Z.**

That single invariant is what makes a shared bus safe.

### Arbitration: who gets to drive, and when

"Exactly one driver at a time" raises the obvious question — *who decides which one?* That decision is **arbitration**. In the common single-master case it's not a fight at all; it's a strict protocol orchestrated by one boss:

```
A SINGLE-MASTER BUS TRANSACTION (CPU reads one byte from RAM)
================================================================================

 1. CPU drives the ADDRESS BUS with the address it wants.        (CPU = master)

 2. ADDRESS DECODER watches the address bus. It recognizes the
    address falls in RAM's range and asserts RAM's CHIP-SELECT.
    (Every other device's chip-select stays inactive → they stay Hi-Z.)

        address bus ──► ┌──────────────┐
                        │ ADDR DECODER │──► RAM   CS = ACTIVE
                        │  (some gates)│──► DISP  CS = inactive (Hi-Z)
                        └──────────────┘──► KBD   CS = inactive (Hi-Z)

 3. CPU asserts the READ line on the CONTROL BUS.

 4. The selected RAM (OE now active) DRIVES the DATA BUS with the byte.
    Because only RAM's output is enabled, there is no contention.

 5. CPU latches the data bus value on the clock edge, then releases READ.
    RAM returns to Hi-Z. The bus is free for the next transaction.
```

The **master** (here, the CPU) always owns the address and control buses. The **selected device** owns the data bus *only* during its turn, *only* in the direction the control bus dictates. Address decoding is just combinational logic (a few gates / a [[learning/notes/quick-context/comparator|comparator]]) that converts "an address appeared" into "this one chip's enable pin goes active."

**Multi-master arbitration (one paragraph).** Some buses have several would-be masters (e.g. a CPU and a DMA controller, or many nodes on [[learning/notes/quick-context/can-bus|CAN]] / [[learning/notes/micro-context/i2c|I2C]]). Then you need a tiebreak rule for simultaneous requests. Schemes include a dedicated **arbiter** that grants the bus to one requester at a time, daisy-chained **priority** lines, or — elegantly — **bitwise arbitration** as on CAN: every node transmits its message ID while listening; a dominant 0 overrides a recessive 1, so a node that sees a bit different from what it sent knows it lost and backs off, all with zero wasted time and no central referee.

</details>

<details>
<summary><strong>The Key Tension</strong> — Parallel bus vs. serial protocol</summary>

The parallel system bus described above (8/16/32/64 data wires switching together) is one end of a spectrum. The other end is the **serial protocols** — [[learning/notes/quick-context/uart|UART]], [[learning/notes/micro-context/i2c|I2C]], [[learning/notes/micro-context/spi|SPI]], [[learning/notes/quick-context/can-bus|CAN]], [[learning/notes/quick-context/usb-peripheral-hardware|USB]] — covered in [[learning/notes/quick-context/embedded-communication-protocols|Embedded Communication Protocols]]. The tension is *width vs. wires vs. distance.*

| | **Parallel bus** (system bus) | **Serial protocol** ([[learning/notes/micro-context/i2c|I2C]], SPI, UART, CAN, USB) |
|---|---|---|
| Data per clock | A whole word at once (8/16/32/64 bits) | 1 bit at a time |
| Wire count | Many (1 per data bit + address + control) | Few (1–4) |
| Speed *per pin* | Lower clock, but wide | Higher clock, but narrow |
| Distance | Short — on-board, between dies | Short to very long (CAN ~40 m, RS-485 ~1200 m) |
| Skew problem | Severe — all bits must arrive aligned; long fast parallel buses suffer **skew** (bits drifting out of step) | None — one wire, no inter-wire skew |
| Where you see it | Inside a chip / CPU↔cache↔RAM | Chip-to-chip, board-to-board, device-to-host |

The historical arc is *parallel → serial*: old PCs had parallel printer ports, PATA disk ribbons, and a parallel PCI bus. Those were replaced by USB, SATA, and PCIe — all **serial**. Why? At high speed, keeping dozens of parallel wires perfectly aligned (no skew) gets harder than just clocking one or two wires very fast. So modern "buses" between boxes are serial, while **parallel buses survive where distance is tiny and width is free** — inside a CPU, and on the short CPU-to-RAM path.

The deep idea, though, is shared by *both* worlds: a shared medium plus a rule for who-talks-when. I2C's open-drain SDA line with 7-bit addressing is conceptually the same as a parallel data bus with chip-select — it's just one wire and an addressing scheme instead of many wires and a decoder.

</details>

<details>
<summary><strong>Concrete Example</strong> — Two code anchors: selection logic + the address map</summary>

The whole "one driver onto a shared wire" idea reduces to two primitive operations from logic design, and the Nand2Tetris course implements both in plain Python.

### Anchor 1 — Selecting one source onto a shared line: the MUX

A bus *read* is "pick one of several drivers' values and put it on the shared wire." That is exactly a **multiplexer (MUX)**. From
`learning/references/courses/python-nand-to-tetris-part-1/src/hardware/elementary_logic_gates/mux_gate.py`:

```python
def mux_gate(a: int, b: int, sel: int) -> int:
    # If sel is 0 -> output a; if sel is 1 -> output b.
    # (a AND (NOT sel)) OR (b AND sel)
    not_sel = not_gate(sel)
    return (a & not_sel) | (b & sel)
```

Read `sel` as the chip-select. Only the *selected* source reaches the output; the unselected one is masked to 0 and contributes nothing — the software echo of "the unselected chip is Hi-Z and contributes nothing to the wire." A real bus with $k$ devices uses a wider MUX (a `mux16` selects a 16-bit word), but it is the same gate scaled up.

### Anchor 2 — Routing one signal to one destination: the DMUX

A bus *write* is the mirror image: take the master's data and steer it to exactly one destination — a **demultiplexer (DMUX)**. From
`.../elementary_logic_gates/dmux_gate.py`:

```python
def dmux_gate(a: int, sel: int) -> Tuple[int, int]:
    # If sel is 0 -> (a, 0); if sel is 1 -> (0, a).
    not_sel = 1 - sel
    return (a & not_sel), (a & sel)
```

`sel` again is the address/chip-select: the input `a` is delivered to one output and the other gets 0 (i.e., is *not written*). MUX = "select one talker"; DMUX = "select one listener." Bus arbitration is, at heart, MUX + DMUX driven by decoded address bits.

### Anchor 3 — Address ranges in action: memory-mapped layout

`learning/references/courses/python-nand-to-tetris-part-1/src/hardware/computer/memory.py`
builds a larger memory from two RAM chips by using the **top address bit** to choose between them — address decoding in miniature:

```python
def __call__(self, ..., load, address0, address1, ..., address14):
    # address0 (the high bit) decides WHICH chip is targeted.
    load_a, load_b = self.dmux_gate(load, address0)   # route the write
    ram_a = self.ram16K_chip_a(..., load_a, address1, ..., address14)
    ram_b = self.ram16K_chip_b(..., load_b, address1, ..., address14)
    # ... and a MUX selects which chip's output is returned on a read:
    result = self.mux16_gate(*ram_a, *ram_b, address0)
    return result
```

That is precisely **memory-mapped I/O** in embryo: the high address bit splits one address space into ranges, a DMUX routes a *write* to the correct range, a MUX selects the correct range's output on a *read*. The full Hack computer extends this so that some address ranges aren't RAM at all — they're the **screen** and **keyboard**. Writing to a screen address lights a pixel; reading the keyboard address returns the pressed key. The CPU uses one set of load/store instructions for everything, because to the CPU, RAM and peripherals are just different address ranges on the same bus. That handoff — write a byte to an address and a pixel changes — is exactly the next rung: [[learning/notes/quick-context/keypress-to-pixel-pipeline|keypress to pixel]].

### A concrete memory map

```
A SMALL 16-BIT MEMORY MAP (memory-mapped I/O)
================================================================================
  Address range        Device              Access
  ─────────────────────────────────────────────────────────────────
  0x0000 – 0x3FFF      RAM (16K words)     read / write data
  0x4000 – 0x5FFF      SCREEN buffer       write → pixels light up
  0x6000               KEYBOARD register   read  → current key code
  0x6001 – 0xFFFF      (unmapped)          reads return garbage / 0

  CPU: store value to 0x4000  ──► a pixel turns on   (no special "I/O" opcode)
  CPU: load from 0x6000       ──► get the pressed key (same load it uses for RAM)
```

**The one thing most outsiders get wrong about this is...** thinking peripherals need special "I/O instructions" or a separate I/O bus. On most modern architectures (ARM, RISC-V, and the Hack CPU) there *is no* separate I/O instruction — talking to the display, a timer, or a UART is just an ordinary memory read/write to an address that happens to be wired to that device instead of to RAM. The peripheral is a chip sitting on the same bus whose chip-select decodes to a reserved address range. "Reading a sensor" and "reading RAM" are, at the bus level, the identical electrical operation.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/quick-context/switches-to-registers-storing-data]]** — Origin of the Output Enable / tri-state mechanism. The 74HC574's OE pin is the exact primitive that lets registers share a data bus; this note picks up where that one leaves off.
- **[[learning/notes/quick-context/keypress-to-pixel-pipeline]]** — The next rung up the spine. Once memory-mapped I/O exists, a keypress (read from the keyboard address) can drive a pixel (write to a screen address) — the bus is the highway it all travels on.
- **[[learning/notes/quick-context/embedded-communication-protocols]]** — The serial alternative to a parallel bus: UART, I2C, SPI, CAN, USB, and when each wins on speed/distance/wire-count.
- **[[learning/notes/quick-context/uart]]** — The simplest serial link (no shared-bus arbitration at all: just one TX → one RX), a clean contrast to a multi-drop bus.
- **[[learning/notes/micro-context/i2c]]** — A 2-wire *shared* serial bus with 7-bit addressing and open-drain lines — serial-world chip-select; the closest serial cousin to address decoding.
- **[[learning/notes/quick-context/can-bus]]** — The canonical example of true **multi-master arbitration**: bitwise dominant/recessive contention resolves who transmits with no central arbiter.
- **[[learning/notes/quick-context/usb-peripheral-hardware]]** — A host-orchestrated serial bus where the host (a single master) polls devices, another point on the arbitration spectrum.
- **[[learning/notes/index/how-a-computer-works-index]]** — The hub: how we climb from electricity up to code executing. This note is rung L9.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What are the three buses in a typical system bus, and what does each carry?
<details>
<summary>Answer</summary>
The **address bus** (which location — driven by the CPU), the **data bus** (the actual value — bidirectional, driven by whoever currently has the bus in the active direction), and the **control bus** (the verb and the timing: READ/WRITE lines and a clock/strobe saying the data is valid now). See: How It Works (The three buses).
</details>

**Q2:** Why is it electrically dangerous for two chips to drive the same wire at the same time?
<details>
<summary>Answer</summary>
Driving HIGH connects the wire to $V_{cc}$; driving LOW connects it to GND. If one chip drives HIGH while another drives LOW on the same wire, you've connected $V_{cc}$ straight to GND through two transistors — a near-short. Large current flows, the wire sits at an undefined middle voltage that's neither a valid 1 nor 0 (garbage data), and the output transistors can overheat or be damaged. This is **bus contention**. See: How It Works (Why two drivers on one wire is a disaster).
</details>

**Q3:** How does the 74HC574's Output Enable pin make it safe to put several registers on one data bus?
<details>
<summary>Answer</summary>
OE controls whether the register's outputs are *driving* the bus or in **high-impedance (Hi-Z)** — electrically disconnected. The bus rule is "at most one device's OE active at a time"; every other device sits Hi-Z, contributing nothing to the wire (it still holds its stored byte internally). With only one active driver there's no contention. This connects directly to the [[learning/notes/quick-context/switches-to-registers-storing-data|register note]], where the same OE pin first appeared. See: How It Works (The fix: tri-state and Output Enable).
</details>

**Q4:** A friend says "peripherals like the display and keyboard must need special I/O instructions, separate from regular memory reads and writes." Why is that wrong on a memory-mapped system?
<details>
<summary>Answer</summary>
On memory-mapped architectures (ARM, RISC-V, the Hack CPU) peripherals live in reserved **address ranges** on the same bus as RAM. The address decoder asserts the display's or keyboard's chip-select when its range appears, so an ordinary store to a screen address lights a pixel and an ordinary load from the keyboard address returns the key — no special opcode, no separate I/O bus. At the bus level, "read a sensor" and "read RAM" are the identical electrical operation; only the decoded chip-select differs. See: Concrete Example (the misconception note and memory map).
</details>

**Q5:** Modern computers replaced parallel buses (PATA, parallel PCI, printer ports) with serial ones (SATA, PCIe, USB), yet CPUs *still* use a wide parallel bus to talk to cache and RAM. Reconcile these two facts.
<details>
<summary>Answer</summary>
Both choices optimize the same tradeoff (throughput vs. wire count vs. distance), and the right answer depends on **distance and skew**. Across a cable or board (centimeters to meters), keeping dozens of parallel wires perfectly time-aligned at high speed is harder than clocking one [[learning/notes/quick-context/differential-pair|differential pair]] very fast — so serial wins between boxes (USB, SATA, PCIe), avoiding inter-wire **skew** entirely. But CPU↔cache↔RAM links are millimeters long and width is essentially free on-die/on-package, so a wide parallel bus moves a whole 64-bit word per cycle with negligible skew and wins where it lives. Same physics, opposite verdict at different distances. See: The Key Tension (Parallel bus vs. serial protocol).
</details>

</details>
</details>
