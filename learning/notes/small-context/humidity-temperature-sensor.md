---
case: Humidity and Temperature Sensor
components: [capacitor, resistor]
created: 2026-03-28
---

# Case: Humidity and Temperature Sensor

> **Components:** [[quick-context/capacitor]] | [[quick-context/resistor]] | [[quick-context/capacitance]]
> **Micro-context:** [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/i2c]]

> **In brief:** A humidity and temperature sensor combines two analog sensing elements -- a [[quick-context/capacitance|capacitive]] polymer film whose dielectric constant shifts with absorbed moisture and an NTC thermistor whose [[quick-context/resistor|resistance]] drops with heat -- with an on-chip [[micro-context/adc-analog-to-digital-converter|ADC]] that digitizes both signals and sends calibrated readings to a [[micro-context/i2c|microcontroller over I2C]].

## The Situation

You want a microcontroller to know the humidity and temperature of the air around it -- for climate control, weather monitoring, or environmental sensing. Air humidity and temperature are continuous physical quantities. A microcontroller only understands digital numbers. Something must transduce the physical world into electrical signals, then convert those signals into bits.

## The Pieces

**Capacitive humidity element:** A parallel-plate [[quick-context/capacitor|capacitor]] whose dielectric is a thin hygroscopic polymer film (~1 $\mu$m thick). As the polymer absorbs water vapor, its [[quick-context/capacitance|dielectric constant]] changes, shifting the measured capacitance. This is the humidity transducer. [[quick-context/capacitance|Full treatment on capacitance -->]]

**NTC thermistor:** A [[quick-context/resistor|resistor]] made from sintered metal-oxide ceramics whose resistance decreases as temperature rises (Negative Temperature Coefficient). Thermal energy excites electrons across the semiconductor band gap, creating more charge carriers. This is the temperature transducer. [[quick-context/resistor|Full treatment on resistors -->]]

**On-chip ADC:** An [[micro-context/adc-analog-to-digital-converter|analog-to-digital converter]] that measures the capacitance change and resistance change, converting them into 16-bit digital numbers. Modern sensors use sigma-delta converters for high resolution.

**I2C interface:** A standard [[micro-context/i2c|2-wire digital bus]] that delivers the calibrated readings to your microcontroller. The sensor is a slave device; the MCU requests a measurement and reads back the result.

## Step by Step: What Happens

### Step 1: Moisture enters the polymer film (humidity sensing)

The sensing element is a parallel-plate capacitor with a porous polymer (typically polyimide) as the dielectric. Water vapor from the air diffuses into the polymer through its porous structure.

```
CAPACITIVE HUMIDITY ELEMENT
==============================================================================

    Ambient air (water vapor molecules: o)
           o    o      o   o
           o       o     o
    ┌──────────────────────────────┐
    │  Top electrode (porous Au)   │  ← permeable to water vapor
    ├══════════════════════════════╡
    │  Polymer dielectric (~1 um) │  ← absorbs water molecules
    │   o  o     o    o  o        │     from the air
    ├══════════════════════════════╡
    │  Bottom electrode            │
    └──────────────────────────────┘

    Key equation: C = epsilon_0 * epsilon_r * A / d

    DRY polymer:   epsilon_r ~ 3-5       C ~ 180 pF (typical)
    WET polymer:   epsilon_r increases    C ~ 200 pF
    (Water has epsilon_r ~ 80, so even small
     amounts of absorbed water raise epsilon_r)
```

The polymer reaches equilibrium with the surrounding air's relative humidity. More moisture in the air means more water molecules absorbed, which means a higher effective dielectric constant, which means higher capacitance. A typical sensor might swing from ~180 pF (dry) to ~200 pF (saturated) -- a change of roughly 0.1-0.5 pF per %RH.

### Step 2: Heat changes thermistor resistance (temperature sensing)

The NTC thermistor is a ceramic semiconductor. At higher temperatures, thermal energy kicks more electrons from the valence band into the conduction band, creating additional charge carriers. More carriers means lower resistance.

```
NTC THERMISTOR RESISTANCE vs. TEMPERATURE
==============================================================================

    Resistance
    (ohms)
        |
   100k |--x
        |    \
    50k |     \
        |      \
    25k |       x
        |        \
    10k |         --x
        |             ---x
     5k |                  ----x----x----
        +----+----+----+----+----+----+-----> Temperature
           -20    0    25   50   75  100  (C)

    The relationship is exponential, described by:

    R(T) = R_25 * exp[ B * (1/T - 1/298.15) ]

    Where:
      R_25  = resistance at 25C (e.g. 10 kohm)
      B     = material constant (typically 3000-5000 K)
      T     = temperature in Kelvin

    EXAMPLE: 10 kohm NTC with B = 3950
      At  0C (273 K): R ~ 33.6 kohm
      At 25C (298 K): R = 10.0 kohm  (reference point)
      At 50C (323 K): R ~ 3.6 kohm
```

The sensor IC measures this resistance (typically by passing a known current and measuring the voltage, or using an RC timing circuit) and applies the Steinhart-Hart equation for accurate conversion to temperature:

$$\frac{1}{T} = A + B \ln(R) + C [\ln(R)]^3$$

### Step 3: The ADC digitizes both signals

The sensor IC contains an [[micro-context/adc-analog-to-digital-converter|ADC]] that converts both analog measurements into digital numbers. For the capacitance measurement, modern sensors use a sigma-delta capacitance-to-digital converter (CDC):

```
SIGMA-DELTA CAPACITANCE-TO-DIGITAL CONVERTER
==============================================================================

    C_sensor ──┐
               │     ┌────────────┐     ┌────────────┐     ┌─────────┐
               ├────>│ Charge     │────>│ Comparator │────>│ Digital │
               │     │ Integrator │     │ (1-bit)    │     │ Filter  │──> 16-bit
    C_ref ─────┘     └────────────┘     └────────────┘     └─────────┘   result
                          │                    │
                          │                    │
                          └────────────────────┘
                            Feedback loop balances
                            charge from C_sensor vs C_ref

    How it works:
    1. Switches alternately pump charge from C_sensor and C_ref
       into an integrator (Q = C * V, so charge ~ capacitance)
    2. Comparator outputs a 1-bit stream: density of 1s encodes
       the ratio C_sensor / C_ref
    3. Digital decimation filter extracts a stable 16-bit number
       from the bit stream

    Resolution: 16-bit = 65,536 levels
    Over a 0-100% RH range, that's ~0.0015% RH per step
    (far finer than the sensor's ~1-2% accuracy)
```

The temperature ADC works similarly but measures voltage from the thermistor (or in modern sensors like the SHT40, from a bandgap temperature sensor built into the silicon).

### Step 4: Calibration and compensation

Raw ADC counts don't mean anything without calibration. During factory manufacturing, each sensor is exposed to known humidity and temperature references. Correction coefficients are stored in on-chip non-volatile memory.

```
FROM RAW ADC COUNTS TO CALIBRATED OUTPUT
==============================================================================

    Raw capacitance count ──┐
                            │     ┌──────────────────────┐
    Raw temperature count ──┼────>│ Calibration Engine   │
                            │     │                      │──> Humidity (%RH)
    Stored coefficients ────┘     │ 1. Apply polynomial  │──> Temperature (C)
    (factory-programmed)          │    correction         │
                                  │ 2. Cross-compensate  │
                                  │    (humidity depends  │
                                  │    on temperature)    │
                                  └──────────────────────┘

    Why cross-compensation matters:
      Water's dielectric constant is temperature-dependent
      (epsilon_r ~ 87 at 0C, ~ 80 at 20C, ~ 55 at 100C)

      Without temperature correction, humidity readings
      can drift 8+ %RH across the operating range
```

### Step 5: Digital readout over I2C

The microcontroller requests a measurement over [[micro-context/i2c|I2C]]. The sensor performs the conversion internally and returns calibrated data.

```
I2C COMMUNICATION SEQUENCE (e.g. SHT40 at address 0x44)
==============================================================================

    MCU (Master)                      Sensor (Slave 0x44)
        |                                   |
        |── START + [0x44 + W] ────────────>|
        |<──────────────────────── ACK ─────|
        |── [0xFD = "measure, high prec"] ─>|
        |<──────────────────────── ACK ─────|
        |── STOP ──────────────────────────>|
        |                                   |
        |        (sensor measures            |
        |         ~8.2 ms conversion time)   |
        |                                   |
        |── START + [0x44 + R] ────────────>|
        |<──────────────────────── ACK ─────|
        |<── [Temp MSB] ────────────────────|
        |── ACK ───────────────────────────>|
        |<── [Temp LSB] ────────────────────|
        |── ACK ───────────────────────────>|
        |<── [Temp CRC-8] ─────────────────|
        |── ACK ───────────────────────────>|
        |<── [Hum MSB] ────────────────────|
        |── ACK ───────────────────────────>|
        |<── [Hum LSB] ────────────────────|
        |── ACK ───────────────────────────>|
        |<── [Hum CRC-8] ──────────────────|
        |── NACK + STOP ──────────────────>|
        |                                   |

    6 bytes total: 2 temp + 1 CRC + 2 humidity + 1 CRC

    Conversion formulas:
      T (C) = -45 + 175 * (temp_raw / 65535)
      RH (%) = -6 + 125 * (hum_raw / 65535)
```

## The Result

```
COMPLETE SIGNAL CHAIN: FROM AIR TO DIGITAL NUMBER
==============================================================================

    Physical         Transducer         Electrical       ADC         Digital
    quantity                            signal                       output
    ─────────       ──────────         ──────────      ─────       ───────

    Humidity  ───>  Polymer film  ───>  ~180-200 pF ──> CDC ──> 0x7A5B
    (% RH)          (capacitor)         (capacitance)            = 55.3% RH

    Temperature ──> NTC thermistor ──>  ~3-30 kohm ──> ADC ──> 0x6732
    (degrees C)     (resistor)          (resistance)            = 23.4 C

    Both values sent as 16-bit integers over I2C to the MCU
```

## Why Each Piece Matters

- **Polymer dielectric:** Translates an invisible quantity (water vapor concentration) into a measurable electrical property (capacitance). Without it, there's no electrical signal to work with.
- **NTC thermistor:** Translates temperature into resistance. Also essential for compensating the humidity reading, since the polymer's dielectric response is temperature-dependent.
- **On-chip ADC:** Bridges the analog and digital worlds. The sigma-delta architecture achieves 16-bit resolution from tiny capacitance changes (fractions of a picofarad).
- **I2C interface:** Delivers clean, calibrated digital numbers to the microcontroller over just two wires, immune to the analog noise that would corrupt raw sensor signals over long traces.

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/adc-analog-to-digital-converter]] -- How analog voltages become digital numbers
- [[micro-context/i2c]] -- The 2-wire bus protocol sensors use to talk to microcontrollers

**Full treatment (10 minutes):**
- [[quick-context/capacitance]] -- Dielectric constants, the parallel-plate equation, and parasitic capacitance
- [[quick-context/capacitor]] -- Types, charge/discharge behavior, RC time constants
- [[quick-context/resistor]] -- Ohm's law, voltage dividers, pull-up resistors for I2C
