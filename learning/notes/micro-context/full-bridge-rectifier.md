---
term: Full-Wave Bridge Rectifier
created: 2026-02-08
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# Full-Wave Bridge Rectifier[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[quick-context/diode]] | [[micro-context/diode-rectification]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] circuit of [[learning/notes/quick-context/ram-addressing-decoder|four]] [[quick-context/diode|diodes]] arranged in a diamond that converts AC to pulsating [[learning/notes/micro-context/mosfet|DC]] by steering [[quick-context/electric-current|current]] through [[learning/notes/quick-context/capacitance|the]] load in the same direction during [[learning/notes/quick-context/bjt-specifications|both]] halves of the AC cycle.

## How It Works

- Four diodes are arranged in a diamond (bridge) configuration [[learning/notes/quick-context/breaking-elongation-rate|with]] AC input connected across [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] opposite corners [[learning/notes/micro-context/push-pull-vs-open-drain|and]] DC output taken from the other two.
- During the positive AC half-cycle, two diodes ([[learning/notes/micro-context/buck-converter|D1]], D4) conduct, steering [[learning/notes/quick-context/capacitance|current]] through the load in the forward direction.
- During the negative AC half-cycle, the other two diodes (D2, D3) conduct, again steering current through the load in the same forward direction.
- The result is [[learning/notes/quick-context/singular-value-decomposition|full]]-wave rectified DC — both halves of the AC cycle contribute, [[learning/notes/quick-context/camera-fundamentals|doubling]] the ripple frequency compared to [[learning/notes/quick-context/ac-to-dc-rectification|half-wave]].

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

**Key insight:** Two diodes always conduct at once, so the output is ~[[learning/notes/quick-context/meddpicc-qualification-framework|1]].4V below the AC peak ([[learning/notes/quick-context/meddpicc-qualification-framework|2]] × [[learning/notes/quick-context/meddpicc-qualification-framework|0]].7V drop)—this is [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] [[learning/notes/quick-context/diode|Schottky]] bridges are used in low-[[learning/notes/quick-context/voltage|voltage]] supplies.

---
> **See also:** [[quick-context/ac-to-dc-rectification|AC-to-DC Rectification (quick-context)]]

> **Human notes:**
> - ElectroBOOM explains it well: https://www.youtube.com/watch?[[learning/notes/quick-context/capacitor|v]]=Fwj_d3uO5g8
