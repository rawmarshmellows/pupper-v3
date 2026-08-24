---
term: SRAM (Static Random-Access Memory)
created: 2026-04-07
---
> **Related:** [[learning/notes/micro-context/mosfet]] | [[learning/notes/quick-context/capacitor]] | [[learning/notes/quick-context/transistor]] | [[learning/notes/quick-context/voltage]] | [[learning/notes/quick-context/physics-of-writing-data-to-memory]]

# SRAM (Static Random-Access Memory)

**Definition:** A volatile memory technology that stores each bit using six cross-coupled [[learning/notes/micro-context/mosfet|MOSFETs]] arranged as two inverters in a feedback loop. "Static" means the data stays stable as long as power is on — no refresh needed, unlike [[learning/notes/quick-context/physics-of-writing-data-to-memory|DRAM's leaking capacitors]].

## How It Works

- Two CMOS inverters are wired output-to-input in a loop, creating two stable states: if Q = HIGH then Q' = LOW, which drives Q back to HIGH (self-reinforcing).
- Two access transistors connect the cell to bitlines; the wordline turns them on during reads/writes.
- To write, the bitline is driven to the desired voltage and the wordline is pulsed — the external driver overwhelms the cell's internal state, flipping it in <1 ns.
- No charge transfer through oxide barriers (unlike flash) and no capacitor leakage (unlike DRAM), so writes are unlimited and data is stable without refresh.

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

**Key insight:** SRAM is the fastest memory type (<1 ns read/write) but the least dense (6 transistors per bit), which is why it's used only where speed matters most — L1/L2/L3 cache and register files — while cheaper, denser DRAM handles main memory.
