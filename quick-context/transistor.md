---
topic: Transistor
created: 2026-01-25
---

> **Related:** [[quick-context/pcb-chip-transistor-hierarchy]] | [[quick-context/semiconductor-fabrication]] | [[quick-context/transistor-analog-to-digital]]

> **TL;DR:** A transistor is an electrically-controlled switch with no moving parts, made of specially-treated silicon, that can switch billions of times per second at nanometer scales—enabling all modern digital electronics by combining into logic gates that perform computation.

# Transistor

## The Core Problem: Controlling Electricity Without Moving Parts

Imagine you need to turn a light on and off, but the switch is a thousand miles away. Or you need to switch something millions of times per second. Or you need to control something with no physical movement because you are building circuits smaller than bacteria. Before transistors, we used mechanical relays (electromagnetic switches) and vacuum tubes (glass bulbs with heated metal filaments). Relays were slow and wore out; vacuum tubes were hot, fragile, power-hungry, and enormous. A computer made of vacuum tubes filled entire rooms and failed constantly.

The transistor solved all of this: an **electrically-controlled switch with no moving parts**, made entirely of specially-treated silicon. It can switch billions of times per second, runs cool, never wears out mechanically, and can be shrunk to just a few nanometers. Modern computer chips contain **billions of transistors** on a piece of silicon smaller than your fingernail. Without transistors, there are no smartphones, no laptops, no internet routers, no digital watches, no modern cars, no medical devices. Every piece of digital electronics exists because of transistors.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Silicon** | The most common semiconductor material; a purified form of sand (silicon dioxide). Neither a good conductor nor a good insulator, which makes it controllable. |
| **Doping** | Intentionally adding impurities to silicon to change its electrical properties. Adding phosphorus creates "n-type" silicon (extra electrons); adding boron creates "p-type" silicon (missing electrons, called "holes"). |
| **Gate** | The control terminal of a transistor. Applying voltage to the gate switches the transistor on or off, like a valve controlling water flow. |
| **Source/Drain** | The two terminals between which [[quick-context/electric-current|current]] flows when the transistor is "on." Think of them as the inlet and outlet of a pipe controlled by the gate. |
| **Channel** | The region between source and drain where current flows. The gate controls whether this channel conducts electricity or blocks it. |

<details>
<summary><strong>How It Works</strong></summary>

A transistor is fundamentally a **voltage-controlled switch**. Apply a small voltage to the gate, and the transistor "closes" (conducts electricity between source and drain). Remove the gate voltage, and the transistor "opens" (blocks current). This simple on/off behavior is the foundation of all digital computing: on = 1, off = 0.

The magic happens through semiconductor physics. Pure silicon is a poor conductor. But by adding tiny amounts of impurities (doping), we create two types of silicon: n-type (with extra free electrons that can carry current) and p-type (with "holes" where electrons are missing, which also carry current by moving in the opposite direction). A transistor arranges these differently-doped regions so that the gate can create or destroy a conductive path.

```
THE TRANSISTOR: A Voltage-Controlled Switch
================================================================================

WHAT YOU ALREADY UNDERSTAND: A Light Switch

    OFF (no current flows)              ON (current flows)

    ┌─────┐                             ┌─────┐
    │POWER│                             │POWER│
    └──┬──┘                             └──┬──┘
       │                                   │
       ╱  ← switch OPEN                    │  ← switch CLOSED
       │    (gap = no path)               ═╪═
       │                                   │
    ┌──┴──┐                             ┌──┴──┐
    │LIGHT│ (off)                       │LIGHT│ (on!)
    └─────┘                             └─────┘


WHAT A TRANSISTOR DOES: Same Thing, But Electrically Controlled

    OFF (gate voltage = 0)              ON (gate voltage = HIGH)

         GATE                                GATE
           │                                   │
           ▼                                   ▼
    ┌──────┴──────┐                     ┌──────┴──────┐
    │      │      │                     │      │      │
    │  ╱   │      │                     │  ║   │      │
    │      │      │                     │  ║   │      │
    │ SOURCE    DRAIN                   │ SOURCE    DRAIN
    │   (no current)                    │   (current flows!)
    └─────────────┘                     └─────────────┘

    The GATE controls whether current can flow between SOURCE and DRAIN.
    No physical movement needed. Works at nanometer scale.
```

The most common modern transistor type is the **MOSFET** (Metal-Oxide-Semiconductor Field-Effect Transistor). Here is how it works step by step:

```
INSIDE A MOSFET TRANSISTOR
================================================================================

STRUCTURE (cross-section view):

                         GATE ELECTRODE (metal)
                              │
                    ┌─────────┴─────────┐
                    │    OXIDE LAYER    │  ← thin insulator (SiO2)
                    │   (glass, ~1nm)   │     prevents current into gate
                    └─────────┬─────────┘
         ┌────────────────────┴────────────────────┐
         │                                         │
    ┌────┴────┐                               ┌────┴────┐
    │ SOURCE  │         CHANNEL REGION        │  DRAIN  │
    │ (n-type)│         (p-type silicon)      │ (n-type)│
    │  ████   │                               │  ████   │
    │  ████   │                               │  ████   │
    └────┬────┴───────────────────────────────┴────┬────┘
         │           P-TYPE SUBSTRATE              │
         │      (bulk silicon, p-doped)            │
         └─────────────────────────────────────────┘


HOW THE TRANSISTOR TURNS ON AND OFF:

Step 1: OFF STATE (Gate voltage = 0)
─────────────────────────────────────────────────────────────────────────────

                    GATE (0 volts)
                         │
                    ┌────┴────┐
                    │  OXIDE  │
                    └────┬────┘
    ┌────────────────────┴────────────────────┐
    │                                         │
    │ SOURCE      No channel exists!      DRAIN │
    │ (n-type)       ✗ ✗ ✗ ✗ ✗           (n-type)│
    │  ████     blocked by p-type         ████  │
    │  ████           silicon             ████  │
    └─────────────────────────────────────────────┘

    The p-type region between source and drain acts like an insulator.
    Current cannot flow. The transistor is OFF.


Step 2: ON STATE (Gate voltage = positive)
─────────────────────────────────────────────────────────────────────────────

                    GATE (+1 volt)
                         │
                         ⚡ ← positive voltage attracts electrons
                    ┌────┴────┐
                    │  OXIDE  │
                    └────┬────┘
    ┌────────────────────┴────────────────────┐
    │                                         │
    │ SOURCE    ●●●●● CHANNEL ●●●●●    DRAIN  │
    │ (n-type)  (electrons pulled up)  (n-type)│
    │  ████   → → → → → → → → → → →     ████  │
    │  ████       current flows!        ████  │
    └─────────────────────────────────────────────┘

    Positive gate voltage pulls electrons from the p-type silicon
    up to the surface, creating a thin conductive "channel."
    Current can now flow from source to drain. The transistor is ON.


THE KEY INSIGHT: The gate doesn't carry current itself. It just creates
an electric field that attracts/repels electrons in the silicon below.
This is why it's called a "Field-Effect" Transistor (FET).
```

```
HOW TRANSISTORS BECOME COMPUTERS: From Switch to Logic
================================================================================

A single transistor is just an on/off switch. But combine them cleverly,
and you can build logic gates, which can compute any calculation.

EXAMPLE: NAND GATE (the universal building block)
─────────────────────────────────────────────────────────────────────────────

    Two transistors in series:

    POWER (+V)
        │
        ├──────────┐
        │          │
    ┌───┴───┐      │
    │   T1  │←─ Input A    If BOTH A AND B are ON (1):
    └───┬───┘      │           both transistors conduct,
        │          │           output connects to GROUND → Output = 0
    ┌───┴───┐      │
    │   T2  │←─ Input B    If EITHER A OR B is OFF (0):
    └───┬───┘      │           path to ground is broken,
        │          │           output connects to POWER → Output = 1
      GROUND       │
                   │
              OUTPUT ←──┘

    TRUTH TABLE:
    ┌─────┬─────┬────────┐
    │  A  │  B  │ OUTPUT │
    ├─────┼─────┼────────┤
    │  0  │  0  │   1    │
    │  0  │  1  │   1    │
    │  1  │  0  │   1    │
    │  1  │  1  │   0    │  ← "NOT AND" = NAND
    └─────┴─────┴────────┘

From NAND gates alone, you can build:
  • NOT gates (invert a signal)
  • AND gates
  • OR gates
  • XOR gates
  • Memory cells (flip-flops)
  • Adders, multipliers, comparators
  • CPUs, GPUs, entire computers!

A modern CPU has 10-50 BILLION transistors arranged as billions of logic gates.
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

Size vs. Power vs. Speed vs. Heat

The transistor world is governed by a fundamental tradeoff: **smaller transistors are faster and use less power, but they leak more current and are harder to manufacture.**

```
THE SHRINKING TRANSISTOR: 50 Years of Progress
================================================================================

Year     │ Process Node │ Transistor Size    │ Transistors/Chip
─────────┼──────────────┼────────────────────┼─────────────────
1971     │ 10 μm        │ 10,000 nm          │ 2,300 (Intel 4004)
1989     │ 1 μm         │ 1,000 nm           │ 1.2 million
1999     │ 180 nm       │ 180 nm             │ 28 million
2007     │ 45 nm        │ 45 nm              │ 820 million
2015     │ 14 nm        │ 14 nm              │ 5 billion
2022     │ 3 nm         │ ~12 nm (actual)    │ 50+ billion
2024     │ 2 nm         │ ~10 nm (actual)    │ 100+ billion

Note: Modern "process nodes" (3nm, 2nm) are marketing names.
Actual transistor dimensions are larger than the node name suggests.
```

As transistors shrink, several problems emerge:

1. **[[quick-context/transistor-analog-to-digital|Leakage Current]]**: When transistors are "off," some current still leaks through. At nanometer scales, this leakage becomes significant, wasting power and generating heat even when idle.

2. **Heat Density**: More transistors in the same area = more heat to dissipate. A modern CPU generates more heat per square centimeter than a stovetop.

3. **Manufacturing Difficulty**: Features smaller than the wavelength of light require extreme ultraviolet (EUV) lithography machines costing $200+ million each.

4. **Quantum Effects**: At atomic scales, electrons can "tunnel" through barriers that should block them, causing unpredictable behavior.

This is why "Moore's Law" (transistor count doubling every ~2 years) is slowing down. The industry responds with innovations like 3D transistor structures (FinFET, Gate-All-Around), new materials (high-k dielectrics), and [[quick-context/pcb-chip-transistor-hierarchy|advanced packaging]] (putting multiple chips in one package instead of shrinking further).

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

A Transistor in Your Phone's Processor

Let us trace what happens when you tap an app icon on your phone:

```
FROM TAP TO TRANSISTOR: What Actually Happens
================================================================================

1. YOU TAP THE SCREEN
   ─────────────────────────────────────────────────────────────────────────
   Touch sensor detects capacitance change
   Sends signal to touch controller chip

   Your finger
       │
       ▼
   ┌──────────────────────┐
   │   TOUCH SCREEN       │
   │   (capacitive grid)  │
   └──────────────────────┘
              │
              ▼ Signal: "touched at coordinates (x, y)"

2. SIGNAL TRAVELS TO CPU (through the [[quick-context/pcb-chip-transistor-hierarchy|packaging hierarchy]])
   ─────────────────────────────────────────────────────────────────────────
   Touch controller → PCB trace → CPU package → CPU die

   Takes about 1-2 nanoseconds for signal to reach the transistors

3. INSIDE THE CPU: Billions of Transistors Respond
   ─────────────────────────────────────────────────────────────────────────

   The touch coordinates trigger a cascade of transistor switching:

   ┌─────────────────────────────────────────────────────────────────────┐
   │ CPU DIE (simplified view)                                           │
   │                                                                      │
   │   ┌────────────┐    ┌────────────┐    ┌────────────┐                │
   │   │ CACHE      │    │   CORE 1   │    │   CORE 2   │                │
   │   │ (memory)   │◄──►│ (billions  │◄──►│ (billions  │                │
   │   │ transistors│    │  of gates) │    │  of gates) │                │
   │   │ store 0s/1s│    │            │    │            │                │
   │   └────────────┘    └────────────┘    └────────────┘                │
   │                                                                      │
   │   Touch coordinate data (as binary: e.g., x=0110, y=1001)           │
   │   enters the cache as voltage patterns stored in SRAM cells         │
   │                                                                      │
   │   Each SRAM cell = 6 transistors holding one bit (0 or 1):          │
   │                                                                      │
   │   ┌─────────────────────────────────────────┐                        │
   │   │        SRAM CELL (stores 1 bit)         │                        │
   │   │                                          │                        │
   │   │    T1 ─┬─ T2         T3 ─┬─ T4          │                        │
   │   │        │                  │              │                        │
   │   │        ├────────────────────►           │                        │
   │   │        │                  │              │                        │
   │   │       T5                 T6              │                        │
   │   │   (access)           (access)           │                        │
   │   │                                          │                        │
   │   │   Transistors T1-T4 hold the bit value  │                        │
   │   │   T5-T6 control read/write access       │                        │
   │   └─────────────────────────────────────────┘                        │
   │                                                                      │
   └──────────────────────────────────────────────────────────────────────┘

4. THE LOGIC GATES COMPUTE
   ─────────────────────────────────────────────────────────────────────────

   The CPU executes instructions like "Is touch inside app icon boundary?"

   This becomes millions of transistor switching operations:

   Compare X coordinate:
   ┌─────────────────────────────────────────────────────────────────────┐
   │                                                                      │
   │  Touch X ──►┌────────┐                                              │
   │             │COMPARE │──► Result: 1 (yes, X is in range)            │
   │  Icon X  ──►│ LOGIC  │                                              │
   │             └────────┘                                              │
   │                                                                      │
   │  (This "compare" block is built from hundreds of transistors        │
   │   forming NAND, NOR, XOR gates wired together)                      │
   │                                                                      │
   └─────────────────────────────────────────────────────────────────────┘

   Each gate switches in ~100 picoseconds (0.0000000001 seconds)
   Millions of gates switch in parallel
   Total time for your tap to be processed: ~1 millisecond

5. RESULT: App Launches
   ─────────────────────────────────────────────────────────────────────────

   All of this happened in the time it took light to travel 300 km.
   Your phone ran through billions of transistor state changes.
   You just see: app opens.
```

```
SCALE COMPARISON: How Small is a Transistor?
================================================================================

Object                              │ Size
────────────────────────────────────┼─────────────────────────────
Human hair width                    │ 70,000 - 100,000 nm
Red blood cell                      │ 7,000 nm
Bacterium (E. coli)                 │ 2,000 nm
Virus (influenza)                   │ 100 nm
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┼─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
MODERN TRANSISTOR (3nm node)        │ ~12 nm (actual feature size)
DNA double helix width              │ 2 nm
Water molecule                      │ 0.3 nm
Silicon atom                        │ 0.2 nm

A transistor is:
• 6,000x smaller than a human hair
• 500x smaller than a bacterium
• Only about 50-60 silicon atoms across

You could fit 50 BILLION transistors in a space the size of your fingernail.
```

**The one thing most outsiders get wrong about this is...** thinking transistors are simple on/off switches like a light switch. In reality, a transistor is an exquisitely engineered quantum device that exploits the weird boundary between conductors and insulators. The "on" state is not 100% on, and the "off" state is not 100% off. Modern transistors operate with gate voltages under 1 volt, switching in picoseconds, while managing quantum effects like electron tunneling. The entire digital revolution rests on the ability to make these [[quick-context/transistor-analog-to-digital|imperfect analog devices behave as if they were perfect digital switches]], billions of them working in concert, every single one fabricated with atomic precision.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/pcb-chip-transistor-hierarchy|PCB-Chip-Transistor Hierarchy]]** - How transistors connect to the outside world. Transistors are the bottom of a scale pyramid that goes transistor to die to package to PCB; each level bridges a massive size gap.

- **[[quick-context/semiconductor-fabrication|Semiconductor Fabrication (Photolithography)]]** - How transistors are actually manufactured. Patterns of light are projected onto silicon wafers coated with light-sensitive chemicals, building up layer by layer like printing but at nanometer scale.

- **Boolean Logic and Digital Circuits** - How transistor switches combine to perform computation. AND, OR, NOT gates built from transistors form the basis of all digital processing.

- **[[quick-context/electric-current|Electric Current]]** - The flow of electrons that transistors control. Understanding current and voltage is essential for grasping what a transistor actually switches.

- **[[quick-context/parallel-vs-series-voltage|Why Billions of Transistors Don't Need Billions of Volts]]** — Explains why a chip with 50 billion transistors at 0.65V doesn't need 32.5 billion volts. All transistors are in parallel, sharing the same voltage while currents add up.

- **Moore's Law** - The observation that transistor density doubles roughly every two years. This exponential growth has driven 60 years of computing progress but is now slowing as we approach atomic limits.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What are the three terminals of a basic MOSFET transistor, and what does each do?
<details>
<summary>Answer</summary>
The three terminals are: (1) **Gate** - the control terminal where voltage is applied to turn the transistor on or off; (2) **Source** - where current enters/exits; (3) **Drain** - where current exits/enters. Current flows between source and drain when the gate voltage is high enough; the gate itself draws almost no current because it is insulated by an oxide layer. See: 5 Essential Terms
</details>

**Q2:** What is "doping" and why is it necessary for transistors to work?
<details>
<summary>Answer</summary>
Doping is the intentional addition of impurities to pure silicon. Adding phosphorus creates n-type silicon (extra electrons that can carry current); adding boron creates p-type silicon (electron "holes"). Pure silicon is a poor conductor. By arranging n-type and p-type regions strategically, transistors create a situation where the gate voltage can control whether a conductive channel exists. See: 5 Essential Terms, How It Works
</details>

**Q3:** Why can NAND gates be used to build any other type of logic gate or computing circuit?
<details>
<summary>Answer</summary>
NAND gates are "functionally complete" - any Boolean logic function can be expressed using only NAND operations. By combining NAND gates in specific patterns, you can create NOT (one input to NAND), AND (NAND followed by NOT), OR (NOT both inputs, then NAND), and all other gates. From these, you can build memory, arithmetic units, and entire CPUs. This is why NAND is called the "universal gate." See: How It Works (NAND Gate diagram)
</details>

**Q4:** A chip manufacturer claims their new "2nm" transistors are 2 nanometers in size. What is misleading about this claim?
<details>
<summary>Answer</summary>
Modern process node names (3nm, 2nm) are marketing terms that do not reflect actual transistor dimensions. A "2nm" process might have transistors with gate lengths of 10-12nm and other features even larger. The names are useful for comparing generations but should not be taken literally. Actual transistor features are always larger than the node name suggests. See: The Key Tension (the shrinking transistor table and note)
</details>

**Q5:** As transistors shrink toward atomic scales, what physical phenomenon threatens to break the simple on/off model, and how does this relate to the limits of Moore's Law?
<details>
<summary>Answer</summary>
**Quantum tunneling** allows electrons to pass through barriers that should block them when those barriers become thin enough (just a few atoms). This causes "leakage current" - transistors that should be "off" still conduct some current. At scales below ~5nm, quantum effects become significant enough that transistors behave unpredictably. This, combined with manufacturing difficulty and heat density, is why Moore's Law is slowing. The industry responds with 3D transistor structures and [[quick-context/pcb-chip-transistor-hierarchy|advanced packaging]] rather than pure shrinking. See: The Key Tension
</details>

</details>
