---
term: Electromigration
created: 2026-01-26
---

# Electromigration

> **See also:** [[quick-context/metal-interconnect-layers]] | [[quick-context/semiconductor-fabrication]]

**Definition:** Electromigration is the gradual movement of metal atoms in a wire caused by momentum transfer from flowing electrons. At high current densities, electrons "push" atoms in the direction of current flow, creating voids (breaks) at one end and hillocks (bulges) at the other, eventually causing wire failure.

```
CURRENT FLOWING THROUGH A THIN WIRE
═══════════════════════════════════════════════════════════════

Before (healthy wire):
    ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
    ──────────────────────────────────────────────►  e⁻ flow
    Metal atoms evenly distributed

After (electromigration damage):
    ○ ○ ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●▓▓
    ──────────────────────────────────────────────►  e⁻ flow
    │                                              │
    VOID (atoms left)                    HILLOCK (atoms piled up)
    → wire breaks here                   → may short to neighbor
```

**Key insight:** Electromigration sets the maximum current a chip's wires can carry—not thermal limits, but atomic-scale erosion. This is why shrinking wires is doubly hard: thinner wires have both higher resistance *and* lower current-carrying capacity before atoms start migrating.
