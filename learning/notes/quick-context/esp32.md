---
topic: ESP32
created: 2026-05-28
---

# ESP32

> **Related:** [[learning/notes/micro-context/microcontroller]] | [[learning/notes/micro-context/power-inductor]]

> **TL;DR:** The ESP32 is a family of cheap (~$2) wireless [[learning/notes/micro-context/microcontroller|microcontroller]] system-on-chips from Espressif Systems that combines a 32-bit CPU, 320–520 KB of SRAM, dozens of peripherals (SPI, I2C, I2S, ADC, PWM, CAN), and an integrated 2.4 GHz radio for WiFi and Bluetooth onto one die. It's the default chip when you want an [[learning/notes/quick-context/firmware|MCU]] that can also talk to the internet without a separate radio module.

## The Core Problem

Connecting an embedded device to WiFi used to mean pairing a microcontroller with a separate, expensive WiFi module talking over UART — two chips, two power rails, ~$15 in parts, and a clumsy AT-command protocol. The ESP32 collapses that whole stack onto a single die for under $3: the same chip that runs your application code also drives the antenna directly. This made wireless IoT cheap enough to put a WiFi-connected MCU into a lightbulb, a doorbell, or every joint of a robot.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **SoC (System-on-Chip)** | An entire computer — CPU, RAM, ROM, radio, peripherals — integrated on one silicon die. The ESP32 is an SoC because it's not just an MCU; it bundles a complete 2.4 GHz radio transceiver on the same chip. |
| **Espressif Systems** | Shanghai-based fabless semiconductor company that designs the ESP family. Launched the ESP8266 in 2014 (cheap WiFi MCU) and the ESP32 in 2016 (added dual-core, Bluetooth, more peripherals). |
| **Xtensa LX6/LX7** | Tensilica's 32-bit configurable RISC CPU architecture used in the original ESP32 and S2/S3 variants. Newer ESP32-C/H/P variants use RISC-V cores instead — Espressif is migrating off proprietary Xtensa toward open RISC-V. |
| **ESP-IDF** | Espressif IoT Development Framework — the official C/C++ SDK. FreeRTOS-based, gives you full hardware access. The alternative is Arduino-ESP32 (a wrapper layer over ESP-IDF that exposes the familiar `setup()`/`loop()` API). |
| **ULP Coprocessor** | Ultra-Low-Power coprocessor that keeps running while the main cores are in deep sleep. Wakes on sensor thresholds; deep sleep draws ~10 μA with only the RTC timer, ~100 μA with the ULP actively running. Classic ESP32's ULP is a custom FSM core with a tiny instruction set; ESP32-S2 onward use a RISC-V ULP. Enables battery-powered devices that sleep months between events. |

<details>
<summary><strong>How It Works</strong> — Inside the ESP32 SoC</summary>

The ESP32's superpower is that it crams a complete WiFi/BLE radio onto the same die as a dual-core MCU. Block diagram of an ESP32 (original "classic" variant):

```
ESP32 BLOCK DIAGRAM (e.g., ESP32-D0WD)
================================================================================

┌──────────────────────────────────────────────────────────────────────────┐
│                              ESP32 SoC                                   │
│                                                                          │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────┐  │
│  │   Xtensa LX6       │  │   Xtensa LX6       │  │  ULP               │  │
│  │   Core 0 (PRO_CPU) │  │   Core 1 (APP_CPU) │  │  Coprocessor       │  │
│  │   240 MHz          │  │   240 MHz          │  │  (8 MHz FSM;       │  │
│  │                    │  │                    │  │   RISC-V on S2+)   │  │
│  │   Runs WiFi/BLE    │  │   Runs user app    │  │  Deep sleep:       │  │
│  │   stack by default │  │   by default       │  │  ~10 μA idle,      │  │
│  │                    │  │                    │  │  ~100 μA active    │  │
│  └─────────┬──────────┘  └─────────┬──────────┘  └─────────┬──────────┘  │
│            │                       │                       │             │
│            └───────────────────────┼───────────────────────┘             │
│                                    │                                     │
│   ┌────────────────┬──────────┬────┴──────────┬───────────────────────┐  │
│   │ 520 KB SRAM    │ 448 KB   │ 1 KB eFuse    │ External SPI flash    │  │
│   │ (data + code)  │ ROM      │ (factory-set  │ 4–16 MB               │  │
│   │                │ (boot)   │  MAC, keys)   │ (off-chip, on module) │  │
│   └────────────────┴──────────┴───────────────┴───────────────────────┘  │
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────────┐ │
│   │                         PERIPHERALS                                │ │
│   │  4× SPI · 2× I2C · 2× I2S · 3× UART · 2× CAN(TWAI) · SDIO          │ │
│   │  18× ADC (12-bit) · 2× DAC (8-bit) · 16× PWM (LEDC) · RMT          │ │
│   │  Touch sensor (10 ch) · Hall sensor · 34× GPIO                     │ │
│   └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│   ┌──────────────────────────┐     ┌──────────────────────────────────┐  │
│   │  WiFi 802.11 b/g/n       │     │  Bluetooth 4.2 BR/EDR + BLE      │  │
│   │  MAC + Baseband (PHY)    │     │  MAC + Baseband                  │  │
│   └────────────┬─────────────┘     └────────────────┬─────────────────┘  │
│                │                                    │                    │
│                └──────────────────┬─────────────────┘                    │
│                                   │                                      │
│                  ┌────────────────▼────────────┐                         │
│                  │  Shared 2.4 GHz RF Front-   │                         │
│                  │  End: PA, LNA, Balun,       │                         │
│                  │  T/R switch                 │                         │
│                  └────────────────┬────────────┘                         │
└───────────────────────────────────┼──────────────────────────────────────┘
                                    │
                               ┌────▼─────┐
                               │  Antenna │  (PCB trace or external)
                               └──────────┘
```

### Boot Sequence

The ESP32 has no internal flash for user code — only mask ROM. On power-up:

```
1. First-stage bootloader (in mask ROM):
   - Configures clocks, GPIO straps
   - Reads strapping pins (GPIO0, GPIO2, GPIO12) to decide:
        GPIO0 = LOW  → enter UART bootloader (flashing mode)
        GPIO0 = HIGH → boot from external SPI flash (run mode)

2. Second-stage bootloader (in external flash, address 0x1000):
   - Loaded into IRAM, sets up flash mapping (XIP — execute-in-place)
   - Verifies app partition signature (if secure boot enabled)

3. Application image:
   - FreeRTOS scheduler starts
   - app_main() runs on Core 0 (PRO_CPU)
   - WiFi/BLE stack initialized on its own task
```

### Why "Execute in Place" matters

The 520 KB of on-chip SRAM is too small to hold a real WiFi app. So the ESP32 uses external SPI flash mapped into the CPU's address space via the MMU — the CPU fetches instructions directly from flash through a cache. This is called XIP (Execute-In-Place). The cache is small (~32 KB), so cache misses on flash reads cost ~100s of nanoseconds — fine for most code, painful for tight ISRs. Performance-critical code is annotated `IRAM_ATTR` to force it into SRAM.

### Dual-Core Asymmetry

The two cores are identical hardware, but FreeRTOS pins specific tasks to each by convention:
- **PRO_CPU (Core 0)** runs the WiFi/BLE stack and low-level drivers
- **APP_CPU (Core 1)** runs the user application

You can override this with `xTaskCreatePinnedToCore()` — but if you starve Core 0 of CPU time, the WiFi connection drops. Most ESP32 bugs in the wild are people running blocking code on Core 0.

</details>

<details>
<summary><strong>The Key Tension</strong> — Choosing among the ESP32 variants</summary>

"ESP32" is a family, not a single chip. Picking the wrong variant is the most common mistake. The lineup as of 2026:

| Variant | CPU | RAM | Radio | Killer feature | When to pick |
|---------|-----|-----|-------|----------------|--------------|
| **ESP32** (classic, 2016) | Xtensa LX6 dual @ 240 MHz | 520 KB | WiFi 4 + BT 4.2 + BLE | Cheapest dual-core | Legacy designs, generic IoT |
| **ESP32-S2** (2020) | Xtensa LX7 single @ 240 MHz | 320 KB | WiFi 4 only (no BT) | USB OTG built-in | USB peripherals when BT not needed |
| **ESP32-S3** (2021) | Xtensa LX7 dual @ 240 MHz | 512 KB | WiFi 4 + BLE 5.0 | Vector instructions for AI/DSP, USB OTG | Edge ML, audio, the Arduino Uno R4 WiFi |
| **ESP32-C3** (2021) | RISC-V single @ 160 MHz | 400 KB | WiFi 4 + BLE 5.0 | Cheapest BLE 5 chip (~$1) | Cost-sensitive BLE devices |
| **ESP32-C6** (2023) | RISC-V HP @ 160 MHz + LP @ 20 MHz | 512 KB | WiFi 6 + BLE 5 + 802.15.4 | WiFi 6 + Thread/Matter/Zigbee in one | Smart-home (Matter), future-proof IoT |
| **ESP32-H2** (2023) | RISC-V single @ 96 MHz | 320 KB | BLE 5 + 802.15.4 (no WiFi) | Ultra-low-power Thread/Zigbee | Battery mesh-network nodes |
| **ESP32-P4** (2024) | RISC-V HP dual @ 400 MHz + LP @ 40 MHz | 768 KB HP + 32 KB LP | none (HMI focus) | MIPI-CSI camera, MIPI-DSI display | HMI panels needing display + camera |

### The three axes designers actually trade

```
                Cost / Power
                   │
                   │
   ESP32-H2 ●      │       ● ESP32-C3
            \      │      /
             \     │     /
              \    │    /
  Connectivity ────●──── Compute
   (WiFi/BLE/      │      (cores / clock /
    802.15.4)      │       AI accel)
                   │
                   ●  ESP32-S3
                   ●  ESP32-P4
```

- **Want maximum connectivity in one part?** ESP32-C6 (WiFi 6 + BLE + Thread/Zigbee).
- **Want maximum compute, willing to spend $4?** ESP32-S3 (vector DSP, USB).
- **Want $1 wireless?** ESP32-C3.
- **Want lowest power?** ESP32-H2 + ULP, no WiFi at all.

### Xtensa vs RISC-V — the strategic shift

The original ESP32 used Cadence's proprietary Tensilica Xtensa cores. Espressif licensed them per-chip. Starting with the C3 (2021), Espressif switched all new low-cost variants to open-source RISC-V — they can implement the cores royalty-free and customize them. Xtensa stuck around in the S2/S3 because those reuse the existing high-end LX7 design. Going forward, expect new chips to be RISC-V only.

</details>

<details>
<summary><strong>Concrete Example</strong> — Blinking an LED over WiFi with Arduino-ESP32</summary>

A minimal "Hello, internet" sketch — connect to WiFi, expose a web endpoint, toggle the onboard LED when hit:

```cpp
#include <WiFi.h>          // Built-in to Arduino-ESP32
#include <WebServer.h>

const char* SSID = "MyHomeWiFi";
const char* PASS = "hunter2";
const int   LED  = 2;       // GPIO2 — onboard LED on most dev boards

WebServer server(80);

void handleToggle() {
  digitalWrite(LED, !digitalRead(LED));
  server.send(200, "text/plain", "ok");
}

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);

  // 1. Calls esp_wifi_init() under the hood
  // 2. Brings up the WiFi MAC + PHY on Core 0
  // 3. Scans, associates, does WPA2 4-way handshake
  // 4. DHCP negotiates an IP
  WiFi.begin(SSID, PASS);
  while (WiFi.status() != WL_CONNECTED) { delay(200); Serial.print("."); }
  Serial.println(WiFi.localIP());

  server.on("/toggle", handleToggle);
  server.begin();
}

void loop() {
  server.handleClient();    // Polls the TCP socket — runs on Core 1
}
```

Connect over USB, flash with `arduino-cli` or Arduino IDE (which talks to `esptool.py` over [[learning/notes/quick-context/embedded-communication-protocols|UART]] at 921600 baud), open the serial monitor, see the IP, then `curl http://<ip>/toggle` from your laptop.

### What's happening underneath

That ~25 lines of user code rides [[learning/notes/quick-context/pupper-lab5-neural-controller|on top]] of roughly **3 MB of compiled firmware** (FreeRTOS, LwIP TCP/IP stack, wpa_supplicant, mbedTLS, WiFi MAC, ROM driver glue) that ESP-IDF links in automatically. The LED toggle takes <1 ms; the request travels through:

```
HTTP GET /toggle
   ▼
TCP socket (LwIP) on Core 1
   ▼
WiFi MAC frame (Core 0)
   ▼
OFDM modulator (PHY hardware)
   ▼
2.4 GHz RF front-end → antenna → air → router
```

### Programming the chip — the auto-reset circuit

Almost every ESP32 dev board (the ones with a USB connector) has a two-transistor circuit on its USB-UART bridge that toggles `EN` (reset) and `GPIO0` (boot mode) automatically when `esptool.py` opens the serial port. Without it you'd have to hold a BOOT button and tap RST every time you flash. The Arduino Uno R4 WiFi reuses the same trick — see [[learning/notes/quick-context/wifi-chip-arduino-uno-r4|that note]] for how Arduino routes USB through the ESP32-S3 as a USB-to-serial bridge for the Renesas main MCU.

**The one thing most outsiders get wrong about this is...** thinking the ESP32 is "just a faster Arduino." Architecturally it's closer to a tiny Linux SoC: dual cores, MMU with flash cache, preemptive RTOS, a ~3 MB binary blob handling 802.11 in real time, hardware crypto accelerators, and watchdogs you have to feed. The Arduino `setup()`/`loop()` API is a thin shim — `loop()` is itself a FreeRTOS task that you can starve. This is why blocking `delay(5000)` calls work fine on AVR but cause "Brownout detector was triggered" or "Task watchdog got triggered" panics on ESP32 if they run on Core 0.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/quick-context/wifi-chip-arduino-uno-r4]]** — Deep dive on the ESP32-S3's WiFi radio ([[learning/notes/quick-context/wifi-chip-arduino-uno-r4|OFDM]], MAC/PHY split, antenna). Read that for what happens after `WiFi.begin()`.
- **[[learning/notes/micro-context/microcontroller]]** — Where the ESP32 sits in the broader MCU family tree (vs STM32, AVR, PIC).
- **[[learning/notes/micro-context/stm32-microcontroller]]** — The other MCU family used in Pupper. STM32 = hard real-time motor control; ESP32 = networking, audio, ML.
- **[[learning/notes/quick-context/firmware]]** — The firmware concept; the ESP32's bootloader chain (ROM → 2nd-stage → app) is a worked example.
- **[[learning/notes/quick-context/embedded-communication-protocols]]** — All the buses (SPI, I2C, I2S, CAN/TWAI, UART) the ESP32 exposes as peripherals.
- **[[learning/notes/quick-context/raspberry-pi-5-components]]** — Higher up the stack: Pi runs Linux, ESP32 runs FreeRTOS. The ESP32 fills the gap between bare-metal MCUs and full Linux SBCs.
- **[[learning/notes/quick-context/silicon-die]]** — The ESP32's WiFi radio, CPUs, and [[learning/notes/micro-context/sram|SRAM]] all share a single die — the cost magic comes from this integration.
- **FreeRTOS** — The preemptive RTOS the ESP32 runs by default. Tasks, queues, semaphores. ESP-IDF wraps it; Arduino-ESP32 hides it.
- **ESPHome / Tasmota** — Pre-built firmware projects that turn an ESP32 into a YAML-configured smart-home device with no C code.
- **Matter / Thread** — New smart-home interop protocol; the ESP32-C6 and H2 were designed around it.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does the ESP32 need external SPI flash when an STM32 has flash on-die?
<details>
<summary>Answer</summary>
Cost and process tech. The ESP32's wireless transceiver, RF front-end, and ADCs are built on a mixed-signal RF-friendly process where embedded flash is expensive or unavailable. Putting flash off-chip on a cheap separate die (commodity NOR flash) keeps the SoC small and lets users pick their own flash size (4/8/16 MB). The cost is added board area + the XIP cache complexity. See: How It Works — Why "Execute in Place" matters.
</details>

**Q2:** You see `IRAM_ATTR` in front of an interrupt handler in someone's ESP32 code. What does it do and why does it matter?
<details>
<summary>Answer</summary>
`IRAM_ATTR` forces the [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|function]] to be linked into internal SRAM (IRAM) instead of left in external flash. Without it, the ISR would be fetched through the flash cache; a cache miss adds hundreds of nanoseconds, and if the cache is disabled (e.g., during a flash write), code in flash is literally unreachable and the chip panics. ISRs and any code that runs while flash is being written must live in IRAM. See: How It Works — Why "Execute in Place" matters.
</details>

**Q3:** Your ESP32 keeps panicking with "Task watchdog got triggered" whenever you call a long-running computation. What's the likely cause and fix?
<details>
<summary>Answer</summary>
You're starving the IDLE task on Core 0 (or whichever core the watchdog is monitoring). FreeRTOS feeds the watchdog from the idle task; if your task never yields, idle never runs, watchdog fires. Fix: insert `vTaskDelay(1)` to yield, split the work into smaller chunks, or move the heavy work to Core 1 with `xTaskCreatePinnedToCore(..., 1)` so it doesn't fight the WiFi stack on Core 0. See: How It Works — Dual-Core Asymmetry.
</details>

**Q4:** Someone claims "the ESP32-C3 is strictly better than the ESP32 because it's newer and has BLE 5." What's wrong with that claim?
<details>
<summary>Answer</summary>
"Newer" isn't strictly better — they target different points. The C3 is single-core RISC-V at 160 MHz; the original ESP32 is dual-core Xtensa at 240 MHz. For CPU-bound or concurrent workloads (audio processing, multi-task firmware where the WiFi stack needs its own core), the ESP32 is faster. The C3 is cheaper and lower-power for simple BLE/WiFi sensor nodes, but it sacrifices compute. "Newer" in the ESP32 family means "more variants targeting more niches," not "drop-in upgrade." See: The Key Tension — Choosing among the ESP32 variants.
</details>

**Q5:** Why would you put an ESP32 alongside an STM32 in the same product (like the Pupper or Arduino Uno R4 WiFi) instead of using just the ESP32?
<details>
<summary>Answer</summary>
Determinism and peripheral specialization. The ESP32's CPU spends a non-trivial fraction of every second servicing the WiFi MAC, FreeRTOS scheduling, and flash cache misses — its interrupt latency has long tails. An STM32 running bare-metal or with a stripped RTOS responds to interrupts in single-digit microseconds, every time, which is what 1 kHz motor control loops or motor commutation need. STM32s also have peripherals the ESP32 lacks (high-resolution motor-control timers, true 12-bit DACs, op-amps on the C-series, 5V tolerant I/O on some parts). So the split is: STM32 does hard-real-time motion, ESP32 does networking and rich peripherals. See [[learning/notes/quick-context/wifi-chip-arduino-uno-r4]] for the dual-chip pattern in Arduino's design.
</details>

</details>
