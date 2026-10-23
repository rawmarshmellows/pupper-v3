---
term: Power Inductor
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# Power Inductor

> **See also:** [[quick-context/electric-current]] | [[micro-context/buck-converter]]

**[[learning/notes/quick-context/capacitance|Definition]]:** A coil that stores energy in a magnetic field [[learning/notes/micro-context/push-pull-vs-open-drain|and]] resists changes in [[learning/notes/quick-context/capacitance|current]]. In switching [[learning/notes/quick-context/d-flip-flop|power]] supplies like [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] [[learning/notes/micro-context/buck-converter|buck converter]], [[learning/notes/quick-context/capacitance|the]] 10µH [[learning/notes/quick-context/fundamental-electronic-parts-index|inductor]] smooths the chopped switching waveform into steady DC current. It acts as a "flywheel" that keeps current flowing during the [[learning/notes/quick-context/switches-to-registers-storing-data|switch]]-[[learning/notes/quick-context/bjt-specifications|off]] phase.

## How It Works

- [[learning/notes/quick-context/bare-minimal-data-storage-circuit|When]] current flows through the coil, it generates a magnetic field that stores energy ($E = \frac{1}{2}LI^2$).
- If current tries to change suddenly, the collapsing or growing magnetic field induces a [[learning/notes/quick-context/voltage|voltage]] that opposes the change ($V = L \times dI/dt$).
- In a buck converter's ON phase, the inductor stores energy from the input; in the OFF phase, it releases that energy to [[learning/notes/quick-context/existing-account-management-playbook|keep]] current flowing to the load through the freewheeling [[learning/notes/quick-context/diode|diode]].

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

**Key insight:** The inductor value (10µH) is chosen to balance ripple current against transient response—too large and the converter [[learning/notes/quick-context/embedded-communication-protocols|can]]'t respond to load changes, too small and output voltage becomes noisy.
