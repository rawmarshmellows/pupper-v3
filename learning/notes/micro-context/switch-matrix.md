---
term: Switch Matrix
created: 2026-04-07
---

# Switch Matrix

> **See also:** [[learning/notes/micro-context/scan-loop]] | [[learning/notes/micro-context/stm32-microcontroller]] | [[learning/notes/micro-context/sram]] | [[quick-context/keypress-to-pixel-pipeline]]

**Definition:** A grid of electrical switches wired at the intersections of row and column lines, allowing a [[learning/notes/micro-context/stm32-microcontroller|microcontroller]] to monitor $N \times M$ switches using only $N + M$ GPIO pins instead of one pin per switch.

## How It Works

- Each switch sits at a unique (row, col) intersection — pressing it electrically connects that row wire to that column wire.
- A [[learning/notes/micro-context/scan-loop|scan loop]] drives one row LOW at a time and reads all columns; a LOW column means that intersection's switch is closed.
- Without protection, pressing 3+ keys in an L-shape creates a "sneak path" that makes a fourth key appear pressed (**ghosting**) — adding a diode in series with each switch blocks reverse current and eliminates this.

```
        Col 0    Col 1    Col 2
          │        │        │
Row 0 ────┤────────┤────────┤
          ╳        ╳        ╳    ← switch at each
Row 1 ────┤────────┤────────┤      intersection
          ╳        ╳        ╳
Row 2 ────┤────────┤────────┤
          ╳        ╳        ╳

  3 rows + 3 cols = 6 pins → 9 switches
  (vs. 9 pins if wired individually)
```

**Key insight:** The matrix trick works because each switch is uniquely addressed by activating its row and reading its column — the same multiplexing principle used in [[learning/notes/micro-context/sram|SRAM]] and DRAM arrays, where wordlines and bitlines address individual memory cells.
