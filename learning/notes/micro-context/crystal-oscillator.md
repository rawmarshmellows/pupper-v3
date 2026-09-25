---
term: Crystal Oscillator
created: 2026-03-27
---

# Crystal Oscillator

> **Related:** [[micro-context/diode-rectification]] | [[quick-context/ac-to-dc-rectification]] | [[quick-context/bjt-specifications]] | [[quick-context/comparator-specification]] | [[quick-context/embedded-communication-protocols]]

**[[quick-context/capacitance|Definition]]:** A circuit that uses a quartz crystal's piezoelectric resonance to generate a precise, stable frequency — the universal [[micro-context/clock-source|clock source]] for CPUs. Every digital processor, from a laptop's Intel chip to a Pupper's [[micro-context/stm32-microcontroller|STM32]], derives its [[micro-context/clock-speed|clock]] from some [[quick-context/mcp6541-as-lmc7211-replacement|form]] of crystal or resonator oscillator, with PLLs multiplying the base frequency up to operating [[quick-context/embedded-communication-protocols|speed]]. Far more accurate than [[quick-context/rc-oscillator|RC oscillators]] (±20 ppm vs. ±1-5%), but requires an external [[quick-context/pcb-assembly-files-bom-cpl|component]].

## How It Works

- An amplifier circuit drives a thin quartz crystal, which mechanically vibrates at its natural resonant frequency (determined by its cut [[micro-context/push-pull-vs-open-drain|and]] thickness).
- The crystal's vibration generates an extremely stable electrical signal — quartz holds frequency to ±20 ppm (±0.002%), far [[quick-context/comparator-specification|better]] than any electronic-only oscillator.
- This low base frequency (typically 8–40 MHz) feeds into one or more PLLs that multiply it up to the CPU's operating frequency (e.g., 8 MHz $\times$ 22.5 = 180 MHz on STM32, or 38.4 MHz $\rightarrow$ PLL $\rightarrow$ 100 MHz BCLK $\rightarrow$ PLL $\times$ 50 = 5 GHz on a modern desktop CPU).

```
QUARTZ CRYSTAL → OSCILLATOR CIRCUIT → PLL → CPU CLOCK
════════════════════════════════════════════════════════

        ┌─────────┐      ┌─────┐      ┌─────┐
        │ Quartz  │      │ Osc │      │ PLL │
        │ Crystal ├─────►│ Amp ├─────►│×N/÷M├──► CPU Clock
        │ (XTAL)  │      │     │      │     │
        └─────────┘      └─────┘      └─────┘
         8-100 MHz      stable ref    GHz range
        mechanical       signal       operating
        vibration                     frequency

  Desktop: 38 MHz crystal → PLL → 100 MHz BCLK → PLL → 5 GHz
  MCU:       8 MHz crystal → PLL → 180 MHz
```

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** No CPU runs directly [[quick-context/bjt-specifications|off]] a crystal — the crystal just provides an accurate *[[quick-context/comparator|reference]]* frequency that PLLs multiply up. The crystal's job is stability, [[micro-context/can-bus-termination|not]] speed; the PLL's job is speed, not stability.
