---
term: AC vs DC Current
created: 2026-02-07
updated: 2026-03-27
---

> **Related:** [[learning/notes/quick-context/ac-to-dc-rectification]] | [[learning/notes/micro-context/current-electrons-per-second]] | [[learning/notes/micro-context/current-inductor-capacitor-relationship]] | [[learning/notes/micro-context/current-mirror]] | [[learning/notes/micro-context/input-bias-current]]

# AC vs DC Current[[learning/notes/quick-context/tensile-strength-materials|]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/micro-context/mosfet|DC]] (direct [[learning/notes/quick-context/capacitance|current]]) flows in [[learning/notes/quick-context/ram-addressing-decoder|one]] direction constantly—[[quick-context/galvanic-cells-batteries|batteries]] produce DC. AC (alternating current) reverses direction periodically, typically 50-60 times per second—wall outlets provide AC. Most electronics need DC internally but [[learning/notes/quick-context/capacitance|the]] grid uses AC because it's easily transformed to different voltages.

## How It Works

- DC is produced by [[learning/notes/quick-context/electricity-generation|chemical reactions]] (batteries) [[learning/notes/micro-context/push-pull-vs-open-drain|or]] photovoltaic cells, pushing [[learning/notes/quick-context/anions-and-oxidation|electrons]] in [[learning/notes/quick-context/anions-and-oxidation|a]] constant direction.
- AC is produced by rotating a coil in a magnetic field ([[learning/notes/quick-context/electricity-generation|generator]]), which naturally creates a sinusoidal alternating [[learning/notes/quick-context/voltage|voltage]].
- Transformers — which [[learning/notes/quick-context/comparator-specification|only]] work [[learning/notes/quick-context/breaking-elongation-rate|with]] AC — step voltage up for efficient long-[[learning/notes/quick-context/embedded-communication-protocols|distance]] transmission [[learning/notes/micro-context/push-pull-vs-open-drain|and]] down for safe household use.
- Electronics internally convert AC to DC using rectifier diodes and filter [[learning/notes/quick-context/voltage|capacitors]] (the [[learning/notes/quick-context/d-flip-flop|power]] supply).

```
DC (Direct Current)            AC (Alternating Current)

  I ▲                            I ▲  /\      /\
    │ ─────────────────          + │ /  \    /  \
    │  constant direction        0─┼/────\──/────\──► t
    └──────────────────► t       - │      \/      \/
                                   │
  Batteries, solar panels,       Power grid, transformers,
  USB ports, electronics         motors, generators
```

**Key insight:** AC won the "war of currents" because [[quick-context/inductor|transformers]] (which only work with AC) allow stepping voltage up for efficient long-distance transmission, then down for safe household use—something DC couldn't do cheaply until modern power electronics.

> **See also:** [[quick-context/ac-to-dc-rectification|AC-to-DC Rectification (quick-context)]]
