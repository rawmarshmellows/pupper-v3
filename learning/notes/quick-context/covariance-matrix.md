---
topic: Covariance Matrix
created: 2026-04-04
---

# Covariance Matrix

> **Related:** [[quick-context/helmert-transform|Helmert Transform]] | [[quick-context/absolute-orientation|Absolute Orientation]] | [[quick-context/singular-value-decomposition|Singular Value Decomposition]] | [[quick-context/similarity-transform|Similarity Transform]]

> **TL;DR:** A covariance matrix captures how pairs of variables move together -- its diagonal holds variances and its off-diagonals hold covariances. It's the fundamental object for understanding multivariate spread, correlation, and the basis for PCA, Mahalanobis distance, and point cloud alignment.

## The Core Problem

A single variable has variance -- one number that describes how spread out it is. But when you have two or more variables, variance alone is blind to their *relationships*. Two sensors might drift together, three GPS coordinates might be correlated through satellite geometry, or twelve point-cloud dimensions might cluster along a hidden axis. The covariance matrix is the minimal structure that captures all pairwise linear relationships in multivariate data. Without it, you cannot perform principal component analysis, compute Mahalanobis distance, estimate Kalman filter uncertainty, or solve the [[quick-context/absolute-orientation|absolute orientation]] problem.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Variance** | The expected squared deviation of a single variable from its mean: $\sigma^2 = E[(X - \mu)^2]$ -- the diagonal entries of a covariance matrix |
| **Covariance** | The expected product of deviations of two variables from their means: $\text{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)]$ -- the off-diagonal entries |
| **Positive semi-definite** | A matrix property guaranteeing $\mathbf{v}^T \Sigma \mathbf{v} \geq 0$ for all vectors $\mathbf{v}$ -- every covariance matrix must satisfy this because variance can never be negative |
| **Cross-covariance** | A covariance matrix between *two different* vectors $\mathbf{x}$ and $\mathbf{y}$, written $H = E[(\mathbf{x} - \bar{\mathbf{x}})(\mathbf{y} - \bar{\mathbf{y}})^T]$ -- not necessarily square or symmetric, and central to the [[quick-context/helmert-transform|Helmert transform]] |
| **Correlation matrix** | The covariance matrix normalized so every diagonal entry is 1: $R_{ij} = \Sigma_{ij} / (\sigma_i \sigma_j)$ -- strips out magnitude, leaving only the strength and direction of linear relationships |

<details>
<summary><strong>How It Works</strong> -- Building and interpreting covariance matrices</summary>

### Auto-covariance: one dataset, pairwise structure

Given $n$ observations of a $p$-dimensional vector $\mathbf{x}$, the sample covariance matrix is:

$$\Sigma = \frac{1}{n-1} \sum_{i=1}^{n} (\mathbf{x}_i - \bar{\mathbf{x}})(\mathbf{x}_i - \bar{\mathbf{x}})^T$$

This produces a $p \times p$ symmetric matrix. The $(j,k)$ entry is the covariance between the $j$-th and $k$-th variables. The diagonal entries are the variances.

### Cross-covariance: two datasets, correspondence structure

Given $n$ paired observations of vectors $\mathbf{x}$ (input) and $\mathbf{y}$ (output), the cross-covariance matrix is:

$$H = \sum_{i=1}^{n} (\mathbf{x}_i - \bar{\mathbf{x}})(\mathbf{y}_i - \bar{\mathbf{y}})^T$$

This is the matrix used in the [[quick-context/helmert-transform|Helmert transform]] and [[quick-context/absolute-orientation|Kabsch/absolute orientation algorithm]]. It is *not* necessarily symmetric and *not* necessarily square (if $\mathbf{x}$ and $\mathbf{y}$ have different dimensions). The [[quick-context/singular-value-decomposition|SVD]] of $H$ directly yields the optimal rotation matrix.

### Geometric interpretation: the covariance ellipsoid

The covariance matrix defines an ellipsoid in $p$-dimensional space. The eigenvectors of $\Sigma$ are the principal axes of this ellipsoid, and the eigenvalues are the variances along those axes. This is exactly what PCA extracts.

In 2D, the covariance matrix defines an ellipse. The shape of the ellipse tells you the correlation:

```
  High positive           Zero correlation          High negative
  correlation (r~0.9)     (r~0)                     correlation (r~-0.9)

             y                         y                         y
             | ...                  .......                  ... |
             |.. .                 ..  |  ..                 . ..|
             .. ..                 .   |   .                 .. ..
            .| ..                  .   |   .                  .. |.
  ---------.-+-.------- x   -------.---+---.----- x   ---------.-+-.------- x
          .. |.                    .   |   .                    .| ..
         .. ..                     .   |   .                     .. ..
         . ..|                     ..  |  ..                     |.. .
         ... |                      .......                      | ...
             |                         |                         |

  Ellipse tilted 45deg    Circle (equal var.)       Ellipse tilted -45deg
  Sigma = [1  .9]         Sigma = [1  0]            Sigma = [1  -.9]
          [.9  1]                 [0  1]                    [-.9  1]
```

### Connection to eigenvalues

Since $\Sigma$ is symmetric, the spectral theorem guarantees it has real eigenvalues $\lambda_1 \geq \lambda_2 \geq \dots \geq \lambda_p$ and orthogonal eigenvectors. These eigenvalues are the variances along the principal axes. PCA simply rotates the data so the axes align with these eigenvectors.

### Why positive semi-definite

For any vector $\mathbf{v}$, the quantity $\mathbf{v}^T \Sigma \mathbf{v}$ equals the variance of the linear combination $\mathbf{v}^T \mathbf{x}$. Variance cannot be negative, so $\mathbf{v}^T \Sigma \mathbf{v} \geq 0$ for all $\mathbf{v}$. This is the definition of positive semi-definiteness. It guarantees all eigenvalues are $\geq 0$, and the ellipsoid never has a "negative radius."

A covariance matrix is strictly positive *definite* (all eigenvalues > 0) when no variable is a perfect linear combination of the others. It becomes merely semi-definite (some eigenvalues = 0) when there is perfect linear dependency -- the ellipsoid collapses to a lower-dimensional ellipse.

</details>

<details>
<summary><strong>The Key Tension</strong> -- Sample vs population and the bias-variance tradeoff</summary>

### Bessel's correction: $n$ vs $n - 1$

| Estimator | Formula | Bias | When to use |
|-----------|---------|------|-------------|
| **Population covariance** | $\frac{1}{n} \sum (\mathbf{x}_i - \mu)(\mathbf{x}_i - \mu)^T$ | Unbiased (if $\mu$ is known) | When you have the entire population or the true mean is known |
| **Sample covariance** | $\frac{1}{n-1} \sum (\mathbf{x}_i - \bar{\mathbf{x}})(\mathbf{x}_i - \bar{\mathbf{x}})^T$ | Unbiased | When estimating from a sample (the standard case) |
| **MLE covariance** | $\frac{1}{n} \sum (\mathbf{x}_i - \bar{\mathbf{x}})(\mathbf{x}_i - \bar{\mathbf{x}})^T$ | Biased low | Maximum likelihood under Gaussian assumption |

The $n - 1$ denominator (Bessel's correction) accounts for the fact that using the sample mean $\bar{\mathbf{x}}$ instead of the true mean $\mu$ costs one degree of freedom. The sample points are, on average, slightly closer to $\bar{\mathbf{x}}$ than to $\mu$, so dividing by $n$ systematically underestimates the true variance. Dividing by $n - 1$ corrects this bias.

**Important caveat:** While $\frac{1}{n-1}$ gives an unbiased *variance* estimate, the square root of this is *not* an unbiased estimate of the standard deviation. And the unbiased estimator does not minimize mean squared error -- it trades MSE for zero bias.

### Sensitivity to outliers

Covariance is based on squared deviations, making it highly sensitive to outliers. A single extreme point can dominate the entire matrix. Robust alternatives include:

- **Minimum covariance determinant (MCD)** -- finds the subset of points with smallest determinant covariance
- **Ledoit-Wolf shrinkage** -- shrinks the sample covariance toward a structured target (e.g., diagonal matrix)
- **Median absolute deviation (MAD)** -- replaces variance with a robust scale estimator

### Cross-covariance: no Bessel's correction needed?

In the [[quick-context/helmert-transform|Helmert transform]] and [[quick-context/absolute-orientation|absolute orientation]] problem, the cross-covariance $H = \sum (\mathbf{x}_i - \bar{\mathbf{x}})(\mathbf{y}_i - \bar{\mathbf{y}})^T$ is typically written *without* the $\frac{1}{n-1}$ factor. This is because the rotation extracted via [[quick-context/singular-value-decomposition|SVD]] depends only on the *direction* of $H$'s singular vectors, not its magnitude. Scaling $H$ by a constant does not change the SVD's $U$ or $V$ matrices.

</details>

<details>
<summary><strong>Concrete Example</strong> -- Computing covariance by hand and with numpy</summary>

### Auto-covariance: 2D dataset

Consider 4 points in 2D:

| Point | $x$ | $y$ |
|-------|-----|-----|
| A | 2 | 4 |
| B | 4 | 6 |
| C | 6 | 7 |
| D | 8 | 9 |

**Step 1: Compute means**

$$\bar{x} = \frac{2 + 4 + 6 + 8}{4} = 5, \quad \bar{y} = \frac{4 + 6 + 7 + 9}{4} = 6.5$$

**Step 2: Center the data**

| Point | $x - \bar{x}$ | $y - \bar{y}$ |
|-------|----------------|----------------|
| A | -3 | -2.5 |
| B | -1 | -0.5 |
| C | 1 | 0.5 |
| D | 3 | 2.5 |

**Step 3: Compute covariance matrix entries** (using $n - 1 = 3$)

$$\sigma_{xx} = \frac{(-3)^2 + (-1)^2 + 1^2 + 3^2}{3} = \frac{20}{3} \approx 6.67$$

$$\sigma_{yy} = \frac{(-2.5)^2 + (-0.5)^2 + 0.5^2 + 2.5^2}{3} = \frac{13}{3} \approx 4.33$$

$$\sigma_{xy} = \frac{(-3)(-2.5) + (-1)(-0.5) + (1)(0.5) + (3)(2.5)}{3} = \frac{16}{3} \approx 5.33$$

$$\Sigma = \begin{bmatrix} 6.67 & 5.33 \\ 5.33 & 4.33 \end{bmatrix}$$

**Step 4: Verify with numpy**

```python
import numpy as np

data = np.array([[2, 4], [4, 6], [6, 7], [8, 9]])
cov = np.cov(data.T)  # np.cov uses n-1 by default
print(cov)
# [[6.667  5.333]
#  [5.333  4.333]]
```

The correlation coefficient is $r = 5.33 / \sqrt{6.67 \times 4.33} \approx 0.992$ -- strong positive correlation.

### Cross-covariance: Helmert transform setup

Two corresponding 3D point sets (input and output coordinates). Using axis-aligned points centered at the origin so the centroids are zero and the math stays clean:

```python
import numpy as np

# Input points (source coordinate system, centered at origin)
x_in = np.array([[ 1,  0,  0],
                  [-1,  0,  0],
                  [ 0,  1,  0],
                  [ 0, -1,  0],
                  [ 0,  0,  1],
                  [ 0,  0, -1]])

# Output points (target, rotated 90deg about z-axis)
# R_z(90) = [[0,-1,0],[1,0,0],[0,0,1]]
x_out = np.array([[ 0,  1,  0],
                   [ 0, -1,  0],
                   [-1,  0,  0],
                   [ 1,  0,  0],
                   [ 0,  0,  1],
                   [ 0,  0, -1]])

# Step 1: Centroids are both [0, 0, 0] -- already centered
# Step 2: Compute cross-covariance matrix H
H = x_in.T @ x_out
print(H)
# [[ 0  2  0]
#  [-2  0  0]
#  [ 0  0  2]]

# Step 3: SVD to extract rotation
U, S, Vt = np.linalg.svd(H)
d = np.linalg.det(Vt.T @ U.T)
D = np.diag([1, 1, d])  # Correct for reflection
R = Vt.T @ D @ U.T
print(R)
# [[ 0. -1.  0.]    <-- 90-degree rotation about z-axis
#  [ 1.  0.  0.]
#  [ 0.  0.  1.]]
```

The cross-covariance matrix $H$ encodes all the rotational information. The [[quick-context/singular-value-decomposition|SVD]] extracts it cleanly.

**The one thing most outsiders get wrong about this is...** confusing the auto-covariance matrix with the cross-covariance matrix. The auto-covariance $\Sigma$ describes the spread of a *single* dataset -- it is always symmetric and positive semi-definite. The cross-covariance $H$ describes the *correspondence* between two datasets -- it is generally not symmetric, not positive semi-definite, and not even necessarily square. In the [[quick-context/helmert-transform|Helmert transform]], it is the cross-covariance $H$ (not the auto-covariance $\Sigma$) that gets decomposed by SVD to find the rotation.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> -- Related topics to explore</summary>

- **[[quick-context/helmert-transform|Helmert Transform]]** -- Uses the cross-covariance matrix $H$ as the key input to SVD-based rotation estimation
- **[[quick-context/absolute-orientation|Absolute Orientation]]** -- The problem of finding the best rigid-body transform between two point sets, solved through cross-covariance + SVD
- **[[quick-context/singular-value-decomposition|Singular Value Decomposition]]** -- The decomposition $H = U\Sigma V^T$ that extracts rotation from the cross-covariance matrix
- **[[quick-context/similarity-transform|Similarity Transform]]** -- Extends the [[quick-context/helmert-transform|Helmert transform]] with scale; covariance is used in least-squares estimation of all parameters
- **Principal Component Analysis (PCA)** -- Eigendecomposition of the auto-covariance matrix yields the principal components; the dominant eigenvectors capture the most variance
- **Mahalanobis distance** -- Distance metric $d = \sqrt{(\mathbf{x} - \mu)^T \Sigma^{-1} (\mathbf{x} - \mu)}$ that accounts for covariance structure, used in outlier detection and Kalman filter gating
- **Kalman filter** -- Propagates a state estimate and its covariance matrix through time; the covariance matrix tracks uncertainty at every step
- **Correlation matrix** -- The standardized form of the covariance matrix where all diagonal entries equal 1; obtained by dividing each entry by the product of the marginal standard deviations

</details>

<details>
<summary><strong>Test Your Understanding</strong> -- 5 progressive questions</summary>

**Q1:** What does the $(i, j)$ entry of a covariance matrix represent, and what do the diagonal entries specifically tell you?
<details>
<summary>Answer</summary>
The $(i, j)$ entry is the covariance between variable $i$ and variable $j$ -- how much they tend to move together. The diagonal entries ($i = j$) are the variances of each individual variable. See: 5 Essential Terms.
</details>

**Q2:** Why must every covariance matrix be positive semi-definite? What would it mean physically if an eigenvalue were negative?
<details>
<summary>Answer</summary>
The quantity $\mathbf{v}^T \Sigma \mathbf{v}$ equals the variance of the linear combination $\mathbf{v}^T \mathbf{x}$. Variance is always $\geq 0$, so $\mathbf{v}^T \Sigma \mathbf{v} \geq 0$ for all $\mathbf{v}$. A negative eigenvalue would imply that some linear combination of your variables has negative variance -- which is impossible. If you encounter a "covariance matrix" with a negative eigenvalue, something has gone wrong numerically. See: How It Works.
</details>

**Q3:** In the Helmert transform, why can we omit the $\frac{1}{n-1}$ factor when computing the cross-covariance matrix $H$?
<details>
<summary>Answer</summary>
The rotation matrix is extracted from $H$ via SVD: $H = U\Sigma V^T$, and $R = V D U^T$. The singular vectors $U$ and $V$ depend only on the *direction* of $H$, not its magnitude. Multiplying $H$ by any positive scalar $\frac{1}{n-1}$ scales the singular values $\Sigma$ but leaves $U$ and $V$ unchanged. So the rotation result is identical with or without the normalization factor. See: The Key Tension.
</details>

**Q4:** Someone claims "the cross-covariance matrix is always symmetric." What's wrong with this statement, and when *is* a covariance matrix guaranteed to be symmetric?
<details>
<summary>Answer</summary>
The cross-covariance matrix $H = \sum (\mathbf{x}_i - \bar{\mathbf{x}})(\mathbf{y}_i - \bar{\mathbf{y}})^T$ relates two *different* vectors and is generally not symmetric -- its transpose gives the cross-covariance in the opposite direction. It is not even necessarily square if $\mathbf{x}$ and $\mathbf{y}$ have different dimensions. The *auto-covariance* matrix $\Sigma = \frac{1}{n-1}\sum (\mathbf{x}_i - \bar{\mathbf{x}})(\mathbf{x}_i - \bar{\mathbf{x}})^T$ is always symmetric because $\text{Cov}(X_j, X_k) = \text{Cov}(X_k, X_j)$. See: Concrete Example, "The one thing most outsiders get wrong."
</details>

**Q5:** You have a 3D point cloud with covariance matrix $\Sigma$ whose eigenvalues are $\lambda_1 = 100$, $\lambda_2 = 100$, $\lambda_3 = 0.01$. What does this tell you about the geometry of the point cloud, and how would this affect the [[quick-context/helmert-transform|Helmert transform]] if this were one of your input point sets?
<details>
<summary>Answer</summary>
The eigenvalues describe the variance along the principal axes. Two large equal eigenvalues and one tiny eigenvalue mean the points lie nearly in a plane (a flat disk-shaped ellipsoid). For the Helmert transform, this is problematic: the rotation about the normal to that plane is well-determined (constrained by spread in two directions), but the rotation *within* the plane's normal direction is poorly conditioned because there is almost no depth variation to anchor it. The cross-covariance matrix $H$ will have one very small singular value, making the SVD solution sensitive to noise in that direction. In practice, you would need either more points with depth variation or additional constraints to stabilize the solution.
</details>

</details>
