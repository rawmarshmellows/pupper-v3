---
topic: Camera Fundamentals — Sensors, Lenses, and Calibration
created: 2026-03-23
---

# Camera Fundamentals — Sensors, Lenses, and Calibration

> **Related:** [[micro-context/spinev1-elf]] | [[quick-context/absolute-orientation]] | [[quick-context/ppo-proximal-policy-optimization]] | [[quick-context/preempt-rt]] | [[quick-context/preempt-rt-ros2-plc-replacement]]

> **TL;DR:** A camera converts photons into a 2D pixel array by focusing light through a lens onto a grid of [[quick-context/diode|photodiodes]] on a [[quick-context/silicon-die|silicon die]], where sensor size controls image quality tradeoffs, focal length determines field of view, dynamic range measures the brightest-to-darkest scene the sensor can capture, and the intrinsic/extrinsic calibration matrices describe how 3D world points map to 2D pixel coordinates.

## The Core Problem

Without understanding how cameras actually form images — the physics of sensors and lenses, and the math of projection — you cannot calibrate a vision system, correct for distortion, fuse camera data with other sensors, or reason about why an image looks the way it does. Every computer vision pipeline (from [[quick-context/pupper-lab7-vision-tracking|Pupper's object tracking]] to autonomous vehicles) depends on knowing the camera's intrinsic parameters (focal length, sensor size, distortion) and extrinsic parameters (where the camera is and which way it points). Get these wrong and your 3D reconstructions, distance estimates, and bounding box geometries will all be incorrect.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Image Sensor** | A [[quick-context/silicon-die|silicon die]] containing a 2D grid of millions of [[quick-context/diode\|photodiodes]] that convert incoming photons into electrical charge, which is then digitized into pixel values by on-chip [[micro-context/adc-analog-to-digital-converter\|ADCs]] |
| **Focal Length** | The distance (in mm) from the lens's optical center to the sensor when focused at infinity; determines magnification and, combined with sensor size, the field of view |
| **Sensor Format** | The physical dimensions of the image sensor (e.g., full frame = 36 x 24 mm, Micro Four Thirds = 17.3 x 13 mm); larger sensors collect more light per pixel and produce shallower depth of field |
| **Dynamic Range** | The ratio between the brightest and darkest light levels a sensor can capture in a single exposure, measured in stops (each stop = $2\times$ light) or decibels ($20 \log_{10}$ of voltage ratio) |
| **Intrinsic Matrix (K)** | A $3 \times 3$ upper-triangular matrix encoding the camera's internal geometry — focal lengths $f_x, f_y$ in pixel units, principal point $(c_x, c_y)$, and optionally skew — used to project 3D camera-frame points onto the 2D image plane |

<details>
<summary><strong>How It Works</strong> — From photon to pixel to 3D geometry</summary>

### Stage 1: Photon Capture (The Sensor)

An image sensor is a grid of tiny [[quick-context/diode|photodiodes]] — PN junctions operated in [[micro-context/reverse-and-forward-bias|reverse bias]]. When a photon strikes the [[quick-context/doped-silicon|silicon]], it knocks an electron free (photoelectric effect). The reverse-biased junction sweeps this electron into a charge well. More photons = more accumulated charge = brighter pixel.

```
FROM PHOTON TO PIXEL VALUE
================================================================

  PHOTON ARRIVES
       │
       ▼
  ┌─────────────────────────────────────────────────────────────┐
  │              PHOTODIODE (reverse-biased PN junction)        │
  │                                                             │
  │   Photon → knocks electron free → charge accumulates        │
  │                                                             │
  │   Exposure time = how long charge collects                  │
  │   ("shutter speed")                                         │
  └──────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                    READOUT CIRCUIT                          │
  │                                                             │
  │   Charge → voltage (amplifier) → digital number (ADC)       │
  │   10-bit ADC: 0-1023                                        │
  │   12-bit ADC: 0-4095                                        │
  │   14-bit ADC: 0-16383                                       │
  └──────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
                     PIXEL VALUE (e.g., 2847)


  SENSOR GRID (e.g., 4000 x 3000 = 12 megapixels)
  ┌───┬───┬───┬───┬───┬───┬───┐
  │ P │ P │ P │ P │ P │ P │ P │   Each P = one photodiode
  ├───┼───┼───┼───┼───┼───┼───┤   + color filter (Bayer pattern)
  │ P │ P │ P │ P │ P │ P │ P │   + microlens on top
  ├───┼───┼───┼───┼───┼───┼───┤
  │ P │ P │ P │ P │ P │ P │ P │   Typical pixel pitch: 1-8 μm
  ├───┼───┼───┼───┼───┼───┼───┤
  │ P │ P │ P │ P │ P │ P │ P │
  └───┴───┴───┴───┴───┴───┴───┘

  COLOR via BAYER FILTER (one color filter per pixel):
  ┌───┬───┬───┬───┐
  │ G │ R │ G │ R │   G = green, R = red, B = blue
  ├───┼───┼───┼───┤   50% green (eye is most sensitive)
  │ B │ G │ B │ G │   25% red, 25% blue
  ├───┼───┼───┼───┤
  │ G │ R │ G │ R │   Demosaicing algorithm interpolates
  ├───┼───┼───┼───┤   full RGB at every pixel from neighbors
  │ B │ G │ B │ G │
  └───┴───┴───┴───┘
```

### Stage 2: Sensor Size and Its Consequences

The physical dimensions of the sensor determine almost everything about image quality and lens behavior. "Full frame" (36 x 24 mm) is the reference standard, matching 35mm film.

```
SENSOR SIZE COMPARISON (to scale relative to full frame)
================================================================

  Full Frame (36 x 24 mm) — crop factor 1.0x
  ┌──────────────────────────────────────────────────┐
  │                                                  │
  │                                                  │
  │     APS-C (23.5 x 15.6 mm) — crop factor 1.5x    │
  │     ┌──────────────────────────────────┐         │
  │     │                                  │         │
  │     │   Micro 4/3 (17.3 x 13 mm)       │         │
  │     │   crop factor 2.0x               │         │
  │     │   ┌──────────────────────┐       │         │
  │     │   │                      │       │         │
  │     │   │  1-inch (13.2x8.8mm) │       │         │
  │     │   │  crop 2.7x           │       │         │
  │     │   │  ┌───────────┐       │       │         │
  │     │   │  │1/2.3"     │       │       │         │
  │     │   │  │(6.2x4.6mm)│       │       │         │
  │     │   │  │crop 5.6x  │       │       │         │
  │     │   │  └───────────┘       │       │         │
  │     │   └──────────────────────┘       │         │
  │     └──────────────────────────────────┘         │
  │                                                  │
  └──────────────────────────────────────────────────┘
```

| Format | Dimensions | Crop Factor | Typical Use |
|--------|-----------|-------------|-------------|
| **Full Frame** | 36 x 24 mm | 1.0x | Professional photo/video |
| **APS-C** | 23.5 x 15.6 mm | 1.5x (Nikon/Sony) or 1.6x (Canon) | Consumer/prosumer DSLRs |
| **Micro Four Thirds (MFT)** | 17.3 x 13 mm | 2.0x | Compact mirrorless (Panasonic, OM System) |
| **1-inch** | 13.2 x 8.8 mm | 2.7x | Premium compacts, drones (DJI) |
| **1/2.3-inch** | 6.2 x 4.6 mm | 5.6x | Smartphones, action cameras |

**Why size matters:** A larger sensor has larger pixels (or more of them). Larger pixels capture more photons before saturating, giving better signal-to-noise ratio — directly improving dynamic range and low-light performance. The [[quick-context/thermal-noise-electronics|thermal noise floor]] is roughly constant regardless of pixel size, so bigger pixels mean a better signal-to-noise ratio.

**Crop factor** describes how a smaller sensor "crops" the image compared to full frame. A 50 mm lens on a 2x crop sensor gives the same field of view as a 100 mm lens on full frame.

### Stage 3: Focal Length and Field of View

Focal length determines magnification. Combined with sensor size, it determines the angular field of view (FOV):

$$\text{FOV} = 2 \arctan\!\left(\frac{d}{2f}\right)$$

where $d$ is the sensor dimension (width or height) and $f$ is the focal length.

```
FOCAL LENGTH, SENSOR SIZE, AND FIELD OF VIEW
================================================================

  Same 50mm lens on different sensors:

  Full Frame (d = 36mm):     FOV = 2·arctan(36/(2·50)) = 39.6°
  APS-C (d = 23.5mm):       FOV = 2·arctan(23.5/(2·50)) = 26.5°
  MFT (d = 17.3mm):         FOV = 2·arctan(17.3/(2·50)) = 19.6°

  Smaller sensor → narrower FOV → equivalent to "zooming in"


  LENS FOCAL LENGTH EFFECT (on full frame):

  Wide (16mm)        Normal (50mm)       Telephoto (200mm)
  FOV ≈ 97°         FOV ≈ 40°          FOV ≈ 10°

  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  │  ╱        ╲  │   │              │   │              │
  │ ╱  wide    ╲ │   │   building   │   │  ┌────────┐  │
  │╱  landscape ╲│   │    front     │   │  │ window │  │
  │╲            ╱│   │              │   │  │ detail │  │
  │ ╲          ╱ │   │              │   │  └────────┘  │
  └──────────────┘   └──────────────┘   └──────────────┘
  Lots of scene       Natural view       Tight crop on
  visible                                distant detail


  THE THIN LENS MODEL:
  ================================================================

                    Optical
                     axis
         Object        │         Sensor
          ◄────────────┼────────────►
                       │
   ─ ─ ─ ─ ─ ─ ─ ─ ─╱─┼─╲─ ─ ─ ─ ─ ─ ─ ─ ─
   subject          ╱  │  ╲           image
   point  ─────────╱───┼───╲──────────●
          ─ ─ ─ ─╱─ ─ ─┼─ ─ ╲─ ─ ─ ─ ─ ─ ─ ─
                 ╱      │      ╲
                lens    │      sensor
                        │      plane
          │◄─── d_o ───►│◄─ f ─►│
          (object dist)  (focal length ≈ lens-to-sensor
                          when focused at infinity)

   Thin lens equation:  1/f = 1/d_o + 1/d_i
   where d_i = image distance (lens to sensor)
```

### Stage 4: Dynamic Range, Stops, and Decibels

#### What is a "stop"?

A **stop** is photography's universal unit for measuring light ratios. One stop equals exactly one **doubling** (or halving) of light. The term comes from the physical click-stops on a lens aperture ring — each click doubles or halves the light reaching the sensor. But stops apply far beyond aperture: they describe any factor-of-two change in exposure, whether from shutter speed, ISO, ND filters, or scene brightness.

The key insight is that stops are **logarithmic** — they compress huge brightness ratios into small, human-friendly numbers. The sun is roughly $2^{20}$ (about a million) times brighter than a dimly lit room, but in stops that's just "20 stops apart." Our eyes perceive brightness logarithmically too, which is why stops feel like even steps even though each one doubles the actual photon count.

```
WHAT "ONE STOP" MEANS ACROSS CAMERA CONTROLS
================================================================

  Every camera control that changes exposure by 1 stop
  doubles or halves the light reaching the sensor:

  APERTURE (f-number): controls lens opening area
  ─────────────────────────────────────────────────────────
  f/1.4 → f/2.0 → f/2.8 → f/4 → f/5.6 → f/8 → f/11 → f/16
     ←── each step = 1 stop less light ──→

  Why the weird numbers? Area of a circle = π·r².
  Halving the area means dividing the diameter by √2 ≈ 1.414.
  So each f-number is the previous × 1.414:
    f/1.4 × 1.414 = f/2.0 × 1.414 = f/2.8 × 1.414 = f/4 ...

  SHUTTER SPEED: controls exposure time
  ─────────────────────────────────────────────────────────
  1/30s → 1/60s → 1/125s → 1/250s → 1/500s → 1/1000s
     ←── each step = 1 stop less light ──→

  Straightforward: half the time = half the photons.

  ISO (sensor gain): amplifies the signal electronically
  ─────────────────────────────────────────────────────────
  ISO 100 → 200 → 400 → 800 → 1600 → 3200 → 6400
     ←── each step = 1 stop more sensitivity ──→

  Doubling ISO doubles the signal, but also amplifies noise.
  This is why high-ISO images look grainy.


  THE EXPOSURE TRIANGLE:
  ─────────────────────────────────────────────────────────

  These three controls trade off against each other.
  Adding 1 stop of aperture = removing 1 stop of shutter speed
  if you want the same total exposure:

  "Same exposure" examples (all produce identical brightness):
    f/2.8,  1/500s,  ISO 100
    f/4.0,  1/250s,  ISO 100    (+1 stop aperture, -1 stop shutter)
    f/4.0,  1/500s,  ISO 200    (+1 stop aperture, +1 stop ISO)
    f/5.6,  1/125s,  ISO 100    (+2 stop aperture, -2 stop shutter)
```

Because stops are base-2 logarithms, $n$ stops = $2^n$ linear ratio:

| Stops | Linear Ratio | Intuition |
|-------|-------------|-----------|
| 1 | 2:1 | One click on the aperture ring |
| 2 | 4:1 | Twice as bright as "one stop brighter" |
| 3 | 8:1 | Indoor lamp vs. candle |
| 10 | 1,024:1 | ~bright overcast vs. moonlit night |
| 14 | 16,384:1 | Range of a good full-frame sensor |
| 20 | 1,048,576:1 | Range of human vision with adaptation |

#### Dynamic range

Dynamic range is the ratio between the maximum signal a pixel can hold (full well capacity) and the minimum detectable signal (noise floor, dominated by [[quick-context/thermal-noise-electronics|thermal noise]] and read noise):

$$\text{DR (stops)} = \log_2\!\left(\frac{\text{full well capacity}}{\text{noise floor (electrons)}}\right)$$

$$\text{DR (dB)} = 20 \log_{10}\!\left(\frac{V_{\text{max}}}{V_{\text{noise}}}\right)$$

```
DYNAMIC RANGE — WHY IT MATTERS
================================================================

  SCENE: sunlit window + dark room interior

  ┌──────────────────────────────────────────────────┐
  │                       ┌─────────────────────┐    │
  │   DARK INTERIOR       │  BRIGHT WINDOW      │    │
  │   ~10 lux             │  ~100,000 lux       │    │
  │                       │  (direct sunlight)  │    │
  │   furniture barely    │                     │    │
  │   visible to eye      │  sky and clouds     │    │
  │                       └─────────────────────┘    │
  └──────────────────────────────────────────────────┘

  Brightness ratio: 100,000 / 10 = 10,000:1
  In stops: log2(10,000) ≈ 13.3 stops needed
  In dB: 20·log10(10,000) = 80 dB needed

  Human eye:     ~20 stops (with adaptation)
  Cinema camera: ~14-17 stops (ARRI Alexa; Alexa 35 reaches 17)
  Full frame:    ~13-15 stops (Sony A7 series)
  Smartphone:    ~10-11 stops (compensated with HDR stacking)
  Webcam:        ~8-9 stops


  CONVERSION BETWEEN UNITS:
  ┌───────────┬───────────┬──────────────┐
  │ Stops     │ dB        │ Linear Ratio │
  ├───────────┼───────────┼──────────────┤
  │ 1 stop    │ 6.02 dB   │ 2:1          │
  │ 3 stops   │ 18.1 dB   │ 8:1          │
  │ 6 stops   │ 36.1 dB   │ 64:1         │
  │ 10 stops  │ 60.2 dB   │ 1024:1       │
  │ 13 stops  │ 78.3 dB   │ 8192:1       │
  │ 14 stops  │ 84.3 dB   │ 16384:1      │
  └───────────┴───────────┴──────────────┘

  1 stop = doubling of light = 6.02 dB
  (because 20·log10(2) ≈ 6.02)
```

### Stage 5: Camera Calibration — Intrinsic and Extrinsic Parameters

Every camera maps 3D world points to 2D pixel coordinates. This projection is described by two sets of parameters.

**Intrinsic parameters** describe the camera's internal optics — how the camera's own coordinate frame maps to pixel coordinates:

$$K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}$$

where $f_x, f_y$ are focal lengths in pixel units ($f_x = f_{\text{mm}} \times \text{pixels\_per\_mm}$) and $(c_x, c_y)$ is the principal point (ideally image center).

**Extrinsic parameters** describe the camera's pose in the world — a rotation $R$ and translation $\mathbf{t}$ that form a [[micro-context/homogeneous-transformation-matrix|homogeneous transformation matrix]] converting world-frame coordinates to camera-frame coordinates:

$$\begin{bmatrix} R & \mathbf{t} \\ \mathbf{0} & 1 \end{bmatrix} \in \mathbb{R}^{4 \times 4}$$

This is the same transformation matrix framework used in [[quick-context/pupper-lab2-forward-kinematics|robot forward kinematics]] — the math of chaining coordinate frames is identical.

```
THE FULL PROJECTION PIPELINE
================================================================

   3D WORLD POINT              CAMERA FRAME              2D PIXEL
   P_world = (X, Y, Z)    →   P_cam = (x, y, z)    →   p = (u, v)

   Step 1: EXTRINSIC              Step 2: INTRINSIC
   (where is the camera?)         (how does the camera "see"?)

   ┌         ┐   ┌     ┐         ┌             ┐   ┌       ┐
   │ R  | t  │   │  X  │         │ fx  0  cx   │   │ x/z   │
   │ ───┼─── │ · │  Y  │   →     │ 0  fy  cy   │ · │ y/z   │
   │ 0  | 1  │   │  Z  │         │ 0   0   1   │   │  1    │
   └         ┘   │  1  │         └             ┘   └       ┘
                  └     ┘
   [Extrinsic 4x4]  [World]      [Intrinsic 3x3]  [Normalized]
                                                    ↓
                                              pixel (u, v)

   Combined:  p = K · [R | t] · P_world

   This single equation is the foundation of ALL camera geometry:
   - Stereo vision (two cameras → depth)
   - Visual SLAM (camera motion → 3D map)
   - AR overlays (place virtual objects in real scenes)
   - Fisheye undistortion (Pupper Lab 7 uses this)


  DISTORTION (added to intrinsic model):
  ================================================================

  Real lenses aren't perfect thin lenses. They introduce distortion:

  Undistorted grid:       Barrel distortion:       Pincushion:
  ┌──┬──┬──┬──┐          ┌──┬──┬──┬──┐           ┌──┬──┬──┬──┐
  │  │  │  │  │          │╲ │╲ │╱ │╱ │           │╱ │╱ │╲ │╲ │
  ├──┼──┼──┼──┤          ├──┼──┼──┼──┤           ├──┼──┼──┼──┤
  │  │  │  │  │          │╲ │  │  │╱ │           │╱ │  │  │╲ │
  ├──┼──┼──┼──┤          ├──┼──┼──┼──┤           ├──┼──┼──┼──┤
  │  │  │  │  │          │╱ │  │  │╲ │           │╲ │  │  │╱ │
  ├──┼──┼──┼──┤          ├──┼──┼──┼──┤           ├──┼──┼──┼──┤
  │  │  │  │  │          │╱ │╱ │╲ │╲ │           │╲ │╲ │╱ │╱ │
  └──┴──┴──┴──┘          └──┴──┴──┴──┘           └──┴──┴──┴──┘

  Wide-angle and fisheye lenses have severe barrel distortion.
  Modeled by radial distortion coefficients (k1, k2, k3...)
  and tangential coefficients (p1, p2).

  OpenCV calibration estimates K + distortion coefficients
  from checkerboard images, then undistorts frames in real time.
```

</details>

<details>
<summary><strong>The Key Tension</strong> — Sensor size vs. everything else</summary>

The central tradeoff in camera design is the **iron triangle of sensor size, resolution, and pixel size**. You can only pick two:

| Goal | Requires | Sacrifices |
|------|----------|-----------|
| More megapixels on same sensor | Smaller pixels | Low-light performance, dynamic range |
| Better low-light (larger pixels) | Larger sensor OR fewer pixels | Cost, lens size, weight |
| Compact system (small sensor) | Small pixels | Dynamic range, depth of field control |
| Wide dynamic range | Large pixels with deep wells | Resolution per mm of sensor |

```
THE PIXEL SIZE TRADEOFF
================================================================

  Same 24 MP sensor, two different sizes:

  FULL FRAME (36 x 24 mm):         SMARTPHONE (6.2 x 4.6 mm):
  Pixel pitch: ~5.9 μm             Pixel pitch: ~1.0 μm

  Full-well capacity: ~50,000 e⁻   Full-well capacity: ~4,000 e⁻
  Read noise:         ~3 e⁻        Read noise:         ~2 e⁻
  DR: log2(50000/3) = 14.0 stops   DR: log2(4000/2) = 11.0 stops

  3 stops difference = 8x more light range on full frame!

  ┌─────────────────┐   ┌──┐
  │                 │   │  │  ← Smartphone pixel:
  │  Full frame     │   └──┘    ~35x less area
  │  pixel          │           ~35x fewer photons
  │                 │           collected per exposure
  │                 │
  └─────────────────┘
  ~5.9 μm                ~1.0 μm
```

**Depth of field** is also sensor-size-dependent. For the same field of view and aperture, a larger sensor requires a longer focal length, which produces shallower depth of field. This is why full-frame cameras produce that "blurry background" (bokeh) look that smartphones simulate computationally.

**Robotics tradeoff:** In robotics (like the Pupper), small sensors with wide-angle or fisheye lenses are preferred — they're lightweight, cheap, and provide maximum FOV for obstacle detection. The cost is lower dynamic range and more distortion, which must be corrected using the distortion coefficients estimated during calibration.

</details>

<details>
<summary><strong>Concrete Example</strong> — Calibrating a camera with OpenCV</summary>

Here's how the Pupper's fisheye camera gets calibrated, estimating intrinsic matrix $K$ and distortion coefficients from checkerboard images:

```python
import numpy as np
import cv2

# 1. Prepare known 3D points of the checkerboard corners
#    (the board defines the world coordinate system)
board_size = (9, 6)  # inner corners
square_size = 0.025  # 25mm squares

obj_points = np.zeros((board_size[0] * board_size[1], 3), np.float32)
obj_points[:, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)
obj_points *= square_size  # scale to meters

# 2. Collect corresponding 2D pixel coordinates from multiple images
all_obj_pts = []  # 3D points (same for every image)
all_img_pts = []  # 2D detected corners (different per image)

for img_path in calibration_images:
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    found, corners = cv2.findChessboardCorners(gray, board_size)
    if found:
        # Sub-pixel refinement for accuracy
        corners = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1),
            criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        )
        all_obj_pts.append(obj_points)
        all_img_pts.append(corners)

# 3. Calibrate: estimate K (intrinsic) and distortion coefficients
#    For standard lens:
ret, K, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    all_obj_pts, all_img_pts, gray.shape[::-1], None, None
)

# K is the 3x3 intrinsic matrix:
# [[fx,  0, cx],
#  [ 0, fy, cy],
#  [ 0,  0,  1]]
#
# dist_coeffs = [k1, k2, p1, p2, k3] (radial + tangential)
#
# rvecs, tvecs = rotation and translation per image
#   (extrinsic parameters — camera pose relative to each checkerboard)

print(f"Focal length: fx={K[0,0]:.1f}, fy={K[1,1]:.1f} pixels")
print(f"Principal point: cx={K[0,2]:.1f}, cy={K[1,2]:.1f}")
print(f"Distortion: {dist_coeffs.ravel()}")

# 4. Undistort images using the calibration
undistorted = cv2.undistort(img, K, dist_coeffs)

# For fisheye (as in Pupper Lab 7):
# ret, K, D, rvecs, tvecs = cv2.fisheye.calibrate(...)
# undistorted = cv2.fisheye.undistortImage(img, K, D)
```

### What the output means:

```
CALIBRATION RESULTS (example Pupper fisheye camera):
================================================================

  Intrinsic matrix K:
  ┌                          ┐
  │ 325.4    0    353.2      │   fx = 325.4 px (focal length)
  │   0    326.1  248.7      │   fy = 326.1 px
  │   0      0      1       │   cx, cy = principal point
  └                          ┘

  Distortion coefficients D (fisheye model):
  k1 = -0.042,  k2 = 0.003,  k3 = -0.001,  k4 = 0.000

  Per-image extrinsics (one checkerboard pose):
  rvec = [0.12, -0.34, 0.02]    (rotation as Rodrigues vector)
  tvec = [0.15, 0.08, 0.45]     (translation in meters)

  These rvec/tvec pairs tell you WHERE the camera was relative
  to the checkerboard for each calibration image.
```

### Project a 3D point to pixel coordinates:

```python
# Given: 3D point in world frame, camera K, R, t
P_world = np.array([0.5, 0.3, 2.0, 1.0])  # [X, Y, Z, 1]

# Extrinsic: world → camera frame
R, _ = cv2.Rodrigues(rvec)  # 3x3 rotation from Rodrigues
T_ext = np.hstack([R, tvec.reshape(3, 1)])  # [R|t] = 3x4

# Project: pixel = K @ [R|t] @ P_world
p_homogeneous = K @ T_ext @ P_world  # [u*w, v*w, w]
u = p_homogeneous[0] / p_homogeneous[2]  # pixel x
v = p_homogeneous[1] / p_homogeneous[2]  # pixel y
```

**The one thing most outsiders get wrong about this is...** thinking "focal length" is a fixed physical property that determines field of view by itself. It isn't — FOV depends on *both* focal length and sensor size. A 25 mm lens on Micro Four Thirds gives the same FOV as a 50 mm lens on full frame, because the MFT sensor is half the size. This is why "crop factor" exists: it converts focal lengths between sensor formats to give equivalent fields of view. When someone says a phone camera has a "26 mm equivalent" lens, the actual glass is ~4-5 mm — the "26 mm" refers to what focal length on a full-frame camera would give the same FOV.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[quick-context/pupper-lab7-vision-tracking]]** — Applies camera fundamentals directly: the Pupper's fisheye camera requires intrinsic calibration (K and distortion coefficients D) to undistort frames before running YOLOv5 object detection. The `cv2.fisheye.undistortImage()` call uses exactly the intrinsic parameters described here.

- **[[quick-context/diode]]** — A photodiode is a specialized PN junction operated in reverse bias, where incident photons generate current proportional to light intensity. Every pixel on an image sensor is fundamentally a photodiode. The diode document's type table lists photodiodes as a key variant.

- **[[micro-context/homogeneous-transformation-matrix]]** — The extrinsic matrix $[R|\mathbf{t}]$ is a homogeneous transformation — the same $4 \times 4$ matrix used in [[quick-context/pupper-lab2-forward-kinematics|robot kinematics]]. Camera pose estimation and robot forward kinematics use identical math.

- **[[micro-context/adc-analog-to-digital-converter]]** — Each pixel's accumulated charge is converted to a digital number by an on-chip ADC. The ADC bit depth (10, 12, 14-bit) directly determines the quantization of dynamic range. A 14-bit ADC provides 16,384 levels, enabling ~14 stops of dynamic range if the noise floor is low enough.

- **[[quick-context/thermal-noise-electronics]]** — The noise floor that limits dynamic range is dominated by thermal noise (Johnson-Nyquist noise in the readout circuit) and shot noise (statistical variation in photon arrival). The Nyquist formula $V_n = \sqrt{4kTR\Delta f}$ directly predicts the minimum detectable signal in the sensor's readout amplifier.

- **[[quick-context/silicon-die]]** — An image sensor IS a silicon die — a CMOS sensor is fabricated using the same [[quick-context/semiconductor-fabrication|semiconductor fabrication]] process as CPUs, with photodiodes, readout transistors, and ADCs all integrated on a single die.

- **Stereo Vision** — Two calibrated cameras with known extrinsic relationship can triangulate 3D depth. Requires accurate intrinsic calibration of both cameras and precise measurement of the baseline (distance between them).

- **SLAM (Simultaneous Localization and Mapping)** — Uses camera intrinsics to convert pixel observations into 3D geometry, and estimates extrinsic parameters (camera pose) on the fly as the camera moves through an unknown environment.

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** A photodiode in an image sensor is operated in reverse bias. Why reverse bias instead of forward bias, and how does incident light generate a signal?
<details>
<summary>Answer</summary>
In reverse bias, the depletion zone is wide and the junction has a strong electric field but essentially no current. When a photon is absorbed in the silicon, it generates an electron-hole pair. The depletion zone's electric field sweeps this carrier across the junction, creating a photocurrent proportional to light intensity. Forward bias wouldn't work because the large forward current would swamp the tiny photocurrent — you need the "quiet" state of reverse bias so that the only current is from incident photons. See: How It Works, Stage 1 and [[micro-context/reverse-and-forward-bias]].
</details>

**Q2:** A 50 mm lens gives a 40 degree horizontal FOV on full frame. What FOV does the same lens give on a Micro Four Thirds sensor, and why?
<details>
<summary>Answer</summary>
MFT has a 2.0x crop factor, so the sensor width is half that of full frame (17.3 mm vs 36 mm). Using $\text{FOV} = 2\arctan(d/2f)$: $\text{FOV} = 2\arctan(17.3/100) = 2\arctan(0.173) \approx 19.6°$. The FOV is roughly halved because the smaller sensor only captures the central portion of the image circle. The lens projects the same image — the smaller sensor just crops it. See: How It Works, Stage 3.
</details>

**Q3:** A camera sensor has a full-well capacity of 30,000 electrons and a read noise of 5 electrons. What is its dynamic range in stops and in dB?
<details>
<summary>Answer</summary>
$\text{DR (stops)} = \log_2(30000/5) = \log_2(6000) \approx 12.6 \text{ stops}$. In dB: $12.6 \times 6.02 \approx 75.8 \text{ dB}$ (or equivalently, $20\log_{10}(6000) \approx 75.6 \text{ dB}$). This is typical of a good APS-C or Micro Four Thirds sensor. See: How It Works, Stage 4.
</details>

**Q4:** Someone claims: "You don't need to calibrate the camera — just use the focal length printed on the lens." What's wrong with this?
<details>
<summary>Answer</summary>
The printed focal length is the physical focal length in mm, but the intrinsic matrix $K$ needs focal length in **pixel units** ($f_x = f_{\text{mm}} \times \text{pixels/mm}$), which depends on pixel pitch — a quantity not printed on the lens. Worse, the printed focal length is nominal and may not be exact, the principal point is rarely exactly at image center, and — most critically — the intrinsic model must also include **distortion coefficients** (radial and tangential) that are unique to each individual lens specimen. Calibration using a known pattern (checkerboard) estimates all of these simultaneously from observed data. See: Concrete Example.
</details>

**Q5:** The extrinsic matrix converts world-frame points to camera-frame points, and the intrinsic matrix projects camera-frame points to pixels. This is the same [[micro-context/homogeneous-transformation-matrix|homogeneous transformation]] framework used in [[quick-context/pupper-lab2-forward-kinematics|Pupper's forward kinematics]]. If you mounted a camera on the Pupper's body at a known position and orientation, how would you combine the robot's FK chain with the camera calibration to project a 3D point in the foot's coordinate frame onto the camera's pixel coordinates?
<details>
<summary>Answer</summary>
You would chain transformations: (1) Use FK to compute $T_{\text{body} \leftarrow \text{foot}}$ — the 4x4 transform from foot frame to body frame (this is exactly what Lab 2 computes). (2) Use the known camera mount to get $T_{\text{cam} \leftarrow \text{body}}$ — the 4x4 transform from body frame to camera frame (from the camera's extrinsic calibration relative to the body). (3) Chain them: $P_{\text{cam}} = T_{\text{cam} \leftarrow \text{body}} \cdot T_{\text{body} \leftarrow \text{foot}} \cdot P_{\text{foot}}$. (4) Project to pixels: $p = K \cdot [I | \mathbf{0}] \cdot P_{\text{cam}}$ (intrinsic projection). The key insight is that both the FK chain and the camera extrinsic are homogeneous transforms — they compose by matrix multiplication. This is exactly how visual servoing works: you close the loop between robot kinematics and camera projection to align the robot with visual targets.
</details>

</details>
