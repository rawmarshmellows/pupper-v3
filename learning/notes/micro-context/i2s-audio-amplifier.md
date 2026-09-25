---
term: I2S Audio Amplifier
created: 2026-01-27
updated: 2026-03-27
---

# I2S Audio Amplifier

> **Related:** [[micro-context/i2s]] | [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]] | [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/ads1110-battery-adc]]

**[[quick-context/capacitance|Definition]]:** A chip that receives digital audio over [[micro-context/i2s|I2S (Inter-IC Sound)]] protocol [[micro-context/push-pull-vs-open-drain|and]] directly drives a speaker—combining DAC and amplifier in one [[quick-context/silicon-die|package]]. The MAX98357A in [[quick-context/mcp6541-as-lmc7211-replacement|your]] Pupper takes serial digital audio from the MCU and outputs up to 3.2W to a speaker, enabling the robot to make sounds without external audio hardware.

## How It Works

- The MCU transmits audio samples as a serial bit stream over three I2S lines: bit [[quick-context/bare-minimal-data-storage-circuit|clock]] (BCLK), left/right select (LRCLK), and data (DIN).
- The MAX98357A's internal DAC reconstructs the analog waveform from the digital samples.
- A Class-D amplifier stage converts the analog [[quick-context/comparator|signal]] into high-frequency PWM that drives the speaker coil.
- The speaker's mechanical inertia acts as a natural low-pass filter, reproducing the original audio waveform.

```
I2S AUDIO SIGNAL CHAIN:

  MCU                   MAX98357A              Speaker
  ┌───┐                ┌─────────┐            ┌─────┐
  │   │──BCLK─────────►│         │            │ ))) │
  │   │──LRCLK────────►│ DAC +   │───Class D──►│     │
  │   │──DIN──────────►│ AMP     │  PWM audio │ ((( │
  └───┘                └─────────┘            └─────┘
    │                       │
  Digital               Analog power
  serial data           to speaker

  I2S Timing:
  BCLK:  ┌┐┌┐┌┐┌┐┌┐┌┐┌┐┌┐┌┐┌┐┌┐┌┐  (bit clock)
  LRCLK: ────────┐       ┌────────  (left/right select)
                 └───────┘
  DIN:   ◄──L channel──►◄──R channel──►  (audio data)
```

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** I2S amplifiers eliminate the analog audio path entirely—digital data goes straight to the speaker driver, avoiding noise pickup and simplifying PCB layout compared to traditional analog audio chains.
