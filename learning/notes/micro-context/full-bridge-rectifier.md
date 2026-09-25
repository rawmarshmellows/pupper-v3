---
term: Full-Wave Bridge Rectifier
created: 2026-02-08
updated: 2026-03-27
---

# Full-Wave Bridge Rectifier

> **Related:** [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]] | [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/ads1110-battery-adc]] | [[micro-context/bjt-mosfet-igbt]]

**[[quick-context/capacitance|Definition]]:** A circuit of four [[quick-context/diode|diodes]] arranged in a diamond that converts AC to pulsating DC by steering [[quick-context/electric-current|current]] through the load in the same direction during [[quick-context/bjt-specifications|both]] halves of the AC cycle.

## How It Works

- Four diodes are arranged in a diamond (bridge) configuration with AC input connected across [[micro-context/schmitt-trigger-hysteresis|two]] opposite corners [[micro-context/push-pull-vs-open-drain|and]] DC output taken from the other two.
- During the positive AC half-cycle, two diodes (D1, D4) conduct, steering current through the load in the forward direction.
- During the negative AC half-cycle, the other two diodes (D2, D3) conduct, again steering current through the load in the same forward direction.
- The result is full-wave rectified DC — both halves of the AC cycle contribute, [[quick-context/camera-fundamentals|doubling]] the ripple frequency compared to [[quick-context/ac-to-dc-rectification|half-wave]].

```
Diode = one-way valve:  ──▶|──  (current flows this way →)

THE BRIDGE (diamond shape):

                (+) OUTPUT
                    │
               ┌────┴────┐
               │         │
            ──▶|D1    D2|▶──
           │                 │
      AC ~~●                 ●~~ AC
           │                 │
            ──▶|D3    D4|▶──
               │         │
               └────┬────┘
                    │
                (−) OUTPUT


WHEN AC SWINGS + ON LEFT:        WHEN AC SWINGS − ON LEFT:

    (+)             (−)              (−)             (+)
     ●               ●                ●               ●
     │               │                │               │
     └──▶D1    D4▶───┘                └──▶D2    D3▶───┘
           ↓    ↑                           ↓    ↑
          LOAD                             LOAD
         (+ to −)                         (+ to −)

     ════════════                    ════════════
     SAME DIRECTION THROUGH LOAD BOTH TIMES!
```

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** Two diodes always conduct at once, so the output is ~1.4V below the AC peak (2 × 0.7V drop)—this is why [[quick-context/diode|Schottky]] bridges are used in low-[[quick-context/voltage|voltage]] supplies.

---
> **See also:** [[quick-context/ac-to-dc-rectification|AC-to-DC Rectification (quick-context)]]

> **Human notes:**
> - ElectroBOOM explains it well: https://www.youtube.com/watch?v=Fwj_d3uO5g8
