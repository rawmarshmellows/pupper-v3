---
topic: Pupper v3 Control Board BOM — Every Part Explained
created: 2026-02-25
---

# Pupper v3 Control Board BOM — Every Part Explained

> **Related:** [[quick-context/pupper-brain]] | [[quick-context/pcb-printed-circuit-board]] | [[quick-context/schematic-reading]] | [[quick-context/common-ic-packages]]

> **TL;DR:** The Pupper v3 Control Board Rev 3.5 BOM contains 36 line items (about 80 individual parts) spanning 7 functional categories — dual STM32 microcontrollers for real-time motor control, 4 [[micro-context/can-bus-transceiver|CAN transceivers]] for servo communication, a BNO086 [[small-context/imu-robot-balance-sensing|IMU]] for orientation sensing, a TPS54561 [[micro-context/buck-converter|buck converter]] for power, an [[micro-context/i2s-audio-amplifier|I2S audio amplifier]], a 16-bit [[micro-context/adc-analog-to-digital-converter|ADC]] for battery monitoring, plus the passive components (capacitors, resistors, inductors, ferrite beads) and connectors that tie everything together.

## The Core Problem: What Are All These Parts and Why Are They There?

A robot control board BOM (Bill of Materials) is intimidating — dozens of cryptic part numbers, odd [[quick-context/resistor|resistor]] values like 60.4kΩ, and capacitors ranging from 6.8pF to 47μF. But every part has a specific job. The passives aren't random: the 12× 100nF [[quick-context/capacitor|capacitors]] are [[micro-context/decoupling-capacitor|decoupling caps]] keeping IC power stable, the 60.4kΩ/11.5kΩ [[quick-context/resistor|resistors]] form a [[quick-context/voltage|voltage]] divider setting the [[micro-context/buck-converter|buck converter]] output to exactly 5.0V, and the 10μH [[quick-context/inductor|inductor]] is the energy storage element in the switching power supply. Understanding the BOM means understanding each part's role in the system.

BOM: learning/notes/quick-context/BOM_Control Board Rev 3.5_PCB1_3_2025-02-20.xlsx
Pick and Place: learning/notes/quick-context/PickAndPlace_PCB1_3_2025-02-20.xlsx

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **BOM (Bill of Materials)** | The complete parts list for a [[quick-context/pcb-printed-circuit-board|PCB]] — specifies every component's value, package, manufacturer part number, and board location (designator). It's the recipe for building the board. |
| **Reference Designator** | The unique label for each component on the [[quick-context/schematic-reading|schematic]] and PCB: R = [[quick-context/resistor|resistor]], C = [[quick-context/capacitor|capacitor]], U = IC, L = [[quick-context/inductor|inductor]], D = [[quick-context/diode|diode]], CN/H = connector, LED = LED, X = crystal/resonator. |
| **Footprint / Package** | The physical size and pad pattern of a component — C0402 means a [[quick-context/capacitor|capacitor]] in 0402 size (1.0 × 0.5 mm), LQFP-64 is a 64-pin quad flat package. See [[quick-context/common-ic-packages|IC Packages]]. |
| **LCSC Part Number** | A supplier catalog number from LCSC Electronics (JLCPCB's component library). Having an LCSC number means the part is available for automated assembly at JLCPCB. Missing numbers (like the BNO086) mean manual sourcing. |
| **Decoupling Network** | The system of [[quick-context/capacitor|capacitors]] placed near each IC's power pins — 100nF ceramics handle high-frequency transients, larger caps (1μF, 4.7μF, 10μF) handle medium-frequency noise, and bulk caps (47μF) provide energy reservoir. |

<details>
<summary><strong>How It Works</strong> — The BOM organized by function</summary>

Every part on the board serves one of seven functional roles. Here's the complete BOM mapped to its purpose:

```
FUNCTIONAL BLOCK DIAGRAM — Pupper v3 Control Board Rev 3.5
================================================================

     BATTERY (7-24V)
         │
         ▼
    ┌────────────────┐
    │  POWER SUPPLY  │  TPS54561 (U8) buck converter → 5V
    │  L1 (10μH)     │  SS56 (D1) Schottky protection diode
    │  C16,C18,C19   │  R5,R6 feedback divider (60.4k/11.5k)
    │  R10,R13,R22   │  C13,C14,C15 compensation network
    │  C68           │  R39 (1MΩ) soft-start
    └───────┬────────┘
            │ 5V
            ▼
    ┌───────────────────────────────────────────────────┐
    │                  5V POWER RAIL                    │
    │  Decoupling: C1,C3,C7,C9 (1μF) + C4,C10 (4.7μF)   │
    │  + C2,C5,C6,C8,C11,C12,C17... (100nF) per IC      │
    └──┬──────────┬──────────┬──────────┬───────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
    ┌──────┐  ┌──────┐  ┌──────┐  ┌────────┐
    │ U1   │  │ U5   │  │ U15  │  │ U16    │
    │STM32 │  │STM32 │  │BNO086│  │ADS1110 │
    │(Main)│  │(Motor│  │(IMU) │  │(ADC)   │
    │      │  │  MCU)│  │      │  │        │
    └──┬───┘  └──┬───┘  └──────┘  └────────┘
       │         │
       │    ┌────┴────────────────────┐
       │    │   CAN TRANSCEIVERS      │
       │    │ U3,U4,U6,U7 (MAX3051)  │
       │    │ → To 12 servo motors    │
       │    └─────────────────────────┘
       │
    ┌──┴──────┐    ┌──────────────────┐
    │ U18     │    │ CONNECTORS       │
    │MAX98357A│    │ CN1,CN2 (7-pin)  │
    │(Audio)  │    │ CN17 (10-pin)    │
    │         │    │ CN18 (4-pin)     │
    └─────────┘    │ CN21 (2-pin pwr) │
                   │ H4,H5 (3-pin)   │
    ┌──────────┐   │ U2 (40-pin Pi)  │
    │ CLOCK    │   └──────────────────┘
    │ X1,X2    │
    │ (8MHz)   │
    └──────────┘
```

### Category 1: The Brains — Microcontrollers (U1, U5)

**[[micro-context/stm32-microcontroller|STM32F446RET6]]** — ARM Cortex-M4 @ 180 MHz, 512 KB flash, 128 KB RAM, LQFP-64 package (10 × 10 mm, 0.5 mm pitch).

Two are used with distinct roles:
- **U1 (Main MCU):** Receives joint commands from the Raspberry Pi over [[micro-context/spi|SPI]] via the 40-pin header (U2), relays them to U5, reads battery voltage via the [[micro-context/ads1110-battery-adc|ADS1110]] ADC over [[micro-context/i2c|I2C]], and sends audio to the MAX98357A over I2S. (Note: the Pi reads the IMU directly over I2C through the 40-pin header, not through U1 — see [source](https://github.com/Nate711/pupperv3-monorepo/tree/main/ros2_ws/src/control_board_hardware_interface/src/rt).)
- **U5 (Motor MCU):** Dedicated to the 1 kHz motor control loop — receives joint targets from U1 over [[micro-context/spi|SPI]], sends/receives CAN messages to all 12 servos via the 4 MAX3051 transceivers.

Each MCU requires:
- One 8 MHz [[micro-context/ceramic-resonator|ceramic resonator]] (X1, X2) as its [[micro-context/clock-source|clock source]]
- Multiple decoupling capacitors on its power pins (100nF + 1μF + 4.7μF)
- 120Ω [[quick-context/resistor|resistors]] (R1-R4) as [[micro-context/can-bus-termination|CAN bus termination]]

### Category 2: Communication — CAN Transceivers (U3, U4, U6, U7)

**MAX3051EKA+T** — 3.3V CAN transceiver in SOT-23-8 package, 1 Mbps data rate.

Four transceivers create 4 independent CAN buses. Each bus connects to 3 servo motors (4 buses × 3 servos = 12 total). The MAX3051 converts the MCU's single-ended TX/RX signals into differential CAN_H/CAN_L pairs that are noise-immune over long wires — critical for a robot where motor cables run through legs and pick up electromagnetic interference.

The 120Ω resistors (R1-R4) are [[quick-context/can-bus|CAN bus]] termination [[quick-context/resistor|resistors]] — they match the characteristic [[quick-context/impedance-and-reactance|impedance]] of the CAN bus to prevent signal reflections.

### Category 3: Sensing — IMU and ADC (U15, U16)

**BNO086** (U15) — 9-axis IMU (accelerometer + gyroscope + magnetometer) with onboard Cortex-M0+ processor running sensor fusion. Outputs quaternions over I2C/SPI. LGA-28 package (5.2 × 3.8 mm). This tells the robot which way is up — essential for balance control.

**ADS1110A0IDBVR** (U16) — 16-bit delta-sigma ADC with I2C interface, SOT-23-6 package. Monitors battery voltage through a [[quick-context/resistor|voltage divider]] so the system can warn of low battery and prevent over-discharge.

### Category 4: Audio — I2S Amplifier (U18)

**MAX98357AEWL+T** — Class-D mono audio amplifier, 3.2W into 4Ω, in a tiny WLP-9 package (1.35 × 1.44 mm). Takes digital I2S audio from U1 and drives a speaker directly — no external DAC needed. Used for beeps, status tones, and potentially voice synthesis.

### Category 5: Power Supply — Buck Converter (U8, D1, L1)

**TPS54561DPRR** (U8) — Wide-input (4.5–60V) buck converter, 5A output, adjustable frequency (100 kHz – 2.5 MHz), WSON-10 package with exposed thermal pad.

This is the board's main power supply, converting battery voltage (typically 7–24V) down to 5V for all logic. The supporting components form a complete switching power supply:

```
BUCK CONVERTER CIRCUIT (simplified)
================================================================

    VBAT (7-24V)
      │
      ├──D1 (SS56)──┐  Reverse polarity protection
      │              │  (Schottky: low Vf = 0.7V, 5A, 60V)
      ▼              │
    ┌─────────────┐  │
    │  TPS54561   │  │
    │    (U8)     │  │
    │  SW pin ────┼──┴──⊃⊃⊃⊃──┬──── 5V OUTPUT
    │             │      L1     │
    │  FB pin ────┼──┐  10μH   ═╪═ C18,C19
    │             │  │          │   (47μF × 2)
    └─────────────┘  │         GND
                     │
               R5 ───┤──── FB (feedback pin sees Vout×R6/(R5+R6))
              60.4kΩ │
                     │
               R6 ───┤
              11.5kΩ │
                    GND

    Output voltage:
    VOUT = VREF × (1 + R5/R6) = 0.8V × (1 + 60.4k/11.5k) = 5.0V

    R10 (34kΩ), R13 (174kΩ): set switching frequency
    C13 (3nF), C14 (6.8pF), C15 (2.7nF): compensation network
    R22 (200kΩ): soft-start / enable
    R39 (1MΩ): bootstrap
    C16 (10μF): input bypass
```

The 10μH [[quick-context/inductor|inductor]] (L1, Sunlord MWSA1004S-100MT) is the energy storage element — it smooths the chopped voltage from the buck converter's internal switch into steady DC. The 47μF output capacitors (C18, C19) further smooth the output ripple.

### Category 6: Passive Components — Capacitors, Resistors, Ferrite Beads

**Capacitors by function:**

| Value | Qty | Designators | Function |
|-------|-----|-------------|----------|
| 100nF | 13 | C2,C5,C6,C8,C11,C12,C17,C53-C58 | IC decoupling (one per power pin) |
| 1μF | 4 | C1,C3,C7,C9 | Medium-frequency decoupling |
| 4.7μF | 2 | C4,C10 | Bulk decoupling near MCUs |
| 10μF | 2 | C16,C68 | Input bypass for buck converter |
| 47μF | 2 | C18,C19 | Buck converter output filter |
| 3nF, 6.8pF, 2.7nF | 3 | C13,C14,C15 | Buck converter compensation |

All small caps are C0402 (1.0 × 0.5 mm) — too small to hand-solder. The 47μF caps are C0805 and the 10μF C16 is C1206, both using higher-[[quick-context/capacitance|capacitance]] [[quick-context/capacitor|MLCC]] (ceramic) technology.

**Resistors by function:**

| Value | Qty | Designators | Function |
|-------|-----|-------------|----------|
| 120Ω | 4 | R1-R4 | CAN bus termination |
| 60.4kΩ / 11.5kΩ | 2 | R5,R6 | Buck converter feedback divider → 5.0V |
| 34kΩ / 174kΩ | 2 | R10,R13 | Buck converter frequency set |
| 10kΩ | 3 | R18,R21,R23 | Pull-up resistors (I2C, reset) |
| 2.2kΩ | 4 | R19,R20,R24,R25 | I2C pull-ups / current limit |
| 200kΩ | 1 | R22 | Buck enable / soft-start |
| 1MΩ | 1 | R39 | Bootstrap / high-impedance bias |

All resistors are R0402 (1.0 × 0.5 mm) from UNI-ROYAL or YAGEO. The odd values (60.4kΩ, 11.5kΩ, 174kΩ) come from the E96 precision series — they're calculated from the buck converter datasheet's feedback formula, not chosen arbitrarily.

**Ferrite beads (L2, L3):**

CBG160808U501T — 50Ω impedance at 100 MHz, L0603 package. These aren't [[quick-context/inductor|inductors]] in the traditional sense — they act as frequency-dependent [[quick-context/resistor|resistors]] that absorb high-frequency noise and convert it to heat. Placed on power lines feeding sensitive analog circuits (IMU, ADC) to isolate them from digital switching noise.

### Category 7: Connectors and Mechanical

| Part | Qty | Designator | Function |
|------|-----|------------|----------|
| BM07B-SRSS-TB ([[micro-context/jst-connector-families|JST]], 7-pin) | 2 | CN1, CN2 | Servo bus connectors (CAN + power) |
| HC-ZH-10PWT (10-pin) | 1 | CN17 | Multi-signal connector |
| BM04B-SRSS-TB (JST, 4-pin) | 1 | CN18 | I2C / peripheral connector |
| HC-PH-2ALT (2-pin) | 1 | CN21 | Battery power input |
| HC-PH-3ALT (3-pin) | 2 | H4, H5 | Servo signal connectors (S, +5V, GND) |
| FH-00339 (40-pin header) | 1 | U2 | Raspberry Pi GPIO header |

The 40-pin header (U2) is the physical interface to the Raspberry Pi — it carries SPI signals for motor commands between the Pi and the MCU (via `/dev/spidev0.0` and `/dev/spidev0.1` at 6 MHz), and I2C signals for the Pi to read the IMU directly (via `/dev/i2c-N`). Source: [`rt_spi.cpp`](https://github.com/Nate711/pupperv3-monorepo/blob/main/ros2_ws/src/control_board_hardware_interface/src/rt/rt_spi.cpp) and [`rt_bno055.cpp`](https://github.com/Nate711/pupperv3-monorepo/blob/main/ros2_ws/src/control_board_hardware_interface/src/rt/rt_bno055.cpp). See [[quick-context/pupper-brain]] for the dual-MCU + Pi architecture.

**LEDs (LED9, LED10):** XL-1005UWC — white 0402-size LEDs for status indication. Connected through current-limiting resistors (likely from the 2.2kΩ set).

**Crystals (X1, X2):** CSTNE8M00G55A000R0 — 8 MHz ceramic resonators by muRata with built-in 33pF load capacitors. One per STM32. The MCU's internal PLL multiplies this 8 MHz reference up to the 180 MHz operating frequency: $f_{CPU} = 8\text{MHz} \times \frac{180}{8} = 180\text{MHz}$.

</details>

<details>
<summary><strong>The Key Tension</strong> — Assembly complexity vs. component availability</summary>

The BOM reveals two major design tradeoffs:

**1. C0402 everywhere = machine-assembly-only**

Every passive on this board is 0402 size (1.0 × 0.5 mm) — smaller than a grain of rice. This minimizes board size (critical for fitting inside a robot) but makes hand assembly virtually impossible. The board is designed for JLCPCB's [[micro-context/pick-and-place-file|pick-and-place]] service, and every part except the BNO086 has an LCSC supplier number for automated sourcing.

```
PACKAGE SIZE vs. HAND-SOLDERABILITY
================================================================

    0201 (0.6×0.3mm)  ██  ← needs microscope, robotic placement
    0402 (1.0×0.5mm)  ████  ← THIS BOARD: machine-only
    0603 (1.6×0.8mm)  ██████  ← expert hand-solder with magnification
    0805 (2.0×1.25mm) ████████  ← hand-solderable with practice
    1206 (3.2×1.6mm)  ████████████  ← comfortable hand-solder
    Through-hole       ████████████████  ← beginner-friendly

    Every passive on this BOM is in the "machine-only" zone.
    This is typical for production robot boards.
```

**2. The BNO086 sourcing problem**

The BNO086 IMU has no LCSC part number — it's not in JLCPCB's standard component library. Options:
- Order from Mouser/Digi-Key and use JLCPCB's consignment service
- Hand-solder the LGA-28 package (extremely difficult — pads are underneath)
- Use a hot-air rework station

This is a common tension: the best sensor for the job (BNO086's onboard fusion processor is unmatched) doesn't always align with the easiest assembly path.

**3. Why so many capacitor values?**

The 7 different capacitor values (6.8pF to 47μF) aren't random — each serves a specific frequency range:

| Value | Frequency Role | Self-Resonant Freq (approx) |
|-------|---------------|---------------------------|
| 6.8pF | GHz-range filtering | >1 GHz |
| 2.7nF, 3nF | Buck compensation | 10-100 MHz |
| 100nF | High-freq decoupling | 20-50 MHz |
| 1μF | Mid-freq decoupling | 5-10 MHz |
| 4.7μF, 10μF | Low-freq bypass | 1-3 MHz |
| 47μF | Bulk energy storage | <1 MHz |

Together they form a [[quick-context/frequency-and-filtering|broadband decoupling network]] covering noise from DC to hundreds of MHz.

</details>

<details>
<summary><strong>Concrete Example</strong> — Reading a BOM line and understanding every field</summary>

Let's decode BOM line 32 completely:

```
DECODING A BOM LINE
================================================================

Line: "32 | 1 | TPS54561DPRR | U8 | WSON-10_L4.0-W4.0-P0.80-TL-EP | | TPS54561DPRR | TI | C180369 | LCSC"

Field-by-field:
─────────────────────────────────────────────────────────────

  No.: 32            → Line number (just for ordering)

  Quantity: 1        → One of these on the board

  Comment: TPS54561DPRR  → Part number (identifies exact IC)

  Designator: U8     → "U" = IC, "8" = the 8th IC placed
                        This is how the schematic, BOM, and
                        PCB silkscreen reference the same part

  Footprint: WSON-10_L4.0-W4.0-P0.80-TL-EP
             │       │    │    │     │  │
             │       │    │    │     │  └─ EP = Exposed Pad
             │       │    │    │     └─ TL = Top Lid
             │       │    │    └─ P0.80 = 0.80mm pin pitch
             │       │    └─ W4.0 = 4.0mm wide
             │       └─ L4.0 = 4.0mm long
             └─ WSON-10 = 10-pin Very Small Outline No-lead

  Manufacturer Part: TPS54561DPRR
                     │        │││
                     │        ││└─ R = tape and reel packaging
                     │        │└── R = tape and reel (doubled)
                     │        └─── P = PowerPAD package variant
                     └─ TPS54561 = the base part from TI's datasheet

  Manufacturer: TI (Texas Instruments)

  Supplier Part: C180369  → LCSC catalog number
                           Search lcsc.com/C180369 to buy

  Supplier: LCSC → Available for JLCPCB assembly


NOW TRACE IT ON THE BOARD:
─────────────────────────────────────────────────────────────

  1. Open schematic → find U8 → see TPS54561 symbol with
     pins: VIN, SW, BOOT, EN, SS/TR, RT/CLK, COMP, FB, GND, EP

  2. Trace FB pin → voltage divider R5 (60.4kΩ) + R6 (11.5kΩ)
     → confirms output set to 5.0V

  3. Trace SW pin → L1 (10μH inductor) → output caps C18,C19
     → confirms buck converter topology

  4. Open PCB layout → find U8 near power input (CN21)
     → exposed pad soldered to ground plane for heat sinking
```

**The one thing most outsiders get wrong about this is...** thinking a BOM is just a shopping list. It's actually a complete specification that encodes deep design decisions. The 60.4kΩ feedback resistor isn't "approximately 60k" — it's calculated to 3 significant figures from the voltage reference. The 100nF decoupling caps aren't "some capacitors near the chip" — each one is placed within 2mm of a specific power pin, and their impedance at the STM32's switching frequencies determines whether the MCU runs reliably. The BOM is the bridge between the schematic's electrical design and the physical board that gets built.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/pupper-brain]]** — The architectural overview of this same board: why dual MCUs, why CAN bus, how the 1 kHz control loop works. This BOM document explains WHAT parts are used; the brain document explains WHY.

- **[[quick-context/pupper-v3-labs]]** — The 7-lab CS123 curriculum that runs on this hardware. Labs 1-4 directly control the motors via CAN bus and read the IMU; Lab 5 deploys RL policies through the neural controller; Labs 6-7 add voice and vision on the Raspberry Pi side.

- **[[quick-context/pcb-printed-circuit-board]]** — How all these components physically connect — traces carry signals between ICs, vias connect layers, and the copper pour provides the [[quick-context/grounding-and-return-paths|ground plane]] return path for every signal.

- **[[quick-context/pcb-assembly-files-bom-cpl]]** — How to *read* the BOM and CPL (pick-and-place) file pair itself, column by column. This note explains what each part on the board is; that one explains the file formats the assembler consumes.

- **[[quick-context/pcb-layers]]** — The Gerber files that define where each component lands on the board. The paste mask layer determines which pads get solder paste during assembly — critical for the 0402-size passives on this board.

- **[[quick-context/schematic-reading]]** — How to trace the connections between BOM parts on the circuit diagram. Reference designators (R5, U8, C18) are the link between BOM, schematic, and physical board.

- **[[quick-context/capacitor]]** — Why the board needs 25+ capacitors spanning 6.8pF to 47μF. The decoupling network, compensation network, and bulk bypass all serve different frequency ranges.

- **[[quick-context/resistor]]** — Why resistor values like 60.4kΩ and 174kΩ exist (E96 precision series), how voltage dividers set the buck output, and why 120Ω terminates CAN buses.

- **[[quick-context/inductor]]** — The 10μH [[micro-context/power-inductor|power inductor]] is the heart of the buck converter. Its saturation current must exceed the 5A output current, and its DCR determines power loss.

- **[[quick-context/diode]]** — The SS56 Schottky diode protects against reverse battery polarity. Its low forward voltage (0.7V vs 1.1V for silicon) minimizes power loss.

- **[[quick-context/common-ic-packages]]** — This BOM uses LQFP-64, SOT-23-8, SOT-23-6, WSON-10, LGA-28, and WLP-9 packages. Understanding package types explains why certain parts can't be hand-soldered.

- **[[quick-context/soldering]]** — All 0402 passives and SMD ICs require reflow soldering. The paste mask layer defines the stencil apertures for solder paste deposition.

- **[[quick-context/frequency-and-filtering]]** — The ferrite beads (L2, L3) and multi-value capacitor network form a distributed filter that suppresses switching noise across a wide bandwidth.

- **[[quick-context/power-watts-joules]]** — The buck converter's 85-95% efficiency means 0.25-0.75W of waste heat at full load. The exposed thermal pad on U8's WSON package conducts this heat into the PCB ground plane.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** The BOM lists 12× 100nF capacitors and 4× 1μF capacitors. Why both values instead of just using 1μF for everything?
<details>
<summary>Answer</summary>
**Different capacitor values are effective at different frequencies.** A 100nF ceramic capacitor has lower parasitic inductance (ESL) and a higher self-resonant frequency than a 1μF cap, making it more effective at suppressing high-frequency noise (>10 MHz). The 1μF caps handle medium-frequency transients better due to their larger charge reservoir. Using both covers a wider frequency range. In practice, you almost always see 100nF + a larger value at each IC — the 100nF is the "fast" cap and the larger cap is the "bulk" cap. See [[quick-context/capacitor]] for the full decoupling explanation.
</details>

**Q2:** Why are R5 and R6 such specific values (60.4kΩ and 11.5kΩ) instead of round numbers?
<details>
<summary>Answer</summary>
**They're calculated from the TPS54561 datasheet's feedback formula to set exactly 5.0V output.** The formula is: $V_{OUT} = V_{REF} \times (1 + R5/R6) = 0.8V \times (1 + 60.4k/11.5k) = 0.8V \times 6.252 = 5.0V$. These values come from the E96 resistor series (1% tolerance), which provides enough precision to hit the target voltage. Using E12 values (10% tolerance, round numbers like 56kΩ and 10kΩ) would give 5.28V — unacceptably far from 5.0V. See [[quick-context/resistor]] for the E-series explanation.
</details>

**Q3:** The board has 4 CAN transceivers but only 2 MCUs. Why not use just 2 transceivers (one per MCU)?
<details>
<summary>Answer</summary>
**Bandwidth and fault isolation.** With 12 servos sending position feedback at 1 kHz, a single CAN bus at 1 Mbps approaches saturation. Splitting into 4 buses (3 servos each) keeps utilization around 25%, leaving headroom for retransmissions. Additionally, a wiring fault on one leg only takes down 3 servos instead of all 12. U5 (Motor MCU) has 2 CAN peripherals, and each bus pair likely handles front/rear or left/right legs. See [[quick-context/pupper-brain]] for the architecture.
</details>

**Q4:** The BNO086 has no LCSC supplier part number. What are your options for building this board?
<details>
<summary>Answer</summary>
**Three options:** (1) Use JLCPCB's consignment service — order the BNO086 from Mouser/Digi-Key and ship it to JLCPCB, who will place it during assembly. (2) Have JLCPCB assemble everything except the BNO086, then solder it yourself with a hot-air station (the LGA-28 package has pads only on the bottom — impossible with a [[quick-context/soldering|soldering]] iron). (3) Find an alternative assembly house that stocks Bosch sensors. Option 1 is most common. This sourcing gap is typical for specialized sensors not in mainstream Chinese distributor catalogs.
</details>

**Q5:** If you removed the 10μH [[quick-context/inductor|inductor]] (L1) from the buck converter circuit, what would happen?
<details>
<summary>Answer</summary>
**The 5V output would collapse into violent pulses instead of smooth DC.** The TPS54561's internal switch chops the battery voltage on and off at hundreds of kHz. The [[quick-context/inductor|inductor]] smooths these pulses by storing energy in its magnetic field during the "on" phase and releasing it during "off." Without L1, the output would be a square wave between battery voltage and 0V — no IC on the board could survive that. The output capacitors (C18, C19) would see massive ripple current and likely fail. The inductor is not optional in a buck converter; it IS the converter's fundamental energy storage element. See [[quick-context/inductor]] for the buck converter explanation.
</details>

</details>
