---
topic: How Source Code Is Stored — Text, Encoding, and Bytes in Memory
created: 2026-06-07
---

# How Source Code Is Stored — Text, Encoding, and Bytes in Memory

> **Related:** [[learning/notes/quick-context/code-to-gates-and-bootstrapping]] | [[learning/notes/quick-context/from-code-to-running-firmware]] | [[learning/notes/quick-context/python-to-machine-code-pipeline]] | [[learning/notes/micro-context/clock-source]] | [[learning/notes/quick-context/physics-of-writing-data-to-memory]]

> **TL;DR:** A source file like `hello.py` is not magic — it is plain **text**, a sequence of characters. Each character is turned into one or more **bytes** by an **encoding** (ASCII for the basics, UTF-8 in practice), and those bytes are stored exactly like any other data: as numbers in addressable memory (a file on disk/flash, copied into [[learning/notes/quick-context/ram-addressing-decoder|RAM]] when you open it). The big idea is **code is data** — the same bytes-in-memory mechanism holds your text, the compiled artifact, and the final machine code. Nothing about the bytes themselves makes them "code"; that depends only on how they are later interpreted or executed.

## The Core Problem

Before a single thing gets *compiled* or *run*, your program has to *exist somewhere* as a concrete object you can save, copy, and reopen. If a "program" were some special intangible substance, there would be no way to email it, store it on a disk, or load it into memory. The resolution is almost anticlimactic: a program-on-disk is just **text encoded as bytes**, and bytes are just numbers living in the same addressable memory cells that hold everything else. This is rung **B1** — the bottom of the SOFTWARE tower — and it answers "what *is* a program before any of the clever transformation happens?" Later rungs ([[learning/notes/quick-context/python-to-machine-code-pipeline|the pipeline]], [[learning/notes/quick-context/code-to-gates-and-bootstrapping|compilation to gates]]) take these bytes and transform them; B1 is about the raw starting material and where it sits.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Character** | A single abstract symbol a human reads — a letter (`x`), a digit (`2`), a space, a `+`, or an invisible control mark like newline. A text file is a *sequence* of these. |
| **Byte** | A group of 8 bits, holding a number from 0 to 255 (`0x00`–`0xFF`). The smallest unit memory and disks address. Everything stored is ultimately a string of bytes. |
| **Encoding** | The agreed-upon lookup table that maps each character to one or more byte values (and back). **ASCII** covers the basic 128 symbols in 1 byte each; **UTF-8** extends this to every Unicode character using 1–4 bytes, while staying byte-for-byte identical to ASCII for the basics. |
| **Plain text** | A file that *is* just the encoded characters, with no hidden formatting — exactly what an editor shows you, glyph for glyph. Source code is plain text; a `.docx` or `.png` is not. |
| **Code is data** | The reframe at the heart of B1: source text, compiled output, and runnable machine code are *all* just bytes in the same kind of [[learning/notes/quick-context/ram-addressing-decoder|addressable memory]]. What makes some bytes "code" is only that something later *interprets or executes* them. |

<details>
<summary><strong>How It Works</strong> — From a glyph you see to a number in a memory cell</summary>

### Step 1 — A source file is a sequence of characters

Open `hello.py` in an editor and you see glyphs: `x`, ` `, `=`, ` `, `2`, ` `, `+`, ` `, `3`, and then the line ends. That last "end of line" is itself a character — the **newline** (`\n`) — even though it has no visible glyph. So the *line* `x = 2 + 3` is really nine characters in a row:

```
character:   x   ' '   =   ' '   2   ' '   +   ' '   3   \n
position:    0    1    2    3    4    5    6    7    8    9
             └────── the visible line is 9 chars ──────┘   └ \n = 10th
                     (' ' = a space character)
```

The editor's whole job is to *render* each character as a shape on screen. But the file is the *characters*, not the shapes.

### Step 2 — An encoding turns each character into byte values

A memory cell or a disk can only hold numbers, not "the idea of the letter x." So we need a fixed table that says "the character `x` is the number 120, the character `+` is 43," and so on. That table is the **encoding**. The original table is **ASCII**, which assigns the 128 basic characters to the numbers 0–127, each fitting in a single byte.

Here is the line `x = 2 + 3\n` run through ASCII. (Spaces are character 32; `\n` is 10. These are the *same* numbers in UTF-8 — the basic characters are identical.)

```
char :    x     ' '     =     ' '     2     ' '     +     ' '     3      \n
        ─────  ─────  ─────  ─────  ─────  ─────  ─────  ─────  ─────  ─────
dec  :   120     32     61     32     50     32     43     32     51     10
hex  :  0x78   0x20   0x3D   0x20   0x32   0x20   0x2B   0x20   0x33   0x0A
```

So the human-readable line becomes a list of ten byte values. That list of bytes — `78 20 3D 20 32 20 2B 20 33 0A` in hex — *is* the file's contents.

### Step 3 — A conceptual hexdump

A "hexdump" is just a tool that shows you a file's raw bytes (in hex) next to the characters they decode to. The whole `x = 2 + 3\n` file looks like this:

```
offset    raw bytes (hex)                  decoded chars
────────  ───────────────────────────────  ──────────────
00000000  78 20 3D 20 32 20 2B 20 33 0A     x . = . 2 . + . 3 .
                                            (the "." are the spaces / newline,
                                             which have no printable glyph)
```

Left column: where in the file each chunk starts (the *offset*, like an address). Middle: the actual bytes on disk. Right: what those bytes mean once decoded through the encoding. The bytes are the reality; the glyphs are an interpretation.

### Step 4 — Those bytes live in addressable memory

When the file sits on disk or flash, those ten bytes occupy ten storage locations. When you *open* the file, the operating system copies the bytes into [[learning/notes/quick-context/ram-addressing-decoder|RAM]] — an array of cells, each with a numbered **address**, where you can fetch or store any cell by its number. (How a bit is physically held in a cell — a [[learning/notes/quick-context/voltage|voltage]], a charge, trapped electrons — is [[learning/notes/quick-context/physics-of-writing-data-to-memory|the rung below]].)

```
RAM as a numbered array of byte-cells (the file loaded at address 1000)
================================================================================

  address:  1000 1001 1002 1003 1004 1005 1006 1007 1008 1009
           ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
  byte:    │ 78 │ 20 │ 3D │ 20 │ 32 │ 20 │ 2B │ 20 │ 33 │ 0A │
           └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
  means:     'x'  ' '  '='  ' '  '2'  ' '  '+'  ' '  '3' '\n'

  ── The cells know nothing about Python. They hold ten numbers.
     "It is source code" is a fact about how we will USE them, not
     a property of the cells.
```

This is exactly the model in the Nand-to-Tetris machine: there is **one addressable memory space**, and *everything* — data, text, instructions — is a number in some cell, reached by its address. The `Memory` chip in `learning/references/courses/python-nand-to-tetris-part-1/src/hardware/computer/memory.py` takes an `address` and returns the one word stored there; it has no concept of "this address holds code" vs "this address holds data." Both are just words in the same array. That is the simplest possible "all bytes live in one addressable space" model, and it is the whole point of B1.

</details>

<details>
<summary><strong>The Key Tension</strong> — ASCII vs. UTF-8, and the "code is data" double-edge</summary>

### Tension 1 — Which encoding? ASCII's simplicity vs. UTF-8's universality

ASCII is dead simple: 128 characters, one byte each, no ambiguity. But it only covers English letters, digits, and basic punctuation — no `é`, no `中`, no emoji. The modern default is **UTF-8**, which can encode every character in Unicode (over 150,000 assigned, out of a ~1.1 million code-point space) using a *variable* number of bytes (1 to 4). The brilliance of UTF-8 is that its 1-byte encodings are **byte-for-byte identical to ASCII**, so plain English source code is exactly the same bytes either way — but non-English text and symbols "just work."

| | ASCII | UTF-8 |
|---|---|---|
| Bytes per character | Always 1 | 1 to 4 (variable) |
| Characters covered | 128 (English basics) | All of Unicode (150k+ assigned) |
| `x`, `=`, `2`, `+` encode as | `78 3D 32 2B` | `78 3D 32 2B` (identical) |
| `é` encodes as | impossible | `C3 A9` (2 bytes) |
| Self-synchronizing / ASCII-compatible | n/a | Yes (a superset of ASCII) |
| Today's default for source files | legacy | Yes |

The tradeoff: fixed-width (ASCII, or fixed multi-byte like UTF-32) makes "jump to the Nth character" trivial but wastes space; variable-width (UTF-8) is compact and universal but you can't assume "byte N = character N." For source code — overwhelmingly ASCII characters — UTF-8 gives you the best of both: ASCII-cheap for the common case, universal when you need it.

### Tension 2 — "Code is data" cuts both ways

Treating code as ordinary bytes is what makes compilers, interpreters, editors, and version control possible: a compiler is just a program that *reads bytes* (your source) and *writes other bytes* (the compiled artifact). But the same flexibility is the root of whole classes of security bugs — if attacker-supplied *data* can be made to *execute* as code (buffer overflows, injection, self-modifying malware), the machine happily runs it, because nothing in the bytes distinguishes the two. Hardware and OSes claw some safety back by marking memory regions as "executable" or "not" (the NX / W^X bit), precisely *because* the bytes themselves carry no such label.

</details>

<details>
<summary><strong>Concrete Example</strong> — Seeing the bytes of a real file, and the three artifacts</summary>

### Looking at the actual bytes

You can prove all of this at a terminal. Write the one-line file and dump its bytes:

```bash
$ printf 'x = 2 + 3\n' > hello.py     # write the 10 characters to disk
$ wc -c hello.py                       # how many BYTES?
10 hello.py                            # ← exactly 10, one per character

$ xxd hello.py                         # hexdump: bytes (hex) | decoded chars
00000000: 7820 3d20 3220 2b20 330a              x = 2 + 3.
          └──────── the 10 bytes ────────┘      └ decoded ┘
```

The `.` at the end of the decoded column is the newline (`0a`), which `xxd` can't draw as a glyph. Notice `wc -c` reports **10 bytes** — character count equals byte count *only because every character here is plain ASCII*. Add one accented letter and the byte count would exceed the character count, because UTF-8 spends extra bytes on it:

```bash
$ printf 'café\n' > x.txt
$ wc -m x.txt    # characters: 5  (c, a, f, é, newline)
5 x.txt
$ wc -c x.txt    # bytes: 6       (é is TWO bytes: c3 a9 in UTF-8)
6 x.txt
```

### The three artifacts — keep them straight

B1 is only about artifact (a). It is easy to conflate these three, but they are distinct objects:

```
(a) SOURCE TEXT FILE          (b) COMPILED ARTIFACT          (c) RUNNING PROCESS
    hello.py on disk              hello.pyc / a.out              live in RAM
    ─────────────────             ──────────────────             ───────────────
    Human-readable text,          Bytecode or machine code,      The bytes of (b)
    bytes via an ENCODING.        bytes the runtime/CPU          loaded into RAM and
                                  consumes. Produced FROM (a).   actively EXECUTED,
    78 20 3D 20 32 ...            (different bytes than (a))      plus its data/stack.

              compile / assemble            load + execute
        (a) ──────────────────► (b) ──────────────────► (c)  CPU fetches & runs
              (a later rung)                (a later rung)

   ALL THREE ARE "JUST BYTES IN ADDRESSABLE MEMORY."
   The only difference is who reads them and how.
```

- **(a) Source text** — what you edit. Plain text, this note's whole subject. Lives as a file; loaded into RAM as bytes when opened.
- **(b) Compiled artifact** — the bytecode or machine code produced *from* (a) by a compiler/assembler. *Different bytes* than the source, but still just bytes in a file (see [[learning/notes/quick-context/code-to-gates-and-bootstrapping|code to gates]]).
- **(c) Running process** — artifact (b) loaded into RAM and actually executed by the CPU, with its live data and stack alongside. This is where "code" finally *does* something.

The transformation (a) → (b) → (c) is the SOFTWARE tower above B1; the [[learning/notes/quick-context/python-to-machine-code-pipeline|Python-to-machine-code pipeline]] walks it.

**The one thing most outsiders get wrong about this is...** thinking a source file is somehow a *special kind of object* — that "a program" is fundamentally different from "a document" or "a photo." It is not. `hello.py`, a love letter, and a JPEG are all the same species of thing: a sequence of bytes in a file. The `.py` extension is just a hint to humans and tools; the bytes carry no built-in "I am code" flag. A file becomes "source code" only the moment some *other* program (a compiler or interpreter) chooses to read its bytes that way. Code is data, all the way down.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[learning/notes/quick-context/ram-addressing-decoder]]** — The rung directly below: how "addressable memory" is actually built — an array of registers picked one at a time by a numeric address. The cells your file's bytes land in.
- **[[learning/notes/quick-context/physics-of-writing-data-to-memory]]** — One level deeper still: how a single byte's bits are *physically* held — a voltage in SRAM, a charge in DRAM, trapped electrons in the flash that stores `hello.py` on an SSD.
- **[[learning/notes/quick-context/python-to-machine-code-pipeline]]** — The rung directly above: how the source bytes from B1 get transformed into bytecode and machine code — artifacts (b) and (c).
- **[[learning/notes/quick-context/code-to-gates-and-bootstrapping]]** — The full compilation chain that turns these source bytes all the way down into binary instructions the CPU's gates execute.
- **how a computer works index** — The spine hub: the full ladder from electricity up to running code. This note is B1, the foot of the SOFTWARE tower.
- **Unicode & code points** — The character-numbering standard that UTF-8 encodes; the layer above "which encoding" that defines *which* characters exist in the first place.

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** A source file `hello.py` — what is it, physically, before anything compiles or runs it?
<details>
<summary>Answer</summary>
A sequence of **bytes** stored as a file on disk/flash. Those bytes are the **characters** of the program turned into numbers by an **encoding** (ASCII/UTF-8). It is plain text — exactly the glyphs the editor shows, nothing hidden. See "How It Works," steps 1–2.
</details>

**Q2:** The line `x = 2 + 3` (with no newline) has 9 characters. In ASCII, how many bytes is that, and why?
<details>
<summary>Answer</summary>
9 bytes — one byte per character, because ASCII encodes each of its 128 characters in exactly one byte (and `x`, space, `=`, `2`, `+`, `3` are all ASCII). Add a trailing newline `\n` and it becomes 10 bytes. See the hexdump in "How It Works," step 3.
</details>

**Q3:** Why do `wc -m` (characters) and `wc -c` (bytes) report the *same* number for `hello.py` but *different* numbers for a file containing `café`?
<details>
<summary>Answer</summary>
Because UTF-8 uses 1 byte for ASCII characters but 2–4 bytes for non-ASCII ones. Every character in `hello.py` is ASCII, so characters == bytes. In `café`, the `é` takes **2 bytes** (`C3 A9`), so the byte count exceeds the character count. This is the fixed-vs-variable-width tradeoff. See "The Key Tension," Tension 1, and "Concrete Example."
</details>

**Q4:** Someone says: "Source code is stored in a special part of memory reserved for programs, totally different from where data lives." What's wrong with that claim?
<details>
<summary>Answer</summary>
There is no special "program substance." Source text, compiled artifacts, and running machine code are *all* just bytes in the *same* kind of addressable memory — exactly like any document or image. The Nand-to-Tetris `Memory` chip takes an address and returns a word with no notion of "code" vs "data." Bytes become "code" only when something later *interprets or executes* them; nothing in the bytes themselves marks them. See "How It Works," step 4, and "code is data" in the terms table.
</details>

**Q5:** If the bytes of source code, compiled bytecode, and running machine code are all "just bytes in addressable memory," what actually distinguishes the three artifacts — and why does that distinction matter for security?
<details>
<summary>Answer</summary>
The distinction is **not in the bytes** but in **who reads them and how**: (a) source is read by a compiler/interpreter *as text to translate*; (b) the compiled artifact is read by the runtime/CPU *as instructions to consume*; (c) a running process is those instruction-bytes *actively executed* by the CPU, alongside its live data. Since nothing intrinsic separates "data" from "executable code," an attacker who can get their *data* executed *as code* (injection, buffer overflow) gets the machine to run it. That is exactly why CPUs/OSes add an explicit "this region is executable / not" marker (NX / W^X) — to impose a distinction the bytes don't carry on their own. See "Concrete Example" (three artifacts) and "The Key Tension," Tension 2.
</details>

</details>
