---
topic: Comparator Specifications
created: 2026-06-06
---

# Comparator Specifications (Reading the LMC7211-N Datasheet)

> **Related:** [[learning/notes/quick-context/tlv7211-as-lmc7211-replacement]]
>
> **Source datasheet:** [LMC7211-N (TI) — local PDF](lmc7211-n.pdf) — the worked example throughout this note. Section numbers (§4.1–4.6, §5) reference this file.

> **TL;DR:** The "Specifications" section of a comparator datasheet (the numbered `4.x` tables) is the part's contract. It tells you the limits you must *never* cross ([Absolute Maximum Ratings](#41-absolute-maximum-ratings-the-do-not-cross-lines)), the conditions where the part is *guaranteed* to work ([Operating Ratings](#42-operating-ratings-where-the-guarantees-apply)), its DC accuracy at each supply voltage ([Electrical Characteristics](#43-27v-electrical-characteristics-dc-accuracy-at-the-low-supply)), its speed ([AC Characteristics](#45-ac-electrical-characteristics-the-speed-numbers)), and graphs of how all of it drifts with voltage, load, and temperature ([Typical Characteristics](#46-typical-characteristics-the-graphs-how-it-all-drifts)). This walkthrough uses TI's [[quick-context/comparator|comparator]] **[LMC7211-N](lmc7211-n.pdf)**, a micropower CMOS rail-to-rail part, as the worked example.

## The Core Problem: "It Works on the Bench" Is Not a Spec

A [[learning/notes/quick-context/comparator|comparator]] that switches cleanly on your bench at room temperature can fail in the field if you run it past its rated supply, ask it to decide faster than its propagation delay allows, or trust a "typical" number that is only centered---not guaranteed---at 25°C. The datasheet's spec section exists to answer three questions precisely: *which* numbers are guaranteed, *under what conditions*, and *where the cliffs are*. Misreading it is how designs pass prototype and die in production.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Absolute Maximum Ratings** | Stress limits you must never exceed, even for an instant. Beyond them the part can be permanently damaged. These are *not* an operating range---a part is not designed to run at its absolute max. |
| **Operating Ratings** | The conditions (supply [[learning/notes/quick-context/voltage|voltage]], temperature) under which the device is functional and the electrical specs are guaranteed. The "safe operating envelope." |
| **Typical vs. Limit (boldface)** | *Typical* (Typ) is the average part at 25°C and nominal conditions---not guaranteed. *Limit* columns are tested and guaranteed worst case. **Boldface** limits hold across the full temperature range, not just at 25°C. |
| **Input Offset Voltage ($V_{OS}$)** | A small built-in voltage error between the two inputs from [[learning/notes/quick-context/transistor|transistor]] mismatch. The real switching point is $V_{REF} \pm V_{OS}$, so $V_{OS}$ sets your threshold accuracy. |
| **Propagation Delay ($t_{PD}$)** | Time from the input crossing the threshold until the output actually switches. It *shrinks as input overdrive grows*---a comparator hovering near its threshold is slow. |

<details>
<summary><strong>How It Works</strong> --- Walking through every spec section, 4.1 to 4.6</summary>

A datasheet's "Specifications" chapter is organized from *survival* (what won't break it) → *guarantees* (where the numbers hold) → *DC accuracy* → *speed* → *graphs*. Reading them in order builds the full picture. Here is each section of the LMC7211-N datasheet and what it actually means.

```
HOW THE 4.x SECTIONS RELATE
==============================================================================

   4.1 Absolute Max ──── outer fence: cross it → damage
        │
        │   (stay inside)
        ▼
   4.2 Operating Ratings ── safe envelope where specs are guaranteed
        │
        ├──► 4.3 Electrical Characteristics @ 2.7V  ── DC accuracy (offset,
        ├──► 4.4 Electrical Characteristics @ 5/15V     gain, swing, current);
        │                                               same table per supply
        ├──► 4.5 AC Characteristics ── speed (rise/fall, propagation delay)
        │
        └──► 4.6 Typical Characteristics ── graphs vs V, load, temperature
```

#### Every spec is grading one *stage* of the comparator

These numbers are not abstract---each one measures how well a specific stage of the [[quick-context/comparator|comparator's]] internal circuit does its job. The [[quick-context/comparator|comparator]] note breaks the chip into four stages: a [[quick-context/differential-pair|differential input pair]] (Q1/Q2) that senses `V(+) − V(-)`, a current-mirror active load (Q3/Q4), a [[quick-context/high-gain-amplifier-stage|high-gain node]] that amplifies the tiny difference, and an output stage (Q6) that drives the digital level. Map each spec onto that chain and the datasheet turns into a report card on the silicon:

```
SPEC  →  WHICH STAGE OF THE COMPARATOR IT GRADES
==============================================================================

   V(+) ──┐   ┌──────────────┐   ┌──────────────┐   ┌──────────┐
          ├──►│ DIFFERENTIAL │──►│  HIGH-GAIN   │──►│  OUTPUT  │──► Vout
   V(-) ──┘   │  PAIR Q1/Q2  │   │  NODE + Av   │   │ STAGE Q6 │
              └──────┬───────┘   └──────┬───────┘   └────┬─────┘
                     │                  │                │
              VOS, TCVOS,         Av (voltage      VOH, VOL, ISC,
              IB, CMVR            gain), CMRR       tPD, trise/tfall
                     │                  │                │
              "how cleanly       "how hard it     "how hard & how
               it senses the      amplifies the    close to the rails
               difference"        difference"      it drives"

              IS (supply current) = the standing bias the whole chain burns
              4.1 limits          = the ESD diodes + transistors' breakdown
```

| Spec | Grades which stage (see [[quick-context/comparator]]) |
|---|---|
| $V_{OS}$, $TCV_{OS}$ | The [[quick-context/differential-pair|differential pair]] (Q1/Q2) --- offset *is* its built-in mismatch |
| $I_B$ | The [[learning/notes/micro-context/mosfet|MOSFET]] input gates --- insulated, so ~zero current flows in |
| $CMRR$ | The [[learning/notes/micro-context/tail-current|tail current]] source (Q5) --- how well it holds total current fixed and ignores common-mode |
| $A_V$ | The [[quick-context/high-gain-amplifier-stage|high-gain node]] + mirror load --- the gain that slams the output to a rail |
| $CMVR$ | The input pair's usable voltage window (the rail-to-rail-and-beyond design) |
| $V_{OH}$, $V_{OL}$, $I_{SC}$ | The output stage (Q6 push-pull) --- how hard and how close to the rails it drives |
| $t_{PD}$, $t_{rise/fall}$ | The whole chain run with **no compensation [[learning/notes/quick-context/capacitor|capacitor]]** --- the structural reason a comparator is fast |
| $I_S$ | The standing bias current (tail + mirror) the chip burns just to stay alive |

### 4.1 Absolute Maximum Ratings --- "the do-not-cross lines"

These are **stress limits, not operating specs**. Exceed any one of them---even for a microsecond---and you risk permanent damage or permanently shifted parameters. The header note says it outright: "Absolute Maximum Ratings indicate limits beyond which damage to the device can occur."

| Rating (LMC7211-N) | Value | What it means |
|---|---|---|
| Supply Voltage ($V^+ - V^-$) | **16 V** | Total rail-to-rail supply that destroys the part above this. |
| Voltage at any Input/Output pin | $(V^+ +0.3)$ to $(V^- -0.3)$ V | Pins must stay within ~0.3 V of the rails (the on-chip protection diodes start conducting beyond this). |
| Current at Input pin | **±5 mA** | If an input is driven outside the rails, series resistors must limit current to this. |
| Current at Output pin | **±30 mA** | Beyond this the output transistor can be damaged. |
| Current at Power Supply pin | **40 mA** | Hard ceiling on what the supply pin can pass. |
| ESD Tolerance (HBM) | **2 kV** | Survives a 2 kV human-body-model static zap (1.5 kΩ + 100 pF). |
| Storage Temperature | **−65 to +150°C** | Survival range with no power applied. |
| Junction Temperature | **150°C** | The [[learning/notes/quick-context/silicon-die|silicon die]] itself must never get this hot. |

**Key idea:** a part is *not* designed to *operate* at these numbers---they only bound what won't break it. Notice the supply absolute max (16 V) sits just above the operating max (15 V): a deliberate 1 V margin.

> **↳ In the circuit:** these limits guard specific hardware inside the [[quick-context/comparator|comparator]]. The "stay within 0.3 V of the rails" input/output limit exists because every pin has on-chip ESD protection diodes to V+ and V−; push a pin past a rail and those diodes conduct, which is why the ±5 mA input limit then matters (you must add a series resistor to hold their current down). The ±30 mA output limit is the breakdown ceiling of the output transistor (Q6) that drives `Vout`. So 4.1 is really "don't cook the protection diodes or the output FET."

### 4.2 Operating Ratings --- "where the guarantees apply"

These define the **safe operating envelope**: the conditions under which the device is functional and the electrical specs in 4.3--4.5 actually hold.

| Operating Rating (LMC7211-N) | Value | What it means |
|---|---|---|
| Supply Voltage | **2.7 V ≤ $V_{CC}$ ≤ 15 V** | Works anywhere in this range; specs are characterized at 2.7, 5, and 15 V. |
| Junction Temp Range (–NAI, –NBI grades) | **−40 to +85°C** | The industrial temperature band over which boldface limits are guaranteed. |
| Thermal Resistance $\theta_{JA}$ (SO-8) | **136°C/W** | Each watt dissipated raises the die 136°C above ambient. |
| Thermal Resistance $\theta_{JA}$ (SOT23-5) | **203°C/W** | The tiny package sheds heat worse---it heats up faster per watt. |

$\theta_{JA}$ lets you check you won't blow past the 150°C junction limit: $T_J = T_A + \theta_{JA}\times P_D$. For a micropower comparator drawing microamps this is almost never a concern, but for the output driving a load it can matter.

> **↳ In the circuit:** the 2.7 V floor is the minimum supply that still leaves enough headroom to stack and bias the internal stages of the [[quick-context/comparator|comparator]]---the tail current source (Q5), the [[quick-context/differential-pair|differential pair]], the mirror load, and the output FET all need a few hundred mV across them to stay in their active region. Drop below the floor and the transistors starve, the [[quick-context/high-gain-amplifier-stage|gain]] collapses, and the clean digital snap turns mushy. That this part still works at 2.7 V is exactly the "rail-to-rail, low-voltage" design point the [[quick-context/comparator|comparator]] note describes.

### 4.3 2.7V Electrical Characteristics --- "DC accuracy at the low supply"

This is the first full **DC parameter table**, measured at $V^+=2.7\text{V}$, $V^-=0\text{V}$, $T_J=25°C$. Learn to read the *columns* first:

```
HOW TO READ AN ELECTRICAL-CHARACTERISTICS ROW
==============================================================================

   Symbol  Parameter     Conditions   Typ   NAI Limit   NBI Limit   Units
   ──────  ─────────     ──────────   ───   ─────────   ─────────   ─────
    VOS    Input Offset      —         3      5 / 8       15 / 18    mV max

   Reading each column:
     Symbol / Parameter  →  what the spec is (here, input offset voltage)
     Conditions          →  the exact test setup it was measured under
     Typ                 →  average part at 25°C        (NOT guaranteed)
     NAI Limit  5 / 8    →  guaranteed worst case, 5 mV offset grade
                            (plain 5 = limit at 25°C; bold 8 = over temp)
     NBI Limit  15 / 18  →  guaranteed worst case, 15 mV offset grade
     Units      mV max   →  the unit, and whether it bounds a max or min

   Plain number = limit at 25°C.   BOLDFACE = limit over full −40..+85°C.
```

Key LMC7211-N rows at 2.7 V:

| Symbol | Parameter | Typ | Meaning |
|---|---|---|---|
| $V_{OS}$ | [[micro-context/input-offset-voltage|Input Offset Voltage]] | 3 mV (max 5 / 8) | Built-in threshold error. The "–NAI" grade guarantees ≤5 mV (≤8 mV hot); the "–NBI" grade ≤15 mV. |
| $TCV_{OS}$ | [[micro-context/offset-voltage-drift|Offset Drift]] | 1.0 µV/°C | How much the offset wanders per degree. |
| $I_B$ | [[micro-context/input-bias-current|Input Current]] | 0.04 pA | Almost nothing---CMOS gates draw essentially zero current, so high-impedance sources are fine. |
| $CMRR$ | [[micro-context/common-mode-rejection-ratio|Common-Mode Rejection]] | 75 dB | How well it ignores a voltage common to both inputs. |
| $PSRR$ | [[micro-context/power-supply-rejection-ratio|Power-Supply Rejection]] | 80 dB | How well it ignores supply-rail wiggle. |
| $A_V$ | [[micro-context/open-loop-voltage-gain|Voltage Gain]] | 100 dB | The open-loop gain that slams the output to a rail. |
| $CMVR$ | [[micro-context/input-common-mode-range|Input Common-Mode Range]] | −0.3 to 3.0 V | Inputs work slightly *beyond both rails*---this is the "rail-to-rail-and-beyond" feature. |
| $V_{OH}/V_{OL}$ | [[micro-context/output-voltage-swing|Output High / Low]] | 2.5 V / 0.2 V | How close the push-pull output gets to each rail under 2.5 mA load. |
| $I_S$ | [[micro-context/quiescent-supply-current|Supply Current]] | 7 µA (max 12 / 14) | Micropower---runs for years off a coin cell. |

> **↳ In the circuit:** this table grades, parameter by parameter, the stages the [[quick-context/comparator|comparator]] note draws:
> - **$V_{OS}$ / $TCV_{OS}$ → the [[quick-context/differential-pair|differential pair]] (Q1/Q2).** Q1 and Q2 are *drawn* identical, but real silicon etches slightly differently, so they don't split the tail current evenly at exactly `V(+) = V(-)`. The few mV of input difference needed to re-balance them *is* the offset. This is why your real threshold is $V_{REF} \pm V_{OS}$, not exactly $V_{REF}$---the "ideal" rule "output flips when V(+) > V(-)" from the [[quick-context/comparator|comparator]] note has this small built-in error.
> - **$A_V$ (100 dB) → the [[quick-context/high-gain-amplifier-stage|high-gain node]].** This is the number behind the comparator's defining behavior: the [[quick-context/comparator|comparator]] note's "20 µA mismatch × 2 MΩ = huge swing → rail." Enormous open-loop gain is what turns a millivolt of imbalance into a full-rail digital output.
> - **$CMRR$ → the tail current source (Q5).** A perfect tail source keeps Q1+Q2's total current fixed, so moving *both* inputs together changes nothing at the output. CMRR measures how close to perfect it is---the same Q5 the [[quick-context/comparator|comparator]] note credits with "rejecting common-mode noise on both inputs."
> - **$CMVR$ → the input pair's voltage window.** It works from −0.3 V to 3.0 V (slightly past both rails)---the "rail-to-rail-and-beyond input" feature, which is what lets you sense a divider node sitting near ground or near V+.
> - **$V_{OH}$ / $V_{OL}$ → the output stage (Q6).** How close the push-pull output gets to each rail---i.e. how clean the digital HIGH/LOW levels are that feed your logic.
> - **$I_S$ → the standing bias** (tail + mirror currents) the chip burns just to stay biased and ready, even when the output isn't switching.

### 4.4 5.0V and 15.0V Electrical Characteristics --- "same DC table, higher supplies"

The **same parameters re-characterized** at the other two popular rails (5 V and 15 V), because comparator behavior is supply-dependent. What shifts versus the 2.7 V table:

- **CMRR improves** with supply: 75 dB at 5 V → **82 dB at 15 V** (more headroom rejects common-mode better).
- **Offset drift rises** with supply: $TCV_{OS}$ = 1.0 µV/°C at 5 V → **4.0 µV/°C at 15 V**.
- **Output drive tested harder**: $V_{OH}/V_{OL}$ now specified at **5 mA** load (vs 2.5 mA at 2.7 V).
- **New parameter $I_{SC}$ (Short-Circuit Current)** appears: **30 mA sourcing, 45 mA sinking**---how much the push-pull output dumps into a dead short.

**Lesson:** never read a single spec in isolation---pick the table that matches *your* rail. A number guaranteed at 5 V is not guaranteed at 15 V.

> **↳ In the circuit:** the new $I_{SC}$ row is purely an output-stage number---the most current the Q6 push-pull FETs in the [[quick-context/comparator|comparator]]'s output stage will dump into a dead short before current-limiting (30 mA sourcing, 45 mA sinking). It's asymmetric because the pull-down and pull-up FETs aren't the same size. This is also the spec that makes the [[quick-context/comparator|comparator]] note's "can drive an LED or a logic gate directly" claim true: a push-pull output that sources *and* sinks milliamps needs exactly this drive strength.

### 4.5 AC Electrical Characteristics --- "the speed numbers"

The **timing** table, measured at $V^+=5\text{V}$, $f=10\text{kHz}$, $C_L=50\text{pF}$:

| Symbol | Parameter | Typ | Meaning |
|---|---|---|---|
| $t_{rise}$ | Output Rise Time | 15 ns | How fast the output edge climbs once switching. |
| $t_{fall}$ | Output Fall Time | 15 ns | How fast the output edge falls. |
| $t_{PHL}$ | Prop. Delay, High→Low | 900 ns @ 10 mV / **450 ns @ 100 mV** | Crossing-to-switch delay. |
| $t_{PLH}$ | Prop. Delay, Low→High | 900 ns @ 10 mV / **420 ns @ 100 mV** | Same, other direction. |

```
PROPAGATION DELAY DEPENDS ON OVERDRIVE
==============================================================================

   Input (overdrive = how far past the threshold the input goes)

   small overdrive (10 mV):                 large overdrive (100 mV):

   Vth ──────╱──────                        Vth ──╱──────────
            ╱  slow to "decide"                  ╱  decides fast
   Output:                                  Output:
        ┌──────  (~900 ns later)                ┌──  (~450 ns later)
   ─────┘                                   ────┘

   MORE overdrive  →  FASTER decision.
   A comparator hovering right at its threshold is at its SLOWEST
   and most noise-sensitive --- the case for hysteresis.
```

This overdrive-dependence is the single most misread AC spec: the "420 ns" headline only applies with a healthy 100 mV kick. Near the threshold the part is 2× slower, which is exactly when noise causes chatter (see [[quick-context/comparator|hysteresis]]).

> **↳ In the circuit:** the AC numbers trace straight back to two structural facts from the [[quick-context/comparator|comparator]] note. **(1) Speed comes from what's *missing*:** a comparator omits the compensation capacitor an [[quick-context/op-amp|op-amp]] adds for feedback stability. That cap deliberately slows the [[quick-context/high-gain-amplifier-stage|gain]] node to microseconds; with no cap, the node snaps in nanoseconds---this is *the* reason "never use an op-amp as a comparator." **(2) Overdrive maps to the [[quick-context/differential-pair|differential pair]]:** more `V(+) − V(-)` drives a bigger current imbalance between Q1 and Q2, which charges the high-impedance gain node faster, so the output flips sooner. A tiny overdrive barely unbalances the pair → the node creeps → long delay. That's why the same chip is 900 ns at 10 mV but ~450 ns at 100 mV, and why hysteresis (which guarantees a minimum overdrive after each flip) also keeps the part fast.

### 4.6 Typical Characteristics --- "the graphs: how it all drifts"

These are **curves, not guaranteed limits**---they show how the part behaves across the continuous space the discrete tables can only sample. The LMC7211-N gives ten:

- **Supply current vs. supply voltage** (output high and low), across −40/25/125°C---confirms it stays in the single-digit µA across the whole range.
- **Output voltage vs. output sinking/sourcing current** at 5 V and 12 V---shows the output *can't quite reach the rail under load*; the harder you pull, the more volts it drops.
- **Propagation delay vs. input overdrive** at 5 V and 12 V, across temperature---the curve behind the 4.5 numbers, letting you read the delay at *your* overdrive and temperature.

> **↳ In the circuit:** the most instructive graph---output voltage vs. output current---is a direct picture of the [[quick-context/comparator|comparator]]'s output transistor (Q6). An ideal switch would clamp `Vout` exactly to a rail; the real FET has on-resistance, so the harder you make it sink or source, the more volts drop across it and the further `Vout` strays from the rail. That curve is *why* $V_{OH}/V_{OL}$ in §4.3--4.4 are specified *at a stated load current*. The supply-current and propagation-delay curves likewise show the bias network and [[quick-context/differential-pair|differential pair]] drifting with temperature---the same stages the DC and AC tables grade at fixed points.

**Why they exist:** the tables guarantee a few points; the graphs let you *interpolate* to your actual operating conditions. Use tables for go/no-go limits, graphs for "what will it roughly do here."

</details>

<details>
<summary><strong>The Key Tension</strong> --- Typical numbers vs. guaranteed limits</summary>

The central tension in reading any spec sheet: **the nice numbers are not the guaranteed numbers.** Marketing and your optimism both gravitate to the "Typical" column (3 mV offset! 7 µA!). But production parts scatter, and they drift over temperature. The only numbers you can *design against* are the Limit columns---especially the **boldface** ones that hold across the full −40 to +85°C range.

```
TYPICAL vs. GUARANTEED LIMIT (LMC7211-N input offset, −NAI grade)
==============================================================================

   Distribution of real parts' VOS:

       count
         │            ╱▔▔╲          Typ = 3 mV  ← center, NOT a promise
         │          ╱      ╲
         │        ╱          ╲
         │      ╱              ╲
         │    ╱                  ╲___
         └───┼─────────┼──────────┼────────► VOS
            -8        +3         +5    +8 mV
             │                    │     │
        bold limit            25°C limit  bold limit
        (cold)                          (hot)

   Design to ±8 mV (boldface) and EVERY shipped part, at any rated
   temperature, is covered. Design to the 3 mV typical and a chunk
   of production fails in the field.
```

| Approach | Upside | Downside |
|---|---|---|
| **Design to Typical** | Tighter thresholds, looks great on paper | Field failures---real parts miss it; nothing is guaranteed |
| **Design to 25°C Limit** | Guaranteed at room temp | Fails at temperature extremes (the boldface numbers are wider) |
| **Design to Boldface Limit** | Guaranteed for every part over full temp range | Must budget more margin (wider thresholds, more hysteresis) |

A second, related tension is **Absolute Maximum vs. Operating Ratings**. It is tempting to push the supply toward the 16 V absolute max for more range---but specs are only guaranteed to 15 V, and running near an absolute-max limit erodes reliability and ESD/transient headroom. The professional habit: design inside Operating Ratings with margin, and treat Absolute Maximum Ratings as a fence you instrument *against* (series resistors, clamp diodes), never a target.

</details>

<details>
<summary><strong>Concrete Example</strong> --- Vetting the LMC7211-N for a 3.0V battery monitor</summary>

You want to flag when a Li-ion cell sags below 3.0 V (see the worked circuit in [[quick-context/comparator]]). Before committing the LMC7211-N, you *walk the spec sections* to confirm each constraint is actually permitted---this is what the datasheet is for.

```
SPEC-SECTION CHECKLIST FOR A 3.0V UNDERVOLTAGE MONITOR
==============================================================================

  Requirement                        Section  Number              Verdict
  ──────────────────────────────────  ───────  ─────────────────   ───────
  Run from a 3.0–4.2 V cell           4.2      2.7–15 V operating   ✓ fits
  Never exceed survival limits        4.1      16 V abs max         ✓ huge
                                                                       margin
  Sense a divider node near ~1.5 V    4.3      CMVR −0.3 to 3.0 V   ✓ well
                                       (CMVR)                          inside
  Threshold accuracy                  4.3      VOS ≤ 8 mV (bold)    → ±8 mV
                                       (VOS)                           error
                                                                       budget
  Slow battery signal, speed irrelev. 4.5      tPD ~450 ns          ✓ don't
                                       (tPD)                           care
  Sip from the coin/backup cell       4.3      IS = 7 µA typ        ✓ years
                                       (IS)                            of life
```

Walking it concretely:

1. **4.2 Operating Ratings** --- the cell swings 3.0--4.2 V, comfortably inside the 2.7--15 V supply envelope. ✓
2. **4.1 Absolute Maximum** --- 4.2 V is nowhere near the 16 V damage limit; even a charger transient has margin. ✓
3. **4.3 CMVR** --- your divider presents ~1.5 V to the input; the −0.3 to 3.0 V common-mode range covers it (and would even let you sense right at ground). ✓
4. **4.3 $V_{OS}$** --- worst case ±8 mV offset over temperature. On a divide-by-2 node that is a ~16 mV uncertainty referred to the battery, so your 3.0 V trip point is really 3.0 V ±16 mV. Add hysteresis to swamp it.
5. **4.5 $t_{PD}$** --- a battery sags over seconds; 450 ns of delay is irrelevant. ✓
6. **4.3 $I_S$** --- 7 µA quiescent plus the divider current barely dents a 2000 mAh cell. ✓

Every box ticks. The point: you didn't *guess* the part fit---you read each requirement against the matching spec section and its *guaranteed* number.

**The one thing most outsiders get wrong about this is...** treating the big "Typical" numbers as guarantees, and treating "Absolute Maximum Ratings" as an operating range. Both are backwards. *Typical* is just the statistical center at 25°C and nominal supply---only the Limit columns (and especially the **boldface** over-temperature limits) are tested and promised. And *Absolute Maximum* is the opposite of an operating spec: it is the stress ceiling where damage begins, with *no* performance guaranteed near it. Designing to the wrong column or the wrong table is the classic way a board passes prototype and fails in the field.

</details>

<details>
<summary><strong>Choosing a Replacement</strong> --- cross-referencing a comparator by spec and package</summary>

When a part goes end-of-life, gets too expensive, or you just want a second source, you "cross-reference" it: find another comparator that does the same job. The trap is shopping by name or price---the right way is to read the *spec sections you just learned* and match them. Sort every requirement into two buckets:

```
FINDING A REPLACEMENT --- TWO QUESTIONS
==============================================================================

   1. WILL IT WORK?  (FUNCTION --- the 4.x electrical specs)
        │
        ├─ output type: push-pull vs open-drain?  → must match the circuit
        ├─ supply range covers my rail?           → §4.2 Operating Ratings
        ├─ input range covers my signals?         → §4.3 CMVR
        ├─ offset ≤ my threshold budget?          → §4.3 VOS
        ├─ fast enough at my overdrive?           → §4.5 tPD
        ├─ drives my load, reaches logic levels?  → §4.4 ISC, VOH/VOL
        ├─ supply current within budget?          → §4.3 IS
        └─ survives my worst-case transients?     → §4.1 Absolute Max
        │
   2. WILL IT FIT?   (FORM --- mechanical / dimensions)
        │
        ├─ same package?     (SOT23-5 vs SO-8)
        ├─ same pinout?      (pin ORDER can differ between same-size parts!)
        └─ same dimensions?  (length × width × height footprint)
        │
        ▼
   ALL yes  → DROP-IN replacement (no board change)
   function yes, form no → FUNCTIONAL equivalent (redesign the footprint)
   either NO on a "must match" row → keep looking
```

### What to match, and where each number lives

| What to check | Datasheet section | Replacement rule |
|---|---|---|
| **Output type** (push-pull vs open-drain) | §4.4 + [[quick-context/comparator]] | **Must match the circuit.** Open-drain needs a [[quick-context/comparator\|pull-up resistor]]; push-pull doesn't. Swap types and the board breaks unless you also add/remove the pull-up. |
| **Supply voltage range** | §4.2 Operating Ratings | New part's operating range must *contain* your rail, with margin. |
| **Input common-mode range** ($CMVR$) | §4.3 | Must include every voltage your inputs actually see. If you relied on rail-to-rail-and-beyond, keep it. |
| **Input offset grade** ($V_{OS}$) | §4.3 | New boldface $V_{OS}$ ≤ your threshold-error budget (don't regress accuracy). |
| **Propagation delay** ($t_{PD}$) | §4.5 | Fast enough at *your* overdrive. A "5 ns" part is fine replacing a 450 ns part; the reverse may not be. |
| **Output drive** ($I_{SC}$, $V_{OH}/V_{OL}$) | §4.4 | Must source/sink your load (LED, logic) and reach clean HIGH/LOW levels. |
| **Supply current** ($I_S$) | §4.3 | ≤ your power budget---critical for battery designs. |
| **Hysteresis** | [[quick-context/comparator]] | Built-in vs external changes noise behavior; match it or re-add external positive feedback. |
| **Temperature grade** | §4.2 | Operating temp range must cover your environment (e.g. industrial −40 to +85°C). |
| **Package + pinout + dimensions** | Mechanical section (§5/§8) | For a true *drop-in*: identical package, identical pin map, fits the same footprint and height. |

### Three tiers of "replacement"

1. **Drop-in / pin-compatible** --- same package, same pinout, specs equal-or-better. Solder it onto the existing board, no layout change. This is the only kind that needs *zero* rework.
2. **Functional equivalent** --- does the electrical job but differs mechanically (different package or pin order), so you redraw the footprint. Common when the original package is obsolete.
3. **Upgrade** --- better specs (faster, lower offset, lower current). Still re-check that *nothing* regressed---a faster part can be more noise-sensitive and may now need hysteresis it didn't before.

### Form matters as much as function

Two comparators can be electrically identical and still not interchange:

- **Same package ≠ same pinout.** The LMC7211-N itself proves it---its SOT23-5 and SOIC-8 versions put the inputs and supplies on *different* pin numbers (see the pinout in [[quick-context/comparator]]). A drop-in must match the *pin map*, not just the package name.
- **Dimensions can be the whole reason the part was chosen.** The LMC7211-N was picked for designs where its SOT23-5 body---**3.05 mm × 3.00 mm × 1.43 mm** (§5.1)---fits a tight space (it's thin enough for PCMCIA Type III cards). An electrically perfect replacement in an SO-8 body won't physically fit that slot, so dimensions are a hard constraint, not a nicety.

### Worked cross-reference: replacing the LMC7211-N

Handily, the LMC7211-N datasheet *is* a cross-reference guide---§5.7--5.8 list its own family, all rail-to-rail-input low-power comparators:

| Candidate | Output | Channels / package | Drop-in for LMC7211-N? |
|---|---|---|---|
| **LMC7211-N** | Push-pull | Single, SOT23-5 / SO-8 | (the original) |
| **LMC7221** | **Open-drain** | Single, SOT23-5 / SO-8 | *No*---functional cousin. Needs a pull-up; but **better** for mixed-voltage logic, where open-drain sets the HIGH level from a different rail. |
| **LMC6762** | Push-pull | **Dual**, SO-8 | Only if you want two comparators; different pinout. |
| **LMC6772** | Open-drain | Dual, SO-8 / DIP | Two channels + open-drain; not a single-part swap. |

So if your LMC7211-N circuit relies on its **push-pull** output driving an LED or logic directly, the LMC7221 is *not* a drop-in despite being nearly the same chip---you'd have to add a pull-up and re-check $V_{OH}$. But if you need to level-shift the output to a different logic rail, the open-drain LMC7221 is the *better* choice. That decision comes straight from the output-type row of the table above---which is exactly the [[quick-context/comparator|push-pull vs open-drain]] distinction the comparator note explains.

**Bottom line:** a comparator cross-reference is just the spec checklist from the *Concrete Example* above, run in reverse---instead of "does this part meet my needs?", you ask "does this *candidate* meet every number the original met, *and* fit the same footprint?"

> **↳ Worked cross-vendor example:** [[quick-context/mcp6541-as-lmc7211-replacement|Can the MCP6541 (LCSC C623499) replace the LMC7211-N?]] runs this exact checklist against a Microchip part. The verdict is the instructive one: a *mechanically perfect* drop-in (identical SOT23-5 pinout) that is electrically valid **only** below 5.5 V and for slow signals---an *upgrade* on current and hysteresis, but a *non-starter* above its 7 V absolute max. It shows why "same footprint" never settles a swap.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> --- Related topics to explore</summary>

- **[[quick-context/comparator]]** --- The device these specs describe. Read it first for *how a comparator works* ([[learning/notes/quick-context/differential-pair|differential pair]], hysteresis, open-drain vs push-pull); this doc covers *how to read its datasheet*. The LMC7211-N pinout and the two-inputs explanation live there.

- **[[quick-context/op-amp]]** --- Shares the same spec vocabulary ($V_{OS}$, CMRR, PSRR, $A_V$, CMVR). An op-amp datasheet has the same 4.x layout; the difference is op-amps add slew-rate/bandwidth specs while comparators add propagation-delay/overdrive specs.

- **[[quick-context/resistor]]** --- The reference divider that sets the trip voltage is built from [[quick-context/resistor|resistors]]; their tolerance stacks with the comparator's $V_{OS}$ to set total threshold accuracy.

- **[[quick-context/bjt-specifications]]** --- The same datasheet discipline applied to a discrete transistor instead of an IC: absolute-max "fences" ($V_{CEO}$, $I_C$, $P_C$) you never cross vs. design inputs ($\beta$) you work around, and the *typical ≠ guaranteed-across-temperature* trap shows up there as $h_{FE}$ spread and $P_C$ derating.

- **[[quick-context/pwm-controller-circuit]]** --- A real application where the comparator's *propagation delay* spec (4.5) directly limits switching frequency.

- **[[quick-context/tlv7211-as-lmc7211-replacement]]** --- The *unconditional* drop-in: TI's TLV7211/TLV7211A is the renamed, spec-identical successor to the LMC7211-N (same silicon, same pinout). The easiest replacement case --- with one trap: the grade-suffix is inverted (5 mV = TLV7211**A**).

- **[[quick-context/mcp6541-as-lmc7211-replacement]]** --- The *conditional* cross-vendor swap: the Microchip MCP6541 (LCSC C623499) fits the same footprint but trades away half the specs. Concrete proof that form-compatibility ≠ functional replacement. Read alongside the TLV7211 note for the full replacement spectrum.

- **[[micro-context/adc-analog-to-digital-converter]]** --- A comparator is a 1-bit ADC; its $V_{OS}$ and propagation-delay specs become the ADC's offset error and conversion-speed limits.

- **Datasheet "Typical / Limit / Boldface" convention** --- A reading skill that transfers to *every* analog part: typical = center, limit = guaranteed, boldface = guaranteed over full temperature.

</details>

<details>
<summary><strong>Test Your Understanding</strong> --- 5 progressive questions</summary>

**Q1:** The LMC7211-N lists a 16 V "Absolute Maximum" supply and a 15 V "Operating" supply. Can you run it continuously at 15.5 V?
<details>
<summary>Answer</summary>
**No.** 15.5 V is above the Operating Rating (max 15 V), so *no electrical spec is guaranteed* there---offset, gain, output swing, and supply current are all uncharacterized. It is below the 16 V Absolute Maximum, so it probably won't be instantly destroyed, but Absolute Maximum is a *damage/survival* limit, not an operating point. Run inside Operating Ratings with margin. See: How It Works (4.1 and 4.2).
</details>

**Q2:** The offset table shows "Typ 3, max 5, **8** (boldface)" for the –NAI grade. Which number do you design your threshold around, and why?
<details>
<summary>Answer</summary>
**The boldface 8 mV.** *Typ 3 mV* is only the statistical center at 25°C---not guaranteed for any individual part. *5 mV* is the guaranteed limit at 25°C only. The **boldface 8 mV** is the guaranteed worst case across the full −40 to +85°C operating range, so it's the only number that covers every shipped part at every rated temperature. Designing to 3 mV invites field failures. See: The Key Tension.
</details>

**Q3:** The AC table gives propagation delay as "900 ns @ 10 mV overdrive" but "450 ns @ 100 mV overdrive." Why does the same part have two different delays, and which case is the worst for a noisy slowly-moving signal?
<details>
<summary>Answer</summary>
**Propagation delay shrinks as input overdrive (how far past the threshold the input swings) grows---more overdrive turns the internal gain stage harder and faster.** A slowly-moving signal crosses the threshold with *tiny* overdrive, so it sees the slow ~900 ns case, right when it lingers near the threshold and noise can cause multiple crossings. That combination (low overdrive + slow + noisy) is the textbook argument for adding hysteresis. See: How It Works (4.5) and [[quick-context/comparator|comparator]] hysteresis.
</details>

**Q4:** A teammate quotes "CMRR = 82 dB" from the datasheet for a circuit running on a 5 V rail. What's wrong with that, and where would you look?
<details>
<summary>Answer</summary>
**82 dB is the 15 V number, not the 5 V number.** Section 4.4 lists CMRR as 75 dB at $V^+=5\text{V}$ and 82 dB at $V^+=15\text{V}$---the spec is supply-dependent. On a 5 V rail the correct figure is 75 dB. The lesson: electrical specs are characterized per supply voltage (2.7 V in 4.3, 5 V and 15 V in 4.4); always read the table/row matching your actual rail. See: How It Works (4.4).
</details>

**Q5:** The Electrical Characteristics tables give discrete guaranteed numbers, yet your design runs at 3.6 V and +60°C---a point that appears in *no* table. How do you estimate the part's behavior there, and what's the catch?
<details>
<summary>Answer</summary>
**Use the Typical Characteristics graphs (4.6) to interpolate.** The tables only guarantee a handful of points (2.7, 5, 15 V; 25°C and the temperature extremes); the *curves* in 4.6 plot supply current, output drop, and propagation delay continuously across voltage, load, and temperature, so you can read off the approximate value at 3.6 V / 60°C. The catch: graph values are **typical, not guaranteed**---they tell you what the part will *roughly* do, but only the table limits are a promise. Use graphs to predict behavior, tables to bound worst case. See: How It Works (4.6) and The Key Tension.
</details>

</details>
