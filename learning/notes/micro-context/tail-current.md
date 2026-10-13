---
term: Tail Current
created: 2026-04-02
---
> **Related:** [[learning/notes/micro-context/current-mirror]] | [[learning/notes/micro-context/input-bias-current]] | [[learning/notes/micro-context/quiescent-supply-current]] | [[learning/notes/micro-context/common-mode-rejection-ratio]] | [[learning/notes/micro-context/input-common-mode-range]]


# Tail Current

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** A fixed-value [[learning/notes/quick-context/voltage-current-causality|current source]] connected to the shared source [[learning/notes/quick-context/ros2-architecture|node]] of a [[learning/notes/quick-context/differential-pair|differential pair]]. It sets the [[learning/notes/quick-context/similarity-transform|total]] current budget that the two transistors [[learning/notes/quick-context/ros2-architecture|must]] split between them, ensuring the pair operates as a current-steering [[learning/notes/quick-context/switches-to-registers-storing-data|switch]] rather than two independent amplifiers.

## How It Works

- A current source (typically a [[micro-context/current-mirror|current mirror]]) forces a constant total current $I_{tail}$ through the shared source node — e.g., 100 $\mu$A.
- The differential input [[learning/notes/quick-context/voltage|voltage]] $V(+) - V(-)$ steers this fixed current left or right: if $V(+)$ is slightly higher, more current flows through the left [[learning/notes/quick-context/transistor|transistor]] and less through the right.
- Because $I_{tail}$ is constant, the two [[learning/notes/quick-context/differential-pair|drain]] currents always sum to $I_{tail}$ — one side's gain is the other side's loss.
- This constant-sum [[learning/notes/quick-context/voltage-current-causality|constraint]] is [[learning/notes/quick-context/bare-minimal-data-storage-circuit|what]] converts a voltage difference into a differential current [[learning/notes/quick-context/comparator|signal]], which is the core [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|function]] of the differential pair.

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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** The [[learning/notes/quick-context/differential-pair|tail current source]] is what makes a differential pair reject common-mode signals — if [[learning/notes/quick-context/bjt-specifications|both]] inputs rise together, neither transistor can draw more current because the total is clamped, so the output doesn't change.
