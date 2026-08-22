---
topic: BJT Specifications (Choosing a Transistor)
created: 2026-06-07
---

# BJT Specifications — The 5 Numbers That Decide If a Transistor Survives

> **Related:** [[quick-context/bjt]] | [[quick-context/transistor]] | [[quick-context/power-watts-joules]] | [[quick-context/resistor]] | [[quick-context/fundamental-electronic-parts-index|Parts Index]]
>
> **Companion note:** [[quick-context/bjt|BJT (how it works)]] explains the physics and operating regions. *This* note is the buyer's checklist — the datasheet numbers you check before you drop a part into a circuit.

> **TL;DR:** Before you pick a [[quick-context/bjt|BJT]], five datasheet specs decide whether it survives your circuit: **type** (NPN vs PNP — polarity, not "less [[quick-context/voltage|voltage]]"), **$V_{CEO}$** (the off-state voltage it can hold before it breaks down), **$I_C$** (the most current it can carry), **$P_C$** (the most heat it can dissipate, $P = V_{CE}\cdot I_C$), and **$\beta$ / $h_{FE}$** (the current gain, which tells you the *minimum* base current you must supply). The first three are "do-not-cross" limits; the last is what you design *around*.

## The Core Problem: A Transistor That Works on the Bench Can Still Burn Up

A BJT that switches your LED perfectly at 5 V can be destroyed instantly by a 30 V inductive spike, cooked by a motor that pulls more current than rated, or simply fail to turn fully on because you starved its base. Every one of those failures is predicted by a number printed in the datasheet. Reading those numbers *before* you solder is the difference between a circuit that ships and one that releases [the magic smoke](https://en.wikipedia.org/wiki/Magic_smoke). This note is the five-item checklist.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Type (NPN / PNP)** | The polarity of the part. NPN turns on with the base *above* the emitter and is wired emitter-to-ground; PNP turns on with the base *below* the emitter and is wired emitter-to-supply. Both need ~0.7 V across the base–emitter junction to conduct — NPN does **not** need "less voltage." NPN is simply preferred because electrons move ~2–3× faster than holes, giving it more gain and speed for the same size. |
| **$V_{CEO}$ (Collector–Emitter Breakdown, base Open)** | The maximum voltage the transistor can hold across collector→emitter while **off** before it avalanche-breaks-down. When the BJT is off, nearly the full supply $V_{CC}$ appears across it, so you need $V_{CEO} > V_{CC}$ (with margin). |
| **$I_C$ (Max Collector Current)** | The largest continuous current the collector can carry without the bond wires or silicon failing. Your load current must stay below this. |
| **$P_C$ / $P_D$ (Power Dissipation)** | The most heat the package can shed before the junction overheats. The heat made *inside* the BJT is $P = V_{CE}\cdot I_C$. This rating shrinks as the part gets hotter (thermal derating). |
| **$\beta$ / $h_{FE}$ (DC Current Gain)** | The amplification factor: $I_C = \beta \cdot [[micro-context/input-bias-current|I_B]]$. Typically 50–300. It tells you the **minimum base current** you must inject to support a given collector current: $I_B \ge I_C / \beta_{min}$. It drifts with current and temperature — never a precision number. |

<details>
<summary><strong>How It Works</strong> — Walking the 5 specs in the order you check them</summary>

The five specs split into two groups with very different jobs. Three of them ($V_{CEO}$, $I_C$, $P_C$) are **fences** — cross any one and the part can be permanently damaged. The other two (type, $\beta$) are **design inputs** — they shape how you wire and drive the part. Check the fences first (will it survive?), then the design inputs (will it do the job?).

```
THE BJT SPEC CHECKLIST
==============================================================================

  SURVIVAL FENCES (never cross — damage)        DESIGN INPUTS (work around)
  ----------------------------------------      ----------------------------
   1. Type        polarity + which way it       (also a design input —
                  is wired                        listed first by habit)
   2. V_CEO  ───  off-state voltage ceiling
   3. I_C    ───  on-state current ceiling      5. beta / hFE  current gain
   4. P_C    ───  heat ceiling  (V_CE x I_C)        -> sets minimum I_B

   Pick so that:   V_CC        <   V_CEO
                   I_load      <   I_C
                   V_CE x I_C  <   P_C        (after temp derating)
                   I_B         >=  I_load / beta_min   (then over-drive)
```

**1. Type — NPN vs PNP (polarity, not voltage).**
The single most common beginner myth is "NPN needs less voltage to turn on." It does not. *Both* types need roughly the same ~0.6–0.7 V across the base–emitter junction to start conducting. The real differences:

- **Direction of control.** NPN turns on when the base is pulled *more positive* than the emitter; PNP turns on when the base is pulled *more negative* than the emitter.
- **How it's wired.** NPN sits with its emitter at ground and switches a load on the high side toward the supply — the natural fit for a [[micro-context/microcontroller|microcontroller]] pin that idles low and drives high. PNP sits with its emitter at the supply (high-side switch).
- **Why NPN is preferred.** In NPN the charge carriers are electrons; in PNP they are holes. Electrons drift roughly **2–3× faster** than holes (higher mobility), so for the same chip area an NPN gives higher gain, faster switching, and a lower saturation voltage. That physics — not voltage — is why NPN is the default.

```
NPN — LOW-SIDE SWITCH   (emitter at GND;   drive base HIGH to turn ON)

      +V_CC
        │
     ┌──┴──┐
     │LOAD │
     └──┬──┘
        │
        C
    ┌───┴───┐
B ─►┤  NPN  │
    └───┬───┘
        E
        │
       GND


PNP — HIGH-SIDE SWITCH  (emitter at +V_CC;  drive base LOW to turn ON)

      +V_CC
        │
        E
    ┌───┴───┐
B ─►┤  PNP  │
    └───┬───┘
        C
        │
     ┌──┴──┐
     │LOAD │
     └──┬──┘
        │
       GND
```

**2. $V_{CEO}$ — the off-state voltage ceiling.**
When a switch transistor is *off*, it is blocking the supply: almost the entire $V_{CC}$ drops across the collector–emitter terminals. $V_{CEO}$ is how much it can block before the junction avalanche-breaks-down and conducts uncontrollably (often destroying the part). The subscript spells out the test condition: **C**ollector–**E**mitter, base **O**pen.

$$V_{CEO} > V_{CC} \quad(\text{always — with margin, ideally } V_{CEO} \ge 2\times V_{CC})$$

The margin matters because inductive loads (motors, relays, solenoids) generate spikes *far* above $V_{CC}$ when switched off ($V = L \,di/dt$). A 12 V motor can fling a 60 V+ spike at a transistor rated $V_{CEO} = 40$ V and kill it — which is exactly why the [[quick-context/bjt|BJT motor-driver]] needs a flyback diode.

> There are three breakdown specs and they are not interchangeable: **$V_{CEO}$** (collector–emitter, base open — the one quoted for switching), **$V_{CBO}$** (collector–base, emitter open — usually the highest), and **$V_{EBO}$** (emitter–base, base–emitter reverse breakdown — usually only ~5–7 V, easy to exceed by accident).

**3. $I_C$ — the on-state current ceiling.**
The maximum continuous current the collector terminal can carry. Above it the bond wires overheat and the silicon degrades. Your worst-case load current must stay comfortably under it (derate to ~50–70% for reliability). Datasheets also list a higher *peak/pulsed* $I_{CM}$ for brief surges — don't confuse the two.

**4. $P_C$ — the heat ceiling.**
This is the one beginners forget, and it's the one that quietly cooks parts. The transistor itself dissipates power equal to the voltage across it times the current through it:

$$P_{dissipated} = V_{CE} \cdot I_C$$

That power becomes heat in the junction. $P_C$ (often called $P_D$, total device dissipation) is the most heat the package can shed before the junction exceeds its max temperature (~150 °C). **The danger zone is the linear region**, where $V_{CE}$ and $I_C$ are *both* large at the same time:

- **Saturated switch (good):** $V_{CE}\approx 0.2$ V, $I_C = 0.5$ A → $P = 0.1$ W. Cool.
- **Half-on linear (bad):** $V_{CE}= 6$ V, $I_C = 0.5$ A → $P = 3$ W. Likely smoke.

This is why you drive a switching BJT *hard* into saturation — to keep $V_{CE}$ tiny so $P = V_{CE}\cdot I_C$ stays small. The datasheet's **Safe Operating Area (SOA)** graph plots $I_C$ vs $V_{CE}$ and draws the $P_C$ limit as a diagonal hyperbola ($I_C = P_C / V_{CE}$): you must stay *under* all the boundaries at once.

```
SAFE OPERATING AREA (log-log, conceptual)
==============================================================================

  I_C
  (A)
  1.0 |******|                         I_C max (horizontal ceiling)
      |      |*****
      |      |     *****
      |      |          ***            P_C limit:  I_C = P_C / V_CE
      |      |             ***              (constant-power hyperbola)
  0.1 |      |                **
      |      |                   **
      |      |                     *|
      |      |  SAFE: stay under    |  <- V_CEO (vertical ceiling)
      |      |  every boundary      |
      +------+----------------------+--------------- V_CE (V)
            V_CE(sat)              V_CEO

   The operating point (V_CE, I_C) must sit BELOW the hyperbola,
   LEFT of V_CEO, and BELOW I_C-max — simultaneously.
```

**Thermal derating:** $P_C$ is quoted at a reference case/ambient temperature (e.g. 25 °C). Above that, the rating falls off linearly to zero at the max junction temperature. A "625 mW" small-signal part in free air at 25 °C might only safely handle ~300 mW once the board warms up. The governing relation is $P_{max} = (T_{j,max} - T_{ambient}) / R_{\theta JA}$, where $R_{\theta JA}$ (junction-to-ambient thermal resistance, °C/W) is the part's "thermal Ohm's law" — see [[quick-context/power-watts-joules|electrical power & heat]].

**5. $\beta$ / $h_{FE}$ — the gain that sets your base current.**
Gain is the ratio of collector current to base current:

$$\beta = h_{FE} = \frac{I_C}{I_B}$$

Its practical job is to tell you the **minimum base current** you must supply to support the collector current you want:

$$I_B \ge \frac{I_C}{\beta_{min}}$$

Read that as: "to push $I_C$ through the part, the base must be fed at least $I_C/\beta$." The trap is which $\beta$ you trust. $h_{FE}$ on a datasheet is given as a *range* (e.g. min 100, typ 200) and **swings with collector current, with $V_{CE}$, and with temperature** — it is not a constant. For a *switch* you must use the **minimum guaranteed $\beta$**, then deliberately supply 2–10× more base current than the bare minimum (the "overdrive factor" or "forced beta") so the part slams fully into saturation despite the spread. For a *linear amplifier* you bias around the typical $\beta$ but design the surrounding network so the gain doesn't depend on it. Either way, the rule is: **never trust a single $\beta$ number.**

</details>

<details>
<summary><strong>The Key Tension</strong> — Survival fences vs. design inputs, and where they fight</summary>

The five specs pull against each other; choosing a BJT is balancing them.

| Spec | What raising it costs you | The tension |
|------|---------------------------|-------------|
| **$V_{CEO}$** | Higher-voltage parts often have **lower $\beta$** and higher $V_{CE(sat)}$ | Voltage headroom vs. gain/efficiency |
| **$I_C$** | Bigger die / package, costs more, $\beta$ often falls at high $I_C$ | Current capacity vs. gain at the top end |
| **$P_C$** | Bigger package or a heatsink — board area, cost | Heat capacity vs. size/cost |
| **$\beta$** | High-$\beta$ parts trade off voltage and ruggedness | Easy drive vs. robustness |

**The central design tension is saturation vs. speed vs. drive.** Overdriving the base (forced $\beta$ much smaller than the rated $\beta$) guarantees a low $V_{CE(sat)}$ — which *minimizes* $P_C$ heating — but stuffing the base full of charge makes the transistor **slow to turn off** (stored charge has to drain out, the "storage time"). So: more base drive → lower conduction loss but slower switching. This exact tradeoff is one reason [[quick-context/transistor|MOSFETs]] displaced BJTs for high-speed switching — a [[micro-context/mosfet|MOSFET]] gate is a [[quick-context/capacitor|capacitor]], not a current-hungry, charge-storing junction.

```
PICKING THE PART — the decision order
======================================================

  V_CC ──────────────────►  need V_CEO > V_CC  (x2 if inductive)
  I_load ────────────────►  need I_C   > I_load (with derating)
  worst-case V_CE x I_C ─►  need P_C   > that  (after temp derating)
  drive available ───────►  check I_B = I_load / beta_min is suppliable
                            then over-drive 2-10x for clean saturation
```

</details>

<details>
<summary><strong>Concrete Example</strong> — Reading the 2N2222 spec line for a 0.3 A relay driver</summary>

You want a generic small NPN to switch a 12 V, 300 mA relay from a 3.3 V microcontroller pin. You grab a **2N2222A** (a classic jellybean NPN) and check the five numbers against the circuit.

```
PN2222A / TO-92 plastic  (ON Semi limits)  YOUR CIRCUIT NEEDS
-----------------------------------        ----------------------------------
  Type     : NPN                           NPN (emitter to GND, high-side load) OK
  V_CEO    : 40 V                          V_CC = 12 V  ->  40 > 12  OK (3.3x margin)
  I_C      : 600 mA (continuous)           I_load = 300 mA  ->  600 > 300  OK
  P_C      : 625 mW @ 25C (TO-92)          see calc below
  h_FE     : 100 (min @ I_C=150mA) ... 300 use 100 (min) for the switch
```

> **Watch the variant.** These are the values for the **TO-92 plastic PN2222A**. The original **metal-can TO-18 "2N2222A"** differs — typically $I_C = 800$ mA and $P_D = 500$ mW (it sheds heat differently). Same family name, different limits: always read the *specific* datasheet for the package you're [[quick-context/soldering|soldering]]. Also note $h_{FE,min}=100$ is quoted at a test current of $I_C = 150$ mA; the guaranteed minimum *falls* at higher $I_C$ (e.g. ≥40 at 500 mA) — another reason to overdrive the base.

**Step 1 — Voltage fence.** Off-state, the relay coil pulls the collector to ~12 V, so $V_{CE}\approx 12$ V $< 40$ V $V_{CEO}$. Plus margin for the coil's inductive turn-off spike → add a flyback diode and you're safe. PASS.

**Step 2 — Current fence.** $I_C = 300$ mA $< 600$ mA rating. PASS (but only 2× margin — fine for a relay, derate harder for continuous loads).

**Step 3 — Power / heat fence.** Drive it into saturation so $V_{CE(sat)}\approx 0.3$ V:

$$P = V_{CE(sat)} \cdot I_C = 0.3\,\text{V} \times 0.3\,\text{A} = 0.09\,\text{W} = 90\,\text{mW}$$

That's well under the 625 mW rating (even derated to ~300 mW in a warm enclosure). PASS. *Note the contrast:* if the part were stuck half-on at $V_{CE}=6$ V, $P = 6\times0.3 = 1.8$ W — **3× over the rating, instant failure.** Saturation is what saves it.

**Step 4 — Base current (design input).** Minimum base current to support 300 mA at the worst-case (minimum) gain:

$$I_{B,min} = \frac{I_C}{\beta_{min}} = \frac{300\,\text{mA}}{100} = 3\,\text{mA}$$

Overdrive 3× for crisp saturation → design for $I_B = 9$ mA. Size the [[quick-context/resistor|base resistor]]:

$$R_B = \frac{V_{pin} - V_{BE}}{I_B} = \frac{3.3\,\text{V} - 0.7\,\text{V}}{9\,\text{mA}} = 289\,\Omega \rightarrow \text{use } 270\,\Omega$$

Check the pin can source 9 mA (most MCU pins do ~20 mA). Done — all five specs verified, part is safe.

**The one thing most outsiders get wrong about this is** assuming the $h_{FE}$ printed on the datasheet (or measured by a cheap component tester) is *the* gain. It isn't — it's one point on a curve that slides with current and temperature, and the *typical* value is meaningless for a switch. Always design switches around the **minimum guaranteed** $h_{FE}$ and then overdrive the base. The runner-up mistake is forgetting that $P_C$ is a *temperature-derated* number, not a fixed one — "625 mW" is a 25 °C lab value, not what you get inside a hot enclosure.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[quick-context/bjt]]** — The companion note: the physics (NPN/PNP structure, the three operating regions, why the base is thin). Read it to understand *why* these specs exist; read this note to *use* them.
- **[[quick-context/power-watts-joules]]** — $P_C$ is just $P = V \cdot I$ applied to the transistor, plus thermal resistance ($R_{\theta JA}$) deciding how fast that heat escapes. The heat ceiling is really a thermal problem.
- **[[quick-context/resistor]]** — The base resistor sets $I_B$ from $\beta$; it is the component that turns the gain spec into an actual circuit value.
- **[[quick-context/transistor]]** — The MOSFET sibling. Its spec sheet swaps $\beta$/$I_B$ for $V_{GS(th)}$ and $R_{DS(on)}$, and its "$V_{CEO}$" equivalent is $V_{DS(max)}$ — the survival-fence logic is identical.
- **[[quick-context/diode]]** — A flyback/freewheeling diode protects the BJT from inductive spikes that would otherwise blow past $V_{CEO}$.
- **[[quick-context/comparator-specification]]** — The same "read-the-datasheet-before-you-trust-it" discipline applied to a [[quick-context/comparator|comparator]] IC (absolute-max vs. guaranteed limits, typical vs. boldface).

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** Your supply is 24 V. A transistor lists $V_{CEO} = 30$ V. Is that a safe pick, and what would change your answer?
<details>
<summary>Answer</summary>
Marginal. $30 > 24$, so on paper it survives the steady off-state (See: *How It Works → $V_{CEO}$*). But the margin is only 1.25×, and if the load is **inductive** (motor, relay, solenoid) the turn-off spike can momentarily blow far past 24 V and exceed 30 V, destroying the part. You'd want $V_{CEO}\ge \sim 2\times V_{CC}$ (≥48 V here) *and* a flyback diode. For a purely resistive load it's acceptable but tight.
</details>

**Q2:** A datasheet says $h_{FE} = 200$. Your collector current is 100 mA. How much base current do you supply for a reliable *switch*?
<details>
<summary>Answer</summary>
**Not $100\text{mA}/200 = 0.5$ mA.** That uses the *typical* gain, which you must never trust for a switch. Use the **minimum guaranteed** $h_{FE}$ (say 100): $I_{B,min} = 100\text{mA}/100 = 1$ mA. Then **overdrive** 2–10× to force hard saturation → supply ~3–5 mA. (See: *How It Works → $\beta$ / $h_{FE}$*.)
</details>

**Q3:** Two identical loads (12 V, 0.2 A). In circuit A the BJT is saturated ($V_{CE}=0.2$ V); in circuit B it's stuck half-on ($V_{CE}=6$ V). Both transistors are rated $P_C = 625$ mW. Which one fails, and why does it connect the $P_C$ and $\beta$ specs?
<details>
<summary>Answer</summary>
**B fails.** A: $P = 0.2\times0.2 = 40$ mW (safe). B: $P = 6\times0.2 = 1.2$ W ≈ 2× over the 625 mW limit → overheats. The link to $\beta$: circuit B is half-on precisely *because* its base was under-driven (not enough $I_B$ to reach saturation). So a $\beta$/base-current mistake shows up as a $P_C$ (thermal) failure. Adequate base overdrive keeps $V_{CE}$ tiny, which keeps $P=V_{CE}I_C$ small. (See: *How It Works → $P_C$*.)
</details>

**Q4:** What's wrong with the claim "NPN transistors turn on at a lower voltage than PNP, so they're more efficient"?
<details>
<summary>Answer</summary>
The premise is false. **Both** NPN and PNP need roughly the same ~0.6–0.7 V across the base–emitter junction to conduct — NPN does *not* turn on at a lower voltage. NPN is preferred for a different reason: its carriers are **electrons**, which have ~2–3× the mobility of the **holes** that carry current in a PNP. Higher mobility → more gain, faster switching, and lower $V_{CE(sat)}$ for the same die. The advantage is carrier physics, not turn-on voltage. (See: *How It Works → Type*.)
</details>

**Q5:** A part's $P_C$ is "625 mW." You calculate your transistor dissipates 400 mW and conclude it's safe. Under what realistic condition is that conclusion wrong?
<details>
<summary>Answer</summary>
When the part runs **hot**. The 625 mW is quoted at a reference temperature (typically 25 °C). $P_C$ **derates linearly** as ambient/case temperature rises: $P_{max} = (T_{j,max}-T_{amb})/R_{\theta JA}$. Inside a warm enclosure at, say, 60 °C, that small TO-92 might only safely dissipate ~350–400 mW — so your 400 mW is now *at or over* the real limit. Always check the derating curve, not just the headline number. (See: *How It Works → $P_C$ → Thermal derating*.) This is the same "typical ≠ guaranteed across temperature" trap as in [[quick-context/comparator-specification|comparator specs]].
</details>

</details>
