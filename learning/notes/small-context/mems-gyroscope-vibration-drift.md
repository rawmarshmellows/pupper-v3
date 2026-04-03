---
case: MEMS Gyroscope — Vibration, Drift, and Correction
components: [pupper-bom-control-board, capacitance, capacitor]
created: 2026-03-28
---

# Case: MEMS Gyroscope — Vibration, Drift, and Correction

> **Components:** [[quick-context/pupper-bom-control-board]] | [[quick-context/capacitance]] | [[quick-context/capacitor]]
> **Micro-context:** [[micro-context/coriolis-effect]] | [[micro-context/piezoelectric-effect]] | [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/i2c]]

> **In brief:** A MEMS gyroscope measures rotation rate by continuously vibrating a silicon proof mass using electrostatic [[quick-context/capacitance|comb drives]], then detecting the [[micro-context/coriolis-effect|Coriolis]]-induced sideways deflection when the chip rotates. The deflection is tiny (nanometers) and measured as a differential capacitance change. Drift accumulates because of thermal noise, flicker noise in the electronics, and fabrication imperfections — corrected by fusing gyro data with accelerometer and magnetometer readings via complementary or Kalman filters.

## The Situation

The [[small-context/imu-robot-balance-sensing|Pupper's BNO086 IMU]] contains a MEMS gyroscope that measures angular velocity on three axes. But the one-paragraph description — "a vibrating structure exploiting the Coriolis effect" — hides several non-obvious mechanisms. How does a chip *vibrate* a piece of silicon? Why does that vibration let it sense rotation? And why does the reading drift over time?

## The Pieces

**Electrostatic Comb Drives:** Two sets of interleaved silicon "fingers" — one fixed, one attached to the proof mass. Applying an AC voltage creates alternating electrostatic forces that push-pull the mass back and forth at its mechanical resonant frequency (~10–30 kHz). Same principle as [[quick-context/capacitance|capacitive sensing]] in the accelerometer, but run in reverse: instead of measuring capacitance change, you *apply* voltage to create motion.

**Proof Mass (Tuning Fork):** Most designs use two proof masses vibrating in anti-phase (toward each other, then apart) — a tuning fork configuration. This differential motion cancels linear acceleration (both masses move the same way under shock) while doubling the Coriolis signal (masses deflect in opposite directions when rotating).

**Capacitive Sense Electrodes:** Interleaved fingers on the sense axis that form a differential [[quick-context/capacitor|capacitor]] pair. When the [[micro-context/coriolis-effect|Coriolis force]] deflects the proof mass sideways, one gap shrinks (C₁ increases) while the opposite gap grows (C₂ decreases). The readout circuit measures $\Delta C = C_1 - C_2$, which is proportional to angular velocity.

**Readout ASIC:** The charge-sensitive amplifier and [[micro-context/adc-analog-to-digital-converter|ADC]] that convert femtofarad-scale capacitance changes into digital angular velocity readings (degrees/second).

## Step by Step: What Happens

### Step 1: Comb drives vibrate the proof mass

The drive circuit applies an AC voltage to the comb-drive electrodes, exciting the proof mass into steady oscillation along the **drive axis** at the structure's mechanical resonant frequency. The resonance amplifies displacement by the quality factor $Q$ (10,000–100,000 in vacuum-packaged devices), so a small voltage produces a large, stable vibration amplitude of ~1 $\mu$m.

```
ELECTROSTATIC COMB DRIVE — TOP VIEW (one side)

  Fixed         Movable (on proof mass)
  fingers       fingers
    ║             ║
    ║   ◄──gap──► ║
    ║             ║            AC voltage applied:
    ║             ║            push-pull force oscillates
    ║             ║            mass at resonant frequency
    ║             ║
    ║             ║
    ╠══springs════╣
    substrate    (silicon flexures connect mass to substrate)

  Two sets on opposite sides operate in push-pull:
  when left pulls, right pushes → clean sinusoidal motion

  Drive frequency:  ~10–30 kHz (set by geometry + mass)
  Amplitude:        ~1 μm (amplified by Q in vacuum)
  Quality factor:   10,000–100,000 (vacuum-packaged)
```

Two feedback loops work in parallel to sustain the oscillation. A **phase-locked loop (PLL)** tracks the resonant frequency and locks the drive signal's phase to it — ensuring the push always arrives at exactly the right moment. An **automatic gain control (AGC)** loop monitors the drive amplitude via capacitive sensing and adjusts drive voltage to keep the oscillation constant — like controlling how hard you push a swing each cycle.

### Step 2: Rotation creates a Coriolis force on the sense axis

When the chip rotates about an axis perpendicular to the drive motion, the vibrating proof mass experiences the [[micro-context/coriolis-effect|Coriolis force]]:

$$F_{\text{Coriolis}} = -2m(\vec{\omega} \times \vec{v}_{\text{drive}})$$

Since the drive velocity is sinusoidal ($v = A \cdot \omega_d \cdot \cos(\omega_d t)$), the Coriolis force is also sinusoidal **at the drive frequency**, with an amplitude proportional to the rotation rate $\Omega$. This is the key: the signal you're looking for oscillates at a known frequency, making it easy to extract from noise via demodulation.

```
THREE ORTHOGONAL AXES:

           Z (yaw)
           │
           │    Rotation ω about Z
           │    ─── ─── ───►
           │
           │         Coriolis force
           │         ▼ (along Y)
    ───────┼──────────────────── X (drive axis)
           │     ◄══════════►
           │     proof mass vibrates
           │     along X
           │
           Y (sense axis)

  Drive: mass vibrates along X with velocity v
  Rotate: chip turns about Z with rate ω
  Result: Coriolis force deflects mass along Y
          F_y = -2m(ω_z × v_x)

  The cross product ω × v always points perpendicular
  to both — that's why drive and sense axes must be orthogonal.
```

### Step 3: Sense electrodes detect the deflection as a capacitance change

The Coriolis-induced displacement along the sense axis is **extremely small** — on the order of nanometers for typical rotation rates. The capacitive sense electrodes detect this via differential measurement:

```
DIFFERENTIAL CAPACITIVE SENSING (sense axis, top-down)

  AT REST (no rotation):

    Fixed       Proof mass      Fixed
    sense       fingers         sense
    electrode                   electrode
      ║           ║    ║          ║
      ║    d₁     ║    ║    d₂    ║     d₁ = d₂
      ║◄─────────►║    ║◄────────►║     C₁ = C₂
      ║           ║    ║          ║     ΔC = 0
      ║           ║    ║          ║

  CHIP ROTATING (Coriolis deflects mass toward left):

      ║         ║        ║            ║
      ║  d₁↓   ║        ║    d₂↑     ║   Mass shifts left
      ║◄───────►║        ║◄──────────►║
      ║         ║        ║            ║   d₁ shrinks → C₁ UP
      ║         ║        ║            ║   d₂ grows   → C₂ DOWN
                                          ΔC ∝ angular velocity Ω

  Sense-axis displacement at 1 deg/s:  ~nanometers
  Capacitance change:  sub-femtofarads (10⁻¹⁶ F)
  Detected by charge-sensitive amplifier + demodulator
```

The readout circuit uses **synchronous demodulation** (lock-in detection) — it multiplies the sense signal by a reference at the drive frequency. Since the Coriolis signal oscillates at exactly the drive frequency and is in phase with the drive velocity, this extracts the angular velocity signal while rejecting noise at all other frequencies. **Quadrature error** (a false signal 90 degrees out of phase, caused by fabrication imperfections) is also rejected because it's at the wrong phase.

### Step 4: Tuning fork rejects linear acceleration

The two proof masses vibrate in anti-phase. This is critical for rejecting false signals:

```
TUNING FORK — WHY TWO MASSES?

  VIBRATING (no rotation, no shock):

    Mass A  ◄════►        ►════◄  Mass B
    (moves left)          (moves right)
    Anti-phase: always opposite directions

  ROTATION (Coriolis force):

    Mass A     ▲           ▼     Mass B      DIFFERENTIAL:
    deflects   │           │     deflects     Coriolis pushes them
    UP         │           │     DOWN         in OPPOSITE directions
                                              → ΔC doubles (2× signal)

  LINEAR ACCELERATION (shock, vibration):

    Mass A     ►           ►     Mass B      COMMON-MODE:
    shifts     │           │     shifts       Both move SAME direction
    RIGHT      │           │     RIGHT        → ΔC cancels (0 signal)

  Result: The differential output contains only rotation,
  not linear acceleration or vibration artifacts.
```

## The Result

The ASIC outputs a digital angular velocity reading (deg/s) for each axis — updated at the sensor's output data rate (up to 400 Hz for most outputs, or 1000 Hz for the gyro-integrated rotation vector). The BNO086 on the Pupper runs three of these sense structures (one per axis) and feeds the raw gyro readings into its on-chip sensor fusion algorithm.

## Why Gyroscopes Drift (And How to Fix It)

### Sources of Drift

Drift is the slow accumulation of error when you **integrate** angular velocity to get angle. Even tiny biases in the gyro output compound over time: a constant bias of just 1 deg/hr means 1 degree of error per hour.

```
DRIFT ACCUMULATION:

  True angular velocity:  0 deg/s (stationary chip)
  Gyro output:            0.01 deg/s (tiny bias)
                          │
                          ▼
  Integrated angle error over time:

  Time:     0     1 min    10 min    1 hr
  Error:    0°    0.6°     6°        36°
            ▲     ▲        ▲         ▲
            │     │        │         └─ Unusable without correction
            │     │        └─ Noticeable tilt error
            │     └─ Already significant for balance
            └─ Perfect at start
```

The physical and electronic sources:

| Source | Mechanism | Typical magnitude |
|--------|-----------|-------------------|
| **Bias instability** | 1/f (flicker) noise in the readout electronics — slow random wandering of the zero-rate output | 3–65 deg/hr (consumer) |
| **Angle random walk** | Brownian motion of gas molecules hitting the proof mass + Johnson noise in electronics | 0.5–2 deg/$\sqrt{\text{hr}}$ (consumer) |
| **Temperature sensitivity** | Resonant frequency shifts ~90 mHz/deg C; Young's modulus of silicon changes; thermal stress from CTE mismatch between die, bond, and PCB | ~5 mdps/deg C offset shift |
| **Quadrature error** | Imperfect etching creates slight misalignment between drive and sense axes, coupling drive motion into the sense channel | Compensated by demodulation + DC trim electrodes |
| **Fabrication tolerances** | Sidewall angle errors, thickness variations change spring constants → unpredictable frequency mismatch between drive and sense modes | Compensated by electrostatic tuning |

### Sensor-Level Corrections

- **Factory calibration:** Thermal sweep in a climatic chamber measures bias vs. temperature; polynomial coefficients stored in on-chip memory for real-time compensation.
- **Quadrature trim electrodes:** DC voltages null out the quadrature coupling mechanically.
- **Mode matching:** Electrostatic tuning voltages bring drive and sense resonant frequencies closer together (to within 0.005 Hz in advanced designs), maximizing sensitivity.

### System-Level Correction: Sensor Fusion

This is the critical fix. No amount of sensor-level calibration eliminates drift entirely — you need an external reference. The [[small-context/imu-robot-balance-sensing|BNO086's on-chip fusion]] blends gyro, accelerometer, and magnetometer:

```
COMPLEMENTARY FILTER (simplest fusion):

  angle = α × (angle + gyro_rate × dt) + (1-α) × accel_angle
          ▲                                  ▲
          │                                  │
          High-pass on gyro                  Low-pass on accelerometer
          (trust fast changes)               (trust gravity long-term)

  α ≈ 0.96–0.98

  When α = 1:  pure gyro integration (fast but drifts)
  When α = 0:  pure accelerometer (stable but jittery)
  Blended:     fast response + zero long-term drift


KALMAN FILTER (optimal estimation):

  State vector: [roll, pitch, yaw, gyro_bias_x, gyro_bias_y, gyro_bias_z]
                                    ▲
                                    │
                The filter continuously ESTIMATES the gyro bias
                and subtracts it from measurements in real time

  1. PREDICT:  Use gyro to propagate orientation forward (fast, ~1 ms)
  2. UPDATE:   Use accel/mag to correct prediction (slower, absolute ref)
  3. REPEAT:   Bias estimate converges → drift eliminated
```

The key insight: the accelerometer measures gravity (which doesn't drift) and the magnetometer measures Earth's magnetic field (which doesn't drift). Neither is fast enough for balance control alone, but they provide the absolute reference that the gyroscope lacks. The fusion algorithm trusts the gyro for millisecond-to-millisecond changes and uses the accel/mag to slowly correct cumulative bias — exactly what the [[small-context/imu-robot-balance-sensing|Pupper's balance controller]] relies on.

## Why Each Piece Matters

- **Comb drives:** Convert electrical energy into mechanical vibration — without the reference motion, there's no Coriolis force to detect
- **Tuning fork (dual mass):** Rejects linear acceleration, doubling rotation sensitivity while eliminating false signals from walking vibration
- **Capacitive sensing:** Detects sub-nanometer deflections as differential capacitance changes — the only practical way to measure such tiny displacements on-chip
- **Synchronous demodulation:** Extracts the Coriolis signal at the known drive frequency, rejecting broadband noise and quadrature error
- **Sensor fusion:** Eliminates drift by anchoring the gyro's fast-but-drifting output to the accelerometer's slow-but-stable gravity reference

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/coriolis-effect]] — The pseudo-force that deflects moving objects in rotating frames
- [[micro-context/piezoelectric-effect]] — Alternative drive mechanism to electrostatic comb drives
- [[micro-context/adc-analog-to-digital-converter]] — How the analog capacitance change becomes a digital reading
- [[micro-context/i2c]] — The bus carrying gyro data to the main MCU

**Full treatment (10 minutes):**
- [[quick-context/capacitance]] — Why $C = \varepsilon A / d$ governs both drive and sense in MEMS gyroscopes
- [[quick-context/capacitor]] — Differential capacitor pairs used in the sense electrodes
- [[quick-context/thermal-noise-electronics]] — The fundamental noise floor that limits gyro sensitivity
- [[quick-context/pupper-bom-control-board]] — The BNO086 IMU and its place on the Pupper's board

**Related walkthroughs:**
- [[small-context/imu-robot-balance-sensing]] — How the fused IMU output feeds the Pupper's balance controller
