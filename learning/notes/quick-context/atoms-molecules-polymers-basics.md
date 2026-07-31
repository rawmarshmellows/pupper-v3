---
topic: Atoms, Molecules, and Polymers Basics
created: 2026-01-20
updated: 2026-01-21
---

> **Related:** [[quick-context/covalent-bonds]] | [[quick-context/polymer-crystallinity-vs-amorphous]] | [[quick-context/3d-printing-filament-types]]

> **TL;DR:** Matter builds up in layers (atoms -> molecules -> monomers -> polymers), and 3D printing works by heating thermoplastics enough to let polymer chains slide past each other without breaking them, then cooling to re-lock chains in new positions.

## The Core Problem

Everything physical you touch—including the plastic [[quick-context/3d-printing-filament-types|filament]] feeding into a 3D printer—is made of atoms bonded into increasingly complex structures. Understanding this hierarchy (atoms → molecules → monomers → polymers) explains **why** different filaments behave differently: why PLA melts at 180°C but ABS needs 240°C, why some prints are brittle and others flexible, why layer adhesion fails or succeeds. Without this foundation, you're just memorizing temperature settings without understanding the "why." If polymers didn't exist, we'd have no plastics, no rubber, no nylon—essentially no modern manufacturing. The entire 3D printing industry depends on our ability to melt polymer chains, extrude them through a nozzle, and have them re-solidify into a solid object.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **[[quick-context/subatomic-particles\|Atom]]** | The smallest unit of an element (like carbon or hydrogen) that retains that element's chemical properties; made of [[quick-context/subatomic-particles\|protons, neutrons, and electrons]]. |
| **Molecule** | Two or more atoms bonded together; water (H₂O) is a molecule of 2 hydrogen atoms + 1 oxygen atom. |
| **Monomer** | A small molecule that can bond repeatedly to form long chains; the "building block" unit. |
| **Polymer** | A long chain made of many monomers bonded together; plastics are polymers. |
| **Thermoplastic** | A polymer that softens when heated (above its [[quick-context/glass-transition-temperature\|glass transition temperature]]) and hardens when cooled, repeatedly—this is what makes [[quick-context/3d-printing-filament-types\|3D printing]] possible. |

<details>
<summary><strong>How It Works</strong></summary>

Matter builds up in layers of increasing complexity, and each layer determines different properties. At the base, atoms are the fundamental units—protons and neutrons in a nucleus, surrounded by electrons. Atoms bond together by sharing or transferring electrons, forming molecules. When a molecule has reactive "ends" that can link to other identical molecules, we call it a monomer—the building block for polymers. Through polymerization reactions, hundreds to thousands of monomers link end-to-end into long chains called polymers. The properties of the final plastic (strength, flexibility, melting point) emerge from three factors: (1) what the monomer is (determines backbone chemistry), (2) how long the chains are (determines entanglement and strength), and (3) how the chains pack together (crystalline regions are rigid; amorphous regions are flexible).

In 3D printing, you exploit the thermoplastic property: heating gives polymer chains enough energy to overcome the weak intermolecular forces (van der Waals, hydrogen bonds) that hold them in place. The chains don't break—they just gain mobility to slide past each other, allowing the material to flow through the nozzle. Upon cooling, chains lose energy, intermolecular forces reassert themselves, and chains lock into new positions. The extruded material solidifies. Crucially, if chains from the new layer can interpenetrate with chains from the previous layer before cooling, you get strong layer adhesion—the layers literally tangle together at the molecular level. If the previous layer is too cold, chains can't intermix, and you get weak layer bonds.

```
THE HIERARCHY OF MATTER → POLYMERS
══════════════════════════════════════════════════════════════════════════════

    SCALE          WHAT IT IS                    WHAT DETERMINES PROPERTIES
    ─────          ──────────                    ──────────────────────────

    ATOM           ●  (carbon, hydrogen,         Element type (C, H, O, N...)
    ~0.1 nm           oxygen, nitrogen)          determines bonding behavior
                       │
                       │ share electrons
                       ▼
    MOLECULE       ●─●─●  (water, CO₂,          Atom arrangement determines
    ~0.1-1 nm          lactic acid)             reactivity, polarity
                       │
                       │ reactive ends link
                       ▼
    MONOMER        [●─●─●]  (single unit        Functional groups determine
    ~0.5-2 nm          with linkable ends)      polymerization type
                       │
                       │ repeat 100s-1000s×
                       ▼
    POLYMER        [M]─[M]─[M]─[M]─[M]─...      Chain length, branching,
    ~10-1000 nm    (one long chain)             and chemistry determine
                       │                         mechanical properties
                       │ many chains tangle
                       ▼
    BULK           ∿∿∿∿∿∿∿∿∿∿∿∿∿                Crystallinity, chain
    PLASTIC        ∿∿∿∿∿∿∿∿∿∿∿∿∿                entanglement, and
    mm-cm scale    (tangled spaghetti)          additives determine
                                                 final material behavior


HOW 3D PRINTING EXPLOITS THIS HIERARCHY:
══════════════════════════════════════════════════════════════════════════════

SOLID FILAMENT                MELTED IN NOZZLE              SOLIDIFIED LAYER
(room temperature)            (~200°C)                      (cooling on bed)

┌────────────────┐           ┌────────────────┐           ┌────────────────┐
│ ════════════   │           │ ∿  ∿  ∿  ∿  ∿  │           │ ════════════   │
│ ════════════   │   HEAT    │ ∿  ∿  ∿  ∿  ∿  │   COOL    │ ════════════   │
│ ════════════   │  ═════►   │ ∿  ∿  ∿  ∿  ∿  │  ═════►   │ ════════════   │
│ ════════════   │           │ ∿  ∿  ∿  ∿  ∿  │           │ ════════════   │
│ ════════════   │           │ ∿  ∿  ∿  ∿  ∿  │           │ ════════════   │
└────────────────┘           └────────────────┘           └────────────────┘

 Chains locked by             Chains have energy          Chains re-lock in
 intermolecular forces        to slide freely             NEW configuration!
 (van der Waals,              (can flow through
 hydrogen bonds)               nozzle)

      BONDS THAT BREAK/REFORM:              BONDS THAT STAY INTACT:
      ─────────────────────────             ──────────────────────
      • Van der Waals (weak)                • Covalent bonds in
      • Hydrogen bonds (medium)               polymer backbone
      → Break with ~150-250°C               → Require ~400°C+ to break
      → Reform upon cooling                 → Chains stay whole!

      This is why thermoplastics are RECYCLABLE and REPRINTABLE
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The central tradeoff in polymer science is **molecular weight** (chain length) vs. **ease of processing**. Longer polymer chains = stronger final parts with better mechanical properties, but also = higher melting temperatures and more viscous (thick) melts that are harder to extrude. Practitioners constantly balance: do you want a filament that prints easily at low temps but produces weaker parts, or one that's difficult to print but yields industrial-strength results? This is why "printing temperature" isn't just a number—it's a negotiation between your printer's capabilities and the polymer's chain characteristics. Additives, blends, and co-polymers exist largely to cheat this tradeoff.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Here's the hierarchy visualized with ASCII diagrams:

```
LEVEL 1: ATOMS (the smallest pieces)
==========================================

    H           C           O
   (.)        (●)         (@)
  Hydrogen   Carbon      Oxygen

  These are individual atoms - the LEGO bricks of matter.
  Carbon has 6 protons, Oxygen has 8, Hydrogen has 1.


LEVEL 2: MOLECULES (atoms bonded together)
==========================================

  Water molecule (H₂O):        Carbon dioxide (CO₂):

       H                           O === C === O
        \
         O                        (one carbon double-bonded
        /                          to two oxygens)
       H

  Atoms share electrons to form bonds (the lines).


LEVEL 3: MONOMERS (special molecules that can link up)
======================================================

  Lactic Acid monomer (the building block of PLA):

           O
           ‖
      H₃C—C—O—H        <-- This -O-H group and
          |                the =O group can react
          H                with OTHER lactic acid
          |                molecules!
         O—H

  Key insight: Monomers have "reactive sites" that
  let them grab onto other monomers.


LEVEL 4: POLYMER CHAINS (many monomers linked together)
=======================================================

  PLA = Poly(lactic acid) = MANY lactic acids linked:

  [M]—[M]—[M]—[M]—[M]—[M]—[M]—[M]—[M]—[M]—[M]—[M]...
   └─────────────────────────────────────────────────┘
            One polymer chain (thousands of M's)

  Where each [M] is one lactic acid monomer.


  Zoomed out view of polymer chains in solid plastic:

     ~~~~~/\~~~~\/~~~~~~/\/\~~~~
    ~~~~/\/\~~~~~/\~~~~/\~~~~~~~
   ~~~~~~~/\/\/\~~~~~/\/\/\~~~~~
    ~~~~~\/~~~~~~\/\/~~~~~~\/~~~

  Chains tangle together like cooked spaghetti.
  This tangling = mechanical strength!


THE 3D PRINTING PROCESS (what heat does):
=========================================

  COLD (solid filament):        HOT (melted in nozzle):

  Chains locked together        Chains slide past each other

   |||||||||||||||||            ~  ~  ~  ~  ~  ~
   |||||||||||||||||            ~  ~  ~  ~  ~  ~
   |||||||||||||||||     →→→    ~  ~  ~  ~  ~  ~
   |||||||||||||||||    HEAT    ~  ~  ~  ~  ~  ~
   |||||||||||||||||            ~  ~  ~  ~  ~  ~

   (rigid, organized)           (flowing, disordered)

                    COOLING
                      ↓↓↓

                 |||||||||||||
                 |||||||||||||  ← Chains re-lock
                 |||||||||||||    into new shape!
```

**Real-world chain lengths:**
- PLA: ~700-2000 monomer units per chain
- ABS: ~1000-3000 monomer units per chain
- Nylon: ~100-300 monomer units per chain (but very strong bonds between chains)

```
WHY DIFFERENT FILAMENTS BEHAVE DIFFERENTLY:
==========================================

PLA chains:                    ABS chains:

[M]-[M]-[M]-[M]-[M]           [M]--[M]--[M]--[M]--[M]
                                   |
Simple, straight chains.           [branch]
Easy to melt (180-220°C).          |
Brittle when cold.            Branched, tangled chains.
                              Needs more heat (220-250°C).
                              More impact-resistant.
```

**The one thing most outsiders get wrong about this is...** thinking that melting plastic "breaks" something. In reality, heating a thermoplastic just gives the polymer chains enough energy to wiggle free and slide past each other—the chains themselves stay intact. This is why you can melt and re-solidify PLA dozens of times (it's the same chains re-tangling). The atoms, the monomers, the chains—they're all still there. You're just rearranging how they're packed together. This reversibility is the entire foundation of FDM 3D printing.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- [[quick-context/covalent-bonds]] — The primary bond type holding atoms together within molecules and polymer chains; understanding [[learning/notes/quick-context/covalent-bonds|covalent bonds]] explains why polymer chains are strong but the material can still melt.
- [[quick-context/polymer-chemical-bonds|Chemical bonds]] — Deeper dive into the specific bond types that form polymer backbones and crosslinks; essential for understanding thermosets vs. thermoplastics.
- [[quick-context/hydrogen-bonds-beginners|Hydrogen bonds]] — Weak attractions between chains that affect melting point and layer adhesion; explains why nylon absorbs moisture and prints differently when wet.
- [[quick-context/van-der-waals-forces|Van der Waals forces]] — The weakest intermolecular forces, but they add up across long polymer chains; crucial for understanding why longer chains = stronger parts.
- [[quick-context/biology-fundamentals]] — Biological macromolecules (proteins, DNA, carbohydrates) are polymers following the same chemical principles as synthetic polymers, but organized for self-replication and metabolism.
- [[quick-context/subatomic-particles]] — The fundamental building blocks (protons, neutrons, electrons, quarks) that make up atoms; explains why different elements have different numbers of bonds and chemical behaviors.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What is the difference between a molecule and a polymer?
<details>
<summary>Answer</summary>
A molecule is simply two or more atoms bonded together (like water, H₂O). A polymer is a specific type of molecule: a very long chain made of many repeating units (monomers) bonded together. All polymers are molecules, but most molecules are not polymers. The key distinction is the repeating structure and extreme length—polymers typically contain hundreds to thousands of monomer units.
</details>

**Q2:** Why can thermoplastics be melted and re-solidified repeatedly without degrading?
<details>
<summary>Answer</summary>
When you heat a thermoplastic, you're not breaking the [[quick-context/covalent-bonds|covalent bonds]] within the polymer chains—you're just giving the chains enough energy to overcome the weaker intermolecular forces ([[quick-context/van-der-waals-forces|van der Waals]], [[quick-context/hydrogen-bonds-beginners|hydrogen bonds]]) that hold them in place relative to each other. The chains slide past each other when hot, then re-tangle and lock together when cooled. The actual polymer chains remain chemically intact throughout this process.
</details>

**Q3:** Why do longer polymer chains generally produce stronger parts but require higher printing temperatures?
<details>
<summary>Answer</summary>
Longer chains have more contact points with neighboring chains, creating more intermolecular attractions ([[learning/notes/quick-context/van-der-waals-forces|van der Waals forces]]) that hold the solid together—hence parts with greater [[quick-context/tensile-strength-materials|tensile strength]]. However, those same additional attractions mean you need more thermal energy to free the chains from each other, resulting in higher melting/processing temperatures and more viscous melts that are harder to extrude.
</details>

**Q4:** A print has poor layer adhesion. Using what you know about polymer chains, what might be happening at the molecular level?
<details>
<summary>Answer</summary>
Poor layer adhesion suggests that polymer chains from the new layer are not sufficiently interpenetrating (tangling with) chains from the previous layer. This could happen if: (1) the previous layer cooled too much before the new layer was deposited, so chains couldn't intermingle; (2) the extrusion temperature is too low, so chains lack mobility; or (3) the polymer type has weak intermolecular forces between chains. At the molecular level, strong layer bonds require chains from both layers to physically interweave across the interface.
</details>

**Q5:** PLA and ABS are both thermoplastics, yet ABS requires higher printing temperatures. Based on chain structure, why might this be?
<details>
<summary>Answer</summary>
ABS has branched, more tangled chain structures compared to PLA's relatively straight chains. Branched chains create more inter-chain entanglements and contact points, requiring more thermal energy to free them and allow flow. Additionally, ABS is a copolymer (acrylonitrile, butadiene, styrene) with different monomer types contributing different intermolecular interactions, while PLA is made from a single monomer type (lactic acid) with more uniform, and apparently weaker, intermolecular forces.
</details>

</details>
