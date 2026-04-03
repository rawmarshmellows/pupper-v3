---
case: IMU Orientation Sensing for Robot Balance
components: [pupper-brain, pupper-bom-control-board]
created: 2026-03-28
---

# Case: IMU Orientation Sensing for Robot Balance

> **Components:** [[quick-context/pupper-brain]] | [[quick-context/pupper-bom-control-board]]
> **Micro-context:** [[micro-context/i2c]] | [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/stm32-microcontroller]] | [[micro-context/homogeneous-transformation-matrix]]

> **In brief:** A walking robot must know which way is "up" at all times. The BNO086 [[micro-context/microcontroller|IMU]] on the Pupper's control board combines three MEMS sensors — accelerometer, gyroscope, and magnetometer — through on-chip sensor fusion to produce a drift-corrected quaternion orientation. This quaternion flows over [[micro-context/i2c|I2C]] to the main [[micro-context/stm32-microcontroller|STM32]] every millisecond, where it feeds the balance controller that keeps the robot from falling over.

## The Situation

When the Pupper trots, each stride tilts the body in roll, pitch, and yaw. The balance controller needs to know the current orientation to compute corrective joint angles — but no single sensor can measure orientation reliably. Accelerometers are noisy and fooled by motion. Gyroscopes drift over time. The BNO086 solves this by fusing all three sensor types on-chip, giving the robot a stable "which way is up" signal at up to 400 Hz (full rotation vector with magnetometer) or 1000 Hz (gyro rotation vector, accel + gyro only).

## The Pieces

**MEMS Accelerometer:** A microscopic proof mass suspended on silicon springs, with comb-like fingers that form tiny [[quick-context/capacitor|capacitors]] using air as the dielectric. When the chip accelerates, the proof mass shifts, changing the air gap ($d$) between interleaved fingers. Since [[quick-context/capacitance|$C = \varepsilon A / d$]], the capacitance changes — and a differential readout ($\Delta C = C_1 - C_2$) gives a signal proportional to acceleration while canceling thermal drift. This is the same "subtract to cancel noise" principle used in [[quick-context/can-bus|CAN bus]] differential signaling. Gravity always pulls at $9.8\text{ m/s}^2$ downward, so at rest the accelerometer tells you exactly which direction is "down." [[small-context/mems-accelerometer-capacitive-sensing|Full capacitive sensing walkthrough →]]

**MEMS Gyroscope:** A vibrating structure on silicon that exploits the [[micro-context/coriolis-effect|Coriolis effect]] — electrostatic comb drives oscillate a proof mass at ~10–30 kHz, and when the chip rotates, the Coriolis force deflects the mass sideways by nanometers, detected as a differential [[quick-context/capacitance|capacitance]] change proportional to angular velocity. Measures rotation rate in degrees/second on three axes. Fast and responsive, but readings accumulate small errors over time (drift) from flicker noise, thermal noise, and fabrication imperfections — after a few minutes of pure gyro integration, "level" might be off by several degrees. [[small-context/mems-gyroscope-vibration-drift|Full walkthrough: vibration, drift, and correction →]]

**Magnetometer:** Senses the direction of Earth's magnetic field, providing an absolute heading reference (compass bearing). Unlike the gyroscope, it doesn't drift — but it's slow, noisy, and easily distorted by nearby motors and wires.

**Sensor Fusion (BNO086's Cortex-M0+ processor):** An on-chip algorithm that continuously blends all three sensors. It trusts the gyroscope for fast, short-term motion and uses the accelerometer and magnetometer to correct long-term drift. The output is a quaternion — four numbers $(x, y, z, w)$ that unambiguously represent 3D orientation without the singularities of Euler angles.

## Step by Step: What Happens

### Step 1: Three sensors measure simultaneously

At each sample interval (up to 400 Hz for the full rotation vector, or 1000 Hz for the gyro-only variant), the BNO086's three MEMS sensors produce raw readings:

```
RAW SENSOR OUTPUTS (one sample):

  Accelerometer (m/s²):     Gyroscope (°/sec):     Magnetometer (μT):
  ax = +0.15                gx = -2.3              mx = +22.1
  ay = -0.08                gy = +0.7              my = -15.4
  az = -9.79                gz = +0.1              mz = +41.2
  │                         │                      │
  └─ gravity dominates      └─ rotation rates      └─ Earth's field
     az ≈ -9.8 → chip is       small → robot is      absolute heading
     roughly level              turning slowly         reference
```

The accelerometer shows $a_z \approx -9.8\text{ m/s}^2$ — nearly pure gravity — meaning the robot is roughly level. Small $a_x$ and $a_y$ components indicate a slight tilt.

### Step 2: Sensor fusion combines short-term and long-term accuracy

The BNO086's on-chip processor runs a complementary/Kalman-style filter that blends the three inputs:

```
SENSOR FUSION — WHY EACH SENSOR MATTERS:

  Time scale:   Milliseconds          Seconds           Minutes+
                ◄──────────────────────────────────────────────►

  Gyroscope:    ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                excellent               drifts badly
                (fast, smooth)          (cumulative error)

  Accelerometer:░░░░░░░░░░░░████████████████████████████████████
                noisy                   excellent
                (vibration, motion)     (gravity = truth)

  Magnetometer: ░░░░░░░░░░░░░░░░░░░░░░░████████████████████████
                very noisy              good for heading
                (motor interference)    (Earth's field = truth)

  FUSED OUTPUT: ████████████████████████████████████████████████
                smooth, responsive, drift-free across all time scales
```

- **Short term (< 1 second):** The fusion algorithm trusts the gyroscope — it's smooth and responsive, perfect for tracking rapid tilt changes during a stride.
- **Long term (> 1 second):** Gravity measured by the accelerometer gradually corrects gyro drift in pitch and roll. The magnetometer corrects yaw drift using Earth's magnetic field.
- **Result:** A quaternion $(x, y, z, w)$ that is both fast-responding AND drift-free.

### Step 3: Quaternion travels over I2C to the main STM32

The fused quaternion is read by the main MCU (U1, STM32F446) over the [[micro-context/i2c|I2C]] bus at 400 kHz:

```
BNO086 (U15)                        STM32 (U1)
┌──────────────┐    I2C @ 400kHz    ┌─────────────┐
│  Accel       │    SDA ───────────→│             │
│  Gyro    ───►│    SCL ───────────→│  State      │
│  Mag     Fusion   (2 wires +     │  Estimator  │
│          ───►│     pull-ups)      │             │
│    Quaternion│                    │  q = (x,y,  │
│   (x,y,z,w) │                    │      z,w)   │
└──────────────┘                    └──────┬──────┘
                                          │
                                          ▼
                                    Balance Controller
```

The I2C transaction transfers the quaternion (four 16-bit fixed-point components) wrapped in CEVA's SHTP protocol headers — roughly 20+ bytes total, taking ~0.5 ms at 400 kHz. Pull-up resistors (R18, R21 on the [[quick-context/pupper-bom-control-board|control board]]) hold the SDA/SCL lines high between transactions.

### Step 4: Balance controller corrects the robot's posture

The quaternion feeds into U1's state estimator, which combines it with motor encoder feedback to know the full robot pose. The balance controller then computes corrective joint angles:

```
1 ms CONTROL LOOP — IMU'S ROLE:

  ┌────────┐    quaternion    ┌──────────┐    joint     ┌──────────┐
  │ BNO086 ├─────────────────►│   U1     │   targets   │   U5     │
  │  IMU   │    (I2C)        │  State   ├────────────►│  Motor   │
  └────────┘                 │  Est +   │   (SPI)     │  MCU     │
                             │  Balance │             │          │
  ┌────────┐    encoder      │  Control │             │  CAN TX  │
  │ Motors ├─────────────────►│          │             │  → 12    │
  │(via CAN)│   feedback     └──────────┘             │  servos  │
  └────────┘                                          └──────────┘

  Example: Robot tilts 3° forward
  → IMU quaternion shows pitch change
  → Balance controller shifts weight backward
  → Front legs extend, rear legs contract
  → Robot returns to level within ~50 ms
```

## The Result

From three noisy, incomplete sensor streams, the BNO086 produces a single clean orientation signal. The robot knows which way is "up" within ~2° static accuracy (per the BNO086 datasheet), updated hundreds of times per second. Without this, the Pupper would have no idea it was tilting and would fall over on its first step.

```
WITHOUT IMU:                          WITH IMU:

  Robot tilts →  No correction         Robot tilts →  IMU detects
                 →  Falls over                        →  Controller corrects
                                                      →  Stays balanced

  Gyro alone:   Drifts after           Fused:  Stable for hours
                10-30 seconds                   (drift-corrected)

  Accel alone:  Jittery, fooled        Fused:  Smooth, responsive
                by walking vibration           (gyro for fast motion)
```

## Why Each Piece Matters

- **Accelerometer:** Provides the gravity reference — without it, the gyroscope would drift and "level" would slowly rotate away from reality.
- **Gyroscope:** Provides fast, smooth rotation tracking — without it, the accelerometer alone would be too jittery and too slow for balance during walking.
- **Magnetometer:** Provides absolute heading — without it, yaw would drift over time (the robot would slowly lose track of which direction it's facing).
- **On-chip fusion:** Offloads the computationally expensive filtering from the STM32, freeing U1's CPU for the balance controller and state estimator.
- **I2C bus:** Delivers the quaternion with only 2 wires and 2 pull-up resistors — simple and reliable for the short on-board distance.

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/i2c]] — 2-wire serial bus connecting the BNO086 to the STM32
- [[micro-context/stm32-microcontroller]] — The ARM Cortex-M4 MCU that reads the IMU
- [[micro-context/adc-analog-to-digital-converter]] — How the MEMS sensors digitize analog measurements
- [[micro-context/homogeneous-transformation-matrix]] — The $4 \times 4$ matrices used in the kinematics that consume IMU orientation data
- [[micro-context/microcontroller]] — What an MCU is and why robots use them

**Full treatment (10 minutes):**
- [[quick-context/pupper-brain]] — Full architecture of the dual-MCU + Raspberry Pi system
- [[quick-context/pupper-bom-control-board]] — Every component on the board, including the BNO086's sourcing challenges
- [[quick-context/pupper-lab4-gait-control]] — How IMU data integrates with the trotting gait controller
- [[quick-context/pupper-lab1-pid-control]] — The PD control loop that uses IMU-informed joint targets
