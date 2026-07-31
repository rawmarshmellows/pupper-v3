---
topic: Maxwell's Equations
created: 2026-02-20
---

# Maxwell's Equations

> **Related:** [[learning/notes/quick-context/lenzs-law]] | [[learning/notes/micro-context/i2s-audio-amplifier]] | [[learning/notes/micro-context/quiescent-supply-current]] | [[learning/notes/quick-context/dipole-dipole-interactions]]

> **TL;DR:** Maxwell's equations are four mathematical statements that completely describe all classical electromagnetic phenomena—from static charges to light itself. They unify electricity and magnetism by showing that changing electric fields create magnetic fields and vice versa, enabling self-sustaining electromagnetic waves that travel at the speed of light.

## The Core Problem: Unifying Electricity and Magnetism

Before Maxwell, electricity and magnetism seemed like separate phenomena with unexplained connections. [[quick-context/electric-current|Current]] deflects compass needles (Oersted, 1820). Moving magnets induce [[quick-context/voltage|voltage]] (Faraday, 1831). But why? Maxwell's genius was realizing these connections weren't coincidental—they were manifestations of a single underlying reality. His four equations, published in 1865, showed that electric and magnetic fields are coupled: each can create the other through change. This coupling predicts electromagnetic waves that travel at exactly the measured speed of light, revealing that light *is* an electromagnetic wave. Radio, microwaves, X-rays, and gamma rays followed as predictions confirmed by experiment.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Electric Field (E)** | A vector field that exerts force on electric charges ($\mathbf{F} = q\mathbf{E}$). Created by charges and by changing magnetic fields. Measured in V/m or N/C. |
| **Magnetic Field (B)** | A vector field that exerts force on moving charges ($\mathbf{F} = q\mathbf{v} \times \mathbf{B}$). Created by [[quick-context/electric-current\|currents]] (moving charges) and by changing electric fields. Measured in tesla (T). |
| **Electric Flux ($\Phi_E$)** | The "amount" of electric field passing through a surface: $\Phi_E = \int \mathbf{E} \cdot d\mathbf{A}$. Gauss's law relates total flux to enclosed charge. |
| **Magnetic Flux ($\Phi_B$)** | The "amount" of magnetic field passing through a surface: $\Phi_B = \int \mathbf{B} \cdot d\mathbf{A}$. Changes in magnetic flux induce EMF ([[quick-context/lenzs-law|Faraday's law]]). |
| **Displacement Current** | Maxwell's key addition: a changing electric field acts like a current for purposes of creating magnetic fields. Written as $\varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}$. Completes the symmetry between E and B. |

<details>
<summary><strong>How It Works</strong> — The four equations explained</summary>

## The Four Equations: What Each Says

Maxwell's equations can be written in multiple forms (integral, differential, with or without materials). Here's the differential form in vacuum, with physical meaning:

```
MAXWELL'S EQUATIONS — Differential Form (Vacuum)
══════════════════════════════════════════════════════════════════════════════

1. GAUSS'S LAW FOR ELECTRICITY
   ─────────────────────────────────────────────────────────────────────────
   ∇ · E = ρ / ε₀

   "Electric field lines diverge from positive charges and converge on
    negative charges."

   • ∇ · E = divergence of E (how much field "spreads out" from a point)
   • ρ = charge density (C/m³)
   • ε₀ = permittivity of free space = 8.85 × 10⁻¹² F/m

   IMPLICATIONS:
   • Positive charges are sources of E-field lines
   • Negative charges are sinks of E-field lines
   • Total flux out of any closed surface = enclosed charge / ε₀
   • This is why [[quick-context/capacitor|capacitors]] work: charges on plates create
     field between them


2. GAUSS'S LAW FOR MAGNETISM
   ─────────────────────────────────────────────────────────────────────────
   ∇ · B = 0

   "Magnetic field lines have no beginning or end—they always form
    closed loops."

   IMPLICATIONS:
   • There are no magnetic monopoles (isolated N or S poles)
   • Every magnetic field line that enters a region must exit it
   • Cut a magnet in half → two complete magnets, not isolated poles

            ┌────────────────────┐
            │                    │
            ▼                    │
       N ═══════════════════ S  │
            │                    │
            └────────────────────┘

   Field lines loop from N to S outside, S to N inside.


3. FARADAY'S LAW OF INDUCTION
   ─────────────────────────────────────────────────────────────────────────
   ∇ × E = -∂B/∂t

   "A changing magnetic field creates a circulating electric field."

   • ∇ × E = curl of E (how much E-field circulates around a point)
   • ∂B/∂t = rate of change of magnetic field
   • The minus sign is [[quick-context/lenzs-law|Lenz's Law]]: induced E opposes the change

   IMPLICATIONS:
   • This is why generators work: rotating coil in magnetic field
     experiences changing B, which induces E, which drives current
   • This is why [[quick-context/inductor|inductors]] oppose current changes: changing I
     creates changing B, which induces opposing E (back-EMF)
   • This is why transformers transfer power between isolated coils

            Changing B
               ↓↓↓↓↓
            ┌────────┐
            │        │ ← induced E circulates around the changing B
            │  coil  │
            └────────┘


4. AMPÈRE-MAXWELL LAW
   ─────────────────────────────────────────────────────────────────────────
   ∇ × B = μ₀J + μ₀ε₀ ∂E/∂t

   "Magnetic field circulates around currents AND around changing
    electric fields."

   • ∇ × B = curl of B (how much B-field circulates around a point)
   • μ₀ = permeability of free space = 4π × 10⁻⁷ T·m/A
   • J = current density (A/m²)
   • μ₀ε₀ ∂E/∂t = Maxwell's displacement current term

   IMPLICATIONS:
   • Currents create circulating magnetic fields (right-hand rule):

                Current I
                   │
                   ▼
          ─────────⊗─────────  Wire (current into page)
                   │
              ┌────┴────┐
              │    B    │  B-field circles around current
              │ circles │
              └─────────┘

   • Maxwell's addition: changing E-field ALSO creates B-field
   • This completes the symmetry: changing B creates E, changing E creates B
   • This symmetry enables electromagnetic waves!


THE KEY INSIGHT: MAXWELL'S DISPLACEMENT CURRENT
══════════════════════════════════════════════════════════════════════════════

Before Maxwell, Ampère's law was just: ∇ × B = μ₀J

Problem: Consider a charging [[quick-context/capacitor|capacitor]]:

    ┌───────────────────────────────────────────────┐
    │                                               │
    │  Current I flows in wire, but NOT between    │
    │  capacitor plates (it's an insulator!)       │
    │                                               │
    │      I →→→→→   │gap│   →→→→→ I               │
    │  ════════════  │   │  ════════════           │
    │      wire      │ C │     wire                │
    │                │   │                         │
    └───────────────────────────────────────────────┘

Draw a loop around the wire: current I passes through → B-field exists ✓
Draw a loop around the gap: no current passes through → B = 0 ???

But the B-field can't suddenly disappear at the gap!

MAXWELL'S SOLUTION:
───────────────────────────────────────────────────────────────────────────

    Between the plates, E-field is changing (as charge accumulates):

         (+)  →→→→→→→→→→→  (-)
              E increasing

    Maxwell said: treat ε₀ ∂E/∂t as an equivalent "displacement current"

    This displacement current equals the real current in the wire!

         I_displacement = ε₀ × dΦ_E/dt = ε₀ × A × dE/dt

    For a capacitor: I = C × dV/dt, and E = V/d, so:
    I = ε₀ × (A/d) × dV/dt = ε₀ × A × (1/d) × dV/dt
    Since C = ε₀A/d, this equals C × dV/dt = I  ✓

    The displacement current between the plates equals the conduction
    current in the wire. Continuity restored, and ∇ × B = μ₀J + μ₀ε₀ ∂E/∂t
    gives consistent results everywhere.
```

## How the Equations Predict Electromagnetic Waves

The revolutionary consequence: combining Faraday's law and the Ampère-Maxwell law shows that E and B fields can sustain each other through empty space.

```
DERIVING ELECTROMAGNETIC WAVES
══════════════════════════════════════════════════════════════════════════════

Take curl of Faraday's law:
    ∇ × (∇ × E) = -∂(∇ × B)/∂t

Substitute Ampère-Maxwell (in vacuum, J = 0):
    ∇ × (∇ × E) = -∂/∂t (μ₀ε₀ ∂E/∂t)
    ∇ × (∇ × E) = -μ₀ε₀ ∂²E/∂t²

Use vector identity ∇ × (∇ × E) = ∇(∇ · E) - ∇²E:
    In vacuum, ∇ · E = 0 (no charges), so:
    -∇²E = -μ₀ε₀ ∂²E/∂t²

This is the WAVE EQUATION:
    ∇²E = μ₀ε₀ ∂²E/∂t²

    Wave speed: c = 1/√(μ₀ε₀)

CALCULATING THE SPEED:
───────────────────────────────────────────────────────────────────────────

    μ₀ = 4π × 10⁻⁷ T·m/A
    ε₀ = 8.854 × 10⁻¹² F/m

    c = 1/√(μ₀ε₀)
    c = 1/√(4π × 10⁻⁷ × 8.854 × 10⁻¹²)
    c = 1/√(1.112 × 10⁻¹⁷)
    c = 2.998 × 10⁸ m/s

    This is EXACTLY the measured speed of light!

MAXWELL'S CONCLUSION (1865):
───────────────────────────────────────────────────────────────────────────

    "This velocity is so nearly that of light that it seems we have
     strong reason to conclude that light itself is an electromagnetic
     disturbance."

    Light is an electromagnetic wave. So are radio waves, microwaves,
    infrared, ultraviolet, X-rays, and gamma rays—all the same physics
    at different frequencies.


THE SELF-SUSTAINING WAVE
══════════════════════════════════════════════════════════════════════════════

    Changing E creates B (Ampère-Maxwell)
         +
    Changing B creates E (Faraday)
         =
    SELF-SUSTAINING WAVE through empty space

    Direction of propagation ───────────────────────────────►  c

         E (vertical)
           │
           │    ╱╲          ╱╲          ╱╲
           │   ╱  ╲        ╱  ╲        ╱  ╲
       ────┼──╱────╲──────╱────╲──────╱────╲──────► z
           │ ╱      ╲    ╱      ╲    ╱      ╲
           │╱        ╲  ╱        ╲  ╱        ╲╱
           │          ╲╱          ╲╱

         B (into/out of page, perpendicular to E)
           ⊙  ⊙  ⊗  ⊗  ⊙  ⊙  ⊗  ⊗  ⊙  ⊙  ⊗  ⊗

    E and B oscillate perpendicular to each other AND perpendicular
    to the direction of propagation. This is a transverse wave.

    Energy carried: S = (1/μ₀) E × B  (Poynting vector)
```

</details>

<details>
<summary><strong>The Key Tension</strong> — Integral vs. differential form</summary>

## Two Ways to Write the Same Physics

Maxwell's equations can be expressed in integral form (useful for calculations with symmetry) or differential form (useful for general analysis and deriving waves). They're mathematically equivalent via Stokes' and Gauss's theorems.

```
INTEGRAL vs. DIFFERENTIAL FORMS
══════════════════════════════════════════════════════════════════════════════

EQUATION 1: GAUSS'S LAW (ELECTRIC)
───────────────────────────────────────────────────────────────────────────

    INTEGRAL:    ∮ E · dA = Q_enc / ε₀

    "Total electric flux through any
     closed surface equals the enclosed
     charge divided by ε₀"

    Best for: Spheres, cylinders, planes
    with charge symmetry

    DIFFERENTIAL:    ∇ · E = ρ / ε₀

    "Divergence of E at any point equals
     charge density at that point"

    Best for: General analysis, deriving
    wave equations


EQUATION 2: GAUSS'S LAW (MAGNETIC)
───────────────────────────────────────────────────────────────────────────

    INTEGRAL:    ∮ B · dA = 0

    "Total magnetic flux through any
     closed surface is zero"

    DIFFERENTIAL:    ∇ · B = 0

    "B-field has no divergence anywhere
     (no magnetic monopoles)"


EQUATION 3: FARADAY'S LAW
───────────────────────────────────────────────────────────────────────────

    INTEGRAL:    ∮ E · dl = -dΦ_B/dt

    "EMF around any closed loop equals
     negative rate of change of magnetic
     flux through the loop"

    Best for: Generators, [[quick-context/inductor|inductors]],
    [[quick-context/electricity-generation|transformers]]

    DIFFERENTIAL:    ∇ × E = -∂B/∂t

    "Curl of E equals negative time
     derivative of B"

    Best for: Wave propagation analysis


EQUATION 4: AMPÈRE-MAXWELL LAW
───────────────────────────────────────────────────────────────────────────

    INTEGRAL:    ∮ B · dl = μ₀I_enc + μ₀ε₀ dΦ_E/dt

    "Circulation of B around any loop
     equals μ₀ times enclosed current
     plus displacement current"

    Best for: Calculating B from known
    current distributions

    DIFFERENTIAL:    ∇ × B = μ₀J + μ₀ε₀ ∂E/∂t

    "Curl of B equals μ₀ times current
     density plus displacement current"

    Best for: General field analysis
```

| When to Use | Integral Form | Differential Form |
|-------------|---------------|-------------------|
| High-symmetry problems | Better | Works but overkill |
| Deriving wave equations | Awkward | Required |
| Circuit analysis (EMF, flux) | Better | Works |
| Numerical simulation | Possible | Required |
| Relativistic formulation | Possible | Natural ([[quick-context/tensor|tensor]] form) |
| Conceptual understanding | Often clearer | More compact |

</details>

<details>
<summary><strong>Concrete Example</strong> — Understanding each equation physically</summary>

## Physical Manifestation of Each Equation

Each Maxwell equation has direct, observable consequences:

```
EQUATION 1: GAUSS'S LAW → CAPACITORS AND SHIELDING
══════════════════════════════════════════════════════════════════════════════

    ∮ E · dA = Q_enc / ε₀

    APPLICATION: Electric field of a parallel plate [[quick-context/capacitor|capacitor]]

    Draw a Gaussian surface (box) with one face between the plates:

         (+) ───────────────────────
              │  E  │  E  │  E  │
              ▼     ▼     ▼     ▼
         ┌────┬─────────────────────┐
         │    │                     │ ← Gaussian box
         └────┴─────────────────────┘
         (-) ───────────────────────

    • E-field only passes through top face (uniform, perpendicular)
    • Flux = E × A
    • Enclosed charge = σ × A (surface charge density × area)

    Therefore: E × A = σA / ε₀
               E = σ / ε₀

    This is how we derive the [[quick-context/capacitor|capacitor]] formula C = ε₀A/d


EQUATION 2: GAUSS'S LAW (MAGNETIC) → NO MAGNETIC MONOPOLES
══════════════════════════════════════════════════════════════════════════════

    ∮ B · dA = 0

    Draw ANY closed surface around ANY region—the total B-flux is zero.

    Consequence: You can never isolate a single magnetic pole.

         ┌────────────────────────────────┐
         │     ┌─────────────────────┐    │
         │     │                     │    │
         │     │   N ═══════════ S   │    │
         │     │                     │    │
         │     └─────────────────────┘    │
         │                                │
         │  Gaussian surface around       │
         │  the magnet: flux in = flux out│
         │                                │
         └────────────────────────────────┘

    Lines entering at S pole exit at N pole. Net flux = 0.

    If you cut the magnet, you get two smaller magnets, not N and S separately!


EQUATION 3: FARADAY'S LAW → [[quick-context/electricity-generation|GENERATORS]] AND [[quick-context/inductor|INDUCTORS]]
══════════════════════════════════════════════════════════════════════════════

    ∮ E · dl = -dΦ_B/dt       or       EMF = -N × dΦ/dt

    APPLICATION: Generator

         N ════════════════════════════════ S
                       ┌──────────┐
                       │          │
                       │   COIL   │ ← rotates on axis
                       │          │
                       └────┬─────┘
                            │
                         SHAFT

    As coil rotates:
    • Angle between coil and B-field changes
    • Flux Φ = B × A × cos(θ) changes
    • dΦ/dt ≠ 0 → EMF induced!
    • EMF drives current through external circuit

    One rotation = one complete AC cycle


    APPLICATION: [[quick-context/inductor|Inductor]] back-EMF

    Current through coil creates flux: Φ = L × I
    If current changes: dΦ/dt = L × dI/dt
    Faraday's law: EMF = -L × dI/dt (back-EMF)

    This is [[quick-context/lenzs-law|Lenz's Law]] in action—the minus sign means
    the induced EMF opposes the change that caused it.


EQUATION 4: AMPÈRE-MAXWELL → ELECTROMAGNETS AND EM WAVES
══════════════════════════════════════════════════════════════════════════════

    ∮ B · dl = μ₀I_enc + μ₀ε₀ dΦ_E/dt

    APPLICATION: [[quick-context/coil-magnetic-field|Magnetic field of a solenoid]]

    Draw an Amperian loop through the solenoid:

         ───────────────────────────────────────
         ⊗   ⊗   ⊗   ⊗   ⊗   ⊗   ⊗   ⊗   ⊗   ⊗
         │                                     │
         │  ═══════════════════════════════   │ ← B uniform inside
         │                                     │
         ⊙   ⊙   ⊙   ⊙   ⊙   ⊙   ⊙   ⊙   ⊙   ⊙
         ───────────────────────────────────────

    • B is uniform inside, ~0 outside
    • ∮ B · dl = B × L (only inside segment contributes)
    • I_enc = n × L × I (turns per length × length × current per turn)

    Therefore: B × L = μ₀ × n × L × I
               B = μ₀nI

    This is the [[quick-context/coil-magnetic-field|solenoid field formula]].


    APPLICATION: Electromagnetic waves (displacement current)

    The μ₀ε₀ ∂E/∂t term enables waves to propagate through vacuum
    where there are no real currents. Changing E creates B, and
    that changing B creates E, bootstrapping through empty space.
```

**The one thing most outsiders get wrong about Maxwell's equations is...** thinking they're just a mathematical formalism for what we already knew. They're not. Before Maxwell added the displacement current term ($\varepsilon_0 \partial \mathbf{E}/\partial t$), there was no theoretical basis for electromagnetic waves. The equations predicted that light is an electromagnetic wave *before* this was experimentally confirmed. They predicted radio waves 20+ years before Hertz detected them. Maxwell's equations are genuinely predictive physics, not just a summary of known phenomena.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/electromagnetism]]** — Conceptual treatment of electromagnetic phenomena without heavy mathematics. Covers the same physics from a more intuitive angle.

- **[[quick-context/electric-magnetic-field-unification|Field Unification]]** — Why E and B are two aspects of one underlying field, connected through the motion of observers. The conceptual foundation for Maxwell's unification.

- **[[quick-context/faraday-tensor]]** — The relativistic formulation: Maxwell's four equations compress into two [[learning/notes/quick-context/tensor|tensor]] equations, making Lorentz covariance manifest. E and B mix together under velocity transformations.

- **[[quick-context/inductor]]** — Practical application of Faraday's law: V = L × dI/dt. Inductors store energy in magnetic fields and oppose current changes.

- **[[quick-context/capacitor]]** — Stores energy in electric fields. Displacement current flows "through" capacitors during charging, completing the circuit conceptually.

- **[[quick-context/lenzs-law]]** — The physics behind the minus sign in Faraday's law: induced effects always oppose the change that caused them, enforcing energy conservation.

- **[[quick-context/electricity-generation]]** — How generators convert mechanical energy to electricity using Faraday's law. The practical workhorse application of Maxwell's equations.

- **[[quick-context/coil-magnetic-field]]** — Detailed treatment of how current through coils creates magnetic fields, including the solenoid formula B = μ₀nI derived from Ampère's law.

- **[[quick-context/voltage]]** — Electric field integrated along a path gives [[learning/notes/quick-context/voltage|voltage]]. Maxwell's equations govern the field; voltage is how we measure it in circuits.

- **Vector Calculus** — Understanding ∇·, ∇×, line integrals, and surface integrals is essential for working with Maxwell's equations mathematically.

- **Special Relativity** — Einstein showed that Maxwell's equations are already relativistically correct. It was Newton's mechanics that needed modification, not [[learning/notes/quick-context/electromagnetism|electromagnetism]].

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Gauss's law for magnetism states ∇ · B = 0. What does this physically mean?
<details>
<summary>Answer</summary>
**There are no magnetic monopoles.** Magnetic field lines always form closed loops—they never start or end at a point. Every N pole comes with an S pole. If you draw any closed surface, the same amount of B-field that enters must exit. This contrasts with electric fields, where ∇ · E = ρ/ε₀ means field lines can start on positive charges and end on negative charges.
</details>

**Q2:** Why did Maxwell add the displacement current term (ε₀ ∂E/∂t) to Ampère's law?
<details>
<summary>Answer</summary>
**To fix a mathematical inconsistency with charging capacitors.** Without it, Ampère's law ∮ B · dl = μ₀I would give different answers depending on which surface you used to calculate enclosed current. A loop around a wire carrying current to a [[learning/notes/quick-context/capacitor|capacitor]] would show I ≠ 0, but the same loop using a surface passing through the capacitor gap would show I = 0 (no charges crossing). Maxwell realized that the changing E-field between the plates acts like a current for creating B-fields, restoring consistency. See: Concrete Example (displacement current section).
</details>

**Q3:** Maxwell calculated electromagnetic wave speed as c = 1/√(μ₀ε₀). Why was this result so significant?
<details>
<summary>Answer</summary>
**It matched the known speed of light exactly.** μ₀ and ε₀ were measured independently through electric and magnetic experiments—nothing to do with light. Yet when combined, they gave 3×10⁸ m/s, the speed of light. This couldn't be coincidence. Maxwell concluded that light IS an electromagnetic wave. This unified optics with electromagnetism and predicted the entire electromagnetic spectrum (radio, infrared, UV, X-rays) before most were discovered.
</details>

**Q4:** Faraday's law says ∇ × E = -∂B/∂t. How does this equation explain why inductors resist current changes?
<details>
<summary>Answer</summary>
**Changing current creates changing B, which creates opposing E.** In an [[quick-context/inductor|inductor]], current I creates magnetic field B = μ₀nI. If I changes, B changes, so ∂B/∂t ≠ 0. Faraday's law says this creates a circulating E-field (the curl of E is non-zero). This induced E-field manifests as back-EMF: V = -L × dI/dt. The minus sign ([[quick-context/lenzs-law|Lenz's Law]]) ensures the induced voltage opposes the change in current.
</details>

**Q5:** In empty space with no charges or currents, Maxwell's equations still allow solutions. What are these solutions?
<details>
<summary>Answer</summary>
**Electromagnetic waves.** With ρ = 0 and J = 0, the equations become: ∇ · E = 0, ∇ · B = 0, ∇ × E = -∂B/∂t, ∇ × B = μ₀ε₀ ∂E/∂t. These combine into wave equations: ∇²E = μ₀ε₀ ∂²E/∂t² and ∇²B = μ₀ε₀ ∂²B/∂t². The solutions are waves where E and B oscillate perpendicular to each other and to the propagation direction, traveling at c = 1/√(μ₀ε₀). Light, radio waves, and all electromagnetic radiation are these solutions.
</details>

</details>
