---
term: I2S (Inter-IC Sound)
created: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/i2s-audio-amplifier]] | [[learning/notes/micro-context/spi]] | [[learning/notes/quick-context/embedded-communication-protocols]] | [[learning/notes/quick-context/pupper-bom-control-board]]

# I2S (Inter-IC Sound)

> **See also:** [[learning/notes/micro-context/i2s-audio-amplifier]] | [[learning/notes/micro-context/spi]] | [[learning/notes/quick-context/embedded-communication-protocols]]

**Definition:** A 3-wire serial protocol designed specifically for streaming digital audio between ICs. Created by Philips in 1986, it carries stereo PCM audio using a bit clock (BCLK), a left/right channel select (LRCLK/WS), and a serial data line (SD). On the [[learning/notes/quick-context/pupper-bom-control-board|Pupper control board]], the main STM32 sends audio over I2S to the [[learning/notes/micro-context/i2s-audio-amplifier|MAX98357A amplifier]].

## How It Works

- The master generates BCLK (bit clock) to shift audio samples out one bit at a time, and LRCLK (word select) to indicate left vs. right channel.
- When LRCLK is low, the left channel sample is transmitted; when high, the right channel — one complete stereo frame per LRCLK cycle.
- The receiver latches data on the rising edge of BCLK (transmitters typically transition on the falling edge so data is stable in time). MSB (most significant bit) is sent first, one clock cycle after the LRCLK transition.
- Unlike [[learning/notes/micro-context/spi|SPI]], I2S has no chip-select — it's a dedicated point-to-point audio link, not a shared bus.

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

**Key insight:** I2S is essentially [[learning/notes/micro-context/spi|SPI]] repurposed for audio — same clock-and-data shifting, but with LRCLK replacing chip-select to multiplex stereo channels on a single data line.
