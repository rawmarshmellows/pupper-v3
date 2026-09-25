---
term: Diode Rectification (AC → DC)
created: 2026-02-07
updated: 2026-03-27
---

# Diode Rectification (AC → DC)

**[[quick-context/capacitance|Definition]]:** Using [[quick-context/diode|diodes]] as one-way valves to convert AC to DC. Since diodes [[quick-context/comparator-specification|only]] let current flow in one direction, they block or flip the negative portions of AC, producing output that's always positive.

## How It Works

- During the positive half of the AC cycle, the diode is forward-biased [[micro-context/push-pull-vs-open-drain|and]] passes current through to the load.
- During the negative half, the diode blocks current (reverse-biased), preventing reverse flow.
- The result is pulsating DC — all-positive but still bumpy with gaps where the negative half was removed.
- A smoothing [[quick-context/capacitor|capacitor]] fills in the gaps by storing [[quick-context/cations-and-reduction|charge]] during peaks and releasing it during dips, producing steady DC.

```
AC input               After diodes            + Capacitor

    /\      /\           /\  /\  /\
   /  \    /  \         /  \/  \/  \
──/────\──/────\──    ─/────────────\─      ════════════════
        \/      \/                           (smooth DC out)

 swings positive      all-positive now       fills the dips
 and negative         (still bumpy)          into steady DC
```

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** Every phone charger and [[quick-context/d-flip-flop|power]] supply does this—diodes make the current all-positive, then a [[quick-context/capacitor|capacitor]] smooths out the bumps into steady DC.

> **Related:** [[micro-context/crystal-oscillator]] | [[quick-context/ac-to-dc-rectification]] | [[quick-context/bjt-specifications]] | [[quick-context/comparator-specification]] | [[quick-context/embedded-communication-protocols]]
