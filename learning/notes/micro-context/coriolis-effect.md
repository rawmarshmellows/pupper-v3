---
term: Coriolis Effect
created: 2026-03-28
---

> **Related:** [[learning/notes/micro-context/4-wire-kelvin-measurement]] | [[learning/notes/micro-context/ac-dc-current]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/anode]]

# Coriolis Effect

> **See also:** mems-gyroscope-vibration-drift | imu-robot-balance-sensing | [[quick-context/pupper-bom-control-board]]

**[[learning/notes/quick-context/capacitance|Definition]]:** A pseudo-force that acts on objects moving within a rotating [[learning/notes/quick-context/comparator|reference]] [[learning/notes/quick-context/can-bus|frame]], deflecting them perpendicular to their velocity. [[learning/notes/quick-context/capacitance|The]] force is $F_{\[[learning/notes/quick-context/how-source-code-is-stored|text]]{Coriolis}} = -2m(\vec{\omega} \times \vec{v})$ — proportional to [[learning/notes/quick-context/bjt-specifications|both]] the [[learning/notes/quick-context/pcb-assembly-files-bom-cpl|rotation]] rate $\omega$ [[learning/notes/micro-context/push-pull-vs-open-drain|and]] the object's velocity $v$, and always at right angles to the motion. It's called a "pseudo-force" because it vanishes in a non-rotating frame — [[learning/notes/quick-context/tlv7211-as-lmc7211-replacement|nothing]] is actually pushing the object; it just *appears* to curve because the frame itself is rotating [[learning/notes/quick-context/bga-ball-grid-array|underneath]] it.

## How It Works

- An object moving in a straight line (inertial frame) appears to curve [[learning/notes/quick-context/bare-minimal-data-storage-circuit|when]] observed from a rotating frame. The Coriolis force explains this apparent deflection.
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

| [[learning/notes/quick-context/absolute-orientation|Scale]] | Example | [[learning/notes/quick-context/silymarin|Mechanism]] |
|-------|---------|-----------|
| Planetary | Weather cyclones | Air moving toward low-pressure deflects right (N. hemisphere) / left (S. hemisphere) |
| Laboratory | Foucault pendulum | Pendulum's swing plane rotates as Earth turns beneath it: $T = T_{\text{Earth}} / \sin(\text{latitude})$ |
| Ballistic | Long-range artillery | 1,000-yard northward shot deflects ~71 mm rightward (mid-latitudes) |
| MEMS | Gyroscope chip | Vibrating proof mass deflects ~nanometers when chip rotates at 1 deg/s |
