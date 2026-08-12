---
topic: UART — Universal Asynchronous Receiver/Transmitter
created: 2026-04-08
---

# UART — Universal Asynchronous Receiver/Transmitter

> **Related:** [[learning/notes/quick-context/voltage]] | [[learning/notes/micro-context/microcontroller]] | [[learning/notes/quick-context/capacitance]] | [[learning/notes/quick-context/embedded-communication-protocols]]

> **TL;DR:** A UART is a hardware peripheral that converts between serial (one-bit-at-a-time on a wire) and parallel (a full byte on the CPU's data bus). It's the oldest and simplest serial protocol still in widespread use — two wires (TX and RX), no clock wire, and both sides must pre-agree on a baud rate. Internally, the key component is a **shift register**: a chain of flip-flops that captures bits one at a time from the wire and, once a full byte is assembled, latches it into a data register the CPU can read. UARTs were originally separate chips (the Western Digital WD1402A in 1971, then the National Semiconductor INS8250 and NS16550), but today they're built into virtually every [[learning/notes/micro-context/stm32-microcontroller|microcontroller]] as on-chip peripherals.

## The Core Problem

A CPU works in parallel — it reads and writes 8, 16, or 32 bits at once over its data bus. But wires between devices carry one bit at a time (serial). Something has to sit at the boundary and convert between these two worlds: accumulate incoming serial bits into a parallel byte, and break outgoing parallel bytes into serial bits. That something is the UART. Without it, every serial device (debug console, GPS module, Bluetooth radio, another MCU) would need custom bit-banging code that ties up the CPU for every single bit.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Baud Rate** | The number of signal transitions per second. Both sides must agree on this before communication. Common rates: 9600, 115200. At 115200 baud, each bit lasts ~8.68 $\mu$s. |
| **Frame** | The packaging around each byte: 1 start bit + 8 data bits + (optional parity) + 1-2 stop bits. The most common format is **8N1** (8 data, no parity, 1 stop = 10 bits per byte). |
| **Shift Register** | A chain of [[learning/notes/micro-context/clock-edges|edge-triggered]] flip-flops that captures one bit per clock tick, shifting all previous bits over. After 8 ticks, it holds a complete byte. This is the core hardware that converts serial ↔ parallel. |
| **Data Register** | A parallel latch that holds the completed byte for the CPU to read (receive) or accepts a byte from the CPU to transmit. Decoupled from the shift register so the CPU and the serial line can work at different speeds. |
| **Oversampling** | The UART's internal clock runs at 16× the baud rate (e.g., 1,843,200 Hz for 115200 baud). It samples the RX line 16 times per bit period and uses the middle samples to determine the bit value, tolerating clock drift and noise. |

<details>
<summary><strong>How It Works</strong> — From [[learning/notes/quick-context/voltage|voltage]] on a wire to a byte in a register</summary>

### High-Level: Two Jobs

A UART has exactly two data paths:

```
UART — HIGH-LEVEL INPUTS AND OUTPUTS
================================================================================

           SERIAL SIDE             PARALLEL SIDE
           (wire/pins)             (CPU data bus)

  RX pin -----> [RX Shift   ] -----> RX Data Register ---->  CPU reads byte
  (serial in)   [Register   ]       (8 bits parallel)

  TX pin <----- [TX Shift   ] <----- TX Data Register <----  CPU writes byte
  (serial out)  [Register   ]       (8 bits parallel)

  Other signals:
    IRQ -------> to CPU interrupt controller
                 (fires when byte received, or TX buffer empty)
    Baud rate generator (internal divider from system clock)
    Status register (framing error, overrun, parity error, etc.)

  The shift register is the bridge: it converts between
  "one bit at a time" (serial) and "all 8 bits at once" (parallel).
```

### The Frame on the Wire

Before diving into the hardware, here's what a single byte looks like as a voltage waveform:

```
UART FRAME FORMAT (8N1) — Sending ASCII "A" (0x41 = 01000001)
================================================================================

  Idle state: line held HIGH continuously ("mark" = 1)

  To send "A" (0x41 = 01000001, sent LSB first as 1,0,0,0,0,0,1,0):

        START
  IDLE  bit   b0  b1  b2  b3  b4  b5  b6  b7  STOP  IDLE
  ─────┐   ┌────┐                        ┌────┐   ┌────────
  HIGH │   │ 1  │                        │ 1  │   │ HIGH
       └───┘    └────────────────────────┘    └───┘
       (0)  (1)  (0) (0) (0) (0) (0) (1) (0) (1)

       <------------- 8 data bits ------------->
                     (LSB first)
       
  start bit = line goes LOW (space) — tells receiver "byte coming"
  data bits = HIGH (1) or LOW (0) for each bit, LSB first
  stop bit  = line goes HIGH (mark) — minimum gap before next byte

  At 115200 baud: each bit lasts ~8.68 μs
  Full 8N1 frame (1 start + 8 data + 1 stop = 10 bits): ~86.8 μs
  Maximum throughput: 115200 ÷ 10 = 11,520 bytes/sec
```

### How the Receive Shift Register Actually Works

This is the heart of the UART. The shift register is a chain of 8 D flip-flops connected in series — the output of each flip-flop feeds the input of the next. On every baud clock tick, each flip-flop captures its neighbor's value, and the first flip-flop captures whatever voltage is on the RX pin. Bits "shift" through the chain like items on a conveyor belt.

```
RECEIVE SHIFT REGISTER — 8 D FLIP-FLOPS IN A CHAIN
================================================================================

  Each box is one D flip-flop. On the rising edge of the baud
  clock, each flip-flop latches whatever is on its D input and
  presents it on its Q output. The Q output of each flip-flop
  feeds the D input of the next one.

  Baud clock (derived from 16x oversampling — see below)
      |     |     |     |     |     |     |     |
      v     v     v     v     v     v     v     v
  +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+
  |D   Q|-|D   Q|-|D   Q|-|D   Q|-|D   Q|-|D   Q|-|D   Q|-|D   Q|
  | FF7 | | FF6 | | FF5 | | FF4 | | FF3 | | FF2 | | FF1 | | FF0 |
  +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+ +-----+
  ^                                                              ^
  |                                                              |
  RX pin                                                 oldest bit
  (newest bit                                           (arrived first,
   enters here)                                      shifted to the end)
```

**Step-by-step: receiving "A" (0x41 = 01000001, sent LSB first)**

The wire sends bits in order: `1, 0, 0, 0, 0, 0, 1, 0` (LSB first). After each baud clock tick, here's what's in the shift register:

```
SHIFT REGISTER FILLING UP — ONE BIT PER CLOCK TICK
================================================================================

  Clock   RX    FF7  FF6  FF5  FF4  FF3  FF2  FF1  FF0   Status
  tick    pin
  ─────────────────────────────────────────────────────────────────
  (idle)   1     -    -    -    -    -    -    -    -     waiting
  
  START BIT detected (line drops LOW) → UART begins sampling
  
  1        1     1    -    -    -    -    -    -    -     bit 0 (LSB)
  2        0     0    1    -    -    -    -    -    -     bit 1
  3        0     0    0    1    -    -    -    -    -     bit 2
  4        0     0    0    0    1    -    -    -    -     bit 3
  5        0     0    0    0    0    1    -    -    -     bit 4
  6        0     0    0    0    0    0    1    -    -     bit 5
  7        1     1    0    0    0    0    0    1    -     bit 6
  8        0     0    1    0    0    0    0    0    1     bit 7 (MSB)
                 ─────────────────────────────────────
  After 8 ticks: 0  1  0  0  0  0  0  1  = 0x41 = "A" ✓
                 b7 b6 b5 b4 b3 b2 b1 b0

  STOP BIT validates the frame, then the UART latches the shift
  register contents into the data register (see below).
```

Each clock tick, every bit moves one position to the right, and the new bit from the RX pin enters on the left. After 8 ticks, the shift register contains the complete byte.

### From Shift Register to Data Register (The Parallel Latch)

Once 8 data bits have been shifted in and the stop bit is validated, the UART needs to make the byte available to the CPU **without disturbing the shift register** (which may need to start receiving the next byte immediately). This is done with a parallel latch:

```
TRANSFER: SHIFT REGISTER → DATA REGISTER
================================================================================

  After 8 bits received + stop bit validated:

  Shift Register (still filling from wire):
  +-----+-----+-----+-----+-----+-----+-----+-----+
  | FF7 | FF6 | FF5 | FF4 | FF3 | FF2 | FF1 | FF0 |
  |  0  |  1  |  0  |  0  |  0  |  0  |  0  |  1  |
  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
     |     |     |     |     |     |     |     |
     | LATCH pulse (internal signal: "byte complete")
     v     v     v     v     v     v     v     v
  +-----+-----+-----+-----+-----+-----+-----+-----+
  | D7  | D6  | D5  | D4  | D3  | D2  | D1  | D0  |  ← Data Register
  |  0  |  1  |  0  |  0  |  0  |  0  |  0  |  1  |    (parallel latch)
  +-----+-----+-----+-----+-----+-----+-----+-----+
     |     |     |     |     |     |     |     |
     +-----+-----+-----+-----+-----+-----+-----+----> CPU Data Bus
                                                       (8 bits at once)

  1. UART's internal state machine counts 8 data bits received
  2. Checks the stop bit is HIGH (valid frame)
  3. Fires an internal LATCH signal — all 8 Q outputs of the shift
     register flip-flops are simultaneously captured by the data
     register (another set of 8 D flip-flops, clocked by the latch
     signal instead of the baud clock)
  4. Sets the RXNE (RX Not Empty) flag in the status register
  5. Raises IRQ to the CPU: "come read your byte"
  6. The shift register is now FREE to start receiving the next byte
     immediately — even before the CPU reads the data register

  If the CPU doesn't read before the NEXT byte finishes →
  the old byte is overwritten → OVERRUN ERROR flag set.
```

This two-stage design (shift register + data register) is what lets the UART operate continuously — the shift register captures bits in real time while the CPU reads completed bytes at its own pace.

### Oversampling: How the UART Knows When to Sample

The UART doesn't have a clock wire from the sender. So how does it know exactly when each bit is present on the RX line? It uses **oversampling** — its internal clock runs at 16× the baud rate:

```
OVERSAMPLING AT 16× BAUD RATE
================================================================================

  At 115200 baud, the internal clock is 115200 × 16 = 1,843,200 Hz

  One bit period = 16 internal clock ticks:

  RX line:  ──────────┐                                          ┌──────
            (prev bit) │            THIS BIT = 0                  │(next)
                       └──────────────────────────────────────────┘
  16x clock: ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑
             1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16  1
                       |              ↑  ↑  ↑
                       |         samples 8,9,10 — take
                 start of bit   majority vote → bit = 0

  HOW IT WORKS:
  1. UART watches RX line at 16x speed, waiting for HIGH→LOW
     (falling edge = start bit)
  2. Once detected, it counts 8 ticks (half a bit period) to
     land in the CENTER of the start bit
  3. Verifies start bit is still LOW (not a glitch)
  4. Then counts 16 ticks to reach the center of each data bit
  5. At each bit center, it takes 3 samples (ticks 8, 9, 10)
     and does a majority vote: 2 out of 3 wins
  6. That voted value shifts into the shift register
  7. Repeat for all 8 data bits + stop bit

  WHY 16x?
  - Gives fine-grained positioning to find the center of each bit
  - The 3-sample majority vote filters single-tick noise spikes
  - Tolerates up to ~3% clock mismatch between sender and receiver
    (at 16x, a 3% error drifts ~0.5 ticks per bit — still within
    the center ±2 tick window after 10 bits)
```

### Transmit Path (Reverse Direction)

Transmission is the mirror image:

```
TRANSMIT PATH
================================================================================

  1. CPU writes a byte to the TX Data Register
  2. TX Data Register loads into the TX Shift Register (parallel load)
  3. UART's state machine clocks out bits one at a time:
     - First: drive TX pin LOW for 1 bit period (start bit)
     - Then: drive TX pin to each data bit value, LSB first
     - Finally: drive TX pin HIGH for 1+ bit periods (stop bit)
  4. When shift register is empty, UART sets TXE (TX Empty) flag
     and optionally raises IRQ so the CPU can load the next byte
```

### Historical Context: The Teletype Connection

The UART was invented specifically to interface teletypes with computers. In the 1960s, a teletype's keyboard mechanically encoded characters as 7-bit ASCII and transmitted them as [[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens|20mA current loop]] serial signals at 110 baud. On the computer side, a UART captured these bits and presented them as parallel bytes. The ASR-33 teletype's frame format — 1 start bit, 7 data bits, 2 stop bits, at 110 baud — was the original UART standard.

For the full teletype-to-computer I/O path (keyboard encoding → current loop → UART → interrupt → OS buffer → echo back → print mechanism), see [[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens|From Vacuum Tubes to Coding on Screens, Era 3]].

</details>

<details>
<summary><strong>The Key Tension</strong> — Simplicity vs. robustness</summary>

UART sits at the "dead simple" end of the [[learning/notes/quick-context/embedded-communication-protocols|protocol spectrum]]:

| | UART | SPI | I2C | CAN |
|---|---|---|---|---|
| **Wires** | 2 (TX, RX) | 4+ (SCLK, MOSI, MISO, CS) | 2 (SDA, SCL) | 2 (CANH, CANL) |
| **Clock** | None (async) | Shared clock wire | Shared clock wire | None (async) |
| **Topology** | Point-to-point | Star (1 CS per device) | Multi-drop bus | Multi-drop bus |
| **Error detection** | Optional parity bit | None built-in | ACK/NACK only | CRC-15 + 5 error types |
| **Max speed** | ~10 Mbps (typical 115200) | 50+ MHz | 3.4 Mbps | 1 Mbps (FD: 8 Mbps) |
| **Max distance** | ~15 m (TTL) | ~30 cm | ~1 m | 40 m |

**UART's advantage is simplicity:** two wires, no clock to route, no addressing, no protocol overhead. This makes it the default choice for debug consoles, GPS modules, and any point-to-point link where you just need to send bytes.

**UART's weakness is everything else:** no error detection (unless you add parity, and even then it only catches 1-bit errors), no multi-device support, no noise immunity (single-ended signaling), clock drift can cause framing errors at high speeds. For anything more demanding, you layer a physical standard on top (RS-232 for voltage levels, RS-485 for differential long-haul) or switch to a different protocol entirely.

The deeper tension is **asynchronous vs. synchronous**: UART requires both sides to independently generate matching clocks from crystal oscillators. A ~3% mismatch is tolerable (the oversampling handles it), but beyond that, bits get sampled at the wrong time and you get framing errors. Synchronous protocols (SPI, I2C) avoid this entirely by sending a clock wire — but that's one more wire to route.

</details>

<details>
<summary><strong>Concrete Example</strong> — Configuring UART on an STM32 for debug output</summary>

On the Pupper v3's [[learning/notes/micro-context/stm32-microcontroller|STM32]], UART is used as the debug console. Here's what the configuration looks like:

```c
// STM32 HAL — Configure UART2 for 115200 baud debug output
UART_HandleTypeDef huart2;

huart2.Instance          = USART2;
huart2.Init.BaudRate     = 115200;
huart2.Init.WordLength   = UART_WORDLENGTH_8B;
huart2.Init.StopBits     = UART_STOPBITS_1;
huart2.Init.Parity       = UART_PARITY_NONE;      // 8N1
huart2.Init.Mode         = UART_MODE_TX_RX;
huart2.Init.HwFlowCtl    = UART_HWCONTROL_NONE;
huart2.Init.OverSampling = UART_OVERSAMPLING_16;   // 16x oversampling
HAL_UART_Init(&huart2);

// Send a string (blocking)
HAL_UART_Transmit(&huart2, (uint8_t*)"Hello\r\n", 7, 100);

// Receive one byte (interrupt-driven)
uint8_t rx_byte;
HAL_UART_Receive_IT(&huart2, &rx_byte, 1);

// In the callback (called from ISR when byte arrives):
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    // rx_byte now contains the received character
    // The UART hardware did all the shift register work —
    // you just read the data register through the HAL
    process_byte(rx_byte);
    HAL_UART_Receive_IT(huart, &rx_byte, 1);  // re-arm for next byte
}
```

Under the hood, `HAL_UART_Receive_IT` enables the UART's RXNE interrupt. When a byte arrives:
1. The shift register captures 8 bits from the RX pin (oversampled at 16×)
2. The byte latches into the data register → RXNE flag set → IRQ fires
3. The HAL's ISR reads the data register → clears RXNE → calls your callback

**Baud rate generation on STM32:** The STM32's UART peripheral divides the peripheral bus clock (APB clock) to produce the baud rate. For 115200 baud with 16× oversampling on a 72 MHz APB clock:

$$\text{USARTDIV} = \frac{f_{\text{APB}}}{16 \times \text{baud}} = \frac{72{,}000{,}000}{16 \times 115{,}200} = 39.0625$$

The integer part (39) goes in BRR[15:4], the fraction (0.0625 × 16 = 1) goes in BRR[3:0]. The actual baud rate is $72{,}000{,}000 / (16 \times 39.0625) = 115{,}200$ exactly.

**The one thing most outsiders get wrong about this is...** thinking UART is a "protocol" like I2C or CAN. UART is really just the **hardware peripheral** — it handles framing (start/stop bits) and serial↔parallel conversion, but it defines no electrical standard (voltage levels, signaling, connectors). RS-232, RS-485, and 20mA current loop are all **physical layers** that carry UART frames. When someone says "UART" they usually mean TTL-level (0V/3.3V) point-to-point, but the same UART peripheral can drive any of these physical layers through an external transceiver chip.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[learning/notes/quick-context/embedded-communication-protocols]]** — The full comparison of UART, I2C, SPI, CAN, RS-232, RS-485, 1-Wire, USB, and I3C. Covers when to choose each protocol and the tradeoffs between them. UART is the simplest entry in this comparison.

- **[[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens]]** — The historical context: how UARTs enabled the transition from punch cards to interactive terminals in the 1960s. Covers the full teletype I/O loop: keyboard → current loop → UART → interrupt → OS buffer → echo.

- **[[learning/notes/quick-context/usb-peripheral-hardware]]** — How USB works at the hardware level inside an MCU. USB's Serial Interface Engine (SIE) is conceptually similar to a UART — it has shift registers for serial↔parallel conversion — but adds NRZI encoding, bit stuffing, CRC, and packet framing.

- **[[learning/notes/micro-context/stm32-microcontroller]]** — The STM32 family of microcontrollers that include UART peripherals. The Pupper v3 uses UART for debug console output.

- **[[learning/notes/quick-context/d-flip-flop]]** — Deep dive into how the D flip-flop works: from SR latches to edge-triggered master-slave design, the clock's role, and how DFFs compose into shift registers and registers. The UART's shift register is a chain of 8 of these.

- **[[learning/notes/micro-context/clock-edges]]** — How flip-flops sample data on clock edges. This is the foundation of how the shift register works: each D flip-flop captures its input on the rising edge of the baud clock.

- **[[learning/notes/quick-context/code-to-gates-and-bootstrapping]]** — How logic gates and flip-flops are built from transistors. The UART's shift register and data register are ultimately chains of these gate-level primitives.

- **RS-232** — The electrical standard that defines bipolar voltage levels (±3-15V) for UART signals. Requires a level-shifting IC like the MAX232. See [[learning/notes/quick-context/embedded-communication-protocols|embedded communication protocols]] for details.

- **RS-485** — Differential signaling physical layer for UART frames. Enables multi-drop buses over 1200 m. See [[learning/notes/quick-context/embedded-communication-protocols|embedded communication protocols]] for details.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does a UART need a start bit at all? Why not just send the 8 data bits?
<details>
<summary>Answer</summary>
Because UART is **asynchronous** — there's no shared clock wire. The receiver doesn't know when the sender starts transmitting. The start bit (a guaranteed HIGH→LOW transition) gives the receiver a synchronization edge: "a byte starts NOW." The receiver then uses its 16× oversampled clock to find the center of each subsequent bit. Without the start bit, the receiver would have no way to align its sampling to the incoming data. See: Oversampling in How It Works.
</details>

**Q2:** If the shift register is actively receiving bits, how can the CPU read the previous byte without corrupting the current reception?
<details>
<summary>Answer</summary>
The **two-stage design**: shift register + data register. Once 8 bits are received and the stop bit is validated, the completed byte is latched into the data register (a separate set of flip-flops). The shift register immediately starts receiving the next byte. The CPU reads from the data register, which is independent of the shift register. This is why you get an **overrun error** if the CPU doesn't read before the next byte finishes — the new byte overwrites the data register before the old one was read. See: Transfer from Shift Register to Data Register.
</details>

**Q3:** At 115200 baud, how much clock mismatch between sender and receiver can the UART tolerate before bits get misread?
<details>
<summary>Answer</summary>
About **±3-4%**. At 16× oversampling, the receiver samples at the center of each bit (ticks 8-10 out of 16). Over a 10-bit frame, a 3% clock error accumulates to ~0.3 bits of drift by the last bit — still within the ±0.5 bit tolerance window. Beyond ~4-5%, the sampling point drifts past the bit boundary and you get framing errors. This is why both sides typically use crystal oscillators (~50 ppm accuracy = 0.005%) rather than internal RC oscillators (~1-5% accuracy). See: Oversampling in How It Works.
</details>

**Q4:** Someone claims "UART can't go over 5 meters." Is this right?
<details>
<summary>Answer</summary>
It depends on the **physical layer**, not the UART itself. TTL-level UART (0V/3.3V single-ended) degrades over long wires due to [[learning/notes/quick-context/capacitance|capacitance]] and noise — practically limited to ~15 m at 115200 baud, though 5 m is safer for high reliability. But the same UART frames can travel 1200 m over RS-485 (differential signaling) or miles over 20mA current loop (as teletypes did in the 1960s). UART is the framing/conversion hardware; the physical layer determines distance. See: The Key Tension and [[learning/notes/quick-context/embedded-communication-protocols]].
</details>

**Q5:** On an STM32 running at 72 MHz with 16× oversampling, what happens if you configure the UART for 2,000,000 baud? Will it work?
<details>
<summary>Answer</summary>
Calculate: $\text{USARTDIV} = 72{,}000{,}000 / (16 \times 2{,}000{,}000) = 2.25$. The BRR register can represent this (integer 2, fraction 0.25 × 16 = 4). The actual baud rate would be $72{,}000{,}000 / (16 \times 2.25) = 2{,}000{,}000$ exactly. So the hardware *can* generate it. But will it work? At 2 Mbps, each bit is 500 ns — signal integrity becomes critical. TTL-level UART over more than a few centimeters of PCB trace may suffer from ringing, crosstalk, and capacitive loading. You'd need short traces, good ground planes, and probably impedance matching. The UART peripheral is fine; the physics of the wire is the limit. Many STM32s support even higher rates (up to 10+ Mbps) with 8× oversampling mode, which doubles the max baud rate for a given clock.
</details>

</details>
