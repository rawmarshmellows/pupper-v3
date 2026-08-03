---
term: Current Mirror
created: 2026-04-02
---
> **Related:** [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/quick-context/high-gain-amplifier-stage]] | [[learning/notes/micro-context/current-electrons-per-second]] | [[learning/notes/micro-context/current-inductor-capacitor-relationship]] | [[learning/notes/micro-context/input-bias-current]]

# Current Mirror

**Definition:** A circuit that copies a reference current from one transistor to another, producing a constant output current regardless of load conditions. It is the standard way to build on-chip current sources, including the [[micro-context/tail-current|tail current]] in [[learning/notes/quick-context/capacitance|differential pairs]].

## How It Works

- A reference current $I_{ref}$ (set by a resistor or upstream source) flows through a diode-connected [[micro-context/mosfet|MOSFET]] (gate tied to drain), forcing it to develop whatever $V_{gs}$ is needed to carry that current.
- A second matched transistor shares the same $V_{gs}$ (gates tied together), so it develops the same channel conditions and conducts the same current: $I_{out} \approx I_{ref}$.
- Because the output transistor operates in saturation, its drain current is nearly independent of drain voltage — giving high output impedance, which is what makes it a good [[learning/notes/quick-context/voltage-current-causality|current source]].
- Scaling the output transistor's $W/L$ ratio relative to the reference transistor scales the copied current proportionally: $I_{out} = I_{ref} \times (W/L)_{out} / (W/L)_{ref}$.

```
    I_ref                 I_out ≈ I_ref
  (from Vdd)              (to load)
      |                       |
      |  drain          drain |
      +--+                +---+
         |   shared gate  |
         +------- + ------+
         |        |       |
     M1 -+        |       +- M2
         |     gate tied   |
         |     to M1 drain |
        GND               GND
```

**Key insight:** The "mirror" isn't magic — it works because [[learning/notes/quick-context/differential-pair|matched transistors]] with identical $V_{gs}$ carry identical currents, so fixing one transistor's current automatically fixes the other's.
