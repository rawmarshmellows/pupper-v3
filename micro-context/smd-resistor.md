---
term: SMD Resistor
created: 2026-01-27
---

# SMD Resistor

> **See also:** [[quick-context/pcb-printed-circuit-board]] | [[quick-context/electric-current]]

**Definition:** Surface-mount resistors are tiny rectangular components that limit current flow. The "0402" size (1.0mm × 0.5mm) used in your Pupper BOM is about the size of a grain of sand. Values like "10kΩ" set voltage dividers, pull-ups, current limits, and feedback networks throughout the circuit.

```
SMD RESISTOR SIZES (to scale):

  0402     0603      0805      1206
  ┌─┐      ┌──┐      ┌───┐     ┌────┐
  └─┘      └──┘      └───┘     └────┘
  1.0mm    1.6mm     2.0mm     3.2mm
  (grain   (sesame   (rice     (easily
  of sand)  seed)    grain)    hand-solderable)

  COMMON USES IN YOUR BOM:
  ┌────────────┬─────────┬─────────────────────────┐
  │ Value      │ Qty     │ Typical use             │
  ├────────────┼─────────┼─────────────────────────┤
  │ 120Ω       │ 4       │ CAN bus termination     │
  │ 10kΩ       │ 3       │ Pull-up/pull-down       │
  │ 2.2kΩ      │ 4       │ I2C pull-ups            │
  │ 60.4kΩ etc │ various │ Voltage dividers/       │
  │            │         │ feedback networks       │
  └────────────┴─────────┴─────────────────────────┘
```

**Key insight:** The odd resistor values (60.4kΩ, 11.5kΩ, 174kΩ) in your BOM are feedback resistors for the buck converter—they set the exact output voltage through a voltage divider ratio.
