---
term: AC vs DC Current
created: 2026-02-07
updated: 2026-03-27
---
> **Related:** [[micro-context/current-electrons-per-second]] | [[micro-context/current-inductor-capacitor-relationship]] | [[micro-context/current-mirror]] | [[micro-context/input-bias-current]] | [[micro-context/quiescent-supply-current]]


# AC vs DC Current

**Definition:** DC (direct current) flows in one direction constantly—[[quick-context/galvanic-cells-batteries|batteries]] produce DC. AC (alternating current) reverses direction periodically, typically 50-60 times per second—wall outlets provide AC. Most electronics need DC internally but the grid uses AC because it's easily transformed to different voltages.

## How It Works

- DC is produced by chemical reactions (batteries) or photovoltaic cells, pushing electrons in a constant direction.
- AC is produced by rotating a coil in a magnetic field (generator), which naturally creates a sinusoidal alternating [[quick-context/voltage|voltage]].
- Transformers — which only work with AC — step [[quick-context/voltage|voltage]] up for efficient long-distance transmission and down for safe household use.
- Electronics internally convert AC to DC using rectifier diodes and filter capacitors (the power supply).

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
