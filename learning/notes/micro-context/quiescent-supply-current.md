---
term: Quiescent Supply Current (I_S)
created: 2026-06-07
---

# Quiescent Supply Current ($I_S$)

> **See also:** [[quick-context/comparator-specification]] | [[micro-context/tail-current]] | [[quick-context/comparator]]

**Definition:** The standing current a [[quick-context/comparator|comparator]] or op-amp draws from its supply just to stay biased and ready, even when its output isn't switching. For micropower parts it is microamps.

## How It Works

- Internal stages — the [[micro-context/tail-current|tail current source]], the mirror load, the output bias — burn a steady current to keep their transistors in the active region.
- This quiescent draw exists independent of the signal: it's the cost of being "on" and ready to respond instantly.
- Micropower parts (LMC7211-N: 7 µA typ) trade speed for tiny standing current, enabling battery and coin-cell operation for years.
- Total supply current climbs above $I_S$ only when the output actively drives a load.

```
   coin cell
   +---+        I_S (e.g. 7 uA, always flowing)
   | + |----------------+
   |3V |                v
   | - |        +---------------+
   +---+        |   comparator   |---> out
     ^          | (biased, idle) |
     +----------+---------------+
   Draws I_S just to stay ready, even with no switching.
   7 uA -> years off a single coin cell.
```

**Key insight:** Quiescent current is the price of always-on readiness — it's why a micropower comparator can watch a battery for years off the same cell it monitors, while a fast comparator might drain that cell in days.
