---
term: Diode Rectification (AC → DC)
created: 2026-02-07
---

# Diode Rectification (AC → DC)

**Definition:** Using [[quick-context/diode|diodes]] as one-way valves to convert AC to DC. Since diodes only let current flow in one direction, they block or flip the negative portions of AC, producing output that's always positive.

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
