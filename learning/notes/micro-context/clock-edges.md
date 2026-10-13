---
term: Clock Edge
created: 2026-01-26
updated: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/clock-source]] | [[learning/notes/micro-context/clock-speed-vs-temperature]] | [[learning/notes/micro-context/clock-speed]] | [[learning/notes/quick-context/clock-sources-and-timing]] | [[learning/notes/micro-context/ceramic-resonator]]


# Clock Edge

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[quick-context/transistor-analog-to-digital]] | [[micro-context/clock-speed]] | [[quick-context/clock-sources-and-timing|Clock Sources and Timing]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** The precise moment [[learning/notes/quick-context/bare-minimal-data-storage-circuit|when]] a [[learning/notes/quick-context/switches-to-registers-storing-data|clock signal]] transitions between states—either rising (0→1) or falling (1→0). Digital circuits like [[quick-context/d-flip-flop|D flip-flops]] sample data [[learning/notes/quick-context/comparator-specification|only]] at clock edges, avoiding the "forbidden zone" where signals are mid-transition and invalid.

## How It Works

- A clock oscillator generates a continuous square wave alternating between high and low [[learning/notes/quick-context/voltage|voltage]] levels.
- On each transition (rising or falling edge), flip-flops and registers capture ("[[learning/notes/quick-context/d-flip-flop|latch]]") their input signals.
- Between edges, combinational logic computes new values that propagate and settle before the next edge arrives.
- This [[learning/notes/quick-context/switches-to-registers-storing-data|edge-triggered]] discipline ensures all [[learning/notes/quick-context/tensor|components]] read consistent, stable data [[learning/notes/quick-context/bare-minimal-data-storage-circuit|simultaneously]].

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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** Clock edges are why billions of imperfect analog transistors can coordinate as perfect digital switches—they all agree to only "look" at signals at the same precise moments, ignoring the messy analog transitions in between.
