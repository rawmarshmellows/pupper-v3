---
topic: Electrolysis
created: 2026-01-22
updated: 2026-01-22
---

> **Related:** [[learning/notes/quick-context/covalent-bonds]] | [[learning/notes/quick-context/electrolyte]] | [[learning/notes/micro-context/anode]] | [[learning/notes/micro-context/cathode]] | [[learning/notes/micro-context/oxidation]]

> **TL;DR:** Electrolysis uses electricity to force non-spontaneous chemical reactions (like splitting water into hydrogen and oxygen), essentially running a battery in reverse by supplying energy to break stable bonds rather than harvesting energy from spontaneous reactions.

# Electrolysis

## The Core Problem

Many important chemical changes won't happen on their own because they require climbing to a higher energy state. Electrolysis uses electricity to push these non-spontaneous reactions forward, supplying energy directly to move electrons against their natural flow—pushing reactions "uphill" to make otherwise impossible chemistry occur.

The fundamental insight: **electrolysis is the reverse of a [[quick-context/galvanic-cells-batteries|battery]]**. In a [[quick-context/galvanic-cells-batteries|galvanic cell]], spontaneous chemical reactions push electrons through a circuit, generating electricity. In electrolysis, you push electricity through chemicals to force non-spontaneous reactions. Same components ([[learning/notes/quick-context/electrodes|electrodes]], electrolyte, electron flow), opposite energy direction.

This reversal principle connects to [[quick-context/chemical-bonds-spectrum|chemical bond energies]]: breaking bonds costs energy, forming bonds releases it. Water's O-H bonds are stable (~460 kJ/mol each)—nature doesn't want to break them. Electrolysis supplies that bond-breaking energy electrically, storing it in the separated H₂ and O₂ gases. Recombining them (in a fuel cell or combustion) releases that stored energy.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Electrolyte** | The ionic conductor that carries current between electrodes; can be molten salt or ionic solution—pure water is NOT an electrolyte (too few ions) |
| **Cathode/Anode** | Cathode = reduction (electrons flow in, cations migrate here); Anode = oxidation (electrons flow out, anions migrate here). Mnemonic: AN OX, RED CAT |
| **Overpotential** | Extra [[learning/notes/quick-context/voltage|voltage]] beyond thermodynamic minimum needed for practical reaction rates; includes activation, concentration, and ohmic components |
| **Faraday's Laws** | The quantitative link between electricity and chemistry—96,485 coulombs transfers to/from one mole of singly-charged ions |
| **Current Efficiency** | Fraction of electrons doing useful chemistry vs. side reactions; industrial processes obsess over this since small losses mean millions in wasted electricity |

<details>
<summary><strong>How It Works</strong></summary>

Electrolysis operates through a coordinated dance of electrons and ions across two electrodes immersed in a conducting solution. When you connect a power supply, it acts as an "electron pump"—pulling electrons away from one electrode (the anode) and pushing them onto the other (the cathode). This creates an electrical imbalance that drives chemical change. At the cathode, the excess electrons need somewhere to go, so they transfer to positive ions (cations) in the solution, reducing them. At the anode, the electron deficiency pulls electrons away from negative ions (anions) or neutral molecules, oxidizing them. The solution itself doesn't conduct electrons—instead, ions physically migrate through the liquid to carry the current between electrodes, completing the circuit.

The key to understanding electrolysis is recognizing that the power supply is doing two things simultaneously: providing electrons where reduction needs to happen, and removing electrons where oxidation needs to happen. The minimum voltage required corresponds to the thermodynamic "cost" of the overall reaction—for water splitting, that's 1.23V because that's the energy needed to break O-H bonds and form H-H and O=O bonds. Any voltage above this minimum goes into overcoming kinetic barriers (activation energy) and resistive losses, appearing as heat.

```
THE ELECTROLYSIS CIRCUIT: Electron and Ion Flow
═══════════════════════════════════════════════════════════════════════════

                         POWER SUPPLY
                    ┌─────────────────────┐
                    │    ⊖ ←───── ⊕       │
                    │    (-)     (+)      │  Electron pump: pulls e⁻ from
                    └─────┬───────┬───────┘  anode, pushes to cathode
                          │       │
         electrons IN     │       │     electrons OUT
              ↓           │       │           ↑
         ┌────────────────┴───────┴────────────────┐
         │                                         │
         │    CATHODE (-)         ANODE (+)        │
         │        ║                   ║            │
         │        ║                   ║            │
         │   ═════╬═══════════════════╬═════       │  Electrode surfaces
         │        │                   │            │
         │        ▼                   ▲            │
         │    Reduction           Oxidation        │
         │    (gain e⁻)           (lose e⁻)        │
         │        │                   │            │
         │        │   ELECTROLYTE     │            │
         │        │   SOLUTION        │            │
         │   ┌────┴───────────────────┴────┐       │
         │   │                             │       │
         │   │   Cations (+) ──────────►   │       │  Ions migrate to
         │   │   ◄────────── Anions (-)    │       │  opposite electrodes
         │   │                             │       │
         │   │   Ions carry current        │       │
         │   │   through the liquid        │       │
         │   └─────────────────────────────┘       │
         │                                         │
         └─────────────────────────────────────────┘

THE SEQUENCE OF EVENTS:
───────────────────────
1. Power supply creates voltage difference between electrodes
2. Electrons flow through external wire (metal conductor)
3. At cathode: electrons arrive → cations accept them → REDUCTION
4. At anode: electrons leave → anions donate them → OXIDATION
5. Inside solution: ions migrate to maintain charge balance
   • Cations (+) drift toward cathode (-)
   • Anions (-) drift toward anode (+)
6. Circuit complete: electrons through wire, ions through solution
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

Two separate questions govern every electrolysis process:

**Thermodynamics asks: "Is it possible?"** — The minimum voltage (cell potential) tells you whether you've supplied enough energy to make the reaction energetically feasible. Water electrolysis needs at least 1.23V. Below this, *nothing happens*, no matter how long you wait.

**Kinetics asks: "Is it fast enough?"** — Even above the minimum voltage, reactions might be painfully slow. Real systems need *overpotential*—extra voltage to overcome activation energy barriers, just like heating a reaction mixture speeds it up. This is where electrode materials matter enormously: platinum catalyzes hydrogen evolution with minimal overpotential; cheap steel needs much more.

This thermodynamic/kinetic split echoes throughout chemistry. A reaction can be thermodynamically favored but kinetically blocked (diamond → graphite is favorable but takes geological time), or thermodynamically unfavorable but kinetically fast if you supply the energy. Electrolysis operates in the second regime: thermodynamically unfavorable reactions made kinetically accessible through electrical driving force.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

```
THE CONCEPTUAL PICTURE
══════════════════════════════════════════════════════════════════════════════

What's actually happening at the molecular level:

                     Power Supply
                    ⊖ ─────────── ⊕
                    │             │
         electrons  │             │  electrons
         flow IN    ▼             ▲  flow OUT
                ┌───────┐     ┌───────┐
                │CATHODE│     │ ANODE │
                │  (-)  │     │  (+)  │
                └───┬───┘     └───┬───┘
                    │             │
        ════════════╪═════════════╪════════════  Electrode surface
                    │             │
                    ▼             ▲
               ┌─────────────────────────┐
               │                         │
               │  H₂O + electrolyte      │
               │  (e.g., H₂SO₄ or KOH)   │
               │                         │
               │  Ions carry current     │
               │  through the solution   │
               │                         │
               └─────────────────────────┘

AT THE CATHODE (reduction):                  AT THE ANODE (oxidation):
─────────────────────────────                ────────────────────────────
Electrons arrive and need                    Electrons are pulled away,
somewhere to go. H⁺ ions (or                 leaving behind species that
water itself) accept them:                   must lose electrons:

    2H⁺ + 2e⁻ → H₂↑                              2H₂O → O₂↑ + 4H⁺ + 4e⁻

H⁺ gets reduced (gains e⁻)                   O in water gets oxidized
from +1 to 0 oxidation state                 from -2 to 0 oxidation state

The hydrogen bubbles off                     The oxygen bubbles off
as gas (2:1 ratio vs O₂)                     as gas (1:2 ratio vs H₂)


WHY THE ELECTROLYTE MATTERS:
────────────────────────────
Pure water: conductivity ≈ 0.05 μS/cm (nearly insulating)
With 1M H₂SO₄: conductivity ≈ 100,000 μS/cm (2 million× better!)

The electrolyte doesn't get consumed—it provides mobile ions to
carry current, but the net reaction is still just: 2H₂O → 2H₂ + O₂
```

The electrode surface is where electrons actually transfer to/from chemical species—the material dramatically affects efficiency, cost, and longevity. The key tradeoff: **catalytic activity vs. cost vs. stability**.

```
ELECTRODE MATERIAL COMPARISON FOR WATER ELECTROLYSIS
══════════════════════════════════════════════════════════════════════════════

Material         │ Cost      │ Overpotential │ Best For           │ Notes
─────────────────┼───────────┼───────────────┼────────────────────┼──────────────────
PLATINUM (Pt)    │ $$$$$     │ Very low      │ Hydrogen evolution │ Best catalyst, but
                 │ ~$30k/kg  │ ~50 mV        │ (cathode)          │ too expensive for
                 │           │               │                    │ industrial scale
─────────────────┼───────────┼───────────────┼────────────────────┼──────────────────
IRIDIUM OXIDE    │ $$$$$     │ Very low      │ Oxygen evolution   │ Best OER catalyst
(IrO₂)           │ ~$50k/kg  │ ~250 mV       │ (anode) in acid    │ Extremely rare metal
─────────────────┼───────────┼───────────────┼────────────────────┼──────────────────
NICKEL (Ni)      │ $         │ Moderate      │ Both electrodes    │ Industrial workhorse
                 │ ~$15/kg   │ ~300-400 mV   │ in alkaline        │ for alkaline systems
─────────────────┼───────────┼───────────────┼────────────────────┼──────────────────
STAINLESS STEEL  │ $         │ High          │ Budget/hobby       │ Works but inefficient
                 │ ~$3/kg    │ ~500-800 mV   │ setups             │ ~30-50% more energy
─────────────────┼───────────┼───────────────┼────────────────────┼──────────────────
CARBON/GRAPHITE  │ $         │ Variable      │ Inert applications │ Won't corrode but
                 │ ~$5/kg    │               │ chlor-alkali       │ limited catalysis
─────────────────┼───────────┼───────────────┼────────────────────┼──────────────────
DSA (Dimensionally│ $$$      │ Low           │ Industrial chlorine│ Ti substrate + RuO₂
Stable Anode)    │           │ ~100-200 mV   │ production         │ or IrO₂ coating
══════════════════════════════════════════════════════════════════════════════

WHY MATERIAL MATTERS - THE OVERPOTENTIAL COST:
──────────────────────────────────────────────

Thermodynamic minimum for water splitting: 1.23 V

With platinum electrodes:     1.23 + 0.05 + 0.25 ≈ 1.5 V  (efficient)
With nickel electrodes:       1.23 + 0.35 + 0.40 ≈ 2.0 V  (practical)
With steel electrodes:        1.23 + 0.60 + 0.80 ≈ 2.6 V  (wasteful)
                               ↑      ↑      ↑
                          theory  cathode  anode
                                  overp.   overp.

Energy efficiency = 1.23V / actual voltage
  • Platinum: 1.23/1.5 = 82% efficient
  • Nickel:   1.23/2.0 = 62% efficient
  • Steel:    1.23/2.6 = 47% efficient

That 35% efficiency gap means 35% more electricity cost forever!


THREE MAIN ELECTROLYZER TECHNOLOGIES:
─────────────────────────────────────

1. ALKALINE ELECTROLYZERS (most common industrial)
   • Electrolyte: KOH or NaOH solution (25-30%)
   • Cathode: Nickel or nickel alloy (Raney nickel)
   • Anode: Nickel or nickel-iron oxide
   • Operating temp: 60-80°C
   • Efficiency: 60-70%
   • Cost: Lowest capital cost

2. PEM ELECTROLYZERS (Proton Exchange Membrane)
   • Electrolyte: Solid polymer membrane (Nafion)
   • Cathode: Platinum on carbon
   • Anode: Iridium oxide
   • Operating temp: 50-80°C
   • Efficiency: 70-80%
   • Cost: Higher (precious metals required)

3. SOLID OXIDE ELECTROLYZERS (high temperature)
   • Electrolyte: Ceramic (yttria-stabilized zirconia)
   • Cathode: Nickel-YSZ cermet
   • Anode: Lanthanum strontium manganite (LSM)
   • Operating temp: 700-850°C
   • Efficiency: 80-90% (uses waste heat)
   • Cost: High, but no precious metals
```

**The research frontier**: Finding cheap catalysts that rival platinum's performance. Nickel-molybdenum alloys, cobalt phosphides, and nanostructured materials are promising. The goal: precious-metal-free electrodes that still achieve <200 mV overpotential. This is THE bottleneck for affordable green hydrogen.

**Relation to [[quick-context/chemical-bonds-spectrum|bond energies]]**: Electrolysis breaks strong [[quick-context/covalent-bonds|covalent bonds]] (O-H in water, ~460 kJ/mol) that require significant energy input. The 1.23V minimum for water electrolysis directly reflects this bond energy: 1.23V × 96,485 C/mol × 2 mol e⁻ per mol H₂O = 237 kJ/mol, matching the Gibbs free energy of water splitting.

**Relation to oxidation states**: Track where electrons go by watching oxidation numbers change. In water (H₂O), hydrogen is +1 and oxygen is -2. After electrolysis, hydrogen in H₂ is 0 (reduced: gained electrons), oxygen in O₂ is 0 (oxidized: lost electrons). The total electron bookkeeping must balance.

**Relation to electrochemical series**: Metals and ions have different "eagerness" to accept electrons ([[quick-context/reduction-potential|reduction potential]]). Copper (E° = +0.34V) reduces more easily than zinc (E° = -0.76V), which reduces more easily than sodium (E° = -2.71V). This explains why electrolyzing a copper/zinc mixture plates copper first, and why sodium can only be extracted from molten salt, not solution (water reduces first).

**Relation to energy storage**: Electrolysis is half of the hydrogen energy cycle. Electricity → electrolysis → H₂ stored → fuel cell → electricity. Round-trip efficiency is ~40-50%, much worse than [[quick-context/galvanic-cells-batteries|batteries]] (~90%), but hydrogen stores energy for months without loss and can be transported. The physics of [[quick-context/chemical-bonds-spectrum|bond formation]] in the fuel cell (H₂ + O₂ → H₂O) releases exactly what electrolysis put in, minus losses.

**The one thing most outsiders get wrong about this is...** thinking the energy gets "stored in the bonds" of hydrogen. This is backwards. **Breaking** bonds costs energy; **forming** bonds releases it. The O-H bonds in water are *strong*—that's why water is stable. Electrolysis puts energy *into* the system by breaking those bonds, creating separated H₂ and O₂ at higher chemical potential. When H₂ and O₂ recombine (combustion or fuel cell), *new* O-H bonds form, releasing that stored potential energy. The energy isn't in the H-H bond of hydrogen; it's in the *system's configuration*—separated fuel and oxidizer that "want" to combine. This misconception extends to nutrition ("breaking down food releases energy")—actually, it's the *formation* of CO₂ and H₂O bonds (plus ATP) during metabolism that releases energy, not the breaking of food molecule bonds.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/chemical-bonds-spectrum]]** — The energy hierarchy: breaking covalent bonds in electrolysis costs 100-400+ kJ/mol, while intermolecular forces (what you overcome when melting/boiling) are 1-40 kJ/mol. Electrolysis operates at the high-energy end.

- **[[quick-context/galvanic-cells-batteries|Galvanic/Voltaic Cells (Batteries)]]** — Spontaneous redox reactions producing electricity. Same components as electrolysis cells, opposite energy flow. Understanding one illuminates the other.

- **Redox Chemistry** — The broader framework: any reaction where electrons transfer between species. Electrolysis forces non-spontaneous redox; batteries harvest spontaneous redox; corrosion is uncontrolled redox; metabolism is biological redox.

- **[[quick-context/reduction-potential|Electrode Potentials (E° values)]]** — The "voltage table" predicting which species reduce/oxidize preferentially. Higher E° = more easily reduced. The difference between two half-reactions gives the cell voltage.

- **Industrial Applications** — Hall-Héroult process (aluminum from Al₂O₃), chlor-alkali process (Cl₂, NaOH, H₂ from brine), electroplating, electrorefining of metals—all electrolysis at scale.

- **[[quick-context/biology-fundamentals]]** — Cellular respiration is the chemical inverse of electrolysis at the bond level: respiration releases energy when forming bonds (CO₂ + H₂O), while electrolysis inputs energy to break them.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A [[quick-context/galvanic-cells-batteries|battery]] and an electrolysis cell both have anodes, cathodes, and electrolytes. What's the fundamental difference between them?
<details>
<summary>Answer</summary>
**Energy flow direction.** In a [[quick-context/galvanic-cells-batteries|battery]], spontaneous chemical reactions drive electrons through an external circuit—chemical energy converts to electrical energy. In electrolysis, external electrical energy forces a non-spontaneous reaction to occur—electrical energy converts to chemical energy. They're thermodynamic opposites: batteries release stored chemical potential; electrolysis creates it. The same cell can often work both ways (rechargeable batteries do exactly this—discharge = galvanic, charge = electrolytic). See: The Core Problem
</details>

**Q2:** Why can't you produce sodium metal by electrolyzing a sodium chloride solution (brine), but you *can* produce it from molten sodium chloride?
<details>
<summary>Answer</summary>
**In solution, water reduces before sodium does.** At the cathode, both Na⁺ and H₂O can accept electrons. Water's reduction (2H₂O + 2e⁻ → H₂ + 2OH⁻) has a much more favorable potential (~-0.83V) than sodium's (Na⁺ + e⁻ → Na, E° = -2.71V). Water "wins" and hydrogen evolves instead of sodium depositing. In molten NaCl, there's no water—Na⁺ is the only option. This is why all alkali and alkaline earth metals are produced from molten salt electrolysis, never aqueous solutions. See: Connection to Other Concepts (electrochemical series)
</details>

**Q3:** Someone claims "hydrogen fuel stores energy in its chemical bonds." What's wrong with this statement, and what's the correct way to think about it?
<details>
<summary>Answer</summary>
**Energy is stored in the system's configuration, not "in bonds."** Breaking bonds always *costs* energy; forming bonds *releases* energy. When you electrolyze water, you put energy IN to break strong O-H bonds. The products (H₂ and O₂) are at higher chemical potential—they "want" to react. When they recombine in a fuel cell, new O-H bonds form, releasing that potential energy. The energy was stored by separating reactive species, not by putting energy "into" hydrogen's H-H bond. This is like storing energy by lifting a weight (gravitational potential) vs. claiming the energy is "in the weight." See: What Outsiders Get Wrong
</details>

**Q4:** Water electrolysis theoretically needs 1.23V, but real electrolyzers run at 1.8-2.0V. Where does the extra energy go, and how could you reduce this waste?
<details>
<summary>Answer</summary>
**The extra energy becomes heat due to overpotential.** Three contributors: (1) *activation overpotential*—energy barrier to initiate electrode reactions, reduced by using better catalysts (platinum instead of steel); (2) *concentration overpotential*—ions depleted near electrode surfaces, reduced by stirring or higher temperatures; (3) *ohmic losses*—resistance in electrolyte and electrodes, reduced by closer electrode spacing, higher concentration electrolyte, better conductors. Industrial research focuses heavily on cheap, effective catalysts—platinum works great but is too expensive for large-scale hydrogen production. See: The Key Tension (thermodynamics vs. kinetics)
</details>

**Q5:** Explain why "electrolysis is the reverse of a fuel cell" in terms of bond breaking and bond forming.
<details>
<summary>Answer</summary>
**Electrolysis breaks O-H bonds (costs energy); fuel cells form them (releases energy).** In electrolysis: 2H₂O → 2H₂ + O₂. You input electrical energy to break 4 O-H bonds (~460 kJ/mol each). The products H₂ and O₂ have their own bonds, but the system is now at higher potential. In a fuel cell: 2H₂ + O₂ → 2H₂O. You break H-H and O=O bonds, then form 4 new O-H bonds. Because the O-H bonds being formed are stronger than the H-H and O=O bonds being broken, energy is released as electricity. It's the same reaction running in opposite directions—electrolysis is endothermic (absorbs energy), fuel cells are exothermic (releases energy). See: Connection to Other Concepts (energy storage)
</details>

</details>
