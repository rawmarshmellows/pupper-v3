---
topic: Melt Index (MFI/MFR)
created: 2026-01-20
updated: 2026-01-21
---

> **Related:** [[learning/notes/quick-context/fundamental-electronic-parts-index|Fundamental Electronic Parts — Index]]

> **TL;DR:** Melt Index (MFI/MFR) measures how easily a polymer flows when melted - grams extruded through a standard die in 10 minutes. Higher MFI means easier processing but weaker parts; lower MFI means tougher parts but harder to process. It's the universal handshake between resin suppliers and processors.

# Melt Index: Quick Context

## The Core Problem

Melt Index (MI), formally called **Melt Flow Index (MFI)** or **Melt Flow Rate (MFR)**, measures how easily a thermoplastic [[quick-context/atoms-molecules-polymers-basics|polymer]] flows when melted—specifically, how many grams of polymer extrude through a standardized die in 10 minutes under controlled temperature and load. Your value of **36.5 ± 2.6 g/10 min** indicates a relatively high-flow material (easy to process, lower viscosity). Without this metric, manufacturers would be flying blind: injection molding machines, extruders, and blow molding equipment all require precise viscosity matching. Too low an MI means incomplete mold filling, short shots, and excessive machine wear from fighting a sluggish melt. Too high means the material runs like water—poor mechanical properties, flash at mold seams, and dimensional instability. MI is the universal handshake between resin suppliers and processors; it determines whether a given polymer will actually work in your specific process and equipment.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **MFI/MFR (Melt Flow Index/Rate)** | Grams of polymer extruded in 10 minutes through a 2.095mm die at specified temperature and load (e.g., 190°C/2.16kg for polyethylene). |
| **Shear rate** | How fast polymer layers slide past each other during flow—real processing involves much higher shear than the MFI test, so MFI is only an approximation. |
| **Molecular weight distribution (MWD)** | The range of chain lengths in a polymer batch; two materials with identical MFI can behave differently if their MWD differs. |
| **Load (kg)** | The weight applied during testing (common: 2.16kg, 5kg, 21.6kg)—higher loads for stiffer materials; your result is meaningless without knowing the load used. |
| **ASTM D1238 / ISO 1133** | The standardized test methods defining exactly how MFI is measured—critical for comparing values across suppliers. |

<details>
<summary><strong>How It Works</strong></summary>

The MFI test uses a device called a **melt flow indexer** (or extrusion plastometer). A small sample of polymer pellets (typically 4-5 grams) is loaded into a heated barrel set to a standardized temperature—190°C for polyethylene and polypropylene, 220°C for ABS, and so on depending on the material standard. Once the polymer melts (usually after a 5-minute preheat), a weighted piston is placed on top, applying a standardized load (commonly 2.16 kg, 5 kg, or 21.6 kg). Gravity forces the piston down, pushing the molten polymer through a precision die with a 2.095 mm diameter opening.

The operator collects the extrudate that oozes out over a timed interval, typically cutting samples every 30 seconds to 1 minute. These "cuts" are weighed, and the mass is extrapolated to determine how many grams would extrude in 10 minutes. Higher MFI means the polymer flows more easily under the test conditions—shorter molecular chains slide past each other readily. Lower MFI indicates longer chains that tangle and resist flow, requiring more force or higher temperatures to process.

```
MELT FLOW INDEX TEST APPARATUS
==============================

        ┌───────────────┐
        │   PISTON      │  ← Standardized weight
        │   (2.16 kg)   │     (or 5 kg, 21.6 kg)
        └───────┬───────┘
                │
                ▼
    ┌───────────────────────┐
    │   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   │  ← Heated barrel
    │   ▒ MOLTEN POLYMER ▒   │     (190°C, 220°C, etc.)
    │   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   │
    │         │             │
    │    ┌────┴────┐        │
    │    │  DIE    │        │  ← Precision die
    │    │ 2.095mm │        │     (standardized diameter)
    │    └────┬────┘        │
    └─────────│─────────────┘
              │
              ▼
         ░░░░░░░░░░           ← Extrudate collected
         (cut every              and weighed
          30-60 sec)

INTERPRETATION SCALE
====================

MFI (g/10min)   │  Flow Behavior    │  Typical Application
────────────────┼───────────────────┼─────────────────────────
  < 1           │  Very stiff       │  Pipes, thick profiles
  1 - 10        │  Low flow         │  Blow molding, films
  10 - 25       │  Medium flow      │  General injection molding
  25 - 50       │  High flow        │  Thin-wall containers
  > 50          │  Very high flow   │  Ultra-thin packaging

Note: Same polymer, higher MFI = shorter chains = easier flow = weaker part
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The fundamental tradeoff is **processability vs. mechanical performance**. Higher MI polymers flow easily (faster cycle times, lower injection pressures, complex geometries possible) but have shorter molecular chains, meaning weaker [[quick-context/tensile-strength-materials|tensile strength]], lower impact resistance, and reduced chemical resistance. Lower MI materials are tougher and more durable but demand higher processing temperatures, pressures, and longer cycle times—increasing energy costs and equipment stress. Practitioners constantly argue about the "sweet spot": automotive engineers want low-MI for crash-worthy parts; packaging engineers want high-MI for thin-wall containers produced at high speed. The ± 2.6 tolerance in your spec reflects batch-to-batch variation—too wide a window and your process becomes unpredictable; too tight and you pay premium pricing for tighter quality control.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

A typical MFI test setup and how to interpret batch data:

```python
# Interpreting MFI batch data for quality control
# ASTM D1238 test: 190°C, 2.16 kg load (standard for HDPE/PP)

batch_results = [
    {"batch": "A-2024-001", "mfi": 35.2},
    {"batch": "A-2024-002", "mfi": 37.8},
    {"batch": "A-2024-003", "mfi": 36.1},
    {"batch": "A-2024-004", "mfi": 39.5},  # Outside spec!
]

spec_target = 36.5
spec_tolerance = 2.6  # ± tolerance
spec_min = spec_target - spec_tolerance  # 33.9
spec_max = spec_target + spec_tolerance  # 39.1

for batch in batch_results:
    status = "PASS" if spec_min <= batch["mfi"] <= spec_max else "FAIL"
    # Batch A-2024-004 fails: 39.5 > 39.1 upper limit
    print(f"{batch['batch']}: MFI={batch['mfi']:.1f} -> {status}")

# Output:
# A-2024-001: MFI=35.2 -> PASS
# A-2024-002: MFI=37.8 -> PASS
# A-2024-003: MFI=36.1 -> PASS
# A-2024-004: MFI=39.5 -> FAIL (reject batch or blend with lower-MFI material)
```

In practice, if batch A-2024-004 enters your injection molding process, you'd see flash at parting lines (material too runny) and possibly weaker parts from the degraded molecular weight.

**The one thing most outsiders get wrong about this is...** assuming MFI tells the whole story about how a polymer will behave in real processing. MFI is measured at extremely low shear rates (~1-10 s⁻¹), while injection molding operates at 1,000-100,000 s⁻¹. Polymers are shear-thinning, so their behavior under processing conditions can diverge dramatically from what MFI predicts. Two resins with identical MFI can perform completely differently in your mold—you need rheological curves (viscosity vs. shear rate) for serious process engineering, not just a single-point MFI number.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/glass-transition-temperature]]**: The temperature at which a polymer transitions from rigid/glassy to flexible/rubbery—MFI testing must occur well above this point for meaningful flow measurements.
- **[[quick-context/polymer-crystallinity-vs-amorphous]]**: Crystalline regions in a polymer melt more sharply and affect flow behavior; semi-crystalline polymers often show more dramatic MFI changes with temperature than amorphous ones.
- **[[quick-context/3d-printing-filament-types]]**: Different filament materials (PLA, ABS, PETG) have characteristic MFI ranges that determine optimal printing temperatures and speeds.
- **[[quick-context/3d-printer-hotends]]**: Hotend design must accommodate the viscosity (related to MFI) of target materials—all-metal hotends handle higher temperatures for low-MFI engineering polymers.
- **[[quick-context/tensile-strength-materials]]**: Higher MFI generally correlates with lower tensile strength due to shorter polymer chains—the fundamental processability vs. performance tradeoff.
- **[[quick-context/bambu-p2s-print-quality]]**: MFI variation between batches drives why per-spool flow ratio and pressure advance (K-value) calibration matters on the P2S—different MFI means different optimal extrusion settings.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A resin supplier offers two grades of polypropylene: Grade A with MFI 4 g/10min and Grade B with MFI 40 g/10min. Which would you choose for thin-wall food containers, and why?
<details>
<summary>Answer</summary>
Grade B (MFI 40). Thin-wall containers require the polymer to flow easily into fine features at high speeds. The higher MFI means lower viscosity, enabling faster cycle times and complete filling of thin sections. The tradeoff is reduced mechanical strength, but for disposable packaging, processability typically wins. See: The Key Tension.
</details>

**Q2:** Two HDPE resins both have MFI of 12 g/10min but behave differently in your injection mold. What property might explain this?
<details>
<summary>Answer</summary>
Molecular weight distribution (MWD). Two polymers can have identical average flow (same MFI) but different distributions of chain lengths. A broad MWD may have some very long chains that increase melt strength and elasticity, while a narrow MWD flows more predictably. MFI is a single-point measurement that masks these differences. See: 5 Essential Terms (MWD entry).
</details>

**Q3:** Why is it critical to know the test load (e.g., 2.16 kg vs. 21.6 kg) when comparing MFI values between suppliers?
<details>
<summary>Answer</summary>
MFI values are meaningless without the test conditions. A higher load forces more material through the die, yielding a higher MFI number for the same polymer. Comparing an MFI measured at 2.16 kg to one measured at 21.6 kg would be like comparing apples to oranges—the values are not interchangeable. Always confirm both temperature and load match ASTM D1238 or ISO 1133 conditions. See: 5 Essential Terms (Load entry).
</details>

**Q4:** Your MFI specification is 36.5 ± 2.6 g/10min. A batch tests at 39.5 g/10min. What processing problems might you expect if you use this material anyway?
<details>
<summary>Answer</summary>
The material is too fluid (exceeds the 39.1 upper limit). Expected problems include: flash at mold parting lines from material squeezing into gaps, dimensional instability as the part shrinks unpredictably, and potentially weaker mechanical properties from the degraded/shorter molecular chains causing the high MFI. See: Concrete Example.
</details>

**Q5:** Why can't you rely solely on MFI to predict how a polymer will perform in an injection mold operating at 10,000 s⁻¹ shear rate?
<details>
<summary>Answer</summary>
MFI is measured at very low shear rates (~1-10 s⁻¹), while real injection molding operates at 1,000-100,000 s⁻¹. Polymers are shear-thinning, meaning their viscosity decreases as shear rate increases—but this behavior varies by polymer. Two resins with identical MFI can have completely different viscosity curves at processing shear rates. For serious process engineering, you need full rheological data, not just a single-point MFI. See: The one thing most outsiders get wrong.
</details>

</details>
