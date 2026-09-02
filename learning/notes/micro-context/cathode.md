---
term: Cathode
created: 2026-02-25
updated: 2026-03-27
---

> **Related:** [[learning/notes/quick-context/differential-pair]] | [[learning/notes/quick-context/diode]] | [[learning/notes/quick-context/doped-silicon]] | [[learning/notes/quick-context/pcb-chip-transistor-hierarchy]]

# Cathode

> **See also:** [[quick-context/electrodes]]

**Definition:** The terminal where electrons flow IN — regardless of context. In [[quick-context/electrolysis|electrolysis]], it's the negative [[learning/notes/quick-context/electrodes|electrode]] where [[learning/notes/quick-context/cations-and-reduction|reduction]] (electron gain) occurs. In a [[quick-context/diode|diode]], it's the bar side of the symbol, marked K — where conventional current exits.

## How It Works

- Electrons arrive at the cathode from the external circuit and are consumed by reduction reactions (species gain electrons here).
- In [[learning/notes/quick-context/electrolysis|electrolysis]], the [[learning/notes/quick-context/power-watts-joules|power]] supply forces electrons onto the cathode, making it the negative terminal where cations are reduced.
- In a [[learning/notes/quick-context/diode|diode]], conventional current exits through the cathode (marked K or bar) — electron flow enters.

```
  CHEMISTRY (electrolysis):         ELECTRONICS (diode):

  Power Supply ⊖                       A              K
         │                          (anode)       (cathode)
         ▼ electrons IN                │              │
    ┌─────────┐                        ├────|>|───────┤
    │ CATHODE │                      triangle        bar
    │  (−)    │ ← reduction
    │         │   happens here      Current ════▶ (A → K)
    └─────────┘                     Electrons ◀══ (K → A)

  Common thread: electrons ARRIVE at the cathode
```

**Key insight:** "Cathode" always means "where electrons enter and reduction occurs" — in electrolysis it's the negative electrode, but in a [[quick-context/galvanic-cells-batteries|battery]] it's the positive terminal. The polarity flips, but the electron-flow rule never does. Mnemonic: **C**athode attracts **C**ations.
