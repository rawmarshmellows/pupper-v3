---
term: Short Circuit
created: 2026-04-17
---
> **Related:** [[learning/notes/quick-context/bare-minimal-data-storage-circuit]] | [[learning/notes/quick-context/pcb-printed-circuit-board]] | [[learning/notes/quick-context/pwm-controller-circuit]] | [[learning/notes/quick-context/voltage]]


# Short Circuit

> **See also:** [[learning/notes/quick-context/voltage-current-causality]] | [[learning/notes/quick-context/grounding-and-return-paths]]

**Definition:** An unintended low-resistance path between two points in a circuit (typically power and ground) that bypasses the intended load. By [[learning/notes/quick-context/voltage-current-causality|Ohm's law]] $I = V/R$, near-zero resistance produces a near-infinite current surge.

## How It Works

- A conductive path forms where none was designed — solder bridge, frayed wire, damaged insulation, or component failure.
- Current divides among all available paths inversely proportional to their resistance — so when the short's resistance approaches zero, it carries almost all the current and starves the intended load.
- Power dissipated as heat is $P = I^2 R$ across the wire's tiny residual resistance, which still produces enough energy to melt traces or ignite insulation.
- Protection devices (fuses, breakers, current-limited supplies) detect the surge and cut power before damage spreads.

```
   Normal path:              Short circuit:

   V+ ──┬──[ LOAD ]──┐       V+ ──┬──[ LOAD ]──┐
        │            │            │            │
        │   I small  │            └─[~0 Ω]─────┤
        │            │                ↑        │
   GND ─┴────────────┘       GND ─────┴────────┘
                                  I huge → 🔥
```

**Key insight:** A short circuit isn't about wires touching — it's about resistance collapsing. The "damage" is just $V/R$ doing exactly what physics says it must when $R$ approaches zero.
