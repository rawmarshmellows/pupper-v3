---
term: Input Bias Current (I_B)
created: 2026-06-07
---

> **Related:** [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/current-electrons-per-second]] | [[learning/notes/micro-context/current-inductor-capacitor-relationship]] | [[learning/notes/micro-context/current-mirror]] | [[learning/notes/micro-context/input-common-mode-range]]

# Input Bias Current ($I_B$)

> **[[learning/notes/quick-context/tensile-strength-materials|]]See also:** [[quick-context/comparator-specification]] | [[micro-context/mosfet]] | [[quick-context/resistor]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] tiny [[learning/notes/quick-context/capacitance|current]] that flows into ([[learning/notes/micro-context/push-pull-vs-open-drain|or]] [[learning/notes/micro-context/push-pull-vs-open-drain|out]] of) [[learning/notes/quick-context/anions-and-oxidation|a]] [[learning/notes/quick-context/comparator|comparator]]'s or op-amp's input pin to bias its input transistors. For CMOS-input parts it is essentially [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|zero]] — picoamps.

> **[[learning/notes/quick-context/bare-minimal-data-storage-circuit|What]] "bias the input transistors" means:** *Biasing* a [[learning/notes/quick-context/silicon-die|transistor]] = holding it at the standing [[learning/notes/micro-context/mosfet|DC]] operating [[learning/notes/quick-context/epson-rc-plus-programming|point]] where it sits **turned-on, in its active (amplifying) region**, ready to respond. The input [[learning/notes/quick-context/differential-pair|differential pair]] [[learning/notes/quick-context/ros2-architecture|must]] be biased "on" *before* it [[learning/notes/quick-context/embedded-communication-protocols|can]] sense `V(+) − V(−)`. $I_B$ is the current that upkeep costs — pulled from whatever drives the input pin.

## How It Works

- Each input pin connects to a [[learning/notes/quick-context/transistor|transistor]] [[learning/notes/quick-context/transistor|gate]] (CMOS) or base (bipolar) that must be held at its DC operating point to stay in the active region.
- Bipolar (BJT) inputs need a **continuous base current** to stay forward-active, so the part keeps drawing it from [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] [[learning/notes/quick-context/differential-pair|source]] — real $I_B$ (nanoamps to microamps).
- CMOS ([[micro-context/mosfet|MOSFET]]-gate) inputs sit behind a thin oxide insulator that makes the gate **[[learning/notes/quick-context/ram-addressing-decoder|one]] plate of a [[learning/notes/quick-context/capacitor|capacitor]]**. Charging it to the bias [[learning/notes/quick-context/voltage|voltage]] takes [[learning/notes/quick-context/comparator-specification|only]] a brief transient; at steady DC a capacitor passes [[learning/notes/micro-context/capacitive-voltage-sensing|no]] current, so holding the input transistor on costs ~zero. Only tiny leakage — oxide tunneling, ESD-[[learning/notes/quick-context/diode|diode]] [[learning/notes/micro-context/push-pull-vs-open-drain|and]] PCB surface leakage — crosses, giving the [[learning/notes/quick-context/comparator-specification|LMC7211-N]] its ~[[learning/notes/quick-context/meddpicc-qualification-framework|0]].04 pA (leakage roughly doubles every ~10 °[[learning/notes/micro-context/cathode|C]]). *[[learning/notes/quick-context/silymarin|Mechanism]]: [[micro-context/mosfet#The Gate as a Capacitor (No DC Gate Current)|MOSFET → the gate as a capacitor]].*
- Bias current flowing through your source or [[quick-context/resistor|resistor]] divider creates an error voltage $I_B \times [[learning/notes/quick-context/cations-and-reduction|R]]$; near-zero $I_B$ means a high-impedance divider isn't loaded down.

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

**Key insight:** Near-zero input current is exactly [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] a CMOS comparator can sense a high-impedance [[learning/notes/quick-context/fundamental-electronic-parts-index|resistor]] divider without disturbing it — a bipolar part would bleed enough current to shift the divider's voltage and corrupt the [[learning/notes/micro-context/capacitive-voltage-sensing|threshold]].
