---
term: AC vs DC Current
created: 2026-02-07
---

# AC vs DC Current

**Definition:** DC (direct current) flows in one direction constantly—[[quick-context/galvanic-cells-batteries|batteries]] produce DC. AC (alternating current) reverses direction periodically, typically 50-60 times per second—wall outlets provide AC. Most electronics need DC internally but the grid uses AC because it's easily transformed to different voltages.

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
