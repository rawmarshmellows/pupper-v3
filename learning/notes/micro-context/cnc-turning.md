---
term: CNC Turning
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/cnc-milling]] | [[learning/notes/micro-context/cnc-process-selection]] | [[learning/notes/quick-context/cnc-machining]]

# CNC Turning[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[quick-context/cnc-machining]] ([[learning/notes/quick-context/singular-value-decomposition|full]] treatment) | [[micro-context/cnc-milling]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] subtractive manufacturing process where a computer-controlled lathe spins [[learning/notes/quick-context/capacitance|the]] workpiece while a stationary cutting [[learning/notes/quick-context/epson-rc-plus-programming|tool]] removes material. The inverse of milling—here the part rotates, [[learning/notes/micro-context/can-bus-termination|not]] the tool. Used to create cylindrical [[learning/notes/micro-context/push-pull-vs-open-drain|or]] rotationally [[learning/notes/quick-context/singular-value-decomposition|symmetric]] parts like shafts, bolts, [[learning/notes/micro-context/push-pull-vs-open-drain|and]] bushings.

## How It Works

- The workpiece is clamped in a rotating chuck that spins it at high [[learning/notes/quick-context/embedded-communication-protocols|speed]] (hundreds to thousands of RPM).
- A stationary cutting tool is fed into the spinning workpiece, shaving [[learning/notes/quick-context/bjt-specifications|off]] material in a continuous spiral.
- The CNC controller moves the tool along and into the workpiece axis to produce the programmed cylindrical profile.

```
MILLING vs TURNING:

  MILLING                      TURNING (Lathe)
  ───────                      ───────────────
  Tool rotates                 Workpiece rotates
  Part stays still             Tool stays still

       ║                            ┌───────────┐
      ╔╩╗ ← Spinning               ◄│███████████│► Chuck grips
      ║░║   cutter                  │███████████│   and spins
      ╚═╝                           │███████████│   workpiece
  ─────────── Part                  └───────────┘
                                         ▲
                                    ═════╪═════ Tool carriage
                                         │       (moves along axis)
```

**Key insight:** Turning is inherently limited to parts [[learning/notes/quick-context/breaking-elongation-rate|with]] rotational symmetry (round cross-sections), but produces extremely smooth cylindrical surfaces and tight concentricity that milling struggles to match.
