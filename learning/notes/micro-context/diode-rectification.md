---
term: Diode Rectification (AC → DC)
created: 2026-02-07
updated: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/quick-context/ac-to-dc-rectification]] | [[learning/notes/quick-context/capacitor]] | [[learning/notes/quick-context/diode]]


# Diode Rectification (AC → DC)

**Definition:** Using [[quick-context/diode|diodes]] as one-way valves to convert AC to DC. Since diodes only let current flow in one direction, they block or flip the negative portions of AC, producing output that's always positive.

## How It Works

- During the positive half of the AC cycle, the [[learning/notes/quick-context/diode|diode]] is forward-biased and passes current through to the load.
- During the negative half, the diode blocks current (reverse-biased), preventing reverse flow.
- The result is pulsating DC — all-positive but still bumpy with gaps where the negative half was removed.
- A smoothing [[learning/notes/quick-context/capacitor|capacitor]] fills in the gaps by storing charge during peaks and releasing it during dips, producing steady DC.

```
AC input               After diodes            + Capacitor

    /\      /\           /\  /\  /\
   /  \    /  \         /  \/  \/  \
──/────\──/────\──    ─/────────────\─      ════════════════
        \/      \/                           (smooth DC out)

 swings positive      all-positive now       fills the dips
 and negative         (still bumpy)          into steady DC
```

**Key insight:** Every phone charger and power supply does this—diodes make the current all-positive, then a [[quick-context/capacitor|capacitor]] smooths out the bumps into steady DC.

> **See also:** [[quick-context/ac-to-dc-rectification|AC-to-DC Rectification (quick-context)]]
