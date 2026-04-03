---
case: Why Sunlight Destroys Plastic but Not Glass
components: [chemical-bonds, uv-radiation, free-radical-chain-reactions]
created: 2026-04-04
---

# Case: Why Sunlight Destroys Plastic but Not Glass

> **Components:** [[quick-context/chemical-bonds-spectrum]] | [[quick-context/covalent-bonds]] | [[quick-context/polymer-chemical-bonds]]

> **In brief:** Sunlight carries UV photons with enough energy to snap the [[quick-context/covalent-bonds|carbon-carbon backbone]] of plastics, triggering a self-amplifying chain reaction with oxygen that chews the material apart. Glass is built from silicon-oxygen bonds that are too strong for solar UV to break, and its 3D network structure dissipates any absorbed energy as harmless heat.

## The Situation

Leave a plastic chair outside for a few years and it yellows, cracks, and crumbles. A glass window in the same sunlight stays structurally identical for centuries. Both materials sit in the same photon bath — so why does one survive and the other doesn't? The answer comes down to bond energy vs. photon energy, and what happens after a bond breaks.

## The Pieces

**UV photons:** Sunlight that reaches Earth's surface includes UV-A (315–400 nm) and some UV-B (280–315 nm). Each photon carries a fixed packet of energy: $E = hc/\lambda$. Shorter wavelength = higher energy. Solar UV tops out around 295 nm (~4.2 eV, ~405 kJ/mol).

**[[quick-context/chemical-bonds-spectrum|Chemical bonds]]:** Every bond has a dissociation energy — the minimum energy needed to snap it. If a photon delivers at least that much energy to a bond, the bond can break. If not, the energy passes through or dissipates as heat.

**Glass (SiO₂ network):** An enormous 3D web of silicon atoms each bonded to four oxygen atoms. The Si–O bond requires 452 kJ/mol (4.69 eV) to break — corresponding to 264 nm light, deep in UV-C that never reaches Earth's surface.

**Plastic ([[quick-context/polymer-chemical-bonds|polymer chains]]):** Long 1D chains of carbon atoms with hydrogen and other atoms hanging off. The C–C backbone bond requires only 346 kJ/mol (3.59 eV) — corresponding to 345 nm, which is UV-A. Abundant in sunlight.

## Step by Step: What Happens

### The Energy Comparison

Everything hinges on whether solar photons carry enough energy to break the bonds in each material:

```
  Photon energy (solar UV at Earth's surface)
  ├─────────────────────────────────────────────────┤
  3.1 eV                                         4.2 eV
  (400 nm, UV-A)                           (295 nm, UV-B)

  Bond dissociation energies:
  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  C-N  C-Cl  C-C     C-O       C-H       Si-O
  3.16  3.39  3.59    3.71      4.26      4.69 eV
  |     |     |       |         |         |
  v     v     v       v         v         v
  ├──BREAKABLE BY SOLAR UV──────┤  border  │ TOO STRONG
                                    line
```

Solar UV photons (3.1–4.2 eV) comfortably exceed the C–C bond energy (3.59 eV) and several other polymer bonds. They fall short of the Si–O bond energy (4.69 eV) by about 0.5 eV.

### Step 1: UV Hits Glass — Nothing Happens

When a UV photon hits glass, one of two things occurs:

1. **It passes through.** Pure silica (SiO₂) has a band gap of ~8.9 eV. Solar UV photons (3–4 eV) don't have enough energy to excite electrons across this gap, so the glass is transparent to them.

2. **It gets absorbed by impurities.** Ordinary window glass contains trace iron oxide (Fe₂O₃), which absorbs UV-B in the 300–340 nm range. But the absorbed energy doesn't break Si–O bonds — instead, the excited electrons relax by transferring energy into lattice vibrations (heat). The 3D network acts as an enormous heat sink, distributing the energy across billions of bonds.

```
  UV photon (4.0 eV)
        |
        v
  ┌─────────────────────────────────┐
  │  Glass: 3D SiO₂ network         │
  │                                 │
  │    O   O   O   O                │
  │     \ / \ / \ / \               │
  │  ··· Si   Si   Si ···           │
  │     / \ / \ / \ /               │
  │    O   O   O   O                │
  │                                 │
  │  Si-O bond = 4.69 eV            │
  │  Photon energy = 4.0 eV         │
  │  4.0 < 4.69 → bond survives     │
  │                                 │
  │  Energy → heat → dissipated     │
  └─────────────────────────────────┘
```

**Result:** No bond breaks. No damage. The glass is unchanged.

### Step 2: UV Hits Plastic — A Bond Snaps

When a UV-A photon (say, 345 nm = 3.59 eV) hits a polymer chain, it has exactly enough energy to break a C–C bond. The bond splits homolytically — each carbon keeps one electron, creating two **free radicals** (atoms with unpaired electrons, highly reactive):

$$\text{P–P} + h\nu \rightarrow \text{P}^\bullet + \text{P}^\bullet$$

In practice, initiation usually starts at weak points: impurities from manufacturing, catalyst residues, or hydroperoxide groups (–OOH) already present in the plastic. These chromophoric groups absorb UV and crack open first.

```
  UV photon (3.6 eV)
        |
        v
  ─ C ─ C ─ C ─ C ─ C ─ C ─ C ─    polymer chain
              |
              × bond breaks (3.59 eV needed)
              |
  ─ C ─ C ─ C•    •C ─ C ─ C ─ C ─  two radicals formed
```

### Step 3: Oxygen Joins — The Chain Reaction Ignites

This is where plastic degradation turns from damage into destruction. The free radical reacts instantly with atmospheric O₂:

$$\text{P}^\bullet + \text{O}_2 \rightarrow \text{POO}^\bullet$$

The resulting peroxyl radical steals a hydrogen from a neighboring chain:

$$\text{POO}^\bullet + \text{PH} \rightarrow \text{POOH} + \text{P}^\bullet$$

A new radical is born. The cycle repeats. Each round creates a hydroperoxide (POOH) — and here's the devastating part: hydroperoxides themselves absorb UV and split into *two* radicals:

$$\text{POOH} + h\nu \rightarrow \text{PO}^\bullet + {}^\bullet\text{OH}$$

This is **autocatalytic** — the reaction accelerates as it produces more of its own initiators.

```
  The radical chain reaction:

  P• + O₂ ──→ POO•                ← radical grabs oxygen
      │
      ↓
  POO• + P-H ──→ POOH + P•        ← steals H, new radical born
      │                  │
      ↓                  └──→ repeats
  POOH + hν ──→ PO• + •OH         ← UV splits product → 2 radicals
      │            │                  (autocatalytic branching)
      ↓            ↓
    more         more
   radicals    radicals ──→ exponential acceleration
```

### Step 4: The Polymer Falls Apart

The alkoxyl radical (PO•) from Step 3 undergoes **beta-scission** — the C–C backbone breaks right next to it:

```
  Before beta-scission:
  ─ C ─ C ─ C ─ C ─ C ─
            |
            O•  (alkoxyl radical)

  After beta-scission:
  ─ C ─ C ─ C•    C═O  +  •C ─ C ─
            ↑      ↑
      new radical  ketone (absorbs more UV!)
```

The ketone product absorbs UV too, undergoing **Norrish reactions** that cleave more chains. Meanwhile, some radicals combine with each other, creating **crosslinks** between chains that make the surface rigid and brittle.

### Step 5: Visible Destruction

The cascade produces observable damage in this order:

1. **Yellowing** — chains of conjugated double bonds form that absorb blue/violet light
2. **Loss of strength** — chain scission reduces molecular weight, destroying the entanglement network that gives plastic its toughness
3. **Surface cracking** — crosslinked surface layer becomes brittle, cracks under thermal stress
4. **Chalking and crumbling** — the material fragments into powder and eventually microplastics

## The Result

```
  GLASS after 100 years of sunlight:       PLASTIC after 5 years of sunlight:

  ┌───────────────────────┐                 ┌ ─ ─  ─ ─  ─ ─  ─ ┐
  │                       │                   cracked, yellowed,
  │   Structurally        │                 │ brittle surface    │
  │   identical           │                    ╱  ╲    ╱  ╲
  │                       │                 │╱  chalky ╲╱ flaking│
  │   (maybe slightly     │                   powder underneath
  │    purple if it has   │                 │                    │
  │    manganese)         │                   fragments / micro-
  └───────────────────────┘                 └ plastics ─  ─  ─  ┘
```

## Why Each Piece Matters

- **Bond energy gap:** Si–O (4.69 eV) sits above the solar UV ceiling; C–C (3.59 eV) sits below it. This single fact determines which material survives.
- **3D vs. 1D structure:** Glass's network dissipates energy across the lattice as heat. A polymer chain is a single thread — break it once and the whole structure weakens.
- **Oxygen + radicals:** The autocatalytic free-radical chain reaction with O₂ means one photon's worth of damage multiplies into thousands of broken bonds. Glass has no equivalent — it's already fully oxidized.
- **No hydrogen to steal:** The chain reaction depends on abstracting H atoms from neighboring chains. Glass has no hydrogen — even if a radical somehow formed, it would have nothing to react with.

## Nuances

**Teflon (PTFE) is the exception that proves the rule.** Its C–F bond (485 kJ/mol, 5.03 eV) is actually *stronger* than Si–O. Solar UV can't break it, so Teflon sits in sunlight for decades without degrading — demonstrating that bond energy, not whether a material is "organic" or "inorganic," is what matters.

**Glass does change, slowly.** Trace manganese in antique glass (used as a decolorizer ~1880–1915) photo-oxidizes from Mn²⁺ to Mn³⁺ under decades of UV exposure, turning the glass purple. This "solarization" affects color but not structural integrity. The bulk Si–O network remains untouched.

**UV stabilizers extend plastic life.** Commercial plastics contain additives like HALS (hindered amine light stabilizers) that intercept radicals before the chain reaction takes off, or UV absorbers (benzotriazoles) that convert UV to heat — essentially trying to make plastic behave more like glass.

## Key Numbers

| Bond  | Energy (kJ/mol) | Energy (eV) | $\lambda$ to break (nm) | Solar UV can break? |
|-------|-----------------|-------------|--------------------------|---------------------|
| Si–O  | 452             | 4.69        | 264 (UV-C)               | No                  |
| C–H   | 411             | 4.26        | 291 (UV-B)               | Borderline          |
| C–O   | 358             | 3.71        | 334 (UV-A)               | Yes                 |
| C–C   | 346             | 3.59        | 345 (UV-A)               | Yes                 |
| C–Cl  | 327             | 3.39        | 366 (UV-A)               | Yes                 |
| C–F   | 485             | 5.03        | 247 (UV-C)               | No                  |

Solar UV at Earth's surface: 295–400 nm (3.1–4.2 eV, 299–405 kJ/mol)

## Go Deeper

**Full treatment:**
- [[quick-context/chemical-bonds-spectrum]] — The full bond strength spectrum from covalent (~350 kJ/mol) to van der Waals (~2 kJ/mol), with energy comparisons that underpin this entire article
- [[quick-context/covalent-bonds]] — How electron sharing creates bonds, single vs. double vs. triple, and why carbon's 4-bond versatility makes polymers possible
- [[quick-context/polymer-chemical-bonds]] — How covalent backbones + intermolecular forces determine polymer behavior; the same chains UV destroys here are what melt during 3D printing
