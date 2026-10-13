---
term: Quiescent Supply Current (I_S)
created: 2026-06-07
---
> **Related:** [[learning/notes/micro-context/current-mirror]] | [[learning/notes/micro-context/input-bias-current]] | [[learning/notes/micro-context/power-supply-rejection-ratio]] | [[learning/notes/micro-context/tail-current]] | [[learning/notes/micro-context/common-mode-rejection-ratio]]


# Quiescent Supply Current ($I_S$)

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[quick-context/comparator-specification]] | [[micro-context/tail-current]] | [[quick-context/comparator]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** The standing [[learning/notes/quick-context/capacitance|current]] a [[learning/notes/quick-context/comparator|comparator]] or op-amp draws from its supply just to stay biased and ready, even [[learning/notes/quick-context/bare-minimal-data-storage-circuit|when]] its output isn't switching. For micropower parts it is microamps.

## How It Works

- Internal stages — the [[micro-context/tail-current|tail current source]], the mirror load, the output bias — burn a steady current to [[learning/notes/quick-context/existing-account-management-playbook|keep]] their transistors in the active region.
- This quiescent draw exists independent of the [[learning/notes/quick-context/comparator|signal]]: it's the [[learning/notes/quick-context/bond-pad|cost]] of being "on" and ready to respond instantly.
- Micropower parts ([[learning/notes/quick-context/comparator-specification|LMC7211-N]]: 7 µA typ) trade speed for tiny standing current, enabling battery and coin-cell operation for years.
- [[learning/notes/quick-context/similarity-transform|Total]] [[learning/notes/quick-context/comparator-specification|supply current]] climbs above $I_S$ [[learning/notes/quick-context/comparator-specification|only]] when the output actively drives a load.

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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|Quiescent current]] is the [[learning/notes/quick-context/3d-printing-filament-refill-vs-spool|price]] of always-on readiness — it's why a micropower comparator can watch a battery for years off the same cell it monitors, while a [[learning/notes/quick-context/comparator|fast]] comparator might [[learning/notes/quick-context/differential-pair|drain]] that cell in days.
