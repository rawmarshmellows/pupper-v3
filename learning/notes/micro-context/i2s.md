---
term: I2S (Inter-IC Sound)
created: 2026-03-27
---

# I2S (Inter-IC Sound)

> **Related:** [[micro-context/i2s-audio-amplifier]] | [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]] | [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/ads1110-battery-adc]]

**[[quick-context/capacitance|Definition]]:** A 3-wire serial protocol designed specifically for streaming digital audio between ICs. Created by Philips in 1986, it carries stereo PCM audio using a bit clock (BCLK), a left/right [[micro-context/mosfet|channel]] select (LRCLK/WS), and a serial data line (SD). On the [[quick-context/pupper-bom-control-board|Pupper control board]], the main STM32 sends audio over I2S to the [[micro-context/i2s-audio-amplifier|MAX98357A amplifier]].

## How It Works

- The master generates BCLK (bit clock) to shift audio samples [[micro-context/push-pull-vs-open-drain|out]] one bit at a time, and LRCLK (word select) to indicate left vs. right channel.
- When LRCLK is low, the left channel sample is transmitted; when high, the right channel — one complete stereo [[quick-context/can-bus|frame]] per LRCLK cycle.
- The receiver latches data on the [[quick-context/bare-minimal-data-storage-circuit|rising edge]] of BCLK (transmitters typically transition on the falling edge so data is stable in time). MSB (most significant bit) is sent first, one clock cycle after the LRCLK transition.
- Unlike [[micro-context/spi|SPI]], I2S has no chip-select — it's a dedicated point-to-point audio link, [[micro-context/can-bus-termination|not]] a shared bus.

```
I2S TIMING (16-bit stereo):

         ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐ ┌┐
BCLK:  ──┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└─┘└──
                  ↑ receiver latches on rising edge

                          ┌──────────────────┐
LRCLK: ──────────────────┘                    └─────
       ◄── LEFT (WS=0) ──►◄── RIGHT (WS=1) ──►

SD:      X MSB  ...  LSB    MSB  ...  LSB
         ◄── 16-bit left ──►◄── 16-bit right─►
         ↑ MSB 1 BCLK after WS transition
```

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** I2S is essentially [[micro-context/spi|SPI]] repurposed for audio — same clock-and-data shifting, but with LRCLK replacing chip-select to multiplex stereo channels on a single data line.
