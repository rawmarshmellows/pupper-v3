---
topic: Keypress to Pixel — The Full Path from a Key to a Letter on Screen
created: 2026-06-07
---

# Keypress to Pixel — The Full Path from a Key to a Letter on Screen

> **Related:** [[learning/notes/index/how-a-computer-works-index]] | [[learning/notes/quick-context/switches-to-registers-storing-data]] | [[learning/notes/quick-context/cpu-fetch-execute-cycle]] | [[learning/notes/quick-context/firmware]] | [[micro-context/microcontroller|Microcontroller]]

> **TL;DR:** Pressing a key closes a tiny mechanical switch (a physical 1/0), and that single bit travels up a chain of ever-more-abstract layers — matrix scan, scancode, USB packet, CPU interrupt, keymap lookup, character code, application code, font glyph, framebuffer in RAM, display scan-out — until the display lights up a pattern of pixels shaped like the letter. This note is the **capstone**: it ties the whole "how a computer works" ladder together, from a switch making a bit at the bottom to a list of instructions (code) running on the CPU deciding what to draw at the top.

## The Core Problem

A computer is, at bottom, just switches that are either on or off — there is no "letter A" anywhere in the silicon. Yet you press a key and an "A" appears on a glowing screen made of millions of independent dots. The whole reason every lower rung of this ladder exists — switches, registers, RAM, buses, the fetch-execute cycle, interrupts, protocols, firmware — is to bridge that gap: to turn one physical contact into a meaningful symbol and then back into a physical pattern of light. If you understand this one end-to-end path, you understand what a computer fundamentally *is*: a machine that moves a bit up through layers of meaning and back down into the physical world.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Scancode** | The raw number the keyboard sends identifying *which physical key* changed — not which letter. Key "A" sends the same scancode whether or not Shift is held; meaning is added later. |
| **Interrupt** | A hardware signal that yanks the CPU away from whatever it was doing to handle an urgent event ("a key arrived"). The alternative — constantly asking "any key yet?" — would waste the entire CPU. See [[learning/notes/quick-context/firmware|firmware]]. |
| **Keymap** | A lookup table (held in the OS) that translates a scancode + modifier state (Shift, layout) into a **character code** like ASCII/Unicode. This is where "physical key" becomes "letter." |
| **Framebuffer** | A region of RAM (an array of memory cells = scaled-up [[learning/notes/quick-context/switches-to-registers-storing-data|registers]]) holding one value per pixel. Writing here is how software "draws"; the display controller reads here to emit light. |
| **Glyph** | The picture of a character, stored in a font. Rendering means looking up the glyph for a character code and copying its pixel pattern into the framebuffer. |

<details>
<summary><strong>How It Works</strong> — The full pipeline, rung by rung</summary>

The journey of one keystroke is a relay race up an abstraction ladder and back down. Each handoff turns the signal into something slightly more abstract, until at the very top a **list of instructions running on the CPU** (software) decides "draw this," and then the chain runs back down into physical light.

```
KEYPRESS -> PIXEL : THE FULL ABSTRACTION LADDER
================================================================================

  PHYSICAL WORLD          MEANING / SOFTWARE        PHYSICAL WORLD
  (a bit is born)         (the CPU runs code)       (the bit becomes light)
  ---------------         -------------------       -----------------------

  finger
    |
    v
  [1]  key switch closes ........... a physical switch = a 1/0   <-- BOTTOM ANCHOR
    |                                (same idea as a toggle
    |                                 switch storing a bit)
    v
  [2]  keyboard matrix scan ........ rows x columns; which
    |                                 wire crossing shorted?
    v
  [3]  debounce (keyboard MCU) ..... contact bounces ~ms;
    |                                 ignore the chatter
    v
  [4]  encode -> SCANCODE .......... a number naming the KEY
    |                                 (not yet a letter)
    v
  [5]  wrap in USB/HID packet ...... or, on a simple board,
    |                                 write a memory-mapped
    |                                 keyboard register
    v
  ====== TRANSPORT (a protocol carries the bits) ======
    |
    v
  [6]  USB/serial -> host ctrlr .... UART/USB framing, error
    |                                 checks, addressing
    v
  [7]  host raises an INTERRUPT .... "CPU! stop! a key!"
    |
    v
  ====== THE CPU RUNS CODE (fetch-execute) ======
    |
    v
  [8]  interrupt handler reads ..... firmware/OS code reads
    |    the scancode                 the scancode value
    v
  [9]  KEYMAP: scancode -> char .... table lookup +
    |                                 Shift/layout -> 'A'
    |                                 (ASCII 65 / Unicode U+0041)
    v
  [10] OS delivers char to the ..... routed to the focused
    |    focused application          window
    v
  [11] app CODE decides to show .... a list of instructions,
    |    it (fetch-execute loop)      running, chooses to draw
    v
  ====== RENDER BACK DOWN INTO THE PHYSICAL WORLD ======
    |
    v
  [12] char -> GLYPH (font) ........ look up the picture of 'A'
    |
    v
  [13] glyph pixels -> FRAMEBUFFER . write values into a
    |    (a region of RAM)            region of memory cells
    v
  [14] GPU / display ctrlr ......... scans the framebuffer out
    |    scans framebuffer            row by row, 60x/sec
    v
  [15] display refresh lights ...... LCD/OLED pixels emit        <-- TOP-DOWN:
       the pixels                     the letter                  code decided,
    |                                                             light obeys
    v
   you see "A"
```

**Walking each stage in plain language:**

1. **Switch closes (a bit is born).** Under each key is a switch. Pressing it shorts two contacts together — exactly the [[learning/notes/quick-context/switches-to-registers-storing-data|switch-makes-a-bit]] idea at the very bottom of this ladder. Open = 0, closed = 1. That is the *entire* physical input: one bit.

2. **Matrix scan.** Keyboards do not run one wire per key (that would be ~100 wires). Keys sit at the crossings of a grid of rows and columns. A small chip drives one row at a time and reads the columns; a crossing that reads "shorted" tells it *which key* is down. This is cheap multiplexing: about $\sqrt{N}$ wires instead of $N$.

3. **Debounce.** A metal contact physically bounces for a few milliseconds, opening and closing several times. The keyboard's [[learning/notes/quick-context/firmware|microcontroller]] waits until the signal is stable so one press is not read as ten.

4. **Encode to a scancode.** The keyboard chip converts "row 3, column 5 just went down" into a **scancode** — a number that names the key. Crucially it is *not* the letter: the key labeled "A" sends the same scancode whether or not Shift is held. Meaning is added much later.

5. **Wrap for transport.** On a PC keyboard the scancode is packed into a **USB HID** packet. On a bare-metal toy or microcontroller, the equivalent step is simply *writing the value into a memory-mapped keyboard register* — a fixed memory address the CPU can read (this is the anchor below, and the kernel of the whole idea).

6. **Transport.** The packet rides a [[learning/notes/quick-context/embedded-communication-protocols|serial protocol]] — [[learning/notes/quick-context/usb-peripheral-hardware|USB]] or [[learning/notes/quick-context/uart|UART]] — across a wire to the host's controller, which handles framing, addressing, and error checks.

7. **Interrupt.** The host controller raises an **interrupt**: a wire to the CPU that says "stop what you're doing, something arrived." Without interrupts the CPU would have to poll ("any key? any key?") forever, wasting nearly all its cycles.

8. **Interrupt handler reads the scancode.** The interrupt diverts the CPU's [[learning/notes/quick-context/cpu-fetch-execute-cycle|fetch-execute cycle]] into a small piece of [[learning/notes/quick-context/firmware|firmware/OS]] code whose job is to read the scancode out of the controller and stash it.

9. **Keymap: scancode -> character.** The OS looks the scancode up in a **keymap** table, combines it with the current modifier state (Shift held? which keyboard layout?), and produces a **character code** — e.g. ASCII 65 / Unicode U+0041 for `A`. *This is the exact rung where "a physical key" becomes "a letter."*

10. **OS delivers the character.** The OS knows which window has keyboard focus and hands the character to that application as an event.

11. **Application code decides.** The app is itself **a list of instructions running on the CPU** in a fetch-execute loop. Its code decides what to do with the character — a text editor appends it to a buffer and asks to redraw. *This is the top of the ladder: code, deciding.*

12. **Character -> glyph.** To display the letter, software looks up its **glyph** in a font: the actual picture of `A` as a small grid of pixels (or a vector outline rasterized to pixels).

13. **Glyph -> framebuffer.** The renderer copies the glyph's pixels into the **framebuffer** — a region of RAM with one value per screen pixel. RAM is just an enormous array of memory cells, which are [[learning/notes/quick-context/switches-to-registers-storing-data|scaled-up registers]]. "Drawing" literally means *writing numbers into memory addresses*.

14. **Scan-out.** A GPU / display controller continuously reads the framebuffer in order, ~60 times a second, and streams the pixel values to the panel.

15. **Refresh.** The LCD/OLED turns each value into light. The pattern that began as one closed switch is now a glowing `A`.

**The two ends meet the spine's anchors.** At the **bottom**, a switch making a bit (rung [1]) is the same physics as a toggle switch storing a 1. At the **top**, code — a list of instructions running fetch-execute (rungs [8]-[11]) — decides what to draw. Everything in between exists only to carry that bit up into meaning and back down into light.

</details>

<details>
<summary><strong>The Key Tension</strong> — Where does "meaning" get added, and who pays for it?</summary>

The central design tension of this whole pipeline is **how late to add meaning**, and **interrupts vs. polling** for moving the data.

**Add meaning late (scancodes), not early.** The keyboard could, in principle, send the letter `A` directly. Almost no general-purpose keyboard does. Instead it sends a meaningless **scancode** and lets the host's keymap decide what it means. Why? Because "what key X means" depends on context the keyboard cannot know: the user's layout (QWERTY vs. AZERTY vs. Dvorak), whether Shift/Ctrl/Alt are held, and what the focused app wants. Keeping the keyboard "dumb" and pushing meaning up to software makes one keyboard work for every language and every app. The cost is more layers and more lookups.

| Approach | Where meaning is added | Pro | Con |
|----------|------------------------|-----|-----|
| **Dumb keyboard + keymap (standard)** | Host OS | One keyboard fits all layouts/apps; remappable in software | More layers, more latency |
| **Smart keyboard sends letters** | Keyboard firmware | Fewer host layers | Locked to one layout; cannot remap; per-app behavior impossible |

**Interrupts vs. polling.** Once the bit reaches the host it must reach the CPU. Two ways:

| Approach | How | Pro | Con |
|----------|-----|-----|-----|
| **Interrupt-driven** | Hardware signals the CPU on arrival | CPU does real work until a key actually comes | Needs interrupt hardware + handler code |
| **Polling** | CPU repeatedly reads the keyboard register | Dead simple; great for tiny bare-metal toys | Wastes nearly all CPU cycles spinning |

The toy Hack computer (anchor below) **polls** a memory-mapped keyboard register; real PCs use **interrupts**. Same destination, different cost model. There is also a rendering tension — *immediate* drawing (write straight to the framebuffer) vs. *double-buffered* drawing (build off-screen, then swap) to avoid tearing — but the core lesson is identical: every layer trades simplicity against flexibility and speed.

</details>

<details>
<summary><strong>Concrete Example</strong> — The toy machine where keyboard + screen are just RAM addresses</summary>

The simplest possible version of this entire pipeline is the **Hack computer** from *Nand to Tetris*, implemented in this repo. There, the keyboard and the screen are not exotic devices — they are just **fixed regions of the memory address space**. Reading "the keyboard" means reading one memory address; "drawing a pixel" means writing one bit to another memory address. This is the *kernel* of the real pipeline, stripped of all the protocol machinery.

The standard Hack `Memory` unit lays its 15-bit address space out like this:

```
HACK MEMORY MAP (the kernel of the whole pipeline)
================================================================================

  address range        what lives there       role in the pipeline
  -------------        ----------------       --------------------
  0     .. 16383       general RAM            variables, the stack
  16384 .. 24575       SCREEN (framebuffer)   1 bit per pixel; write here
        (0x4000)                              = draw  (rungs [12]-[13])
  24576 (0x6000)       KEYBOARD register      holds the code of the key
                                              currently down, 0 if none
                                              (rung [5]; the toy stores an
                                              ASCII code, collapsing 4 & 9)
```

In this repo's implementation, `Memory.__call__` is built from **two stacked 16K RAM chips** selected by the top address bit (`address0`). That top-bit split *is* the address decoder — the exact mechanism the full Hack machine uses to route an address to RAM vs. Screen vs. Keyboard:

```python
# learning/references/courses/python-nand-to-tetris-part-1/
#   src/hardware/computer/memory.py  (DO NOT EDIT -- cited for accuracy)

def __call__(self, a0, ..., a15, load, address0, ..., address14):
    # The top address bit (address0) selects which 16K block.
    # In the FULL Hack machine this same decode picks RAM / Screen / Keyboard.
    load_a, load_b = self.dmux_gate(load, address0)    # route the write
    ram_a = self.ram16K_chip_a(a0, ..., a15, load_a, address1, ..., address14)
    ram_b = self.ram16K_chip_b(a0, ..., a15, load_b, address1, ..., address14)
    result = self.mux16_gate(*ram_a, *ram_b, address0)  # select the read
    return result
```

Note an honest caveat about this *specific* implementation: its accompanying test (`tests/src/hardware/computer/test_memory.py`) states it **deliberately implements only the RAM portion**, not the Screen/Mouse devices ("it is modified as the test script takes into account tests on mouse and screen which we are not implementing"). So what you see here is the bare address-decode skeleton; the full Hack architecture extends this *same* `Memory` unit by making the high block respond as Screen and one address respond as Keyboard. The mechanism — *a single address bit dmux/mux routing reads and writes to different physical things* — is identical, and it is exactly how a real machine maps a peripheral into memory.

**How a Hack program would run our whole pipeline:** poll the keyboard address; when it is non-zero a key is down (rungs [1]-[7] collapsed into one register read); use it as a character; write the matching glyph's bits into the SCREEN region (rungs [12]-[13]); the simulated display scans those bits out (rungs [14]-[15]). Twelve real-world rungs become "read one address, write some others" — which is precisely why this toy is the right Rosetta stone for the whole climb. (One simplification to keep honest: the Hack keyboard register already holds an **ASCII code**, e.g. 65 for `A`, and 0 when no key is down — so the toy quietly fuses the scancode step [4] and the keymap step [9] into one. A real keyboard sends a raw scancode and the OS does the keymap lookup separately.)

**The one thing most outsiders get wrong about this is...** thinking the keyboard "sends the letter A." It does not. It sends a meaningless **scancode** naming a *key*; the letter is manufactured later by the host's keymap from scancode + Shift + layout. Equally, people imagine the screen has letters in it — it does not. The screen is a dumb grid of dots; the framebuffer is just numbers in RAM, and "drawing" is just writing those numbers. There is no `A` anywhere — only a switch's bit at the bottom and code choosing a pixel pattern at the top.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — The rungs this capstone ties together</summary>

- **[[learning/notes/index/how-a-computer-works-index]]** — The hub for the whole "electricity up to code executing" ladder; this note (L11) is its capstone.
- **[[learning/notes/quick-context/switches-to-registers-storing-data]]** — The bottom anchor: a switch makes a bit, flip-flops store it, registers/RAM are scaled-up versions — i.e. both the key switch (rung 1) and the framebuffer (rung 13).
- **[[learning/notes/quick-context/cpu-fetch-execute-cycle]]** — The engine that runs the interrupt handler, the keymap lookup, and the application's drawing code (rungs 8-11). *(sibling — may not exist yet)*
- **[[learning/notes/quick-context/ram-addressing-decoder]]** — How an address selects one cell; the top-bit dmux/mux in the anchor is exactly this, and it is what makes a memory-mapped keyboard/screen possible. *(sibling — may not exist yet)*
- **[[learning/notes/quick-context/data-bus-and-arbitration]]** — How bytes actually travel between CPU, memory, and peripherals on shared wires. *(sibling — may not exist yet)*
- **[[learning/notes/quick-context/uart]]** — A bare serial transport; the simplest version of "carry the scancode over a wire" (rung 6).
- **[[learning/notes/quick-context/usb-peripheral-hardware]]** — How a real PC keyboard's HID packets reach the host (rungs 5-6).
- **[[learning/notes/quick-context/embedded-communication-protocols]]** — The general menu of buses (UART/[[micro-context/spi|SPI]]/[[micro-context/i2c|I2C]]/USB) that move bytes between chips.
- **[[learning/notes/quick-context/firmware]]** — The keyboard MCU's code (scan/debounce/encode) and the host's interrupt handler are both firmware.

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** When you press the "A" key, what does the keyboard actually send to the computer — the letter `A`, or something else?
<details>
<summary>Answer</summary>
Something else: a **scancode**, a number that names *which physical key* changed. It is the same scancode whether or not Shift is held. The letter `A` is produced much later by the host's keymap. See: How It Works, rung 4; and "The one thing most outsiders get wrong."
</details>

**Q2:** Why does the host raise an **interrupt** when a key arrives instead of just checking the keyboard over and over?
<details>
<summary>Answer</summary>
Constantly checking (polling) would burn nearly all the CPU's cycles spinning on "any key yet?" An interrupt lets the CPU do useful work and only stops to handle a key when one actually arrives. See: The Key Tension (interrupts vs. polling). Tiny bare-metal toys like the Hack computer *do* poll, because simplicity matters more than wasted cycles there.
</details>

**Q3:** At which exact rung does "a physical key" turn into "a letter," and at which rung does "a letter" turn back into "physical light"? Name what the bit is at each end.
<details>
<summary>Answer</summary>
"Physical key -> letter" happens at the **keymap** (rung 9): a scancode + Shift/layout becomes a character code like ASCII 65. "Letter -> light" happens at **display refresh** (rung 15), after the glyph has been written into the framebuffer (rung 13) and scanned out (rung 14). At the very bottom the bit is *a closed switch* (rung 1); at the very top it is *code choosing what to draw* (rung 11). See: How It Works, "The two ends meet the spine's anchors."
</details>

**Q4:** A friend says "the framebuffer is where the computer stores the letters that are on screen." Why is that wrong, and what does the framebuffer actually store?
<details>
<summary>Answer</summary>
There are no "letters" in the framebuffer — it stores **pixel values**, one per screen dot, in a region of RAM (i.e. scaled-up [[learning/notes/quick-context/switches-to-registers-storing-data|registers]]). The letter only exists transiently as a *character code* in the application's data and a *glyph* in the font; rendering flattens that glyph into raw pixel values before they hit the framebuffer. The display controller reading the framebuffer has no idea an `A` is there — it just emits dots. See: Concrete Example.
</details>

**Q5:** In the Nand-to-Tetris Hack machine, the keyboard and screen are just memory addresses, yet a real PC has USB controllers, interrupts, and a GPU. What is the single shared mechanism that makes both work, and why is the toy a faithful kernel of the real thing?
<details>
<summary>Answer</summary>
The shared mechanism is **memory-mapped I/O via address decoding**: a peripheral is reachable by reading/writing a fixed address, and a decoder routes that address to the right physical thing. In the repo's `Memory`, the top address bit (`address0`) dmux/mux-routes reads and writes between two RAM blocks — the same decode the full Hack machine uses to pick RAM vs. Screen vs. Keyboard. A real PC adds protocol transport (USB), interrupts (instead of polling), and a GPU for fast scan-out, but the *core idea* — "a device is an address; talking to it is reading/writing memory" — is identical. The toy strips away the transport and leaves the kernel. See: Concrete Example; and [[learning/notes/quick-context/ram-addressing-decoder]].
</details>

</details>
