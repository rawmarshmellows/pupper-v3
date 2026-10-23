---
term: Open-Loop Voltage Gain (A_V)
created: 2026-06-07
---

> **Related:** [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/buck-converter]] | [[learning/notes/micro-context/capacitive-voltage-sensing]] | [[learning/notes/micro-context/input-offset-voltage]] | [[learning/notes/micro-context/offset-voltage-drift]]

# Open-Loop Voltage Gain ($A_V$)

> **See also:** [[quick-context/comparator-specification]] | [[quick-context/high-gain-amplifier-stage]] | [[quick-context/comparator]] | decibels-across-domains

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] enormous gain a [[learning/notes/quick-context/comparator|comparator]] or op-amp applies to the tiny [[learning/notes/quick-context/voltage|voltage]] difference between its inputs before any feedback — typically 100 dB (100,000×) — which is [[learning/notes/quick-context/bare-minimal-data-storage-circuit|what]] slams the output hard against a supply rail.

## How It Works

- The [[quick-context/differential-pair|differential pair]] turns an input difference into a small [[learning/notes/quick-context/capacitance|current]] imbalance.
- That imbalance drives a very high-impedance [[quick-context/high-gain-amplifier-stage|gain node]] (the current-mirror load), so even microamps create a huge voltage swing.
- 100 dB = 100,000×, so a millivolt of input difference would demand a 100 V output — far past the rails — so the output simply pins to $V^+$ or $V^-$.
- This rail-slamming [[learning/notes/quick-context/bjt|saturation]] *is* the clean digital snap a comparator is built to produce.

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

**Key insight:** It's the "gain" you never use *as* gain — it's so large the output [[learning/notes/quick-context/embedded-communication-protocols|can]]'t stay linear, which is exactly the [[learning/notes/quick-context/epson-rc-plus-programming|point]]: a comparator wants to saturate to a rail, [[learning/notes/micro-context/can-bus-termination|not]] amplify proportionally.
