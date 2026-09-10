---
topic: PCB Layers
created: 2026-02-21
updated: 2026-02-21
---

# PCB Layers

> **Related:** [[learning/notes/quick-context/pcb-printed-circuit-board]] | [[learning/notes/quick-context/soldering]] | [[learning/notes/quick-context/grounding-and-return-paths]]

> **TL;DR:** A PCB is a sandwich of distinct functional layers — copper for carrying signals and power, soldermask for protection, silkscreen for labeling, paste mask for assembly, and drill files for holes — each manufactured and designed separately, then stacked together to form the complete board you see in a Gerber viewer.

> **Reference Board:** Pupper v3 Control Board Rev 3.5.2 (Gabrael & Nathan) — all examples in this document reference this 2-layer board.
> ![Pupper PCB Gerber View](quick-context/Pupper%20PCB.png)

## The Core Problem: One Board, Many Manufacturing Steps

A PCB isn't a single thing — it's a stack of 10+ distinct layers, each with a different material and purpose, manufactured in a precise sequence. Designers must think in layers because the manufacturer needs separate instructions (Gerber files) for each one: where to etch copper, where to apply solder paste, where to print labels, where to drill holes. Getting any single layer wrong — a missing soldermask opening, a misaligned drill, a silkscreen covering a pad — produces a board that can't be assembled or doesn't work. Understanding what each layer does is the key to reading Gerber files, reviewing PCB designs, and diagnosing manufacturing problems.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Copper Layer** | The conductive layer where [[learning/notes/quick-context/pcb-printed-circuit-board#traces-and-vias\|traces, pads, and planes]] are etched from a solid copper sheet — this IS the circuit |
| **Soldermask** | A polymer coating (typically green) applied over copper, with openings only at [[learning/notes/quick-context/soldering\|solder]] pads — prevents shorts and protects traces from oxidation |
| **Silkscreen (Legend)** | White ink printed on top of the soldermask showing component outlines, reference designators (R1, C3, U1), and labels for human readability |
| **Paste Mask (Stencil)** | Defines where [[learning/notes/quick-context/soldering#reflow\|solder paste]] gets deposited during SMD assembly — openings match (or slightly shrink) the pad locations |
| **Drill File** | Instructions for the CNC drill specifying hole locations, diameters, and whether holes are plated (PTH) or non-plated (NPTH) |

<details>
<summary><strong>How It Works</strong> — The complete layer stack</summary>

Every PCB layer exists as a separate Gerber file sent to the manufacturer. Here's what each one does, using the Pupper v3 Control Board (Rev 3.5.2, a 2-layer board) as a running example:

```
COMPLETE PCB LAYER STACK (cross-section, 2-layer board)
================================================================

        Silkscreen (Top)         white ink: "U1", "C3", "Left Servo"
    ─────────────────────────────────────────────────────────────────
        Soldermask (Top)         green coating with pad openings
    ─────────────────────────────────────────────────────────────────
  ══════╤══════════════╤══════   Top Copper          signal traces +
        │    [PAD]     │                              component pads
    ░░░░█░░░░░░░░░░░░░░█░░░░░   FR-4 Core           fiberglass insulator
        │              │                              (0.8-1.6 mm thick)
  ══════╧══════════════╧══════   Bottom Copper       more traces + ground
    ─────────────────────────────────────────────────────────────────
        Soldermask (Bottom)      green coating
    ─────────────────────────────────────────────────────────────────
        Silkscreen (Bottom)      white ink (if used)

    Legend: ═══ copper    ░░░ fiberglass    █ via (plated hole)
            ─── soldermask/silkscreen       [PAD] exposed copper


NOT PHYSICAL LAYERS (but still separate Gerber files):
    ┌──────────────────────────────────────────────────────────┐
    │  Paste Mask (Top)     → used to make the solder stencil │
    │  Paste Mask (Bottom)  → (only if bottom has SMD parts)  │
    │  Board Outline        → CNC routing path for board edge │
    │  Drill Files (PTH)    → plated through-hole locations   │
    │  Drill Files (NPTH)   → non-plated holes (mounting)     │
    │  Drill Drawing        → human-readable drill diagram    │
    │  Document Layer       → fab notes, dimensions, specs    │
    └──────────────────────────────────────────────────────────┘
```

### Layer-by-Layer: What It Is, How It's Made, and Its Gerber File

The manufacturing sequence doesn't follow the layer stacking order — the factory builds the board from the inside out. Here's each layer with both its function and how it's physically manufactured:

```
PCB MANUFACTURING SEQUENCE (2-layer board)
================================================================

    Step 1: Start with copper-clad FR-4 (copper on both sides)
    Step 2: Drill all holes (PTH + NPTH)
    Step 3: Plate through-holes (electroless copper + electrolytic copper)
    Step 4: Image & etch copper patterns (both sides)
    Step 5: Apply soldermask (both sides)
    Step 6: Apply silkscreen (both sides)
    Step 7: Apply surface finish (HASL, ENIG, or OSP)
    Step 8: Route board outline (CNC)
    Step 9: Electrical test (flying probe)

    Note: Paste mask & document layers are NOT manufactured ON
    the board — they're used for assembly (stencil) and fab notes.
```

---

**1. Top Copper** — `Gerber_TopLayer.GTL`

*What it is:* The primary signal and component layer — shown in red on the Pupper board viewer. Contains signal traces, [[micro-context/smd-pad|component pads]] (SMD and through-hole), copper pours/fills, and via pads. This is where the actual circuit lives.

*How it's manufactured:* The factory starts with a sheet of FR-4 fiberglass with solid copper foil laminated to both sides (typically 1 oz/ft², ~35 μm thick). The copper pattern from the Gerber file is transferred using **photolithography**: a UV-sensitive photoresist is applied over the copper, UV light is shone through a film mask of the trace pattern, then the board is dipped in developer solution to wash away unexposed resist. Finally, a chemical etchant (ferric chloride or cupric chloride) dissolves the unprotected copper, leaving only the traces and pads behind. The remaining photoresist is then stripped off.

```
COPPER ETCHING PROCESS (subtractive)
================================================================

  1. Copper-clad board
  ══════════════════  ← copper
  ░░░░░░░░░░░░░░░░░░  ← FR-4

  2. Apply photoresist
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ← resist
  ══════════════════  ← copper
  ░░░░░░░░░░░░░░░░░░  ← FR-4

  3. UV expose through mask
      ██      ██        ← mask blocks UV over traces
  ↓↓↓↓  ↓↓↓↓  ↓↓↓↓↓↓  UV light
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ← resist
  ══════════════════    ← copper
  ░░░░░░░░░░░░░░░░░░   ← FR-4

  4. Develop (wash away unexposed resist)
      ▓▓      ▓▓        ← only hardened resist remains
  ══════════════════    ← copper (still intact)
  ░░░░░░░░░░░░░░░░░░   ← FR-4

  5. Etch (acid dissolves exposed copper)
      ▓▓      ▓▓        ← resist protects copper below
      ══      ══     ← unprotected copper dissolved
  ░░░░░░░░░░░░░░░░░░   ← FR-4

  6. Strip resist → finished traces!
      ══      ══        ← copper traces remain
  ░░░░░░░░░░░░░░░░░░   ← FR-4
```

On the Pupper board: most IC footprints and the large ground copper pour are on this layer (visible as the red fill area).

---

**2. Bottom Copper** — `Gerber_BottomLayer.GBL`

*What it is:* The second copper layer — shown in blue on the Pupper board viewer. Used for additional routing that couldn't fit on top, plus ground/power distribution. Traces on bottom cross under top traces freely (connected by [[learning/notes/quick-context/pcb-printed-circuit-board#vias|vias]]). May have its own copper pour for [[learning/notes/quick-context/grounding-and-return-paths#ground-plane|ground plane]] coverage.

*How it's manufactured:* Same photolithography + etching process as the top copper, performed simultaneously on the bottom side. Both sides are imaged and etched in the same manufacturing steps.

---

**3. Drill Files** — `.DRL` (Excellon format)

*What they are:* CNC drill instructions specifying every hole's X/Y location, diameter, and plating type. Split into three files:
- **PTH Through** (`Drill_PTH_Through.DRL`): Plated through-holes for component leads — copper-lined holes connecting top and bottom
- **PTH Through Via** (`Drill_PTH_Through_Via.DRL`): Plated holes for vias (layer-to-layer connections, no component inserted)
- **NPTH Through** (`Drill_NPTH_Through.DRL`): Non-plated holes for mounting screws or alignment pins — bare fiberglass, no copper

*How it's manufactured:* **Drilling happens BEFORE copper etching** on production boards. A CNC drill machine spins carbide drill bits at 100,000-150,000 RPM, drilling each hole in ~0.1 seconds. Boards are stacked 2-3 high to drill multiple panels simultaneously. After drilling, PTH holes go through **electroless copper deposition** (a chemical bath that deposits a thin conductive copper layer on the bare fiberglass hole walls), followed by **electrolytic copper plating** (builds up copper thickness to ~25 μm on hole walls). NPTH holes are masked off during plating.

```
DRILL HOLE TYPES
================================================================

    PTH (Plated Through-Hole)        NPTH (Non-Plated Through-Hole)

    Component lead or via            Mounting screw or alignment pin

    ═══════╤═══════                  ═══════   ═══════
    ░░░░░░░█░░░░░░░                  ░░░░░░░   ░░░░░░░
    ═══════╧═══════                  ═══════   ═══════
           │                                │
    Copper-plated walls              Bare fiberglass walls
    Electrically connects            No electrical connection
    top and bottom copper            Just a mechanical hole

    █ = copper-plated walls          (space) = bare fiberglass
```

---

**4. Top Soldermask** — `Gerber_TopSolderMaskLayer.GTS`

*What it is:* A polymer coating (typically green) applied over the top copper. **Negative layer**: the Gerber file defines where soldermask is REMOVED (pad openings), not where it's applied. Exposes only [[micro-context/smd-pad|pads]] where components will be soldered; everything else stays covered. Prevents solder bridges between close traces and protects copper from corrosion.

*How it's manufactured:* Modern PCBs use **LPI (Liquid Photo-Imageable)** soldermask. The liquid polymer is applied to the entire board surface by curtain coating or screen printing. It's then "tack cured" (partially dried) so it can be handled. Next, the soldermask Gerber film is aligned over the board and UV light is shone through it — the UV **hardens** the mask everywhere EXCEPT where the film blocks light (over pads). The unhardened soldermask over pads is washed away in an alkaline developer bath, exposing the copper pads underneath. A final thermal cure (~150°C) fully hardens the remaining soldermask permanently.

```
SOLDERMASK (LPI) APPLICATION PROCESS
================================================================

    1. APPLY liquid mask over entire board

    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ← liquid soldermask covers everything
    ════╤═════╤═════╤═══  ← copper traces/pads underneath
    ░░░░░░░░░░░░░░░░░░░░  ← FR-4

    2. UV EXPOSE through film (film blocks light at pads)

        ██    ██    ██      ← film blocks UV over pads
    ↓↓↓↓  ↓↓↓↓  ↓↓↓↓  ↓↓  ← UV light hardens exposed mask
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ← mask (exposed areas harden)
    ════╤═════╤═════╤═══

    3. DEVELOP (wash away unexposed mask at pads)

    ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓  ← hardened mask stays
    ════╤═════╤═════╤═══       ← pads now exposed!

    4. FINAL THERMAL CURE (~150C) → done!

    ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓  ← permanent green soldermask
    ════╤═════╤═════╤═══       ← pads ready for soldering
```

**5. Bottom Soldermask** — `Gerber_BottomSolderMaskLayer.GBS`

*What it is:* Same function as top soldermask, but for the bottom side. Opens up pads for through-hole soldering and any bottom-side SMD components.

*How it's manufactured:* Applied simultaneously with the top soldermask — both sides are coated, exposed, and developed in the same process steps.

---

**6. Top Silkscreen** — `Gerber_TopSilkscreenLayer.GTO`

*What it is:* White (or other color) ink printed on top of the cured soldermask. Shows component outlines, pin 1 markers, reference designators (R1, C3, U1), and human-readable labels. On the Pupper board: "Left Servo", "Right Servo", "S +5 GND" pin labels, connector names like "CN1B". Must not overlap pad openings (ink on a pad prevents good solder joints).

*How it's manufactured:* Two methods are common:
- **Screen printing** (traditional): A fine mesh screen with the legend pattern is placed over the board, and ink is squeegeed through. Cost-effective for high volume. Resolution: ~100 μm minimum line width, ~1.5mm minimum text height.
- **Direct legend printing / inkjet** (modern): A UV-curing inkjet printer sprays acrylic ink directly onto the board from the Gerber data — no screen needed. Higher resolution (~30-40 μm), faster changeover, better for prototypes and small runs. Ink is UV-cured during printing.

**7. Bottom Silkscreen** — `Gerber_BottomSilkscreenLayer.GBO`

*What it is:* Labels on the bottom side. Often minimal — on the Pupper board: "Control Board Rev 3.5.2 Gabrael & Nathan."

*How it's manufactured:* Same process as top silkscreen, applied to the bottom side.

---

**8. Surface Finish** (not a separate Gerber layer — specified in fab notes)

*What it is:* A protective coating applied to exposed copper pads AFTER soldermask. Bare copper oxidizes within hours, making it unsolderable. The surface finish preserves pad solderability during storage and assembly.

*Common types:*
| Finish | Process | Cost | Best For |
|--------|---------|------|----------|
| **HASL** | Board dipped in molten solder, leveled with hot air | Low | General purpose, through-hole |
| **Lead-free HASL** | Same, with lead-free solder | Low | RoHS-compliant general purpose |
| **ENIG** | Electroless nickel (3-6 μm) + immersion gold (0.05-0.1 μm) | Medium | Fine-pitch, BGA, flat pads |
| **OSP** | Thin organic coating on copper | Lowest | Short shelf life, reflow-only |

---

**9. Board Outline** — `Gerber_BoardOutlineLayer.GKO` (GKO technically stands for "Keep-Out," but is widely used for board outlines)

*What it is:* Defines the PCB's physical shape as a closed polygon. Also defines internal cutouts.

*How it's manufactured:* After all layers are complete, a **CNC router** follows the outline path to cut the board from the production panel. Typical routing bit: 2mm diameter, cutting at 1-2 m/min. V-scoring (partial cuts) is used when boards will be snapped apart from a panel later.

---

**10. Top Paste Mask** — `Gerber_TopPasteMaskLayer.GTP`

*What it is:* Defines [[micro-context/paste-mask-and-solder-stencil|stencil]] openings for solder paste application during [[learning/notes/quick-context/soldering#reflow|reflow assembly]]. Paste openings are typically 5-20% smaller than the actual pad (depending on component pitch) to prevent excess solder bridging.

*How it's used (NOT manufactured on the board):* The paste mask Gerber is sent to a stencil vendor who **laser-cuts** matching apertures in a thin stainless steel sheet (0.1-0.15 mm thick). During assembly, this stencil is aligned over the bare PCB and solder paste (a mixture of tiny solder balls suspended in flux) is squeegeed across the stencil surface. Paste fills the apertures but can't reach areas where the steel blocks it — so only the pads receive paste. The stencil is then lifted straight up off the board, and the paste stays behind on the pads due to adhesion (it's a thick, sticky consistency, like toothpaste). The result is precise rectangular deposits of solder paste sitting on each pad, with the height controlled by stencil thickness and the footprint controlled by aperture size. From here, a pick-and-place machine positions components onto the pasted pads (the paste is tacky enough to hold them), and then the whole board goes through a [[learning/notes/quick-context/soldering#reflow|reflow oven]] that melts the paste into permanent solder joints.

---

**11. Drill Drawing** — `Gerber_DrillDrawingLayer.GDD`

*What it is:* A human-readable map showing drill locations with a table of hole sizes and counts. Used for visual verification and communication between designer and fab — not for CNC programming (the `.DRL` files are used for that).

---

**12. Document Layer** — `Gerber_DocumentLayer.GDL`

*What it is:* Fabrication notes, dimensions, tolerances, material specs, layer stackup instructions, and any special requirements. Not part of the physical board — instructions for the manufacturer. May include: board thickness, copper weight, soldermask color, surface finish type, impedance control requirements, and UL markings.

</details>

<details>
<summary><strong>The Key Tension</strong> — Soldermask openings vs. paste openings</summary>

The most common source of PCB assembly problems is the relationship between three layers that must align precisely at every pad:

```
THE THREE-LAYER ALIGNMENT AT EVERY PAD
================================================================

    Top View of One SMD Pad:

    ┌─────────────────────────────────────────────────┐
    │                                                 │
    │   ┌─────────────────────────────────────┐       │
    │   │                                     │       │
    │   │   ┌─────────────────────────┐       │       │
    │   │   │                         │       │       │
    │   │   │     SOLDER PASTE        │       │       │
    │   │   │     (paste mask)        │       │       │
    │   │   │                         │       │       │
    │   │   └─────────────────────────┘       │       │
    │   │         COPPER PAD                  │       │
    │   │         (copper layer)              │       │
    │   └─────────────────────────────────────┘       │
    │           SOLDERMASK OPENING                    │
    │           (soldermask layer)                    │
    │                                                 │
    │    SOLDERMASK (covers everything else)           │
    └─────────────────────────────────────────────────┘

    Size relationship:
    Paste opening < Copper pad < Soldermask opening

    Why paste is smaller than pad:
    • Excess paste → solder bridges between adjacent pads
    • Too little paste → weak joints, tombstoning

    Why soldermask opening is larger than pad:
    • Ensures pad is fully exposed even with alignment tolerance
    • Solder needs to wet the entire pad surface

    Example values for a 0.5mm pitch QFP (varies by package):
    Pad:              0.30 × 1.20 mm
    Paste opening:    0.25 × 1.10 mm  (~83% of pad area)
    Soldermask opening: 0.40 × 1.30 mm  (0.05mm clearance all around)
```

For fine-pitch components (0.4-0.5mm pitch [[learning/notes/quick-context/common-ic-packages|QFP or QFN]]), getting paste volume wrong by even 10% causes bridging (too much) or open joints (too little). This is why paste mask design is a separate engineering discipline — and why the paste mask is a distinct Gerber file, not just a copy of the copper layer.

</details>

<details>
<summary><strong>Concrete Example</strong> — Reading the Pupper Control Board Gerbers</summary>

The Pupper v3 Control Board (Rev 3.5.2) is a 2-layer board. Here's how to interpret what you see in a Gerber viewer with all layers overlaid:

```
COLOR MAP (typical Gerber viewer conventions)
================================================================

    Color     │ Layer                    │ What You're Seeing
    ──────────┼──────────────────────────┼──────────────────────────
    Red       │ Top Copper (GTL)         │ Traces, pads, copper pour
    Blue      │ Bottom Copper (GBL)      │ Traces visible "through"
    Green     │ Soldermask (both sides)  │ The board color itself
    Yellow    │ Silkscreen (GTO/GBO)     │ Component labels, text
    Gray      │ Paste Mask (GTP)         │ Stencil openings
    Purple    │ Drill Drawing (GDD)      │ Hole locations
    White     │ Board Outline (GKO)      │ Board edge shape
    Teal      │ Drill holes              │ Actual drill positions


WHAT TO LOOK FOR ON THE PUPPER BOARD
================================================================

    ┌─────────────────────────────────────────────────────────────┐
    │   ○                                           ○            │
    │   mounting                              mounting           │
    │   hole (NPTH)                           hole (NPTH)        │
    │                                                            │
    │   ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                     │
    │   │ IC  │  │ IC  │  │ IC  │  │ IC  │  ← ICs on TOP       │
    │   └─────┘  └─────┘  └─────┘  └─────┘    COPPER (red)     │
    │   ═══════════════════════════════════  ← red traces        │
    │   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  ← blue traces       │
    │                                          (bottom copper)   │
    │                                                            │
    │   S  +5  GND    S  +5  GND   ← SILKSCREEN labels         │
    │   Left Servo    Right Servo     (yellow text)              │
    │                                                            │
    │   ┌──────────────────────────────┐                         │
    │   │ Control Board Rev 3.5.2     │  ← SILKSCREEN (bottom)  │
    │   │ Gabrael & Nathan            │                          │
    │   └──────────────────────────────┘                         │
    │   ○                                           ○            │
    └─────────────────────────────────────────────────────────────┘

    Key observations:
    • Red (top copper) dominates — most routing on top, large ground pour
    • Blue (bottom copper) fills gaps — traces that couldn't route on top
    • Yellow text — servo pin labels (S = Signal, +5 = Power, GND = Ground)
    • Teal circles at corners — mounting holes (NPTH, no copper plating)
    • Small teal dots scattered on board — vias connecting top↔bottom
```

The Gerber file list maps directly to the layer stack:

| Gerber File | Layer | Purpose |
|-------------|-------|---------|
| `Gerber_TopPasteMaskLayer.GTP` | Paste, Top | Solder stencil template |
| `Gerber_TopSilkscreenLayer.GTO` | Legend 1, Top | Component labels |
| `Gerber_TopSolderMaskLayer.GTS` | Top copper group | Pad exposure mask |
| `Gerber_TopLayer.GTL` | Copper 1, Top | Signal traces + pads |
| `Gerber_BottomLayer.GBL` | Copper, Bot | Additional routing |
| `Gerber_BottomSolderMaskLayer.GBS` | Bottom copper group | Pad exposure mask |
| `Gerber_BottomSilkscreenLayer.GBO` | Legend 1, Bot | Bottom labels |
| `Gerber_BoardOutlineLayer.GKO` | Profile | Board edge (CNC route) |
| `Gerber_DrillDrawingLayer.GDD` | Drillmap | Visual drill diagram |
| `Gerber_DocumentLayer.GDL` | Other | Fab notes + dimensions |
| `Drill_PTH_Through.DRL` | Drill | Plated component holes |
| `Drill_PTH_Through_Via.DRL` | Drill | Plated via holes |
| `Drill_NPTH_Through.DRL` | Drill | Mounting/mechanical holes |

**The one thing most outsiders get wrong about this is...** thinking "layers" only means copper layers. When someone says "a 2-layer board," they mean 2 copper layers — but the board actually has 10+ distinct manufacturing layers (2 copper + 2 soldermask + 2 silkscreen + 2 paste mask + outline + drills + documentation). Every one of these needs its own file, and mistakes on any non-copper layer cause just as many production failures as copper errors.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/quick-context/pcb-printed-circuit-board]]** — The parent topic covering PCB fundamentals: what traces, vias, pads, and planes do. This layers file details the individual Gerber files that describe each manufacturing step.

- **[[learning/notes/quick-context/soldering]]** — The paste mask layer is designed specifically for the reflow soldering process. Stencil printing, paste volume, and pad opening ratios directly determine solder joint quality.

- **[[learning/notes/quick-context/grounding-and-return-paths]]** — Ground planes live on copper layers. On a 2-layer board, one copper layer often serves as a partial ground plane; on 4+ layer boards, dedicated inner layers provide unbroken ground planes for better return paths.

- **[[learning/notes/quick-context/common-ic-packages]]** — Package type (DIP, QFP, QFN, BGA) determines pad geometry on the copper layer, paste mask openings, and whether the board needs thermal vias under exposed pads.

- **[[learning/notes/quick-context/schematic-reading]]** — The schematic defines WHAT is connected; the PCB layers define HOW and WHERE those connections are physically implemented as copper traces, pads, and vias.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What's the difference between a soldermask layer and a paste mask layer?
<details>
<summary>Answer</summary>
**Soldermask** is a permanent polymer coating on the finished PCB that protects copper and prevents solder bridges — it stays on the board forever. **Paste mask** is NOT on the board at all — it's a template for cutting a stainless steel stencil used during assembly to deposit solder paste onto pads before reflow. Both define openings at pad locations, but paste openings are typically 5-10% smaller than soldermask openings.
</details>

**Q2:** Why are drill files split into PTH, PTH-Via, and NPTH?
<details>
<summary>Answer</summary>
**PTH (Plated Through-Hole)** holes get copper plating on their walls, creating an electrical connection between top and bottom layers — used for through-hole component leads. **PTH-Via** holes are also plated but specifically for vias (no component inserted, just layer-to-layer connection). **NPTH (Non-Plated Through-Hole)** holes have bare fiberglass walls with no copper — used for mounting screws, alignment pins, and mechanical features. They're separate files because the manufacturer processes plated and non-plated holes differently (plating requires additional chemical deposition steps).
</details>

**Q3:** The soldermask Gerber is described as a "negative layer." What does this mean in practice?
<details>
<summary>Answer</summary>
**The Gerber file defines where soldermask is REMOVED, not where it's applied.** The shapes in the soldermask Gerber represent openings (holes in the green coating) that expose copper pads underneath. Everything NOT drawn in the soldermask file gets covered with green polymer. This is the opposite of the copper layer, where drawn shapes represent copper that stays. This negative convention confuses many beginners — if you see a rectangle in the soldermask file, it means "remove soldermask here" to expose the pad.
</details>

**Q4:** On the Pupper board, top copper is red and bottom copper is blue. If a trace needs to cross another trace on the same layer, how does it get from red to blue and back?
<details>
<summary>Answer</summary>
**Through vias.** The trace on the top copper (red) reaches a via — a small plated hole that connects to the bottom copper (blue). The trace continues on the bottom layer, passing under the obstruction, then hits another via to return to the top layer. Each via appears in the drill file (PTH-Via) and has a pad on both copper layers. On the Pupper board, the small teal dots scattered across the board are these vias. See [[learning/notes/quick-context/pcb-printed-circuit-board]] for the detailed via cross-section.
</details>

**Q5:** A manufacturer receives Gerber files for a board but the paste mask file is missing. Can they still manufacture and assemble the board?
<details>
<summary>Answer</summary>
**They can fabricate (manufacture) the bare PCB, but assembly becomes problematic.** The paste mask file is only needed to cut the solder stencil for SMD assembly — it's not part of the physical board itself. The bare PCB only needs copper, soldermask, silkscreen, outline, and drill files. However, without a paste mask, the assembler can't make a proper stencil, so they'd have to generate one from the copper layer (less accurate, since paste openings should be smaller than pads) or apply solder paste manually (unreliable for fine-pitch parts). Through-hole components would be unaffected since they're hand-soldered or wave-soldered without paste.
</details>

</details>
