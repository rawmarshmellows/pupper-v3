---
topic: Voltage-Current Causality (Which Causes Which?)
created: 2026-03-27
---

# Voltage-Current Causality

> **Related:** [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/quick-context/ac-to-dc-rectification]] | [[learning/notes/micro-context/buck-converter]] | [[learning/notes/micro-context/capacitive-voltage-sensing]] | [[learning/notes/micro-context/current-electrons-per-second]]

> **TL;DR:** Neither voltage "causes" current nor current "causes" voltage in any universal sense---the relationship depends on context. What's really happening is that the **electric field** is the fundamental entity: it both defines [[quick-context/voltage|voltage]] (as the integral of the field over distance) and drives [[quick-context/electric-current|current]] (as the force on charges). Voltage and current are *simultaneous constraints* on a circuit, not a one-way causal chain. The right question isn't "which causes which?" but "what establishes the field, and how does the circuit respond?"

## The Core Problem

You've learned $V = IR$ ([[quick-context/resistor|Ohm's law]]). It seems like voltage is the cause and current is the effect---apply voltage, get current. But then you learn that a changing current in an [[quick-context/inductor|inductor]] creates voltage ($V = L \times dI/dt$), and that in a [[quick-context/galvanic-cells-batteries|battery]], chemical reactions---not voltage---are the true starting point. The "voltage causes current" story breaks down because it was always an oversimplification. Understanding when each perspective applies (and when neither does) is the difference between memorizing equations and understanding circuits.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Electric Field** | The actual force-carrying entity. It pushes charges (creating current) and its integral over distance defines voltage. The field is always the mediator between V and I. |
| **Voltage Source** | A device (battery, power supply) that maintains a fixed voltage; current adjusts based on the load. Here, voltage is the *constraint* and current is the *response*---so it looks like "V causes I." |
| **Current Source** | A device that maintains a fixed current; voltage adjusts to whatever is needed. Here, current is the *constraint* and voltage is the *response*---so it looks like "I causes V." |
| **Constitutive Relation** | The equation relating V and I for a specific component: $V = IR$ for [[quick-context/resistor|resistors]], $V = L \, dI/dt$ for [[quick-context/inductor|inductors]], $I = C \, dV/dt$ for [[quick-context/capacitor|capacitors]]. These are *simultaneous constraints*, not causal arrows. |
| **Kirchhoff's Laws** | The circuit constraints: voltages around a loop sum to zero (KVL), currents into a node sum to zero (KCL). These enforce consistency but don't say which quantity "caused" the other. |

<details>
<summary><strong>How It Works</strong> --- Why the causality question is a trap</summary>

The confusion comes from treating $V = IR$ as a causal statement ("voltage causes current") rather than what it really is: a **constraint** that voltage and current must satisfy simultaneously.

```
THE CAUSAL CHAIN DEPENDS ON WHAT'S DRIVING THE CIRCUIT
==============================================================================

SCENARIO 1: BATTERY + RESISTOR ("Voltage causes current")
--------------------------------------------------------------------------

    Chemical reactions in the battery
         │
         ▼
    Charge separation at terminals
         │
         ▼
    Electric field established in circuit
         │
         ├──────────────────────────────────────┐
         ▼                                      ▼
    Voltage (integral of field)          Force on electrons
         │                                      │
         │              ┌───────┐               │
         └─────────────►│ V = IR │◄──────────────┘
                        └───┬───┘
                            │
                            ▼
                     Current flows

    The battery fixes the voltage.
    Current adjusts based on resistance.
    It LOOKS like V causes I.


SCENARIO 2: INDUCTOR ("Current causes voltage")
--------------------------------------------------------------------------

    Current is flowing through a coil
         │
         ▼
    Current changes (increases or decreases)
         │
         ▼
    Magnetic flux through coil changes
         │
         ▼
    Changing flux induces electric field (Faraday's law)
         │
         ▼
    V = L × dI/dt  (voltage appears across inductor)

    Here the changing current creates the voltage.
    It LOOKS like I causes V.


SCENARIO 3: CURRENT SOURCE + RESISTOR ("Current causes voltage")
--------------------------------------------------------------------------

    Current source forces fixed current through circuit
         │
         ▼
    Electrons push through resistor at rate I
         │
         ▼
    Collisions with atoms create voltage drop
         │
         ├──────────────────────────────────────┐
         ▼                                      ▼
    Current (forced by source)            Voltage (response)
         │              ┌───────┐               │
         └─────────────►│ V = IR │◄──────────────┘
                        └───┬───┘
                            │
                            ▼
                    Voltage = I × R

    The source fixes the current.
    Voltage adjusts based on resistance.
    Now V = IR reads as "I causes V."


SCENARIO 4: GENERATOR ("Mechanical motion causes both")
--------------------------------------------------------------------------

    Spinning turbine rotates coil in magnetic field
         │
         ▼
    Changing magnetic flux through coil
         │
         ▼
    Induced electric field in conductor (Faraday's law)
         │
         ├──────────────────────────────────────┐
         ▼                                      ▼
    Voltage appears                      If circuit is closed,
    (open circuit: V exists,             current flows
     no current)
         │                                      │
         └───────── NEITHER caused ─────────────┘
                    the other first.
                    Both arise from the
                    changing magnetic flux.
```

The real picture: **the electric field is the fundamental thing**, and voltage and current are two different ways of measuring what the field does.

```
THE FIELD-CENTRIC VIEW (the right mental model)
==============================================================================

                    ┌────────────────────────────────┐
                    │       ELECTRIC FIELD (E)        │
                    │   The actual physical entity     │
                    │   that exerts force on charges   │
                    └───────────┬──────────┬───────────┘
                                │          │
              ┌─────────────────┘          └─────────────────┐
              ▼                                              ▼
    ┌──────────────────────┐                   ┌──────────────────────────┐
    │  VOLTAGE (V)         │                   │  CURRENT (I)             │
    │                      │                   │                          │
    │  Integral of E       │                   │  Response of charges     │
    │  over distance       │                   │  to E in a material      │
    │                      │                   │                          │
    │  V = ∫ E · dl        │                   │  J = σE                  │
    │                      │                   │  (current density =      │
    │  Measures HOW MUCH   │                   │   conductivity × field)  │
    │  work the field      │                   │                          │
    │  does between        │                   │  Measures HOW MUCH       │
    │  two points          │                   │  charge actually moves   │
    └──────────────────────┘                   └──────────────────────────┘

    Voltage and current are BOTH consequences of the field.
    Neither one "causes" the other.
    They are two measurements of the same underlying phenomenon.


WHY Ohm's Law ISN'T a causal statement:
─────────────────────────────────────────────────────────────────────────────

    V = IR  is like  distance = speed × time

    Does speed "cause" distance? Or does distance "cause" speed?
    Neither---they're three quantities linked by a constraint.
    Which one you solve for depends on what you're controlling.

    Controlling V (voltage source):  I = V/R    →  "V causes I"
    Controlling I (current source):  V = IR     →  "I causes V"
    Controlling R (variable resistor): both adjust  →  "R causes the change"

    The equation is the SAME. The "causality" comes from
    the experimental setup, not the physics.
```

</details>

<details>
<summary><strong>The Key Tension</strong> --- Voltage-source thinking vs. current-source thinking</summary>

Most introductory courses teach circuits from a "voltage-source" perspective: batteries provide voltage, and current results. This is fine for simple resistive circuits but breaks down for more complex scenarios.

| Perspective | When It Works | When It Breaks Down |
|------------|--------------|-------------------|
| **"V causes I"** | Battery/supply driving resistors, LEDs, simple DC circuits | [[quick-context/inductor\|Inductors]] (where changing I creates V), current sources, electromagnetic induction |
| **"I causes V"** | Current sources, transistor bias analysis, inductor back-EMF | Voltage sources, [[quick-context/capacitor\|capacitors]] (where changing V creates I) |
| **"Field causes both"** | Always correct, but harder to use for circuit calculations | Never---this is the fundamental physics |

```
THE PRACTITIONER'S APPROACH: IT DEPENDS ON THE COMPONENT
==============================================================================

    COMPONENT          │ WHAT'S CONTROLLED    │ WHAT RESPONDS
    ═══════════════════╪══════════════════════╪═══════════════════════
    Voltage source     │ Voltage (fixed)      │ Current adjusts
    Current source     │ Current (fixed)      │ Voltage adjusts
    Resistor           │ (neither)            │ V and I linked by R
    Capacitor          │ Voltage can't jump   │ Current can jump
    Inductor           │ Current can't jump   │ Voltage can jump
    ───────────────────┼──────────────────────┼───────────────────────
    Generator          │ Mechanical input     │ Both V and I result
    Battery            │ Chemistry fixes V    │ I depends on load
    Piezo crystal      │ Mechanical stress    │ V appears
    Thermocouple       │ Temperature diff     │ V appears

    Engineers don't ask "which causes which?"
    They ask "what's the constraint, and what's free to adjust?"
```

The expert mental model: think of circuits as **systems of simultaneous constraints** (Kirchhoff's laws + constitutive relations for each component). Solve the system. "Causality" is just which variable you chose to fix and which you're solving for.

</details>

<details>
<summary><strong>Concrete Example</strong> --- Same circuit, three causal stories</summary>

Consider a simple series circuit: a source driving a [[quick-context/resistor|resistor]] (1 k$\Omega$) and an [[quick-context/inductor|inductor]] (10 mH) in series.

```
THREE STORIES ABOUT THE SAME CIRCUIT
==============================================================================

    ┌────────────────────────┐
    │   Source (5V step)     │
    └───┬────────────────┬───┘
        │                │
        │   ┌────────┐   │
        ├───┤  1 kΩ  ├───┤
        │   └────────┘   │
        │   ┌────────┐   │
        └───┤  10 mH ├───┘
            └────────┘

    Time constant: τ = L/R = 10 mH / 1 kΩ = 10 μs


STORY 1: "Voltage drives current" (voltage-source perspective)
──────────────────────────────────────────────────────────────────────────
    t = 0: Source applies 5V step
    • Inductor resists current change → current starts at 0
    • Full 5V appears across inductor (V_L = 5V, V_R = 0)
    • Current begins to ramp: dI/dt = V_L/L = 5V/10mH = 500 A/s

    t = 10 μs (one time constant):
    • Current reaches 3.16 mA (63% of final)
    • V_R = 3.16V, V_L = 1.84V

    t → ∞ (steady state):
    • Current reaches 5V/1kΩ = 5 mA (Ohm's law)
    • V_R = 5V, V_L = 0V (no more current change)

    Narrative: "The voltage source drove current through the RL circuit."


STORY 2: "Current creates voltage" (inductor perspective)
──────────────────────────────────────────────────────────────────────────
    t = 0: Current tries to change from 0
    • Inductor opposes: V_L = L × dI/dt = back-EMF
    • As current ramps, the CURRENT creates voltage across the inductor
    • The inductor's voltage is a direct consequence of current change

    At any moment: V_L = L × dI/dt
    • Current changing fast → big inductor voltage
    • Current changing slow → small inductor voltage
    • Current steady → zero inductor voltage

    Narrative: "The changing current created voltage across the inductor."


STORY 3: "Constraints determine everything" (the real answer)
──────────────────────────────────────────────────────────────────────────
    At every instant, ALL of these must be true simultaneously:

    1. KVL: V_source = V_R + V_L                    (voltages sum to source)
    2. V_R = I × R                                   (resistor constraint)
    3. V_L = L × dI/dt                               (inductor constraint)
    4. Same I flows through both components (series)

    Combining: 5V = I × 1000 + 0.01 × dI/dt

    This differential equation has ONE solution.
    No "cause"---just a system of constraints being satisfied.

    The equations don't say "V_source causes I."
    They say "V_source, I, V_R, and V_L are all linked."

    I(t) = 5 mA × (1 - e^(-t/10μs))

    Current, voltage across R, and voltage across L are all
    determined simultaneously by the constraints.
```

**The one thing most outsiders get wrong about this is...** thinking that Ohm's law ($V = IR$) tells you that voltage always comes first and current follows. This is a misreading of what the equation says. $V = IR$ is an *algebraic relationship*, not a causal arrow. It's like $F = ma$---does force cause acceleration, or does acceleration cause force? In Newtonian mechanics, force is the cause. But in general relativity, what we call "gravitational force" is actually a consequence of curved spacetime. The "causality" depends on which level of physics you're using. Similarly, in circuits: at the field level, the electric field is fundamental. At the circuit level, it depends on what you're controlling. Asking "does V cause I?" is like asking "does the left side of the equation cause the right side?" The equation doesn't have a direction.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]** — the end-to-end ladder from electricity to code executing; this note is one rung of it.

- **[[quick-context/voltage]]** --- Voltage is the integral of the electric field. The field is what actually pushes electrons; voltage quantifies how much work the field does between two points. Understanding this resolves most of the causality confusion.

- **[[quick-context/electric-current]]** --- Current is the flow of charge in response to the electric field. In different materials, the same field produces different currents (J = $\sigma$E), which is why resistance matters.

- **[[quick-context/resistor]]** --- The simplest V-I relationship (V = IR). In a resistor, V and I are proportional and in phase---no time delay, no stored energy, so the "cause" question is purely about what's driving the circuit.

- **[[quick-context/impedance-and-reactance]]** --- In AC circuits, capacitors and inductors create phase shifts between V and I. Current leads voltage in capacitors; voltage leads current in inductors. The phase shift makes the "which causes which" question even more confused---neither peaks first in any absolute sense.

- **[[quick-context/self-induction]]** --- The clearest case of "current causes voltage": changing current through an inductor creates back-EMF. The current change comes first; the voltage is the response.

- **[[quick-context/galvanic-cells-batteries]]** --- In batteries, chemistry is the true cause. Chemical reactions create charge separation, which creates the electric field, which manifests as both voltage and current. Neither V nor I is the root cause.

- **[[quick-context/electricity-generation]]** --- In generators, mechanical motion changes magnetic flux, which induces both voltage and current. The electromagnetic field mediates everything.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A 9V battery is connected to a 100$\Omega$ resistor. Does the voltage "cause" the current?
<details>
<summary>Answer</summary>
**It depends on what you mean by "cause."** At the circuit level, the battery fixes the voltage at 9V, and current results (I = 9V/100$\Omega$ = 90 mA). In that sense, voltage is the constraint and current is the response---so yes, "V causes I" is a useful description. But at the physics level, the battery's chemical reactions create an electric field, and both the voltage (integral of the field) and the current (field pushing electrons) are consequences of that field. Neither truly "causes" the other. See: How It Works (Scenario 1).
</details>

**Q2:** You suddenly open a switch in a circuit carrying current through an inductor. What happens, and which "causes" which?
<details>
<summary>Answer</summary>
**The inductor generates a large voltage spike.** When you open the switch, you try to instantly reduce current to zero. The inductor opposes this: $V = L \times dI/dt$, and a very fast dI/dt creates a very large voltage. This can be hundreds or thousands of volts---enough to arc across the switch contacts. Here, the *change in current* clearly causes the voltage. This is the most vivid example of "I causes V." See: How It Works (Scenario 2) and [[quick-context/self-induction]].
</details>

**Q3:** In an AC circuit with a capacitor, current leads voltage by 90 degrees. Does this mean current "happens first" and causes the voltage?
<details>
<summary>Answer</summary>
**No---phase lead doesn't mean temporal causation.** The 90-degree phase shift is a steady-state relationship: both the voltage and current sinusoids have existed "forever" in the AC analysis. The relationship $I = C \times dV/dt$ means current is proportional to the *rate of change* of voltage. When voltage is changing fastest (zero crossing), current is at its peak. When voltage is at its peak (not changing), current is zero. This is a constraint, not a causal sequence. If forced to pick a "cause," the AC source driving the circuit is the cause of both. See: [[quick-context/impedance-and-reactance]].
</details>

**Q4:** A student says "Ohm's law proves voltage always causes current because V = IR means voltage is on the left side." What's wrong with this reasoning?
<details>
<summary>Answer</summary>
**Equation arrangement doesn't imply causation.** You can equally write I = V/R or R = V/I. The same equation written three ways doesn't change the physics. It's like saying $F = ma$ proves force causes acceleration, but $a = F/m$ proves acceleration causes force. Which variable is "cause" depends on which one you're controlling in your experiment, not which side of the equals sign it's on. With a voltage source, V is the input and I is the output. With a current source, I is the input and V is the output. The equation itself is direction-neutral. See: How It Works (Why Ohm's Law ISN'T a causal statement).
</details>

**Q5:** A piezoelectric sensor produces voltage when you squeeze it. A thermocouple produces voltage from a temperature difference. How do these fit into the "voltage vs. current causality" picture?
<details>
<summary>Answer</summary>
**They demonstrate that neither voltage nor current is always the root cause---other physical phenomena are.** A piezoelectric crystal converts mechanical stress into charge separation (and thus voltage). A thermocouple converts thermal energy into voltage via the Seebeck effect. In both cases, the "cause" is something entirely outside the V-I framework: force and heat respectively. This reinforces the field-centric view: various energy sources create electric fields through different mechanisms. Voltage and current are both *downstream consequences* of those fields. The real question is always "what creates the field?"---and the answer varies: chemistry (batteries), magnetism (generators), mechanical stress (piezo), heat (thermocouples), light (photovoltaics).
</details>

</details>
