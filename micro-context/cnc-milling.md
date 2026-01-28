---
term: CNC Milling
created: 2026-01-27
---

# CNC Milling

> **See also:** [[quick-context/3d-printing-filament-types]] | [[quick-context/tensile-strength-materials]]

**Definition:** A subtractive manufacturing process where a computer-controlled rotating cutter removes material from a solid block (workpiece) to create precise parts. The opposite of 3D printing—you start with more material than you need and carve away the excess.

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
