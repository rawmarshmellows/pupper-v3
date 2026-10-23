---
term: CNC Milling
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# CNC Milling

> **See also:** [[quick-context/cnc-machining]] ([[learning/notes/quick-context/singular-value-decomposition|full]] treatment) | [[quick-context/3d-printing-filament-types]] | [[quick-context/tensile-strength-materials]]

**[[learning/notes/quick-context/capacitance|Definition]]:** A subtractive manufacturing process where a computer-controlled rotating cutter removes material from a solid block (workpiece) to create precise parts. [[learning/notes/quick-context/capacitance|The]] opposite of 3D printing—you start with more material than you need [[learning/notes/micro-context/push-pull-vs-open-drain|and]] carve away the excess.

## How It Works

- A rotating multi-edge cutter (end mill) is mounted in a motorized spindle that spins at thousands of RPM.
- The CNC controller moves either the spindle or the workpiece table along X, Y, and Z axes according to [[learning/notes/quick-context/3d-printing-slicer-settings|G-code]].
- Each pass removes a thin [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|layer]] of material as chips, gradually carving the programmed geometry from the block.

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

**Key insight:** [[learning/notes/quick-context/cnc-machining|CNC milling]] produces parts with full material [[learning/notes/quick-context/cnc-machining|strength]] (no [[learning/notes/quick-context/3d-printing-filament-types|layer adhesion]] weakness like FDM prints), but wastes material as chips and [[learning/notes/quick-context/embedded-communication-protocols|can]]'t create fully enclosed [[learning/notes/quick-context/cnc-machining|internal cavities]].
