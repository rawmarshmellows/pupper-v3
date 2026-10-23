---
term: Pick and Place File
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/bjt-mosfet-igbt]] | [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]]

# Pick and Place File

> **See also:** [[quick-context/pcb-assembly-files-bom-cpl]] | [[quick-context/pcb-printed-circuit-board]] | [[quick-context/pupper-bom-control-board]]

**[[learning/notes/quick-context/capacitance|Definition]]:** A spreadsheet (CSV/Excel) exported from PCB design [[learning/notes/quick-context/code-to-gates-and-bootstrapping|software]] that tells automated assembly machines exactly where to place each [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|component]] on a [[quick-context/pcb-printed-circuit-board|PCB]]—including XY coordinates, [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|rotation]] angle, [[learning/notes/micro-context/push-pull-vs-open-drain|and]] which side of [[learning/notes/quick-context/capacitance|the]] board. Used by contract manufacturers (JLCPCB, PCBWay) to populate [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] bare PCB with [[learning/notes/quick-context/tensor|components]].

## How It Works

- PCB design software exports a spreadsheet listing every component's [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|reference designator]], XY position, rotation, and board side.
- The assembly house loads this file into the pick-and-place machine's software alongside the component reels.
- The machine's vacuum [[learning/notes/quick-context/3d-printer-hotends|nozzle]] picks each component from its feeder, rotates it to the correct angle, and places it on the [[learning/notes/quick-context/soldering|solder]]-pasted PCB [[learning/notes/quick-context/bga-ball-grid-array|pad]].
- After all components are placed, the board passes through a [[learning/notes/quick-context/bga-ball-grid-array|reflow]] oven to permanently solder them.

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

**Key insight:** Without this file, someone would have to manually place hundreds of tiny components under a microscope—the P&P file is [[learning/notes/quick-context/bare-minimal-data-storage-circuit|what]] makes automated PCB assembly affordable ($0.001/component vs hand-[[learning/notes/quick-context/soldering|soldering]]).
