---
term: Thermal Runaway
created: 2026-01-26
updated: 2026-03-27
---

# Thermal Runaway

> **See also:** [[quick-context/transistor-analog-to-digital]] | [[quick-context/thermal-noise-electronics]] | [[micro-context/clock-speed-vs-temperature]]

**[[quick-context/capacitance|Definition]]:** A destructive feedback loop where heat increases [[quick-context/transistor-analog-to-digital|leakage current]], which generates more heat, which increases leakage further—until the chip throttles, shuts down, or permanently damages itself.

## How It Works

- Transistor [[quick-context/transistor-analog-to-digital|leakage current]] grows exponentially with temperature due to increased carrier energy in the [[quick-context/transistor|silicon]].
- More leakage means more [[quick-context/d-flip-flop|power]] dissipated as heat, even [[quick-context/bare-minimal-data-storage-circuit|when]] the chip is idle.
- The extra heat further raises temperature, creating a [[quick-context/pupper-lab7-vision-tracking|positive feedback]] loop that accelerates until cooling can no longer [[quick-context/existing-account-management-playbook|keep]] up.
- Protection circuits detect the rising temperature [[micro-context/push-pull-vs-open-drain|and]] throttle [[micro-context/clock-speed|clock speed]] or shut down the chip before [[quick-context/bambu-p2s-print-quality|permanent]] damage occurs.

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

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** The "off" transistors that [[quick-context/transistor-analog-to-digital|leak current even when supposedly off]] leak MORE when hot—this is why cooling isn't optional and why chips have thermal limits baked into [[quick-context/firmware|firmware]].
