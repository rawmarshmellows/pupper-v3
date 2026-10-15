---
term: Short Circuit
created: 2026-04-17
---

> **Related:** [[learning/notes/quick-context/bare-minimal-data-storage-circuit]] | [[learning/notes/quick-context/pcb-printed-circuit-board]] | [[learning/notes/quick-context/pwm-controller-circuit]]

# Short Circuit[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[learning/notes/quick-context/voltage-current-causality]] | [[learning/notes/quick-context/grounding-and-return-paths]]

**[[learning/notes/quick-context/capacitance|Definition]]:** An unintended low-resistance path between [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] points in [[learning/notes/quick-context/anions-and-oxidation|a]] circuit (typically [[learning/notes/quick-context/d-flip-flop|power]] [[learning/notes/micro-context/push-pull-vs-open-drain|and]] ground) that bypasses [[learning/notes/quick-context/capacitance|the]] intended load. By [[learning/notes/quick-context/voltage-current-causality|Ohm's law]] $[[learning/notes/quick-context/anions-and-oxidation|I]] = [[learning/notes/quick-context/capacitor|V]]/[[learning/notes/quick-context/cations-and-reduction|R]]$, near-[[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|zero]] resistance produces a near-infinite [[learning/notes/quick-context/capacitance|current]] surge.

## How It Works

- A conductive path forms where [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|none]] was designed — [[learning/notes/quick-context/soldering|solder]] bridge, frayed wire, damaged insulation, [[learning/notes/micro-context/push-pull-vs-open-drain|or]] [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|component]] failure.
- Current divides among all available paths inversely proportional to their resistance — so [[learning/notes/quick-context/bare-minimal-data-storage-circuit|when]] the short's resistance approaches zero, it carries almost all the current and starves the intended load.
- Power dissipated as heat is $P = I^[[learning/notes/quick-context/meddpicc-qualification-framework|2]] R$ across the wire's tiny residual resistance, which still produces enough energy to melt traces or ignite insulation.
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

**Key insight:** A short circuit isn't about [[learning/notes/quick-context/uart|wires]] touching — it's about resistance collapsing. The "damage" is just $V/R$ doing exactly [[learning/notes/quick-context/bare-minimal-data-storage-circuit|what]] physics says it [[learning/notes/quick-context/ros2-architecture|must]] when $R$ approaches zero.
