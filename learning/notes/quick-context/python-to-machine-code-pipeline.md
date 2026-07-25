---
topic: Python to Machine Code — Compiling, Bytecode, the Virtual Machine, and the Machine Underneath
created: 2026-06-07
---

# Python to Machine Code — Compiling, Bytecode, the Virtual Machine, and the Machine Underneath

> **Related:** [[quick-context/cpu-fetch-execute-cycle]] | [[quick-context/keypress-to-pixel-pipeline]]

> **TL;DR:** Your Python source never runs on the CPU. CPython first **compiles** it to **bytecode** (the `.pyc` cache) — instructions for an imaginary **stack machine**, not for any real processor. A loop inside the `python` program (conceptually `ceval`, the "evaluation loop") then reads those bytecodes one at a time and acts on a value stack — this is the **virtual machine**. The twist that closes the circle: that VM loop is *itself* a C program that was compiled **ahead of time** into real machine code (the `python` executable). So every route from any language — compiled, interpreted, JIT, or transpiled — bottoms out in the same place: **machine-code instructions the CPU fetch-executes**. That meeting point is exactly where the software tower lands on the hardware tower (the [[learning/notes/quick-context/cpu-fetch-execute-cycle|CPU rung]]).

## The Core Problem

A CPU understands exactly one thing: binary machine-code instructions for *its* instruction set, fetched from memory one at a time. It has never heard of `def`, `+`, or `x = 2 + 3`. So if a CPU only eats machine code, how does a language like Python — which is never compiled to machine code — run at all? The answer is a tower of translation, and the whole point of this note is to make the tower concrete and show **where every language, no matter how it's processed, finally hands real machine code to the CPU.**

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Compile** | Translate source into a *lower* form ahead of running it. CPython compiles `.py` source into **bytecode** before execution (not into CPU machine code). A C compiler instead compiles all the way down to CPU machine code. |
| **Bytecode** | A compact list of simple instructions (`LOAD_CONST`, `STORE_NAME`, `BINARY_OP`) for a *made-up* CPU — the Python **virtual machine**. Cached in `__pycache__/*.pyc`. It is **not** machine code; no physical chip can run it directly. |
| **Virtual Machine (VM)** | A program that pretends to be a CPU. CPython's VM is an **evaluation loop** (conceptually `ceval`) that reads one bytecode op and updates a **value stack**. "Interpreting bytecode" = this loop running. |
| **Interpreter** | The whole `python` program: it compiles your source to bytecode, then its VM loop executes that bytecode. Crucially, the interpreter itself is **machine code** (a C program compiled ahead of time). |
| **Machine code** | The binary instructions the physical CPU actually fetches and executes via the [[learning/notes/quick-context/cpu-fetch-execute-cycle|fetch-execute cycle]]. Every execution route ends here — this is where software meets hardware. |

<details>
<summary><strong>How It Works</strong> — The essential mechanism</summary>

### Step 1: source → bytecode (CPython COMPILES, it doesn't "just run")

People say Python is "interpreted," but the first thing CPython does is **compile**. It reads your `.py` text, tokenizes it, parses it into a tree (an AST), and emits **bytecode**: a flat list of tiny instructions for an imaginary machine. That bytecode is cached next to your file as a `.pyc` in `__pycache__/` so it doesn't have to be recompiled next time.

You can see the bytecode with the standard-library `dis` ("disassemble") module:

```python
import dis
dis.dis("a = 2\nb = 3\nx = a + b")
```

```
  1           0 LOAD_CONST    0 (2)     # push 2 onto the value stack
              2 STORE_NAME    0 (a)     # pop, store into name 'a'

  2           4 LOAD_CONST    1 (3)     # push 3
              6 STORE_NAME    1 (b)     # pop, store into 'b'

  3           8 LOAD_NAME     0 (a)     # push value of 'a'  -> stack: [2]
             10 LOAD_NAME     1 (b)     # push value of 'b'  -> stack: [2, 3]
             12 BINARY_ADD              # pop 2, pop 3, push 2+3 -> stack: [5]
             14 STORE_NAME    2 (x)     # pop 5, store into 'x'
             16 LOAD_CONST    2 (None)  # modules implicitly return None
             18 RETURN_VALUE
```

(Opcode names drift between versions: CPython 3.11+ replaced the dedicated
`BINARY_ADD` with a single generic `BINARY_OP` op that carries an argument
saying *which* operator — but the shape is identical. The output above is from
CPython 3.6.)

### Bytecode targets a STACK machine

Notice there are no register names. Every op either **pushes** a value onto a
shared stack or **pops** values off it. `BINARY_ADD` doesn't say "add R1 and R2";
it says "pop the top two, add them, push the result." This is a **stack machine**,
and it's why bytecode is so compact and portable — it assumes nothing about how
many registers a real CPU has.

```
THE VALUE STACK while running  x = a + b   (a=2, b=3)
================================================================================

  op             stack before    ──►  stack after
  ───────────────────────────────────────────────
  LOAD_NAME a    [        ]      ──►  [ 2      ]
  LOAD_NAME b    [ 2      ]      ──►  [ 2, 3   ]
  BINARY_ADD     [ 2, 3   ]      ──►  [ 5      ]      (popped 2 and 3, pushed 5)
  STORE_NAME x   [ 5      ]      ──►  [        ]      (popped 5 into x)
```

### Step 2: the VM loop interprets the bytecode

Bytecode is data, not anything a CPU can run. So *something* has to walk the
list and actually do each op. That something is CPython's **evaluation loop**,
conceptually a giant function called `ceval` ("C eval"). In spirit it is just:

```c
/* conceptual sketch of CPython's bytecode interpreter loop */
for (;;) {
    opcode = *next_instruction++;          /* "fetch" the next bytecode    */
    switch (opcode) {                      /* "decode" — pick the handler  */
        case LOAD_CONST:  push(constant);     break;
        case LOAD_NAME:   push(lookup(name)); break;
        case BINARY_ADD:  { b = pop(); a = pop(); push(a + b); } break;
        case STORE_NAME:  store(name, pop());  break;
        case RETURN_VALUE: return pop();
        /* ...one case per opcode... */
    }
}
```

That `for(;;) { fetch; switch; }` shape should look familiar — it is a
**software re-creation of the [[learning/notes/quick-context/cpu-fetch-execute-cycle|fetch-execute cycle]]**, but the
"instructions" are Python bytecodes and the "registers" are the value stack.
This loop *is* the virtual machine.

### Step 3 — THE KEY RECURSION: the VM is itself machine code

Here is the move that confuses everyone the first time. The VM loop above is
written in C. Before you ever ran `python`, that C was compiled **ahead of
time** by a C compiler into real CPU machine code, producing the `python`
executable on your disk. So when you run a Python script:

```
WHO ACTUALLY EXECUTES WHAT
================================================================================

  your_script.py   ── compiled by CPython ──►   bytecode (.pyc)
                                                    │
                                                    │  is DATA read by...
                                                    ▼
  the `python` executable  ◄── this is REAL MACHINE CODE, made earlier by a
   (CPython's VM loop)          C compiler, running on the CPU right now
                                                    │
                                                    │  its fetch-execute cycle
                                                    ▼
  the physical CPU  ── fetch-execute the VM loop's machine code, which in turn
                       walks your bytecode op by op
```

So your Python bytecode is executed **by machine code** (the interpreter)
running on the CPU. The CPU never sees a single Python bytecode — it only ever
sees the interpreter's own machine instructions. Your bytecode is just *data*
that the interpreter's machine code happens to be chewing through.

</details>

<details>
<summary><strong>The Key Tension</strong> — What practitioners argue about</summary>

### Translate everything up front, or translate as you go?

Every language picks a strategy for getting from source to running on the CPU,
trading **startup/portability** against **raw speed**. There are four main
routes, but they all converge on the same destination: machine code in the CPU.

```
FOUR ROUTES FROM SOURCE TO THE CPU  (all end at the same place)
================================================================================

  (1) COMPILED  AHEAD-OF-TIME     C, Rust, Go, Swift
      source ──► assembly ──► MACHINE CODE ──────────────────────► CPU
      (no interpreter at runtime; the CPU runs your code directly)

  (2) INTERPRETED / BYTECODE      CPython, Ruby (MRI)
      source ──► bytecode ──► [ VM loop ] ──► machine code of the VM ──► CPU
                              (the VM loop is itself AOT-compiled C)

  (3) JIT COMPILED                PyPy, Java HotSpot, JS V8, .NET
      source ──► bytecode ──► interpret at first; for HOT (frequently-run)
                 code, COMPILE that bytecode to MACHINE CODE at runtime ──► CPU
                 (fast paths skip the VM loop entirely after warm-up)

  (4) TRANSPILED                  TypeScript ──► JavaScript, Babel
      source ──► OTHER SOURCE (still high-level!) ──► then needs route 2/3
      (a transpiler does NOT reach the CPU; an engine below it still must)
```

| Route | Translated when | Runs on CPU as | Trade |
|-------|-----------------|----------------|-------|
| **Compiled (AOT)** | Before running | Your code, as machine code | Fastest exec; slow build; one binary per CPU type |
| **Interpreted/bytecode** | Source→bytecode up front, then a loop | The *interpreter's* machine code | Portable + fast startup; per-op loop overhead is slow |
| **JIT** | Bytecode→machine code *during* run, for hot paths | Mostly machine code after warm-up | Near-compiled speed; warm-up cost + memory + complexity |
| **Transpiled** | Source→other source | Whatever the target language runs as | Just shifts the problem down one language; needs an engine |

The real argument: **CPython chooses simplicity and portability over speed.**
Its plain VM loop spends most of its time on per-instruction bookkeeping rather
than your actual arithmetic — which is exactly why **PyPy** (a JIT) and tools
like Cython or Numba exist: they push hot Python down route (1) or (3) to get
machine code on the fast path. But none of them changes the destination; they
only change *when* and *how much* gets turned into machine code.

</details>

<details>
<summary><strong>Concrete Example</strong> — What this looks like in practice</summary>

### `x = 2 + 3` — and the surprise that CPython folds it

Run this and you get a result that teaches an important lesson:

```python
import dis
dis.dis("x = 2 + 3")
```

```
  1           0 LOAD_CONST    3 (5)     # <-- the 5 is ALREADY computed!
              2 STORE_NAME    0 (x)
              4 LOAD_CONST    2 (None)
              6 RETURN_VALUE
```

There is no `BINARY_ADD` at all. Because both operands are **literal constants**,
the CPython compiler does **constant folding** at compile time: it adds `2 + 3`
*while compiling* and bakes the literal `5` straight into the bytecode. The
addition never happens at runtime. This is why the "How It Works" example used
variables (`x = a + b`) — only then can you actually see `BINARY_ADD`/`BINARY_OP`
in the bytecode, because the compiler can't know `a` and `b` ahead of time.

So the honest picture of `x = 2 + 3` is:

```
  SOURCE          COMPILE-TIME            BYTECODE              RUNTIME
  ──────          ─────────────           ────────              ───────
  x = 2 + 3  ──►  fold 2+3 into 5    ──►  LOAD_CONST 5     ──►  VM loop pushes 5,
                  (no add at runtime)     STORE_NAME  x         stores into x
```

### Map to the toy model in this repo (Nand2Tetris)

The same tower appears in the Nand2Tetris course this repo studies, just with a
toy language instead of Python:

```
NAND2TETRIS PIPELINE (the full Part 1 + Part 2 tower)
================================================================================

  Jack (high-level)  ──compiler──►  VM bytecode  ──VM translator──►  Hack assembly
                                                                          │
                                                                     assembler
                                                                          ▼
                                                                  HACK MACHINE CODE
                                                                  (16-bit numbers)
                                                                          │
                                                                          ▼
                                                            the hardware CPU runs it
```

**Honest scope note:** this repo only contains **Part 1 (the hardware)** —
gates, ALU, registers, RAM, and the CPU. The compiler, VM translator, and
assembler are **Part 2**, which is not in this repo. But Part 1 *does* contain
the thing every route in this note ultimately targets: a CPU that fetch-executes
machine code. That CPU is real, runnable Python at
`learning/references/courses/python-nand-to-tetris-part-1/src/hardware/computer/cpu.py`.
Its very first act mirrors a real CPU's decode — split the instruction on its top
bit with a single gate:

```python
# cpu.py — the instruction's top bit decides address-load vs. compute
is_compute_instruction = op_code            # top bit = 1 -> C-instruction
is_address_instruction = self.not_gate(op_code)   # top bit = 0 -> A-instruction
```

No `if opcode == "ADD"` anywhere — the bits *are* the control wires (see
[[learning/notes/quick-context/cpu-fetch-execute-cycle|the fetch-execute note]] for the full trace of how
`D=D+A` becomes mux/ALU selects). Whether the machine code came from Jack via the
full Part-2 chain, from C via gcc, or is the compiled `python` interpreter
itself, **this `cpu.py`-style fetch-execute is the bottom of the tower.**

**The one thing most outsiders get wrong about this is...** thinking "Python is
interpreted" means there is no compilation. There absolutely is — CPython
compiles your source to bytecode every time (caching it in `.pyc`). What's
"interpreted" is the *bytecode*, by the VM loop. And that VM loop is not magic
either: it's a C program that was **compiled ahead of time to machine code**.
"Interpreted vs. compiled" isn't a property of a language, it's a property of an
implementation — and underneath *every* implementation, the CPU is still just
fetch-executing machine code.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[learning/notes/quick-context/cpu-fetch-execute-cycle]]** — The destination of this whole pipeline. The VM loop here is a software re-creation of this hardware loop; the real CPU runs the *interpreter's* machine code via this exact cycle. The down-link toward hardware.

- **[[learning/notes/quick-context/code-to-gates-and-bootstrapping]]** — The fuller picture: the complete 7-layer chain from a high-level statement all the way down to NAND gates and transistors, plus how machine code is encoded by an assembler and how the first compiler was bootstrapped. This note zooms in on the Python-specific top of that chain; that note shows the whole descent.

- **[[learning/notes/quick-context/how-source-code-is-stored]]** — The up-link: how the `.py` text (and the `.pyc` bytecode cache) physically exist as bytes on disk before any of this translation begins. *(sibling note — may not exist yet.)*

- **[[learning/notes/quick-context/from-code-to-running-firmware]]** — The compiled-AOT route in detail for embedded targets: how machine code is placed at real addresses by the linker, flashed to a chip, and reached at the reset vector. The mirror image of Python's runtime route.

- **[[learning/notes/quick-context/firmware]]** — What the AOT-compiled machine code *is* on a real chip: instructions sitting in flash that the CPU fetch-executes from power-on. The `python` interpreter is the desktop analog — machine code that, once running, interprets your bytecode.

- **AST (Abstract Syntax Tree)** — The tree the compiler builds between parsing your source and emitting bytecode. The `ast` module lets you inspect it; it's where structure (loops, expressions, scope) is captured before flattening to a stack-machine op list.

- **JIT compilation (PyPy, V8, HotSpot)** — Route (3): profiling which bytecode runs hot, then compiling just those paths to machine code at runtime to skip the VM loop's overhead. Where interpreted and compiled blur together.

- **GIL / reference counting** — Other things the CPython VM loop does between ops (memory management, the Global Interpreter Lock) that make the per-instruction overhead — and Python's single-core threading limits — what they are.

- **[[learning/notes/index/how-a-computer-works-index]]** — The hub: the full ladder from electricity to running code. This note sits on the software side of rung L8/L10, explaining how a high-level language reaches the machine code that L8's CPU executes.

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** Is Python "compiled" or "interpreted"? What actually happens when you run a `.py` file?
<details>
<summary>Answer</summary>
Both, in stages. CPython first **compiles** your source to **bytecode** (caching it in `__pycache__/*.pyc`), then its VM loop **interprets** that bytecode. So compilation definitely happens — just not to CPU machine code. "Interpreted vs. compiled" is a property of the *implementation*, not the language. See: How It Works (Step 1) and Concrete Example (the misconception).
</details>

**Q2:** Bytecode like `LOAD_CONST` and `BINARY_ADD` — what kind of machine is it written for, and how does that machine differ from a register-based CPU?
<details>
<summary>Answer</summary>
It targets a **stack machine** (the CPython virtual machine). Instead of naming registers, every op pushes values onto, or pops them off, a shared value stack: `BINARY_ADD` pops the top two values and pushes their sum. A real CPU is typically register-based (the Hack CPU has A/D registers). The stack model is more compact and portable because it assumes nothing about how many registers the physical CPU has. See: How It Works (THE VALUE STACK).
</details>

**Q3:** If the CPU can't run Python bytecode, what is actually executing on the CPU while a Python program runs?
<details>
<summary>Answer</summary>
The **`python` interpreter's own machine code**. CPython's VM loop is a C program that was compiled ahead of time into a real executable. The CPU fetch-executes *that* machine code, and the loop in turn walks your bytecode op by op, treating it as data. The CPU never sees a Python bytecode — only the interpreter's machine instructions. See: How It Works (Step 3, the key recursion).
</details>

**Q4:** You disassemble `x = 2 + 3` and there's no `BINARY_ADD` — just `LOAD_CONST 5`. Did the disassembler lie?
<details>
<summary>Answer</summary>
No — CPython did **constant folding** at compile time. Because both operands are literal constants, the compiler computed `2 + 3 = 5` while compiling and baked the literal `5` into the bytecode, so the addition never runs at runtime. To see an actual `BINARY_ADD`/`BINARY_OP` you must use values the compiler can't know in advance, e.g. variables (`x = a + b`). See: Concrete Example (the surprise that CPython folds it).
</details>

**Q5:** A JIT (PyPy), a transpiler (TypeScript→JavaScript), and an AOT compiler ([[quick-context/rust|Rust]]) all process source very differently. What is the single thing they nonetheless share, and where does this repo's code prove it?
<details>
<summary>Answer</summary>
They all **bottom out in machine-code instructions the CPU fetch-executes** — that's the fixed meeting point of the software and hardware towers. AOT compiles straight to machine code; the bytecode VM runs the interpreter's machine code; a JIT compiles hot paths to machine code at runtime; a transpiler just produces more source that still needs an engine (which itself ends in machine code). The repo proves the destination exists: `learning/references/courses/python-nand-to-tetris-part-1/src/hardware/computer/cpu.py` is a runnable CPU that fetch-executes machine code — the same target every route hands its output to. See: The Key Tension (four routes) and Concrete Example (Nand2Tetris mapping + cpu.py).
</details>

</details>
