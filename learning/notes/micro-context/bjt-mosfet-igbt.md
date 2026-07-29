---
term: BJT vs MOSFET vs IGBT
created: 2026-06-02
---

# BJT vs MOSFET vs IGBT

> **See also:** [[learning/notes/quick-context/bjt]] | [[learning/notes/micro-context/mosfet]] | [[learning/notes/quick-context/transistor]]

**Definition:** The three main power-[[quick-context/transistor|transistor]] families used as electronic switches and amplifiers. A [[learning/notes/quick-context/bjt|BJT]] is current-controlled, a [[learning/notes/micro-context/mosfet|MOSFET]] is [[quick-context/voltage|voltage]]-controlled and fast, and an IGBT is a hybrid—a [[micro-context/mosfet|MOSFET]]-style insulated gate driving a [[quick-context/bjt|BJT]]-style high-power output.

## How It Works

- **BJT:** a small base current controls a much larger collector→emitter current (bipolar conduction); the base draws continuous current and switches at moderate speed.
- **MOSFET:** an insulated gate sets up an electric field with near-zero gate current, giving the fastest switching and lowest loss at low–mid voltage—dominates logic and switch-mode supplies.
- **IGBT:** the insulated gate (easy voltage drive, like a MOSFET) feeds an internal BJT output, so it conducts like a BJT—low loss at high voltage, but slower than a MOSFET.
- **Pick by voltage/frequency:** MOSFET for low-voltage high-frequency, IGBT for high-voltage high-power (motor drives, EV/solar inverters, welders), BJT for analog and small-signal.

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

**Key insight:** An IGBT is literally a MOSFET front-end bolted to a BJT back-end—drive it like a MOSFET (cheap voltage gate) but it conducts like a BJT (big volts and amps)—which is why IGBTs rule high-power conversion above ~400 V while MOSFETs own the low-voltage, high-speed domain.

> **Video:** https://youtu.be/EddYiCeL16Q
