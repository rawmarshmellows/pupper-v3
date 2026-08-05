---
topic: BGA (Ball Grid Array)
created: 2026-01-25
---

> **Related:** [[quick-context/pcb-chip-transistor-hierarchy]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]] | [[learning/notes/quick-context/wire-bonding]] | [[learning/notes/quick-context/substrate-ic-packaging]] | [[learning/notes/quick-context/silicon-die]]

> **TL;DR:** BGA (Ball Grid Array) solves the problem of connecting chips with hundreds or thousands of electrical connections by placing solder balls in a grid underneath the chip instead of metal pins around the edges, enabling far higher connection density for modern processors, memory, and graphics cards.

# BGA (Ball Grid Array)

## The Core Problem

Imagine you have a computer chip containing millions of microscopic circuits, and you need to connect it to a circuit board (the green board inside electronics). The chip needs hundreds or even thousands of electrical connections to receive power and exchange data. The old solution was metal "legs" (pins) sticking out from the chip's edges—but there's only so much room around the edges. BGA solves this by putting connections **underneath** the chip as an array of tiny solder balls, like a grid of metallic dots on the bottom. This lets manufacturers pack far more connections into the same space. Without BGA, modern processors, memory chips, and graphics cards couldn't exist—they simply wouldn't have enough connections to function.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Solder Ball** | A tiny sphere of metal alloy (~0.5-0.8 mm diameter) that melts during assembly to form an electrical and mechanical connection between the chip package and the circuit board |
| **Pitch** | The distance from the center of one solder ball to the center of the next; smaller pitch = more balls can fit, but harder to manufacture (typical: 0.5-0.8 mm) |
| **Reflow** | The process of heating the entire assembly in an oven until solder balls melt and form permanent joints, then cooling to solidify |
| **Pad** | A flat copper circle on the circuit board or chip package where a solder ball attaches; pads on both sides must align precisely |
| **X-ray Inspection** | Since BGA connections are hidden underneath, you can't visually check them—X-ray imaging is used to verify solder joints aren't cracked, bridged, or missing |

<details>
<summary><strong>How It Works</strong></summary>

Think of BGA like a bed of nails, but upside down and made of metal. The chip package has a flat bottom covered with a precise grid of solder balls—hundreds of tiny spheres arranged in rows and columns. The circuit board ([[quick-context/pcb-chip-transistor-hierarchy|PCB]]) has matching copper pads in exactly the same pattern. During assembly, the chip is placed ball-side-down onto the board, and the whole thing goes into a special oven. As temperature rises, the solder balls melt, surface tension pulls them into alignment with the pads, and when cooled, each ball forms a solid electrical bridge. Every ball carries either power, ground, or a data signal between the chip and the board.

```
WHAT IS A BGA? - Side-by-side Comparison
════════════════════════════════════════════════════════════════════════════

OLD WAY: Pins Around Edges (QFP)          NEW WAY: Balls Underneath (BGA)
───────────────────────────────────       ───────────────────────────────────

     ┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐                      ┌─────────────────┐
   ──┤                    ├──                    │                 │
   ──┤                    ├──                    │   CHIP PACKAGE  │
   ──┤    CHIP PACKAGE    ├──                    │                 │
   ──┤                    ├──                    └─────────────────┘
   ──┤                    ├──                    ● ● ● ● ● ● ● ● ●
     └─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘                      ● ● ● ● ● ● ● ● ●
           ↓ ↓ ↓                                ● ● ● ● ● ● ● ● ●
         Pins on                                ● ● ● ● ● ● ● ● ●
         edges only                             ● ● ● ● ● ● ● ● ●
                                                     ↑
                                              Balls on entire
                                              bottom surface

Why BGA wins:
─────────────
• QFP with pins: ~200 connections max (limited by edge space)
• BGA same size:  ~500+ connections (entire bottom is available!)
```

```
BGA CROSS-SECTION: What You'd See if You Cut It in Half
═══════════════════════════════════════════════════════════════════════════

                    ┌─────────────────────────────────────┐
                    │         CHIP PACKAGE TOP            │ ← Protective cover
                    │   ┌───────────────────────────┐     │
                    │   │      SILICON DIE          │     │ ← The actual chip
                    │   │   (where computing        │     │    (very small!)
                    │   │    happens)               │     │
                    │   └───────────────────────────┘     │
                    │         ║     ║     ║               │
                    │   ╔═════╩═════╩═════╩═════╗         │ ← Internal wiring
                    │   ║   SUBSTRATE (routing)  ║         │    fans out signals
                    │   ╚══╦═══╦═══╦═══╦═══╦════╝         │
                    └──────╫───╫───╫───╫───╫──────────────┘
                           ●   ●   ●   ●   ●               ← SOLDER BALLS
                                                             (~0.5-0.8 mm)
         - - - - - - - - - ↓ - ↓ - ↓ - ↓ - ↓ - - - - - - -
                           │   │   │   │   │
                    ┌──────●───●───●───●───●──────────────┐
                    │      COPPER PADS on PCB            │ ← Matching pads
                    │ ═══════════════════════════════════│ ← Copper traces
                    │                                    │    route signals
                    │         CIRCUIT BOARD (PCB)        │
                    └────────────────────────────────────┘

    Ball diameter: ~500-800 micrometers (about the width of 5-8 human hairs)
    Ball pitch:    ~500-800 micrometers (distance between ball centers)
```

```
THE REFLOW PROCESS: How BGA Gets Attached
════════════════════════════════════════════════════════════════════════════

STEP 1: Apply Solder Paste           STEP 2: Place Component
────────────────────────             ───────────────────────
    Stencil                              BGA Package
    ┌─────────┐                          ┌─────────┐
    │ ○ ○ ○ ○ │                          │         │
    │ ○ ○ ○ ○ │  ← holes match           │         │
    └────┬────┘    pad pattern           └────┬────┘
         ↓                                    ● ● ● ●  ← solder balls
    ┌─────────┐                               ↓ ↓ ↓ ↓
    │ ▓ ▓ ▓ ▓ │  ← paste deposits       ┌─────────────┐
    │ ▓ ▓ ▓ ▓ │    on each pad          │  ▓ ▓ ▓ ▓   │ ← balls sit on paste
    └─────────┘                          └─────────────┘
       PCB                                    PCB


STEP 3: Reflow Oven                  STEP 4: Finished Joint
───────────────────                  ─────────────────────

   ~~~~~ HEAT (220-250°C) ~~~~~          Temperature Profile:

       ┌─────────┐                       260°C ┤      ╱╲
       │ Package │                             │     ╱  ╲  ← Peak
       └────┬────┘                       220°C ┤    ╱    ╲
            ◠ ◠ ◠ ◠  ← balls melt              │   ╱      ╲
            │ │ │ │    and merge         150°C ┤  ╱        ╲
       ┌────┴─┴─┴─┴───┐                        │ ╱          ╲
       │    PCB       │                   25°C ┼──────────────→
       └──────────────┘                        0  2  4  6  8 min

   • Paste and balls melt together           "Reflow" = controlled
   • Surface tension self-aligns               melting and cooling
   • Cooling solidifies the joint
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The fundamental tradeoff in BGA is **connection density vs. accessibility**. BGA enables fitting 2000+ connections on a single chip, which is impossible with edge pins—but those connections are completely hidden underneath. If a single solder ball fails (crack, cold joint, or bridge to a neighbor), you can't see it without X-rays. You can't easily touch up one bad joint with a [[learning/notes/quick-context/soldering|soldering]] iron like you could with through-hole components. Rework requires specialized equipment to heat the entire package evenly, remove it, clean both surfaces, and attach a replacement with fresh solder balls. Hobbyists and repair shops debate: is the density worth the nightmare of repair? For consumer electronics, manufacturers say yes—the performance gain justifies treating failures as board-level replacements. For aerospace and medical, extensive X-ray inspection and expensive rework capability are factored in from the start.

</details>

<details>
<summary><strong>Concrete Example: Examining a Real BGA</strong></summary>

Here's what a typical processor BGA looks like, with real dimensions:

```
EXAMPLE: A 676-BALL BGA PACKAGE (26 x 26 grid)
════════════════════════════════════════════════════════════════════════════

Package Size: 27mm × 27mm
Ball Count:   676 balls (26 rows × 26 columns)
Ball Pitch:   1.0 mm (center to center)
Ball Diameter: ~0.6 mm

    TOP VIEW (looking at bottom of chip):

          1  2  3  4  5  6  7  . . . . . . . . . . .  24 25 26
        ┌──────────────────────────────────────────────────────┐
     A  │ ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  │
     B  │ ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  │
     C  │ ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  │
     D  │ ●  ●  ●  ○  ○  ○  ○  ○  ○  ○  ○  ○  ○  ○  ●  ●  ●  │
     E  │ ●  ●  ●  ○                                ○  ●  ●  ●  │
     F  │ ●  ●  ●  ○     (center may be             ○  ●  ●  ●  │
     G  │ ●  ●  ●  ○      depopulated for           ○  ●  ●  ●  │
     H  │ ●  ●  ●  ○      thermal reasons           ○  ●  ●  ●  │
     .  │ .  .  .  .      or unused)                .  .  .  .  │
     .  │ .  .  .  .                                .  .  .  .  │
     W  │ ●  ●  ●  ○  ○  ○  ○  ○  ○  ○  ○  ○  ○  ○  ●  ●  ●  │
     X  │ ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  │
     Y  │ ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  │
     Z  │ ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  ●  │
        └──────────────────────────────────────────────────────┘
                          27mm

    ● = solder ball present
    ○ = no ball (thermal void or unused pin)

    Ball naming: Position A1, B5, Z26, etc. (like Excel cells)


BALL FUNCTION MAP (typical allocation):
────────────────────────────────────────

┌────────────────────────────────────────────────────────────┐
│                     Ball Type         │  Typical Count     │
├────────────────────────────────────────────────────────────┤
│  VCC (Power supply)                   │     ~100 balls     │
│  GND (Ground)                         │     ~150 balls     │
│  Data signals (I/O)                   │     ~350 balls     │
│  Reserved/No connect                  │      ~76 balls     │
│  ─────────────────────────────────────│────────────────    │
│  TOTAL                                │      676 balls     │
└────────────────────────────────────────────────────────────┘

Note: Many balls carry power/ground because modern chips
      need massive amounts of current delivered with low noise
```

```
X-RAY VIEW: What Inspectors See
═══════════════════════════════════════════════════════════════════════════

    GOOD JOINTS               BAD JOINTS (defects)
    ───────────               ────────────────────

    ● ● ● ● ●                 ● ◐ ● ● ●
    ● ● ● ● ●                 ● ● ◉ ● ●
    ● ● ● ● ●                 ● ●●● ● ●
    ● ● ● ● ●                 ●   ● ● ●
    ● ● ● ● ●                 ● ● ● ● ○

    Uniform, round,           ◐ = void (bubble inside)
    properly sized            ◉ = head-in-pillow (didn't merge)
                              ●●● = bridge (balls merged together!)
                              (blank) = missing ball
                              ○ = cold joint (didn't fully melt)

    Real X-ray machines detect these at 1000+ joints per second
```

**The one thing most outsiders get wrong about this is...** assuming solder balls are placed individually during assembly. They're not—the balls are permanently attached to the chip package during manufacturing (by the chip vendor), and they stay there during shipping and storage. When you buy a BGA chip, it comes with balls already in place. During [[learning/notes/quick-context/pcb-printed-circuit-board|PCB]] assembly, you just add solder paste to the board, place the component, and reflow. The existing balls melt and merge with the paste to form the final joint. The balls are pre-attached to the package, not to the board.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/pcb-chip-transistor-hierarchy|PCB/Chip Packaging Hierarchy]]** — BGAs are one package type in the larger system that connects silicon dies to circuit boards; understanding the full hierarchy shows where BGA fits in the scale from [[learning/notes/quick-context/transistor|transistors]] to systems.

- **Surface Mount Technology (SMT)** — The broader manufacturing process that includes BGA; covers how pick-and-place machines, stencils, and reflow ovens work together to assemble entire circuit boards.

- **Thermal Management** — BGA packages often include thermal balls (larger balls for heat transfer) or exposed metal pads on top; understanding heat flow explains many BGA design decisions.

- **Signal Integrity** — At high frequencies, the path from die through BGA ball to PCB trace matters; shorter connections (one advantage of BGA) mean less signal degradation.

- **Lead-Free Solder (RoHS)** — Modern BGAs use lead-free alloys (typically SAC305: tin-silver-copper) which melt at higher temperatures than traditional lead solder, affecting reflow profiles and reliability.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why can't you visually inspect BGA solder joints like you can with through-hole components?
<details>
<summary>Answer</summary>
The solder balls are located underneath the chip package, completely hidden from view once the component is placed. You can only see the edges. This is why X-ray inspection is necessary to verify joint quality. See: 5 Essential Terms (X-ray Inspection)
</details>

**Q2:** What is "pitch" in the context of BGA, and what's a typical value?
<details>
<summary>Answer</summary>
Pitch is the distance from the center of one solder ball to the center of the adjacent ball. Typical BGA pitches range from 0.5 mm to 0.8 mm (500-800 micrometers). Smaller pitch allows more connections but is harder to manufacture and inspect. See: 5 Essential Terms and How It Works diagram
</details>

**Q3:** Why do BGA packages often have many balls dedicated to power (VCC) and ground (GND) rather than using just one or two?
<details>
<summary>Answer</summary>
Modern chips consume enormous amounts of current (sometimes 100+ amps) at very low voltages. A single ball can only carry limited current and has some resistance/inductance. Multiple parallel power and ground balls provide lower resistance paths, better current distribution, and cleaner power delivery with less electrical noise. See: Concrete Example (Ball Function Map)
</details>

**Q4:** Someone claims: "If one BGA solder joint fails, you can just touch it up with a regular soldering iron." What's wrong with this?
<details>
<summary>Answer</summary>
This is incorrect for two reasons: (1) You can't see the joints underneath to identify which one failed—you'd need X-ray inspection first. (2) You can't physically access the joints with a soldering iron tip because they're hidden under the package. BGA rework requires specialized equipment that heats the entire package evenly from above to remove it, then reattach with fresh solder balls. See: The Key Tension
</details>

**Q5:** Given that BGA balls are pre-attached to chip packages by the manufacturer, what would happen if a circuit board assembler ran the reflow oven at too low a temperature?
<details>
<summary>Answer</summary>
If the reflow temperature is too low, the solder paste on the PCB pads would melt (paste has flux that lowers melting point initially), but the pre-attached BGA balls might not fully melt or might only partially soften. This creates "head-in-pillow" defects where the ball and paste don't properly merge—they touch but don't form a true metallurgical bond. The joint looks okay from outside but fails under mechanical stress or thermal cycling. This connects to The Key Tension—such defects are invisible without X-ray and explain why temperature profile control during reflow is critical. See: The Reflow Process diagram and X-Ray View
</details>

</details>
