---
term: Reverse and Forward Bias
created: 2026-02-25
updated: 2026-03-27
---

> **Related:** [[learning/notes/quick-context/differential-pair]] | [[learning/notes/quick-context/diode]] | [[learning/notes/quick-context/doped-silicon]] | [[learning/notes/quick-context/pcb-chip-transistor-hierarchy]]

# Reverse and Forward Bias

**Definition:** The two ways to apply [[learning/notes/quick-context/voltage|voltage]] across a [[quick-context/diode|PN junction]]. **Forward bias** (positive to P-side, negative to N-side) shrinks the [[quick-context/doped-silicon|depletion zone]] and lets current flow. **Reverse bias** (flipped polarity) widens the depletion zone and blocks current. This is what makes diodes one-way valves.

## How It Works

- At equilibrium, a depletion zone forms at the PN junction where mobile carriers have diffused away, creating a built-in electric field (~0.7V for silicon).
- Forward bias applies positive voltage to the P-side, opposing the built-in field and shrinking the depletion zone until carriers flood across — current flows.
- Reverse bias applies positive voltage to the N-side, reinforcing the built-in field and widening the depletion zone — current is blocked.
- If reverse voltage exceeds the breakdown voltage, the field accelerates carriers enough to ionize atoms (avalanche), and current flows destructively.

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

> **See also:** [[quick-context/ac-to-dc-rectification|AC-to-DC Rectification (quick-context)]]
