---
term: PCB vs PLC Relationship
created: 2026-01-26
---

# PCB vs PLC Relationship

> **See also:** [[quick-context/pcb-printed-circuit-board]] | [[quick-context/pcb-chip-transistor-hierarchy]]

**Definition:** A PCB (Printed Circuit Board) is a physical substrate with copper traces that connects electronic components, while a PLC (Programmable Logic Controller) is an industrial computer built to control machinery. PLCs *contain* PCBs as their internal wiring, but serve completely different purposes: PCB is a manufacturing technology; PLC is a computing device.

```
PCB = Physical Structure          PLC = Industrial Controller
(how components connect)          (what controls machines)

    ┌─────────────────┐              ┌───────────────────┐
    │  ═══════════    │              │  ┌─────────────┐  │
    │  □  □  ═══  □   │    ◄────     │  │   CPU on    │  │
    │    ▓▓▓      ○○  │   inside     │  │    PCB      │  │
    │  ═══════════════│              │  └─────────────┘  │
    └─────────────────┘              │  I/O  I/O  I/O    │
         copper traces               └───────────────────┘
         on fiberglass                  sensors & motors

    Your phone has PCBs.            Factories use PLCs.
    PLCs have PCBs inside.          PLCs don't replace PCBs.
```

**Key insight:** Asking "PCB vs PLC" is like asking "metal vs car"—one is a material/technology used to build things, the other is a complete functional device that happens to contain that material.
