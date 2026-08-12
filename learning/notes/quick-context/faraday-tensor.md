---
topic: Faraday Tensor
created: 2026-02-20
---

# Faraday Tensor

> **Related:** [[learning/notes/quick-context/tensor]] | [[learning/notes/quick-context/coil-magnetic-field]] | [[learning/notes/quick-context/voltage]] | [[learning/notes/quick-context/inductor]] | [[learning/notes/quick-context/capacitor]]

> **TL;DR:** The Faraday [[learning/notes/quick-context/tensor|tensor]] (or electromagnetic field tensor) is a 4×4 antisymmetric matrix that packages the electric field **E** and magnetic field **B** into a single mathematical object, revealing that they are not separate phenomena but two aspects of one unified electromagnetic field that transforms together under special relativity—what one observer sees as a pure electric field, another moving observer may see as a mix of electric and magnetic fields.

## The Core Problem: E and B Transform Weirdly

When you learn [[learning/notes/quick-context/electromagnetism|electromagnetism]], electric and magnetic fields seem like distinct things: **E** pushes charges regardless of their motion, **B** only affects moving charges. But there's a puzzle: a stationary charge next to a current-carrying wire sees a magnetic field (from the moving electrons). If you run alongside those electrons at the same speed, you now see stationary charges—and stationary charges don't create magnetic fields. Where did the B field go? The answer is that from your moving reference frame, what was a magnetic field now appears as an electric field. E and B aren't separate—they're components of a single entity that rotates into each other when you change velocity. The Faraday tensor is the mathematical object that captures this unity.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Faraday Tensor ($F^{\mu\nu}$)** | A rank-2 antisymmetric tensor encoding both **E** and **B** fields in a 4×4 matrix. The indices μ and ν run from 0 to 3 (time and three spatial dimensions). Antisymmetric means $F^{\mu\nu} = -F^{\nu\mu}$. |
| **Four-Vector** | A quantity with four components (one time, three space) that transforms properly under Lorentz transformations. Examples: position $(ct, x, y, z)$, momentum $(E/c, p_x, p_y, p_z)$, current density $(c\rho, J_x, J_y, J_z)$. |
| **Lorentz Transformation** | The rules for converting measurements between reference frames moving relative to each other at constant velocity. Length contracts, time dilates, and the Faraday tensor components mix together. |
| **Dual Tensor ($\tilde{F}^{\mu\nu}$)** | The "partner" tensor obtained by swapping E and B (with sign changes): where $F$ has E components, $\tilde{F}$ has B, and vice versa. Used to write the other half of [[learning/notes/quick-context/maxwell-equations|Maxwell's equations]]. |
| **Covariant** | A formulation that takes the same mathematical form in all inertial reference frames. The Faraday tensor makes [[learning/notes/quick-context/electromagnetism|electromagnetism]] manifestly covariant—you write the equations once, and they automatically work in any frame. |

<details>
<summary><strong>How It Works</strong> — Packaging E and B into one object</summary>

## The Electric and Magnetic Fields as Tensor Components

In three-dimensional physics, we have two vector fields: **E** = $(E_x, E_y, E_z)$ and **B** = $(B_x, B_y, B_z)$—six independent components total. The Faraday tensor packages all six into a 4×4 matrix:

```
THE FARADAY TENSOR — Structure and Components
══════════════════════════════════════════════════════════════════════════════

    The electromagnetic field tensor F^μν is a 4×4 antisymmetric matrix.
    Antisymmetric means: F^μν = -F^νμ (diagonal is zero, upper and lower
    triangles are negatives of each other).

    Using units where c = 1 for clarity:

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

    Note the pattern:
    • First row/column: Electric field components E_x, E_y, E_z
    • 3×3 spatial block: Magnetic field components (as antisymmetric matrix)


    THE SIGN CONVENTION:
    ────────────────────────────────────────────────────────────────────────────

    F^0i =  E_i     (time-space components = electric field)
    F^ij = ε_ijk B_k  (space-space components = magnetic field)

    Where ε_ijk is the Levi-Civita symbol (±1 for cyclic/anticyclic, 0 otherwise)


    WHY ANTISYMMETRIC?
    ────────────────────────────────────────────────────────────────────────────

    A 4×4 antisymmetric matrix has:
    • Diagonal: 4 zeros (forced by antisymmetry: F^μμ = -F^μμ → F^μμ = 0)
    • Off-diagonal: 16 - 4 = 12 entries, but antisymmetry pairs them
    • Independent components: 12/2 = 6

    Exactly enough to hold 3 E-components + 3 B-components!

    This isn't a coincidence—it's deep geometry. The electromagnetic field
    is naturally a 2-form in 4D spacetime, which has exactly 6 independent
    components (the number of ways to choose 2 directions from 4).
```

## Why the Tensor Form Matters: Lorentz Transformations

The power of the tensor formulation becomes clear when you change reference frames. Under a Lorentz transformation (boost), the Faraday tensor transforms according to standard tensor rules:

```
HOW E AND B MIX UNDER BOOSTS
══════════════════════════════════════════════════════════════════════════════

Consider a reference frame S' moving at velocity v along the x-axis
relative to frame S.

TRANSFORMATION RULES (to first order in v/c for intuition):
────────────────────────────────────────────────────────────────────────────

    E'_x = E_x                    B'_x = B_x

    E'_y = γ(E_y - vB_z)          B'_y = γ(B_y + vE_z/c²)

    E'_z = γ(E_z + vB_y)          B'_z = γ(B_z - vE_y/c²)

    Where γ = 1/√(1 - v²/c²) ≈ 1 for slow speeds


THE KEY INSIGHT:
────────────────────────────────────────────────────────────────────────────

    E and B components MIX together!

    • E_y in frame S becomes a combination of E_y AND B_z in frame S'
    • B_z in frame S becomes a combination of B_z AND E_y in frame S'

    What you call "electric" and what you call "magnetic" depends on
    your velocity.


EXAMPLE: A Moving Charge Near a Wire
────────────────────────────────────────────────────────────────────────────

    In the lab frame (wire stationary):

         Wire: - - - - - - - - -  ← electrons flowing left (current I)
               + + + + + + + + +  ← protons stationary

                    ⊕ ← positive test charge at rest

    • Wire is electrically neutral (equal + and - charges)
    • Wire creates magnetic field B (from current)
    • Stationary test charge feels NO force (B only affects moving charges)
    • E = 0, B ≠ 0


    In the electron's rest frame (moving right with electrons):

         Wire: - - - - - - - - -  ← electrons now stationary
               + + + + + + + +    ← protons moving right (length contracted!)
                    ↑
               Protons appear DENSER due to length contraction

                    ⊕ ← test charge now moving right

    • More protons per length than electrons → net POSITIVE charge!
    • Wire now creates an electric field E pointing toward wire
    • Test charge feels force toward wire (attraction to + charge)
    • E ≠ 0, B = different


    SAME PHYSICS, DIFFERENT DESCRIPTION:
    ────────────────────────────────────────────────────────────────────────────

    Lab frame:    F = qv × B     (magnetic force from B on moving charge)
    Moving frame: F = qE         (electric force from E on charge)

    The FORCE is the same. The DESCRIPTION changes.
    The Faraday tensor transforms correctly to give the same physics.
```

## Maxwell's Equations in Tensor Form

The four Maxwell equations compress into just two tensor equations:

```
[[learning/notes/quick-context/maxwell-equations|MAXWELL'S EQUATIONS]] — From Four to Two
══════════════════════════════════════════════════════════════════════════════

CLASSICAL FORM (in 3D vectors):
────────────────────────────────────────────────────────────────────────────

    1. ∇ · E = ρ/ε₀                (Gauss's law for E)
    2. ∇ · B = 0                   (Gauss's law for B — no monopoles)
    3. ∇ × E = -∂B/∂t              (Faraday's law)
    4. ∇ × B = μ₀J + μ₀ε₀ ∂E/∂t   (Ampère-Maxwell law)


TENSOR FORM (in 4D spacetime):
────────────────────────────────────────────────────────────────────────────

    ∂_μ F^μν = μ₀ J^ν             ← Contains equations 1 and 4

    ∂_μ F̃^μν = 0                  ← Contains equations 2 and 3


    That's it. Two equations capture all of electromagnetism.


WHAT THE TENSOR EQUATIONS MEAN:
────────────────────────────────────────────────────────────────────────────

    ∂_μ F^μν = μ₀ J^ν
    ─────────────────

    • Left side: Divergence of the field tensor (how field "spreads")
    • Right side: Current 4-vector J^ν = (cρ, J_x, J_y, J_z)
    • ν = 0 component: gives Gauss's law (charges are sources of E)
    • ν = 1,2,3 components: give Ampère-Maxwell law (currents create B)


    ∂_μ F̃^μν = 0  (using the dual tensor)
    ──────────────

    • Says "no magnetic monopoles" and "Faraday's law"
    • The dual tensor swaps E ↔ B (with sign changes)
    • ν = 0: ∇ · B = 0 (no magnetic charges)
    • ν = 1,2,3: ∇ × E = -∂B/∂t (changing B creates E)


WHY THIS MATTERS:
────────────────────────────────────────────────────────────────────────────

    These tensor equations are "manifestly covariant":

    • They look the same in EVERY inertial reference frame
    • No need to transform and check—the form guarantees it
    • The physics of electromagnetism is frame-independent

    This is what Einstein realized: Maxwell's equations were already
    relativistic. It was Newtonian mechanics that needed fixing.
```

</details>

<details>
<summary><strong>The Key Tension</strong> — Mathematical elegance vs. physical intuition</summary>

## The Tensor Hides the Fields; the Fields Hide the Unity

There's a pedagogical tension in how to teach electromagnetism:

```
TWO WAYS TO UNDERSTAND ELECTROMAGNETISM
══════════════════════════════════════════════════════════════════════════════

APPROACH 1: SEPARATE E AND B (classical, intuitive)
────────────────────────────────────────────────────────────────────────────

    ┌──────────────────────────────────────────────────────────────────────┐
    │                                                                      │
    │   ELECTRIC FIELD (E)              MAGNETIC FIELD (B)                │
    │   ────────────────                ──────────────────                │
    │                                                                      │
    │   Created by charges              Created by currents               │
    │   (stationary or moving)          (moving charges)                  │
    │                                                                      │
    │   Acts on ANY charge              Only acts on MOVING charges       │
    │   F = qE                          F = qv × B                        │
    │                                                                      │
    │   Can do work                     Cannot do work (F ⊥ v)            │
    │   (energy transfer)               (only deflects)                   │
    │                                                                      │
    │   Stored in capacitors            Stored in inductors               │
    │                                                                      │
    └──────────────────────────────────────────────────────────────────────┘

    Pros: Intuitive, practical for engineering, matches lab experience
    Cons: Hides the relativistic unity, makes transformations complex


APPROACH 2: UNIFIED FARADAY TENSOR (relativistic, elegant)
────────────────────────────────────────────────────────────────────────────

    ┌──────────────────────────────────────────────────────────────────────┐
    │                                                                      │
    │   ELECTROMAGNETIC FIELD (F^μν)                                      │
    │   ────────────────────────────                                      │
    │                                                                      │
    │   Single unified field in spacetime                                 │
    │   E and B are just components (like x and y of a vector)            │
    │                                                                      │
    │   Different observers see different E/B mixtures                    │
    │   But they all agree on invariants like B² - E²/c²                  │
    │                                                                      │
    │   Two tensor equations replace four Maxwell equations               │
    │   Manifest Lorentz covariance                                       │
    │                                                                      │
    └──────────────────────────────────────────────────────────────────────┘

    Pros: Relativistically correct, mathematically compact, reveals unity
    Cons: Abstract, requires tensor calculus, hides intuitive pictures
```

| When to Use | E/B Separate | Faraday Tensor |
|-------------|--------------|----------------|
| Circuit design | Better | Overkill |
| [[quick-context/inductor\|Inductor]]/[[quick-context/capacitor\|capacitor]] analysis | Better | Overkill |
| High-velocity particles | Works but messy | Natural |
| Particle physics | Awkward | Required |
| General relativity + EM | Impossible | Required |
| Building physical intuition | Better | Abstract |

The deepest understanding comes from knowing both perspectives and switching between them as needed.

</details>

<details>
<summary><strong>Concrete Example</strong> — The invariants of the electromagnetic field</summary>

## What ALL Observers Agree On

When different observers disagree about E and B values, what do they agree on? There are two Lorentz invariants constructed from the Faraday tensor:

```
ELECTROMAGNETIC INVARIANTS
══════════════════════════════════════════════════════════════════════════════

From the Faraday tensor, we can construct two quantities that are the SAME
for ALL observers, regardless of their relative motion:

FIRST INVARIANT:  B² - E²/c²  =  (1/2) F_μν F^μν
────────────────────────────────────────────────────────────────────────────

    This compares magnetic and electric field "strengths"

    If B² - E²/c² < 0:  Electric-dominated field
                        There exists a frame where B = 0 (pure electric)

    If B² - E²/c² > 0:  Magnetic-dominated field
                        There exists a frame where E = 0 (pure magnetic)

    If B² - E²/c² = 0:  Light-like field
                        E and B always perpendicular and equal magnitude
                        This is the case for electromagnetic waves!


SECOND INVARIANT:  E · B  =  (1/4) F_μν F̃^μν
────────────────────────────────────────────────────────────────────────────

    The dot product of E and B

    If E · B ≠ 0:  Fields are not perpendicular
                   No frame exists where either E or B is zero

    If E · B = 0:  Fields are perpendicular
                   A frame exists where one field vanishes
                   (which one depends on the first invariant)


EXAMPLE: Electromagnetic Wave
────────────────────────────────────────────────────────────────────────────

    For a plane wave propagating in the z-direction:

         E field (x-direction)
            ↑
            │     ╱╲
            │    ╱  ╲
            │   ╱    ╲
        ────┼──╱──────╲──────────────▶ z (propagation)
            │          ╲    ╱
            │           ╲  ╱
            │            ╲╱
            │
         ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
        B field (y-direction, 90° out of page)

    Properties:
    • E ⊥ B (perpendicular)  →  E · B = 0
    • |E| = c|B|             →  B² - E²/c² = 0

    These are the hallmarks of an electromagnetic wave.

    No matter how fast you chase the wave, you CANNOT reach a frame
    where it looks like a static E or static B field. The invariants
    forbid it!


EXAMPLE: Point Charge at Rest
────────────────────────────────────────────────────────────────────────────

    A point charge creates a radial electric field, no magnetic field:

    In rest frame of charge:
        E ≠ 0 (radial, falls as 1/r²)
        B = 0

        B² - E²/c² = -E²/c² < 0  (electric-dominated)
        E · B = 0


    In frame moving past the charge at velocity v:
        E' ≠ 0 (compressed in direction of motion)
        B' ≠ 0 (now there's a magnetic field!)

        B'² - E'²/c² = -E²/c²    (same as before!)
        E' · B' = 0              (same as before!)

    The field "looks different" but the invariants are preserved.


EXAMPLE: Current-Carrying Wire
────────────────────────────────────────────────────────────────────────────

    Lab frame (wire at rest):
        E = 0 (wire is neutral)
        B = circular field around wire

        B² - E²/c² = B² > 0  (magnetic-dominated)
        E · B = 0

    Frame moving with the electrons:
        E' ≠ 0 (wire appears charged due to length contraction!)
        B' ≠ 0 (but different value)

        B'² - E'²/c² = B²    (still magnetic-dominated, same value!)
        E' · B' = 0          (still zero!)
```

**The one thing most outsiders get wrong about this is...** thinking that since E and B transform into each other, you could boost to a frame where a magnetic field completely disappears, or where any electric field becomes purely magnetic. You can't—the invariants constrain what's possible. For electromagnetic waves, both E and B are always present in every frame (B² - E²/c² = 0 means neither dominates). For a pure electric field (B² - E²/c² < 0), you can find a frame with B = 0 but never B without E. The Faraday tensor respects these invariants under all transformations.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/quick-context/electromagnetism]]** — The classical treatment with separate E and B fields. The Faraday tensor is the relativistic packaging of these fields into a single geometric object.

- **[[learning/notes/quick-context/electric-magnetic-field-unification|Field Unification]]** — Explains from a physical perspective why moving charges create magnetic fields and why E and B are really one phenomenon. The Faraday tensor is the mathematical formalization of this unity.

- **[[learning/notes/quick-context/coil-magnetic-field]]** — The relativistic explanation section discusses how magnetism is "relativistic electricity"—what the Faraday tensor makes mathematically precise.

- **[[learning/notes/quick-context/voltage]]** — [[learning/notes/quick-context/voltage|Voltage]] is the line integral of the electric field. In tensor language, this connects to the time-space components of the Faraday tensor.

- **[[learning/notes/quick-context/electric-current]]** — Current appears in the source term (4-current $J^\mu$) of Maxwell's equations in tensor form.

- **Special Relativity** — The Lorentz transformations that mix E and B components come from special relativity. The Faraday tensor is defined to transform correctly under these transformations.

- **[[learning/notes/quick-context/tensor]]** — The general mathematical framework that the Faraday tensor is a specific instance of. Covers what tensors are, why transformation laws matter, and how rank-2 tensors like $F^{\mu\nu}$ fit into the hierarchy from scalars to higher-rank objects.

- **Differential Forms** — In advanced mathematics, the Faraday tensor is understood as a 2-form on spacetime. This explains why it has 6 independent components (ways to choose 2 dimensions from 4) and why it's antisymmetric.

- **[[learning/notes/quick-context/maxwell-equations]]** — The four classical Maxwell equations reduce to two tensor equations when written using the Faraday tensor: ∂_μ F^μν = μ₀ J^ν and ∂_μ F̃^μν = 0. This is the most compact form of classical electromagnetism.

- **General Relativity** — In curved spacetime, the Faraday tensor formulation generalizes naturally. You replace ordinary derivatives with covariant derivatives, and the formalism still works.

- **Quantum Electrodynamics (QED)** — The quantum theory of electromagnetism uses the Faraday tensor (or its potential $A^\mu$) as the fundamental field. Photons are quantized excitations of this field.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** The Faraday tensor is a 4×4 matrix, giving 16 entries. Why does it only represent 6 independent field components?
<details>
<summary>Answer</summary>
**Antisymmetry.** $F^{\mu\nu} = -F^{\nu\mu}$ forces the diagonal entries to zero (4 entries) and pairs the off-diagonal entries as negatives of each other. Of the remaining 12 off-diagonal entries, each pair contains the same information with opposite sign, leaving 6 independent components—exactly matching the 3 components of **E** and 3 components of **B**.
</details>

**Q2:** A reference frame exists where a certain electromagnetic field is purely electric (B = 0). What can you conclude about the invariants?
<details>
<summary>Answer</summary>
**B² - E²/c² < 0 and E · B = 0.** In the frame where B = 0, the first invariant equals -E²/c² < 0, so it must be negative in all frames. The second invariant E · B = 0 because B = 0. These values are the same in every frame, so any observer would find B² - E²/c² < 0 (electric-dominated) and E · B = 0 (perpendicular fields).
</details>

**Q3:** For an electromagnetic wave, B² - E²/c² = 0 and E · B = 0. Can you find a reference frame where the wave looks like a static electric or magnetic field?
<details>
<summary>Answer</summary>
**No.** B² - E²/c² = 0 means neither field dominates—if you tried to make B = 0, you'd need E = 0 too, giving no field at all. The invariants forbid finding a frame where only one field exists. This is related to the fact that electromagnetic waves travel at speed c in all frames—you cannot "catch up" to a light wave and see it at rest.
</details>

**Q4:** In classical 3D vector notation, Maxwell's equations are four separate equations. In tensor form, how many equations are there?
<details>
<summary>Answer</summary>
**Two.** The equation $\partial_\mu F^{\mu\nu} = \mu_0 J^\nu$ contains Gauss's law for E (ν=0 component) and the Ampère-Maxwell law (ν=1,2,3 components). The equation $\partial_\mu \tilde{F}^{\mu\nu} = 0$ contains Gauss's law for B and Faraday's law. The tensor formulation is more compact and manifestly covariant.
</details>

**Q5:** A stationary charge sees only an electric field from another stationary charge. If you run past this setup at high speed, will you see a magnetic field?
<details>
<summary>Answer</summary>
**Yes.** From your moving frame, the charges are moving, and moving charges create magnetic fields. The Faraday tensor transformation mixes E and B: the pure E field in the rest frame appears as E' and B' in your frame. This is the essence of why magnetism is "relativistic electricity"—it appears when you observe electric phenomena from a moving reference frame. The force on a test charge is the same in both frames, but the description (electric vs. magnetic) differs.
</details>

</details>
