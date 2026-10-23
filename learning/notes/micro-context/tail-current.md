---
term: Tail Current
created: 2026-04-02
---

> **Related:** [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/current-electrons-per-second]] | [[learning/notes/micro-context/current-inductor-capacitor-relationship]] | [[learning/notes/micro-context/current-mirror]] | [[learning/notes/micro-context/input-bias-current]]

# Tail Current

**[[learning/notes/quick-context/capacitance|Definition]]:** A fixed-value [[learning/notes/quick-context/voltage-current-causality|current source]] connected to [[learning/notes/quick-context/capacitance|the]] shared [[learning/notes/quick-context/differential-pair|source]] [[learning/notes/quick-context/ros2-architecture|node]] of a [[learning/notes/quick-context/differential-pair|differential pair]]. It sets the [[learning/notes/quick-context/similarity-transform|total]] [[learning/notes/quick-context/capacitance|current]] budget that the [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] transistors [[learning/notes/quick-context/ros2-architecture|must]] split between them, ensuring the pair operates as a current-steering [[learning/notes/quick-context/switches-to-registers-storing-data|switch]] rather than two independent amplifiers.

## How It Works

- A current source (typically a [[micro-context/current-mirror|current mirror]]) forces a constant total current $I_{tail}$ through the shared source node — e.g., 100 $\mu$A.
- The differential input [[learning/notes/quick-context/voltage|voltage]] $V(+) - V(-)$ steers this fixed current left or right: if $V(+)$ is slightly higher, more current flows through the left [[learning/notes/quick-context/silicon-die|transistor]] [[learning/notes/micro-context/push-pull-vs-open-drain|and]] less through the right.
- Because $I_{tail}$ is constant, the two [[learning/notes/quick-context/differential-pair|drain]] currents always sum to $I_{tail}$ — [[learning/notes/quick-context/ram-addressing-decoder|one]] side's gain is the other side's loss.
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

**Key insight:** The [[learning/notes/quick-context/differential-pair|tail current source]] is what makes a differential pair reject common-mode signals — if [[learning/notes/quick-context/bjt-specifications|both]] inputs rise together, neither transistor [[learning/notes/quick-context/embedded-communication-protocols|can]] draw more current because the total is clamped, so the output doesn't change.
