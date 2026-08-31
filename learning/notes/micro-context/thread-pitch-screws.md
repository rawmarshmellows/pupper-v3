---
term: Thread Pitch (Screws)
created: 2026-05-04
---

# Thread Pitch (Screws)

> **Related:** [[learning/notes/quick-context/bjt-specifications]] | [[learning/notes/quick-context/camera-fundamentals]] | [[learning/notes/quick-context/comparator-specification]] | [[learning/notes/quick-context/pcb-layers]] | [[learning/notes/quick-context/bambu-p2s-print-quality]]
**Definition:** The axial distance between two adjacent thread crests on a screw — i.e. how far the screw advances per full turn. Metric specs it in millimeters (e.g. $M3 \times 0.5$ = 3 mm diameter, 0.5 mm pitch); imperial specs it as threads per inch (TPI, e.g. $\frac{1}{4}\text{-}20$ = 20 threads per inch).

## How It Works

- Threads are a helical ramp; one full rotation moves the screw axially by exactly one pitch.
- **Coarse** pitch (large value, e.g. $M3 \times 0.5$, 1/4-20) installs fast and tolerates dirty or damaged threads — used in softer materials and general assembly.
- **Fine** pitch (small value, e.g. $M3 \times 0.35$, 1/4-28) gives more thread engagement per length, higher clamp force at a given torque, and resists vibration loosening — used in thin walls, precision adjustments, and aerospace.
- Pitch must match between screw and tapped hole; mixing $M3 \times 0.5$ into an $M3 \times 0.35$ hole strips threads.

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

**Key insight:** Pitch is *not* thread depth or screw diameter — it's purely the spacing along the shaft. An $M3 \times 0.5$ and an $M3 \times 0.35$ look almost identical to the eye but are not interchangeable.
