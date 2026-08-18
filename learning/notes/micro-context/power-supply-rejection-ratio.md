---
term: Power-Supply Rejection Ratio (PSRR)
created: 2026-06-07
---
> **Related:** [[micro-context/common-mode-rejection-ratio]] | [[micro-context/open-loop-voltage-gain]] | [[micro-context/offset-voltage-drift]] | [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/input-common-mode-range]]

# Power-Supply Rejection Ratio ($PSRR$)

> **See also:** [[quick-context/comparator-specification]] | [[micro-context/input-offset-voltage]] | [[micro-context/decoupling-capacitor]] | [[small-context/decibels-across-domains]]

**Definition:** A measure (in dB) of how well a [[quick-context/comparator|comparator]] or op-amp ignores wiggle, noise, or ripple on its power-supply rails, keeping the output from following the supply.

## How It Works

- Internal bias currents and reference points are derived from the supply rails, so rail variation can leak through to the inputs and output.
- An imperfect design passes some of that variation through; PSRR measures how much is rejected, referred back to the input.
- Higher dB = better: 80 dB attenuates supply ripple by about 10,000×.
- It's why a noisy or sagging battery rail doesn't directly move the switching threshold — though a [[micro-context/decoupling-capacitor|decoupling capacitor]] still helps at high frequency where PSRR falls off.

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

**Key insight:** PSRR is the [[micro-context/input-offset-voltage|input-offset]] twin for the supply pin — instead of "how much does an input difference matter," it answers "how much does a wiggle on the power rail leak in as if it were a real signal."
