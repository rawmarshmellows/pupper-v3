---
topic: Differential Pair
created: 2026-04-01
---

# Differential Pair

> **Related:** [[quick-context/transistor]] | [[quick-context/high-gain-amplifier-stage]] | [[quick-context/inside-the-triangle|All Stages Together]] | [[quick-context/op-amp]] | [[quick-context/comparator]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]

> **TL;DR:** A differential pair is two matched [[quick-context/transistor|transistors]] sharing a single tail current source, forming the universal input stage of [[quick-context/op-amp|op-amps]], [[quick-context/comparator|comparators]], and ADCs---it converts a voltage difference between two inputs into a current difference, rejecting any signal common to both inputs.

## The Core Problem: Sensing a Tiny Voltage Difference in a Noisy World

A sensor outputs a 2 mV signal sitting on top of a 1.5V common-mode [[learning/notes/quick-context/voltage|voltage]], and both wires pick up 50 mV of 60 Hz noise from nearby power lines. You need to amplify the 2 mV signal and ignore the 1.55V of unwanted voltage. A single [[learning/notes/quick-context/transistor|transistor]] amplifier can't do this---it amplifies everything. A differential pair amplifies only the *difference* between its two inputs, naturally rejecting noise and DC offsets that appear on both wires equally. This is why every [[learning/notes/quick-context/op-amp|op-amp]], [[learning/notes/quick-context/comparator|comparator]], and instrumentation amplifier starts with a differential pair at its input.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Matched transistors (Q1, Q2)** | Two transistors fabricated identically (same geometry, same process, physically adjacent on the die) so they have the same threshold voltage, transconductance, and temperature behavior. Matching is what makes the circuit reject common-mode signals. |
| **[[learning/notes/micro-context/tail-current|Tail current]] source** | A fixed current source (e.g., 100 $\mu$A) connected to the shared source node. It sets the total current budget that Q1 and Q2 compete for. The tail is what converts a voltage difference into a current difference. |
| **Common-mode signal** | The average of the two inputs: $V_{CM} = (V_+ + V_-) / 2$. A differential pair rejects this---if both inputs rise by the same amount, both transistors try to conduct more, but the tail current can't increase, so nothing changes at the output. |
| **Differential signal** | The difference between the two inputs: $V_{DIFF} = V_+ - V_-$. This is what the pair amplifies. A 1 mV differential signal on top of a 1.5V common-mode voltage produces the same output as a 1 mV signal on top of 0V. |
| **[[learning/notes/micro-context/common-mode-rejection-ratio|Common-Mode Rejection Ratio]] (CMRR)** | How well the pair ignores common-mode signals vs. amplifying differential signals, in dB. A CMRR of 80 dB means common-mode signals are attenuated 10,000× relative to differential signals. Higher = better. |

<details>
<summary><strong>How It Works</strong> --- Two transistors, one current budget</summary>

### The Circuit

```
DIFFERENTIAL PAIR (NMOS version)
==============================================================================

                        Vdd
                         │
                    ┌────┴────┐
                    │  Load   │  (current mirror or resistors)
                    ├────┬────┤
                    │    │    │
                  drain  │  drain       (higher voltage — near Vdd)
                  60 μA  │  40 μA       example: V(+) slightly > V(-)
                    ↓    │    ↓
               ┌────┴─┐  └─┌──┴────┐
          ┌───►│  Q1  │    │  Q2   │◄─── V(-)
          │    │      │    │       │     (gate)
          │    └──┬───┘    └───┬───┘
          │     source      source      (lower voltage — near GND)
   V(+) ──┘       ↓            ↓        Q1 and Q2 are matched
   (gate)         └──────┬─────┘         (same geometry, same process)
                         ↓
                    shared source node
                         ↓
                    ┌────┴────┐
                    │  TAIL   │    Fixed current source (e.g., 100 μA)
                    │ CURRENT │    Total always = 100 μA
                    └────┬────┘
                         │
                        GND

    TERMINAL MAPPING:
    • GATE   (side)   = input voltage.  V(+) drives Q1, V(-) drives Q2.
                        Draws ~zero current (it's a capacitor plate).
    • DRAIN  (top)    = high-voltage side. Connects up to load.
    • SOURCE (bottom) = low-voltage side. Tied together at shared node.
    • Current path: Vdd → load → drain → source → tail → GND
    • Both transistors carry current in the SAME direction (↓).
      Only the split changes: higher Vgs = more of the 100 μA budget.
```

### Why Current Flows Drain → Source

Drain is connected up toward Vdd (higher voltage). Source is connected down toward GND (lower voltage). Conventional current flows from high to low potential, so: drain → source.

At the electron level it's actually reversed: electrons flow **source → drain** (attracted toward the positive drain). That's literally why the terminals are named that way:

- **Source** = source of electrons (they originate here)
- **Drain** = where electrons drain to (collected here)

Conventional current is defined opposite to electron flow.

### How the Voltage Difference Steers Current

Both transistors share the same source node. Each transistor's conductivity depends on its gate-to-source voltage ($V_{gs}$):

$$V_{gs1} = V(+) - V_{source\_node}$$
$$V_{gs2} = V(-) - V_{source\_node}$$

When V(+) > V(-), Q1 has a higher $V_{gs}$ than Q2, so Q1 tries to conduct harder. But the tail current source is a fixed budget---it forces $I_{Q1} + I_{Q2} = 100\ \mu A$ always. So Q1 "winning" more current automatically means Q2 gets less. The shared source node and fixed tail current are what turn a voltage difference into a current difference.

```
CURRENT STEERING
==============================================================================

    V(+) = V(-):           V(+) > V(-):           V(+) >> V(-):

      Q1     Q2              Q1     Q2               Q1      Q2
     50 μA  50 μA           60 μA  40 μA            ~100 μA  ~0 μA
       ↓      ↓               ↓      ↓                ↓
       └──┬───┘               └──┬───┘                └──┬───┘
          ↓                      ↓                       ↓
       100 μA                 100 μA                  100 μA
     (balanced)            (steered left)          (fully steered)

    Total is ALWAYS 100 μA. Only the split changes.
    A few mV of differential input is enough to fully steer the current
    in a high-gain comparator (because the gain stages amplify the
    small current difference into a large output swing).
```

### Why Negative Gate Voltage Turns It OFF (Not Backwards)

A negative gate voltage does NOT reverse current flow. It turns the transistor OFF---no current in either direction.

The channel region between source and drain is **p-type silicon**. The gate sits above, separated by the oxide insulator. The gate-oxide-channel forms a [[quick-context/capacitor|capacitor]], and opposite charges attract across the oxide:

```
GATE VOLTAGE vs CHANNEL STATE (NMOS)
==============================================================================

    POSITIVE gate voltage (+V):          NEGATIVE gate voltage (-V):

    Gate: + + + + + +                    Gate: - - - - - -
    ═══════════════════ oxide            ═══════════════════ oxide
    Surface: - - - - - -                 Surface: + + + + + +
    (electrons pulled up                 (holes pulled up to surface,
     to surface → inversion              electrons pushed away
     layer forms → n-type                → even MORE p-type
     channel connects                    → stronger barrier
     source to drain)                    between source and drain)

    Channel: EXISTS → ON                 Channel: GONE → OFF
```

- **+V on gate** → attracts electrons to surface → creates n-type channel → transistor ON
- **0V on gate** → no field → no channel → transistor OFF
- **-V on gate** → attracts holes to surface, repels electrons → reinforces p-type barrier → even MORE off

The gate controls **whether** current flows, not **which direction**. Direction is always set by the drain-source voltage (drain is higher, so current goes drain → source). A negative gate just slams the valve shut harder.

### Common-Mode Rejection: Why Noise Cancels

```
COMMON-MODE REJECTION
==============================================================================

    DIFFERENTIAL SIGNAL (amplified):
    ────────────────────────────────────────────────────────────────
    V(+) rises by 1 mV, V(-) stays the same

      Q1: Vgs increases → conducts MORE → draws more current
      Q2: Vgs unchanged → conducts SAME

      But tail forces total = 100 μA
      → Q1 current goes UP, Q2 goes DOWN
      → Current DIFFERENCE appears at drains → output changes
      → Signal is amplified ✓


    COMMON-MODE SIGNAL (rejected):
    ────────────────────────────────────────────────────────────────
    V(+) and V(-) BOTH rise by 50 mV (noise on both wires)

      Q1: Vgs tries to increase → tries to conduct more
      Q2: Vgs tries to increase → tries to conduct more

      But tail forces total = 100 μA — can't increase!
      → Shared source node voltage rises by ~50 mV to compensate
      → Vgs1 and Vgs2 stay the same as before
      → Current split unchanged → no change at output
      → Noise is rejected ✓

    The tail current source is the hero: it prevents the total
    current from changing, so signals that move both inputs equally
    have no effect on the current split.
```

Both BJTs and MOSFETs can be used as Q1/Q2:
- **BJT pairs:** higher transconductance ($g_m$), faster, lower [[learning/notes/micro-context/input-offset-voltage|input offset voltage]]
- **[[learning/notes/micro-context/mosfet|MOSFET]] pairs:** essentially zero input current, easier to integrate on-chip, dominate in IC design

</details>

<details>
<summary><strong>The Key Tension</strong> --- Matching vs. gain vs. speed</summary>

The differential pair's performance depends on three competing goals:

| Want | Problem |
|------|---------|
| **Better matching** (lower offset) | Requires larger transistors → slower, more [[learning/notes/quick-context/capacitance|capacitance]] |
| **Higher gain** ($g_m$) | Requires more tail current → more power, more heat |
| **Faster response** | Requires smaller transistors → worse matching, more offset |
| **Higher CMRR** | Requires a perfect tail current source (infinite output impedance), which doesn't exist |

```
MATCHING AND OFFSET
==============================================================================

    Even "matched" transistors have tiny differences due to
    manufacturing variation. These differences create an
    INPUT OFFSET VOLTAGE: the small Vdiff needed to make
    the output exactly zero.

    Typical offsets:
    ┌──────────────────────┬──────────────────────┐
    │ Technology           │ Input offset voltage  │
    ├──────────────────────┼──────────────────────┤
    │ Discrete BJTs        │ 1-5 mV               │
    │ IC BJT pair          │ 0.1-1 mV             │
    │ IC MOSFET pair       │ 1-10 mV              │
    │ Chopper-stabilized   │ 1-10 μV              │
    └──────────────────────┴──────────────────────┘

    For a comparator, offset just shifts the trip point slightly.
    For a precision op-amp, offset is a critical spec.
```

</details>

<details>
<summary><strong>Concrete Example</strong> --- Where differential pairs appear</summary>

The differential pair is the most reused analog circuit block in electronics. Every one of these starts with a differential pair at the input:

```
WHERE YOU'LL FIND DIFFERENTIAL PAIRS
==============================================================================

    ┌────────────────────────────────────────────────────────────────┐
    │ Circuit                   │ What the diff pair does            │
    ├───────────────────────────┼────────────────────────────────────┤
    │ Op-amp (LM358, AD8605)   │ Senses V(+) - V(-), feeds to      │
    │                           │ gain stages for linear output      │
    ├───────────────────────────┼────────────────────────────────────┤
    │ Comparator (LM393)       │ Same input, but no compensation    │
    │                           │ cap → output snaps to rail         │
    ├───────────────────────────┼────────────────────────────────────┤
    │ Instrumentation amp      │ Three op-amps, each starting       │
    │ (INA128)                 │ with a diff pair → ultra-high CMRR │
    ├───────────────────────────┼────────────────────────────────────┤
    │ Flash ADC                │ 2ⁿ-1 comparators, each with a     │
    │                           │ diff pair, all firing in parallel  │
    ├───────────────────────────┼────────────────────────────────────┤
    │ Voltage regulator        │ Error amp compares output to       │
    │ (LDO, buck IC)           │ reference via a diff pair          │
    ├───────────────────────────┼────────────────────────────────────┤
    │ USB/PCIe receiver        │ Diff pair detects tiny voltage     │
    │                           │ swings on differential data lines  │
    └───────────────────────────┴────────────────────────────────────┘
```

**The one thing most outsiders get wrong about this is...** thinking a differential pair is specific to op-amps. It's not---it's a universal building block that predates and underlies op-amps, comparators, voltage references, and high-speed data receivers. The op-amp is just the most famous *packaging* of the differential pair. Understanding the pair itself lets you understand all of these circuits, because they all start from the same two-transistor current-steering mechanism.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> --- Related topics to explore</summary>

- **[[quick-context/transistor]]** --- The differential pair is built from two [[quick-context/transistor|MOSFETs]] (or BJTs). Understanding how gate voltage controls drain current ($V_{gs}$ → $I_d$) is prerequisite to understanding why the pair steers current.

- **[[quick-context/op-amp]]** --- An [[quick-context/op-amp|op-amp]] is a differential pair followed by gain stages and an output buffer, wrapped in negative feedback. The differential pair IS the op-amp's input.

- **[[quick-context/comparator]]** --- A [[quick-context/comparator|comparator]] is a differential pair followed by gain stages and a digital output stage, with no compensation [[learning/notes/quick-context/capacitor|capacitor]]. Same input, different optimization.

- **[[quick-context/bjt]]** --- [[quick-context/bjt|BJT]] differential pairs were the original (1960s). They have higher $g_m$ per unit current and lower offset than MOSFETs, which is why precision analog ICs still use BJT input stages.

- **[[quick-context/doped-silicon]]** --- The p-type channel, n-type source/drain, and oxide insulator that make MOSFET switching possible. Explains why negative gate voltage repels electrons and prevents channel formation.

- **[[quick-context/resistor]]** --- [[quick-context/resistor|Resistor]] loads can be used instead of a [[learning/notes/micro-context/current-mirror|current mirror]] at the drain, trading gain for simplicity. The tail current source is often implemented with a resistor + voltage reference in simple designs.

</details>

<details>
<summary><strong>Test Your Understanding</strong> --- 5 progressive questions</summary>

**Q1:** In a differential pair with a 100 $\mu$A tail current, what happens to Q1 and Q2 currents when V(+) = V(-)?
<details>
<summary>Answer</summary>
**Both carry exactly 50 $\mu$A.** With identical gate voltages and matched transistors, both have the same $V_{gs}$, so they conduct equally. The tail current splits 50/50. This is the balanced condition. See: How It Works (Current Steering).
</details>

**Q2:** Both inputs rise from 1.0V to 1.5V simultaneously (common-mode step). What happens to the output?
<details>
<summary>Answer</summary>
**Nothing.** Both transistors try to conduct more, but the tail current source can't supply more than 100 $\mu$A. Instead, the shared source node voltage rises by ~0.5V, keeping $V_{gs1}$ and $V_{gs2}$ the same as before. The current split doesn't change, so the output doesn't change. This is common-mode rejection. See: How It Works (Common-Mode Rejection).
</details>

**Q3:** What happens if you apply a negative voltage to the gate of Q1 in the differential pair?
<details>
<summary>Answer</summary>
**Q1 turns completely OFF** (no current, not reversed current). A negative $V_{gs}$ repels electrons from the channel surface and attracts holes, reinforcing the p-type barrier. With Q1 off, the entire 100 $\mu$A flows through Q2. The current is fully steered to one side. See: How It Works (Why Negative Gate Voltage Turns It OFF).
</details>

**Q4:** Why do IC designers make the differential pair transistors physically large, even though smaller transistors are faster?
<details>
<summary>Answer</summary>
**Matching.** Manufacturing variation (random dopant fluctuation, lithographic error) affects small transistors more than large ones. A mismatch between Q1 and Q2 creates an input offset voltage---the pair thinks there's a differential signal even when both inputs are equal. Larger transistors average out these random variations, reducing offset from ~10 mV to ~1 mV or less. The cost is more gate capacitance (slower). See: The Key Tension.
</details>

**Q5:** An engineer replaces the tail current source with a simple [[learning/notes/quick-context/resistor|resistor]] to GND. The circuit "works" on the bench but has poor CMRR. Why?
<details>
<summary>Answer</summary>
**A resistor doesn't have infinite output impedance.** When both inputs rise (common-mode), both transistors try to draw more current. A perfect current source holds the total at exactly 100 $\mu$A regardless. But a resistor allows more current when the voltage across it increases ($I = V/R$). So the total current changes with common-mode input, meaning the current split *does* change slightly, and the common-mode signal leaks into the output. A current source (implemented with a transistor in saturation, e.g., a cascode mirror) has much higher output impedance, rejecting common-mode signals far better.
</details>

</details>
