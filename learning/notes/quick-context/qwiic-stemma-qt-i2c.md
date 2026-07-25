---
topic: Qwiic / STEMMA QT — Plug-and-Play I2C Connector Ecosystem
created: 2026-03-28
---

# Qwiic / STEMMA QT — Plug-and-Play I2C

> **Related:** [[micro-context/jst-connector-families]]

> **TL;DR:** Qwiic (SparkFun) and STEMMA QT (Adafruit) are cross-compatible plug-and-play [[micro-context/i2c|I2C]] ecosystems that use a standardized 4-pin JST SH 1.0mm connector carrying power (3.3V), ground, SDA, and SCL. They eliminate soldering and wiring errors for sensor hookup — just plug in a cable and start reading data over I2C. Hundreds of breakout boards (IMUs, temperature sensors, displays, ADCs) use this connector.

## The Core Problem

Wiring up an I2C sensor on a breadboard means 4 jumper wires — **VCC** (supply [[quick-context/voltage|voltage]], typically 3.3V or 5V that powers the sensor), **GND** (ground, the return path that completes the circuit), **SDA** (Serial Data, the line that carries the actual data bits back and forth), and **SCL** (Serial Clock, the line the master toggles to set the timing for each bit) — plus pull-up [[quick-context/resistor|resistors]], and plenty of opportunities to swap SDA/SCL or short power to ground. Every new sensor means re-reading the datasheet pinout. Qwiic/STEMMA QT solves this by standardizing the physical connector, pinout, and voltage — every board has the same 4-pin JST SH jack with the same pin order. Plug in a cable, and I2C just works. No [[quick-context/soldering|soldering]], no wrong pins, no missing pull-ups (they're on the breakout board).

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Qwiic** | SparkFun's brand name for their I2C plug-and-play system. Uses JST SH 1.0mm 4-pin connectors. All Qwiic boards operate at 3.3V logic only. |
| **STEMMA QT** | Adafruit's equivalent system — physically identical connector and pinout to Qwiic (fully cross-compatible). STEMMA QT boards include onboard level shifting, so they work with both 3.3V and 5V logic (important for 5V Arduinos like Uno/Mega). |
| **[[micro-context/jst-connector-families|JST SH]] 1.0mm** | The actual connector: a 4-pin, 1.0mm pitch, surface-mount JST SH receptacle. The same connector used in FPV drones and small electronics. The cable has a molded plug on each end. |
| **Daisy-chaining** | Most Qwiic/STEMMA QT boards have two JST SH jacks — one "in" and one "out" — so you can chain multiple sensors on the same I2C bus without a hub. Each device needs a unique I2C address. |
| **STEMMA (classic)** | Adafruit's larger connector system using JST PH 2.0mm (3 or 4 pin). Used for analog, digital, and I2C connections. Not the same as STEMMA QT — different connector, different pitch. Don't mix them up. |

<details>
<summary><strong>How It Works</strong> — From cable to data</summary>

### The Pinout

All Qwiic and STEMMA QT cables use the same pin order:

```
QWIIC / STEMMA QT — 4-PIN JST SH 1.0mm:

  Pin 1    Pin 2    Pin 3    Pin 4
  ┌────┐  ┌────┐  ┌────┐  ┌────┐
  │GND │  │VCC │  │SDA │  │SCL │
  │Black│  │Red │  │Blue│  │Yel │
  └────┘  └────┘  └────┘  └────┘

  Wire colors (standard):
    Black  = GND
    Red    = 3.3V (Qwiic) or 3.3-5V (STEMMA QT)
    Blue   = SDA (I2C data)
    Yellow = SCL (I2C clock)

  Note: Some cables use Green instead of Blue for SDA.
```

### Daisy-Chaining Multiple Sensors

```
DAISY-CHAIN TOPOLOGY:

  Arduino / MCU
  ┌──────────┐
  │      Qwiic├───cable───┐
  │      jack │           │
  └──────────┘       ┌────┴────┐
                     │ Sensor A│  (addr: 0x4B)
                     │  IN  OUT├───cable───┐
                     └─────────┘           │
                                      ┌────┴────┐
                                      │ Sensor B│  (addr: 0x68)
                                      │  IN  OUT├───cable───┐
                                      └─────────┘           │
                                                        ┌────┴────┐
                                                        │ Display │  (addr: 0x3C)
                                                        │  IN  OUT│
                                                        └─────────┘

  All devices share the same SDA + SCL + VCC + GND wires.
  Each must have a UNIQUE I2C address.
  Pull-up resistors are on each breakout board — no external pull-ups needed.

  Practical limit: ~5-8 devices before bus capacitance causes signal issues.
  (Each board + cable adds ~10-30 pF; I2C bus max is ~400 pF.)
```

### Voltage Compatibility with Arduino

```
VOLTAGE COMPATIBILITY MATRIX:

  Arduino Board    Logic Level   Qwiic?    STEMMA QT?
  ──────────────────────────────────────────────────────
  Uno / Mega         5V          ⚠ NEEDS     ✓ OK
                                 ADAPTER   (has level
                                           shifting)
  Nano 33 IoT       3.3V         ✓ OK       ✓ OK
  MKR series        3.3V         ✓ OK       ✓ OK
  Arduino Nano      5V           ⚠ NEEDS     ✓ OK
  Every              ADAPTER
  SparkFun          3.3V         ✓ OK       ✓ OK
  Thing Plus
  Adafruit          3.3V         ✓ OK       ✓ OK
  Feather

  ⚠ = SparkFun Qwiic boards are 3.3V only.
      Connecting to a 5V Arduino requires a
      Qwiic Level Shifter or Logic Level Converter.

  STEMMA QT boards have onboard level shifting,
  so they work at both 3.3V and 5V natively.
```

### What's on a Typical Breakout Board

Every Qwiic/STEMMA QT breakout board includes:

1. **The sensor IC** (e.g., BNO085 IMU, BME280 temperature/humidity, ADS1115 ADC)
2. **Two JST SH jacks** — for daisy-chaining
3. **3.3V voltage regulator** — so you can power from 3.3-5V
4. **I2C pull-up resistors** (typically 2.2–10k$\Omega$) — already on the board
5. **Address jumper** — solder bridge to change the I2C address if you have two of the same sensor
6. **[[micro-context/decoupling-capacitor|Decoupling capacitor]]** — for stable power to the sensor

This means the breakout board handles all the electrical details. You just plug in the cable.

</details>

<details>
<summary><strong>The Key Tension</strong> — Convenience vs. control</summary>

### Qwiic vs. STEMMA QT vs. Grove

| Feature | Qwiic (SparkFun) | STEMMA QT (Adafruit) | Grove (Seeed) |
|---------|-------------------|----------------------|---------------|
| **Connector** | JST SH 1.0mm | JST SH 1.0mm | HY 2.0mm |
| **Cross-compatible** | ✓ with STEMMA QT | ✓ with Qwiic | ✗ different connector |
| **Logic voltage** | 3.3V only | 3.3V and 5V | 3.3V and 5V |
| **Protocols** | I2C only | I2C only | I2C, UART, analog, digital |
| **Board count** | ~200+ | ~300+ | ~400+ |
| **Pull-ups on board** | ✓ | ✓ | ✓ |
| **Typical price** | $5-15 per board | $5-15 per board | $3-12 per board |

**The tradeoff:** Qwiic/STEMMA QT optimizes for I2C simplicity — one connector type, one protocol, zero configuration. Grove is more flexible (supports analog, digital, UART) but at the cost of a larger connector and needing to know which Grove port type to use.

**When Qwiic/STEMMA QT doesn't work:**
- **[[micro-context/spi|SPI]] sensors** — these ecosystems are I2C only. High-speed sensors that need SPI require traditional wiring.
- **Long cable runs** — I2C is limited to ~1 m. For longer distances, you need [[quick-context/can-bus|CAN bus]] or RS-485.
- **High-current devices** — the JST SH connector is rated for ~1A. Motors, heaters, or solenoids need separate power wiring.
- **Address conflicts** — if two identical sensors have the same fixed I2C address and no address jumper, you need a TCA9548A I2C multiplexer.

</details>

<details>
<summary><strong>Concrete Example</strong> — Reading a BNO085 IMU with Arduino + Qwiic</summary>

### Hardware Setup

Just one cable:

```
WIRING (total: 1 cable, 0 soldering):

  Arduino Nano 33 IoT          SparkFun BNO085 Breakout
  ┌────────────────┐            ┌──────────────────┐
  │            Qwiic├──cable──►Qwiic  BNO085       │
  │            jack │           │     (addr: 0x4B) │
  └────────────────┘            └──────────────────┘

  That's it. Power, ground, SDA, SCL — all in one cable.
  Pull-ups are on the breakout. Voltage regulator is on the breakout.
```

### Arduino Code

```cpp
#include <Wire.h>
#include <SparkFun_BNO08x_Arduino_Library.h>

BNO08x imu;

void setup() {
  Serial.begin(115200);
  Wire.begin();  // Start I2C as master

  // Initialize IMU at default Qwiic address
  if (!imu.begin(0x4B, Wire)) {
    Serial.println("BNO085 not found! Check Qwiic cable.");
    while (1);
  }

  // Enable rotation vector reports at 100 Hz
  imu.enableRotationVector(10);  // 10 ms interval
}

void loop() {
  if (imu.getSensorEvent()) {
    float roll  = imu.getRoll()  * 180.0 / PI;
    float pitch = imu.getPitch() * 180.0 / PI;
    float yaw   = imu.getYaw()   * 180.0 / PI;

    Serial.print("Roll: ");  Serial.print(roll);
    Serial.print(" Pitch: "); Serial.print(pitch);
    Serial.print(" Yaw: ");   Serial.println(yaw);
  }
}
```

### Adding a Second Sensor (Daisy-Chain)

```cpp
// Add a BME280 temperature sensor — just plug another cable
// from BNO085's second Qwiic jack to the BME280 board

#include <SparkFun_BME280.h>

BME280 tempSensor;

void setup() {
  // ... (BNO085 init from above)

  // BME280 is at address 0x77 (different from BNO085's 0x4A)
  if (!tempSensor.beginI2C()) {
    Serial.println("BME280 not found!");
  }
}

void loop() {
  // Read both sensors on the same I2C bus, same cable chain
  float temp = tempSensor.readTempC();
  // ... plus IMU data from above
}
```

**The one thing most outsiders get wrong about this is...** thinking you need special Qwiic or STEMMA QT libraries. You don't — these are just I2C devices with a standardized connector. Any I2C library works. `Wire.h` is all you need at the protocol level. The branded libraries (SparkFun_BNO08x, Adafruit_BME280) are convenience wrappers that handle register-level details, but they'd work identically if you soldered the wires directly. The connector ecosystem standardizes the *physical* layer, not the *software* layer.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[micro-context/i2c]]** — The protocol running over these cables: 2-wire (SDA + SCL), 7-bit addressing, 100-400 kHz. Understanding I2C is essential for debugging address conflicts and bus issues.

- **[[micro-context/jst-connector-families]]** — JST SH (1.0mm) is the connector used by Qwiic/STEMMA QT. This micro-context covers the full range of JST families and common mix-ups (like "MX 1.25mm" being a misnomer).

- **[[quick-context/embedded-communication-protocols]]** — Where I2C sits in the landscape of UART, SPI, CAN, and Ethernet. Explains why I2C is the right choice for short-range sensor communication.

- **[[small-context/imu-robot-balance-sensing]]** — The BNO086 IMU is one of the most popular Qwiic/STEMMA QT devices. The Pupper v3 uses this sensor for balance control.

- **[[micro-context/adc-analog-to-digital-converter]]** — ADC breakouts (ADS1115, ADS1015) are common Qwiic devices for reading analog sensors that a digital-only MCU can't measure directly.

- **[[quick-context/pupper-bom-control-board]]** — The Pupper control board has a 4-pin JST connector (CN18) for I2C peripherals, following the same 4-wire pattern as Qwiic/STEMMA QT.

- **TCA9548A I2C Multiplexer** — When you have address conflicts (two identical sensors), this chip creates 8 independent I2C buses behind a single address, letting you talk to devices with the same address by switching channels.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** You have an Arduino Uno (5V logic) and a SparkFun Qwiic BNO085 breakout. Can you just plug in a Qwiic cable?
<details>
<summary>Answer</summary>
No — SparkFun Qwiic boards are 3.3V only. The Arduino Uno's I2C lines run at 5V, which could damage the 3.3V sensor. You need a Qwiic Level Shifter board between the Uno and the sensor, or use an Adafruit STEMMA QT version of the breakout (which has onboard level shifting for 5V compatibility). Alternatively, use a 3.3V Arduino (Nano 33 IoT, MKR) where Qwiic works directly.
</details>

**Q2:** You've daisy-chained 3 Qwiic sensors and the last one in the chain isn't responding. What's likely wrong?
<details>
<summary>Answer</summary>
Most likely **bus [[quick-context/capacitance|capacitance]]**. Each breakout board adds ~10-30 pF of capacitance, plus each cable adds capacitance proportional to its length. Beyond ~400 pF total, I2C signal edges become too slow for the pull-up resistors to restore the bus voltage in time. Fixes: use shorter cables, reduce the number of boards, use stronger pull-ups (lower resistance, e.g., 4.7k$\Omega$ instead of 10k$\Omega$), or use an I2C bus extender chip.
</details>

**Q3:** You want to connect two identical BME280 temperature sensors to measure two different locations. Both have address 0x77. How do you solve this with Qwiic?
<details>
<summary>Answer</summary>
Three options: (1) **Address jumper** — many breakout boards have a solder jumper to switch between 0x77 and 0x76. Cut the default trace and bridge the alternate pad. (2) **TCA9548A I2C multiplexer** — this Qwiic-compatible board creates 8 separate I2C buses behind one address. Put each BME280 on a different channel and select the channel before reading. (3) **Use two I2C buses** — some MCUs have multiple I2C peripherals (Wire and Wire1 on Arduino). Put one sensor on each bus.
</details>

**Q4:** Why do Qwiic/STEMMA QT use JST SH 1.0mm instead of the larger, easier-to-handle JST PH 2.0mm that STEMMA (classic) uses?
<details>
<summary>Answer</summary>
Size. JST SH 1.0mm connectors are roughly half the footprint of PH 2.0mm, allowing them to fit on small breakout boards (15mm x 15mm) that would have no room for a PH connector. The Qwiic ecosystem targets compact prototyping where board real estate matters. The tradeoff is that SH connectors are harder to crimp by hand and the cables are less robust — but since these are meant for prototyping and short-range sensor hookup, not industrial wiring harnesses, the small size wins.
</details>

**Q5:** The Pupper v3 control board has a 4-pin JST connector (CN18) for I2C peripherals. Could you plug a standard Qwiic cable into it?
<details>
<summary>Answer</summary>
Only if CN18 is a JST SH 1.0mm connector with the same pinout (GND, VCC, SDA, SCL). Looking at the Pupper BOM, CN18 is a BM04B-SRSS-TB — which is a JST **SH** 4-pin receptacle. However, you need to verify the pin order matches Qwiic's standard (GND, 3.3V, SDA, SCL). If the board designer used a different pin order (e.g., VCC first instead of GND first), plugging in a Qwiic cable directly would connect the wrong signals to the wrong pins. Always check the schematic before assuming connector compatibility.
</details>

</details>
