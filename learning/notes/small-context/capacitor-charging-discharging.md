---
case: Capacitor Charging and Discharging
components: [capacitor, voltage, electric-current]
created: 2026-02-17
---

# Case: Capacitor Charging and Discharging

> **Components:** [[quick-context/capacitor]] | [[quick-context/voltage]] | [[quick-context/electric-current]]
> **Micro-context:** [[micro-context/decoupling-capacitor]]

> **In brief:** A capacitor stores energy by accumulating charge on two conductive plates separated by an insulating [[quick-context/capacitor#dielectric|dielectric]]. When connected to a battery through a complete circuit, the [[quick-context/voltage|electric field]] from the battery pushes electrons onto one plate and pulls them off the other—but crucially, electrons never cross the dielectric. When the circuit opens, the charge stays trapped, maintaining the voltage. When a load reconnects, the stored field pushes electrons through the load until equilibrium.

## The Situation

You want to store electrical energy temporarily and release it later. Unlike a [[quick-context/galvanic-cells-batteries|battery]] that stores energy chemically, a capacitor stores energy directly in an electric field. The key question: how does charge get onto the plates when the dielectric blocks electron flow?

## The Pieces

**The Dielectric:** An insulating material (ceramic, plastic, oxide layer) between the two metal plates. Electrons cannot flow through it. But the [[quick-context/voltage|electric field]] passes through it freely—this is the key insight. The dielectric stores the field's energy.

**The Plates:** Two conductive surfaces. One accumulates excess electrons (becomes negative). The other loses electrons (becomes positive). The charge difference creates the electric field across the dielectric.

**The Battery:** Creates the [[quick-context/voltage|electric field]] that pushes electrons around the circuit. It doesn't push electrons *through* the capacitor—it pushes them *around* the circuit onto one plate and off the other.

**The Complete Circuit:** Both sides of the capacitor must connect to the battery for charging to occur. Without a complete path, no [[quick-context/electric-current|current]] flows, no charge accumulates, and no field develops.

## Step by Step: What Happens

### Step 1: Initial State (Uncharged)

The capacitor has no stored charge. Both plates are electrically neutral—same number of protons and electrons on each side. No electric field exists between the plates.

```
UNCHARGED CAPACITOR
═══════════════════════════════════════════════════════════════════

    PLATE A                           PLATE B
    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    │  ● ● ● ● ●     DIELECTRIC      ● ● ● ● ●               │
    │  ● ● ● ● ●    (insulator)      ● ● ● ● ●               │
    │  ● ● ● ● ●                     ● ● ● ● ●               │
    │                                                         │
    └─────────────────────────────────────────────────────────┘

    ● = neutral atoms (equal protons and electrons)

    Electric field between plates: NONE
    Voltage across capacitor: 0V
    Stored energy: 0J
```

### Step 2: Battery Connected (Circuit Closed)

When you connect a battery with both terminals reaching both plates through wires, you create a complete circuit. The battery's chemical reactions create an electric field throughout the entire circuit—including through the wires connected to the capacitor.

```
BATTERY CONNECTED - CIRCUIT CLOSES
═══════════════════════════════════════════════════════════════════

                        ┌──────────────────────┐
                        │      BATTERY         │
                        │    (+)      (-)      │
                        └───┬────────────┬─────┘
                            │            │
            ───────────→ electric field ────────────→
                            │            │
                            ▼            ▼
    ┌───────────────────────┴────────────┴────────────────────┐
    │                                                         │
    │   PLATE A         DIELECTRIC           PLATE B          │
    │  ┌───────┐       ┌─────────┐         ┌───────┐         │
    │  │       │       │         │         │       │         │
    │  │       │       │         │         │       │         │
    │  └───┬───┘       └─────────┘         └───┬───┘         │
    │      │                                   │              │
    └──────┼───────────────────────────────────┼──────────────┘
           │                                   │
           └──────────── WIRE ─────────────────┘
                    (completes circuit)

    The battery creates an electric field that extends through the
    entire circuit. This field pushes electrons in the wires.

    CRITICAL: Both plates must connect back to the battery.
    No complete circuit = no current = no charging.
```

### Step 3: Electrons Redistribute (Current Flows)

The battery's field pushes electrons through the wires. Electrons flow INTO one plate and OUT OF the other plate. No electron crosses the dielectric—they just pile up on one side and deplete on the other.

```
CHARGING IN PROGRESS
═══════════════════════════════════════════════════════════════════

                        ┌──────────────────────┐
                        │      BATTERY         │
                        │    (+)      (-)      │
                        └───┬────────────┬─────┘
                            │            │
                            │            │
              e⁻ pulled     │            │   e⁻ pushed
              toward (+) ───┘            └─── from (-)
                            │            │
                            ▼            ▼
    ┌───────────────────────┴────────────┴────────────────────┐
    │                                                         │
    │   PLATE A         DIELECTRIC           PLATE B          │
    │  ┌───────┐       ┌─────────┐         ┌───────┐         │
    │  │ + + + │       │↓↓↓↓↓↓↓↓↓│         │ - - - │         │
    │  │ + + + │       │ FIELD   │         │ - - - │         │
    │  │ + + + │       │↓↓↓↓↓↓↓↓↓│         │ - - - │         │
    │  └───┬───┘       └─────────┘         └───┬───┘         │
    │      │                                   │              │
    │   electrons                          electrons          │
    │   depleted                          accumulated         │
    └──────┼───────────────────────────────────┼──────────────┘
           │                                   │
           └───────────── WIRE ────────────────┘
                       ←─ e⁻ ←─ e⁻ ←─
                    (current flows through wire)

    WHAT'S HAPPENING:
    • Battery pulls e⁻ OFF plate A (through the wire to + terminal)
    • Battery pushes e⁻ ONTO plate B (from - terminal through wire)
    • Plate A becomes positive (electron deficit)
    • Plate B becomes negative (electron surplus)
    • Electric field builds up across dielectric
    • NO electrons cross the dielectric—field passes through instead
```

### Step 4: Equilibrium Reached (Fully Charged)

As charge accumulates, the capacitor develops its own electric field that opposes the battery's field. When the capacitor's voltage equals the battery's voltage, the fields cancel in the wire—no more net push on electrons, so current stops.

```
FULLY CHARGED - EQUILIBRIUM
═══════════════════════════════════════════════════════════════════

                        ┌──────────────────────┐
                        │      BATTERY         │
                        │    (+)      (-)      │
                        │     9V               │
                        └───┬────────────┬─────┘
                            │            │
                            │            │
                            ▼            ▼
    ┌───────────────────────┴────────────┴────────────────────┐
    │                                                         │
    │   PLATE A         DIELECTRIC           PLATE B          │
    │  ┌───────┐       ┌─────────┐         ┌───────┐         │
    │  │+ + + +│       │↓↓↓↓↓↓↓↓↓│         │- - - -│         │
    │  │+ + + +│       │ E-FIELD │         │- - - -│         │
    │  │+ + + +│       │  = 9V   │         │- - - -│         │
    │  │+ + + +│       │↓↓↓↓↓↓↓↓↓│         │- - - -│         │
    │  └───┬───┘       └─────────┘         └───┬───┘         │
    │      │                                   │              │
    └──────┼───────────────────────────────────┼──────────────┘
           │                                   │
           └─────────── no current ────────────┘

    Battery field (pushing e⁻ clockwise): 9V
    Capacitor field (pushing e⁻ counterclockwise): 9V
    Net field in wire: 0V → NO CURRENT

    The capacitor is now "full" at this voltage.
    Energy stored: E = ½CV² (in the electric field, not the electrons)
```

### Step 5: Circuit Opened (Battery Disconnected)

When you disconnect the battery, the charge has nowhere to go. Electrons are trapped on plate B because the dielectric blocks them, and there's no path through the air gap. The electric field persists. The capacitor remains charged.

```
BATTERY DISCONNECTED - CHARGE TRAPPED
═══════════════════════════════════════════════════════════════════

                        ┌──────────────────────┐
                        │      BATTERY         │  (disconnected)
                        │    (+)      (-)      │
                        └──────────────────────┘
                               ╳    ╳
                          (open circuit)

    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    │   PLATE A         DIELECTRIC           PLATE B          │
    │  ┌───────┐       ┌─────────┐         ┌───────┐         │
    │  │+ + + +│       │↓↓↓↓↓↓↓↓↓│         │- - - -│         │
    │  │+ + + +│       │ FIELD   │         │- - - -│         │
    │  │+ + + +│       │ REMAINS │         │- - - -│         │
    │  │+ + + +│       │↓↓↓↓↓↓↓↓↓│         │- - - -│         │
    │  └───────┘       └─────────┘         └───────┘         │
    │                                                         │
    └─────────────────────────────────────────────────────────┘

    WHY THE CHARGE STAYS:
    • Electrons on plate B cannot cross dielectric (insulator)
    • No external path exists (circuit is open)
    • Charge is TRAPPED on the plates
    • Electric field persists in dielectric
    • Voltage remains at 9V (or slowly leaks over hours/days)

    This is stored energy—ready to be released when a load connects.
```

### Step 6: Load Connected (Discharging)

When you connect a load (resistor, LED, motor) across the capacitor, you create a new complete circuit. Now the capacitor's electric field pushes electrons from the negative plate, through the load, to the positive plate—doing work along the way.

```
LOAD CONNECTED - DISCHARGING
═══════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────┐
    │                                                         │
    │   PLATE A         DIELECTRIC           PLATE B          │
    │  ┌───────┐       ┌─────────┐         ┌───────┐         │
    │  │+ + + +│       │↓↓↓↓↓↓↓↓↓│         │- - - -│         │
    │  │+ + + +│       │ FIELD   │         │- - - -│         │
    │  │+ +    │←───── │ pushes  │ ─────→  │    - -│         │
    │  │+ +    │ e⁻ to │ e⁻ thru │ e⁻ from │    - -│         │
    │  └───┬───┘ here  └─────────┘ here    └───┬───┘         │
    │      │                                   │              │
    └──────┼───────────────────────────────────┼──────────────┘
           │                                   │
           │         ┌───────────┐             │
           │         │   LOAD    │             │
           └─────────┤ (resistor)├─────────────┘
                     │    💡     │
                     └───────────┘
                     e⁻ ──────────→
                   (current through load)

    WHAT'S HAPPENING:
    • Capacitor's field pushes e⁻ from plate B toward plate A
    • Electrons flow THROUGH the load (doing work—light, heat, motion)
    • Plate B loses negative charge (becomes less negative)
    • Plate A gains electrons (becomes less positive)
    • Field weakens as charge equalizes
    • Current decreases exponentially (τ = RC)
    • Eventually: both plates neutral, no field, no voltage
```

## The Result

The capacitor cycled through: uncharged → charged by battery → stored energy with no current → discharged through load.

```
ENERGY FLOW SUMMARY
═══════════════════════════════════════════════════════════════════

CHARGING:                         DISCHARGING:
  Battery                           Capacitor
    │                                 │
    ▼                                 ▼
Chemical energy              Electric field energy
    │                                 │
    ▼                                 ▼
 Electric field              Work done on load
 in capacitor                (light, heat, motion)


KEY INSIGHT: Electrons never cross the dielectric.
─────────────────────────────────────────────────

  During charging:  e⁻ flow through wires, piling on one plate
  During storage:   e⁻ are trapped (no path)
  During discharge: e⁻ flow through load, equalizing plates

  The FIELD crosses the dielectric.
  The ELECTRONS go around through the external circuit.

  This is why both terminals must connect for charging:
  - If only one side connects, e⁻ have nowhere to come from/go to
  - No complete path = no current = no charge accumulation
```

## Why Each Piece Matters

- **Dielectric:** Blocks electrons (keeping charge separated) while allowing the electric field to exist between plates. Without it, electrons would flow directly between plates—no storage.

- **Complete Circuit:** Electrons can only accumulate on one plate if they have somewhere to come from (the other plate, via the external circuit). Open either connection and charging stops.

- **Electric Field:** The actual energy storage mechanism. The field exists in the dielectric and contains the stored energy (E = ½CV²). Not the electrons themselves—the field.

- **Voltage Equilibrium:** Charging stops when the capacitor's field strength matches the battery's. The capacitor "fills up" to the source voltage, not to some fixed charge amount.

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/decoupling-capacitor]] — Capacitors placed near ICs for instant local charge

**Full treatment (10 minutes):**
- [[quick-context/capacitor]] — Dielectrics, RC time constants, types, decoupling applications
- [[quick-context/voltage]] — Electric fields, potential difference, field vs. voltage distinction
- [[quick-context/electric-current]] — Electron flow, Ohm's law, DC vs. AC
- [[quick-context/galvanic-cells-batteries]] — Chemical energy storage (contrast with capacitors)
