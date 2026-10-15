---
term: Schmitt Trigger & Hysteresis
created: 2026-06-07
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# Schmitt Trigger & Hysteresis[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[learning/notes/quick-context/comparator]] | [[learning/notes/quick-context/comparator-specification]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] [[learning/notes/quick-context/comparator|comparator]]-[[learning/notes/quick-context/bjt-specifications|type]] circuit [[learning/notes/quick-context/breaking-elongation-rate|with]] **two** switching thresholds instead of [[learning/notes/quick-context/ram-addressing-decoder|one]]. **[[learning/notes/quick-context/comparator-specification|Hysteresis]]** is [[learning/notes/quick-context/capacitance|the]] deliberate [[learning/notes/quick-context/voltage|voltage]] gap between them: the output flips HIGH [[learning/notes/quick-context/comparator-specification|only]] [[learning/notes/quick-context/bare-minimal-data-storage-circuit|when]] the input rises above the upper [[learning/notes/micro-context/capacitive-voltage-sensing|threshold]] $V_{T+}$, [[learning/notes/micro-context/push-pull-vs-open-drain|and]] flips LOW only when it falls below the lower threshold $V_{T-}$.

## How It Works

- Instead of one trip [[learning/notes/quick-context/epson-rc-plus-programming|point]], there are two — an upper $V_{T+}$ and a lower $V_{T-}$; the gap between them is the hysteresis.
- A rising input [[learning/notes/quick-context/ros2-architecture|must]] climb past $V_{T+}$ to [[learning/notes/quick-context/switches-to-registers-storing-data|switch]] the output HIGH; a falling input must drop below $V_{T-}$ to switch it LOW.
- While the input sits *between* the two thresholds, the output [[learning/notes/quick-context/pupper-lab7-vision-tracking|holds]] its last state — this "[[learning/notes/quick-context/bare-minimal-data-storage-circuit|memory]]" makes it immune to small noise wiggles.
- [[learning/notes/quick-context/pupper-lab7-vision-tracking|Positive feedback]] (the output fed back to the input) shifts which threshold is active after each switch, which is [[learning/notes/quick-context/bare-minimal-data-storage-circuit|what]] physically creates the gap.

```
  Vout
 HIGH ┤        ┌─────┬─────►
      │        │     │        rising:  Vin > V_T+ → flips HIGH
      │        │     │        falling: Vin < V_T- → flips LOW
  LOW ┤────────┴─────┘
      └────────┬─────┬─────► Vin
             V_T-  V_T+
                └─────┘
             hysteresis band
```

**Key insight:** A single-threshold [[learning/notes/quick-context/comparator|comparator]] *chatters* — toggling many times — when a slow [[learning/notes/micro-context/push-pull-vs-open-drain|or]] noisy input lingers near the trip point; the hysteresis band swallows the noise so the output switches once, cleanly.
