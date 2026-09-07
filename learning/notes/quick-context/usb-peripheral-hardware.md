---
topic: USB Peripheral Hardware — How an MCU Turns Bytes into Voltage on a Wire
created: 2026-04-07
---

> **Related:** [[quick-context/differential-pair]] | [[micro-context/microcontroller]] | [[quick-context/capacitance]] | [[quick-context/transistor]] | [[micro-context/scan-loop]]

> **TL;DR:** When firmware writes a byte to a USB endpoint buffer, a dedicated hardware block inside the MCU — the **Serial Interface Engine (SIE)** — autonomously serializes it into a bitstream, encodes it using NRZI (where a "0" bit = [[quick-context/voltage|voltage]] transition, "1" = no transition), inserts bit-stuffing to guarantee clock recovery, appends a CRC, and drives the D+/D- lines through push-pull [[micro-context/mosfet|MOSFET]] pairs that toggle between 3.3V and 0V at 12 MHz. The CPU's job ends at writing bytes to a buffer in [[micro-context/sram|SRAM]]; the SIE's [[quick-context/transistor|transistor]]-level logic gates handle the rest in hardware, responding to host requests within ~500 ns — far too fast for firmware. The device can never transmit spontaneously; the host PC initiates every transaction.

## The Core Problem

Your [[micro-context/stm32-microcontroller|MCU]] has a byte — a scan code, a sensor reading, a debug message — that needs to reach a PC over USB. The CPU can't bit-bang the USB data lines because full-speed USB requires toggling voltages at 12 MHz with sub-microsecond response times, plus simultaneously computing CRCs, inserting stuff bits, and encoding NRZI — all while running your main application. So MCUs contain a dedicated USB peripheral: a block of logic gates (built from [[quick-context/transistor|transistors]]) that handles the entire USB protocol in hardware. Firmware just writes bytes to a buffer and sets a flag; the hardware does the rest. Understanding how this peripheral works bridges the gap between "my code writes to a register" and "voltage transitions appear on a wire."

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Serial Interface Engine (SIE)** | The digital logic block inside the USB peripheral that autonomously handles packet framing, NRZI encoding, bit stuffing, CRC, and handshaking. It responds to host requests without CPU involvement — the CPU only loads data and reads status. |
| **NRZI (Non-Return-to-Zero Inverted)** | The line encoding USB uses on the wire. A data "0" causes a voltage transition (J→K or K→J); a data "1" causes no transition. This ensures clock-recovery transitions appear regularly, since bit stuffing forces a "0" after every 6 consecutive "1"s. |
| **Endpoint Buffer** | A small block of dedicated SRAM inside the MCU (512B-4KB depending on the chip) where firmware writes outgoing data and reads incoming data. The SIE reads from / writes to this buffer autonomously during USB transactions. |
| **D+ / D- ([[quick-context/differential-pair|Differential Pair]])** | The two data wires in a USB cable. Data is encoded as the voltage *difference* between them: J state = D+ HIGH, D- LOW; K state = D+ LOW, D- HIGH. Differential signaling rejects common-mode noise (EMI hits both wires equally and cancels out). |
| **IN Token** | A packet the host sends to request data from the device. USB is 100% host-initiated — the device can *never* transmit spontaneously. When the SIE sees an IN token matching its address, it responds with the data from the endpoint buffer (or NAK if no data is ready). |

<details>
<summary><strong>How It Works</strong> — From buffer write to voltage on the wire</summary>

### Inside the USB Peripheral

The USB peripheral is a self-contained hardware block on the MCU die, built from the same [[quick-context/transistor|logic gates]] as the CPU but with a single specialized job. It contains these sub-blocks:

```
USB PERIPHERAL BLOCK DIAGRAM
================================================================================

  ┌─────────────────────────────────────────────────────────────────────┐
  │  MCU DIE                                                           │
  │                                                                    │
  │  ┌──────────┐         ┌──────────────────────────────────────────┐ │
  │  │          │  bus     │  USB PERIPHERAL                          │ │
  │  │   CPU    │────────►│                                          │ │
  │  │  (fetch- │  write   │  ┌──────────────────┐                   │ │
  │  │  execute)│  bytes   │  │  ENDPOINT BUFFER  │  dedicated SRAM  │ │
  │  │          │  to buf  │  │  (512B - 4KB)     │  (dual-port or   │ │
  │  └──────────┘         │  └────────┬─────────┘  arbitrated)      │ │
  │       ▲                │           │ byte                         │ │
  │       │ interrupt      │           ▼                              │ │
  │       │ (transfer      │  ┌────────────────┐                     │ │
  │       │  complete)     │  │  SHIFT REGISTER │  parallel→serial   │ │
  │       │                │  │  (8-bit ↔ 1-bit)│  at 12 MHz         │ │
  │       │                │  └────────┬────────┘                    │ │
  │       │                │           │ serial bits                  │ │
  │       │                │           ▼                              │ │
  │       │                │  ┌────────────────┐                     │ │
  │       │                │  │  BIT STUFFER    │  inserts "0" after  │ │
  │       │                │  │                 │  6 consecutive "1"s │ │
  │       │                │  └────────┬────────┘                    │ │
  │       │                │           │                              │ │
  │       │                │           ▼                              │ │
  │       │                │  ┌────────────────┐                     │ │
  │       │                │  │  NRZI ENCODER   │  "0"=toggle line   │ │
  │       │                │  │                 │  "1"=hold line      │ │
  │       │                │  └────────┬────────┘                    │ │
  │       │                │           │ J/K states                   │ │
  │       │                │           ▼                              │ │
  │       │                │  ┌────────────────┐       ┌───────────┐ │ │
  │       │                │  │ OUTPUT DRIVERS  │──────►│ D+ pin    │─┼──►
  │       │                │  │ (MOSFET pairs)  │──────►│ D- pin    │─┼──►
  │       │                │  └────────────────┘       └───────────┘ │ │
  │       │                │                                          │ │
  │       │                │  Also in hardware (not shown):           │ │
  │       │                │  • CRC generator (LFSR circuit)          │ │
  │       │                │  • SYNC pattern generator                │ │
  │       │                │  • Protocol state machine (SIE core)     │ │
  │       │                │  • Clock recovery DPLL (48 MHz)          │ │
  │       │                │  • Receive path (reverse of above)       │ │
  │       └────────────────┤                                          │ │
  │                        └──────────────────────────────────────────┘ │
  └─────────────────────────────────────────────────────────────────────┘
```

### Step-by-Step: Byte in Buffer → Voltage on Wire

Here is the full sequence from finger-on-key to voltage-on-wire:

```
THE COMPLETE TRANSACTION: KEYPRESS → VOLTAGE ON WIRE
================================================================================

PHASE 0: KEYPRESS → SCAN CODE → ENDPOINT BUFFER
─────────────────────────────────────────────────────────────────
(what happens BEFORE the USB peripheral gets involved)

  The keyboard MCU (often a CH552, 8051, or Cortex-M0) has
  firmware stored in its flash memory — machine code that exists
  as trapped electrons on floating gates, written at the factory
  via the same [[quick-context/from-code-to-running-firmware|link-flash-boot pipeline]] used for any MCU. That
  firmware runs a continuous scan loop:

  a) KEY MATRIX SCAN — The MCU's CPU fetches instructions from
     flash and executes them. The firmware drives GPIO rows LOW
     one at a time and reads all columns. If a column reads LOW,
     that (row, col) key is pressed.

     ┌─────────────────────────────────────────────────────┐
     │  KEY MATRIX (simplified 4x4)                        │
     │                                                     │
     │          Col 0   Col 1   Col 2   Col 3              │
     │  Row 0:  [ Q ]   [ W ]   [ E ]   [ R ]             │
     │  Row 1:  [ A ]   [ S ]   [ D ]   [ F ]             │
     │  Row 2:  [ Z ]   [→X←]   [ C ]   [ V ]             │
     │  Row 3:  [Spc]   [...]   [...]   [...]              │
     │                                                     │
     │  Your finger presses "X" → switch at (Row 2, Col 1) │
     │  closes → MCU drives Row 2 LOW, reads Col 1 = LOW   │
     │  → key detected.                                    │
     └─────────────────────────────────────────────────────┘

     This scan repeats every ~1-5 ms (the "polling rate").
     The firmware also handles debouncing — mechanical switches
     bounce for ~5 ms, so the firmware ignores transitions
     until the signal has been stable for several scan cycles.

  b) SCAN CODE LOOKUP — The firmware looks up (Row 2, Col 1) in
     a keymap table stored in flash → USB HID scan code 0x1B
     (the standard code for "x" in the USB HID Usage Tables).

     This is NOT ASCII. The keyboard sends position-based scan
     codes; the PC's OS translates them to characters later
     (which is how the same keyboard works in every language).

  c) BUILD HID REPORT — The firmware packages the scan code into
     an 8-byte USB HID keyboard report (the standard format
     defined by the USB HID specification):

       Byte 0: 0x00  (modifier keys — none pressed)
       Byte 1: 0x00  (reserved)
       Byte 2: 0x1B  (key code for "x")
       Bytes 3-7: 0x00 (no other keys pressed)

  d) WRITE TO ENDPOINT BUFFER — The CPU executes a store
     instruction that writes these 8 bytes into the USB
     peripheral's endpoint buffer. This is a dedicated block of
     SRAM inside the MCU — the bytes now exist as voltage states
     across cross-coupled [[micro-context/mosfet|
     transistor]] pairs (see [[quick-context/physics-of-writing-data-to-memory|physics of memory]] for
     how SRAM stores bits).

     At the hardware level, this store instruction is a machine
     code binary pattern fetched from flash (trapped electrons)
     by the [[quick-context/code-to-gates-and-bootstrapping|fetch-execute cycle]], decoded by the CPU's
     control unit (logic gates), which routes the data byte
     through the internal bus to the USB peripheral's SRAM
     address.

  Everything above is firmware-driven (CPU fetching and
  executing instructions). Everything below is hardware-only.


PHASE 1: FIRMWARE SETS "VALID" (CPU's last involvement)
─────────────────────────────────────────────────────────────────

  The CPU writes one more register to hand off to the SIE:

    // STM32 example — writing to Packet Memory Area
    PMA[endpoint_tx_addr] = report;   // 8-byte HID report
    EPnR.STAT_TX = VALID;             // tell SIE: data ready

  This flips a status bit from NAK ("nothing to send") to VALID
  ("data waiting — respond to the next IN token"). From this
  point on, the CPU is done. The byte sits in SRAM waiting for
  the host.


PHASE 2: WAITING (SIE monitors the bus — no CPU)
─────────────────────────────────────────────────────────────────

  USB is host-initiated. The device CANNOT transmit on its own.
  The SIE monitors D+/D- for incoming packets, looking for a
  SYNC pattern (KJKJKJKK) that signals the start of a packet.

  The host's USB controller polls endpoints on a schedule:
  • Interrupt endpoints: every 1-10 ms (set in endpoint descriptor)
  • Bulk endpoints: whenever bus bandwidth is available


PHASE 3: HOST SENDS IN TOKEN (host → device, ~2 μs)
─────────────────────────────────────────────────────────────────

  The host sends: SYNC | PID=IN | ADDR(7 bits) | ENDP(4 bits) | CRC5

  The SIE's receive path:
  1. DPLL locks to the SYNC transitions (clock recovery)
  2. NRZI decoder: voltage transitions → data bits
  3. Bit destuffer: removes any inserted stuff bits
  4. Shift register: serial → parallel bytes
  5. Protocol engine checks: PID=IN? ADDR=mine? ENDP valid? CRC5 OK?

  All in hardware. Takes ~2 μs for the token packet.


PHASE 4: SIE RESPONDS WITH DATA PACKET (device → host, ~46 μs)
─────────────────────────────────────────────────────────────────

  The SIE must begin responding within 7.5 bit times (625 ns)
  of the token's end — far too fast for a CPU interrupt.
  Everything below happens autonomously in hardware:

  ┌──────────────────────────────────────────────────────────┐
  │                                                          │
  │  a) SYNC PATTERN (8 bits, 667 ns)                       │
  │     Shift register outputs: 00000001                     │
  │     NRZI encodes to: KJKJKJKK on the wire               │
  │     Output drivers switch D+/D- at 12 MHz                │
  │                                                          │
  │  b) PID FIELD (8 bits, 667 ns)                           │
  │     DATA0 PID = 0xC3 (0011 + complement 1100)            │
  │     Shift register → bit stuffer → NRZI → drivers        │
  │                                                          │
  │  c) DATA PAYLOAD (8 bits for our 1-byte example)         │
  │     Buffer manager reads 0x1B from endpoint SRAM         │
  │     → into shift register                                │
  │     → bits clock out LSB-first at 12 MHz (83.3 ns/bit)   │
  │     → bit stuffer monitors (inserts "0" if 6 ones in     │
  │       a row — 0x1B = 00011011, no stuffing needed here)  │
  │     → NRZI encoder: each bit either toggles or holds     │
  │       the D+/D- state                                    │
  │     → output drivers physically switch MOSFETs           │
  │                                                          │
  │     Simultaneously: CRC16 LFSR is fed each data bit      │
  │                                                          │
  │  d) CRC16 (16 bits, 1.33 μs)                             │
  │     LFSR contents (inverted) shift out through the same   │
  │     NRZI + bit stuffer + driver pipeline                  │
  │                                                          │
  │  e) EOP — End of Packet (3 bit times, 250 ns)            │
  │     SE0 for 2 bit times: both D+ and D- driven LOW       │
  │       (both N-MOSFETs ON, both P-MOSFETs OFF)            │
  │     J for 1 bit time: D+ HIGH, D- LOW                    │
  │     Then high-impedance: all MOSFETs OFF, bus floats      │
  │                                                          │
  └──────────────────────────────────────────────────────────┘


PHASE 5: HOST ACKNOWLEDGES (host → device, ~1 μs)
─────────────────────────────────────────────────────────────────

  Host verifies CRC16, sends ACK handshake packet.
  SIE receives ACK, toggles DATA0/DATA1 bit, flips endpoint
  status to NAK (no more data until firmware loads more),
  and fires a "transfer complete" interrupt to the CPU.

  The CPU wakes up: "oh, the host took my byte."
```

### NRZI Encoding: Why "0" = Transition

USB has no clock wire. The receiver recovers timing from transitions in the data signal. NRZI ensures transitions happen regularly:

```
NRZI ENCODING — DATA BITS BECOME VOLTAGE TRANSITIONS
================================================================================

  Rule: "0" bit → TOGGLE the line state (J→K or K→J)
        "1" bit → HOLD the line state (no change)

  Example: transmitting 0x1B = 00011011 (LSB first = 11011000)

  Data bits:    1    1    0    1    1    0    0    0
                ─    ─    ─    ─    ─    ─    ─    ─
  NRZI action:  hold hold tog  hold hold tog  tog  tog

  D+ voltage:   _____|          |__________|  |  |
  (J=HIGH,     |     |         |            | | | |
   K=LOW)      |     |_________|            |_| |_|____
               J     J    K    K    K    J    K   J

  Each vertical edge = a MOSFET switching:
  J→K: D+ P-MOS turns OFF, D+ N-MOS turns ON  (D+ falls to 0V)
        D- N-MOS turns OFF, D- P-MOS turns ON  (D- rises to 3.3V)
  K→J: reverse


WHY THIS MATTERS FOR CLOCK RECOVERY
─────────────────────────────────────────────────────────────────

  The receiver's DPLL samples D+/D- at 48 MHz (4× oversampling).
  It recenters its sampling window on every transition. Between
  transitions, it free-runs.

  Problem: a run of "1" bits produces NO transitions. The DPLL
  drifts. After ~7 bit periods, sampling hits the edge of the
  bit window → errors.

  Solution: BIT STUFFING. After 6 consecutive "1"s (= 6 bit
  periods with no transition), the transmitter hardware inserts
  a forced "0" bit (= a transition). The receiver knows to
  discard it.

  Worst case without stuffing:  111111111111... → no transitions
  With stuffing:                111111 0 111111 0 ... → transition
                                       ↑              ↑  every 7 bits
                                   stuff bit       stuff bit

  This guarantees the DPLL never goes more than 7 bit times
  without a transition. At 0.25% crystal tolerance, drift over
  7 bits is only 1.75% of a bit width — well within margin.
```

### The Output Driver: MOSFETs That Create the Signal

The final stage is a pair of [[micro-context/mosfet|CMOS push-pull drivers]] — the same transistor topology used in every digital output:

```
OUTPUT DRIVER — ONE PER DATA LINE (D+ and D-)
================================================================================

         VDDUSB (3.3V)
            │
       ┌────┴────┐
       │  P-MOS  │  gate LOW → ON  → drives pin HIGH
       │         │  gate HIGH → OFF
       └────┬────┘
            ├──── 22Ω ────── D+ pad ──── USB cable ──→ PC
       ┌────┴────┐
       │  N-MOS  │  gate HIGH → ON → drives pin LOW
       │         │  gate LOW → OFF
       └────┬────┘
            │
           GND

  To output J state (D+ HIGH, D- LOW):
    D+ driver: P-MOS ON, N-MOS OFF → pin = 3.3V
    D- driver: P-MOS OFF, N-MOS ON → pin = 0V

  To output K state (D+ LOW, D- HIGH):
    D+ driver: P-MOS OFF, N-MOS ON → pin = 0V
    D- driver: P-MOS ON, N-MOS OFF → pin = 3.3V

  To output SE0 (end-of-packet):
    Both D+ and D- drivers: P-MOS OFF, N-MOS ON → both = 0V

  To go high-impedance (listening):
    All four MOSFETs OFF. Bus floats to J via 1.5kΩ pull-up
    on D+ (identifies device as full-speed to host).

  Rise/fall time: 4-20 ns (USB 2.0 spec 7.1.2)
  Switching rate: 12 million times/second (12 MHz)
  Each transition = gate capacitance charging/discharging,
  same transistor physics as any digital circuit.
```

The 22 $\Omega$ series [[quick-context/resistor|resistor]] (external on some MCUs, integrated on others) plus the [[micro-context/mosfet|MOSFET]]'s on-resistance ($R_{DS(on)}$) matches the 90 $\Omega$ differential impedance of the USB cable, minimizing signal reflections.

</details>

<details>
<summary><strong>The Key Tension</strong> — Hardware autonomy vs. firmware control</summary>

### How Much Should the Hardware Do?

The core design tension in a USB peripheral is: **how much protocol logic belongs in hardware (fast, inflexible) vs. firmware (slow, flexible)?**

| Aspect | Handled in Hardware (SIE) | Handled in Firmware (CPU) |
|--------|--------------------------|--------------------------|
| NRZI encoding/decoding | Always | Never (too fast) |
| Bit stuffing | Always | Never (12 MHz, inline) |
| CRC generation/checking | Always | Never (would stall the pipeline) |
| Packet framing (SYNC, EOP) | Always | Never |
| IN/OUT/SETUP token response | Always | Never (must respond in <625 ns) |
| ACK/NAK handshaking | Always | Never |
| DATA0/DATA1 toggle | Always | Never |
| Endpoint buffer management | Hardware reads/writes | Firmware fills/drains buffers |
| Enumeration (SET_ADDRESS, GET_DESCRIPTOR) | SIE delivers SETUP packet | Firmware parses and responds |
| Class-specific protocol (HID, CDC, MSC) | Nothing | Everything |
| Power management (suspend/resume) | Hardware detects | Firmware decides policy |

**The boundary is at the endpoint buffer.** Everything below the buffer (serialization, encoding, timing, electrical) is hardware. Everything above the buffer (what data to send, when, what it means) is firmware. The SIE is fast but dumb — it doesn't know or care that the bytes are a keyboard scan code, a serial port message, or a mass storage block. It just moves bytes between the buffer and the wire according to the USB protocol.

**Why not do everything in hardware?** Enumeration and class protocols are complex, variable, and rarely time-critical. Handling GET_DESCRIPTOR in hardware would mean burning a fixed descriptor table into silicon — no firmware updates possible. The hybrid approach lets a $0.20 chip (like the CH552) handle the full USB protocol: hardware for the fast/fixed parts, firmware for the slow/flexible parts.

**Why not bit-bang USB in firmware?** Some projects do (V-USB for AVR), but only at **low-speed** (1.5 Mbit/s) — full-speed (12 Mbit/s) bit-banging is essentially impossible since even a 48 MHz MCU would have only 4 cycles per bit. V-USB requires a 12+ MHz AVR clock, giving ~8 clock cycles per low-speed USB bit — barely enough for NRZI encoding, bit stuffing, and CRC inline, with almost nothing left for your application. A dedicated SIE does all of this in parallel with zero CPU load, and handles full-speed that no firmware could match.

</details>

<details>
<summary><strong>Concrete Example</strong> — Tracing a keyboard "x" keypress through the SIE</summary>

### From Scan Code to Wire: The Exact Bits

The keyboard MCU has detected the "x" key (USB HID scan code `0x1B`). It packages this into an 8-byte HID report (the standard format for USB keyboards):

```
HID KEYBOARD REPORT (8 bytes)
================================================================================

  Byte 0: 0x00  modifier keys (none pressed)
  Byte 1: 0x00  reserved
  Byte 2: 0x1B  key code for "x"
  Bytes 3-7: 0x00 (no other keys pressed)

  These 8 bytes are written to the endpoint 1 TX buffer in the
  MCU's packet buffer SRAM. Firmware sets EP1 status to VALID.
```

When the host sends an IN token for endpoint 1, the SIE constructs and transmits this packet:

```
THE COMPLETE USB PACKET ON THE WIRE
================================================================================

  Field        Bits  Content              Purpose
  ──────────── ────  ──────────────────── ──────────────────────
  SYNC           8   KJKJKJKK             Receiver clock sync
  PID            8   DATA1 (0x4B)         Packet type + check
  DATA          64   00 00 1B 00 ...      The 8-byte HID report
  CRC16         16   (computed by LFSR)   Error detection
  EOP            3   SE0, SE0, J          End of packet
  ──────────── ────  ──────────────────── ──────────────────────
  Total:       ~99   bits (before bit stuffing)

  At 12 Mbit/s → ~8.3 μs on the wire

  Plus bit stuffing overhead (worst case +16.7%, typically <5%)
  Plus the IN token (~2 μs) and ACK (~1 μs)
  Total transaction: ~12 μs for 8 bytes

  The host polls the keyboard's interrupt endpoint every 1-10 ms
  (specified in the endpoint descriptor). Between polls, the SIE
  responds with NAK ("no new data") — a 2-byte packet, ~1 μs.
```

### What Happens to Each Data Bit in Hardware

Follow bit 0 of the scan code byte (0x1B = 0001 1011, LSB-first = 1101 1000):

```
TRACING ONE BIT THROUGH THE HARDWARE PIPELINE
================================================================================

  1. BUFFER READ: SIE's buffer manager reads 0x1B from SRAM
     → loads parallel byte into the 8-bit shift register

  2. SHIFT REGISTER: clocks out bit 0 (LSB) = 1
     → bit enters the bit stuffer

  3. BIT STUFFER: is this the 7th consecutive "1"? No (count=1)
     → pass through unchanged

  4. NRZI ENCODER: data bit = 1 → HOLD current line state
     → if line was in J state, it stays in J state
     → no transition on the wire

  5. OUTPUT DRIVER: no change needed
     → D+ P-MOS stays ON (D+ = 3.3V)
     → D- N-MOS stays ON (D- = 0V)
     → no MOSFET switching this bit period

  6. CRC16 LFSR: the data bit "1" is XORed into the LFSR
     → shifts the 16-bit state by one position

  Time elapsed: 83.3 ns (one bit period at 12 MHz)
  Then: shift register advances to bit 1, repeat for all 64 data bits
```

**The one thing most outsiders get wrong about this is...** thinking the CPU "sends" data over USB. The CPU writes bytes to a buffer and walks away. The Serial Interface Engine — a state machine built from logic gates — handles everything from NRZI encoding to CRC calculation to driving the output MOSFETs. The CPU could be in a sleep state, and the SIE would still respond to IN tokens and transmit data. The hardware boundary is the endpoint buffer: firmware fills it, hardware empties it onto the wire. This is why even a $0.20 8-bit MCU running at 24 MHz can handle 12 Mbit/s USB — the CPU isn't doing the fast work.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/physics-of-writing-data-to-memory]]** — Where the bytes in the endpoint buffer physically live (SRAM = cross-coupled inverter pairs) and how the firmware itself exists as trapped electrons in the MCU's flash. The keyboard MCU section of that document is what spawned this one.

- **[[quick-context/embedded-communication-protocols]]** — USB in context: how it compares to [[micro-context/spi|SPI]], [[micro-context/i2c|I2C]], [[quick-context/can-bus|CAN]], UART, and RS-485 in the tradeoff space of speed, wire count, distance, and complexity.

- **[[quick-context/transistor]]** — The [[micro-context/mosfet|MOSFET]] switches in the output drivers that physically create the voltage transitions on D+/D-. Same transistor physics as any digital output, just switching at 12 MHz.

- **[[quick-context/code-to-gates-and-bootstrapping]]** — The SIE is built from the same logic gates (NAND, NOR, flip-flops) described in the compilation chain document. The CRC generator is a Linear Feedback Shift Register; the NRZI encoder is an XOR gate and a D flip-flop; the bit stuffer is a counter and a MUX.

- **[[quick-context/from-code-to-running-firmware]]** — How the keyboard MCU's firmware got into its flash in the first place. The factory programming process that writes the USB stack code to the chip.

- **USB Descriptors and Enumeration** — Before any data transfer, the host reads device/configuration/interface/endpoint descriptors to learn what the device is and how to talk to it. The SIE delivers SETUP packets to firmware; firmware constructs descriptor responses. This is the firmware-side complement to the hardware described here.

- **USB Classes (HID, CDC, MSC)** — Standardized protocols that run on top of the USB transport layer. HID (Human Interface Device) defines the 8-byte keyboard report format. CDC (Communication Device Class) emulates a serial port. MSC (Mass Storage Class) implements a block device. All are pure firmware — the SIE doesn't know about them.

- **V-USB (Software USB)** — A project that bit-bangs low-speed USB (1.5 Mbit/s) entirely in firmware on AVR MCUs with no USB hardware. Demonstrates exactly how painful it is without a SIE — the CPU spends ~80% of its time handling USB timing, with tight assembly loops counting individual clock cycles.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why can't the device transmit a USB packet whenever it has data ready?
<details>
<summary>Answer</summary>
USB is a host-initiated (polled) bus. The device can only transmit in response to an IN token from the host. If the device has data ready but the host hasn't sent an IN token yet, the data sits in the endpoint buffer waiting. If the host sends an IN token and the device has no data, the SIE responds with NAK (a 2-byte handshake meaning "nothing to send, ask again later"). This design simplifies the bus — only one device ever transmits at a time, and the host controls all scheduling. See: How It Works (Phase 2: Waiting)
</details>

**Q2:** The SIE must respond to an IN token within 625 ns. Why can't firmware handle this in an interrupt?
<details>
<summary>Answer</summary>
At 625 ns, a 48 MHz MCU has only ~30 clock cycles — not enough to save registers, enter an interrupt handler, read the token, look up the endpoint, fetch data from the buffer, begin NRZI encoding, and drive the output pins. Even a single cache miss or pipeline stall would blow the deadline. The SIE handles this entirely in combinational and sequential logic — the protocol state machine recognizes the IN token, checks the endpoint status, and begins shifting out the response packet within a few gate delays, all without the CPU. See: How It Works (Phase 4, and The Key Tension)
</details>

**Q3:** NRZI encoding maps "0" to a transition and "1" to no transition. Why not the reverse?
<details>
<summary>Answer</summary>
The choice interacts with bit stuffing. The pathological case for clock recovery is long runs with no transitions. In NRZI, that happens with consecutive "1" bits. Bit stuffing inserts a "0" (forced transition) after 6 consecutive "1"s, breaking up the worst case. If the convention were reversed, runs of "0"s would already produce transitions (no clock problem), while runs of "1"s would produce no transitions — and you'd need a different stuffing rule. The current convention makes the "problem case" (no transitions) correspond to the bit pattern (all 1s) that bit stuffing naturally addresses. The convention also means the idle state (all 1s = J held steady) produces no unnecessary transitions on the bus. See: How It Works (NRZI Encoding)
</details>

**Q4:** The CRC is computed by an LFSR (Linear Feedback Shift Register) that runs in parallel with the shift register. Why is it impractical to compute the CRC in firmware and pre-append it to the buffer?
<details>
<summary>Answer</summary>
Two reasons. First, the CRC must be computed over the exact bitstream that goes on the wire, *including* the PID field that the SIE generates — firmware doesn't control PID selection (DATA0 vs DATA1 toggles automatically). Second, the CRC must be computed *after* bit stuffing decisions are made but *before* the stuff bits are inserted into the CRC calculation (stuff bits are not included in CRC). The SIE computes CRC inline as bits flow through the pipeline, feeding each data bit into the LFSR before the bit stuffer adds stuff bits. Firmware would need to replicate the SIE's internal state to get this right — and it would need to do it before the packet is even triggered, since there's no time during transmission. See: How It Works (Phase 4, step d)
</details>

**Q5:** A CH552 ($0.20, 8051 core at 24 MHz) and an STM32F4 ($3, Cortex-M4 at 168 MHz) both handle full-speed USB at the same 12 Mbit/s. Why doesn't the faster CPU give any USB speed advantage?
<details>
<summary>Answer</summary>
Because the USB bit rate is determined by the SIE hardware and the USB specification, not the CPU. Both chips contain a SIE clocked at 48 MHz that handles NRZI, bit stuffing, CRC, and packet framing identically. The CPU only fills the endpoint buffer and sets a flag — a task that even the 8051 completes in microseconds, well before the host's next poll. The 12 Mbit/s line rate is a property of the USB full-speed physical layer specification, not the MCU's processing power. The faster CPU helps with *application* throughput (parsing data, running protocol stacks, handling multiple endpoints simultaneously), but the bottleneck is the bus, not the CPU. To get faster USB, you need high-speed USB (480 Mbit/s) — which requires a different PHY and a USB OTG peripheral, not a faster processor. See: The Key Tension
</details>

</details>
