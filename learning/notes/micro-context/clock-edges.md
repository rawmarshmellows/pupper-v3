---
term: Clock Edge
created: 2026-01-26
updated: 2026-03-27
---

# Clock Edge

> **Related:** [[quick-context/raspberry-pi-ai-hat]] | [[quick-context/bare-minimal-data-storage-circuit]] | [[micro-context/clock-source]] | [[quick-context/clock-sources-and-timing]] | [[micro-context/clock-speed]]
> **See also:** [[quick-context/transistor-analog-to-digital]] | [[micro-context/clock-speed]] | [[quick-context/clock-sources-and-timing|Clock Sources and Timing]]

**Definition:** The precise moment when a clock signal transitions between states—either rising (0→1) or falling (1→0). Digital circuits like [[quick-context/d-flip-flop|D flip-flops]] sample data only at clock edges, avoiding the "forbidden zone" where signals are mid-transition and invalid.

## How It Works

- A clock oscillator generates a continuous square wave alternating between high and low [[quick-context/voltage|voltage]] levels.
- On each transition (rising or falling edge), flip-flops and registers capture ("latch") their input signals.
- Between edges, combinational logic computes new values that propagate and settle before the next edge arrives.
- This edge-triggered discipline ensures all components read consistent, stable data simultaneously.

```
Clock:  ───┐   ┌───┐   ┌───┐   ┌───
           └───┘   └───┘   └───┘
           ↑   ↑
           │   │
       RISING  FALLING
        EDGE    EDGE

     Sample data at edges → signals have settled
     Ignore data between edges → may be invalid
```

**Key insight:** Clock edges are why billions of imperfect analog transistors can coordinate as perfect digital switches—they all agree to only "look" at signals at the same precise moments, ignoring the messy analog transitions in between.
