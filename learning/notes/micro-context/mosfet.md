---
term: MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor)
created: 2026-02-25
updated: 2026-03-27
---

> **Related:** [[learning/notes/quick-context/transistor]] | [[learning/notes/quick-context/doped-silicon]] | [[learning/notes/quick-context/bjt]] | [[learning/notes/micro-context/buck-converter]] | [[learning/notes/quick-context/semiconductor-fabrication]]

# MOSFET

> **See also:** [[learning/notes/quick-context/transistor]]

**Definition:** The dominant [[learning/notes/quick-context/transistor|transistor]] type in modern electronics. A voltage-controlled switch where a thin oxide layer insulates the gate from the [[learning/notes/quick-context/doped-silicon|doped silicon]] channel, forming a capacitor—applying voltage creates an electric field that turns the channel on or off without the gate drawing current. NMOS and PMOS variants pair together in CMOS logic.

## How It Works

- Applying voltage to the gate creates an electric field through the oxide insulator, attracting charge carriers into the channel region.
- Above the threshold voltage ($V_{th}$), enough carriers accumulate to form a conductive channel between source and drain.
- Removing the gate voltage collapses the channel, turning the transistor off — no gate current flows because the oxide is an insulator.
- In CMOS logic, NMOS and PMOS transistors are paired so that one is always off, minimizing static power consumption.

```
NMOS cross-section:

          Gate
            │
     ┌──────┴──────┐
     │ Metal  Gate │
     ├─────────────┤  ← Oxide (SiO₂ or high-k)
  ┌──┴───┐     ┌───┴──┐
  │  N⁺  │  P  │  N⁺  │
  │Source │ ch. │Drain │
  └──────┴─────┴──────┘
     P-type substrate

 +V gate → field through oxide
 → channel conducts → current flows
```

**Key insight:** The gate is one plate of a capacitor—it switches by electric field, not current flow—which is why MOSFETs are far more power-efficient than [[learning/notes/quick-context/bjt|BJTs]] and dominate digital circuits with billions per chip.
