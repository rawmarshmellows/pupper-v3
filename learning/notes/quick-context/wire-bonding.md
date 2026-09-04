---
topic: Wire Bonding
created: 2026-01-25
---

> **Related:** [[learning/notes/micro-context/microcontroller]] | [[learning/notes/quick-context/bond-pad]] | [[learning/notes/quick-context/substrate-ic-packaging]] | [[learning/notes/quick-context/flip-chip]] | [[learning/notes/quick-context/fundamental-electronic-parts-index]]

> **TL;DR:** Wire bonding solves the problem of connecting impossibly small chip connection points (~50 micrometers) to the outside world by using specialized machines to attach extremely thin wires between the chip and its protective housing, making it the cheapest and most common chip connection method for billions of chips annually.

# Wire Bonding

## The Core Problem

Inside every computer chip is a tiny [[learning/notes/quick-context/silicon-die|silicon die]] with connection points only about 50 micrometers wide—thinner than a human hair—that need to connect to the outside world for power and data. Wire bonding solves this by using specialized machines to attach extremely thin wires (about 25 micrometers) between the chip and its protective housing, making it possible for chips to actually function in devices.

## 5 Essential Terms

| Term | Plain English Definition |
|------|--------------------------|
| **[[learning/notes/quick-context/bond-pad\|Bond pad]]** | A tiny metal square on the chip surface where a wire can be attached—think of it as a microscopic "landing zone" for connections |
| **[[learning/notes/quick-context/substrate-ic-packaging\|Substrate]]** | The intermediate platform (like a small circuit board) that the chip sits on; wire bonds connect the chip to this platform |
| **Ultrasonic welding** | Using high-frequency vibrations (like a tiny tuning fork) to melt/fuse the wire to the metal pad without traditional heat |
| **Loop height** | How tall the wire arc is above the chip; taller loops are more forgiving but add electrical interference |
| **Ball bond / Wedge bond** | The two ends of a wire bond—the "ball" is a melted sphere at the start, the "wedge" is a flat pressed connection at the end |

<details>
<summary><strong>How It Works</strong></summary>

Wire bonding is essentially robotic micro-sewing. A machine called a "wire bonder" uses a needle-like tool (the capillary) to thread extremely thin wire from the chip to its housing. Here's the step-by-step process:

**Step 1: Ball Formation** — An electrical spark melts the tip of the gold or copper wire, forming a tiny ball (like a match head, but microscopic). Surface tension makes it perfectly round.

**Step 2: Ball Bond** — The machine presses this ball onto the chip's bond pad while applying ultrasonic vibration. The vibration creates friction heat that welds the ball to the pad in milliseconds. This is the first attachment point.

**Step 3: Looping** — The machine lifts up and arcs the wire over to the substrate's landing pad, creating a curved bridge. The loop shape is precisely controlled.

**Step 4: Wedge Bond** — At the destination, the machine presses the wire flat against the substrate pad (no ball this time) and uses ultrasonic welding again. Then it breaks the wire and moves to the next connection.

```
THE WIRE BONDING PROCESS (Step by Step)
═══════════════════════════════════════════════════════════════════════════

STARTING POSITION:
                                        Capillary tool (holds wire)
                                              │
                                              ▼
                                         ┌─────────┐
                                         │    │    │
                                         │   ═╪═   │ ← Wire spool feeds
                                         │    │    │   through here
                                         └────┼────┘
                                              │
                                              ● ← Wire tip (gold/copper)

STEP 1: BALL FORMATION
───────────────────────
An electric spark melts the wire tip into a ball:

                         SPARK!
                           ⚡
                           │
                           ● ← Molten ball forms
                          ╱ ╲   (~60 μm diameter)


STEP 2: BALL BOND
─────────────────
Press ball onto chip's bond pad + ultrasonic vibration:

          Capillary presses down
                    │
                    ▼
               ┌─────────┐
               │    ║    │
               │    ║    │
               │    ●    │ ← Ball pressed flat
               └────┼────┘
                    │
    ┌───────────────┼───────────────┐
    │ CHIP (die)    ●               │  ← Bond pad (tiny metal square)
    │               ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
    └───────────────────────────────┘

    ∿∿∿∿∿∿∿∿∿∿∿∿∿ ← Ultrasonic vibration (60-120 kHz)
                     welds ball to pad in ~10ms

STEP 3: LOOPING
───────────────
Machine lifts and arcs wire to destination:

                    ┌─────────┐
                    │    ║    │ ← Capillary moves up and over
                    └────╫────┘
                         ║
                    ┌────╫────────────────────┐
                    │    ║                    │
                    │    ╚═══════════╗        │ ← Wire forms loop
                    │                ║        │   (controlled arc shape)
                    │                ║        │
    ┌───────────────┼────────────────╫────────┼───────┐
    │ CHIP          ●                ║        │       │
    │               ▓▓▓▓▓▓▓▓▓▓       ║     SUBSTRATE  │
    └───────────────┼────────────────╫────────────────┘
                    │                ▓▓▓▓▓▓▓▓▓│
                    │                         │
                    └─────────────────────────┘

STEP 4: WEDGE BOND
──────────────────
Press wire flat onto substrate pad + break wire:

                         ┌─────────┐
                         │ ═══════ │ ← Wire clamped and broken
                         └─────────┘

                         Loop height
                         (~150 μm typical)
                              │
                    ┌─────────┼─────────┐
                    │         ▼         │
                    │    ╭─────────╮    │
                    │   ╱           ╲   │
                    │  ╱             ╲  │
    ┌───────────────┼─╱───────────────╲─┼───────┐
    │ CHIP          ●                  ▬│       │ ← Wedge bond
    │ (silicon die) ▓▓▓▓▓▓▓▓▓▓         ▓│       │   (flat press)
    └───────────────┼──────────────────────────┘
                    │            SUBSTRATE      │
                    └───────────────────────────┘

RESULT: ONE COMPLETE WIRE BOND
──────────────────────────────
Repeat 100-2000 times per chip!

    CROSS-SECTION VIEW OF FINISHED BONDS:

    ┌────────────────────────────────────────────────────────────────┐
    │                                                                │
    │    Wire bonds: thin arches connecting chip to substrate        │
    │                                                                │
    │              ╭──╮    ╭──╮    ╭──╮    ╭──╮    ╭──╮              │
    │             ╱    ╲  ╱    ╲  ╱    ╲  ╱    ╲  ╱    ╲             │
    │    ┌───────●──────●●──────●●──────●●──────●●──────●───────┐    │
    │    │ CHIP  ▓▓  ▓▓  ▓▓  ▓▓  ▓▓  ▓▓  ▓▓  ▓▓  ▓▓  ▓▓  CHIP  │    │
    │    └───────────────────────────────────────────────────────┘    │
    │                              │                                  │
    │    ┌─────────────────────────┼──────────────────────────────┐  │
    │    │                         │                              │  │
    │    │      S U B S T R A T E  │  (with routing layers)       │  │
    │    │                         │                              │  │
    │    │    ●     ●     ●     ●  │  ●     ●     ●     ●         │  │
    │    └─────────────────────────┼──────────────────────────────┘  │
    │                              │                                  │
    │                         BGA balls connect                       │
    │                         to circuit board                        │
    │                                                                │
    └────────────────────────────────────────────────────────────────┘
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

Wire bonding is the **cheapest** way to connect a chip to its package—equipment costs less, it's well-understood, and gold/copper wire is relatively inexpensive. But it has real limitations:

```
WIRE BONDING TRADEOFFS
═════════════════════════════════════════════════════════════════════════

                        WIRE BONDING              FLIP-CHIP (alternative)
                        ────────────              ──────────────────────

    CONNECTION          Only around                Entire bottom surface
    LOCATIONS           chip edges                 of chip

                        ┌─────────┐                ┌─────────┐
                        │         │                │●●●●●●●●●│
                        │  CHIP   │                │●●●●●●●●●│
                        │         │                │●●●●●●●●●│
                        └─────────┘                └─────────┘
                         ↑↑↑↑↑↑↑                   ●●●●●●●●●●
                         wires here                bumps everywhere
                         only

    MAX CONNECTIONS     ~500-700 per chip          ~10,000+ per chip
    (I/O density)

    WIRE LENGTH         1-3 mm (long loops)        ~0.1 mm (direct bumps)

    INDUCTANCE          Higher (longer wires       Lower (shorter path)
    (signal quality)    = more interference)

    SPEED LIMIT         Works well up to           Better for >3 GHz
                        ~1 GHz signals             signals

    COST                $0.001-0.01 per wire       $0.10+ per bump

    USE CASES           • Memory chips             • CPUs, GPUs
                        • Sensors                  • High-speed networking
                        • Low-cost MCUs            • Smartphone processors
                        • Automotive               • Data center chips

WHY INDUCTANCE MATTERS (for complete beginners):
───────────────────────────────────────────────

    Inductance = resistance to changing current

    Long wire = more inductance = signals get "smeared"

    LOW INDUCTANCE (good):          HIGH INDUCTANCE (bad):

    Signal in:  ▁▁▁█████▁▁▁         Signal in:  ▁▁▁█████▁▁▁

    Signal out: ▁▁▁█████▁▁▁         Signal out: ▁▁▂▄▆███▆▄▂▁
                clean!                          smeared/slow

    At low speeds (<100 MHz): doesn't matter much
    At high speeds (>1 GHz): wire bonds become a bottleneck
```

The industry uses wire bonding when **cost matters more than speed**—which is most chips! Only high-performance processors, graphics cards, and specialized high-frequency chips need the more expensive flip-chip technology.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Here's what a real wire-bonded DRAM (memory) chip looks like in cross-section:

```
DRAM MEMORY PACKAGE (Wire-Bonded)
═══════════════════════════════════════════════════════════════════════════

    TOP VIEW (package with lid removed):
    ┌──────────────────────────────────────────────────────────────────┐
    │                                                                  │
    │     Wire bonds visible as tiny gold arches around chip edges     │
    │                                                                  │
    │     ┌────────────────────────────────────────────────────┐       │
    │     │╲                                                  ╱│       │
    │     │ ╲                                                ╱ │       │
    │     │  ╲              DRAM DIE                        ╱  │       │
    │     │   ╲          (~8mm × 10mm)                     ╱   │       │
    │     │    ╲                                          ╱    │       │
    │     │     ╲        [Silicon chip with              ╱     │       │
    │     │      ╲        memory cells and              ╱      │       │
    │     │       ╲       control logic]               ╱       │       │
    │     │        ╲                                  ╱        │       │
    │     │         ╲                                ╱         │       │
    │     │╱                                                  ╲│       │
    │     └────────────────────────────────────────────────────┘       │
    │                                                                  │
    │                    S U B S T R A T E                             │
    │              (organic laminate, ~0.3mm thick)                    │
    │                                                                  │
    └──────────────────────────────────────────────────────────────────┘

          ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ● ●
                    BGA solder balls on bottom
                  (connect to your motherboard)


    SIDE VIEW (cross-section):

                              Encapsulant (plastic protection)
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │░░░░░░░░░░░░░░░░░░░░░│░░░░░░░░░░░░░░░░░░░░░│
                    │░░░░░░░░░░░░░░░░░░░░░│░░░░░░░░░░░░░░░░░░░░░│
                    │░░░░  ╭───╮  ╭───╮  ╭┼──╮  ╭───╮  ╭───╮ ░░░│
                    │░░░░ ╱     ╲╱     ╲╱ │   ╲╱     ╲╱     ╲░░░│
                    │░░░ ╱       ╳       ╳│    ╳       ╳     ╲░░│
                    │   ●═══════════════════════════════════●   │
                    │   │           DRAM DIE                │   │
                    │   │          (silicon)                │   │
                    │   └───────────────┬───────────────────┘   │
                    │                   │ die attach (glue)     │
                    │═══════════════════╧═══════════════════════│ ← Substrate
                    │     Internal routing (copper traces)      │
                    └──────┬─────┬─────┬─────┬─────┬─────┬──────┘
                           ●     ●     ●     ●     ●     ●
                           │     │     │     │     │     │
                           BGA solder balls (~0.4mm diameter)


    WIRE BOND SPECIFICATIONS FOR TYPICAL DRAM:
    ┌───────────────────────────┬─────────────────────────────┐
    │ Parameter                 │ Typical Value               │
    ├───────────────────────────┼─────────────────────────────┤
    │ Wire material             │ Gold (Au) or Copper (Cu)    │
    │ Wire diameter             │ 18-25 μm (0.018-0.025 mm)   │
    │ Bond pad size             │ 50-80 μm × 50-80 μm         │
    │ Loop height               │ 100-200 μm                  │
    │ Number of wires           │ 80-200 per chip             │
    │ Bonding speed             │ 10-15 wires per second      │
    │ Wire inductance           │ ~0.5-1.5 nH per mm          │
    │ Bond pull strength        │ >3 grams (quality check)    │
    └───────────────────────────┴─────────────────────────────┘


    SCALE COMPARISON:

    Human hair:           ~70 μm  ═══════════════════════════
    Wire bond:            ~25 μm  ═════════
    Bond pad:             ~60 μm  ═════════════════
    Solder ball:         ~400 μm  ══════════════════════════════════════
                                            (huge by comparison!)
```

**The one thing most outsiders get wrong about this is...** assuming wire bonding is primitive or outdated technology. In reality, it's incredibly precise—modern wire bonders place thousands of wires per hour with micron-level accuracy, and the ultrasonic welding creates bonds stronger than the wire itself. Wire bonding handles the majority of chips manufactured today (billions annually) because it's the perfect balance of cost and reliability for most applications. The "better" alternatives like flip-chip are only necessary when you need extreme speed or density. A $5 [[learning/notes/micro-context/microcontroller|microcontroller]] and a $500 CPU both need connections to the outside world—wire bonding makes the $5 chip economically possible.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it (the fabrication basement).

- **[[quick-context/pcb-chip-transistor-hierarchy|Chip Packaging Hierarchy]]** — The broader context of how chips connect to circuit boards; wire bonding is one step in this multi-level system.

- **Flip-Chip (C4) Bonding** — The main alternative to wire bonding; uses solder bumps under the chip for higher density and performance.

- **Die Attach** — How the silicon chip is physically glued to the substrate before wire bonding; affects thermal performance.

- **Ultrasonic Welding** — The core joining technology behind wire bonding; uses vibration instead of heat to fuse metals.

- **[[quick-context/electric-current|Electric Current]]** — Understanding how electricity flows helps explain why wire length, diameter, and inductance matter for signal quality.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What are the two types of bonds at each end of a wire bond, and how do they differ?
<details>
<summary>Answer</summary>
The "ball bond" at the start is formed by melting the wire into a sphere and pressing it flat onto the chip's bond pad. The "wedge bond" at the end is made by pressing the wire flat against the substrate pad without forming a ball first. Both use ultrasonic welding to create the connection. See: How It Works (Steps 2 and 4)
</details>

**Q2:** Approximately how thin is a typical bond wire compared to a human hair?
<details>
<summary>Answer</summary>
A bond wire is about 25 μm in diameter, while a human hair is about 70 μm. So bond wire is roughly one-third the thickness of a human hair—or about half, depending on the wire specification. See: Concrete Example (Scale Comparison table)
</details>

**Q3:** Why does wire bonding become problematic for signals above 1 GHz?
<details>
<summary>Answer</summary>
Wire bonds are 1-3 mm long, and longer wires have higher inductance. Inductance resists changes in current, which "smears" fast-changing signals—the faster the signal switches (higher frequency), the worse this effect becomes. At frequencies above 1 GHz, the signal degradation from wire bond inductance becomes unacceptable for many applications. See: The Key Tension (inductance diagram)
</details>

**Q4:** A chip designer says "we need more than 800 I/O connections." Why would this statement make wire bonding impractical?
<details>
<summary>Answer</summary>
Wire bonds can only connect around the edges of the chip (perimeter bonding), limiting the total number of connections to roughly 500-700 per chip. With 800+ connections needed, there's physically not enough edge space for all the bond pads and wires. This chip would require flip-chip technology, which uses the entire bottom surface of the chip for connections. See: The Key Tension (connection locations comparison)
</details>

**Q5:** Given what you know about the chip packaging hierarchy, why might a memory chip (DRAM) use wire bonding while the CPU that accesses it uses flip-chip?
<details>
<summary>Answer</summary>
Memory chips have fewer I/O connections (80-200 wires for DRAM vs. thousands for CPUs) and operate at lower signal frequencies than CPU-to-memory buses. The cost savings of wire bonding are significant when you have multiple memory chips per system. CPUs, however, need thousands of connections for power delivery and high-speed data lanes running at multi-GHz frequencies—wire bonding's inductance and limited density make flip-chip essential. The packaging hierarchy shows that each level is optimized for its specific requirements; wire bonding is "good enough" for memory but not for the processor. See: [[quick-context/pcb-chip-transistor-hierarchy]] and The Key Tension
</details>

</details>
