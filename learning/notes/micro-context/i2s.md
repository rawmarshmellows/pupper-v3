---
term: I2S (Inter-IC Sound)
created: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/i2s-audio-amplifier]] | [[learning/notes/micro-context/can-bus-termination]] | [[learning/notes/micro-context/can-bus-transceiver]] | [[learning/notes/micro-context/i2c]] | [[learning/notes/micro-context/push-pull-vs-open-drain]]


# I2S (Inter-IC Sound)

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[micro-context/i2s-audio-amplifier]] | [[micro-context/spi]] | [[quick-context/embedded-communication-protocols]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** A 3-wire [[learning/notes/quick-context/data-bus-and-arbitration|serial protocol]] designed specifically for streaming digital audio between ICs. Created by Philips in 1986, it carries stereo PCM audio using a bit [[learning/notes/quick-context/bare-minimal-data-storage-circuit|clock]] (BCLK), a left/right [[learning/notes/micro-context/mosfet|channel]] select (LRCLK/WS), and a serial data line (SD). On the [[quick-context/pupper-bom-control-board|Pupper control board]], the main STM32 sends audio over I2S to the [[micro-context/i2s-audio-amplifier|MAX98357A amplifier]].

## How It Works

- The [[learning/notes/quick-context/data-bus-and-arbitration|master]] generates BCLK (bit clock) to shift audio samples out one bit at a time, and LRCLK ([[learning/notes/quick-context/ram-addressing-decoder|word]] select) to indicate left vs. right channel.
- [[learning/notes/quick-context/bare-minimal-data-storage-circuit|When]] LRCLK is low, the left channel sample is transmitted; when high, the right channel — one complete stereo [[learning/notes/quick-context/can-bus|frame]] per LRCLK cycle.
- The receiver latches data on the [[learning/notes/quick-context/bare-minimal-data-storage-circuit|rising edge]] of BCLK (transmitters typically transition on the falling edge so data is stable in time). MSB (most significant bit) is sent first, one clock cycle after the LRCLK transition.
- Unlike [[micro-context/spi|SPI]], I2S has no chip-select — it's a dedicated [[learning/notes/quick-context/epson-rc-plus-programming|point]]-to-point audio link, not a shared bus.

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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** I2S is essentially [[micro-context/spi|SPI]] repurposed for audio — same clock-and-data shifting, but with LRCLK replacing chip-select to multiplex stereo channels on a single data line.
