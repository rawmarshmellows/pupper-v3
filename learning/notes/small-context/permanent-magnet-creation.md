---
case: Creating a Permanent Magnet from Iron
components: [electromagnetism, unpaired-electrons, exchange-interaction, capacitor-discharge]
created: 2026-02-13
---

# Case: Creating a Permanent Magnet from Iron

> **Components:** [[quick-context/electromagnetism]] | [[quick-context/electric-current]] | [[quick-context/capacitor]]
> **Micro-context:** [[micro-context/electromagnetic-induction]]

> **In brief:** Iron has unpaired electrons that each act as tiny magnets. In unmagnetized iron, these atomic magnets point in random directions and cancel out. A magnetizer (a coil carrying high current) creates a strong [[quick-context/electromagnetism|magnetic field]] that forces all the atomic magnets to align in the same direction—and once aligned, the quantum mechanical "exchange interaction" locks them in place, creating a permanent magnet.

## The Situation

You have a piece of ordinary iron. It's not magnetic—it won't stick to your fridge or pick up paperclips. But iron *can* become a permanent magnet. How do you transform it? The answer involves electrons, quantum mechanics, and a simple coil of wire carrying [[quick-context/electric-current|high current]].

## The Pieces

**Unpaired Electrons:** Electrons spin on their axes, and this spin makes each electron a tiny magnet. In most materials, electrons pair up with opposite spins that cancel out. Iron has 4 unpaired electrons per atom—4 tiny magnets that don't cancel. [[quick-context/electromagnetism|Full treatment →]]

**Magnetic Domains:** Atoms don't act alone. In ferromagnetic materials like iron, groups of billions of atoms spontaneously align their magnetic moments in the same direction, forming "domains" typically 0.1-1 mm across (can be as small as 1 μm). Each domain is a tiny magnet, but domains point in random directions and cancel out overall.

**Exchange Interaction:** A quantum mechanical effect that forces neighboring atoms' electrons to align their spins in the same direction. This is what makes domains possible—it's the "glue" that holds atomic magnets together. It only works over short distances (~1 nm).

**Magnetizer:** A coil of wire (solenoid) connected to a high-current power source. When [[quick-context/electric-current|current]] flows, it creates a strong magnetic field inside the coil. By Ampère's Law, more current = stronger field. Industrial magnetizers use thousands of amps for milliseconds—achieved through capacitor discharge circuits that store energy slowly and release it all at once.

## Step by Step: What Happens

### Step 1: Unmagnetized Iron — Domains Cancel Out

Fresh iron has magnetic domains, but they point in random directions. The vector sum of all domains is zero—no net magnetism.

```
UNMAGNETIZED IRON — Random Domain Orientations
═══════════════════════════════════════════════════════════════════════════

    Top view of iron bar (each arrow = one magnetic domain):

    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                 │
    │    →    ↑    ←    ↓    →    ↑    ←    ↑    →    ↓    ←    ↓    │
    │                                                                 │
    │    ↑    ←    ↓    →    ↑    ↓    →    ←    ↓    →    ↑    ←    │
    │                                                                 │
    │    ↓    →    ↑    ←    ↓    →    ↑    →    ←    ↓    →    ↑    │
    │                                                                 │
    │    ←    ↓    →    ↑    ←    ↑    ↓    ←    ↑    →    ↓    →    │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘

    Net magnetization: ~ZERO (all arrows cancel out)
    The iron won't stick to anything.
```

**What's happening at the atomic level:** Inside each domain, billions of iron atoms have their unpaired electrons all pointing the same way (thanks to exchange interaction). But each domain formed independently when the iron cooled, so different domains ended up pointing different directions.

### Step 2: Apply External Field — Place Iron in Magnetizer

The magnetizer is a solenoid (coil of wire). When high current flows, it creates a powerful magnetic field along the coil's axis.

```
MAGNETIZER STRUCTURE — Solenoid with High Current
═══════════════════════════════════════════════════════════════════════════

                        Current: 1000+ Amps (brief pulse)

    Power supply                              Coil cross-section
    ┌──────────┐
    │  ~~~~    │─────────┐
    │  HIGH    │         │
    │ CURRENT  │    ┌────┴─────────────────────────────────────┐
    │  PULSE   │    │    ════════════════════════════════      │
    └──────────┘    │    ║                               ║      │
                    │    ║   ┌─────────────────────┐    ║      │
                    │    ║   │                     │    ║      │
                    │    ║   │    IRON BAR         │    ║      │
                    │    ║   │    inside coil      │    ║      │
                    │    ║   │                     │    ║      │
                    │    ║   └─────────────────────┘    ║      │
                    │    ║                               ║      │
                    │    ════════════════════════════════      │
                    └──────────────────────────────────────────┘

    Magnetic field (B) inside coil:

         B = μ₀ × N × I / L

         N = number of turns
         I = current (amps)
         L = coil length
         μ₀ = permeability of free space

    Industrial magnetizers: B > 1 Tesla (20,000× Earth's field)
```

### How the Magnetizer Creates Thousands of Amps

A magnetizer doesn't run thousands of amps continuously—that would require a dedicated power substation and would melt the coil. Instead, it uses a **capacitor discharge circuit**: store energy slowly, release it all at once.

```
MAGNETIZER CIRCUIT — Capacitor Discharge
═══════════════════════════════════════════════════════════════════════════

    PHASE 1: SLOW CHARGE (seconds)
    ─────────────────────────────────────────────────────────────────────────

        Wall outlet           Charger circuit             Capacitor bank
        (120V AC)            (three stages)               (stores energy)

                         ┌─────────────────────────┐
                         │                         │
        ~~~~  ───►  [Rectifier]  ───►  [Boost]  ───►  ═══════
                         │              │              ═══════
                         │              │              ═══════
                         ▼              ▼                 │
                      Converts      Steps up              │
                      AC → DC       voltage               │
                      (see below)   120V → 1500V          │
                                                          ▼
                                                    Takes 5-30 seconds
                                                    Low current (~1A)


    THE CHARGER CIRCUIT IN DETAIL:
    ─────────────────────────────────────────────────────────────────────────

    STAGE 1: Rectifier — Convert AC to DC
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │    Wall AC (120V ~)                   Pulsating DC (~160V peak)     │
    │                                                                     │
    │           ╱╲                                  ╱╲      ╱╲            │
    │          ╱  ╲           ┌──────┐             ╱  ╲    ╱  ╲           │
    │     ────╱────╲────      │Bridge│            ╱    ╲  ╱    ╲          │
    │    0V ──────────── ───► │Recti-│  ───►  ───╱──────╲╱──────╲───      │
    │              ╲  ╱       │fier  │           (all positive,           │
    │               ╲╱        └──────┘            no negative)            │
    │                                                                     │
    │    A [[micro-context/full-bridge-rectifier|bridge rectifier]]       │
    │    (4 diodes) flips negative half-cycles to positive.               │
    │    See: [[small-context/ac-to-dc-conversion]]                          │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

    STAGE 2: Boost Converter — Step up voltage
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │    ~160V DC input                        1000-2000V DC output       │
    │                                                                     │
    │    Unlike a [[micro-context/buck-converter|buck converter]] that    │
    │    steps DOWN, a boost converter steps UP by:                       │
    │                                                                     │
    │    1. Switch closes → current builds in inductor                    │
    │    2. Switch opens → inductor "kicks back" with HIGH voltage        │
    │    3. Diode steers this high voltage into the capacitor            │
    │    4. Repeat thousands of times per second                          │
    │                                                                     │
    │         160V ──┬──⊃⊃⊃⊃──┬──▶|──┬── 1500V                          │
    │                │    L    │   D   │                                  │
    │              [SW]        │      ═╪═ C (charges up)                  │
    │                │         │       │                                  │
    │               GND ───────┴───────┴── GND                            │
    │                                                                     │
    │    V_out = V_in / (1 - D)  where D = duty cycle                    │
    │    At 90% duty: V_out = 160 / 0.1 = 1600V                          │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘

    STAGE 3: Capacitor Bank — Store the energy
    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │    Multiple capacitors in series/parallel for high voltage + capacity│
    │                                                                     │
    │    Energy stored: E = ½CV²   (see [[quick-context/capacitor]])     │
    │                                                                     │
    │    Example: 1000μF capacitor bank at 1500V                          │
    │    E = ½ × (1000 × 10⁻⁶) × (1500)² = 1125 Joules                  │
    │                                                                     │
    │    That's enough energy to:                                         │
    │    • Lift a 1kg weight 115 meters                                   │
    │    • Power a 1000W microwave for 1 second                           │
    │    • Create a 15,000 Amp pulse for 2 milliseconds                   │
    │                                                                     │
    │    Why high voltage matters: E ∝ V². Double the voltage = 4× energy │
    │    Charging to 1500V instead of 150V gives 100× more energy!        │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘


    ═══════════════════════════════════════════════════════════════════════
    IMPORTANT: There are TWO different inductors in this system!
    ═══════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │  INDUCTOR 1: Inside boost converter (small, ~100μH)                │
    │  ─────────────────────────────────────────────────────────────────  │
    │  • Part of the charger circuit                                      │
    │  • Switches at ~100kHz during charging                              │
    │  • Steps up voltage from 160V to 1500V                              │
    │  • NOT connected to the iron bar                                    │
    │                                                                     │
    │  INDUCTOR 2: Magnetizing coil/solenoid (large, ~10-100μH)          │
    │  ─────────────────────────────────────────────────────────────────  │
    │  • The coil that wraps around the iron bar                          │
    │  • Only connected during discharge phase                            │
    │  • Carries 15,000+ amps for milliseconds                            │
    │  • Creates the magnetic field that aligns domains                   │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘


    PHASE 2: FAST DISCHARGE (milliseconds)
    ─────────────────────────────────────────────────────────────────────────

    During discharge, the capacitor bank connects to the magnetizing coil:

                         DISCHARGE SWITCH
                           (SCR/IGBT)
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        │    ┌───────────┐         ┌─────────────────────────────┐
        │    │           │         │   MAGNETIZING COIL          │
        │    │ CAPACITOR │         │   (solenoid around iron)    │
        │    │   BANK    │         │                             │
        │    │           │         │    ════════════════════     │
        │    │  ═══════  │         │    ║ ┌─────────────┐ ║     │
        │    │  ═══════  │────────►│    ║ │  IRON BAR   │ ║     │
        │    │  ═══════  │         │    ║ └─────────────┘ ║     │
        │    │           │         │    ════════════════════     │
        │    │  1500V    │         │                             │
        │    │  1000μF   │         │   L_coil ≈ 10-100 μH        │
        │    │           │         │   R_coil ≈ 0.01-0.1 Ω       │
        │    └─────┬─────┘         └──────────────┬──────────────┘
        │          │                              │
        │          └──────────────────────────────┘
        │                         │
        └─────────────────────────┘
                                 GND

    When switch closes:
    • Capacitor voltage (1500V) appears across coil
    • Peak current: I = V/R = 1500V / 0.1Ω = 15,000 Amps
    • Current rises in ~L/R = 100μH / 0.1Ω = 1 millisecond
    • Discharge completes in ~2-5 ms (limited by resistance)


    CURRENT WAVEFORM THROUGH MAGNETIZING COIL
    ─────────────────────────────────────────────────────────────────────────

    I (amps)
        ▲
        │
   15000├──────╮  ← peak (limited by V/R)
        │     ╱ ╲
        │    ╱   ╲
   10000├   ╱     ╲
        │  ╱       ╲
    5000├ ╱         ╲
        │╱           ╲
        │             ╲───────────
        └──┬──┬──┬──┬──┬──┬──┬──► t (ms)
           0  1  2  3  4  5  6
           ↑        ↑
           │        └─ exponential decay as
           │           capacitor depletes
           │
           └─ exponential rise limited by L/R
              (current can't change instantly
               through an inductor)

    Total pulse: ~2-5 milliseconds
    Brief but intense—enough to saturate the iron
```

The key insight: **Power = Energy / Time**. The [[quick-context/capacitor|capacitor]] stores 1000+ joules slowly from a wall outlet, then dumps it all in milliseconds. The coil survives because the pulse is too brief to cause overheating.

**Why such high current?** The external field must be strong enough to overcome the resistance domains have to reorienting. Domain walls (boundaries between domains) are pinned by crystal defects—you need enough magnetic "pressure" to push them.

### Step 3: Domains Begin to Align — Two Mechanisms

When the external field is applied, domains respond in two ways:

```
DOMAIN RESPONSE TO EXTERNAL FIELD
═══════════════════════════════════════════════════════════════════════════

    External field direction: →→→→→→→→→→→→→→→→→→→→→→

    MECHANISM 1: Domain Wall Motion
    ─────────────────────────────────────────────────────────────────────────

    Before:                      After:
    ┌──────┬──────┬──────┐      ┌──────────────┬──────┐
    │  →   │  ←   │  →   │      │      →       │  →   │
    │      │      │      │  ──► │              │      │
    │  →   │  ←   │  →   │      │      →       │  →   │
    └──────┴──────┴──────┘      └──────────────┴──────┘

    Domains aligned WITH the field GROW
    Domains aligned AGAINST the field SHRINK
    Domain walls move (they don't rotate)


    MECHANISM 2: Domain Rotation (at high fields)
    ─────────────────────────────────────────────────────────────────────────

    Before:          After:
    ┌──────┐        ┌──────┐
    │  ↗   │        │  →   │
    │      │   ──►  │      │
    │  ↗   │        │  →   │
    └──────┘        └──────┘

    Entire domain rotates to align with field
    Requires stronger field than wall motion
    Happens when walls can't move anymore
```

**The key insight:** Domain wall motion is "easy"—it happens first. Domain rotation requires much stronger fields because you're fighting against the exchange interaction that holds atoms aligned within the domain.

### Step 4: Saturation — All Domains Aligned

With enough field strength, all domains align in the same direction. This is called magnetic saturation—you can't make it more magnetic by applying more field.

```
MAGNETIZED IRON — Single Domain Orientation
═══════════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                 │
    │    →    →    →    →    →    →    →    →    →    →    →    →    │
    │                                                                 │
    │    →    →    →    →    →    →    →    →    →    →    →    →    │
    │                                                                 │
    │    →    →    →    →    →    →    →    →    →    →    →    →    │
    │                                                                 │
    │    →    →    →    →    →    →    →    →    →    →    →    →    │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘
       S                                                           N
       ↑                                                           ↑
    South pole                                               North pole
    (field enters)                                       (field exits)

    Net magnetization: MAXIMUM
    Now it's a permanent magnet!
```

### Step 5: Remove External Field — Domains Stay Aligned

Here's the crucial question: why don't the domains randomize again when you turn off the magnetizer?

```
WHY MAGNETIZATION IS PERMANENT — Three Locking Mechanisms
═══════════════════════════════════════════════════════════════════════════

    1. EXCHANGE INTERACTION (quantum mechanical)
    ─────────────────────────────────────────────────────────────────────────

        Within each domain, neighboring atoms "want" their electrons
        to spin the same direction. This is NOT a classical magnetic
        attraction—it's a quantum effect from the Pauli exclusion
        principle and electron wave function overlap.

        Energy cost to flip one atom: ~0.1 eV
        At room temperature (kT ≈ 0.025 eV): flipping is unlikely
        Exchange keeps atoms aligned with their neighbors


    2. CRYSTAL ANISOTROPY
    ─────────────────────────────────────────────────────────────────────────

        Iron crystals have preferred magnetization directions along
        certain crystal axes. Domains "lock" into these easy directions.

              ┌─────────────────────────────────┐
              │                                 │
              │  Easy axis: →                   │
              │                                 │
              │  Hard axis: ↗ (costs energy)   │
              │                                 │
              └─────────────────────────────────┘


    3. DOMAIN WALL PINNING
    ─────────────────────────────────────────────────────────────────────────

        Domain walls get "stuck" on crystal defects, impurities,
        and grain boundaries. Moving them requires energy.

              ═══════════════╳═══════════════
                             ↑
                   Domain wall pinned on defect
                   (won't move without external field)


    RESULT: Without external field, domains STAY where they are
            The iron is now permanently magnetized
```

## The Result

```
BEFORE AND AFTER
═══════════════════════════════════════════════════════════════════════════

    BEFORE MAGNETIZATION              AFTER MAGNETIZATION
    (unmagnetized iron)               (permanent magnet)

    ┌───────────────────┐             ┌───────────────────┐
    │ ← ↑ → ↓ ← ↑ → ↓  │             │ → → → → → → → →  │
    │ ↓ → ↑ ← ↓ → ↑ ←  │             │ → → → → → → → →  │
    │ → ↓ ← ↑ → ↓ ← ↑  │     ──►     │ → → → → → → → →  │
    │ ↑ ← ↓ → ↑ ← ↓ →  │             │ → → → → → → → →  │
    └───────────────────┘             └───────────────────┘
      Net field: ZERO                   Net field: STRONG

    Won't pick up paperclips         Will pick up paperclips forever
                                     (until demagnetized)
```

The iron is now a permanent magnet. The same piece of metal, same atoms, same electrons—but now they're all working together instead of canceling out.

## Why Each Piece Matters

- **Unpaired Electrons:** These are the source of atomic magnetism. Without unpaired electrons (like in copper), no permanent magnetism is possible—paired electrons cancel out.

- **Exchange Interaction:** This quantum effect creates domains in the first place and keeps them stable. Without exchange, thermal motion would randomize atomic magnets instantly.

- **Magnetizer (High Current Coil):** Provides the external field needed to overcome domain wall pinning and force alignment. The current creates the field; the iron's electrons do the rest.

## Demagnetization: How to Undo It

Two ways to destroy a permanent magnet:

```
DEMAGNETIZATION METHODS
═══════════════════════════════════════════════════════════════════════════

    1. HEAT ABOVE CURIE TEMPERATURE
    ─────────────────────────────────────────────────────────────────────────

       Iron's Curie temperature: 770°C (1418°F)

       Above this temperature:
       • Thermal energy (kT) exceeds exchange energy
       • Atoms vibrate too violently for exchange to maintain alignment
       • Domains randomize → net magnetization → ZERO

       ┌──────────────────────────────────────────────────────────┐
       │  Energy                                                  │
       │    ▲                                                     │
       │    │                        ╱  Thermal energy (kT)       │
       │    │                      ╱    increases with T          │
       │    │                    ╱                                │
       │    │    ────────────╳─╱─────  Exchange energy            │
       │    │               ╱         (roughly constant)          │
       │    │             ╱                                       │
       │    │           ╱    ↑                                    │
       │    │         ╱      │ At Tc: thermal = exchange          │
       │    │       ╱        │ Above Tc: thermal wins             │
       │    └─────────────────┬───────────────────────────► T     │
       │          0       770°C (Tc)                              │
       │                    Curie temperature                     │
       └──────────────────────────────────────────────────────────┘

       When iron cools back down, domains re-form but in RANDOM
       directions → unmagnetized again.


    2. APPLY ALTERNATING FIELD (AC demagnetization)
    ─────────────────────────────────────────────────────────────────────────

       Apply AC magnetic field while slowly reducing amplitude

       ┌──────────────────────────────────────────────────────────┐
       │  B                                                       │
       │  ▲      ╱╲          ╱╲        ╱╲                         │
       │  │     ╱  ╲        ╱  ╲      ╱  ╲    ╱╲   ╱╲            │
       │  │    ╱    ╲      ╱    ╲    ╱    ╲  ╱  ╲ ╱  ╲  ╱╲      │
       │ 0├───╱──────╲────╱──────╲──╱──────╲╱────╲╱────╲╱──╲──→ 0│
       │  │          ╲  ╱        ╲╱        (amplitude decreases)  │
       │  │           ╲╱                                          │
       │  │                                                       │
       │  └──────────────────────────────────────────────────► t  │
       └──────────────────────────────────────────────────────────┘

       Each reversal scrambles domains a little more
       When amplitude reaches zero, domains are randomized
       Net magnetization → ZERO
```

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/electromagnetic-induction]] — How changing magnetic fields create current (related principle)
- [[micro-context/full-bridge-rectifier]] — The 4-diode circuit that converts AC to pulsating DC
- [[micro-context/buck-converter]] — Steps voltage DOWN (the opposite of the boost converter used here)

**Full treatment (10 minutes):**
- [[quick-context/electromagnetism]] — Maxwell's equations, how current creates magnetic fields, electromagnetic waves
- [[quick-context/electric-current]] — What current is, why high current creates strong magnetic fields
- [[quick-context/inductor]] — Coils that store energy in magnetic fields, related to magnetizer coils
- [[quick-context/capacitor]] — How capacitors store energy in electric fields (E = ½CV²)—the basis of magnetizer discharge circuits

**Related small-context:**
- [[small-context/ac-to-dc-conversion]] — The rectification step explained in depth with diagrams
