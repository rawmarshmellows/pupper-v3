---
term: Homogeneous Transformation Matrix
created: 2026-03-11
updated: 2026-03-27
---

> **Related:** [[learning/notes/micro-context/switch-matrix]] | [[learning/notes/quick-context/covariance-matrix]]

# Homogeneous Transformation Matrix[[learning/notes/quick-context/tensile-strength-materials|]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/anions-and-oxidation|A]] $[[learning/notes/quick-context/similarity-transform|4]] \times 4$ matrix that encodes [[learning/notes/quick-context/bjt-specifications|both]] [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|rotation]] [[learning/notes/micro-context/push-pull-vs-open-drain|and]] [[learning/notes/quick-context/pupper-lab2-forward-kinematics|translation]] in a single structure, allowing chained coordinate [[learning/notes/quick-context/can-bus|frame]] transformations [[learning/notes/quick-context/metal-interconnect-layers|via]] matrix multiplication. [[learning/notes/quick-context/capacitance|The]] standard representation in [[quick-context/pupper-lab2-forward-kinematics|forward kinematics]] for computing [[learning/notes/quick-context/pupper-lab2-forward-kinematics|end-effector]] position from joint angles.

## How It Works

- A [[learning/notes/quick-context/meddpicc-qualification-framework|3]]×3 [[learning/notes/quick-context/helmert-transform|rotation matrix]] is embedded in the [[learning/notes/quick-context/keypress-to-pixel-pipeline|top]]-left, [[learning/notes/quick-context/how-source-code-is-stored|encoding]] the orientation change between coordinate frames.
- A 3×[[learning/notes/quick-context/meddpicc-qualification-framework|1]] translation vector occupies the right column, encoding the position offset.
- The [[learning/notes/quick-context/keypress-to-pixel-pipeline|bottom]] row [0 [[learning/notes/quick-context/meddpicc-qualification-framework|0]] 0 1] preserves the matrix structure so that multiplying [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] 4×4 matrices correctly composes both rotation and translation in [[learning/notes/quick-context/ram-addressing-decoder|one]] step.
- Chaining $T_{01} \cdot T_{12} \cdot T_{23}$ transforms a [[learning/notes/quick-context/epson-rc-plus-programming|point]] from frame 3 all the way back to frame 0 — the basis of forward kinematics.

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

**Key insight:** A $3 \times 3$ rotation matrix [[learning/notes/quick-context/embedded-communication-protocols|can]]'t represent translation — the extra row and column in a $4 \times 4$ let you compose arbitrary rotations *and* translations by simple multiplication, which is [[learning/notes/quick-context/atoms-molecules-polymers-basics|why]] every joint in a [[learning/notes/quick-context/pupper-lab2-forward-kinematics|kinematic chain]] is just another matrix in the product.
