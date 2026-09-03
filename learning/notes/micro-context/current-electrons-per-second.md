---
term: Current and Electrons Per Second
created: 2026-01-26
updated: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]


# Current and Electrons Per Second

> **See also:** [[learning/notes/quick-context/electric-current]] | [[learning/notes/quick-context/parallel-vs-series-voltage]]

**Definition:** [[learning/notes/quick-context/electric-current|Electric current]] (measured in amperes) is charge flow per second. One ampere equals one coulomb per second, which equals 6.24 × 10¹⁸ electrons per second passing a point in a wire.

## How It Works

- An electric field (from a [[learning/notes/quick-context/voltage|voltage]] source) pushes free electrons through the conductor in a coordinated drift.
- At any cross-section of the wire, the number of electrons passing per second determines the current in amperes.
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

**Key insight:** The conversion factor (6.24 × 10¹⁸) is simply 1 divided by the electron's charge (1.6 × 10⁻¹⁹ coulombs)—current in amps times this number gives electrons per second.
