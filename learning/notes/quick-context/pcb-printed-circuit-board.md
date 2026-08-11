---
topic: PCB (Printed Circuit Board)
created: 2026-01-25
---

> **Related:** [[quick-context/pcb-chip-transistor-hierarchy]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]

> **TL;DR:** PCBs replace the nightmare of hand-soldered wire connections with thin copper pathways printed onto a rigid fiberglass board, providing the physical foundation for reliable, manufacturable, and repairable electronics in every smartphone, computer, and electronic device.

# PCB (Printed Circuit Board)

## The Core Problem: Connecting Electronic Components Reliably

Imagine you have a bunch of electronic components—chips (the "brains"), capacitors (tiny energy storage tanks), resistors (current limiters), and connectors (ports for cables). Each needs electrical connections to the others: power must flow in, signals must travel between parts, and everything needs a common ground reference. Without PCBs, you'd have to hand-solder individual wires between every component—a nightmare of tangled wires, unreliable connections, and impossible-to-repair rats' nests. Early electronics actually looked like this! A PCB solves this by replacing all those wires with **thin copper pathways printed onto a rigid board**. The board itself (usually green, but can be any color) is made of fiberglass, and the copper "traces" act as permanent, reliable wires. Every smartphone, computer, TV, and car contains dozens of PCBs—they're the physical foundation that makes modern electronics possible.

```
BEFORE PCBs: Point-to-Point Wiring (1950s)      AFTER PCBs: Clean, Reliable Connections
════════════════════════════════════════════    ═══════════════════════════════════════

    ┌────┐     ┌────┐                              ┌─────────────────────────────┐
    │CHIP│╲   ╱│CHIP│                              │  ┌────┐         ┌────┐     │
    └────┘ ╲ ╱ └────┘                              │  │CHIP│═════════│CHIP│     │
      │╲    ╳    │╱                                │  └────┘         └────┘     │
      │ ╲  ╱ ╲  ╱ │                                │     ║             ║        │
    ┌────┐╱   ╲┌────┐                              │  ═══╬═════════════╬════    │
    │CHIP│─────│CHIP│                              │  ┌────┐         ┌────┐     │
    └────┘     └────┘                              │  │CHIP│═════════│CHIP│     │
                                                   │  └────┘         └────┘     │
    Messy! Unreliable! Hard to fix!                └─────────────────────────────┘

                                                   Clean copper traces on a board
```

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Trace** | A thin copper "wire" printed onto the board that carries electrical signals or power between components—like a highway for electrons |
| **Via** | A tiny hole drilled through the board with copper plating inside, connecting traces on different layers—like an elevator between floors |
| **Pad** | A copper area where a component's pin or ball gets soldered—the "parking spot" where components attach to the board |
| **Layer** | One level of copper traces; simple boards have 2 layers (top and bottom), complex ones can have 16+ layers sandwiched together |
| **Soldermask** | The colored coating (usually green) that covers most of the copper, leaving only pads exposed—prevents accidental short circuits. See [[quick-context/pcb-layers]] for all layer types. |

```
ANATOMY OF A PCB (Side View Cross-Section)
═══════════════════════════════════════════════════════════════════════════════

                    Component (like a chip)
                        ┌───────┐
                        │  ▓▓▓  │
                        └┬─┬─┬─┬┘
                         │ │ │ │ ← Component pins/balls
    ─────────────────────┼─┼─┼─┼────────────────────────────  SOLDERMASK (green)
                         ▼ ▼ ▼ ▼                               protects copper
    ═══════════════════[PAD][PAD]══════════════════════════  TOP COPPER (traces)
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  FR-4 (fiberglass)
    ══════════════════════════════════════════════════════  INNER COPPER LAYER
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  FR-4 (fiberglass)
    ══════════════════════════════════════════════════════  BOTTOM COPPER (traces)
    ────────────────────────────────────────────────────────  SOLDERMASK (green)

    VIA (connects layers):
         │                    │
    ═════╪════                │    ← Top copper
    ░░░░░█░░░░                │    ← Fiberglass with copper-plated hole
    ═════╪════                │    ← Bottom copper
         │                    │
      A via is like an        │
      elevator between        │
      floors                  │
```

<details>
<summary><strong>How It Works</strong></summary>

A PCB is essentially a **sandwich of insulating fiberglass with patterned copper layers**. The copper starts as a solid sheet bonded to the fiberglass. Manufacturers use a process similar to photography: they coat the copper with light-sensitive material, shine UV light through a mask of the desired pattern, then chemically dissolve the unwanted copper—leaving only the traces, pads, and planes you designed. This is called "etching." For multi-layer boards, these copper-fiberglass sheets are stacked and laminated together with heat and pressure, then drilled to create vias (the connections between layers). Finally, everything gets coated with soldermask except the pads, and the exposed pads get a thin coating of solder or gold to prevent [[learning/notes/micro-context/oxidation|oxidation]] and improve solderability.

The magic of PCBs is that each copper layer can have its own independent pattern. Typically, you dedicate certain layers entirely to power and ground (called "planes")—these act as reservoirs of electricity that components can tap into anywhere they need. Signal traces run on other layers, weaving around each other. When a trace needs to cross another trace, it simply drops down to a different layer via a via, crosses underneath, and pops back up. This is how thousands of connections can coexist without touching each other.

```
HOW TRACES AND VIAS SOLVE ROUTING PROBLEMS
════════════════════════════════════════════════════════════════════════════════

Problem: Two traces need to cross. They can't touch or they'd short-circuit!

    TOP VIEW (looking down at the board)
    ─────────────────────────────────────────────────────

    WITHOUT VIAS (impossible!):        WITH VIAS (solved!):

    A──────────────────►B              A══════════════════►B
           │                                   │
           │  ← Would short-circuit!           ●  ← via (goes down)
           │                                   │
    C──────x───────────►D              C═══════╪══════════►D
           │                                   │
           │                                   ●  ← via (comes back up)
                                               │
    "X" marks a collision!                     ▼
                                        (the crossed trace is on
                                         a different layer)

    SIDE VIEW (cross-section) of the via solution:
    ───────────────────────────────────────────────────────────────────────────

    A══════════════╪═══════════════B    ← TOP LAYER (trace A→B continues)
    ░░░░░░░░░░░░░░░█░░░░░░░░░░░░░░░░    ← fiberglass
    C══════════════╪═══════════════D    ← BOTTOM LAYER (trace C→D crosses under)
                   │
                   └── via (copper-plated hole connecting layers)


A REAL 4-LAYER PCB STACK-UP
════════════════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────────────────────┐
    │ LAYER 1 (TOP): Signal traces and component pads                        │
    │    ┌─────┐           ┌─────┐                                           │
    │    │ CPU │══════════ │ RAM │                                           │
    │    └─────┘           └─────┘                                           │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ LAYER 2: GROUND PLANE (solid copper sheet)                             │
    │ ███████████████████████████████████████████████████████████████████████│
    │       Every component can connect to ground anywhere—like a huge       │
    │       copper "sea" that returns all the current to the power supply    │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ LAYER 3: POWER PLANE (solid copper sheet at 3.3V or 5V etc.)           │
    │ ███████████████████████████████████████████████████████████████████████│
    │       Every component can tap into power anywhere it needs             │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ LAYER 4 (BOTTOM): More signal traces and component pads                │
    │         ═══════════════════════════════════════════                    │
    │    ●    ●    ●    ●    ●    ●    ●    ●    ●    ●   ← [[quick-context/capacitor|decoupling caps]]  │
    └─────────────────────────────────────────────────────────────────────────┘

    Why planes instead of traces for power/ground?
    • Lower resistance → less voltage drop
    • Lower inductance → faster response to sudden current demands
    • Better shielding → less electrical noise between signal layers
```

</details>

<details>
<summary><strong>The Key Tension: Layer Count vs. Cost vs. Manufacturability</strong></summary>

PCB designers constantly balance three competing pressures. **More layers** means more routing freedom (traces can weave around each other easily), better signal integrity (power/ground planes shield signals from interference), and smaller board size (more routes fit in less area). But **each added layer dramatically increases cost**—a 2-layer board might cost $5, while an equivalent 8-layer board costs $50+ because of the complex lamination, alignment, and drilling processes. **Manufacturing tolerance** is the third factor: as trace widths shrink and layer counts grow, fewer factories can reliably produce the board, and defect rates climb.

The practical result: a simple Arduino uses a cheap 2-layer board because it has few connections. A smartphone motherboard uses 10+ layers because thousands of high-speed signals must fit in a tiny space. A high-performance server might use 20+ layers with exotic materials to handle 25+ Gbps signals. Designers always ask: "What's the minimum layer count that achieves our electrical and size requirements?"

```
LAYER COUNT TRADEOFFS
═══════════════════════════════════════════════════════════════════════════════

Board Type         │ Layers │ Typical Cost │ Use Case
───────────────────┼────────┼──────────────┼───────────────────────────────────
Hobby/Arduino      │   2    │    $2-10     │ Simple circuits, LED blinkers
Consumer IoT       │   4    │    $10-30    │ WiFi modules, smart home devices
Smartphone         │  8-12  │   $30-100    │ Complex, dense, many high-speed
                   │        │              │   signals in tiny space
Server/Networking  │ 16-24  │  $200-1000+  │ Maximum signal integrity for
                   │        │              │   multi-gigabit speeds

More layers = more routing freedom, but exponentially higher cost!
```

</details>

<details>
<summary><strong>Concrete Example: A Simple LED Circuit on a PCB</strong></summary>

Let's trace what happens when you press a button to light an LED—this shows how traces, vias, and pads work together.

```
SCHEMATIC (the logical circuit diagram):
════════════════════════════════════════════════════════════════════════════════

    9V Battery (+) ──┬── Button ── LED ── Resistor ── Ground (-)
                     │
                     └── (provides the push to move electrons)

    When button pressed: electrons flow from (-) → resistor → LED → button → (+)
    (Current flows opposite to electron flow by historical convention)


PCB LAYOUT (how it physically looks):
════════════════════════════════════════════════════════════════════════════════

    TOP VIEW (looking down at the board, 50mm x 30mm):
    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │   ┌─────────┐                                       │
    │   │  9V     │  Battery                              │
    │   │ Battery │  connector                            │
    │   │  CONN   │  (pads for                            │
    │   └────┬────┘   + and - wires)                      │
    │        │                                            │
    │        │  TRACE (copper path carrying +9V)          │
    │        │                                            │
    │   ┌────┴────┐                                       │
    │   │ BUTTON  │  ← Tactile switch                     │
    │   │  ░░░░   │    (4 pads, 2 connected internally)   │
    │   └────┬────┘                                       │
    │        │                                            │
    │        │  TRACE (copper path, only "live" when      │
    │        │         button is pressed)                 │
    │   ┌────┴────┐                                       │
    │   │   LED   │  ← Light-emitting diode               │
    │   │   (-)●  │    (2 pads: anode + and cathode -)    │
    │   └────┬────┘                                       │
    │        │                                            │
    │        │  TRACE                                     │
    │        │                                            │
    │   ┌────┴────┐                                       │
    │   │ 330 Ohm │  ← Resistor (limits current so        │
    │   │   ▓▓▓   │    LED doesn't burn out)              │
    │   └────┬────┘                                       │
    │        │                                            │
    │        │  TRACE (connected to ground plane or       │
    │        │         ground trace)                      │
    │        │                                            │
    │   ─────┴───── GND (connected back to battery -)     │
    │                                                     │
    │   ● ● ● = Pads (exposed copper for soldering)       │
    │   ═══ = Traces (copper pathways, covered by         │
    │          green soldermask except at pads)           │
    └─────────────────────────────────────────────────────┘


CROSS-SECTION (side view, showing how a via might connect layers):
════════════════════════════════════════════════════════════════════════════════

                        LED
                    ┌───┴───┐
                    │  ◄►   │
    ────────────────┴───┬───┴───────────────────────────  Soldermask (green)
    ════════════════════╪════════════════════════════════  Top copper (trace)
    ░░░░░░░░░░░░░░░░░░░░█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  FR-4 fiberglass
    ████████████████████╪█████████████████████████████████  GROUND PLANE
    ────────────────────╨───────────────────────────────  Soldermask (green)
                        │
                        └── Via connecting LED ground pad
                            to the ground plane layer
```

**The one thing most outsiders get wrong about this is...** thinking PCBs are just "green boards that hold components." In reality, the PCB *is* the circuit—the copper traces are the wires, carefully designed with specific widths (to handle current), specific lengths (for timing), and specific spacing (to avoid interference). A PCB designer spends most of their time not placing components, but routing traces—figuring out how to connect thousands of points without any paths crossing on the same layer, while meeting strict electrical requirements. The green part (soldermask) is just protective paint; the real engineering is in the invisible copper sandwich inside.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it (the fabrication basement).

- **[[quick-context/pcb-chip-transistor-hierarchy|The Packaging Hierarchy]]** — PCBs are one level in the hierarchy from transistors to complete systems. Understanding how chips, substrates, and PCBs connect gives context for why PCBs exist at the 100-400mm scale.

- **[[quick-context/electric-current|Electric Current]]** — PCB traces must carry current without overheating. Wider traces carry more current; trace width calculators help designers size traces for their expected current loads.

- **Signal Integrity** — At high speeds (MHz to GHz), traces act like transmission lines and signals can reflect, ring, or crosstalk. This drives many PCB design choices like controlled impedance traces and ground plane placement.

- **Soldering and SMT (Surface Mount Technology)** — How components actually attach to PCB pads. Understanding reflow soldering explains why pad design matters for manufacturing reliability.

- **[[quick-context/pcb-layers|PCB Layers]]** — Detailed breakdown of every layer in a PCB (copper, soldermask, silkscreen, paste mask, drill files, board outline) and their corresponding Gerber files. Essential for understanding what the manufacturer actually receives.

- **EDA (Electronic Design Automation) Software** — Tools like KiCad, Altium, or Eagle where designers draw schematics and lay out PCBs. The software enforces design rules and generates the files sent to PCB manufacturers.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What is the difference between a trace and a via?
<details>
<summary>Answer</summary>
A **trace** is a copper pathway that runs along a single layer of the PCB, carrying signals or power horizontally across the board. A **via** is a vertical connection—a drilled hole with copper plating that connects traces on different layers, like an elevator between floors of a building. See: 5 Essential Terms and the ASCII diagram showing how vias solve crossing-trace problems.
</details>

**Q2:** What does the soldermask (the green coating) actually do?
<details>
<summary>Answer</summary>
The soldermask is a protective coating that covers most of the copper, leaving only the pads exposed. It prevents accidental short circuits (if a stray piece of metal touched two adjacent traces, it would connect them—the soldermask prevents this). It also protects the copper from oxidation and environmental damage. See: 5 Essential Terms.
</details>

**Q3:** Why do PCB designers dedicate entire layers to power and ground "planes" instead of just routing power traces like signal traces?
<details>
<summary>Answer</summary>
Solid copper planes provide three major benefits: (1) **Lower resistance**—a solid sheet has much less resistance than a thin trace, reducing voltage drop across the board. (2) **Lower inductance**—planes respond faster to sudden current demands from chips (important for high-speed digital circuits). (3) **Better shielding**—planes act as shields between signal layers, reducing electromagnetic interference and crosstalk. This is why even a 4-layer board typically dedicates 2 layers to power/ground planes. See: How It Works (the 4-layer stack-up diagram).
</details>

**Q4:** A designer needs to connect 500 signals between a processor and memory on a PCB. They could use a 2-layer board with very thin traces and tiny spacing, or a 6-layer board with normal trace sizes. What factors would push them toward the more expensive 6-layer option?
<details>
<summary>Answer</summary>
Several factors favor the 6-layer board despite higher cost: (1) **Manufacturability**—very thin traces and tight spacing require specialized (expensive) manufacturing and have higher defect rates. (2) **Signal integrity**—without dedicated ground/power planes, high-speed signals suffer from noise and crosstalk; 6 layers allows 2 signal layers plus 2 power/ground planes. (3) **Reliability**—extremely thin traces are more prone to breaking or defects. (4) **Design time**—routing 500 signals on 2 layers is a nightmare puzzle; more layers dramatically simplify routing. The key tension tradeoff often favors spending more on manufacturing to save engineering time and improve reliability. See: The Key Tension.
</details>

**Q5:** The quick-context on the packaging hierarchy shows that chips connect to PCBs via [[learning/notes/quick-context/bga-ball-grid-array|BGA (Ball Grid Array)]]/quick-context/bga-ball-grid-array|Ball Grid Array]]) solder balls at ~0.8mm pitch. How does this relate to PCB design, and why can't you just use a 2-layer board for a modern CPU?
<details>
<summary>Answer</summary>
A modern CPU might have 1,500+ BGA balls in a 45mm x 45mm area. Each ball needs its own pad on the PCB, and each pad needs a trace routed away to somewhere else on the board. With balls only 0.8mm apart, there's no room to route traces between the balls on a single layer—you can only fit traces on the outer edges. The solution is **via-in-pad**: each inner ball has a via that drops the signal to an inner layer, where it can route freely without colliding with neighboring balls. This fundamentally requires multiple layers. High-end CPUs might need 8-12 layers just to "escape" all the signals from under the package, plus additional layers for power planes and other routing. The 100-400mm PCB scale mentioned in the hierarchy accommodates this complex layer stack. See: [[quick-context/pcb-chip-transistor-hierarchy]] for how the substrate fans out to ~800um pitch, and The Key Tension for why layer count correlates with complexity.
</details>

</details>
