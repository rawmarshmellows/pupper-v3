---
term: I2S (Inter-IC Sound)
created: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/i2s-audio-amplifier]]

# I2S (Inter-IC Sound)

> **[[learning/notes/quick-context/tensile-strength-materials|]]See also:** [[micro-context/i2s-audio-amplifier]] | [[micro-context/spi]] | [[quick-context/embedded-communication-protocols]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] [[learning/notes/quick-context/meddpicc-qualification-framework|3]]-wire [[learning/notes/quick-context/data-bus-and-arbitration|serial protocol]] designed specifically for streaming digital audio between ICs. Created by Philips in 1986, it carries stereo PCM audio using a bit [[learning/notes/quick-context/bare-minimal-data-storage-circuit|clock]] (BCLK), a left/right [[learning/notes/micro-context/mosfet|channel]] select (LRCLK/WS), [[learning/notes/micro-context/push-pull-vs-open-drain|and]] a [[learning/notes/quick-context/data-bus-and-arbitration|serial]] data line (SD). On [[learning/notes/quick-context/capacitance|the]] [[quick-context/pupper-bom-control-board|Pupper control board]], the main STM32 sends audio over I2S to the [[micro-context/i2s-audio-amplifier|MAX98357A amplifier]].

## How It Works

- The [[learning/notes/quick-context/data-bus-and-arbitration|master]] generates BCLK (bit clock) to shift audio samples [[learning/notes/micro-context/push-pull-vs-open-drain|out]] [[learning/notes/quick-context/ram-addressing-decoder|one]] bit at a time, and LRCLK ([[learning/notes/quick-context/ram-addressing-decoder|word]] select) to indicate left vs. right channel.
- [[learning/notes/quick-context/bare-minimal-data-storage-circuit|When]] LRCLK is low, the left channel sample is transmitted; when high, the right channel — one complete stereo [[learning/notes/quick-context/can-bus|frame]] per LRCLK cycle.
- The receiver latches data on the [[learning/notes/quick-context/bare-minimal-data-storage-circuit|rising edge]] of BCLK (transmitters typically transition on the falling edge so data is stable in time). MSB (most significant bit) is sent first, one clock cycle after the LRCLK transition.
- Unlike [[micro-context/spi|SPI]], I2S has [[learning/notes/micro-context/capacitive-voltage-sensing|no]] chip-select — it's a dedicated [[learning/notes/quick-context/epson-rc-plus-programming|point]]-to-point audio link, [[learning/notes/micro-context/can-bus-termination|not]] a shared [[learning/notes/quick-context/data-bus-and-arbitration|bus]].

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

**Key insight:** I2S is essentially [[micro-context/spi|SPI]] repurposed for audio — same clock-and-data shifting, but [[learning/notes/quick-context/breaking-elongation-rate|with]] LRCLK replacing chip-select to multiplex stereo channels on a single data line.
