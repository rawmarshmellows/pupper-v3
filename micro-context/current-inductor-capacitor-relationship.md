---
term: Current Behavior with Inductors vs Capacitors
created: 2026-02-08
---

# Current Behavior with Inductors vs Capacitors

**Definition:** [[quick-context/inductor|Inductors]] and [[quick-context/capacitor|capacitors]] have opposite relationships with current. Inductors oppose current *changes* (current stays steady, voltage can jump). Capacitors oppose voltage *changes* (voltage stays steady, current can jump). They're exact duals.

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
