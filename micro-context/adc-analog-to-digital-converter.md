---
term: ADC (Analog-to-Digital Converter)
created: 2026-01-27
---

# ADC (Analog-to-Digital Converter)

> **See also:** [[quick-context/transistor-analog-to-digital]] | [[quick-context/electric-current]]

**Definition:** A circuit that converts continuous analog voltage into discrete digital numbers. The ADS1110 in your Pupper is a 16-bit ADC, meaning it divides its input range into 65,536 levels—if measuring 0–3.3V, each step is ~50 microvolts. Used for precise measurements like battery voltage, current sensing, or analog sensor readings.

```
ANALOG TO DIGITAL CONVERSION:

  Analog input          ADC              Digital output
  (continuous)       (samples)           (discrete)
       │                 │                    │
   3.3V┤    ╭─╮         │                 1111111111111111
       │   ╱   ╲        │ 16-bit          (65535)
       │  ╱     ╲       │ resolution
       │ ╱       ╲      │                      ▪
       │╱         ╲     │                      ▪
   0V  ┼───────────────►│                 0000000000000000
       t               Sample              (0)
                       points

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
