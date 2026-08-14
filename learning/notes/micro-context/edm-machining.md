---
term: EDM Machining
created: 2026-01-27
updated: 2026-03-27
---
> **Related:** [[quick-context/electrodes]] | [[quick-context/electrolysis]] | [[quick-context/voltage]]

# EDM Machining (Electrical Discharge Machining)

> **See also:** [[quick-context/cnc-machining]] (full treatment) | [[quick-context/electrolysis]] | [[quick-context/electrodes]]

**Definition:** A subtractive manufacturing process that removes metal by creating rapid electrical sparks between an electrode and the workpiece, vaporizing tiny amounts of material without mechanical contact. Ideal for cutting hard metals and complex shapes that conventional tools cannot machine.

## How It Works

- A shaped electrode is brought close to the conductive workpiece, separated by a thin gap filled with dielectric fluid.
- High-voltage pulses ionize the fluid, creating brief electrical sparks that vaporize tiny craters in the workpiece surface.
- The dielectric fluid flushes away debris and re-insulates the gap between discharges.
- The electrode slowly advances as material is removed, reproducing its shape as a cavity in the workpiece.

```
      Electrode (tool)
            │
            ▼
      ┌─────────┐
      │ ▓▓▓▓▓▓▓ │
      └────┬────┘
           │
     ⚡⚡⚡⚡⚡⚡⚡  ← Spark gap (~0.01-0.5mm)
           │        filled with dielectric fluid
     ┌─────┴─────┐
     │░░░░░░░░░░░│
     │░░ WORK ░░░│  ← Material vaporized
     │░░ PIECE ░░│    spark by spark
     │░░░░░░░░░░░│
     └───────────┘
```

**Key insight:** Because EDM uses electrical erosion rather than mechanical force, it can cut any conductive material regardless of hardness - hardened steel is just as easy to machine as soft aluminum.
