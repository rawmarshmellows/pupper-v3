---
topic: Inside the Triangle — Complete Op-Amp / Comparator Signal Path
created: 2026-04-01
---

# Inside the Triangle

> **Related:** [[quick-context/keypress-to-pixel-pipeline]] | [[quick-context/op-amp]] | [[quick-context/comparator]] | [[quick-context/comparator-specification]]

> **TL;DR:** The triangle symbol on a schematic hides 5--20 [[quick-context/transistor|transistors]] wired in three stages: a [[quick-context/differential-pair|differential pair]] that senses the input difference, a [[quick-context/high-gain-amplifier-stage|current-mirror gain stage]] that amplifies it to a full-rail swing, and an output stage that drives the load. The same three stages appear in both [[quick-context/op-amp|op-amps]] and [[quick-context/comparator|comparators]]---the only difference is whether a compensation capacitor is added between stages 2 and 3.

## The Core Problem: The Triangle Is a Black Box

You see this symbol everywhere in schematics:

```
    ───┤+  ╲
       │    ╲
       │     ╲──── Vout
       │     ╱
    ───┤-  ╱
       │  ╱
```

Datasheets tell you the gain is 100,000x, input impedance is infinite, and output impedance is zero. But what's actually *inside*? How does a [[quick-context/voltage|voltage]] difference of 1 mV become a 3.3V output swing? Why do [[quick-context/op-amp|op-amps]] need negative feedback to be stable but [[quick-context/comparator|comparators]] don't? The answers come from understanding the three-stage signal path that every [[quick-context/op-amp|op-amp]] and [[quick-context/comparator|comparator]] shares.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Stage 1: [[quick-context/differential-pair\|Differential pair]]** | Two matched transistors + [[micro-context/tail-current|tail current]] source. Converts a [[quick-context/voltage|voltage]] difference ($V_+ - V_-$) into a current difference. Rejects common-mode signals. |
| **Stage 2: [[quick-context/high-gain-amplifier-stage\|High-gain amplifier]]** | [[micro-context/current-mirror|Current mirror]] active load on the [[quick-context/differential-pair|differential pair]]. Converts the $\mu$A current difference into a full-rail voltage swing by exploiting the high impedance at the mirror output node. |
| **Stage 3: Output buffer** | Drives the external load. Push-pull ([[quick-context/op-amp|op-amp]]) or open-drain/open-collector ([[quick-context/comparator|comparator]]). Provides low output impedance so the signal doesn't droop under load. |
| **Compensation [[quick-context/capacitor|capacitor]] ($C_c$)** | A small [[quick-context/capacitor|capacitor]] (~10--30 pF) at the Stage 2 output node. Present in op-amps (limits speed, ensures stability). Absent in comparators (maximum speed, no feedback to stabilize). **This is the single component that separates an op-amp from a comparator.** |
| **Bias network** | Current mirrors and voltage references that set the DC operating point for every [[quick-context/transistor|transistor]]. Ensures all transistors sit in saturation, ready to amplify. Typically adds 3--5 more transistors beyond the 5 in the core signal path. |

<details>
<summary><strong>How It Works</strong> --- The complete 7-[[quick-context/transistor|transistor]] signal path</summary>

### The Full Circuit: All Three Stages Connected

This is the simplest complete op-amp/comparator---7 transistors that do everything. Q1--Q5 form the core amplifier (Stages 1+2 combined in the [[quick-context/high-gain-amplifier-stage|5-transistor OTA]]). Q6--Q7 form the output buffer (Stage 3).

```
COMPLETE OP-AMP / COMPARATOR (7 transistors)
==============================================================================

                                    Vdd
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
               ┌────┴────┐          │           ┌────┴────┐
               │   Q3    │          │           │   Q6    │
               │  (PMOS) │          │           │  (PMOS) │ ← output
               └────┬────┘          │           └────┬────┘   pull-up
                    │               │                │
                    ├──── Q3=Q4 ────┤                │
                    │    (mirror)   │                │
               ┌────┴────┐         │           ┌────┴────┐
               │   Q4    │         │           │         │
               │  (PMOS) │         │           ├─────────┼──► Vout
               └────┬────┘         │           │         │
                    │              │           │    ┌────┴────┐
     ┌──────────────┤              │           │    │   Q7    │
     │              │              │           │    │  (NMOS) │ ← output
     │         high-impedance      │           │    └────┬────┘   pull-dn
     │           node A ──────────►gate Q6     │         │
     │              │              │           │        GND
     │              │              │           │
     │         ┌────┴────┐         │     ┌─ ─ ─┴─ ─ ─┐
     │         │   Q2    │         │     │   Cc       │ ← COMPARATOR:
     │         │  (NMOS) │         │     │ (10-30 pF) │   this cap is
     │         └────┬────┘         │     │            │   ABSENT
     │              │              │     │  OP-AMP:   │
┌────┴────┐         │              │     │  this cap  │
│   Q1    │         │              │     │  is PRESENT│
│  (NMOS) │         │              │     └─ ─ ─┬─ ─ ─┘
└────┬────┘         │              │           │
     │              │              │           │
V(+)►gate      gate◄V(-)          │      gate◄── node A
     │              │              │           │
   source        source            │           │
     └──────┬───────┘              │           │
            │                      │           │
       ┌────┴────┐                 │           │
       │   Q5    │                 │           │
       │  (NMOS) │  ← tail (100 μA)           │
       └────┬────┘                 │           │
            │                      │           │
           GND                     │           │
                                   │           │
                              Vbias network    │
                            (not shown: sets   │
                             Q5, Q6, Q7 bias)  │


    SIGNAL PATH:
    ═══════════════════════════════════════════════════════════

    V(+), V(-)                    node A                   Vout
        │                           │                        │
        ▼                           ▼                        ▼
    ┌─────────┐  current diff  ┌─────────┐  voltage    ┌─────────┐
    │ STAGE 1 ├───────────────►│ STAGE 2 ├────────────►│ STAGE 3 ├──► Vout
    │ Diff    │  (μA)          │ Gain    │  (volts)    │ Output  │
    │ Pair    │                │ Stage   │             │ Buffer  │
    │ Q1, Q2  │                │ Q3, Q4  │             │ Q6, Q7  │
    └─────────┘                └─────────┘             └─────────┘
     V → I                      I → V                    V → V
     (sense)                    (amplify)               (drive)
```

### Stage-by-Stage Signal Trace: 1 mV Input → Full Output Swing

```
COMPLETE SIGNAL TRACE (V+ = 1.501V, V- = 1.500V, Vdd = 3.3V)
==============================================================================

STAGE 1: Differential Pair (Q1, Q2, Q5)
──────────────────────────────────────────────────────────────────────────────
Input:  V(+) - V(-) = 1 mV
Action: Q1 gate is 1 mV higher than Q2 gate
        → Q1 Vgs slightly larger → Q1 conducts slightly more
        → Q1 = 51 μA, Q2 = 49 μA  (tail Q5 enforces total = 100 μA)
Output: 2 μA current difference between left and right branches

    What changed:  voltage difference → current difference
    Gain so far:   none yet (just transduction, not amplification)


STAGE 2: Current Mirror Gain Stage (Q3, Q4 on top of Q1, Q2)
──────────────────────────────────────────────────────────────────────────────
Input:  Left branch = 51 μA (through Q1 and Q3)
        Right branch = 49 μA (through Q2)
Action: Q3 carries 51 μA (forced by Q1). Mirror copies to Q4 → 51 μA.
        At node A: Q4 pushes 51 μA down, Q2 pulls only 49 μA down.
        Mismatch: 2 μA net into node A.
        Node A impedance: ~2 MΩ (Q4 ‖ Q2 output impedances)
        Voltage: 2 μA × 2 MΩ = 4V → clipped to ~3.1V (near Vdd)
Output: Node A swings to near Vdd (3.1V)

    What changed:  2 μA current mismatch → ~3V voltage swing
    Gain so far:   1 mV input → 3.1V at node A = ~3,100× (70 dB)


STAGE 3: Output Buffer (Q6, Q7)
──────────────────────────────────────────────────────────────────────────────
Input:  Node A = 3.1V (drives gate of Q7 in NMOS output, or Q6 in PMOS)
Action: Depends on output stage type:

    OP-AMP (push-pull):
    • Node A = 3.1V → Q7 (NMOS) turns ON hard → pulls Vout to ~0V
    • Q6 (PMOS) gate also controlled → turns OFF
    • Vout driven LOW with low output impedance (~50Ω)
    • Can source or sink current to the load

    COMPARATOR (open-drain):
    • Node A = 3.1V → output NMOS turns ON → pulls Vout to GND
    • External pull-up resistor provides HIGH level when NMOS is OFF
    • Can only sink current (open-drain)

Output: Vout = 0V (LOW) for op-amp; Vout = GND for comparator

    What changed:  high-impedance node voltage → low-impedance output
    Total gain:    1 mV → 0V output (saturated)


THE ONE DIFFERENCE: Compensation Capacitor
──────────────────────────────────────────────────────────────────────────────

    Same input (1 mV), same transistors, same gain — but:

                  OP-AMP                      COMPARATOR
                  ──────                      ──────────
    Cc present?   YES (10-30 pF)              NO

    What Cc does: limits how fast node A       node A swings at
                  can change voltage           full transistor speed
                  (SR = I_tail / Cc)

    Time for      ~1 μs                       ~5 ns
    output to
    swing:

    Why:          Op-amp uses negative         Comparator has no
                  feedback. Without Cc,        feedback loop. Speed
                  the high gain + speed        is the only goal.
                  causes oscillation.          No stability concern.
                  Cc trades speed for
                  stability.
```

### Why the Golden Rules Work (Now You Can See Why)

The [[quick-context/op-amp|op-amp's]] "golden rules" (no input current, V+ = V-) are direct consequences of this circuit:

```
GOLDEN RULES EXPLAINED BY THE CIRCUIT
==============================================================================

RULE 1: "No current flows into the inputs"
──────────────────────────────────────────────────────────────────────────────
    V(+) and V(-) connect to MOSFET gates (Q1, Q2).
    MOSFET gates are capacitor plates — insulated by oxide.
    No DC current can flow through an insulator.
    → Input impedance is essentially infinite.

    (BJT-input op-amps DO draw a tiny base current — nanoamps
     to microamps — which is why the datasheet lists "input bias
     current." MOSFET-input op-amps have picoamp input current.)


RULE 2: "V+ = V-" (with negative feedback)
──────────────────────────────────────────────────────────────────────────────
    The gain from V(+)-V(-) to Vout is ~100,000×.
    If V+ - V- = even 0.01 mV → Vout moves by 1V.

    With negative feedback: Vout connects back to V(-).
    If V+ > V- by even a tiny amount:
      → Vout rises (by 100,000× the difference)
      → Feedback raises V- toward V+
      → Difference shrinks
      → Vout stops rising

    Equilibrium: V+ - V- = Vout / 100,000 ≈ 0
    → V+ ≈ V-  (within microvolts)

    Without feedback (comparator mode):
      → V+ ≠ V- (no mechanism to equalize)
      → Vout saturates at rail
      → This is INTENTIONAL for a comparator
```

</details>

<details>
<summary><strong>The Key Tension</strong> --- Op-amp vs. comparator is a one-component difference</summary>

The entire difference between an op-amp and a comparator comes down to **one capacitor** and the design choices that follow from it:

| Feature | Op-Amp | Comparator | Why Different |
|---------|--------|------------|---------------|
| Compensation cap | 10--30 pF | None | Op-amp needs stability under feedback |
| Output transition | 1--50 $\mu$s | 1--500 ns | Cap limits slew rate |
| Output stage | Push-pull (linear) | Open-drain or push-pull (digital) | Op-amp needs proportional output; comparator needs rail-to-rail snap |
| Overdrive recovery | Slow (input stage saturates) | Fast (designed for it) | Op-amp never expects large Vdiff; comparator always has it |
| Intended use | Negative feedback loop | Open-loop or positive feedback | Fundamentally different operating mode |

```
THE SAME 5 TRANSISTORS, TWO DIFFERENT PRODUCTS
==============================================================================

    PRODUCT: OP-AMP                      PRODUCT: COMPARATOR

    ┌─────────────────────────┐          ┌─────────────────────────┐
    │                         │          │                         │
    │  Q1 Q2  (diff pair)    │          │  Q1 Q2  (diff pair)    │
    │  Q3 Q4  (mirror)       │          │  Q3 Q4  (mirror)       │
    │  Q5     (tail)         │          │  Q5     (tail)         │
    │                         │          │                         │
    │  + Cc (compensation)   │          │  (no Cc)               │
    │  + push-pull output    │          │  + open-drain output   │
    │  + trimmed for low     │          │  + optimized for fast  │
    │    offset voltage      │          │    overdrive recovery  │
    │                         │          │                         │
    │  Use: feedback circuits │          │  Use: threshold detect │
    │  Speed: moderate        │          │  Speed: fast            │
    │  Output: analog         │          │  Output: digital        │
    └─────────────────────────┘          └─────────────────────────┘

    Same silicon. Same physics. Different optimization.
```

This is why you should never use an op-amp as a comparator: the compensation capacitor slows it down, the output stage isn't designed for rail-to-rail digital levels, and the input stage isn't designed for large overdrive. It "works" in a prototype but fails in production.

</details>

<details>
<summary><strong>Concrete Example</strong> --- Building intuition with the LM358 (op-amp) vs. LM393 (comparator)</summary>

These two ICs are often sold together and have nearly identical pinouts. Internally, they share the same basic three-stage topology but with different optimizations:

```
LM358 (OP-AMP) vs LM393 (COMPARATOR)
==============================================================================

    Package:     Both DIP-8, both dual (two units per package)
    Pinout:      Nearly identical (Vcc, GND, +in, -in, out × 2)
    Price:       Both ~$0.20
    Die size:    Similar (~20 transistors each)
    Input stage: Both BJT differential pairs

    DIFFERENCE         │ LM358 (op-amp)      │ LM393 (comparator)
    ═══════════════════╪═════════════════════╪════════════════════
    Compensation cap   │ ~30 pF internal     │ None
    Output stage       │ Push-pull           │ Open-collector NPN
    Slew rate          │ 0.3 V/μs            │ N/A (digital output)
    Propagation delay  │ N/A (analog output) │ ~1.3 μs (typ.)
    GBW product        │ 1 MHz               │ N/A
    Output HIGH        │ Vcc - 1.5V          │ External pull-up
    Output LOW         │ ~0V                 │ ~0.1V (Vce_sat)
    Can drive logic?   │ Poorly              │ Yes (designed for it)
    Input offset       │ 2 mV (trimmed)      │ 5 mV (less critical)


WHAT HAPPENS WHEN YOU SWAP THEM
==============================================================================

    Using LM358 (op-amp) as comparator:
    ──────────────────────────────────────────────────────────────
    Input:  V+ crosses V- by 1 mV
    • Diff pair steers 2 μA mismatch to node A
    • Node A charges through Cc (30 pF)
    • Time to swing: ΔV / SR = 3V / 0.3 V/μs = 10 μs ← SLOW!
    • Output can't reach Vcc rail (tops out at Vcc - 1.5V)
    • If input bounces, op-amp takes another 10 μs to recover
    → Works on bench, fails in noisy environment

    Using LM393 (comparator) as op-amp:
    ──────────────────────────────────────────────────────────────
    Connect in inverting amplifier configuration with feedback
    • No compensation cap → gain stage responds instantly
    • High gain + fast response + feedback = OSCILLATION
    • Output oscillates at MHz, never settles
    • Open-collector output can't drive analog loads properly
    → Doesn't work at all
```

**The one thing most outsiders get wrong about this is...** thinking op-amps and comparators are fundamentally different devices. They're not. They're the same three-stage circuit with one component changed. The triangle on the schematic hides 5--20 transistors that are almost identical in both cases. The entire behavioral difference---speed, output type, stability---comes from whether a ~20 pF capacitor is present at one internal node. That's it. Understanding the three stages and the role of that capacitor lets you predict the behavior of any op-amp or comparator from first principles.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> --- Related topics to explore</summary>

- **[[quick-context/differential-pair]]** --- Stage 1 in detail. How matched transistors steer current, why the [[micro-context/tail-current|tail current]] source is essential, and how common-mode rejection works.

- **[[quick-context/high-gain-amplifier-stage]]** --- Stage 2 in detail. How current mirrors create high impedance, why $V = I \times R$ with a 2 M$\Omega$ impedance produces huge gain, and the gain-vs-headroom tradeoff with cascodes.

- **[[quick-context/op-amp]]** --- The [[quick-context/op-amp|op-amp]] as a user-facing component: golden rules, inverting/non-inverting configurations, gain-bandwidth product. This file explains what the triangle *does*; the current file explains what's *inside* it.

- **[[quick-context/comparator]]** --- The [[quick-context/comparator|comparator]] as a user-facing component: hysteresis, propagation delay, open-drain outputs. Same internal circuit but optimized for binary output instead of linear amplification.

- **[[quick-context/transistor]]** --- Every element in all three stages is a [[quick-context/transistor|MOSFET or BJT]]. The gate-oxide capacitor structure explains Rule 1 (no input current); saturation-mode output impedance explains the gain mechanism.

- **[[quick-context/pwm-controller-circuit]]** --- A real-world system where both an op-amp (error amplifier) and a comparator ([[micro-context/pwm-pulse-width-modulation|PWM]] generator) work together inside the same IC, each using the same three-stage topology.

</details>

<details>
<summary><strong>Test Your Understanding</strong> --- 5 progressive questions</summary>

**Q1:** What are the three stages inside an op-amp or comparator, and what does each convert?
<details>
<summary>Answer</summary>
**Stage 1: [[quick-context/differential-pair|Differential pair]]** — converts a voltage difference into a current difference (V → I). **Stage 2: High-gain amplifier** — converts the current difference into a large voltage swing (I → V). **Stage 3: Output buffer** — converts the high-impedance voltage into a low-impedance output that can drive loads (V → V, with impedance transformation). See: How It Works (Signal Path diagram).
</details>

**Q2:** What single component differentiates an op-amp from a comparator?
<details>
<summary>Answer</summary>
**The compensation capacitor ($C_c$), typically 10--30 pF, connected at the Stage 2 output node.** Present in op-amps (limits speed, ensures stability under negative feedback). Absent in comparators (allows maximum speed, since there's no feedback loop to stabilize). Everything else---speed, output type, overdrive recovery---follows from this one choice. See: The Key Tension.
</details>

**Q3:** Why does the op-amp golden rule "V+ = V-" work, explained in terms of the three stages?
<details>
<summary>Answer</summary>
**The gain is ~100,000×, and negative feedback forces equilibrium.** If V+ exceeds V- by even 0.01 mV, Stage 1 creates a current difference, Stage 2 amplifies it to a ~1V swing at node A, and Stage 3 drives Vout. With negative feedback, Vout connects back to V-, raising V- until V+ - V- ≈ Vout/100,000 ≈ 0. The inputs are driven to be equal *because* the gain is so enormous that any difference is immediately corrected. Without feedback (comparator), this equilibrium never forms, and Vout saturates at the rail. See: How It Works (Golden Rules Explained).
</details>

**Q4:** An engineer measures an LM358 op-amp's response time when used as a comparator and gets 10 $\mu$s. An LM393 comparator responds in ~1.3 $\mu$s. Both have similar transistor counts. Why the ~8× speed difference?
<details>
<summary>Answer</summary>
**The LM358's internal 30 pF compensation capacitor limits its slew rate.** The cap must charge/discharge through the tail current: $SR = 100\ \mu A / 30\ pF = 3.3\ V/\mu s$. To swing 3.3V takes $\sim 1\ \mu s$, and overdrive recovery adds more delay, pushing total response to ~10 $\mu$s. The LM393 has no compensation cap, so node A charges only the parasitic [[quick-context/capacitance|capacitance]], giving much faster slewing. Additionally, the LM393's output stage and input stage are designed for overdrive recovery, while the LM358's are not. See: Concrete Example (What Happens When You Swap Them).
</details>

**Q5:** Could you build a "universal" IC that works as both an op-amp and a comparator by adding a switch to connect/disconnect the compensation capacitor?
<details>
<summary>Answer</summary>
**In theory yes, but it would be a poor version of both.** The compensation cap is only one of several design differences. Op-amps also have: (1) trimmed [[micro-context/input-offset-voltage|input offset voltage]] (important for precision, less critical for comparators), (2) output stages optimized for linear operation over the full swing range, (3) bias currents optimized for low noise rather than speed. Comparators have: (1) output stages optimized for clean logic levels and fast transitions, (2) input stages designed for large overdrive without saturation, (3) internal clamping to prevent latch-up under overdrive. A switchable cap would give you the speed difference but not the output or overdrive optimizations. In practice, both parts cost $0.20, so using the right one for the job is cheaper than building a compromise.
</details>

</details>
