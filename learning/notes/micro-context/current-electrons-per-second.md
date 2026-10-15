---
term: Current and Electrons Per Second
created: 2026-01-26
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/current-inductor-capacitor-relationship]] | [[learning/notes/micro-context/current-mirror]] | [[learning/notes/micro-context/input-bias-current]] | [[learning/notes/micro-context/quiescent-supply-current]]

# Current and Electrons Per Second[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[quick-context/electric-current]] | [[quick-context/parallel-vs-series-voltage]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[quick-context/electric-current|Electric current]] (measured in amperes) is [[learning/notes/quick-context/cations-and-reduction|charge]] flow per second. [[learning/notes/quick-context/ram-addressing-decoder|One]] ampere equals one coulomb per second, which equals [[learning/notes/quick-context/tensor|6.]]24 × 10¹⁸ [[learning/notes/quick-context/anions-and-oxidation|electrons]] per second passing [[learning/notes/quick-context/anions-and-oxidation|a]] [[learning/notes/quick-context/epson-rc-plus-programming|point]] in a wire.

## How It Works

- An [[learning/notes/quick-context/voltage-current-causality|electric field]] (from a [[learning/notes/quick-context/voltage-current-causality|voltage source]]) [[learning/notes/quick-context/python-to-machine-code-pipeline|pushes]] free electrons through [[learning/notes/quick-context/capacitance|the]] conductor in a coordinated drift.
- At any cross-section of the wire, the number of electrons passing per second determines the [[learning/notes/quick-context/capacitance|current]] in amperes.
- One ampere equals one coulomb (6.24 × 10¹⁸ electrons) flowing past that point every second.

```
1 Ampere = 1 Coulomb/second = 6.24 × 10¹⁸ electrons/second

    ───────────────────────────────────────►
       e⁻  e⁻  e⁻  e⁻  e⁻  e⁻  e⁻  e⁻  e⁻
    ───────────────────────────────────────►
                      │
                      ▼ count here
              ┌───────────────┐
              │ 6.24 × 10¹⁸   │
              │ electrons/sec │
              │    = 1 Amp    │
              └───────────────┘
```

**Key insight:** The conversion factor (6.24 × 10¹⁸) is simply [[learning/notes/quick-context/meddpicc-qualification-framework|1]] divided by the [[learning/notes/quick-context/anions-and-oxidation|electron]]'s charge (1.6 × 10⁻¹⁹ coulombs)—current in amps times this number gives electrons per second.
