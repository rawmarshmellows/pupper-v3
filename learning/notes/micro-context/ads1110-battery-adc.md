---
term: ADS1110 (Battery Voltage ADC)
created: 2026-02-25
updated: 2026-03-27
---

# ADS1110 (Battery Voltage ADC)

> **See also:** [[micro-context/adc-analog-to-digital-converter|ADC fundamentals]]

**Definition:** The ADS1110A0IDBVR (U16) is a delta-sigma [[micro-context/adc-analog-to-digital-converter|ADC]] from Texas Instruments in a SOT-23-6 package with an [[micro-context/i2c|I2C]] interface, internal 2.048V reference, and programmable resolution: 16-bit at 15 SPS, down to 12-bit at 240 SPS. On the [[quick-context/pupper-bom-control-board|Pupper control board]], it reads battery [[quick-context/voltage|voltage]] through a [[quick-context/resistor|voltage divider]] (scaling ~7-24V down to the ADC's input range) so the STM32 can warn of low battery.

## How It Works

- A [[quick-context/resistor|resistor]] voltage divider scales the battery voltage (7–24V) down to the ADC's 0–2.048V input range.
- The ADS1110's delta-sigma converter oversamples the input and digitally filters it, trading speed for high resolution (16-bit at 15 SPS).
- The STM32 reads the digital result over I2C (address 0x48) and multiplies by the divider ratio to recover the true battery voltage.

```
 VBAT (7-24V)
   │
  ┌┴┐ R_top
  └┬┘
   ├────────┐
  ┌┴┐       │ VIN+    SOT-23-6
  └┬┘       │      ┌───────────┐       ┌─────────┐
   │ R_bot  └─────►│  ADS1110  ├─SDA──►│         │
  GND              │  ΔΣ ADC   ├─SCL──►│  STM32  │
             VIN-─►│           │       │  (U1)   │
              GND  └───────────┘       └─────────┘
                     I2C addr: 0x48

 Divider scales VBAT into 0–2.048V range.
 15 SPS (16-bit) is plenty fast for battery monitoring.
```

**Key insight:** Delta-sigma ADCs trade speed for resolution — the ADS1110 gives 16-bit at 15 SPS or 12-bit at 240 SPS. Battery voltage changes over seconds, so even 15 SPS is overkill, making this the ideal architecture: full 16-bit precision in a 6-pin package with no external reference needed.
