---
topic: Capacitive Sensing and Measurement
created: 2026-03-28
---

# Capacitive Sensing and Measurement

> **Related:** [[quick-context/capacitance]] | [[quick-context/capacitor]] | [[quick-context/rc-oscillator]] | [[micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/capacitive-voltage-sensing]]

> **TL;DR:** Capacitance can't be measured with DC -- a charged [[quick-context/capacitor|capacitor]] is an open circuit -- so every capacitive sensor relies on some form of AC excitation: repeatedly charge/discharge a capacitor and time it, pump charge between a sensor and reference capacitor and count the ratio, or drive an AC signal and measure the impedance. These three families of techniques -- RC timing, charge-balance (sigma-delta), and impedance measurement -- underpin every capacitive sensor from [[small-context/humidity-temperature-sensor|humidity films]] and [[small-context/mems-accelerometer-capacitive-sensing|MEMS accelerometers]] to touchscreens and proximity detectors.

## The Core Problem

Dozens of physical quantities -- humidity, acceleration, pressure, proximity, touch, liquid level -- can be transduced into a [[quick-context/capacitance|capacitance]] change by varying the plate area, gap distance, or dielectric constant of a capacitor structure. But capacitance isn't a voltage or a current -- you can't just connect a [[micro-context/adc-analog-to-digital-converter|ADC]] to a capacitor and read a number. You need a measurement circuit that *converts* capacitance into something digital. The choice of conversion technique determines the sensor's resolution, speed, noise rejection, and cost -- and the same three families of technique keep appearing across wildly different sensor types.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Capacitance-to-Digital Converter (CDC)** | An IC or on-chip block that directly converts a capacitance value to a digital number, typically using a sigma-delta charge-balancing architecture. Found inside sensor ICs like the SHT40 ([[small-context/humidity-temperature-sensor|humidity sensor]]) and MEMS accelerometer readout ASICs. |
| **Charge Transfer** | A measurement technique where charge is repeatedly shuttled from an unknown capacitor ($C_x$) to a known accumulator capacitor ($C_s$), counting cycles until $C_s$ reaches a threshold. The count is proportional to $C_x$. Used in touchscreen controllers (e.g., Microchip QTouch). |
| **Excitation Signal** | The AC voltage or switched-capacitor clock applied to the sensor to create measurable current flow. Without excitation, a capacitor at steady state passes zero current ($I = C \cdot dV/dt$, and $dV/dt = 0$ at DC). |
| **Sigma-Delta Modulation** | An oversampling technique that encodes the ratio $C_{\text{sensor}} / C_{\text{ref}}$ as the density of 1s in a high-speed bitstream. A digital decimation filter extracts a high-resolution result (16-24 bits) from this noisy 1-bit stream. |
| **Differential Capacitance** | A sensor architecture with two capacitors ($C_1$, $C_2$) that change in opposite directions when the measurand changes. The readout measures $\Delta C = C_1 - C_2$, which doubles sensitivity and cancels common-mode drift -- the same principle as [[quick-context/can-bus|CAN bus]] differential signaling. |

<details>
<summary><strong>How It Works</strong> -- Three families of capacitance measurement</summary>

### Why DC Doesn't Work

A capacitor at steady-state voltage is an open circuit. No current flows, so there's nothing to measure. To extract information from a capacitance, you must *change* the voltage across it -- that creates current proportional to capacitance:

$$I = C \cdot \frac{dV}{dt}$$

Every capacitive measurement technique is ultimately a way of applying $dV/dt$ and measuring the resulting $I$ (or the time, charge, or frequency that results). The three families differ in *how* they apply the excitation and *what* they measure:

```
THREE FAMILIES OF CAPACITANCE MEASUREMENT
==============================================================================

1. RC TIMING                2. CHARGE BALANCE            3. AC IMPEDANCE
   (cheapest)                  (sigma-delta CDC)            (highest precision)
                               (most common in sensors)

   Charge C through R,         Pump charge from C_sensor    Drive sine/square wave,
   measure time to              and C_ref into integrator,   measure amplitude and
   reach threshold              count the ratio              phase of resulting current

   ┌───╱╱╱──┬──┐              C_s──┐                       V_ac ──┤├── I_out
   │   R    │  │                   ├──►Integrator──►1-bit         C_x
   │       ═╪═ │  → Timer     C_r──┘   ──►Digital filter   I = V × 2πfC
   Vs      C_x │                                            (at known f)
   │        │  │
   └────────┴──┘

   Resolution: 8-12 bit       Resolution: 16-24 bit       Resolution: 20-23 bit (LCR)
   Speed: fast (μs)           Speed: moderate (ms)         Speed: slow (ms-s)
   Cost: pennies              Cost: cents to dollars        Cost: dollars to $$
   Noise: moderate            Noise: excellent              Noise: excellent
                              (oversampling averages)       (lock-in detection)
```

---

### Family 1: RC Timing

The simplest approach: charge $C_x$ through a known [[quick-context/resistor|resistor]] $R$, and measure how long it takes to reach a threshold voltage. Since $\tau = RC$, the time is directly proportional to capacitance.

```
RC TIMING — HOW TOUCHSCREEN CONTROLLERS WORK
==============================================================================

    VCC
     │
    ┌┴┐
    │R│  known resistor (e.g., 10 kΩ)
    └┬┘
     │
     ├────── to MCU timer input (digital pin with threshold)
     │
    ═╪═  C_x (unknown — the touch pad capacitance)
     │
    GND

    MEASUREMENT:
    1. Discharge C_x to 0V (pull pin LOW briefly)
    2. Release pin, start timer
    3. C_x charges through R toward VCC
    4. Timer stops when voltage crosses the digital input threshold (~1.5V)
    5. Count = timer value ∝ R × C_x

    NO TOUCH:  C_x ≈ 10 pF    →  τ = 10kΩ × 10pF = 100 ns   → count = 47
    TOUCHED:   C_x ≈ 15 pF    →  τ = 10kΩ × 15pF = 150 ns   → count = 71
                                                                 ↑ 50% increase!

    The MCU just watches for count changes — no analog circuitry needed.
```

This is how the [[quick-context/rc-oscillator|RC oscillator]] principle gets repurposed for sensing: instead of generating a clock, the RC circuit measures an unknown capacitance by timing the charge curve. Simple enough to implement on a bare [[micro-context/microcontroller|microcontroller]] GPIO pin with no external ICs.

**Where it's used:** Capacitive touch buttons, simple proximity sensors, liquid level probes, some low-cost humidity sensors.

**Limitation:** Accuracy depends on $R$ tolerance, threshold voltage stability, and timer resolution. Typically 8-12 effective bits -- fine for "touched or not," but too coarse for precision sensing.

---

### Family 2: Charge Balance (Sigma-Delta CDC)

The workhorse of modern capacitive sensor ICs. Instead of timing, it *compares* the sensor capacitance to a reference capacitance by shuffling charge packets:

```
SIGMA-DELTA CAPACITANCE-TO-DIGITAL CONVERTER
==============================================================================

    SIMPLIFIED ARCHITECTURE:

    C_sensor ──┐     ┌────────────┐     ┌────────────┐     ┌─────────┐
               ├────►│ Charge     │────►│ Comparator │────►│ Digital │
               │     │ Integrator │     │ (1-bit)    │     │ Filter  │──► 16-24 bit
    C_ref ─────┘     └────────────┘     └────────────┘     └─────────┘    result
                          │                    │
                          └────────────────────┘
                            Feedback loop

    HOW IT WORKS (one cycle):

    Phase 1: SAMPLE                     Phase 2: TRANSFER
    ─────────────────                   ─────────────────

    V_exc ──┤├──►Integrator             V_ref ──┤├──►Integrator
            C_s                                 C_r
                                                (opposite polarity)

    Charge delivered: Q_s = C_s × V       Charge removed: Q_r = C_r × V_ref

    The feedback loop adjusts how many Phase-1 vs Phase-2 cycles occur
    to keep the integrator balanced:

    At balance:  N_s × C_s × V = N_r × C_r × V_ref

    The ratio N_s / (N_s + N_r) encodes C_s / C_r as a digital fraction.

    The digital filter averages thousands of these 1-bit decisions
    into a stable 16-24 bit result.

    EXAMPLE (humidity sensor — see humidity-temperature-sensor for full chain):
    ─────────────────────────────────────────────────────────────────────
    C_sensor = ~190 pF (polymer film absorbing moisture)
    C_ref    = 200 pF  (stable on-chip reference)

    Bitstream density: 190/200 = 0.95 → 95% of bits are "1"
    After decimation:  16-bit result = 0xF333 → maps to 62.1% RH
```

**Why sigma-delta dominates sensor ICs:**
- Oversampling naturally averages out noise (better resolution without better components)
- Ratio-metric: result depends on $C_{\text{sensor}} / C_{\text{ref}}$, so supply voltage variations cancel
- Works directly with capacitance -- no need to convert to voltage first
- The same architecture works for resistance (thermistors) and voltage (strain gauges)

**Where it's used:** [[small-context/humidity-temperature-sensor|Humidity sensors]] (SHT40, HDC1080), [[small-context/mems-accelerometer-capacitive-sensing|MEMS accelerometers]] (ADXL345, BNO086's accel), MEMS gyroscopes, capacitive pressure sensors, precision touch interfaces.

---

### Family 3: AC Impedance

Drive a known AC signal through $C_x$ and measure the resulting current. Since [[quick-context/impedance-and-reactance|capacitive reactance]] is $X_C = 1/(2\pi f C)$, the current $I = V / X_C = V \cdot 2\pi f C$ is directly proportional to capacitance.

```
AC IMPEDANCE MEASUREMENT (LCR meter principle)
==============================================================================

    V_ac (known f, known amplitude)
     │
     └──────┤├──────┬──► I_measure
            C_x     │
                    ▼
              Phase-sensitive
              detector (lock-in)

    Measures BOTH:
      |I| = V × 2πfC        → capacitance magnitude
      ∠I = +90° vs V        → confirms it's capacitive (not resistive)

    LOCK-IN DETECTION (the key to precision):
    ─────────────────────────────────────────────────────────────────────

    Multiply measured signal by reference signal at same frequency:
    - Signal at the excitation frequency → DC output (detected)
    - Noise at all other frequencies → averages to zero

    This is why LCR meters can resolve femtofarads despite millivolt noise.
```

**Where it's used:** Bench LCR meters, some high-precision industrial sensors, bioimpedance analyzers, and the readout ASICs in high-end MEMS devices (which use switched-capacitor versions of this at MHz frequencies).

---

### Which Sensors Use Which Technique?

```
SENSOR TYPE vs. MEASUREMENT TECHNIQUE
==============================================================================

Sensor                    │ What Changes          │ Typical         │ Readout
                          │ in C = εA/d           │ ΔC Range        │ Technique
══════════════════════════╪═══════════════════════╪═════════════════╪════════════
Humidity (polymer film)   │ ε_r of dielectric     │ ~0.1 pF/%RH    │ Sigma-delta
  (SHT40)                │ (water absorption)     │ (180→200 pF)   │ CDC
──────────────────────────┼───────────────────────┼─────────────────┼────────────
MEMS accelerometer        │ d (gap between         │ ~0.1-1 fF/g    │ Sigma-delta
  (ADXL, BNO086)         │  comb fingers)         │ (differential)  │ CDC
──────────────────────────┼───────────────────────┼─────────────────┼────────────
MEMS gyroscope            │ d (Coriolis-induced   │ ~attofarads     │ Sigma-delta
  (BNO086)               │  lateral displacement) │ (differential)  │ + demod
──────────────────────────┼───────────────────────┼─────────────────┼────────────
MEMS pressure sensor      │ d (membrane deflects   │ ~0.01 pF/kPa   │ Sigma-delta
  (barometers)            │  toward fixed plate)   │                 │ CDC
──────────────────────────┼───────────────────────┼─────────────────┼────────────
Touchscreen (projected    │ A (finger adds          │ ~1-5 pF        │ Charge
  capacitive)             │  coupling area)         │ per touch      │ transfer
──────────────────────────┼───────────────────────┼─────────────────┼────────────
Touch button              │ A or ε (finger near     │ ~0.5-5 pF      │ RC timing
  (self-capacitance)      │  pad changes field)     │                 │ or charge
                          │                         │                 │ transfer
──────────────────────────┼───────────────────────┼─────────────────┼────────────
Capacitive proximity      │ ε and fringing fields   │ ~fF to pF      │ RC timing
  sensor                  │ (object enters field)   │ (distance-      │ or CDC
                          │                         │  dependent)     │
──────────────────────────┼───────────────────────┼─────────────────┼────────────
Liquid level sensor       │ ε_r (liquid replaces    │ large           │ RC timing
  (capacitive probe)      │  air between plates)    │ (ε_water ≈ 80) │ or AC imp.
──────────────────────────┼───────────────────────┼─────────────────┼────────────
Camera photodiode         │ NOT capacitive sensing  │ N/A             │ Charge
  (image sensor)          │ — photoelectric effect  │                 │ integration
                          │ but charge IS stored    │                 │ + ADC
                          │ on junction capacitance │                 │
```

Note: [[quick-context/camera-fundamentals|Camera photodiodes]] are *not* capacitive sensors -- they exploit the photoelectric effect (photons free electrons in [[quick-context/doped-silicon|doped silicon]]). But the accumulated charge IS stored on the junction capacitance of the reverse-biased [[quick-context/diode|diode]], and the readout circuit must deal with that capacitance. The underlying physics is photon-to-electron conversion, not geometry-to-capacitance transduction.

</details>

<details>
<summary><strong>The Key Tension</strong> -- Resolution vs. speed vs. cost</summary>

Every capacitance measurement technique trades off the same three things:

| Technique | Resolution | Speed | Cost | Best For |
|-----------|-----------|-------|------|----------|
| RC timing | 8-12 bits | Fast (1-100 $\mu$s) | Near zero (GPIO pin + R) | Touch/proximity, binary decisions |
| Charge transfer | 10-16 bits | Moderate (100 $\mu$s - 1 ms) | Low (dedicated controller IC) | Multi-channel touchscreens |
| Sigma-delta CDC | 16-24 bits | Slow (1-100 ms) | Moderate (sensor IC) | Precision sensors (humidity, accel) |
| AC impedance | 20-23 bits (LCR meter) | Very slow (10 ms - 1 s) | High (LCR meter / bridge) | Lab measurement, calibration |

```
THE RESOLUTION-SPEED TRADEOFF
==============================================================================

    Resolution
    (bits)
        │
    24  │                            ● Sigma-delta CDC
        │                           (humidity, MEMS accel)
    20  │
        │
    16  │              ● Charge transfer
        │             (touchscreens)
    12  │    ● RC timing
        │   (touch buttons)
     8  │
        │
        └────────────────────────────────────────────► Speed
            1 μs      100 μs      1 ms      100 ms

    More averaging (oversampling) = better resolution but slower.
    Sigma-delta gets 24 bits by averaging millions of 1-bit samples.

    THE FUNDAMENTAL LIMIT:  kT/C noise
    ────────────────────────────────────────────────────────────────
    Thermal noise on a capacitor: V_noise = sqrt(kT/C)

    At room temperature (T = 300K), C = 10 pF:
    V_noise = sqrt(1.38e-23 × 300 / 10e-12) = 20.3 μV (rms)

    On a 3.3V range, that's ~17.3 effective bits — no measurement
    technique can do better without reducing noise or increasing C.

    At C = 1 pF (MEMS accelerometer scale):
    V_noise = sqrt(1.38e-23 × 300 / 1e-12) = 64 μV (rms) → ~15.6 ENOB
    Smaller C = more noise = harder to measure precisely.
```

The dominant trend in modern sensor design is sigma-delta CDC integration: put the converter on the same die as the sensor element, so the tiny analog signals never leave the chip. This is why modern sensor ICs (SHT40, BMP390, ADXL345) output clean digital numbers over [[micro-context/i2c|I2C]] or [[micro-context/spi|SPI]] -- the entire capacitance-to-digital chain is inside the package.

</details>

<details>
<summary><strong>Concrete Example</strong> -- From polymer film to "%RH" over I2C</summary>

The [[small-context/humidity-temperature-sensor|SHT40 humidity sensor]] demonstrates the full capacitive sensing chain. Here's every step from physical stimulus to digital readout:

```
COMPLETE CAPACITIVE SENSING CHAIN (SHT40 humidity measurement)
==============================================================================

    1. PHYSICAL QUANTITY        2. TRANSDUCTION          3. MEASUREMENT
       (humidity)                  (C = εA/d)              (sigma-delta CDC)

    Water vapor in air         Polymer absorbs H₂O      CDC compares charge
    RH = 55%                   → ε_r increases           from C_sensor vs C_ref
         │                     → C rises to ~190 pF           │
         ▼                          │                         ▼
    ┌────────────┐            ┌────────────┐           ┌────────────┐
    │ Porous Au  │            │ C = εA/d   │           │ Bitstream: │
    │ electrode  │            │            │           │ 110110111  │
    │ Polymer    │  H₂O ──►  │ ε_r ≈ 4.2  │  ──────►  │ 101111011  │
    │ film       │  diffuses  │ A = fixed   │  C_s/C_r  │ (density   │
    │ Bottom     │  into film │ d = fixed   │  ratio    │  = 0.95)   │
    │ electrode  │            │            │           └─────┬──────┘
    └────────────┘            └────────────┘                 │
                                                              ▼
    4. DIGITAL FILTER           5. CALIBRATION            6. I2C OUTPUT

    Decimation extracts         Factory-stored             MCU reads
    16-bit count from           coefficients correct       6 bytes:
    oversampled bitstream       for nonlinearity and       T_MSB, T_LSB, CRC,
         │                      temperature cross-effect   H_MSB, H_LSB, CRC
         ▼                           │                         │
    ┌────────────┐            ┌────────────┐           ┌────────────┐
    │ raw count: │            │ polynomial │           │ 0x44 + W:  │
    │ 0xF333     │  ──────►  │ correction │  ──────►  │ cmd 0xFD   │
    │ (62259)    │            │ + T comp   │           │ wait 8.2ms │
    └────────────┘            │ → 55.3% RH │           │ read 6B    │
                              └────────────┘           └────────────┘

    Total latency: ~8.2 ms from command to calibrated result
    Resolution: 0.01% RH (far finer than sensor accuracy of ±1.8% RH)
```

The same sigma-delta CDC architecture appears in MEMS accelerometers, but measuring femtofarads (not picofarads) from comb-finger displacement instead of dielectric change. See [[small-context/mems-accelerometer-capacitive-sensing]] for that chain.

**The one thing most outsiders get wrong about this is...** thinking that capacitive sensors "measure capacitance" the way a multimeter measures resistance -- as a static property you read once. In reality, capacitance measurement is always *dynamic*: the circuit is constantly cycling excitation signals through the sensor at kHz-MHz rates, integrating tiny charge packets, and averaging millions of samples to extract a stable reading. A "single measurement" from an SHT40 actually involves millions of charge-balance cycles executed in 8 milliseconds. The sensor is never at rest -- it's continuously pumping charge to track a moving target.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/capacitance]]** -- The physics of $C = \varepsilon A / d$, parasitic capacitance, and why capacitance shows up everywhere in electronics. This article covers how capacitance is *created*; the current article covers how it's *measured*.

- **[[quick-context/capacitor]]** -- Capacitor types, charge/discharge curves, and RC time constants. The RC charge curve ($V(t) = V_s(1 - e^{-t/RC})$) is the mathematical basis of RC timing measurement.

- **[[quick-context/rc-oscillator]]** -- The same RC timing principle used for capacitive measurement also generates clock signals. An RC oscillator is essentially a capacitive sensor that measures its own capacitance continuously.

- **[[quick-context/impedance-and-reactance]]** -- Capacitive reactance $X_C = 1/(2\pi fC)$ is the basis of AC impedance measurement, and explains why capacitive sensors need AC excitation.

- **[[small-context/humidity-temperature-sensor]]** -- Full walkthrough of the SHT40 humidity sensor: polymer dielectric, sigma-delta CDC, calibration, and I2C readout.

- **[[small-context/mems-accelerometer-capacitive-sensing]]** -- Full walkthrough of MEMS accelerometer comb-finger capacitive sensing with differential readout.

- **[[small-context/imu-robot-balance-sensing]]** -- How the capacitive accelerometer fits into the BNO086's sensor fusion for robot balance.

- **[[quick-context/camera-fundamentals]]** -- Photodiode-based image sensors are *not* capacitive sensors, but charge storage on junction capacitance is central to how they work. Contrasts with capacitive transduction.

- **[[micro-context/piezoelectric-effect]]** -- Piezoelectric sensors generate charge proportional to force. Their readout circuits (charge amplifiers) share design principles with capacitive sensor readout -- both must measure tiny charge quantities.

- **[[quick-context/oscilloscope-and-multimeter]]** -- Multimeters often include a capacitance mode that uses RC timing or charge counting. Oscilloscopes can visualize the charge/discharge waveforms directly.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why can't you measure capacitance with a DC voltage and an ADC?
<details>
<summary>Answer</summary>
A capacitor at steady-state DC is an open circuit -- no current flows, so there's nothing for the ADC to measure. Current only flows when voltage is *changing*: $I = C \cdot dV/dt$. At DC, $dV/dt = 0$, so $I = 0$ regardless of the capacitance value. You need AC excitation (charge/discharge cycles, switched capacitors, or sine wave drive) to create measurable current. See: How It Works -- "Why DC Doesn't Work."
</details>

**Q2:** A MEMS accelerometer measures femtofarad changes, while a humidity sensor measures picofarad changes. Both use sigma-delta CDCs. Why does the accelerometer need differential sensing but the humidity sensor doesn't?
<details>
<summary>Answer</summary>
The accelerometer's signal ($\Delta C \approx 0.1$ fF) is ~1000x smaller than the humidity sensor's ($\Delta C \approx 0.1$ pF = 100 fF). At femtofarad levels, thermal drift, aging, and manufacturing variation in the base capacitance would swamp the tiny signal. Differential sensing ($C_1 - C_2$) cancels these common-mode effects because both capacitors drift equally. The humidity sensor's signal is large enough relative to drift that single-ended measurement works. See: 5 Essential Terms (Differential Capacitance) and [[small-context/mems-accelerometer-capacitive-sensing]].
</details>

**Q3:** You're designing a capacitive touch button using an MCU GPIO pin and a 10 k$\Omega$ resistor. The pad capacitance is ~10 pF untouched and ~15 pF when touched. Your MCU timer runs at 48 MHz. Can you reliably detect a touch?
<details>
<summary>Answer</summary>
The RC time constants are $\tau_{\text{no touch}} = 10\text{k}\Omega \times 10\text{pF} = 100\text{ns}$ and $\tau_{\text{touch}} = 10\text{k}\Omega \times 15\text{pF} = 150\text{ns}$. At 48 MHz, one timer tick = 20.8 ns. Charging to a threshold at ~0.69$\tau$ (50% of VCC): no-touch ≈ 69 ns ≈ 3.3 counts; touch ≈ 104 ns ≈ 5 counts. The difference (2 counts) is small but detectable. In practice you'd average many samples or use a lower resistance to spread the counts further apart. See: How It Works (Family 1: RC Timing).
</details>

**Q4:** Why does the SHT40 humidity sensor achieve 0.01% RH resolution but only ±1.8% RH accuracy?
<details>
<summary>Answer</summary>
Resolution and accuracy are different. The 16-bit sigma-delta CDC can *resolve* tiny capacitance changes (0.01% RH steps) because oversampling averages noise effectively. But *accuracy* is limited by the physical sensor: the polymer film's response to humidity is nonlinear, hysteretic, temperature-dependent, and changes with aging. Even with perfect calibration at the factory, these physical effects introduce ±1.8% systematic error that no amount of digital resolution can fix. Resolution tells you the smallest *change* you can detect; accuracy tells you how close the *absolute* reading is to truth. See: Concrete Example.
</details>

**Q5:** The $kT/C$ thermal noise limit gives $V_{\text{noise}} = \sqrt{kT/C}$. A MEMS accelerometer has comb-finger capacitance of ~1 pF, while a humidity sensor has ~190 pF. Which has a harder time with thermal noise, and what does this mean for readout circuit design?
<details>
<summary>Answer</summary>
The accelerometer. At 1 pF: $V_{\text{noise}} = \sqrt{1.38 \times 10^{-23} \times 300 / 10^{-12}} \approx 64\ \mu\text{V}$ rms. At 190 pF: $V_{\text{noise}} \approx 4.7\ \mu\text{V}$ rms -- about 14x lower. The smaller capacitance means the charge per measurement cycle is tiny and noise is relatively large. This is why MEMS accelerometers use differential sensing (doubles signal, cancels common-mode noise), shielded readout paths, and often correlated double sampling. The humidity sensor's large base capacitance gives it a natural noise advantage, so simpler readout suffices. The $kT/C$ limit also explains why DRAM capacitors can't shrink indefinitely -- see [[quick-context/capacitor|capacitor thermal noise discussion]].
</details>

</details>
