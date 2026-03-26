---
term: Reverse and Forward Bias
created: 2026-02-25
---

# Reverse and Forward Bias

**Definition:** The two ways to apply voltage across a [[quick-context/diode|PN junction]]. **Forward bias** (positive to P-side, negative to N-side) shrinks the [[quick-context/doped-silicon|depletion zone]] and lets current flow. **Reverse bias** (flipped polarity) widens the depletion zone and blocks current. This is what makes diodes one-way valves.

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

**Key insight:** The same PN junction does both jobs—forward bias is how diodes conduct, reverse bias is how they block, and every [[quick-context/transistor|transistor]] relies on biasing junctions in specific combinations to switch on and off.
