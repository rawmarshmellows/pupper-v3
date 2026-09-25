---
term: Schmitt Trigger & Hysteresis
created: 2026-06-07
---

# Schmitt Trigger & Hysteresis

> **Related:** [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]] | [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/ads1110-battery-adc]] | [[micro-context/bjt-mosfet-igbt]]

**[[quick-context/capacitance|Definition]]:** A [[learning/notes/quick-context/comparator|comparator]]-[[quick-context/bjt-specifications|type]] circuit with **two** switching thresholds instead of one. **Hysteresis** is the deliberate [[quick-context/voltage|voltage]] gap between them: the output flips HIGH [[quick-context/comparator-specification|only]] when the input rises above the upper [[micro-context/capacitive-voltage-sensing|threshold]] $V_{T+}$, [[micro-context/push-pull-vs-open-drain|and]] flips LOW only when it falls below the lower threshold $V_{T-}$.

## How It Works

- Instead of one trip point, there are two — an upper $V_{T+}$ and a lower $V_{T-}$; the gap between them is the hysteresis.
- A rising input must climb past $V_{T+}$ to switch the output HIGH; a falling input must drop below $V_{T-}$ to switch it LOW.
- While the input sits *between* the two thresholds, the output holds its last state — this "[[quick-context/bare-minimal-data-storage-circuit|memory]]" makes it immune to small noise wiggles.
- Positive feedback (the output fed back to the input) shifts which threshold is active after each switch, which is what physically creates the gap.

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

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** A single-threshold [[quick-context/comparator|comparator]] *chatters* — toggling many times — when a slow or noisy input lingers near the trip point; the hysteresis band swallows the noise so the output switches once, cleanly.
