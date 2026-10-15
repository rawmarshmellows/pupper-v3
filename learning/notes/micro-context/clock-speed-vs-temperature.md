---
term: Clock Speed vs Temperature
created: 2026-01-26
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/clock-speed]] | [[learning/notes/micro-context/clock-edges]] | [[learning/notes/micro-context/clock-source]] | [[learning/notes/quick-context/clock-sources-and-timing]] | [[learning/notes/quick-context/glass-transition-temperature]]

# Clock Speed vs Temperature[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[micro-context/clock-speed]] | [[micro-context/thermal-runaway]] | [[quick-context/transistor-analog-to-digital]] | [[quick-context/thermal-noise-electronics]] | [[quick-context/clock-sources-and-timing|Clock Sources and Timing]]

**[[learning/notes/quick-context/capacitance|Definition]]:** Every [[learning/notes/micro-context/clock-edges|clock edge]] causes transistors to [[learning/notes/quick-context/switches-to-registers-storing-data|switch]], [[learning/notes/micro-context/push-pull-vs-open-drain|and]] switching dissipates energy as heat. [[learning/notes/quick-context/d-flip-flop|Power]] scales [[learning/notes/quick-context/breaking-elongation-rate|with]] frequency (P ∝ f) and [[learning/notes/quick-context/voltage|voltage]] squared (P ∝ V²), so higher [[learning/notes/quick-context/bare-minimal-data-storage-circuit|clock]] speeds generate more heat—which is [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] CPUs need cooling and why "turbo boost" is temporary.

## How It Works

- Every [[learning/notes/micro-context/clock-edges|clock edge]] causes transistors to [[learning/notes/quick-context/cations-and-reduction|charge]] and discharge [[learning/notes/quick-context/transistor|gate]] capacitances, converting electrical energy into heat ($P = CV^2f$).
- Higher clock speeds require more switching events per second, linearly increasing dynamic [[learning/notes/quick-context/resistor|power dissipation]].
- Pushing clocks higher often demands raising supply voltage too, which increases power quadratically ($[[learning/notes/quick-context/capacitor|V]]^[[learning/notes/quick-context/meddpicc-qualification-framework|2]]$).
- [[learning/notes/quick-context/bare-minimal-data-storage-circuit|When]] junction temperature rises too high, [[learning/notes/quick-context/firmware|firmware]] thermal throttling reduces [[learning/notes/micro-context/clock-speed|clock speed]] to bring power back under [[learning/notes/quick-context/capacitance|the]] cooling budget.

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

**Key insight:** Clock [[learning/notes/quick-context/embedded-communication-protocols|speed]] and temperature are locked in [[learning/notes/quick-context/anions-and-oxidation|a]] feedback loop—faster clocks make more heat, but heat increases [[quick-context/transistor-analog-to-digital|leakage current]] and [[quick-context/thermal-noise-electronics|thermal noise]], degrading [[learning/notes/quick-context/bond-pad|performance]] until the chip [[learning/notes/quick-context/ros2-architecture|must]] slow down [[learning/notes/micro-context/push-pull-vs-open-drain|or]] risk errors.
