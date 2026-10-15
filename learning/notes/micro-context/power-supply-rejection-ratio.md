---
term: Power-Supply Rejection Ratio (PSRR)
created: 2026-06-07
---

> **Related:** [[learning/notes/micro-context/common-mode-rejection-ratio]] | [[learning/notes/micro-context/power-inductor]] | [[learning/notes/micro-context/quiescent-supply-current]] | [[learning/notes/quick-context/power-watts-joules]]

# Power-Supply Rejection Ratio ($PSRR$)

> **[[learning/notes/quick-context/tensile-strength-materials|]]See also:** [[quick-context/comparator-specification]] | [[micro-context/input-offset-voltage]] | [[micro-context/decoupling-capacitor]] | [[small-context/decibels-across-domains]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] measure (in dB) of how well a [[learning/notes/quick-context/comparator|comparator]] [[learning/notes/micro-context/push-pull-vs-open-drain|or]] op-amp ignores wiggle, noise, or ripple on its [[learning/notes/quick-context/d-flip-flop|power]]-supply rails, keeping [[learning/notes/quick-context/capacitance|the]] output from following the supply.

## How It Works

- Internal bias currents [[learning/notes/micro-context/push-pull-vs-open-drain|and]] [[learning/notes/quick-context/comparator|reference]] points are derived from the supply rails, so rail variation [[learning/notes/quick-context/embedded-communication-protocols|can]] leak through to the inputs and output.
- An imperfect design passes some of that variation through; PSRR measures how much is rejected, referred back to the input.
- Higher dB = [[learning/notes/quick-context/comparator-specification|better]]: 80 dB attenuates supply ripple by about 10[[learning/notes/quick-context/how-passive-and-discrete-components-are-made|,]]000×.
- It's [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] a noisy or sagging battery rail doesn't directly move the switching [[learning/notes/micro-context/capacitive-voltage-sensing|threshold]] — though a [[micro-context/decoupling-capacitor|decoupling capacitor]] still helps at high frequency where PSRR falls [[learning/notes/quick-context/bjt-specifications|off]].

```
   V+ rail (noisy)                output
   .--.  .--.  .--.               ---------  (clean)
  -'  '--'  '--'  '- ripple        ripple rejected
        |                          by PSRR
        v
   +------------+
   | comparator |---> out
   +------------+
   80 dB ~ 10,000x rejection of supply wiggle.
```

**Key insight:** PSRR is the [[micro-context/input-offset-voltage|input-offset]] twin for the supply pin — instead of "how much does an input difference matter," it answers "how much does a wiggle on the [[learning/notes/quick-context/schematic-reading|power rail]] leak in as if it were a real [[learning/notes/quick-context/comparator|signal]]."
