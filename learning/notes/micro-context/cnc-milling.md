---
term: CNC Milling
created: 2026-01-27
updated: 2026-03-27
---
> **Related:** [[learning/notes/quick-context/cnc-machining]] | [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]]


# CNC Milling

> **See also:** [[learning/notes/quick-context/cnc-machining]] (full treatment) | [[learning/notes/quick-context/3d-printing-filament-types]] | [[learning/notes/quick-context/tensile-strength-materials]]

**Definition:** A subtractive manufacturing process where a computer-controlled rotating cutter removes material from a solid block (workpiece) to create precise parts. The opposite of 3D printing—you start with more material than you need and carve away the excess.

## How It Works

- A rotating multi-edge cutter (end mill) is mounted in a motorized spindle that spins at thousands of RPM.
- The CNC controller moves either the spindle or the workpiece table along X, Y, and Z axes according to G-code.
- Each pass removes a thin layer of material as chips, gradually carving the programmed geometry from the block.

```
SUBTRACTIVE vs ADDITIVE:

  CNC MILLING                    3D PRINTING
  ───────────                    ───────────
  ┌─────────────┐                     ▄▄▄
  │█████████████│                   ▄█████▄
  │███┌─────┐███│  ← Remove       ████████████  ← Add
  │███│     │███│    material    ██████████████   material
  │███└─────┘███│                ████████████████
  └─────────────┘                ══════════════════
       Block                         Build plate

  Spindle with cutter:
       ║
      ╔╩╗
      ║░║  ← Rotating end mill
      ╚═╝    cuts into material
```

**Key insight:** CNC milling produces parts with full material strength (no layer adhesion weakness like FDM prints), but wastes material as chips and can't create fully enclosed internal cavities.
