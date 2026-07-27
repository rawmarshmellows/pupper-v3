---
topic: Voltage and Thermodynamic Relationship in Electrolysis
created: 2026-01-22
---

> **Related:** [[learning/notes/quick-context/electrolysis]] | [[learning/notes/quick-context/electric-current]] | [[learning/notes/quick-context/galvanic-cells-batteries]] | [[learning/notes/quick-context/electricity-generation]] | [[learning/notes/quick-context/making-electrolytes]]

> **TL;DR:** The equation dG = -nFE links the energy requirement of a reaction (Gibbs free energy) to the minimum [[learning/notes/quick-context/voltage|voltage]] needed for [[learning/notes/quick-context/electrolysis|electrolysis]], with water splitting requiring at least 1.23V theoretically but 1.8-2.5V in practice due to overpotential losses.

# Voltage and Thermodynamic Relationship in Electrolysis

## The Core Problem

[[quick-context/electrolysis|Electrolysis]] forces chemical reactions that wouldn't happen on their own, but how much electricity do you actually need? The equation **ΔG = -nFE** connects the energy requirement of a reaction (Gibbs free energy) to the minimum voltage you must apply. For water splitting, this translates to a theoretical minimum of **1.23 volts**—without this relationship, we'd have no rational way to design electrochemical systems, batteries, fuel cells, or industrial hydrogen production.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Gibbs Free Energy (ΔG)** | The total energy a reaction needs (positive) or releases (negative)—think of it as the "energy price tag" of a chemical change |
| **Overpotential** | Extra voltage beyond the theoretical minimum, wasted fighting real-world inefficiencies like sluggish electrodes and resistance |
| **Faraday Constant (F)** | A conversion factor (96,485 C/mol) that translates between "chemistry units" (moles of electrons) and "electricity units" (coulombs) |
| **Cell Potential (E)** | The voltage that corresponds to a reaction's energy requirement—directly calculated from Gibbs free energy |
| **Non-spontaneous** | A reaction that won't happen unless you force it with external energy (like pushing a ball uphill) |

## What Does "Non-Spontaneous" Mean?

```
SPONTANEOUS REACTION                    NON-SPONTANEOUS REACTION
(Happens on its own)                    (Needs energy input)

    Ball rolls downhill                     Ball must be pushed uphill

         O                                           ___
        /|\                                         /   \
         |   ↓                                     |  O  | ← YOU PUSHING
        / \  ↓                                     | /|\ |
    ~~~~~~~~~~~~\                            ~~~~~~|  |  |~~~~~~
                 \____                       ______|/ \ \|
                                            /
                                           /

    ΔG < 0 (negative)                       ΔG > 0 (positive)
    Energy is RELEASED                      Energy must be ADDED
    Example: Burning wood                   Example: Splitting water
```

Water splitting has **ΔG = +237 kJ/mol**. The "+" sign is crucial—it means you must *add* that much energy per mole of water split.

<details>
<summary><strong>How It Works</strong></summary>

The voltage-thermodynamics relationship operates through a straightforward energy conversion: electrical work (voltage times charge) must equal or exceed the chemical energy requirement (Gibbs free energy). When you apply voltage to an electrolysis cell, you're providing electrical potential energy that gets converted into chemical potential energy stored in the products. The equation ΔG = -nFE bridges these two energy forms, where n electrons each carrying charge F (the Faraday constant) are pushed through potential E. For the reaction to proceed, the electrical energy supplied (nFE) must at least match what the chemistry demands (ΔG).

The process unfolds at two electrodes immersed in an [[learning/notes/quick-context/electrolyte|electrolyte]]. At the [[learning/notes/micro-context/cathode|cathode]] (negative electrode), electrons arrive and force a reduction reaction—in water splitting, hydrogen ions grab electrons to become hydrogen gas. At the [[learning/notes/micro-context/anode|anode]] (positive electrode), electrons are pulled away, forcing [[learning/notes/micro-context/oxidation|oxidation]]—water molecules lose electrons to become oxygen gas. The electrolyte provides a path for ions to migrate between electrodes, completing the circuit internally while electrons flow through the external circuit. The minimum voltage (1.23V for water) represents the thermodynamic floor: the absolute minimum electrical "push" needed to make both electrode reactions energetically possible.

```
ENERGY FLOW IN ELECTROLYSIS
════════════════════════════════════════════════════════════════════

         POWER SUPPLY
        ┌───────────┐
        │  + 1.23V  │ (minimum)
        └─────┬─────┘
              │
    ──────────┼──────────── ELECTRICAL ENERGY INPUT
              │                 (Voltage × Current × Time)
              ▼
    ┌─────────────────────────────────────────────────────────┐
    │                   ELECTROLYSIS CELL                     │
    │                                                         │
    │   CATHODE (-)              ANODE (+)                    │
    │   ┌─────────┐              ┌─────────┐                  │
    │   │  2H⁺ +  │              │  H₂O →  │                  │
    │   │  2e⁻ →  │              │ ½O₂ +   │                  │
    │   │   H₂    │              │  2H⁺ +  │                  │
    │   │         │              │   2e⁻   │                  │
    │   └────┬────┘              └────┬────┘                  │
    │        │    ←── H⁺ ions ───     │                       │
    │        │       (electrolyte)    │                       │
    │        └────────────────────────┘                       │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
              │
              ▼
    ──────────────────────── CHEMICAL ENERGY STORED
                                (ΔG = +237 kJ/mol)
                                   in H₂ and O₂ bonds

    THE CONVERSION:
    ┌────────────────────────────────────────────────────────┐
    │  Electrical Work  =  Chemical Energy Stored            │
    │       nFE         =         ΔG                         │
    │                                                        │
    │  (2 mol e⁻)(96,485 C/mol)(1.23 V) = 237,000 J          │
    │                                                        │
    │  Voltage is just energy-per-electron translated        │
    │  into volts (joules per coulomb)                       │
    └────────────────────────────────────────────────────────┘
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

Here's what practitioners argue about constantly: **the gap between theoretical voltage and real-world voltage**. Theory says 1.23V should split water. Reality demands 1.8–2.5V. That extra voltage is called **overpotential**, and it's the enemy of efficiency.

```
VOLTAGE BREAKDOWN IN REAL ELECTROLYSIS
═══════════════════════════════════════════════════════════════

                    ┌─────────────────────────────────────┐
                    │         TOTAL APPLIED VOLTAGE       │
                    │            (1.8 - 2.5 V)            │
                    └─────────────────────────────────────┘
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           │                         │                         │
           ▼                         ▼                         ▼
    ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
    │ THEORETICAL │          │  ACTIVATION │          │  RESISTANCE │
    │   MINIMUM   │          │ OVERPOTENTIAL│         │    LOSSES   │
    │   1.23 V    │          │  (Kinetic    │          │  (Ohmic)    │
    │             │          │   barriers)  │          │             │
    │ "The energy │          │ "Sluggish    │          │ "Electrons  │
    │  the rxn    │          │  electrode   │          │  fighting   │
    │  actually   │          │  surfaces"   │          │  through    │
    │  needs"     │          │              │          │  the wire"  │
    └─────────────┘          └─────────────┘          └─────────────┘
         │                         │                         │
         │    THERMODYNAMICS       │      KINETICS           │   PHYSICS
         │    (unavoidable)        │   (can be reduced)      │  (can be
         │                         │                         │   reduced)
         └─────────────────────────┴─────────────────────────┘
```

**What engineers optimize:**
| Factor | Problem | Solution Approaches |
|--------|---------|---------------------|
| Activation overpotential | Electrode surfaces resist reaction | Better catalysts (platinum, iridium) |
| Concentration overpotential | Reactants can't reach electrode fast enough | Better flow design, stirring |
| Ohmic losses | Resistance in wires, electrolyte, membranes | Shorter distances, better conductors |

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Let's walk through the actual calculation for water electrolysis:

**The Reaction:**
```
2 H₂O (liquid) → 2 H₂ (gas) + O₂ (gas)
```

**Given Information:**
- ΔG = +237 kJ/mol (energy required per mole of H₂O split)
- n = 2 (two electrons transferred per water molecule)
- F = 96,485 C/mol (Faraday constant)

**The Master Equation:**
```
ΔG = -nFE

Solving for E (voltage):

E = -ΔG / (nF)
```

**Step-by-Step Calculation:**
```
Step 1: Convert kJ to J
        237 kJ/mol = 237,000 J/mol

Step 2: Plug into equation
        E = -ΔG / (nF)
        E = -(+237,000 J/mol) / (2 × 96,485 C/mol)

Step 3: Calculate
        E = -237,000 / 192,970
        E = -1.23 V

Step 4: Interpret the sign
        The NEGATIVE result means we must APPLY +1.23 V
        (We're reversing a spontaneous direction)
```

**Visual Summary:**
```
WHAT THE NUMBERS MEAN
═════════════════════

    ΔG = +237 kJ/mol
         ↑
         │ positive = non-spontaneous
         │ (nature doesn't want to do this)
         │
         ▼
    ┌─────────────────────────────────────────┐
    │           ΔG = -nFE                     │
    │                                         │
    │  "Energy needed = electrons × Faraday   │
    │                   constant × voltage"   │
    └─────────────────────────────────────────┘
         │
         ▼
    E = 1.23 V (theoretical minimum)
         │
         │ BUT IN REALITY...
         ▼
    ┌─────────────────────────────────────────┐
    │  Real systems need 1.8 - 2.5 V          │
    │                                         │
    │  Extra 0.6-1.3 V = OVERPOTENTIAL        │
    │  (the "tax" you pay for imperfection)   │
    └─────────────────────────────────────────┘
```

**Efficiency Calculation:**
```
Efficiency = (Theoretical Voltage / Actual Voltage) × 100%

Best case:  (1.23 / 1.8) × 100% = 68% efficient
Worst case: (1.23 / 2.5) × 100% = 49% efficient

    THEORETICAL        ACTUAL           WASTED
    ┌──────────┐   ┌───────────────┐
    │  1.23 V  │ + │  0.6-1.3 V    │ = 1.8-2.5 V
    │  (useful)│   │  (overpotential)│
    └──────────┘   └───────────────┘
        68%              32%           (best case)
        49%              51%           (worst case)
```

**The one thing most outsiders get wrong about this is...** assuming that "theoretical minimum voltage" means you can actually run an electrolyzer at that voltage. You can't. The 1.23V is a thermodynamic floor—the absolute minimum energy the chemistry demands. But chemistry also has *kinetics* (how fast things happen), and coaxing electrons through real materials with real surfaces at practical speeds always costs extra. It's like knowing a trip is 100 miles—that's the minimum distance—but traffic, hills, and detours mean you'll actually drive 130-150 miles. Engineers spend careers shaving fractions of a volt off that overpotential because in industrial hydrogen production, those fractions translate to millions of dollars in electricity costs.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/electrolysis]]** — The broader process that this voltage relationship enables; understanding the full electrolysis cell setup ([[quick-context/electrodes|anode]], [[quick-context/electrodes|cathode]], [[quick-context/making-electrolytes|electrolyte]]) provides essential context for where these voltages are applied.

- **Electrochemistry fundamentals** — The study of chemical reactions that produce or consume electricity; this relationship is one specific application of broader electrochemical principles like the Nernst equation.

- **Catalysis** — The science of speeding up reactions without being consumed; platinum and iridium catalysts on electrodes are how engineers reduce activation overpotential.

- **Thermodynamics (entropy and enthalpy)** — Gibbs free energy combines enthalpy (heat content) and entropy (disorder); understanding these components explains *why* ΔG has the value it does.

- **Hydrogen economy** — The vision of using hydrogen as a clean fuel; the efficiency of electrolysis (determined by overpotential) is a key bottleneck in making "green hydrogen" economically viable.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** If a reaction has a negative ΔG value, does that mean you need to apply voltage to make it happen?
<details>
<summary>Answer</summary>
No—a negative ΔG means the reaction is spontaneous and will happen on its own, actually *releasing* energy. You would need to apply voltage only for positive ΔG reactions. Water electrolysis has ΔG = +237 kJ/mol (positive), which is why it requires external electricity. See: The Core Problem It Solves
</details>

**Q2:** An engineer improves an electrolyzer from requiring 2.2V down to 1.9V while still producing the same amount of hydrogen. What specifically did they reduce?
<details>
<summary>Answer</summary>
They reduced the overpotential by 0.3V. The theoretical minimum (1.23V) is fixed by thermodynamics and cannot be changed—it's determined by the chemistry itself. The improvement must have come from reducing activation overpotential (better catalysts), concentration overpotential (better flow), or ohmic losses (better conductors). See: The Key Tension
</details>

**Q3:** In the equation ΔG = -nFE, what does "n" represent and why does it matter for calculating voltage?
<details>
<summary>Answer</summary>
"n" represents the number of electrons transferred per molecule in the reaction. It matters because voltage is energy *per electron*—more electrons means the same total energy (ΔG) is spread across more charge carriers, resulting in a lower voltage requirement per electron. For water, n=2 because each water molecule requires 2 electrons to split. See: A Concrete Example
</details>

**Q4:** Why can't you run a commercial water electrolyzer at exactly 1.23 volts, even with perfect equipment?
<details>
<summary>Answer</summary>
Because 1.23V is only the thermodynamic minimum—the energy the chemistry fundamentally requires. Real systems face kinetic barriers (activation overpotential from sluggish electrode surfaces), mass transport limitations (concentration overpotential), and electrical resistance (ohmic losses). These factors are never zero in real materials, so practical systems always need 1.8-2.5V. See: The one thing most outsiders get wrong...
</details>

**Q5:** If overpotential is "wasted" energy, where does that energy actually go?
<details>
<summary>Answer</summary>
It becomes heat. The extra voltage beyond 1.23V drives current through resistive materials and overcomes kinetic barriers, both of which convert electrical energy to thermal energy. This is why electrolyzers need cooling systems and why reducing overpotential improves both efficiency and thermal management. See: The Key Tension (Voltage Breakdown diagram)
</details>

</details>
