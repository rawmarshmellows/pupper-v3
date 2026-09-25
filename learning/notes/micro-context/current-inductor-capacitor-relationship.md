---
term: Current Behavior with Inductors vs Capacitors
created: 2026-02-08
updated: 2026-03-27
---

> **Related:** [[micro-context/ac-dc-current]] | [[micro-context/current-electrons-per-second]] | [[micro-context/current-mirror]] | [[micro-context/decoupling-capacitor]] | [[micro-context/input-bias-current]]

# Current Behavior with Inductors vs Capacitors

**[[quick-context/capacitance|Definition]]:** [[quick-context/inductor|Inductors]] [[micro-context/push-pull-vs-open-drain|and]] [[quick-context/capacitor|capacitors]] have opposite relationships with current. Inductors oppose current *changes* (current stays steady, [[quick-context/voltage|voltage]] [[quick-context/embedded-communication-protocols|can]] jump). Capacitors oppose voltage *changes* (voltage stays steady, current can jump). They're exact duals.

## How It Works

- An [[quick-context/inductor|inductor]] stores energy in a magnetic field; increasing current builds the field gradually ($V = L \times dI/dt$), so current can't jump instantly.
- A [[quick-context/capacitor|capacitor]] stores energy in an [[quick-context/voltage-current-causality|electric field]]; adding charge raises voltage gradually ($I = C \times dV/dt$), so voltage can't jump instantly.
- Inductors pass DC freely (just a wire at steady state) but resist AC (high impedance at high frequency).
- Capacitors block DC (open circuit at steady state) but pass AC (low impedance at high frequency).

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

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** Think of an inductor as "current inertia" (hard to start or [[quick-context/camera-fundamentals|stop]] current) and a capacitor as "voltage inertia" (hard to change voltage quickly).
