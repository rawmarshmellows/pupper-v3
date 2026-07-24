---
topic: Hydrogen Bonds for Beginners (PLA vs TPU Explained)
created: 2026-01-20
updated: 2026-01-21
---

> **Related:** [[quick-context/covalent-bonds|Covalent Bonds]] | [[quick-context/glass-transition-temperature|Glass Transition Temperature]] | [[quick-context/atoms-molecules-polymers-basics|Atoms, Molecules, and Polymers Basics]] | [[quick-context/dipole-dipole-interactions|Dipole-Dipole Interactions]] | [[quick-context/polymer-chemical-bonds|Polymer Chemical Bonds in 3D Printing Filaments]]

> **TL;DR:** Hydrogen bonds are weak attractions between H atoms and O/N atoms on neighboring chains—TPU is flexible because it concentrates these bonds in "hard segments" while leaving "soft segments" free to stretch, whereas PLA's uniform bonding makes it rigid and brittle.

# Hydrogen Bonds: Why PLA Snaps and TPU Bounces

## The Core Problem (Zero Chemistry Background Required)

Imagine you have a bowl of spaghetti. The individual noodles are "polymer chains" - long strings of atoms connected together. Now the question is: **what holds those noodles together as a clump?** If the noodles slide past each other easily, you get a flexible, bendy material (like TPU). If they're stuck together tightly, you get a stiff, rigid material (like PLA). The "stickiness" between chains comes from **hydrogen bonds** - a special kind of attraction that happens when a hydrogen atom on one chain gets close to an oxygen or nitrogen atom on a neighboring chain. Understanding this one concept explains why PLA is rigid and brittle while TPU is rubbery and flexible, even though both are made of similar-sized polymer chains.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Hydrogen bond** | A weak attraction between a hydrogen atom (slight +) and an oxygen or nitrogen atom (slight -) on a neighboring molecule—it's the "velcro" holding polymer chains together |
| **Hard segment** | In TPU, the urethane-rich portion with dense H-bonding that forms rigid anchor points—these are the "knots" that give TPU its strength |
| **Soft segment** | In TPU, the flexible chain sections with minimal H-bonding—these "springs" allow stretching and provide elasticity |
| **Crystalline domain** | A region where polymer chains pack together in an ordered, repeating pattern due to strong intermolecular attractions—hard segments form these |
| **Phase separation** | The phenomenon where hard and soft segments naturally segregate into distinct regions rather than mixing—this is WHY TPU works as an elastomer |

<details>
<summary><strong>How It Works</strong></summary>

Hydrogen bonds form because of unequal electron sharing within molecules. When hydrogen bonds to oxygen or nitrogen (via a strong covalent bond), the oxygen or nitrogen hogs the shared electrons, leaving hydrogen with a slight positive charge and the O or N with a slight negative charge. This creates a "polar" bond with a positive end and a negative end. When a positively-charged hydrogen on one molecule gets close to a negatively-charged oxygen or nitrogen on a different molecule, they attract each other electrostatically. This attraction is the hydrogen bond—it is much weaker than the [[quick-context/covalent-bonds|covalent bonds]] holding atoms together within molecules, but strong enough to significantly affect how materials behave.

The key to understanding hydrogen bonds is recognizing the players: you need a "donor" (an H attached to O or N, making it slightly positive) and an "acceptor" (a lone O or N with negative charge that attracts the H). The hydrogen essentially acts as a bridge between two electronegative atoms. Water is the classic example: each water molecule can donate two hydrogen bonds (from its two H atoms) and accept two hydrogen bonds (at its oxygen), creating an extensive network that explains water's unusually high boiling point and surface tension.

```
HOW HYDROGEN BONDS FORM: Step by Step
══════════════════════════════════════════════════════════════════════════

Step 1: UNEQUAL SHARING creates partial charges
────────────────────────────────────────────────

    Within a COVALENT bond (strong, holds atoms together):

         O═══════H            Oxygen "hogs" the shared electrons
         │       │            ───────────────────────────────────
      (δ-)    (δ+)            δ- = partial negative (electron-rich)
                              δ+ = partial positive (electron-poor)

    Same happens with N-H bonds:

         N═══════H
         │       │
      (δ-)    (δ+)


Step 2: OPPOSITE CHARGES ATTRACT across molecules
──────────────────────────────────────────────────

    Molecule 1                        Molecule 2
    ══════════                        ══════════

         ┌─────── covalent bond (STRONG, ~400 kJ/mol)
         │
         ▼
        O───H                         O───H
        │   │                         │   │
     (δ-)  (δ+)  ←── ATTRACTION ──→ (δ-)  (δ+)
                         │
                         │
                         ▼
                 HYDROGEN BOND forms!
                 (WEAK, ~20 kJ/mol)


Step 3: THE HYDROGEN BOND - A bridge between molecules
───────────────────────────────────────────────────────

               covalent bond           covalent bond
               (within mol.)           (within mol.)
                    │                       │
                    ▼                       ▼
    Molecule 1:    O ─── H ┄┄┄┄┄┄┄┄┄ O ─── H    :Molecule 2
                   │           │           │
                (δ-)        (δ+)        (δ-)
                   │           │           │
                   └───────────┼───────────┘
                               │
                         H-BOND HERE
                    (~2.8 Angstroms long)

    Key: ─── = covalent bond (strong, permanent)
         ┄┄┄ = hydrogen bond (weak, breaks/reforms constantly)


DONORS AND ACCEPTORS: The Two Players
══════════════════════════════════════════════════════════════════════════

    DONOR: Provides the hydrogen          ACCEPTOR: Attracts the hydrogen
    ═══════════════════════════           ═════════════════════════════════

    Must be H attached to O or N          Must be O or N with available
                                          electrons (lone pairs)

         O ─── H  ──────────┄┄┄┄┄┄┄┄┄┄┄┄──────────  O
         │     │                                    │
      (pulls e-)  (δ+)       H-bond            (δ-)(has lone pairs)
               │      ←─────────────────→           │
            DONOR                              ACCEPTOR


    WATER: The Perfect H-Bond Molecule
    ───────────────────────────────────
    Each water can be BOTH donor AND acceptor:

                    can ACCEPT
                    2 H-bonds
                        │
                        ▼
              H ┄┄┄┄┄┄  O  ┄┄┄┄┄┄ H
                       / \
                      H   H
                      │   │
                      ▼   ▼
                 can DONATE
                 2 H-bonds

    Result: Water forms a 3D NETWORK of H-bonds
            (This is why water has high boiling point!)


IN POLYMERS: H-Bonds Hold Chains Together
══════════════════════════════════════════════════════════════════════════

    SINGLE H-BOND: Weak (like one piece of velcro)
    ───────────────────────────────────────────────

    Chain A: ───────── O ─────────────────────
                       │
                       H
                       ┊     ← easy to pull apart
                       ┊
                       O
                       │
    Chain B: ───────────────────────────────────


    MANY H-BONDS: Strong (like a strip of velcro)
    ──────────────────────────────────────────────

    Chain A: ──O──H┄┄┄O──H┄┄┄O──H┄┄┄O──H┄┄┄O──
               ┊     ┊     ┊     ┊     ┊
               ┊     ┊     ┊     ┊     ┊     ← HARD to pull apart!
               ┊     ┊     ┊     ┊     ┊       Many weak bonds
               H     H     H     H     H       = strong connection
               │     │     │     │     │
    Chain B: ──O─────O─────O─────O─────O──────


    WHY THIS MATTERS FOR MATERIALS:

    ┌────────────────────────────────────────────────────┐
    │  More H-bonds between chains = STIFFER material    │
    │  Fewer H-bonds between chains = FLEXIBLE material  │
    └────────────────────────────────────────────────────┘
```

## What IS a Hydrogen Bond? (The Simple Version)

First, atoms. Everything is made of atoms. For our purposes, you only need three:

```
   HYDROGEN (H)     OXYGEN (O)      NITROGEN (N)
   ~~~~~~~~~~~~     ~~~~~~~~~~      ~~~~~~~~~~~~

   Tiny, positive    Bigger,         Bigger,
   "sticks out"      negative        negative
   from chains       "attracts H"    "attracts H"
```

Here's the key insight: **Hydrogen has a slight positive charge, while Oxygen and Nitrogen have slight negative charges.** Opposites attract. When an H gets close to an O or N on a *different* chain, they pull toward each other:

```
HYDROGEN BOND = Attraction between H and O (or H and N)
===========================================================

         Chain 1                    Chain 2
        ~~~~~~~~~~                 ~~~~~~~~~~
             |                          |
             H  <-- slight (+)          |
              \                        /
               \    ATTRACTION       /
                \   ~~~~~~~~~~>    /
                 \               /
                  \            /
                   \         /
                    O  <-- slight (-)
                    |
               ~~~~~~~~~~

   The H "reaches out" toward the O on the neighboring chain.
   This creates a weak but real connection between chains.
```

**Key point:** Hydrogen bonds are NOT as strong as the bonds holding atoms together within a chain. They're more like velcro - easy to pull apart one at a time, but many of them together create significant holding power.

## H-O vs H-N Attractions (ASCII Diagrams)

### H-O Attraction (Found in PLA)

PLA has ester groups with oxygen atoms. Hydrogen atoms nearby can form bonds to these oxygens:

```
PLA CHAIN INTERACTIONS (H-O hydrogen bonding)
==============================================

Chain A:   --CH--C==O
                  |         <-- This O can attract H from Chain B
                  |
                  |  H-bond
                  |  (weak
                  |   pull)
                  v
Chain B:       H-O--         <-- This H reaches toward Chain A's O


ZOOMED IN VIEW:

    Chain A                          Chain B
    =========                        =========
        \                               /
         C==O ........................H-O
        /    ^                       ^
       CH     \                     /
      /        \___ATTRACTION_____/
     ~
              distance: ~2-3 Angstroms
              strength: MODERATE

Result: Chains are LOOSELY connected
        Material is STIFF but can SNAP if bent too far
```

### H-N Attraction (Found in TPU Hard Segments)

TPU has urethane groups with both N-H (donor) and C=O (acceptor). This allows for STRONG, ORGANIZED hydrogen bonding:

```
TPU HARD SEGMENT INTERACTIONS (H-N and H-O hydrogen bonding)
============================================================

Chain A:    N--H.......................O==C      Chain B
            |   ^                      ^   |
            |    \                    /    |
            C==O  \                  /  H--N
            |      \                /      |
            O       \__ATTRACTION__/       O
            |                              |

         DONOR                          ACCEPTOR
         (H-N)                          (O=C)

BOTH directions! TPU hard segments form a NETWORK:

   --N-H - - - O=C--N-H - - - O=C--N-H - - - O=C--
     |           |     |           |     |
   --C=O - - - H-N--C=O - - - H-N--C=O - - - H-N--

   Key: - - - = hydrogen bonds (between chains)
        ----- = covalent bonds (within chains)

Result: Hard segments LOCK TOGETHER like velcro
        Forms organized "crystalline" domains
```

## Why This Makes PLA and TPU Behave Differently

Here's where it all comes together:

```
PLA STRUCTURE (Uniform, modest H-bonding everywhere)
====================================================

  Chain 1:  ===O...H===O...H===O...H===O...H===
                 |     |     |     |     |
  Chain 2:  ===O...H===O...H===O...H===O...H===
                 |     |     |     |     |
  Chain 3:  ===O...H===O...H===O...H===O...H===

  - H-bonds distributed evenly along entire chain
  - All parts of the material behave the same way
  - Result: UNIFORMLY STIFF
  - When bent too far: chains separate suddenly = SNAP/CRACK


TPU STRUCTURE (Alternating hard and soft segments)
==================================================

        [HARD]         [SOFT]         [HARD]         [SOFT]
  ======|||||======~~~~~~~~~~~~======|||||======~~~~~~~~~~~~
        |||||                        |||||
  ======|||||======~~~~~~~~~~~~======|||||======~~~~~~~~~~~~
        |||||                        |||||
  ======|||||======~~~~~~~~~~~~======|||||======~~~~~~~~~~~~

  [HARD] = Strong H-bond network    (|||| = many H-bonds)
           Acts like a "knot"
           Holds chains together

  [SOFT] = Almost no H-bonds        (~~~~ = flexible chain)
           Chains slide freely
           Can stretch and coil

  Result: Material can STRETCH (soft parts extend)
          but RECOVERS (hard parts pull it back)
          = RUBBERY/ELASTIC behavior
```

### The Practical Difference

```
BENDING TEST: What happens when you flex each material?
=======================================================

PLA:
    Before:   |=========|         After bending:   |====\  /====|
                                                       CRACK!

    Why: All H-bonds break at once when stress exceeds threshold.
         No recovery mechanism. Once broken, stays broken.


TPU:
    Before:   |==||~~||==|        During bending:   |==||~~~~~~||==|
                                                        (stretches)

              After release:      |==||~~||==|
                                     (recovers!)

    Why: Soft segments stretch like rubber bands.
         Hard segments stay bonded, acting as anchors.
         When you let go, soft segments retract.
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The fundamental tradeoff is **bond strength vs. flexibility**. More hydrogen bonds between polymer chains create a stiffer, stronger material—but one that's also more brittle and prone to sudden fracture. Fewer hydrogen bonds allow chains to slide freely, enabling flexibility and stretch—but at the cost of structural rigidity and load-bearing capacity. PLA exemplifies the "too uniform" failure mode: its evenly distributed H-bonds make it stiff everywhere, so when stress concentrates, chains separate catastrophically. TPU resolves this by *segregating* the bonds—dense H-bond networks in hard segments provide anchor points and strength, while bond-free soft segments provide stretch and energy absorption. The engineering challenge is that you can't easily tune this ratio after synthesis; you're choosing from pre-designed polymer architectures. Practitioners argue about whether to modify the hard/soft segment ratio (changes Shore hardness), add plasticizers (weakens H-bonds), or use blends of different polymers to achieve target properties.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Shore Hardness and H-Bond Ratio

TPU comes in different "Shore A" hardness ratings. The number tells you the ratio of hard-to-soft segments:

```
SHORE HARDNESS vs HYDROGEN BOND CONTENT
=======================================

Shore 95A (Stiff TPU - easier to print):
[HARD][SOFT][HARD][SOFT][HARD][SOFT][HARD][SOFT][HARD]
 ||||  ~~   ||||  ~~   ||||  ~~   ||||  ~~   ||||

  More hard segments = More H-bonds = Stiffer material
  Feels like: firm rubber, like a car tire


Shore 70A (Soft TPU - harder to print):
[HARD]    [SOFT]    [HARD]    [SOFT]    [HARD]
 ||||  ~~~~~~~~~~   ||||  ~~~~~~~~~~   ||||

  Fewer hard segments = Fewer H-bonds = Softer material
  Feels like: soft rubber, like a rubber band


PRINTING IMPLICATION:

  Stiffer TPU (95A):
    - More H-bonds = chains don't slide as easily
    - Easier to push through extruder
    - Resists buckling in Bowden tubes

  Softer TPU (70A):
    - Fewer H-bonds = chains slide easily
    - Tends to compress and buckle
    - REQUIRES direct drive extruder
```

### Temperature Behavior

```
WHY PLA DEFORMS IN A HOT CAR BUT TPU DOESN'T:

PLA at 25C (room temp):
  Chains locked by H-bonds = rigid solid

PLA at 60C (hot car):
  H-bonds start breaking = chains can slide = DEFORMATION
  (Glass transition ~55-60C)


TPU at 25C:
  Soft segments already flexible (above their [[quick-context/glass-transition-temperature|Tg]])
  Hard segments locked by H-bonds = holds shape

TPU at 60C:
  Soft segments: still flexible (no change)
  Hard segments: H-bonds still intact (Tg much higher, ~100-150C)
  = NO DEFORMATION until you exceed hard segment Tg
```

---

**The one thing most outsiders get wrong about this is...** thinking that flexibility means "weaker bonds." TPU's hard segments actually have *stronger* hydrogen bonding than PLA - the N-H...O=C bonds in urethane groups are more directional and form more organized networks than PLA's ester-based H-bonds. The flexibility comes not from weak bonds, but from clever *architecture*: putting strong bonds only where you want rigidity (hard segments) and leaving other regions (soft segments) free to stretch. TPU is essentially "rigid anchors connected by rubber bands" at the molecular level. PLA fails because it's uniformly semi-rigid everywhere - no give means sudden fracture when stress concentrates.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/van-der-waals-forces]]**: Even weaker than hydrogen bonds, these universal attractions exist between all molecules and contribute to baseline chain cohesion in all polymers.

- **[[quick-context/dipole-dipole-interactions]]**: Hydrogen bonds are actually a special, extra-strong type of dipole-dipole interaction - understanding the general case helps clarify why H-bonds are uniquely powerful.

- **[[quick-context/covalent-bonds]]**: The strong bonds holding atoms together *within* polymer chains - hydrogen bonds connect chains *between* each other, but covalent bonds are what make the chains themselves.

- **[[quick-context/glass-transition-temperature]]**: The temperature where polymer chains gain enough energy to overcome intermolecular forces (including H-bonds) and begin moving freely - directly explains why PLA softens in a hot car.

- **[[quick-context/atoms-molecules-polymers-basics]]**: Foundation concepts for understanding what polymer chains actually are before diving into how they interact with each other.

- **biology-fundamentals**: Hydrogen bonds are critical in biology—DNA base pairing (A-T has 2, G-C has 3), protein secondary structure (alpha helices, beta sheets), and enzyme-[[quick-context/substrate-ic-packaging|substrate]] recognition all depend on H-bonding.

- **[[quick-context/bambu-p2s-print-quality]]**: Why nylon must be dried at 95°C / 7h vs. PLA at 45°C / 6h — amide groups (–CO–NH–) form especially strong H-bonds with water, locking moisture between polymer chains.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why does TPU recover its shape after stretching while PLA simply snaps?
<details>
<summary>Answer</summary>
TPU has alternating hard and soft segments. The soft segments stretch like rubber bands while the hard segments remain locked together by strong hydrogen bond networks, acting as anchors. When released, the soft segments retract back. PLA has uniform H-bonding throughout, so when stress exceeds the threshold, bonds break everywhere at once with no recovery mechanism. See: TPU STRUCTURE (Alternating hard and soft segments)
</details>

**Q2:** Which has stronger hydrogen bonds - PLA or TPU's hard segments? Why is the answer counterintuitive?
<details>
<summary>Answer</summary>
TPU's hard segments actually have *stronger* hydrogen bonding than PLA. The N-H...O=C bonds in urethane groups are more directional and form more organized networks than PLA's ester-based H-bonds. This is counterintuitive because TPU is the flexible material - but its flexibility comes from architecture (where bonds are placed), not from having weaker bonds. See: The one thing most outsiders get wrong about this is...
</details>

**Q3:** Why is Shore 70A TPU harder to 3D print than Shore 95A TPU?
<details>
<summary>Answer</summary>
Shore 70A has fewer hard segments (and thus fewer hydrogen bonds), meaning the chains slide past each other more easily. This causes the filament to compress and buckle in the extruder and Bowden tube rather than being pushed through smoothly. Shore 95A has more H-bonds holding chains together, making it stiffer and easier to push through the extrusion system. See: PRINTING IMPLICATION section under Shore Hardness
</details>

**Q4:** What are the three atoms you need to know to understand hydrogen bonding, and what charge does each carry?
<details>
<summary>Answer</summary>
Hydrogen (H) - slight positive charge, "sticks out" from chains. Oxygen (O) - slight negative charge, attracts hydrogen. Nitrogen (N) - slight negative charge, attracts hydrogen. The attraction between positive H and negative O or N creates hydrogen bonds. See: What IS a Hydrogen Bond? (The Simple Version)
</details>

**Q5:** Why doesn't TPU deform in a hot car (60C) while PLA does?
<details>
<summary>Answer</summary>
PLA's [[quick-context/glass-transition-temperature|glass transition temperature]] is around 55-60C, so at 60C its hydrogen bonds start breaking and chains can slide, causing deformation. TPU's soft segments are already above their Tg at room temperature (that's why they're flexible), but the hard segments that hold the shape together have a much higher Tg (100-150C). At 60C, the hard segment H-bonds remain intact, so TPU keeps its shape. See: WHY PLA DEFORMS IN A HOT CAR BUT TPU DOESN'T
</details>

</details>
