---
topic: Frequency and Filtering
created: 2026-02-06
---

> **Related:** [[learning/notes/quick-context/comparator-specification]] | [[learning/notes/quick-context/fundamental-electronic-parts-index]] | [[learning/notes/quick-context/capacitance]] | [[learning/notes/quick-context/pupper-bom-control-board]] | [[learning/notes/quick-context/inductor]]

> **TL;DR:** Real-world signals are mixtures of many frequencies; filters use the frequency-dependent behavior of [[quick-context/capacitor|capacitors]] and [[quick-context/inductor|inductors]] (described by [[quick-context/impedance-and-reactance|impedance]]) to keep desired frequencies and reject unwanted ones—they're essential for separating signals from noise, processing audio, and preventing electromagnetic interference.

# Frequency and Filtering

## The Core Problem: Separating Signal from Noise

A microphone picks up a voice (300 Hz - 3 kHz) plus a 60 Hz hum from nearby power lines plus high-frequency hiss from the amplifier. You want the voice and nothing else. A filter does this: it passes frequencies in the desired range and attenuates everything outside it. Every audio system, radio receiver, power supply, and communication link depends on filters. Without filtering, every electronic signal would be buried in noise from every other signal and interference source sharing the same wires or airwaves.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Frequency (f)** | How many times a signal repeats per second, measured in hertz (Hz). Period T = 1/f. Human hearing: 20 Hz - 20 kHz. WiFi: 2.4 GHz. |
| **Cutoff Frequency (fc)** | The frequency at which a filter's output drops to -3 dB (70.7% voltage, 50% power). Defines the boundary between "pass" and "stop." |
| **Decibel (dB)** | A logarithmic ratio: dB = 20 × log₁₀(Vout/Vin). -3 dB = half power. -20 dB = 1/10 voltage. -40 dB = 1/100 voltage. |
| **Low-pass / High-pass** | Low-pass: passes below fc, blocks above. High-pass: passes above fc, blocks below. Band-pass: passes a range. Band-stop/notch: blocks a range. |
| **Order** | How many reactive elements (C or L) in the filter. Higher order = sharper cutoff slope. 1st order = -20 dB/decade. 2nd order = -40 dB/decade. |

<details>
<summary><strong>How It Works</strong></summary>

```
FILTER TYPES
══════════════════════════════════════════════════════════════════════════════

    LOW-PASS                   HIGH-PASS
    Vin─╱╱╱╱─┬─Vout           Vin─┤├──┬─Vout
         R    │                    C    │
             ═╪═ C                     ╱╱╱╱ R
              │                        │
             GND                      GND

    fc = 1/(2πRC)              fc = 1/(2πRC)

    Gain                       Gain
     0dB──────╲                     ╱──────0dB
              ╲                    ╱
    -3dB──────╳                   ╳──────-3dB
               ╲                 ╱
                ╲───            ╱
                    ────       ╱
    └─────────────────► f     └─────────────────► f
              fc                       fc


    BAND-PASS                  BAND-STOP (NOTCH)
    Passes a range             Blocks a specific frequency

    Gain                       Gain
              ╱╲              ──────╲  ╱──────
             ╱  ╲                    ╲╱
            ╱    ╲                    ╳ fc
    ───────╱      ╲───────    ───────╱╲───────
          fL  fc  fH                fL  fH


FREQUENCY AND PERIOD
══════════════════════════════════════════════════════════════════════════════

    f = 1/T     T = 1/f

    Signal        │ Frequency    │ Period        │ Wavelength
    ──────────────┼──────────────┼───────────────┼────────────────
    Mains power   │ 50/60 Hz     │ 16.7/20 ms    │ 5000 km
    Audio (voice) │ 300-3000 Hz  │ 0.3-3.3 ms    │ 100-1000 km
    Audio (music) │ 20-20,000 Hz │ 50μs-50ms     │ 15 km-15,000 km
    Ultrasound    │ 40 kHz       │ 25 μs         │ 8.5 mm (in air)
    AM Radio      │ 1 MHz        │ 1 μs          │ 300 m
    WiFi          │ 2.4 GHz      │ 0.4 ns        │ 12.5 cm
    5G mmWave     │ 28 GHz       │ 36 ps         │ 10.7 mm


DECIBELS: THE LANGUAGE OF SIGNAL LEVELS
══════════════════════════════════════════════════════════════════════════════

    dB = 20 × log₁₀(Vout / Vin)    (voltage ratio)
    dB = 10 × log₁₀(Pout / Pin)    (power ratio)

    Voltage Ratio    │ dB       │ Meaning
    ─────────────────┼──────────┼──────────────────
    1.0              │  0 dB    │ No change
    0.707            │ -3 dB    │ Half power (cutoff)
    0.5              │ -6 dB    │ Half voltage
    0.1              │ -20 dB   │ 1/10 voltage
    0.01             │ -40 dB   │ 1/100 voltage
    0.001            │ -60 dB   │ 1/1000 voltage
    2.0              │ +6 dB    │ Double voltage
    10.0             │ +20 dB   │ 10× voltage

    Why dB? Because multiplying gains becomes adding dB:
    Two stages of -20dB each = -40dB total (not -400!)


FILTER ORDER AND ROLLOFF
══════════════════════════════════════════════════════════════════════════════

    Gain (dB)
     0 ───────────╲
                   ╲╲╲
    -3 ────────────╳╳╳
                    │╲ ╲
                    │ ╲  ╲
    -20 ────────────│──╲──╲───
                    │   ╲   ╲
                    │    ╲    ╲
    -40 ────────────│─────╲────╲──
                    │      ╲     ╲
                    fc    10fc  100fc

    ─── 1st order: -20 dB/decade  (1 cap or 1 inductor)
    ─── 2nd order: -40 dB/decade  (LC or active, sharper)
    ─── 4th order: -80 dB/decade  (very sharp, complex)

    Sharper filtering = more components = more phase distortion
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Sharpness vs. Complexity vs. Phase Distortion

A 1st-order filter is simple (one R + one C) but its -20 dB/decade slope means unwanted signals only 10× above the cutoff are only attenuated 10×. For many applications, that's not enough.

Higher-order filters have sharper rolloff but introduce more phase shift (which distorts waveforms) and need more components. Active filters (using [[quick-context/op-amp|op-amps]]) can achieve sharper rolloff without inductors, but add noise, power consumption, and complexity.

```
FILTER TOPOLOGY TRADEOFFS
══════════════════════════════════════════════════════════════════════════════

    Butterworth: Maximally flat passband, moderate rolloff
                 "No ripple, gentle slope"

    Chebyshev:   Steeper rolloff, but has ripple in passband
                 "Sharper but wavy"

    Bessel:      Best phase response (least waveform distortion)
                 "Gentlest slope but cleanest step response"

    Elliptic:    Steepest possible rolloff, ripple in both bands
                 "Sharpest but messiest"
```

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## EMI Filter on a Switching Power Supply

Switching power supplies operate at 100 kHz - 2 MHz, generating enormous high-frequency noise that would radiate into other circuits and violate EMC regulations. An LC input filter keeps this noise contained.

```
EMI FILTER
══════════════════════════════════════════════════════════════════════════════

    AC Mains ──⊃⊃⊃⊃──┬──⊃⊃⊃⊃── Switching Supply
       (50Hz)    L1    │    L2     (200kHz switching)
                      ═╪═ Cy
                       │
                      GND

    fc ≈ 10-50 kHz (between mains 50Hz and switching 200kHz)

    Below fc: 50 Hz mains power passes freely through to supply
    Above fc: 200 kHz switching noise is blocked from escaping to mains

    Without this filter:
    • Switching noise travels back through power cord
    • Radiates as electromagnetic interference (EMI)
    • Disrupts nearby AM radios, medical equipment
    • Fails regulatory compliance (FCC, CE marking)
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/impedance-and-reactance]]** — Filters work because capacitive and inductive reactance change with frequency. Understanding impedance is prerequisite to understanding filter behavior.

- **[[quick-context/capacitor]]** — The primary component in most filters. Its reactance (Xc = 1/2πfC) decreasing with frequency is what makes low-pass filters work.

- **[[quick-context/inductor]]** — Inductors combined with capacitors form second-order filters with -40 dB/decade rolloff and LC resonant circuits at f = 1/(2π√LC).

- **[[quick-context/resistor]]** — RC filters are the simplest and most common. The R sets the impedance level and, together with C, determines the cutoff frequency.

- **[[quick-context/thermal-noise-electronics]]** — Filtering reduces noise by limiting bandwidth. A filter with 1 kHz bandwidth passes 1/1000th the noise power of a 1 MHz bandwidth system.

- **[[quick-context/wifi-chip-arduino-uno-r4]]** — WiFi chips use bandpass filters extensively in their RF front-end to select the 2.4 GHz band and reject out-of-band interference. The frequency table above lists WiFi at 2.4 GHz / 12.5 cm wavelength.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** An RC low-pass filter has R = 1kΩ and C = 10nF. What is its cutoff frequency?
<details>
<summary>Answer</summary>
**15.9 kHz.** fc = 1/(2πRC) = 1/(2π × 1000 × 10×10⁻⁹) = 15,915 Hz ≈ 15.9 kHz. Signals below this pass; signals above are progressively attenuated at -20 dB/decade.
</details>

**Q2:** A signal at 100 kHz is passed through a 1st-order low-pass filter with fc = 1 kHz. How much is it attenuated?
<details>
<summary>Answer</summary>
**-40 dB (1/100th voltage).** The signal is 100× above the cutoff (2 decades). A 1st-order filter rolls off at -20 dB/decade, so 2 decades × -20 = -40 dB. In voltage, that's a factor of 100: a 1V signal would be reduced to 10 mV.
</details>

**Q3:** What does "-3 dB" actually mean in practical terms?
<details>
<summary>Answer</summary>
**Half the power, or 70.7% of the voltage.** -3 dB voltage = 10^(-3/20) = 0.707. Since power is proportional to voltage squared: 0.707² = 0.5 = half power. The -3 dB point is chosen as the cutoff because it's where the filter transitions from "mostly passing" to "mostly blocking."
</details>

**Q4:** Why would you choose a 2nd-order filter over a 1st-order for audio applications?
<details>
<summary>Answer</summary>
**Sharper rolloff (-40 dB/decade vs -20 dB/decade) better separates desired audio from unwanted frequencies.** For example, in an audio crossover splitting bass from treble at 3 kHz, a 1st-order filter at 30 kHz (10× above) only attenuates by 20 dB—still audible. A 2nd-order gives 40 dB attenuation—practically inaudible. The tradeoff is more components and potentially more phase distortion.
</details>

**Q5:** To make an RC high-pass filter from an RC low-pass filter, what do you change?
<details>
<summary>Answer</summary>
**Swap the resistor and capacitor positions.** In a low-pass, the resistor is in series and the capacitor shunts to ground. In a high-pass, the capacitor is in series and the resistor shunts to ground. The cutoff frequency formula fc = 1/(2πRC) stays the same. At low frequencies the capacitor has high impedance (blocks signal); at high frequencies it has low impedance (passes signal).
</details>

</details>
