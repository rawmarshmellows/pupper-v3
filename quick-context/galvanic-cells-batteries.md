---
topic: Galvanic Cells (Batteries)
created: 2026-01-23
---

> **Related:** [[quick-context/electrolysis]] | [[quick-context/chemical-bonds-spectrum]] | [[quick-context/electrodes]]

> **TL;DR:** Galvanic cells (batteries) harvest electricity from spontaneous chemical reactions by forcing electrons to flow through an external circuit; certain metals naturally want to give up electrons while others want to accept them, and batteries exploit this difference to power devices.

# Galvanic Cells (Batteries)

## The Core Problem: Harvesting Electricity from Spontaneous Chemistry

Some chemical reactions *want* to happen—they're thermodynamically favorable, releasing energy as they proceed. A galvanic cell (battery) captures this released energy as electrical [[quick-context/electric-current|current]] instead of letting it dissipate as heat. Without batteries, we'd have no portable electronics, no electric vehicles, no grid-scale energy storage, and no way to store renewable energy for when the sun isn't shining. The core insight: **certain metals "want" to give up electrons more than others**. Zinc atoms readily shed electrons; copper atoms readily accept them. Put zinc and copper in contact through an ionic solution, and electrons will spontaneously flow from zinc to copper. A battery intercepts this electron flow, forcing it through an external circuit where it can do useful work (power a motor, light an LED, charge your phone) before completing its journey.

This is the **thermodynamic opposite of [[quick-context/electrolysis|electrolysis]]**: batteries convert chemical potential energy into electrical energy (spontaneous, releases energy), while electrolysis converts electrical energy into chemical potential energy (non-spontaneous, requires energy input). Same components—electrodes, electrolyte, electron flow—but energy flows in opposite directions.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **[[quick-context/reduction-potential\|Electrode potential (E°)]]** | A measure of how strongly a material wants to gain or lose electrons, measured in volts relative to a standard hydrogen electrode. Zinc (E° = -0.76V) readily gives up electrons; copper (E° = +0.34V) readily accepts them. The *difference* between two electrodes determines cell voltage. |
| **Anode/Cathode** | In a galvanic cell, the **anode** is where [[quick-context/anions-and-oxidation\|oxidation]] occurs (electrons leave, metal dissolves)—it's the *negative* terminal. The **cathode** is where [[quick-context/cations-and-reduction\|reduction]] occurs (electrons arrive, ions deposit)—it's the *positive* terminal. **Warning**: This is reversed from electrolysis, where cathode is negative. The definitions follow electron flow direction, which reverses when you flip from spontaneous to forced reactions. |
| **[[quick-context/making-electrolytes\|Electrolyte]]** | The ionic medium (liquid, gel, or solid) that allows ions to move between [[quick-context/electrodes\|electrodes]], completing the internal circuit. Electrons flow through the external wire; ions flow through the electrolyte. Without both paths, no current flows. |
| **State of Charge (SoC)** | The percentage of remaining capacity in a battery (100% = full, 0% = empty). As the battery discharges, reactants are consumed and SoC drops. Most batteries shouldn't be fully discharged—lithium-ion degrades rapidly below ~20% SoC. |
| **Internal resistance** | The opposition to current flow within the battery itself. Higher internal resistance means more energy lost as heat, lower efficiency, and reduced power output. Internal resistance increases as batteries age and as temperature drops (why your phone dies faster in cold weather). |

<details>
<summary><strong>How It Works</strong></summary>

A galvanic cell operates by physically separating a spontaneous chemical reaction into two half-reactions at different locations, then forcing electrons to travel through an external circuit to complete the reaction. At the anode, a reactive metal (like zinc) spontaneously oxidizes—its atoms give up electrons and dissolve into the electrolyte as ions. Those electrons can't travel through the electrolyte (which only conducts ions), so they must flow through a wire to reach the cathode. At the cathode, a less reactive material (like copper) accepts those electrons, reducing ions from solution into solid metal. The electrolyte provides a path for ions to migrate between the two compartments, maintaining electrical neutrality—without this ionic pathway, charge would build up and stop the reaction almost immediately.

The voltage a cell produces comes directly from the difference in "electron hunger" between the two electrode materials, quantified by their standard electrode potentials. Zinc has a strong tendency to release electrons (E° = -0.76V), while copper has a moderate tendency to accept them (E° = +0.34V). The cell voltage equals the difference: 0.34 - (-0.76) = 1.10V. Higher voltage differences mean more energy per electron transferred. During discharge, chemical bonds in the anode material are broken (zinc metal becomes zinc ions), and new bonds form at the cathode (copper ions become copper metal). The energy difference between bonds broken and bonds formed is what powers your device.

```
GALVANIC CELL OPERATION - Step by Step
══════════════════════════════════════════════════════════════════════════════

STEP 1: OXIDATION AT ANODE
──────────────────────────
     ZINC ELECTRODE
         │
         │  Zn atom on surface
    ┌────┴────┐
    │   Zn    │ ──→  Zn²⁺  +  2e⁻
    │  atoms  │      (goes into    (stay in
    │         │       solution)     metal)
    └─────────┘

   Zinc WANTS to lose electrons.
   Electrons accumulate in the electrode.


STEP 2: ELECTRON FLOW THROUGH EXTERNAL CIRCUIT
──────────────────────────────────────────────

    ANODE (-)              CATHODE (+)
       │                       │
       │    ←── e⁻ ←── e⁻ ←──  │
       │    ═══════════════    │
       │         WIRE          │
       │    (electrons flow    │
       │     to do work)       │
       │                       │

   Electrons flow from where they're
   released (anode) to where they're
   wanted (cathode). Put a device in
   this path = POWER!


STEP 3: REDUCTION AT CATHODE
────────────────────────────
                           COPPER ELECTRODE
                               │
                               │
                          ┌────┴────┐
         Cu²⁺  +  2e⁻ ──→ │   Cu    │
         (from     (arriving  │  atoms  │
         solution)  via wire) │ (plated)│
                          └─────────┘

   Copper ions WANT those electrons.
   They plate out as solid copper metal.


STEP 4: ION MIGRATION COMPLETES THE CIRCUIT
───────────────────────────────────────────

    ┌─────────┐    SALT BRIDGE    ┌─────────┐
    │  ZnSO₄  │  ═══════════════  │  CuSO₄  │
    │         │  ←── SO₄²⁻ ────   │         │
    │ (Zn²⁺   │  ──── K⁺ ────→    │ (Cu²⁺   │
    │ building│                   │ depleting│
    │   up)   │                   │   down)  │
    └─────────┘                   └─────────┘

   Anions move toward anode (balances Zn²⁺)
   Cations move toward cathode (replaces Cu²⁺)
   Without ion flow → charge builds up →
   reaction STOPS!


THE COMPLETE ENERGY FLOW:
═════════════════════════════════════════════════════════════════════

  CHEMICAL            ELECTRICAL           USEFUL
   ENERGY    ──────→    ENERGY    ──────→   WORK

┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Zn-Zn bonds  │    │  Electrons   │    │ Light, heat, │
│ are WEAKER   │ →  │  flow at     │ →  │ motion,      │
│ than Cu-Cu   │    │  1.10 volts  │    │ computation  │
│ bonds formed │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘

   ΔG < 0              Voltage = -ΔG/nF        P = VI
   (favorable)         (thermodynamics)       (power)
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

Battery engineering is a four-way optimization problem with no perfect solution:

- **Energy density** (Wh/kg): How much total energy can be stored per unit mass? Critical for EVs and phones where weight matters.
- **Power density** (W/kg): How fast can that energy be delivered? Critical for power tools and vehicle acceleration.
- **Cycle life**: How many charge/discharge cycles before significant degradation? Critical for grid storage and EVs.
- **Cost** ($/kWh): Can you afford to build it at scale?

Lithium-ion dominates because it balances these reasonably well, but it's not best at any single metric. Lead-acid batteries have terrible energy density but excellent power density and low cost (car starters). Sodium-sulfur batteries have great energy density but require 300°C operating temperatures. Solid-state batteries promise better safety and density but aren't manufacturable at scale yet. Every battery chemistry is a compromise—practitioners argue endlessly about which tradeoffs matter for specific applications.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## The Zinc-Copper Daniell Cell

```
THE DANIELL CELL - A Classic Galvanic Battery
══════════════════════════════════════════════════════════════════════════════

                         EXTERNAL CIRCUIT
                    ←─────── e⁻ ─────────
                   │                      │
                   │      VOLTMETER       │
                   │        1.10V         │
                   │                      │
              ┌────┴────┐            ┌────┴────┐
              │  ANODE  │            │ CATHODE │
              │  ZINC   │            │ COPPER  │
              │   (-)   │            │   (+)   │
              └────┬────┘            └────┬────┘
                   │                      │
     ══════════════╪══════════════════════╪══════════════
                   │     SALT BRIDGE      │
                   │    (KNO₃ in gel)     │
                   │  ←── SO₄²⁻ ──────    │
                   │                      │
              ┌────┴────┐            ┌────┴────┐
              │  ZnSO₄  │            │  CuSO₄  │
              │solution │            │solution │
              │         │            │ (blue)  │
              └─────────┘            └─────────┘


WHAT'S HAPPENING:

AT THE ZINC ANODE (oxidation):
──────────────────────────────
Zn(s) → Zn²⁺(aq) + 2e⁻

• Zinc metal dissolves into solution
• Each zinc atom releases 2 electrons
• Electrons flow through external circuit to cathode
• The zinc electrode slowly shrinks over time
• E° = -0.76V (zinc "wants" to give up electrons)


AT THE COPPER CATHODE (reduction):
──────────────────────────────────
Cu²⁺(aq) + 2e⁻ → Cu(s)

• Electrons arrive from external circuit
• Copper ions in solution accept electrons
• Copper metal plates onto the electrode
• The copper electrode slowly grows
• E° = +0.34V (copper "wants" to accept electrons)


CELL VOLTAGE CALCULATION:
─────────────────────────
E°cell = E°cathode - E°anode
E°cell = (+0.34V) - (-0.76V)
E°cell = +1.10V

The positive value confirms this reaction is SPONTANEOUS—
electrons will flow without external power.


THE SALT BRIDGE - Why It's Essential:
─────────────────────────────────────
Without the salt bridge, the reaction stops almost immediately.

Why? As zinc dissolves:
  • ZnSO₄ solution becomes more positive (excess Zn²⁺)
  • CuSO₄ solution becomes more negative (Cu²⁺ depleted)
  • This charge buildup opposes further electron flow

The salt bridge allows ions to migrate:
  • SO₄²⁻ moves toward the zinc side (balances Zn²⁺)
  • K⁺ moves toward the copper side (balances depleted Cu²⁺)
  • Electrical neutrality maintained, current keeps flowing
```

**Practical battery comparison:**

| Chemistry | Voltage | Energy Density | Cycle Life | Use Case |
|-----------|---------|----------------|------------|----------|
| Zinc-Carbon | 1.5V | 30 Wh/kg | 1 (primary) | TV remotes |
| Alkaline | 1.5V | 80 Wh/kg | 1 (primary) | Flashlights |
| Lead-Acid | 2.1V/cell | 35 Wh/kg | 500-800 | Car starters |
| NiMH | 1.2V | 60-120 Wh/kg | 500-1000 | Hybrid cars |
| Li-ion | 3.6-3.7V | 150-260 Wh/kg | 500-2000 | Phones, EVs |
| LiFePO₄ | 3.2V | 90-120 Wh/kg | 2000-5000 | Solar storage |

**The one thing most outsiders get wrong about this is...** thinking batteries "store electricity." They don't—batteries store *chemical potential energy* and convert it to electricity on demand. When you "charge" a lithium-ion battery, you're not pumping electrons into a tank; you're using electrical energy to force lithium ions from the cathode material back into the anode material (intercalation), which is a non-spontaneous process. When you discharge, the lithium ions spontaneously migrate back, and that spontaneous chemical change releases electrical energy. The battery is always doing chemistry—it just reverses direction depending on whether you're charging (electrolysis mode) or discharging (galvanic mode).

This also explains why batteries degrade: you're physically moving atoms around thousands of times. Eventually, the electrode materials crack, lose contact, or undergo irreversible side reactions. A battery isn't wearing out from "holding too many electrons"—it's wearing out from repeated atomic-scale structural stress.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/electrolysis]]** — The thermodynamic opposite of galvanic cells. Charging a rechargeable battery is electrolysis; discharging is galvanic operation. Understanding both illuminates how energy flows in electrochemical systems.

- **[[quick-context/chemical-bonds-spectrum]]** — Battery reactions involve breaking and forming bonds. The energy released comes from forming more stable bonds in the products than existed in the reactants.

- **[[quick-context/reduction-potential|Electrochemical Series (Standard Reduction Potentials)]]** — The ranked list of E° values that predicts which metals will oxidize/reduce relative to others. Metals with more negative E° make better anodes; more positive E° make better cathodes.

- **Battery Management Systems (BMS)** — The electronics that monitor and protect battery packs: cell balancing, overcharge/overdischarge protection, temperature monitoring. Critical for lithium-ion safety.

- **Solid-State Batteries** — The "next generation" technology replacing liquid electrolytes with solid conductors. Promises higher energy density and safety, but manufacturing challenges remain unsolved at scale.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** In a galvanic cell, electrons flow from anode to cathode through the external circuit. Why don't they just flow directly through the electrolyte instead?
<details>
<summary>Answer</summary>
**Electrolytes conduct ions, not electrons.** The electrolyte is an ionic conductor—dissolved salts or acids that allow charged ions (like Zn²⁺, Cu²⁺, SO₄²⁻) to move through the solution. Free electrons cannot travel through ionic solutions; they must go through the metallic external circuit. This separation is what allows us to extract useful work—if electrons could shortcut through the electrolyte, the reaction would just produce heat instead of electrical current. See: The salt bridge explanation in Concrete Example
</details>

**Q2:** The Daniell cell produces 1.10V. If you wanted a 3.3V battery for a microcontroller, how would you achieve this using Daniell cells?
<details>
<summary>Answer</summary>
**Connect three Daniell cells in series.** When batteries are connected in series (positive terminal of one to negative terminal of the next), their voltages add: 1.10V + 1.10V + 1.10V = 3.30V. The capacity (Ah) stays the same as a single cell, but voltage stacks. This is how a 12V car battery works—six 2.1V lead-acid cells in series. See: Concrete Example (cell voltage calculation)
</details>

**Q3:** Why does the copper electrode grow larger while the zinc electrode shrinks during discharge of a Daniell cell?
<details>
<summary>Answer</summary>
**Mass is being transferred via ion flow.** At the anode, solid zinc atoms lose electrons and dissolve into solution as Zn²⁺ ions—the electrode loses mass. At the cathode, Cu²⁺ ions from solution gain electrons and deposit as solid copper metal—the electrode gains mass. The electrolyte acts as the mass-transfer medium. Over complete discharge, you'd theoretically transfer all the zinc mass to the copper side (though the cell would stop working long before that due to concentration changes). See: Concrete Example (anode/cathode reactions)
</details>

**Q4:** Your phone battery lasts much shorter in winter. Based on what you've learned, what's happening electrochemically?
<details>
<summary>Answer</summary>
**Cold increases internal resistance and slows ion mobility.** At low temperatures: (1) the electrolyte becomes more viscous, slowing lithium ion diffusion between electrodes; (2) charge transfer kinetics at electrode surfaces slow down (higher activation energy barrier); (3) internal resistance increases, meaning more energy is lost as heat inside the battery rather than delivered to your phone. The battery still has the same stored energy, but it can't deliver it as efficiently or quickly. This is why EVs have reduced range in cold weather. See: 5 Essential Terms (internal resistance)
</details>

**Q5:** A rechargeable battery can switch between "galvanic mode" (discharging) and "electrolytic mode" (charging). What physically reverses when you plug in the charger?
<details>
<summary>Answer</summary>
**The direction of the electrode reactions and ion flow reverses.** During discharge (galvanic): the anode oxidizes spontaneously, releasing electrons that flow to the cathode where reduction occurs. During charging (electrolytic): an external power supply forces electrons in the opposite direction, causing the discharged cathode material to oxidize and the discharged anode material to reduce—reversing the chemistry. In lithium-ion specifically, lithium ions shuttle from cathode → anode during charging, and anode → cathode during discharging. The charger must supply voltage *higher* than the cell's equilibrium voltage to overcome the thermodynamic preference and force the reverse reaction. See: What Outsiders Get Wrong
</details>

</details>
