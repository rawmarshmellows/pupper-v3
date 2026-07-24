---
term: Decoupling Capacitor
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[quick-context/capacitor|Capacitor]] | [[micro-context/power-supply-rejection-ratio|Power-Supply Rejection Ratio]] | [[quick-context/capacitance|Capacitance]] | [[quick-context/voltage|Voltage]] | [[quick-context/electric-current|Electric Current]]

# Decoupling Capacitor

> **See also:** [[quick-context/pcb-printed-circuit-board]] | [[quick-context/electric-current]]

**Definition:** Small capacitors (typically 100nF ceramic) placed near IC power pins to provide instant local charge when the chip switches states. They "decouple" the IC from the power supply by filtering high-frequency noise and supplying transient current faster than the distant power source can respond.

## How It Works

- When an IC switches states, it demands a sudden spike of current from the power rail.
- The distant power supply can't respond instantly because PCB trace inductance limits current slew rate.
- A small [[quick-context/capacitor|capacitor]] placed right next to the IC's power pin stores local charge and releases it instantly during the demand spike.
- The capacitor then slowly recharges from the power supply, ready for the next switching event.

```
WHY DECOUPLING IS NEEDED:

  Without decoupling:          With decoupling:
  ┌─────┐                      ┌─────┐
  │ IC  │◄── long trace ──PSU  │ IC  │◄─┬─ long trace ──PSU
  └─────┘    (inductance)      └─────┘  │
     │                            │    ═══ 100nF
     └── voltage sags when       │     │   (local charge)
         IC switches rapidly     └─────┴── stable voltage

  Current demand spike:
       │
  IC   │  ┌──┐     Without cap: PSU can't respond fast enough
  needs│  │  │                   → voltage drops → glitches
       └──┘  └──

       Decoupling cap supplies instant current locally
       then refills slowly from PSU
```

**Key insight:** Every IC needs decoupling capacitors placed as close as possible to its power pins—the PCB trace inductance between capacitor and chip determines how well high-frequency noise is filtered.
