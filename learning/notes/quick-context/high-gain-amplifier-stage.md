---
topic: High-Gain Amplifier Stage
created: 2026-04-01
---

# High-Gain Amplifier Stage

> **Related:** [[learning/notes/quick-context/comparator]] | [[learning/notes/quick-context/ros2-architecture]] | [[learning/notes/quick-context/capacitance]] | [[learning/notes/quick-context/differential-pair]] | [[learning/notes/quick-context/op-amp]]

> **TL;DR:** The high-gain amplifier stage sits between the [[learning/notes/quick-context/differential-pair|differential pair]] input and the output buffer in [[learning/notes/quick-context/op-amp|op-amps]] and [[learning/notes/quick-context/comparator|comparators]]---it converts the differential pair's small current difference (microamps) into a large [[learning/notes/quick-context/voltage|voltage]] swing (volts) by forcing that current through a very high impedance node, achieving 60--100 dB of voltage gain with just a few [[learning/notes/quick-context/transistor|transistors]].

## The Core Problem: A Current Difference Isn't Useful Yet

The [[learning/notes/quick-context/differential-pair|differential pair]] senses the voltage difference between two inputs and converts it into a current difference---say 60 $\mu$A vs. 40 $\mu$A, a 20 $\mu$A difference. But downstream circuits (output stages, logic gates, [[learning/notes/micro-context/mosfet|MOSFET]] drivers) need a large *voltage* swing, not a current difference. You need to convert 20 $\mu$A of current imbalance into a voltage swing approaching the full supply rails (0V to 3.3V). That's the job of the high-gain amplifier stage: it multiplies the small signal by 1,000--100,000x by exploiting one simple principle---push a small current through a very high impedance and you get a large voltage ($V = I \times R$).

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **[[learning/notes/micro-context/current-mirror|Current mirror]]** | A circuit that copies a current from one branch to another using matched [[quick-context/transistor\|transistors]]. In the gain stage, it acts as an "active load" with extremely high output impedance---much higher than any [[quick-context/resistor\|resistor]] could practically provide. |
| **Active load** | Using a transistor (current mirror) instead of a resistor as the drain load. A resistor's impedance is just R (e.g., 10 k$\Omega$). A transistor in saturation has output impedance of 100 k$\Omega$--10 M$\Omega$, giving 10--1000x more gain from the same current. |
| **High-impedance node** | The point where the differential pair's drain current meets the current mirror's output. Both sides present high impedance, so even a tiny current mismatch creates a large voltage change. This node is where gain happens. |
| **Voltage gain ($A_v$)** | The ratio of output voltage swing to input voltage difference. For the gain stage: $A_v = g_m \times (r_{o,n} \| r_{o,p})$, where $g_m$ is the differential pair's transconductance and $r_o$ is the output resistance. Typical: 60--100 dB (1,000--100,000x). |
| **Cascode** | Stacking a second transistor on top of the first to increase the output impedance (and therefore gain) even further. Common in precision op-amps where 100+ dB gain is needed. Adds complexity but doesn't add more current consumption. |

<details>
<summary><strong>How It Works</strong> --- Current mirror turns current into voltage</summary>

### The Key Insight: $V = I \times R$, So Make R Enormous

If you have a 20 $\mu$A current imbalance and push it through a 10 k$\Omega$ resistor, you get $V = 20\ \mu A \times 10\ k\Omega = 0.2\ V$. That's gain, but not much.

If you push that same 20 $\mu$A through a 5 M$\Omega$ impedance, you get $V = 20\ \mu A \times 5\ M\Omega = 100\ V$ --- which gets clipped to the supply rail (say 3.3V). That's the gain stage in action: the output slams to the rail with a tiny input, which is exactly what a [[learning/notes/quick-context/comparator|comparator]] needs.

The trick is: you can't use a 5 M$\Omega$ resistor (it would be physically huge and drop the entire supply voltage). Instead, you use a **transistor in saturation** as the load. A saturated transistor acts like a current source with very high output impedance---it passes a roughly fixed current regardless of the voltage across it. Two current sources fighting at a single node creates the high-impedance condition.

### The 5-Transistor Gain Stage (Simplest Complete Amplifier)

This is the most common building block inside op-amps and comparators. It combines the [[learning/notes/quick-context/differential-pair|differential pair]] (Q1, Q2) with a current mirror active load (Q3, Q4) and a [[learning/notes/micro-context/tail-current|tail current]] source (Q5):

```
5-TRANSISTOR OTA (Operational Transconductance Amplifier)
==============================================================================

                        Vdd
                         │
              ┌──────────┼──────────┐
              │          │          │
         ┌────┴────┐     │     ┌────┴────┐
         │   Q3    │     │     │   Q4    │   Q3, Q4 = PMOS current mirror
         │  (PMOS) │     │     │  (PMOS) │   (active load)
         └────┬────┘     │     └────┬────┘
              │          │          │
         Q3 drain        │     Q4 drain
              │          │          │
              ├──mirror──┤          ├──────────── Vout
              │  (gates  │          │             (HIGH-IMPEDANCE NODE)
              │  tied)   │          │
              │          │          │
         Q1 drain        │     Q2 drain
              │          │          │
         ┌────┴────┐     │     ┌────┴────┐
         │   Q1    │     │     │   Q2    │   Q1, Q2 = NMOS differential pair
         │  (NMOS) │     │     │  (NMOS) │
         └────┬────┘     │     └────┬────┘
              │          │          │
    V(+) ────►gate       │     gate◄──── V(-)
              │          │          │
            source       │       source
              └──────┬───┘───┬──────┘
                     │       │
                     │  ┌────┴────┐
   Vbias ───────────►gate  Q5    │   Q5 = NMOS tail current source
                     │  │  (NMOS) │   (sets total current, e.g., 100 μA)
                     │  └────┬────┘
                     │       │
                     │      GND
```

### Step-by-Step: How Current Becomes Voltage

```
SIGNAL FLOW THROUGH THE GAIN STAGE
==============================================================================

Step 1: Differential pair steers current
──────────────────────────────────────────────────────────────────────────────

    Inputs: V(+) is slightly higher than V(-)
    → Q1 conducts more, Q2 conducts less
    → Q1 drain current = 60 μA, Q2 drain current = 40 μA
    (Total stays at 100 μA — tail current source Q5 enforces this)


Step 2: Current mirror copies Q1's current to Q4
──────────────────────────────────────────────────────────────────────────────

    Q3 and Q4 form a PMOS current mirror:
    • Q3's gate and drain are tied together (diode-connected)
    • Q3 is forced to carry whatever Q1 pushes: 60 μA
    • Q3's gate voltage adjusts to sustain 60 μA
    • Q4's gate is tied to Q3's gate → Q4 also tries to push 60 μA

    Q3 ← 60 μA (forced by Q1)     Q4 → 60 μA (copies Q3)
              mirror
    Q3 gate ──────── Q4 gate
    (same Vgs → same current)


Step 3: Current mismatch at the output node
──────────────────────────────────────────────────────────────────────────────

    At the output node (Q4 drain = Q2 drain):

    Q4 pushes DOWN:  60 μA  (copied from Q3/Q1 side)
    Q2 pulls UP:     40 μA  (set by differential pair)
                     ──────
    Mismatch:        20 μA  net current trying to flow INTO the node

         Vdd
          │
     ┌────┴────┐
     │   Q4    │ pushes 60 μA ↓
     └────┬────┘
          │
          ├──── Vout  ← WHERE DOES THE EXTRA 20 μA GO?
          │
     ┌────┴────┐
     │   Q2    │ pulls 40 μA ↓
     └────┬────┘
          │
         tail


Step 4: Voltage rises to absorb the mismatch
──────────────────────────────────────────────────────────────────────────────

    The output node has very high impedance (both Q4 and Q2 are
    in saturation, acting like imperfect current sources).

    The extra 20 μA has nowhere to go → it charges the parasitic
    capacitance at the output node → Vout rises.

    Vout rises UNTIL one transistor leaves saturation:
    • As Vout approaches Vdd, Q4 (PMOS) loses drain-source headroom
      → Q4 enters triode (linear) region → can no longer maintain 60 μA
      → current equalizes → Vout settles near Vdd

    The result: a tiny input difference (maybe 1 mV) pushed Vout
    from mid-rail all the way to near Vdd.


Step 5: Opposite input → opposite result
──────────────────────────────────────────────────────────────────────────────

    If V(+) < V(-):
    • Q1 = 40 μA, Q2 = 60 μA
    • Mirror copies 40 μA to Q4
    • Q4 pushes 40 μA, Q2 pulls 60 μA → net 20 μA OUT of node
    • Vout drops toward GND

    This is why the stage has GAIN: a millivolt input difference
    creates a full-rail output swing.


GAIN EQUATION:
──────────────────────────────────────────────────────────────────────────────

    Av = gm × (ro_Q4 ‖ ro_Q2)

    where:
    • gm = transconductance of Q1/Q2 ≈ 1 mA/V (typical at 100 μA)
    • ro_Q4 = output impedance of Q4 (PMOS) ≈ 500 kΩ
    • ro_Q2 = output impedance of Q2 (NMOS) ≈ 500 kΩ
    • ro_Q4 ‖ ro_Q2 = 250 kΩ  (parallel combination)

    Av = 1 mA/V × 250 kΩ = 250  (≈ 48 dB)

    For higher gain, use cascode transistors to increase ro
    to 10-50 MΩ → Av = 10,000-50,000 (80-94 dB)
```

### Why This Is Different in Op-Amps vs. Comparators

In an [[learning/notes/quick-context/op-amp|op-amp]], a **compensation [[learning/notes/quick-context/capacitor|capacitor]]** is connected at the high-impedance output node. This capacitor deliberately slows the voltage transition (limits the slew rate) to prevent oscillation when negative feedback is applied. The capacitor trades speed for stability.

In a [[learning/notes/quick-context/comparator|comparator]], there is **no compensation capacitor**. The high-impedance node is free to swing as fast as the transistors allow. This is why comparators are much faster than op-amps---the gain stage isn't deliberately slowed down.

```
OP-AMP vs COMPARATOR GAIN STAGE
==============================================================================

    OP-AMP:                              COMPARATOR:

    Q4 drain ──┬──── Vout                Q4 drain ──┬──── Vout
               │                                    │
             ──┴──  Cc (compensation cap)           │  (no cap!)
             ──┬──  (~10-30 pF on-chip)             │
               │                                    │
    Q2 drain ──┘                         Q2 drain ──┘

    Slew rate limited by:                Slew rate limited by:
    SR = I_tail / Cc                     parasitic capacitance only
    = 100 μA / 30 pF                    (~0.1-1 pF)
    = 3.3 V/μs                          → 100-1000 V/μs

    Deliberately slow                    As fast as physics allows
    (prevents oscillation                (no feedback loop to
     in feedback circuits)                worry about)
```

</details>

<details>
<summary><strong>The Key Tension</strong> --- Gain vs. speed vs. power</summary>

| Want | Problem |
|------|---------|
| **Higher gain** | Need higher output impedance → use cascode → adds voltage headroom loss, reduces output swing |
| **Faster response** | Need lower parasitic capacitance at output node → smaller transistors → worse matching, lower gain |
| **Lower power** | Need less tail current → lower $g_m$ → lower gain. $g_m \propto \sqrt{I_{tail}}$ for MOSFETs. |
| **Wider output swing** | Need transistors to stay in saturation over a wide voltage range → longer channel lengths → slower |

```
GAIN vs. HEADROOM TRADEOFF
==============================================================================

    Simple mirror (Q3, Q4):
    ─────────────────────────────────────────────────────────────
    Gain: ~40-50 dB
    Headroom: only Vds_sat (~0.2V) per transistor consumed
    Output swing: Vdd - 2×Vds_sat to GND + 2×Vds_sat
    Speed: fast (fewer nodes)

    Cascode mirror (Q3+Q3c, Q4+Q4c):
    ─────────────────────────────────────────────────────────────
    Gain: ~80-90 dB
    Headroom: 2×Vds_sat (~0.4V) per side consumed
    Output swing: reduced (stacked transistors eat headroom)
    Speed: similar (impedance is higher but capacitance similar)

    Folded cascode:
    ─────────────────────────────────────────────────────────────
    Gain: ~80-90 dB
    Headroom: only 1×Vds_sat per side (folds the cascode sideways)
    Output swing: better than telescopic cascode
    Speed: moderate (extra current paths add capacitance)
    Power: higher (separate bias current for cascode stage)
```

At low supply voltages (1.2V or below), the headroom problem becomes severe. Stacking two transistors in a cascode eats 0.4V of the 1.2V budget. This is why modern low-voltage ICs use gain-boosted cascodes or multi-stage designs instead.

</details>

<details>
<summary><strong>Concrete Example</strong> --- Following a signal through the LM393 comparator</summary>

The LM393 is one of the most common comparators. Let's trace a signal through its gain stage:

```
LM393 SIGNAL PATH (simplified)
==============================================================================

    Inputs: V(+) = 1.501V,  V(-) = 1.500V  (1 mV difference)
    Supply: Vcc = 5V, GND = 0V

    STAGE 1: Differential pair
    ─────────────────────────────────────────────────────────────
    Tail current: 100 μA
    Q1 (driven by V+): 51 μA    (slightly more, due to 1 mV advantage)
    Q2 (driven by V-): 49 μA
    Current difference: 2 μA

    STAGE 2: Current mirror active load
    ─────────────────────────────────────────────────────────────
    Mirror copies Q1 current to Q4 side: Q4 pushes 51 μA
    Q2 pulls only 49 μA
    Mismatch: 2 μA net INTO the high-impedance node

    Output impedance at node: ~2 MΩ (both transistors in saturation)
    Voltage generated: 2 μA × 2 MΩ = 4V
    → Clipped to Vcc = 5V (node saturates high)

    STAGE 3: Output (open-collector NPN)
    ─────────────────────────────────────────────────────────────
    High voltage at gain node → turns ON the output NPN transistor
    → Output pin pulled to GND (LOW)

    Result: 1 mV input difference → output = LOW (0V)
    Propagation delay: ~300 ns (limited by parasitic capacitance)


    If V(+) < V(-) by 1 mV:
    ─────────────────────────────────────────────────────────────
    Mirror pushes 49 μA, Q2 pulls 51 μA → 2 μA OUT of node
    → Node drops to near GND → output NPN turns OFF
    → Output floats (open collector) → pulled HIGH by external resistor

    Result: output = HIGH
```

**The one thing most outsiders get wrong about this is...** thinking the gain stage is some exotic circuit. It's just **two current sources fighting at a node**. The mirror says "push 60 $\mu$A," the differential pair says "pull 40 $\mu$A." The 20 $\mu$A mismatch has nowhere to go except to charge/discharge the node's parasitic capacitance, swinging the voltage to the rail. That's all gain is: a current mismatch at a high-impedance point. The same principle works in op-amps, comparators, voltage regulators, and any analog IC with gain.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> --- Related topics to explore</summary>

- **[[learning/notes/quick-context/differential-pair]]** --- The stage that feeds the high-gain amplifier. The [[learning/notes/quick-context/differential-pair|differential pair]] converts a voltage difference into the current difference that the gain stage then amplifies into a voltage swing.

- **[[learning/notes/quick-context/comparator]]** --- The [[learning/notes/quick-context/comparator|comparator]] is the simplest user of the gain stage: differential pair + gain stage + digital output, with no compensation capacitor. The gain stage's speed (not its precision) is what matters.

- **[[learning/notes/quick-context/op-amp]]** --- In an [[learning/notes/quick-context/op-amp|op-amp]], a compensation capacitor at the gain stage's output node deliberately limits the speed to prevent oscillation under negative feedback. The gain stage is identical; the compensation is the difference.

- **[[learning/notes/quick-context/transistor]]** --- Every element in the gain stage (mirror transistors, cascode transistors, bias sources) is a [[learning/notes/quick-context/transistor|MOSFET or BJT]] in saturation. Understanding saturation ($V_{ds} > V_{gs} - V_{th}$) and output impedance ($r_o$) is key to understanding why the node impedance is so high.

- **[[learning/notes/quick-context/resistor]]** --- The gain stage exists because [[learning/notes/quick-context/resistor|resistors]] can't provide enough impedance. A 5 M$\Omega$ resistor would be physically impractical and would drop the entire supply voltage. Active loads (transistor current mirrors) solve both problems: high impedance in a tiny area with no DC voltage waste.

</details>

<details>
<summary><strong>Test Your Understanding</strong> --- 5 progressive questions</summary>

**Q1:** The differential pair outputs 55 $\mu$A on Q1 and 45 $\mu$A on Q2. What current does the current mirror push through Q4?
<details>
<summary>Answer</summary>
**55 $\mu$A.** Q3 carries Q1's 55 $\mu$A (forced by Q1). Q4's gate is tied to Q3's gate, so Q4 copies this current and pushes 55 $\mu$A. At the output node, Q4 pushes 55 $\mu$A but Q2 only pulls 45 $\mu$A, so there's a 10 $\mu$A mismatch that drives the output voltage up. See: How It Works (Step 2).
</details>

**Q2:** Why can't you use a regular resistor as the load instead of a current mirror?
<details>
<summary>Answer</summary>
**Not enough impedance.** A practical resistor might be 10 k$\Omega$. With a 10 $\mu$A current difference, you get $V = 10\ \mu A \times 10\ k\Omega = 0.1\ V$ --- not enough to swing the output to the rails. A current mirror in saturation has output impedance of 500 k$\Omega$--10 M$\Omega$, giving 50--1000x more gain. Also, a large resistor would drop too much DC voltage (10 k$\Omega$ at 50 $\mu$A = 0.5V, eating into headroom), while a transistor in saturation only needs ~0.2V. See: The Core Problem.
</details>

**Q3:** What does the compensation capacitor in an op-amp do to the gain stage, and why doesn't a comparator have one?
<details>
<summary>Answer</summary>
**The compensation cap limits how fast the output node voltage can change** (slew rate = $I_{tail} / C_c$). In an op-amp, this prevents the loop from oscillating when negative feedback is applied---without it, the high gain and speed would cause instability. A comparator has no negative feedback loop (it operates open-loop or with positive feedback for hysteresis), so there's no stability concern. Removing the cap lets the output swing as fast as the parasitic capacitance allows, which is why comparators are 100--1000x faster than op-amps. See: How It Works (Op-Amp vs Comparator Gain Stage).
</details>

**Q4:** In the 5-transistor OTA, what happens if Q3 and Q4 are poorly matched (Q4 copies 62 $\mu$A instead of 60 $\mu$A)?
<details>
<summary>Answer</summary>
**The output has a DC offset.** Even with equal inputs (V+ = V-), the current mismatch between Q4 (62 $\mu$A) and Q2 (50 $\mu$A) drives the output away from mid-rail. This appears as an **input offset voltage**---the comparator or op-amp will trip at a slightly different threshold than intended. In an op-amp, negative feedback corrects for this somewhat, but it still degrades precision. In a comparator, it shifts the trip point by a millivolt or so. This is why matching is critical. See: [[learning/notes/quick-context/differential-pair]] (The Key Tension: Matching).
</details>

**Q5:** An engineer wants more gain from the 5-transistor OTA without adding more power. What can they do?
<details>
<summary>Answer</summary>
**Add cascode transistors** (stack a second transistor on top of Q2 and Q4). This increases the output impedance from $r_o$ to $g_m \times r_o^2$ (gain squared), boosting voltage gain from ~50 dB to ~80--90 dB with the same tail current. The cost is reduced output voltage swing (each cascode eats ~0.2V of headroom) and slightly more complexity. At very low supply voltages (<1.5V), this headroom loss becomes a problem, which is why folded-cascode and gain-boosted architectures were invented. See: The Key Tension (Gain vs. Headroom Tradeoff).
</details>

</details>
