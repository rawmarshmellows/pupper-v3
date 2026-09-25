---
term: Tail Current
created: 2026-04-02
---

> **Related:** [[micro-context/ac-dc-current]] | [[micro-context/current-electrons-per-second]] | [[micro-context/current-inductor-capacitor-relationship]] | [[micro-context/current-mirror]] | [[micro-context/input-bias-current]]

# Tail Current

**[[quick-context/capacitance|Definition]]:** A fixed-value [[quick-context/voltage-current-causality|current source]] connected to the shared source node of a differential pair. It sets the total current budget that the [[micro-context/schmitt-trigger-hysteresis|two]] transistors must split between them, ensuring the pair operates as a current-steering switch rather than two independent amplifiers.

## How It Works

- A current source (typically a [[micro-context/current-mirror|current mirror]]) forces a constant total current $I_{tail}$ through the shared source node — e.g., 100 $\mu$A.
- The differential input voltage $V(+) - V(-)$ steers this fixed current left or right: if $V(+)$ is slightly higher, more current flows through the left [[quick-context/transistor|transistor]] [[micro-context/push-pull-vs-open-drain|and]] less through the right.
- Because $I_{tail}$ is constant, the two drain currents always sum to $I_{tail}$ — one side's gain is the other side's loss.
- This constant-sum constraint is [[quick-context/bare-minimal-data-storage-circuit|what]] converts a voltage difference into a differential current [[quick-context/comparator|signal]], which is the core [[quick-context/mcp6541-as-lmc7211-replacement|function]] of the differential pair.

```
                 Vdd
                  |
            +-----------+
            |   Loads   |
            +-----+-----+
            |           |
          I_L          I_R       I_L + I_R = I_tail (always)
            |           |
  V(+)--| M1         M2 |--V(-)
            \           /
             \         /
              +---+---+
                  |
            shared source
                  |
            +-----+-----+
            |   I_tail   |      Fixed current source
            +-----+-----+
                  |
                 GND
```

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** The [[quick-context/differential-pair|tail current source]] is what makes a differential pair reject common-mode signals — if [[quick-context/bjt-specifications|both]] inputs rise together, neither transistor [[quick-context/embedded-communication-protocols|can]] draw more current because the total is clamped, so the output doesn't change.
