---
term: Current Behavior with Inductors vs Capacitors
created: 2026-02-08
updated: 2026-03-27
---

> **Related:** [[quick-context/voltage]] | [[micro-context/can-bus-termination]] | [[micro-context/can-bus-transceiver]] | [[quick-context/can-bus]] | [[quick-context/capacitor]]

# Current Behavior with Inductors vs Capacitors

**Definition:** [[quick-context/inductor|Inductors]] and [[quick-context/capacitor|capacitors]] have opposite relationships with current. Inductors oppose current *changes* (current stays steady, [[quick-context/voltage|voltage]] [[micro-context/can-bus-termination|can]] jump). Capacitors oppose voltage *changes* (voltage stays steady, current [[micro-context/can-bus-transceiver|can]] jump). They're exact duals.

## How It Works

- An inductor stores energy in a magnetic field; increasing current builds the field gradually ($V = L \times dI/dt$), so current [[quick-context/can-bus|can]]'t jump instantly.
- A capacitor stores energy in an electric field; adding charge raises voltage gradually ($I = C \times dV/dt$), so voltage can't jump instantly.
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

**Key insight:** Think of an inductor as "current inertia" (hard to start or stop current) and a capacitor as "voltage inertia" (hard to change voltage quickly).
