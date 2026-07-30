---
topic: Van der Waals Forces
created: 2026-01-20
updated: 2026-01-21
---

> **Related:** [[quick-context/polymer-chemical-bonds]] | [[quick-context/glass-transition-temperature|Glass Transition Temperature - A Beginner's Guide]] | [[quick-context/pi-pi-stacking-aromatic-interactions|Pi-Pi Stacking: Why Your 3D Prints Need Heat]] | [[quick-context/dipole-dipole-interactions|Dipole-Dipole Interactions: A Beginner's Guide]] | [[quick-context/electromagnetism|Electromagnetism]]

> **TL;DR:** Van der Waals forces are weak, universal attractions between all molecules caused by temporary electron fluctuations—individually trivial but collectively powerful enough to let geckos walk on walls.

# Van der Waals Forces

## The Core Problem: Why Stuff Sticks Together (Even When It Shouldn't)

Imagine you have two neutral atoms—no positive or negative charge, just sitting there. Logic says they shouldn't attract each other at all. Yet geckos climb walls, plastic wrap clings to bowls, and noble gases (which refuse to bond chemically) still become liquids when cold enough. **Van der Waals forces are the "background attraction" that explains why neutral molecules still feel each other's presence.** Without these forces, there would be no liquid helium, no sticky tape, and proteins couldn't fold into their proper shapes. These forces are the weakest of all intermolecular attractions, but they're *universal*—every atom and molecule experiences them, making them the glue that holds together things that shouldn't stick.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Dispersion forces (London forces)** | The specific type of van der Waals force caused by temporary, random electron movements creating instant dipoles—this is what we focus on here |
| **Dipole** | An uneven distribution of electrical charge, like a tiny battery with a + end and a - end |
| **Polarizability** | How easily an atom's electron cloud can be distorted—larger atoms with more electrons are more polarizable and have stronger van der Waals forces |
| **Instantaneous dipole** | A temporary, fleeting moment when electrons randomly cluster on one side of an atom, creating a brief + and - end |
| **Induced dipole** | When one atom's instantaneous dipole causes a neighboring atom's electrons to shift in response, creating a second dipole |

<details>
<summary><strong>How It Works</strong></summary>

ASCII Diagrams of Electron Cloud Attraction

### Step 1: The Neutral Starting Point

Atoms have a nucleus (positive) surrounded by electrons (negative). On average, the electrons are evenly spread, so the atom appears neutral from outside:

```
        ATOM A                         ATOM B

      - - - - -                      - - - - -
    -           -                  -           -
   -    (e-)     -                -    (e-)     -
  -   (e-) (+)    -              -   (e-) (+)    -
   -    (e-)     -                -    (e-)     -
    -           -                  -           -
      - - - - -                      - - - - -

    [electrons evenly               [electrons evenly
     distributed around              distributed around
     positive nucleus]               positive nucleus]

    NET CHARGE: 0                   NET CHARGE: 0

    No attraction or repulsion yet...
```

### Step 2: Random Fluctuation Creates an Instantaneous Dipole

Electrons are always moving. By pure chance, they momentarily cluster on one side:

```
        ATOM A (now has instantaneous dipole!)

                  - - - - -
                -   (e-)    -
               -  (e-)(e-)   -
              -     (+)       -        <-- electrons randomly
               -              -            bunched on LEFT side
                -            -
                  - - - - -

           (-)            (+)
           side           side

    This atom is now TEMPORARILY a tiny magnet!
    The left side is slightly negative (more electrons)
    The right side is slightly positive (fewer electrons)
```

### Step 3: The Induced Dipole in the Neighbor

Atom A's temporary negative side *repels* electrons in nearby Atom B, pushing them away. This *induces* a dipole in Atom B:

```
    ATOM A                              ATOM B
    (instantaneous dipole)              (induced dipole)

         (e-)
        (e-)(e-)                                    (e-)
          (+)              ------>           (+)  (e-)(e-)
                           REPELS                    (e-)
                          ELECTRONS

    (-)       (+)                       (+)       (-)
    side      side                      side      side


    Now opposite charges are FACING each other!

              (+) ............ (-)
               ^                 ^
               |                 |
           Atom A's          Atom B's
           + side            - side

           THESE ATTRACT EACH OTHER!
```

### Step 4: The Attraction (Finally!)

```
    ATOM A                              ATOM B

         (e-)                                      (e-)
        (e-)(e-)                              (e-)(e-)
          (+)           <------->              (+)
                        ATTRACTION

    (-)       (+)  <~~~PULL~~~>  (+)       (-)


    Timeline of what just happened:

    t=0    Both atoms neutral, no interaction
           [    A    ]  [    B    ]

    t=1    Random electron fluctuation in A
           [ (-)A(+) ]  [    B    ]

    t=2    A's field induces dipole in B
           [ (-)A(+) ]  [ (+)B(-) ]

    t=3    Opposite charges attract!
           [ (-)A(+) ]<--->[ (+)B(-) ]

    t=4    Electrons shift again, cycle repeats...
           (happens trillions of times per second)
```

### Why Is It Always Attraction? (The Electron Repulsion Paradox)

A natural question: if electrons randomly fluctuate, won't there be times when electrons on the gecko spatula and electrons on the glass wall end up facing each other and repel?

**The answer: The dipoles aren't random—they're correlated.**

```
    WHY REPULSION DOESN'T WIN:

    SCENARIO 1: What you might expect (WRONG - uncorrelated)
    ═══════════════════════════════════════════════════════

    If fluctuations were truly random and independent:

    Time 1:  [ (-)A(+) ]  [ (+)B(-) ]   ← Attract!
    Time 2:  [ (+)A(-) ]  [ (+)B(-) ]   ← Repel!  (both - sides facing)
    Time 3:  [ (-)A(+) ]  [ (-)B(+) ]   ← Repel!  (both + sides facing)
    Time 4:  [ (+)A(-) ]  [ (-)B(+) ]   ← Attract!

    If random: 50% attract, 50% repel = NO NET FORCE

    But that's NOT what happens...


    SCENARIO 2: What actually happens (CORRECT - correlated)
    ════════════════════════════════════════════════════════

    B's dipole is INDUCED BY A's dipole. It's not independent!

    A's field FORCES B's electrons to the far side:

         ATOM A                    ATOM B
           │                         │
           ▼                         ▼
        ┌─────┐      ELECTRIC     ┌─────┐
        │(e-) │      FIELD        │     │
        │(e-) │  ───────────►     │  (+)│(e-)
        │ (+) │  pushes B's       │     │(e-)
        │     │  electrons        │     │(e-)
        └─────┘  to FAR side      └─────┘
           │                         │
        (-)  (+)                  (+)  (-)
           └────── ATTRACT! ────────┘

    The electrons in B CAN'T be on the near side because
    A's electrons are actively repelling them away!


    TIMELINE OF CORRELATED FLUCTUATIONS:
    ════════════════════════════════════

    t=1: A's electrons happen to bunch LEFT
         → A's electric field pushes B's electrons RIGHT
         → Result: (-)A(+)  ←attracts→  (+)B(-)

    t=2: A's electrons happen to bunch RIGHT
         → A's electric field pushes B's electrons LEFT
         → Result: (+)A(-)  ←attracts→  (-)B(+)

    t=3: A's electrons happen to bunch UP
         → A's electric field pushes B's electrons DOWN
         → Result: Still attracts! (in vertical alignment)

    EVERY configuration leads to attraction because
    B's dipole is always a RESPONSE to A's dipole!


    THE MATH (simplified):
    ══════════════════════

    If uncorrelated:   ⟨dipole_A × dipole_B⟩ = 0  (random = averages out)

    If correlated:     ⟨dipole_A × dipole_B⟩ > 0  (always same-sign product)

    The correlation exists because electromagnetism travels
    at the speed of light—A's field reaches B and influences
    it BEFORE B fluctuates independently.
```

**The gecko spatula example:**
```
    GLASS SURFACE              GECKO SPATULA

    ┌────────────────┐        ┌────────────────┐
    │  e- e- e- e-   │        │                │
    │    ↑           │   ◄──  │   (electrons   │
    │  glass atoms   │  field │    pushed      │
    │  with electron │  from  │    away!)      │
    │  fluctuation   │ gecko  │          e- e- │
    └────────────────┘        └────────────────┘

    When electrons in the glass bunch toward the gecko,
    they PUSH the gecko's electrons away from the interface.

    Result: Glass's (-) side faces gecko's (+) side.
            ALWAYS ATTRACTION at the interface.
```

**What about when atoms get TOO close?**

At very short distances (< ~0.3 nm), you DO get repulsion—this is called **Pauli repulsion** or "steric repulsion." The electron clouds start to overlap and the Pauli exclusion principle kicks in. This creates the "hard wall" that prevents atoms from merging:

```
    FORCE vs DISTANCE:

    Repulsion │  *
              │   *
              │    *
              │     *
    ──────────│──────○───────────────────── 0
              │       *         equilibrium
              │        *
              │         *
    Attraction│          *  *  *  *  *  *
              │
              └───────────────────────────────►
                       Distance
               ↑       ↑
               │       └── Van der Waals attraction
               │           (dominates at medium range)
               │
               └── Pauli repulsion
                   (dominates when TOO close)

    ○ = Equilibrium: where these balance (the "touching" distance)
```

So to answer directly: **Yes, electron-electron repulsion exists, but it only wins when atoms are forced extremely close together.** At normal "contact" distances (gecko on glass), the correlated nature of van der Waals dipoles ensures net attraction always wins.

### Why Are These the WEAKEST Forces?

```
    STRENGTH COMPARISON OF INTERMOLECULAR FORCES:

    |================================================================|
    |                                                                |
    | IONIC BONDS          ████████████████████████████████  ~500 kJ/mol
    | (Na+ and Cl-)        "Permanent, full charges"
    |                                                                |
    | HYDROGEN BONDS       ████████████  ~20-40 kJ/mol
    | (water molecules)    "Permanent partial charges"
    |                                                                |
    | VAN DER WAALS        ██  ~0.5-5 kJ/mol
    | (everything)         "Temporary, induced charges"
    |                                                                |
    |================================================================|


    WHY SO WEAK?

    1. TEMPORARY - The dipoles last femtoseconds (0.000000000000001 sec)

       Ionic bond:     (+)----------(-)     PERMANENT LOCK

       Van der Waals:  (+)...(-)...(+)...(-)  FLICKERING ON/OFF


    2. PARTIAL CHARGES - Not full +1 or -1, just tiny imbalances

       Ionic:     Na(+1)     Cl(-1)      Full electron transferred

       vdW:       (+0.001)   (-0.001)    Just electrons shifted slightly


    3. DISTANCE DEPENDENT - Falls off VERY fast with distance

       Van der Waals strength ~ 1/r^6  (r = distance)

       Double the distance? Force drops to 1/64th!

       Distance:  |  1x  |  2x  |  3x  |  4x  |
       ----------------------------------------
       Strength:  | 100% | 1.6% | 0.1% | 0.02%|
```

### Real-World Example: Why Geckos Stick to Walls

```
    GECKO FOOT (microscopic view)

    Each toe has ~500,000 hair-like structures (setae)
    Each seta splits into ~1,000 tiny tips (spatulae)

    That's ~500 MILLION contact points per foot!


           GLASS WALL                    GECKO SPATULA

           ___________                   ___________
          |           |                 /
          |  atoms    |    <~~~~>      /  atoms
          |  o  o  o  |   vdW force   /   o  o  o
          |   o  o    |              /     o  o
          |  o  o  o  |             /    o  o  o
          |___________|            /_______________


    Single spatula force:    ~0.00001 N  (basically nothing)

    500 million spatulae:    ~0.00001 N × 500,000,000
                             = ~5 N per foot
                             = ~20 N total (4 feet)
                             = Can support ~2 kg

    Gecko weighs ~0.05 kg... they could hold 40x their weight!


    KEY INSIGHT: Weakness × Huge Numbers = Strong Effect
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The central tradeoff practitioners navigate is that van der Waals forces are **individually pathetically weak but collectively significant**. A single van der Waals interaction might be 100x weaker than a [[quick-context/hydrogen-bonds-beginners|hydrogen bond]]. But because *every* atom contributes, large molecules or surfaces can accumulate thousands of these tiny attractions. This is why geckos—with millions of tiny hair-like structures on their feet—can support their body weight on glass. The debate centers on: when do you need to account for these forces (drug design, nanotech, adhesives) vs. when can you safely ignore them (most everyday chemistry)? In computational chemistry, including van der Waals interactions accurately is expensive, so there's constant optimization between precision and computational cost.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

Consider cooking oil versus water. Both are liquids at room temperature, but cooking oil has a much higher boiling point. Why? Oil molecules are much larger than water molecules—they have more electrons and more surface area. This means more van der Waals interactions between oil molecules, requiring more heat energy to separate them into a gas.

```
WATER (H₂O)                    COOKING OIL (e.g., C57H104O6)
Small molecule                  Very large molecule
~3 atoms                        ~167 atoms

    O                           [long chain of carbons with
   / \                           hydrogen atoms attached]
  H   H
                                Much more surface area
Few electrons                   for van der Waals contact
= weak vdW                      = strong cumulative vdW

Boiling point: 100°C            Boiling point: ~300°C
```

The same principle explains why waxes (even longer carbon chains) are solid at room temperature, while short-chain hydrocarbons like methane are gases.

**The one thing most outsiders get wrong about this is...** thinking van der Waals forces only matter for exotic physics or chemistry problems. In reality, they're everywhere: they're why your cooking oil is liquid at room temperature (bigger molecules = more van der Waals = higher boiling point), why plastic wrap sticks, why proteins fold correctly, and why drug molecules bind to their targets. The "weakness" is misleading—what makes them special isn't individual strength but their *universality*. Every atom, every molecule, every surface experiences them. They're the background hum of molecular interaction that makes the material world behave the way it does.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

1. **[[quick-context/dipole-dipole-interactions]]** — [[quick-context/dipole-dipole-interactions|Dipole-dipole interactions]] are the "stronger cousin" of van der Waals forces, occurring between molecules with permanent dipoles rather than temporary ones.

2. **[[quick-context/hydrogen-bonds-beginners]]** — Hydrogen bonds are a special, much stronger type of dipole interaction; understanding van der Waals forces helps you appreciate why hydrogen bonds are exceptionally powerful by comparison.

3. **[[quick-context/pi-pi-stacking-aromatic-interactions]]** — [[quick-context/pi-pi-stacking-aromatic-interactions|Pi-pi stacking]] in aromatic rings relies heavily on van der Waals forces between the electron clouds of flat ring structures, explaining why molecules like DNA bases stack so neatly.

4. **[[quick-context/polymer-chemical-bonds]]** — In polymers, van der Waals forces between chains determine properties like flexibility and melting point—chains held only by van der Waals are easier to pull apart than those with stronger intermolecular bonds.

5. **[[quick-context/glass-transition-temperature]]** — The [[quick-context/glass-transition-temperature|glass transition temperature]] is influenced by how strongly polymer chains interact via van der Waals forces; weaker interactions mean chains can slide past each other at lower temperatures.

6. **[[quick-context/biology-fundamentals]]** — Van der Waals forces contribute to protein folding (hydrophobic core formation), membrane structure, and the precise molecular recognition between enzymes and substrates.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** If van der Waals forces are the weakest intermolecular force, why can geckos support their body weight on glass walls?
<details>
<summary>Answer</summary>
Because geckos have ~500 million tiny contact points (spatulae) per foot, each contributing a small van der Waals attraction. Individually weak forces become collectively strong when multiplied across huge numbers of contact points. See: "Real-World Example: Why Geckos Stick to Walls"
</details>

**Q2:** What is the difference between an "instantaneous dipole" and an "induced dipole"?
<details>
<summary>Answer</summary>
An instantaneous dipole forms spontaneously when electrons randomly cluster on one side of an atom. An induced dipole forms in a neighboring atom as a response—the first atom's charge distribution pushes or pulls the neighbor's electrons, creating a second dipole. See: "The 5 Words You Need to Know"
</details>

**Q3:** Why do van der Waals forces decrease so rapidly with distance (following a 1/r^6 relationship)?
<details>
<summary>Answer</summary>
Because the dipoles are temporary and partial (not full charges), and the interaction depends on both atoms simultaneously having aligned dipoles. The effect compounds: both the creation of the instantaneous dipole and the induction of the response weaken with distance, making the overall force fall off extremely fast. See: "Why Are These the WEAKEST Forces?"
</details>

**Q4:** A large molecule and a small molecule are both non-polar. Which will have stronger van der Waals forces, and why?
<details>
<summary>Answer</summary>
The larger molecule will have stronger van der Waals forces because it has more electrons and a larger, more polarizable electron cloud. Greater polarizability means it's easier to create instantaneous dipoles and respond to neighboring dipoles. See: "The 5 Words You Need to Know" (polarizability)
</details>

**Q5:** Why is it misleading to dismiss van der Waals forces as "too weak to matter"?
<details>
<summary>Answer</summary>
Because van der Waals forces are universal—every atom and molecule experiences them. While individually weak, they accumulate across large surfaces or many atoms, affecting everything from protein folding to why cooking oil has a higher boiling point than water. Additionally, gecko feet demonstrate that millions of weak interactions can sum to support significant weight. See: "The Key Tension" and "How It Works" (gecko example)
</details>

</details>
