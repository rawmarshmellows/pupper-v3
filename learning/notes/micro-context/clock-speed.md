---
term: Clock Speed
created: 2026-01-26
updated: 2026-03-27
---

> **Related:** [[micro-context/clock-edges]] | [[quick-context/clock-sources-and-timing]] | [[micro-context/clock-source]] | [[quick-context/transistor]] | [[micro-context/clock-speed-vs-temperature]]

# Clock Speed

> **See also:** [[micro-context/clock-edges]] | [[micro-context/clock-speed-vs-temperature]] | [[quick-context/transistor-analog-to-digital]] | [[quick-context/clock-sources-and-timing|Clock Sources and Timing]]

**Definition:** The frequency at which a CPU's clock generates edges, measured in GHz (billions of cycles per second). A 3 GHz CPU produces 3 billion [[micro-context/clock-edges|clock edges]] per second—each edge triggers one step of computation.

## How It Works

- An oscillator circuit generates a continuous square wave at the rated frequency (e.g., 3 GHz = 3 billion toggles/sec).
- Each rising edge triggers the CPU's pipeline to advance one step — fetch, decode, or execute an instruction.
- Faster clocks mean less time between edges, so signals must propagate and settle through all logic gates within a shrinking window.

```
CLOCK SPEED = How many edges per second
════════════════════════════════════════════════════════════════

  1 GHz clock:  1 billion edges/sec  →  1 ns between edges
  3 GHz clock:  3 billion edges/sec  →  0.33 ns between edges
  5 GHz clock:  5 billion edges/sec  →  0.2 ns between edges

  ┌─────────────────────────────────────────────────────────┐
  │  Higher clock speed = more edges = more operations/sec  │
  │  BUT signals must settle before next edge arrives!      │
  └─────────────────────────────────────────────────────────┘

  At 5 GHz, signals have only 0.2 nanoseconds to settle.
  Light travels just 6 cm in that time.
```

**Key insight:** Clock speed is limited by how fast [[quick-context/transistor|transistors]] can switch AND how fast signals can propagate—you can't clock faster than your slowest circuit path can settle between edges.
