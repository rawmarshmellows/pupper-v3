---
term: Diode Rectification (AC → DC)
created: 2026-02-07
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/buck-converter]] | [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]]

# Diode Rectification (AC → DC)

**[[learning/notes/quick-context/capacitance|Definition]]:** Using [[quick-context/diode|diodes]] as [[learning/notes/quick-context/ram-addressing-decoder|one]]-way valves to convert AC to DC. Since diodes [[learning/notes/quick-context/comparator-specification|only]] let [[learning/notes/quick-context/capacitance|current]] flow in one direction, they block or flip [[learning/notes/quick-context/capacitance|the]] negative portions of AC, producing output that's always positive.

## How It Works

- During the positive half of the AC cycle, the [[learning/notes/quick-context/diode|diode]] is forward-biased [[learning/notes/micro-context/push-pull-vs-open-drain|and]] passes current through to the load.
- During the negative half, the diode blocks current (reverse-biased), preventing reverse flow.
- The result is pulsating DC — all-positive but still bumpy with gaps where the negative half was removed.
- A smoothing [[learning/notes/quick-context/capacitor|capacitor]] fills in the gaps by storing [[learning/notes/quick-context/cations-and-reduction|charge]] during peaks and releasing it during dips, producing steady DC.

```
AC input               After diodes            + Capacitor

    /\      /\           /\  /\  /\
   /  \    /  \         /  \/  \/  \
──/────\──/────\──    ─/────────────\─      ════════════════
        \/      \/                           (smooth DC out)

 swings positive      all-positive now       fills the dips
 and negative         (still bumpy)          into steady DC
```

**Key insight:** Every phone charger and [[learning/notes/quick-context/d-flip-flop|power]] supply does this—diodes make the current all-positive, then a [[quick-context/capacitor|capacitor]] smooths [[learning/notes/micro-context/push-pull-vs-open-drain|out]] the bumps into steady DC.

> **See also:** [[quick-context/ac-to-dc-rectification|AC-to-DC Rectification (quick-context)]]
