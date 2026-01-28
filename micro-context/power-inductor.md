---
term: Power Inductor
created: 2026-01-27
---

# Power Inductor

> **See also:** [[quick-context/electric-current]] | [[micro-context/buck-converter]]

**Definition:** A coil that stores energy in a magnetic field and resists changes in current. In switching power supplies like your buck converter, the 10µH inductor smooths the chopped switching waveform into steady DC current. It acts as a "flywheel" that keeps current flowing during the switch-off phase.

```
INDUCTOR IN BUCK CONVERTER:

  Switch ON:                    Switch OFF:
  ┌────┐                        ┌────┐
  │ SW │──►current──►           │ SW │ (open)
  └────┘      │                 └────┘
              ▼
         ┌───ŻŻŻŻ───┐           ┌───ŻŻŻŻ───┐
         │ L stores │           │ L releases│──►current──►
         │ energy   │           │ energy    │
         └───____───┘           └───____───┘
              │                      ▲
              ▼                      │
            GND                   Diode provides path

  Inductor current (ripple):
         ╱╲    ╱╲    ╱╲
  IL:   ╱  ╲  ╱  ╲  ╱  ╲   ← smoothed, not pulsing
       ╱    ╲╱    ╲╱    ╲

  Larger L = less ripple, slower response
  Smaller L = more ripple, faster response
```

**Key insight:** The inductor value (10µH) is chosen to balance ripple current against transient response—too large and the converter can't respond to load changes, too small and output voltage becomes noisy.
