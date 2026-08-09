---
term: Schmitt Trigger & Hysteresis
created: 2026-06-07
---
> **Related:** [[learning/notes/quick-context/comparator]] | [[learning/notes/quick-context/voltage]]


# Schmitt Trigger & Hysteresis

> **See also:** [[learning/notes/quick-context/comparator]] | [[learning/notes/quick-context/comparator-specification]]

**Definition:** A [[learning/notes/quick-context/comparator|comparator]]-type circuit with **two** switching thresholds instead of one. **Hysteresis** is the deliberate [[learning/notes/quick-context/voltage|voltage]] gap between them: the output flips HIGH only when the input rises above the upper threshold $V_{T+}$, and flips LOW only when it falls below the lower threshold $V_{T-}$.

## How It Works

- Instead of one trip point, there are two — an upper $V_{T+}$ and a lower $V_{T-}$; the gap between them is the hysteresis.
- A rising input must climb past $V_{T+}$ to switch the output HIGH; a falling input must drop below $V_{T-}$ to switch it LOW.
- While the input sits *between* the two thresholds, the output holds its last state — this "memory" makes it immune to small noise wiggles.
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

**Key insight:** A single-threshold [[learning/notes/quick-context/comparator|comparator]] *chatters* — toggling many times — when a slow or noisy input lingers near the trip point; the hysteresis band swallows the noise so the output switches once, cleanly.
