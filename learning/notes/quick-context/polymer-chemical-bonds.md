---
topic: Polymer Chemical Bonds in 3D Printing Filaments
created: 2026-01-20
updated: 2026-01-21
---

> **Related:** [[learning/notes/quick-context/covalent-bonds]] | [[learning/notes/quick-context/dipole-dipole-interactions]] | [[learning/notes/quick-context/glass-transition-temperature]] | [[learning/notes/quick-context/pi-pi-stacking-aromatic-interactions]] | [[learning/notes/quick-context/van-der-waals-forces]]

> **TL;DR:** Polymer behavior (melt temperature, flexibility, layer adhesion) is governed by intermolecular forces between chains - van der Waals (weak), dipole-dipole (moderate), and hydrogen bonds (strong). Understanding these forces explains why PLA melts at 180C but ABS needs 240C, and why TPU flexes while PLA snaps.

# Polymer Chemical Bonds: Quick Context for 3D Printing Filaments

## The Core Problem

Understanding [[quick-context/chemical-bonds-spectrum|chemical bonds]] explains *why* PLA melts at 180°C but ABS needs 240°C, why TPU flexes while PLA snaps, and why PETG survives in a hot car but PLA deforms. Every [[quick-context/atoms-molecules-polymers-basics|polymer]] is a chain of repeating molecular units (monomers) held together by **[[quick-context/covalent-bonds|covalent bonds]]** (strong, electron-sharing bonds within the chain). But the *behavior* of the bulk material—melt temperature, flexibility, layer adhesion—is governed by **intermolecular forces** between chains: [[quick-context/van-der-waals-forces|van der Waals forces]] (weak, universal), [[quick-context/dipole-dipole-interactions|dipole-dipole interactions]] (moderate, from polar groups), and [[quick-context/hydrogen-bonds-beginners|hydrogen bonds]] (strong, from O-H or N-H groups). Without understanding these forces, filament selection is just memorizing temperature tables. PLA has ester groups that hydrogen-bond moderately, keeping chains locked until ~180°C. ABS has aromatic rings (benzene) that stack via strong π-π interactions, requiring ~240°C to mobilize chains. TPU is a segmented copolymer—"hard segments" (urethane linkages with strong H-bonds) and "soft segments" (flexible polyol chains)—creating an elastomer that bounces back after deformation. PETG's glycol modification disrupts crystallization, keeping it amorphous and transparent while maintaining decent intermolecular cohesion.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Covalent bond** | Strong electron-sharing bond holding atoms together within molecules—breaking these (>300°C) means degradation, not melting; printing operates below this threshold. |
| **Hydrogen bond** | Moderate intermolecular attraction between H attached to O/N and a nearby O/N—gives PLA its moderate Tg, gives TPU hard segments their cohesion, gives Nylon its strength and hygroscopicity. |
| **Van der Waals forces** | Weak, universal attractions between all molecules from temporary electron fluctuations—always present but only dominant when stronger forces are absent (like in PE/PP). |
| **[[quick-context/glass-transition-temperature|Glass transition temperature]] (Tg)** | The temperature where amorphous regions mobilize and the polymer softens—controlled entirely by intermolecular force strength; below Tg = glassy/rigid, above Tg = rubbery/flexible. |
| **[[quick-context/polymer-crystallinity-vs-amorphous|Crystallinity]]** | Degree of ordered chain packing—higher crystallinity = stronger intermolecular forces = higher shrinkage/warping; PETG's "G" (glycol) intentionally disrupts this for easier printing. |

<details>
<summary><strong>How It Works</strong></summary>

Polymer behavior emerges from a two-level bonding hierarchy. At the first level, strong covalent bonds link atoms into long chains—the polymer backbone. These bonds are so strong (300-400 kJ/mol) that they never break during normal 3D printing; breaking them means burning the plastic. At the second level, weaker intermolecular forces hold neighboring chains together. When you heat filament, you're adding enough thermal energy to overcome these weaker forces, allowing chains to slide past each other and flow. The type and strength of intermolecular forces present determine the exact temperature needed.

The printing process is essentially: heat to break intermolecular forces (chains become mobile), extrude the flowing polymer, then cool to re-establish intermolecular forces (chains lock in place). Layer adhesion depends on chains from the new layer entangling and forming intermolecular bonds with chains from the previous layer before cooling "freezes" them apart. Materials with stronger intermolecular forces (like ABS's aromatic stacking) create stronger layer bonds—but also require higher temperatures to achieve that chain mobility in the first place.

```
POLYMER BONDING HIERARCHY: TWO LEVELS OF "STICKINESS"
================================================================================

LEVEL 1: WITHIN CHAINS (Covalent Bonds)
─────────────────────────────────────────────────────────────────────────────────
    Strong electron-sharing bonds hold atoms together into polymer chains.
    Energy: 300-400 kJ/mol  |  NEVER broken during printing

    ───●───●───●───●───●───●───●───●───●───●───●───●───●───  Chain 1
           covalent bonds (very strong)

    ───●───●───●───●───●───●───●───●───●───●───●───●───●───  Chain 2


LEVEL 2: BETWEEN CHAINS (Intermolecular Forces)
─────────────────────────────────────────────────────────────────────────────────
    Weaker attractions between neighboring chains determine material behavior.
    Energy: 2-40 kJ/mol  |  THESE are what you overcome when melting

    ───●───●───●───●───●───●───●───●───●───●───●───●───●───  Chain 1
           :     :     :     :     :     :     :
           :     :     :     :     :     :     :   intermolecular
           :     :     :     :     :     :     :   forces (weaker)
           :     :     :     :     :     :     :
    ───●───●───●───●───●───●───●───●───●───●───●───●───●───  Chain 2


WHAT HAPPENS DURING PRINTING:
─────────────────────────────────────────────────────────────────────────────────

   COLD (below Tg)              HEATED (above Tg)              COOLED (printed)
   Chains locked                Chains mobile                  Chains re-locked

   ═══●═══●═══●═══              ~~~●~~~●~~~●~~~                ═══●═══●═══●═══
       :::::                         (free)                       :::::
   ═══●═══●═══●═══              ~~~●~~~●~~~●~~~                ═══●═══●═══●═══
       :::::                         (flow)                       ::::: NEW
   ═══●═══●═══●═══              ~~~●~~~●~~~●~~~                ═══●═══●═══●═══
                                                                  :::::  LAYER
   rigid,                       viscous,                      ═══●═══●═══●═══
   intermolecular               flows through                    BONDS
   bonds intact                 nozzle                        interlocked

   ═ covalent (never breaks)    ~ chain in motion             : intermolecular
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The fundamental tradeoff is **intermolecular force strength vs. processability vs. flexibility**. Stronger intermolecular forces (more hydrogen bonding, [[quick-context/pi-pi-stacking-aromatic-interactions|π-π stacking]]) mean higher [[quick-context/glass-transition-temperature|Tg]], better heat resistance, and stronger layer adhesion—but also higher print temperatures, more warping (thermal stress), and brittleness. Weaker forces mean easier printing but parts that fail in warm environments. [[quick-context/polymer-crystallinity-vs-amorphous|Crystallinity]] adds another axis: semi-crystalline polymers (like unmodified PET) pack into ordered regions with stronger interactions, improving strength and heat resistance but causing dramatic shrinkage (warping). Amorphous polymers (PETG, ABS) stay disordered, shrink less, but have no sharp melting point—they gradually soften. TPU cheats the system by being phase-separated: hard crystalline domains act as physical crosslinks providing strength, while soft amorphous regions provide elasticity. Practitioners argue about whether ABS's aromatic strength is "worth" the fumes and warping, whether PETG's glycol modification sacrifices too much crystallinity for the convenience, and whether TPU's hydrogen-bonded hard segments can ever match vulcanized rubber's covalently-crosslinked durability.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

How bond chemistry maps to filament behavior:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MOLECULAR STRUCTURE → PRINTING BEHAVIOR                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PLA: Polylactic Acid                                                       │
│  ─────────────────────                                                      │
│     O    O    O                                                             │
│     ‖    ‖    ‖       ← Ester groups (C=O) enable moderate H-bonding        │
│  ~O-C-CH-O-C-CH-O-C~     between chains                                     │
│       |       |                                                             │
│      CH₃    CH₃       → Tg: 55-60°C (moderate intermolecular forces)        │
│                       → Crystallizes slowly → low warping                   │
│                       → Biodegradable (ester hydrolysis)                    │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ABS: Acrylonitrile-Butadiene-Styrene                                      │
│  ───────────────────────────────────                                        │
│       ⬡            ≡N                                                       │
│       |            |    ← Benzene rings (⬡): strong π-π stacking           │
│  ~CH₂-CH~  ~CH₂-CH~     ← Nitrile groups (≡N): strong dipole-dipole        │
│   styrene   acrylo-                                                         │
│             nitrile  → Tg: ~105°C (strong intermolecular forces)            │
│                      → Amorphous but still warps (high thermal stress)      │
│  + butadiene rubber  → Butadiene provides toughness (impact modifier)       │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PETG: Polyethylene Terephthalate + Glycol                                  │
│  ─────────────────────────────────────────                                  │
│      O       O                                                              │
│      ‖   ⬡   ‖         ← Aromatic ring + ester groups                       │
│  ~O-C───────C-O-CH₂-CH₂-O~                                                  │
│                 |                                                           │
│                OH      ← Glycol modification: disrupts crystallization      │
│                                                                             │
│                       → Tg: ~75°C (balanced forces)                         │
│                       → Amorphous = transparent, low shrinkage              │
│                       → Glycol -OH = slightly hygroscopic                   │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TPU: Thermoplastic Polyurethane                                            │
│  ───────────────────────────────                                            │
│         O   H       O   H                                                   │
│         ‖   |       ‖   |   ← HARD SEGMENT: urethane linkages               │
│  ~N-C-O-────N-C-O-~         Strong H-bonds between N-H and C=O              │
│    |           |            Forms crystalline domains                       │
│   ─R─         ─R─                                                           │
│                                                                             │
│  ~O-CH₂-CH₂-O-CH₂-CH₂-O~   ← SOFT SEGMENT: polyether/polyester chain        │
│                             Weak van der Waals only                         │
│                             Flexible, amorphous                             │
│                                                                             │
│  PHASE SEPARATION:  [hard]═══[soft]═══[hard]═══[soft]═══[hard]              │
│                       ↓                  ↓                                  │
│                   physical            elasticity                            │
│                   crosslinks          & flexibility                         │
│                                                                             │
│                       → No single Tg—behaves rubbery at room temp           │
│                       → Hard segments: H-bond strength → reprocessable      │
│                       → Shore 95A: more hard segment, stiffer               │
│                       → Shore 70A: more soft segment, more flexible         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Why layer adhesion varies by material:**

| Material | Primary Intermolecular Force | Layer Adhesion Mechanism |
|----------|------------------------------|--------------------------|
| PLA | H-bonds via ester C=O | Moderate—chains entangle as layers fuse at ~200°C |
| ABS | π-stacking + dipole-dipole | Excellent—aromatic rings interlock across layer boundary |
| PETG | H-bonds + π-stacking | Very good—glycol -OH groups actively H-bond to adjacent layers |
| TPU | H-bonds (urethane) | Excellent—hard segments in adjacent layers H-bond strongly |

**The one thing most outsiders get wrong about this is...** thinking that higher print temperatures mean "stronger" parts. Temperature only mobilizes chains for layer fusion—actual *strength* comes from intermolecular forces that re-establish as the layer cools. ABS prints hotter than PLA but doesn't necessarily make stronger parts; it makes parts that *survive heat better* because ABS's π-stacking is stronger than PLA's ester H-bonding. And TPU's flexibility isn't "weakness"—it's the deliberate phase separation of hard and soft segments, engineered at the molecular level to behave like crosslinked rubber without actually being crosslinked (which is why it's thermoplastic and printable at all).

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

Concepts that deepen understanding of polymer chemical bonds:

- **[[quick-context/covalent-bonds]]** — The strong electron-sharing bonds forming the polymer backbone; understanding these explains why degradation (chain breaking) is different from melting (chain mobilization).
- **[[quick-context/hydrogen-bonds-beginners]]** — The key intermolecular force in PLA, TPU hard segments, and Nylon that determines Tg, layer adhesion, and hygroscopicity.
- **[[quick-context/van-der-waals-forces]]** — The weak universal forces that dominate in non-polar polymers like PE/PP; understanding these explains why polyethylene is so slippery and low-melting.
- **[[quick-context/pi-pi-stacking-aromatic-interactions]]** — The aromatic ring interactions that give ABS and PETG their elevated Tg and heat resistance.
- **[[quick-context/polymer-crystallinity-vs-amorphous]]** — How chain packing affects shrinkage, transparency, and thermal behavior; explains why PETG's glycol modification matters.
- **[[small-context/glass-vs-plastic-uv-degradation]]** — What happens when UV breaks the same C–C backbone bonds that hold polymer chains together: free-radical chain reaction with O₂ causes yellowing, embrittlement, and fragmentation.
- **[[quick-context/bambu-p2s-print-quality]]** — Layer adhesion in 3D printing is exactly chain interdiffusion across layer boundaries via these same intermolecular forces; viscoelastic melt behavior driven by chain entanglement is why pressure advance (K-value) calibration is needed per filament.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does PLA deform in a hot car (~60°C) while ABS parts survive?
<details>
<summary>Answer</summary>
PLA has a glass transition temperature (Tg) of only 55-60°C because its ester groups form moderate hydrogen bonds between chains. Above Tg, the amorphous regions mobilize and the material softens. ABS has a Tg of ~105°C because its aromatic rings (benzene) engage in strong π-π stacking interactions, requiring significantly more thermal energy to mobilize chains. A hot car interior easily exceeds PLA's Tg but stays well below ABS's.
</details>

**Q2:** TPU is flexible and elastic, yet it has strong hydrogen bonds. How is this possible?
<details>
<summary>Answer</summary>
TPU achieves elasticity through phase separation. It contains "hard segments" (urethane linkages with strong H-bonds that form crystalline domains) and "soft segments" (flexible polyether/polyester chains with only weak van der Waals forces). The hard segments act as physical crosslinks providing structural integrity, while the soft segments provide the flexibility and elastic recovery. This is different from a homogeneous material where strong H-bonds would make it rigid throughout.
</details>

**Q3:** What does the "G" in PETG actually do at the molecular level?
<details>
<summary>Answer</summary>
The "G" stands for glycol modification. Standard PET (polyethylene terephthalate) is semi-crystalline—its chains pack into ordered crystalline regions that create strong intermolecular forces but also cause dramatic shrinkage during cooling (warping). The glycol modification introduces irregular side groups that physically prevent chains from packing into crystals. This keeps PETG amorphous: transparent, lower shrinkage, easier to print, but with a slightly lower Tg and heat resistance compared to crystalline PET.
</details>

**Q4:** Why does Nylon absorb moisture while PLA (also with oxygen-containing groups) absorbs much less?
<details>
<summary>Answer</summary>
Nylon contains amide groups (-NH-C=O-) with both N-H donors and C=O acceptors for hydrogen bonding. Water molecules can directly hydrogen bond to these amide groups, inserting between polymer chains and plasticizing the material. PLA has ester groups (-C=O-O-) which can only act as H-bond acceptors (no N-H or O-H donors). While PLA can absorb some moisture, it lacks the strong donor-acceptor combination that makes Nylon so hygroscopic. The N-H group in Nylon is the key difference.
</details>

**Q5:** ABS prints at ~240°C while PLA prints at ~200°C, but ABS doesn't necessarily make stronger parts. Explain why.
<details>
<summary>Answer</summary>
Print temperature only determines how well polymer chains mobilize for layer fusion—it doesn't determine final part strength. What matters is the strength of intermolecular forces that re-establish as the layer cools. ABS's higher print temperature is needed to overcome its strong π-π stacking and dipole-dipole interactions. Once cooled, those same forces provide excellent layer adhesion and heat resistance, but not necessarily higher ultimate tensile strength than PLA. In fact, PLA often has higher tensile strength than ABS—ABS's advantage is impact resistance (from the butadiene rubber phase) and thermal performance, not raw strength.
</details>

</details>
