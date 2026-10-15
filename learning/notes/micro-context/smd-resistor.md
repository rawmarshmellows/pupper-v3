---
term: SMD Resistor
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[learning/notes/quick-context/resistor]]

# SMD Resistor[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[quick-context/pcb-printed-circuit-board]] | [[quick-context/electric-current]] | [[learning/notes/small-context/pull-up-pull-down-resistors]]

**[[learning/notes/quick-context/capacitance|Definition]]:** Surface-mount resistors are tiny rectangular [[learning/notes/quick-context/tensor|components]] that limit [[learning/notes/quick-context/capacitance|current]] flow. [[learning/notes/quick-context/capacitance|The]] "0402" size ([[learning/notes/quick-context/meddpicc-qualification-framework|1]].0mm × [[learning/notes/quick-context/meddpicc-qualification-framework|0]].5mm) used in [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] Pupper [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|BOM]] is about the size of [[learning/notes/quick-context/anions-and-oxidation|a]] grain of sand. Values like "10kΩ" set [[learning/notes/quick-context/voltage|voltage]] dividers, pull-ups, current limits, [[learning/notes/micro-context/push-pull-vs-open-drain|and]] feedback networks throughout the circuit.

## How It Works

- A thin [[learning/notes/quick-context/capacitor|film]] [[learning/notes/micro-context/push-pull-vs-open-drain|or]] thick film of resistive material is deposited on a ceramic [[learning/notes/quick-context/flip-chip|substrate]], [[learning/notes/quick-context/breaking-elongation-rate|with]] metal terminations on each end for [[learning/notes/quick-context/soldering|soldering]].
- Current flowing through the resistive film converts electrical energy to heat according to $P = [[learning/notes/quick-context/anions-and-oxidation|I]]^2R$.
- The resistance value is set during manufacturing by the film's composition, thickness, and laser-trimmed geometry.

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

**Key insight:** The odd [[learning/notes/quick-context/fundamental-electronic-parts-index|resistor]] values (60.4kΩ, [[learning/notes/quick-context/similarity-transform|11]].5kΩ, 174kΩ) in your BOM are feedback resistors for the [[learning/notes/micro-context/buck-converter|buck converter]]—they set the exact output voltage through a [[learning/notes/quick-context/pwm-controller-circuit|voltage divider]] ratio.
