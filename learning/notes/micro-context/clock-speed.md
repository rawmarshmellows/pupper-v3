---
term: Clock Speed
created: 2026-01-26
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/clock-speed-vs-temperature]] | [[learning/notes/micro-context/clock-edges]] | [[learning/notes/micro-context/clock-source]] | [[learning/notes/micro-context/push-pull-vs-open-drain]] | [[learning/notes/micro-context/4-wire-kelvin-measurement]]

# Clock Speed

> **See also:** [[micro-context/clock-edges]] | [[micro-context/clock-speed-vs-temperature]] | [[quick-context/transistor-analog-to-digital]] | [[quick-context/clock-sources-and-timing|Clock Sources and Timing]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] frequency at which a CPU's [[learning/notes/quick-context/bare-minimal-data-storage-circuit|clock]] generates edges, measured in GHz (billions of cycles per second). A 3 GHz CPU produces 3 billion [[micro-context/clock-edges|clock edges]] per second—each edge triggers [[learning/notes/quick-context/ram-addressing-decoder|one]] step of computation.

## How It Works

- An oscillator circuit generates a continuous square wave at the rated frequency (e.g., 3 GHz = 3 billion toggles/sec).
- Each [[learning/notes/quick-context/bare-minimal-data-storage-circuit|rising edge]] triggers the CPU's pipeline to advance one step — [[learning/notes/quick-context/cpu-fetch-execute-cycle|fetch]], [[learning/notes/quick-context/cpu-fetch-execute-cycle|decode]], or execute an [[learning/notes/quick-context/cpu-fetch-execute-cycle|instruction]].
- Faster clocks mean less time between edges, so signals [[learning/notes/quick-context/ros2-architecture|must]] propagate and settle through all logic gates within a shrinking window.

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

**Key insight:** Clock [[learning/notes/quick-context/embedded-communication-protocols|speed]] is limited by [[learning/notes/quick-context/electric-current|how fast]] transistors [[learning/notes/quick-context/embedded-communication-protocols|can]] [[learning/notes/quick-context/switches-to-registers-storing-data|switch]] AND how [[learning/notes/quick-context/comparator|fast]] signals can propagate—you can't clock faster than [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] slowest circuit path can settle between edges.
