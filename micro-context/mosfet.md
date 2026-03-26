---
term: MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor)
created: 2026-02-25
---

# MOSFET

> **See also:** [[quick-context/transistor]]

**Definition:** The dominant [[quick-context/transistor|transistor]] type in modern electronics. A voltage-controlled switch where a thin oxide layer insulates the gate from the [[quick-context/doped-silicon|doped silicon]] channel, forming a capacitor—applying voltage creates an electric field that turns the channel on or off without the gate drawing current. NMOS and PMOS variants pair together in CMOS logic.

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

**Key insight:** The gate is one plate of a capacitor—it switches by electric field, not current flow—which is why MOSFETs are far more power-efficient than [[quick-context/bjt|BJTs]] and dominate digital circuits with billions per chip.
