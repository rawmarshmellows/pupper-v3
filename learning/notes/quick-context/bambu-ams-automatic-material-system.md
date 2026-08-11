---
topic: Bambu AMS (Automatic Material System)
created: 2026-01-21
updated: 2026-01-21
---

> **Related:** [[quick-context/3d-printer-hotends]], [[quick-context/3d-printing-filament-types]], [[quick-context/bambu-p2s-print-quality]]

> **TL;DR:** The AMS automates multi-color printing and filament backup. It holds 4 spools and automatically retracts, cuts, and loads filament as needed. The killer feature for functional printing is spool backup for unattended long prints - not just colorful artistic prints.

# Bambu AMS: Quick Context

## The Core Problem

The AMS (Automatic Material System) solves two problems that plague FDM 3D printing: **multi-color/multi-material printing** and **filament runout mid-print**. Without an AMS, printing in multiple colors requires either manual filament swaps (pause print → yank filament → load new color → resume → repeat dozens of times) or buying separate printers for each material. A 4-color print might need 50+ manual swaps over an 8-hour print—one missed swap ruins the entire job. The AMS automates this: it holds 4 spools, and the printer automatically retracts, cuts, and loads the next color as needed. Beyond multi-color, the AMS enables **automatic spool backup**—when one spool runs out mid-print, it seamlessly switches to the next spool of the same material without human intervention. This turns unattended overnight prints from risky gambles into reliable workflows. The system also provides humidity monitoring and RFID auto-detection for Bambu filaments, automatically applying optimal temperature and flow settings.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Purge/waste tower** | Sacrificial block printed alongside your model to flush old color from the nozzle before printing new color—the main source of multi-color filament waste. |
| **RFID tag** | Embedded chip in Bambu spools that the AMS reads to auto-detect material type, color, and remaining length—third-party filaments require manual profile configuration. |
| **Filament buffer/hub** | The junction box between AMS and printer that manages filament paths and provides slack for the reverse-Bowden tube—each AMS connects through this. |
| **Spool backup** | AMS feature that automatically switches to another slot when current spool runs out—requires pre-mapping which slots contain the same material. |
| **AMS Lite vs AMS vs AMS 2 Pro** | Lite is simpler/cheaper for A1 series (4 colors max, no drying); standard AMS for X1/P1 series (stackable to 16 colors); AMS 2 Pro adds active drying up to 65°C and faster motors. |

<details>
<summary><strong>How It Works</strong></summary>

The AMS operates through a coordinated sequence of mechanical actions controlled by the printer's firmware. When a color change is needed, the extruder first reverses direction to pull the current filament back out of the hotend and through the Bowden tube. A cutting mechanism inside the AMS then snips the filament tip clean, ensuring a fresh end for the next load. The AMS hub—a central junction box—manages the routing between up to four AMS units (16 total slots) and the single path to the printer's toolhead.

For loading, the AMS uses motorized rollers to feed the selected filament through its internal path, into the hub, and down the reverse-Bowden tube to the extruder. The extruder gears then grip the filament and push it through the hotend. Before printing resumes, the printer must **purge** the old color from the nozzle—this is done by extruding material into a waste tower or into the model's infill until only the new color emerges. RFID readers at each slot detect Bambu-branded spools and automatically configure temperature, flow rate, and material type; third-party filaments require manual profile selection in the slicer software.

```
FILAMENT CHANGE SEQUENCE
========================

1. RETRACT          2. CUT              3. SELECT NEW       4. FEED & LOAD
   ────────            ───                 ────────────        ──────────

   Extruder          Cutter blade         Hub routes to       Motors push
   reverses          snips tip            new spool slot      new filament

   ┌─────────┐       ┌─────────┐         ┌─────────┐         ┌─────────┐
   │ HOTEND  │       │ HOTEND  │         │ HOTEND  │         │ HOTEND  │
   │    │    │       │         │         │         │         │    │    │
   │    ↑    │       │  ✂ cut  │         │         │         │    ↓    │
   │ filament│       │    │    │         │         │         │ new clr │
   └────│────┘       └────│────┘         └─────────┘         └────│────┘
        │                 │                   │                    │
   ┌────│────┐       ┌────│────┐         ┌────│────┐         ┌────│────┐
   │   HUB   │       │   HUB   │         │   HUB   │ ←route  │   HUB   │
   └─┬──┬──┬─┘       └─┬──┬──┬─┘         └─┬──┬──┬─┘         └─┬──┬──┬─┘
     │  │  │           │  │  │             │  │  │             │  │  │
   [1][2][3][4]      [1][2][3][4]        [1][2][3][4]        [1][2][3][4]
    ↑                                           ↑                   ↑
   OLD                                         NEW                 NEW
   (retracted)                              (selected)           (feeding)

5. PURGE            6. RESUME PRINT
   ─────               ────────────

   Extrude old         Clean color
   color into          ready to print
   waste tower

   ┌─────────┐         ┌─────────┐
   │ HOTEND  │         │ HOTEND  │
   │    │░░░░│→waste   │    │    │→ model
   │ new clr │         │ new clr │
   └────│────┘         └────│────┘
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The central tradeoff is **print time vs. color capability vs. material waste**. Every color change requires purging the old color from the [[quick-context/3d-printer-hotends|hotend]] before the new color can print cleanly—this purge block wastes 1-3g of filament per swap. A 16-color artistic print might waste 200g+ of filament just on purging (often more than the actual model). Practitioners optimize this through: (1) **purge-to-infill** techniques that hide purge material inside the model, (2) careful color ordering to minimize dark→light transitions, and (3) designing models that minimize color changes per layer. There's also a speed penalty: each swap adds 15-30 seconds of retract/cut/load/purge time. The AMS 2 Pro reduces this with faster motors (60% quicker feeds), but multi-color prints are inherently slower than single-color. Material compatibility is another tension—soft filaments (TPU), abrasive filaments (carbon fiber), and hygroscopic filaments (PVA) can jam the AMS feeding mechanism, forcing manual loading for these materials.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Setting up a 4-color print with automatic backup in Bambu Studio:

```json
// Bambu Studio project config (simplified from .3mf internal structure)
{
  "filament_settings": [
    {
      "slot": 1,
      "ams_id": 0,
      "type": "PLA",
      "color": "#FFFFFF",
      "nozzle_temp": 220,
      "bed_temp": 60,
      "backup_slots": [5]  // Slot 5 (AMS 2, slot 1) has same white PLA
    },
    {
      "slot": 2,
      "ams_id": 0,
      "type": "PLA",
      "color": "#000000",
      "nozzle_temp": 220
    },
    {
      "slot": 3,
      "ams_id": 0,
      "type": "PLA",
      "color": "#FF0000",
      "nozzle_temp": 220
    },
    {
      "slot": 4,
      "ams_id": 0,
      "type": "PLA",
      "color": "#0000FF",
      "nozzle_temp": 220
    }
  ],
  "flush_volumes_matrix": [
    // Purge volume (mm³) needed when switching FROM row TO column
    // Higher values for dark→light transitions
    [0,   180, 180, 180],   // From white
    [140,   0, 200, 200],   // From black (needs more purge going to colors)
    [140, 180,   0, 180],   // From red
    [140, 180, 180,   0]    // From blue
  ],
  "prime_tower_width": 35,  // mm - wider = more purge capacity but more waste
  "enable_prime_tower": true
}
```

**Physical setup for 2x AMS (8 slots):**
```
AMS Unit 0 (slots 1-4)          AMS Unit 1 (slots 5-8)
┌─────┬─────┬─────┬─────┐      ┌─────┬─────┬─────┬─────┐
│White│Black│ Red │Blue │      │White│Black│     │     │
│(1)  │(2)  │(3)  │(4)  │      │(5)  │(6)  │(7)  │(8)  │
│500g │500g │250g │250g │      │500g │500g │empty│empty│
│     │     │     │     │      │BKUP │BKUP │     │     │
└─────┴─────┴─────┴─────┘      └─────┴─────┴─────┴─────┘
         │                              │
         └──────────┬───────────────────┘
                    ▼
              Filament Hub
                    │
                    ▼
              Printer Toolhead
```

Slots 5-6 are configured as backups for slots 1-2. When slot 1's white runs out at 3am, the printer automatically:
1. Retracts remaining filament from slot 1
2. Loads white from slot 5
3. Continues printing with zero intervention

**The one thing most outsiders get wrong about this is...** assuming the AMS is just for multi-color artistic prints they don't care about. The killer feature for functional printing is **spool backup for unattended prints**. A 40-hour engineering prototype that runs out of filament at hour 35 is a complete failure—the AMS lets you load two 1kg spools of the same material and walk away for the weekend. Multi-color is the flashy feature; reliability is the practical one.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- [[quick-context/3d-printing-filament-types]] — Understanding material properties (PLA, PETG, TPU, etc.) is essential since AMS compatibility varies by filament type; soft and abrasive materials often require manual loading
- [[quick-context/3d-printer-hotends]] — The hotend determines purge efficiency and material compatibility; all-metal hotends handle higher temps but may require different purge volumes
- [[quick-context/3d-printing-slicer-settings]] — Slicer configuration (flush volumes, tower placement, color sequencing) directly controls AMS waste and print time overhead

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does switching from black to white filament require more purge volume than white to black?
<details>
<summary>Answer</summary>
Black pigment is highly saturating—even small traces contaminate lighter colors visibly. When purging black before printing white, you need extensive flushing (often 200+ mm³) to eliminate all dark residue. Going the opposite direction (white to black), tiny white contamination is invisible against the black, so minimal purging suffices. This asymmetry is why the flush_volumes_matrix isn't symmetric, and why experienced users sequence colors to minimize dark-to-light transitions.
</details>

**Q2:** What's the difference between "purge to infill" and a standard prime tower, and when would you choose each?
<details>
<summary>Answer</summary>
A **prime tower** is a separate sacrificial structure printed alongside your model solely to waste purge material—it's reliable but adds print time, uses plate space, and wastes filament. **Purge to infill** routes purge material into your model's internal infill instead, hiding waste inside the part. Choose purge-to-infill when your model has substantial infill volume and you want to minimize waste; choose a prime tower when your model is thin-walled, has minimal infill, or when you need guaranteed purge consistency (infill purging can occasionally cause surface artifacts if misconfigured).
</details>

**Q3:** If you have a 16-hour print using a single material, what AMS feature provides value even without multi-color printing?
<details>
<summary>Answer</summary>
**Spool backup/automatic filament switching.** You can load two spools of identical material in different AMS slots and configure one as backup for the other. If the first spool runs out mid-print (especially common with large prints that consume 800g+), the AMS automatically retracts the empty spool's remnant, loads from the backup spool, and continues printing—no human intervention required. This enables truly unattended long prints without the risk of filament runout failures.
</details>

**Q4:** Why might you choose to manually load TPU filament even if you have an AMS?
<details>
<summary>Answer</summary>
[[quick-context/3d-printing-filament-types|TPU]] (flexible filament) is soft and elastic, which causes feeding problems in the AMS's Bowden tube system. The filament can compress, stretch, or buckle instead of pushing smoothly through the tube, leading to jams or inconsistent feeding. The AMS was designed primarily for rigid filaments like [[quick-context/3d-printing-filament-types|PLA]] and PETG. For TPU and other flexible materials, direct manual loading into the printer's extruder (bypassing the AMS entirely) provides reliable feeding. Similar issues occur with very abrasive filaments (carbon fiber, glow-in-the-dark) that can wear AMS components.
</details>

**Q5:** The AMS enables multi-material prints. How do differences in Tg, thermal expansion, and inter-material adhesion create challenges that single-material printing doesn't face?
<details>
<summary>Answer</summary>
Multi-material printing introduces compatibility physics: (1) **Thermal mismatch**—materials with different Tg values cool at different rates, causing warping or delamination at interfaces (PLA shrinks more than PETG as it cools past its Tg); (2) **Adhesion problems**—some materials chemically bond (PLA/PLA) while others don't (PLA won't stick to TPU), requiring careful interface design or soluble interface materials; (3) **Temperature compromises**—the hotend must purge and switch between materials at potentially different optimal temps, risking under-extrusion or degradation; (4) **Expansion differences**—materials with different thermal expansion coefficients create internal stresses that cause cracking during cooling. The AMS mechanically enables swaps, but multi-material physics remains the user's challenge. See: [[quick-context/glass-transition-temperature]] and [[quick-context/3d-printing-filament-types]] for [[learning/notes/quick-context/breaking-elongation-rate|material property]] details.
</details>

</details>
