---
term: Offset Voltage Drift (TCV_OS)
created: 2026-06-07
---
> **Related:** [[micro-context/input-offset-voltage|Input Offset Voltage ($V_{OS}$)]] | [[micro-context/ads1110-battery-adc|ADS1110 (Battery Voltage ADC)]] | [[micro-context/capacitive-voltage-sensing]] | [[micro-context/open-loop-voltage-gain|Open-Loop Voltage Gain ($A_V$)]] | [[micro-context/output-voltage-swing|Output Voltage Swing ($V_{OH}$ / $V_{OL}$)]]

# Offset Voltage Drift ($TCV_{OS}$)

> **See also:** [[quick-context/comparator-specification]] | [[micro-context/input-offset-voltage]] | [[quick-context/differential-pair]]

**Definition:** The rate at which a [[quick-context/comparator|comparator]]'s or [[quick-context/op-amp|op-amp]]'s [[micro-context/input-offset-voltage|input offset voltage]] changes with temperature, expressed in µV/°C. It tells you how much the offset wanders as the chip heats or cools.

## How It Works

- Offset comes from [[quick-context/differential-pair|differential-pair]] mismatch, and that mismatch isn't constant — it shifts as temperature changes the transistors' characteristics.
- Multiply drift by your temperature span to get the added offset error: e.g. 1 µV/°C over a 60°C swing adds 60 µV.
- Drift can worsen at higher supply (LMC7211-N: 1.0 µV/°C at 5 V → 4.0 µV/°C at 15 V), so read the table for *your* rail.
- Total worst-case offset $\approx$ room-temperature offset limit $+$ $TCV_{OS} \times \Delta T$.

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

**Key insight:** A part with tiny room-temperature offset can still miss its threshold in the field if its drift is high — total accuracy is the 25°C offset *plus* drift over your whole operating range, not the 25°C number alone.
