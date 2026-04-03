---
case: Relativity, Back-EMF, and the Faraday Tensor
components: [faraday-tensor, electromagnetism, lenzs-law, self-induction]
created: 2026-02-20
---

# Case: Relativity, Back-EMF, and the Faraday Tensor

> **Components:** [[quick-context/faraday-tensor]] | [[quick-context/electromagnetism]] | [[quick-context/lenzs-law]] | [[quick-context/self-induction]]
> **Micro-context:** [[micro-context/electromagnetic-induction]] | [[micro-context/ac-dc-current]]

> **In brief:** From a stationary reference frame, what we call the "magnetic field" around a current-carrying wire is actually the [[quick-context/voltage|electric field]] transformed by special relativity—length contraction makes the wire appear charged. When the magnetic field changes, Faraday's Law creates an electric field that opposes the change (back-EMF). The [[quick-context/faraday-tensor|Faraday tensor]] packages both phenomena into one mathematical object, revealing that $\vec{E}$ and $\vec{B}$ are two faces of a single electromagnetic field.

## The Situation

You've learned that [[quick-context/electric-current|current]] creates magnetic fields, and changing magnetic fields create [[quick-context/voltage|voltages]]. But *why*? These seem like separate rules memorized from a textbook. The deeper truth: both are consequences of one unified electromagnetic field. Special relativity explains why a magnetic field appears when charges move, and Faraday's Law explains why changing magnetic fields create electric fields. The Faraday tensor makes this unity mathematically precise.

## The Pieces

**Electric field ($\vec{E}$):** A force field created by charges. Acts on any charge, moving or stationary. Can do work on charges (transfer energy). See [[quick-context/electric-magnetic-field-unification]].

**Magnetic field ($\vec{B}$):** A force field created by *moving* charges. Only acts on *moving* charges, and the force is perpendicular to velocity (so it deflects but can't speed up or slow down). See [[quick-context/electromagnetism]].

**Length contraction:** In special relativity, objects moving relative to you appear shorter in the direction of motion by factor $\gamma = 1/\sqrt{1 - v^2/c^2}$. At everyday speeds this is tiny, but it's enough to explain magnetism.

**Faraday's Law:** A changing magnetic flux induces an EMF: $\mathcal{E} = -N \times d\Phi/dt$. The minus sign ([[quick-context/lenzs-law|Lenz's Law]]) means the induced EMF opposes the change. See [[quick-context/self-induction]] for how this creates back-EMF.

**Faraday tensor ($F^{\mu\nu}$):** A 4×4 antisymmetric matrix that packages $\vec{E}$ and $\vec{B}$ into one object. When you change reference frames (Lorentz transformation), the tensor components mix $E$ and $B$ automatically. See [[quick-context/faraday-tensor]] for the full treatment.

## Step by Step: What Happens

### Step 1: A Current-Carrying Wire (Lab Frame)

Start with a simple wire carrying current. From the lab's perspective:

```
LAB FRAME: Wire at rest, electrons moving
══════════════════════════════════════════════════════════════════════════════

    The wire contains:
    • Positive ions (protons in metal lattice) — STATIONARY
    • Free electrons — MOVING to the right (current flows left by convention)

         ← ← ← ← ← ← ← ← ← ← I (conventional current direction)

    ─────────────────────────────────────────────────────────────────
    ⊕   ⊕   ⊕   ⊕   ⊕   ⊕   ⊕   ⊕   ⊕   ⊕   ⊕   ⊕   ⊕   ⊕   ⊕   ⊕
    ─────────────────────────────────────────────────────────────────
        →e⁻ →e⁻ →e⁻ →e⁻ →e⁻ →e⁻ →e⁻ →e⁻ →e⁻ →e⁻ →e⁻ →e⁻

    In the lab frame:
    • Equal number of + and - charges per unit length
    • Wire is electrically NEUTRAL
    • No electric field radially outward

    BUT: electrons are moving → magnetic field circles the wire!

                     ↑ B
                ┌────┼────┐
            B ← │    ⊗    │ → B         (current into page at this cross-section)
                └────┼────┘
                     ↓ B

    A stationary test charge nearby feels NO force (no E, and B only acts on moving charges).
    A moving test charge feels a magnetic force F = qv × B.
```

**Question:** Where does this magnetic field come from? The electrons are just moving charges. There's no "magnetism" source inside them.

### Step 2: Switch to Electron's Rest Frame

Now imagine you're moving with the electrons (at drift velocity $v$). In YOUR frame:

```
ELECTRON'S REST FRAME: Electrons stationary, protons moving
══════════════════════════════════════════════════════════════════════════════

    In this frame:
    • Electrons are STATIONARY (you're moving with them)
    • Protons are moving LEFT (opposite to your motion)

    ─────────────────────────────────────────────────────────────────
        e⁻    e⁻    e⁻    e⁻    e⁻    e⁻    e⁻    e⁻    e⁻    e⁻
    ─────────────────────────────────────────────────────────────────
    ← ⊕ ← ⊕ ← ⊕ ← ⊕ ← ⊕ ← ⊕ ← ⊕ ← ⊕ ← ⊕ ← ⊕ ← ⊕ ← ⊕ ← ⊕ ← ⊕
                     protons moving left

    LENGTH CONTRACTION changes the game:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    In the lab frame, the spacing between protons is d_p.
    In the lab frame, the spacing between electrons is d_e.
    In the lab frame, d_p = d_e (wire is neutral).

    But in YOUR frame (moving with electrons):
    • Electrons are at rest → their spacing is d_e (unchanged)
    • Protons are moving → their spacing appears CONTRACTED: d'_p = d_p/γ < d_p

    ─────────────────────────────────────────────────────────────────
        e⁻    e⁻    e⁻    e⁻    e⁻    e⁻    e⁻    e⁻    e⁻    e⁻
    ─────────────────────────────────────────────────────────────────
      ←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕←⊕
                     ↑
                     MORE protons per unit length!

    The wire now has NET POSITIVE CHARGE in this frame!
    Net positive charge → radial ELECTRIC FIELD pointing outward!

    ┌────────────────────────────────────────────────────────────────────────┐
    │  NOTE: This is the "Purcell explanation"—a pedagogical simplification. │
    │  The full treatment must account for both contractions and expansions │
    │  of charge spacings when transforming frames. The qualitative insight │
    │  (charge imbalance creates E field) is correct; the detailed math is  │
    │  more subtle. See Purcell's "Electricity and Magnetism" for rigor.    │
    └────────────────────────────────────────────────────────────────────────┘

                     ↑ E
                ┌────┼────┐
            E ← │    ⊕    │ → E         (net positive = outward E field)
                └────┼────┘
                     ↓ E
```

### Step 3: Same Physics, Different Description

Both observers agree on the force experienced by a test charge. But they explain it differently:

```
THE SAME FORCE, TWO DESCRIPTIONS
══════════════════════════════════════════════════════════════════════════════

    Consider a positive test charge moving with the electrons (to the right):

    LAB FRAME (test charge moving):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        Wire is neutral → E = 0
        Test charge is moving → experiences magnetic force

        F = qv × B  (force toward wire, perpendicular to v and B)

                          Wire
        ─────────────────────────────────────────────
                           │
                      F ←──⊕──→ v (moving right)
                           │
                     Test charge

        "The magnetic field deflects the moving charge toward the wire."


    ELECTRON FRAME (test charge at rest):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        Wire has net positive charge → E ≠ 0 (points toward wire)
        Test charge is stationary → no magnetic force possible

        F = qE  (force toward wire, attracted to + charge)

                          Wire (+)
        ─────────────────────────────────────────────
                           │
                      F ←──⊕     (at rest)
                           │
                     Test charge

        "The electric field attracts the stationary charge toward the wire."


    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │   BOTH frames predict the SAME force magnitude and direction.          │
    │                                                                        │
    │   Lab frame:     F = qvB      (magnetic)                              │
    │   Moving frame:  F = qE       (electric)                              │
    │                                                                        │
    │   The physics is identical. Only the description changes.              │
    │   Magnetism is "relativistic electricity."                            │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘
```

### Step 4: How the Faraday Tensor Captures This

The Faraday tensor $F^{\mu\nu}$ is a 4×4 matrix containing all six components of $\vec{E}$ and $\vec{B}$:

```
THE FARADAY TENSOR — E and B as One Object
══════════════════════════════════════════════════════════════════════════════

                    ν = 0       ν = 1       ν = 2       ν = 3
                   (time)       (x)         (y)         (z)
                ┌─────────────────────────────────────────────────┐
    μ = 0 (t)   │     0         E_x         E_y         E_z      │
                │                                                 │
    μ = 1 (x)   │   -E_x         0          B_z        -B_y      │
                │                                                 │
    μ = 2 (y)   │   -E_y       -B_z          0          B_x      │
                │                                                 │
    μ = 3 (z)   │   -E_z        B_y        -B_x          0       │
                └─────────────────────────────────────────────────┘

    Key insight:
    • E components fill the first row/column (time-space)
    • B components fill the spatial block (space-space)
    • Antisymmetric: F^μν = -F^νμ

    Under a Lorentz boost (change of reference frame):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    The tensor transforms as: F'^μν = Λ^μ_ρ Λ^ν_σ F^ρσ

    In plain terms:
    • E'_y = γ(E_y - vB_z)       ← E and B mix together!
    • B'_z = γ(B_z - vE_y/c²)   ← B picks up contributions from E!

    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │   What one observer calls a "magnetic field,"                         │
    │   another moving observer calls (partly) an "electric field."         │
    │                                                                        │
    │   The tensor automatically handles this mixing.                       │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘
```

### Step 5: Changing B Creates E (Back-EMF)

Now consider what happens when the magnetic field *changes*. This is Faraday's Law:

```
FARADAY'S LAW: Changing Magnetic Flux Creates Electric Field
══════════════════════════════════════════════════════════════════════════════

    A changing magnetic field induces a circulating electric field:

        ∇ × E = -∂B/∂t    (one of Maxwell's equations)

    In words: "A time-varying B creates a curling E."


    EXAMPLE: Inductor with changing current
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Current is increasing → magnetic field is building:

         ┌────────⊃⊃⊃⊃⊃⊃────────────╱╱╱╱╱─────┐
         │           L                 R       │
      Vs │                                     │
         │     I increasing →                  │
         │                                     │
         └─────────────────────────────────────┘
                    ║║║║║║
                    B (increasing)

    Inside the coil:
    • dI/dt > 0 → dB/dt > 0 (field strengthening)
    • By Faraday's Law: changing B creates a circulating E field
    • This E field opposes the current increase (Lenz's Law)
    • We measure this as back-EMF: V_L = -L × dI/dt

    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │   THE INDUCED ELECTRIC FIELD IS REAL                                  │
    │                                                                        │
    │   It's not the electrostatic E from charges.                          │
    │   It's a new E created by the time-varying B.                         │
    │   This E circulates in loops (no beginning or end).                   │
    │   It's what pushes back against the current change.                   │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘


    WHERE DOES THE ENERGY GO?
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    While current increases:
    • Source does work against the back-EMF
    • This work becomes energy stored in the magnetic field: E = ½LI²

    When current tries to decrease:
    • Changing B creates E that maintains current (opposes decrease)
    • Stored magnetic energy converts back to electrical energy
    • If no path exists, huge voltage spike (see [[quick-context/self-induction]])
```

### Step 6: The Tensor Perspective on Faraday's Law

Maxwell's four equations become just two tensor equations:

```
MAXWELL'S EQUATIONS IN TENSOR FORM
══════════════════════════════════════════════════════════════════════════════

    Classical (4 equations):              Tensor (2 equations):
    ━━━━━━━━━━━━━━━━━━━━━                 ━━━━━━━━━━━━━━━━━━━━━━

    ∇ · E = ρ/ε₀                ┐
                                ├───→    ∂_μ F^μν = μ₀ J^ν
    ∇ × B = μ₀J + μ₀ε₀ ∂E/∂t   ┘

    ∇ · B = 0                   ┐
                                ├───→    ∂_μ F̃^μν = 0
    ∇ × E = -∂B/∂t              ┘


    Faraday's Law (∇ × E = -∂B/∂t) is contained in the second tensor equation!

    ┌────────────────────────────────────────────────────────────────────────┐
    │                                                                        │
    │   The tensor formulation shows E and B are aspects of ONE field.       │
    │                                                                        │
    │   • A static charge creates F^0i components (electric field)          │
    │   • A moving charge creates F^ij components (magnetic field)          │
    │   • A changing F^ij (B) induces changes in F^0i (E)                   │
    │                                                                        │
    │   It's all one unified electromagnetic field F^μν.                    │
    │                                                                        │
    └────────────────────────────────────────────────────────────────────────┘
```

## The Result

Both phenomena—magnetism from moving charges and EMF from changing fields—are unified:

```
THE COMPLETE PICTURE
══════════════════════════════════════════════════════════════════════════════

    PHENOMENON 1: Magnetism from Current
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    • In lab frame: moving electrons create B field
    • In electron frame: length contraction creates charge imbalance → E field
    • Both are correct! The Faraday tensor mixes E and B under boosts.

    PHENOMENON 2: Back-EMF from Changing Current
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    • Changing current → changing B field
    • Changing B induces circulating E field (Faraday's Law)
    • This E opposes the current change (Lenz's Law)
    • We measure it as back-EMF: V = -L × dI/dt


    THE UNITY (Faraday Tensor):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

              ┌──────────────────────────────────────────┐
              │                                          │
              │   Electric and Magnetic fields are       │
              │   COMPONENTS of one tensor F^μν          │
              │                                          │
              │   • Space-time components → E field      │
              │   • Space-space components → B field     │
              │                                          │
              │   Frame change mixes them automatically. │
              │   Time change of one creates the other.  │
              │                                          │
              │   They were never separate.              │
              │                                          │
              └──────────────────────────────────────────┘
```

## Why Each Piece Matters

- **Length contraction:** Without relativity, there's no explanation for why moving charges create magnetic fields. The charge density transformation is the *reason* for magnetism.

- **Faraday's Law:** Without it, changing magnetic fields would have no effect. The fact that $\nabla \times E = -\partial B/\partial t$ is what makes inductors, generators, and transformers work.

- **Lenz's Law (the minus sign):** Without opposition, energy wouldn't be conserved. The minus sign ensures you must do work to change the field, and that work goes into stored energy.

- **The Faraday Tensor:** Without it, E and B seem like separate things with mysterious connections. The tensor shows they're one object, explaining both frame transformations and time evolution in a unified framework.

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/electromagnetic-induction]] — Faraday's Law in brief: changing flux induces EMF
- [[micro-context/ac-dc-current]] — AC vs DC and why transformers need changing current

**Full treatment (10 minutes):**
- [[quick-context/faraday-tensor]] — Complete treatment of the tensor, Lorentz transformations, and invariants
- [[quick-context/electric-magnetic-field-unification]] — Physical intuition for why E and B are unified
- [[quick-context/electromagnetism]] — Maxwell's equations and electromagnetic waves
- [[quick-context/lenzs-law]] — Why the minus sign matters and what happens without it
- [[quick-context/self-induction]] — Complete walkthrough of inductor voltage and back-EMF
- [[quick-context/coil-magnetic-field]] — How current through a coil creates the B field in the first place
