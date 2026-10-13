---
term: PWM (Pulse Width Modulation)
created: 2026-02-25
updated: 2026-03-27
---
> **Related:** [[learning/notes/quick-context/pwm-controller-circuit]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/buck-converter]] | [[learning/notes/micro-context/current-inductor-capacitor-relationship]] | [[learning/notes/micro-context/decoupling-capacitor]]


# PWM (Pulse Width Modulation)

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** A technique for controlling average [[learning/notes/quick-context/d-flip-flop|power]] by rapidly switching a [[learning/notes/quick-context/comparator|signal]] fully ON and fully OFF, varying the fraction of time spent ON (the duty cycle, $D = t_{on} / T$). The load sees the time-averaged [[learning/notes/quick-context/voltage|voltage]]: $V_{avg} = V_{IN} \times D$. Used in [[micro-context/buck-converter|buck converters]] (the PWM signal drives the [[learning/notes/micro-context/mosfet|MOSFET]] [[learning/notes/quick-context/transistor|gate]]), motor speed control, LED dimming, and [[micro-context/i2s-audio-amplifier|Class-D audio amplifiers]]. https://www.youtube.com/watch?v=nXFoVSN3u-E

## How It Works

- A timer peripheral generates a square wave at a fixed frequency, toggling an output pin between fully ON (rail voltage) and fully OFF (ground).
- The duty cycle (fraction of time spent ON) is set by a compare register — changing this value changes the average output voltage.
- The load's natural inertia (mechanical, thermal, or an LC filter) smooths the rapid switching into a steady average.
- Because the [[learning/notes/quick-context/switches-to-registers-storing-data|switch]] is always fully ON or fully OFF, very little power is wasted in the switch itself (unlike a [[learning/notes/quick-context/power-watts-joules|linear regulator]] in the resistive middle).

```
        ton
    ├────────┤
    ┌────────┐                  ┌────────┐
    │        │                  │        │
    │   ON   │      OFF         │   ON   │
 ───┘        └──────────────────┘        └───
    ├───────────────────────────┤
               T (period)

 Duty cycle D = ton / T

 Average output = VIN × D
   D = 25%:  █░░░  →  3V from 12V
   D = 50%:  ██░░  →  6V from 12V
   D = 75%:  ███░  →  9V from 12V
```

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** PWM is a digital signal doing an analog job — by switching [[learning/notes/quick-context/comparator|fast]] enough (kHz to MHz), the load's inertia (thermal, mechanical, or an [[quick-context/inductor|inductor]]/[[quick-context/capacitor|capacitor]] filter) smooths the pulses into a steady average, achieving precise analog control with minimal power loss — the switch is either fully ON (low resistance) or fully OFF (no [[learning/notes/quick-context/capacitance|current]]), unlike a linear regulator stuck in the lossy middle. For how the PWM signal is actually generated inside a [[learning/notes/micro-context/buck-converter|buck converter]] IC ([[learning/notes/quick-context/pwm-controller-circuit|sawtooth oscillator]] + [[learning/notes/quick-context/pwm-controller-circuit|error amplifier]] + [[learning/notes/quick-context/comparator|comparator]] feedback loop), see [[quick-context/pwm-controller-circuit]].
