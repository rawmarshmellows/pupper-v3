---
term: ADS1110 (Battery Voltage ADC)
created: 2026-02-25
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/buck-converter]] | [[learning/notes/micro-context/capacitive-voltage-sensing]] | [[learning/notes/micro-context/input-offset-voltage]] | [[learning/notes/micro-context/offset-voltage-drift]] | [[learning/notes/micro-context/open-loop-voltage-gain]]

# ADS1110 (Battery Voltage ADC)

> **See also:** [[micro-context/adc-analog-to-digital-converter|ADC fundamentals]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] [[learning/notes/quick-context/pupper-bom-control-board|ADS1110A0IDBVR]] (U16) is a delta-sigma [[micro-context/adc-analog-to-digital-converter|ADC]] from Texas Instruments in a [[learning/notes/quick-context/common-ic-packages|SOT-23]]-6 [[learning/notes/quick-context/silicon-die|package]] with an [[micro-context/i2c|I2C]] interface, internal 2.048V [[learning/notes/quick-context/comparator|reference]], [[learning/notes/micro-context/push-pull-vs-open-drain|and]] programmable [[learning/notes/quick-context/semiconductor-fabrication|resolution]]: 16-bit at 15 SPS, down to 12-bit at 240 SPS. On the [[quick-context/pupper-bom-control-board|Pupper control board]], it reads battery [[learning/notes/quick-context/voltage|voltage]] through a [[quick-context/resistor|voltage divider]] (scaling ~7-24V down to the ADC's input range) so the STM32 [[learning/notes/quick-context/embedded-communication-protocols|can]] warn of low battery.

## How It Works

- A [[learning/notes/quick-context/fundamental-electronic-parts-index|resistor]] [[learning/notes/quick-context/pwm-controller-circuit|voltage divider]] scales the battery voltage (7–24V) down to the ADC's 0–2.048V input range.
- The ADS1110's delta-sigma converter oversamples the input and digitally [[learning/notes/quick-context/pupper-lab7-vision-tracking|filters]] it, trading [[learning/notes/quick-context/embedded-communication-protocols|speed]] for high resolution (16-bit at 15 SPS).
- The STM32 reads the digital result over [[learning/notes/micro-context/i2c|I2C]] ([[learning/notes/quick-context/how-source-code-is-stored|address]] 0x48) and multiplies by the divider ratio to recover the true battery voltage.

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

**Key insight:** Delta-sigma ADCs trade speed for resolution — the ADS1110 gives 16-bit at 15 SPS or 12-bit at 240 SPS. Battery voltage changes over seconds, so even 15 SPS is overkill, making this the ideal architecture: [[learning/notes/quick-context/singular-value-decomposition|full]] 16-bit precision in a 6-pin package with no external reference needed.
