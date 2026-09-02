---
topic: How Resistors, Capacitors, Diodes, and Comparators Are Made — On-Chip vs Discrete Fabrication
created: 2026-06-07
---

> **Related:** [[learning/notes/quick-context/bga-ball-grid-array]] | [[learning/notes/quick-context/bond-pad]] | [[learning/notes/quick-context/common-ic-packages]] | [[learning/notes/quick-context/flip-chip]]

# How Resistors, Capacitors, Diodes, and Comparators Are Made — On-Chip vs Discrete


> **TL;DR:** The same four everyday parts get manufactured two completely different ways. **On-chip (monolithic):** a [[learning/notes/quick-context/resistor|resistor]] is a doped strip, a [[learning/notes/quick-context/capacitor|capacitor]] is two metal/silicon layers with a thin insulator between them, a [[learning/notes/quick-context/diode|diode]] is a PN junction, and a [[learning/notes/quick-context/comparator|comparator]] is a whole integrated circuit of many transistors — all *patterned together* on one silicon wafer by the same [[learning/notes/quick-context/semiconductor-fabrication|photolithography process]] that makes transistors. **Discrete:** each is a tiny standalone object built by its own specialized process (screen-printed resistive paste, stacked ceramic layers, a single junction die) and then soldered onto a [[learning/notes/quick-context/pcb-printed-circuit-board|PCB]].

## The Core Problem: A "Part" Is Not One Thing

When the hardware tower says "put a 10 kΩ resistor here" or "use a comparator," it hides a fork in the road: that part can either be *grown into the silicon alongside the transistors* (cheap per unit once you're already making a chip, but only as good as the chip process allows) or *manufactured separately as a discrete object* and stuck on a board (more accurate, higher [[learning/notes/quick-context/power-watts-joules|power]], but it costs board space and a solder joint). If you don't know which world a part comes from, you can't reason about its accuracy, its size, why a comparator is *never* a discrete two-lead part, or why the resistor inside a chip is sloppy while the one on your board can hit ±1%.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Monolithic / on-chip** | Made *inside* a single piece of silicon, in the same fab run as the transistors — patterned by litho, etch, ion implant, and deposition. "One stone." |
| **Discrete** | A standalone component manufactured by itself in its own process, then soldered onto a board as a separate physical object (e.g. an [[learning/notes/micro-context/smd-resistor|SMD chip resistor]]). |
| **Sheet resistance ($R_s$)** | The resistance of one square of a thin doped or printed film, in ohms-per-square (Ω/□). Total resistance = $R_s \times (L/W)$ — value comes from *geometry*, not a separate "amount of resistor." |
| **Thick-film** | A resistive (or conductive) paste *screen-printed* onto a ceramic body and fired in a furnace — the standard way discrete chip resistors and many hybrids are built. |
| **Co-firing** | Stacking many printed ceramic + metal layers and baking them into one solid block in a single high-temperature step — how a multilayer ceramic capacitor (MLCC) is made. |

<details>
<summary><strong>How It Works</strong> — Two manufacturing worlds, part by part</summary>

There are two roads to every one of these four parts. Pick the road first, then the part.

```
TWO ROADS TO THE SAME FOUR PARTS
==============================================================================

                          ┌──────────────────────┐
                          │  "I need a resistor / │
                          │   cap / diode / comp" │
                          └───────────┬───────────┘
                                      │
                ┌─────────────────────┴─────────────────────┐
                ▼                                            ▼
    ┌───────────────────────┐                  ┌───────────────────────────┐
    │   ON-CHIP (MONOLITHIC) │                  │   DISCRETE                 │
    │   Built INTO the die,  │                  │   Built SEPARATELY, then   │
    │   same fab run as the  │                  │   soldered onto the PCB    │
    │   transistors.         │                  │                            │
    │   Litho · etch ·       │                  │   Each part its OWN        │
    │   implant · deposit.   │                  │   specialized process.     │
    └───────────────────────┘                  └───────────────────────────┘
                │                                            │
                ▼                                            ▼
       same silicon wafer,                          a tiny standalone object
       patterned all at once                        with metal end-caps / leads
```

### ON-CHIP — all four are patterned together on one wafer

Everything below is created by the *same* cycle described in [[learning/notes/quick-context/semiconductor-fabrication|semiconductor fabrication]]: deposit a layer, spin photoresist, expose a mask, etch or implant, repeat. The mask shapes decide whether a given patch of silicon becomes a [[learning/notes/quick-context/transistor|transistor]], a resistor, a capacitor, or a diode. Nothing is "added on" — it is all carved out of the layer stack.

```
ON-CHIP COMPONENTS — same wafer, same litho, different mask shapes
==============================================================================

RESISTOR  (a doped strip)
──────────────────────────────────────────────────────────────────────────────
    A long, thin region of doped silicon (a "diffused" resistor) OR a strip
    of polysilicon laid on top of the oxide. Current must travel its LENGTH.

          contact                          contact
           │                                    │
        ┌──┴────────────────────────────────┴───┐
        │ ▓▓ doped strip (n- or p-type), width W │   R = Rs × (L / W)
        └────────────────────────────────────────┘
         │◄───────────── length L ──────────────►│

    Value is set by:  doping level (sets Rs, the Ω/□)  ×  drawn L/W geometry.
    More squares (longer & thinner) = more ohms. No separate "resistor part"
    exists — it's just a shaped patch of the SAME doped silicon transistors
    use.  → [[learning/notes/quick-context/doped-silicon|doped silicon]]


CAPACITOR  (two plates + a thin insulator)
──────────────────────────────────────────────────────────────────────────────
    Two flavors, both = "conductor / insulator / conductor" sandwich:

    MOS capacitor                    MIM (metal–insulator–metal)
    (gate over silicon)              (between upper metal layers)

      gate metal/poly                  metal plate (top)
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓               ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
    ░░░░ thin oxide ░░░             ░░ thin dielectric ░░
    ████ doped silicon ███          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                                     metal plate (bottom)

    C = ε·A / d  — area A is drawn by the mask, gap d is the deposited
    insulator thickness. MIM sits up in the [[learning/notes/quick-context/metal-interconnect-layers|metal layers]];
    MOS reuses the transistor's own gate-oxide sandwich.


DIODE  (a PN junction — the SAME physics as a transistor)
──────────────────────────────────────────────────────────────────────────────
    Implant a p-region next to an n-region. The junction between them IS the
    diode. This is the identical junction that makes transistors work — a
    transistor is literally back-to-back junctions.

        ┌───────────┬───────────┐
        │  P-type   │  N-type   │   anode ── P│N ── cathode
        └───────────┴───────────┘   conducts one way only (~0.7 V drop)
                    ▲
              PN junction   → [[learning/notes/quick-context/diode|diode]] / [[learning/notes/quick-context/transistor|transistor]]


COMPARATOR / OP-AMP  (NOT a single part — a whole IC)
──────────────────────────────────────────────────────────────────────────────
    A comparator is an INTEGRATED CIRCUIT: a dozen-plus transistors PLUS
    on-chip resistors and capacitors, all fabricated together on one die.

        ┌──────────────────────────────────────────────┐
        │  one silicon die                              │
        │   [diff pair Q1 Q2]──[mirror Q3 Q4]──[out Q6] │  ← transistors
        │   [poly resistor Rbias]   [MIM comp cap]      │  ← on-chip R & C
        └──────────────────────────────────────────────┘
                 packaged → looks like a small black chip

    So "is a comparator a part you make?" → No. It is a CHIP, fabricated
    exactly like any other chip. → [[learning/notes/quick-context/comparator|comparator]]
```

### DISCRETE — each part is its own little factory product

```
DISCRETE COMPONENTS — built separately, then soldered on
==============================================================================

SMD CHIP RESISTOR  (thick-film, laser-trimmed)
──────────────────────────────────────────────────────────────────────────────
    1. Screen-print resistive paste (often ruthenium-oxide based) onto a tiny
       ceramic (alumina) body.
    2. Fire it in a furnace so the paste fuses to the ceramic.
    3. LASER-TRIM a slot into the film to raise resistance to the exact value.
    4. Add metal end-caps for soldering; mark the value.

        ┌──────────────────────────────────┐
        │██  ▓▓▓▓▓▓▓ resistive film ▓▓▓▓  ██│  ▓ = printed film
        │██  ▓▓▓▓▓▓ ╗ laser cut ▓▓▓▓▓▓▓  ██│  ╗ = trim slot (tunes value)
        │██  ceramic body (alumina)      ██│  ██ = solderable end-cap
        └──────────────────────────────────┘
    Value set by: paste sheet resistance × printed geometry, THEN fine-tuned
    by trimming. → [[learning/notes/micro-context/smd-resistor|SMD resistor]]


MLCC CAPACITOR  (many co-fired ceramic + electrode layers)
──────────────────────────────────────────────────────────────────────────────
    A Multi-Layer Ceramic Capacitor stacks HUNDREDS of thin layers:
    ceramic dielectric / metal electrode / ceramic / electrode ... then
    CO-FIRES the whole stack into one solid block. Alternating electrodes
    connect to opposite end-caps → all layers are caps in PARALLEL (huge C
    in a grain-of-sand package).

        end-cap A                       end-cap B
        ║ ──────────── electrode ────────────  ║
        ║ ░░░░░░░░░░ ceramic ░░░░░░░░░░░░░░░░░  ║
        ║ ──────────── electrode ────────────  ║   ── = electrode → cap A
        ║ ░░░░░░░░░░ ceramic ░░░░░░░░░░░░░░░░░  ║   ── = electrode → cap B
        ║ ──────────── electrode ────────────  ║   ░░ = ceramic dielectric
        (interleaved; each ceramic gap = one tiny cap, all in parallel)
    → [[learning/notes/quick-context/capacitor|capacitor (see MLCC vs electrolytic)]]


DISCRETE DIODE  (one junction die in a 2-lead package)
──────────────────────────────────────────────────────────────────────────────
    A single PN-junction die (a small chip of the SAME junction silicon)
    bonded into a tiny package with exactly two terminals: anode & cathode.

             ┌──────────────────────┐
        ─────┤   [PN junction die]  ├─────   band marks the cathode end
        anode│  glass / epoxy body  │cathode
             └──────────────────────┘
    Same junction physics as the on-chip diode — just packaged alone instead
    of sharing a wafer. → [[learning/notes/quick-context/diode|diode]]
```

**Math notation:** On-chip resistance follows $R = R_s \cdot \dfrac{L}{W}$, where $R_s$ is sheet resistance in $\Omega/\square$. A parallel-plate capacitor (MOS, MIM, or one MLCC layer) follows $C = \dfrac{\varepsilon \cdot A}{d}$, with $\varepsilon$ the dielectric permittivity, $A$ the plate area, and $d$ the insulator thickness.

</details>

<details>
<summary><strong>The Key Tension</strong> — Why ever choose one road over the other?</summary>

The whole point of two roads is that they optimize different things. On-chip wins when you're *already making a chip* and need thousands of components essentially for free, tightly matched to each other. Discrete wins when you need **accuracy, high power, high [[learning/notes/quick-context/voltage|voltage]], or large values** that a chip process physically can't deliver.

```
WHY ON-CHIP PARTS ARE "SLOPPY" BUT DISCRETE PARTS CAN BE PRECISE
==============================================================================

   On-chip resistor:  ±20-30% absolute  ◄─── doping & geometry drift across
                                              the wafer; no trimming per part
   Discrete resistor: ±1% (±0.1% thin-film) ◄─ laser-trimmed to value, one
                                              by one

   BUT on-chip parts MATCH each other extremely well (made side by side in
   the same conditions). So chips use RATIOS (a 2:1 resistor pair, a divider)
   instead of relying on any single absolute value. Matching, not accuracy,
   is the on-chip superpower.
```

| Factor | On-chip (monolithic) | Discrete (on PCB) |
|--------|---------------------|-------------------|
| **Absolute accuracy** | Poor (±20–30%) | Excellent (±1% to ±0.1%) |
| **Matching to neighbor** | Excellent (ratios trustworthy) | Poor (separate parts) |
| **Cost per part** | ~free (rides the chip run) | A real BOM line + a solder joint |
| **Board space** | Zero (inside the die) | Takes a footprint |
| **Power / voltage handling** | Tiny | High (big body sheds heat / withstands kV) |
| **Max value** | Small (R, C) | Large (mF caps, MΩ resistors) |
| **Tuning** | Fixed at mask design | Laser-trimmed per part |

This is exactly why a comparator is an *on-chip* assembly of many transistors but you still put a *discrete* MLCC and a *discrete* pull-up resistor next to it on the board: the precise pull-up value and the bulk decoupling [[learning/notes/quick-context/capacitance|capacitance]] are things the chip process is bad at, so they live on the [[learning/notes/quick-context/pcb-printed-circuit-board|PCB]].

</details>

<details>
<summary><strong>Concrete Example</strong> — The same comparator circuit, both worlds at once</summary>

The [[learning/notes/quick-context/comparator|comparator battery-monitor]] circuit is the perfect illustration: parts from *both* roads sit in one tiny circuit, and you can point at which is which.

```
ONE BATTERY-MONITOR CIRCUIT — which parts are on-chip vs discrete?
==============================================================================

        VBAT
         │
       ┌─┴─┐ R1  ◄── DISCRETE 0402 thick-film resistor (laser-trimmed
       └─┬─┘         to ±1% — accuracy lives on the board)
         ├──────► V(+)
       ┌─┴─┐ R2  ◄── DISCRETE thick-film resistor (the divider ratio
       └─┬─┘         must be trustworthy → discrete, trimmed)
        GND
                         ╔════════════════════════════════════════╗
   Vref ─────────► (-)   ║  COMPARATOR IC  (one silicon die)       ║
                         ║   diff pair (transistors)               ║
   V(+) ───────────►(+)  ║   current mirror (transistors)          ║
                         ║   bias resistor  ◄ ON-CHIP poly strip   ║
                         ║   PN junctions   ◄ ON-CHIP diodes        ║
                         ║   open-drain output transistor          ║
                         ╚══════════════════╤═════════════════════╝
                                            │
        Vdd ──[ Rpull-up ]──────────────────┤ Vout
                   ▲                          (open-drain needs a
                   └── DISCRETE MLCC's        pull-up the chip can't
                       cousin: a discrete     provide accurately)
                       resistor on the PCB
        ─┤├─ decoupling cap across Vdd/GND ◄── DISCRETE MLCC
              (co-fired ceramic block, soldered next to the chip)
```

Walk it through:

1. **The comparator chip itself** is one die fabricated like any IC — its [[learning/notes/quick-context/differential-pair|differential pair]], [[learning/notes/micro-context/current-mirror|current mirror]], *its own internal bias resistor (an on-chip poly strip)*, and *its internal PN-junction diodes* were all patterned together in the same fab. You can't buy "the resistor inside the comparator" separately; it's etched into the die.
2. **R1 and R2** (the divider) are **discrete** thick-film [[learning/notes/micro-context/smd-resistor|SMD resistors]] precisely because the divider *ratio* sets the trip voltage and must be accurate — laser-trimmed discretes deliver the ±1% the chip process can't.
3. **The pull-up resistor** for the [[learning/notes/micro-context/push-pull-vs-open-drain|open-drain]] output is **discrete** — its exact value (RC speed vs. power) is a board-level choice.
4. **The [[learning/notes/micro-context/decoupling-capacitor|decoupling capacitor]]** is a **discrete MLCC** — a co-fired ceramic block providing bulk capacitance no on-chip cap could match in value.

Down the ladder, every "on-chip" part above traces to the raw [[learning/notes/quick-context/semiconductor-fabrication|fabrication]] cycle on a [[learning/notes/quick-context/silicon-die|silicon die]]; every "discrete" part traces to its own screen-print / co-fire / junction-dicing line and then a [[learning/notes/quick-context/pcb-printed-circuit-board|PCB]] solder joint, with the finished chips landing in their [[learning/notes/quick-context/substrate-ic-packaging|packages]] first.

**The one thing most outsiders get wrong about this is...** thinking a "comparator" or "[[learning/notes/quick-context/op-amp|op-amp]]" is a basic component like a resistor or capacitor — a single physical thing you fabricate in one shot. It isn't. A comparator is a *circuit* — a small integrated circuit of many transistors plus on-chip resistors and capacitors — manufactured exactly like a CPU, just smaller. There is no such thing as a single-element "comparator" the way there is a single doped strip "resistor." The naming makes them all sound like peers, but a resistor/capacitor/diode are *elements*, while a comparator is an *assembly of elements* on a chip.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — this note is rung F3 of the Fabrication Basement: the hardware rungs are built from parts, and this explains how those parts are themselves made.
- **[[learning/notes/quick-context/semiconductor-fabrication|Semiconductor Fabrication]]** — the litho/etch/implant/deposit cycle that patterns *all* the on-chip parts here, exactly as it patterns transistors. The "down" link.
- **[[learning/notes/quick-context/doped-silicon|Doped Silicon]]** — the raw material an on-chip resistor (diffused strip) and diode (PN junction) are carved from; doping level sets sheet resistance.
- **[[learning/notes/quick-context/silicon-die|Silicon Die]]** & **[[learning/notes/quick-context/metal-interconnect-layers|Metal Interconnect Layers]]** — where on-chip parts physically live: diffused resistors and MOS caps near the transistors, MIM caps up in the metal stack.
- **[[learning/notes/quick-context/transistor|Transistor]]** — the diode's PN junction is the same physics; a comparator is a circuit of these. The component all four parts share fabrication with.
- **[[learning/notes/quick-context/resistor|Resistor]]**, **[[learning/notes/quick-context/capacitor|Capacitor]]**, **[[learning/notes/quick-context/diode|Diode]]**, **[[learning/notes/quick-context/comparator|Comparator]]** — what each part *does* in a circuit; this note explains how each is *built*.
- **[[learning/notes/micro-context/smd-resistor|SMD Resistor]]** — the canonical discrete part: thick-film paste on ceramic, laser-trimmed.
- **[[learning/notes/quick-context/substrate-ic-packaging|Substrate / IC Packaging]]** & **[[learning/notes/quick-context/pcb-printed-circuit-board|PCB]]** — the "up" links: how a finished die gets packaged, and how discrete parts get soldered onto a board to form the hardware tower.

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** What is the single biggest structural difference between an "on-chip" resistor and a "discrete" [[learning/notes/micro-context/smd-resistor|SMD resistor]]?
<details>
<summary>Answer</summary>
The on-chip resistor is *part of the [[learning/notes/quick-context/silicon-die|silicon die]] itself* — a shaped patch of [[learning/notes/quick-context/doped-silicon|doped silicon]] (or polysilicon) patterned in the same fab run as the transistors, never a separate object. The discrete SMD resistor is a standalone product (resistive paste screen-printed and fired onto a tiny ceramic body, laser-trimmed, with solder end-caps) that is manufactured separately and then soldered onto the board. Same function, two entirely different manufacturing roads. See: How It Works.
</details>

**Q2:** On-chip, what physically sets a resistor's value, and what sets a capacitor's value?
<details>
<summary>Answer</summary>
The resistor's value is $R = R_s \cdot (L/W)$ — the *doping level* fixes the sheet resistance $R_s$ (ohms-per-square) and the *drawn geometry* (length over width, in number of squares) sets the rest. The capacitor's value is $C = \varepsilon A / d$ — the mask sets the plate *area* $A$ and the deposited insulator sets the gap $d$. Both come from geometry plus material, not from adding a discrete "amount of part." See: How It Works (on-chip diagrams).
</details>

**Q3:** Why is a comparator *never* a discrete two-lead part the way a diode can be?
<details>
<summary>Answer</summary>
Because a comparator is not a single circuit element — it is an *integrated circuit*: a dozen-plus transistors plus on-chip resistors and capacitors (a differential pair, a current mirror, a bias resistor, an output stage) all fabricated together on one die. A diode is one PN junction, which fits on a single tiny die with two terminals. You can package one junction with two leads; you cannot reduce a multi-transistor circuit to a single two-terminal element. A comparator is therefore made like any chip, not like a passive part. See: How It Works (comparator) and the misconception note.
</details>

**Q4:** A designer says: "I'll just use the resistors inside my chip for the [[learning/notes/quick-context/parallel-vs-series-voltage|voltage divider]] that sets my reference — saves two parts." What's wrong with relying on on-chip resistors for an *accurate absolute* value?
<details>
<summary>Answer</summary>
On-chip resistor absolute accuracy is poor (±20–30%) because doping and geometry drift across the wafer and there's no per-part trimming. So an on-chip divider's absolute output voltage is unreliable. *However*, on-chip parts *match each other* extremely well, so a divider that depends only on the *ratio* of two on-chip resistors can be trustworthy even though neither absolute value is. If the reference truly needs an accurate absolute trip point, you use discrete, laser-trimmed (±1%) resistors on the board instead. See: The Key Tension.
</details>

**Q5:** Trace a 10 kΩ pull-up resistor and the comparator it pulls up "down" to raw fabrication and "up" to the board. Where do the two roads diverge and where do they re-converge?
<details>
<summary>Answer</summary>
The **comparator** goes down the *on-chip* road: doped-silicon and metal layers patterned by the litho/etch/implant/deposit cycle of [[learning/notes/quick-context/semiconductor-fabrication|semiconductor fabrication]] into one [[learning/notes/quick-context/silicon-die|silicon die]] — its internal resistors/caps/diodes are etched in, inseparable. The **pull-up resistor** goes down the *discrete* road: resistive paste screen-printed and fired onto a ceramic body, laser-trimmed to 10 kΩ, given solder end-caps. The roads **diverge** at the very start (one process is a wafer fab, the other a thick-film print line). They **re-converge** on the [[learning/notes/quick-context/pcb-printed-circuit-board|PCB]]: the packaged comparator die (now in its [[learning/notes/quick-context/substrate-ic-packaging|package]]) and the discrete resistor are both soldered onto the same board, where they finally form one working circuit — a rung of the hardware tower. See: Concrete Example and Peripheral Knowledge.
</details>

</details>
