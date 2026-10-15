---
term: MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor)
created: 2026-02-25
updated: 2026-06-08
---

> **Related:** [[learning/notes/micro-context/bjt-mosfet-igbt]]

# MOSFET[[learning/notes/quick-context/tensile-strength-materials|]]

> **See also:** [[quick-context/transistor]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] dominant [[quick-context/transistor|transistor]] [[learning/notes/quick-context/bjt-specifications|type]] in modern electronics. [[learning/notes/quick-context/anions-and-oxidation|A]] [[learning/notes/quick-context/transistor|voltage-controlled switch]] where a thin oxide [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|layer]] insulates the [[learning/notes/quick-context/transistor|gate]] from the [[quick-context/doped-silicon|doped silicon]] [[learning/notes/quick-context/transistor|channel]], [[learning/notes/quick-context/electrolysis|forming]] a [[learning/notes/quick-context/capacitor|capacitor]]—applying [[learning/notes/quick-context/voltage|voltage]] creates an [[learning/notes/quick-context/voltage-current-causality|electric field]] that turns the channel on [[learning/notes/micro-context/push-pull-vs-open-drain|or]] [[learning/notes/quick-context/bjt-specifications|off]] without the gate drawing [[learning/notes/quick-context/capacitance|current]]. NMOS [[learning/notes/micro-context/push-pull-vs-open-drain|and]] PMOS variants pair together in CMOS logic.

## How It Works

- Applying voltage to the gate creates an electric field through the oxide insulator, attracting [[learning/notes/quick-context/cations-and-reduction|charge]] carriers into the channel region.
- Above the [[learning/notes/micro-context/capacitive-voltage-sensing|threshold]] voltage ($V_{th}$), enough carriers accumulate to [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|form]] a conductive channel between [[learning/notes/quick-context/differential-pair|source]] and [[learning/notes/quick-context/differential-pair|drain]].
- Removing the gate voltage collapses the channel, turning the [[learning/notes/quick-context/silicon-die|transistor]] off — [[learning/notes/micro-context/capacitive-voltage-sensing|no]] gate current flows because the oxide is an insulator.
- In CMOS logic, NMOS and PMOS transistors are paired so that [[learning/notes/quick-context/ram-addressing-decoder|one]] is always off, minimizing static [[learning/notes/quick-context/d-flip-flop|power]] consumption.

```
NMOS cross-section:

          Gate
            │
     ┌──────┴──────┐
     │ Metal  Gate │
     ├─────────────┤  ← Oxide (SiO₂ or high-k)
  ┌──┴───┐     ┌───┴──┐
  │  N⁺  │  P  │  N⁺  │
  │Source │ ch. │Drain │
  └──────┴─────┴──────┘
     P-type substrate

 +V gate → field through oxide
 → channel conducts → current flows
```

## The Gate as a Capacitor (No DC Gate Current)

The gate plate, the thin oxide, and the [[learning/notes/quick-context/transistor|silicon]] channel form a **[[learning/notes/quick-context/parallel-vs-series-voltage|parallel]]-plate capacitor** ($C_{gate}$): [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] conductors separated by an insulating [[learning/notes/quick-context/capacitor|dielectric]][[learning/notes/quick-context/glass-transition-temperature|. This is the]] root reason a [[learning/notes/quick-context/transistor|MOSFET]] switches by *field*, [[learning/notes/micro-context/can-bus-termination|not]] by *current*.

```
   GATE     ──────────   ← plate 1 (metal / polysilicon)
   oxide    ░░░░░░░░░░   ← insulating dielectric (SiO₂, ~1–10 nm)
   CHANNEL  ──────────   ← plate 2 (in the doped silicon)

   gate │ oxide │ channel  =  capacitor C_gate
```

- **Turning on charges it.** Driving the gate to $V_{gs}$ moves a charge $[[learning/notes/quick-context/capacitor|Q]] = C_{gate}\,V_{gs}$ onto the plate — a brief *transient* current. Once the gate sits at a steady DC voltage, $dQ/dt = [[learning/notes/quick-context/meddpicc-qualification-framework|0]]$ and the current stops: **a capacitor blocks DC.** Holding the channel on (or off) costs ~[[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|zero]] gate current.
- **[[learning/notes/quick-context/comparator-specification|Only]] leakage crosses the oxide.** A real gate passes a tiny DC leakage — [[learning/notes/quick-context/transistor|quantum tunneling]] through ultra-thin oxide, reverse-biased junction / ESD-[[learning/notes/quick-context/diode|diode]] leakage at the pin, and PCB surface leakage — totaling picoamps (and roughly [[learning/notes/quick-context/camera-fundamentals|doubling]] every ~10 °[[learning/notes/micro-context/cathode|C]]).
- **Switching still costs charge.** "No current" is a *DC* statement: every on→off→on cycle re-charges $C_{gate}$, which is the source of CMOS dynamic power $P = C [[learning/notes/quick-context/capacitor|V]]^[[learning/notes/quick-context/meddpicc-qualification-framework|2]] f$.

This near-zero **DC** gate current is the root cause of a MOSFET-input part's picoamp [[micro-context/input-bias-current|input bias current]] — [[learning/notes/quick-context/bjt-specifications|e]].[[learning/notes/quick-context/cations-and-reduction|g]]. the [[learning/notes/quick-context/comparator-specification|LMC7211-N]]'s ~0.04 pA.

## What Holds the Charge in Place

Once charged, the gate charge stays put for **two [[learning/notes/quick-context/pupper-lab7-vision-tracking|reasons]] working together**:

- **No road [[learning/notes/micro-context/push-pull-vs-open-drain|out]].** The oxide is a dielectric [[learning/notes/quick-context/breaking-elongation-rate|with]] a huge band-gap (~9 eV for SiO₂) — no free carriers, no conduction states inside it. To leave the plate, a charge [[learning/notes/quick-context/ros2-architecture|must]] cross the oxide, but the oxide is an energy "wall" it [[learning/notes/quick-context/embedded-communication-protocols|can]]'t classically climb. The escape route is blocked.
- **Electrostatically pinned.** The charge on the gate pulls an equal-and-opposite charge onto the other plate (the channel) across the thin oxide. The [[learning/notes/quick-context/cations-and-reduction|opposite charges attract]] and [[learning/notes/quick-context/d-flip-flop|hold]] *each other* against the inner faces — the charge is bound by the field, not merely "stuck for lack of a door."

The tiny pA leakage is exactly the small failure of "no road out": a few [[learning/notes/quick-context/anions-and-oxidation|electrons]] *tunnel* through the wall (worse the thinner the oxide), plus a trickle sneaks around it [[learning/notes/quick-context/metal-interconnect-layers|via]] reverse-biased junctions and PCB surface paths.

> **Tie-in — flash / EEPROM:** a *floating* gate (no wire at all) [[learning/notes/quick-context/pupper-lab7-vision-tracking|holds]] its charge for years on this same principle. It uses a **thicker** oxide so even tunneling is negligible → the stored bit survives a decade. A logic MOSFET uses a thin oxide for [[learning/notes/quick-context/embedded-communication-protocols|speed]], so it leaks a little more.

## Turning It On and Off — the Gate Driver

On/off is set by **where $V_{gs}$ sits relative to $V_{th}$**, and the charge is pushed on / pulled off by the **gate driver** — the circuit driving the gate pin. Crucially that charge flows **in and out the gate wire (a conductor)**, *never* across the oxide.

- **Turn ON** ($V_{gs} > V_{th}$): the driver [[learning/notes/quick-context/python-to-machine-code-pipeline|pushes]] + charge onto the gate plate → field reaches into the silicon → pulls electrons up to the surface → they form the conductive **channel** → source↔drain conducts.
- **Hold ON:** [[learning/notes/quick-context/existing-account-management-playbook|keep]] $V_{gs}$ there. Cap stays charged, channel stays — **no DC gate current** (oxide blocks the cross-path).
- **Turn OFF** ($V_{gs} < V_{th}$, e.g. 0 V): the driver **pulls the charge back off** the gate plate, out the same wire → field collapses → channel vanishes → source↔drain opens.

You don't need an ever-*larger* voltage to [[learning/notes/quick-context/switches-to-registers-storing-data|switch]] off — you bring the gate *down* below threshold. The cap discharges through the **gate [[learning/notes/quick-context/from-vacuum-tubes-to-coding-on-screens|terminal]]**, not through the oxide.

```
   ON  : driver ──+charge──►[gate]   field ON  → channel forms → S↔D conducts
   HOLD: gate held at Vgs    charge stays   no DC current (oxide blocks cross-path)
   OFF : driver ◄──charge───[gate]   field OFF → channel gone  → S↔D open
            (charge enters/exits the GATE WIRE, never through the oxide)
```

**Two separate currents — don't mix them:**

- **Gate current:** only brief charge/discharge blips [[learning/notes/quick-context/bare-minimal-data-storage-circuit|when]] you *switch* (the source of CMOS dynamic power $P = C V^2 f$); DC ≈ 0.
- **Source↔drain current:** the actual load the switch controls — flows through the channel, fully separate from the gate.

Knob analogy: gate charge = how far you turn the knob; channel = the valve it opens. *Holding* the knob costs ~[[learning/notes/quick-context/tlv7211-as-lmc7211-replacement|nothing]]; only *moving* it costs a blip.

**Key insight:** The gate is [[learning/notes/micro-context/input-bias-current|one plate of a capacitor]]—it switches by electric field, not current flow—which is [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] MOSFETs are far more power-efficient than [[quick-context/bjt|BJTs]] and dominate digital circuits with billions per chip.
