---
term: SRAM (Static Random-Access Memory)
created: 2026-04-07
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# SRAM (Static Random-Access Memory)

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] [[learning/notes/quick-context/tensile-strength-materials|]]volatile [[learning/notes/quick-context/bare-minimal-data-storage-circuit|memory]] technology that stores each bit using six cross-coupled [[learning/notes/micro-context/mosfet|MOSFETs]] arranged as [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] inverters in a feedback loop. "Static" means [[learning/notes/quick-context/capacitance|the]] data stays stable as long as [[learning/notes/quick-context/d-flip-flop|power]] is on — [[learning/notes/micro-context/capacitive-voltage-sensing|no]] refresh needed, unlike [[learning/notes/quick-context/physics-of-writing-data-to-memory|DRAM's leaking capacitors]].

## How It Works

- Two CMOS inverters are wired output-to-input in a loop, creating two stable states: if [[learning/notes/quick-context/capacitor|Q]] = HIGH then Q' = LOW, which drives Q back to HIGH (self-reinforcing).
- Two access transistors connect the cell to bitlines; the [[learning/notes/quick-context/physics-of-writing-data-to-memory|wordline]] turns them on during reads/writes.
- To [[learning/notes/quick-context/d-flip-flop|write]], the [[learning/notes/quick-context/physics-of-writing-data-to-memory|bitline]] is driven to the desired [[learning/notes/quick-context/voltage|voltage]] [[learning/notes/micro-context/push-pull-vs-open-drain|and]] the wordline is pulsed — the external driver overwhelms the cell's internal state, flipping it in <[[learning/notes/quick-context/meddpicc-qualification-framework|1]] ns.
- No [[learning/notes/quick-context/capacitive-sensing-measurement|charge transfer]] through oxide barriers (unlike flash) and no [[learning/notes/quick-context/capacitor|capacitor]] leakage (unlike [[learning/notes/quick-context/ram-addressing-decoder|DRAM]]), so writes are unlimited and data is stable without refresh.

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

**Key insight:** [[learning/notes/quick-context/ram-addressing-decoder|SRAM]] is the fastest memory [[learning/notes/quick-context/bjt-specifications|type]] (<1 ns read/write) but the least dense (6 transistors per bit), which is [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] it's used [[learning/notes/quick-context/comparator-specification|only]] where [[learning/notes/quick-context/embedded-communication-protocols|speed]] matters most — [[learning/notes/micro-context/buck-converter|L1]]/L2/L3 cache and register files — while cheaper, denser DRAM handles main memory.
