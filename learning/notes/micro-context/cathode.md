---
term: Cathode
created: 2026-02-25
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# Cathode[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[quick-context/electrodes]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] [[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens|terminal]] where [[learning/notes/quick-context/anions-and-oxidation|electrons]] flow IN — regardless of context. In [[quick-context/electrolysis|electrolysis]], it's the negative [[learning/notes/quick-context/cations-and-reduction|electrode]] where [[learning/notes/quick-context/cations-and-reduction|reduction]] ([[learning/notes/quick-context/anions-and-oxidation|electron]] gain) occurs. In [[learning/notes/quick-context/anions-and-oxidation|a]] [[quick-context/diode|diode]], it's the bar side of the symbol, marked K — where conventional [[learning/notes/quick-context/capacitance|current]] exits.

## How It Works

- Electrons arrive at the [[learning/notes/quick-context/cations-and-reduction|cathode]] from the external circuit [[learning/notes/micro-context/push-pull-vs-open-drain|and]] are consumed by reduction reactions (species gain electrons here).
- In [[learning/notes/quick-context/electrolysis|electrolysis]], the [[learning/notes/quick-context/d-flip-flop|power]] supply forces electrons onto the cathode, making it the negative terminal where cations are reduced.
- In a [[learning/notes/quick-context/diode|diode]], conventional current exits through the cathode (marked K [[learning/notes/micro-context/push-pull-vs-open-drain|or]] bar) — [[learning/notes/quick-context/electrodes|electron flow]] enters.

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

**Key insight:** "Cathode" always means "where electrons enter and reduction occurs" — in electrolysis it's the negative electrode, but in a [[quick-context/galvanic-cells-batteries|battery]] it's the positive terminal. The polarity flips, but the electron-flow rule never does. Mnemonic: **[[learning/notes/quick-context/bjt-specifications|C]]**athode attracts **C**ations.
