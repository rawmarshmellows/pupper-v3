---
topic: Embedded Communication Protocols — UART, I2C, SPI, CAN, and When to Use Each
created: 2026-03-27
---

> **Related:** [[learning/notes/quick-context/can-bus]] | [[learning/notes/quick-context/pupper-brain]] | [[learning/notes/micro-context/i2c]] | [[learning/notes/micro-context/spi]] | [[learning/notes/micro-context/stm32-microcontroller]]

# Embedded Communication Protocols

> **TL;DR:** Embedded systems choose between a handful of serial protocols — UART, [[learning/notes/micro-context/i2c|I2C]], [[learning/notes/micro-context/spi|SPI]], [[learning/notes/quick-context/can-bus|CAN]], and Ethernet — each optimizing a different point in the tradeoff space of speed, distance, wire count, and noise immunity. The Pupper v3 uses four of them simultaneously: SPI between MCUs, I2C for sensors, CAN for motors, and UART for debug — because no single protocol is best at everything. https://www.youtube.com/watch?v=0rlpwVNyBO8

## The Core Problem

A microcontroller needs to talk to other chips — sensors, motors, displays, other MCUs, a host computer. But a typical [[learning/notes/micro-context/stm32-microcontroller|STM32]] only has 100 or so pins, and dedicating one pin per data bit (parallel communication) wastes pins and board space. Serial protocols solve this by sending data one bit at a time over just 1-4 wires, using a clock signal or agreed-upon timing to keep sender and receiver synchronized. The challenge is that different peripherals have wildly different needs: a temperature sensor sends 2 bytes every second (I2C is fine), but a motor controller needs 8 bytes every millisecond over a 1-meter cable with motors generating EMI (only CAN will do).

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Synchronous vs. Asynchronous** | Synchronous protocols (SPI, I2C) send a clock signal alongside data so both sides stay in lockstep. Asynchronous protocols (UART) pre-agree on a baud rate and each side runs its own clock — simpler wiring but requires matched clock accuracy. |
| **Full-duplex vs. Half-duplex** | Full-duplex (SPI, UART) can send and receive simultaneously on separate wires. Half-duplex (I2C, CAN) shares the same wire(s) for both directions, taking turns. |
| **Differential signaling** | Encoding data as the voltage *difference* between two wires rather than voltage relative to ground. Electromagnetic noise affects both wires equally and cancels when the receiver subtracts them, enabling long noisy cable runs. CAN and Ethernet use this; UART, I2C, and SPI don't. |
| **Bus topology** | How multiple devices connect. Point-to-point (UART): one sender, one receiver. Multi-drop bus (I2C, CAN): many devices on shared wires. Star (SPI): one master with a dedicated select line per device. |
| **Baud rate / Bit rate** | The number of signal transitions (baud) or data bits (bit rate) per second. For most embedded protocols these are equal. UART's 115200 baud = 115.2 kbps; CAN's 1 Mbps means each bit is 1 $\mu$s wide. |

<details>
<summary><strong>How It Works</strong> — Protocol comparison and selection</summary>

### The Protocol Landscape

```
EMBEDDED COMMUNICATION PROTOCOLS — COMPARISON:

Protocol    Wires  Speed       Distance   Topology         Use Case
────────────────────────────────────────────────────────────────────────
UART          2    115 kbps†   15 m       Point-to-point   Debug, GPS
I2C           2    400 kbps‡   1 m        Multi-drop       Sensors (IMU, ADC)
SPI           4+   50 Mbps     0.3 m      Star             Fast on-board comms
CAN           2    1 Mbps      40 m       Bus (linear)     Motors, vehicles
CAN FD        2    8 Mbps**    40 m***    Bus (linear)     Next-gen automotive
Ethernet      2-4  100 Mbps+   100 m      Star/switched    Cameras, high-bandwidth

† UART hardware supports 1-10+ Mbps; 115200 is the most common embedded rate
‡ 400 kbps = Fast Mode; also: Fm+ (1 Mbps), HS (3.4 Mbps), UFm (5 Mbps)
** 8 Mbps applies to data phase only; arbitration runs at ≤1 Mbps
*** 40 m at arbitration speed; data phase at 8 Mbps limited to a few meters
```

### UART — The Simplest Protocol

UART (Universal Asynchronous Receiver-Transmitter) is the oldest and simplest serial protocol. No clock wire — both sides agree on a baud rate beforehand (typically 115200 baud). Two wires: TX (transmit) and RX (receive), crossed between devices.

```
UART — Asynchronous, point-to-point:

  Device A              Device B
  ┌──────┐              ┌──────┐
  │   TX ├──────────────► RX   │
  │      │              │      │
  │   RX ◄──────────────┤ TX   │
  └──────┘              └──────┘
    (no clock wire — baud rate must match)

  Frame format (8N1 = 8 data bits, no parity, 1 stop bit):

  IDLE ─┐ ┌─┬─┬─┬─┬─┬─┬─┬─┐ ┌── IDLE
  (high) └─┤0│1│2│3│4│5│6│7├─┘  (high)
        START └─┴─┴─┴─┴─┴─┴─┘ STOP
        bit   data (LSB first)  bit

  10 bits per byte → 115200 baud ÷ 10 = 11,520 bytes/sec max
```

**Strengths:** Dead simple, universally supported, only 2 wires, good debug interface.
**Weaknesses:** Slow, point-to-point only (can't share a bus), no error detection built in, clock drift causes framing errors at high speeds.

### I2C — The Sensor Bus

[[learning/notes/micro-context/i2c|I2C]] (Inter-Integrated Circuit) uses 2 wires — SDA (data) and SCL (clock) — with open-drain drivers and pull-up [[learning/notes/quick-context/resistor|resistors]]. A master generates the clock and addresses devices by their 7-bit address (up to 128 devices on one bus, though typically 10-20).

```
I2C — Synchronous, multi-drop, half-duplex:

          ┌───────────────────────────────────── VCC
          │          │          │          │
         ┌┴┐        ┌┴┐        ┌┴┐        ┌┴┐
  pull-up│R│  SDA   │ │  SCL   │ │  SDA   │ │
         └┬┘        └┬┘        └┬┘        └┬┘
          │          │          │          │
  SDA ────┴──────────┼──────────┴──────────┼────
                     │                     │
  SCL ───────────────┴─────────────────────┴────
          │                     │
       ┌──┴─────┐           ┌──┴──┐
       │Master   │           │Slave│
       │(STM32)  │           │(IMU)│
       └─────────┘           └─────┘
        address: --           address: 0x4A

  Transaction: [START][addr+R/W][ACK][data][ACK]...[STOP]
```

**Strengths:** Only 2 wires for many devices, simple addressing, widely supported by sensors.
**Weaknesses:** Slow (400 kbps in Fast Mode, the most common embedded speed), short range (~1 m due to capacitive loading), half-duplex, pull-ups consume power, ACK/NACK is the only error handling.

### SPI — The Fast On-Board Bus

[[learning/notes/micro-context/spi|SPI]] (Serial Peripheral Interface) uses 4 wires: SCLK (clock), MOSI (master-out-slave-in), MISO (master-in-slave-out), and CS (chip select — one per slave). Full-duplex at speeds from 1 to 50+ MHz.

```
SPI — Synchronous, star topology, full-duplex:

                ┌─────────┐
                │  Master  │
                │ (STM32)  │
                └┬──┬──┬──┬┘
                 │  │  │  │
            SCLK │  │  │  │ CS0  CS1  CS2
            MOSI │  │  │  ├──┐
            MISO │  │  │  │  │    │    │
                 │  │  │  │  │    │    │
              ┌──┴──┴──┴──┴┐ │  ┌─┴┐ ┌─┴┐
              │   Slave 0  │ │  │S1│ │S2│
              │  (Flash)   │ │  └──┘ └──┘
              └────────────┘ │
                             │ (directly wired,
                              not a shared bus)

  SCLK + MOSI + MISO shared; one CS line per slave
  → 4 + (N-1) wires for N slaves
```

**Strengths:** Very fast (50+ MHz), full-duplex, no addressing overhead (hardware CS), no pull-ups needed.
**Weaknesses:** Many wires (one CS per slave), short range (~30 cm, single-ended), no flow control, no error detection, no standard — every chip defines its own SPI mode (CPOL/CPHA).

### CAN — The Noise-Immune Motor Bus

[[learning/notes/quick-context/can-bus|CAN]] (Controller Area Network) uses 2-wire differential signaling (CANH/CANL) with hardware arbitration, CRC error detection, and automatic retransmission. See the dedicated [[learning/notes/quick-context/can-bus|CAN bus article]] for the deep dive.

```
CAN — Asynchronous*, differential, linear bus:

   120Ω                                           120Ω
   ┤├────┬──────────┬──────────┬──────────┬────────┤├
  CANH   │          │          │          │       CANH
  CANL   │          │          │          │       CANL
   ┤├────┴──────────┴──────────┴──────────┴────────┤├
         │          │          │          │
      ┌──┴──┐    ┌──┴──┐    ┌──┴──┐    ┌──┴──┐
      │Node │    │Node │    │Node │    │Node │
      └─────┘    └─────┘    └─────┘    └─────┘

  * "Synchronous" at the bit level (bit stuffing keeps clocks
    aligned), but no external clock wire — each node uses its
    own oscillator, resynchronized on every edge.
```

**Strengths:** Differential = noise-immune, 40 m range, hardware arbitration (no collisions), 5-layer error detection, multi-master, 2 wires only.
**Weaknesses:** 1 Mbps max (classic CAN), 8-byte payload limit, needs [[learning/notes/micro-context/can-bus-transceiver|transceivers]] ($0.50-1 per node), [[learning/notes/micro-context/can-bus-termination|120$\Omega$ termination]] at both ends.

### Ethernet — The High-Bandwidth Option

Ethernet (typically 100BASE-TX or 1000BASE-T) uses differential pairs over Cat5/6 cable with a full TCP/IP or UDP stack. Massive bandwidth but significant complexity and latency for embedded use.

**Strengths:** 100 Mbps+, 100 m range, standard networking stack, switches enable complex topologies.
**Weaknesses:** High latency (milliseconds for TCP), large software stack (lwIP or Linux), per-node PHY chip + magnetics, power-hungry, overkill for simple sensor data.

### How the Pupper Uses All Four

```
PUPPER v3 — FOUR PROTOCOLS WORKING TOGETHER:

  ┌──────────────────────────────────────────────────────┐
  │                  Raspberry Pi                         │
  │              (Linux + Python + ROS2)                  │
  │                                                      │
  │  WiFi/Ethernet ◄──► laptop     UART ◄──► debug log  │
  └──────────────────────┬───────────────────────────────┘
                         │ SPI (40-pin header)
                         │ high-speed, on-board
                    ┌────┴─────┐
                    │ U1 (Main │    I2C ──► BNO086 (IMU)
                    │   MCU)   │    I2C ──► ADS1110 (ADC)
                    │          │    I2S ──► Speaker amp
                    └────┬─────┘
                         │ SPI
                    ┌────┴─────┐
                    │ U5 (Motor│
                    │   MCU)   │
                    └──┬─┬─┬─┬─┘
                       │ │ │ │   CAN (4 buses)
                       │ │ │ │   long cables, noisy
                       │ │ │ │   environment
                       ▼ ▼ ▼ ▼
                    3  3  3  3   servo motors
                    (12 total)

  SPI  = fast MCU-to-MCU (on-board, ~cm distance)
  I2C  = slow sensor reads (on-board, ~cm distance)
  CAN  = reliable motor comms (through legs, ~30 cm)
  UART = debug console (to Pi or USB adapter)
```

Each protocol is chosen for its sweet spot:
- **SPI** between U1↔U5: needs speed (joint targets at 1 kHz), both chips are on the same PCB
- **I2C** for IMU and ADC: low data volume, sensors come with I2C interfaces, only 2 wires
- **CAN** for servos: signals travel through leg cables where motors generate EMI, differential signaling is essential
- **UART** for debug: simple printf-style logging to a terminal, no configuration needed

</details>

<details>
<summary><strong>The Key Tension</strong> — No protocol wins on all axes</summary>

Every protocol makes tradeoffs between five axes. No protocol wins on more than 2-3:

```
PROTOCOL TRADEOFF RADAR:

                    Speed
                      │
                  SPI ████████
                  ETH █████████
                  CAN ███
                  I2C ██
                 UART █
                      │
  Wire Count ─────────┼───────── Distance
  (fewer=better)      │
   UART ██            │          CAN ████████
   I2C  ██            │          ETH █████████
   CAN  ██            │         UART ████
   SPI  ████████      │          I2C █
   ETH  ████          │          SPI █
                      │
                Noise Immunity
                  CAN ████████
                  ETH ████████
                  SPI █
                 UART █
                  I2C █
```

| Criterion | Best | Worst |
|-----------|------|-------|
| **Speed** | Ethernet (100 Mbps+), SPI (50 Mbps) | UART (115 kbps) |
| **Distance** | Ethernet (100 m), CAN (40 m) | SPI (0.3 m) |
| **Wire count** | UART/I2C/CAN (2 wires) | SPI (4 + N-1 CS lines) |
| **Noise immunity** | CAN/Ethernet (differential) | SPI/I2C/UART (single-ended) |
| **Simplicity** | UART (no config, just baud rate) | Ethernet (full TCP/IP stack) |
| **Multi-device** | I2C (128 addresses) | UART (point-to-point only) |
| **Latency** | SPI (hardware, microseconds) | Ethernet/TCP (milliseconds) |

**The real-world rule:** Pick the simplest protocol that meets your distance and speed requirements. For on-board sensors → I2C. For on-board fast data → SPI. For off-board in noisy environments → CAN. For high bandwidth → Ethernet. For debug → UART.

</details>

<details>
<summary><strong>Concrete Example</strong> — Reading a sensor over I2C vs. SPI</summary>

The same BNO086 IMU supports both I2C and SPI. Here's what the transaction looks like for each:

### I2C Read (2 wires, 400 kHz)

```
Reading 6 bytes of quaternion data from BNO086 at address 0x4A:

Master (STM32)                           Slave (BNO086)
─────────────                            ──────────────
START condition (SDA↓ while SCL high)
Send: 0x4A + W (write)          ──►
                                ◄──      ACK
Send: register address 0x14     ──►
                                ◄──      ACK
REPEATED START
Send: 0x4A + R (read)           ──►
                                ◄──      ACK
                                ◄──      Data byte 0 (quat W low)
ACK                             ──►
                                ◄──      Data byte 1 (quat W high)
ACK                             ──►
... (4 more bytes)
NACK (signals last byte)        ──►
STOP condition

Total: ~180 μs at 400 kHz for 6 bytes
       (address + register + 6 data + overhead)
```

### SPI Read (4 wires, 10 MHz)

```
Same 6 bytes over SPI:

Master                                   Slave
──────                                   ─────
CS → LOW (select BNO086)
SCLK starts toggling at 10 MHz
MOSI: send register 0x14 + read bit  ──►
MISO:                                ◄──  Data byte 0
MOSI: (don't care)                   ──►
MISO:                                ◄──  Data byte 1
... (4 more bytes, simultaneous)
CS → HIGH (deselect)

Total: ~5.6 μs at 10 MHz for 6 bytes
       (1 command byte + 6 data bytes = 56 bits at 10 MHz)
```

SPI is ~32x faster for this read — but it uses 4 wires vs I2C's 2, and can't share the bus with other sensors without extra CS lines. On the Pupper, the BNO086 uses I2C because the board already has I2C pull-ups and other I2C devices sharing the bus, and the IMU only sends data at ~100 Hz — 180 $\mu$s per read is negligible.

**The one thing most outsiders get wrong about this is...** assuming faster protocols are always better. SPI at 50 MHz sounds impressive, but if your sensor only produces 100 bytes/second, the 400 kbps I2C bus is utilizing 0.2% of its bandwidth — the "slow" protocol is more than fast enough, and you saved 2 PCB traces and a CS pin. Protocol selection is about matching the *minimum viable protocol* to the actual data requirements, not picking the fastest option.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/quick-context/can-bus]]** — Deep dive into CAN: arbitration, frame format, differential signaling, error detection, and the Pupper's 4-bus motor architecture. This is the most complex protocol in the comparison and gets its own article.

- **[[learning/notes/micro-context/i2c]]** — I2C protocol details: addressing, open-drain signaling, pull-up resistors, clock stretching. The standard sensor bus on embedded boards.

- **[[learning/notes/micro-context/spi]]** — SPI protocol details: clock polarity/phase modes (CPOL/CPHA), full-duplex data shifting, chip select. The fastest on-board bus.

- **[[learning/notes/micro-context/i2s]]** — I2S (Inter-IC Sound): a specialized SPI variant for streaming digital audio. Used on the Pupper between U1 and the MAX98357A amplifier.

- **[[learning/notes/micro-context/can-bus-transceiver]]** — The MAX3051 chip that converts single-ended MCU signals to differential CAN bus voltages. Every CAN node needs one.

- **[[learning/notes/micro-context/can-bus-termination]]** — The 120$\Omega$ termination resistors required at both ends of a CAN bus to prevent signal reflections.

- **[[learning/notes/quick-context/pupper-brain]]** — The full dual-MCU + Raspberry Pi architecture showing all four protocols in action: SPI between MCUs, I2C to sensors, CAN to motors, UART for debug.

- **[[learning/notes/quick-context/pupper-bom-control-board]]** — The physical components implementing these protocols: STM32s with hardware CAN/SPI/I2C peripherals, MAX3051 transceivers, pull-up resistors, connectors.

- **[[learning/notes/quick-context/oscilloscope-and-multimeter]]** — How to debug protocol issues: oscilloscope shows signal integrity (rise times, reflections, noise), logic analyzer decodes the actual data frames.

- **RS-485** — An industrial differential protocol similar to UART but with multi-drop capability and ~1200 m range. Common in factory automation where CAN isn't fast enough or Ethernet is overkill. Not used on the Pupper but frequently compared to CAN.

- **[[learning/notes/quick-context/wifi-chip-arduino-uno-r4]]** — How WiFi works at the chip level: radio transceiver, OFDM modulation, MAC/PHY layers, and antenna design. WiFi complements the wired protocols here — great for internet connectivity but too unreliable and high-latency for real-time control.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does the Pupper use I2C instead of SPI for the BNO086 IMU, even though SPI is ~32x faster?
<details>
<summary>Answer</summary>
The IMU only outputs data at ~100 Hz — roughly 600 bytes/second. I2C at 400 kbps has 50 kB/s of bandwidth, using ~1.2% capacity. The "slow" protocol is more than sufficient. Meanwhile, I2C saves pins (2 shared wires vs. 4 + CS), shares the bus with the ADS1110 ADC, and the board already has pull-up resistors. Speed only matters when data volume demands it.
</details>

**Q2:** A designer wants to connect 8 temperature sensors on a single PCB. Which protocol would you recommend and why?
<details>
<summary>Answer</summary>
**I2C.** Eight sensors on one PCB means short distances (<10 cm) and low data rates (a few bytes per second each). I2C uses only 2 wires shared by all 8 sensors (each with a unique address), vs. SPI which would need 2 + 8 = 10 wires (SCLK, MOSI/MISO, plus one CS per sensor). The simplicity and low wire count of I2C far outweighs its speed disadvantage for this use case.
</details>

**Q3:** Why can't I2C be used to communicate with the Pupper's servo motors instead of CAN?
<details>
<summary>Answer</summary>
Three reasons: (1) **Distance** — I2C is limited to ~1 m due to bus capacitance from pull-up resistors and trace length; servo cables run through robot legs at 30+ cm each. (2) **Noise immunity** — I2C uses single-ended signaling (voltage relative to ground), so motor EMI on the ground wire directly corrupts data; CAN's differential signaling rejects common-mode noise. (3) **Error handling** — I2C has only ACK/NACK; CAN has 5-layer error detection with automatic retransmission, critical for real-time motor control where a lost command could cause the robot to fall.
</details>

**Q4:** SPI is listed as having "no standard." What practical problem does this cause?
<details>
<summary>Answer</summary>
Every SPI device defines its own clock polarity (CPOL: idle high or low), clock phase (CPHA: sample on rising or falling edge), bit order (MSB or LSB first), word size, and command format. There are 4 possible CPOL/CPHA combinations (Mode 0-3), and the datasheet for each device specifies which one it uses. If you set the wrong mode, you get corrupted data with no error indication — SPI has no ACK or CRC, so the master can't tell the read failed. Compare to I2C where the spec defines exactly one protocol, or CAN where the frame format is standardized.
</details>

**Q5:** You're designing a robot arm with 6 joints. The motors need position commands at 500 Hz, each command is 4 bytes, and the longest cable run is 2 meters. CAN seems like overkill — could you use UART with RS-232 levels instead?
<details>
<summary>Answer</summary>
No — UART is point-to-point, so you'd need 6 separate UART ports (one per motor), consuming 12 MCU pins and 12 wires. Even with a multidrop hack (RS-485 transceivers + software addressing), UART has no hardware arbitration or collision detection — if two devices respond simultaneously, data is corrupted with no recovery. At 500 Hz × 6 motors × ~10 bytes/frame (including overhead), you need ~30,000 bytes/sec = 300 kbps — within UART's range, but with no error detection on a 2-meter cable near motors. CAN gives you: one shared bus (2 wires, not 12), hardware arbitration (no collisions), 5-layer error detection, automatic retransmission, and differential noise immunity — all for an extra $3 in transceivers. "Overkill" is actually "exactly right" for motor control over cables.
</details>

</details>
