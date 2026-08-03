---
term: Piezoelectric Effect
created: 2026-03-27
---
> **Related:** [[learning/notes/micro-context/i2s-audio-amplifier]] | [[learning/notes/micro-context/output-voltage-swing]]

# Piezoelectric Effect

**Definition:** The ability of certain crystals (quartz, ceramics like PZT, some polymers) to generate an electric voltage when mechanically stressed, and conversely, to deform when an [[learning/notes/quick-context/electric-magnetic-field-unification|electric field]] is applied. The first direction is the *direct* effect (sensing); the reverse is the *converse* effect (actuation).

## How It Works

- Certain crystal lattices lack a center of symmetry, so mechanical stress shifts positive and negative charge centers apart, creating a net polarization and measurable voltage across the material.
- Applying an external electric field reverses the process — it displaces ions in the lattice, causing the material to physically [[learning/notes/quick-context/existing-account-management-playbook|expand]] or contract.
- The relationship is linear for small deformations: $D = dT + \varepsilon E$ (electric displacement = piezoelectric coefficient $\times$ stress + permittivity $\times$ field).
- This bidirectionality enables sustained oscillation in a [[micro-context/ceramic-resonator|ceramic resonator]]: an AC voltage deforms the crystal (converse effect), but the crystal's elastic lattice overshoots past equilibrium like a spring, and that overshoot generates a voltage (direct effect) that feeds back into the amplifier circuit — sustaining vibration at the crystal's mechanical resonant frequency, which is set by its physical dimensions, not the circuit.

```
  Direct effect              Converse effect
  (stress → voltage)         (voltage → deformation)

  ┌──────────┐               ┌──────────┐
  │  crystal  │  squeeze      │  crystal  │  apply V
  │ + − + − + │  ───────►    │ + − + − + │  ───────►
  │ − + − + − │              │ − + − + − │
  └──────────┘               └──────────┘
       │                          │
       ▼                          ▼
  ┌──────────┐               ┌──────────┐
  │ +++++++  │  voltage       │          │  shape
  │          │  appears       │ ──────── │  changes
  │ −−−−−−−  │               │          │
  └──────────┘               └──────────┘
```

## Why This Creates Sustained Oscillation

Both effects working together is what makes a [[micro-context/ceramic-resonator|ceramic resonator]] vibrate at a precise frequency:

1. **Voltage applied** → converse effect → crystal physically deforms (expands or contracts depending on field direction)
2. **Voltage removed/reversed** → the crystal's lattice has elastic restoring force (like a spring), so it doesn't just return to rest — it **overshoots** past its equilibrium position
3. **Overshoot generates a voltage** → direct effect — the mechanical motion creates charge separation, which feeds back into the oscillator amplifier circuit
4. **Amplifier returns that energy** at just the right phase, pushing the crystal again — sustaining the oscillation

The crucial point is **mechanical resonance**. The crystal is a physical object with a natural resonant frequency determined by its dimensions and material properties — exactly like a tuning fork or a guitar string. At that specific frequency, mechanical vibrations constructively reinforce each other. At all other frequencies, they destructively interfere and die out.

The frequency isn't set by the electrical circuit — it's set by the **physical geometry** of the ceramic. A thinner piece vibrates faster. The circuit just provides enough energy to keep it ringing at that natural frequency, the same way you push a child on a swing at just the right moment.

```
SUSTAINED OSCILLATION (one cycle):

  1. Voltage applied    2. Voltage removed    3. Overshoot!        4. Springs back
     → crystal expands     → springs back        (like a spring)      → cycle repeats

  ┌────────────┐       ┌──────────┐        ┌──────────┐         ┌────────────┐
  │ ←────────→ │       │  ──────  │        │ →──────← │         │  ──────    │
  │  expanded  │       │  normal  │        │compressed│         │  normal    │
  └────────────┘       └──────────┘        └──────────┘         └────────────┘
        │                    │                   │                     │
        ▼                    ▼                   ▼                     ▼
  V: ───────┐          ─────────           ┌─────────             ─────────
            │                              │
            └──────                  ──────┘
         (+)                            (−)

  The overshoot is the key — without it, you'd get a single
  twitch, not a vibration. The elastic lattice acts like a
  spring with an extremely well-defined resonant frequency.
```

**Key insight:** Piezoelectricity requires a non-centrosymmetric crystal structure — if the lattice has a center of symmetry, stress pushes charges equally in all directions and no net polarization appears. This is why only ~20 of the 32 crystal classes exhibit the effect.
