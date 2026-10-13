---
term: Offset Voltage Drift (TCV_OS)
created: 2026-06-07
---
> **Related:** [[learning/notes/micro-context/input-offset-voltage]] | [[learning/notes/micro-context/open-loop-voltage-gain]] | [[learning/notes/micro-context/output-voltage-swing]] | [[learning/notes/micro-context/common-mode-rejection-ratio]] | [[learning/notes/micro-context/current-mirror]]


# Offset Voltage Drift ($TCV_{OS}$)

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[quick-context/comparator-specification]] | [[micro-context/input-offset-voltage]] | [[quick-context/differential-pair]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** The rate at which a [[learning/notes/quick-context/comparator|comparator]]'s or op-amp's [[micro-context/input-offset-voltage|input offset voltage]] changes with temperature, expressed in µV/°C. It tells you how much the offset wanders as the chip heats or cools.

## How It Works

- Offset comes from [[quick-context/differential-pair|differential-pair]] mismatch, and that mismatch isn't constant — it shifts as temperature changes the transistors' characteristics.
- Multiply drift by [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] temperature span to get the added offset error: e.g. 1 µV/°C over a 60°C swing adds 60 µV.
- Drift can worsen at higher supply ([[learning/notes/quick-context/comparator-specification|LMC7211-N]]: 1.0 µV/°C at 5 V → [[learning/notes/quick-context/comparator-specification|4.0 µV/°C at 15 V]]), so read the table for *your* rail.
- [[learning/notes/quick-context/similarity-transform|Total]] worst-case offset $\approx$ room-temperature offset limit $+$ $TCV_{OS} \times \Delta T$.

```
 V_OS
 (mV) |                            /  slope = TCV_OS (uV/degC)
      |                         /
      |                      /
      |                   /
      |                /
      +--------------------------------> Temperature (degC)
     -40            25              +85

   Total error = offset(25 degC) + TCV_OS x (delta T)
```

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** A part with tiny room-temperature offset can still miss its [[learning/notes/micro-context/capacitive-voltage-sensing|threshold]] in the field if its drift is high — total [[learning/notes/quick-context/rc-oscillator|accuracy]] is the 25°C offset *plus* drift over your whole operating range, not the 25°C number alone.
