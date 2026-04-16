---
topic: Covalent Bonds
created: 2026-01-20
updated: 2026-01-21
---

> **Related:** [[quick-context/polymer-chemical-bonds]], [[quick-context/3d-printing-filament-types]]

> **TL;DR:** Covalent bonds form when atoms share electrons to complete their outer shells, creating the strong intra-molecular connections that hold polymer chains together—these bonds never break during normal 3D printing.

# Quick Context: Covalent Bonds

## The Core Problem: Why Atoms Need to Share

Everything around you—your desk, your skin, your 3D printer filament—is made of atoms that need to stick together somehow. Covalent bonds solve the fundamental problem of **how atoms hold onto each other strongly enough to form stable molecules and materials**. Without covalent bonds, there would be no water, no plastics, no DNA, no you. Atoms have electrons orbiting them, and most atoms are "unhappy" (unstable) unless they have a specific number of electrons in their outer shell—typically 8, called the "octet rule." The problem: most atoms don't naturally have 8. The solution: **share electrons with a neighbor**. When two atoms share electrons, both get to "count" those shared electrons toward their octet, and the sharing creates an attractive force that locks them together. If covalent bonds didn't exist, matter would only exist as isolated atoms or the relatively weak arrangements formed by other bond types—no complex molecules, no polymers, no life.

```
    LONELY ATOMS (UNSTABLE)              BONDED ATOMS (STABLE)

    Carbon needs 4 more e-               Carbon shares with 4 Hydrogens
    Hydrogen needs 1 more e-             Each H shares 1 e- with Carbon

         H                                      H
         |                                      |
    H    C    H                            H -- C -- H     (Methane: CH4)
         |                                      |
         H                                      H

    (each "--" represents 2 shared electrons = 1 covalent bond)
```

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **[[quick-context/subatomic-particles\|Electron]]** | A tiny negatively-charged [[quick-context/subatomic-particles\|subatomic particle]] that orbits atoms and gets shared in covalent bonds |
| **[[quick-context/atoms-molecules-polymers-basics\|Polymer]]** | A long chain molecule made of repeating units (monomers) connected by covalent bonds—what your 3D printer filament is made of |
| **Monomer** | The single repeating unit that links together to form a polymer chain (like a single LEGO brick) |
| **Cross-linking** | When polymer chains form covalent bonds sideways to neighboring chains, creating a rigid network |
| **Thermoplastic** | A polymer that softens when heated and hardens when cooled (reversible)—what FDM 3D printing uses |

<details>
<summary><strong>How It Works</strong></summary>

Covalent bonding happens when two atoms get close enough that their outer electron clouds overlap. Instead of one atom stealing electrons from the other (that would be ionic bonding), they set up a "time-share" arrangement: the shared electrons spend time orbiting both nuclei simultaneously. This shared electron pair creates a region of negative charge between the two positively charged nuclei, and electrostatic attraction pulls the nuclei toward this shared region, holding the atoms together. The bond length (distance between nuclei) settles at the point where attraction and repulsion balance out.

The number of bonds an atom can form depends on how many electrons it needs to complete its outer shell. Hydrogen needs 1 electron, so it forms 1 bond. Oxygen needs 2, so it forms 2 bonds. Nitrogen needs 3, forming 3 bonds. Carbon needs 4 electrons and forms 4 bonds—this versatility is why carbon is the backbone of all organic chemistry and polymer science. Atoms can share more than one pair of electrons: a double bond shares 4 electrons (2 pairs), and a triple bond shares 6 electrons (3 pairs). More shared electrons means stronger, shorter, and more rigid bonds.

```
HOW COVALENT BONDS FORM: The Electron Sharing Process
══════════════════════════════════════════════════════════════════════════

Step 1: ATOMS APPROACH - Each has incomplete outer shells
──────────────────────────────────────────────────────────

      HYDROGEN (H)                    HYDROGEN (H)
      Has 1 electron                  Has 1 electron
      Wants 2 (full shell)            Wants 2 (full shell)

        ( e- )                          ( e- )
           H ●                            ● H
        (nucleus)                      (nucleus)

              ─────────────►  ◄─────────────
                   atoms approach each other


Step 2: ELECTRON CLOUDS OVERLAP - Sharing begins
─────────────────────────────────────────────────

        ┌─────────────────────────────────┐
        │                                 │
        │    ●  ←── e- ──→  ●             │   Electrons now orbit
        │    H    shared    H             │   BOTH nuclei
        │         pair                    │
        │                                 │
        └─────────────────────────────────┘
                overlapping
               electron cloud


Step 3: BOND STABILIZES - Attraction balances repulsion
────────────────────────────────────────────────────────

        ATTRACTIVE FORCES:              REPULSIVE FORCES:
        • Each nucleus (+)              • Both nuclei (+/+)
          attracted to                    repel each other
          shared electrons (-)          • Electrons (-/-)
                                          repel each other

              (+)       (-)      (+)
               H ●←────(e-e-)────→● H
                  \      │      /
                   \     │     /
                    \    │    /
                     attraction

        Bond length = where forces BALANCE
        For H-H: 0.74 Angstroms (very short!)


SINGLE, DOUBLE, AND TRIPLE BONDS
═══════════════════════════════════════════════════════════════════════════

SINGLE BOND: 2 shared electrons (1 pair)
─────────────────────────────────────────
Example: H-H, C-C, C-H

    H ── H        or       C ── C

    ● ●─● ●               ● ●─● ●
      └─┘                   └─┘
      1 pair               1 pair

    Properties: Longest, weakest, allows rotation
    Bond energy: ~350 kJ/mol (C-C)


DOUBLE BOND: 4 shared electrons (2 pairs)
──────────────────────────────────────────
Example: O=O, C=C, C=O

    O ══ O        or       C ══ C

    ● ●═● ●               ● ●═● ●
      └╦┘                   └╦┘
       ║                     ║
    2 pairs               2 pairs

    Properties: Shorter, stronger, NO rotation (rigid)
    Bond energy: ~615 kJ/mol (C=C)


TRIPLE BOND: 6 shared electrons (3 pairs)
──────────────────────────────────────────
Example: N≡N (nitrogen gas), C≡C

    N ≡≡ N        or       C ≡≡ C

    ● ●≡● ●               ● ●≡● ●
      └╬┘                   └╬┘
       ╬                     ╬
    3 pairs               3 pairs

    Properties: Shortest, strongest, completely rigid
    Bond energy: ~840 kJ/mol (C≡C)


CARBON: THE MASTER BUILDER (Why Polymers Exist)
═══════════════════════════════════════════════════════════════════════════

Carbon has 4 outer electrons, needs 4 more → forms 4 bonds

          This gives carbon incredible VERSATILITY:

          │                    │
    ─── C ───      or     ═══ C ═══     or    ─── C ≡≡≡
          │                    │                  │
      4 single              2 double         1 single + 1 triple


    CHAIN BUILDING (basis of all polymers):

    ─C─C─C─C─C─C─C─C─C─C─C─C─C─C─C─C─C─C─
     │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │

    Each carbon uses 2 bonds for the chain backbone
    Still has 2 bonds left for side groups (H, OH, etc.)

    This is why carbon can form chains of MILLIONS of atoms
    = POLYMERS (plastics, proteins, DNA)
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

Practitioners in materials science and polymer chemistry constantly wrestle with the tradeoff between **bond strength and material flexibility**. Stronger covalent bonds (like triple bonds) or more cross-linking between polymer chains creates harder, more rigid, more heat-resistant materials—but also more brittle ones that crack under stress. Fewer bonds or single bonds create flexible, stretchy materials—but they melt easier and can deform permanently. In 3D printing, this shows up directly: **PLA** (polylactic acid) has relatively simple polymer chains with limited cross-linking, making it easy to print at low temperatures but brittle. **ABS** has a more complex structure that's tougher but needs higher temps and tends to warp. The holy grail is engineering polymers that balance these properties—strong where needed, flexible where needed, printable at reasonable temperatures.

```
    LINEAR POLYMER (more flexible, lower melting point)

    --[A]--[A]--[A]--[A]--[A]--[A]--[A]--[A]--

    (chains slide past each other easily)


    CROSS-LINKED POLYMER (more rigid, higher melting point)

    --[A]--[A]--[A]--[A]--[A]--[A]--[A]--[A]--
              |           |
              |           |
    --[A]--[A]--[A]--[A]--[A]--[A]--[A]--[A]--
                     |
                     |
    --[A]--[A]--[A]--[A]--[A]--[A]--[A]--[A]--

    (cross-links lock chains together like rungs on a ladder)
```

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

When you 3D print with PLA, here's what's happening at the molecular level:

```
    PLA MONOMER (Lactic Acid unit):

           O
           ||
    HO -- C -- C -- C -- H
           |    |
           H    O
                |
                H

    POLYMERIZATION (monomers link up via covalent bonds):

    [LA] + [LA] + [LA] + [LA] → [LA]--[LA]--[LA]--[LA]...
                                    ↑
                        (covalent bonds form, water released)


    PRINTING PROCESS:

    COLD FILAMENT           HEATED (200°C)           COOLED ON BED
    ============           =============           =============

    ~~~~chains~~~~         ~  ~  ~  ~  ~          ~~~~chains~~~~
    ~~~~locked~~~~    →    ~  ~  ~  ~  ~    →     ~~~~locked~~~~
    ~~~~rigid~~~~          ~  ~  ~  ~  ~          ~~~~rigid~~~~
                           (chains slide,          (chains lock
                            material flows)         back in place)

    The covalent bonds within chains NEVER break during printing.
    Only the weak forces BETWEEN chains let them slide past each other.
```

Here's the chemical reality in a simplified molecular view:

```
    INSIDE YOUR HEATED NOZZLE (200°C):

    Before heating:
    ========================================
    Chain A: --[*]--[*]--[*]--[*]--[*]--
                ↕↕↕  ↕↕↕  ↕↕↕  ↕↕↕        ← weak attractions ([[quick-context/van-der-waals-forces|van der Waals]])
    Chain B: --[*]--[*]--[*]--[*]--[*]--
                ↕↕↕  ↕↕↕  ↕↕↕  ↕↕↕
    Chain C: --[*]--[*]--[*]--[*]--[*]--

    (rigid solid - chains can't move)

    After heating:
    ========================================
    Chain A: --[*]--[*]--[*]--[*]--[*]--
                                              ← weak attractions overcome
    Chain B:    --[*]--[*]--[*]--[*]--[*]--

    Chain C: --[*]--[*]--[*]--[*]--[*]--

    (flowing liquid - chains slide freely)

    [*]--[*] = COVALENT BONDS (never break during printing, ~350 kJ/mol)
    ↕↕↕      = WEAK FORCES (easily overcome by heat, ~5 kJ/mol)
```

**The one thing most outsiders get wrong about this is...** thinking that melting plastic "breaks" the molecular bonds. It doesn't. When you heat PLA in your 3D printer, you're only overcoming the weak attractions *between* polymer chains, letting them slide past each other. The strong covalent bonds *within* each chain stay completely intact. That's why you can melt and re-solidify thermoplastics repeatedly—you're never actually breaking and reforming the covalent bonds, just letting the chains move around. (This is also why recycling thermoplastics works, but why you can't "un-cure" epoxy or vulcanized rubber—those have permanent cross-links.)

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

Related concepts that connect to covalent bonds:

- [[quick-context/atoms-molecules-polymers-basics]] — Foundation for understanding what atoms and molecules are and how they build into larger structures like polymers
- [[quick-context/polymer-chemical-bonds]] — Deeper dive into how covalent bonds specifically work within polymer chains and determine material properties
- [[quick-context/hydrogen-bonds-beginners]] — A weaker type of bond that works alongside covalent bonds to influence material behavior (like water's unique properties)
- [[quick-context/van-der-waals-forces]] — The weak attractions between polymer chains that you overcome when melting thermoplastics
- [[quick-context/dipole-dipole-interactions]] — Another type of intermolecular force that affects how polymer chains interact with each other
- Biology fundamentals — Covalent bonds form the backbone of all biological molecules: peptide bonds in proteins, phosphodiester bonds in DNA, glycosidic bonds in carbohydrates
- [[quick-context/subatomic-particles]] — Explains what electrons are, why atoms have specific numbers of them in outer shells, and why carbon with 4 outer electrons can form 4 bonds
- [[small-context/glass-vs-plastic-uv-degradation]] — Bond dissociation energy in action: UV photons break C–C covalent bonds (346 kJ/mol) in plastics but can't reach Si–O bonds (452 kJ/mol) in glass

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Why don't covalent bonds break when you melt PLA filament in a 3D printer?
<details>
<summary>Answer</summary>
Covalent bonds are extremely strong (~350 kJ/mol) compared to the weak intermolecular forces between polymer chains (~5 kJ/mol). The heat from your printer (around 200C) provides enough energy to overcome the weak van der Waals forces between chains, allowing them to slide past each other, but nowhere near enough energy to break the covalent bonds within the chains themselves. This is why thermoplastics can be melted and re-solidified repeatedly without degrading—the polymer chains stay intact.
</details>

**Q2:** What is the "octet rule" and why does it drive covalent bond formation?
<details>
<summary>Answer</summary>
The octet rule states that atoms are most stable when they have 8 electrons in their outer shell. Most atoms don't naturally have this configuration, so they "solve" this problem by sharing electrons with neighboring atoms. When two atoms share electrons, both atoms get to count those shared electrons toward their octet, making both more stable. This sharing creates an attractive force—the covalent bond—that holds the atoms together.
</details>

**Q3:** Why are cross-linked polymers more rigid and heat-resistant than linear polymers?
<details>
<summary>Answer</summary>
In linear polymers, chains can slide past each other when heated because they're only held together by weak intermolecular forces. Cross-linked polymers have covalent bonds connecting chains sideways to each other, creating a rigid 3D network. Since these cross-links are covalent bonds (not weak forces), they don't break when heated—the chains can't slide, so the material stays rigid. This is why you can't melt vulcanized rubber or cured epoxy.
</details>

**Q4:** Carbon can form 4 covalent bonds. How does this relate to its role in polymers?
<details>
<summary>Answer</summary>
Carbon's ability to form 4 covalent bonds makes it uniquely suited for building long, complex polymer chains. It can bond to two neighboring carbons (continuing the chain) while still having 2 bonds available for side groups or functional groups. This versatility allows for enormous variety in polymer structures—different side groups create different properties, and the ability to branch or cross-link gives materials engineers precise control over material characteristics.
</details>

**Q5:** What's the practical difference between a single covalent bond and a double or triple bond?
<details>
<summary>Answer</summary>
Single bonds share 2 electrons, double bonds share 4, and triple bonds share 6. More shared electrons means a stronger, shorter, and more rigid bond. Single bonds allow rotation around the bond axis (flexibility), while double and triple bonds lock atoms in place (rigidity). In polymers, chains with mostly single bonds are more flexible and have lower melting points, while those with double bonds are stiffer. Triple bonds are rare in polymers but common in small molecules like nitrogen gas (N2).
</details>

</details>
