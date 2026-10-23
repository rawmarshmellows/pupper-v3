---
term: I2S Audio Amplifier
created: 2026-01-27
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# I2S Audio Amplifier

> **See also:** [[quick-context/electric-current]] | [[quick-context/pcb-printed-circuit-board]] | [[quick-context/pupper-bom-control-board]]

**[[learning/notes/quick-context/capacitance|Definition]]:** A chip that receives digital audio over I2S (Inter-IC Sound) protocol [[learning/notes/micro-context/push-pull-vs-open-drain|and]] directly drives a speaker—combining DAC and amplifier in [[learning/notes/quick-context/ram-addressing-decoder|one]] [[learning/notes/quick-context/silicon-die|package]]. [[learning/notes/quick-context/capacitance|The]] MAX98357A in [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] Pupper takes [[learning/notes/quick-context/data-bus-and-arbitration|serial]] digital audio from the MCU and outputs up to 3.2W to a speaker, enabling the robot to make sounds without external audio [[learning/notes/quick-context/code-to-gates-and-bootstrapping|hardware]].

## How It Works

- The MCU transmits audio samples as a serial bit stream over three I2S lines: bit [[learning/notes/quick-context/bare-minimal-data-storage-circuit|clock]] (BCLK), left/right select (LRCLK), and data (DIN).
- The MAX98357A's internal DAC reconstructs the analog waveform from the digital samples.
- A Class-D amplifier stage converts the analog [[learning/notes/quick-context/comparator|signal]] into high-frequency PWM that drives the speaker coil.
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
