---
topic: PCB Assembly Files — BOM & CPL (Pick-and-Place)
created: 2026-06-05
---

# PCB Assembly Files — BOM & CPL (Pick-and-Place)

> **Related:** [[learning/notes/quick-context/pupper-bom-control-board]] | [[learning/notes/quick-context/comparator-specification]] | [[learning/notes/quick-context/tensile-strength-materials]] | [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement]] | [[learning/notes/quick-context/pcb-layers]]

> **TL;DR:** [[learning/notes/quick-context/bare-minimal-data-storage-circuit|When]] you send a board [[learning/notes/micro-context/push-pull-vs-open-drain|out]] for assembly, [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] spreadsheets travel with [[learning/notes/quick-context/capacitance|the]] bare-board files: the **BOM** (Bill of [[learning/notes/quick-context/cnc-machining|Materials]]) lists *[[learning/notes/quick-context/bare-minimal-data-storage-circuit|what]] parts to buy* — grouped [[learning/notes/quick-context/ram-addressing-decoder|one]] row per unique part — [[learning/notes/micro-context/push-pull-vs-open-drain|and]] the **CPL** (Component Placement List, a.k.a. pick-and-place file) lists *where each part goes* — one row per physical component, with XY coordinates, rotation, and which side of the board. They are joined by the **[[learning/notes/quick-context/comparator|reference]] designator** (Q1, C50, R15…), and you need [[learning/notes/quick-context/bjt-specifications|both]].

## The Core Problem

A bare PCB is just patterned copper — empty pads. A contract [[learning/notes/quick-context/code-to-gates-and-bootstrapping|assembler]] (JLCPCB, PCBWay) needs two questions answered before a machine [[learning/notes/quick-context/embedded-communication-protocols|can]] populate it: **what** [[learning/notes/quick-context/tensor|components]] to load, and **where/how** to drop each one. The BOM answers "what + how many + from which supplier"; the CPL answers "exact position + angle + [[learning/notes/quick-context/keypress-to-pixel-pipeline|top]] or [[learning/notes/quick-context/keypress-to-pixel-pipeline|bottom]]." Miss either file (or mismatch a designator between them) and the assembly stops. The `PDB_BOM.csv` and `PDB_CPL.csv` here are exactly this pair for the Pupper **[[learning/notes/quick-context/d-flip-flop|Power]] Distribution Board (PDB)**.

## 5 Essential Terms

| Term | [[learning/notes/quick-context/capacitance|Definition]] |
|------|------------|
| **BOM (Bill of Materials)** | The purchasing list — **one row per unique part [[learning/notes/quick-context/bjt-specifications|type]]**, with quantity, the [[learning/notes/quick-context/resistor|value]], [[learning/notes/quick-context/common-ic-packages|footprint]], manufacturer part number (MPN), and supplier catalog number. It's the recipe for *buying*. |
| **CPL / Pick-and-Place** | The placement list — **one row per physical component**, giving centroid XY, rotation, board side, and pin [[learning/notes/quick-context/switches-to-registers-storing-data|count]]. It's the instructions for *placing*. See [[learning/notes/micro-context/pick-and-place-file|Pick and Place File]]. |
| **Reference Designator** | The unique ID stamped on each part: `Q`=[[learning/notes/quick-context/silicon-die|transistor]], `C`=[[learning/notes/quick-context/capacitor|cap]], `R`=[[learning/notes/quick-context/resistor|resistor]], `D`=[[learning/notes/quick-context/diode|diode]], `U`=IC, `CN`/`J`=[[learning/notes/quick-context/qwiic-stemma-qt-i2c|connector]], `SW`=[[learning/notes/quick-context/switches-to-registers-storing-data|switch]]. **This is the join key** linking BOM ↔ CPL ↔ schematic ↔ silkscreen. |
| **Footprint** | The physical [[learning/notes/quick-context/bga-ball-grid-array|pad]] pattern / [[learning/notes/quick-context/silicon-die|package]] the part solders to (`C0402`, `SOT-23-5`, `SMA`, `PG-TDSON-8`). [[learning/notes/quick-context/ros2-architecture|Must]] match the real part exactly, or it won't fit. |
| **Centroid + Rotation + [[learning/notes/quick-context/pcb-printed-circuit-board|Layer]]** | The [[learning/notes/quick-context/ram-addressing-decoder|four]] numbers the machine actually needs: **Mid X/Y** (part center), **Rotation** (degrees CCW), and **Layer** (`T` top / `B` bottom). `SMD = Yes/No` tells it surface-mount vs through-hole. |

<details>
<summary><strong>How It Works</strong> — Two files, one join key</summary>

The two files describe the **same components from two angles**. The BOM *groups* — [[learning/notes/quick-context/ram-addressing-decoder|identical]] parts collapse into one line whose `Designator` field lists every instance (`Q1,Q2`). The CPL *expands* — every instance gets its own row with a unique position. The reference designator is what stitches them back together.

```
ONE PART, TWO FILES — joined by the reference designator
══════════════════════════════════════════════════════════════════

  BOM  (what to buy — grouped, one row per part type)
  ┌─────┬───────────────┬────────────┐
  │ Qty │ Comment       │ Designator │
  ├─────┼───────────────┼────────────┤
  │  2  │ BSC067N06LS3G │ Q1,Q2      │
  └─────┴───────────────┴────────────┘
              │  "Q1,Q2" = 2 designators
              ▼  expands into the 2 CPL rows below
  CPL  (where to place — one row per component)
  ┌────────┬───────────────┬───────┬───────┬─────┬───────┐
  │ Desig. │ Device        │ Mid X │ Mid Y │ Rot │ Layer │
  ├────────┼───────────────┼───────┼───────┼─────┼───────┤
  │  Q1    │ BSC067N06LS3G │ 21mm  │ 7.25  │ 90  │  T    │
  │  Q2    │ BSC067N06LS3G │ 21mm  │ 12.75 │ 90  │  T    │
  └────────┴───────────────┴───────┴───────┴─────┴───────┘

  BOM says: buy 2× this MOSFET (supplier C24199, LCSC)
  CPL says: one at (21, 7.25), one at (21, 12.75), top side, 90°
```

**A built-in sanity check:** the sum of all BOM quantities must equal the number of CPL rows. In this PDB the BOM lists 18 part types totaling **36 parts**, and the CPL has exactly **36 component rows**. If they don't match, a designator was dropped or duplicated.

**Where these fit in the [[learning/notes/quick-context/singular-value-decomposition|full]] hand-[[learning/notes/quick-context/bjt-specifications|off]]:** the assembler also needs the [[learning/notes/quick-context/pcb-layers|Gerber]] files (to make/identify the bare board). Gerbers = the board, BOM = the parts, CPL = the placement.

```
ASSEMBLY HAND-OFF PACKAGE
══════════════════════════════════════════════

   Gerbers ──► fabricate / load the bare PCB
   BOM     ──► order + load component reels
   CPL     ──► program the pick-and-place machine
                       │
                       ▼
              solder paste ► place parts ► reflow oven
                       │
                       ▼
                 populated board
```

</details>

<details>
<summary><strong>[[learning/notes/quick-context/3d-printing-filament-types|The Key Tension]]</strong> — Grouped vs. per-instance, and export gotchas</summary>

**[[learning/notes/quick-context/atoms-molecules-polymers-basics|Why]] two files instead of one?** Because the two consumers want opposite shapes. The *purchasing* side wants parts grouped (you [[learning/notes/quick-context/frequency-and-filtering|order]] "2 MOSFETs," [[learning/notes/micro-context/can-bus-termination|not]] "a [[learning/notes/quick-context/transistor|MOSFET]] at (21, 7.25)"). The *placement machine* wants them exploded (it places one part at a time and couldn't care less what it costs). Cramming both into one table would either repeat purchasing data 36 times or hide the positions.

| | BOM | CPL |
|---|---|---|
| Row granularity | one per **part type** | one per **component** |
| Key [[learning/notes/quick-context/code-to-gates-and-bootstrapping|fields]] | Qty, MPN, supplier # | Mid X/Y, Rotation, Layer |
| Answers | *what / how many / from where* | *where / what angle / which side* |
| Has positions? | No | Yes |
| Has purchasing info? | Yes | No |

**The gotchas that bite people reading these files:**

- **[[learning/notes/quick-context/how-source-code-is-stored|Encoding]].** These exports are often **UTF-16, tab-delimited** (note the [[learning/notes/quick-context/how-source-code-is-stored|byte]]-order mark and "spaced-out" look in a raw viewer). Open in a spreadsheet and pick *Tab* as the delimiter, or they look like garbage.
- **[[learning/notes/quick-context/pupper-lab2-forward-kinematics|Rotation conventions]] differ.** Degrees are counter-clockwise, but the "zero" orientation isn't standardized across EDA tools and fab houses — a part right in your [[learning/notes/quick-context/epson-rc-plus-programming|tool]] can land 90°/180° off at the assembler[[learning/notes/quick-context/glass-transition-temperature|. This is the]] #1 cause of reversed diodes and ICs.
- **Missing/placeholder fields.** Watch for literal placeholders like `{Manufacturer Part!}` — in this PDB that appears for **J2** and **U40**, meaning the designer never filled the field. The assembler can't [[learning/notes/quick-context/differential-pair|source]] those automatically; you must supply the part manually.
- **No supplier number = manual sourcing.** Blank `Supplier Part` rows (the passives here: caps, most resistors) aren't in the assembler's standard library and need to be specified or consigned.

</details>

<details>
<summary><strong>Concrete Example</strong> — Decoding one real BOM line and its CPL rows</summary>

Take the power [[learning/notes/micro-context/mosfet|MOSFET]] on this board, `BSC067N06LS3G` (an Infineon 60 V N-[[learning/notes/quick-context/transistor|channel]] power FET — the `06` ≈ 60 V class).

**Its BOM line (grouped):**

```
No.          : 10
Quantity     : 2
Comment      : BSC067N06LS3G          ← the part name
Designator   : Q1,Q2                  ← TWO instances on the board
Footprint    : PG-TDSON-8_L5.0-W6.0-P1.27-LS6.2-BL-EP
Value        : (blank)
Manufacturer Part : BSC067N06LS3G     ← exact orderable MPN
Manufacturer      : Infineon
Supplier Part     : C24199            ← LCSC catalog #  → lcsc.com/C24199
Supplier          : LCSC              ← available for automated assembly
```

**Its two CPL rows (per instance):**

```
Designator│ Device       │ Mid X │ Mid Y  │ Pad X  │ Pad Y │Pins│Layer│Rot│SMD
──────────┼──────────────┼───────┼────────┼────────┼───────┼────┼─────┼───┼────
  Q1      │ BSC067N06LS3G│ 21mm  │ 7.25mm │23.865  │ 5.345 │ 9  │  T  │90 │Yes
  Q2      │ BSC067N06LS3G│ 21mm  │12.75mm │23.865  │10.845 │ 9  │  T  │90 │Yes
```

- **Mid X / Mid Y** = the part's center — where the [[learning/notes/quick-context/3d-printer-hotends|nozzle]] aims.
- **Ref X / Ref Y** = the placement origin (here same as Mid).
- **Pad X / Pad Y** = location of pin-1 pad — lets you verify orientation independent of rotation.
- **Pins = 9** (8 leads + the exposed thermal pad), **Layer = T**, **Rotation = 90°**, **SMD = Yes**.

Reading both together you know: *buy two Infineon FETs from LCSC C24199, place one mid-board and one 5.5 mm above it, both top side, rotated 90°.* The rest of this PDB reads the same way — power MOSFETs (Q1, Q2), protection diodes (D2–D4 — SMAJ12A TVS plus a [[learning/notes/quick-context/diode|Zener]]), a [[learning/notes/quick-context/comparator|comparator]] (U40), a small [[learning/notes/quick-context/power-watts-joules|linear regulator]] (U42, a 78L12), and a dozen [[learning/notes/quick-context/dupont-jumper-wires|JST connectors]] ([[learning/notes/micro-context/jst-connector-families|JST ZR family]]) for battery/cell wiring.

**[[learning/notes/quick-context/bjt-specifications|The one thing most outsiders get wrong about this is]]...** thinking the two files are redundant, or that the BOM contains positions. They're complementary halves: the BOM has zero geometry, the CPL has zero purchasing info, and the **reference designator is the only thing connecting them**. Lose the join (rename `Q1`→`Q3` in one file but not the other) and the assembler places a part it can't identify, or orders a part it can't place.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/quick-context/pupper-bom-control-board]]** — A full part-by-part teardown of the Pupper *Control Board* BOM. That note explains WHAT each part does; this note explains how to READ the BOM/CPL file pair itself.
- **[[learning/notes/micro-context/pick-and-place-file]]** — The glossary-level definition of the CPL and the SMT machine workflow it drives.
- **[[learning/notes/quick-context/pcb-layers]]** — The Gerber/paste-mask files that accompany the BOM + CPL in the assembly hand-off; the paste layer defines the solder stencil.
- **[[learning/notes/quick-context/schematic-reading]]** — Reference designators are the bridge between the schematic, the BOM, the CPL, and the physical silkscreen.
- **[[learning/notes/quick-context/common-ic-packages]]** — Decoding the `Footprint` field (SOT-23, SMA, TDSON) and why package [[learning/notes/quick-context/transistor-analog-to-digital|choice]] gates hand vs. machine assembly.
- **[[learning/notes/quick-context/soldering]]** — What happens after placement: solder paste + [[learning/notes/quick-context/bga-ball-grid-array|reflow]] permanently bond every part the CPL positioned.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A BOM line has `Quantity = 8` and a `Designator` field listing `CN6,CN7,CN9,CN10,CN12,CN13,CN15,CN16`. How many rows should that part produce in the CPL?
<details>
<summary>Answer</summary>
**Eight** — one CPL row per designator. The BOM groups [[learning/notes/quick-context/ram-addressing-decoder|all eight]] identical JST connectors into a single purchasing line (buy 8), but the pick-and-place machine places them one at a time, so each gets its own CPL row with a unique Mid X/Y and rotation. (This is exactly the `B6B-ZR-SM4-TF` connector in this PDB.) See *How It Works*.
</details>

**Q2:** Which file tells you the supplier part number to order, and which tells you the board side a part sits on?
<details>
<summary>Answer</summary>
**BOM** has the `Supplier Part` (e.g. LCSC `C24199`) and `Manufacturer Part`. **CPL** has the `Layer` field (`T` = top, `B` = bottom). Neither field appears in the other file — that's why you need both. See *The Key Tension* table.
</details>

**Q3:** You open `PDB_CPL.csv` in a [[learning/notes/quick-context/how-source-code-is-stored|text]] editor and every [[learning/notes/quick-context/how-source-code-is-stored|character]] looks separated by spaces, with odd [[learning/notes/quick-context/how-source-code-is-stored|bytes]] at the start. What's going on and how do you read it?
<details>
<summary>Answer</summary>
**It's UTF-16 encoded with a byte-order mark, tab-delimited.** The "spaces" are the high (zero) bytes of each 16-bit character. Open it in a spreadsheet and choose **Tab** as the delimiter (and UTF-16 encoding if prompted), or convert to [[learning/notes/quick-context/how-source-code-is-stored|UTF-8]] first. It is not corrupted. See *The Key Tension → Encoding*.
</details>

**Q4:** The BOM lists `{Manufacturer Part!}` in the Comment/MPN field for `J2` and `U40`. Why can't the assembler just build the board anyway?
<details>
<summary>Answer</summary>
**That placeholder means the part field was never filled in** by the design tool, so there is no orderable part for that designator. The pad/footprint exists on the board, but the assembler doesn't know *which physical component* to buy and place. You must supply the real MPN (for U40 the CPL actually reveals it as `LMC7211AIM5/NOPB`) before that position can be populated. See *The Key Tension → Missing fields*.
</details>

**Q5:** Why isn't the BOM+CPL pair enough on its own to manufacture an assembled board — what third thing is required, and why?
<details>
<summary>Answer</summary>
**You also need the [[learning/notes/quick-context/pcb-layers|Gerber]] files.** BOM + CPL describe the *components and their placement*, but assume a finished bare board already exists. The Gerbers define the copper, drill [[learning/notes/quick-context/bjt-specifications|holes]], solder mask, silkscreen, and — critically for SMT — the **paste mask** that becomes the stencil for depositing solder paste. Without paste, placed parts have [[learning/notes/quick-context/tlv7211-as-lmc7211-replacement|nothing]] to bond to during reflow. Gerbers = the board, BOM = the parts, CPL = the placement; all three are the assembly hand-off. See *How It Works → assembly hand-off*.
</details>

</details>
