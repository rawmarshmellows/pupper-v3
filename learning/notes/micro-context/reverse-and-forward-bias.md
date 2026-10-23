---
term: Reverse and Forward Bias
created: 2026-02-25
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/input-bias-current]] | [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]]

# Reverse and Forward Bias

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] ways to apply [[learning/notes/quick-context/voltage|voltage]] across a [[quick-context/diode|PN junction]]. **[[learning/notes/quick-context/ac-to-dc-rectification|Forward bias]]** (positive to P-side, negative to N-side) shrinks the [[quick-context/doped-silicon|depletion zone]] [[learning/notes/micro-context/push-pull-vs-open-drain|and]] lets [[learning/notes/quick-context/capacitance|current]] flow. **[[learning/notes/quick-context/ac-to-dc-rectification|Reverse bias]]** (flipped polarity) widens the depletion zone and blocks current. This is [[learning/notes/quick-context/bare-minimal-data-storage-circuit|what]] makes diodes [[learning/notes/quick-context/ram-addressing-decoder|one]]-way valves.

## How It Works

- At equilibrium, a depletion zone forms at the [[learning/notes/quick-context/diode|PN junction]] where mobile carriers have diffused away, creating a built-in [[learning/notes/quick-context/voltage-current-causality|electric field]] (~0.7V for [[learning/notes/quick-context/transistor|silicon]]).
- Forward bias applies positive voltage to the P-side, opposing the built-in field and shrinking the depletion zone until carriers flood across — current flows.
- Reverse bias applies positive voltage to the N-side, reinforcing the built-in field and widening the depletion zone — current is blocked.
- If reverse voltage exceeds the [[learning/notes/quick-context/diode|breakdown voltage]], the field accelerates carriers enough to ionize atoms (avalanche), and current flows destructively.

```
Forward bias:  current flows          Reverse bias:  current blocked

  (+)── P │░│ N ──(-)                 (-)── P │░░░░░░░░│ N ──(+)
         ←─→                                 ←────────→
       narrow                               widened
    depletion zone                       depletion zone

  Voltage pushes carriers               Voltage pulls carriers
  TOWARD junction → collapse            AWAY from junction → barrier grows
  → current flows (Vf ≈ 0.7V Si)       → no current (until breakdown)
```

**Key insight:** The same PN junction does [[learning/notes/quick-context/bjt-specifications|both]] jobs—forward bias is how diodes conduct, reverse bias is how they block, and every [[quick-context/transistor|transistor]] relies on biasing junctions in specific combinations to [[learning/notes/quick-context/switches-to-registers-storing-data|switch]] on and [[learning/notes/quick-context/bjt-specifications|off]].

> **See also:** [[quick-context/ac-to-dc-rectification|AC-to-DC Rectification (quick-context)]]
