---
term: Clock Edge
created: 2026-01-26
---

# Clock Edge

> **See also:** [[quick-context/transistor-analog-to-digital]] | [[micro-context/clock-speed]]

**Definition:** The precise moment when a clock signal transitions between states—either rising (0→1) or falling (1→0). Digital circuits sample data only at clock edges, avoiding the "forbidden zone" where signals are mid-transition and invalid.

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
