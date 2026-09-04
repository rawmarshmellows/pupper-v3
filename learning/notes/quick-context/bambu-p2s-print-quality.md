---
topic: Bambu P2S Print Quality
created: 2026-04-29
---

# Bambu P2S Print Quality

> **Related:** [[learning/notes/quick-context/covalent-bonds]] | [[learning/notes/quick-context/dipole-dipole-interactions]] | [[learning/notes/quick-context/glass-transition-temperature]] | [[learning/notes/quick-context/melt-index]]

> **TL;DR:** The single highest-leverage move for P2S print quality is **per-filament calibration** (Flow Dynamics K-value + Flow Rate), followed by tuning **outer-wall mechanics** (slow outer wall ≤50 mm/s, accel 3000–5000 mm/s², outer-before-inner wall order). Hardware (PMSM servo extruder, Adaptive Airflow, hardened steel nozzle) does the rest if the filament is dry and the plate is clean.

## The Core Problem

The P2S ships with strong defaults but every spool of filament has slightly different melt behavior, moisture content, and friction. Without calibration, you fight ghosting, bulging corners, stringing, and weak layer adhesion no matter how good the printer is. The fix is mostly software (calibrate per filament, slow the visible surface, aggressive cooling) plus moisture control.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Flow Dynamics (K-value)** | Pressure advance — predicts nozzle pressure lag when speed changes; kills bulged corners and blobs at line ends. |
| **Flow Ratio** | Per-filament extrusion multiplier — fixes over/under-extrusion streaks; calibrate after K-value. |
| **Input Shaping** | Vibration compensation that cancels mechanical resonance frequencies — eliminates ringing/ghosting on outer walls. |
| **DynaSense (PMSM servo extruder)** | P2S's permanent-magnet servo extruder — ~70% more force than P1S stepper, detects grinding/clogs in real time. |
| **Adaptive Airflow** | Active flap system that pulls outside cool air for overhangs, seals chamber heat for engineering filaments. |

<details>
<summary><strong>How It Works</strong> — Highest-leverage knobs, ranked</summary>

Print quality on the P2S is a stack. Each layer below depends on the one above being correct.

```
P2S PRINT QUALITY STACK (top = highest leverage)
═══════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────┐
│  1. DRY FILAMENT                                            │
│     Wet filament = popping, stringing, weak layers.         │
│     PLA 45°C / 6–8h, PETG 65°C / ~7h,                       │
│     PA-CF 80°C / 8–12h, raw Nylon 95°C / ~7h.               │
│     AMS 2 Pro active venting dries 30% faster than sealed.  │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  2. CLEAN PLATE + Z-OFFSET                                  │
│     Anhydrous (>99%) IPA wipe before every print.           │
│     P2S factory Z-offset = 0.01 (most printers ≈ -0.04).    │
│     If first layer too high → drop Z-offset.                │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  3. PER-FILAMENT CALIBRATION (the big one)                  │
│                                                             │
│     Step A: Flow Dynamics (K-value)  ← do FIRST             │
│         Pick K where corners are sharp, no bulging,         │
│         no gap at line ends.                                │
│                                                             │
│     Step B: Flow Rate (flow ratio)   ← do SECOND            │
│         Pick value where top surface is smooth,             │
│         no ridges (over) or gaps (under).                   │
│                                                             │
│     Save both into a custom filament preset.                │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  4. OUTER-WALL MECHANICS (what you SEE)                     │
│     • Outer wall speed:  ≤ 50 mm/s                          │
│     • Outer wall accel:  3000–5000 mm/s²                    │
│     • Wall order:  Outer / Inner  (outer printed first)     │
│     Inner walls + infill stay fast — no time penalty.       │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  5. COOLING (overhangs + small features)                    │
│     • Overhang cooling threshold: 25%                       │
│     • Adaptive Airflow ON for PLA/PETG overhangs            │
│     • Reduce min layer time for tiny parts                  │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  6. MECHANICAL HEALTH (only if ringing returns)             │
│     • Re-tension belts (X & Y)                              │
│     • Re-run Vibration Compensation                         │
│     • Check rod lubrication                                 │
└─────────────────────────────────────────────────────────────┘
```

**Why ordering matters:** calibrating K-value on wet filament gives the wrong K. Tuning outer-wall speed before fixing flow ratio just hides the symptom. Always work top-down.

**Why outer-wall first beats just "print slow":** the outer wall is the only line a human sees. Slowing it from 200 → 50 mm/s on a 1mm-thick shell adds maybe 10% to total time but removes nearly all ghosting and ringing because the visible perimeter no longer excites resonance. Inner walls + infill stay at full P2S speed (600 mm/s capable, 20,000 mm/s² accel).

**Why P2S wall order = Outer/Inner:** when outer prints first, no extrusion pressure pushes against the visible surface. Default Inner/Outer pushes the fresh outer wall outward → slight bulge, blurred sharp edges.

</details>

<details>
<summary><strong>The Science Behind It</strong> — Polymer chemistry & physics for every knob</summary>

Every print-quality lever maps to a real physical or chemical mechanism. Understanding the science tells you *why* a setting matters and *when* a workaround will or won't work.

### 1. Why drying matters — hydrolysis + steam explosions

Filaments are [[learning/notes/quick-context/atoms-molecules-polymers-basics|polymers]] — long chains of repeating monomer units held together by [[learning/notes/quick-context/covalent-bonds|covalent bonds]] within each chain and intermolecular forces between chains. Many of those intermolecular forces are [[learning/notes/quick-context/hydrogen-bonds-beginners|hydrogen bonds]] or [[learning/notes/quick-context/dipole-dipole-interactions|dipole-dipole interactions]]. Water (H₂O) is highly polar and forms strong hydrogen bonds with any polymer that has C=O, N-H, or O-H groups exposed.

| Filament | Polar groups | Hygroscopic? | Why |
|----------|--------------|--------------|-----|
| **PLA** | Ester (–COO–) | Mild | Few H-bond acceptors |
| **PETG** | Ester + glycol | Moderate | More polar groups |
| **ABS** | Nitrile (–CN) | Low | Mostly non-polar backbone |
| **PA / Nylon** | Amide (–CO–NH–) | Severe | Amide group is a near-perfect H-bond donor *and* acceptor — like a sponge for water |
| **PC** | Carbonate ester | High | Hydrolyzes catastrophically when wet |

Two failure modes when wet filament hits the 200–280°C melt zone:
1. **Steam explosion.** Trapped H₂O flashes to vapor at >100°C → micro-bubbles in the extruded bead → popping sound, pockmarked surface, weak layer bonds.
2. **Hydrolysis.** Water attacks the ester or amide bond and breaks the polymer chain. Shorter chains = lower viscosity, weaker tensile strength, brittle parts. PETG, PC, and PA are most vulnerable. The damage is **permanent** — drying afterward removes water but cannot rejoin broken chains.

This is why nylon needs 95°C / 7h while PLA only needs 45°C / 6h. The amide groups in nylon trap water *between* chains via H-bonds; you must heat above the H-bond rupture energy to evict it.

### 2. Why pressure advance (K-value) exists — viscoelasticity

Molten plastic isn't a simple fluid. It's **viscoelastic**: it both flows (viscous) and stretches like a rubber band (elastic). When the toolhead accelerates, the extruder pushes filament harder, but the molten column inside the [[learning/notes/quick-context/3d-printer-hotends|hotend]] compresses like a spring before the bead emerges. When the toolhead decelerates, that stored elastic energy keeps pushing plastic out — even after the extruder stops feeding.

Result without compensation:
- **At line ends (decel):** blob, because pressure keeps oozing.
- **At line starts (accel):** thin or missing line, because pressure hasn't built yet.
- **At corners:** outward bulge, because tangential velocity drops but pressure lags.

Pressure advance (K-value) **predicts** how much pressure will build at a given speed and pre-adjusts the extruder ahead of time — extra push during accel, retract during decel.

The right K depends on the polymer's [[learning/notes/quick-context/melt-index|melt index]] and chain entanglement. Higher melt index (longer chains, more entanglement) → more elastic memory → higher K. Lower melt index → less elasticity → lower K. This is why every filament needs its own K — the polymer's molecular architecture dictates it.

### 3. Why flow ratio drifts per spool — density, fillers, molecular weight

Flow ratio is the slicer's "how much filament to push per mm of toolpath." Three molecular reasons it varies:
- **Pigment loading.** Black PLA often has 1–3% carbon black; matte PLA has glass beads or chalk. These fillers displace polymer volume but don't melt — they raise the *effective* viscosity and reduce volumetric output per gram fed.
- **Molecular weight distribution.** Different production batches have slightly different chain-length distributions, which changes [[learning/notes/quick-context/melt-index|melt index]] and therefore flow at the same temperature.
- **Diameter tolerance.** "1.75 mm" filament is really 1.70–1.80 mm. The extruder feeds by length but the slicer assumes nominal diameter. A 1.78 mm spool delivers 3.4% more cross-section than 1.75 mm.

Calibration zeroes out all three sources at once.

### 4. Why cooling matters — glass transition + crystallization

A freshly extruded bead is above the polymer's [[learning/notes/quick-context/glass-transition-temperature|glass transition temperature (Tg)]] — chains are mobile and the bead deforms under the next layer's weight. The fan must drag the bead below Tg before that next layer arrives, otherwise overhangs droop and bridges sag.

But cooling too fast on [[learning/notes/quick-context/polymer-crystallinity-vs-amorphous|semi-crystalline polymers]] (PA, PP, PE) prevents proper crystal formation and reduces interlayer adhesion — the chains "freeze" before they can tangle across the layer boundary. This is why:
- **PLA** (mostly amorphous): blast it with 100% fan — overhangs love it, layer adhesion fine.
- **PETG** (slow-crystallizing): 30–50% fan — full fan weakens layers.
- **ABS / PA**: minimal fan — needs slow cooling for crystallinity and warp control. **Enclose the chamber.** This is exactly what the P2S Adaptive Airflow seals shut for engineering filaments.

### 5. Why layer adhesion needs heat — polymer interdiffusion

Two layers don't bond by glue or melt-fusion alone. Adjacent chains must **interdiffuse** — wiggle into each other's territory and form fresh van der Waals + [[learning/notes/quick-context/hydrogen-bonds-beginners|hydrogen bonds]] across the boundary. Interdiffusion only happens above Tg, and its rate scales with $\sqrt{t}$ (square root of time spent above Tg).

Practical consequences:
- Tall thin towers (each layer cools too fast) → weak layers.
- Print fast → less time above Tg → less interdiffusion → can be peeled apart.
- Enclosed chamber keeps lower layers warmer → better interdiffusion → stronger parts.

### 6. Why outer-wall speed/accel matters — mechanical resonance, not chemistry

Ringing/ghosting is **not** a polymer issue. It's structural: the printer's gantry has natural resonance frequencies (typically 30–80 Hz on bedslingers, higher on CoreXY like P2S). A sharp accel pulse contains energy across many frequencies — if any matches a resonance, the toolhead oscillates after the move ends, leaving wavy "echoes" of corners on the wall. Slowing outer wall lowers the excitation amplitude; reducing accel removes the high-frequency components. Input shaping cancels the resonance directly. Three independent levers, one symptom.

### Summary — chemistry → setting

```
HYGROSCOPIC POLYMERS (PA, PETG, PC)  →  must dry, otherwise hydrolysis + steam
VISCOELASTIC MELT                    →  pressure advance (K-value) per filament
MELT INDEX + FILLER VARIATION        →  flow ratio per spool
GLASS TRANSITION TEMP (Tg)           →  cooling profile + chamber temp
CRYSTALLIZATION KINETICS             →  fan speed (low for PA, high for PLA)
POLYMER INTERDIFFUSION TIME          →  enclosure for tall/strong parts
GANTRY RESONANCE (mechanical)        →  outer wall speed / accel / input shaping
NOZZLE WEAR (mechanical)             →  hardened steel for CF/GF filaments
```

</details>

<details>
<summary><strong>The Key Tension</strong> — Speed vs. surface, and stock vs. custom profiles</summary>

**Tension 1: Speed vs. surface finish.** P2S can hit 600 mm/s, but visible quality lives below 80 mm/s on outer walls. The trick is asymmetric: slow the outer perimeter, run everything else fast. You pay maybe 10–15% time for huge quality gains.

**Tension 2: Stock RFID profile vs. custom calibrated profile.** Bambu RFID auto-loads a generic profile per filament SKU. It's fine. A *calibrated* profile (your specific spool, your specific environment) is better. Real maker workflow: clone the stock profile, run K-value + flow rate calibrations once per spool batch, save as "Bambu PLA Matte — Spool 47."

**Tension 3: P2S vs. P1S calibration UX.** P1S has no LiDAR or eddy sensor — calibration is manual visual judgment of test patterns. **P2S adds an eddy current sensor between extruder and hotend**, enabling automatic Flow Dynamics (K-value) calibration: start the routine, printer returns the K. Manual mode still exists for users who want fine control. Plan to spend ~20 min per new filament regardless.

| Setting | Stock default | Quality preset |
|---------|---------------|----------------|
| Outer wall speed | 200 mm/s | 50 mm/s |
| Outer wall accel | 5000–10000 mm/s² | 3000 mm/s² |
| Wall order | Inner/Outer | Outer/Inner |
| Overhang cooling threshold | 50% | 25% |
| Layer height | 0.20 mm | 0.12–0.16 mm (display parts) |

</details>

<details>
<summary><strong>Concrete Example</strong> — Calibrating a fresh spool of PLA</summary>

Workflow for a new spool of generic (non-RFID) PLA on P2S:

```
1. DRY (if humid or older spool)
   AMS 2 Pro: PLA, 45°C, 6h.
   Or oven: 45°C / 6h with door cracked.

2. WIPE PLATE
   Cool textured PEI plate. 99% IPA on lint-free cloth.
   Don't touch surface with bare fingers afterward.

3. CLONE PROFILE
   Bambu Studio → Filament → "Generic PLA" → Clone
   Rename: "Generic PLA — Hatchbox Black — 2026-04"

4. FLOW DYNAMICS (K-value)
   Calibration → Flow Dynamics → Auto (P2S has eddy sensor)
   Or Manual mode → pick row with sharpest corners,
   no bulge, no end-of-line gap.
   Typical PLA range: K = 0.015 – 0.040 (varies by brand)
   Save K into the cloned profile.

5. FLOW RATE
   Calibration → Flow Rate → Pass 1 (coarse)
   Print test → pick smoothest top surface.
   Pass 2 (fine) → narrower range around Pass 1 winner.
   Typical flow ratio: 0.94 – 1.00
   Save into profile.

6. PRINT A BENCHY
   Use the calibrated profile.
   Inspect: corners, overhangs, layer lines, top surface.
```

Slicer settings to verify before clicking print:

```
Bambu Studio → your project → Process → Quality:
  • Layer height:                0.16 mm  (display) / 0.20 mm (functional)
  • Outer wall speed:            50 mm/s
  • Outer wall acceleration:     3000 mm/s²
  • Wall printing order:         Outer/Inner
  • Overhang cooling threshold:  25%
  • Top surface ironing:         ON (for flat top parts)
```

**The one thing most outsiders get wrong about this is...** thinking "Bambu = perfect prints out of the box." Stock profiles are *good*, not optimal. Two hours of per-spool calibration upfront beats months of fighting stringing, ghosting, and weak overhangs. The P2S hardware ([[learning/notes/quick-context/3d-printer-hotends|hotend]] + DynaSense extruder + Adaptive Airflow) is only as good as the K-value and flow ratio you feed it.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[learning/notes/quick-context/3d-printing-slicer-settings]]** — Layer height × nozzle width × speed = volumetric flow rate. Calibrating K and flow ratio on the P2S is meaningless if your slicer settings demand more flow than the [[learning/notes/quick-context/3d-printer-hotends|hotend]] can melt.
- **[[learning/notes/quick-context/3d-printer-hotends]]** — P2S hardened-steel hotend handles fiber-reinforced filaments and reaches 300°C. Max volumetric throughput is the hard ceiling that no amount of K-value tuning can exceed.
- **[[learning/notes/quick-context/3d-printing-filament-types]]** — Each material (PLA / PETG / ABS / PA-CF) has a different optimal K-value, flow ratio, dry temp, and cooling target. Calibration is *per material*, not just per printer.
- **[[learning/notes/quick-context/bambu-ams-automatic-material-system]]** — P2S ships with AMS 2 Pro, which actively vents to dry filament 30% faster than sealed heating. Dry filament is precondition #1 for quality.
- **[[learning/notes/quick-context/3d-printing-filament-refill-vs-spool]]** — Refill spools sometimes have different flow behavior than full spools (slightly different supplier batches). Re-run flow calibration when switching.
- **[[learning/notes/quick-context/glass-transition-temperature]]** — Tg is the threshold above which polymer chains can interdiffuse between layers. Cooling, chamber temp, and overhang fan speed are all really about controlling time above Tg.
- **[[learning/notes/quick-context/polymer-crystallinity-vs-amorphous]]** — Why PLA (amorphous) tolerates aggressive cooling but PA / PP (semi-crystalline) warp and delaminate without an enclosed, slow-cooling environment.
- **[[learning/notes/quick-context/melt-index]]** — Polymer flow rate at melt — directly drives optimal K-value and flow ratio. High-MFI batches need different settings than low-MFI batches of the "same" filament.
- **[[learning/notes/quick-context/hydrogen-bonds-beginners]]** — Why nylon is the worst hygroscopic offender: amide groups donate *and* accept hydrogen bonds with water, locking H₂O between chains.
- **[[learning/notes/quick-context/polymer-chemical-bonds]]** — Intermolecular forces (van der Waals / dipole / H-bond) explain layer adhesion strength and why different filaments melt at different temperatures.
- **Input Shaping / Vibration Compensation** — P2S runs this at startup; re-run after belt tension changes or if ringing reappears.

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** Why calibrate Flow Dynamics (K-value) *before* Flow Rate, not the other way around?
<details>
<summary>Answer</summary>
K-value affects how much filament is at the nozzle during accel/decel transitions. If K is wrong, the test patterns for flow rate (which look at smooth top surfaces) get distorted by pressure-lag artifacts at line ends. Fix the dynamics first, then measure steady-state flow.
</details>

**Q2:** You drop outer wall speed from 200 → 50 mm/s. Total print time only goes up ~10%. Why so little?
<details>
<summary>Answer</summary>
Outer wall is one perimeter line per layer — usually <15% of toolpath length. Inner walls and infill (the other 85%) still run at full speed. Slowing only the visible 15% of the path costs little time and removes most of the ringing/ghosting because outer-wall vibration dominates what humans perceive as quality. See: The Key Tension.
</details>

**Q3:** A user says "I dialed in K-value and flow rate, but my parts still string between towers." What did they likely skip?
<details>
<summary>Answer</summary>
Filament drying. Wet filament has water trapped in the polymer; at melt temp, water flashes to steam and pops out of the nozzle, leaving stringing residue and surface defects. K-value tuning can't fix moisture-driven defects. PLA at 45°C / 6–8h or use AMS 2 Pro active venting.
</details>

**Q4:** P1S can't auto-calibrate K-value because it lacks LiDAR/eddy sensors. Why does this matter for quality even though the user can still calibrate manually?
<details>
<summary>Answer</summary>
Manual calibration relies on visual judgment of test patterns — humans pick "the sharpest corner row." This is subjective and skipped by many users, leaving them on default K. Auto-calibration runs deterministically every time. The P2S closes this gap: it ships with an eddy current sensor between extruder and hotend that measures pressure changes during a probe extrusion, returning the optimal K automatically — same capability as the X1C. P1S users must still build the discipline of manual per-spool calibration; P2S users can just hit "Auto."
</details>

**Q5:** You're printing a fiber-reinforced nylon (PA-CF) part for a [[learning/notes/quick-context/pupper-bom-control-board|robot chassis]]. Which P2S features matter most, and why?
<details>
<summary>Answer</summary>
(1) Hardened steel nozzle and extrusion gears — carbon fiber abrades brass nozzles in hours. (2) Enclosed chamber — PA shrinks aggressively as it cools; sealed heat keeps the chamber warm and prevents warping/delamination. (3) Adaptive Airflow set to seal mode (no fresh air intake during PA print). (4) Drying at 80°C for 12+ hours — nylon absorbs moisture from air faster than any other common filament; printing wet PA gives weak, foamy parts regardless of every other setting. (5) Re-calibrate K and flow ratio for PA-CF specifically — values are very different from PLA.
</details>

</details>

## Sources

- [Bambu Lab P2S Product Page](https://bambulab.com/en-us/p2s)
- [Bambu Lab P2S Specifications](https://bambulab.com/en/p2s/specs)
- [Tom's Hardware — Bambu Lab P2S Review](https://www.tomshardware.com/3d-printing/bambu-lab-p2s-review)
- [P2S First-Layer Optimization Guide (Bambu Wiki)](https://wiki.bambulab.com/en/p2s/troubleshooting/first-layer-printing-optimization-guide)
- [Flow Dynamics Calibration (Bambu Wiki)](https://wiki.bambulab.com/en/software/bambu-studio/calibration_pa)
- [Flow Rate Calibration (Bambu Wiki)](https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate)
- [Print Quality Guide for A1, P1S, X1C (MakerWorld)](https://makerworld.com/en/models/536929-print-quality-guide-for-a1-a1-mini-p1s-x1c)
- [10 Bambu Studio Tips for Better Quality (PrintPal)](https://blog.printpal.io/10-bambu-studio-tips-for-better-quality-3d-prints/)
- [Bambu Lab K-Value Guide (BabaBuilds)](https://bababuilds.com/blog/bambu-lab-flow-dynamics-calibration-k-value/)
