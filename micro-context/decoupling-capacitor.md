---
term: Decoupling Capacitor
created: 2026-01-27
---

# Decoupling Capacitor

> **See also:** [[quick-context/pcb-printed-circuit-board]] | [[quick-context/electric-current]]

**Definition:** Small capacitors (typically 100nF ceramic) placed near IC power pins to provide instant local charge when the chip switches states. They "decouple" the IC from the power supply by filtering high-frequency noise and supplying transient current faster than the distant power source can respond.

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
