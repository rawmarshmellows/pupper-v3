---
topic: Raspberry Pi AI HAT+ — Edge AI Acceleration
created: 2026-04-07
---

# Raspberry Pi AI HAT+ — Edge AI Acceleration

> **Related:** [[learning/notes/quick-context/voltage]] | [[learning/notes/quick-context/transistor]] | [[learning/notes/quick-context/can-bus]] | [[learning/notes/micro-context/eeprom]] | [[learning/notes/quick-context/soldering]]

> **TL;DR:** The Raspberry Pi AI HAT+ is a family of add-on boards that snap onto a [[learning/notes/quick-context/raspberry-pi-5-components|Raspberry Pi 5]] and provide a dedicated NPU (Neural Processing Unit) for running AI inference locally — 10-40x faster than the CPU alone at a fraction of the power. The lineup ranges from a 13 TOPS vision-focused board ($70) to the AI HAT+ 2 with 40 TOPS and its own 8GB RAM for running small LLMs on-device ($180).

## The Core Problem

Running AI models (object detection, pose estimation, image classification) on a Raspberry Pi's CPU is slow (~2 FPS for YOLOv8) and pegs all four cores at 100%, leaving nothing for the rest of your application. The AI HAT+ offloads neural network math to a purpose-built Hailo NPU over [[learning/notes/quick-context/raspberry-pi-5-components|PCIe]], freeing the CPU while delivering real-time inference at low power (2.5-3W). This also enables fully local, cloud-free AI — critical for privacy, latency, cost, and offline operation in applications like [[learning/notes/quick-context/pupper-lab7-vision-tracking|Pupper's autonomous tracking]].

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **HAT (Hardware Attached on Top)** | Official Raspberry Pi spec for add-on boards: 65 x 56 mm, 40-pin GPIO header, I2C [[learning/notes/micro-context/eeprom|EEPROM]] for auto-configuration — the mechanical and electrical standard that makes boards plug-and-play |
| **NPU (Neural Processing Unit)** | A chip designed specifically for the multiply-accumulate operations that dominate neural networks, with massively parallel datapaths that a general-purpose CPU cannot match |
| **TOPS (Tera Operations Per Second)** | NPU throughput metric — how many trillion math operations per second the chip can perform. Caveat: TOPS depends on precision (INT4 vs INT8) and does not capture memory bandwidth or software efficiency |
| **Hailo** | Israeli semiconductor company that manufactures the NPU chips used in all Pi AI HATs: Hailo-8L (13 TOPS), Hailo-8 (26 TOPS), and Hailo-10H (40 TOPS) |
| **Edge AI** | Running inference on the device itself rather than sending data to cloud servers — trading model size for privacy, latency, cost, and offline capability |

<details>
<summary><strong>How It Works</strong> — From camera frame to detection result</summary>

### Physical Connection

The AI HAT+ mounts on top of the Pi 5 via standoffs and a 40-pin stacking header. A flat ribbon cable (FPC) plugs into the Pi 5's PCIe connector (the 16-pin FPC port labeled J20 on the [[learning/notes/quick-context/raspberry-pi-5-components|Pi 5 board]]). This gives the Hailo NPU a direct PCIe Gen 3 link to the SoC — much faster than USB.

```
PHYSICAL STACK (side view)
═══════════════════════════════════════════════

         ┌─────────────────────────────┐
         │       AI HAT+ board        │  ← Hailo NPU + (optional) 8GB DDR
         │  ┌───────┐                 │
         │  │ Hailo │   [FPC ribbon]──┤──► PCIe (J20)
         │  │  NPU  │                 │
         │  └───────┘                 │
         └──────────┬──────────────────┘
                    │ 40-pin stacking header
         ┌──────────┴──────────────────┐
         │     Raspberry Pi 5          │
         │  ┌────────┐  ┌─────┐       │
         │  │BCM2712 │  │ RP1 │       │
         │  │ (SoC)  │  │(I/O)│       │
         │  └────────┘  └─────┘       │
         └─────────────────────────────┘
```

### Data Flow: AI HAT+ (Original — Vision)

For computer vision workloads on the original AI HAT+ (13T or 26T):

1. [[learning/notes/quick-context/camera-fundamentals|Camera]] captures a frame via MIPI CSI
2. Pi CPU preprocesses the image (resize, normalize, color convert)
3. Preprocessed [[learning/notes/quick-context/tensor|tensor]] is sent to the Hailo NPU over PCIe
4. NPU executes the neural network (e.g., YOLOv8) in its internal pipeline
5. Results (bounding boxes, class IDs, confidence scores) return over PCIe
6. Pi CPU post-processes results (non-max suppression, coordinate mapping)

The model weights live in the **Pi's system RAM** and are streamed to the NPU each inference pass. This works fine for vision models (a few MB of weights), but becomes a bottleneck for LLMs (hundreds of MB).

```
DATA FLOW — VISION INFERENCE (AI HAT+ 13T/26T)
═══════════════════════════════════════════════════════════════

  Camera ──CSI──► Pi CPU ──PCIe──► Hailo NPU ──PCIe──► Pi CPU
   (raw         (preprocess)     (inference)        (postprocess)
    frame)                        ~5-30 FPS           bboxes,
                                  @ 2.5W              classes

  Model weights: stored in Pi's LPDDR4X RAM
  Bottleneck:    PCIe bandwidth for large models
```

### Data Flow: AI HAT+ 2 (Generative AI)

The AI HAT+ 2 changes the architecture fundamentally: the Hailo-10H chip has its **own dedicated 8GB DDR RAM** soldered onto the HAT board, invisible to the Pi. Model weights live entirely in this on-board memory, eliminating the PCIe bottleneck for model loading.

```
DATA FLOW — LLM INFERENCE (AI HAT+ 2)
═══════════════════════════════════════════════════════════════

                        AI HAT+ 2
                  ┌─────────────────────┐
                  │  ┌───────┐ ┌──────┐ │
  Pi CPU ──PCIe──►│  │Hailo  │ │ 8GB  │ │──PCIe──► Pi CPU
  (prompt         │  │10H    │◄┤ DDR  │ │          (tokens)
   tokens)        │  │(NPU)  │ │(on-  │ │
                  │  └───────┘ │board) │ │
                  │            └──────┘ │
                  └─────────────────────┘

  Model weights: stored in HAT's own 8GB DDR (not Pi RAM)
  Benefit:       Pi RAM stays free; no PCIe weight streaming
  Limitation:    8GB caps models at ~1.5-2B params (INT4)
```

### Software Stack

The Raspberry Pi OS auto-detects the Hailo NPU at boot. The software ecosystem includes:

- **`rpicam-apps` / `picamera2`** — Camera frameworks with native Hailo integration. Adding `--post-process-file detect.json` to a camera command runs YOLO inference automatically.
- **HailoRT** — Low-level runtime and API for loading compiled models (`.hef` files) and running inference.
- **Hailo Model Zoo** — Pre-compiled models for common tasks: YOLOv5/v8 detection, pose estimation, segmentation, image classification.
- **Hailo Dataflow Compiler** — Converts models from ONNX/TensorFlow to Hailo's `.hef` format, applying quantization (FP32 → INT8/INT4) and layer fusion.
- **Hailo Ollama server** (AI HAT+ 2 only) — Exposes a standard Ollama REST API for LLM chat, compatible with tools that speak the Ollama protocol.

</details>

<details>
<summary><strong>GPIO-Free Alternatives</strong> — Using Hailo without blocking the 40-pin header</summary>

### Why This Matters

The official AI HAT+ mounts on top of the Pi 5 via the 40-pin GPIO stacking header, physically blocking access to those pins. For robotics projects like [[learning/notes/quick-context/pupper-v3-labs|Pupper v3]] that need GPIO for motor control, sensors, and communication buses, this is a dealbreaker. The good news: **all AI inference data flows over PCIe via the flat ribbon cable (FPC), not GPIO.**

### What the GPIO Header Actually Does on the AI HAT+

| Function | Pins Used | Required for Inference? |
|----------|-----------|----------------------|
| Mechanical mounting / alignment | All 40 | No |
| Power delivery (5V from Pi) | 5V + GND pins | No (FPC carries 5V too) |
| HAT ID EEPROM (auto-detect at boot) | GPIO 0 & 1 (I2C0) | No (manual config.txt works) |
| PCIe data transfer | None — uses FPC cable | N/A |

**Bottom line:** Zero GPIO pins carry inference data. The FPC connector (J20) on the Pi 5 provides PCIe (1 lane, Gen 2/3), 5V power (1A / 5W max), and control signals — everything needed to run a Hailo module.

### The Pi 5 PCIe FPC Connector (J20) — What It Carries

```
16-PIN FPC CONNECTOR PINOUT
═══════════════════════════════════════════════
Pin  Signal              Notes
───  ──────────────────  ─────────────────────
 1   5V                  500mA max
 2   5V                  500mA max (1A total)
 3   GND
 4   PCIE_CLK_P          Reference clock +
 5   GND
 6   GND
 7   PCIE_CLK_N          Reference clock −
 8   PCIE_RX_P           Data receive +
 9   GND
10   PCIE_RX_N           Data receive −
11   PCIE_TX_P           Data transmit +
12   GND
13   PCIE_PWR_EN         3.3V out (power up signal)
14   PCIE_DET_WAKE       3.3V in (device present)
15   PCIE_CLKREQ_N       Clock request
16   PCIE_RST_B          Reset

Power budget: 5V × 1A = 5W max through FPC
```

### Option 1: FPC-Only M.2 Adapters (Best for Pupper)

These boards connect ONLY via the FPC ribbon cable — zero GPIO contact, all 40 pins free.

**Geekworm M901** — Top recommendation
- ~$15-20, M.2 M-Key slot (2230/2242/2260/2280)
- Connects via FPC cable only, mounts on top without touching GPIO
- Explicitly tested with Hailo-8 and Hailo-8L
- No EEPROM → manually set `dtparam=pciex1_gen=3` in config.txt
- Power: 5W from FPC only — fine for Hailo-8L (~1.5W typ, ~4W peak), tight for Hailo-8 (~8.25W peak)

**Pineboards HatDrive! Bottom**
- Mounts underneath the Pi 5 board
- 40mm FPC cable, integrated 3A [[learning/notes/quick-context/voltage|voltage]] regulator
- M.2 M-Key, supports 2230/2242/2280
- GPIO completely unobstructed on top

**Seeed Studio PCIe 3.0 Dual M.2 HAT (back-mounted)**
- ~$45, mounts on the back of the Pi
- Two M.2 slots — run NVMe storage + Hailo simultaneously (solves the PCIe exclusivity problem)
- PCIe Gen 3 with ASM2806 switch
- GPIO free on top

```
MOUNTING COMPARISON (side view)
═══════════════════════════════════════════════

OFFICIAL AI HAT+ (blocks GPIO):

    ┌─────────────────────┐
    │  AI HAT+ (Hailo)    │ ← sits ON TOP of GPIO
    │  ███ GPIO header ███│
    ├─────────────────────┤
    │  Raspberry Pi 5     │
    └─────────────────────┘
    GPIO: BLOCKED


GEEKWORM M901 (FPC-only):

    ┌─────────────────────┐
    │  M901 + Hailo M.2   │ ← FPC cable only, no GPIO contact
    └─────────┬───────────┘
              │ FPC ribbon
    ┌─────────┴───────────┐
    │  Raspberry Pi 5     │
    │  ░░░ GPIO FREE ░░░  │ ← all 40 pins available
    └─────────────────────┘


PINEBOARDS BOTTOM-MOUNT:

    ┌─────────────────────┐
    │  Raspberry Pi 5     │
    │  ░░░ GPIO FREE ░░░  │ ← all 40 pins available
    ├─────────┬───────────┤
              │ FPC ribbon
    ┌─────────┴───────────┐
    │  HatDrive + M.2     │ ← underneath the Pi
    └─────────────────────┘
```

### Option 2: Stacking Header Workaround (If You Already Own the AI HAT+)

If you already have the official AI HAT+, you can use extra-tall stacking headers (15mm pin length) so GPIO pins protrude above the HAT board. The HAT only electrically uses GPIO 0 & 1 (I2C EEPROM) — the other ~36 pins pass through and are fully usable. Physical access with jumper wires is the main challenge, not electrical incompatibility.

### Option 3: USB-Based (Not Recommended for Pi 5)

Hailo-8 M.2 modules can work inside USB3-to-NVMe enclosures, and Hailo has confirmed basic functionality. However:
- Pi 5 lacks USB4/Thunderbolt — stuck with USB 3.0 bandwidth
- Added CPU overhead defeats the purpose of a dedicated accelerator
- Hailo does not recommend this configuration for Pi 5

### Power Budget Considerations

| Hailo Module | Typical Power | Peak Power | Fits 5W FPC Budget? |
|-------------|--------------|------------|---------------------|
| Hailo-8L (13 TOPS) | ~1.5W | ~4W | Yes — comfortable margin |
| Hailo-8 (26 TOPS) | ~2.5W | ~8.25W | Risky — peak exceeds 5W |
| Hailo-10H (40 TOPS) | TBD | TBD | Verify with adapter specs |

For FPC-only adapters with no supplemental power, the **Hailo-8L is the safe choice**. If you need 26+ TOPS, look for adapters with auxiliary power input (Geekworm X1003, Seeed dual M.2) or use the GPIO stacking header workaround.

### Recommendation for Pupper v3

**Geekworm M901 + Hailo-8L (M-key)** is the simplest path:
- ~$15-20 for the adapter + ~$45-55 for the Hailo-8L M.2 module
- FPC-only: all 40 GPIO pins free for motor control, IMU, [[learning/notes/quick-context/can-bus|CAN bus]]
- 13 TOPS is sufficient for real-time YOLOv8 at ~15 FPS
- Power draw stays well within FPC's 5W budget
- One line in config.txt: `dtparam=pciex1_gen=3`
- Trade-off: no auto-detect EEPROM (trivial) and the official AI HAT+ has slightly better thermal design (the soldered Hailo chip has a heatsink integrated into the PCB)

</details>

<details>
<summary><strong>The Product Lineup</strong> — Three boards, three use cases</summary>

### Evolution

| Product | Released | Hailo Chip | TOPS | Precision | On-board RAM | Price | Primary Use |
|---------|----------|-----------|------|-----------|-------------|-------|-------------|
| AI Kit | Jun 2024 | Hailo-8L (M.2 module) | 13 | INT8 | None | ~$70 | First-gen, modular design |
| AI HAT+ 13T | Oct 2024 | Hailo-8L (soldered) | 13 | INT8 | None | ~$70 | Budget vision |
| AI HAT+ 26T | Oct 2024 | Hailo-8 (soldered) | 26 | INT8 | None | ~$110 | High-perf vision |
| AI HAT+ 2 | Apr 2026 | Hailo-10H (soldered) | 40 | INT4 | 8GB DDR | $180 | LLMs + vision |

The progression from AI Kit to AI HAT+ eliminated the M.2 module in favor of [[learning/notes/quick-context/soldering|soldering]] the Hailo chip directly to the PCB — better thermals, simpler assembly, and a thinner stack.

### Which One to Buy?

```
DECISION TREE
═══════════════════════════════════════════════════════════════

  Need LLMs / generative AI on-device?
    │
    ├── YES ──► AI HAT+ 2 ($180)
    │           Only option with dedicated RAM for model weights
    │
    └── NO ──► Need max vision FPS?
                │
                ├── YES ──► AI HAT+ 26T ($110)
                │           ~28 FPS YOLOv8-XL, best vision perf
                │
                └── NO ──► AI HAT+ 13T ($70)
                            ~15 FPS YOLOv8-M, good enough for
                            most single-camera applications
```

### Total System Cost

| Component | Cost |
|-----------|------|
| Raspberry Pi 5 (4GB) | $60 |
| AI HAT+ 26T | $110 |
| Camera Module 3 | $25 |
| Power supply + SD card | $20 |
| **Total edge AI system** | **~$215** |

Compare to an NVIDIA Jetson Orin Nano Super ($249 board alone, no camera, no storage).

</details>

<details>
<summary><strong>The Key Tension</strong> — TOPS don't tell the whole story</summary>

### TOPS vs. Real-World Performance

The headline metric for NPUs is TOPS — but it's misleading across architectures:

| Chip | TOPS | Precision | Effective INT8 TOPS |
|------|------|-----------|-------------------|
| Hailo-8L | 13 | INT8 | 13 |
| Hailo-8 | 26 | INT8 | 26 |
| Hailo-10H | 40 | INT4 | ~20 (INT8 equiv.) |

The Hailo-10H's "40 TOPS" uses INT4 precision — each operation does half the numerical work of an INT8 operation. For vision tasks that need INT8 accuracy, the 26T actually outperforms the AI HAT+ 2. Real-world YOLOv8-XL benchmarks confirm this:

- AI HAT+ 26T: ~28 FPS
- AI HAT+ 2: ~25 FPS

**The AI HAT+ 2 is not a strictly better product** — it's a different product for a different workload (generative AI), enabled by its dedicated RAM.

### NPU vs. CPU for LLMs: A Surprising Tradeoff

Paradoxically, the Pi 5's CPU can sometimes match or beat the Hailo-10H in raw LLM token generation:

| Method | Power Draw | Tokens/sec (Llama 3.2 1B) |
|--------|-----------|--------------------------|
| Pi 5 CPU (llama.cpp) | ~10W | ~8-10 |
| AI HAT+ 2 (Hailo Ollama) | ~3W | ~6-8 |

The NPU is power-limited (3W thermal budget) while the CPU can burst up to 10W. The NPU's real advantage is **concurrency** — it runs inference without consuming any CPU cycles, so the Pi can simultaneously handle other tasks (camera capture, ROS 2 nodes, network I/O).

### The PCIe Exclusivity Problem

The Pi 5 has a **single PCIe lane**. Using an AI HAT means you cannot simultaneously use:
- An NVMe SSD via PCIe (must use USB or SD storage instead)
- Any other PCIe expansion card

This forces a choice between fast storage and AI acceleration — a real constraint for applications that need both (e.g., video recording + real-time analysis).

### LLM Quality Ceiling

The 8GB of dedicated RAM on the AI HAT+ 2 constrains models to ~1.5-2 billion parameters at INT4 quantization. For context:

| Model Size | Parameters | Quality Level |
|-----------|-----------|--------------|
| AI HAT+ 2 max | ~1.5-2B | Basic chat, simple Q&A — frequent errors, no nuance |
| Llama 2 70B class | ~70B | Competent general assistant |
| Frontier LLMs (GPT-4+) | ~1T+ (estimated) | Expert-level reasoning |

The AI HAT+ 2 enables a parlor trick, not a replacement for cloud AI. Its sweet spot is structured, domain-specific tasks: extracting sensor readings from voice, classifying simple intents, or generating short templated responses.

</details>

<details>
<summary><strong>Concrete Example</strong> — Running YOLOv8 object detection</summary>

### Setup (AI HAT+ 26T)

```bash
# 1. Install the Hailo runtime and camera support
sudo apt update && sudo apt install hailo-all rpicam-apps

# 2. Reboot to load the PCIe driver
sudo reboot

# 3. Verify the Hailo NPU is detected
hailortcli fw-control identify
# Output: Hailo-8 (Device: 0000:01:00.0)
#         Firmware Version: 4.x.x
#         Board Name: Hailo-8

# 4. Run YOLOv8 detection on a live camera feed
rpicam-hello -t 0 --post-process-file /usr/share/rpi-camera-assets/hailo_yolov8_detection.json

# That's it — bounding boxes overlay on the preview window.
# The Hailo NPU handles inference; the Pi CPU handles camera + display.
```

### Using It from Python (Picamera2)

```python
from picamera2 import Picamera2
from picamera2.devices import Hailo
import numpy as np

# Load YOLOv8 model onto the Hailo NPU
model = Hailo("/usr/share/hailo-models/yolov8s_h8l.hef")

# Configure camera
cam = Picamera2()
cam.configure(cam.create_preview_configuration(
    main={"size": (640, 480)},
))
cam.start()

while True:
    frame = cam.capture_array()

    # Run inference on the NPU (returns in ~30ms on 26T)
    detections = model.run(frame)

    for det in detections:
        class_name = det["label"]       # e.g., "person"
        confidence = det["confidence"]  # e.g., 0.87
        bbox = det["bbox"]              # [x1, y1, x2, y2]
        print(f"{class_name}: {confidence:.0%} at {bbox}")
```

### In Pupper's Vision Stack

[[learning/notes/quick-context/pupper-lab7-vision-tracking|Lab 7]] uses the Hailo accelerator (26 TOPS variant) to run YOLOv5 at ~5 FPS on the robot. The detection results feed into a ROS 2 node that publishes `Detection2DArray` messages, which drive the IDLE → SEARCH → TRACK state machine for autonomous object following. The NPU handles inference while the Pi simultaneously runs ROS 2, the LLM voice interface from Lab 6, and the neural locomotion controller from Lab 5.

### Custom Model Pipeline

To run your own model on the Hailo NPU:

```
Your Model (PyTorch/TF/ONNX)
         │
         ▼
  Hailo Dataflow Compiler        ← Runs on a powerful x86 machine
  ┌─────────────────────────┐
  │ 1. Parse model graph    │
  │ 2. Quantize FP32→INT8   │    Requires a calibration dataset
  │ 3. Fuse layers          │    (~100 representative images)
  │ 4. Map to NPU pipeline  │
  │ 5. Output .hef file     │
  └─────────────────────────┘
         │
         ▼
  Deploy .hef to Pi + Hailo      ← Just copy the file
```

The compilation step is the main friction point — it requires an x86 Linux machine with Hailo's SDK, and the quantization can reduce model accuracy. You need to validate that your model's accuracy survives the FP32 → INT8 conversion.

**The one thing most outsiders get wrong about this is...** thinking higher TOPS automatically means better performance. In practice, the 26T (26 TOPS, INT8) outperforms the AI HAT+ 2 (40 TOPS, INT4) on most vision tasks because INT8 precision is more efficient for the models that actually run on these boards. TOPS is like engine horsepower — it matters, but tire grip (memory bandwidth), transmission (software stack), and aerodynamics (model optimization) determine lap times.

</details>

<details>
<summary><strong>Competitive Landscape</strong> — How Pi AI HAT compares</summary>

| Platform | TOPS | Power | Price | Ecosystem | Best For |
|----------|------|-------|-------|-----------|----------|
| **Pi AI HAT+ 26T** | 26 (INT8) | ~3W | $110 + $60 Pi | Pi ecosystem, rpicam | Hobbyist vision, robotics |
| **Pi AI HAT+ 2** | 40 (INT4) | ~3W | $180 + $60 Pi | Pi ecosystem, Ollama | Edge LLM experiments |
| **Google Coral USB** | 4 (INT8) | ~2W | ~$60 | TFLite only | Simple classification |
| **NVIDIA Jetson Orin Nano Super** | 67 (INT8) | 7-15W | $249 | CUDA, full PyTorch | Production vision/LLM |
| **Pi AI Camera (IMX500)** | ~3 (INT8) | ~1W | $70 | Camera-only | Single-camera detection |

The Pi AI HAT occupies a sweet spot: cheaper than Jetson, vastly more capable than Coral, and integrated into the massive Raspberry Pi ecosystem. The tradeoff is vendor lock-in to Hailo's model compiler and `.hef` format — you can't run arbitrary PyTorch models directly.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[learning/notes/quick-context/raspberry-pi-5-components]]** — The host board: PCIe connector, GPIO header, BCM2712 SoC, LPDDR4X RAM — everything the AI HAT connects to
- **[[learning/notes/quick-context/pupper-lab7-vision-tracking]]** — Real-world use: Hailo 26T running YOLOv5 for autonomous object tracking on the Pupper robot
- **[[learning/notes/quick-context/camera-fundamentals]]** — How cameras capture the frames that the AI HAT processes — sensors, lenses, intrinsics
- **[[learning/notes/quick-context/pupper-lab5-neural-controller]]** — Neural network inference for locomotion — a different kind of on-device AI (policy networks vs. vision models)
- **[[learning/notes/quick-context/embedded-communication-protocols]]** — PCIe is one of many protocols; understanding the communication layer between Pi and NPU
- **[[learning/notes/quick-context/common-ic-packages]]** — The Hailo chips use BGA packages soldered to the HAT PCB
- **[[learning/notes/quick-context/silicon-die]]** — What's inside the Hailo chip at the [[learning/notes/quick-context/transistor|transistor]] level
- **Model quantization** — The process of converting FP32 weights to INT8/INT4 for NPU deployment — a deep topic in its own right
- **ONNX (Open Neural Network Exchange)** — The intermediate model format used as input to Hailo's compiler

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** Why can't you just run YOLOv8 on the Pi 5's CPU instead of buying an AI HAT?
<details>
<summary>Answer</summary>
You can, but at ~2 FPS while consuming all four CPU cores at 100%. The AI HAT delivers 15-28 FPS at ~3W while leaving the CPU free for your application logic. See: The Core Problem.
</details>

**Q2:** The AI HAT+ 2 has 40 TOPS vs. the AI HAT+ 26T's 26 TOPS. Why is the 26T actually faster for vision tasks?
<details>
<summary>Answer</summary>
The 40 TOPS figure is measured at INT4 precision (4-bit operations), while the 26 TOPS is at INT8 (8-bit). Each INT4 operation does half the numerical work. For vision models that need INT8 accuracy, the 26T's 26 INT8 TOPS outperforms the AI HAT+ 2's ~20 effective INT8 TOPS. See: The Key Tension.
</details>

**Q3:** Why does the AI HAT+ 2 need its own 8GB of RAM when the Pi 5 already has up to 8GB?
<details>
<summary>Answer</summary>
LLM weights (hundreds of MB) need to be streamed to the NPU continuously during token generation. On the original AI HAT+, this streams over the PCIe bus from the Pi's RAM, creating a bandwidth bottleneck. The AI HAT+ 2's on-board RAM holds the entire model next to the NPU, eliminating PCIe round-trips for weight access and freeing Pi RAM for other uses. See: How It Works — Data Flow: AI HAT+ 2.
</details>

**Q4:** "The AI HAT+ 2 can run a ChatGPT-quality assistant locally." What's wrong with this claim?
<details>
<summary>Answer</summary>
The 8GB RAM constrains models to ~1.5-2B parameters at INT4. Frontier LLMs use 70B-1T+ parameters — orders of magnitude larger. A 1.5B model produces basic responses with frequent errors and no nuanced reasoning. The AI HAT+ 2 is useful for structured, narrow tasks (intent classification, sensor parsing) but is not a general-purpose assistant. See: LLM Quality Ceiling.
</details>

**Q5:** You're designing a robot that needs to simultaneously run object detection at 15+ FPS, record video to an NVMe SSD, and serve a web dashboard. Can you use a Pi 5 + AI HAT+ for this? What's the architectural problem, and how would you solve it?
<details>
<summary>Answer</summary>
The Pi 5 has only one PCIe lane, so you must choose between the AI HAT (NPU acceleration) and an NVMe SSD (fast storage). You can't use both simultaneously. Solutions: (1) Use USB 3.0 storage instead of NVMe — slower but workable for video recording at moderate bitrates. (2) Use a Compute Module 5 with an I/O board that exposes multiple PCIe lanes. (3) Use the AI Camera (IMX500) for detection instead of an AI HAT — it doesn't use PCIe — and keep the PCIe lane for the NVMe SSD. (4) Use a Seeed Studio PCIe 3.0 Dual M.2 adapter with a PCIe switch — gives you two M.2 slots (NVMe + Hailo) on the single PCIe lane, at the cost of shared bandwidth. Each solution has tradeoffs in cost, performance, and complexity. See: The PCIe Exclusivity Problem and GPIO-Free Alternatives.
</details>

</details>
