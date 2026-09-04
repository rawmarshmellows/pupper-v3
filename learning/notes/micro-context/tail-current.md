---
term: Tail Current
created: 2026-04-02
---
> **Related:** [[learning/notes/quick-context/differential-pair]] | [[learning/notes/quick-context/comparator-specification]] | [[learning/notes/quick-context/fundamental-electronic-parts-index]] | [[learning/notes/micro-context/current-mirror]] | [[learning/notes/micro-context/common-mode-rejection-ratio]]

# Tail Current

**Definition:** A fixed-value current source connected to the shared source node of a [[learning/notes/quick-context/differential-pair|differential pair]]. It sets the total current budget that the two transistors must split between them, ensuring the pair operates as a current-steering switch rather than two independent amplifiers.

## How It Works

- A current source (typically a [[micro-context/current-mirror|current mirror]]) forces a constant total current $I_{tail}$ through the shared source node — e.g., 100 $\mu$A.
- The differential input [[learning/notes/quick-context/voltage|voltage]] $V(+) - V(-)$ steers this fixed current left or right: if $V(+)$ is slightly higher, more current flows through the left [[learning/notes/quick-context/transistor|transistor]] and less through the right.
- Because $I_{tail}$ is constant, the two drain currents always sum to $I_{tail}$ — one side's gain is the other side's loss.
- This constant-sum constraint is what converts a voltage difference into a differential current signal, which is the core function of the differential pair.

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

**Key insight:** The tail current source is what makes a differential pair reject common-mode signals — if both inputs rise together, neither transistor can draw more current because the total is clamped, so the output doesn't change.
