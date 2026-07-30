---
topic: Common IC Packages (DIP, QFP, QFN, SOT)
created: 2026-02-06
---

> **Related:** [[quick-context/pcb-chip-transistor-hierarchy]] | [[quick-context/pcb-printed-circuit-board]] | [[quick-context/soldering]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]] | [[micro-context/microcontroller|Microcontroller]]

> **TL;DR:** IC packages are the protective housings that connect a microscopic [[quick-context/silicon-die|silicon die]] to the macroscopic world—they range from large, hand-solderable through-hole DIP packages to tiny surface-mount QFN and [[quick-context/bga-ball-grid-array|BGA]] packages, each trading off size, pin count, thermal performance, and ease of assembly.

# Common IC Packages

## The Core Problem: Bridging Microscopic to Human-Scale

The [[quick-context/silicon-die|silicon die]] inside a chip is fragile (a few mm across, ~0.5 mm thick), has connection points only ~50 μm apart, and would be destroyed by handling, moisture, or mechanical stress. The package protects the die and provides connections (pins, leads, or solder balls) at a pitch that humans and machines can work with. The same chip design often comes in multiple package options—choosing the right one involves tradeoffs between size, thermal performance, pin count, and whether you can actually solder it by hand.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Through-hole** | Package with wire leads that go through holes in the [[quick-context/pcb-printed-circuit-board|PCB]] and are soldered on the other side. Easy to hand-solder. Being replaced by SMD in production. |
| **Surface mount (SMD/SMT)** | Package that sits flat on the PCB surface with leads or pads soldered to the top copper layer only. Smaller, cheaper, machine-friendly. |
| **Pitch** | The distance between adjacent pin centers. Smaller pitch = more pins in less space, but harder to solder. DIP: 2.54 mm. QFP: 0.5-0.8 mm. BGA: 0.4-1.27 mm. |
| **Pin count** | Total number of electrical connections. A simple voltage regulator: 3-5 pins. [[micro-context/microcontroller|Microcontroller]]: 20-100 pins. Processor: 500-3000+ pins. |
| **Thermal pad (exposed pad)** | A large metal pad on the bottom of some packages, soldered directly to the PCB. Conducts heat from the die into the board—critical for power components. |

<details>
<summary><strong>How It Works</strong></summary>

```
PACKAGE FAMILY TREE
══════════════════════════════════════════════════════════════════════════════

    THROUGH-HOLE (leads go through PCB holes)
    ─────────────────────────────────────────
    │
    ├── DIP (Dual In-line Package)
    │   • 2 rows of pins, 2.54mm (0.1") pitch
    │   • 8 to 40 pins typical
    │   • The classic IC package, breadboard-friendly
    │   • Still used for prototyping and hobby
    │
    └── SIP (Single In-line Package)
        • 1 row of pins (less common)


    SURFACE MOUNT (sits on PCB surface)
    ─────────────────────────────────────────
    │
    ├── SOT (Small Outline Transistor)
    │   • SOT-23: 3 pins, 2.9×1.3mm (transistors, diodes, regulators)
    │   • SOT-223: 4 pins, larger thermal pad
    │   • SC-70: 3-6 pins, even smaller than SOT-23
    │
    ├── SOIC (Small Outline IC)
    │   • DIP's SMD equivalent, 8-28 pins
    │   • 1.27mm pitch, hand-solderable with care
    │
    ├── QFP (Quad Flat Package)
    │   • Pins on all 4 sides, 0.5-0.8mm pitch
    │   • 32 to 256 pins
    │   • Hand-solderable with flux and patience
    │
    ├── QFN (Quad Flat No-lead)
    │   • Pads underneath edges (no protruding leads)
    │   • 0.4-0.65mm pitch, 8 to 100+ pins
    │   • Needs reflow or hot air (NOT hand-solderable with iron)
    │   • Excellent thermal performance (exposed pad)
    │
    └── BGA (Ball Grid Array)
        • Solder balls on the ENTIRE bottom surface
        • 0.4-1.27mm pitch, 50 to 3000+ pins
        • Reflow only, X-ray inspection required
        • Best for high pin count (processors, FPGAs)


SIZE COMPARISON (approximate scale)
══════════════════════════════════════════════════════════════════════════════

    DIP-8                    SOIC-8              SOT-23
    ┌────────────────────┐   ┌──────────┐       ┌───┐
    │ ●                  │   │ ●        │       │●  │
    ├─┤              ├───┤   ├──┐    ┌──┤       └─┬─┘
    ├─┤              ├───┤   ├──┘    └──┤        2.9mm
    ├─┤              ├───┤   ├──┐    ┌──┤
    ├─┤              ├───┤   ├──┘    └──┤
    └────────────────────┘   └──────────┘
    ~9.5 × 6.4 mm            ~5 × 4 mm         ~2.9 × 1.3 mm


    QFP-48 (0.5mm pitch)    QFN-32 (0.5mm pitch)    BGA-256
    ┌──┬┬┬┬┬┬┬┬┬┬──┐       ┌──────────┐            ┌─────────┐
    ├─            ─┤       │ ○○○○○○○○ │            │●●●●●●●●●│
    ├─            ─┤       │ ○      ○ │            │●●●●●●●●●│
    ├─            ─┤       │ ○  [EP] ○ │            │●●●●●●●●●│
    ├─            ─┤       │ ○      ○ │            │●●●●●●●●●│
    ├─            ─┤       │ ○○○○○○○○ │            │●●●●●●●●●│
    └──┴┴┴┴┴┴┴┴┴┴──┘       └──────────┘            └─────────┘
    ~7 × 7 mm               ~5 × 5 mm              ~15 × 15 mm


PIN NUMBERING
══════════════════════════════════════════════════════════════════════════════

    DIP / QFP: Pin 1 is marked with a dot.
    Count COUNTER-CLOCKWISE from pin 1.

    DIP-8 (top view):           QFP (top view):
    ┌──────────┐                ┌─┬┬┬┬┬┬─┐
    │ ●  1  8  │               ─┤ ●       ├─  Pin 1 at dot
    │    2  7  │               ─┤         ├─  Count CCW
    │    3  6  │               ─┤         ├─
    │    4  5  │                └─┴┴┴┴┴┴─┘
    └──────────┘

    BGA: Uses grid coordinates (A1, B2, C3, etc.)
    like a spreadsheet.
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Hand-Solderable vs. Machine-Only vs. Thermal Performance

| Package | Hand Solder? | Pins | Thermal | Size | Production Cost |
|---------|-------------|------|---------|------|-----------------|
| **DIP** | Easy | 8-40 | Poor | Large | High (through-hole) |
| **SOIC** | Moderate | 8-28 | Moderate | Medium | Low |
| **SOT-23** | Moderate | 3-6 | Poor | Tiny | Very low |
| **QFP** | Hard (needs flux) | 32-256 | Moderate | Medium | Low |
| **QFN** | Hot air only | 8-100+ | Excellent (EP) | Small | Low |
| **BGA** | Impossible | 50-3000+ | Good | Small-large | Medium |

```
THE TRADEOFF IN PRACTICE
══════════════════════════════════════════════════════════════════════════════

    PROTOTYPING / HOBBY          PRODUCTION
    ────────────────────         ──────────────────
    DIP (breadboard-friendly)    QFN (small, thermal pad)
    SOIC (hand-solderable)       BGA (max pin density)
    QFP (challenging but doable) Auto pick-and-place

    The same IC often comes in multiple packages:
    ATmega328P: DIP-28, QFP-32, QFN-32
    Same silicon die, different housing.
    DIP for Arduino prototyping, QFN for commercial products.
```

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Same Chip, Three Packages: ATmega328P

```
CHOOSING A PACKAGE FOR THE ATmega328P
══════════════════════════════════════════════════════════════════════════════

    DIP-28 (PDIP)               TQFP-32                MLF/QFN-32
    ┌────────────────────┐      ┌──┬┬┬┬┬┬┬──┐          ┌──────────┐
    │ ●  1         28    │      ├─ ●         ├─         │ ○○○○○○○○ │
    │    PC6      PC5    │      ├─           ├─         │ ○      ○ │
    │    PD0      PC4    │      ├─           ├─         │ ○  EP  ○ │
    │    PD1      PC3    │      ├─           ├─         │ ○      ○ │
    │    ...      ...    │      └──┴┴┴┴┴┴┴──┘          │ ○○○○○○○○ │
    │   PD7      PB5     │      7 × 7 mm               └──────────┘
    └────────────────────┘      0.8mm pitch             5 × 5 mm
    ~35 × 7.6 mm                                        0.5mm pitch
    2.54mm pitch


    Use Case Comparison:
    ────────────────────────────────────────────────────────────────────────

                        DIP-28          TQFP-32         QFN-32
    ─────────────────   ──────────      ──────────      ──────────
    Board area          267 mm²         49 mm²          25 mm²
    Hand-solderable?    Yes (easy)      Yes (tricky)    No (hot air)
    Breadboard?         Yes             No              No
    I/O pins            23              23 + 4 extra    23 + 4 extra
    Thermal             Poor            Moderate        Excellent (EP)
    Production cost     Highest         Low             Lowest
    When to use         Learning,       Low-volume      Commercial
                        prototyping     production      products

    The QFN is 10× smaller than the DIP. Same exact chip inside.
    Commercial products almost never use DIP—it wastes too much
    PCB space and costs more in automated assembly.
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it (the fabrication basement).

- **[[quick-context/pcb-chip-transistor-hierarchy]]** — IC packages are one level in the hierarchy from die to PCB. The package contains the die, connected via [[quick-context/wire-bonding|wire bonds]] or [[quick-context/flip-chip|flip-chip]], and connects to the PCB via leads, pads, or [[quick-context/bga-ball-grid-array|BGA balls]].

- **[[quick-context/soldering]]** — Package type dictates [[quick-context/soldering|soldering]] method. DIP = through-hole iron. SOIC/QFP = SMD iron with flux. QFN = hot air or reflow oven. BGA = reflow oven only.

- **[[quick-context/pcb-printed-circuit-board]]** — Package footprint (land pattern) must match the PCB pads exactly. A QFN-32 with 0.5mm pitch needs PCB pads accurate to ~0.05mm. The exposed pad needs thermal vias to conduct heat to inner copper layers.

- **[[quick-context/wire-bonding]]** — Inside most packages (DIP, QFP, QFN), the die is connected to the lead frame via wire bonds. BGA packages typically use [[quick-context/flip-chip|flip-chip]] bonding.

- **[[quick-context/substrate-ic-packaging]]** — High-pin-count packages (BGA) use a multi-layer [[quick-context/substrate-ic-packaging|substrate]] between the die and the solder balls, acting as a miniature PCB inside the package.

- **[[quick-context/pupper-bom-control-board]]** — A real BOM using LQFP-64, SOT-23-8, SOT-23-6, WSON-10, LGA-28, and WLP-9 packages on one board. Shows how package choice affects assembly (the LGA-28 BNO086 can't be sourced through standard JLCPCB assembly).

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why would a commercial product use QFN instead of DIP for the same chip?
<details>
<summary>Answer</summary>
**Smaller (10× less board area), better thermal performance (exposed pad), lower assembly cost (pick-and-place reflow is cheaper than through-hole at scale), and more available I/O pins.** DIP is larger, has no thermal pad, and through-hole assembly costs more in production. DIP is only preferred for prototyping and educational purposes where hand-[[quick-context/soldering|soldering]] is needed.
</details>

**Q2:** How do you find pin 1 on an IC?
<details>
<summary>Answer</summary>
**Look for the dot, notch, or line marking.** DIP packages have a notch on one end and/or a dot at pin 1. QFP/QFN packages have a dot at pin 1. BGA packages have a marking at the A1 corner. From pin 1, count counter-clockwise for DIP/QFP. For BGA, use the grid coordinates (rows = letters, columns = numbers).
</details>

**Q3:** Why can't you hand-solder a QFN package with a regular soldering iron?
<details>
<summary>Answer</summary>
**The pads are underneath the package, not on protruding leads.** A QFN has flat pads on its bottom surface with no leads extending beyond the package edge. A soldering iron can't reach under the package. You need hot air (heats the entire area from above, reflowing solder paste underneath) or a reflow oven. The exposed thermal pad on the bottom also must be soldered, which is impossible with an iron.
</details>

**Q4:** A BGA package has 1mm pitch and is 15mm × 15mm. Approximately how many balls does it have?
<details>
<summary>Answer</summary>
**Roughly 225 (15 × 15 grid).** At 1mm pitch on a 15mm package, you get approximately 15 rows × 15 columns = 225 positions. In practice, some positions are depopulated (removed for routing or thermal reasons), so the actual pin count might be ~200. Finer pitch (0.5mm) on the same package would give ~900 balls.
</details>

**Q5:** What is the thermal pad (exposed pad) on the bottom of a QFN, and why does it matter?
<details>
<summary>Answer</summary>
**It's a large metal pad connected to the die attach paddle inside the package, providing a direct thermal path from the chip to the PCB.** Heat from the die conducts through the paddle to this exposed pad, then through solder into the PCB copper (especially if thermal vias connect to internal ground planes). Without soldering the exposed pad, the IC can overheat even at moderate power levels. It often also serves as the ground connection.
</details>

</details>
