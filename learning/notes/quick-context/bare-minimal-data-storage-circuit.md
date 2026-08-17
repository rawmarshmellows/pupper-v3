---
topic: Bare-Minimal Data Storage Circuit — Keyboard, Clock, and 8-bit ASCII Storage
created: 2026-05-03
updated: 2026-05-07
---

# Bare-Minimal Data Storage Circuit — Keyboard, Clock, and 8-bit ASCII Storage

> **Related:** [[learning/notes/quick-context/switches-to-registers-storing-data]] | [[learning/notes/quick-context/d-flip-flop]] | [[learning/notes/quick-context/physics-of-writing-data-to-memory]] | [[learning/notes/quick-context/clock-sources-and-timing]] | [[learning/notes/quick-context/rc-oscillator]] | [[learning/notes/quick-context/code-to-gates-and-bootstrapping]] | [[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens]] | [[learning/notes/micro-context/clock-edges]] | [[learning/notes/micro-context/clock-source]] | [[learning/notes/micro-context/sram]] | [[learning/notes/micro-context/decoupling-capacitor]] | [[learning/notes/micro-context/eeprom]] | [[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]

> **TL;DR:** Press a key on a 16-key keypad → an encoder chip emits a 4-bit code + a "key pressed" strobe → a tiny EEPROM converts that 4-bit code to the **8-bit ASCII value** of that key → those 8 lines sit on a *data bus* feeding the D inputs of an **8-bit register** ([[learning/notes/quick-context/d-flip-flop|74HC574]]) → meanwhile a 555 timer is producing a steady square-wave **clock** at ~2 Hz → an AND gate gates the clock so register updates only happen *while a key is held* → on the next rising clock edge, all 8 ASCII bits are captured **simultaneously** and lit up on 8 LEDs. **The clock is not deciding what to store — it is deciding *when* to store.** That single distinction is the entire intuition behind "how a clock controls a computer".

## Human notes

The 1-bit version of this circuit had no clock — pressing a button instantly flipped the [[learning/notes/quick-context/d-flip-flop|SR latch]]. **In Nand2Tetris, the clock is a black box** (the curriculum just says "the register updates on the rising edge"), and the question that keeps not clicking is: what does that mean *electrically*? What is the clock physically? Where does it live on the breadboard? And *how* does it cause one specific instant to become the "store this now" instant? This document builds that intuition by extending the 1-bit storage circuit to an **8-bit ASCII keyboard storage circuit**, with the clock made fully visible — its own [[learning/notes/quick-context/rc-oscillator|oscillator chip]], its own probe-able wire, its own LED you can watch blink, and its own [[learning/notes/micro-context/clock-edges|edge-triggered]] gating into the register.

## The Core Problem: Nand2Tetris hides the clock; this circuit makes it physical

Most digital-logic curricula draw the clock as a small triangle on a schematic and state "the register updates here." That's a *behavioural* description — true, but unsatisfying. What gets hidden:

1. The clock is a **physical [[learning/notes/quick-context/voltage|voltage]] waveform** produced by an oscillator (a 555 timer, an [[learning/notes/quick-context/rc-oscillator|RC oscillator]], or a [[learning/notes/micro-context/crystal-oscillator|crystal]]). It has a frequency, a duty cycle, and a real wire you can poke with a scope.
2. The clock signal is **broadcast** to every register in the system at the same time — that's how 32 D flip-flops in one register file all update on a single instant.
3. **The clock does not choose *what* to store.** The data lines (the D inputs) do. The clock only chooses *when* the storage element samples those data lines.
4. **Whether a given clock edge "counts" for a given register** is itself controlled by combinational logic — usually an AND gate that says "this register only updates when *its* enable line is HIGH right now."

Once you see all four facts on a breadboard with their own LEDs, "the clock controls the computer" stops being mystical and becomes: *the clock is a metronome every register listens to, and combinational logic picks which registers actually clap on each beat.*

## The 1-Bit Building Block (Brief Recap)

The previous version of this circuit was an **SR latch on a single 74HC00**: two cross-coupled NAND gates, two pushbuttons (LOAD/RESET), pull-ups, and an LED. **No clock.** Press LOAD → Q goes HIGH and stays HIGH. Press RESET → Q goes LOW and stays LOW. The cross-coupled feedback *is* the memory.

That worked because the value-to-store was hardcoded into *which button you pressed* — LOAD inherently meant "1", RESET inherently meant "0". As soon as you want to store **arbitrary external data** (an 8-bit ASCII byte from a keypress), the SR latch can no longer do it: there's no D input. You graduate to a [[learning/notes/quick-context/d-flip-flop|D flip-flop]], which has both a data input *and* a clock input, and that's where the clock enters the picture for real. See [[learning/notes/quick-context/switches-to-registers-storing-data]] for the conceptual ladder from latch → flip-flop → register.

## What the Clock Physically Is

The clock is a square-wave voltage signal toggling between LOW (~0 V) and HIGH (~Vcc) at a fixed frequency:

```
            HIGH ──┐    ┌────┐    ┌────┐    ┌────┐    ┌──
                   │    │    │    │    │    │    │    │
                   │    │    │    │    │    │    │    │
            LOW    └────┘    └────┘    └────┘    └────┘
                        ↑         ↑         ↑
                   rising edges (where registers sample D inputs)

                        ◄─── T ───►
            T = 1/f, e.g. 500 ms for 2 Hz, or 1 ns for 1 GHz
```

For our circuit we use a **555 timer in astable mode** running at ~2 Hz so you can *see* each cycle on an LED. A real CPU runs the same waveform at $10^9$ Hz (1 GHz = 1 cycle per nanosecond), but the geometry is identical — only the time axis is compressed by ~$5×10^8$. The 555's output is a single wire that fans out to every register in the system. See [[learning/notes/quick-context/rc-oscillator]] for how the oscillator generates this waveform from an RC charging loop, and [[learning/notes/micro-context/clock-source]] for the spectrum of clock generators (RC → [[learning/notes/micro-context/ceramic-resonator|ceramic resonator]] → crystal → PLL).

A D flip-flop's clock input is **edge-sensitive** — it only does anything at the moment the clock voltage transitions from LOW to HIGH (the **rising edge**). For the rest of the cycle, the input D can wiggle freely; the flip-flop ignores it. This is the entire mechanism behind "synchronous" digital logic. See [[learning/notes/micro-context/clock-edges]] for why edge-triggering exists rather than level-triggering.

## 5 Essential Terms

| Term | What it is | Role in this circuit |
|------|-----------|----------------------|
| **555 timer (astable mode)** | An 8-pin chip that, with two resistors and a [[learning/notes/quick-context/capacitor|capacitor]] on its timing pins, produces a continuous square wave on its output pin. Frequency $f \approx 1.44 / ((R_1 + 2R_2) \cdot C)$. | Generates the system clock — a free-running ~2 Hz square wave broadcast to the register's CLK input (via a gate). |
| **74HC574 octal D flip-flop** | An 8-bit register: 8 D flip-flops sharing one CLK pin and one $\overline{\text{OE}}$ (output enable) pin. On each rising clock edge, all 8 D inputs are sampled and their values appear on the 8 Q outputs. | The 8-bit storage element. Holds the captured ASCII byte until the next gated rising edge replaces it. |
| **74C922 keyboard encoder** | A 16-key (4×4 matrix) decoder chip that auto-scans the keypad, debounces the contacts internally, and outputs (a) a 4-bit binary code identifying which key is pressed, and (b) a **DA (Data Available)** pin that goes HIGH for as long as a key is held. | Translates "physical keypress" into "4-bit identifier + valid-data strobe." Without it you'd have to hand-build a scan + debounce circuit. |
| **EEPROM lookup (28C16 or similar)** | A small non-volatile memory chip you pre-program with a 16-byte table mapping 4-bit address → 8-bit ASCII code. With A0–A3 driven by the encoder and A4–A10 tied LOW, it reads out the right ASCII byte on D0–D7 within ~150 ns. | Converts the keypad's internal 4-bit key index into actual ASCII (e.g. key index $2 \to$ ASCII `'2'` $= 0x32 = 0011\,0010$). See [[learning/notes/micro-context/eeprom]]. |
| **Clock gating (AND gate)** | A 74HC08 AND gate whose two inputs are (a) the raw 555 clock and (b) the encoder's DA strobe. Output `GATED_CLK = 555_CLK ∧ DA`. | The "should this register update *this* cycle?" decision. When no key is held, DA is LOW, so GATED_CLK never rises and the register holds its last value. When a key is held, GATED_CLK passes the 555 waveform through. |

## The Circuit Architecture

### Block diagram — what produces what

```
┌─────────────┐    4 rows + 4 cols     ┌──────────────┐
│  4×4 KEYPAD │ ◄────────────────────► │   74C922     │
│  0 1 2 3    │       scan matrix      │   ENCODER    │
│  4 5 6 7    │                        │              │
│  8 9 A B    │                        │              │
│  C D E F    │                        │              │
└─────────────┘                        └─┬──────────┬─┘
                                         │          │
                              D-OUT[3:0] │          │ DA strobe
                                (4-bit)  │          │ (HIGH = key held)
                                         ▼          │
                                ┌─────────────────┐ │
                                │  28C16 EEPROM   │ │
                                │  A[3:0]   ◄──   │ │
                                │  A[10:4] = GND  │ │
                                │                 │ │
                                │  D[7:0] ────────┼─┼──► 8-bit ASCII bus ──┐
                                └─────────────────┘ │                      │
                                                    │                      │
┌──────────────┐                                    │                      │
│ 555 TIMER    │   ~2 Hz square wave                │                      │
│ astable mode │ ────► CLK_RAW ──┐                  │                      │
└──────────────┘                 │                  │                      │
                                 ▼                  ▼                      │
                                ┌────────────────────┐                     │
                                │    74HC08 AND      │                     │
                                │                    │                     │
                                │    GATED_CLK ──────┼──┐                  │
                                └────────────────────┘  │                  │
                                                        ▼                  ▼
                                ┌──────────────────────────────────────────────┐
                                │       74HC574 (8-bit register)               │
                                │       CLK    ◄── GATED_CLK                   │
                                │       D[7:0] ◄── ASCII bus                   │
                                │                                              │
                                │       Q[7:0] ──► 8 LEDs ──► ASCII display    │
                                └──────────────────────────────────────────────┘
```

Three independent signal *families* meet at the 74HC574:

- **Data path** (8 wires): keypad → encoder → EEPROM → register's D[7:0]. Always reflects "the ASCII of the key currently pressed", or undefined when no key is held.
- **Clock path** (1 wire): 555 → AND gate → register's CLK. Free-running square wave, but only passed through to the register when DA is HIGH.
- **Strobe / enable path** (1 wire): encoder DA → AND gate's other input. The "is there valid data right now?" combinational signal.

### Bill of materials

| Part | Qty | Notes |
|------|-----|-------|
| 4×4 matrix keypad | 1 | Membrane or tactile, ~$3. 8 pins (4 rows + 4 cols). |
| 74C922 encoder | 1 | DIP-18. Internal debouncing via an external 1 µF cap on KBM and 0.1 µF on OSC. |
| 28C16 EEPROM (or AT28C64, or 27C16) | 1 | Pre-programmed with 16 bytes of ASCII for keys `0`–`9`, `A`–`F`. Programmed once with a TL866 / MiniPro / Arduino sketch. |
| NE555 timer | 1 | DIP-8. Clock generator. |
| 74HC08 quad AND | 1 | DIP-14. We use 1 of 4 gates for clock-gating; tie unused inputs LOW. |
| 74HC574 octal D flip-flop | 1 | DIP-20. The 8-bit register itself. Tie $\overline{\text{OE}}$ (pin 1) LOW so outputs are always driven. |
| LED + ~330 Ω [[learning/notes/quick-context/resistor|resistor]] | 8 | One per output bit Q0–Q7. Wire them anode-to-Q, cathode-to-GND-via-resistor. |
| LED + ~330 Ω resistor | 1 | "Clock heartbeat" indicator on the 555 output — invaluable for visualizing the metronome. |
| LED + ~330 Ω resistor | 1 | "Key pressed" indicator on the DA line. |
| 10 kΩ resistor | several | Pull-ups, encoder timing, 555 timing. |
| 1 µF + 0.1 µF + 22 µF caps | 1 each | 1 µF on encoder KBM (sets ~10 ms debounce), 0.1 µF on encoder OSC, 22 µF for 555 timing. With $R_1 = R_2 = 10\,\text{kΩ}$ and $C = 22\,\mu\text{F}$: $f \approx 1.44 / ((R_1+2R_2) \cdot C) = 1.44 / (30\,\text{kΩ} \cdot 22\,\mu\text{F}) \approx 2.2$ Hz. Swap to $C = 47\,\mu\text{F}$ if you want ~1 Hz instead. |
| 0.1 µF decoupling caps | 4 | One per chip, across Vcc/GND. Non-negotiable. See [[learning/notes/micro-context/decoupling-capacitor]]. |
| 5 V supply | 1 | USB breakout, bench supply, or 4×AA. |

Total: **~$15 in parts**, fits on a full-size breadboard.

### EEPROM contents (the keymap)

Address bits A0–A3 come from the encoder; A4–A10 are tied to GND. The 16 bytes at addresses `0x00`–`0x0F` are programmed to the ASCII codes for the keypad's labels:

| Encoder out (A3..A0) | Key label | EEPROM data (D7..D0) | ASCII |
|----------------------|-----------|----------------------|-------|
| `0000` | `0` | `0011 0000` | `0x30` |
| `0001` | `1` | `0011 0001` | `0x31` |
| `0010` | `2` | `0011 0010` | `0x32` |
| ... | ... | ... | ... |
| `1001` | `9` | `0011 1001` | `0x39` |
| `1010` | `A` | `0100 0001` | `0x41` |
| `1011` | `B` | `0100 0010` | `0x42` |
| `1100` | `C` | `0100 0011` | `0x43` |
| `1101` | `D` | `0100 0100` | `0x44` |
| `1110` | `E` | `0100 0101` | `0x45` |
| `1111` | `F` | `0100 0110` | `0x46` |

(All other 2032 EEPROM addresses are don't-care; you can leave them `0xFF` — they're never addressed because A4–A10 are grounded.)

## How It Works — Pressing the Key `'A'`

The cleanest way to internalize the clock's role is to walk every signal through one full press. Imagine the 555 has been running for a while — the clock LED is pulsing at 2 Hz steadily, but the 8 output LEDs are static (holding whatever was last latched).

### Timeline

```
                                  t →
                            0     0.5   1.0   1.5   2.0   2.5   3.0  (seconds)
                            │     │     │     │     │     │     │

CLK_RAW (555 output)        ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──
                            │  │  │  │  │  │  │  │  │  │  │  │  │
                         ───┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘
                            ▲     ▲     ▲     ▲     ▲     ▲     ▲
                            rising edges (every 500 ms)

DA (encoder strobe)         ────────────┌─────────────────┐──────────
                                        │                 │
                                        ▲                 ▲
                                      t=1.0             t=2.5
                                  [key pressed]      [released]

ASCII bus D[7:0]            ── XX XX XX │    0100 0001    │ XX XX ──
                                              (= 0x41, ASCII 'A')

GATED_CLK (to register)                       ┌──┐  ┌──┐
(= CLK_RAW AND DA)          ──────────────────┘  └──┘  └──────────────
                                              ▲     ▲
                                              │     │
                                  first gated rising edges while DA=HIGH
                                  → register samples 0x41 on the first one

Q[7:0] (register output)    = previous value =│ 0100 0001 ============
                                              ▲
                                              │
                                       register updates here
                                       (8 LEDs jump to 'A')
```

### What happens in each stage

1. **Idle (t < 1.0 s):** No key held. DA is LOW. The AND gate's output is LOW regardless of the 555. The register holds its last latched value forever. *The clock is running, but nobody is listening.*
2. **Key 'A' pressed (t = 1.0 s):** The encoder's internal scanner detects the keypress, *waits ~10 ms for the contacts to debounce* (set by the 1 µF KBM cap), then sets D-OUT to `1010` (binary 10 = 'A's index) and pulls DA HIGH. The EEPROM, now addressed at `0x0A`, drives `0100 0001` onto its 8 data outputs within ~150 ns of the address being valid. The 8-bit ASCII bus is now valid (~10 ms after the physical keypress, dominated entirely by debounce). *But the register has not updated yet* — the gated clock has not yet seen a rising edge with DA HIGH.
3. **Next rising edge of CLK_RAW with DA HIGH (t ≈ 1.5 s):** The AND gate's output transitions LOW→HIGH. This is the rising edge the 74HC574 has been waiting for. **All 8 D inputs are sampled simultaneously**, and the 8 Q outputs change to `0100 0001`. The 8 LEDs now spell out `0x41` in binary. *This is the moment the clock "controls" the storage.*
4. **Key still held (t = 1.5–2.5 s):** Subsequent rising edges keep capturing the same value (the key is still 'A'), so the LEDs don't change visibly. But internally, the register is being re-loaded with 0x41 every 500 ms. (The 74HC574's setup time is ~17 ns and the EEPROM's access time is ~150 ns; the 500 ms clock period swamps both by ~$10^6×$, so timing margin is not even close to a constraint at this speed.)
5. **Key released (t = 2.5 s):** DA goes LOW. The gated clock immediately stops producing rising edges. The register freezes on the last captured value. The LEDs continue to display `0x41` until you press another key. *The clock is still running — the register is just no longer listening.*

### The key insight you can see on a scope

Probe these four signals simultaneously:

```
CHANNEL 1: CLK_RAW   (555 output)
CHANNEL 2: DA        (encoder strobe)
CHANNEL 3: GATED_CLK (AND gate output, register CLK pin)
CHANNEL 4: D0        (one bit of the ASCII bus)
```

You'll see CH1 metronoming away forever. CH2 only HIGH while a key is held. CH3 = CH1 ∧ CH2, so most of the time CH3 is silent and only "wakes up" during keypresses. CH4 changes whenever you press a different key — but the *register's output* only follows CH4 at moments where CH3 has a rising edge. **This is the mechanical picture of "clocked synchronous logic":** data lines are noisy and wiggling all the time; the register only believes them at clock edges; combinational gating decides which edges the register pays attention to.

## Why a Computer Needs a Free-Running Clock

In Nand2Tetris the clock seems gratuitous — "why not just have the keypress directly latch?" The reason becomes obvious when you scale up:

1. **Synchronization across many registers.** A real CPU has thousands of registers — program counter, instruction register, ALU input/output latches, register file slots. They all need to update in *lockstep* so data flowing through combinational logic from register A reaches register B before B's next sample. The shared clock guarantees this. Without it, every register would update on its own schedule and you'd have race conditions everywhere.
2. **Sequencing pipelined operations.** "Fetch instruction → decode → execute → writeback" is four clock cycles. Each cycle, the data physically moves one stage forward through the pipeline because each stage's output register samples on the same clock edge. The clock is the *peristalsis* that pushes data through the chip.
3. **Bounded settling time.** Combinational logic (gates, multiplexers, ALU adders) has propagation delay. Inputs change → outputs glitch chaotically for some time → outputs eventually settle to the correct value. The clock period must be longer than the longest combinational path so that *by the next rising edge*, everything has settled. "Clock speed" is literally how short you can make the period before paths fail to settle in time. See [[learning/notes/micro-context/clock-speed]].
4. **Per-register write enable.** This is the part our circuit makes most concrete. Every register in a real CPU has its own enable line, gated against the global clock with an AND gate (or built-in clock-enable input). On every clock edge, *every* register sees the edge — but only those whose enable is HIGH actually update. The instruction decoder drives those enables. **The clock doesn't pick which register writes — combinational logic does. The clock just fires the gun simultaneously for all of them.**

When you internalize point 4, "the clock controls the computer" stops meaning "the clock decides what happens" and starts meaning *"the clock provides the synchronized firing instants; the rest of the circuit decides who responds."*

## The Key Tension: Two Different Mental Models of Storage

| | **SR latch** (1-bit, no clock) | **Clocked register** (8-bit, with clock) |
|---|---|---|
| Trigger | Level on $\overline{S}$ / $\overline{R}$ — change happens *whenever* the input is asserted | Rising edge of CLK — change happens *only at* discrete instants |
| What chooses the stored value? | Which input button you pressed (`Set` = 1, `Reset` = 0) | The D inputs at the moment of the clock edge |
| What chooses *when* to write? | The act of pressing | The combinational gating signal (DA in our circuit; instruction decoder in a CPU) |
| Scales to N bits? | Awkwardly (each bit needs its own pair of buttons) | Cleanly — 8 D flip-flops share one CLK |
| Synchronizes multiple storage elements? | No — each updates independently | Yes — all share one clock edge |

**The one thing most outsiders get wrong about this is...** thinking the clock is what *causes* a storage event, when really the clock just *permits* a storage event at a regular rhythm and the data lines + enable lines decide the rest. The clock is closer to a stage manager calling "places, now!" than to a director picking the dialogue. Once you make that mental swap, every "clock-controlled" diagram (CPUs, FPGAs, DSPs) becomes legible: find the clock, then look at what's gating each register's clock-enable to see what the system is *actually* doing.

## Connecting to Real CPUs

This circuit is a 1-byte slice of a CPU register file. To get to a working CPU from here, you'd add:

- **More registers** — duplicate the 74HC574 16 or 32 times. Each gets its own enable line.
- **A multiplexer in front of the data bus** — so the bus can carry data from different sources (keyboard, ALU output, memory) at different times. The clock still fires every register; the mux + enable combination decides which register gets which source.
- **An instruction decoder** — combinational logic that takes the current opcode and lights up the right enable lines. "Opcode 0x4 → enable register R1; opcode 0x5 → enable register R2."
- **A program counter** — itself a register that re-loads from `PC + 1` on every clock edge (its enable is always HIGH unless the CPU is halted). The PC is the clearest example of "the clock advances the machine one step per edge."
- **Memory** — large arrays of [[learning/notes/micro-context/sram|SRAM cells]] (which are *also* cross-coupled latches, just like our 1-bit base case, with extra access transistors).

Every one of those uses the same three-signal-family pattern this circuit demonstrates: a *data* path, a *clock* path, and *enable* paths that gate which clock edges count for which destination. Once that pattern is concrete, [[learning/notes/quick-context/code-to-gates-and-bootstrapping|how a computer actually runs code]] reduces to "every clock cycle, the decoder lights up enables that route data through one stage of the fetch/decode/execute pipeline."

## Peripheral Knowledge

- [[learning/notes/quick-context/switches-to-registers-storing-data]] — the conceptual ladder from "switch as 1 bit" to "register as N bits." Read first if the SR-latch building block isn't intuitive yet.
- [[learning/notes/quick-context/d-flip-flop]] — the next-step-up storage primitive: a single edge-triggered D flip-flop. The 74HC574 is just 8 of these in one chip.
- [[learning/notes/quick-context/physics-of-writing-data-to-memory]] — what's *physically* happening inside the flip-flop at the rising edge.
- [[learning/notes/quick-context/clock-sources-and-timing]] — full treatment of clock generators, jitter, and skew.
- [[learning/notes/quick-context/rc-oscillator]] — how a 555 in astable mode actually generates the square wave from RC charging dynamics.
- [[learning/notes/quick-context/code-to-gates-and-bootstrapping]] — how the same clocked-register pattern scales up to "the CPU runs your program."
- [[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens]] — the historical arc that produces this entire stack.
- [[learning/notes/micro-context/clock-edges]] — why edge-triggering exists rather than level-triggering.
- [[learning/notes/micro-context/clock-source]] — the spectrum of clock generators (RC → ceramic → crystal → PLL).
- [[learning/notes/micro-context/eeprom]] — how the keymap lookup chip works.
- [[learning/notes/micro-context/sram]] — how the same cross-coupled-latch pattern scales to gigabytes of CPU cache.
- [[learning/notes/micro-context/decoupling-capacitor]] — why the 0.1 µF cap on every chip is non-negotiable.

## Test Your Understanding

**Q1:** What are the *three* independent signal families that meet at the 74HC574, and what does each one carry?
<details>
<summary>Answer</summary>
(1) The **data path** — 8 wires from the EEPROM carrying the ASCII byte for whichever key is currently pressed. (2) The **clock path** — 1 wire from the AND gate, carrying the gated 2 Hz square wave that fires rising edges only while a key is held. (3) The **enable / strobe path** — the encoder's DA pin, combinationally combined with the raw clock by the AND gate to produce the gated clock. The register's job is to capture the data path on rising edges of the clock path; whether such an edge ever arrives is decided by the enable path. See "The Circuit Architecture."
</details>

**Q2:** Why is the 555's clock output run through an AND gate with the encoder's DA strobe before reaching the register's CLK pin? What would happen if you connected the 555 directly to CLK?
<details>
<summary>Answer</summary>
The AND gate is a **clock gate** — it lets the clock through only when DA is HIGH (i.e., only when a key is held). If you connected the 555 directly to CLK, the register would re-sample the data bus on every single rising edge, *forever*. Between keypresses the data bus would be driven to undefined values (no key → encoder DA is LOW → EEPROM may be in a stale or floating state), so the register would constantly capture garbage. The DA-gated clock makes "no key pressed" indistinguishable from "no clock running" *as far as the register is concerned*, even though the 555 keeps oscillating. See "Why a Computer Needs a Free-Running Clock," point 4.
</details>

**Q3:** When you press 'A', the ASCII byte `0x41` may not appear on the LEDs immediately — there can be up to ~500 ms of latency. Why? Is this a bug?
<details>
<summary>Answer</summary>
Not a bug — it's the cost of **synchronizing to a slow clock**. The register only updates on rising edges of the gated clock. If you press the key just *after* a rising edge, the gated clock has to complete the rest of its 500 ms cycle before the next edge arrives. The data bus settles within ~10 ms of the keypress (dominated by the encoder's debounce time, plus ~150 ns of EEPROM access), but the register doesn't sample it until the next edge — which can be up to one full clock period later. Real CPUs have the same latency mechanically — every signal takes at least one clock cycle to propagate from one register to the next — but their clocks run at $10^9$ Hz, so the latency is nanoseconds rather than half-seconds. **This circuit is just a CPU with the time axis stretched by ~$5 \times 10^8$ so you can see the latency happening.** See "How It Works — Pressing the Key 'A'."
</details>

**Q4:** A common confusion from Nand2Tetris is "the clock decides what gets stored." Explain why that statement is misleading, using this circuit as the counter-example.
<details>
<summary>Answer</summary>
The clock decides **when**, not **what**. In this circuit, the clock is a free-running 2 Hz square wave that knows nothing about the keypad, the ASCII bus, or which register exists. *What* gets stored is determined entirely by (a) the data lines (driven by the keypad → encoder → EEPROM chain) and (b) the AND-gate enable (driven by the encoder's DA pin). The clock just provides synchronized "moments to commit." If you change the EEPROM contents, the same clock edges store different values. If you change the gating logic, the same data and clock produce different write patterns. The clock is the *metronome*, not the *score*. This is exactly how a real CPU works — the global clock fires every register's CLK input simultaneously, and the instruction decoder's combinational logic decides which registers' enables are HIGH on this edge. See "The Key Tension."
</details>

**Q5:** Suppose you wanted to extend this to a *two*-byte storage circuit (so you could capture two consecutive keypresses into two separate registers — like the first byte of an opcode and its argument). What new signal would you need to add, and what existing signal stays exactly the same?
<details>
<summary>Answer</summary>
You'd add a **second per-register enable signal** — call it `WE_A` for register A and `WE_B` for register B — driven by some sequencing logic (perhaps a 1-bit counter that flips on each keypress). Both registers would still share **exactly the same global clock** from the 555. Both enables would be ANDed with that shared clock to produce two gated clocks: `CLK_A = 555 ∧ WE_A ∧ DA`, `CLK_B = 555 ∧ WE_B ∧ DA`. Press the first key while `WE_A=1` → only register A captures. Press the second key while `WE_B=1` → only register B captures. **The clock remains a single shared resource broadcast to every register; what changes from one storage element to the next is its enable.** This is the *exact* mechanism by which a real CPU's register file works: 32 registers all listening to one clock, with a 5-bit "destination register" field from the instruction selecting which one's enable goes HIGH this cycle. The leap from this circuit to a CPU register file is just *more enables*, not a different concept of clocking.
</details>
