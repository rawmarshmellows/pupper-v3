---
term: Input Bias Current (I_B)
created: 2026-06-07
---

> **Related:** [[learning/notes/quick-context/comparator-specification]] | [[learning/notes/micro-context/mosfet]] | [[learning/notes/micro-context/input-offset-voltage]]

# Input Bias Current ($I_B$)

> **See also:** [[quick-context/comparator-specification]] | [[micro-context/mosfet]] | [[quick-context/resistor]]

**Definition:** The tiny current that flows into (or out of) a [[learning/notes/quick-context/comparator|comparator]]'s or op-amp's input pin to bias its input transistors. For CMOS-input parts it is essentially zero — picoamps.

> **What "bias the input transistors" means:** *Biasing* a [[learning/notes/quick-context/transistor|transistor]] = holding it at the standing DC operating point where it sits **turned-on, in its active (amplifying) region**, ready to respond. The input [[learning/notes/quick-context/differential-pair|differential pair]] must be biased "on" *before* it can sense `V(+) − V(−)`. $I_B$ is the current that upkeep costs — pulled from whatever drives the input pin.

## How It Works

- Each input pin connects to a transistor gate (CMOS) or base (bipolar) that must be held at its DC operating point to stay in the active region.
- Bipolar (BJT) inputs need a **continuous base current** to stay forward-active, so the part keeps drawing it from your source — real $I_B$ (nanoamps to microamps).
- CMOS ([[micro-context/mosfet|MOSFET]]-gate) inputs sit behind a thin oxide insulator that makes the gate **one plate of a [[learning/notes/quick-context/capacitor|capacitor]]**. Charging it to the bias [[learning/notes/quick-context/voltage|voltage]] takes only a brief transient; at steady DC a capacitor passes no current, so holding the input transistor on costs ~zero. Only tiny leakage — oxide tunneling, ESD-[[learning/notes/quick-context/diode|diode]] and PCB surface leakage — crosses, giving the LMC7211-N its ~0.04 pA (leakage roughly doubles every ~10 °C). *Mechanism: [[micro-context/mosfet#The Gate as a Capacitor (No DC Gate Current)|MOSFET → the gate as a capacitor]].*
- Bias current flowing through your source or [[quick-context/resistor|resistor]] divider creates an error voltage $I_B \times R$; near-zero $I_B$ means a high-impedance divider isn't loaded down.

```
   high-impedance
   source / divider
        |
   R ---+
        |   I_B ~ 0.04 pA   (CMOS gate, insulated)
        v
      --| gate            error voltage = I_B x R ~ 0
        | (input pin)
        |
   CMOS input draws almost nothing -> divider not loaded.
   (A bipolar input would draw nA-uA and shift the node.)
```

**Key insight:** Near-zero input current is exactly why a CMOS comparator can sense a high-impedance [[learning/notes/quick-context/resistor|resistor]] divider without disturbing it — a bipolar part would bleed enough current to shift the divider's voltage and corrupt the threshold.
