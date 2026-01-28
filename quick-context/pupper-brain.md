---
topic: Pupper Control Board Rev 3.5 - The Robot's Brain
created: 2026-01-27
---

> **Related:** [[quick-context/pcb-printed-circuit-board]] | [[quick-context/pcb-chip-transistor-hierarchy]] | [[quick-context/electric-current]]

> **TL;DR:** The Pupper control board is a custom PCB that combines dual STM32 microcontrollers, CAN bus communication to motors, a 9-axis IMU for balance sensing, and power regulation—all the electronics needed to make a quadruped robot walk, sense its orientation, and respond to commands.

# Pupper Control Board: How the Robot's Brain Works

## The Core Problem: Coordinating a Walking Robot

A quadruped robot like Pupper needs to simultaneously: (1) know its orientation in 3D space, (2) send coordinated position commands to 12 servo motors (3 per leg), (3) receive sensor feedback from those motors, (4) run real-time control algorithms at 1000Hz, and (5) communicate with a host computer for high-level commands. Each of these requires specialized hardware—an [[micro-context/imu-inertial-measurement-unit|IMU]] for orientation, [[micro-context/can-bus-transceiver|CAN transceivers]] for motor communication, [[micro-context/stm32-microcontroller|microcontrollers]] for computation, and a [[micro-context/buck-converter|power supply]] to convert battery voltage. The control board integrates all these components onto a single PCB, with carefully routed traces and proper [[micro-context/decoupling-capacitor|decoupling]] to ensure reliable operation.

```
PUPPER CONTROL BOARD ARCHITECTURE
═══════════════════════════════════════════════════════════════════════════════

                           ┌─────────────────────────────────────────────────┐
                           │          PUPPER CONTROL BOARD Rev 3.5           │
    BATTERY ──────────────►│                                                 │
    (12-24V)               │  ┌─────────────┐                                │
                           │  │ TPS54561    │  5V @ 5A                       │
                           │  │ Buck Conv.  ├──────────────┬─────────────────┤
                           │  └─────────────┘              │                 │
                           │         │                     │                 │
                           │         ▼ 3.3V LDO            │                 │
                           │  ┌──────┴──────┐       ┌──────┴──────┐          │
                           │  │  STM32F446  │       │  STM32F446  │          │
                           │  │    (U1)     │◄─────►│    (U5)     │          │
                           │  │  Main MCU   │ SPI   │  Motor MCU  │          │
                           │  └──────┬──────┘       └──────┬──────┘          │
                           │         │                     │                 │
                           │    ┌────┴────┐           ┌────┴────┐            │
                           │    │  BNO086 │           │ MAX3051 │ ×4        │
                           │    │   IMU   │           │CAN Xcvr │            │
                           │    └─────────┘           └────┬────┘            │
                           │                               │                 │
                           │    ┌─────────┐           ┌────┴────┐            │
                           │    │ADS1110  │           │ CAN Bus │            │
                           │    │  ADC    │           │  Conn.  │            │
                           │    └─────────┘           └─────────┘            │
                           │                               │                 │
                           │    ┌─────────┐                ▼                 │
                           │    │MAX98357 │         To 12 Servos             │
                           │    │ Audio   │         (3 per leg)              │
                           │    └─────────┘                                  │
                           └─────────────────────────────────────────────────┘
                                      │
                                      ▼
                              Raspberry Pi (40-pin header)
                              High-level control & WiFi
```

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **[[micro-context/stm32-microcontroller\|STM32F446]]** | ARM Cortex-M4 microcontroller @ 180MHz—runs real-time motor control loops; two are used (one for sensors, one for motors) |
| **[[micro-context/can-bus-transceiver\|CAN Bus]]** | Differential 2-wire protocol used in cars/robots—allows all 12 servos to share one wire pair with collision-free messaging |
| **[[micro-context/imu-inertial-measurement-unit\|BNO086 IMU]]** | 9-axis sensor (accel + gyro + mag) with built-in fusion—outputs quaternions telling which way the robot is tilting |
| **[[micro-context/buck-converter\|Buck Converter]]** | Switching power supply that efficiently converts 12-24V battery to 5V logic power at 90%+ efficiency |
| **[[micro-context/decoupling-capacitor\|Decoupling Caps]]** | The 100nF capacitors sprinkled near every IC—provide instant local charge when chips switch, preventing glitches |

## Component Map by Function

```
POWER PATH:
═══════════════════════════════════════════════════════════════════════════════

  Battery ──► D1 (SS56 diode) ──► TPS54561 ──► 5V rail
  12-24V      reverse polarity     buck         │
              protection           converter    ├──► 3.3V LDO ──► MCUs, IMU, ADC
                                               │
                                               └──► 5V ──► CAN transceivers

  Inductor L1 (10µH): stores energy for buck converter
  Capacitors C18, C19 (47µF): smooth output voltage ripple


SIGNAL PATH (sensing):
═══════════════════════════════════════════════════════════════════════════════

  BNO086 IMU ──I2C──► STM32 U1 (main MCU)
     │                    │
     │  Quaternion        │  Processes orientation
     │  output            │  at 400Hz
     │                    │
     └────────────────────┴──► Feeds into balance controller

  ADS1110 ADC ──I2C──► STM32 U1
     │
     └── Battery voltage monitoring (16-bit precision)


SIGNAL PATH (motor control):
═══════════════════════════════════════════════════════════════════════════════

  STM32 U5 ──► MAX3051 (×4) ──► CAN Bus ──► 12 Servos
  (motor MCU)  CAN transceivers   │
       │                          │
       │  1000Hz control loop     │  Each servo has:
       │  Position commands       │  - Motor driver
       │                          │  - Encoder feedback
       │                          │  - CAN interface
       └──────────────────────────┘

  Why 4 transceivers? Redundancy + separate buses for front/rear legs


COMMUNICATION PATH:
═══════════════════════════════════════════════════════════════════════════════

  Raspberry Pi ◄──40-pin header──► STM32 U1
       │              (U2)              │
       │                                │
  WiFi/SSH                         UART/SPI
  High-level                       Low-level
  commands                         telemetry
```

<details>
<summary><strong>How It Works: Signal Flow During Walking</strong></summary>

When Pupper walks, here's what happens every millisecond (1000Hz control loop):

1. **Orientation sensing**: The BNO086 IMU continuously measures acceleration, rotation, and magnetic field. Its internal processor fuses these into a quaternion (4 numbers representing 3D orientation) and sends it over I2C to the main STM32 (U1).

2. **State estimation**: U1 combines IMU data with motor feedback to estimate the robot's current pose—where each foot is, which way the body is tilting, how fast it's moving.

3. **Control calculation**: U1 runs a balance controller that computes desired joint angles for all 12 motors to keep the robot upright while executing the desired gait (walking pattern).

4. **Command transmission**: U1 sends joint targets to U5 (motor MCU) over SPI. U5 packages these into CAN messages.

5. **Motor communication**: The MAX3051 transceivers convert U5's digital signals into differential CAN bus signals. Each servo receives its position command, moves its motor, and sends back encoder feedback—all on the same 2-wire bus.

6. **Audio feedback**: If enabled, U1 sends audio samples over I2S to the MAX98357A amplifier for sound output (beeps, status indicators).

```
1ms CONTROL LOOP TIMING:
═══════════════════════════════════════════════════════════════════════════════

  0.0ms    0.2ms    0.4ms    0.6ms    0.8ms    1.0ms
    │        │        │        │        │        │
    ▼        ▼        ▼        ▼        ▼        ▼
  ┌────┐  ┌────┐  ┌────────┐  ┌────┐  ┌────┐  ┌────┐
  │IMU │  │Est │  │Control │  │CAN │  │Wait│  │IMU │  ← next cycle
  │Read│  │    │  │Calc    │  │TX  │  │    │  │Read│
  └────┘  └────┘  └────────┘  └────┘  └────┘  └────┘

  Total compute time ~0.5ms, leaving margin for jitter
```

</details>

<details>
<summary><strong>The Key Tension: Real-Time vs. Flexibility</strong></summary>

The dual-MCU architecture reflects a fundamental tension in robot control: **real-time guarantees vs. software flexibility**.

**Why not use just a Raspberry Pi?** Linux is great for WiFi, Python, machine learning—but it's not real-time. A garbage collection pause or kernel interrupt could delay motor commands by 10ms, causing the robot to stumble. The STM32s run bare-metal or RTOS code with deterministic microsecond timing.

**Why not use just STM32s?** Microcontrollers are terrible at high-level tasks: no WiFi stack, no filesystem, limited memory for neural networks or path planning. The Pi handles everything that doesn't need precise timing.

**Why two STM32s?** The original design used one, but motor CAN traffic and IMU processing competed for CPU time. Separating them ensures neither starves the other. U1 handles sensors and high-level commands; U5 handles the demanding 1000Hz motor loop with 4 CAN buses.

```
ARCHITECTURE TRADEOFFS:
═══════════════════════════════════════════════════════════════════════════════

  ┌─────────────────┬─────────────────┬─────────────────┐
  │  Raspberry Pi   │  STM32 (Main)   │  STM32 (Motor)  │
  ├─────────────────┼─────────────────┼─────────────────┤
  │  WiFi, SSH      │  IMU fusion     │  CAN TX/RX      │
  │  Python scripts │  State estimate │  Position loops │
  │  Neural nets    │  High-level cmd │  1kHz timing    │
  │  Logging        │  Audio output   │  Fault handling │
  ├─────────────────┼─────────────────┼─────────────────┤
  │  ~100ms latency │  ~100µs latency │  ~10µs latency  │
  │  OK             │  OK             │  CRITICAL       │
  └─────────────────┴─────────────────┴─────────────────┘
```

</details>

<details>
<summary><strong>Concrete Example: Reading the BOM</strong></summary>

Here's how to interpret key entries from the Bill of Materials:

```
LINE-BY-LINE BOM ANALYSIS:
═══════════════════════════════════════════════════════════════════════════════

"2 | 12 | 100nF | C2,C5,C6,C8,C11,C12,C17,C53,C54,C55,C56,C57 | C0402"
 │   │    │       │                                             │
 │   │    │       │                                             └─ Package: 1.0×0.5mm
 │   │    │       └─ Designators: 12 individual caps on schematic
 │   │    └─ Value: 100 nanofarads (decoupling caps)
 │   └─ Quantity: 12 pieces needed
 └─ Line number

These are decoupling caps—one near each IC power pin.
See: [[micro-context/decoupling-capacitor]]


"29 | 2 | STM32F446RET6 | U1,U5 | LQFP-64"
                          │
                          └─ Two MCUs: U1 (main), U5 (motor)

180MHz ARM Cortex-M4 with CAN, I2C, SPI peripherals.
See: [[micro-context/stm32-microcontroller]]


"31 | 4 | MAX3051EKA+T | U3,U4,U6,U7 | SOT-23-8"

Four CAN transceivers—two buses per MCU for redundancy.
See: [[micro-context/can-bus-transceiver]]


"33 | 1 | BNO086 | U15 | LGA-28"

9-axis IMU with sensor fusion. Note: no supplier part number!
May need to source separately from Bosch/Mouser.
See: [[micro-context/imu-inertial-measurement-unit]]


"21 | 1 | 60.4kΩ | R5 | R0402"
"22 | 1 | 11.5kΩ | R6 | R0402"

Odd values = buck converter feedback divider.
VOUT = VREF × (1 + R5/R6) = 0.8V × (1 + 60.4/11.5) ≈ 5.0V
See: [[micro-context/smd-resistor]], [[micro-context/buck-converter]]
```

**Common BOM gotchas:**
- Empty "Supplier Part" field (like BNO086) means manual sourcing required
- "LCSC" supplier = designed for JLCPCB assembly service
- C0402 parts are nearly impossible to hand-solder—use assembly service or hot air

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

### Component Deep-Dives
- [[micro-context/stm32-microcontroller]] — The dual ARM Cortex-M4 MCUs running the show
- [[micro-context/can-bus-transceiver]] — How differential signaling enables reliable motor communication
- [[micro-context/buck-converter]] — Switching power supply converting battery to 5V
- [[micro-context/imu-inertial-measurement-unit]] — 9-axis sensor fusion for orientation
- [[micro-context/adc-analog-to-digital-converter]] — 16-bit ADC for battery monitoring
- [[micro-context/i2s-audio-amplifier]] — Digital audio output for speaker
- [[micro-context/decoupling-capacitor]] — Why every IC needs nearby 100nF caps
- [[micro-context/smd-resistor]] — The tiny 0402 resistors and what they do
- [[micro-context/power-inductor]] — Energy storage in the buck converter
- [[micro-context/ceramic-resonator]] — 8MHz clock source for the MCUs

### PCB & Electronics Fundamentals
- [[quick-context/pcb-printed-circuit-board]] — How traces, vias, and layers work
- [[quick-context/pcb-chip-transistor-hierarchy]] — The scale hierarchy from transistors to boards
- [[quick-context/electric-current]] — Fundamentals of current flow

### Related Robotics Topics
- Servo motor control (not yet documented)
- PID control loops (not yet documented)
- Quaternions and orientation representation (not yet documented)

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does the Pupper control board use two separate STM32 microcontrollers instead of one more powerful chip?

<details>
<summary>Answer</summary>

Separation of concerns for real-time reliability. The motor control MCU (U5) must maintain a strict 1000Hz control loop—any delay causes jerky motion or falls. By dedicating U5 solely to CAN communication and motor control, it's protected from IMU processing, audio output, or Pi communication stealing CPU cycles. U1 handles everything else without risking motor timing. See: The Key Tension section.
</details>

**Q2:** The BOM shows 12× 100nF capacitors (C0402 size) scattered across designators C2, C5, C6, etc. What are these for and why so many?

<details>
<summary>Answer</summary>

These are decoupling capacitors, placed near each IC's power pins. When a chip switches states, it draws a brief spike of current. The decoupling cap provides this current instantly from local stored charge, preventing voltage dips that could cause glitches. Each IC needs its own nearby cap because PCB trace inductance limits how fast distant capacitors can respond. 12 caps for roughly 12 IC power pins (STM32s have multiple power pins each). See: [[micro-context/decoupling-capacitor]].
</details>

**Q3:** The buck converter uses resistors R5 (60.4kΩ) and R6 (11.5kΩ). What do these specific values accomplish?

<details>
<summary>Answer</summary>

They form a voltage divider in the feedback network that sets the output voltage. The TPS54561 regulates to keep its feedback pin at 0.8V (internal reference). With R5 and R6 dividing the output: VOUT = 0.8V × (1 + 60.4k/11.5k) = 0.8V × 6.25 ≈ 5.0V. The odd precision values (not round numbers like 60kΩ) achieve the exact 5.0V target. See: [[micro-context/buck-converter]], [[micro-context/smd-resistor]].
</details>

**Q4:** Why does the board use 4 CAN transceivers (MAX3051) when CAN is designed to have many devices on one bus?

<details>
<summary>Answer</summary>

Multiple reasons: (1) **Bandwidth**—with 12 servos sending position feedback at 1kHz, one bus approaches saturation; splitting into 2-4 buses reduces congestion. (2) **Redundancy**—if one bus fails, only some legs are affected. (3) **Topology**—front legs might be physically far from rear legs; separate buses simplify wiring. (4) **Isolation**—a short or fault on one bus doesn't take down the whole robot. See: [[micro-context/can-bus-transceiver]].
</details>

**Q5:** The BNO086 IMU entry shows no LCSC supplier part number. What does this mean for building the board?

<details>
<summary>Answer</summary>

The BNO086 isn't available through JLCPCB's standard assembly service. You'll need to either: (1) Order the BNO086 separately from distributors like Mouser/Digi-Key and hand-solder it (difficult—it's an LGA package), (2) Use JLCPCB's "consignment" service where you ship them the parts, or (3) Find a different assembly house that stocks Bosch sensors. This is common for specialized sensors not in LCSC's catalog. See: Concrete Example section on BOM interpretation.
</details>

</details>
