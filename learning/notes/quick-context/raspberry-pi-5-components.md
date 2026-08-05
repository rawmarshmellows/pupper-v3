---
topic: Raspberry Pi 5 — Board Components
created: 2026-04-05
---

> **Related:** [[quick-context/pcb-printed-circuit-board]] | [[quick-context/pupper-brain]] | [[micro-context/stm32-microcontroller]] | [[quick-context/common-ic-packages]] | [[quick-context/embedded-communication-protocols]]

> **TL;DR:** The Raspberry Pi 5 is a credit-card-sized single-board computer built around a Broadcom BCM2712 SoC and a custom RP1 "southbridge" I/O controller. It runs a full Linux OS and serves as the high-level brain in robots like Pupper, handling vision, planning, and communication — while real-time motor control is delegated to dedicated [[micro-context/stm32-microcontroller|STM32 microcontrollers]].

> **Photo reference:** [[micro-context/raspberry-pi-5.png]]

# Raspberry Pi 5 — Board Components

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **BCM2712 SoC** | Broadcom system-on-chip — quad-core ARM Cortex-A76 @ 2.4GHz, the main processor that runs Linux and applications |
| **RP1** | Raspberry Pi's custom I/O controller chip — a "southbridge" that manages USB, Ethernet, GPIO, camera, and display interfaces so the SoC doesn't have to |
| **LPDDR4X** | Low-Power Double Data Rate 4X [[learning/notes/quick-context/ram-addressing-decoder|RAM]] — the board's working memory (1/2/4/8GB variants, marked on the PCB silkscreen) |
| **GPIO** | General-Purpose Input/Output — the 40-pin header that connects to HATs, sensors, and other hardware via [[learning/notes/micro-context/i2c|I2C]], [[learning/notes/micro-context/spi|SPI]], [[learning/notes/quick-context/uart|UART]], and raw digital pins |
| **PCIe** | Peripheral Component Interconnect Express — a high-speed serial bus (1-lane Gen 2 on Pi 5) used to connect NVMe SSDs or other expansion cards |

## Every Component on the Board

Starting from the top-left and working around the board:

### Connectors & Ports (left/top/bottom edges)

| Label on PCB | Component | What It Does |
|---|---|---|
| **PWR** | USB-C power input | Supplies 5V/5A (25W) to the board via USB Power Delivery |
| **STAT** | Status LED | Indicates board power/activity state |
| **BAT (J5)** | RTC battery connector | JST connector for a coin cell to keep the real-time clock running when powered off |
| **HDMI0 (J7)** | Micro HDMI port | First display output — up to 4Kp60 via HDMI 2.0 |
| **HDMI1 (J7)** | Micro HDMI port | Second display output — dual 4K monitors supported simultaneously |
| **VID** | Composite video test point | Legacy analog video output (active via config) |
| **CAM/DISP 1** | MIPI CSI/DSI connector | 22-pin FPC connector for camera module or DSI display (active lane via software) |
| **CAM/DISP 0** | MIPI CSI/DSI connector | Second camera/display FPC connector |
| **PoE (J14)** | Power over Ethernet header | 4-pin header for a PoE+ HAT — powers the board through the Ethernet cable |
| **Ethernet (J14 area)** | Gigabit Ethernet jack | Trxcom magjack with integrated magnetics — 1 Gbps networking |
| **USB 3.0** | 2x USB 3.0 Type-A | SuperSpeed 5 Gbps ports (the blue-tabbed pair) — via RP1 |
| **USB 2.0** | 2x USB 2.0 Type-A | 480 Mbps ports (the white-tabbed pair) — via RP1 |
| **PCIe (J20)** | PCIe FPC connector | 16-pin FPC for a PCIe x1 Gen 2 (5 GT/s) link — used with an NVMe HAT or [[quick-context/raspberry-pi-ai-hat|AI HAT+]] for neural network acceleration |
| **HAT+ GPIO** | 40-pin header | Standard Raspberry Pi GPIO header with I2C, SPI, UART, [[learning/notes/micro-context/pwm-pulse-width-modulation|PWM]], and 26 general-purpose pins |
| **FAN** | 4-pin fan connector | JST connector for the official active cooler — PWM speed control and tach feedback |

### Major ICs (chips on the board)

| Chip | Markings / Location | What It Does |
|---|---|---|
| **Broadcom BCM2712** | Large silver heat-spreader chip, center-top, labeled "BROADCOM" | The main SoC: quad-core Cortex-A76 @ 2.4GHz, VideoCore VII GPU, hardware video decode (H.265/H.264), crypto engine. Connects to RAM directly and to RP1 over a dedicated 4-lane MIPI link |
| **RP1** | Dark chip with Raspberry Pi logo, center-right | Custom southbridge IC designed by Raspberry Pi. Manages: 2x USB 3.0, 2x USB 2.0, Gigabit Ethernet MAC, 2x MIPI camera/display transceivers, GPIO bank, SPI, I2C, UART. Connected to BCM2712 via a PCIe Gen 2 x4 link |
| **LPDDR4X RAM** | Chip adjacent to BCM2712, with silkscreen markers "8G / 4G / 2G / 1G" | Working memory — the PCB has solder pads for different density packages; your variant has one populated (the markers indicate which is active) |
| **WiFi/BT module** | Metal RF shield, top-right area | Dual-band 802.11ac Wi-Fi 5 and Bluetooth 5.0 / BLE — likely Infineon CYW43455 under the shield |
| **PMIC** | Smaller IC near bottom-center area | Power Management IC — generates the multiple voltage rails (1.1V core, 1.8V I/O, 3.3V peripherals) from the 5V USB-C input |
| **Ethernet PHY** | Small IC near the Ethernet jack (J14 area) | Physical layer transceiver for Gigabit Ethernet — converts digital signals to/from the cable |

```
RASPBERRY PI 5 — COMPONENT MAP (top view, ports facing down):

    USB-C   STAT                  PCIe (J20)         WiFi/BT
    (PWR)    LED                  FPC conn            shield
      │       │                     │                   │
  ┌───┴───────┴─────────────────────┴───────────────────┴───┐
  │  ○                                                   ○  │
  │  BAT(J5)     ┌──────────┐    ┌─────────┐               │
  │              │ BROADCOM │    │  RAM    │    ┌────────┐  │
  │  HDMI0       │ BCM2712  │    │LPDDR4X │    │ 40-pin │  │
  │  HDMI1       │  (SoC)   │    └─────────┘   │  GPIO  │  │
  │              └──────────┘                   │ header │  │
  │  VID                         ┌─────────┐    └────────┘  │
  │  CAM/DISP 1                  │   RP1   │                │
  │  CAM/DISP 0                  │ (I/O)   │          FAN   │
  │              PoE(J14) PMIC   └─────────┘             ○  │
  │  ○                                                   ○  │
  └───┬──────────────┬──────────────┬───────────────────────┘
      │              │              │
   Ethernet     2x USB 3.0    2x USB 2.0
   (Trxcom)      (blue)        (white)
```

## How It Fits in Pupper

The Raspberry Pi 5 is the **high-level controller**: it runs Linux, ROS 2, computer vision (camera via CSI), and voice/LLM processing. It communicates with the [[quick-context/pupper-brain|Pupper control board]] (which holds the [[micro-context/stm32-microcontroller|STM32 MCUs]]) over a serial or CAN-to-USB bridge. The Pi handles *what* the robot should do; the STM32s handle *how* — executing the 1kHz motor control loops in hard real-time.

| Layer | Hardware | Runs | Timing |
|-------|----------|------|--------|
| High-level | Raspberry Pi 5 (BCM2712, Linux) | ROS 2, vision, planning, LLM | Soft real-time (~100Hz) |
| Low-level | STM32 MCUs (Cortex-M4, bare-metal) | PID loops, motor commands, IMU fusion | Hard real-time (1000Hz) |
