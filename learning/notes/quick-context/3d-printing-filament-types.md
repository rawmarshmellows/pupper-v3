---
topic: 3D Printing Filament Types (PLA vs PETG vs ABS vs TPU)
created: 2026-01-20
updated: 2026-01-21
---

> **Related:** [[quick-context/3d-printing-filament-refill-vs-spool|3D Printing Filament - Refill vs Spool]] | [[quick-context/3d-printer-hotends|3D Printer Hotends]] | [[quick-context/3d-printing-slicer-settings|3D Printing Slicer Settings]] | [[quick-context/glass-transition-temperature|Glass Transition Temperature]] | [[quick-context/pi-pi-stacking-aromatic-interactions|Pi-Pi Stacking]]

> **TL;DR:** Different 3D printing filaments (PLA, PETG, ABS, TPU) offer distinct tradeoffs between printability and performance—PLA prints easily but fails under heat/stress, while ABS and TPU offer better performance at the cost of printing difficulty.

# 3D Printing Filament Types: PLA, PETG, ABS, and TPU

## The Core Problem

**The core problem filament choice solves** is matching material properties to your part's requirements—mechanical stress, temperature exposure, aesthetics, flexibility, and printability. Choose wrong and your part warps off the bed mid-print, becomes brittle in sunlight, deforms in a hot car, or looks terrible despite perfect settings. PLA is the easy-mode default (low temp, minimal [[quick-context/polymer-crystallinity-vs-amorphous|warping]], biodegradable), but it fails above ~55°C and is relatively brittle. PETG sits in the middle—better heat resistance (~75°C), more flexible, food-safe variants exist—but strings like crazy and scratches easily. ABS is the old-school industrial choice (heat resistant to ~100°C, tough, acetone-smoothable) but requires an enclosure, smells toxic, and warps aggressively without proper bed adhesion. TPU (thermoplastic polyurethane) is the flexible/rubber-like option—excellent impact resistance, bends without breaking, great for gaskets and grips—but requires a direct drive extruder, painfully slow print speeds, and fights retraction settings.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **[[quick-context/glass-transition-temperature|Glass transition temperature]] (Tg)** | The temp where plastic softens—PLA ~55°C, PETG ~75°C, ABS ~100°C |
| **Warping** | Corners lifting off the bed due to uneven cooling/shrinkage—ABS is notorious, PLA is forgiving |
| **Stringing** | Thin wisps of plastic between travel moves—PETG's nemesis, requires retraction tuning |
| **Hygroscopic** | Absorbs moisture from air, degrading print quality—PETG, Nylon, and TPU are worst offenders |
| **Layer adhesion** | How well layers bond together—affects part strength; ABS and PETG excel, PLA is adequate |

<details>
<summary><strong>How It Works</strong></summary>

Filament printing is fundamentally a controlled melting and re-solidification process. Solid plastic enters the hotend as a rigid rod, gets heated past its [[quick-context/glass-transition-temperature|glass transition temperature]] (Tg) where the polymer chains gain enough energy to slide past each other, and exits the nozzle as a viscous fluid that immediately begins cooling. The cooling rate and ambient temperature determine how the material re-solidifies—too fast and you get internal stresses (warping), too slow and the part sags before setting. Each filament type has different molecular structures that dictate how much energy is needed to achieve flow and how the material behaves during cooling.

The key to understanding filament differences lies in their polymer chain architecture and intermolecular forces. PLA has short, relatively simple chains with weak intermolecular attractions—easy to melt, quick to solidify, minimal shrinkage. ABS contains aromatic styrene rings that engage in [[quick-context/pi-pi-stacking-aromatic-interactions|pi-pi stacking]], creating stronger inter-chain attractions that require more heat to overcome and cause significant shrinkage when those attractions reform during cooling. PETG has a balance of chain flexibility and polar groups that make it sticky when molten (hence stringing) but dimensionally stable. TPU's elasticity comes from alternating hard and soft polymer segments—the soft segments stay flexible while hard segments provide structure.

```
FILAMENT PRINTING PROCESS:

  SOLID FILAMENT              HOTEND (heated zone)              DEPOSITED LAYER
       |                            |                                |
       v                            v                                v

  ============           ╔═══════════════════╗           ~~~~~~~~~~~~~~~~
  ============  ──────►  ║  MELT ZONE        ║  ──────►  ~~~~~~~~~~~~~~~~
  ============           ║  (above Tg)       ║           ~~~~~~~~~~~~~~~~
       |                 ║                   ║                 |
   Rigid rod             ╠═══════════════════╣           Cooling/bonding
   (chains locked)       ║  NOZZLE           ║           to previous layer
                         ╚═══════════════════╝


MOLECULAR VIEW OF EACH FILAMENT TYPE:

PLA (simple chains, weak forces):
  ~~~~~~~~~~~      ~~~~~~~~~~~      Low Tg (~55C)
  ~~~~~~~~~~~      ~~~~~~~~~~~      Easy melt, fast set
  ~~~~~~~~~~~      ~~~~~~~~~~~      Minimal shrinkage

ABS (aromatic rings create stacking):
  ~~[B]~~[B]~~     ~~[B]~~[B]~~     [B] = benzene ring
     |     |          |     |       High Tg (~100C)
  ~~[B]~~[B]~~     ~~[B]~~[B]~~     Pi-pi stacking forces
     |     |          |     |       Significant shrinkage
  ~~[B]~~[B]~~     ~~[B]~~[B]~~     (rings re-stack on cooling)

PETG (polar groups, moderate stacking):
  ~~(O)~~[B]~~     ~~(O)~~[B]~~     (O) = ester group
  ~~(O)~~[B]~~     ~~(O)~~[B]~~     [B] = benzene ring
  ~~(O)~~[B]~~     ~~(O)~~[B]~~     Sticky melt, moderate shrinkage

TPU (alternating hard/soft segments):
  ═══~~~═══~~~     ═══~~~═══~~~     ═══ = hard segment (rigid)
  ═══~~~═══~~~     ═══~~~═══~~~     ~~~ = soft segment (flexible)
  ═══~~~═══~~~     ═══~~~═══~~~     Elastic recovery on cooling


WHY TEMPERATURE MATTERS:

            Energy input
                 |
                 v
    [Solid] ──────────► [Rubbery] ──────────► [Flowing]
         Tg threshold        Melt threshold

    PLA:   |----55C----|--------180C--------|   (low energy needed)
    PETG:  |----75C----|--------220C--------|   (moderate)
    ABS:   |---100C----|--------230C--------|   (high energy needed)
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

**The key tension** is the printability-vs-performance tradeoff. PLA prints beautifully but performs poorly under stress or heat. ABS performs well but fights you the entire print. PETG is the compromise that's "good enough" at both but excels at neither. TPU opens up an entirely different axis—flexibility—but at the cost of print speed and extruder requirements. Within PLA variants: Basic is cheap and functional; Matte hides layer lines but may be slightly weaker; Silk+ has a shiny metallic finish but is more brittle and harder to tune; Translucent enables light-diffusing applications but shows every internal flaw. PETG HF (High Flow) prints faster with larger nozzles but sacrifices fine detail. TPU comes in different Shore hardnesses (95A is common, lower = softer)—softer is more flexible but exponentially harder to print. Practitioners argue endlessly about whether PETG has truly replaced ABS for functional parts, and whether TPU is "worth the hassle" vs. just buying rubber parts.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

**Concrete example—typical slicer settings comparison:**

```
Material        | Nozzle Temp | Bed Temp | Enclosure | Part Cooling | Print Speed
----------------|-------------|----------|-----------|--------------|------------
PLA Basic       | 200-220°C   | 50-60°C  | No        | 100%         | 50-100mm/s
PLA Matte       | 200-220°C   | 50-60°C  | No        | 100%         | 50-100mm/s
PLA Silk+       | 215-230°C   | 55-65°C  | No        | 50-80%*      | 40-60mm/s
PLA Translucent | 200-220°C   | 50-60°C  | No        | 100%         | 50-100mm/s
PETG HF         | 240-260°C   | 70-85°C  | Optional  | 30-50%       | 60-150mm/s
PETG Translucent| 230-250°C   | 70-85°C  | Optional  | 30-50%       | 40-60mm/s
ABS             | 240-260°C   | 90-110°C | Required  | 0-20%        | 40-60mm/s
TPU 95A         | 220-250°C   | 40-60°C  | Optional  | 50-100%      | 15-30mm/s**

* Silk+ needs less cooling to maintain sheen but more to prevent drooping
** TPU requires direct drive extruder; Bowden setups will jam. Disable or minimize retraction.
```

**When to use what:**
- **PLA Basic**: Prototypes, decorative items, anything that stays indoors at room temp
- **PLA Matte**: Visible parts where you want to hide layer lines without post-processing
- **PLA Silk+**: Vases, display pieces, anything where aesthetics trump function
- **PETG (any)**: Functional parts with moderate heat/stress—phone cases, brackets, outdoor items
- **ABS**: Automotive parts, enclosures near heat sources, anything needing acetone smoothing
- **TPU**: Phone cases, drone bumpers, gaskets, vibration dampeners, watch bands, anything that needs to flex or absorb impact

The one thing most outsiders get wrong about this is **assuming "stronger" or "more advanced" filaments are always better**. A PLA part printed with good layer adhesion often outperforms a poorly-printed ABS part, and the dimensional accuracy of easy-printing PLA frequently matters more than raw material strength. Similarly, people try TPU expecting rubber-like flexibility and get frustrated when their Bowden setup jams constantly—check your hardware first. The best filament is the one you can actually print well on your machine.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

Related concepts that deepen understanding of filament types:

- [[quick-context/glass-transition-temperature]] — Why PLA fails in hot cars and ABS survives; the critical temperature threshold for each material
- [[quick-context/polymer-crystallinity-vs-amorphous]] — Explains warping behavior differences between materials and why some filaments shrink more than others
- [[quick-context/melt-index]] — How filament flow characteristics affect printability and why PETG HF exists
- [[quick-context/3d-printer-hotends]] — Hardware requirements for different filaments; why all-metal hotends matter for PETG/ABS temps
- [[quick-context/3d-printing-slicer-settings]] — Translating filament properties into actual print profiles

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** You need to print a bracket that will be mounted inside a car dashboard in summer. Which filament should you use and why?
<details>
<summary>Answer</summary>
ABS or PETG, but ABS is preferred. Car interiors can reach 60-80°C in summer sun, which exceeds PLA's [[quick-context/glass-transition-temperature|glass transition temperature]] (~55°C) and approaches PETG's limit (~75°C). ABS with its ~100°C Tg is the safest choice. See the **glass transition temperature** definition in "5 Essential Terms" and the temperature comparison in the settings table.
</details>

**Q2:** Your PETG prints have thin wisps of plastic connecting different parts of the model. What's happening and how do you fix it?
<details>
<summary>Answer</summary>
This is stringing, PETG's most common problem. The material doesn't cleanly retract during travel moves due to its sticky, viscous nature when melted. Fix by increasing retraction distance/speed, lowering nozzle temperature slightly (within recommended range), and enabling "wipe" or "coasting" in your slicer. See "stringing" in the "5 Essential Terms" section.
</details>

**Q3:** Why would someone choose PLA Matte over PLA Basic for a visible functional part?
<details>
<summary>Answer</summary>
PLA Matte hides layer lines without requiring post-processing like sanding or painting. The matte finish diffuses light rather than reflecting it off the ridged surface of each layer. Trade-off: it may be slightly weaker than basic PLA. See the "When to use what" section for application guidance.
</details>

**Q4:** You want to print flexible phone bumpers but your printer has a Bowden tube setup. What problems will you encounter?
<details>
<summary>Answer</summary>
TPU will likely jam. Bowden setups have a long, flexible path between the extruder motor and hotend, and soft TPU compresses and buckles in this tube instead of being pushed forward. You need a direct drive extruder where the motor sits directly on the hotend. See the TPU row in the settings table (footnote **) and the final paragraph about hardware requirements.
</details>

**Q5:** A friend claims ABS is "better" than PLA because it's stronger. How would you respond?
<details>
<summary>Answer</summary>
This is the common misconception addressed in the final paragraph. A well-printed PLA part often outperforms a poorly-printed ABS part. ABS requires an enclosure, fights warping, and produces toxic fumes—if you can't manage these, your ABS prints will have weak layer adhesion and dimensional inaccuracy. PLA's easy printability often matters more than raw material strength. The "best" filament is the one you can actually print well.
</details>

</details>
