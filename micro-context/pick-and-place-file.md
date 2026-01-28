---
term: Pick and Place File
created: 2026-01-27
---

# Pick and Place File

> **See also:** [[quick-context/pcb-printed-circuit-board]]

**Definition:** A spreadsheet (CSV/Excel) exported from PCB design software that tells automated assembly machines exactly where to place each component on a [[quick-context/pcb-printed-circuit-board|PCB]]—including XY coordinates, rotation angle, and which side of the board. Used by contract manufacturers (JLCPCB, PCBWay) to populate your bare PCB with components.

```
PICK AND PLACE WORKFLOW:

  PCB Design Software              Pick & Place File             Assembly Machine
  (KiCad, Altium, etc.)                                          (SMT line)
        │                                │                              │
        │   Export                       │                              │
        └──────────►  ┌─────────────────────────────────┐              │
                      │ Designator │ X     │ Y    │ Rot │              │
                      │──────────────────────────────────│   Program   │
                      │ U1         │ 5mm   │ 10mm │ 90° │ ──────────► │
                      │ C2         │ 8mm   │ 3mm  │ 0°  │              │
                      │ R3         │ 12mm  │ 7mm  │ 180°│     ┌───┐   │
                      └─────────────────────────────────┘     │ ▪ │ place
                                                              └───┘
```

**Key insight:** Without this file, someone would have to manually place hundreds of tiny components under a microscope—the P&P file is what makes automated PCB assembly affordable ($0.001/component vs hand-soldering).
