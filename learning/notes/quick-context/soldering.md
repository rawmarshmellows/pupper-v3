---
topic: Soldering
created: 2026-02-06
---

> **Related:** [[quick-context/resistor]] | [[micro-context/pick-and-place-file]] | [[micro-context/smd-resistor]] | [[quick-context/bga-ball-grid-array]] | [[quick-context/bjt-specifications]]

> **TL;DR:** Soldering creates permanent electrical and mechanical connections by melting a metal alloy (solder) between component leads and [[quick-context/pcb-printed-circuit-board|PCB]] pads—it's the fundamental assembly technique for all electronics, from hand-built prototypes to billions of machine-soldered connections on factory production lines.

# Soldering

## The Core Problem: Making Reliable Permanent Connections

You have a component ([[quick-context/resistor|resistor]], IC, connector) and a PCB with copper pads. You need to create a connection that is electrically conductive, mechanically strong, and reliable for years. Breadboards and wire-wrapping are temporary. Soldering is permanent: a low-melting-point metal alloy (solder) is melted to form a metallurgical bond between the component lead and the copper pad. The joint must wet properly (solder flows and adheres to clean metal surfaces) and solidify into a reliable, low-resistance connection. Bad solder joints are the #1 cause of electronic failures in the field.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Solder** | A metal alloy that melts at 180-220°C (far below copper's 1085°C). Traditional: 63% tin / 37% lead (melts at 183°C). Lead-free: SAC305 (Sn96.5/Ag3.0/Cu0.5, melts at 217°C). |
| **Flux** | A chemical agent (rosin or acid-based) that removes oxide layers from metal surfaces so solder can wet them. Without flux, solder beads up and won't stick. Flux is in the core of solder wire and in solder paste. |
| **Wetting** | When molten solder flows onto and adheres to a metal surface, forming a concave fillet. Good wetting = shiny, smooth, concave joint. Poor wetting = balled-up solder that barely touches the pad. |
| **Reflow** | Machine soldering process: solder paste (tiny solder balls + flux) is printed onto PCB pads, components are placed by pick-and-place machines, then the whole board goes through an oven that melts the paste. Used for SMD production. |
| **Cold Joint** | A defective solder joint where the solder didn't fully melt or the parts moved during cooling. Looks dull and grainy instead of shiny and smooth. Has high resistance or is intermittent. |

<details>
<summary><strong>How It Works</strong></summary>

```
GOOD vs BAD SOLDER JOINTS (cross-section)
══════════════════════════════════════════════════════════════════════════════

    GOOD JOINT                  COLD JOINT              DRY JOINT
    (concave fillet)            (dull, grainy)          (solder ball)

       Lead                       Lead                    Lead
        │                          │                       │
    ╱───┤───╲   shiny          ▓▓▓▓┤▓▓▓▓   dull       ┌──○──┐  balled up
    ║   │   ║   smooth         ▓▓▓▓│▓▓▓▓   grainy     │     │  not wetted
    ╚═══╧═══╝   concave        ▓▓▓▓╧▓▓▓▓   irregular  └──┴──┘  poor contact
    ─────────── fillet         ───────────              ───────────
      PCB pad                    PCB pad                PCB pad

    Key: good wetting creates a concave meniscus between lead and pad


HAND SOLDERING PROCESS
══════════════════════════════════════════════════════════════════════════════

    1. Clean the tip (wipe on brass sponge)
    2. Tin the tip (melt a small amount of solder on it)
    3. Touch tip to BOTH pad and lead simultaneously
    4. Wait 1-2 seconds (heat transfers to joint)
    5. Feed solder wire into the joint (NOT onto the iron tip)
    6. Remove solder wire
    7. Remove iron
    8. Don't move the joint for 2-3 seconds (let it solidify)

         Step 3-4                Step 5                Step 7-8
       ┌─────────┐           ┌─────────┐           ┌─────────┐
       │    ╲    │           │    ╲    │           │         │
       │     ╲   │           │     ╲   │ solder   │  ╱──┐   │
       │  ┌───╲──│──lead     │  ┌───╲──│──wire→   │ ║   │   │
       │  │    ╲ │           │  │  ╱═╲ │          │ ╚═══╧═══│
       │──┴──────│── pad     │──┴══════│── pad    │─────────│── done!
       └─────────┘           └─────────┘           └─────────┘
       Heat both             Feed solder           Clean, shiny
       pad AND lead          into joint             concave fillet


THROUGH-HOLE vs SURFACE MOUNT
══════════════════════════════════════════════════════════════════════════════

    THROUGH-HOLE                    SURFACE MOUNT (SMD)

    Component lead goes             Component sits on top
    THROUGH a hole in PCB          of pads on PCB surface

    ┌──component──┐                 ┌─component─┐
    │             │                 │           │
    ─┼─────────────┼─ top           ═╧═══════════╧═ top (pads)
     │  solder    │
    ─╧═════════════╧─ bottom        No holes needed!
       fillets                      Smaller, cheaper,
                                    machine-placeable
    Bigger, hand-friendly           Harder to hand-solder
    Good for prototyping            Used for production
```

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

## Leaded vs. Lead-Free Solder

```
LEADED (Sn63/Pb37)                LEAD-FREE (SAC305)
───────────────────                ────────────────────
Melts at 183°C                    Melts at 217°C (+34°C hotter)
Shiny, smooth joints              Duller finish (normal, not a defect)
Easy to work with                 Harder to hand-solder
Better wetting                    Requires more flux, hotter iron
Contains toxic lead               RoHS compliant (no lead)
Being phased out                  Required for commercial products

Both work fine. Lead-free requires ~30°C hotter iron temperature
and slightly more skill. Most hobby work still uses leaded solder
(legal for personal use). All commercial products sold in the EU
must use lead-free (RoHS directive, 2006).
```

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

## Reflow Soldering: How Factories Build 1000 PCBs/Hour

```
REFLOW SOLDERING PROCESS (SMD production)
══════════════════════════════════════════════════════════════════════════════

    Step 1: STENCIL PRINTING
    ───────────────────────────
    Stainless steel stencil with holes matching pad locations
    Solder paste squeegeed through holes onto bare PCB pads

    Stencil ─┬─────┬─────┬─────┬─ (holes aligned to pads)
             │paste│     │paste│
    PCB    ──╧═════╧═════╧═════╧── (pads receive paste)


    Step 2: PICK AND PLACE
    ───────────────────────────
    Machine places components onto pasted pads at 10,000+ parts/hour
    Components stick to tacky solder paste (not soldered yet!)


    Step 3: REFLOW OVEN
    ───────────────────────────
    PCB moves through temperature zones on a conveyor belt

    Temp (°C)
    260 ─────────────────────╱╲──── Peak (solder melts)
    217 ───────────────────╱──╲─── Above liquidus
    200 ──────────────╱───╱    ╲── Soak (flux activates)
    150 ─────────╱───╱          ╲─ Preheat
     25 ───╱────╱                ╲── Cooling
        └────────────────────────────► Time (4-6 minutes total)

    The temperature profile is critical:
    • Too fast heating → thermal shock cracks components
    • Too low peak → solder doesn't fully melt → cold joints
    • Too high peak → components damaged, PCB delamination
    • Too fast cooling → brittle joints, thermal stress


    Step 4: INSPECTION
    ───────────────────────────
    • AOI (Automated Optical Inspection): cameras check every joint
    • X-ray inspection for hidden joints (BGA balls under packages)
    • ICT (In-Circuit Test): electrical testing of every connection
```

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it (the fabrication basement).

- **[[quick-context/pcb-printed-circuit-board]]** — PCB pad design, soldermask openings, and copper finish (HASL, ENIG, OSP) all affect solder joint quality. The PCB and soldering process are designed together.

- **[[quick-context/pcb-layers]]** — The paste mask layer is specifically designed for stencil printing during reflow. Paste openings are 5-10% smaller than pads to control solder volume and prevent bridging.

- **[[quick-context/bga-ball-grid-array]]** — BGA packages are soldered using reflow only (no hand soldering possible). The solder balls ARE the connection. X-ray inspection is required because joints are hidden under the package.

- **[[quick-context/flip-chip]]** — Flip-chip solder bumps (C4) are a microscopic version of the same soldering principle, connecting the die directly to the substrate.

- **[[quick-context/common-ic-packages]]** — Package type determines soldering method. DIP = through-hole (easy hand solder). QFP = SMD (hand-solderable with care). QFN = SMD (hot air or reflow only). BGA = reflow only.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** What does flux do, and why is it necessary?
<details>
<summary>Answer</summary>
**Flux removes oxide layers from metal surfaces so solder can wet them.** All metals oxidize in air. Copper oxide and tin oxide prevent solder from bonding to the metal underneath. Flux is a mildly acidic or rosin-based chemical that dissolves these oxides when heated, exposing clean metal for the solder to bond to. Without flux, solder beads up and rolls off the pad.
</details>

**Q2:** What's the difference between a cold joint and a good joint, visually?
<details>
<summary>Answer</summary>
**A good joint is shiny, smooth, and has a concave fillet shape.** A cold joint is dull, grainy or rough-textured, and may have an irregular or convex shape. Cold joints occur when the solder didn't fully melt, the parts moved during cooling, or there was insufficient heat. Note: lead-free solder naturally has a slightly duller finish than leaded—this is normal, not a defect.
</details>

**Q3:** Why is the reflow oven temperature profile so critical?
<details>
<summary>Answer</summary>
**Each zone serves a specific purpose.** Preheat: gradually raises temperature to avoid thermal shock. Soak: activates flux and equalizes temperature across the board. Peak/reflow: solder melts and wets the pads (must exceed liquidus temperature). Cooling: controlled rate prevents brittle joints and thermal stress. Too fast, too hot, or too cold at any stage produces defective joints or damaged components.
</details>

**Q4:** Why is leaded solder easier to work with than lead-free?
<details>
<summary>Answer</summary>
**Lower melting point (183°C vs 217°C), better wetting, and a clear shiny/dull visual indicator of joint quality.** The lower temperature gives more working time and is less likely to damage components or PCBs. Leaded solder flows more easily and creates shinier joints. Lead-free requires higher temperatures, more flux, and the natural dull finish makes visual inspection of joint quality harder.
</details>

**Q5:** How are BGA packages inspected after soldering if you can't see the joints?
<details>
<summary>Answer</summary>
**X-ray inspection.** The solder balls are hidden under the package, invisible to optical inspection. X-rays pass through the PCB and package but are absorbed by the dense solder, creating an image of each ball. Voids (air bubbles), bridges (shorts between adjacent balls), and missing balls are visible. This is why BGA rework is expensive and why BGA designs need careful DFM (Design for Manufacturability).
</details>

</details>
