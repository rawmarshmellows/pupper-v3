---
term: Anode
created: 2026-02-25
updated: 2026-03-27
---

# Anode

> **See also:** [[quick-context/electrodes]]

**[[quick-context/capacitance|Definition]]:** The [[quick-context/cations-and-reduction|electrode]] where [[quick-context/anions-and-oxidation|oxidation]] occurs — species lose [[quick-context/anions-and-oxidation|electrons]] here, and those electrons flow [[micro-context/push-pull-vs-open-drain|out]] through the external circuit. In [[quick-context/electrolysis|electrolysis]] the anode is positive (+); in [[quick-context/galvanic-cells-batteries|batteries]] it's negative (−). The name comes from Greek *anodos* ("way up").

## How It Works

- At the anode, chemical species lose electrons ([[micro-context/oxidation|oxidation]]) — these electrons flow out through the external circuit to do useful work.
- In electrolysis, the external [[quick-context/d-flip-flop|power]] supply pulls electrons away from the anode, making it positive (+).
- In a battery, the anode material spontaneously oxidizes, pushing electrons out — making it the negative (−) [[quick-context/from-vacuum-tubes-to-coding-on-screens|terminal]] from the external circuit's perspective.

```
  ELECTROLYSIS                    BATTERY
  (energy IN)                     (energy OUT)

  ANODE (+)    CATHODE (-)    ANODE (-)    CATHODE (+)
    │              │            │              │
    │  ┌───────┐   │            │  ┌───────┐   │
    │  │       │   │            │  │       │   │
    ▼  │ e⁻ ──►├───┘            └──┤◄── e⁻ │   ▼
  Ox   │       │  Red          Ox  │       │  Red
       └───────┘                   └───────┘
    electrons OUT              electrons OUT
    from anode                 from anode

  BOTH: oxidation at anode, reduction at cathode
  FLIPPED: which terminal is + vs −
```

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** "Anode" doesn't mean "positive electrode" — it means "where oxidation happens." The polarity flips between electrolysis (+) and batteries (−), but oxidation at the anode is always the same.
