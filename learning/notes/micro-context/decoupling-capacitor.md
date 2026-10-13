---
term: Decoupling Capacitor
created: 2026-01-27
updated: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/current-inductor-capacitor-relationship]] | [[learning/notes/quick-context/capacitor]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/buck-converter]] | [[learning/notes/micro-context/diode-rectification]]


# Decoupling Capacitor

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[quick-context/pcb-printed-circuit-board]] | [[quick-context/electric-current]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** Small [[learning/notes/quick-context/voltage|capacitors]] (typically 100nF ceramic) placed near IC [[learning/notes/quick-context/d-flip-flop|power]] pins to provide instant local [[learning/notes/quick-context/cations-and-reduction|charge]] [[learning/notes/quick-context/bare-minimal-data-storage-circuit|when]] the chip switches states. They "decouple" the IC from the power supply by filtering high-frequency noise and supplying transient [[learning/notes/quick-context/capacitance|current]] faster than the distant power [[learning/notes/quick-context/differential-pair|source]] can respond.

## How It Works

- When an IC switches states, it demands a sudden spike of current from the [[learning/notes/quick-context/schematic-reading|power rail]].
- The distant power supply can't respond instantly because PCB [[learning/notes/quick-context/pcb-printed-circuit-board|trace]] inductance limits current slew rate.
- A small [[learning/notes/quick-context/capacitor|capacitor]] placed right next to the IC's power pin stores local charge and releases it instantly during the demand spike.
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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** Every IC needs decoupling capacitors placed as close as possible to its power pins—the PCB trace inductance between capacitor and chip determines how well high-frequency noise is filtered.
