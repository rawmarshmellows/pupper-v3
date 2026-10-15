---
term: BJT vs MOSFET vs IGBT
created: 2026-06-02
---

> **Related:** [[learning/notes/micro-context/mosfet]] | [[learning/notes/quick-context/bjt-specifications]] | [[learning/notes/quick-context/bjt]]

# BJT vs MOSFET vs IGBT[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[learning/notes/quick-context/bjt]] | [[learning/notes/micro-context/mosfet]] | [[learning/notes/quick-context/transistor]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] three main [[learning/notes/quick-context/d-flip-flop|power]]-[[learning/notes/quick-context/silicon-die|transistor]] families used as electronic switches [[learning/notes/micro-context/push-pull-vs-open-drain|and]] amplifiers. [[learning/notes/quick-context/anions-and-oxidation|A]] [[learning/notes/quick-context/bjt|BJT]] is [[learning/notes/quick-context/capacitance|current]]-controlled, a [[learning/notes/micro-context/mosfet|MOSFET]] is [[learning/notes/quick-context/voltage|voltage]]-controlled and [[learning/notes/quick-context/comparator|fast]], and an IGBT is a hybrid—a [[learning/notes/micro-context/mosfet|MOSFET]]-style insulated [[learning/notes/quick-context/transistor|gate]] driving a BJT-style high-power output.

## How It Works

- **BJT:** a small base current controls a much larger collector→emitter current (bipolar conduction); the base draws continuous current and switches at moderate [[learning/notes/quick-context/embedded-communication-protocols|speed]].
- **MOSFET:** an insulated gate sets up an [[learning/notes/quick-context/voltage-current-causality|electric field]] [[learning/notes/quick-context/breaking-elongation-rate|with]] near-[[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|zero]] gate current, giving the fastest switching and lowest loss at low–mid voltage—dominates logic and [[learning/notes/quick-context/switches-to-registers-storing-data|switch]]-mode supplies.
- **IGBT:** the insulated gate (easy voltage drive, like a MOSFET) feeds an internal BJT output, so it conducts like a BJT—low loss at high voltage, but slower than a MOSFET.
- **Pick by voltage/frequency:** MOSFET for low-voltage high-frequency, IGBT for high-voltage high-power (motor drives, EV/solar inverters, welders), BJT for analog and small-[[learning/notes/quick-context/comparator|signal]].

```
              BJT            MOSFET        IGBT
              ──────────────────────────────────────────────
 Driven by    current        voltage       voltage
 Speed        slow           fastest       medium
 Voltage      low–mid        low–mid       high
              (legacy)       (<~250 V)     (>~400 V)
 Terminals    B, C, E        G, D, S       G, C, E

 IGBT internals = insulated gate + bipolar output:

   Gate ─┤│ MOSFET ├─► base of internal BJT ─► C↔E conducts
         (voltage in)      (low-loss, high-voltage current)
```

**Key insight:** An IGBT is literally a MOSFET front-end bolted to a BJT back-end—drive it like a MOSFET (cheap voltage gate) but it conducts like a BJT (big volts and amps)—which is [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] IGBTs rule high-power conversion above ~400 [[learning/notes/quick-context/capacitor|V]] while MOSFETs own the low-voltage, high-speed domain.

> **Video:** https://youtu.be/EddYiCeL16Q
