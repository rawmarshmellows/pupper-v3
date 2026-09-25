---
term: Clock Edge
created: 2026-01-26
updated: 2026-03-27
---

# Clock Edge

> **Related:** [[micro-context/clock-source]] | [[micro-context/clock-speed]] | [[micro-context/clock-speed-vs-temperature]] | [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]]

**[[quick-context/capacitance|Definition]]:** The precise moment when a clock [[quick-context/comparator|signal]] transitions between states—either rising (0→1) or falling (1→0). Digital circuits like [[quick-context/d-flip-flop|D flip-flops]] sample data [[quick-context/comparator-specification|only]] at clock edges, avoiding the "forbidden zone" where signals are mid-transition [[micro-context/push-pull-vs-open-drain|and]] invalid.

## How It Works

- A clock oscillator generates a continuous square wave alternating between high and low [[quick-context/voltage|voltage]] levels.
- On each transition (rising or falling edge), flip-flops and registers capture ("latch") their input signals.
- Between edges, combinational logic computes new values that propagate and settle before the next edge arrives.
- This edge-triggered discipline ensures all components read consistent, stable data [[quick-context/bare-minimal-data-storage-circuit|simultaneously]].

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

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** Clock edges are why billions of imperfect analog transistors [[quick-context/embedded-communication-protocols|can]] coordinate as perfect digital switches—they all agree to only "look" at signals at the same precise moments, ignoring the messy analog transitions in between.
