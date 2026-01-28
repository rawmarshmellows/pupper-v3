---
term: PLC vs CPU
created: 2026-01-26
---

# PLC vs CPU

> **See also:** [[quick-context/transistor]] | [[quick-context/pcb-chip-transistor-hierarchy]] | [[micro-context/pcb-plc-relationship]]

**Definition:** A CPU (Central Processing Unit) is a general-purpose chip that executes software instructions. A PLC (Programmable Logic Controller) is a ruggedized industrial computer—containing a CPU inside—designed specifically to control factory machinery with real-time reliability and I/O for sensors/actuators.

```
CPU = A chip                    PLC = A complete industrial computer
(the brain)                     (has a CPU inside + everything else)

   ┌─────────┐                     ┌─────────────────────────┐
   │ ░░░░░░░ │                     │  ┌───┐                  │
   │ ░ CPU ░ │   ◄── inside ──     │  │CPU│  Power  Comms    │
   │ ░░░░░░░ │                     │  └───┘  Supply Module   │
   └─────────┘                     │                         │
    ~10-50mm                       │  IN: ● ● ● ● ● ● ● ●    │
    silicon die                    │  OUT: ○ ○ ○ ○ ○ ○ ○ ○   │
                                   └─────────────────────────┘
                                    Sensors    Motors/Valves

   In laptops, phones,             In factories, controlling
   servers, everything             conveyor belts, robots
```

**Key insight:** Comparing PLC to CPU is like comparing "car" to "engine"—one contains the other. PLCs are specialized computers; CPUs are components inside all computers.
