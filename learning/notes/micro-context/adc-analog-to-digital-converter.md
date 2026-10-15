---
term: ADC (Analog-to-Digital Converter)
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[learning/notes/quick-context/transistor-analog-to-digital]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/buck-converter]]

# ADC (Analog-to-Digital Converter)

> **[[learning/notes/quick-context/tensile-strength-materials|]]See also:** [[quick-context/transistor-analog-to-digital]] | [[quick-context/electric-current]] | [[quick-context/pupper-bom-control-board]] | [[learning/notes/small-context/pull-up-pull-down-resistors]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] circuit that converts continuous analog [[learning/notes/quick-context/voltage|voltage]] into [[learning/notes/quick-context/how-passive-and-discrete-components-are-made|discrete]] digital numbers. [[learning/notes/quick-context/capacitance|The]] ADS1110 in [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] Pupper is a 16-bit ADC, meaning it divides its input range into 65[[learning/notes/quick-context/how-passive-and-discrete-components-are-made|,]]536 levels—if measuring [[learning/notes/quick-context/meddpicc-qualification-framework|0]]–[[learning/notes/quick-context/meddpicc-qualification-framework|3]].3V, each step is ~50 microvolts. Used for precise measurements like battery voltage, [[learning/notes/quick-context/capacitance|current]] sensing, [[learning/notes/micro-context/push-pull-vs-open-drain|or]] analog sensor readings.

## How It Works

- The ADC samples the analog input voltage at regular intervals determined by the sample rate.
- Each sample is compared against an internal [[learning/notes/quick-context/comparator|reference]] voltage [[learning/notes/micro-context/push-pull-vs-open-drain|and]] quantized to the nearest digital level ([[learning/notes/quick-context/bjt-specifications|e]].[[learning/notes/quick-context/cations-and-reduction|g]]., [[learning/notes/quick-context/ram-addressing-decoder|one]] of 65,536 levels for 16-bit).
- The resulting binary number is stored in a register and made available to the MCU [[learning/notes/quick-context/metal-interconnect-layers|via]] a [[learning/notes/quick-context/data-bus-and-arbitration|bus]] interface ([[learning/notes/micro-context/i2c|I2C]], [[learning/notes/micro-context/spi|SPI]], or internal peripheral).
- Higher bit [[learning/notes/quick-context/semiconductor-fabrication|resolution]] means finer voltage steps, but [[learning/notes/quick-context/thermal-noise-electronics|noise floor]] and reference stability ultimately limit practical [[learning/notes/quick-context/rc-oscillator|accuracy]].

```
ANALOG TO DIGITAL CONVERSION:

  Analog input          ADC              Digital output
  (continuous)       (samples)           (discrete)
       │                 │                    │
   3.3V┤   /\           │                 1111111111111111
       │  /  \    /     │ 16-bit          (65535)
       │ /    \  /      │ resolution
       │/      \/       │                      :
   0V  ┼───────────────►│                      :
       t               Sample             0000000000000000
                       points              (0)

  Resolution comparison:
  ┌──────────┬─────────┬──────────────────┐
  │ Bits     │ Levels  │ 3.3V resolution  │
  ├──────────┼─────────┼──────────────────┤
  │ 8-bit    │ 256     │ 12.9 mV/step     │
  │ 12-bit   │ 4,096   │ 0.8 mV/step      │
  │ 16-bit   │ 65,536  │ 0.05 mV/step     │
  └──────────┴─────────┴──────────────────┘
```

**Key insight:** More bits doesn't always mean more accuracy—noise floor, reference voltage stability, and sampling rate often matter more than raw resolution for real-world measurements.
