---
term: Current Behavior with Inductors vs Capacitors
created: 2026-02-08
updated: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/decoupling-capacitor]] | [[learning/notes/micro-context/power-inductor]] | [[learning/notes/quick-context/capacitor]] | [[learning/notes/quick-context/inductor]]


# Current Behavior with Inductors vs Capacitors

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** [[quick-context/inductor|Inductors]] and [[quick-context/capacitor|capacitors]] have opposite relationships with [[learning/notes/quick-context/capacitance|current]]. Inductors oppose current *changes* (current stays steady, [[learning/notes/quick-context/voltage|voltage]] can jump). [[learning/notes/quick-context/voltage|Capacitors]] oppose voltage *changes* (voltage stays steady, current can jump). They're exact duals.

## How It Works

- An [[learning/notes/quick-context/inductor|inductor]] stores energy in a magnetic field; increasing current builds the field gradually ($V = L \times dI/dt$), so current can't jump instantly.
- A [[learning/notes/quick-context/capacitor|capacitor]] stores energy in an [[learning/notes/quick-context/voltage-current-causality|electric field]]; adding [[learning/notes/quick-context/cations-and-reduction|charge]] raises voltage gradually ($I = C \times dV/dt$), so voltage can't jump instantly.
- Inductors pass DC freely (just a wire at steady state) but resist AC (high impedance at high frequency).
- Capacitors [[learning/notes/quick-context/capacitance|block DC]] (open circuit at steady state) but pass AC (low impedance at high frequency).

```
             INDUCTOR                    CAPACITOR
          (opposes ΔI)                 (opposes ΔV)

    V = L × dI/dt                 I = C × dV/dt

    Current ramps slowly:         Current jumps instantly:

    I ▲      ╱─────              I ▲ │
      │    ╱                       │ │╲
      │  ╱                         │ │ ╲
      │╱                           │ │  ╲____
      └───────────► t              └─┴───────► t

    • Passes DC (wire at DC)      • Blocks DC (open at DC)
    • Blocks AC (high impedance)  • Passes AC (low impedance)
```

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** Think of an inductor as "current inertia" (hard to start or [[learning/notes/quick-context/camera-fundamentals|stop]] current) and a capacitor as "voltage inertia" (hard to change voltage quickly).
