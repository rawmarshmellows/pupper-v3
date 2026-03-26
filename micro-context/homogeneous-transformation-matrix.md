---
term: Homogeneous Transformation Matrix
created: 2026-03-11
---

# Homogeneous Transformation Matrix

**Definition:** A $4 \times 4$ matrix that encodes both rotation and translation in a single structure, allowing chained coordinate frame transformations via matrix multiplication. The standard representation in [[quick-context/pupper-lab2-forward-kinematics|forward kinematics]] for computing end-effector position from joint angles.

```
        ┌                        ┐
        │ R₁₁  R₁₂  R₁₃ │ tₓ  │
    T = │ R₂₁  R₂₂  R₂₃ │ tᵧ  │
        │ R₃₁  R₃₂  R₃₃ │ t_z │
        │  0    0    0   │  1  │
        └                        ┘
         ├── 3×3 rotation ─┤ translation
         │  (orientation)  │ (position)
         └─────────────────┘

  Chain: T_base→foot = T₀₁ · T₁₂ · T₂₃ · T₃ₑₑ
```

**Key insight:** A $3 \times 3$ rotation matrix can't represent translation — the extra row and column in a $4 \times 4$ let you compose arbitrary rotations *and* translations by simple multiplication, which is why every joint in a kinematic chain is just another matrix in the product.
