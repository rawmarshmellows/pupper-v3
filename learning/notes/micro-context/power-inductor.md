---
term: Power Inductor
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[micro-context/ac-dc-current]] | [[micro-context/buck-converter]] | [[micro-context/capacitive-voltage-sensing]] | [[micro-context/current-inductor-capacitor-relationship]] | [[micro-context/decoupling-capacitor]]

# Power Inductor

> **See also:** [[quick-context/electric-current]] | [[micro-context/buck-converter]]

**Definition:** A coil that stores energy in a magnetic field and resists changes in current. In switching power supplies like your buck converter, the 10µH [[quick-context/inductor|inductor]] smooths the chopped switching waveform into steady DC current. It acts as a "flywheel" that keeps current flowing during the switch-off phase.

## How It Works

- When current flows through the coil, it generates a magnetic field that stores energy ($E = \frac{1}{2}LI^2$).
- If current tries to change suddenly, the collapsing or growing magnetic field induces a voltage that opposes the change ($V = L \times dI/dt$).
- In a buck converter's ON phase, the inductor stores energy from the input; in the OFF phase, it releases that energy to keep current flowing to the load through the freewheeling [[quick-context/diode|diode]].

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
