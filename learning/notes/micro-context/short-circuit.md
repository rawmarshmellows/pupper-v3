---
term: Short Circuit
created: 2026-04-17
---

# Short Circuit

> **Related:** [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]] | [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/ads1110-battery-adc]] | [[micro-context/bjt-mosfet-igbt]]

**[[quick-context/capacitance|Definition]]:** An unintended low-resistance path between [[micro-context/schmitt-trigger-hysteresis|two]] points in a circuit (typically power [[micro-context/push-pull-vs-open-drain|and]] ground) that bypasses the intended load. By [[learning/notes/quick-context/voltage-current-causality|Ohm's law]] $I = V/R$, near-zero resistance produces a near-infinite current surge.

## How It Works

- A conductive path forms where [[quick-context/mcp6541-as-lmc7211-replacement|none]] was designed — [[quick-context/soldering|solder]] bridge, frayed wire, damaged insulation, or [[quick-context/pcb-assembly-files-bom-cpl|component]] failure.
- Current divides among all available paths inversely proportional to their resistance — so [[quick-context/bare-minimal-data-storage-circuit|when]] the short's resistance approaches zero, it carries almost all the current and starves the intended load.
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

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** A short circuit isn't about [[quick-context/uart|wires]] touching — it's about resistance collapsing. The "damage" is just $V/R$ doing exactly what physics says it must when $R$ approaches zero.
