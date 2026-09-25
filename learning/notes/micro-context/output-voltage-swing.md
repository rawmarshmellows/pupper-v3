---
term: Output Voltage Swing (V_OH / V_OL)
created: 2026-06-07
---

# Output Voltage Swing ($V_{OH}$ / $V_{OL}$)

> **Related:** [[micro-context/capacitive-voltage-sensing]] | [[micro-context/input-offset-voltage]] | [[micro-context/offset-voltage-drift]] | [[micro-context/open-loop-voltage-gain]] | [[micro-context/4-wire-kelvin-measurement]]

**[[quick-context/capacitance|Definition]]:** How close a [[quick-context/comparator|comparator]]'s or op-amp's output [[quick-context/embedded-communication-protocols|can]] drive to the positive rail ($V_{OH}$, output high) [[micro-context/push-pull-vs-open-drain|and]] to the negative rail or ground ($V_{OL}$, output low), measured under a stated load current.

## How It Works

- The output stage is a [[micro-context/push-pull-vs-open-drain|push-pull]] pair of transistors (Q6) with nonzero on-resistance.
- Under load, the load current times that on-resistance drops a few hundred millivolts, so the output can't quite reach the rail.
- $V_{OH}$ is the highest the output reaches near $V^+$; $V_{OL}$ the lowest near ground — [[quick-context/bjt-specifications|both]] quoted at a given load (e.g. 2.[[quick-context/comparator-specification|5 mA]]).
- The harder you load it, the worse the swing — which is why these numbers are *always* specified at a load current.

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

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** "[[quick-context/op-amp|Rail-to-rail]] output" never means *exactly* the rail under load — the output transistors' on-resistance always leaves a small gap, and that gap decides [[quick-context/differential-pair|whether]] the next logic [[quick-context/transistor|gate]] reads a clean HIGH/LOW.
