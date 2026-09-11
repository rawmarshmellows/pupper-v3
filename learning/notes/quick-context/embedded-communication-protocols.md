---
topic: Embedded Communication Protocols — UART, I2C, SPI, CAN, RS-232, RS-485, 1-Wire, USB, I3C, and When to Use Each
created: 2026-03-27
updated: 2026-04-06
---

# Embedded Communication Protocols

> **Related:** [[quick-context/can-bus]] | [[quick-context/pupper-brain]] | [[quick-context/pupper-bom-control-board]]

> **TL;DR:** Embedded systems choose between a family of serial protocols — UART, [[micro-context/i2c|I2C]], [[micro-context/spi|SPI]], [[quick-context/can-bus|CAN]], RS-232, RS-485, 1-Wire, USB, I3C, and Ethernet — each optimizing a different point in the tradeoff space of speed, distance, wire count, noise immunity, and complexity. The Pupper v3 uses four simultaneously: SPI between MCUs, I2C for sensors, CAN for motors, and UART for debug — because no single protocol is best at everything. https://www.youtube.com/watch?v=0rlpwVNyBO8

## The Core Problem

A [[micro-context/microcontroller|microcontroller]] needs to talk to other chips — sensors, motors, displays, other MCUs, a host computer. But a typical [[micro-context/stm32-microcontroller|STM32]] only has 100 or so pins, and dedicating one pin per data bit (parallel communication) wastes pins and board space. Serial protocols solve this by sending data one bit at a time over just 1-4 wires, using a clock signal or agreed-upon timing to keep sender and receiver synchronized. The challenge is that different peripherals have wildly different needs: a temperature sensor sends 2 bytes every second (I2C is fine), but a motor controller needs 8 bytes every millisecond over a 1-meter cable with motors generating EMI (only CAN will do). And sometimes you need to talk to a PC (USB), reach industrial equipment 1200 m away (RS-485), or wire dozens of sensors on a single wire through a building (1-Wire).

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Synchronous vs. Asynchronous** | Synchronous protocols (SPI, I2C, I3C) send a clock signal alongside data so both sides stay in lockstep. Asynchronous protocols (UART, RS-232, RS-485, CAN) pre-agree on a baud rate and each side runs its own clock — simpler wiring but requires matched clock accuracy. |
| **Full-duplex vs. Half-duplex** | Full-duplex (SPI, UART, RS-232, USB 3.x) can send and receive simultaneously on separate wires. Half-duplex (I2C, I3C, CAN, RS-485, 1-Wire) shares the same wire(s) for both directions, taking turns. |
| **Differential signaling** | Encoding data as the voltage *difference* between two wires rather than voltage relative to ground. Electromagnetic noise affects both wires equally and cancels when the receiver subtracts them, enabling long noisy cable runs. CAN, RS-485, USB, and Ethernet use this; UART, I2C, SPI, and 1-Wire don't. |
| **Bus topology** | How multiple devices connect. Point-to-point (UART, RS-232, USB): one sender, one receiver. Multi-drop bus (I2C, I3C, CAN, RS-485, 1-Wire): many devices on shared wires. Star (SPI): one master with a dedicated select line per device. |
| **Baud rate / Bit rate** | The number of signal transitions (baud) or data bits (bit rate) per second. For most embedded protocols these are equal. UART's 115200 baud = 115.2 kbps; CAN's 1 Mbps means each bit is 1 $\mu$s wide. USB uses encoding schemes where baud and bit rate differ. |

<details>
<summary><strong>How It Works</strong> — Protocol comparison and selection</summary>

### The Protocol Landscape

```
EMBEDDED COMMUNICATION PROTOCOLS — COMPARISON:

Protocol    Wires  Speed       Distance   Topology         Use Case
────────────────────────────────────────────────────────────────────────
UART          2    115 kbps†   15 m       Point-to-point   Debug, GPS
RS-232        2-9  115 kbps†   15 m       Point-to-point   Legacy PCs, industrial
RS-485        2    10 Mbps     1200 m     Multi-drop       Industrial, long-haul
1-Wire        1    16 kbps‡    100 m      Multi-drop       Temp sensors, iButtons
I2C           2    400 kbps§   1 m        Multi-drop       Sensors (IMU, ADC)
I3C           2    12.5 Mbps   ~0.3 m     Multi-drop       Next-gen sensors
SPI           4+   50 Mbps     0.3 m      Star             Fast on-board comms
CAN           2    1 Mbps      40 m       Bus (linear)     Motors, vehicles
CAN FD        2    8 Mbps**    40 m***    Bus (linear)     Next-gen automotive
USB 2.0       4    480 Mbps    5 m        Star/tiered      PC↔device, storage
USB 3.x       9+   5-20 Gbps   3 m        Star/tiered      High-speed peripherals
Ethernet      2-4  100 Mbps+   100 m      Star/switched    Cameras, high-bandwidth

† UART/RS-232 hardware supports 1-10+ Mbps; 115200 is the most common rate
‡ 16 kbps standard; ~142 kbps in overdrive mode
§ 400 kbps = Fast Mode; also: Fm+ (1 Mbps), HS (3.4 Mbps), UFm (5 Mbps, unidirectional)
** 8 Mbps applies to data phase only; arbitration runs at ≤1 Mbps
*** 40 m at arbitration speed; data phase at 8 Mbps limited to a few meters
```

### UART — The Simplest Protocol

[[quick-context/uart|UART]] (Universal Asynchronous Receiver-Transmitter) is the oldest and simplest serial protocol. No clock wire — both sides agree on a baud rate beforehand (typically 115200 baud). Two wires: TX (transmit) and RX (receive), crossed between devices. For the full internal mechanics (shift registers, oversampling, baud rate generation), see the [[quick-context/uart|dedicated UART article]].

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

### RS-232 — UART's Physical Layer Standard

RS-232 is not a separate protocol — it defines the **electrical characteristics** for UART signals. While bare UART uses TTL/CMOS levels (0 V / 3.3 V), RS-232 uses inverted bipolar voltages: logic 1 = $-3$ to $-15$ V, logic 0 = $+3$ to $+15$ V. This wider voltage swing provides better noise margin over longer cables, but requires a level-shifting IC like the MAX232 (which uses charge pumps to generate ±7.5 V from a single 5 V supply).

```
RS-232 — UART with bipolar voltage levels:

  MCU (3.3V logic)    MAX232           DE-9 Connector      PC/Device
  ┌──────┐          ┌────────┐         ┌─────────┐        ┌──────┐
  │   TX ├──────────┤TTL→232 ├─────────┤3  TXD   ├────────┤ RXD  │
  │      │  0/3.3V  │        │ ±7.5V   │         │        │      │
  │   RX ◄──────────┤232→TTL ◄─────────┤2  RXD   ◄────────┤ TXD  │
  └──────┘          └────────┘         │5  GND   │        └──────┘
                    charge pump        │7  RTS   │ ← flow control
                    generates ±V       │8  CTS   │   (optional)
                    from +5V           └─────────┘

  Voltage levels (inverted logic!):
  ─────────────────────────────────────────────────
  TTL UART:   Logic 0 = 0V      Logic 1 = 3.3V
  RS-232:     Logic 0 = +3~+15V Logic 1 = -3~-15V
  ─────────────────────────────────────────────────
  The -3V to +3V range is the "transition region"
  (undefined) — valid signals must exceed ±3V.
```

The DE-9 connector (often incorrectly called "DB-9") has 9 pins, but most embedded use only needs 3: TXD, RXD, and GND. The extra pins (RTS, CTS, DTR, DSR, DCD, RI) provide hardware flow control and modem signaling — remnants of the dial-up era, but still used in industrial equipment.

**Strengths:** Better noise margin than TTL UART (wider voltage swing), standardized connector (DE-9), hardware flow control pins, huge legacy ecosystem (industrial PLCs, lab instruments, CNC machines).
**Weaknesses:** Still single-ended and point-to-point, max ~15 m at 115200 baud, requires level-shifting IC, bulky connectors, largely obsolete for new designs (replaced by USB or RS-485).

### RS-485 — The Industrial Long-Haul Bus

RS-485 takes the UART data frame and transmits it over differential signaling — similar conceptually to CAN but without CAN's built-in arbitration and framing. Two wires (A and B) carry the differential signal, enabling multi-drop networks of up to 32 devices (or 256 with high-impedance receivers) over cables up to 1200 m.

```
RS-485 — Differential, multi-drop:

  MCU          MAX485
  ┌──────┐    ┌───────┐       Twisted pair (up to 1200 m)
  │   TX ├────┤DI    A├───┬──────────┬──────────┬────── 120Ω
  │      │    │       │   │          │          │       termination
  │   RX ◄────┤RO    B├───┼──────────┼──────────┼────── 120Ω
  │      │    │       │   │          │          │
  │  DIR ├────┤DE/RE  │ ┌─┴──┐    ┌─┴──┐    ┌─┴──┐
  └──────┘    └───────┘ │Node│    │Node│    │Node│
                        │ 1  │    │ 2  │    │ 3  │
  DIR pin switches      └────┘    └────┘    └────┘
  between TX and RX
  (half-duplex)

  Differential voltage:
  ───────────────────────────────────────────
  Logic 1:  A > B by ≥ +200 mV
  Logic 0:  A < B by ≥ -200 mV
  ───────────────────────────────────────────
  Receiver needs only 200 mV differential → very noise-immune
```

RS-485 is **half-duplex** on 2 wires — a direction-control pin (DE/RE) on the transceiver switches between transmit and receive. Full-duplex requires 4 wires (two differential pairs). Note: RS-422 (TIA-422) is a related but separate standard that specifies one driver with up to 10 receivers — similar physical layer but different topology than multi-driver RS-485. Unlike CAN, RS-485 has **no built-in arbitration or framing** — if two nodes transmit simultaneously, the data collides. Software protocols (Modbus RTU, PROFIBUS) layer addressing and collision avoidance on top.

**Strengths:** 1200 m range (at lower speeds), differential noise immunity, up to 10 Mbps, multi-drop (32+ nodes), simple transceivers (~$0.30), well-established in industrial automation.
**Weaknesses:** Half-duplex (need software turn-around), no hardware arbitration (collisions possible), no standardized framing (need Modbus/PROFIBUS on top), software must manage bus access, 120 $\Omega$ termination required at both ends.

### 1-Wire — The Minimalist Bus

1-Wire (originally by Dallas Semiconductor, now Analog Devices) pushes minimalism to the extreme: a single data wire plus ground. Power can even be derived parasitically from the data line itself, eliminating the need for a VCC wire. Each device has a factory-programmed **64-bit unique ROM code**, so the master can individually address any device on the bus — no address conflicts, ever.

```
1-Wire — Single wire, parasitic power:

          ┌─── VCC (optional — can use parasitic power)
          │
         ┌┴┐
  4.7 kΩ │R│  pull-up
         └┬┘
          │
  DQ ─────┴───────┬──────────┬──────────┬──── (up to 100 m)
                   │          │          │
                ┌──┴──┐    ┌──┴──┐    ┌──┴──┐
                │DS18  │    │DS18  │    │DS18  │
                │B20   │    │B20   │    │B20   │
                └──┬──┘    └──┬──┘    └──┬──┘
                   │          │          │
  GND ─────────────┴──────────┴──────────┴────

  Parasitic power: when DQ is high, an internal diode charges
  a capacitor (CPP) inside each device. When DQ goes low for
  data, the device runs off the stored charge.

  Bit timing (standard speed):
  ─────────────────────────────────────────────
  Write 0:  Master pulls DQ low for 60-120 μs
  Write 1:  Master pulls low for 1-15 μs, releases
  Read:     Master pulls low 1-15 μs, samples at ~15 μs
  ─────────────────────────────────────────────
  Each bit takes ~60-120 μs → ~16 kbps max
```

The master discovers devices using the **ROM search algorithm** — a binary tree walk that identifies all 64-bit ROM codes on the bus, even without knowing how many devices are connected. This makes 1-Wire uniquely suited for hot-pluggable sensor networks.

**Strengths:** Absolute minimum wiring (1 wire + ground, or even parasitic 1-wire-only), 100 m range, unique 64-bit addresses (no conflicts), simple protocol, great for distributed temperature sensing.
**Weaknesses:** Very slow (~16 kbps standard, ~142 kbps overdrive), timing-critical (often bit-banged, not hardware-supported on most MCUs), limited device ecosystem (mostly temperature sensors and ID chips), parasitic power can't supply high-current operations without a strong pull-up.

### I2C — The Sensor Bus

[[micro-context/i2c|I2C]] (Inter-Integrated Circuit) uses 2 wires — SDA (data) and SCL (clock) — with open-drain drivers and pull-up [[quick-context/resistor|resistors]]. A master generates the clock and addresses devices by their 7-bit address (up to 128 devices on one bus, though typically 10-20).

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
**Weaknesses:** Slow (400 kbps in Fast Mode, the most common embedded speed), short range (~1 m due to capacitive loading), half-duplex, pull-ups consume power, ACK/NACK is the only error handling, a slave can hang the bus by clock-stretching indefinitely.

### I3C — I2C's Successor

I3C (MIPI Improved Inter-Integrated Circuit) is designed to replace I2C while maintaining backward compatibility. It uses the same 2 wires (SDA and SCL) and can share a bus with legacy I2C devices, but switches from open-drain to **push-pull signaling** for dramatically higher speeds and lower power.

```
I3C — Backward-compatible with I2C, much faster:

  Same 2 wires as I2C (SDA + SCL):

  ┌──────────────────────────────────────────────┐
  │                  I3C Bus                      │
  │  SDA ─────┬──────────┬──────────┬────        │
  │  SCL ─────┼──────────┼──────────┼────        │
  │           │          │          │            │
  │        ┌──┴──┐    ┌──┴──┐    ┌──┴──┐         │
  │        │I3C  │    │I3C  │    │I2C  │ legacy  │
  │        │accel│    │gyro │    │temp │ device  │
  │        └─────┘    └─────┘    └─────┘         │
  └──────────────────────────────────────────────┘

  Key differences from I2C:
  ─────────────────────────────────────────────────
  Feature        I2C              I3C
  ─────────────────────────────────────────────────
  Signaling      Open-drain       Push-pull (+ OD)
  Speed          3.4 Mbps max     12.5 Mbps (SDR)
                                  ~100 Mbps (HDR)
  Addressing     Fixed 7-bit      Dynamic assignment
  Interrupts     Extra IRQ wire   In-band (IBI)
  Power          Pull-ups waste   Push-pull saves
  ─────────────────────────────────────────────────
```

I3C's **in-band interrupts (IBI)** let a sensor signal the controller on the same SDA/SCL lines — no extra IRQ wire needed. **Dynamic addressing** means the controller assigns addresses at runtime, eliminating address conflicts. HDR (High Data Rate) modes reach 25-100+ Mbps using multi-lane or ternary encoding.

**Strengths:** Backward-compatible with I2C devices, 12.5 Mbps in standard mode (vs I2C's 3.4 Mbps max), in-band interrupts, dynamic addressing, lower power (push-pull), hot-join support.
**Weaknesses:** Still new — limited device availability as of 2026 (growing in mobile/IoT), more complex controller IP, short range (~30 cm, same as I2C/SPI), specification is managed by MIPI Alliance (membership required for full spec access).

### SPI — The Fast On-Board Bus

[[micro-context/spi|SPI]] (Serial Peripheral Interface) uses 4 wires: SCLK (clock), MOSI (master-out-slave-in), MISO (master-in-slave-out), and CS (chip select — one per slave). Full-duplex at speeds from 1 to 50+ MHz.

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

[[quick-context/can-bus|CAN]] (Controller Area Network) uses 2-wire differential signaling (CANH/CANL) with hardware arbitration, CRC error detection, and automatic retransmission. See the dedicated [[quick-context/can-bus|CAN bus article]] for the deep dive.

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
**Weaknesses:** 1 Mbps max (classic CAN), 8-byte payload limit, needs [[micro-context/can-bus-transceiver|transceivers]] ($0.50-1 per node), [[micro-context/can-bus-termination|120$\Omega$ termination]] at both ends.

### USB — The Host-Device Standard

USB (Universal Serial Bus) is a host-controlled protocol using differential signaling over a tiered star topology. Unlike the other protocols here, USB requires **enumeration** — when a device plugs in, the host interrogates it to discover its capabilities, assigns an address, and loads the appropriate driver. This complexity buys you plug-and-play convenience and very high speeds.

```
USB — Host-controlled, differential, tiered star:

  Host (PC/Pi)       Hub            Devices
  ┌──────────┐     ┌──────┐
  │ Root Hub ├─────┤ Hub  ├──────── Keyboard
  │          │     │      ├──────── Mouse
  │          ├─────┼──────┘
  │          │     └── MCU (STM32 as device)
  └──────────┘

  USB 2.0 wiring (4 wires):
  ─────────────────────────────
  VBUS (+5V) ─── power (500 mA max per port)
  D+         ─┐
  D-         ─┘ differential data pair
  GND        ─── ground

  USB 3.x adds:
  SSTX+/SSTX- ─── SuperSpeed transmit pair
  SSRX+/SSRX- ─── SuperSpeed receive pair
  GND_DRAIN    ─── drain wire
  → Full-duplex at 5-20 Gbps

  Speed tiers:
  ──────────────────────────────────────────
  USB 1.1 Low Speed:     1.5 Mbps
  USB 1.1 Full Speed:    12 Mbps
  USB 2.0 High Speed:    480 Mbps
  USB 3.0 SuperSpeed:    5 Gbps
  USB 3.1 SuperSpeed+:   10 Gbps
  USB 3.2 Gen 2x2:       20 Gbps
  USB4:                   40-80 Gbps
  ──────────────────────────────────────────
```

In embedded systems, USB appears in two roles: (1) the MCU acts as a **USB device** (presenting as a serial port, HID, mass storage, etc. to a host PC), or (2) the MCU acts as a **USB host** (reading a flash drive, controlling a camera). Most STM32s have USB 2.0 Full Speed (12 Mbps) built in; some have High Speed (480 Mbps) with an external PHY.

**Strengths:** Universal PC connectivity, plug-and-play, powers devices (5 V / 500 mA–3 A), extremely high bandwidth, standardized device classes (CDC serial, HID, MSC).
**Weaknesses:** Host-device model (not peer-to-peer), complex protocol stack (descriptors, endpoints, enumeration), 5 m max cable length (USB 2.0), requires USB-capable hardware on the MCU, high latency for real-time control (1 ms frame period on USB 2.0).

### Ethernet — The High-Bandwidth Option

Ethernet (typically 100BASE-TX or 1000BASE-T) uses differential pairs over Cat5/6 cable with a full TCP/IP or UDP stack. Massive bandwidth but significant complexity and latency for embedded use.

**Strengths:** 100 Mbps+, 100 m range, standard networking stack, switches enable complex topologies.
**Weaknesses:** High latency (milliseconds for TCP), large software stack (lwIP or Linux), per-node PHY chip + magnetics, power-hungry, overkill for simple sensor data.

### How the Pupper Uses Four Protocols

```
PUPPER v3 — FOUR PROTOCOLS WORKING TOGETHER:

  ┌──────────────────────────────────────────────────────┐
  │                  Raspberry Pi                         │
  │              (Linux + Python + ROS2)                  │
  │                                                      │
  │  WiFi/Ethernet ◄──► laptop     UART ◄──► debug log  │
  └───────┬──────────────┬───────────────────────────────┘
          │              │
          │ SPI          │ I2C  (both through 40-pin header)
          │ /dev/spidev0 │ /dev/i2c-N
          │ 6 MHz        │
     ┌────┴─────┐   ┌────┴──────┐
     │ MCU      │   │ IMU       │    (Pi reads IMU directly,
     │ (U1/U5)  │   │ (BNO086)  │     not through U1)
     └────┬─────┘   └───────────┘
          │
          │ CAN (4 buses)
          │ long cables, noisy environment
     ┌──┬─┴┬──┐
     ▼  ▼  ▼  ▼
     3  3  3  3   servo motors
     (12 total)

  SPI  = Pi-to-MCU motor commands (40-pin header, ~cm)
  I2C  = Pi-to-IMU sensor reads (40-pin header, ~cm)
  CAN  = MCU-to-motor comms (through legs, ~30 cm)
  UART = debug console (to Pi or USB adapter)

  Source: rt_spi.cpp, rt_bno055.cpp in
  github.com/Nate711/pupperv3-monorepo/
    ros2_ws/src/control_board_hardware_interface/src/rt/
```

Each protocol is chosen for its sweet spot:
- **SPI** between Pi↔MCU: high-speed joint commands at 1 kHz, Pi and board are stacked via 40-pin header
- **I2C** for IMU: low data volume, IMU has I2C interface, Pi reads orientation directly without MCU relay
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
                  USB ██████████
                  SPI ████████
                  ETH █████████
                  I3C ██████
                  CAN ███
                  485 ████
                  I2C ██
                 UART █
                  232 █
                   1W ▌
                      │
  Wire Count ─────────┼───────── Distance
  (fewer=better)      │
    1W █              │          485 ██████████
  UART ██             │          ETH █████████
   I2C ██             │          CAN ████████
   I3C ██             │           1W ████████
   CAN ██             │         UART ████
   232 ██             │          232 ████
   485 ██             │          USB ██
   ETH ████           │          I2C █
   USB ████           │          SPI █
   SPI ████████       │          I3C █
                      │
                Noise Immunity
                  CAN ████████
                  485 ████████
                  ETH ████████
                  USB ██████
                  SPI █
                 UART █
                  232 ██
                  I2C █
                  I3C █
                   1W █
```

| Criterion | Best | Worst |
|-----------|------|-------|
| **Speed** | USB (480 Mbps+), Ethernet (100 Mbps+), SPI (50 Mbps) | 1-Wire (16 kbps) |
| **Distance** | RS-485 (1200 m), Ethernet (100 m), 1-Wire (100 m) | SPI/I3C (0.3 m) |
| **Wire count** | 1-Wire (1+GND) | SPI (4+N-1), USB 3.x (9+) |
| **Noise immunity** | CAN/RS-485/Ethernet (differential) | SPI/I2C/UART/1-Wire (single-ended) |
| **Simplicity** | UART (no config, just baud rate), 1-Wire | USB (full enumeration stack), Ethernet (TCP/IP) |
| **Multi-device** | I2C/I3C (128+ addresses), 1-Wire (unlimited, 64-bit IDs) | UART/RS-232 (point-to-point only) |
| **Latency** | SPI (hardware, microseconds) | Ethernet/TCP (milliseconds), USB (1 ms frames) |

**The real-world rule:** Pick the simplest protocol that meets your distance and speed requirements. For on-board sensors → I2C (or I3C for new designs). For on-board fast data → SPI. For off-board in noisy environments → CAN. For long-haul industrial → RS-485. For minimal wiring over distance → 1-Wire. For PC connectivity → USB. For high bandwidth → Ethernet. For debug → UART.

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

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/uart]]** — Deep dive into UART internals: the receive shift register (chain of D flip-flops), 16× oversampling, parallel latch to data register, baud rate generation. The simplest protocol in the comparison, with its own article covering the hardware mechanics.

- **[[quick-context/can-bus]]** — Deep dive into CAN: arbitration, frame format, differential signaling, error detection, and the Pupper's 4-bus motor architecture. This is the most complex protocol in the comparison and gets its own article.

- **[[micro-context/i2c]]** — I2C protocol details: addressing, open-drain signaling, pull-up resistors, clock stretching. The standard sensor bus on embedded boards.

- **[[micro-context/spi]]** — SPI protocol details: clock polarity/phase modes (CPOL/CPHA), full-duplex data shifting, chip select. The fastest on-board bus.

- **[[micro-context/i2s]]** — [[micro-context/i2s|I2S (Inter-IC Sound)]]: a specialized SPI variant for streaming digital audio. Used on the Pupper between U1 and the MAX98357A amplifier.

- **[[micro-context/can-bus-transceiver]]** — The MAX3051 chip that converts single-ended MCU signals to differential [[quick-context/can-bus|CAN bus]] voltages. Every CAN node needs one.

- **[[micro-context/can-bus-termination]]** — The 120$\Omega$ termination resistors required at both ends of a CAN bus to prevent signal reflections.

- **[[quick-context/pupper-brain]]** — The full dual-MCU + Raspberry Pi architecture showing all four protocols in action: SPI between MCUs, I2C to sensors, CAN to motors, UART for debug.

- **[[quick-context/pupper-bom-control-board]]** — The physical components implementing these protocols: STM32s with hardware CAN/SPI/I2C peripherals, MAX3051 transceivers, pull-up resistors, connectors.

- **[[quick-context/oscilloscope-and-multimeter]]** — How to debug protocol issues: oscilloscope shows signal integrity (rise times, reflections, noise), logic analyzer decodes the actual data frames.

- **[[quick-context/wifi-chip-arduino-uno-r4]]** — How WiFi works at the chip level: radio transceiver, OFDM modulation, MAC/PHY layers, and antenna design. WiFi complements the wired protocols here — great for internet connectivity but too unreliable and high-latency for real-time control.

- **[[quick-context/usb-peripheral-hardware]]** — Deep dive into how the USB peripheral inside an MCU works at the hardware level: the Serial Interface Engine (SIE), NRZI encoding, bit stuffing, CRC generation, and the [[micro-context/mosfet|MOSFET]] output drivers that create voltage transitions on D+/D- at 12 MHz. Covers the bridge between "firmware writes to a buffer" and "voltage appears on the wire."

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does the Pupper use I2C instead of SPI for the BNO086 IMU, even though SPI is ~32x faster?
<details>
<summary>Answer</summary>
The IMU only outputs data at ~100 Hz — roughly 600 bytes/second. I2C at 400 kbps has 50 kB/s of bandwidth, using ~1.2% capacity. The "slow" protocol is more than sufficient. Meanwhile, I2C saves pins (2 shared wires vs. 4 + CS), shares the bus with the [[micro-context/ads1110-battery-adc|ADS1110]] ADC, and the board already has pull-up resistors. Speed only matters when data volume demands it.
</details>

**Q2:** You need to read temperature from 50 sensors spread across a large building (cable runs up to 80 m). Which protocol and why?
<details>
<summary>Answer</summary>
**1-Wire.** Each DS18B20 temperature sensor has a unique 64-bit ROM code, so all 50 can share a single data wire + ground — just 2 conductors running through the building. 1-Wire supports up to 100 m cable runs. The data rate (~16 kbps) is more than sufficient: 50 sensors × 2 bytes × once per second = 100 bytes/sec. I2C can't reach 80 m (limited to ~1 m). CAN could do the distance but requires transceivers at every node ($0.50-1 × 50 = $25-50 in transceivers alone) and each sensor would need an MCU to speak CAN. 1-Wire sensors cost ~$1 each and need no additional hardware.
</details>

**Q3:** An engineer wants to replace the Pupper's CAN motor bus with RS-485 to save money on transceivers. What problems would they face?
<details>
<summary>Answer</summary>
Two critical problems: (1) **No hardware arbitration** — RS-485 is a raw differential bus with no collision detection. If the MCU sends a command while a motor driver is responding, both signals collide and corrupt each other. The engineer would need to implement software turn-around timing and a master-slave polling protocol (like Modbus), adding latency. CAN's hardware arbitration handles this automatically with zero data loss. (2) **No built-in error detection** — CAN has 5-layer error detection (CRC, frame check, ACK, bit monitoring, bit stuffing) with automatic retransmission. RS-485 has none — the software protocol must add checksums and retry logic. At 1 kHz motor control with 12 servos, any missed or corrupted frame could cause the robot to stumble. The ~$6 saved on transceivers isn't worth the reliability loss.
</details>

**Q4:** RS-232 and UART carry the same data frames. Why does RS-232 exist at all — why not just use TTL UART everywhere?
<details>
<summary>Answer</summary>
RS-232's bipolar voltage swing ($\pm$3 to $\pm$15 V) provides much better noise margin than TTL's 0-3.3 V over longer cables. A TTL UART signal riding on a 15 m cable in a factory picks up enough noise to corrupt the 3.3 V signal, but RS-232's ±7.5 V swing with a 6 V noise margin survives. RS-232 also standardized the connector (DE-9), pin assignments, and flow control signals (RTS/CTS/DTR), creating a universal interface for connecting to PCs, modems, and industrial equipment. In the pre-USB era, RS-232 was *the* way to connect anything to a computer. Today, TTL UART is used for on-board or short debug connections (where noise isn't an issue), and RS-232 persists in legacy industrial equipment — but new designs typically use USB or RS-485 instead.
</details>

**Q5:** You're designing an IoT sensor hub that reads from an accelerometer (I3C-capable), 20 temperature probes spread over 50 m of cable, and sends data to a cloud gateway over Ethernet. A colleague suggests "just use I2C for everything." Explain why you'd use three different protocols and how they'd connect.
<details>
<summary>Answer</summary>
Each interface has different distance, speed, and topology requirements that no single protocol can satisfy:

1. **I3C for the accelerometer:** It's on the same PCB as the hub MCU (~cm distance), and the accelerometer supports I3C natively. I3C gives 12.5 Mbps (vs I2C's 400 kbps), in-band interrupts (the accelerometer can signal motion events without a separate IRQ wire), and dynamic addressing. I2C would also work here, but I3C is better for a new design.

2. **1-Wire for the 20 temperature probes:** They're spread over 50 m of cable — far beyond I2C's ~1 m range. 1-Wire DS18B20 sensors can share a single wire over 100 m, each with a unique 64-bit ID. I2C would need repeaters every meter and can only address 128 devices with potential conflicts. Running 20 individual I2C buses is impractical.

3. **Ethernet for the cloud gateway:** Needs reliable, high-bandwidth connectivity over 100 m to a router. I2C maxes out at 3.4 Mbps over 1 m — it can't physically reach the router, let alone carry TCP/IP traffic.

The MCU hub connects all three: I3C on-board pins → accelerometer, a GPIO bit-banging 1-Wire → temperature string, and an Ethernet PHY → network. The colleague's I2C-for-everything approach fails on distance (temperature probes) and connectivity (cloud gateway).
</details>

</details>
