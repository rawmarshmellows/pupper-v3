---
term: Common-Mode Rejection Ratio (CMRR)
created: 2026-06-07
---
> **Related:** [[learning/notes/micro-context/input-common-mode-range]] | [[learning/notes/micro-context/power-supply-rejection-ratio]] | [[learning/notes/micro-context/current-mirror]] | [[learning/notes/micro-context/input-bias-current]] | [[learning/notes/micro-context/input-offset-voltage]]


# Common-Mode Rejection Ratio ($CMRR$)

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[quick-context/comparator-specification]] | [[micro-context/tail-current]] | [[quick-context/differential-pair]] | [[small-context/decibels-across-domains]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** A measure (in dB) of how well a differential amplifier or [[learning/notes/quick-context/comparator|comparator]] ignores a [[learning/notes/micro-context/piezoelectric-effect|voltage applied]] *equally* to [[learning/notes/quick-context/bjt-specifications|both]] inputs, responding [[learning/notes/quick-context/comparator-specification|only]] to the *difference* between them.

## How It Works

- An ideal [[quick-context/differential-pair|differential pair]] responds only to $V(+) - V(-)$ and is blind to a common voltage that moves both inputs together.
- A real [[micro-context/tail-current|tail current source]] (Q5) isn't perfect, so moving both inputs together leaks a little change into the output — CMRR quantifies how little.
- Higher dB = [[learning/notes/quick-context/comparator-specification|better]] rejection: 75 dB attenuates a common-mode swing by about 5600× at the output.
- CMRR usually improves with more supply headroom ([[learning/notes/quick-context/comparator-specification|LMC7211-N]]: 75 dB at 5 V → [[learning/notes/quick-context/comparator-specification|82 dB at 15 V]]).

```
  Both inputs move TOGETHER (common-mode):

  V(+) -.  .--.  .--.            output -------------  (flat)
        '--'  '--'  '-- common    ignored / attenuated
  V(-) -.  .--.  .--.             by CMRR
        '--'  '--'  '--

  Only the DIFFERENCE V(+)-V(-) reaches the output.
  CMRR (dB) = how much common-mode is rejected.
  75 dB ~ 5600x attenuation.
```

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** CMRR is really a report card on the [[micro-context/tail-current|tail current source]] — the closer it [[learning/notes/quick-context/pupper-lab7-vision-tracking|holds]] the pair's [[learning/notes/quick-context/similarity-transform|total]] [[learning/notes/quick-context/capacitance|current]] constant, the more the chip ignores noise riding on both inputs at once.
