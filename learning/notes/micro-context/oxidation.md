---
term: Oxidation
created: 2026-02-25
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# Oxidation

> **See also:** [[quick-context/anions-and-oxidation]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] loss of [[learning/notes/quick-context/anions-and-oxidation|electrons]] by an atom, [[learning/notes/quick-context/anions-and-oxidation|ion]], or [[learning/notes/quick-context/atoms-molecules-polymers-basics|molecule]]—always paired with [[quick-context/cations-and-reduction|reduction]] ([[learning/notes/quick-context/anions-and-oxidation|electron]] gain) somewhere else, [[learning/notes/quick-context/electrolysis|forming]] a redox reaction. Despite the name, oxygen need [[learning/notes/micro-context/can-bus-termination|not]] be involved.

## How It Works

- An atom or ion releases [[learning/notes/quick-context/ram-addressing-decoder|one]] or more electrons, increasing its [[learning/notes/quick-context/anions-and-oxidation|oxidation]] state (becoming more positive).
- The released electrons [[learning/notes/quick-context/ros2-architecture|must]] be accepted by another species (the oxidizing agent), which undergoes [[learning/notes/quick-context/cations-and-reduction|reduction]] — the [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] half-reactions are always coupled.
- The driving force is the difference in electron affinity: electrons flow from species that [[learning/notes/quick-context/d-flip-flop|hold]] them weakly to species that attract them strongly.

```
Oxidation = losing electrons

   BEFORE           AFTER
   ──────           ─────
     Fe      →     Fe²⁺  +  2e⁻
  (neutral)      (positive)  (released)

  Atom loses electrons → becomes more positive
  OIL: Oxidation Is Loss (of electrons)

  Examples:
    Fe   → Fe²⁺ + 2e⁻   (rust)
    Zn   → Zn²⁺ + 2e⁻   (battery anode)
   2Cl⁻  → Cl₂  + 2e⁻   (electrolysis)
```

**Key insight:** Oxidation doesn't require oxygen—it just means losing electrons. [[quick-context/rust|Rusting iron]], a [[quick-context/galvanic-cells-batteries|battery]] discharging, [[learning/notes/micro-context/push-pull-vs-open-drain|and]] chlorine forming during [[quick-context/electrolysis|electrolysis]] are all oxidation because electrons leave, regardless of [[learning/notes/quick-context/differential-pair|whether]] oxygen participates.
