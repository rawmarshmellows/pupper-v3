---
topic: CNC Machining
created: 2026-03-28
---

# CNC Machining

> **Related:** [[learning/notes/quick-context/3d-printing-filament-types|3D Printing Filament Types]] | [[learning/notes/quick-context/tensile-strength-materials|Tensile Strength Materials]] | [[learning/notes/quick-context/electrolysis|Electrolysis]] | [[learning/notes/quick-context/electrodes|Electrodes]]

> **TL;DR:** CNC machining is subtractive manufacturing -- a computer-controlled cutting tool removes material from a solid block to create precision parts. It is the default choice for metal parts at low volumes ($1$--$1{,}000$ units) where tight tolerances ($\pm 0.001"$) and full material strength are required.

## The Core Problem

You need a metal part with precise dimensions, smooth surfaces, and full material strength -- things 3D printing can't reliably deliver. But you only need a few hundred, so investing in injection mold tooling (which can cost tens of thousands of dollars) makes no sense. CNC machining fills this gap: it takes a solid block of material and carves away everything that isn't your part, using computer-controlled tools that follow instructions derived from your CAD model.

## 5 Essential Terms

| Term | Definition |
|------|-----------|
| **CNC Milling** | Rotating cutter removes material from a stationary workpiece. Tool spins at thousands of RPM; CNC moves it along X/Y/Z axes. Produces prismatic and complex 3D shapes. |
| **CNC Turning** | Lathe spins the workpiece while a stationary tool removes material. Inverse of milling. Produces cylindrical/rotationally symmetric parts (shafts, bolts, bushings). |
| **EDM** | Electrical Discharge Machining -- removes metal via rapid electrical sparks between an electrode and the workpiece, vaporizing material without mechanical contact. Cuts any conductive material regardless of hardness. |
| **G-code** | The instruction language CNC machines read. CAD model is converted into a sequence of tool movement commands specifying coordinates, feed rates, and spindle speeds. |
| **Tolerance** | The allowable deviation from a specified dimension. CNC routinely achieves $\pm 0.001"$ ($\pm 0.025\text{mm}$), far tighter than 3D printing or casting. |

<details>
<summary><strong>How It Works</strong></summary>

### The CNC Pipeline

CAD model $\rightarrow$ CAM software generates G-code $\rightarrow$ CNC controller drives servo/stepper motors $\rightarrow$ cutting tool removes material in successive passes $\rightarrow$ finished part.

### Milling: Tool Rotates, Part Stays Still

A rotating multi-edge cutter (end mill) is mounted in a motorized spindle. The CNC controller moves either the spindle or the workpiece table along X, Y, and Z axes. Each pass removes a thin layer of material as chips.

```
CNC MILLING OPERATION:

         Spindle (rotating)
              │
           ┌──┴──┐
           │▓▓▓▓▓│  ← Rotating end mill
           └──┬──┘
        chips ↓ ↓
    ══════════╧══════════  ← Workpiece (metal block)
    ══════════════════════
```

**Strengths:** Full material strength (no layer adhesion weakness like FDM), complex 3D geometries, tight tolerances.
**Limitations:** Wastes material as chips, can't create fully enclosed internal cavities.

### Turning: Part Rotates, Tool Stays Still

The workpiece is clamped in a rotating chuck that spins at high speed. A stationary cutting tool is fed into the spinning workpiece, shaving off material in a continuous spiral.

```
MILLING vs TURNING:

  MILLING                      TURNING (Lathe)
  ───────                      ───────────────
  Tool rotates                 Workpiece rotates
  Part stays still             Tool stays still

       ║                            ┌───────────┐
      ╔╩╗ ← Spinning               ◄│███████████│► Chuck grips
      ║░║   cutter                  │███████████│   and spins
      ╚═╝                           │███████████│   workpiece
  ─────────── Part                  └───────────┘
                                         ▲
                                    ═════╪═════ Tool carriage
                                         │       (moves along axis)
```

**Strengths:** Extremely smooth cylindrical surfaces, tight concentricity.
**Limitations:** Inherently limited to parts with rotational symmetry.

### EDM: Sparks Instead of Cutting

A shaped electrode is brought close to the conductive workpiece, separated by a thin gap filled with dielectric fluid. High-voltage pulses ionize the fluid, creating brief electrical sparks that vaporize tiny craters in the workpiece surface.

```
EDM SPARK EROSION:

      Electrode (shaped tool)
            │
            ▼
      ┌─────────┐
      │ ▓▓▓▓▓▓▓ │
      └────┬────┘
           │
     ~ ~ ~ ~ ~ ~ ~  ← Spark gap (~0.01-0.5mm)
           │           filled with dielectric fluid
     ┌─────┴─────┐
     │░░░░░░░░░░░│
     │░░ WORK ░░░│  ← Material vaporized
     │░░ PIECE ░░│    spark by spark
     │░░░░░░░░░░░│
     └───────────┘
```

**Strengths:** Cuts any conductive material regardless of hardness -- hardened steel is just as easy as soft aluminum. Can produce sharp internal corners that milling tools physically cannot reach.
**Limitations:** Slow, only works on conductive materials, leaves a characteristic surface texture.

### Subtractive vs Additive

```
SUBTRACTIVE (CNC):              ADDITIVE (3D Printing):

  ██████████████                      ░░░░
  ██████████████    ──────►       ░░░░░░░░░░
  ██████████████    cutting       ░░░░░░░░░░░░░░
  ██████████████                  ░░░░░░░░░░░░░░░░░░
  Solid block                       Built layer by layer

  Start with MORE material          Start with NO material
  and remove the excess             and add only what's needed
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

### CNC vs 3D Printing vs Casting/Molding

| Factor | CNC Machining | 3D Printing | Injection Molding / Casting |
|--------|--------------|-------------|---------------------------|
| **Volume** | 1--1,000 parts | 1--100 parts | 10,000+ parts |
| **Tolerance** | $\pm 0.001"$ | $\pm 0.005"$--$0.020"$ | $\pm 0.002"$--$0.005"$ |
| **Materials** | Metals, plastics, wood | Plastics, some metals | Metals, plastics |
| **Strength** | Full material strength | Layer adhesion weakness | Full (cast), full (molded) |
| **Internal cavities** | No (without multi-setup) | Yes | Yes (with cores) |
| **Tooling cost** | None (just G-code) | None (just STL) | High ($10K--$100K+ for molds) |
| **Surface finish** | Excellent | Moderate (layer lines) | Excellent |

### Process Selection Decision Tree

```
1. SHOULD YOU USE CNC AT ALL?

  Need tight tolerances (±0.001")?     ──► YES → CNC
  Metal part with full strength?       ──► YES → CNC
  Low volume (1-1000 parts)?           ──► YES → CNC
  Complex internals, no tool access?   ──► NO  → 3D print or casting
  High volume (10,000+)?               ──► NO  → Injection molding / casting

2. WHICH CNC PROCESS?

  Cylindrical?        Prismatic/complex?      Hard metal, sharp corners?
       │                     │                         │
       ▼                     ▼                         ▼
   TURNING              MILLING                      EDM
```

The fundamental tradeoff: CNC gives you precision and strength but wastes material and cannot create enclosed internal channels. 3D printing gives you geometric freedom but sacrifices strength and precision. Molding gives you everything at scale but demands enormous upfront tooling investment.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

### Making a Motor Shaft Assembly

Imagine you need to manufacture a custom motor shaft with a mounting bracket for a robotics project -- 50 units total.

**Step 1: The shaft (CNC Turning)**
The shaft is a cylindrical part with stepped diameters and a keyway. You start with a round bar of 4140 steel clamped in a lathe chuck. The CNC lathe spins it at 1,500 RPM while a carbide insert tool traverses along the axis, cutting each diameter step to $\pm 0.0005"$ concentricity. Turning is the obvious choice -- the part has rotational symmetry, and no other process matches turning's cylindrical surface finish.

**Step 2: The mounting bracket (CNC Milling)**
The bracket is a rectangular aluminum plate with bolt holes and a central bore. A 3-axis CNC mill holds the aluminum block on a vise, and an end mill cuts the outer profile, drills the bolt holes, and bores the central pocket. Milling handles the prismatic geometry and multiple hole patterns easily.

**Step 3: A hardened steel die insert (EDM)**
One component requires a square internal pocket with perfectly sharp corners in hardened D2 tool steel (62 HRC). An end mill would leave a radius in the corners (the tool is round), and the material is too hard for conventional cutting. A sinker EDM uses a square copper electrode to spark-erode the pocket, producing the sharp corners in the hardened steel that no rotating cutter could achieve.

**Why not 3D print?** The shaft needs concentricity and surface finish that metal 3D printing cannot match. The bracket needs full aluminum strength at bolt interfaces. At 50 units, CNC is cost-effective without tooling investment.

**Why not injection mold?** At 50 units, you would spend more on the mold than on all the parts combined.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- [[learning/notes/quick-context/3d-printing-filament-types|3D Printing Filament Types]] -- the additive manufacturing counterpart to CNC's subtractive approach
- [[learning/notes/quick-context/tensile-strength-materials|Tensile Strength Materials]] -- why CNC parts retain full material strength while 3D printed parts have layer adhesion weaknesses
- [[learning/notes/quick-context/electrolysis|Electrolysis]] -- the electrochemical principles behind EDM's spark erosion process
- [[learning/notes/quick-context/electrodes|Electrodes]] -- the shaped tool in EDM that transfers its geometry to the workpiece
- [[learning/notes/micro-context/cnc-milling|CNC Milling (micro)]] -- concise definition
- [[learning/notes/micro-context/cnc-turning|CNC Turning (micro)]] -- concise definition
- [[learning/notes/micro-context/cnc-process-selection|CNC Process Selection (micro)]] -- decision framework
- [[learning/notes/micro-context/edm-machining|EDM Machining (micro)]] -- concise definition

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

1. You need to make 200 aluminum brackets with $\pm 0.001"$ tolerances and complex pocket features. Which process do you choose, and why would you reject 3D printing and injection molding?

2. A part is a stepped cylindrical shaft with three different diameters. Should you mill it or turn it? What specific advantage does your choice have for this geometry?

3. You need a square hole with perfectly sharp internal corners in hardened tool steel (60 HRC). Why can't you mill this, and what process would you use instead?

4. Your client's order just changed from 500 units to 50,000 units of the same plastic part. How does this shift your manufacturing process recommendation, and why?

5. A designer hands you a part with a fully enclosed internal cooling channel (a tube-within-a-tube). Why is CNC machining fundamentally unable to produce this in a single setup, and what manufacturing method could?

</details>
