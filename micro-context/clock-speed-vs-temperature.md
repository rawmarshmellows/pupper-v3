---
term: Clock Speed vs Temperature
created: 2026-01-26
---

# Clock Speed vs Temperature

> **See also:** [[micro-context/clock-speed]] | [[micro-context/thermal-runaway]] | [[quick-context/transistor-analog-to-digital]] | [[quick-context/thermal-noise-electronics]]

**Definition:** Every clock edge causes transistors to switch, and switching dissipates energy as heat. Power scales with frequency (P ∝ f) and voltage squared (P ∝ V²), so higher clock speeds generate more heat—which is why CPUs need cooling and why "turbo boost" is temporary.

```
THE HEAT-SPEED RELATIONSHIP
════════════════════════════════════════════════════════════════

  Power = C × V² × f    (dynamic power)
          ↑   ↑    ↑
          │   │    └── frequency (clock speed)
          │   └─────── voltage squared (dominates!)
          └─────────── capacitance (fixed by chip design)

  Double clock speed → ~2× heat
  BUT: higher speed often needs higher voltage
       Double voltage → 4× heat!

  ┌─────────────────────────────────────────────────────────┐
  │  This is why chips throttle when hot—they reduce       │
  │  clock speed to stay within thermal limits.            │
  └─────────────────────────────────────────────────────────┘
```

**Key insight:** Clock speed and temperature are locked in a feedback loop—faster clocks make more heat, but heat increases [[quick-context/transistor-analog-to-digital|leakage current]] and [[quick-context/thermal-noise-electronics|thermal noise]], degrading performance until the chip must slow down or risk errors.
