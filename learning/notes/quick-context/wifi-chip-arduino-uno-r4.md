---
topic: WiFi Chip — How Radio Becomes Data (and the Arduino Uno R4 WiFi)
created: 2026-03-28
---

# WiFi Chip — How Radio Becomes Data

> **Related:** [[quick-context/electromagnetism]] | [[quick-context/frequency-and-filtering]] | [[quick-context/embedded-communication-protocols]] | [[quick-context/firmware]]

> **TL;DR:** A WiFi chip is a single-chip radio that converts digital data into 2.4 GHz [[quick-context/electromagnetism|electromagnetic waves]] and back again, using modulation (encoding bits onto radio carrier waves), an antenna to radiate/receive those waves, and a protocol stack (802.11) to manage shared airtime. The Arduino Uno R4 WiFi puts an ESP32-S3 WiFi/BLE SoC alongside a Renesas RA4M1 [[micro-context/microcontroller|microcontroller]] — one chip does the radio, the other runs your code.

## The Core Problem

You want your [[micro-context/microcontroller|microcontroller]] to talk to the internet — but it has no wires to a router. WiFi solves this by encoding data onto radio waves at 2.4 GHz (or 5 GHz), transmitting them through the air, and decoding them on the other end. This requires an entire radio transceiver, digital signal processor, protocol engine, and antenna — all squeezed onto a single chip costing a few dollars. Without a WiFi chip, your embedded device is an island; with one, it can fetch web APIs, stream sensor data to the cloud, or accept commands from a phone.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Radio Transceiver** | The analog RF circuit that transmits and receives electromagnetic waves at 2.4 GHz. "Transceiver" = transmitter + receiver in one. Includes a power amplifier (TX), low-noise amplifier (RX), and mixer. |
| **Modulation / Demodulation** | Modulation encodes digital bits onto an analog carrier wave by varying its amplitude, frequency, or phase. Demodulation reverses the process to recover the bits. WiFi uses OFDM with QAM — encoding multiple bits per symbol across many subcarriers simultaneously. |
| **OFDM (Orthogonal Frequency-Division Multiplexing)** | WiFi's core modulation scheme: splits the 20 MHz channel into 48+ narrow subcarriers (each 312.5 kHz wide), transmitting data on all of them in parallel. This resists multipath interference (signals bouncing off walls) because each subcarrier is narrow enough to experience flat fading. |
| **MAC (Media Access Control)** | The protocol layer that manages who gets to transmit and when. WiFi uses CSMA/CA: "listen before you talk." If the channel is busy, wait a random backoff time, then try again. The MAC also handles encryption (WPA), association with access points, and retransmissions. |
| **PHY (Physical Layer)** | The hardware that converts between digital bits and analog radio signals. Includes the baseband processor (FFT/IFFT for OFDM), DAC/[[micro-context/adc-analog-to-digital-converter|ADC]] converters, and the RF front-end (mixers, filters, amplifiers). |

<details>
<summary><strong>How It Works</strong> — From bits to radio waves and back</summary>

### The WiFi Transmit/Receive Pipeline

When your code calls `WiFi.send(data)`, here's what happens inside the chip:

```
WIFI CHIP INTERNAL ARCHITECTURE (e.g., ESP32-S3)
================================================================================

YOUR CODE                           ANTENNA
  │                                    ▲
  ▼                                    │
┌──────────────────────────────────────────────────────────────┐
│                      WiFi SoC                                │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌───────┐  │
│  │   CPU    │    │   MAC    │    │   PHY    │    │  RF   │  │
│  │  (runs   │───►│(protocol │───►│(baseband │───►│(analog│──┼──► antenna
│  │  WiFi    │    │ engine)  │    │  DSP)    │    │ radio)│  │
│  │  stack)  │    │          │    │          │    │       │  │
│  │          │◄───│  CSMA/CA │◄───│ FFT/IFFT │◄───│ LNA + │◄─┼─── antenna
│  │          │    │  encrypt │    │ ADC/DAC  │    │ mixer │  │
│  └──────────┘    └──────────┘    └──────────┘    └───────┘  │
│                                                              │
│  Software ◄──────────────────────────────────────► Hardware  │
└──────────────────────────────────────────────────────────────┘

CPU:  Runs TCP/IP stack, manages connections, calls MAC
MAC:  Frames data, handles CSMA/CA, encryption, ACKs
PHY:  OFDM modulation (IFFT), coding, interleaving
RF:   Upconverts baseband → 2.4 GHz, amplifies, radiates
```

### Transmit Path (Your Data → Radio Waves)

```
TRANSMIT: Digital bits → Electromagnetic waves
================================================================================

1. APPLICATION LAYER
   Your code: WiFi.send("Hello")
   → TCP adds headers, IP adds routing → raw packet bytes
        │
        ▼
2. MAC LAYER
   Add WiFi frame header (source/dest MAC address, sequence #)
   Encrypt payload (AES-128 for WPA2)
   Wait for clear channel (CSMA/CA)
        │
        ▼
3. PHY / BASEBAND
   a. Divide bit stream across 48 subcarriers
   b. Modulate each subcarrier (BPSK, QPSK, 16-QAM, or 64-QAM
      depending on signal quality):

      BPSK: 1 bit/symbol        64-QAM: 6 bits/symbol
      ──────────────────         ──────────────────────
         ●     ●                 ●  ●  ●  ●  ●  ●  ●  ●
        "0"   "1"                ●  ●  ●  ●  ●  ●  ●  ●
      (robust, slow)             ●  ●  ●  ●  ●  ●  ●  ●
                                 ●  ●  ●  ●  ●  ●  ●  ●
                                 ●  ●  ●  ●  ●  ●  ●  ●
                                 ●  ●  ●  ●  ●  ●  ●  ●
                                 ●  ●  ●  ●  ●  ●  ●  ●
                                 ●  ●  ●  ●  ●  ●  ●  ●
                                 (8×8 = 64 points; fast,
                                  needs strong signal)

   c. IFFT (Inverse Fast Fourier Transform):
      Combines all 48 modulated subcarriers into one
      time-domain waveform — a single OFDM "symbol"

      Frequency domain:          Time domain:
      ┌─────────────────┐        ┌─────────────────┐
      │ ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌ │  IFFT  │    ╱╲  ╱╲╱╲    │
      │ ▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌ │ ─────► │ ╱╲╱  ╲╱    ╲╱╲ │
      │ 48 subcarriers  │        │  composite wave  │
      └─────────────────┘        └─────────────────┘

   d. DAC converts digital samples → analog waveform
        │
        ▼
4. RF FRONT-END
   a. Mixer upconverts baseband (~10 MHz) → 2.4 GHz carrier
      (multiplies signal by 2.4 GHz oscillator)
   b. Power amplifier boosts signal to ~20 dBm (~100 mW)
   c. Bandpass filter removes spurious emissions
        │
        ▼
5. ANTENNA
   Radiates electromagnetic wave at 2.4 GHz
   Wavelength: λ = c/f = 3×10⁸ / 2.4×10⁹ = 12.5 cm
   (This is why WiFi antennas are ~3 cm — quarter wavelength)
```

### Receive Path (Radio Waves → Your Data)

The exact reverse:

```
RECEIVE: Electromagnetic waves → Digital bits
================================================================================

  Antenna captures 2.4 GHz signal (typically -30 to -90 dBm)
      │
      ▼
  LNA (Low-Noise Amplifier): boosts weak signal without adding noise
      │
      ▼
  Mixer: downconverts 2.4 GHz → baseband (~10 MHz)
      │
      ▼
  AGC (Automatic Gain Control): adjusts level for ADC
      │
      ▼
  ADC: analog → digital samples
      │
      ▼
  FFT: decomposes time-domain waveform into 48 subcarriers
      │
      ▼
  Demodulator: reads QAM constellation points → bit stream
      │
      ▼
  MAC: checks CRC, decrypts, removes headers, sends ACK
      │
      ▼
  TCP/IP stack: reassembles packets → your data arrives
```

### Why 2.4 GHz?

The 2.4 GHz ISM (Industrial, Scientific, Medical) band is globally unlicensed — anyone can transmit there without a radio license. This is the same band as microwave ovens (which is why they can interfere with WiFi). The 12.5 cm wavelength passes through walls reasonably well (unlike 5 GHz or 60 GHz which are absorbed more), making it practical for home/office use. The tradeoff: the band is crowded — WiFi, Bluetooth, Zigbee, cordless phones, and microwave ovens all share it.

</details>

<details>
<summary><strong>The Key Tension</strong> — Speed vs. Range vs. Reliability</summary>

Every WiFi design trades between three axes:

| Decision | Faster | More Reliable |
|----------|--------|---------------|
| **Modulation** | 64-QAM (6 bits/symbol) — fast but needs strong signal | BPSK (1 bit/symbol) — slow but works at -90 dBm |
| **Channel width** | 40 MHz — double throughput | 20 MHz — less interference, better range |
| **Frequency band** | 5 GHz — less crowded, more bandwidth | 2.4 GHz — better wall penetration, longer range |
| **TX power** | Higher power — more range | Lower power — less battery drain, less interference |

WiFi handles this automatically through **rate adaptation**: the chip starts with fast modulation (64-QAM) and drops to slower, more robust schemes (QPSK, BPSK) as signal weakens. You've experienced this — video streams smoothly near the router, then stutters in the far bedroom.

```
RATE ADAPTATION IN ACTION:
================================================================================

  Signal       Modulation    Data Rate    Use Case
  Strength
  ──────────────────────────────────────────────────────
  Strong       64-QAM        54 Mbps      Streaming 4K
  (-30 dBm)    (6 bits/sym)               next to router

  Medium       16-QAM        24 Mbps      Web browsing
  (-60 dBm)    (4 bits/sym)               through 1 wall

  Weak         QPSK           12 Mbps     Email, IoT
  (-75 dBm)    (2 bits/sym)               through 2 walls

  Very weak    BPSK            6 Mbps     Barely connected
  (-85 dBm)    (1 bit/sym)                edge of range

  Below        —              0 Mbps      "No WiFi signal"
  -90 dBm
```

### WiFi vs. Wired for Embedded Systems

For the [[quick-context/pupper-brain|Pupper robot]], WiFi is used on the Raspberry Pi for high-level tasks (SSH, [[quick-context/ros2-architecture|ROS2]] networking, web interfaces) — not for real-time motor control. Why? WiFi has variable latency (1-50+ ms), packet loss, and no deterministic timing. The 1 kHz motor control loop uses [[micro-context/spi|SPI]] and [[quick-context/can-bus|CAN]] — wired protocols with microsecond latency and zero packet loss. WiFi is for convenience; wired protocols are for control.

</details>

<details>
<summary><strong>Concrete Example</strong> — The Arduino Uno R4 WiFi's Dual-Chip Architecture</summary>

The Arduino Uno R4 WiFi is a perfect case study because it puts the WiFi problem in plain sight: two separate chips, each doing what they're good at.

### The Two Chips

```
ARDUINO UNO R4 WIFI — DUAL-CHIP ARCHITECTURE
================================================================================

  ┌──────────────────────────────────────────────────────────────────┐
  │                    Arduino Uno R4 WiFi PCB                       │
  │                                                                  │
  │  ┌──────────────────┐         ┌──────────────────────────────┐   │
  │  │  Renesas RA4M1   │  UART   │    ESP32-S3-MINI-1           │   │
  │  │  (Cortex-M4)     │◄───────►│    (Xtensa LX7 dual-core)   │   │
  │  │                  │  via    │                              │   │
  │  │  • 48 MHz        │  logic  │  • 240 MHz                  │   │
  │  │  • 256 KB flash  │  level  │  • 512 KB SRAM              │   │
  │  │  • 32 KB SRAM    │  xlator │  • WiFi 802.11 b/g/n        │   │
  │  │  • 5V I/O        │(TXB0108)│  • Bluetooth LE 5.0         │   │
  │  │  • 12-bit DAC    │         │  • 3.3V I/O                 │   │
  │  │  • 12-bit ADC    │         │  • PCB antenna (on-module)  │   │
  │  │  • CAN bus       │         │  • Also handles USB-to-     │   │
  │  │  • Op-amp        │         │    serial for programming   │   │
  │  │                  │         │                              │   │
  │  │  YOUR SKETCH     │         │  WiFi/BLE FIRMWARE           │   │
  │  │  RUNS HERE       │         │  RUNS HERE                   │   │
  │  └──────────────────┘         └──────────────────────────────┘   │
  │        │                              │                          │
  │        ▼                              ▼                          │
  │   Arduino pins                   PCB antenna                     │
  │   (digital, analog,              (printed copper                 │
  │    I2C, SPI, CAN)                 trace on module)               │
  │                                                                  │
  │   USB-C ◄──── programming goes through ESP32-S3 first           │
  └──────────────────────────────────────────────────────────────────┘
```

### Why Two Chips Instead of One?

The RA4M1 is the "Arduino-compatible" chip — it runs at 5V (matching classic Arduino shields), has a CAN bus peripheral, a real 12-bit DAC, and an on-chip [[quick-context/op-amp|op-amp]]. But it has no radio.

The [[quick-context/esp32|ESP32-S3]] IS a capable [[micro-context/microcontroller|microcontroller]] in its own right (dual-core at 240 MHz!), but it runs at 3.3V and wouldn't be backward-compatible with the 5V Arduino ecosystem. So Arduino uses it as a coprocessor: it runs pre-installed [[quick-context/firmware|firmware]] that handles WiFi, Bluetooth, and also acts as the [[quick-context/usb-peripheral-hardware|USB]]-to-serial bridge for programming the RA4M1.

### What's Inside the ESP32-S3's WiFi Radio

```
ESP32-S3 WiFi RADIO SUBSYSTEM (inside the chip):
================================================================================

  ┌─────────────────────────────────────────────────────────────────┐
  │                       ESP32-S3 SoC                              │
  │                                                                 │
  │  ┌────────────┐    ┌────────────┐    ┌────────────────┐        │
  │  │ Xtensa LX7 │    │ WiFi MAC   │    │ WiFi PHY       │        │
  │  │ dual-core  │───►│            │───►│                │        │
  │  │ @ 240 MHz  │    │ CSMA/CA    │    │ OFDM mod/demod │        │
  │  │            │    │ WPA2/WPA3  │    │ FFT / IFFT     │        │
  │  │ Runs:      │    │ Frame mgmt │    │ AGC            │        │
  │  │ • TCP/IP   │    │ AMPDU      │    │ DC offset cal  │        │
  │  │ • TLS      │    │ QoS        │    │                │        │
  │  │ • HTTP     │    │            │    │ DAC ──► mixer  │        │
  │  │ • DNS      │    │            │    │ ADC ◄── mixer  │        │
  │  └────────────┘    └────────────┘    └───────┬────────┘        │
  │                                              │                  │
  │                                    ┌─────────▼──────────┐      │
  │                                    │  RF Front-End       │      │
  │                                    │                     │      │
  │                                    │  • PA (TX: ~20dBm)  │      │
  │                                    │  • LNA (RX)         │      │
  │                                    │  • Balun             │      │
  │                                    │  • T/R switch        │      │
  │                                    │  • Clock gen 2.4GHz  │      │
  │                                    └─────────┬──────────┘      │
  │                                              │                  │
  └──────────────────────────────────────────────┼──────────────────┘
                                                 │
                                            ┌────▼────┐
                                            │ Antenna │
                                            │ (PCB    │
                                            │  trace) │
                                            └─────────┘
```

The antenna on the ESP32-S3-MINI-1 module is a printed copper trace on the module's [[quick-context/pcb-printed-circuit-board|PCB]] — not a separate component. It's shaped as a meandered inverted-F antenna (MIFA), tuned to resonate at 2.4 GHz. The entire radio — from digital baseband to RF power amplifier — is integrated on the same [[quick-context/silicon-die|silicon die]], which is why a complete WiFi solution costs under $3.

### Code Example: Connecting to WiFi on the Uno R4

```cpp
#include <WiFiS3.h>  // Arduino WiFi library for Uno R4

const char* ssid = "MyNetwork";
const char* pass = "MyPassword";

void setup() {
  Serial.begin(115200);

  // This call triggers a chain:
  // 1. RA4M1 sends AT-style command to ESP32-S3 over UART
  // 2. ESP32-S3 firmware receives command
  // 3. ESP32-S3 CPU configures its WiFi MAC
  // 4. MAC scans channels (sends probe requests on each)
  // 5. PHY modulates probe → RF transmits at 2.4 GHz
  // 6. Router responds → RF receives → PHY demodulates
  // 7. MAC completes 4-way WPA2 handshake
  // 8. ESP32-S3 reports success back to RA4M1 over UART
  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(WiFi.localIP());
  // Now your RA4M1 sketch can make HTTP requests,
  // send MQTT messages, etc. — all routed through
  // the ESP32-S3's radio.
}
```

**The one thing most outsiders get wrong about this is...** thinking WiFi is simple because `WiFi.begin()` is one line of code. Behind that single function call, the chip performs channel scanning across up to 14 frequencies (11 in the US, 13 in Europe), OFDM modulation/demodulation, a 4-way cryptographic handshake (WPA2), DHCP negotiation, ARP resolution, and rate adaptation — all managed by dedicated hardware (MAC + PHY + RF) and a real-time firmware stack running on the ESP32-S3's dual 240 MHz cores. The "simplicity" is an abstraction hiding one of the most complex pieces of silicon on the board.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/electromagnetism]]** — WiFi signals are [[quick-context/electromagnetism|electromagnetic waves]] at 2.4 GHz. [[quick-context/maxwell-equations|Maxwell's equations]] predict their propagation, and the antenna design relies on resonance at the carrier frequency. The EM wave section explains exactly what a WiFi signal physically is.

- **[[quick-context/frequency-and-filtering]]** — The WiFi radio uses bandpass [[quick-context/frequency-and-filtering|filters]] extensively: to select the 2.4 GHz band, reject out-of-band interference, and clean up the transmitted signal. The frequency table in that article lists WiFi at 2.4 GHz with a 12.5 cm wavelength.

- **[[quick-context/impedance-and-reactance]]** — The antenna must be [[quick-context/impedance-and-reactance|impedance]]-matched to the RF front-end (typically 50$\Omega$) to maximize power transfer and minimize reflections. A mismatched antenna wastes transmit power and reduces range.

- **[[quick-context/embedded-communication-protocols]]** — WiFi complements the wired protocols (SPI, [[micro-context/i2c|I2C]], CAN, [[quick-context/uart|UART]]) used in embedded systems. The Pupper architecture diagram shows WiFi on the Raspberry Pi alongside wired protocols on the STM32s — each chosen for its strengths.

- **[[quick-context/firmware]]** — The ESP32-S3 runs [[quick-context/firmware|firmware]] that implements the WiFi stack, just like the STM32s run motor control firmware. The difference: the ESP32's firmware includes a TCP/IP stack, TLS encryption, and the 802.11 protocol engine — far more complex than bare-metal motor control code.

- **[[micro-context/microcontroller]]** — The ESP32-S3 is itself a [[micro-context/microcontroller|microcontroller]] (CPU + memory + peripherals on one chip), but with an integrated radio transceiver — making it a "wireless SoC" (System on Chip).

- **[[quick-context/esp32]]** — Full quick-context on the broader ESP32 family: variants (S2/S3/C3/C6/H2/P4), Xtensa vs RISC-V transition, boot sequence, dual-core asymmetry, and when to pick which chip.

- **[[quick-context/pcb-chip-transistor-hierarchy]]** — The ESP32-S3's radio, CPU, and memory are all on one [[quick-context/silicon-die|silicon die]], packaged in a module with a PCB antenna. The packaging hierarchy applies here: transistors → die → module → Arduino board.

- **802.11ax (WiFi 6) / 802.11be (WiFi 7)** — Newer WiFi standards add OFDMA (dividing subcarriers between users), MU-MIMO (multiple simultaneous streams), and wider channels (160+ MHz). The ESP32-S3 supports 802.11 b/g/n (WiFi 4) — sufficient for IoT but not high-bandwidth streaming.

- **Bluetooth Low Energy (BLE)** — The ESP32-S3 also includes a BLE 5.0 radio that shares the same 2.4 GHz antenna. BLE uses frequency hopping spread spectrum (FHSS) rather than OFDM, optimized for ultra-low-power short-range communication (sensors, beacons, wearables).

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What does OFDM do, and why is it better than sending data on a single frequency?
<details>
<summary>Answer</summary>
OFDM splits the 20 MHz WiFi channel into 48+ narrow subcarriers (each 312.5 kHz wide) and transmits data on all of them simultaneously. This is better than a single wide carrier because: (1) each narrow subcarrier experiences "flat" fading — if a reflection cancels part of the spectrum, only a few subcarriers are lost, not the entire signal; (2) it's spectrally efficient — the subcarriers are mathematically orthogonal, so they can overlap without interfering; (3) it converts a fast serial stream into many slow parallel streams, each easier to process. See: How It Works — Transmit Path step 3.
</details>

**Q2:** Why does the Arduino Uno R4 WiFi use two separate chips instead of just the ESP32-S3?
<details>
<summary>Answer</summary>
Backward compatibility and voltage levels. The RA4M1 runs at 5V, matching the classic Arduino ecosystem's shields and sensors. The ESP32-S3 runs at 3.3V and isn't 5V-tolerant. Using the RA4M1 as the main MCU preserves compatibility with existing Arduino hardware while the ESP32-S3 handles WiFi/BLE as a coprocessor. The ESP32-S3 also lacks the RA4M1's unique peripherals: CAN bus, a true 12-bit DAC, and an on-chip op-amp. See: Concrete Example — Why Two Chips.
</details>

**Q3:** Your WiFi connection drops when you microwave popcorn. Why?
<details>
<summary>Answer</summary>
Microwave ovens operate at 2.45 GHz — right in the middle of the 2.4 GHz WiFi band. They generate high-power RF energy (1000W vs WiFi's 0.1W) that leaks through the oven's shielding. This swamps the WiFi receiver's LNA (low-noise amplifier) and corrupts OFDM symbols, causing packet loss and retransmissions. Solutions: use 5 GHz WiFi (different band, no microwave interference), move the router away from the kitchen, or get a better-shielded microwave. See: How It Works — Why 2.4 GHz.
</details>

**Q4:** WiFi can reach 54 Mbps (802.11g) while I2C maxes out at 400 kbps. Why don't embedded systems use WiFi for everything?
<details>
<summary>Answer</summary>
Three critical reasons: (1) **Latency** — WiFi has 1-50+ ms variable latency due to CSMA/CA contention, packet buffering, and retransmissions; I2C/SPI complete in microseconds, deterministically. (2) **Power** — a WiFi radio draws 100-300 mA while transmitting; an I2C transaction on an [[micro-context/stm32-microcontroller|STM32]] uses <1 mA. (3) **Reliability** — WiFi packets can be lost to interference, requiring retransmission; wired protocols on a PCB have essentially zero packet loss. For the Pupper's 1 kHz motor control loop, a 50 ms WiFi hiccup means 50 missed motor commands — the robot falls. See: The Key Tension — WiFi vs Wired.
</details>

**Q5:** The ESP32-S3 has a "PCB trace antenna." How can a flat copper line on a circuit board receive radio waves?
<details>
<summary>Answer</summary>
An antenna works by having a conductor whose length is a resonant fraction of the signal's wavelength. At 2.4 GHz, λ = 12.5 cm, so a quarter-wave antenna is ~3.1 cm. The PCB trace is a meandered (zigzagged) conductor that fits this electrical length into a small area. When a 2.4 GHz electromagnetic wave passes over the trace, it induces an oscillating current (by Faraday's law — the same principle behind generators and inductors). The RF front-end amplifies this tiny current and feeds it to the demodulator. The antenna must be impedance-matched to 50Ω to maximize power transfer — this is why the trace geometry is carefully calculated, not arbitrary. It works the same in reverse for transmission: the power amplifier drives current through the trace, which radiates electromagnetic waves. See: [[quick-context/electromagnetism]] and [[quick-context/impedance-and-reactance]].
</details>

</details>
