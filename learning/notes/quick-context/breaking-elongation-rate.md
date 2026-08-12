---
topic: Breaking Elongation Rate (Material Property)
created: 2026-01-20
updated: 2026-01-21
---

> **Related:** [[learning/notes/quick-context/chemical-bonds-spectrum]] | [[learning/notes/quick-context/bambu-ams-automatic-material-system]] | [[learning/notes/quick-context/glass-transition-temperature]] | [[learning/notes/quick-context/covalent-bonds]] | [[learning/notes/quick-context/van-der-waals-forces]]

> **TL;DR:** Breaking elongation rate measures how far a material can stretch before snapping (as a percentage of original length)—TPU with ">650%" can stretch to 7.5x its original length, making it ideal for impact-absorbing applications where flexibility matters more than rigidity.

# Breaking Elongation Rate: What "> 650%" Means

## The Core Problem

**Breaking elongation rate** (also called "elongation at break") tells you how much a material can stretch before it snaps.

It's expressed as a percentage of the original length:

```
Original length:  |████████████|  = 100mm

Stretched before breaking:

100% elongation:  |████████████████████████|  = 200mm (doubled)
650% elongation:  |████████████████████████████████████████████████████████████████████|  = 750mm (7.5x original!)
```

**"> 650%"** means the material can stretch to **more than 7.5 times its original length** before it breaks. That's extremely flexible—think rubber bands or TPU (flexible [[learning/notes/quick-context/3d-printing-filament-types|3D printing filament]]).

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Elongation at break** | How far a material stretches (as % of original length) before snapping |
| **[[learning/notes/quick-context/tensile-strength-materials|Tensile strength]]** | How much pulling force a material can handle before breaking (measured in MPa) |
| **Shore hardness** | How squishy/hard a flexible material is (Shore 95A = firm rubber, Shore 60A = soft rubber) |
| **[[learning/notes/quick-context/3d-printing-filament-types|TPU]]** | Thermoplastic polyurethane—the common flexible 3D printing filament with high elongation |
| **Brittle** | A material that breaks with little/no stretching (low elongation, like PLA or glass) |

<details>
<summary><strong>How It Works</strong></summary>

Elongation at break is fundamentally about polymer chain behavior under stress. When you pull on a material, you're forcing the tangled, coiled polymer chains to straighten out and slide past each other. In high-elongation materials like TPU, the chains are long, flexible, and loosely entangled—they can uncoil extensively before the bonds within the chains themselves start breaking. In low-elongation materials like PLA, the chains are either shorter, more rigidly structured, or locked together by crystalline regions that resist chain movement. When those chains can't slip past each other, the stress concentrates and bonds break—the material snaps.

The stretching process happens in stages. First, loosely organized (amorphous) regions allow chains to straighten with relatively little force. As stretching continues, chains begin sliding past each other, overcoming weak intermolecular attractions like [[learning/notes/quick-context/van-der-waals-forces|van der Waals forces]]. In highly elastic materials, this sliding can continue for a long time because the chains are flexible and the intermolecular forces re-form as chains move, preventing catastrophic failure. Eventually, if you keep pulling, the chains either run out of slack, pull apart from each other completely, or the [[learning/notes/quick-context/covalent-bonds|covalent bonds]] in the polymer backbone itself break—that's the breaking point.

```
WHAT HAPPENS WHEN YOU STRETCH A POLYMER
════════════════════════════════════════════════════════════════

INITIAL STATE (0% elongation):
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   ∿∿∿∿∿∿∿     ∿∿∿∿∿∿∿     ∿∿∿∿∿∿∿     Polymer chains are    │
│     ∿∿∿∿∿∿∿     ∿∿∿∿∿∿∿     ∿∿∿∿∿∿∿   coiled and tangled    │
│   ∿∿∿∿∿∿∿     ∿∿∿∿∿∿∿     ∿∿∿∿∿∿∿     like spaghetti       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼ PULLING FORCE APPLIED

STAGE 1 - Chain Uncoiling (~0-100% elongation):
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│   ──∿∿∿∿──    ──∿∿∿∿──    ──∿∿∿∿──    Coils straighten out,        │
│   ──∿∿∿∿──    ──∿∿∿∿──    ──∿∿∿∿──    chains still entangled       │
│   ──∿∿∿∿──    ──∿∿∿∿──    ──∿∿∿∿──    (relatively easy)            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
                            │
                            ▼ MORE FORCE

STAGE 2 - Chain Slippage (~100-500% elongation):
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   ────────────    ────────────    ────────────    Chains sliding past       │
│   ────────────    ────────────    ────────────    each other; weak          │
│   ────────────    ────────────    ────────────    intermolecular bonds      │
│                                                   breaking and reforming     │
└──────────────────────────────────────────────────────────────────────────────┘
                            │
                            ▼ MAXIMUM FORCE

STAGE 3 - Breaking Point (>650% for TPU):
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│   ─────────────  ──   ─────   ──────  ──     Chains fully extended;                 │
│   ──────────   ─────   ────   ─  ──────      no more slack; covalent                │
│   ─────  ──   ────────    ───   ─────   ──   backbone bonds BREAK                   │
│                                              → MATERIAL SNAPS                        │
└──────────────────────────────────────────────────────────────────────────────────────┘


WHY MATERIALS DIFFER:
═══════════════════════════════════════════════════════════════════════════

LOW ELONGATION (PLA ~5%):                HIGH ELONGATION (TPU >650%):

  ████  ████  ████                         ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿
  ████  ████  ████  ← Crystalline          ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿  ← Mostly
  ████  ████  ████    regions lock         ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿    amorphous,
                      chains in place                             chains free
  Chains CAN'T slip                        Chains CAN slip
  → Stress concentrates                    → Stress distributes
  → Bonds break early                      → Stretches far before breaking
  → BRITTLE SNAP                           → DUCTILE STRETCH
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

High elongation materials are:
- ✅ Impact resistant (absorb energy by deforming)
- ✅ Flexible (can bend without cracking)
- ❌ Less rigid (won't hold precise shapes under load)
- ❌ Harder to print (stringy, needs slow speeds)

Low elongation materials are:
- ✅ Rigid and precise
- ✅ Hold shape under load
- ❌ Brittle (crack instead of bending)
- ❌ Poor impact resistance

**You'd want >650% elongation for:** Phone cases, drone bumpers, robot foot pads, hinges, gaskets, watch bands—anything that needs to flex or survive drops.

**You'd NOT want it for:** Structural parts, gears, brackets—anything that needs to stay rigid.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Imagine pulling a 10cm sample until it breaks:

```
Material        Elongation    What happens to 10cm sample
─────────────────────────────────────────────────────────
PLA             ~5%           Stretches to 10.5cm, then SNAP
PETG            ~25%          Stretches to 12.5cm, then breaks
TPU (>650%)     ~700%         Stretches to 80cm before breaking!
```

For a robot foot pad or bumper, you want the TPU behavior—it deforms massively to absorb impact energy instead of cracking.

When you see a filament spec like:

```
Material: TPU 95A
Tensile Strength: 45 MPa
Breaking Elongation Rate: > 650%
Shore Hardness: 95A
Print Temp: 220-240°C
```

This tells you:
- **45 MPa tensile strength**: Moderately strong (won't tear easily)
- **> 650% elongation**: Extremely stretchy/flexible
- **Shore 95A**: Firm but flexible (like a car tire, not a gummy bear)

**The one thing most outsiders get wrong about this is** confusing **elongation** with **softness**. A material can be firm/hard AND have high elongation (like a car tire—stiff but stretches before breaking). Elongation measures *how far* it stretches before snapping, not *how easy* it is to deform. Shore hardness measures softness; elongation measures stretchiness. You can have hard-but-stretchy (TPU 95A) or soft-but-not-very-stretchy (some foams).

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- [[learning/notes/quick-context/tensile-strength-materials]] — The "how much force" counterpart to elongation; together they define a material's mechanical behavior under stress
- [[learning/notes/quick-context/polymer-crystallinity-vs-amorphous|Crystallinity]] — Crystalline vs. [[learning/notes/quick-context/polymer-crystallinity-vs-amorphous|amorphous]] structure directly affects elongation; amorphous regions allow [[learning/notes/quick-context/atoms-molecules-polymers-basics|polymer]] chains to uncoil and stretch
- [[learning/notes/quick-context/glass-transition-temperature|Glass transition temperature]] — Below [[learning/notes/quick-context/glass-transition-temperature|Tg]], polymers become brittle with low elongation; above Tg, they're rubbery with high elongation
- [[learning/notes/quick-context/polymer-chemical-bonds|Chemical bonds]] — The backbone chemistry (ester, urethane, ether) determines chain flexibility and ultimate elongation capability

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A spec sheet shows 45 MPa tensile strength and >650% elongation. Is this material soft like a gummy bear?

<details>
<summary>Answer</summary>

Not necessarily. High elongation tells you the material stretches far before breaking, but it says nothing about *softness* (how easily it deforms). You need Shore hardness for that. With 95A Shore hardness, this material is firm like a car tire—stiff to push but stretchy when pulled hard enough. Elongation measures stretchiness, not softness.

</details>

**Q2:** You're designing a protective bumper for a drone that crashes frequently. Would you choose PLA (5% elongation, 60 MPa tensile) or TPU (650% elongation, 45 MPa tensile)? Why?

<details>
<summary>Answer</summary>

TPU. Despite lower tensile strength, the 650% elongation means the bumper absorbs crash energy by deforming massively rather than cracking. PLA's 5% elongation means it shatters on impact—the energy goes into breaking bonds rather than stretching them. For impact protection, elongation matters more than raw strength.

</details>

**Q3:** Why might a polymer have high elongation at room temperature but become brittle and snap easily in a freezer?

<details>
<summary>Answer</summary>

The freezer temperature may be below the polymer's [[learning/notes/quick-context/glass-transition-temperature|glass transition temperature]] (Tg). Above Tg, polymer chains can move and uncoil, allowing large elongation. Below Tg, the amorphous regions "freeze" into a glassy state where chains can't move—the material becomes rigid and brittle with drastically reduced elongation at break.

</details>

**Q4:** Two TPU samples have identical Shore hardness (95A) but different elongation values (400% vs 700%). What might explain this?

<details>
<summary>Answer</summary>

Shore hardness measures resistance to indentation (surface deformation), while elongation measures how far chains can uncoil before breaking. Differences could come from: (1) molecular weight—longer chains can uncoil further, (2) crosslink density—more crosslinks limit chain movement, (3) crystallinity—more crystalline regions restrict elongation, or (4) additives/fillers that affect chain mobility differently than surface hardness.

</details>

**Q5:** How does elongation at break relate to [[learning/notes/quick-context/glass-transition-temperature|glass transition temperature]], and what happens to a material's elongation as temperature drops below Tg?

<details>
<summary>Answer</summary>

Below Tg, polymer chains are frozen in a glassy state—they can't move or uncoil, making the material rigid and brittle with drastically reduced elongation. As temperature approaches Tg from below, chains gain mobility. Above Tg, the material enters its rubbery/viscoelastic regime where chains can slide past each other, dramatically increasing elongation before breaking. This is why the same TPU that stretches 600% at room temperature might shatter at -40°C if that's below its Tg. The glass transition essentially "unlocks" the molecular mechanisms that allow large deformations. This connects to why heating polymers makes them more ductile—thermal energy enables chain motion. See: [[learning/notes/quick-context/glass-transition-temperature]] and Peripheral Knowledge

</details>

</details>
