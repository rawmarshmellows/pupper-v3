---
term: Buck Converter
created: 2026-01-27
---

# Buck Converter

> **See also:** [[quick-context/electric-current]] | [[quick-context/parallel-vs-series-voltage]]

**Definition:** A switching power supply that efficiently steps down voltage (e.g., 12V battery → 5V for logic). Unlike linear regulators that waste excess voltage as heat, buck converters use rapid switching (100kHz–2MHz) and an inductor to achieve 85–95% efficiency. The TPS54561 in your Pupper converts battery voltage to 5V at up to 5A.

```
BUCK CONVERTER OPERATION:

  VIN (12V)                          VOUT (5V)
     │                                  │
     ▼         L (inductor)             ▼
  ┌──┴──┐    ┌───ŻŻŻŻŻ───┐    ┌────────┴────────┐
  │ SW  │────┤           ├────┤    LOAD         │
  │(FET)│    └───_____───┘    │  (MCU, sensors) │
  └──┬──┘         │           └────────┬────────┘
     │      D (diode)                  │
     └────────┴────────────────────────┘
              GND

  Switching waveform:
  ┌──┐  ┌──┐  ┌──┐     SW ON: energy into inductor
  │  │  │  │  │  │     SW OFF: inductor releases to load
  ┘  └──┘  └──┘  └──   Duty cycle sets VOUT/VIN ratio

  VOUT ≈ VIN × (ton / tperiod)
```

**Key insight:** The inductor is the magic—it stores energy magnetically when the switch is ON and releases it when OFF, smoothing the choppy switched voltage into steady DC without the heat waste of linear regulation.
