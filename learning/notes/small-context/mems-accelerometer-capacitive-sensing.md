---
case: MEMS Accelerometer Capacitive Sensing
components: [capacitor, capacitance]
created: 2026-03-28
---

# Case: MEMS Accelerometer Capacitive Sensing

> **Components:** [[quick-context/capacitor]] | [[quick-context/capacitance]]
> **Micro-context:** [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/mosfet]]
> **Used in:** [[small-context/imu-robot-balance-sensing]] | [[quick-context/pupper-bom-control-board]]

> **In brief:** A MEMS accelerometer measures acceleration by detecting femtofarad-scale [[quick-context/capacitance|capacitance]] changes between microscopic interleaved comb fingers. A proof mass suspended on silicon springs shifts when accelerated, changing the air gap between its fingers and fixed electrodes. The chip reads the *difference* between two capacitances on opposite sides -- the same "subtract to cancel noise" principle that makes [[quick-context/can-bus|CAN bus]] differential signaling immune to electromagnetic interference.

https://www.youtube.com/watch?v=KuekQ-m9xpw

## The Situation

A robot needs to know which way is "down" and how fast it's accelerating. Gravity is always present at $9.8\text{ m/s}^2$, so a sensor that measures acceleration also measures the direction of gravity. But the physical displacement caused by gravity on a microscopic proof mass is *nanometers*. You need a transduction mechanism that converts nanometer motion into an electrical signal -- and capacitive sensing is ideal because it's simple to integrate on-chip, requires no external optics, and consumes very little power. [[quick-context/capacitance|Capacitance]] -- where $C = \varepsilon A / d$ makes the signal inversely proportional to gap distance -- provides exactly this.

## The Pieces

**Proof mass:** A block of silicon (~micrograms) etched from the chip substrate, suspended on thin silicon flexures (springs). It moves freely along one axis when the chip accelerates. Newton's second law: the proof mass's inertia resists the acceleration, so it shifts *opposite* the direction of motion.

**Comb fingers:** Interleaved finger electrodes -- some attached to the proof mass, some fixed to the substrate. They form parallel-plate [[quick-context/capacitor|capacitors]] where the dielectric is the **air** (or inert gas) sealed inside the MEMS package. No solid insulator -- just a ~2 $\mu$m air gap between each finger pair.

**Differential capacitor pair:** Fixed fingers on *both* sides of each proof mass finger create two capacitances: $C_1$ (left gap) and $C_2$ (right gap). When the proof mass shifts, one gap shrinks and the other grows, producing opposite capacitance changes.

**Readout ASIC:** A charge-sensitive amplifier circuit on the same chip that measures $\Delta C = C_1 - C_2$ and converts it to a digital acceleration value via an [[micro-context/adc-analog-to-digital-converter|ADC]].

## Step by Step: What Happens

### Step 1: At rest -- balanced capacitances

With no acceleration, the proof mass sits centered. Both air gaps are equal, so both capacitances are equal:

```
TOP-DOWN VIEW — ONE AXIS OF COMB FINGERS (at rest)
==============================================================================

    Fixed          Proof mass         Fixed
    electrode       fingers           electrode
      ║              ║   ║              ║
      ║     d₁       ║   ║     d₂       ║
      ║◄────────────►║   ║◄────────────►║
      ║    air gap   ║   ║   air gap    ║
      ║              ║   ║              ║
      ║              ╠═══╣              ║
      ║              springs            ║
      ║              (flexures)         ║

    C₁ = εA/d₁       d₁ = d₂ = ~2 μm       C₂ = εA/d₂
    C₁ = C₂  →  ΔC = 0  →  output = 0g
```

### Step 2: Acceleration shifts the proof mass

When the chip accelerates left, inertia pushes the proof mass right (like your body pressing into the car seat when the car accelerates forward):

```
PROOF MASS SHIFTED RIGHT BY ACCELERATION (or gravity)
==============================================================================

      ║           ║        ║                ║
      ║   d₁ ↓   ║        ║     d₂ ↑      ║
      ║◄─────────►║        ║◄─────────────►║
      ║  smaller  ║        ║    larger      ║
      ║   gap     ║        ║     gap        ║
      ║           ╠════════╣                ║
                  springs stretched/compressed

    d₁ shrinks  →  C₁ = εA/d₁  INCREASES    (closer plates = more C)
    d₂ grows    →  C₂ = εA/d₂  DECREASES    (farther plates = less C)

    ΔC = C₁ - C₂  ≠ 0  →  proportional to displacement  →  ∝ acceleration
```

The displacement from 1g of gravity is only ~nanometers on a ~2 $\mu$m gap -- a relative change of roughly 0.1%. But the readout circuit resolves this because it measures the *difference* between two capacitances, not an absolute value.

### Step 3: Differential readout cancels common-mode noise

Here's where the connection to [[quick-context/can-bus|CAN bus]] becomes clear. Both systems use the same principle: **measure the difference between two matched signals so that anything affecting both equally cancels out.**

```
THE DIFFERENTIAL PRINCIPLE — SAME IDEA, TWO DOMAINS
==============================================================================

MEMS ACCELEROMETER (capacitance domain):
─────────────────────────────────────────────────────────────────────

    C₁ and C₂ share the same chip, same temperature, same aging.

    Temperature rises 10°C:
      C₁ drifts +0.3 fF    (thermal expansion changes both gaps equally)
      C₂ drifts +0.3 fF

      ΔC = (C₁ + 0.3) - (C₂ + 0.3) = C₁ - C₂    ← drift CANCELS

    Acceleration of 1g:
      C₁ changes +0.5 fF   (proof mass shifts toward this side)
      C₂ changes -0.5 fF   (proof mass shifts away from this side)

      ΔC = (C₁ + 0.5) - (C₂ - 0.5) = C₁ - C₂ + 1.0 fF  ← signal DOUBLES


CAN BUS (voltage domain):
─────────────────────────────────────────────────────────────────────

    CANH and CANL run through the same twisted-pair cable.

    Motor EMI injects +200 mV noise:
      CANH picks up +200 mV
      CANL picks up +200 mV    (same cable, same noise)

      V_diff = CANH - CANL     ← noise CANCELS (common-mode rejection)

    Transmitter sends a dominant bit:
      CANH driven to +3.5V
      CANL driven to +1.5V     (opposite directions)

      V_diff = 3.5 - 1.5 = +2V  ← signal preserved


THE PATTERN:
─────────────────────────────────────────────────────────────────────

    "Differential" = measure (Signal_A - Signal_B)

    Noise that hits both equally:     cancels     (common-mode rejection)
    Signal that moves them opposite:  doubles     (differential-mode gain)

    Accelerometer:  ΔC = C₁ - C₂     (capacitance difference)
    CAN bus:        ΔV = CANH - CANL  (voltage difference)
    Strain gauge:   ΔR = R₁ - R₂     (Wheatstone bridge, same idea)
    Differential amplifier:  V_out = A × (V+ - V-)
```

### Step 4: ADC digitizes the capacitance difference

The readout ASIC applies AC excitation voltages to the fixed electrodes and measures the resulting charge flow, which is proportional to $\Delta C$. An on-chip [[micro-context/adc-analog-to-digital-converter|ADC]] (typically switched-capacitor or sigma-delta) converts this to a digital value representing acceleration in $\text{m/s}^2$.

Three orthogonal copies of this entire structure (X, Y, Z axes) are etched on the same silicon die, giving full 3-axis acceleration sensing in a chip a few mm across.

## The Result

From a nanometer-scale mechanical displacement, the accelerometer produces a clean digital acceleration reading -- typically at 12-16 bit resolution, sampled hundreds or thousands of times per second. When the chip is still, the Z-axis reads $-9.8\text{ m/s}^2$ (gravity), and the ratio of X/Y/Z components tells you exactly which direction is "down."

```
STILL (level):          TILTED 30°:           FREE FALL:

  ax ≈  0               ax ≈ 4.9 m/s²         ax ≈ 0
  ay ≈  0               ay ≈ 0                 ay ≈ 0
  az ≈ -9.8 m/s²        az ≈ -8.5 m/s²        az ≈ 0  ← no gravity!

  Gravity vector         Gravity splits         All axes zero =
  is purely Z            across X and Z         weightlessness
```

## Why Each Piece Matters

- **Proof mass + springs:** Convert acceleration into mechanical displacement (Newton's $F = ma$)
- **Comb fingers + air gap:** Convert displacement into capacitance change ($C = \varepsilon A / d$)
- **Differential pair:** Doubles sensitivity and rejects temperature drift, aging, and manufacturing variation -- the same principle that makes [[quick-context/can-bus|CAN bus]] robust in noisy environments
- **Readout ASIC:** Converts femtofarad capacitance changes into digital numbers a [[micro-context/stm32-microcontroller|microcontroller]] can use

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/adc-analog-to-digital-converter]] -- How analog capacitance becomes digital numbers
- [[micro-context/can-bus-transceiver]] -- The CAN chip that implements differential voltage signaling

**Full treatment (10 minutes):**
- [[quick-context/capacitance]] -- The $C = \varepsilon A / d$ equation, parasitic capacitance, and why geometry determines capacitance
- [[quick-context/capacitor]] -- Capacitor types, charge/discharge, decoupling
- [[quick-context/can-bus]] -- Full CAN bus protocol, arbitration, and differential signaling explained
- [[small-context/imu-robot-balance-sensing]] -- How the accelerometer fits into the BNO086 IMU's sensor fusion for robot balance
