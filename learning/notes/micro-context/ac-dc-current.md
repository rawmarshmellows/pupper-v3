---
term: AC vs DC Current
created: 2026-02-07
updated: 2026-03-27
---
> **Related:** [[learning/notes/quick-context/ac-to-dc-rectification]] | [[learning/notes/micro-context/current-inductor-capacitor-relationship]] | [[learning/notes/micro-context/buck-converter]] | [[learning/notes/micro-context/decoupling-capacitor]] | [[learning/notes/micro-context/diode-rectification]]


# AC vs DC Current

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** [[learning/notes/quick-context/ac-to-dc-rectification|DC (direct current)]] flows in one direction constantly—[[quick-context/galvanic-cells-batteries|batteries]] produce DC. [[learning/notes/quick-context/ac-to-dc-rectification|AC (alternating current)]] reverses direction periodically, typically 50-60 times per second—wall outlets provide AC. Most electronics need DC internally but the grid uses AC because it's easily transformed to different voltages.

## How It Works

- DC is produced by [[learning/notes/quick-context/electricity-generation|chemical reactions]] (batteries) or photovoltaic cells, pushing [[learning/notes/quick-context/anions-and-oxidation|electrons]] in a constant direction.
- AC is produced by rotating a coil in a magnetic field ([[learning/notes/quick-context/electricity-generation|generator]]), which naturally creates a sinusoidal alternating [[learning/notes/quick-context/voltage|voltage]].
- Transformers — which [[learning/notes/quick-context/comparator-specification|only]] work with AC — step voltage up for efficient long-[[learning/notes/quick-context/embedded-communication-protocols|distance]] transmission and down for safe household use.
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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** AC won the "war of currents" because [[quick-context/inductor|transformers]] (which only work with AC) allow stepping voltage up for efficient long-distance transmission, then down for safe household use—something DC couldn't do cheaply until modern power electronics.

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[quick-context/ac-to-dc-rectification|AC-to-DC Rectification (quick-context)]]
