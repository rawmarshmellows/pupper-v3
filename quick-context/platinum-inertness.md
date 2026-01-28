---
topic: Why Platinum is Chemically Inert
created: 2026-01-25
---

> **Related:** [[quick-context/electrodes]]

> **TL;DR:** Platinum stays unreactive in electrolysis because its nearly-full d-orbitals, high ionization energy, and very positive reduction potential (+1.18V) make it strongly prefer keeping its electrons rather than dissolving.

# Why Platinum is Chemically Inert

## The Core Problem: Why Does Platinum Just Sit There?

In [[quick-context/electrodes|electrolysis]], we need electrodes that conduct electricity without participating in the chemical reaction. Cheap metals like iron or copper dissolve at the anode because they readily give up electrons. But platinum? It just sits there, pristine, letting electrons flow through while refusing to react. Why?

<details>
<summary><strong>How It Works</strong></summary>

The Short Answer

Four factors combine to make platinum unreactive:

```
WHY PLATINUM DOESN'T REACT
══════════════════════════════════════════════════════════════════════════

1. NEARLY-FULL D-ORBITALS
   ─────────────────────────
   Platinum: [Xe] 4f¹⁴ 5d⁹ 6s¹

   The 5d subshell holds up to 10 electrons. Platinum has 9.

       Empty          Platinum (5d⁹)      Full
       d⁰             d⁹                  d¹⁰
       □□□□□          ■■■■■■■■■□          ■■■■■■■■■■
                           ↑
                      Almost full = very stable
                      No "drive" to gain or lose electrons

2. HIGH IONIZATION ENERGY
   ─────────────────────────
   Ionization energy = energy needed to remove an electron

       Metal          1st Ionization Energy
       ─────────────  ─────────────────────
       Sodium (Na)         496 kJ/mol    ← easy to remove
       Iron (Fe)           762 kJ/mol
       Copper (Cu)         745 kJ/mol
       Platinum (Pt)       870 kJ/mol    ← hard to remove

   Platinum's 78 protons pull tightly on its electrons.

3. VERY POSITIVE REDUCTION POTENTIAL
   ───────────────────────────────────
   Reduction potential (E°) = how much a metal "wants" to stay as metal

       More negative = wants to dissolve (give up e⁻)
       More positive = wants to stay solid (keep e⁻)

       Metal      E° (volts)    Behavior
       ─────────  ──────────    ────────────────────
       Iron       -0.44 V       Rusts easily
       Copper     +0.34 V       Tarnishes slowly
       Silver     +0.80 V       Stays shiny mostly
       Platinum   +1.18 V       Almost never reacts
       Gold       +1.50 V       Never reacts

   Platinum strongly "prefers" staying as Pt⁰ metal.

4. NO FAVORABLE OXIDE
   ────────────────────
   Iron + oxygen → Fe₂O₃ (rust) — thermodynamically favorable
   Platinum + oxygen → PtO₂ — NOT favorable under normal conditions

   There's no energetic "payoff" for platinum to oxidize.
```

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Iron Nail vs. Platinum Electrode

```
ELECTROLYSIS EXPERIMENT: What happens at the anode?
══════════════════════════════════════════════════════════════════════════

IRON NAIL AS ANODE                    PLATINUM AS ANODE
──────────────────                    ─────────────────

    (+) ANODE                             (+) ANODE
    ┌───────┐                             ┌───────┐
    │ Fe    │ ← Iron                      │ Pt    │ ← Platinum
    │       │                             │       │
    └───┬───┘                             └───┬───┘
        │                                     │
        ↓                                     ↓

    Fe → Fe²⁺ + 2e⁻                       Nothing happens to Pt!
    (iron dissolves)
                                          Instead:
    After 1 hour:                         OH⁻ → ½O₂ + H₂O + e⁻
    ┌───────┐                             (water gets oxidized)
    │       │ ← Pitted,
    │  ░░░  │   rusty,                    After 1 hour:
    └───────┘   smaller                   ┌───────┐
                                          │ Pt    │ ← Unchanged!
    E° = -0.44 V                          │       │   Still shiny.
    Iron WANTS to                         └───────┘
    give up electrons
                                          E° = +1.18 V
                                          Platinum REFUSES to
                                          give up electrons
```

**The one thing most outsiders get wrong about this is...** assuming that any metal electrode will eventually dissolve if enough current flows through it. Platinum's inertness isn't about durability or hardness—it's about thermodynamics. The reduction potential tells us platinum atoms are far more stable as solid metal than as dissolved ions, so they simply refuse to participate in oxidation reactions that would dissolve them.

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

Platinum's inertness comes at a cost: ~$30,000/kg. Industrial applications often use:
- **Graphite** (carbon) — cheaper, reasonably inert
- **Titanium with coatings** — good balance of cost and durability
- **Sacrificial electrodes** — accept that the electrode will dissolve

</details>

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Inert** | Chemically unreactive; doesn't participate in reactions |
| **Ionization energy** | Energy required to remove an electron from an atom |
| **Reduction potential (E°)** | Voltage indicating how much a species "wants" electrons; positive = wants to stay as metal |
| **Oxidation** | Losing electrons (what happens to reactive metals at anodes) |
| **Noble metal** | Metals like platinum, gold, silver that resist corrosion due to high E° |

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Iron has a reduction potential of -0.44 V and platinum has +1.18 V. Which metal is more likely to dissolve when used as an anode, and why?
<details>
<summary>Answer</summary>
**Iron** is more likely to dissolve. The negative reduction potential means iron "prefers" to give up electrons and become Fe²⁺ ions. Platinum's positive potential means it strongly prefers to keep its electrons and stay as solid metal.
</details>

**Q2:** If platinum is so inert, how can electricity flow through it during electrolysis?
<details>
<summary>Answer</summary>
Platinum conducts electricity by allowing electrons to flow *through* its metallic structure without the platinum atoms themselves reacting. The electrons enter one side, pass through the metal's "sea of electrons," and exit the other side. At the electrode surface, other species (like water or hydroxide ions) react instead of the platinum.
</details>

**Q3:** Why don't we just use gold electrodes instead of platinum, since gold has an even higher reduction potential (+1.50 V)?
<details>
<summary>Answer</summary>
Gold would work chemically, but it's even more expensive than platinum and is softer (less durable). Platinum offers a good balance of inertness, conductivity, mechanical strength, and cost. For most applications, platinum is "inert enough."
</details>

</details>
