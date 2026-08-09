---
topic: From Human Calculators to Coding on Screens — How Programming Interfaces Evolved
created: 2026-03-26
---

# From Human Calculators to Coding on Screens

> **Related:** [[learning/notes/quick-context/epson-rc-plus-programming]] | [[learning/notes/micro-context/microcontroller]] | [[learning/notes/micro-context/spi]] | [[learning/notes/quick-context/transistor]] | [[learning/notes/quick-context/voltage]]

> **TL;DR:** Computing evolved through five eras of human-machine interfaces: teams of human "computers" doing arithmetic by hand with pencils and desk calculators (1600s-1940s), rewiring plugboards on vacuum-tube machines (1940s), feeding punch cards to stored-program computers (1950s), typing on teletype terminals connected to time-sharing systems (1960s), and editing code on CRT screens with compilers running locally (1970s+). The word "computer" originally meant a *person* — rooms full of people, mostly women, who performed calculations as assembly lines of arithmetic. Electronic computers replaced them because ENIAC could compute a ballistics trajectory in 30 seconds that took a human 20 hours. Today, when you type code on a screen, the keystrokes become characters stored in RAM then saved to disk; the compiler reads that file, translates it through the [[quick-context/code-to-gates-and-bootstrapping|compilation chain]] into machine code, and the OS (or a [[quick-context/firmware|flash programmer]], for embedded systems) loads those binary instructions into memory where the CPU fetches and executes them.

## The Core Problem

You sit in front of a screen, type `x = 2 + 3`, press a button, and your program runs. But the computer is just a pile of [[quick-context/transistor|transistors]] switching on and off — it has no concept of "screens," "keyboards," or "files." Someone had to build every layer between your keystrokes and the CPU's fetch-execute cycle: the keyboard controller that converts key presses to character codes, the operating system that buffers those characters in RAM, the filesystem that persists them to disk, the compiler that translates them to machine code, and the loader that places those instructions where the CPU can find them. Each of these layers was itself [[quick-context/code-to-gates-and-bootstrapping|bootstrapped]] from something simpler, stretching back to an era when "programming" meant physically rewiring cables between [[quick-context/transistor-design-history|vacuum tube]] circuits — and before that, when "computer" meant a *person* sitting at a desk with a pencil and a mechanical calculator.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Stored-Program Computer** | A computer that holds both its instructions and data in the same memory (RAM), allowing programs to be loaded, changed, and replaced without rewiring hardware. The foundational idea (von Neumann, 1945) that made software possible. |
| **Batch Processing** | The dominant computing mode of the 1950s-60s: you submit a deck of punch cards, wait hours, and get results back on a printout. No interaction with the running program. |
| **Time-Sharing** | A technique (1961+) where one computer rapidly switches between multiple users, giving each the illusion of an interactive, dedicated machine. This is what made typing programs on terminals possible. |
| **Terminal** | A keyboard + display device (first teletypes printing on paper, then CRT screens) connected to a computer, allowing real-time interaction. The terminal replaced punch cards as the programming interface. |
| **Operating System** | The master program that manages hardware, files, memory, and user programs. It connects your keystrokes on screen to the compiler and CPU — and was itself [[quick-context/code-to-gates-and-bootstrapping|bootstrapped]] from simpler programs. |

<details>
<summary><strong>How It Works</strong> — Five eras of programming interfaces</summary>

### Era 0: Human Computers (1600s–1940s)

Before electronic computers existed, "computer" meant a **person who computes**. The word first appeared in English around 1613 (Richard Braithwait's *The Yong Mans Gleanings*), and for over 300 years it referred exclusively to humans.

Large-scale computation was organized as **assembly lines of arithmetic**. The model was pioneered by Gaspard de Prony in 1790s France, who — inspired by Adam Smith's pin-factory division of labor — hired 60-80 human computers to produce logarithmic tables for the new metric system. The work was divided into three tiers: a handful of elite mathematicians designed the formulas, a middle group prepared worksheets, and a large group of relatively unskilled workers (many were unemployed hairdressers after the French Revolution) performed simple addition and subtraction following strict written instructions. They didn't need to understand the mathematics — just follow the steps.

This pattern repeated for 150 years:

```
ERA 0: HUMAN COMPUTERS (1600s-1940s)
================================================================================

  "COMPUTER" = a person who computes

  ORGANIZATION (de Prony's 3-tier model, replicated through WW2):

    Tier 1: Mathematicians (5-6 people)
    +------------------------------------------+
    |  Design formulas, choose methods         |
    |  (e.g., method of finite differences     |
    |  reduces complex math to simple addition)|
    +-----------------+------------------------+
                      |  worksheets
                      v
    Tier 2: Skilled planners (7-8 people)
    +------------------------------------------+
    |  Break formulas into step-by-step        |
    |  instructions, prepare calculation forms |
    +-----------------+------------------------+
                      |  instruction sheets
                      v
    Tier 3: Human computers (60-80+ people)
    +------------------------------------------+
    |  Perform simple arithmetic with pencil   |
    |  and desk calculator. Pass result to     |
    |  the next person. No math knowledge      |
    |  needed -- just follow the steps.        |
    +------------------------------------------+

  VERIFICATION: Multiple computers calculate the same problem
  independently. Supervisors compare results to catch errors.

  MECHANICAL AIDS OVER THE CENTURIES:
  -----------------------------------------------------------------
  Abacus             (antiquity)    Beads on rods
  Napier's Bones     (1617)         Multiplication aid
  Slide Rule         (c. 1622)      Logarithmic scales
  Pascaline          (1642)         Mechanical add/subtract
  Leibniz Wheel      (1694)         All four arithmetic operations
  Difference Engine  (1822 design)  Babbage's polynomial evaluator
  Desk Calculators   (early 1900s)  Monroe, Marchant, Friden --
                                    the workhorse of WW2 computing
```

By WW2, human computing had become a major wartime operation:

- **Aberdeen Proving Ground:** ~100-200 women with math degrees computed artillery firing tables. A single ballistics trajectory took **~20 hours** with a desk calculator. A complete firing table (750-1,000 trajectories) took a team weeks to months.
- **Manhattan Project (Los Alamos):** Richard Feynman organized teams of ~20-30 human computers into a "human parallel processor" — each person performed one step and passed the result forward, mimicking what we'd later call pipelining.
- **NACA/NASA (from 1935):** Langley hired women as computers for aeronautics research. The West Area Computers — a segregated group of Black women mathematicians established in 1943 — included Dorothy Vaughan, Katherine Johnson, and Mary Jackson (the "Hidden Figures"). Johnson later calculated trajectories for Mercury and Apollo missions; John Glenn specifically requested she verify the electronic computer's calculations for his 1962 orbital flight.

The word "computer" shifted from person to machine gradually between 1945 and 1955. For a brief period both coexisted — some institutions even spelled the human role "computor" to distinguish it. By the mid-1950s the machine meaning dominated, though human computers continued working at NASA into the 1960s.

**Why the transition happened:** ENIAC computed a ballistics trajectory in **30 seconds** — the same calculation that took a human computer **20 hours**. That's a ~2,400x speedup. The economic case was unanswerable, and the six women selected to program ENIAC were themselves former human computers from Aberdeen (Kay McNulty, Betty Jean Jennings, Betty Snyder, Marlyn Wescoff, Frances Bilas, Ruth Lichterman).

### Era 1: Plugboards and Vacuum Tubes (1940s)

The earliest electronic computers (ENIAC, 1945) had no software at all. "Programming" meant physically reconnecting cables and setting switches to route data through vacuum tube circuits. Each vacuum tube acted as an electronic switch — the ancestor of the [[quick-context/transistor|transistor]] — but they were large (the size of a thumb), hot, power-hungry, and failed frequently. ENIAC had 17,468 vacuum tubes, weighed 30 tons, consumed 150 kW, and filled an entire room.

There was no separation between "program" and "hardware." To change the program, you rewired the machine. This could take days.

```
ERA 1: PLUGBOARD PROGRAMMING (1940s)
================================================================================

  "PROGRAM" = physical wire connections

    +-------------------------------------+
    |  ENIAC Plugboard                    |
    |                                     |
    |    o--wire--o    o--wire--o          |
    |    o        o    o        o          |
    |    o--wire--o    o--wire--o          |
    |    o        o    o        o          |
    |    o--wire--o    o--wire--o          |
    |                                     |
    |  Each wire routes data through a    |
    |  specific sequence of vacuum tube   |
    |  arithmetic units.                  |
    |                                     |
    |  Changing the program = rewiring    |
    |  (takes hours to days)              |
    +-------------------------------------+

  Hardware: ~18,000 vacuum tubes
  Speed:    ~5,000 additions/second
  Input:    Plugboards + switch settings
  Output:   Punch cards or lights
```

### Era 2: Punch Cards and the Stored-Program Revolution (1950s)

The breakthrough was the **stored-program concept** (von Neumann, 1945): store instructions in the same memory as data. Now programs were sequences of numbers in memory, not physical wires. EDSAC (1949) was the first stored-program computer to enter routine service (the Manchester Baby ran a stored program in 1948, but EDSAC was the first used for real work). By the 1950s, vacuum tubes were being replaced by [[quick-context/transistor|transistors]] (first [[learning/notes/quick-context/transistor|transistor]]: 1947; first transistorized computer: Manchester University's 1953 prototype), making machines smaller, more reliable, and cheaper.

But how do you get a program into memory? **Punch cards.** Each card had 80 columns of holes representing characters. A programmer wrote code on paper, a keypunch operator punched it onto cards, the card reader fed them into memory, and hours later you got printed output. This was **batch processing** — no interaction with the running machine.

```
ERA 2: PUNCH CARD BATCH PROCESSING (1950s)
================================================================================

  Write code      Punch cards       Feed to           Wait        Get output
  on paper     +--------------+    computer         (hours)      on printer
     |         | o * o o * o  |       |                |             |
     |         | o o * o o *  |       |                |             |
     v         | * o o * o o  |       v                v             v
  +------+     +--------------+  +----------+    +----------+  +----------+
  |PAPER | -->  Stack of cards -->| CARD     |--->| COMPUTER |->| LINE     |
  |FORM  |      (one per line    | READER   |    | (batch   |  | PRINTER  |
  +------+       of code)        +----------+    |  mode)   |  +----------+
                                                 +----------+

  No interaction while program runs!
  Bug in your code? Fix it -> re-punch -> re-submit -> wait hours again.
```

**But how did holes in cardboard become numbers in memory?** The physical chain had four links:

```
FROM HOLES TO MEMORY — THE PUNCH CARD READ PATH
================================================================================

  1. THE CARD
     80 columns, 12 punch positions per column (rows 12, 11, 0-9).
     Characters encoded by combinations of holes (Hollerith code):
       "A" = holes in row 12 + row 1
       "0" = hole in row 0
       "+" = holes in row 12 + row 8 + row 6

     +------------------------------------------------------+
     | 12 ·  ·  ●  ·  ·  ·  ·  ·  ·  ·  ...  (80 columns) |
     | 11 ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ...               |
     |  0 ·  ·  ·  ●  ·  ·  ·  ·  ·  ·  ...               |
     |  1 ·  ·  ●  ·  ·  ·  ·  ·  ·  ·  ...               |
     |  2 ·  ·  ·  ·  ●  ·  ·  ·  ·  ·  ...               |
     |  3 ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ...               |
     |  . .  .  .  .  .  .  .  .  .  .  ...               |
     |  9 ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ...               |
     +------------------------------------------------------+
       ● = hole punched     · = no hole

  2. THE CARD READER (electromechanical)
     The card is pulled past a "read station" at ~250-1000 cards/minute.
     Two sensing methods were common:

     BRUSH SENSING (IBM 711, IBM 1402):
     +-----------card moving this way--------->-----------+
     |                                                    |
     |    metal brush                                     |
     |       |                                            |
     |       v        card                                |
     |     .-/-.   +---------+                            |
     |     | / |===| ● hole  |=== metal roller behind     |
     |     '-\-'   +---------+                            |
     |                                                    |
     |  Brush presses against the card. Where there's     |
     |  a hole, the brush touches the metal roller ->     |
     |  circuit closes -> current flows -> bit = 1.       |
     |  No hole -> brush blocked by cardboard -> bit = 0. |
     +----------------------------------------------------+

     PHOTOELECTRIC SENSING (faster, later machines):
     +----------------------------------------------------+
     |     light source                                    |
     |       |                                             |
     |       v        card                                 |
     |     [LED]   +---------+                             |
     |     ~~~~~~~ | ● hole  |                             |
     |             +---------+                             |
     |                 |                                   |
     |                 v                                   |
     |            [photocell]                              |
     |                                                     |
     |  Light passes through hole -> photocell fires -> 1  |
     |  Cardboard blocks light -> photocell dark -> 0      |
     +----------------------------------------------------+

     One read station scans all 12 rows of a column simultaneously
     (12 brushes or 12 photocells in a vertical line). The card
     advances column by column, producing 80 characters per card.

  3. CHARACTER ENCODING
     The reader's circuitry converts each column's 12-bit hole
     pattern into the machine's character code:

       Holes in card     ->  Hollerith code  ->  BCD / EBCDIC byte
       (row 12 + row 1)  ->  "A"             ->  0xC1 (EBCDIC)

     Early machines used the card's own Hollerith encoding directly.
     Later machines translated to BCD (6-bit) or EBCDIC (8-bit).
     ASCII came later with time-sharing systems.

  4. INTO MEMORY — THE BOOTSTRAP LOADER
     The card reader placed each character in a hardware buffer
     register. But something had to tell the CPU: "read that
     register and store its contents at memory address X."

     That something was a BOOTSTRAP LOADER — a tiny program
     (often just 20-30 instructions) that performed:

       LOOP:
         Read one character from card reader register
         Store it at current memory address
         Increment memory address
         If more characters, go to LOOP

     But here's the chicken-and-egg: how do you load the loader?

     FRONT PANEL SWITCHES (the real bootstrap):
     +----------------------------------------------------+
     |  FRONT PANEL                                        |
     |  +----------------------------------------------+  |
     |  | ADDR: [↑][↓][↑][↓][↓][↓][↑][↓][↓][↓][↓][↓] | <-- toggle switch
     |  |                                              |  |     per bit
     |  | DATA: [↓][↑][↓][↓][↑][↑][↓][↑][↑][↓][↓][↑] |  |
     |  |                                              |  |
     |  | [DEPOSIT]  [NEXT]  [RUN]                     |  |
     |  +----------------------------------------------+  |
     |                                                    |
     |  1. Set ADDRESS switches to memory location 0      |
     |  2. Set DATA switches to first instruction's       |
     |     binary encoding (e.g., "read card reader")     |
     |  3. Press DEPOSIT (writes data into that address)  |
     |  4. Press NEXT (increments address)                |
     |  5. Repeat for each instruction of the loader      |
     |     (~20-30 instructions, entered by hand)         |
     |  6. Press RUN -> CPU executes from address 0       |
     |     -> loader runs -> reads rest of program from   |
     |        punch cards into memory                     |
     +----------------------------------------------------+

     An operator did this EVERY TIME the machine was powered on.
     Later machines stored the bootstrap in a small read-only
     memory (ROM) so the operator just pressed one LOAD button.

  MEMORY AT THIS TIME: MAGNETIC CORE
  +----------------------------------------------------+
  |  Tiny ferrite rings (~1mm diameter) threaded on a   |
  |  grid of wires. Each ring stores one bit.           |
  |                                                     |
  |        X wire                                       |
  |          |                                          |
  |    ------●------  Y wire                            |
  |          |                                          |
  |        sense wire (diagonal, for reading)           |
  |                                                     |
  |  WRITE 1: Current pulse through X + Y wires        |
  |           magnetizes core clockwise                 |
  |  WRITE 0: Opposite current -> counterclockwise     |
  |  READ:    Send current pulse, detect if core flips  |
  |           (destructive -- must rewrite after read)  |
  |                                                     |
  |  A 4096-word memory = tens of thousands of tiny     |
  |  rings, hand-threaded by workers under microscopes. |
  |  Core memory was the dominant RAM from 1955-1975.   |
  +----------------------------------------------------+
```

So the full path was: **holes in cardboard → brush/photocell electrical signal → character code in buffer register → bootstrap loader copies to magnetic core memory → CPU fetches from same memory to execute.**

The stored-program concept also made [[quick-context/code-to-gates-and-bootstrapping|bootstrapping]] possible: instructions and data were just numbers in the same memory, so a program could read text (assembly mnemonics) and output numbers (machine code) — that's the first assembler. The first assemblers were hand-coded in binary on punch cards.

```
THE STORED-PROGRAM CONCEPT (von Neumann, 1945)
================================================================================

  MEMORY (same for instructions AND data)
  +------+------+------+------+------+------+------+
  | INST | INST | INST | DATA | DATA | DATA | ...  |
  | 0001 | 0010 | 0011 | 0042 | 0007 | 0000 |      |
  +------+------+------+------+------+------+------+

  Instructions and data are just numbers in the same memory.
  The CPU fetches from where the Program Counter points --
  it doesn't "know" the difference. This is what separates
  SOFTWARE from HARDWARE: the program is data, not wiring.
```

### Era 3: Terminals and Time-Sharing — The End of Punch Cards (1960s)

The event that changed everything: **MIT's Compatible Time-Sharing System (CTSS), 1961.** For the first time, multiple users could sit at teletype terminals — keyboard-and-printer devices connected by wire to a central computer — and type commands that executed immediately. No punch cards. No waiting hours. You typed a line of code, the computer responded in seconds.

```
ERA 3: TIME-SHARING AND TERMINALS (1960s)
================================================================================

  +----------+
  | User A   |--+
  | terminal |  |
  +----------+  |     +-----------------------------------+
                |     |  CENTRAL COMPUTER                  |
  +----------+  |     |                                    |
  | User B   |--+---->|  Time-sharing OS rapidly switches  |
  | terminal |  |     |  between users (20-50ms slices)    |
  +----------+  |     |                                    |
                |     |  Each user gets the illusion of    |
  +----------+  |     |  a dedicated, interactive machine  |
  | User C   |--+     |                                    |
  | terminal |        +-----------------------------------+
  +----------+

  TELETYPE TERMINAL (ASR-33, 1963):
  +----------------------------------+
  |  +------------------------+      |
  |  |  Typed: PRINT 2+3      |      |  Keyboard input
  |  |  Output: 5             |      |  printed on paper
  |  |  _                     |      |  (no screen yet!)
  |  +------------------------+      |
  |  +------------------------+      |
  |  |  QWERTYUIOP...        |      |
  |  |  ASDFGHJKL...         |      |
  |  +------------------------+      |
  +----------------------------------+
```

**But how did keystrokes on a teletype become bytes in the computer's memory — and how did output get back to the printer?** This was the first real-time I/O loop, and it required new hardware and software working together:

```
FROM KEYPRESS TO MEMORY — THE TELETYPE I/O PATH
================================================================================

  1. THE KEYBOARD (mechanical encoding)
     Each key on the ASR-33 teletype was wired to a set of
     contact bars. Pressing a key mechanically closed a specific
     combination of 7 switches, directly encoding a 7-bit ASCII
     value — no software needed.

       Key "A" pressed
          |
          v
       +---------------------------+
       | Contact bars encode:      |
       | bit 6: ON  (1)            |    1000001 = ASCII 65 = "A"
       | bit 5: OFF (0)            |
       | bit 4: OFF (0)            |    The keyboard is a mechanical
       | bit 3: OFF (0)            |    binary encoder — each key
       | bit 2: OFF (0)            |    closes a unique combination
       | bit 1: OFF (0)            |    of switch contacts.
       | bit 0: ON  (1)            |
       +---------------------------+

  2. SERIAL TRANSMISSION (current loop)
     The teletype transmitted one bit at a time over a wire pair
     using 20mA current loop signaling, at 110 baud (~10 chars/sec):

       Idle state: current ON continuously ("mark" = 1)

       To send "A" (1000001):
       +---+   +---+                       +---+-------
       | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | stop
       +---+   +---+---+---+---+---+   +---+   bits
       start   <-- 7 data bits (LSB first) -->
        bit

       start bit = current OFF (space) — tells receiver: "byte coming"
       data bits = current ON (1) or OFF (0) for each bit
       stop bits = current ON (mark) — gap before next character

       At 110 baud: each bit lasts ~9.09 ms
       Full character (1 start + 7 data + 2 stop = 10 bits): ~91 ms

       Wire from teletype ran to the computer (could be hundreds
       of feet through the building, or miles over phone lines).

     HOW CURRENT LOOP PHYSICALLY CARRIES BITS
     +----------------------------------------------------+
     |  A current loop is a simple series circuit:         |
     |                                                     |
     |  +-------+                              +--------+  |
     |  | Power |---wire--->  SENDER ---wire-->|RECEIVER|  |
     |  | Supply|           (switch)           |(detect)|  |
     |  | (20mA)|<----------wire (return)------|        |  |
     |  +-------+                              +--------+  |
     |                                                     |
     |  The sender is a mechanical switch inside the       |
     |  teletype's keyboard mechanism. Pressing a key      |
     |  triggers a rotating cam/contact assembly that      |
     |  opens and closes the circuit in the pattern of     |
     |  start bit + data bits + stop bits.                 |
     |                                                     |
     |    Switch CLOSED -> current flows (20mA) = 1 "mark" |
     |    Switch OPEN   -> no current   (0mA)  = 0 "space" |
     |                                                     |
     |  The receiver is a sensitive relay (or later, an    |
     |  optocoupler) that detects current vs. no current:  |
     |    - Current flowing -> relay pulls in  -> bit = 1  |
     |    - No current      -> relay releases  -> bit = 0  |
     |                                                     |
     |  WHY CURRENT (not voltage)?                         |
     |    Voltage drops over long wires due to resistance  |
     |    (V = IR). A 5V signal might arrive as 2V after   |
     |    hundreds of feet. But in a series circuit,       |
     |    current is the SAME everywhere — 20mA at the     |
     |    sender = 20mA at the receiver, regardless of     |
     |    wire length or resistance (the power supply      |
     |    just increases voltage to compensate). This      |
     |    made current loop reliable over thousands of     |
     |    feet, even miles over leased phone lines.        |
     |                                                     |
     |  The 20mA level was an industry standard inherited  |
     |  from telegraph circuits — high enough to reliably  |
     |  trip electromechanical relays, low enough to be    |
     |  safe and power-efficient.                          |
     +----------------------------------------------------+

  3. [[quick-context/uart|UART]] — THE BRIDGE BETWEEN SERIAL AND PARALLEL
     On the computer side, a UART (Universal Asynchronous
     Receiver/Transmitter) chip converted the serial bit
     stream into parallel bytes the CPU could read.

     At the highest level, a UART has two jobs:

       RECEIVE:  serial bits in (from wire)  -->  parallel byte out (to CPU)
       TRANSMIT: parallel byte in (from CPU) -->  serial bits out (onto wire)

     Inside, a **shift register** (chain of flip-flops) captures
     one bit per baud clock tick. After 8 bits, the completed byte
     latches into a **data register** the CPU reads. The shift
     register then immediately starts on the next byte.

     For the full internal mechanics — how the shift register
     fills bit by bit, how oversampling at 16× finds the center
     of each bit, and how the parallel latch transfers the
     completed byte — see [[quick-context/uart|UART deep dive]].

     The summary for this I/O path:

     +----------------------------------------------------+
     |  serial bits  -->  [shift register]  -->  [data     |
     |  from wire         (8 flip-flops)         register] |
     |                                              |      |
     |                                    INTERRUPT  |      |
     |                                       to CPU  v      |
     |                                     reads 0x41 "A"  |
     +----------------------------------------------------+

  4. INTERRUPT → OS → MEMORY BUFFER
     The UART's interrupt signal triggers the CPU to pause its
     current work and jump to an interrupt service routine:

     +----------------------------------------------------+
     |  CPU is running User B's program                    |
     |       |                                             |
     |       | <-- UART interrupt fires                    |
     |       v                                             |
     |  CPU saves current state (registers, PC)            |
     |       |                                             |
     |       v                                             |
     |  INTERRUPT SERVICE ROUTINE (in OS kernel):          |
     |    1. Read byte from UART data register (0x41)      |
     |    2. Identify which terminal sent it               |
     |       (each terminal has its own UART / port)       |
     |    3. Store byte in that user's INPUT BUFFER in RAM |
     |       +---+---+---+---+---+---+                     |
     |       | P | R | I | N | T | A | <-- "A" appended   |
     |       +---+---+---+---+---+---+                     |
     |       User A's input buffer                         |
     |    4. Echo the character back (send 0x41 to UART    |
     |       transmitter so user sees what they typed)     |
     |       |                                             |
     |       v                                             |
     |  CPU restores saved state, resumes User B's program |
     |                                                     |
     |  Total interrupt handling time: ~50-100 microseconds|
     |  User perceives: typed "A", saw "A" on paper        |
     +----------------------------------------------------+

  5. OUTPUT: MEMORY → UART → PRINT MECHANISM
     When the program produces output (e.g., "5"), the reverse:

     +----------------------------------------------------+
     |  Program calls: print("5")                          |
     |       |                                             |
     |       v                                             |
     |  OS writes 0x35 ("5") to UART transmit register     |
     |       |                                             |
     |       v                                             |
     |  UART serializes: start + 0110101 + stop            |
     |  Sends as current pulses over wire to teletype      |
     |       |                                             |
     |       v                                             |
     |  TELETYPE PRINT MECHANISM:                          |
     |  +----------------------------------------------+  |
     |  |  Receives serial data -> decodes ASCII        |  |
     |  |  Rotates type cylinder to "5" position        |  |
     |  |  Solenoid fires hammer -> strikes character   |  |
     |  |  through inked ribbon onto paper              |  |
     |  |  Carriage advances one position               |  |
     |  +----------------------------------------------+  |
     |                                                     |
     |  Same mechanism as a typewriter, but driven by      |
     |  electrical signals instead of finger force.        |
     +----------------------------------------------------+

  FULL ROUND TRIP:
  +---------+   serial   +------+  interrupt  +--------+  serial  +---------+
  |  Key    |----------->| UART |------------>|  CPU   |--------->| Print   |
  | pressed |  (110 baud)| chip | (byte ready)|  + OS  | (output) | hammer  |
  +---------+            +------+             +--------+          +---------+
      "A"     ~91ms wire   0x41    ~50us ISR   store in   ~91ms    "A" on
                                               RAM buffer  wire     paper
```

Key milestones:
- **1961:** CTSS at MIT — first practical time-sharing system
- **1964:** Dartmouth BASIC on DTSS — designed specifically so students could write and run programs interactively from terminals, without knowing about punch cards or assembly
- **1964-65:** IBM 2260 — early CRT display terminal (screen instead of paper)
- **1969:** Unix at Bell Labs (Thompson & Ritchie) — built for interactive terminals from the ground up
- **1970:** DEC VT05 — affordable CRT video terminal
- **1978:** DEC VT100 — the terminal that standardized screen-based interaction

**Dartmouth BASIC (1964)** deserves special mention: it was specifically created to let non-specialists program interactively. John Kemeny and Thomas Kurtz designed both the language and the time-sharing system so that a student could sit at a terminal, type `PRINT 2+3`, hit Enter, and see `5` immediately. This was revolutionary — before this, programming required submitting punch cards to a computing center and waiting.

### Era 4: Personal Computers and Modern IDEs (1970s–Today)

When microprocessors arrived (Intel 4004, 1971; Intel 8080, 1974; Zilog Z80, 1976), computing power moved from shared mainframes to personal desktops. Now the terminal and the computer were the same machine. The entire workflow — editing, compiling, running — happened locally.

```
ERA 4: FROM SCREEN TO CPU -- THE MODERN WORKFLOW
================================================================================

  YOU TYPE CODE ON SCREEN
       |
       |  Keyboard sends scancodes (USB HID protocol)
       |  -> OS keyboard driver converts to character codes
       |  -> Text editor stores characters in RAM buffer
       v
  +------------------------------------------+
  |  TEXT EDITOR (in RAM)                     |
  |  +--------------------------------------+ |
  |  |  int main() {                        | |
  |  |      int x = 2 + 3;                 | |
  |  |      return x;                       | |
  |  |  }                                  | |
  |  +--------------------------------------+ |
  |                                          |
  |  File -> Save writes RAM buffer to disk  |
  +--------------------+---------------------+
                       |
                       v
  +------------------------------------------+
  |  FILESYSTEM (SSD/HDD)                    |
  |  /home/user/main.c -> stored as bytes    |
  |  on persistent storage                   |
  +--------------------+---------------------+
                       |
                       |  $ gcc main.c -o main
                       |  (compiler reads from disk)
                       v
  +------------------------------------------+
  |  COMPILATION CHAIN                        |
  |  (see: code-to-gates-and-bootstrapping)  |
  |                                          |
  |  Source -> Preprocessor -> Compiler ->   |
  |  Assembler -> Object file -> Linker ->  |
  |  Executable binary (on disk)             |
  +--------------------+---------------------+
                       |
                       |  $ ./main
                       |  (OS loads executable)
                       v
  +------------------------------------------+
  |  OS LOADER                                |
  |  1. Reads ELF/PE executable from disk     |
  |  2. Allocates virtual memory              |
  |  3. Maps .text, .data, .bss sections      |
  |  4. Sets Program Counter to entry point   |
  |  5. CPU begins fetch-execute cycle        |
  +--------------------+---------------------+
                       |
                       v
  +------------------------------------------+
  |  CPU EXECUTES                             |
  |  Fetch instruction -> Decode -> Execute   |
  |  -> Store result -> Increment PC -> Repeat|
  |  (billions of times per second)           |
  |                                          |
  |  See: code-to-gates-and-bootstrapping    |
  |  for how instructions become gate        |
  |  operations on transistors               |
  +------------------------------------------+
```

For embedded/firmware development (e.g., the Pupper robot), the path is slightly different — instead of an OS loader, a cross-compiler produces an ELF file that a [[quick-context/firmware|flash programmer]] writes directly to the [[micro-context/microcontroller|microcontroller's]] flash memory. See [[quick-context/from-code-to-running-firmware]] for that full pipeline.

### Where Is Your Code Stored?

At each stage of the pipeline, "your code" exists in a different physical form:

```
WHERE YOUR CODE LIVES AT EACH STAGE
================================================================================

  Stage              Physical Location       Format
  -----------------  ----------------------  ----------------------
  Typing             RAM (editor buffer)     Characters (UTF-8)
  Saved              SSD/HDD (filesystem)    Characters (UTF-8)
  After compilation  SSD/HDD (filesystem)    Machine code (ELF binary)
  Running (desktop)  RAM (loaded by OS)      Machine code (binary)
  Running (embedded) Flash memory (on MCU)   Machine code (binary)

  Note: "RAM" at the typing stage and "RAM" at the running stage
  may be the same physical chips, but the OS manages them as
  separate virtual memory regions.
```

### How the Computer "Knows" Where to Find and Compile Your Code

There's no magic — every step is explicit:

1. **The text editor knows the file path** because you opened or created it (e.g., `/home/user/main.c`). It reads from and writes to that path via OS system calls.
2. **The compiler is invoked by you** (or your build system) with the file path as an argument: `gcc main.c`. The compiler asks the OS to read that file from disk.
3. **The linker knows where to place code in memory** from the linker script (for embedded) or OS conventions (for desktop). See [[quick-context/from-code-to-running-firmware|linker scripts]].
4. **The OS loader knows the entry point** because it's recorded in the ELF/PE executable header.
5. **The CPU knows where to start** because the OS sets the Program Counter to the entry point address — or, on bare metal, the [[quick-context/code-to-gates-and-bootstrapping|Reset Vector]] is hardwired into the CPU.

Nothing is automatic or implicit. Every "how does the computer know?" has the same answer: some earlier layer of software (or hardware) was explicitly configured to provide that information.

</details>

<details>
<summary><strong>The Key Tension</strong> — Interactivity vs. efficiency</summary>

The entire history of programming interfaces is a tension between **human interactivity** and **machine efficiency**.

| Era | Human Experience | Machine Efficiency | Tradeoff |
|-----|-----|-----|-----|
| Human Computers (pre-1940s) | Intuitive — humans understand the problem | Extremely slow — hours per trajectory | No machine at all; humans *are* the computer |
| Plugboards (1940s) | Terrible — days to reprogram | 100% — no software overhead | Humans serve the machine |
| Batch/Punch Cards (1950s) | Bad — hours of turnaround | High — no time wasted on interaction | Machine time was expensive, human time was cheap |
| Time-Sharing (1960s) | Good — seconds of feedback | Lower — CPU cycles "wasted" switching users | Humans became more expensive than machines |
| Personal Computers (1980s+) | Excellent — instant, dedicated | Lowest — most CPU cycles idle | Machine time became essentially free |

Each transition happened when economics flipped. Rooms full of human computers were replaced by ENIAC when a single machine could outperform hundreds of people. Then batch processing replaced manual machine setup. Then the shift from batch to interactive programming happened when the economics flipped again. In the 1950s, a computer cost millions of dollars and programmer time was cheap — it made sense to maximize machine utilization with batch processing, even if programmers waited hours. By the 1960s, programmer salaries exceeded computer costs, and the wasted hours spent debugging from printouts became the bottleneck. Time-sharing was the solution: sacrifice some machine efficiency to dramatically increase programmer productivity.

This same tension plays out today in the choice between compiled and interpreted languages (see [[quick-context/code-to-gates-and-bootstrapping|Abstraction vs. Performance]]), and between desktop development (instant feedback, virtual memory, OS manages everything) versus [[quick-context/from-code-to-running-firmware|embedded development]] (cross-compile, flash, reboot — slower iteration but direct hardware control).

</details>

<details>
<summary><strong>Concrete Example</strong> — What actually happens when you type <code>x = 2 + 3</code> and press Enter</summary>

Let's trace the entire path from keypress to CPU execution for a Python one-liner on a modern computer:

### Step 1: Keyboard to Editor

```
KEYPRESS TO CHARACTER
================================================================================

  1. You press the "x" key
  2. Keyboard controller sends USB HID scancode (0x1B for "x")
  3. OS keyboard driver converts scancode to character code:
     - Checks keyboard layout, modifier keys (Shift? Caps Lock?)
     - Produces Unicode code point: U+0078 ("x")
     - Delivers to the focused application (your editor)
  4. Editor inserts 'x' into its in-memory buffer
  5. Editor's rendering engine redraws the screen:
     - Character -> font glyph -> pixel data -> GPU -> display
     - You see "x" appear on screen

  Total time: ~5-15 ms (imperceptible to humans)
```

### Step 2: File Saved to Disk

When you save, the editor writes its RAM buffer to the filesystem:
- The OS filesystem driver allocates blocks on the SSD
- The source file `script.py` contains the UTF-8 bytes: `78 20 3D 20 32 20 2B 20 33 0A` (`x = 2 + 3\n`)
- The SSD stores these as charges in NAND flash cells (persistent — survives power loss)

### Step 3: Python Interpreter Runs

```bash
$ python script.py
```

Python is interpreted, not compiled ahead of time. The Python interpreter (`/usr/bin/python3`) is itself a compiled C program — machine code sitting on your SSD, loaded into RAM by the OS.

```
PYTHON EXECUTION CHAIN
================================================================================

  1. OS loads /usr/bin/python3 (CPython, ~5MB of machine code) into RAM
  2. CPython reads script.py from disk into RAM
  3. CPython's LEXER tokenizes: ['x', '=', '2', '+', '3']
  4. CPython's PARSER builds AST:
     Assign(target=Name('x'),
            value=BinOp(left=Num(2), op=Add, right=Num(3)))
  5. CPython's COMPILER emits bytecode:
     LOAD_CONST 2
     LOAD_CONST 3
     BINARY_ADD
     STORE_NAME 'x'
  6. CPython's VIRTUAL MACHINE executes bytecode:
     For each bytecode instruction, the interpreter (compiled C code)
     runs the corresponding machine code:
     - LOAD_CONST 2 -> C function that pushes PyObject(2) onto VM stack
     - BINARY_ADD   -> C function that calls PyNumber_Add, which
       eventually runs an ADD machine instruction in the CPU's ALU

  The CPU only ever executes machine code -- it runs CPython's compiled C
  code, which interprets your Python bytecode. Your Python source code
  never directly touches the CPU.
```

### Step 4: What the CPU Actually Does

At the bottom of the stack, when the ALU finally adds 2 + 3:

```
CPU EXECUTING THE ADDITION (nanosecond timescale)
================================================================================

  1. The ADD machine instruction enters the fetch-execute cycle
  2. Control unit decodes: "add registers R1 and R2, store in R3"
  3. ALU receives: R1 = 00000010 (2), R2 = 00000011 (3)
  4. Ripple-carry adder (chain of full adders built from logic gates):

     Bit 0: 0 + 1 + 0(carry) = 1, carry=0
     Bit 1: 1 + 1 + 0(carry) = 0, carry=1
     Bit 2: 0 + 0 + 1(carry) = 1, carry=0
     ...remaining bits: 0

     Result: 00000101 (5)

  5. Result written to R3
  6. Program counter increments
  7. Next instruction fetched

  Time for this addition: ~0.3 nanoseconds (at 3 GHz clock)
  The same addition on ENIAC: ~200 microseconds (600,000x slower)
```

For the same operation on the Pupper's [[micro-context/stm32-microcontroller|STM32]] [[learning/notes/micro-context/microcontroller|microcontroller]] (compiled C, not interpreted Python), step 3 would be replaced by ahead-of-time compilation: `gcc` produces machine code stored in [[quick-context/from-code-to-running-firmware|flash]], and the CPU executes the ADD instruction directly — no interpreter overhead.

**The one thing most outsiders get wrong about this is...** thinking that "interactive programming" means the computer understands your keystrokes directly. The screen, keyboard, text editor, filesystem, compiler, and OS are all elaborate layers of software that translate your intent into the only thing the CPU can do: fetch a binary instruction, decode it, and execute it through [[quick-context/code-to-gates-and-bootstrapping|logic gates]]. When you type on a screen and see output, you're interacting with at least six software layers — each one was [[quick-context/code-to-gates-and-bootstrapping|bootstrapped]] from something simpler, going all the way back to binary on punch cards.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/code-to-gates-and-bootstrapping]]** — The compilation chain in full detail: how source code becomes machine instructions through 7 layers of abstraction, and how the first compiler was bootstrapped from hand-coded binary. This document covers what happens *after* you save your file and invoke the compiler.

- **[[quick-context/from-code-to-running-firmware]]** — The embedded variant of the pipeline: linking, flashing, and booting on a microcontroller. What happens when your compiled code targets a chip with no OS.

- **[[quick-context/transistor]]** — The physical switch that replaced vacuum tubes and made modern computing possible. Every logic gate in the CPU is built from these.

- **[[quick-context/transistor-design-history]]** — The evolution from point-contact transistors (1947) through FinFETs to Gate-All-Around — the hardware side of the story that parallels the software interface evolution described here.

- **[[quick-context/semiconductor-fabrication]]** — How billions of transistors are manufactured on silicon. The hardware foundation that enabled the miniaturization from room-sized vacuum tube computers to pocket devices.

- **[[quick-context/uart]]** — Deep dive into how the UART hardware works: the receive shift register (chain of D flip-flops), 16× oversampling to find bit centers, and the parallel latch that transfers completed bytes to the CPU. The key bridge between the teletype's serial wire and the computer's parallel data bus.

- **Von Neumann Architecture** — The stored-program concept that made the transition from plugboards to software possible. Instructions and data share the same memory, enabling programs to be loaded and replaced without rewiring.

- **Unix and C** — The operating system and language (both created at Bell Labs, 1969-1972) that defined modern interactive programming. Unix was designed for terminals from day one; C was designed to write Unix. Together they shaped how we code today.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What was the key conceptual breakthrough that made it possible to go from plugboards to punch cards?
<details>
<summary>Answer</summary>
The **stored-program concept** (von Neumann, 1945): the idea that program instructions and data could be stored in the same memory. Before this, the "program" was the physical wiring of the machine. After this, the program was just numbers in memory that could be loaded from any external medium (punch cards, tape, keyboard). This single insight separated software from hardware forever. See: Era 2 in How It Works.
</details>

**Q2:** Why did punch cards survive for decades despite being slow and error-prone?
<details>
<summary>Answer</summary>
Because **computer time was far more expensive than programmer time** in the 1950s-60s. A mainframe cost millions of dollars. Batch processing maximized machine utilization — the computer was never idle waiting for a human to type. Time-sharing "wasted" CPU cycles switching between users, which was economically unacceptable when a single computer served an entire organization. Punch cards persisted until computers became cheap enough that programmer productivity mattered more than machine utilization. See: The Key Tension.
</details>

**Q3:** When you type `x = 2 + 3` in Python and press Enter, at what point does the CPU first encounter the number `2`?
<details>
<summary>Answer</summary>
The CPU encounters `2` in multiple forms at different stages, but **the CPU is involved from the very first keystroke** — it's running the OS, the text editor, and everything else. The number `2` specifically: (1) first appears as the ASCII/UTF-8 byte `0x32` when you press the "2" key, (2) the Python interpreter's lexer/parser processes it as a token, (3) the bytecode compiler emits `LOAD_CONST 2`, and (4) the VM pushes a Python integer object containing the value 2 onto the stack. At no point does the CPU "see" your Python code as instructions — it's always executing the interpreter's compiled C machine code, which processes your source text as data. See: Concrete Example (Step 3).
</details>

**Q4:** If time-sharing was invented in 1961, why did punch cards continue to be used into the 1980s?
<details>
<summary>Answer</summary>
Because time-sharing required expensive terminals and communications infrastructure that most organizations couldn't afford. A single teletype terminal cost $500-$1,000 in the 1960s (equivalent to $5,000-$10,000 today), and you needed one per user plus a time-sharing-capable computer. Most computing centers had one mainframe serving hundreds of users through batch queues — adding terminals for everyone was prohibitively expensive. Punch cards remained the cheapest way to submit programs at scale until personal computers made terminals obsolete in the 1980s. The transition was economic, not technical.
</details>

**Q5:** The bootstrapping chain started with hand-coded binary on punch cards. But today, if every compiler on Earth were deleted, could we rebuild the toolchain? How?
<details>
<summary>Answer</summary>
Yes — because the CPU hardware still exists and can execute binary instructions. You would repeat the original [[quick-context/code-to-gates-and-bootstrapping|bootstrapping]] process: (1) hand-write a minimal assembler in binary, enter it via any means of getting bytes into memory (hex editor, serial port, even toggle switches if needed), (2) use that assembler to write a better assembler, (3) use that to write a minimal C compiler (this has been done — the "stage0" and bootstrappable.org projects maintain a chain from hex to full compiler), (4) use the minimal compiler to compile GCC or LLVM. The bootstrapping chain is reconstructible because each step only requires tools from the previous step. In practice, this would take months, not decades, because we know what to build — the original pioneers had to invent it. See: Concrete Example in code-to-gates-and-bootstrapping.
</details>

</details>
