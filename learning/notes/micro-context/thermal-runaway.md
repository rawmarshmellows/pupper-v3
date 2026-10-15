---
term: Thermal Runaway
created: 2026-01-26
updated: 2026-03-27
---

> **Related:** [[learning/notes/quick-context/thermal-noise-electronics]]

# Thermal Runaway[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[quick-context/transistor-analog-to-digital]] | [[quick-context/thermal-noise-electronics]] | [[micro-context/clock-speed-vs-temperature]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] destructive feedback loop where heat increases [[quick-context/transistor-analog-to-digital|leakage current]], which generates more heat, which increases leakage further—until [[learning/notes/quick-context/capacitance|the]] chip throttles, shuts down, [[learning/notes/micro-context/push-pull-vs-open-drain|or]] permanently damages itself.

## How It Works

- [[learning/notes/quick-context/silicon-die|Transistor]] [[learning/notes/quick-context/transistor-analog-to-digital|leakage current]] grows exponentially [[learning/notes/quick-context/breaking-elongation-rate|with]] temperature due to increased carrier energy in the [[learning/notes/quick-context/transistor|silicon]].
- More leakage means more [[learning/notes/quick-context/d-flip-flop|power]] dissipated as heat, even [[learning/notes/quick-context/bare-minimal-data-storage-circuit|when]] the chip is idle.
- The extra heat further raises temperature, creating a [[learning/notes/quick-context/pupper-lab7-vision-tracking|positive feedback]] loop that accelerates until cooling [[learning/notes/quick-context/embedded-communication-protocols|can]] [[learning/notes/micro-context/capacitive-voltage-sensing|no]] longer [[learning/notes/quick-context/existing-account-management-playbook|keep]] up.
- Protection circuits detect the rising temperature [[learning/notes/micro-context/push-pull-vs-open-drain|and]] throttle [[learning/notes/micro-context/clock-speed|clock speed]] or shut down the chip before [[learning/notes/quick-context/bambu-p2s-print-quality|permanent]] damage occurs.

```
THE THERMAL RUNAWAY FEEDBACK LOOP
════════════════════════════════════════════════════════════════

     ┌──────────────────────────────────────────────┐
     │                                              │
     ▼                                              │
  TEMPERATURE ──► LEAKAGE CURRENT ──► MORE HEAT ───┘
     rises         increases              generated
                   (I ∝ e^(T))            (P = I×V)

  Leakage grows EXPONENTIALLY with temperature!
  At some point, idle power alone exceeds cooling capacity.

  PROTECTION MECHANISMS:
  ├── Thermal throttling: reduce clock speed
  ├── Emergency shutdown: cut power before damage
  └── Thermal design power (TDP): design limit
```

**Key insight:** The "[[learning/notes/quick-context/bjt-specifications|off]]" transistors that [[quick-context/transistor-analog-to-digital|leak current even when supposedly off]] leak MORE when [[learning/notes/quick-context/bjt-specifications|hot]]—this is [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] cooling isn't optional and why chips have thermal limits baked into [[learning/notes/quick-context/firmware|firmware]].
