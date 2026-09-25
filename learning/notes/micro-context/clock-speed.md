---
term: Clock Speed
created: 2026-01-26
updated: 2026-03-27
---

# Clock Speed

> **Related:** [[micro-context/clock-speed-vs-temperature]] | [[micro-context/clock-edges]] | [[micro-context/clock-source]] | [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]]

**[[quick-context/capacitance|Definition]]:** The frequency at which a CPU's clock generates edges, measured in GHz (billions of cycles per second). A 3 GHz CPU produces 3 billion [[micro-context/clock-edges|clock edges]] per second—each edge triggers one step of computation.

## How It Works

- An oscillator circuit generates a continuous square wave at the rated frequency (e.g., 3 GHz = 3 billion toggles/sec).
- Each [[quick-context/bare-minimal-data-storage-circuit|rising edge]] triggers the CPU's pipeline to advance one step — fetch, decode, or execute an instruction.
- Faster clocks mean less time between edges, so signals must propagate [[micro-context/push-pull-vs-open-drain|and]] settle through all logic gates within a shrinking window.

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

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** Clock speed is limited by [[quick-context/electric-current|how fast]] transistors [[quick-context/embedded-communication-protocols|can]] switch AND how [[quick-context/comparator|fast]] signals can propagate—you can't clock faster than [[quick-context/mcp6541-as-lmc7211-replacement|your]] slowest circuit path can settle between edges.
