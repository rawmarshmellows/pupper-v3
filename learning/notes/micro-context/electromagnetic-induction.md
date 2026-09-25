---
term: Electromagnetic Induction
created: 2026-02-08
updated: 2026-03-27
---

# Electromagnetic Induction

> **Related:** [[quick-context/coil-magnetic-field]] | [[quick-context/frequency-and-filtering]] | [[quick-context/impedance-and-reactance]] | [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]]

**[[quick-context/capacitance|Definition]]:** The phenomenon where a changing magnetic field through a conductor induces a [[quick-context/voltage|voltage]] (and thus [[quick-context/electric-current|current]] if the circuit is closed). Discovered by Faraday in 1831, this single principle generates 99%+ of grid electricity—every coal, gas, nuclear, hydro, and wind plant uses it.

## How It Works

- A changing magnetic [[quick-context/soldering|flux]] through a conductor loop induces an EMF (voltage) proportional to the rate of change ($EMF = -N \times d\Phi/dt$).
- In a [[quick-context/electricity-generation|generator]], rotating a coil in a magnetic field continuously changes the flux, producing AC voltage.
- In a transformer, AC current in one coil creates a changing magnetic field that induces voltage in a nearby second coil.
- The negative sign ([[quick-context/lenzs-law|Lenz's law]]) means the induced current always opposes the change that caused it.

```
FARADAY'S LAW
═══════════════════════════════════════════════

    EMF = -N × dΦ/dt

    N ═══════════ S     Coil rotates in
         ┌────┐         magnetic field
         │~~~~│ ←───────────┐
         └──┬─┘             │
            │            ROTATION
            ▼
       AC OUTPUT

    Changing flux → induced voltage → current
```

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** Motion creates electricity, and electricity creates motion—generators and motors are the same device run in opposite directions.
