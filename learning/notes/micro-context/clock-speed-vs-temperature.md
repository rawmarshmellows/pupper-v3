---
term: Clock Speed vs Temperature
created: 2026-01-26
updated: 2026-03-27
---

# Clock Speed vs Temperature

> **Related:** [[micro-context/clock-speed]] | [[micro-context/clock-edges]] | [[micro-context/clock-source]] | [[micro-context/push-pull-vs-open-drain]] | [[micro-context/4-wire-kelvin-measurement]]

**[[quick-context/capacitance|Definition]]:** Every [[micro-context/clock-edges|clock edge]] causes transistors to switch, [[micro-context/push-pull-vs-open-drain|and]] switching dissipates energy as heat. Power scales with frequency (P ∝ f) and [[quick-context/voltage|voltage]] squared (P ∝ V²), so higher clock speeds generate more heat—which is why CPUs need cooling and why "turbo boost" is temporary.

## How It Works

- Every clock edge causes transistors to charge and discharge [[quick-context/transistor|gate]] capacitances, converting electrical energy into heat ($P = CV^2f$).
- Higher clock speeds require more switching events per second, linearly increasing dynamic [[quick-context/resistor|power dissipation]].
- Pushing clocks higher often demands raising supply voltage too, which increases power quadratically ($V^2$).
- [[quick-context/bare-minimal-data-storage-circuit|When]] junction temperature rises too high, firmware thermal throttling reduces clock speed to bring power back under the cooling budget.

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

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** Clock speed and temperature are locked in a feedback loop—faster clocks make more heat, but heat increases [[quick-context/transistor-analog-to-digital|leakage current]] and [[quick-context/thermal-noise-electronics|thermal noise]], degrading performance until the chip must slow down or risk errors.
