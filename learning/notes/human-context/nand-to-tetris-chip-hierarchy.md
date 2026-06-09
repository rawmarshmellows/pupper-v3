---
concept: Nand to Tetris Chip Hierarchy — From NAND Gate to CPU
created: 2026-04-10
status: verified
---

# Nand to Tetris Chip Hierarchy

> **Related:** [[learning/notes/quick-context/code-to-gates-and-bootstrapping]] | [[learning/notes/quick-context/d-flip-flop]] | [[learning/notes/quick-context/switches-to-registers-storing-data]]

> **My understanding:** first we start of with the nand gate, which is the universal gate, these can then be constructed into the and, or, xor, and not gates. which can then be used to construct the mux (which maps 2 -> 1), or dmux (which maps 1 -> 2). these can then be connected into gates where we can take x inputs, and y outputs. from here we introduce the data flip flop chip which takes in a clock and an input, and return the last inputted value. this forms the foundation of the bit register chip which takes an input, and a load parameter and decides whether or not the store the input. it uses a mux gate. these then can be connected in a series of 16 to create a register chip. these then can be chained up to create a series of 64, 512, 1024, 4096, 8092, 16184 then through a combination of mux gates. the xor and and gate can then be used to construct a half adder then 2 half adders become a full adder which can then be used to construct the incremement 16bit and add 2 16bit chips, all of which can be used to construct the alu, which is part of the CPU (and the brain of it). the CPU will take in data from memory, data from program instruction, and a program reset counter. it will be able to run in 2 modes, either compute something or write something (i think i am wrong here).

---

First we start with the [[learning/notes/quick-context/code-to-gates-and-bootstrapping|NAND gate]], which is the universal gate — these can then be constructed into the AND, OR, XOR, and NOT gates. Which can then be used to construct the MUX (which maps 2 -> 1), or DMUX (which maps 1 -> 2). These can then be connected into multi-way variants where we can take x inputs and y outputs (like Mux4Way16, Mux8Way16, Dmux4Way, Dmux8Way).

From here we introduce the [[learning/notes/quick-context/d-flip-flop|data flip flop]] chip which takes in a clock and an input, and returns the last inputted value — `out(t) = in(t-1)`. This forms the foundation of the bit register chip which takes an input and a load parameter and decides whether or not to store the input. It uses a MUX gate (to select between the new input and the DFF's own previous output as feedback). These then can be connected in a series of 16 to create a [[learning/notes/quick-context/switches-to-registers-storing-data|register chip]].

These then can be chained up to create RAM of sizes 8, 64, 512, 4096, and 16384 [~~"64, 512, 1024, 4096, 8092, 16184"~~ — the actual RAM sizes in the Nand2Tetris course are 8, 64, 512, 4K (4096), and 16K (16384). There is no 1024 size; "8092" and "16184" are typos for 8192 and 16384, but the course skips 8K entirely. Each level groups 8 of the previous level (except the last: RAM16K groups 4 RAM4K units)] through a combination of DMUX and MUX gates [~~"mux gates"~~ — RAM uses both DMUX (to route the write/load signal to the correct register) and MUX (to select the correct register's output for reading)].

The XOR and AND gate can then be used to construct a half adder, then 2 half adders (plus an OR gate) become a full adder [~~"2 half adders become a full adder"~~ — a full adder is 2 half adders **plus an OR gate** to combine the two carry outputs]. Which can then be used to construct the increment-16-bit and add-two-16-bit chips, all of which can be used to construct the ALU, which is part of the CPU (and the brain of it).

The CPU will take in data from memory (inM — a 16-bit value from RAM), a program instruction (the current instruction from ROM), and a reset signal [~~"program reset counter"~~ — the CPU receives a `reset` input signal (a single bit) that resets the program counter to 0; the **program counter** is internal to the CPU, not an input]. It will be able to run in 2 modes: an **A-instruction** (address/load mode) that loads a value into the A register, or a **C-instruction** (compute mode) that performs an ALU computation and optionally writes the result to memory, the D register, or the A register [~~"either compute something or write something"~~ — the two modes are actually "load a constant/address" (A-instruction, opcode=0) and "compute and optionally store" (C-instruction, opcode=1). A C-instruction can both compute AND write in the same cycle — it's not one or the other. The CPU also handles jump conditions based on the ALU output].

---

## Quick Reference

- **NAND** is the universal gate — every other chip is built (transitively) from NANDs
- From NAND build the basic gates: **AND, OR, XOR, NOT**
- From the basic gates build **MUX** (2→1 selector) and **DMUX** (1→2 router), then their multi-way variants (Mux4Way16, Mux8Way16, Dmux4Way, Dmux8Way) for arbitrary $x$-input / $y$-output routing
- Introduce the [[learning/notes/quick-context/d-flip-flop|DFF]] (clock + input → outputs the previous tick's input: `out(t) = in(t-1)`) — this is the only stateful primitive
- A **Bit register** = 1 DFF + 1 MUX with feedback, controlled by a `load` signal (load=1 stores new input, load=0 holds old value)
- Wire 16 Bit registers in parallel → **16-bit Register**
- Memory hierarchy in Nand2Tetris is **RAM8 → RAM64 → RAM512 → RAM4K → RAM16K** (each groups 8 of the previous, except RAM16K which groups 4 RAM4K) — built from **DMUX (route the load signal) + MUX (select the read output)**
- **Half adder** = XOR (sum) + AND (carry); **Full adder** = 2 half adders + 1 OR (to combine the two carry-outs)
- Full adders chain into **Add16** and **Inc16**, which feed into the **ALU** (the compute core of the CPU)
- The **CPU** inputs are: `inM` (16-bit from RAM), `instruction` (16-bit from ROM), and `reset` (1 bit). The **program counter** lives *inside* the CPU
- The CPU runs one of two instruction types per cycle:
  - **A-instruction** (opcode 0) — load a 15-bit constant/address into the A register
  - **C-instruction** (opcode 1) — run an ALU computation and optionally write the result to A, D, and/or M, *and* optionally jump based on the ALU's output flags
- A C-instruction can compute **and** store **and** jump in the same cycle — it's not "either compute or write"

## Corrections at a Glance

| What I said | What's actually correct | Why |
|---|---|---|
| RAM sizes "64, 512, 1024, 4096, 8092, 16184" | RAM8, RAM64, RAM512, RAM4K (4096), RAM16K (16384) | Nand2Tetris skips 1024 and 8K; "8092" and "16184" are typos |
| RAM is built "through a combination of mux gates" | Built from **DMUX + MUX** | DMUX routes the load signal to the right register; MUX selects which register's output to read |
| "2 half adders become a full adder" | 2 half adders **plus an OR gate** | The OR combines the two carry-outs into a single carry-out |
| CPU receives a "program reset counter" as input | CPU receives a single-bit **`reset`** signal; the **program counter is internal** | The PC is a chip *inside* the CPU; only `reset` enters from outside |
| CPU runs in 2 modes: "compute something or write something" | A-instruction (load address) vs C-instruction (compute + optionally store + optionally jump) | The split is by *instruction type* (opcode bit), and a C-instruction can compute AND store AND jump in one cycle |

---

**Verification:** 12 claims checked. 7 correct, 5 corrected. Sources: course source code (python-nand-to-tetris-part-1), learning/notes/quick-context/code-to-gates-and-bootstrapping.md, learning/notes/quick-context/d-flip-flop.md
