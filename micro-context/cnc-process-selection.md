---
term: CNC Process Selection
created: 2026-01-27
---

# CNC Process Selection

> **See also:** [[micro-context/cnc-machining]] | [[micro-context/cnc-milling]] | [[micro-context/cnc-turning]] | [[micro-context/edm-machining]]

**Definition:** A decision framework for when to use CNC machining over other methods, and which CNC process to choose. CNC excels at tight tolerances, metal parts, and low-to-medium volumes where tooling costs for casting/molding aren't justified.

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
