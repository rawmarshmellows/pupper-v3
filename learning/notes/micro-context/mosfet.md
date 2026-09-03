---
term: MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor)
created: 2026-02-25
updated: 2026-06-08
---
> **Related:** [[learning/notes/quick-context/transistor]] | [[learning/notes/micro-context/bjt-mosfet-igbt]] | [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]]


# MOSFET

> **See also:** [[learning/notes/quick-context/transistor]]

**Definition:** The dominant [[learning/notes/quick-context/transistor|transistor]] type in modern electronics. A [[learning/notes/quick-context/voltage|voltage]]-controlled switch where a thin oxide layer insulates the gate from the [[learning/notes/quick-context/doped-silicon|doped silicon]] channel, forming a [[learning/notes/quick-context/capacitor|capacitor]]—applying voltage creates an electric field that turns the channel on or off without the gate drawing current. NMOS and PMOS variants pair together in CMOS logic.

## How It Works

- Applying voltage to the gate creates an electric field through the oxide insulator, attracting charge carriers into the channel region.
- Above the threshold voltage ($V_{th}$), enough carriers accumulate to form a conductive channel between source and drain.
- Removing the gate voltage collapses the channel, turning the [[learning/notes/quick-context/transistor|transistor]] off — no gate current flows because the oxide is an insulator.
- In CMOS logic, NMOS and PMOS transistors are paired so that one is always off, minimizing static power consumption.

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

The gate plate, the thin oxide, and the silicon channel form a **parallel-plate capacitor** ($C_{gate}$): two conductors separated by an insulating dielectric. This is the root reason a MOSFET switches by *field*, not by *current*.

```
   GATE     ──────────   ← plate 1 (metal / polysilicon)
   oxide    ░░░░░░░░░░   ← insulating dielectric (SiO₂, ~1–10 nm)
   CHANNEL  ──────────   ← plate 2 (in the doped silicon)

   gate │ oxide │ channel  =  capacitor C_gate
```

- **Turning on charges it.** Driving the gate to $V_{gs}$ moves a charge $Q = C_{gate}\,V_{gs}$ onto the plate — a brief *transient* current. Once the gate sits at a steady DC voltage, $dQ/dt = 0$ and the current stops: **a capacitor blocks DC.** Holding the channel on (or off) costs ~zero gate current.
- **Only leakage crosses the oxide.** A real gate passes a tiny DC leakage — quantum tunneling through ultra-thin oxide, reverse-biased junction / ESD-[[learning/notes/quick-context/diode|diode]] leakage at the pin, and PCB surface leakage — totaling picoamps (and roughly doubling every ~10 °C).
- **Switching still costs charge.** "No current" is a *DC* statement: every on→off→on cycle re-charges $C_{gate}$, which is the source of CMOS dynamic power $P = C V^2 f$.

This near-zero **DC** gate current is the root cause of a MOSFET-input part's picoamp [[learning/notes/micro-context/input-bias-current|input bias current]] — e.g. the LMC7211-N's ~0.04 pA.

## What Holds the Charge in Place

Once charged, the gate charge stays put for **two reasons working together**:

- **No road out.** The oxide is a dielectric with a huge band-gap (~9 eV for SiO₂) — no free carriers, no conduction states inside it. To leave the plate, a charge must cross the oxide, but the oxide is an energy "wall" it can't classically climb. The escape route is blocked.
- **Electrostatically pinned.** The charge on the gate pulls an equal-and-opposite charge onto the other plate (the channel) across the thin oxide. The opposite charges attract and hold *each other* against the inner faces — the charge is bound by the field, not merely "stuck for lack of a door."

The tiny pA leakage is exactly the small failure of "no road out": a few electrons *tunnel* through the wall (worse the thinner the oxide), plus a trickle sneaks around it via reverse-biased junctions and PCB surface paths.

> **Tie-in — flash / EEPROM:** a *floating* gate (no wire at all) holds its charge for years on this same principle. It uses a **thicker** oxide so even tunneling is negligible → the stored bit survives a decade. A logic MOSFET uses a thin oxide for speed, so it leaks a little more.

## Turning It On and Off — the Gate Driver

On/off is set by **where $V_{gs}$ sits relative to $V_{th}$**, and the charge is pushed on / pulled off by the **gate driver** — the circuit driving the gate pin. Crucially that charge flows **in and out the gate wire (a conductor)**, *never* across the oxide.

- **Turn ON** ($V_{gs} > V_{th}$): the driver pushes + charge onto the gate plate → field reaches into the silicon → pulls electrons up to the surface → they form the conductive **channel** → source↔drain conducts.
- **Hold ON:** keep $V_{gs}$ there. Cap stays charged, channel stays — **no DC gate current** (oxide blocks the cross-path).
- **Turn OFF** ($V_{gs} < V_{th}$, e.g. 0 V): the driver **pulls the charge back off** the gate plate, out the same wire → field collapses → channel vanishes → source↔drain opens.

You don't need an ever-*larger* voltage to switch off — you bring the gate *down* below threshold. The cap discharges through the **gate terminal**, not through the oxide.

```
   ON  : driver ──+charge──►[gate]   field ON  → channel forms → S↔D conducts
   HOLD: gate held at Vgs    charge stays   no DC current (oxide blocks cross-path)
   OFF : driver ◄──charge───[gate]   field OFF → channel gone  → S↔D open
            (charge enters/exits the GATE WIRE, never through the oxide)
```

**Two separate currents — don't mix them:**

- **Gate current:** only brief charge/discharge blips when you *switch* (the source of CMOS dynamic power $P = C V^2 f$); DC ≈ 0.
- **Source↔drain current:** the actual load the switch controls — flows through the channel, fully separate from the gate.

Knob analogy: gate charge = how far you turn the knob; channel = the valve it opens. *Holding* the knob costs ~nothing; only *moving* it costs a blip.

**Key insight:** The gate is one plate of a capacitor—it switches by electric field, not current flow—which is why MOSFETs are far more power-efficient than [[learning/notes/quick-context/bjt|BJTs]] and dominate digital circuits with billions per chip.
