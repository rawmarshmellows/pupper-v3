---
topic: Electrolyte
created: 2026-01-22
updated: 2026-01-22
---

> **Related:** [[learning/notes/quick-context/making-electrolytes]] | [[learning/notes/quick-context/electrolysis]] | [[learning/notes/quick-context/galvanic-cells-batteries]] | [[learning/notes/quick-context/electrodes]] | [[learning/notes/quick-context/subatomic-particles]]

> **TL;DR:** Electrolytes are substances (acids, bases, or salts) that dissolve in water to release free ions, enabling the liquid to conduct electricity; pure water is essentially an insulator, but adding an electrolyte can increase conductivity by 500,000x.

# Electrolyte

```
┌─────────────────────────────────────────────────────────────────────┐
│                     WHAT MAKES AN ELECTROLYTE                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   SOLID SALT (NaCl)          DISSOLVED IN WATER                     │
│   ┌───┬───┬───┬───┐                                                 │
│   │Na⁺│Cl⁻│Na⁺│Cl⁻│          Na⁺  ~~~  Cl⁻    ~~~  Na⁺             │
│   ├───┼───┼───┼───┤    →                                            │
│   │Cl⁻│Na⁺│Cl⁻│Na⁺│       Cl⁻  ~~~    Na⁺   ~~~   Cl⁻              │
│   └───┴───┴───┴───┘                                                 │
│   Ions locked in place       Ions FREE to move = conducts!          │
│   (no conductivity)          (~~~ = water molecules)                │
│                                                                     │
│   KEY INSIGHT: The ions physically MIGRATE through the liquid,      │
│   carrying charge. This is different from metals, where electrons   │
│   flow while atoms stay fixed.                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Three ways to create an electrolyte:**

| Method | Example | What Dissociates |
|--------|---------|------------------|
| **Dissolve an acid** | H₂SO₄ in water | H₂SO₄ → 2H⁺ + SO₄²⁻ |
| **Dissolve a base** | NaOH in water | NaOH → Na⁺ + OH⁻ |
| **Dissolve a salt** | NaCl in water | NaCl → Na⁺ + Cl⁻ |
| **Melt an ionic compound** | Molten NaCl (no water) | NaCl(l) → Na⁺ + Cl⁻ |

See [[quick-context/making-electrolytes]] for detailed preparation methods.

---

## The Core Problem: Making Liquids Conduct Electricity

Pure water is essentially an insulator—it has a conductivity of only ~0.05 μS/cm because water molecules barely split into ions (only 10⁻⁷ M H⁺ and OH⁻ from autoionization). Without an electrolyte, you cannot run [[quick-context/electrolysis|electrolysis]], batteries cannot function, and electrochemical processes halt completely. The ions physically move through the liquid—[[quick-context/cations-and-reduction|cations]] toward the [[quick-context/electrodes|cathode]], [[quick-context/anions-and-oxidation|anions]] toward the [[quick-context/electrodes|anode]]—carrying charge and enabling the electrode reactions. No electrolyte means no current flow through the liquid, which means no chemistry happens at the electrodes.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Ion** | An atom or molecule with net electric charge from gaining or losing electrons (Na⁺, Cl⁻, SO₄²⁻) |
| **Dissociation** | The process where ionic compounds split into free ions when dissolved or melted |
| **Conductivity** | A measure of how well a solution carries [[learning/notes/quick-context/electric-current|electric current]], measured in siemens per centimeter (S/cm) |
| **Strong electrolyte** | Substances that fully dissociate into ions (NaCl, HCl, NaOH)—high conductivity |
| **Weak electrolyte** | Substances that only partially dissociate (acetic acid, ammonia)—lower conductivity |

<details>
<summary><strong>How It Works</strong></summary>

The mechanism of electrolytic conduction is fundamentally different from how metals conduct electricity. In a metal wire, electrons flow freely while atoms stay fixed in place. In an electrolyte solution, the opposite happens: electrons stay bound to atoms, but the entire ions physically migrate through the liquid. When you apply [[learning/notes/quick-context/voltage|voltage]] across two electrodes immersed in an electrolyte, you create an electric field that pushes positive ions (cations) toward the negative electrode ([[learning/notes/micro-context/cathode|cathode]]) and negative ions (anions) toward the positive electrode ([[learning/notes/micro-context/anode|anode]]). This mass migration of charged particles IS the current.

The process begins with dissociation: when an ionic compound like NaCl dissolves in water, the polar water molecules surround and separate the Na⁺ and Cl⁻ ions that were locked together in the crystal lattice. Each ion becomes "solvated"—wrapped in a shell of water molecules with their opposite charges facing inward. These solvated ions are now free to move independently through the solution. The number of ions and how fast they can move determines the solution's conductivity. Temperature matters because warmer solutions have lower viscosity, allowing ions to migrate faster.

```
HOW ELECTROLYTES CONDUCT ELECTRICITY
════════════════════════════════════════════════════════════════════════════

Step 1: DISSOCIATION - Salt dissolves, releasing free ions
─────────────────────────────────────────────────────────────
     NaCl Crystal                    Dissolved in Water
    ┌───┬───┬───┐
    │Na⁺│Cl⁻│Na⁺│       H₂O        Na⁺(aq)   Cl⁻(aq)   Na⁺(aq)
    ├───┼───┼───┤      ────→
    │Cl⁻│Na⁺│Cl⁻│                  Cl⁻(aq)   Na⁺(aq)   Cl⁻(aq)
    └───┴───┴───┘
     (ions locked)                  (ions FREE to move)

Step 2: ION MIGRATION - Electric field moves ions to electrodes
─────────────────────────────────────────────────────────────────

    CATHODE (-)                                    ANODE (+)
        ║                                              ║
        ║    ←── Na⁺  ←── Na⁺  ←── Na⁺  ←── Na⁺      ║
        ║                                              ║
        ║        Cl⁻ ──→  Cl⁻ ──→  Cl⁻ ──→  Cl⁻ ──→  ║
        ║                                              ║
        ║     ELECTRIC FIELD (voltage creates force)   ║
        ║     ─────────────────────────────────────→   ║
        ║                                              ║

    Cations (+) migrate LEFT toward cathode (-)
    Anions  (-) migrate RIGHT toward anode (+)
    This ion movement = electric current through liquid!

Step 3: ELECTRODE REACTIONS - Electrons transfer at surfaces
─────────────────────────────────────────────────────────────

    At CATHODE:                      At ANODE:
    Cations GAIN electrons           Anions LOSE electrons
    (reduction)                      (oxidation)

    2H₂O + 2e⁻ → H₂ + 2OH⁻          2H₂O → O₂ + 4H⁺ + 4e⁻
    (if using inert electrolyte)     (if using inert electrolyte)

    Electrons flow THROUGH wire      Electrons flow THROUGH wire
    INTO the solution here           OUT OF the solution here

COMPLETE CIRCUIT:
═════════════════════════════════════════════════════════════════════
                        ┌──── e⁻ flow ────┐
                        │   (external     │
                        │    wire)        │
                        ▼                 │
    CATHODE (-)  ──────────────────────────────  ANODE (+)
        │                                            │
        │ e⁻ enter    ◄─── CATIONS ───               │ e⁻ leave
        │ solution         migrate                   │ solution
        │                                            │
        │                  ANIONS ───►               │
        │                  migrate                   │
        └────────── ION CURRENT ─────────────────────┘
                   (inside solution)

Current = electron flow in wire + ion flow in solution
Both parts MUST work for the circuit to be complete
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

Practitioners constantly balance **maximizing conductivity** (more ions = lower resistance = more efficient current flow) against **avoiding unwanted reactions** (some electrolytes participate in electrode reactions you don't want). For water [[learning/notes/quick-context/electrolysis|electrolysis]], you want H₂ and O₂—but if you use NaCl as your electrolyte, chlorine gas forms at the anode instead of oxygen. The "ideal" electrolyte provides high ionic conductivity while remaining electrochemically inert at your operating voltages. Sulfuric acid (H₂SO₄) and sodium sulfate (Na₂SO₄) work well for water splitting because SO₄²⁻ is harder to oxidize than water. Concentration matters too: more electrolyte increases conductivity but can shift reaction selectivity, corrode equipment, or create disposal problems. Industrial processes carefully tune electrolyte composition, concentration, temperature, and pH to hit the sweet spot between efficiency and product purity.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Preparing an Electrolyte for Water Electrolysis

```
MAKING A SODIUM SULFATE ELECTROLYTE SOLUTION
════════════════════════════════════════════════════════════════════

Goal: Create a conductive solution for splitting water into H₂ and O₂
      without producing unwanted byproducts

Materials:
  - Distilled water: 1 liter
  - Sodium sulfate (Na₂SO₄): ~30 grams (makes ~0.2 M solution)

Step 1: The Problem with Pure Water
─────────────────────────────────────
  Pure H₂O:  Conductivity ≈ 0.05 μS/cm
             Only ~10⁻⁷ mol/L of H⁺ and OH⁻

             H₂O ⇌ H⁺ + OH⁻    (barely happens)

  Result: Almost no current flows, no gas production

Step 2: Dissolving the Electrolyte
───────────────────────────────────
  Add Na₂SO₄ to water:

       Na₂SO₄(s)  →  2Na⁺(aq) + SO₄²⁻(aq)
       ─────────     ─────────────────────
       solid         free ions in solution
       (no charge    (carry current!)
        movement)

  Na₂SO₄ is a STRONG electrolyte: 100% dissociation

  0.2 M Na₂SO₄ gives:
    - 0.4 M Na⁺ ions
    - 0.2 M SO₄²⁻ ions
    - Conductivity jumps to ~25,000 μS/cm (500,000× increase!)

Step 3: Why Na₂SO₄ Works
─────────────────────────
  At the ANODE (+):
    - SO₄²⁻ arrives but is HARD to oxidize (needs >2V)
    - H₂O is EASIER to oxidize (needs 1.23V)
    - Result: O₂ forms, not sulfur compounds ✓

  At the CATHODE (-):
    - Na⁺ arrives but is HARD to reduce (needs -2.71V)
    - H₂O is EASIER to reduce
    - Result: H₂ forms, not sodium metal ✓

  The Na₂SO₄ carries current WITHOUT participating in reactions!

Comparison of Common Electrolytes:
┌─────────────────┬──────────────┬─────────────────────────────────┐
│ Electrolyte     │ Type         │ Notes for Water Electrolysis    │
├─────────────────┼──────────────┼─────────────────────────────────┤
│ H₂SO₄ (dilute)  │ Acid         │ Excellent. H⁺ aids cathode rxn. │
│ NaOH / KOH      │ Base         │ Excellent. OH⁻ aids anode rxn.  │
│ Na₂SO₄          │ Neutral salt │ Good. Inert, safe, no fumes.    │
│ NaCl            │ Neutral salt │ BAD! Makes Cl₂ gas at anode.    │
│ Pure water      │ (none)       │ Won't work. No conductivity.    │
└─────────────────┴──────────────┴─────────────────────────────────┘
```

**The one thing most outsiders get wrong about this is...** thinking that water itself conducts electricity. Water is the *solvent*, not the conductor. The conductivity you experience (getting shocked in a bathtub, for instance) comes from dissolved salts, minerals, and impurities acting as electrolytes. Deionized water is so non-conductive it's used to rinse electronics. The electrolyte's ions do the actual charge-carrying work—they physically migrate through the solution, which is fundamentally different from how metals conduct (where electrons flow while atoms stay put).

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/electrolysis]]** — Electrolytes are essential for electrolysis; they provide the ion pathway that makes electrode reactions possible.

- **[[quick-context/making-electrolytes]]** — Detailed guide on how acids, bases, and salts create electrolytes through dissociation.

- **[[quick-context/electrodes]]** — The cathode and anode where ions exchange electrons; electrolytes deliver ions to these surfaces.

- **[[quick-context/cations-and-reduction]]** — Positive ions (cations) in the electrolyte migrate to the cathode and gain electrons.

- **[[quick-context/anions-and-oxidation]]** — Negative ions (anions) in the electrolyte migrate to the anode and lose electrons.

- **[[quick-context/voltage-thermodynamics-electrolysis]]** — The minimum voltage needed relates to which ions in the electrolyte will react first.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A student uses table salt (NaCl) as the electrolyte for water electrolysis. They notice a strong chlorine smell instead of getting pure oxygen at the anode. Why did this happen, and what electrolyte should they use instead?
<details>
<summary>Answer</summary>
Chloride ions (Cl⁻) are easier to oxidize than water at the anode, so chlorine gas (Cl₂) forms instead of oxygen. They should use an electrolyte with an anion that's harder to oxidize than water, such as sodium sulfate (Na₂SO₄), dilute sulfuric acid (H₂SO₄), or sodium hydroxide (NaOH). See: Concrete Example (Why Na₂SO₄ Works)
</details>

**Q2:** Pure distilled water has a conductivity of ~0.05 μS/cm, while seawater has ~50,000 μS/cm. What accounts for this million-fold difference?
<details>
<summary>Answer</summary>
Seawater contains ~3.5% dissolved salts (primarily NaCl, plus MgCl₂, MgSO₄, etc.) that dissociate into free ions. These ions carry electric current through the solution. Distilled water has essentially no dissolved ions—only the tiny amount from water's autoionization (10⁻⁷ M). See: The Core Problem
</details>

**Q3:** Why is sodium sulfate considered a "better" electrolyte than sodium chloride for water electrolysis, even though both fully dissociate and provide similar conductivity?
<details>
<summary>Answer</summary>
Selectivity, not conductivity, is the issue. Sulfate ions (SO₄²⁻) have a higher [[learning/notes/micro-context/oxidation|oxidation]] potential than water and remain inert at the anode. Chloride ions (Cl⁻) oxidize more easily than water, producing chlorine gas instead of oxygen. The electrolyte must conduct current without chemically participating in the electrode reactions. See: The Key Tension
</details>

**Q4:** Acetic acid (vinegar) is a weak electrolyte while hydrochloric acid is a strong electrolyte. If you made two solutions with equal molar concentrations, which would have higher conductivity and why?
<details>
<summary>Answer</summary>
Hydrochloric acid would have much higher conductivity. Strong electrolytes like HCl dissociate 100% into ions (H⁺ and Cl⁻), while weak electrolytes like acetic acid only partially dissociate (~1%). Same concentration of acid, but far fewer free ions in the acetic acid solution. See: 5 Essential Terms (strong vs. weak electrolyte)
</details>

**Q5:** In a lead-acid car battery, why does battery performance drop dramatically in cold weather?
<details>
<summary>Answer</summary>
The electrolyte (dilute sulfuric acid) has reduced ion mobility at low temperatures—ions move more slowly through the cold, viscous solution, increasing internal resistance and reducing the current the battery can deliver. This is why "cold cranking amps" is a key battery specification. See: The Key Tension (conductivity depends on conditions)
</details>

</details>
