---
term: Thread Pitch (Screws)
created: 2026-05-04
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# Thread Pitch (Screws)

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] axial [[learning/notes/quick-context/embedded-communication-protocols|distance]] between [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] adjacent thread crests on a screw — i.e. how far the screw advances per [[learning/notes/quick-context/singular-value-decomposition|full]] turn. Metric specs it in millimeters (e.g. $M3 \times 0.5$ = 3 mm diameter, 0.5 mm [[learning/notes/quick-context/bga-ball-grid-array|pitch]]); imperial specs it as threads per inch (TPI, e.g. $\frac{1}{4}\[[learning/notes/quick-context/how-source-code-is-stored|text]]{-}20$ = 20 threads per inch).

## How It Works

- Threads are a helical ramp; [[learning/notes/quick-context/ram-addressing-decoder|one]] full [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|rotation]] moves the screw axially by [[learning/notes/quick-context/ram-addressing-decoder|exactly one]] pitch.
- **Coarse** pitch (large value, e.g. $M3 \times 0.5$, 1/4-20) installs [[learning/notes/quick-context/comparator|fast]] [[learning/notes/micro-context/push-pull-vs-open-drain|and]] tolerates dirty or damaged threads — used in softer [[learning/notes/quick-context/cnc-machining|materials]] and [[learning/notes/quick-context/singular-value-decomposition|general]] assembly.
- **Fine** pitch (small value, e.g. $M3 \times 0.35$, 1/4-28) gives more thread engagement per length, higher clamp force at a given torque, and resists vibration loosening — used in thin walls, precision adjustments, and aerospace.
- Pitch [[learning/notes/quick-context/ros2-architecture|must]] match between screw and tapped hole; mixing $M3 \times 0.5$ into an $M3 \times 0.35$ hole strips threads.

```
            pitch
          ←──────→
        ╱╲      ╱╲      ╱╲      ╱╲
       ╱  ╲    ╱  ╲    ╱  ╲    ╱  ╲
══════╱════╲══╱════╲══╱════╲══╱════╲══════  ← screw shaft axis
      ╲    ╱╲╱    ╲ ╱╲    ╱╲╱    ╱
       ╲  ╱  ╲    ╱  ╲    ╱  ╲  ╱
        ╲╱    ╲  ╱    ╲  ╱    ╲╱
                ╲╱      ╲╱

   one full turn  ──►  shaft advances by one pitch
```

**Key insight:** Pitch is *[[learning/notes/micro-context/can-bus-termination|not]]* thread depth or screw diameter — it's purely the spacing along the shaft. An $M3 \times 0.5$ and an $M3 \times 0.35$ look almost [[learning/notes/quick-context/ram-addressing-decoder|identical]] to the eye but are not interchangeable.
