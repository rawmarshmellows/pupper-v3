---
term: Output Voltage Swing (V_OH / V_OL)
created: 2026-06-07
---

> **Related:** [[learning/notes/micro-context/capacitive-voltage-sensing]] | [[learning/notes/micro-context/input-offset-voltage]] | [[learning/notes/micro-context/offset-voltage-drift]] | [[learning/notes/micro-context/open-loop-voltage-gain]] | [[learning/notes/quick-context/parallel-vs-series-voltage]]

# Output Voltage Swing ($V_{OH}$ / $V_{OL}$)

> **[[learning/notes/quick-context/tensile-strength-materials|]]See also:** [[quick-context/comparator-specification]] | [[micro-context/push-pull-vs-open-drain]] | [[quick-context/comparator]]

**[[learning/notes/quick-context/capacitance|Definition]]:** How close [[learning/notes/quick-context/anions-and-oxidation|a]] [[learning/notes/quick-context/comparator|comparator]]'s [[learning/notes/micro-context/push-pull-vs-open-drain|or]] op-amp's output [[learning/notes/quick-context/embedded-communication-protocols|can]] drive to [[learning/notes/quick-context/capacitance|the]] positive rail ($V_{OH}$, output high) [[learning/notes/micro-context/push-pull-vs-open-drain|and]] to the negative rail or ground ($V_{OL}$, output low), measured under a stated load [[learning/notes/quick-context/capacitance|current]].

## How It Works

- The output stage is a [[micro-context/push-pull-vs-open-drain|push-pull]] pair of transistors ([[learning/notes/micro-context/push-pull-vs-open-drain|Q6]]) [[learning/notes/quick-context/breaking-elongation-rate|with]] nonzero on-resistance.
- Under load, the load current times that on-resistance drops a few hundred millivolts, so the output can't quite reach the rail.
- $V_{OH}$ is the highest the output reaches near $[[learning/notes/quick-context/capacitor|V]]^+$; $V_{OL}$ the lowest near ground — [[learning/notes/quick-context/bjt-specifications|both]] quoted at a given load ([[learning/notes/quick-context/bjt-specifications|e]].[[learning/notes/quick-context/cations-and-reduction|g]]. [[learning/notes/quick-context/meddpicc-qualification-framework|2]].[[learning/notes/quick-context/comparator-specification|5 mA]]).
- The harder you load it, the worse the swing — which is [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] these numbers are *always* specified at a load current.

```
   V+  ----------------------------  (positive rail)
        ^ small gap = I_load x R_on
   V_OH ---------  output HIGH lands just below V+
        :
        :   (output swings between these levels)
        :
   V_OL ---------  output LOW lands just above ground
        v small gap
   GND ----------------------------  (negative rail)

   Bigger load current -> bigger gaps.
```

**Key insight:** "[[learning/notes/quick-context/op-amp|Rail-to-rail]] output" never means *exactly* the rail under load — the output transistors' on-resistance always leaves a small gap, and that gap decides [[learning/notes/quick-context/differential-pair|whether]] the next [[learning/notes/quick-context/code-to-gates-and-bootstrapping|logic gate]] reads a clean HIGH/LOW.
