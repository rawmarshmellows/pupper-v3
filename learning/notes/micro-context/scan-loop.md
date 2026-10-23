---
term: Scan Loop
created: 2026-04-07
---

> **Related:** [[learning/notes/micro-context/switch-matrix]] | [[learning/notes/micro-context/homogeneous-transformation-matrix]] | [[learning/notes/quick-context/keypress-to-pixel-pipeline]] | [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]]

# Scan Loop

**[[learning/notes/quick-context/capacitance|Definition]]:** A [[learning/notes/quick-context/firmware|firmware]] routine that rapidly cycles through rows of a **[[learning/notes/quick-context/switches-to-registers-storing-data|switch]] matrix** — a grid of electrical switches wired at [[learning/notes/quick-context/capacitance|the]] intersections of row [[learning/notes/micro-context/push-pull-vs-open-drain|and]] column lines, so each switch is uniquely identified by its (row, col) coordinate — driving each row LOW in turn and reading all columns to detect which switches are closed. Used by [[learning/notes/quick-context/data-bus-and-arbitration|keyboard]] and keypad [[learning/notes/micro-context/stm32-microcontroller|microcontrollers]] to monitor many switches with few [[learning/notes/quick-context/raspberry-pi-5-components|GPIO]] pins.

## How It Works

- The MCU configures row pins as outputs and column pins as inputs (with pull-up resistors so they default HIGH).
- Each iteration drives [[learning/notes/quick-context/ram-addressing-decoder|one]] row LOW while keeping all other rows HIGH, then reads every column pin — a LOW column means the switch at that (row, col) intersection is closed.
- The loop cycles through all rows every ~1–5 ms, [[learning/notes/quick-context/comparator|fast]] enough that no human keypress is missed.
- [[learning/notes/quick-context/bare-minimal-data-storage-circuit|When]] a press is detected, the firmware maps the (row, col) position to a [[learning/notes/quick-context/physics-of-writing-data-to-memory|scan code]] [[learning/notes/quick-context/metal-interconnect-layers|via]] a lookup table stored in flash.

```
GPIO PINS:    Row 0 ──┬────┬────┬──
              Row 1 ──┼────┼────┼──
              Row 2 ──┼────┼────┼──
                      │    │    │
                    Col 0 Col 1 Col 2

SCAN CYCLE (Row 0 active):
  Row 0 → LOW ─────────────────────
  Row 1 → HIGH ────────────────────
  Row 2 → HIGH ────────────────────

  Read columns:
    Col 0 = HIGH → open
    Col 1 = LOW  → KEY PRESSED at (0,1)
    Col 2 = HIGH → open

  Next iteration: Row 1 → LOW, repeat...
```

**Key insight:** An $N \times M$ matrix lets an MCU monitor $N \times M$ switches using [[learning/notes/quick-context/comparator-specification|only]] $N + M$ GPIO pins — a 6×14 keyboard matrix monitors 84 keys with just 20 pins.
