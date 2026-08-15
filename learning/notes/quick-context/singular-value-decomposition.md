---
topic: "Singular Value Decomposition (SVD)"
created: 2026-04-04
---

# Singular Value Decomposition (SVD)

> **Related:** [[quick-context/helmert-transform|Helmert Transform]] | [[quick-context/covariance-matrix|Covariance Matrix]] | [[quick-context/absolute-orientation|Absolute Orientation]] | [[quick-context/similarity-transform|Similarity Transform]]

> **TL;DR:** SVD factorizes any $m \times n$ matrix into $U\Sigma V^T$ -- three matrices revealing the geometry of the linear map as a rotation, a scaling along orthogonal axes, and another rotation. It's the Swiss Army knife of linear algebra.

## The Core Problem

Every matrix encodes a linear transformation, but looking at the raw numbers tells you almost nothing about *what that transformation does geometrically*. Is it stretching space? Rotating it? Collapsing dimensions? SVD answers all of these by decomposing any matrix -- any shape, any rank -- into its anatomical parts: the directions it acts on, how much it stretches along each, and where those stretched directions end up. Without SVD, problems like finding optimal rotations between point clouds, computing stable pseudoinverses, or compressing data by discarding negligible dimensions would require ad-hoc solutions instead of one universal tool.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Singular values** | The non-negative diagonal entries $\sigma_1 \geq \sigma_2 \geq \dots \geq \sigma_r > 0$ of $\Sigma$; they quantify how much the transformation stretches space along each principal axis |
| **Left singular vectors** | The columns of $U$ -- an orthonormal set of vectors spanning the output (column) space; they are the directions the stretched axes land on |
| **Right singular vectors** | The columns of $V$ -- an orthonormal set of vectors spanning the input (row) space; they are the directions the transformation acts on before stretching |
| **Rank** | The number of non-zero singular values; it tells you the true dimensionality of the transformation's image and determines how many independent equations a system really contains |
| **Pseudoinverse** | The Moore-Penrose pseudoinverse $A^+ = V\Sigma^+ U^T$, computed by inverting the non-zero singular values; it gives the best least-squares solution to overdetermined or rank-deficient systems |

<details>
<summary><strong>How It Works</strong> -- The essential mechanism</summary>

### The Decomposition

Any real $m \times n$ matrix $A$ can be factored as:

$$A = U \Sigma V^T$$

where:
- $U$ is an $m \times m$ orthogonal matrix (left singular vectors)
- $\Sigma$ is an $m \times n$ diagonal matrix (singular values on the diagonal)
- $V$ is an $n \times n$ orthogonal matrix (right singular vectors)

### Geometric Interpretation: Rotate, Stretch, Rotate

The key insight is that *every* linear transformation -- no matter how complicated -- is just a rotation, followed by axis-aligned stretching, followed by another rotation.

```
  Input space                                Output space

       y                                          y
       |  v2                                      |  u2
       | /                                        | /
       |/                                         |/
  ─────+──────── x                           ─────+──────── x
       |    v1 ──>                                |    u1 ──>


  Step 1: V^T          Step 2: Sigma          Step 3: U
  (rotate to align     (stretch along         (rotate from
   principal axes)      each axis)             axes to final
                                               orientation)

        V^T                  Sigma                   U
  ┌──────────────┐    ┌────────────────┐    ┌──────────────┐
  │              │    │ sigma1    0    │    │              │
  │   Rotation   │ ──>│   0    sigma2  │ ──>│   Rotation   │
  │   (rigid)    │    │                │    │   (rigid)    │
  └──────────────┘    └────────────────┘    └──────────────┘
```

**What happens to the unit circle:**

```
  1. Start: unit circle    2. V^T: still a circle   3. Sigma: ellipse
                              (rotation preserves      (axes stretched
                               shape)                   by sigma1, sigma2)

         ____                      ____
       /      \                  /      \            ___________________
      |        |                |        |          /                   \
      |   .    |                |   .    |         |         .          |
      |        |                |        |          \___________________/
       \______/                  \______/
                                                    semi-axes = sigma1, sigma2
      radius = 1               radius = 1

  4. U: rotated ellipse
     (rigid rotation of
      the ellipse to its
      final position)

          ______
        /        \
       /          \
      |      .     |
       \          /
        \________/
```

The singular values $\sigma_1, \sigma_2, \dots$ are the semi-axis lengths of the ellipse (or hyper-ellipsoid in higher dimensions) that the unit sphere gets mapped to.

### Connection to Eigendecomposition

For a **symmetric** matrix $A = A^T$, the SVD and eigendecomposition coincide:
- The singular values are the absolute values of the eigenvalues: $\sigma_i = |\lambda_i|$
- $U = V$ (up to sign flips for negative eigenvalues)

For a **general** (non-symmetric) matrix, eigendecomposition may not even exist (non-square matrices have no eigenvalues), but SVD always does. SVD is strictly more general.

The relationship: $A^T A = V \Sigma^T \Sigma V^T$ is the eigendecomposition of $A^T A$, so the right singular vectors are eigenvectors of $A^T A$ and the squared singular values are its eigenvalues.

### Compact vs Full SVD

| Form | $U$ size | $\Sigma$ size | $V$ size | When to use |
|------|----------|---------------|----------|-------------|
| **Full** | $m \times m$ | $m \times n$ | $n \times n$ | Theoretical derivations, null space computation |
| **Compact (thin)** | $m \times r$ | $r \times r$ | $n \times r$ | Practical computation -- discards zero singular values |
| **Truncated** | $m \times k$ | $k \times k$ | $n \times k$ | Low-rank approximation -- keeps only $k$ largest singular values |

where $r = \text{rank}(A)$ and $k < r$.

### SVD in the Helmert Transform Context

In the [[quick-context/helmert-transform|Helmert Transform]] and [[quick-context/absolute-orientation|absolute orientation]] problem, you compute the [[quick-context/covariance-matrix|cross-covariance matrix]] $H$ between two centered point sets, then decompose it:

$$H = U \Sigma V^T$$

The optimal rotation is then:

$$R = V U^T$$

**Why this works:** $VU^T$ is the closest orthogonal matrix to $H$ in the Frobenius norm. This is equivalent to the polar decomposition of $H$ -- stripping away the stretching and keeping only the rotation.

**The reflection trap:** If $\det(VU^T) = -1$, you've found a reflection, not a rotation. The fix is to negate the column of $V$ corresponding to the smallest singular value:

$$R = V \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & \det(VU^T) \end{pmatrix} U^T$$

This is the Kabsch-Umeyama algorithm, and it guarantees a proper rotation ($\det(R) = +1$).

</details>

<details>
<summary><strong>The Key Tension</strong> -- Computational cost vs universality</summary>

SVD's universality comes at a price: it is one of the most expensive matrix decompositions.

| Decomposition | Cost | What it gives you |
|---------------|------|-------------------|
| **LU** | $O(2n^3 / 3)$ | Solves $Ax = b$ for square, full-rank $A$ |
| **QR** | $O(2n^3 / 3)$ | Least squares, orthogonal basis |
| **SVD** | $O(4n^3 / 3)$ to $O(11n^3)$ | Everything: rank, pseudoinverse, low-rank approx, condition number |

For an $m \times n$ matrix, the full SVD costs roughly $O(mn^2)$ when $m \geq n$ (Golub-Kahan bidiagonalization followed by QR iteration). This is typically 2--4x more expensive than QR alone.

**The practitioner's tradeoff:**
- **When SVD is overkill:** If you just need to solve $Ax = b$ and $A$ is well-conditioned and square, use LU or QR. Don't reach for SVD.
- **When SVD is essential:** If $A$ might be rank-deficient, if you need the pseudoinverse, if you want to know the condition number, or if you need the best rank-$k$ approximation, SVD is the only tool that handles all of these correctly.

**Truncated SVD for dimensionality reduction:** By the Eckart-Young-Mirsky theorem, the best rank-$k$ approximation to $A$ (in both the Frobenius norm and the spectral norm) is:

$$A_k = U_k \Sigma_k V_k^T = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$

This is the theoretical foundation behind Principal Component Analysis (PCA), latent semantic analysis, and image compression. You keep only the $k$ largest singular values and discard the rest, optimally compressing the matrix.

**Randomized SVD:** For very large matrices where even $O(mn^2)$ is too slow, randomized algorithms (Halko, Martinsson, Tropp 2011) compute an approximate truncated SVD in $O(mnk)$ time, where $k \ll \min(m,n)$.

**Numerical algorithm:** The standard method is the Golub-Kahan bidiagonalization followed by an iterative phase:
1. Reduce $A$ to upper bidiagonal form $B$ using Householder reflections: $U_1^T A V_1 = B$
2. Compute SVD of $B$ -- LAPACK offers two approaches: QR iteration (`dgesvd`, the Golub-Reinsch algorithm) or divide-and-conquer (`dgesdd`, the Gu-Eisenstat algorithm, which can be an order of magnitude faster for large matrices)
3. Accumulate the transformations: $U = U_1 U_B$, $V = V_1 V_B$

</details>

<details>
<summary><strong>Concrete Example</strong> -- Worked SVD and Helmert rotation extraction</summary>

### Small Matrix SVD

Consider the $2 \times 2$ matrix:

$$A = \begin{pmatrix} 3 & 2 \\ 2 & 3 \end{pmatrix}$$

**By hand:** $A^T A = \begin{pmatrix} 13 & 12 \\ 12 & 13 \end{pmatrix}$. Eigenvalues: $\lambda_1 = 25, \lambda_2 = 1$. So $\sigma_1 = 5, \sigma_2 = 1$.

Eigenvectors of $A^T A$: $\mathbf{v}_1 = \frac{1}{\sqrt{2}}(1,1)^T$, $\mathbf{v}_2 = \frac{1}{\sqrt{2}}(-1,1)^T$.

Then $\mathbf{u}_i = \frac{1}{\sigma_i} A \mathbf{v}_i$ gives:
$\mathbf{u}_1 = \frac{1}{\sqrt{2}}(1,1)^T$, $\mathbf{u}_2 = \frac{1}{\sqrt{2}}(-1,1)^T$.

$$A = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix} \begin{pmatrix} 5 & 0 \\ 0 & 1 \end{pmatrix} \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ -1 & 1 \end{pmatrix}$$

**Geometric meaning:** $A$ rotates by 45 degrees, stretches by 5 along one axis and 1 along the other, then rotates back by 45 degrees. The unit circle becomes an ellipse with semi-axes 5 and 1, tilted at 45 degrees.

### NumPy SVD

```python
import numpy as np

# Basic SVD
A = np.array([[3, 2],
              [2, 3]])
U, sigma, Vt = np.linalg.svd(A)

print("U =\n", U)
print("Sigma =", sigma)     # [5. 1.]
print("V^T =\n", Vt)

# Reconstruct: A = U @ diag(sigma) @ Vt
A_reconstructed = U @ np.diag(sigma) @ Vt
print("Reconstruction error:", np.linalg.norm(A - A_reconstructed))  # ~0.0
```

### Helmert Rotation Extraction (Kabsch Algorithm)

Given two sets of 3D points (source and target), find the optimal rotation:

```python
import numpy as np

# Source and target points (already centered at their centroids)
P = np.array([[ 1.0,  0.0,  0.0],    # source points (3 x 3)
              [ 0.0,  1.0,  0.0],
              [ 0.0,  0.0,  1.0]])

# Target: source rotated ~30 deg around z-axis (plus some noise)
theta = np.radians(30)
R_true = np.array([[ np.cos(theta), -np.sin(theta), 0],
                   [ np.sin(theta),  np.cos(theta), 0],
                   [ 0,              0,             1]])

Q = (R_true @ P.T).T + np.random.normal(0, 0.01, P.shape)  # noisy target

# Step 1: Compute cross-covariance matrix
H = P.T @ Q  # 3x3 matrix

# Step 2: SVD of H
U, S, Vt = np.linalg.svd(H)

# Step 3: Rotation with reflection check
d = np.linalg.det(Vt.T @ U.T)
D = np.diag([1, 1, np.sign(d)])   # correction matrix
R_estimated = Vt.T @ D @ U.T

print("True rotation:\n", R_true)
print("Estimated rotation:\n", R_estimated)
print("det(R) =", np.linalg.det(R_estimated))  # Should be +1.0
print("Rotation error:", np.linalg.norm(R_true - R_estimated))
```

**Note:** `np.linalg.svd` returns $V^T$ (not $V$), so the rotation formula becomes `Vt.T @ D @ U.T` rather than `V @ D @ U.T`. This is the most common source of bugs.

**The one thing most outsiders get wrong about this is...** that SVD finds the rotation by "decomposing" the rotation matrix. It doesn't. The [[quick-context/covariance-matrix|cross-covariance matrix]] $H$ is not a rotation matrix -- it encodes how the source and target coordinates co-vary. SVD decomposes *that* matrix into its rotation and stretching components, and by discarding the stretching ($\Sigma$) and recombining the two rotations ($VU^T$), you recover the rotation that best aligns the two point sets in the least-squares sense. The stretching you throw away represents the noise and scale mismatch in the data.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> -- Related topics to explore</summary>

- **[[quick-context/helmert-transform|Helmert Transform]]** -- Uses SVD to extract the optimal rotation matrix from the cross-[[learning/notes/quick-context/covariance-matrix|covariance matrix]] of corresponding point sets
- **[[quick-context/similarity-transform|Similarity Transform]]** -- SVD helps estimate the rotation component of a similarity transform (rotation + scale + translation)
- **[[quick-context/absolute-orientation|Absolute Orientation]]** -- The SVD-based Kabsch-Umeyama method is one of three main approaches to solving the absolute orientation problem
- **[[quick-context/covariance-matrix|Covariance Matrix]]** -- SVD of the cross-covariance matrix is central to point cloud alignment; SVD of the covariance matrix yields PCA
- **Principal Component Analysis (PCA)** -- PCA is SVD applied to the centered data matrix; the principal components are the right singular vectors, and the explained variance comes from the squared singular values
- **Polar decomposition** -- Every matrix factors as $A = QS$ (orthogonal times symmetric positive semi-definite); SVD gives you this directly since $Q = UV^T$ and $S = V\Sigma V^T$
- **Condition number** -- $\kappa(A) = \sigma_1 / \sigma_r$, the ratio of largest to smallest singular value; measures how sensitive $Ax = b$ is to perturbations
- **Eckart-Young-Mirsky theorem** -- Proves that the truncated SVD gives the optimal low-rank matrix approximation in both Frobenius and spectral norms
- **Moore-Penrose pseudoinverse** -- Computed via SVD as $A^+ = V\Sigma^+ U^T$; generalizes matrix inversion to non-square and rank-deficient matrices
- **Procrustes analysis** -- The statistical version of the [[learning/notes/quick-context/absolute-orientation|absolute orientation]] problem; SVD provides the optimal orthogonal transformation between shape configurations

</details>

<details>
<summary><strong>Test Your Understanding</strong> -- 5 progressive questions</summary>

**Q1:** A $4 \times 3$ matrix has singular values $\sigma_1 = 7$, $\sigma_2 = 3$, $\sigma_3 = 0$. What is the rank of the matrix, and what does the zero singular value tell you geometrically?
<details>
<summary>Answer</summary>
The rank is 2 (number of non-zero singular values). Geometrically, the zero singular value means the transformation collapses one dimension entirely -- the 3D input space is squashed into a 2D subspace in the output. The unit sphere in $\mathbb{R}^3$ gets mapped to an ellipse (not an ellipsoid) in $\mathbb{R}^4$ with semi-axes of length 7 and 3. See: How It Works, the geometric interpretation section.
</details>

**Q2:** Why can't you use eigendecomposition instead of SVD to factorize a $5 \times 3$ matrix?
<details>
<summary>Answer</summary>
Eigendecomposition requires a square matrix (it solves $A\mathbf{v} = \lambda\mathbf{v}$, which only makes sense when $A$ maps a space to itself). A $5 \times 3$ matrix maps $\mathbb{R}^3$ to $\mathbb{R}^5$ -- these are different spaces, so eigenvalues are undefined. SVD handles rectangular matrices by using *two* sets of orthogonal vectors ($U$ for the output space, $V$ for the input space) instead of one. See: How It Works, connection to eigendecomposition.
</details>

**Q3:** In the Kabsch algorithm, you compute $R = VU^T$ from the SVD of the cross-covariance matrix $H$. Why do you multiply $V$ and $U^T$ rather than, say, $UV^T$ or some other combination?
<details>
<summary>Answer</summary>
The SVD gives $H = U\Sigma V^T$. The matrix $H$ encodes the correlation between source and target coordinates. The optimal rotation must map the principal directions of the source (captured by $V$) to the principal directions of the target (captured by $U$). Since $VU^T = V(U^T)$ composes "rotate from standard axes to source directions" with "rotate from target directions to standard axes," the product $VU^T$ is the rotation from source to target. The alternative $UV^T$ would give the transpose (inverse) rotation. The $\Sigma$ is discarded because it only encodes stretching magnitudes, not direction. See: How It Works, SVD in the [[learning/notes/quick-context/helmert-transform|Helmert Transform]] context.
</details>

**Q4:** You compute $R = VU^T$ and get $\det(R) = -1$. Someone suggests "just negate $R$." Why is this wrong, and what is the correct fix?
<details>
<summary>Answer</summary>
Negating $R$ gives $\det(-R) = (-1)^3 \det(R) = -1 \cdot (-1) = +1$ in 3D, so the determinant would be correct, but $-R$ is not the *closest* proper rotation to $H$ -- it's a 180-degree rotation away from the optimal solution. The correct fix is to negate only the column of $V$ corresponding to the smallest singular value (equivalently, multiply by $D = \text{diag}(1, 1, \det(VU^T))$). This makes the minimal possible change to the solution, flipping only the least-significant direction, which preserves the optimality of the fit. See: How It Works, the reflection trap.
</details>

**Q5:** A colleague is compressing a $1000 \times 1000$ image matrix using truncated SVD with rank $k = 50$. They claim this stores $50 \times 1000 + 50 + 50 \times 1000 = 100{,}050$ numbers instead of $1{,}000{,}000$. Is this correct? When would truncated SVD be a *poor* choice for compression compared to other methods?
<details>
<summary>Answer</summary>
The storage count is correct: you store $U_k$ ($1000 \times 50$), $\sigma_1 \dots \sigma_{50}$ (50 values), and $V_k$ ($1000 \times 50$), totaling $100{,}050$ numbers -- roughly 10x compression. However, truncated SVD is a poor choice when: (1) the singular values decay slowly (all are similar magnitude), meaning you can't discard many without significant error -- this happens with high-frequency or noisy images; (2) the data has local structure that block-based methods (like JPEG's DCT) exploit better; (3) the matrix is sparse, where sparse storage formats beat SVD; (4) you need to compress/decompress quickly, since SVD computation itself costs $O(mn \cdot k)$ which is far more expensive than transform-coding methods. SVD gives the mathematically optimal rank-$k$ approximation (Eckart-Young theorem), but "optimal in Frobenius norm" doesn't always mean "best perceptual quality." See: The Key Tension, truncated SVD and Eckart-Young-Mirsky theorem.
</details>

</details>
