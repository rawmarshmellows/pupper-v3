---
term: Electromagnetic Induction
created: 2026-02-08
updated: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/anode]] | [[learning/notes/micro-context/cathode]] | [[learning/notes/micro-context/coulomb-history]] | [[learning/notes/micro-context/current-electrons-per-second]] | [[learning/notes/micro-context/reverse-and-forward-bias]]


# Electromagnetic Induction

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[quick-context/electromagnetism]] | [[quick-context/electricity-generation]] | [[quick-context/inductor]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** The phenomenon where a changing magnetic field through a conductor induces a [[learning/notes/quick-context/voltage|voltage]] (and thus [[quick-context/electric-current|current]] if the circuit is closed). Discovered by Faraday in 1831, this single principle generates 99%+ of grid electricity—every coal, gas, nuclear, hydro, and wind plant uses it.

## How It Works

- A changing magnetic [[learning/notes/quick-context/soldering|flux]] through a conductor loop induces an EMF (voltage) proportional to the rate of change ($EMF = -N \times d\Phi/dt$).
- In a [[learning/notes/quick-context/electricity-generation|generator]], rotating a coil in a magnetic field continuously changes the flux, producing AC voltage.
- In a transformer, AC [[learning/notes/quick-context/capacitance|current]] in one coil creates a changing magnetic field that induces voltage in a nearby second coil.
- The negative sign ([[learning/notes/quick-context/lenzs-law|Lenz's law]]) means the induced current always opposes the change that caused it.

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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** Motion creates electricity, and electricity creates motion—generators and motors are the same device run in opposite directions.
