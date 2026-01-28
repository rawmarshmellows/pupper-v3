---
topic: 3D Printing Slicer Settings
created: 2026-01-20
updated: 2026-01-21
---

> **Related:** [[quick-context/3d-printing-filament-types]] | [[quick-context/3d-printer-hotends]]

> **TL;DR:** A slicer converts 3D models into printer instructions by cutting models into layers, planning nozzle paths, and applying settings like temperature and speed; settings interact multiplicatively (layer height x nozzle width x speed = flow rate), and understanding these interactions prevents failed prints.

# 3D Printing Slicer Settings: Absolute Beginner Guide

## How 3D Printing Works (30-second version)

A 3D printer works like a hot glue gun on a robot arm. It melts plastic [[quick-context/3d-printing-filament-types|filament]] (a long spool of plastic wire) and squirts it out layer by layer, building up an object from the bottom. Each layer is maybe 0.2-0.3mm thick—about 2-3 sheets of paper. Stack enough layers and you get a 3D object.

A **slicer** is software that takes your 3D model and converts it into instructions the printer understands: "move here, squirt plastic, move there, squirt more." The settings below control *how* it does this.

---

<details>
<summary><strong>How It Works</strong></summary>

The slicer performs three essential transformations on your 3D model. First, **slicing**: it cuts your model into horizontal layers (like slicing a loaf of bread), with each slice becoming one pass of the print head. Second, **pathing**: for each layer, it plans the exact route the nozzle will travel—where to start, which direction to move, when to extrude plastic, when to retract. Third, **parameter application**: it applies your settings (temperature, speed, infill pattern, etc.) to generate the final machine instructions. The output is G-code, a text file of line-by-line commands that tell motors exactly where to move and heaters exactly what temperature to maintain.

The relationship between settings is multiplicative, not independent. Layer height and nozzle width together determine how much plastic exits per millimeter of travel. Print speed multiplied by that cross-section gives you the **volumetric flow rate** (mm³/s)—which must stay within your [[quick-context/3d-printer-hotends|hotend's]] melting capacity. Setting a 0.8mm nozzle with 0.4mm layer height at 150mm/s demands ~48 mm³/s, which exceeds most standard hotends. The slicer doesn't warn you; it just sends commands the hardware can't fulfill, resulting in under-extrusion and failed prints. Understanding how settings interact prevents this.

```
THE SLICING PROCESS: From Model to Machine Instructions
═══════════════════════════════════════════════════════════════════

STAGE 1: Your 3D Model (STL/3MF file)
─────────────────────────────────────
     A solid digital object
          ╱╲
         ╱  ╲
        ╱    ╲
       ╱      ╲
      ╱________╲
     │          │
     │          │
     │__________|

           │
           ▼

STAGE 2: Slicing (cutting into layers)
──────────────────────────────────────
  Layer height determines how many slices

  0.3mm layers (faster)      0.1mm layers (smoother)
  ┌──────────────────┐       ┌──────────────────┐
  │ ═══════════════  │       │ ─────────────────│
  │ ═══════════════  │       │ ─────────────────│
  │ ═══════════════  │       │ ─────────────────│
  │ ═══════════════  │       │ ─────────────────│
  │ ═══════════════  │       │ ─────────────────│
  │ ═══════════════  │       │ ─────────────────│
  │ ═══════════════  │       │ ─────────────────│
  └──────────────────┘       │ ─────────────────│
    ~7 layers                │ ─────────────────│
    (fast to print)          └──────────────────┘
                               ~21 layers
                               (3x longer to print)

           │
           ▼

STAGE 3: Pathing (planning nozzle movement for each layer)
──────────────────────────────────────────────────────────

  Single layer, top view:

  ┌─────────────────────────────────────┐
  │ WALLS (perimeters)                  │
  │ ┌─────────────────────────────────┐ │
  │ │ ┌─────────────────────────────┐ │ │  ← 3 walls = 3 outlines
  │ │ │ ┌─────────────────────────┐ │ │ │
  │ │ │ │                         │ │ │ │
  │ │ │ │   INFILL (interior)     │ │ │ │
  │ │ │ │   ╱╲  ╱╲  ╱╲  ╱╲       │ │ │ │  ← 15% infill =
  │ │ │ │  ╱  ╲╱  ╲╱  ╲╱  ╲      │ │ │ │    sparse honeycomb
  │ │ │ │ ╱╲  ╱╲  ╱╲  ╱╲  ╱╲    │ │ │ │
  │ │ │ │╱  ╲╱  ╲╱  ╲╱  ╲╱  ╲   │ │ │ │
  │ │ │ │                         │ │ │ │
  │ │ │ └─────────────────────────┘ │ │ │
  │ │ └─────────────────────────────┘ │ │
  │ └─────────────────────────────────┘ │
  └─────────────────────────────────────┘

  Nozzle path: Walls first (outside-in or inside-out),
               then infill pattern, then travel to next area

           │
           ▼

STAGE 4: G-code Output (machine instructions)
─────────────────────────────────────────────

  G28              ; Home all axes
  M104 S230        ; Set nozzle temp to 230°C
  M140 S70         ; Set bed temp to 70°C
  G1 X50 Y50 F3000 ; Move to position (50,50) at 3000mm/min
  G1 Z0.3          ; Set height to 0.3mm (first layer)
  G1 E5 F300       ; Extrude 5mm of filament (prime)
  G1 X150 E20 F1800; Move to X150, extruding, at 1800mm/min
  ...              ; Thousands more lines

  Each line = one command to the printer
  A typical print = 100,000+ G-code lines


HOW SETTINGS INTERACT: The Flow Rate Equation
═════════════════════════════════════════════

  Layer     Nozzle    Print       Volumetric
  Height  ×  Width  ×  Speed   =   Flow Rate
  (mm)       (mm)     (mm/s)      (mm³/s)

  Example calculations:

  0.2mm  ×  0.4mm  ×  60mm/s  =   4.8 mm³/s   ✓ Easy for any hotend
  0.3mm  ×  0.6mm  ×  80mm/s  =  14.4 mm³/s   ✓ Standard hotend limit
  0.4mm  ×  0.8mm  × 100mm/s  =  32.0 mm³/s   ✗ Needs high-flow hotend!

  If flow rate exceeds hotend capacity → under-extrusion → failed print
```

</details>

---

## Your Settings Explained

### Material: PETG

**What it is**: The type of plastic you're feeding through the printer.

**[[quick-context/3d-printing-filament-types|PETG]]** is a specific plastic (polyethylene terephthalate glycol). Think of it like choosing between materials for a water bottle—some plastics are flimsy, some are tough.

- **[[quick-context/3d-printing-filament-types|PLA]]**: The "easy mode" plastic. Prints easily, but brittle and melts in hot cars (~60°C)
- **PETG**: Tougher, slightly flexible, survives heat better (~80°C), but trickier to print
- **ABS**: Very tough, but warps easily and produces fumes

**Your choice (PETG)**: Good for functional parts that need to survive real use.

---

### Infill: 15%

**What it is**: How solid the inside of your print is.

3D prints are NOT solid plastic inside—that would waste material and time. Instead, the inside has a pattern (usually honeycomb or grid) that provides structure while being mostly air.

```
100% infill     vs     15% infill
┌──────────┐          ┌──────────┐
│██████████│          │▓░░░▓░░░▓│
│██████████│          │░░░░░░░░░│
│██████████│          │▓░░░▓░░░▓│
│██████████│          │░░░░░░░░░│
└──────────┘          └──────────┘
 Solid, slow,           Light, fast,
 uses lots of           uses less
 plastic                plastic
```

**15%** means only 15% of the interior volume is plastic. The rest is air with a sparse support pattern.

**Your choice (15%)**: Fast prints, light parts. Fine for most things unless you need to bolt through it or it takes heavy loads.

---

### Support: On build plate - Tree (auto)

**What it is**: Temporary scaffolding for parts that stick out in mid-air.

**The problem**: Printers build bottom-up. If your model has parts that stick out horizontally (like a character's outstretched arm), there's nothing underneath to support the plastic as it's laid down. It would just droop or fall.

```
Without support:              With support:

    ┌───┐  ← arm droops          ┌───┐  ← arm prints correctly
   /    │                        │   │
  ▼     │                       ╱│   │
        │                      ╱ │   │
        │                     ╱  │   │
   ─────┴─────              ─╱───┴───╱─
                             ↑ support structure
                               (removed after printing)
```

**"Tree" support**: Instead of a solid block under overhangs, it grows branch-like structures from the build plate up to where they're needed. Easier to snap off and leaves cleaner surfaces.

**"On build plate"**: Support only grows from the bottom plate, not from the model itself. Simpler but can't reach all overhangs.

**Your choice**: You have some overhangs, but want supports that are easy to remove.

---

### Walls: 3

**What it is**: How many solid outlines make up the outer shell of your print.

Before filling in the inside with infill, the printer traces the outline of each layer—like drawing the edges of a shape before coloring it in. More outlines = thicker, stronger outer shell.

```
Cross-section view:

1 wall:          3 walls:
┌────────┐       ┌────────┐
│░░░░░░░░│       │▓▓▓░░▓▓▓│
│░░░░░░░░│       │▓░░░░░░▓│
│░░░░░░░░│       │▓░░░░░░▓│
│░░░░░░░░│       │▓▓▓░░▓▓▓│
└────────┘       └────────┘
 Thin shell,      Thick shell,
 weak edges       strong edges

░ = infill (sparse interior)
▓ = solid wall
```

**Your choice (3 walls)**: A good middle ground. The edges of your part will be solid and reasonably strong.

---

### Layer Height: 0.3mm

**What it is**: How thick each horizontal layer is.

Remember, the printer builds objects by stacking thin layers. Thinner layers = smoother surfaces but more layers to print (slower). Thicker layers = faster but you can see/feel the "stair steps."

```
0.1mm layers:           0.3mm layers:
    ╭─────╮                 ┌─────┐
   ╱       ╲               ╱│     │
  ╱         ╲             ╱ │     │
 ╱           ╲           ╱  │     │
╱             ╲         ╱   │     │
───────────────         ─────┴─────
Smooth curves,          Visible steps,
takes 3x longer         much faster
```

**0.3mm** is on the thick/fast end. You'll see layer lines, but prints finish quickly.

**Your choice**: Speed over beauty. Good for prototypes and functional parts where appearance doesn't matter.

---

### Nozzle Diameter: 0.6mm

**What it is**: The size of the hole the melted plastic comes out of.

Think of it like choosing between a fine-tip pen and a marker:
- **0.4mm** (standard): Good balance of detail and speed
- **0.2mm** (small): Fine details, very slow
- **0.6mm** (large): Fast printing, can't do fine details

```
0.4mm nozzle:     0.6mm nozzle:
───────────       ━━━━━━━━━━━
thin lines,       thick lines,
more passes       fewer passes
needed            needed
```

**Your choice (0.6mm)**: You're printing fast, chunky parts. Small text or fine details will look blobby.

---

## What Your Settings Mean Together

```
PETG + 15% infill + 3 walls + 0.3mm layers + 0.6mm nozzle
                           ↓
        "Fast functional prototype mode"
```

This setup prioritizes **speed over appearance**. You'll get:
- Parts that are reasonably strong (PETG + 3 walls)
- Prints that finish relatively quickly (thick layers + wide nozzle + low infill)
- Visible layer lines and no fine detail
- Parts that won't melt in a hot car

**Good for**: Robot parts, brackets, cases, anything functional
**Bad for**: Display pieces, gifts, anything with fine text or details

---

<details>
<summary><strong>The Key Tension</strong></summary>

The fundamental tension in slicer settings is **speed vs. quality vs. strength**. Thicker layers print faster but show visible stepping. Higher infill increases strength but wastes material and time. Faster print speeds reduce quality and can exceed hotend flow capacity. Every setting is a tradeoff, and the "best" profile depends entirely on what you're making—a display piece needs thin layers and slow speeds, while a functional bracket prioritizes walls and can tolerate thick layers.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## The One Thing Beginners Get Wrong

People think "more infill = stronger part." Not really. A part with **3 walls and 15% infill** is often stronger than **2 walls and 50% infill** because the outer shell carries most of the load in real-world use. Cranking infill to 100% wastes plastic and time for minimal strength gain.

**The one thing most outsiders get wrong about this is...** assuming that slicer settings are independent of each other. In reality, layer height, nozzle width, and print speed combine multiplicatively to determine volumetric flow rate—and if that exceeds your hotend's capacity, you get weak parts with poor layer adhesion regardless of what your other settings say.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

Concepts that connect to slicer settings and deepen your understanding:

- **[[quick-context/3d-printing-filament-types]]** — Different plastics require different slicer profiles. PLA prints cooler and faster; PETG needs higher temps and slower speeds; ABS requires enclosures. Your material choice drives half your slicer decisions.

- **[[quick-context/3d-printer-hotends]]** — The [[quick-context/3d-printer-hotends|hotend]] melts filament before extrusion. Its max temperature limits which materials you can print, and its heat break design affects how fast you can push plastic through (volumetric flow rate).

- **[[quick-context/melt-index]]** — Measures how easily a plastic flows when melted. High melt index plastics flow freely and print faster but may string more. Low melt index plastics are stiffer, need higher temps, and print slower.

- **[[quick-context/glass-transition-temperature]]** — The temperature where a plastic goes from rigid to rubbery. This determines both print bed temperature (to help adhesion without warping) and the max operating temperature of your finished part.

</details>

---

<details>
<summary><strong>Test Your Understanding</strong></summary>

<details>
<summary>Why might you increase wall count instead of infill percentage when you need a stronger part?</summary>

The outer walls carry most of the structural load in real-world use because forces typically act on the surface of a part. Increasing walls from 3 to 4-5 adds solid material where stress concentrates, while increasing infill adds material to the interior where it contributes less to strength. A part with 4 walls and 15% infill is often stronger than one with 2 walls and 50% infill, while using similar amounts of material and print time.
</details>

<details>
<summary>If you switch from PLA to PETG mid-project, which slicer settings would you need to adjust and why?</summary>

You would need to increase:
- **Nozzle temperature**: PETG melts at ~230-250°C vs PLA's ~200-220°C
- **Bed temperature**: PETG needs ~70-80°C vs PLA's ~50-60°C
- **Retraction settings**: PETG is stringier, may need different retraction distance/speed
- **Print speed**: Often slower for PETG to allow proper layer adhesion
- **Cooling**: PETG typically needs less part cooling than PLA

These changes account for PETG's higher glass transition temperature and different flow characteristics.
</details>

<details>
<summary>When would you choose a 0.2mm layer height over your current 0.3mm setting?</summary>

Choose thinner layers (0.2mm) when:
- Printing parts with curved or angled surfaces where "stair-stepping" would be visible and objectionable
- Creating display pieces, gifts, or anything where surface finish matters
- Printing parts with fine details or small text that would blob together at 0.3mm
- Making parts that need to fit precisely with other components (tolerances matter)

The trade-off is print time—0.2mm layers take roughly 50% longer than 0.3mm layers for the same part.
</details>

<details>
<summary>What problem does "tree support" solve that regular block supports don't?</summary>

Tree supports branch upward from the build plate to reach overhangs, touching the model only where absolutely necessary. Regular block supports create solid walls of material directly under overhangs. Tree supports solve several problems:
- **Easier removal**: Branch tips snap off cleanly vs prying away solid blocks
- **Better surface finish**: Minimal contact points mean fewer support scars on the final part
- **Less material waste**: Branches use far less filament than solid blocks
- **Access to interior overhangs**: Can sometimes reach places block supports can't

The trade-off is slightly longer slicing time and occasionally less stability for very heavy overhangs.
</details>

<details>
<summary>Two filaments have identical melting points (240°C), but one is semi-crystalline and one is amorphous. Why might the same slicer profile produce good results with one but failures with the other?</summary>

Melting point is just one property—[[quick-context/polymer-crystallinity-vs-amorphous|crystallinity]] and [[quick-context/glass-transition-temperature|Tg]] profoundly affect printing behavior. A semi-crystalline material releases heat as it crystallizes during cooling, potentially staying soft longer than an amorphous material at the same temperature. Different Tg values mean different "working windows" where the material is moldable but not too soft. A material with Tg close to room temperature might warp as the print cools past Tg, while one with high Tg could crack from thermal stress. The semi-crystalline material may need slower cooling (for proper crystal formation), different bed temps (to manage warping differently), and adjusted retraction (crystallizing material behaves differently during ooze). The slicer sees temperature; the physics depends on molecular architecture. See: [[quick-context/polymer-crystallinity-vs-amorphous]] for how structure affects thermal behavior.
</details>

</details>
