---
term: Coriolis Effect
created: 2026-03-28
---

# Coriolis Effect

> **Related:** [[micro-context/mosfet]] | [[micro-context/piezoelectric-effect]]
> **See also:** [[small-context/mems-gyroscope-vibration-drift]] | [[small-context/imu-robot-balance-sensing]] | [[quick-context/pupper-bom-control-board]]

**Definition:** A pseudo-force that acts on objects moving within a rotating reference frame, deflecting them perpendicular to their velocity. The force is $F_{\text{Coriolis}} = -2m(\vec{\omega} \times \vec{v})$ — proportional to both the rotation rate $\omega$ and the object's velocity $v$, and always at right angles to the motion. It's called a "pseudo-force" because it vanishes in a non-rotating frame — nothing is actually pushing the object; it just *appears* to curve because the frame itself is rotating underneath it.

## How It Works

- An object moving in a straight line (inertial frame) appears to curve when observed from a rotating frame. The Coriolis force explains this apparent deflection.
- The cross product $\vec{\omega} \times \vec{v}$ means the force is perpendicular to both the rotation axis and the velocity — it deflects the object sideways, never speeding it up or slowing it down.
- The force scales linearly with both rotation rate and velocity: faster object or faster rotation = stronger deflection.

```
CORIOLIS EFFECT — ROTATING FRAME vs INERTIAL FRAME

  INERTIAL FRAME (looking down):       ROTATING FRAME (on the turntable):

       Object moves straight              Object appears to curve
       ─────────────────►                 ─────────╮
                                                    ╲
       Turntable rotates                              ╲
       beneath it                                      ▼
                                           "Something is pushing
                                            it sideways!" ← Coriolis force

  MEMS GYROSCOPE APPLICATION:

       Drive axis (vibrating mass)
       ◄════════════════════►  v (velocity along drive)
              │
              │  Chip rotates (ω) about perpendicular axis
              │
              ▼
       Coriolis force deflects mass along SENSE axis
       F = -2m(ω × v)  ∝  angular velocity

  No rotation → no Coriolis force → no sense-axis deflection → output = 0
```

**Key insight:** MEMS gyroscopes exploit this by continuously vibrating a proof mass (providing $v$) — when the chip rotates ($\omega$), the Coriolis force deflects the mass along a perpendicular sense axis by an amount directly proportional to angular velocity. The vibration is the "moving object," and the rotating chip is the "rotating reference frame."

### Real-World Examples

| Scale | Example | Mechanism |
|-------|---------|-----------|
| Planetary | Weather cyclones | Air moving toward low-pressure deflects right (N. hemisphere) / left (S. hemisphere) |
| Laboratory | Foucault pendulum | Pendulum's swing plane rotates as Earth turns beneath it: $T = T_{\text{Earth}} / \sin(\text{latitude})$ |
| Ballistic | Long-range artillery | 1,000-yard northward shot deflects ~71 mm rightward (mid-latitudes) |
| MEMS | Gyroscope chip | Vibrating proof mass deflects ~nanometers when chip rotates at 1 deg/s |
