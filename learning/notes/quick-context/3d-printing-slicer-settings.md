---
topic: 3D Printing Slicer Settings
created: 2026-01-20
updated: 2026-01-21
---

> **Related:** [[learning/notes/quick-context/3d-printing-filament-types]] | [[learning/notes/quick-context/3d-printer-hotends]] | [[learning/notes/quick-context/glass-transition-temperature]] | [[learning/notes/quick-context/melt-index]]

> **TL;DR:** A slicer converts 3D models into printer instructions by cutting models into layers, planning nozzle paths, and applying settings like temperature and speed; settings interact multiplicatively (layer height x nozzle width x speed = flow rate), and understanding these interactions prevents failed prints.

## The Core Problem

A slicer converts 3D models into printer instructions by cutting models into layers, planning nozzle paths, and applying settings like temperature and speed. The challenge is that settings interact multiplicatively (layer height x nozzle width x speed = flow rate), and understanding these interactions prevents failed prints.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Layer height** | Thickness of each horizontal layer (thinner = smoother but slower) |
| **Infill** | Percentage of interior that's solid plastic vs air (15% = mostly hollow) |
| **Walls/perimeters** | Number of solid outlines on the exterior shell |
| **Volumetric flow rate** | How much plastic (mm³/s) must melt and extrude—limited by hotend capacity |
| **G-code** | The text file of line-by-line commands that tell the printer exactly what to do |

<details>
<summary><strong>How It Works</strong></summary>

The slicer performs three essential transformations on your 3D model. First, **slicing**: it cuts your model into horizontal layers (like slicing a loaf of bread), with each slice becoming one pass of the print head. Second, **pathing**: for each layer, it plans the exact route the nozzle will travel—where to start, which direction to move, when to extrude plastic, when to retract. Third, **parameter application**: it applies your settings (temperature, speed, infill pattern, etc.) to generate the final machine instructions. The output is G-code, a text file of line-by-line commands that tell motors exactly where to move and heaters exactly what temperature to maintain.

The relationship between settings is multiplicative, not independent. Layer height and nozzle width together determine how much plastic exits per millimeter of travel. Print speed multiplied by that cross-section gives you the **volumetric flow rate** (mm³/s)—which must stay within your [[learning/notes/quick-context/3d-printer-hotends|hotend's]] melting capacity. Setting a 0.8mm nozzle with 0.4mm layer height at 150mm/s demands ~48 mm³/s, which exceeds most standard hotends. The slicer doesn't warn you; it just sends commands the hardware can't fulfill, resulting in under-extrusion and failed prints. Understanding how settings interact prevents this.

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

<details>
<summary><strong>The Key Tension</strong></summary>

The fundamental tension in slicer settings is **speed vs. quality vs. strength**. Thicker layers print faster but show visible stepping. Higher infill increases strength but wastes material and time. Faster print speeds reduce quality and can exceed hotend flow capacity. Every setting is a tradeoff, and the "best" profile depends entirely on what you're making—a display piece needs thin layers and slow speeds, while a functional bracket prioritizes walls and can tolerate thick layers.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

People think "more infill = stronger part." Not really. A part with **3 walls and 15% infill** is often stronger than **2 walls and 50% infill** because the outer shell carries most of the load in real-world use. Cranking infill to 100% wastes plastic and time for minimal strength gain.

**The one thing most outsiders get wrong about this is...** assuming that slicer settings are independent of each other. In reality, layer height, nozzle width, and print speed combine multiplicatively to determine volumetric flow rate—and if that exceeds your hotend's capacity, you get weak parts with poor layer adhesion regardless of what your other settings say.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

Concepts that connect to slicer settings and deepen your understanding:

- **[[learning/notes/quick-context/3d-printing-filament-types]]** — Different plastics require different slicer profiles. PLA prints cooler and faster; PETG needs higher temps and slower speeds; ABS requires enclosures. Your material choice drives half your slicer decisions.

- **[[learning/notes/quick-context/3d-printer-hotends]]** — The [[learning/notes/quick-context/3d-printer-hotends|hotend]] melts filament before extrusion. Its max temperature limits which materials you can print, and its heat break design affects how fast you can push plastic through (volumetric flow rate).

- **[[learning/notes/quick-context/melt-index]]** — Measures how easily a plastic flows when melted. High melt index plastics flow freely and print faster but may string more. Low melt index plastics are stiffer, need higher temps, and print slower.

- **[[learning/notes/quick-context/glass-transition-temperature]]** — The temperature where a plastic goes from rigid to rubbery. This determines both print bed temperature (to help adhesion without warping) and the max operating temperature of your finished part.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why might you increase wall count instead of infill percentage when you need a stronger part?
<details>
<summary>Answer</summary>
The outer walls carry most of the structural load in real-world use because forces typically act on the surface of a part. Increasing walls from 3 to 4-5 adds solid material where stress concentrates, while increasing infill adds material to the interior where it contributes less to strength. A part with 4 walls and 15% infill is often stronger than one with 2 walls and 50% infill, while using similar amounts of material and print time.
</details>

**Q2:** If you switch from PLA to PETG mid-project, which slicer settings would you need to adjust and why?
<details>
<summary>Answer</summary>
You would need to increase nozzle temperature (PETG melts at ~230-250C vs PLA's ~200-220C), bed temperature (PETG needs ~70-80C vs PLA's ~50-60C), and adjust retraction settings (PETG is stringier). Print speed is often slower for PETG to allow proper layer adhesion, and cooling is typically reduced. These changes account for PETG's higher glass transition temperature and different flow characteristics.
</details>

**Q3:** When would you choose a 0.2mm layer height over a 0.3mm setting?
<details>
<summary>Answer</summary>
Choose thinner layers (0.2mm) when printing parts with curved or angled surfaces where stair-stepping would be visible, creating display pieces or gifts where surface finish matters, printing parts with fine details or small text, or making parts that need precise tolerances. The trade-off is print time—0.2mm layers take roughly 50% longer than 0.3mm layers for the same part.
</details>

**Q4:** What problem does tree support solve that regular block supports don't?
<details>
<summary>Answer</summary>
Tree supports branch upward from the build plate to reach overhangs, touching the model only where absolutely necessary. They provide easier removal (branch tips snap off cleanly), better surface finish (minimal contact points mean fewer support scars), less material waste (branches use far less filament), and sometimes better access to interior overhangs. The trade-off is slightly longer slicing time and occasionally less stability for very heavy overhangs.
</details>

**Q5:** Two filaments have identical melting points (240C), but one is semi-crystalline and one is amorphous. Why might the same slicer profile produce good results with one but failures with the other?
<details>
<summary>Answer</summary>
Melting point is just one property—crystallinity and glass transition temperature profoundly affect printing behavior. A semi-crystalline material releases heat as it crystallizes during cooling, potentially staying soft longer than an amorphous material at the same temperature. Different Tg values mean different working windows where the material is moldable but not too soft. The semi-crystalline material may need slower cooling, different bed temps, and adjusted retraction. The slicer sees temperature; the physics depends on molecular architecture.
</details>

</details>
