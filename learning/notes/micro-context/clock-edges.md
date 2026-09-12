---
term: Clock Edge
created: 2026-01-26
updated: 2026-03-27
---
> **Related:** [[learning/notes/quick-context/clock-sources-and-timing]] | [[learning/notes/quick-context/bare-minimal-data-storage-circuit]] | [[learning/notes/quick-context/transistor]] | [[learning/notes/quick-context/switches-to-registers-storing-data]] | [[learning/notes/micro-context/clock-source]]

# Clock Edge

> **See also:** [[learning/notes/quick-context/transistor-analog-to-digital]] | [[learning/notes/micro-context/clock-speed]] | [[learning/notes/quick-context/clock-sources-and-timing|Clock Sources and Timing]]

**Definition:** The precise moment when a clock signal transitions between states—either rising (0→1) or falling (1→0). Digital circuits like [[learning/notes/quick-context/d-flip-flop|D flip-flops]] sample data only at clock edges, avoiding the "forbidden zone" where signals are mid-transition and invalid.

## How It Works

- A clock oscillator generates a continuous square wave alternating between high and low [[learning/notes/quick-context/voltage|voltage]] levels.
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
