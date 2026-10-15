---
term: Current Mirror
created: 2026-04-02
---

> **Related:** [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/current-electrons-per-second]] | [[learning/notes/micro-context/current-inductor-capacitor-relationship]] | [[learning/notes/micro-context/input-bias-current]] | [[learning/notes/micro-context/quiescent-supply-current]]

# Current Mirror[[learning/notes/quick-context/tensile-strength-materials|]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] circuit that copies a [[learning/notes/quick-context/comparator|reference]] [[learning/notes/quick-context/capacitance|current]] from [[learning/notes/quick-context/ram-addressing-decoder|one]] [[learning/notes/quick-context/silicon-die|transistor]] to another, producing a constant output current regardless of load conditions. It is [[learning/notes/quick-context/capacitance|the]] standard way to build on-chip current sources, including the [[micro-context/tail-current|tail current]] in [[learning/notes/quick-context/capacitance|differential pairs]].

## How It Works

- A reference current $I_{ref}$ (set by a [[learning/notes/quick-context/fundamental-electronic-parts-index|resistor]] [[learning/notes/micro-context/push-pull-vs-open-drain|or]] upstream [[learning/notes/quick-context/differential-pair|source]]) flows through a [[learning/notes/quick-context/diode|diode]]-connected [[micro-context/mosfet|MOSFET]] ([[learning/notes/quick-context/transistor|gate]] tied to [[learning/notes/quick-context/differential-pair|drain]]), forcing it to develop whatever $V_{gs}$ is needed to carry that current.
- A second matched transistor shares the same $V_{gs}$ (gates tied together), so it develops the same [[learning/notes/micro-context/mosfet|channel]] conditions [[learning/notes/micro-context/push-pull-vs-open-drain|and]] conducts the same current: $I_{[[learning/notes/micro-context/push-pull-vs-open-drain|out]]} \approx I_{ref}$.
- Because the output transistor operates in [[learning/notes/quick-context/bjt|saturation]], its drain current is nearly independent of drain [[learning/notes/quick-context/voltage|voltage]] — giving high output impedance, which is [[learning/notes/quick-context/bare-minimal-data-storage-circuit|what]] makes it a good [[learning/notes/quick-context/voltage-current-causality|current source]].
- Scaling the output transistor's $W/[[learning/notes/quick-context/anions-and-oxidation|L]]$ ratio relative to the reference transistor scales the copied current proportionally: $I_{out} = I_{ref} \times (W/L)_{out} / (W/L)_{ref}$.

```
    I_ref                 I_out ≈ I_ref
  (from Vdd)              (to load)
      |                       |
      |  drain          drain |
      +--+                +---+
         |   shared gate  |
         +------- + ------+
         |        |       |
     M1 -+        |       +- M2
         |     gate tied   |
         |     to M1 drain |
        GND               GND
```

**Key insight:** The "mirror" isn't magic — it works because matched transistors [[learning/notes/quick-context/breaking-elongation-rate|with]] [[learning/notes/quick-context/ram-addressing-decoder|identical]] $V_{gs}$ carry identical currents, so fixing one transistor's current automatically fixes the other's.
