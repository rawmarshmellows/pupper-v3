---
topic: Glass Transition Temperature (Tg)
created: 2026-01-20
updated: 2026-01-21
---

> **Related:** [[learning/notes/quick-context/polymer-crystallinity-vs-amorphous]] | [[learning/notes/quick-context/3d-printing-filament-types]] | [[learning/notes/quick-context/atoms-molecules-polymers-basics]] | [[learning/notes/quick-context/polymer-chemical-bonds]]

> **TL;DR:** Glass transition temperature (Tg) is the temperature where polymer chains gain enough thermal energy to wiggle and slide past each other, transforming the plastic from rigid/glassy to soft/rubbery—critical for choosing 3D printing materials that won't warp in hot environments like cars.

# Glass Transition Temperature (Tg) - A Beginner's Guide

## The Core Problem

Plastics are made of **[[learning/notes/quick-context/atoms-molecules-polymers-basics|polymers]]**—long, spaghetti-like chains of molecules tangled together. At low temperatures, these chains are frozen in place, locked together by weak attractions. The plastic feels hard and rigid. But here's the critical insight: **there's a specific temperature where those chains suddenly gain enough energy to wiggle and slide past each other**. This is the **glass transition temperature (Tg)**. Below Tg, your plastic is glassy and stiff. Above Tg, it becomes rubbery, soft, and deformable—even though it hasn't technically "melted" yet. This matters enormously because if you use a plastic above its Tg, it will sag, warp, and lose its shape under any load. Your carefully 3D-printed part becomes a droopy mess. Your phone case warps. Your tool handle bends. Understanding Tg is the difference between picking a material that survives real-world conditions and watching your project fail on a hot summer day.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **[[learning/notes/quick-context/atoms-molecules-polymers-basics|Polymer]]** | Long chain-like molecules made of repeating units; all plastics are polymers (think: molecular spaghetti strands). |
| **Tg (Glass Transition Temperature)** | The specific temperature where a polymer shifts from rigid/glassy to soft/rubbery; the "danger zone" threshold for your material. |
| **[[learning/notes/quick-context/polymer-crystallinity-vs-amorphous|Amorphous]]** | Polymer chains arranged randomly (like tangled headphones); these have a distinct Tg and gradually soften. |
| **[[learning/notes/quick-context/polymer-crystallinity-vs-amorphous|Crystalline/Semi-crystalline]]** | Polymer chains partially organized into ordered regions; these have both Tg and a sharper melting point (Tm). |
| **Annealing** | Heat-treating a printed part below its melting point to increase crystallinity and improve heat resistance; a post-processing trick for PLA. |

<details>
<summary><strong>How It Works</strong></summary>

At the molecular level, Tg represents an energy threshold (related to the same [[learning/notes/quick-context/thermal-noise-electronics|kT thermal energy]] scale that drives noise in electronics). Polymer chains are held in place by **intermolecular forces**—weak attractions like van der Waals forces and hydrogen bonds between neighboring chain segments. At low temperatures, the thermal energy (random molecular vibration) is not enough to overcome these attractions, so the chains are essentially frozen in place. As you heat the material, you add thermal energy. At Tg, the chains finally have enough energy to overcome the intermolecular attractions and begin rotating around their backbone bonds, sliding past neighboring chains, and rearranging their positions.

This transition is not a sharp phase change like ice melting to water. Instead, it occurs over a temperature range (typically 10-30°C wide) where the material progressively softens. The Tg value reported is usually the midpoint of this transition. What matters practically is that mechanical properties change dramatically: the **modulus** (stiffness) can drop by a factor of 1000 between the glassy state and the rubbery state. Time also becomes a factor above Tg—even small loads will cause the material to slowly **creep** and permanently deform over hours or days as chains gradually slide past each other.

```
MOLECULAR VIEW: WHAT HAPPENS AT Tg
==================================

BELOW Tg (Glassy State)                 ABOVE Tg (Rubbery State)
───────────────────────                 ────────────────────────

Polymer chains:                         Polymer chains:
═══════════════                         ~~~~~~~~~~~~~~~
═══════════════                         ~~~~~~~~~~~~~~~
═══════════════                         ~~~~~~~~~~~~~~~

• Chains LOCKED in place                • Chains can WIGGLE and SLIDE
• Intermolecular bonds intact           • Bonds constantly breaking/reforming
• No rotation around backbone           • Free rotation around backbone
• Rigid, brittle behavior               • Soft, flexible behavior


ENERGY DIAGRAM: The Transition
──────────────────────────────

Thermal    │                              ╭──────────────
Energy     │                         ╱
(chain     │                    ╱         ← Rubbery plateau
mobility)  │               ╱                (chains mobile)
           │          ╱
           │      ╱        ← TRANSITION ZONE
           │  ╱              (Tg is here)
           │╱
           │────────────────              ← Glassy region
           │                                (chains frozen)
           └───────────────────────────────────────────────►
                          Tg                Temperature

PROPERTY CHANGES AT Tg
──────────────────────

Property        │  Below Tg      │  Above Tg
────────────────┼────────────────┼─────────────────
Stiffness       │  HIGH          │  LOW (1000x drop)
(modulus)       │  (GPa range)   │  (MPa range)
────────────────┼────────────────┼─────────────────
Deformation     │  Elastic       │  Viscoelastic
behavior        │  (springs back)│  (time-dependent)
────────────────┼────────────────┼─────────────────
Under load      │  Holds shape   │  Creeps/sags
────────────────┼────────────────┼─────────────────
Fracture mode   │  Brittle       │  Ductile/rubbery
```

## ASCII Diagrams: What's Actually Happening

**BELOW Tg - Chains are FROZEN (Glassy State)**
```
Temperature: 25C (room temp)
State: RIGID, HARD, BRITTLE

    ~~~~~~~~~~~~~~~~~~~~~~
   /                      \
  /  =====================  \      <-- Chains locked in place
 |   =====================   |         Cannot slide or rotate
 |   =====================   |         Rigid structure maintained
  \  =====================  /
   \                      /
    ~~~~~~~~~~~~~~~~~~~~~~

   [LOAD APPLIED FROM TOP]
           |
           v
    ~~~~~~~~~~~~~~~~~~~~~~
   /                      \        <-- Shape HOLDS!
  /  =====================  \          No deformation
 |   =====================   |
 |   =====================   |
  \  =====================  /
   \                      /
    ~~~~~~~~~~~~~~~~~~~~~~
```

**ABOVE Tg - Chains are MOBILE (Rubbery State)**
```
Temperature: 70C (hot car)
State: SOFT, FLEXIBLE, DEFORMABLE

    ~~~~~~~~~~~~~~~~~~~~~~
   /                      \
  /  ~~~~~~~~~~~~~~~~~~~~~  \      <-- Chains wiggling freely!
 |   ~~~~~~~~~~~~~~~~~~~~~   |         Can slide past each other
 |   ~~~~~~~~~~~~~~~~~~~~~   |         Structure is mobile
  \  ~~~~~~~~~~~~~~~~~~~~~  /
   \                      /
    ~~~~~~~~~~~~~~~~~~~~~~

   [SAME LOAD APPLIED FROM TOP]
           |
           v
    ______________________
   /                      \        <-- Shape DEFORMS!
  / ~~~~~~~~~~~~~~~~~~~~~~ \           Chains slide under stress
 | ~~~~~~~~~~~~~~~~~~~~~~~~ |          Part sags/warps
 | ~~~~~~~~~~~~~~~~~~~~~~~~ |
  \________________________/

         DROOPY MESS
```

## The Hot Car Scenario: PLA vs ABS

```
SCENARIO: 3D-printed phone mount left in car on summer day

OUTSIDE TEMP: 35C (95F)
CAR INTERIOR: 75C (167F) - dashboard even hotter!

+------------------+------------------+
|       PLA        |       ABS        |
+------------------+------------------+
| Tg = ~60C        | Tg = ~105C       |
+------------------+------------------+
| 75C > 60C        | 75C < 105C       |
| ABOVE Tg!        | BELOW Tg!        |
+------------------+------------------+
| Chains mobile    | Chains frozen    |
| Part softens     | Part stays rigid |
+------------------+------------------+

RESULT:

    PLA Mount               ABS Mount
    _________               _________
   /  ___    \             |  ___    |
  |  |   |    |            | |   |   |
  |  |___|   _|            | |___|   |
   \_______/ /             |_________|
    DROOPED!               PERFECT!

   Phone falls,            Phone stays
   mount ruined            mounted
```

## Practical Reference: Common 3D Printing Materials

```
MATERIAL     |  Tg (C)  | SURVIVES HOT CAR? | PRINT DIFFICULTY
-------------|----------|-------------------|------------------
PLA          |   ~60    |       NO          | Easy (beginner)
PETG         |   ~80    |     MAYBE         | Easy-Medium
ABS          |  ~105    |       YES         | Medium (needs enclosure)
ASA          |  ~100    |       YES         | Medium (ABS alternative)
Nylon (PA)   | ~50-70*  |    DEPENDS*       | Hard (hygroscopic)
Polycarbonate|  ~147    |   DEFINITELY      | Hard (high temps)

*Nylon is semi-crystalline; real-world performance depends on crystallinity

HOT CAR INTERIOR TEMPS:
- Cabin air: 60-80C (140-175F)
- Dashboard: 80-100C (175-212F)
- Under windshield: Can exceed 100C!
```

## Decision Flowchart

```
Will your part experience temperatures above 60C?
                    |
         +----------+----------+
         |                     |
        NO                    YES
         |                     |
    Use PLA            Will it exceed 80C?
   (easiest)                   |
                    +----------+----------+
                    |                     |
                   NO                    YES
                    |                     |
               Use PETG           Will it exceed 105C?
             (good balance)              |
                              +----------+----------+
                              |                     |
                             NO                    YES
                              |                     |
                          Use ABS/ASA      Use Polycarbonate
                       (needs heated bed)  (advanced setup)
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

Here's what engineers constantly wrestle with: **plastics that are easy to work with (low Tg) are terrible in heat, while heat-resistant plastics (high Tg) are harder to process**. PLA prints beautifully at low temperatures and smells nice, but its Tg of ~60C means a hot car interior (easily 70-80C) will destroy your print. ABS has a Tg around 105C, so it survives hot cars—but it needs higher printing temps, a heated bed, and releases fumes. Polycarbonate goes even higher (~147C) but demands specialized equipment. The tradeoff is always: how much processing difficulty are you willing to accept for the heat resistance you need? Practitioners argue about whether to add glass fibers (raises effective heat resistance), use annealing (can raise Tg slightly for some materials), or just design around the limitation.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

**The one thing most outsiders get wrong about this is...** thinking that Tg is like a melting point where the plastic suddenly turns liquid. It's not—it's a gradual transition zone where the material goes from "glass-like" to "rubber-like" while still being solid. Your PLA print in a hot car doesn't melt into a puddle; it softens enough that gravity and any stored stress cause it to slowly sag and warp. This is why a PLA part might look fine after an hour in a hot car but be noticeably deformed after a full day—it's creeping under its own weight above its Tg, not melting.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

Related concepts that deepen your understanding of glass transition temperature:

- **[[learning/notes/quick-context/polymer-crystallinity-vs-amorphous]]** — Understanding why amorphous polymers have a distinct Tg while semi-crystalline polymers have both Tg and a melting point (Tm).

- **[[learning/notes/quick-context/melt-index]]** — How polymer flow characteristics relate to processing temperature; a high melt index means easier flow, which connects to how far above Tg you need to go for processing.

- **[[learning/notes/quick-context/3d-printing-filament-types]]** — Practical comparison of filament materials and their Tg values, helping you choose the right material for your application's thermal environment.

- **[[learning/notes/quick-context/polymer-chemical-bonds|Chemical bonds]]** — The molecular-level interactions ([[learning/notes/quick-context/van-der-waals-forces|van der Waals forces]], [[learning/notes/quick-context/hydrogen-bonds-beginners|hydrogen bonds]]) that must be overcome at Tg, explaining why different polymers have different transition temperatures.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A PLA print left in a hot car (75C interior) deforms over several hours. Why doesn't it deform instantly?
<details>
<summary>Answer</summary>
Above Tg, polymer chains gain mobility but don't instantly rearrange. The deformation happens through **creep**—a slow, time-dependent process where chains gradually slide past each other under sustained stress (even just gravity). The longer the exposure, the more the chains have time to reorganize, which is why a part might look okay initially but show significant warping after extended time above Tg.
</details>

**Q2:** PETG has a Tg of ~80C. Would you trust a PETG part for a dashboard-mounted phone holder? Why or why not?
<details>
<summary>Answer</summary>
**No, you shouldn't trust it.** While PETG's Tg of ~80C is above typical car cabin temperatures (60-80C), dashboards can reach 80-100C or higher under direct sunlight. Since Tg marks the *start* of softening, not a hard cutoff, a PETG part at 80C is right at its transition zone and will begin to creep under load. For dashboard applications, ABS (Tg ~105C) or higher is recommended to provide a safety margin.
</details>

**Q3:** Nylon has a relatively low Tg (~50-70C) but is used in demanding automotive applications. How is this possible?
<details>
<summary>Answer</summary>
Nylon is **semi-crystalline**, meaning it has both amorphous regions (which soften at Tg) and crystalline regions (which remain rigid until the melting point Tm, around 220C). The crystalline domains act as physical crosslinks that maintain structural integrity even when the amorphous regions soften. This is why semi-crystalline polymers can perform well above their Tg—their crystallinity provides heat resistance that purely amorphous materials lack.
</details>

**Q4:** You're designing a part that will see 90C operating temperature. You only have PLA filament. What post-processing technique might help, and what are its limitations?
<details>
<summary>Answer</summary>
**Annealing** can help. By heating a PLA print to 80-100C (below its melting point but above Tg), you encourage the polymer chains to reorganize into more crystalline structures. This can raise the effective heat deflection temperature to 80-90C or slightly higher. **Limitations:** Parts may warp or shrink during annealing (especially thin features), dimensional accuracy suffers, and even annealed PLA won't reliably survive sustained 90C—you're pushing it to its absolute limit. For 90C applications, switching to ABS or PETG is the better solution.
</details>

**Q5:** Why does polycarbonate (Tg ~147C) require higher printing temperatures and specialized equipment compared to PLA (Tg ~60C)?
<details>
<summary>Answer</summary>
To extrude a polymer through a 3D printer nozzle, you must heat it well above its Tg to achieve sufficient chain mobility for flow. PLA flows nicely at 180-220C (about 120-160C above its Tg). Polycarbonate, with Tg at 147C, needs temperatures of 260-310C for proper flow. This demands an all-metal hotend (PTFE tubes degrade above ~250C), a heated bed at 100-120C to prevent warping, and often an enclosure to maintain ambient temperature. The same property that makes PC heat-resistant (high Tg from stiff molecular chains) makes it difficult to process.
</details>

</details>
