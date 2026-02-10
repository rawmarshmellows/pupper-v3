---
term: I2S Audio Amplifier
created: 2026-01-27
---

# I2S Audio Amplifier

> **See also:** [[quick-context/electric-current]] | [[quick-context/pcb-printed-circuit-board]]

**Definition:** A chip that receives digital audio over I2S (Inter-IC Sound) protocol and directly drives a speaker—combining DAC and amplifier in one package. The MAX98357A in your Pupper takes serial digital audio from the MCU and outputs up to 3.2W to a speaker, enabling the robot to make sounds without external audio hardware.

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
