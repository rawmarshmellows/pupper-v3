---
term: SMD Resistor
created: 2026-01-27
updated: 2026-03-27
---

# SMD Resistor

> **Related:** [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]] | [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/ads1110-battery-adc]] | [[micro-context/bjt-mosfet-igbt]]

**[[quick-context/capacitance|Definition]]:** Surface-mount resistors are tiny rectangular components that limit current flow. The "0402" size (1.0mm × 0.5mm) used in [[quick-context/mcp6541-as-lmc7211-replacement|your]] Pupper [[quick-context/pcb-assembly-files-bom-cpl|BOM]] is about the size of a grain of sand. Values like "10kΩ" set [[quick-context/voltage|voltage]] dividers, pull-ups, current limits, [[micro-context/push-pull-vs-open-drain|and]] feedback networks throughout the circuit.

## How It Works

- A thin [[quick-context/capacitor|film]] or thick film of resistive material is deposited on a ceramic [[quick-context/flip-chip|substrate]], with metal terminations on each end for [[quick-context/soldering|soldering]].
- Current flowing through the resistive film converts electrical energy to heat according to $P = I^2R$.
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

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** The odd resistor values (60.4kΩ, 11.5kΩ, 174kΩ) in your BOM are feedback resistors for the [[micro-context/buck-converter|buck converter]]—they set the exact output voltage through a [[quick-context/pwm-controller-circuit|voltage divider]] ratio.
