---
term: Open-Loop Voltage Gain (A_V)
created: 2026-06-07
---
> **Related:** [[learning/notes/micro-context/current-mirror]] | [[learning/notes/micro-context/input-offset-voltage]] | [[learning/notes/micro-context/output-voltage-swing]] | [[learning/notes/quick-context/comparator]] | [[learning/notes/quick-context/differential-pair]]


# Open-Loop Voltage Gain ($A_V$)

> **See also:** [[quick-context/comparator-specification]] | [[quick-context/high-gain-amplifier-stage]] | [[quick-context/comparator]] | [[small-context/decibels-across-domains]]

**Definition:** The enormous gain a [[learning/notes/quick-context/comparator|comparator]] or op-amp applies to the tiny [[learning/notes/quick-context/voltage|voltage]] difference between its inputs before any feedback — typically 100 dB (100,000×) — which is what slams the output hard against a supply rail.

## How It Works

- The [[quick-context/differential-pair|differential pair]] turns an input difference into a small current imbalance.
- That imbalance drives a very high-impedance [[quick-context/high-gain-amplifier-stage|gain node]] (the current-mirror load), so even microamps create a huge voltage swing.
- 100 dB = 100,000×, so a millivolt of input difference would demand a 100 V output — far past the rails — so the output simply pins to $V^+$ or $V^-$.
- This rail-slamming saturation *is* the clean digital snap a comparator is built to produce.

```
   tiny dV in                        output pinned to rail

   V(+)-V(-) = 1 mV --> [ A_V = 100 dB ] --> "wants" 100 V
                          (x 100,000)          |
                                               v
   --- V+ -----------------------------  output slams up to V+
                                          (can't exceed rail)
   --- V- -----------------------------

   Any input difference past a few uV drives the output
   fully to a rail -> the digital decision.
```

**Key insight:** It's the "gain" you never use *as* gain — it's so large the output can't stay linear, which is exactly the point: a comparator wants to saturate to a rail, not amplify proportionally.
