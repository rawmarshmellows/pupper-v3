---
term: I2S Audio Amplifier
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[micro-context/can-bus-termination]] | [[micro-context/can-bus-transceiver]] | [[micro-context/i2c]] | [[micro-context/i2s]] | [[micro-context/push-pull-vs-open-drain]]

# I2S Audio Amplifier

> **See also:** [[quick-context/electric-current]] | [[quick-context/pcb-printed-circuit-board]] | [[quick-context/pupper-bom-control-board]]

**Definition:** A chip that receives digital audio over I2S (Inter-IC Sound) protocol and directly drives a speaker—combining DAC and amplifier in one package. The MAX98357A in your Pupper takes serial digital audio from the MCU and outputs up to 3.2W to a speaker, enabling the robot to make sounds without external audio hardware.

## How It Works

- The MCU transmits audio samples as a serial bit stream over three I2S lines: bit clock (BCLK), left/right select (LRCLK), and data (DIN).
- The MAX98357A's internal DAC reconstructs the analog waveform from the digital samples.
- A Class-D amplifier stage converts the analog signal into high-frequency [[micro-context/pwm-pulse-width-modulation|PWM]] that drives the speaker coil.
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

**Key insight:** I2S amplifiers eliminate the analog audio path entirely—digital data goes straight to the speaker driver, avoiding noise pickup and simplifying PCB layout compared to traditional analog audio chains.
