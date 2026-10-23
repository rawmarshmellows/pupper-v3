---
term: Current Behavior with Inductors vs Capacitors
created: 2026-02-08
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/current-electrons-per-second]] | [[learning/notes/micro-context/current-mirror]] | [[learning/notes/micro-context/input-bias-current]] | [[learning/notes/micro-context/mosfet]]

# Current Behavior with Inductors vs Capacitors

**[[learning/notes/quick-context/capacitance|Definition]]:** [[quick-context/inductor|Inductors]] [[learning/notes/micro-context/push-pull-vs-open-drain|and]] [[quick-context/capacitor|capacitors]] have opposite relationships with [[learning/notes/quick-context/capacitance|current]]. Inductors oppose current *changes* (current stays steady, [[learning/notes/quick-context/voltage|voltage]] [[learning/notes/quick-context/embedded-communication-protocols|can]] jump). [[learning/notes/quick-context/voltage|Capacitors]] oppose voltage *changes* (voltage stays steady, current can jump). They're exact duals.

## How It Works

- An [[learning/notes/quick-context/fundamental-electronic-parts-index|inductor]] stores energy in a magnetic field; increasing current builds [[learning/notes/quick-context/capacitance|the]] field gradually ($V = L \times dI/dt$), so current can't jump instantly.
- A [[learning/notes/quick-context/capacitor|capacitor]] stores energy in an [[learning/notes/quick-context/voltage-current-causality|electric field]]; adding [[learning/notes/quick-context/cations-and-reduction|charge]] raises voltage gradually ($I = C \times dV/dt$), so voltage can't jump instantly.
- Inductors pass DC freely (just a wire at [[learning/notes/quick-context/self-induction|steady state]]) but resist AC (high impedance at high frequency).
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

**Key insight:** Think of an inductor as "current inertia" (hard to start or [[learning/notes/quick-context/camera-fundamentals|stop]] current) and a capacitor as "voltage inertia" (hard to change voltage quickly).
