---
term: Current and Electrons Per Second
created: 2026-01-26
updated: 2026-03-27
---
> **Related:** [[learning/notes/quick-context/electric-current]] | [[learning/notes/quick-context/voltage-current-causality]] | [[learning/notes/micro-context/anode]] | [[learning/notes/micro-context/cathode]] | [[learning/notes/micro-context/coulomb-history]]


# Current and Electrons Per Second

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[quick-context/electric-current]] | [[quick-context/parallel-vs-series-voltage]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** [[quick-context/electric-current|Electric current]] (measured in amperes) is [[learning/notes/quick-context/cations-and-reduction|charge]] flow per second. One ampere equals one coulomb per second, which equals 6.24 × 10¹⁸ [[learning/notes/quick-context/anions-and-oxidation|electrons]] per second passing a [[learning/notes/quick-context/epson-rc-plus-programming|point]] in a wire.

## How It Works

- An [[learning/notes/quick-context/voltage-current-causality|electric field]] (from a [[learning/notes/quick-context/voltage-current-causality|voltage source]]) [[learning/notes/quick-context/python-to-machine-code-pipeline|pushes]] free electrons through the conductor in a coordinated drift.
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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** The conversion factor (6.24 × 10¹⁸) is simply 1 divided by the [[learning/notes/quick-context/anions-and-oxidation|electron]]'s charge (1.6 × 10⁻¹⁹ coulombs)—current in amps times this number gives electrons per second.
