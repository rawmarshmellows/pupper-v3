---
term: PWM (Pulse Width Modulation)
created: 2026-02-25
---

# PWM (Pulse Width Modulation)

**Definition:** A technique for controlling average power by rapidly switching a signal fully ON and fully OFF, varying the fraction of time spent ON (the duty cycle, $D = t_{on} / T$). The load sees the time-averaged voltage: $V_{avg} = V_{IN} \times D$. Used in [[micro-context/buck-converter|buck converters]] (the PWM signal drives the MOSFET gate), motor speed control, LED dimming, and [[micro-context/i2s-audio-amplifier|Class-D audio amplifiers]].

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

**Key insight:** PWM is a digital signal doing an analog job — by switching fast enough (kHz to MHz), the load's inertia (thermal, mechanical, or an [[quick-context/inductor|inductor]]/[[quick-context/capacitor|capacitor]] filter) smooths the pulses into a steady average, achieving precise analog control with minimal power loss — the switch is either fully ON (low resistance) or fully OFF (no current), unlike a linear regulator stuck in the lossy middle.
