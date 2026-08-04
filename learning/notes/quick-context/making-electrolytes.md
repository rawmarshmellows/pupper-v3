---
topic: How to Make an Electrolyte (Acid, Base, or Salt)
created: 2026-01-22
---

> **Related:** [[quick-context/electrolysis]]

> **TL;DR:** Pure water is almost a perfect insulator - you must add an electrolyte (acid, base, or salt) to create mobile ions that carry electrical current. The electrolyte dissociates into charged particles that enable electricity to flow through the liquid.

# How to Make an Electrolyte (Acid, Base, or Salt)

## The Core Problem: Pure Water Does Not Conduct Electricity

Here is a fact that surprises most people: **pure water is almost a perfect insulator**. If you stick two [[quick-context/electrodes|electrodes]] into distilled water and apply [[quick-context/voltage|voltage]], almost nothing happens. No bubbles. No current. Why? Because electricity travels through liquids only when there are charged particles (called **ions**) free to move around. Pure water has almost none—only about 0.0000001 moles per liter (written as 10^-7 M), giving it a conductivity of roughly 0.05 microsiemens per centimeter. That is essentially zero. Without ions to carry the electrical charge from one electrode to the other, the circuit cannot complete. This is the fundamental reason you must add an **[[quick-context/electrolyte|electrolyte]]**—a substance that creates mobile ions in water—before [[quick-context/electrolysis|electrolysis]] (using electricity to split water or other compounds) can work.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Ion** | An atom or molecule with an electrical charge (+ or -) because it lost or gained electrons. Like a person carrying either a positive or negative flag. |
| **Electrolyte** | A substance that creates free-moving ions when dissolved in water (or melted), allowing the liquid to conduct electricity. Like adding "electricity carriers" to water. |
| **Dissociation** | The process where a compound splits into its component ions when dissolved. Like a team breaking into individual players who can now run around the field. |
| **Conductivity** | A measure of how well a solution carries electrical current (more ions = higher conductivity). Like measuring how wide a highway is for traffic. |
| **Molten salt** | A salt heated until it melts into liquid form, where ions can move freely without needing water. Like melting ice so the water molecules can flow. |

<details>
<summary><strong>How It Works</strong></summary>

When you add an electrolyte to water, the compound **dissociates**—it splits apart into its constituent ions. This happens because water molecules are **polar**: the oxygen end carries a partial negative charge, and the hydrogen ends carry partial positive charges. When a salt crystal (like NaCl) contacts water, the water molecules surround the ions on the crystal's surface. The partially negative oxygens attract the positive sodium ions (Na+), while the partially positive hydrogens attract the negative chloride ions (Cl-). These attractions are strong enough to pull individual ions away from the crystal lattice, one by one, until the entire crystal dissolves.

Once freed, the ions become **mobile charge carriers**. When you apply a voltage across two electrodes in the solution, the positive ions (cations) migrate toward the negative electrode ([[micro-context/cathode|cathode]]), while the negative ions (anions) migrate toward the positive electrode ([[micro-context/anode|anode]]). This movement of charged particles IS the [[quick-context/electric-current|electric current]] through the liquid. The more ions you have dissolved, the more charge carriers are available, and the higher the solution's conductivity. This is why adding more electrolyte (up to the saturation limit) increases conductivity proportionally.

```
HOW ELECTROLYTES ENABLE CONDUCTION
==================================

STEP 1: DISSOLUTION - Salt crystal meets water
──────────────────────────────────────────────

    SOLID CRYSTAL                    WATER MOLECULES
    (ions locked)                    (polar - has + and - ends)

    Na⁺─Cl⁻─Na⁺                         H    H
    │    │    │                          ╲  ╱
    Cl⁻─Na⁺─Cl⁻    +    H₂O    →        O    (δ-) oxygen end
    │    │    │                         (δ+) hydrogen ends
    Na⁺─Cl⁻─Na⁺

                    ↓ Water molecules pull ions apart ↓

              H₂O        H₂O                H₂O        H₂O
                 ╲      ╱                      ╲      ╱
            H₂O─  Na⁺  ─H₂O              H₂O─  Cl⁻  ─H₂O
                 ╱      ╲                      ╱      ╲
              H₂O        H₂O                H₂O        H₂O

              (hydrated cation)            (hydrated anion)


STEP 2: ION MIGRATION - Voltage applied
───────────────────────────────────────

    CATHODE (-)                                      ANODE (+)
        │                                                │
        │    ←───── Na⁺  ←───── Na⁺  ←───── Na⁺        │
        │                                                │
        │     Cl⁻ ─────→  Cl⁻ ─────→  Cl⁻ ─────→       │
        │                                                │
    ════╪════════════════════════════════════════════════╪════
        │           SOLUTION (electrolyte)               │

    Cations move LEFT (toward -)     Anions move RIGHT (toward +)

              ═══════════════════════════════════
                   THIS MOVEMENT = CURRENT
              ═══════════════════════════════════


CONDUCTIVITY VS. CONCENTRATION
──────────────────────────────

Conductivity │                           ●  SATURATION
(μS/cm)      │                      ● ╱    (no more dissolves)
             │                  ●  ╱
             │              ●  ╱
             │          ●  ╱
             │      ●  ╱
             │  ●  ╱      ← Linear region:
             │●╱            more salt = more ions = more conductivity
             │╱
             └────────────────────────────────────────────────►
               Pure     Low       Medium      High     Saturated
               water    conc.     conc.       conc.    solution
```

**What is an ion?** Ions are just atoms (or groups of atoms) that have gained or lost electrons, giving them an electrical charge. A positive ion (cation) like Na+ has lost an electron; a negative ion (anion) like Cl- has gained one. These charged particles can move through liquid, carrying electricity with them.

```
ATOMS AND IONS - A Visual Guide
════════════════════════════════════════════════════════════════════

NORMAL ATOM (Sodium - Na)
─────────────────────────

       Nucleus: 11 protons (+)      Electrons: 11 (-)
       ┌─────────────────┐          ┌─────────────────┐
       │  (+)(+)(+)(+)   │          │  (-)(-)(-)(-)(-)│
       │  (+)(+)(+)(+)   │          │  (-)(-)(-)(-)(-)│
       │  (+)(+)(+)      │          │  (-)           │
       └─────────────────┘          └─────────────────┘
            11 +                         11 -
                    ══════════════
                    Total: NEUTRAL (11+ and 11- cancel out)


POSITIVE ION (Sodium Ion - Na⁺)
───────────────────────────────
What happens when sodium LOSES one electron:

       Nucleus: 11 protons (+)      Electrons: only 10 now (-)
       ┌─────────────────┐          ┌─────────────────┐
       │  (+)(+)(+)(+)   │          │  (-)(-)(-)(-)(-)│
       │  (+)(+)(+)(+)   │          │  (-)(-)(-)(-)(-)│
       │  (+)(+)(+)      │          │                 │  ← Lost one!
       └─────────────────┘          └─────────────────┘
            11 +                         10 -
                    ══════════════
                    Total: +1 POSITIVE CHARGE (called a CATION)


NEGATIVE ION (Chloride Ion - Cl⁻)
─────────────────────────────────
What happens when chlorine GAINS one electron:

       Nucleus: 17 protons (+)      Electrons: 18 now (-)
       ┌─────────────────┐          ┌─────────────────────┐
       │  (+)(+)(+)(+)   │          │  (-)(-)(-)(-)(-)(-)│
       │  (+)(+)(+)(+)   │          │  (-)(-)(-)(-)(-)(-)│
       │  (+)(+)(+)(+)   │          │  (-)(-)(-)(-)(-)(-)│
       │  (+)(+)(+)(+)   │          │                    │
       │  (+)            │          │                    │
       └─────────────────┘          └─────────────────────┘
            17 +                         18 -
                    ══════════════
                    Total: -1 NEGATIVE CHARGE (called an ANION)
```

There are three categories of electrolytes that create ions when dissolved in water (or when melted):

```
┌─────────────────────────────────────────────────────────────────────┐
│                    THE THREE ELECTROLYTE TYPES                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   1. ACIDS         2. BASES         3. SALTS                        │
│   ──────────       ──────────       ────────                        │
│   Release H⁺       Release OH⁻      Release metal +                 │
│   (hydrogen        (hydroxide       and non-metal -                 │
│   ions)            ions)            ions                            │
│                                                                     │
│   Examples:        Examples:        Examples:                       │
│   • H₂SO₄          • NaOH           • NaCl (table salt)             │
│     (sulfuric        (sodium          Na⁺ + Cl⁻                     │
│      acid)           hydroxide,                                     │
│   • HCl              "lye")        • Na₂SO₄                         │
│     (hydrochloric  • KOH             (sodium sulfate)               │
│      acid)           (potassium       2Na⁺ + SO₄²⁻                  │
│                      hydroxide)                                     │
│                                                                     │
│   TASTE: Sour      TASTE: Bitter    TASTE: Salty                   │
│   (don't test!)    (don't test!)    (only for table salt!)          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

When you add salt to water, something remarkable happens at the molecular level (related to [[quick-context/chemical-bonds-spectrum|chemical bonds]]):

```
DISSOLVING TABLE SALT (NaCl) IN WATER
═══════════════════════════════════════════════════════════════════════

BEFORE: Solid salt crystal (ions locked in place, cannot move)
─────────────────────────────────────────────────────────────

    Na⁺ Cl⁻ Na⁺ Cl⁻ Na⁺
    Cl⁻ Na⁺ Cl⁻ Na⁺ Cl⁻     ← Ions are stuck in a rigid grid
    Na⁺ Cl⁻ Na⁺ Cl⁻ Na⁺       (called a "crystal lattice")
    Cl⁻ Na⁺ Cl⁻ Na⁺ Cl⁻       Cannot conduct electricity!

                    ↓ ADD WATER ↓

AFTER: Dissolved salt (ions free to move)
─────────────────────────────────────────

                   H₂O  H₂O
               H₂O       H₂O
           H₂O    Na⁺        H₂O    ← Water molecules surround
               H₂O       H₂O          each ion (called "solvation")
                   H₂O  H₂O

                   H₂O  H₂O
               H₂O       H₂O
           H₂O    Cl⁻        H₂O    ← Now ions can move freely
               H₂O       H₂O          through the liquid!
                   H₂O  H₂O

═══════════════════════════════════════════════════════════════════════
RESULT: Free-floating Na⁺ and Cl⁻ ions can now carry electrical current
═══════════════════════════════════════════════════════════════════════
```

**Why does water pull apart salt?** Water molecules have a slight charge imbalance (they are "polar")—the oxygen end is slightly negative, the hydrogen ends are slightly positive. This lets water molecules surround and "pull apart" the ions from each other, one by one.

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

When choosing an electrolyte, practitioners face a fundamental tradeoff. You want **high conductivity** (lots of ions = [[quick-context/electric-current|electricity flows easily]]), but you also want the electrolyte to **not interfere** with the reaction you are trying to achieve. The ions must carry [[quick-context/electric-current|current]] without themselves being the substances that react at the [[quick-context/electrodes|electrodes]].

```
THE ELECTROLYTE SELECTION TRADEOFF
═══════════════════════════════════════════════════════════════════════

                         HIGH CONDUCTIVITY
                               ▲
                               │
        More ions = better     │
        electricity flow       │
                               │
        BUT...                 │     "Sweet Spot"
                               │        ╭───╮
        Some ions can          │       ╱     ╲
        react at electrodes,   │      │   ●   │  ← Want to be here:
        contaminating your     │       ╲     ╱     enough ions, but
        product or consuming   │        ╰───╯      they don't interfere
        your electrodes!       │
                               │
                               └──────────────────────────►
                                   CHEMICAL STABILITY
                                   (ions don't interfere
                                    with desired reaction)

═══════════════════════════════════════════════════════════════════════

EXAMPLE: Water Electrolysis
───────────────────────────

GOAL: Split H₂O → H₂ (hydrogen gas) + O₂ (oxygen gas)

GOOD ELECTROLYTE CHOICES:                 WHY THEY WORK:
─────────────────────────                 ─────────────────
• Dilute H₂SO₄ (sulfuric acid)           SO₄²⁻ does not get oxidized
                                          before water does

• NaOH or KOH (bases)                     Na⁺/K⁺ do not get reduced
                                          before water does

• Na₂SO₄ (sodium sulfate)                Neither ion interferes—they
                                          just carry the current

BAD ELECTROLYTE CHOICE:                   WHY IT FAILS:
───────────────────────                   ─────────────────
• NaCl (table salt)                       Cl⁻ gets oxidized at the anode,
                                          producing toxic chlorine gas
                                          instead of oxygen!
```

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Here is a step-by-step walkthrough of preparing an electrolyte solution:

```
RECIPE: Sodium Sulfate Electrolyte for Water Electrolysis
═══════════════════════════════════════════════════════════════════════

MATERIALS NEEDED:
─────────────────
• Distilled water: 1 liter
• Sodium sulfate (Na₂SO₄): ~30 grams (about 2 tablespoons)
• Clean container (glass or plastic, NOT metal)
• Stirring rod

PROCEDURE:
──────────

Step 1: Start with distilled water
    ┌─────────────────────┐
    │                     │
    │   H₂O  H₂O  H₂O    │   Conductivity: ~0.05 μS/cm
    │      H₂O  H₂O      │   (almost zero!)
    │   H₂O  H₂O  H₂O    │
    │                     │
    └─────────────────────┘

Step 2: Add sodium sulfate powder
    ┌─────────────────────┐
    │                     │
    │   H₂O  H₂O  H₂O    │     Na₂SO₄ powder
    │      H₂O  H₂O      │  ←  (solid crystals)
    │   H₂O ██████ H₂O   │
    │                     │
    └─────────────────────┘

Step 3: Stir until fully dissolved
    ┌─────────────────────┐
    │  Na⁺  SO₄²⁻   Na⁺  │
    │     Na⁺   SO₄²⁻    │   Conductivity: ~10,000 μS/cm
    │  SO₄²⁻  Na⁺  Na⁺   │   (200,000x increase!)
    │     SO₄²⁻   Na⁺    │
    └─────────────────────┘

Step 4: Ready for electrolysis!

         DC Power Supply
          (-)     (+)
           │       │
           ▼       ▼
    ┌─────────────────────┐
    │  Na⁺  SO₄²⁻   Na⁺  │
    │     ↙           ↘   │   ← Ions carry current through solution
    │  CATHODE    ANODE   │     while WATER reacts at electrodes
    │    (-)       (+)    │
    │     │         │     │
    │    H₂↑       O₂↑   │   ← Gases produced (the actual goal!)
    └─────────────────────┘

═══════════════════════════════════════════════════════════════════════

WHAT IS HAPPENING:
──────────────────
• Na⁺ ions migrate toward the negative [[quick-context/electrodes|cathode]] (but don't react)
• SO₄²⁻ ions migrate toward the positive [[quick-context/electrodes|anode]] (but don't react)
• This ion movement completes the electrical circuit
• At the electrodes, WATER molecules are what actually react:
  - Cathode: 2H₂O + 2e⁻ → H₂ + 2OH⁻ ([[quick-context/cations-and-reduction|reduction]])
  - Anode: 2H₂O → O₂ + 4H⁺ + 4e⁻ ([[quick-context/anions-and-oxidation|oxidation]])
```

**Alternative Electrolytes Compared:**

| Electrolyte | Formula | What It Adds | Conductivity | Pros | Cons |
|-------------|---------|--------------|--------------|------|------|
| Sulfuric acid (dilute) | H₂SO₄ | H⁺, SO₄²⁻ | Very high | Excellent conductivity, cheap | Corrosive, dangerous |
| Sodium hydroxide | NaOH | Na⁺, OH⁻ | Very high | Great for industrial use | Caustic, burns skin |
| Potassium hydroxide | KOH | K⁺, OH⁻ | Very high | Slightly better than NaOH | More expensive |
| Sodium sulfate | Na₂SO₄ | Na⁺, SO₄²⁻ | High | Safe, non-corrosive | Slightly lower conductivity |
| Baking soda | NaHCO₃ | Na⁺, HCO₃⁻ | Moderate | Safe, household item | Lower conductivity, CO₂ issues |

**Special Case: Molten Salt Electrolytes.** Sometimes you cannot use water at all. To extract highly reactive metals like sodium, lithium, or aluminum, you must melt the salt itself:

```
MOLTEN SALT ELECTROLYSIS (No Water Involved)
═══════════════════════════════════════════════════════════════════════

WHY CAN'T WE USE WATER?
───────────────────────
For metals like sodium (Na), the metal is MORE reactive than water.
If you try to electrolyze NaCl solution (salt water):

    At cathode: Water gets reduced INSTEAD of Na⁺
                2H₂O + 2e⁻ → H₂ + 2OH⁻  ← This happens
                Na⁺ + e⁻ → Na           ← This does NOT happen

    You get hydrogen gas, not sodium metal!

SOLUTION: Remove the water entirely
───────────────────────────────────

    Heat NaCl to 801°C (its melting point)

    SOLID NaCl                    MOLTEN NaCl
    ┌────────────┐                ┌────────────┐
    │Na⁺Cl⁻Na⁺Cl⁻│   HEAT →      │  Cl⁻  Na⁺  │
    │Cl⁻Na⁺Cl⁻Na⁺│   801°C       │ Na⁺    Cl⁻ │
    │Na⁺Cl⁻Na⁺Cl⁻│               │   Cl⁻ Na⁺  │
    └────────────┘                └────────────┘
     Ions locked in               Ions free to
     rigid crystal                move (liquid!)

    Now electrolysis produces:
    • Cathode: Na⁺ + e⁻ → Na (liquid sodium metal!)
    • Anode: 2Cl⁻ → Cl₂ + 2e⁻ (chlorine gas)

═══════════════════════════════════════════════════════════════════════
```

**The one thing most outsiders get wrong about this is...** assuming that water itself conducts electricity. Movies show people being electrocuted in bathtubs or pools, but pure water is actually an insulator. What conducts is the **dissolved stuff** in the water—minerals, salts, chlorine in pool water, soap residue. Tap water conducts reasonably well because of dissolved minerals. Distilled or deionized water barely conducts at all. This misconception leads to a common failed experiment: someone tries to split water with a battery and two wires, uses distilled water, and wonders why nothing happens. The answer is simple—you forgot the electrolyte! You must add ions for the electricity to have something to "ride on" through the liquid.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/electrolysis]]** — The process that actually uses these electrolytes. Understanding electrolysis explains WHY you need electrolytes and what happens at the electrodes once current flows.

- **[[quick-context/chemical-bonds-spectrum]]** — Understanding ionic vs. [[quick-context/covalent-bonds|covalent bonds]] helps explain why salts dissociate into ions (ionic bonds break easily in water) while covalent compounds like sugar do not.

- **pH and Acid-Base Chemistry** — Acids and bases are defined by whether they release H⁺ or OH⁻ ions. The pH scale measures this ion concentration, which directly affects conductivity.

- **Concentration and Molarity** — How much electrolyte you add matters. More dissolved salt = more ions = higher conductivity, but only up to a point (saturation limit).

- **Electrochemical Series** — A ranking of how easily different ions gain or lose electrons. This determines which electrolyte works for which application (and which would interfere with your reaction).

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** You have two beakers: one with distilled water, one with tap water. You connect a battery and light bulb in series with electrodes dipping into each. Which beaker lights the bulb, and why?
<details>
<summary>Answer</summary>
**The tap water beaker lights the bulb.** Tap water contains dissolved minerals (calcium, magnesium, chloride, etc.) that provide ions to conduct electricity. Distilled water has had these minerals removed, leaving almost no ions (only ~10^-7 M from water's autoionization), so it cannot conduct enough current to light the bulb. See: The Core Problem
</details>

**Q2:** You want to electrolyze water to produce hydrogen and oxygen. You have table salt (NaCl) and Epsom salt (MgSO₄) available. Which should you choose, and why?
<details>
<summary>Answer</summary>
**Choose Epsom salt (MgSO₄).** While both dissolve to create ions, NaCl releases chloride ions (Cl⁻) which get oxidized at the anode before water does, producing toxic chlorine gas instead of oxygen. MgSO₄ releases sulfate ions (SO₄²⁻) which are harder to oxidize than water, so they just carry current while water molecules react to form oxygen. See: The Key Tension (bad electrolyte choice example)
</details>

**Q3:** Why must aluminum be produced using molten salt [[quick-context/electrolysis|electrolysis]] rather than dissolving an aluminum compound in water?
<details>
<summary>Answer</summary>
**Aluminum is too reactive—water would be reduced instead.** Aluminum ions (Al³⁺) have a very negative reduction potential, meaning they "want" electrons less than water molecules do. In aqueous solution, the cathode would reduce water (producing hydrogen gas) before it would reduce Al³⁺ to aluminum metal. By using molten aluminum oxide (Al₂O₃) with no water present, Al³⁺ becomes the only reducible species, so aluminum metal forms. See: Special Case: Molten Salt Electrolytes
</details>

**Q4:** A solid salt crystal contains ions but does not conduct electricity. Why not?
<details>
<summary>Answer</summary>
**The ions are locked in a fixed crystal lattice and cannot move.** Electrical conduction requires mobile charge carriers. In a solid crystal, each Na⁺ and Cl⁻ is held rigidly in place by electrostatic attraction to its neighbors. Only when dissolved (ions surrounded and separated by water molecules) or melted (thermal energy overcomes the lattice forces) can the ions move freely to carry current. See: How Dissolving Creates Ions (the "BEFORE" diagram)
</details>

**Q5:** Baking soda (NaHCO₃) and washing soda (Na₂CO₃) both dissolve in water. If both solutions have the same molar concentration, which has more free ions and thus higher conductivity?
<details>
<summary>Answer</summary>
**Washing soda (Na₂CO₃) has higher conductivity.** Each formula unit of Na₂CO₃ produces 3 ions when dissolved (2 Na⁺ + 1 CO₃²⁻), while each NaHCO₃ produces only 2 ions (1 Na⁺ + 1 HCO₃⁻). At equal molar concentration, washing soda provides 50% more ions. Additionally, the carbonate ion (CO₃²⁻) carries twice the charge of bicarbonate (HCO₃⁻), further increasing current-carrying capacity. See: Alternative Electrolytes Compared (relationship between ion count and conductivity)
</details>

</details>
