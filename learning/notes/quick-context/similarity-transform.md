---
topic: Similarity Transform
created: 2026-04-04
---

> **Related:** [[learning/notes/quick-context/helmert-transform|Helmert Transform]]

# N-Dimensional Similarity Transform


> **TL;DR:** A similarity transform preserves shape (angles and ratios of distances) while allowing uniform scaling, rotation, and translation -- it is the most general transform that keeps "similar" figures similar, in any number of dimensions.

## The Core Problem

Many tasks in science and engineering require comparing or aligning objects that have the same shape but differ in position, orientation, and size. A biologist compares two protein structures measured at different scales. A surveyor reconciles GPS coordinates with a local map. A computer vision system matches a 3D model to a scene viewed from an unknown angle and distance. In every case you need a transform that can absorb differences in pose and scale while guaranteeing that the intrinsic geometry -- all angles, all distance ratios -- stays untouched. Without similarity transforms, you would need to manually strip away each degree of freedom (translation, rotation, scale) in separate ad-hoc steps with no unified mathematical framework.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Similarity transform** | A map $T(\mathbf{x}) = sR\mathbf{x} + \mathbf{t}$ combining uniform scale $s > 0$, orthogonal rotation $R$, and translation $\mathbf{t}$, preserving angles and distance ratios |
| **Isometry** | A similarity transform with $s = 1$ (also called a rigid transform or Euclidean motion) -- preserves absolute distances, not just ratios |
| **Degrees of freedom** | The number of independent parameters defining a transform; a similarity in $n$ dimensions has $\frac{n(n+1)}{2} + 1$ DOF |
| **Conformal map** | Any smooth map that preserves angles locally; similarity transforms are the *global* conformal maps of Euclidean space (angle-preserving everywhere, not just infinitesimally) |
| **Procrustes analysis** | A statistical method that finds the optimal similarity transform to superimpose two or more point configurations, minimizing the sum of squared distances between corresponding points |

<details>
<summary><strong>How It Works</strong> -- The essential mechanism</summary>

### The General Form

A similarity transform in $n$-dimensional Euclidean space is:

$$T(\mathbf{x}) = sR\mathbf{x} + \mathbf{t}$$

where:
- $s > 0$ is a uniform scale factor (one scalar, same in every direction)
- $R \in SO(n)$ is a proper rotation matrix ($R^TR = I$, $\det(R) = +1$)
- $\mathbf{t} \in \mathbb{R}^n$ is a translation vector

If you also allow reflections ($\det(R) = \pm 1$, i.e., $R \in O(n)$), you get an *improper* similarity, sometimes called an opposite similarity.

### Degrees of Freedom in N Dimensions

Each component contributes a specific number of free parameters:

| Component | DOF | Why |
|-----------|-----|-----|
| Translation $\mathbf{t}$ | $n$ | One shift per axis |
| Rotation $R$ | $\frac{n(n-1)}{2}$ | Number of independent plane rotations (Givens rotations) in $n$-space |
| Uniform scale $s$ | $1$ | A single scalar |
| **Total** | $\frac{n(n+1)}{2} + 1$ | |

Concrete values:

| Dimension | Rotation DOF | Translation DOF | Scale DOF | Total |
|-----------|-------------|-----------------|-----------|-------|
| 2D | 1 | 2 | 1 | **4** |
| 3D | 3 | 3 | 1 | **7** |
| 4D | 6 | 4 | 1 | **11** |
| $n$D | $\frac{n(n-1)}{2}$ | $n$ | 1 | $\frac{n(n+1)}{2} + 1$ |

### The Transform Hierarchy

Geometric transforms form a strict inclusion chain. Each level relaxes one constraint and loses one invariant:

```
                    What it preserves
                    ─────────────────────────────────────────────
  Rigid             Distances, angles, parallelism, cross-ratio
  (Isometry)        s = 1, R orthogonal, t free
       ⊂
  Similarity        Angles, distance ratios, parallelism, cross-ratio
                    s free, R orthogonal, t free
       ⊂
  Affine            Parallelism, distance ratios on lines, cross-ratio
                    General invertible linear A (non-uniform scale,
                    shear allowed), t free
       ⊂
  Projective        Cross-ratio only
                    General invertible homogeneous matrix
                    (perspective allowed)
```

A quick reference of what is preserved and what is lost at each level:

```
  Preserved?        Rigid   Similarity   Affine   Projective
  ─────────────     ─────   ──────────   ──────   ──────────
  Distances           Y         N           N          N
  Angles              Y         Y           N          N
  Parallelism         Y         Y           Y          N
  Straight lines      Y         Y           Y          Y
  Cross-ratio         Y         Y           Y          Y
```

### How Uniform Scale Distinguishes Similarity from Rigid

The single parameter that separates a similarity from an isometry is the uniform scale factor $s$. "Uniform" means the same multiplier applies in every direction -- a circle maps to a circle (never an ellipse), a square maps to a square (never a rectangle). The moment you allow different scale factors along different axes, you step into the affine group, which can shear and stretch shapes.

In matrix form, compare:

```
  Rigid (isometry):          Similarity:              Affine:
  ┌         ┐                ┌           ┐            ┌           ┐
  │  R   t  │                │  sR    t  │            │  A     t  │
  │  0   1  │                │  0     1  │            │  0     1  │
  └         ┘                └           ┘            └           ┘
  R in SO(n)                 s > 0, R in SO(n)        A invertible
  6 DOF (3D)                 7 DOF (3D)               12 DOF (3D)
```

### N-Dimensional Generalization

Everything above works identically in any dimension $n \geq 1$. The rotation group $SO(n)$ has dimension $\frac{n(n-1)}{2}$ because rotations in $n$-space are specified by choosing a 2D plane (there are $\binom{n}{2}$ of them) and an angle in each. The full similarity group $\text{Sim}(n)$ is the semidirect product:

$$\text{Sim}(n) = (\mathbb{R}^+ \times SO(n)) \ltimes \mathbb{R}^n$$

This group acts transitively on the space of all oriented, scaled frames in $\mathbb{R}^n$.

### Estimating a Similarity Transform: Umeyama's Method

Given two sets of $m$ corresponding points $\{\mathbf{p}_i\}$ and $\{\mathbf{q}_i\}$ in $\mathbb{R}^n$, the goal is to find $s$, $R$, $\mathbf{t}$ minimizing:

$$\sum_{i=1}^{m} \| \mathbf{q}_i - (sR\mathbf{p}_i + \mathbf{t}) \|^2$$

Umeyama's algorithm (1991) solves this in closed form:

1. **Center the points:** $\bar{\mathbf{p}} = \frac{1}{m}\sum \mathbf{p}_i$, $\bar{\mathbf{q}} = \frac{1}{m}\sum \mathbf{q}_i$
2. **Compute the [[quick-context/covariance-matrix|cross-covariance matrix]]:** $H = \frac{1}{m}\sum (\mathbf{p}_i - \bar{\mathbf{p}})(\mathbf{q}_i - \bar{\mathbf{q}})^T$
3. **[[quick-context/singular-value-decomposition|SVD]] of $H$:** $H = U \Sigma V^T$
4. **Correct for reflections:** $S = \text{diag}(1, 1, \ldots, \text{sign}(\det(UV^T)))$
5. **Rotation:** $R = V S U^T$
6. **Scale:** $s = \frac{\text{tr}(\Sigma S)}{\sigma_p^2}$, where $\sigma_p^2 = \frac{1}{m}\sum \|\mathbf{p}_i - \bar{\mathbf{p}}\|^2$
7. **Translation:** $\mathbf{t} = \bar{\mathbf{q}} - sR\bar{\mathbf{p}}$

The reflection-correction step (step 4) is Umeyama's key contribution -- earlier SVD-based methods (Arun et al., 1987) could produce improper rotations (reflections) when point data was noisy or nearly coplanar.

</details>

<details>
<summary><strong>The Key Tension</strong> -- Similarity vs affine: when is uniform scale not enough?</summary>

The fundamental tradeoff is **model simplicity vs modeling power**.

| Factor | Similarity | Affine |
|--------|-----------|--------|
| DOF (3D) | 7 | 12 |
| Min. point correspondences (3D) | 3 (non-collinear) | 4 (non-coplanar) |
| Preserves angles | Yes | No |
| Preserves parallelism | Yes | Yes |
| Handles non-uniform scale / shear | No | Yes |
| Robustness to noise | Higher (fewer params) | Lower (more params to estimate) |
| Overfitting risk | Lower | Higher |

**When similarity suffices:**
- Aligning two views of the same rigid object measured at different scales (e.g., a laser scan vs a photogrammetric model)
- Registering coordinate systems in geodesy (the [[quick-context/helmert-transform|Helmert transform]] is exactly this)
- Comparing biological shapes in morphometrics where growth is roughly isotropic
- Any [[quick-context/absolute-orientation|absolute orientation]] problem where the objects are known to be geometrically similar

**When you need affine (or beyond):**
- Satellite imagery with different sensor geometries introducing directional scale differences
- Tissue deformation in medical imaging (organs stretch non-uniformly)
- Texture mapping where perspective foreshortening creates directional compression
- Any scenario where the physical process introduces shear or anisotropic scaling

**The practitioner's rule of thumb:** Start with similarity. If the residuals after fitting show a systematic directional pattern (e.g., errors are consistently larger along one axis), upgrade to affine. Going straight to affine when similarity would suffice wastes degrees of freedom on noise.

</details>

<details>
<summary><strong>Concrete Example</strong> -- What this looks like in practice</summary>

### 2D Example with Numbers

Suppose we have a triangle with vertices:

```
  Source points:         Target points (rotated 30deg, scaled 2x, shifted):
  P1 = (0, 0)           Q1 = (1, 1)
  P2 = (1, 0)           Q2 = (1 + sqrt(3), 2)
  P3 = (0, 1)           Q3 = (0, 1 + sqrt(3))
```

The true transform parameters are $s = 2$, $\theta = 30°$, $\mathbf{t} = (1, 1)$:

$$R = \begin{pmatrix} \cos 30° & -\sin 30° \\ \sin 30° & \cos 30° \end{pmatrix} = \begin{pmatrix} 0.866 & -0.5 \\ 0.5 & 0.866 \end{pmatrix}$$

Verify: $T(\mathbf{P_1}) = 2R(0,0)^T + (1,1)^T = (1, 1) = \mathbf{Q_1}$ ✓

### Python Implementation (Umeyama's Method, N-Dimensional)

```python
import numpy as np

def umeyama(src, dst):
    """
    Estimate N-dimensional similarity transform via Umeyama's method.

    Parameters
    ----------
    src : (m, n) array -- m source points in n dimensions
    dst : (m, n) array -- m destination points in n dimensions

    Returns
    -------
    s : float        -- uniform scale factor
    R : (n, n) array -- rotation matrix
    t : (n,) array   -- translation vector

    The transform maps src to dst:  dst_hat = s * (src @ R.T) + t
    """
    m, n = src.shape
    assert src.shape == dst.shape

    # Step 1: Center the points
    mu_src = src.mean(axis=0)
    mu_dst = dst.mean(axis=0)
    src_c = src - mu_src
    dst_c = dst - mu_dst

    # Step 2: Variance of source points
    var_src = np.sum(src_c ** 2) / m

    # Step 3: Cross-covariance matrix
    H = (dst_c.T @ src_c) / m          # (n x n)

    # Step 4: SVD
    U, D, Vt = np.linalg.svd(H)        # H = U @ diag(D) @ Vt

    # Step 5: Correct for reflection
    S = np.eye(n)
    if np.linalg.det(U) * np.linalg.det(Vt) < 0:
        S[-1, -1] = -1

    # Step 6: Rotation, scale, translation
    R = U @ S @ Vt
    s = np.trace(np.diag(D) @ S) / var_src
    t = mu_dst - s * (R @ mu_src)

    return s, R, t


# --- Demo: 2D triangle ---
src = np.array([[0.0, 0.0],
                [1.0, 0.0],
                [0.0, 1.0]])

# True transform: scale=2, rotate 30deg, translate (1,1)
theta = np.radians(30)
R_true = np.array([[np.cos(theta), -np.sin(theta)],
                   [np.sin(theta),  np.cos(theta)]])
s_true, t_true = 2.0, np.array([1.0, 1.0])
dst = s_true * (src @ R_true.T) + t_true

# Add a little noise to make it realistic
rng = np.random.default_rng(42)
dst_noisy = dst + rng.normal(scale=0.01, size=dst.shape)

s_est, R_est, t_est = umeyama(src, dst_noisy)
print(f"Scale:       {s_est:.4f}  (true: {s_true})")
print(f"Rotation:\n{R_est}")
print(f"Translation: {t_est}  (true: {t_true})")
# Output:
# Scale:       2.0130  (true: 2.0)
# Rotation:
# [[ 0.8612 -0.5082]
#  [ 0.5082  0.8612]]
# Translation: [1.0041 0.9871]  (true: [1. 1.])
```

### Generalizing to 3D

The same function works for 3D (or any dimension) -- just pass $(m \times 3)$ arrays. A 3D similarity has 7 DOF, so you need at least 3 non-collinear point correspondences. This is exactly the [[quick-context/absolute-orientation|absolute orientation]] problem: given matched 3D landmarks in two coordinate frames, recover the 7-parameter similarity relating them.

```python
# 3D example: 10 random points, scale=1.5, arbitrary rotation, shift
src_3d = rng.standard_normal((10, 3))
R_3d, _ = np.linalg.qr(rng.standard_normal((3, 3)))  # random rotation
if np.linalg.det(R_3d) < 0:
    R_3d[:, -1] *= -1
s_3d, t_3d = 1.5, np.array([10.0, -5.0, 3.0])
dst_3d = s_3d * (src_3d @ R_3d.T) + t_3d

s_hat, R_hat, t_hat = umeyama(src_3d, dst_3d)
print(f"\n3D scale: {s_hat:.6f}  (true: {s_3d})")
print(f"Rotation error (Frobenius): {np.linalg.norm(R_hat - R_3d):.2e}")
print(f"Translation error: {np.linalg.norm(t_hat - t_3d):.2e}")
```

**The one thing most outsiders get wrong about this is...** confusing a *geometric* similarity transform with a *matrix* similarity transform ($A' = P^{-1}AP$). They share the name but are completely different operations. The geometric version maps points in Euclidean space preserving shape. The matrix version is a change of basis that preserves eigenvalues. When someone says "similarity transform" in a linear algebra textbook, they almost always mean the matrix kind; in computer vision, geodesy, or shape analysis, they almost always mean the geometric kind.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> -- Related topics to explore</summary>

- **[[quick-context/helmert-transform|Helmert Transform]]** -- The 7-parameter 3D similarity transform used in geodesy to convert between coordinate datums (WGS 84, NAD 83, etc.)
- **[[quick-context/absolute-orientation|Absolute Orientation]]** -- The problem of recovering a similarity (or rigid) transform from matched 3D point pairs; Umeyama's method is a standard solution
- **[[quick-context/singular-value-decomposition|Singular Value Decomposition]]** -- The computational engine behind Umeyama's method; decomposes the cross-[[learning/notes/quick-context/covariance-matrix|covariance matrix]] to extract rotation
- **[[quick-context/covariance-matrix|Covariance Matrix]]** -- The cross-covariance between source and destination points encodes the rotation and scale information that SVD extracts
- **Quaternion methods** -- Unit quaternions offer an alternative parameterization of 3D rotations; Horn's method (1987) solves [[learning/notes/quick-context/absolute-orientation|absolute orientation]] via a quaternion eigenproblem instead of SVD
- **Lie groups** -- The similarity group $\text{Sim}(n)$ is a Lie group; its Lie algebra $\mathfrak{sim}(n)$ parameterizes infinitesimal similarities, useful for optimization on the group manifold
- **RANSAC** -- When point correspondences contain outliers, RANSAC wraps around Umeyama to robustly estimate the similarity transform from a minimal sample

</details>

<details>
<summary><strong>Test Your Understanding</strong> -- 5 progressive questions</summary>

**Q1:** A similarity transform has 7 DOF in 3D. What are they, and how many come from each component?
<details>
<summary>Answer</summary>
3 from rotation (three independent angles or axis-angle parameters), 3 from translation (one shift per axis), and 1 from uniform scale. Total: $3 + 3 + 1 = 7$. In general, $\frac{n(n+1)}{2} + 1$. See: How It Works, "Degrees of Freedom in N Dimensions."
</details>

**Q2:** Why does a similarity transform preserve angles but not distances?
<details>
<summary>Answer</summary>
The rotation $R$ preserves both angles and distances. The translation $\mathbf{t}$ preserves both (it is just a shift). The uniform scale $s$ multiplies *all* distances by the same factor -- so ratios of distances and all angles are unchanged, but absolute distances are scaled by $s$. Since angles depend only on direction (ratios), they survive scaling. See: How It Works, "The Transform Hierarchy."
</details>

**Q3:** You fit a similarity transform to align two point clouds and notice the residuals are 3x larger along the Z-axis than along X and Y. What does this suggest, and what should you try next?
<details>
<summary>Answer</summary>
Systematic directional residuals suggest the true relationship between the point clouds includes non-uniform scaling or shear -- something a similarity transform cannot model. You should upgrade to an affine transform (12 DOF in 3D), which allows independent scale factors along each axis. If the affine fit's residuals are still patterned, consider whether there is lens distortion or non-linear deformation. See: The Key Tension.
</details>

**Q4:** Someone claims: "I only have 2 point correspondences in 3D, but that gives me 6 equations (2 points times 3 coordinates), which is enough to solve for 7 DOF if I add one more constraint." What is wrong with this reasoning?
<details>
<summary>Answer</summary>
Two points in 3D define a line segment, which constrains 6 of the 7 DOF: 3 translations (from matching one endpoint), 1 scale (from the distance ratio), and 2 rotations (aligning the line direction in 3D space requires specifying two angles). The remaining 1 DOF corresponds to arbitrary rotation *around* that line. No single algebraic constraint can substitute for the geometric information that a third non-collinear point provides -- you need a point off the line to pin down that last rotational DOF. You need at least 3 non-collinear correspondences. See: Concrete Example, "Generalizing to 3D."
</details>

**Q5:** In Umeyama's method, step 4 checks $\det(UV^T)$ and potentially flips the sign of the last diagonal entry. What would happen if you skipped this step, and under what geometric conditions does it matter?
<details>
<summary>Answer</summary>
Without the reflection correction, the SVD solution minimizes the least-squares cost but may return an improper rotation (a reflection, $\det(R) = -1$) instead of a proper rotation ($\det(R) = +1$). This happens when the point data is nearly coplanar (or nearly collinear in 2D), heavily noisy, or when the smallest singular value of $H$ is close to zero -- the SVD "flips" the weakest axis because the cost function barely distinguishes the two orientations. In practice this would produce a mirror-image alignment that is geometrically nonsensical. Umeyama's correction guarantees a proper rotation by absorbing the sign flip into the scale computation. See: How It Works, "Estimating a Similarity Transform: Umeyama's Method."
</details>

</details>
