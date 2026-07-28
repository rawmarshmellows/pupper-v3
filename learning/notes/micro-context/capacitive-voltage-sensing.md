---
term: Capacitive Voltage Sensing
created: 2026-06-08
---
> **Related:** [[quick-context/voltage]] | [[quick-context/capacitive-sensing-measurement]] | [[micro-context/adc-analog-to-digital-converter]] | [[micro-context/input-offset-voltage]] | [[micro-context/output-voltage-swing]]


# Capacitive Voltage Sensing

> **See also:** [[quick-context/differential-pair]] | [[quick-context/capacitance]] | capacitive sensing measurement

**Definition:** Detecting a [[quick-context/voltage|voltage]] *without touching* the conductor — a sense plate placed near a live conductor couples to it through the electric field, and the charge induced on the plate ($Q = CV$) reveals the source [[quick-context/voltage|voltage]]. Used in non-contact voltage testers and high-voltage capacitive dividers.

## How It Works

- The source conductor and the sense plate form a small coupling [[quick-context/capacitor|capacitor]] $C_c$ across the air/dielectric gap — no metal-to-metal contact.
- The source's electric field induces a proportional charge on the plate, $Q = C_c \cdot V_{source}$, so the plate "feels" the voltage through the field alone.
- $C_c$ in series with a reference [[quick-context/capacitor|capacitor]] $C_{ref}$ to ground makes a capacitive divider: $V_{sense} = V_{source} \cdot \dfrac{C_c}{C_c + C_{ref}}$.
- For a *changing* (AC) source the field drives a displacement current $I = C_c \, dV/dt$ into the plate; this tiny signal feeds a high-impedance [[quick-context/differential-pair|differential pair]], which amplifies it against a reference and rejects common-mode noise.

```
   live conductor @ V_source
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ┊  E-field couples across
                ┊  gap = coupling cap C_c
                ▼
   ┌─────────────────────────┐  sense plate
   └────────────┬────────────┘
                │  V_sense = V_source · C_c/(C_c+C_ref)
                ├───────────────► ┌─────────────┐
                │                 │  diff pair  │ amplify vs
               ═╪═ C_ref          │  (amp/ADC)  │ ref, reject CM
                │                 └─────────────┘
                ▼
               GND
```

**Key insight:** It is galvanically isolated — the plate never touches the wire — but that means pure DC can't be sensed continuously: a static charge passes no current ($dV/dt = 0$), so capacitive sensors detect AC or *changes* in voltage, not steady DC levels.

## Common Questions

**Is it measured relative to ground? Then is the voltage different at different points along the conductor?**
Yes, relative to ground — [[quick-context/voltage|voltage]] is always a difference, and the return path reaches earth through $C_{ref}$ or your body's [[quick-context/capacitance|capacitance]] (no ground path → no current → nothing to sense). But **no**, the voltage is *not* different along the conductor: a wire is one **equipotential** node — negligible $IR$ drop means the same potential everywhere along it at a given instant. What varies is *time* (the AC swing the sensor detects) and *different nodes* (across a load), not position on the wire. (Exception: at RF, where wire length ≈ wavelength, transmission-line standing waves do make position matter — but 60 Hz mains has λ ≈ 5000 km, so any normal wire is equipotential.)

**Where does the [[quick-context/differential-pair|differential pair]]'s reference come from?**
For single-ended sensing (this diagram) the "ref" is just the device's own **ground / 0 V** node — the pair amplifies $V_{sense} - 0$. Other architectures: a **non-contact tester** compares against a fixed **threshold** (bandgap/divider) and beeps when exceeded; a **differential capacitive sensor** (e.g. MEMS accelerometer) uses a **second plate** moving the opposite way, measuring $C_1 - C_2$.

**Why is a capacitor in series *less* [[quick-context/capacitance|capacitance]]?**
Series stacks the dielectric gaps, so the chain acts like one cap with a thicker gap — and $C = \varepsilon A / d$ shrinks as $d$ grows (two identical caps in series = double gap = half C). Equivalently, the same charge $Q$ sits on each cap but the voltages add, so $C = Q/V$ falls. Result: $1/C_{total} = 1/C_1 + 1/C_2$, always *smaller than the smallest* member — which is why the tiny coupling cap $C_c$ dominates the divider and makes $V_{sense}$ a small fraction of the source. See [[quick-context/capacitance]].
