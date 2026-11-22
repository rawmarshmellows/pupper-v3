---
term: 4-Wire Kelvin Measurement
created: 2026-01-27
updated: 2026-03-27
---

# 4-Wire Kelvin Measurement

> **See also:** [[quick-context/electric-current]] | [[quick-context/parallel-vs-series-voltage]]

**Definition:** A precision resistance measurement technique using two separate wire pairs—one pair supplies current through the unknown resistance, while the other pair measures [[quick-context/voltage|voltage]] directly across it. This eliminates lead wire resistance from the measurement.

## How It Works

- Two "force" wires supply a known current through the unknown resistance from an external current source.
- Two separate "sense" wires connect directly across the resistance to a high-impedance voltmeter.
- Because the voltmeter draws negligible current, the sense wire resistance contributes essentially zero voltage drop.
- The unknown resistance is calculated as $R = V_{measured} / I_{known}$, free from lead wire error.

```
PROBLEM: 2-wire measurement includes lead resistance

    Meter ──────R_lead──────┬───[R_unknown]───┬──────R_lead────── Meter
                            │                 │
                      You measure R_lead + R_unknown + R_lead  ✗


SOLUTION: 4-wire Kelvin separates current and voltage paths

         CURRENT PATH (force)           SENSE PATH (measure)
              │                              │
    I───────────────────┬───[R_unknown]───┬───────────────────V
    source              │                 │               voltmeter
    I───────────────────┴─────────────────┴───────────────────V

    Voltmeter draws ~0 current → lead resistance doesn't matter
    R = V_measured / I_known                                   ✓
```

**Key insight:** The voltmeter's high input impedance means negligible current flows through the sense wires, so their resistance contributes essentially zero voltage drop to the measurement.
