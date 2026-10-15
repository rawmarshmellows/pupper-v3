---
topic: CAN Bus (Controller Area Network)
created: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/can-bus-termination]] | [[learning/notes/micro-context/can-bus-transceiver]] | [[learning/notes/quick-context/data-bus-and-arbitration]]

# CAN Bus (Controller Area Network)

> **[[learning/notes/quick-context/tensile-strength-materials|]]Related:** [[quick-context/pupper-brain]] | [[quick-context/pupper-bom-control-board]] | [[quick-context/firmware]] | [[quick-context/embedded-communication-protocols]]

> **TL;DR:** [[learning/notes/quick-context/embedded-communication-protocols|CAN]] [[learning/notes/quick-context/data-bus-and-arbitration|bus]] is [[learning/notes/quick-context/anions-and-oxidation|a]] robust, multi-[[learning/notes/quick-context/data-bus-and-arbitration|master]] [[learning/notes/quick-context/data-bus-and-arbitration|serial protocol]] that lets dozens of devices communicate over a shared [[learning/notes/quick-context/meddpicc-qualification-framework|2]]-wire [[learning/notes/quick-context/differential-pair|differential pair]] without a central controller — originally designed for cars in [[learning/notes/quick-context/capacitance|the]] 1980s, it's now the backbone of automotive, industrial, [[learning/notes/micro-context/push-pull-vs-open-drain|and]] robotic systems (including Pupper's motor control) because it prioritizes [[learning/notes/quick-context/bond-pad|reliability]] in electrically noisy environments over [[learning/notes/quick-context/python-to-machine-code-pipeline|raw speed]].

## The Core Problem

A robot [[learning/notes/quick-context/breaking-elongation-rate|with]] 12 motors needs to send position commands and receive encoder feedback from each motor [[learning/notes/quick-context/meddpicc-qualification-framework|1]][[learning/notes/quick-context/how-passive-and-discrete-components-are-made|,]]000 times per second. Running 12 separate [[learning/notes/quick-context/uart|wires]] would be a heavy, fragile wiring harness. You need a protocol where many devices share a single wire pair, where [[learning/notes/quick-context/ros2-architecture|messages]] get through even with motors generating electromagnetic interference, and where the most urgent messages (like emergency [[learning/notes/quick-context/camera-fundamentals|stop]]) always win — without any central coordinator arbitrating traffic. CAN bus solves all three: shared bus, differential [[learning/notes/quick-context/embedded-communication-protocols|noise immunity]], and [[learning/notes/quick-context/data-bus-and-arbitration|priority]]-based [[learning/notes/quick-context/data-bus-and-arbitration|arbitration]] built into the physics of the wire.

## 5 Essential Terms

| Term | [[learning/notes/quick-context/capacitance|Definition]] |
|------|------------|
| **[[learning/notes/quick-context/uart|Frame]]** | A single CAN message: an [[learning/notes/quick-context/similarity-transform|11]]-bit ([[learning/notes/micro-context/push-pull-vs-open-drain|or]] 29-bit extended) identifier for priority/addressing, [[learning/notes/quick-context/meddpicc-qualification-framework|0]]-[[learning/notes/quick-context/comparator-specification|8]] [[learning/notes/quick-context/how-source-code-is-stored|bytes]] of data, and a CRC for [[learning/notes/quick-context/uart|error detection]] — everything a [[learning/notes/quick-context/ros2-architecture|node]] needs to communicate in [[learning/notes/quick-context/ram-addressing-decoder|one]] shot |
| **Arbitration** | The process by which multiple nodes trying to transmit [[learning/notes/quick-context/bare-minimal-data-storage-circuit|simultaneously]] resolve who wins — each node watches the bus while transmitting, and the message with the lowest ID (most 0-bits) wins without any data loss or collision |
| **[[learning/notes/quick-context/differential-pair|Differential pair]] (CANH/CANL)** | The [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] wires of the bus — a [[micro-context/can-bus-transceiver|transceiver]] drives them in opposite directions so that noise affecting [[learning/notes/quick-context/bjt-specifications|both]] wires equally cancels [[learning/notes/micro-context/push-pull-vs-open-drain|out]] [[learning/notes/quick-context/bare-minimal-data-storage-circuit|when]] the receiver subtracts CANL from CANH |
| **Dominant / Recessive** | CAN's two logical states: dominant (logical 0) actively drives the bus to a differential [[learning/notes/quick-context/voltage|voltage]]; recessive (logical 1) lets the bus float to [[learning/notes/micro-context/capacitive-voltage-sensing|no]] differential voltage — dominant always overwrites recessive, which is [[learning/notes/quick-context/bare-minimal-data-storage-circuit|what]] makes arbitration work |
| **[[micro-context/can-bus-termination|Termination]]** | The 120$\Omega$ [[quick-context/resistor|resistors]] at each end of the bus that match the wire's characteristic [[quick-context/impedance-and-reactance|impedance]] and absorb signals to prevent reflections |

## How CAN Fits in the Protocol Landscape

```
EMBEDDED COMMUNICATION PROTOCOLS — WHERE CAN SITS:

Protocol    Wires  Speed       Distance   Topology     Use Case
────────────────────────────────────────────────────────────────
UART          2    115 kbps    15 m       Point-to-point   Debug, GPS
I2C           2    400 kbps    1 m        Multi-drop       Sensors (IMU, ADC)
SPI           4+   50 Mbps     0.3 m      Star             Fast on-board comms
CAN           2    1 Mbps      40 m       Bus (linear)     Motors, vehicles
CAN FD        2    8 Mbps      40 m       Bus (linear)     Next-gen automotive
Ethernet      2-4  100 Mbps+   100 m      Star/switched    Cameras, high-bandwidth
```

CAN occupies the sweet spot between [[micro-context/i2c|I2C]] (short-range sensor bus) and Ethernet (high-[[learning/notes/quick-context/embedded-communication-protocols|speed]] network): it's [[learning/notes/quick-context/comparator|fast]] enough for real-time motor control, robust enough for long noisy cables, and simple enough that a $0.50 [[micro-context/stm32-microcontroller|microcontroller]] peripheral handles the entire protocol in [[learning/notes/quick-context/code-to-gates-and-bootstrapping|hardware]].

<details>
<summary><strong>How It Works</strong></summary>

### The Bus: One Shared Wire Pair

CAN uses a linear [[learning/notes/quick-context/embedded-communication-protocols|bus topology]] — a single twisted pair (CANH and CANL) with all nodes tapped in [[learning/notes/quick-context/parallel-vs-series-voltage|parallel]]. Each node connects through a [[micro-context/can-bus-transceiver|CAN transceiver]] that converts the [[micro-context/microcontroller|MCU's]] digital TX/RX to differential voltages:

```
CAN BUS TOPOLOGY:

   120Ω                                                    120Ω
   ┤├─────┬──────────────┬──────────────┬──────────────┬───┤├
  CANH    │              │              │              │  CANH
          │              │              │              │
  CANL    │              │              │              │  CANL
   ┤├─────┴──────────────┴──────────────┴──────────────┴───┤├
  (term)  │              │              │              │  (term)
       ┌──┴──┐        ┌──┴──┐        ┌──┴──┐        ┌──┴──┐
       │XCVR │        │XCVR │        │XCVR │        │XCVR │
       └──┬──┘        └──┬──┘        └──┬──┘        └──┬──┘
       ┌──┴──┐        ┌──┴──┐        ┌──┴──┐        ┌──┴──┐
       │ MCU │        │Servo│        │Servo│        │Servo│
       └─────┘        └─────┘        └─────┘        └─────┘
       Controller      Node 1         Node 2         Node 3

  Only TWO endpoints get termination resistors.
  Middle nodes must NOT add termination.
```

### Dominant vs. Recessive: The Wired-AND Trick

CAN's genius is its electrical [[learning/notes/quick-context/how-source-code-is-stored|encoding]]. The bus has two states:

- **Recessive (logic 1):** No node drives the bus. CANH and CANL both sit at ~2.5V. Differential voltage = 0V.
- **Dominant (logic 0):** A transmitting node drives CANH to ~[[learning/notes/quick-context/meddpicc-qualification-framework|3]].5V and CANL to ~1.5V. Differential voltage = ~2V.

If any node drives dominant, the bus goes dominant — regardless of what other nodes are doing. This is a "wired-AND" behavior: dominant (0) always wins over recessive (1).

```
DOMINANT vs. RECESSIVE SIGNAL LEVELS:

  Voltage
  (V)
  3.5 ─  ─ ─ ─ CANH ──┐           ┌── CANH
                        │           │
  2.5 ── ──────────────┼───────────┼────────── (both idle)
                        │           │
  1.5 ─  ─ ─ ─ CANL ──┘           └── CANL
                        │           │
          RECESSIVE     │ DOMINANT  │  RECESSIVE
          (logic 1)     │ (logic 0) │  (logic 1)
          diff = 0V     │ diff = 2V │  diff = 0V
                        │           │
  Receiver threshold: ~0.9V differential
  → Noise must exceed 0.9V on BOTH wires to cause an error
```

### Arbitration: Non-Destructive Priority

When two nodes transmit simultaneously, arbitration happens automatically during the ID field:

1. Both nodes start transmitting their message ID bit-by-bit.
2. After each bit, each node reads the bus to check if its transmitted bit matches.
3. If a node sent recessive (1) but reads dominant (0), some other node with a lower ID is transmitting — the losing node backs [[learning/notes/quick-context/bjt-specifications|off]] immediately.
[[learning/notes/quick-context/similarity-transform|4]]. The winning node doesn't even know contention occurred — its message continues uninterrupted.

```
ARBITRATION EXAMPLE — Two nodes transmit simultaneously:

  Node A (ID = 0x123 = 0001 0010 0011):
  Bit:    0   0   0   1   0   0   1   0   0   0   1   1
          D   D   D   R   D   D   R   D   D   D   R   R
                      ↑
  Node B (ID = 0x125 = 0001 0010 0101):
  Bit:    0   0   0   1   0   0   1   0   0   1   ...
          D   D   D   R   D   D   R   D   D   R
                                              ↑
  Bus:    0   0   0   1   0   0   1   0   0   0  ← DOMINANT wins
                                              │
                          Node B sent R(1) but reads D(0)
                          → Node B BACKS OFF, Node A continues

  Lower ID = more dominant bits = HIGHER PRIORITY
  ID 0x000 is the highest-priority message on the bus
```

### The CAN Frame Format

Every CAN message follows a strict frame structure:

```
STANDARD CAN FRAME (CAN 2.0A):

 SOF  Arbitration    Control    Data       CRC        ACK  EOF
  │   Field          Field      Field      Field      │    │
  │   ┌──────────┐   ┌────┐   ┌────────┐  ┌───────┐  │    │
  ▼   │ 11-bit   │RTR│DLC │   │ 0-8    │  │15-bit │  │    │
  1   │   ID     │ 1 │ 4  │   │ bytes  │  │  CRC  │ACK│ 7 │
 bit  │          │bit│bits│   │(payload)│  │       │2b │bits│
      └──────────┘   └────┘   └────────┘  └───────┘   └───┘

 SOF = Start of Frame (1 dominant bit — synchronizes all nodes)
 ID  = Message identifier (NOT an address — identifies CONTENT)
 RTR = Remote Transmission Request (1 = requesting data)
 DLC = Data Length Code (0-8 bytes)
 CRC = Cyclic Redundancy Check (detects transmission errors)
 ACK = Acknowledgement (receivers pull dominant to confirm receipt)
 EOF = End of Frame (7 recessive bits)

 Total overhead: ~47 bits for up to 64 bits of data
 At 1 Mbps: one 8-byte frame takes ~130 μs
```

**Key insight:** CAN IDs identify message *content*, [[learning/notes/micro-context/can-bus-termination|not]] destination *addresses*. A message with ID 0x201 might mean "motor 1 position feedback" — any node that cares about motor 1 reads it, and others ignore it. This publish-subscribe model means adding a new listener requires [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|zero]] changes to the transmitter.

### Error Detection: Five Layers Deep

CAN is exceptionally [[learning/notes/quick-context/ros2-architecture|reliable]] because it checks for errors at five levels:

1. **CRC check** — 15-bit CRC catches bit errors in the frame
2. **ACK check** — at least one receiver [[learning/notes/quick-context/ros2-architecture|must]] acknowledge, or the frame is retransmitted
3. **Bit monitoring** — transmitter reads back every bit; mismatch = error
4. **Bit stuffing** — after 5 consecutive [[learning/notes/quick-context/ram-addressing-decoder|identical]] bits, a stuff bit is inserted; violation = error
5. **Frame check** — fixed-format [[learning/notes/quick-context/code-to-gates-and-bootstrapping|fields]] (EOF, delimiters) must have expected values

A node that detects errors too often is automatically isolated from the bus ("bus-off" state) to prevent a faulty node from bringing down the entire network.

</details>

<details>
<summary><strong>[[learning/notes/quick-context/3d-printing-filament-types|The Key Tension]]</strong> — Speed vs. [[learning/notes/quick-context/embedded-communication-protocols|Distance]] vs. Node [[learning/notes/quick-context/switches-to-registers-storing-data|Count]]</summary>

CAN's [[learning/notes/quick-context/uart|physical layer]] imposes a fundamental tradeoff governed by the speed of light:

**[[learning/notes/quick-context/atoms-molecules-polymers-basics|Why]] speed limits distance:** Arbitration requires every node to see the bus state *within one bit time*. At 1 Mbps, one bit = 1 μs. A [[learning/notes/quick-context/comparator|signal]] takes ~5 ns/m on a twisted pair, so a 40-meter bus has ~400 ns round-trip delay — just under the 1 μs budget. Double the speed to 2 Mbps and the maximum bus length halves to ~20 m.

```
SPEED vs. DISTANCE TRADEOFF:

  Bit Rate    Max Bus Length    Bit Time    Round-trip budget
  ─────────────────────────────────────────────────────────
  1 Mbps      40 m              1 μs        ~800 ns
  500 kbps    100 m             2 μs        ~1.6 μs
  250 kbps    250 m             4 μs        ~3.2 μs
  125 kbps    500 m             8 μs        ~6.4 μs
  50 kbps     800 m             20 μs       ~16 μs

  The constraint: arbitration bit must propagate to the
  farthest node AND back within one bit time.
```

**CAN 2.0 vs. CAN FD:** Classic CAN (2.0) maxes out at 1 Mbps with 8-[[learning/notes/quick-context/how-source-code-is-stored|byte]] payloads. CAN FD (Flexible Data-rate) keeps the same arbitration phase at the original speed but accelerates the data phase up to 8 Mbps and expands payloads to 64 bytes. This works because arbitration [[learning/notes/quick-context/comparator-specification|only]] needs slow, bus-wide consistency, while the data phase is [[learning/notes/quick-context/epson-rc-plus-programming|point]]-to-point verified by CRC.

**Bus [[learning/notes/quick-context/teep|utilization]]:** With 12 servos each sending/receiving at 1 kHz, a single 1 Mbps CAN bus would need ~24,000 frames/sec. Each 8-byte frame takes ~130 μs, so 24,000 frames need ~3.1 seconds of bus time per second — impossible on a single bus. This is exactly why the Pupper splits into 4 buses with 3 servos each (~25% utilization per bus), leaving headroom for retransmissions. See [[quick-context/pupper-bom-control-board]].

</details>

<details>
<summary><strong>Concrete Example</strong> — Pupper's CAN Motor Control</summary>

The Pupper v3 uses 4 CAN buses at 1 Mbps to command 12 servo motors. Here's the complete signal path for one motor command:

```
PUPPER CAN ARCHITECTURE:
================================================================

  Raspberry Pi (Linux)
       │ high-level commands (walk, turn)
       ▼
  ┌─────────┐  SPI   ┌─────────┐
  │   U1    │───────►│   U5    │  Motor MCU
  │Main MCU │        │(CAN tx) │
  └─────────┘        └────┬────┘
                          │
              ┌───────────┼───────────┐───────────┐
              │           │           │           │
           ┌──┴──┐     ┌──┴──┐     ┌──┴──┐     ┌──┴──┐
           │U3   │     │U4   │     │U6   │     │U7   │
           │3051 │     │3051 │     │3051 │     │3051 │
           └──┬──┘     └──┬──┘     └──┬──┘     └──┬──┘
              │           │           │           │
         CAN Bus 1   CAN Bus 2   CAN Bus 3   CAN Bus 4
         120Ω─┤├     120Ω─┤├     120Ω─┤├     120Ω─┤├
           ┌──┼──┐     ┌──┼──┐     ┌──┼──┐     ┌──┼──┐
           │  │  │     │  │  │     │  │  │     │  │  │
           S1 S2 S3    S4 S5 S6    S7 S8 S9    S10 S11 S12
           └──┼──┘     └──┼──┘     └──┼──┘     └──┼──┘
         120Ω─┤├     120Ω─┤├     120Ω─┤├     120Ω─┤├

  S1-S12 = servo motors (each has its own CAN transceiver + MCU)
  4 buses × 3 servos = 12 total, ~25% utilization each
```

### A Single Motor Command, Step by Step

```
1. U5 firmware builds a CAN frame:
   ┌────────────────────────────────────────────────┐
   │  ID: 0x141          (motor 1 position command) │
   │  DLC: 8             (8 bytes of data)          │
   │  Data: [cmd_type, pos_hi, pos_lo, vel_hi,      │
   │         vel_lo, torque_hi, torque_lo, checksum] │
   └────────────────────────────────────────────────┘

2. STM32's CAN peripheral serializes the frame:
   adds SOF, CRC, ACK slot, EOF, handles bit stuffing

3. MAX3051 transceiver converts to differential:
   TX logic 0 → CANH=3.5V, CANL=1.5V (dominant)
   TX logic 1 → CANH=2.5V, CANL=2.5V (recessive)

4. Signal travels along twisted pair through robot leg cable

5. Servo's CAN transceiver receives differential signal:
   CANH - CANL > 0.9V → dominant (0)
   CANH - CANL < 0.5V → recessive (1)

6. Servo's MCU CAN peripheral deserializes frame,
   checks CRC, sends ACK (drives dominant during ACK slot)

7. Servo firmware reads position target, drives motor via PWM

8. Servo transmits feedback frame (ID: 0x241):
   [position, velocity, current, temperature]
   → U5 reads this to close the control loop
```

### What a CAN Frame Looks Like on an Oscilloscope

```
CANH and CANL on a scope during one frame:

  V
 3.5 ─ ─ CANH ─┐  ┌─┐     ┌─────┐  ┌─┐  ┌───
                │  │ │     │     │  │ │  │
 2.5 ──────────┼──┼─┼─────┼─────┼──┼─┼──┼──── idle
                │  │ │     │     │  │ │  │
 1.5 ─ ─ CANL ─┘  └─┘     └─────┘  └─┘  └───
               D  D R D     D     D  D R  D
              SOF  ←── ID bits ───→  data...

  D = dominant (differential ~2V)
  R = recessive (differential ~0V)
  Each bit at 1 Mbps = 1 μs wide
```

**The one thing most outsiders get wrong about this is...** thinking CAN bus addresses are like IP addresses — that you send a message "to" a specific device. CAN has no addresses at all. The ID field identifies the *message content*, not the destination. When a servo transmits ID 0x241, it's broadcasting "here is motor 1's feedback" — it doesn't know or care who's listening. Any node on the bus can read any message. This content-based publish-subscribe model is why CAN scales so well: adding a new data logger or diagnostic [[learning/notes/quick-context/epson-rc-plus-programming|tool]] requires zero changes to existing nodes.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[micro-context/can-bus-transceiver]]** — The MAX3051 chip that converts the MCU's single-ended digital TX/RX into differential CANH/CANL signals. This micro-context covers the physical [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|layer]] interface that CAN depends on.

- **[[micro-context/can-bus-termination]]** — The 120$\Omega$ resistors at each bus endpoint. Explains why unterminated buses fail at high speeds and how the Pupper's R1-R4 terminate its 4 CAN buses.

- **[[micro-context/spi]]** — The protocol U1 uses to send joint targets to U5 on the Pupper. [[learning/notes/micro-context/spi|SPI]] is faster but point-to-point; CAN is slower but multi-drop and noise-immune — they complement each other.

- **[[micro-context/i2c]]** — Another 2-wire [[learning/notes/quick-context/embedded-communication-protocols|multi-device]] bus, but designed for short-range, [[learning/notes/quick-context/usb-peripheral-hardware|low-speed]] sensor communication. Comparing [[learning/notes/micro-context/i2c|I2C]] and CAN highlights why different communication needs call for different [[learning/notes/quick-context/qwiic-stemma-qt-i2c|protocols]].

- **[[quick-context/pupper-brain]]** — The [[learning/notes/quick-context/singular-value-decomposition|full]] [[learning/notes/quick-context/comparator-specification|dual]]-MCU + Raspberry Pi architecture showing how CAN fits into the Pupper's control loop: Pi → U1 → SPI → U5 → CAN → 12 servos.

- **[[quick-context/pupper-bom-control-board]]** — Every physical [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|component]] in the CAN subsystem: the 4 MAX3051 transceivers (U3, U4, U6, U7), the 120$\Omega$ termination resistors (R1-R4), and the [[learning/notes/quick-context/dupont-jumper-wires|JST connectors]] (CN1, CN2) carrying CAN signals to the servo cables.

- **[[quick-context/firmware]]** — The STM32 [[learning/notes/quick-context/firmware|firmware]] initializes the CAN peripheral, configures bit [[learning/notes/quick-context/comparator-specification|timing]], and handles frame transmission/reception [[learning/notes/quick-context/metal-interconnect-layers|via]] [[learning/notes/quick-context/keypress-to-pixel-pipeline|interrupts]] or DMA. CAN is a [[learning/notes/quick-context/uart|hardware peripheral]] — the protocol [[learning/notes/quick-context/integration-failure-modes-solutions|state machine]] runs in [[learning/notes/quick-context/transistor|silicon]], not [[learning/notes/quick-context/code-to-gates-and-bootstrapping|software]].

- **[[quick-context/grounding-and-return-paths]]** — CAN's [[learning/notes/quick-context/embedded-communication-protocols|differential signaling]] is robust because noise appears as common-mode voltage on both wires; the receiver's subtraction rejects it. Understanding return paths explains why CAN also needs a shared ground [[learning/notes/quick-context/comparator|reference]] between nodes.

- **OBD-II (On-Board Diagnostics)** — The standardized CAN-based diagnostic port in every car since 2008. Protocols like OBD-II, J1939 (heavy trucks), and CANopen (industrial) are application layers built [[learning/notes/quick-context/pupper-lab5-neural-controller|on top]] of the CAN physical and data-link layers.

</details>

<details>
<summary><strong>Test [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|Your]] Understanding</strong></summary>

**Q1:** Why does CAN use dominant and recessive states instead of simple high/low voltage?
<details>
<summary>Answer</summary>
The dominant/recessive encoding enables non-destructive arbitration. When two nodes transmit simultaneously, a dominant bit (0) always overwrites a recessive bit (1) on the shared wire — just like a wired-AND [[learning/notes/quick-context/transistor|gate]]. This means the node with the lowest ID (most dominant bits) automatically wins without any data loss or collision detection/retry. If CAN used simple high/low, two simultaneous transmissions would corrupt each other. See: How It Works — Arbitration.
</details>

**Q2:** A CAN bus has 5 nodes on a 10-meter cable. Where do you place termination resistors?
<details>
<summary>Answer</summary>
Only at the two physical endpoints of the bus — the first and last node on the cable. The 3 middle nodes must NOT have termination. Placing a termination [[learning/notes/quick-context/fundamental-electronic-parts-index|resistor]] at a middle node would create a parallel resistance that lowers the bus impedance below 120$\Omega$, distorting signal levels and causing reflections from the impedance mismatch. See: [[micro-context/can-bus-termination]] and the bus [[learning/notes/quick-context/pupper-brain|topology]] diagram.
</details>

**Q3:** Two CAN messages are transmitted at the same time — ID 0x300 and ID 0x100. Which one wins, and why?
<details>
<summary>Answer</summary>
ID 0x100 wins. In binary, 0x100 = 001 0000 0000 and 0x300 = 011 0000 0000 (11-bit IDs, transmitted MSB first). Both transmit the first bit (0) identically. At the second bit (ID[9]), 0x100 transmits dominant (0) while 0x300 transmits recessive (1). The bus goes dominant, 0x300 sees a mismatch (sent 1, read 0), and backs off. Lower numeric ID = more leading zeros = more dominant bits = higher priority. This is why safety-critical messages (emergency stop) are assigned the lowest IDs. See: How It Works — Arbitration.
</details>

**Q4:** Why can't you simply double CAN's bit rate to 2 Mbps and [[learning/notes/quick-context/existing-account-management-playbook|keep]] the same 40-meter bus length?
<details>
<summary>Answer</summary>
Arbitration requires every node to see the [[learning/notes/quick-context/capacitance|current]] bus state within one bit time. At 1 Mbps, one bit = 1 μs, and a [[learning/notes/quick-context/embedded-communication-protocols|40 m]] cable has ~400 ns round-trip [[learning/notes/quick-context/comparator-specification|propagation delay]] — just within budget. At 2 Mbps, one bit = 500 ns, but the round-trip delay is still 400 ns, leaving almost no margin for transceiver delays and oscillator [[learning/notes/quick-context/cnc-machining|tolerance]]. The speed-of-light [[learning/notes/quick-context/voltage-current-causality|constraint]] means [[learning/notes/quick-context/camera-fundamentals|doubling]] bit rate roughly halves maximum bus length. CAN FD solves this by keeping arbitration at the original slow speed but switching to a faster data rate after arbitration completes. See: The Key Tension.
</details>

**Q5:** The Pupper uses 4 separate CAN buses instead of one bus with all 12 servos. Beyond [[learning/notes/quick-context/oscilloscope-and-multimeter|bandwidth]], what other engineering benefits does this provide?
<details>
<summary>Answer</summary>
Three key benefits beyond bandwidth: (1) **Fault [[learning/notes/quick-context/pupper-brain|isolation]]** — a wiring fault or short in one leg's cable only affects 3 servos, not all 12. The other 3 legs continue operating. (2) **Reduced [[learning/notes/quick-context/embedded-communication-protocols|latency]]** — with 3 nodes per bus instead of 12, there's less contention and shorter worst-case arbitration times, improving the 1 kHz loop's timing determinism. (3) **Simpler wiring** — each bus runs to one leg, so cables follow the robot's physical topology rather than [[learning/notes/quick-context/qwiic-stemma-qt-i2c|daisy-chaining]] through all 4 legs. The tradeoff is 4 transceivers + 4 termination resistors + 4 CAN peripheral channels, but on the STM32F446 these are available in hardware. See: [[quick-context/pupper-bom-control-board]] Category 2 and The Key Tension.
</details>

</details>
