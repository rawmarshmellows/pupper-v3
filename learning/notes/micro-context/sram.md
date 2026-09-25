---
term: SRAM (Static Random-Access Memory)
created: 2026-04-07
---

> **Related:** [[micro-context/eeprom]] | [[micro-context/microcontroller]] | [[micro-context/stm32-microcontroller]] | [[quick-context/physics-of-writing-data-to-memory]] | [[micro-context/4-wire-kelvin-measurement]]

# SRAM (Static Random-Access Memory)

**[[quick-context/capacitance|Definition]]:** A volatile memory technology that stores each bit using six cross-coupled [[learning/notes/micro-context/mosfet|MOSFETs]] arranged as two inverters in a feedback loop. "Static" means the data stays stable as long as [[quick-context/d-flip-flop|power]] is on — no refresh needed, unlike [[learning/notes/quick-context/physics-of-writing-data-to-memory|DRAM's leaking capacitors]].

## How It Works

- Two CMOS inverters are wired output-to-input in a loop, creating two stable states: if Q = HIGH then Q' = LOW, which drives Q back to HIGH (self-reinforcing).
- Two access transistors connect the cell to bitlines; the [[quick-context/physics-of-writing-data-to-memory|wordline]] turns them on during reads/writes.
- To write, the bitline is driven to the desired [[quick-context/voltage|voltage]] [[micro-context/push-pull-vs-open-drain|and]] the wordline is pulsed — the external driver overwhelms the cell's internal state, flipping it in <1 ns.
- No [[quick-context/capacitive-sensing-measurement|charge transfer]] through oxide barriers (unlike flash) and no [[quick-context/capacitor|capacitor]] leakage (unlike [[quick-context/ram-addressing-decoder|DRAM]]), so writes are unlimited and data is stable without refresh.

```
        Vdd ────┬────────────┬──── Vdd
                │            │
             ┌──┴──┐      ┌──┴──┐
             │PMOS │      │PMOS │
             └──┬──┘      └──┬──┘
    Q ──────────┼─────┐┌─────┼────────── Q'
                │     ││     │
             ┌──┴──┐  ││  ┌──┴──┐
             │NMOS │  ││  │NMOS │
             └──┬──┘  ││  └──┬──┘
                │     ││     │
        GND ────┴─────┘└─────┴──── GND
              INV A          INV B
         (output → B input, B output → A input)
```

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** SRAM is the fastest memory [[quick-context/bjt-specifications|type]] (<1 ns read/write) but the least dense (6 transistors per bit), which is why it's used [[quick-context/comparator-specification|only]] where [[quick-context/embedded-communication-protocols|speed]] matters most — L1/L2/L3 cache and register files — while cheaper, denser DRAM handles main memory.
