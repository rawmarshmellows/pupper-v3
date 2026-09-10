---
term: CNC Process Selection
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[learning/notes/quick-context/cnc-machining]]

# CNC Process Selection

> **See also:** [[learning/notes/quick-context/cnc-machining]] (full treatment) | [[learning/notes/micro-context/cnc-milling]] | [[learning/notes/micro-context/cnc-turning]] | [[learning/notes/micro-context/edm-machining]]

**Definition:** A decision framework for when to use CNC machining over other methods, and which CNC process to choose. CNC excels at tight tolerances, metal parts, and low-to-medium volumes where tooling costs for casting/molding aren't justified.

## How It Works

- Evaluate part geometry: cylindrical parts favor turning, prismatic/complex shapes favor milling, hardened metals with sharp internal corners favor EDM.
- Consider volume: CNC is cost-effective for 1–1000 parts; injection molding or casting wins at 10,000+.
- Check tolerance requirements: CNC achieves ±0.001" routinely, which 3D printing and casting generally cannot match.

```
1. SHOULD YOU USE CNC AT ALL?

  Need tight tolerances (±0.001")?     ──► YES → CNC
  Metal part with full strength?       ──► YES → CNC
  Low volume (1-1000 parts)?           ──► YES → CNC
  Complex internals, no tool access?   ──► NO  → 3D print or casting
  High volume (10,000+)?               ──► NO  → Injection molding/casting

2. WHICH CNC PROCESS?

  Cylindrical?        Prismatic/complex?      Hard metal, sharp corners?
       │                     │                         │
       ▼                     ▼                         ▼
   TURNING              MILLING                      EDM
```

**Key insight:** CNC is the default for precision metal parts in low volumes—only consider alternatives when you need internal cavities (3D print), high volumes (molding), or can sacrifice precision (casting).
