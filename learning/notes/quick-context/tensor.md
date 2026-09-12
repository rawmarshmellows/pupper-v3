---
topic: Tensor
created: 2026-03-04
---

# Tensor

> **Related:** [[learning/notes/quick-context/faraday-tensor]] | [[learning/notes/quick-context/covariance-matrix]] | [[learning/notes/quick-context/cations-and-reduction]] | [[learning/notes/quick-context/how-source-code-is-stored]] | [[learning/notes/quick-context/electromagnetism]]

> **TL;DR:** A tensor is a mathematical object that generalizes scalars (rank 0), vectors (rank 1), and matrices (rank 2) to arbitrary dimensions, with the defining property that it transforms predictably under coordinate changes—meaning the physical or geometric quantity it represents stays the same regardless of which coordinate system you use to describe it.

## The Core Problem

Physics and engineering need quantities that exist independently of how you choose to measure them. A force doesn't change just because you rotate your ruler. Stress inside a material doesn't depend on which direction you call "x." But the *numbers* you use to describe these quantities do change with your coordinate choice. Tensors solve this: they package multi-directional information with built-in transformation rules, so the underlying reality is preserved even as the description changes.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Rank (Order)** | The number of indices needed to specify a component. A scalar is rank 0 (no index), a vector is rank 1 (one index: $v_i$), a matrix-like tensor is rank 2 (two indices: $T_{ij}$), and so on. |
| **Components** | The individual numbers that make up a tensor in a particular coordinate system. A rank-2 tensor in 3D has $3^2 = 9$ components; in 4D spacetime, $4^2 = 16$. |
| **Transformation Law** | The rule specifying how tensor components change when you switch coordinate systems. This is *the* defining property: if it transforms like a tensor, it is a tensor. |
| **Contraction** | Summing over a repeated upper and lower index (Einstein summation), which reduces the rank by 2. Example: contracting a rank-2 tensor $T^i{}_i$ gives a scalar (rank 0)—the trace. |
| **Metric Tensor ($g_{ij}$)** | A rank-2 tensor that defines distances and angles in a space. In flat 3D space it's just the identity matrix; in curved spacetime (general relativity) it encodes gravity. |

<details>
<summary><strong>How It Works</strong> — The hierarchy from scalars to tensors</summary>

## Building Up: Scalars, Vectors, Tensors

The key idea is that tensors are a *generalization*. Each level adds a new "direction" of information:

```
THE TENSOR HIERARCHY
══════════════════════════════════════════════════════════════════════════════

RANK 0: SCALAR — A single number
────────────────────────────────────────────────────────────────────────────

    Examples: temperature (25°C), mass (5 kg), electric charge (1.6×10⁻¹⁹ C)

    No direction. Same value in every coordinate system.
    Components: 1 (just the number itself)


RANK 1: VECTOR — A magnitude and direction
────────────────────────────────────────────────────────────────────────────

    Examples: velocity, force, electric field E

    One index: v_i where i = x, y, z

    In 3D:  v = (v_x, v_y, v_z) → 3 components

    Rotate your axes and the COMPONENTS change,
    but the arrow in space stays the same:

         y                y'
         ↑     →v          ╲     →v
         │    ╱              ╲  ╱
         │   ╱                ╲╱
         │  ╱                  ╲
         └──────→ x             ╲──→ x'

    v = (3, 4) in xy     v = (5, 0) in x'y'
    Same vector, different components.


RANK 2: MATRIX-LIKE — Maps vectors to vectors
────────────────────────────────────────────────────────────────────────────

    Examples: stress tensor, moment of inertia tensor,
              Faraday tensor (electromagnetic field)

    Two indices: T_ij where i, j each run over coordinates

    In 3D: 3×3 = 9 components
    In 4D spacetime: 4×4 = 16 components

    A rank-2 tensor captures relationships BETWEEN directions:

    STRESS TENSOR (σ_ij):
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │   "Force in direction i acting on a surface facing          │
    │    direction j"                                             │
    │                                                             │
    │         σ_xx   σ_xy   σ_xz                                  │
    │   σ =  σ_yx   σ_yy   σ_yz                                  │
    │         σ_zx   σ_zy   σ_zz                                  │
    │                                                             │
    │   Diagonal: normal stresses (tension/compression)           │
    │   Off-diagonal: shear stresses (sliding forces)             │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘


HIGHER RANKS: More indices, more directions
────────────────────────────────────────────────────────────────────────────

    Rank 3: T_ijk — e.g., piezoelectric tensor (stress → electric field)
    Rank 4: T_ijkl — e.g., elasticity tensor (maps stress to strain)

    Components grow as n^rank:
    • Rank 2 in 3D: 9 components
    • Rank 3 in 3D: 27 components
    • Rank 4 in 3D: 81 components
```

## The Defining Property: Transformation Rules

What makes a tensor a tensor (and not just a collection of numbers) is *how it transforms*:

```
WHY TRANSFORMATION IS THE KEY
══════════════════════════════════════════════════════════════════════════════

NOT every matrix is a tensor. A tensor must transform correctly
when you change coordinates.

VECTOR TRANSFORMATION (rank 1):
────────────────────────────────────────────────────────────────────────────

    When rotating coordinates by matrix R:

    v'_i = R_ij × v_j    (sum over j)

    Each new component is a linear combination of old components.


RANK-2 TENSOR TRANSFORMATION:
────────────────────────────────────────────────────────────────────────────

    T'_ij = R_ik × R_jl × T_kl    (sum over k and l)

    Two rotation matrices—one for each index.
    This ensures the tensor represents the same physical quantity
    in any coordinate system.


THE FARADAY TENSOR EXAMPLE:
────────────────────────────────────────────────────────────────────────────

    The Faraday tensor F^μν packages E and B fields into a 4×4
    antisymmetric matrix (see: [[learning/notes/quick-context/faraday-tensor]]).

    Under a Lorentz transformation (changing velocity):

    F'^μν = Λ^μ_α × Λ^ν_β × F^αβ

    This is why E and B fields MIX when you change reference frames—
    the transformation law mixes time-space components (E) with
    space-space components (B). The tensor itself doesn't change;
    your decomposition into E and B does.


WHAT FAILS THE TEST:
────────────────────────────────────────────────────────────────────────────

    Christoffel symbols (Γ^i_jk) in general relativity look like
    rank-3 tensors but DON'T transform like tensors. They contain
    information about how coordinates curve, not about physical
    quantities. This distinction matters: you can always find
    coordinates where Γ = 0 at a point, meaning gravity "vanishes"
    locally (Einstein's equivalence principle).
```

</details>

<details>
<summary><strong>The Key Tension</strong> — Abstract math vs. concrete physics</summary>

## Index Gymnastics vs. Geometric Intuition

There are two camps for understanding tensors:

```
TWO APPROACHES TO TENSORS
══════════════════════════════════════════════════════════════════════════════

APPROACH 1: COMPONENT-BASED (traditional physics/engineering)
────────────────────────────────────────────────────────────────────────────

    "A tensor is a multi-indexed array that transforms
     according to specific rules under coordinate changes."

    T'_ij = R_ik R_jl T_kl

    Pros: Concrete, calculable, matches how you do computations
    Cons: Can feel like bookkeeping; easy to lose physical meaning
          in a sea of indices


APPROACH 2: GEOMETRIC/ABSTRACT (modern math, general relativity)
────────────────────────────────────────────────────────────────────────────

    "A tensor is a multilinear map from vectors and covectors
     to scalars, independent of any coordinate system."

    T: V × V* × V → ℝ  (example for a rank-(1,2) tensor)

    Pros: Coordinate-free, reveals deep structure, elegant
    Cons: Abstract, harder to compute with, requires linear algebra
          background
```

| When to Use | Component View | Geometric View |
|-------------|---------------|----------------|
| Engineering stress analysis | Better | Overkill |
| Numerical computation (FEM, CFD) | Required | Background |
| General relativity | Needed for calculation | Needed for understanding |
| Machine learning ("tensors" in PyTorch) | It's just arrays | N/A (not real tensors) |
| Building physical intuition | Start here | Graduate to this |

The deepest understanding comes from fluency in both: knowing *what* a tensor represents geometrically, and being able to *compute* with its components.

</details>

<details>
<summary><strong>Concrete Example</strong> — The stress tensor in materials</summary>

## Stress: Why a Single Number Isn't Enough

When we say a material has a [[learning/notes/quick-context/tensile-strength-materials|tensile strength]] of 27 MPa, that's a simplification. Internally, the stress state at any point is described by a rank-2 tensor with 9 components (6 independent, due to symmetry):

```
THE STRESS TENSOR IN ACTION
══════════════════════════════════════════════════════════════════════════════

SIMPLE TENSION (pulling a rod):
────────────────────────────────────────────────────────────────────────────

    Force F pulling along x-axis:

         ←───── F           F ─────→
         ═══════════════════════════
                   Rod

    Stress tensor:

         ┌              ┐
         │ σ   0   0    │
    σ =  │ 0   0   0    │     Only σ_xx is nonzero
         │ 0   0   0    │     σ = F / A (force / area)
         └              ┘

    This is the "tensile strength" number on a spec sheet—
    the σ_xx component when pulling along one axis.


SHEAR STRESS (twisting or sliding):
────────────────────────────────────────────────────────────────────────────

    Shear force along x, acting on y-face:

              ───────→ F (shear)
         ┌──────────────────┐
         │                  │
         │    Material      │     y
         │                  │     ↑
         └──────────────────┘     └──→ x

    Stress tensor:

         ┌              ┐
         │ 0   τ   0    │
    σ =  │ τ   0   0    │     Off-diagonal = shear
         │ 0   0   0    │     Symmetric: σ_xy = σ_yx
         └              ┘


COMBINED LOADING (real-world):
────────────────────────────────────────────────────────────────────────────

    A bracket under both tension and shear:

         ┌                      ┐
         │ 20 MPa   5 MPa   0  │
    σ =  │  5 MPa  -3 MPa   0  │     Tension, compression,
         │  0       0        0  │     and shear all at once
         └                      ┘

    This is why a single "tensile strength" number doesn't capture
    the full picture—real parts experience multi-axis stress states.

    EIGENVALUES of this tensor = principal stresses
    (the stress values in the orientation where shear vanishes)

    Finding principal stresses = rotating coordinates to diagonalize
    the tensor. This is a coordinate transformation—exactly what
    tensors are designed to handle.
```

**The one thing most outsiders get wrong about this is...** confusing tensors with matrices. Every rank-2 tensor can be *represented* as a matrix in a given coordinate system, but not every matrix is a tensor. The difference: a tensor has a transformation law tied to coordinate changes that preserves physical meaning. A rotation matrix R itself is not a tensor—it describes the *relationship between* coordinate systems, not a physical quantity that exists in space. Similarly, "tensors" in machine learning libraries (PyTorch, TensorFlow) are just multi-dimensional arrays with no transformation law—they borrowed the name but not the physics.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[learning/notes/quick-context/faraday-tensor]]** — The most important tensor in electromagnetism: a rank-2 antisymmetric tensor that packages the electric and magnetic fields into a single object. Demonstrates how tensor transformation laws explain why E and B mix between reference frames.

- **[[learning/notes/quick-context/maxwell-equations]]** — Maxwell's four equations reduce to two tensor equations using the Faraday tensor, making Lorentz covariance manifest. This is the power of the tensor formulation: compactness and frame-independence.

- **[[learning/notes/quick-context/tensile-strength-materials]]** — Tensile strength (MPa) is actually one component of the stress tensor $\sigma_{ij}$. Real materials experience multi-axis stress states described by the full rank-2 stress tensor.

- **[[learning/notes/quick-context/electromagnetism]]** — Electric and magnetic fields are vector fields (rank-1 tensors). Their unification into a single entity requires a rank-2 tensor (the Faraday tensor).

- **[[learning/notes/quick-context/electric-magnetic-field-unification]]** — The physical motivation for why E and B need tensor packaging: they transform into each other under velocity changes, which is precisely what the Faraday tensor's transformation law describes.

- **General Relativity** — Einstein's field equations $G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$ relate two rank-2 tensors: the Einstein tensor (spacetime curvature) and the stress-energy tensor (matter/energy content). Gravity IS spacetime curvature, described entirely by tensors.

- **Linear Algebra** — Eigenvalues, eigenvectors, and matrix diagonalization are the computational backbone for working with rank-2 tensors. Principal stresses, principal axes, and invariants all come from linear algebra.

- **Differential Geometry** — The modern mathematical home of tensors. Tensors live on manifolds (curved spaces) and are defined coordinate-free as multilinear maps. This is essential for general relativity.

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** Temperature at a point is a scalar (rank-0 tensor). Velocity is a vector (rank-1 tensor). Why is stress a rank-2 tensor and not just a vector?
<details>
<summary>Answer</summary>
**Because stress requires two directions to specify: the direction of force AND the orientation of the surface it acts on.** A vector only has one direction. When you say "20 MPa tensile stress," you're implicitly specifying both the pulling direction and the cross-section orientation. The stress tensor $\sigma_{ij}$ captures force in direction $i$ acting on a surface whose normal points in direction $j$. This two-directional nature is exactly what makes it rank 2. See: Concrete Example.
</details>

**Q2:** A rank-2 tensor in 3D has 9 components. The stress tensor is symmetric ($\sigma_{ij} = \sigma_{ji}$). How many independent components does it have?
<details>
<summary>Answer</summary>
**6.** The 3 diagonal components ($\sigma_{xx}$, $\sigma_{yy}$, $\sigma_{zz}$) are independent, and of the 6 off-diagonal components, symmetry pairs them: $\sigma_{xy} = \sigma_{yx}$, $\sigma_{xz} = \sigma_{zx}$, $\sigma_{yz} = \sigma_{zy}$. So 3 diagonal + 3 independent off-diagonal = 6 total. Compare to the [[learning/notes/quick-context/faraday-tensor|Faraday tensor]], which is *anti*symmetric ($F^{\mu\nu} = -F^{\nu\mu}$) in 4D, also giving 6 independent components.
</details>

**Q3:** The [[learning/notes/quick-context/faraday-tensor|Faraday tensor]] is antisymmetric ($F^{\mu\nu} = -F^{\nu\mu}$) and the stress tensor is symmetric ($\sigma_{ij} = \sigma_{ji}$). What does this difference mean physically?
<details>
<summary>Answer</summary>
**Antisymmetry means the "diagonal" (same-index) components are zero, and swapping indices flips the sign.** For the Faraday tensor, this encodes the fact that the electromagnetic field has a rotational character—E and B represent oriented planes in spacetime, not symmetric pairings. For the stress tensor, symmetry reflects conservation of angular momentum: if the stress weren't symmetric, the material would spontaneously start spinning. The symmetry type constrains which physical quantities the tensor can represent.
</details>

**Q4:** In PyTorch, you create a "tensor" with `torch.tensor([1, 2, 3])`. Is this a tensor in the physics/math sense? Why or why not?
<details>
<summary>Answer</summary>
**No.** A PyTorch "tensor" is just a multi-dimensional array of numbers—it has no transformation law. A real tensor must transform in a specific way under coordinate changes so that the physical quantity it represents is preserved. PyTorch tensors don't "know" about coordinate systems or transformations; they're data containers optimized for GPU computation. The name was borrowed from mathematics for its connotation of "multi-dimensional," but the defining property (transformation law) is absent.
</details>

**Q5:** The metric tensor in flat 3D Euclidean space is the identity matrix ($g_{ij} = \delta_{ij}$). In curved spacetime near a black hole, $g_{ij}$ has complex, position-dependent entries. What physical quantity is the metric tensor encoding in each case?
<details>
<summary>Answer</summary>
**Distances and angles.** In flat space, $g_{ij} = \delta_{ij}$ means distance is computed by the Pythagorean theorem: $ds^2 = dx^2 + dy^2 + dz^2$. Near a black hole, the metric tensor encodes how spacetime is *curved* by gravity—distances and time intervals are warped. The line element $ds^2 = g_{\mu\nu} dx^\mu dx^\nu$ gives the "true" spacetime distance between nearby events. The metric tensor is what makes the abstract math of tensors connect to physical measurements of rulers and clocks. Einstein's key insight was that gravity isn't a force—it's the curvature of spacetime described by the metric tensor.
</details>

</details>
