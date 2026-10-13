---
term: Clock Speed vs Temperature
created: 2026-01-26
updated: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/clock-speed]] | [[learning/notes/micro-context/clock-edges]] | [[learning/notes/micro-context/clock-source]] | [[learning/notes/quick-context/clock-sources-and-timing]] | [[learning/notes/micro-context/ceramic-resonator]]


# Clock Speed vs Temperature

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[micro-context/clock-speed]] | [[micro-context/thermal-runaway]] | [[quick-context/transistor-analog-to-digital]] | [[quick-context/thermal-noise-electronics]] | [[quick-context/clock-sources-and-timing|Clock Sources and Timing]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** Every [[learning/notes/micro-context/clock-edges|clock edge]] causes transistors to [[learning/notes/quick-context/switches-to-registers-storing-data|switch]], and switching dissipates energy as heat. [[learning/notes/quick-context/d-flip-flop|Power]] scales with frequency (P ∝ f) and [[learning/notes/quick-context/voltage|voltage]] squared (P ∝ V²), so higher clock speeds generate more heat—which is why CPUs need cooling and why "turbo boost" is temporary.

## How It Works

- Every clock edge causes transistors to [[learning/notes/quick-context/cations-and-reduction|charge]] and discharge [[learning/notes/quick-context/transistor|gate]] capacitances, converting electrical energy into heat ($P = CV^2f$).
- Higher clock speeds require more switching events per second, linearly increasing dynamic [[learning/notes/quick-context/resistor|power dissipation]].
- Pushing clocks higher often demands raising supply voltage too, which increases power quadratically ($V^2$).
- [[learning/notes/quick-context/bare-minimal-data-storage-circuit|When]] junction temperature rises too high, [[learning/notes/quick-context/firmware|firmware]] thermal throttling reduces [[learning/notes/micro-context/clock-speed|clock speed]] to bring power back under the cooling budget.

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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** Clock speed and temperature are locked in a feedback loop—faster clocks make more heat, but heat increases [[quick-context/transistor-analog-to-digital|leakage current]] and [[quick-context/thermal-noise-electronics|thermal noise]], degrading [[learning/notes/quick-context/bond-pad|performance]] until the chip [[learning/notes/quick-context/ros2-architecture|must]] slow down or risk errors.
