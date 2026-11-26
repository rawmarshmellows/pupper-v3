---
term: CNC Turning
created: 2026-01-27
updated: 2026-03-27
---

# CNC Turning

> **See also:** [[learning/notes/quick-context/cnc-machining]] (full treatment) | [[learning/notes/micro-context/cnc-milling]]

**Definition:** A subtractive manufacturing process where a computer-controlled lathe spins the workpiece while a stationary cutting tool removes material. The inverse of milling—here the part rotates, not the tool. Used to create cylindrical or rotationally symmetric parts like shafts, bolts, and bushings.

## How It Works

- The workpiece is clamped in a rotating chuck that spins it at high speed (hundreds to thousands of RPM).
- A stationary cutting tool is fed into the spinning workpiece, shaving off material in a continuous spiral.
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

**Key insight:** Turning is inherently limited to parts with rotational symmetry (round cross-sections), but produces extremely smooth cylindrical surfaces and tight concentricity that milling struggles to match.
