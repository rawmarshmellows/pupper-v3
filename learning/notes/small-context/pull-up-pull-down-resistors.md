---
case: Pull-Up and Pull-Down Resistors on a GPIO Input
components: [resistor]
created: 2026-04-17
---

# Case: Pull-Up and Pull-Down Resistors on a GPIO Input

> **Components:** [[learning/notes/quick-context/resistor]] | [[learning/notes/quick-context/comparator]] | [[learning/notes/quick-context/electric-current]] | [[learning/notes/quick-context/voltage]] | [[learning/notes/index/how-a-computer-works-index|How a Computer Works — Index-Spine]]
> **Micro-context:** [[learning/notes/micro-context/smd-resistor]] | [[learning/notes/micro-context/microcontroller]] | [[learning/notes/micro-context/i2c]] | [[learning/notes/micro-context/scan-loop]] | [[learning/notes/micro-context/adc-analog-to-digital-converter]]

> **In brief:** A [[learning/notes/micro-context/microcontroller|microcontroller]] GPIO input is a high-impedance node -- with nothing connected it's "floating" and reads random noise. A pull-up or pull-down [[learning/notes/quick-context/resistor|resistor]] gently ties the pin to $V_{CC}$ or GND so it reads a known default state, while a button or other driver can overpower the resistor to force the opposite state when active.

## The Situation

You want to read a button press on a [[learning/notes/micro-context/microcontroller|microcontroller]]. The obvious wiring -- button between pin and GND -- fails: when the button is open, the pin isn't connected to anything. CMOS inputs have gigaohm input impedance, so even tiny stray currents from EMI, nearby traces, or finger capacitance push the voltage to random values. The firmware reads HIGH, LOW, or rapid chatter unpredictably. You need to guarantee a default state when nothing is driving the line, without blocking the button from pulling it the other way when pressed.

## The Pieces

**GPIO input pin:** A high-impedance CMOS [[learning/notes/quick-context/transistor|transistor]] gate inside the MCU that samples voltage at the pin. Under the hood it's effectively a [[learning/notes/quick-context/comparator|comparator]] (usually a Schmitt trigger with hysteresis) that compares the pin voltage against an internal threshold and outputs a clean digital 1 or 0 -- a 1-bit [[learning/notes/micro-context/adc-analog-to-digital-converter|ADC]]. It draws almost no current (nanoamps of leakage), which is why it can't establish its own voltage and is vulnerable to noise.

**Pull-up resistor:** A [[learning/notes/quick-context/resistor|resistor]] (commonly 10kΩ) wired from the input pin to $V_{CC}$. It "leaks" a tiny current into the pin to hold it at $V_{CC}$ by default. [[learning/notes/quick-context/resistor|Full treatment on resistors -->]]

**Pull-down resistor:** The mirror image -- a resistor from the pin to GND. Holds the pin at 0 V by default. Choice between pull-up vs pull-down depends on what the "active" signal source looks like.

**Button (switch):** A [[learning/notes/micro-context/switch-matrix|mechanical switch]] that, when closed, hard-connects the pin to GND (for a pull-up circuit) or to $V_{CC}$ (for a pull-down circuit). Because it has near-zero resistance when closed, it easily overpowers the resistor's weak pull.

## Step by Step: What Happens

### Step 1: The floating-input problem

Without any pull resistor, the pin is an isolated high-impedance node.

```
WITHOUT A PULL RESISTOR (BROKEN)
==============================================================================

    VCC (3.3V)
      |
      |           (nothing connected here)
      |
      x   ────────────── MCU input pin   ── reads: ???
      |                    ^
      ^                    |
    Button               high impedance
    (open)               (~1 GΩ)
      |
     GND

    Pin voltage is set by whatever stray charge happens to be
    nearby -- EMI, 60 Hz mains hum, a finger 1 cm away.
    Reads flip between HIGH and LOW unpredictably.
```

With gigaohm input impedance, even nanoamps of stray current can push the pin voltage by volts. The pin is "floating."

### Step 2: Add a pull-up resistor (button reads active-LOW)

Wire 10kΩ from the pin up to $V_{CC}$, with the button from pin to GND.

```
PULL-UP CONFIGURATION, BUTTON RELEASED (idle)
==============================================================================

    VCC (3.3V)
      │
     ┌┴┐
     │R│  10kΩ pull-up
     └┬┘
      │
      ├────────────── MCU input pin   ── reads: HIGH (~3.3V)
      │
      x    <-- button open
      │
     GND

    Current through the resistor: I = (3.3 - 3.3) / 10kΩ = ~0 A
    (pin draws only nanoamps of leakage, so there's almost
     no drop across the resistor -- pin sits at ~VCC)
```

The resistor weakly ties the pin to $V_{CC}$. Tiny leakage current through the MCU input produces negligible voltage drop across 10kΩ, so the pin reads HIGH.

### Step 3: Press the button -- the resistor gets overpowered

Closing the button creates a near-zero-resistance path from pin to GND.

```
PULL-UP CONFIGURATION, BUTTON PRESSED (active)
==============================================================================

    VCC (3.3V)
      │
     ┌┴┐
     │R│  10kΩ pull-up
     └┬┘
      │
      ├────────────── MCU input pin   ── reads: LOW (~0V)
      │
      / <-- button CLOSED
      │
     GND

    Now VCC -> R -> GND forms a direct path.
    Current: I = 3.3V / 10kΩ = 0.33 mA  (a small, acceptable current)
    Voltage at pin: essentially 0V (button has ~0 Ω resistance,
                                    so it wins the voltage divider)
    Power wasted while pressed: P = V²/R = 3.3² / 10k = ~1 mW
```

The resistor and the closed button form a voltage divider. The switch's near-zero resistance dominates, so the pin reads LOW. Logic becomes "active-LOW": pressed = 0, released = 1.

### Step 4: Same idea, flipped -- pull-down for active-HIGH

Swap roles: resistor to GND, button to $V_{CC}$. Same mechanism, opposite defaults.

```
PULL-DOWN CONFIGURATION
==============================================================================

           VCC (3.3V)                      VCC (3.3V)
             │                               │
             /  button open                  /  button CLOSED
             │                               │
             ├── MCU pin: LOW (~0V)          ├── MCU pin: HIGH (~3.3V)
             │                               │
            ┌┴┐                             ┌┴┐
            │R│ 10kΩ pull-down              │R│ 10kΩ pull-down
            └┬┘                             └┬┘
             │                               │
            GND                             GND

    IDLE: pin pulled to GND through R,              ACTIVE: button shorts
    no current flows, reads LOW                     pin to VCC, current
                                                    flows VCC -> button ->
                                                    R -> GND. Pin reads HIGH.
```

Pull-down is useful when the active signal source drives HIGH (e.g., the output of another logic chip that idles low and pulses high) or when you want "pressed = 1" semantics in firmware.

### Step 5: Choosing the resistor value

The value is a classic engineering trade-off between noise immunity, speed, and power.

```
PICKING A PULL RESISTOR VALUE
==============================================================================

    Too small (1 kΩ)        Just right (10 kΩ)       Too large (1 MΩ)
    ────────────────        ───────────────────      ───────────────────

    + Strong pull,          + Good noise margin      + Ultra-low power
      very noise-immune     + Low power (~0.3 mA
    - Wastes 3.3 mA           while pressed)         - Slow: RC with
      while pressed         + Fast edges              parasitic C can
      (~11 mW)                (tau ~ 0.1 us for        take milliseconds
    - Hard on the switch      10 pF stray)          - Leakage currents
      contacts                                        (nA) can overwhelm
                                                      the pull
```

**Rule of thumb:** 10kΩ for general GPIO buttons. For fast-switching signals like [[learning/notes/micro-context/i2c|I2C]], drop to 4.7kΩ or 2.2kΩ because bus [[learning/notes/quick-context/capacitance|capacitance]] charges via the pull-up and dominates rise time ($\tau = RC$).

## The Result

```
BEFORE vs AFTER: SIGNAL BEHAVIOR AT THE GPIO PIN
==============================================================================

   NO PULL (broken)              WITH 10 kΩ PULL-UP
   ───────────────               ──────────────────

   V                              V
   3.3 |  .  . .      .           3.3 |─────────┐     ┌─────
       |.   .    . . . .              |         │     │       <- released
   1.5 | . .  .  .   .            ~0  |         └─────┘       <- pressed
       |.  .   . .  . .               |
   0   |────────────────> t       0   |────────────────> t
       random, noisy                  clean, deterministic
```

The pin now has a well-defined default state *and* a clear "active" state, with crisp edges the MCU can sample reliably. Firmware just reads the pin; no debouncing voodoo needed beyond the usual mechanical-bounce filter.

## Why Each Piece Matters

- **GPIO input's high impedance:** This is *why* pulls are needed -- the pin can't establish its own voltage. The same high impedance is *why* a 10kΩ resistor is enough to dominate the floating potential.
- **Pull-up / pull-down resistor:** Provides a weak but deterministic default. Too weak and noise wins; too strong and you waste power and stress the switch.
- **Button / driving source:** Has effectively zero resistance when active, so it trivially overpowers the resistor's weak pull. This asymmetry is what makes the circuit work.
- **$V_{CC}$ and GND rails:** Supply the "rest state" the resistor ties the pin to. Whichever rail the resistor connects to defines whether idle = HIGH or idle = LOW.

## Extension: Internal Pull Resistors

Most modern MCUs (including [[learning/notes/micro-context/stm32-microcontroller|STM32]]) have programmable internal pull-up and pull-down resistors built into every GPIO pin -- typically 30-50 kΩ. You enable them with one register write, saving the external part. External pulls are still used when you need a specific value (like 4.7kΩ for I2C), when the signal must be defined *before* the MCU boots and configures its pins, or when the internal pull is too weak for a noisy environment.

## Go Deeper

**Quick definitions (30 seconds):**
- [[learning/notes/micro-context/smd-resistor]] -- The physical 0402/0603 packages used for pull resistors on PCBs
- [[learning/notes/micro-context/i2c]] -- A bus that *requires* external pull-ups because both lines are open-drain
- [[learning/notes/micro-context/microcontroller]] -- What a GPIO pin is and how the MCU reads it
- [[learning/notes/micro-context/scan-loop]] -- How keyboard matrices rely on pull-ups on every column

**Full treatment (10 minutes):**
- [[learning/notes/quick-context/resistor]] -- Ohm's law, voltage dividers, the pull-up example in detail
- [[learning/notes/quick-context/voltage]] -- Why "floating" voltage is a real thing and what it means physically
- [[learning/notes/quick-context/transistor]] -- Why CMOS inputs have ~1 GΩ impedance in the first place
- [[learning/notes/quick-context/comparator]] -- The circuit that turns an analog pin voltage into a digital 1 or 0; a GPIO input is a comparator with built-in hysteresis
