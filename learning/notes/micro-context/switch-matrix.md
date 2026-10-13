---
term: Switch Matrix
created: 2026-04-07
---
> **Related:** [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/capacitive-voltage-sensing]] | [[learning/notes/micro-context/piezoelectric-effect]] | [[learning/notes/quick-context/camera-fundamentals]]


# Switch Matrix

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** A grid of electrical switches wired at the intersections of row and column lines, allowing a [[learning/notes/micro-context/stm32-microcontroller|microcontroller]] to monitor $N \times M$ switches using [[learning/notes/quick-context/comparator-specification|only]] $N + M$ [[learning/notes/quick-context/raspberry-pi-5-components|GPIO]] pins instead of one pin per [[learning/notes/quick-context/switches-to-registers-storing-data|switch]].

## How It Works

- Each switch sits at a unique (row, col) intersection — pressing it electrically connects that row wire to that column wire.
- A [[learning/notes/micro-context/scan-loop|scan loop]] drives one row LOW at a time and reads all columns; a LOW column means that intersection's switch is closed.
- Without protection, pressing 3+ keys in an L-shape creates a "sneak path" that makes a fourth key appear pressed (**ghosting**) — adding a [[learning/notes/quick-context/diode|diode]] in [[learning/notes/quick-context/parallel-vs-series-voltage|series]] with each switch blocks reverse [[learning/notes/quick-context/capacitance|current]] and eliminates this.

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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** The matrix trick works because each switch is uniquely addressed by activating its row and reading its column — the same multiplexing principle used in [[learning/notes/micro-context/sram|SRAM]] and [[learning/notes/quick-context/ram-addressing-decoder|DRAM]] arrays, where wordlines and bitlines [[learning/notes/quick-context/how-source-code-is-stored|address]] individual [[learning/notes/quick-context/bare-minimal-data-storage-circuit|memory]] cells.
