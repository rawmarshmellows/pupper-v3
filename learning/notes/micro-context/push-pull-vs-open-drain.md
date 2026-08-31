---
term: Push-Pull vs Open-Collector / Open-Drain
created: 2026-06-07
updated: 2026-06-07
---

# Push-Pull vs Open-Collector / Open-Drain

> **Related:** [[learning/notes/quick-context/comparator-specification]] | [[learning/notes/quick-context/bare-minimal-data-storage-circuit]] | [[learning/notes/quick-context/data-bus-and-arbitration]] | [[learning/notes/quick-context/comparator]] | [[learning/notes/quick-context/embedded-communication-protocols]]
## Human notes

**What does "This lets many outputs share one line safely (wired-AND: any device can pull LOW, none fight)" mean?**

An open-drain output has only two states: **pull LOW** (its [[learning/notes/micro-context/mosfet|NMOS]] turns on, connecting the line to GND) or **release** (NMOS off, line floats). It can *never* drive HIGH on its own — a single shared [[learning/notes/small-context/pull-up-pull-down-resistors|pull-up resistor]] does that, holding the line HIGH whenever everyone has released.

- **"none fight"** → Bus contention (a near-short) only happens when one output drives HIGH while another drives LOW — that's two [[learning/notes/quick-context/transistor|transistors]] fighting, VCC dumping straight to GND. Open-drain *deletes* the HIGH-driving transistor, so that fight is physically impossible. The worst case is several devices pulling LOW at once, which just means several NMOS share the one pull-up's small current — harmless.
- **"any device can pull LOW"** → One device turning on its NMOS drags the *whole* shared line LOW, regardless of what the others do. Low always wins.
- **"wired-AND"** → Treat *released* = logic 1, *pulling LOW* = logic 0. The line reads HIGH **only if every device releases** (all 1s). If *any one* pulls LOW, the line is LOW. That is a logical AND of all the devices' states — computed by the wire itself, no gate needed. Hence "wired-AND."

### "Any device can pull LOW" — where OUT/NMOS sit, and why low always wins

Each "device" on a shared open-drain line is an IC whose output stage is open-drain: the box's top is its **OUT** pin, and the NMOS inside is that chip's *own* output transistor. For a [[learning/notes/quick-context/comparator|comparator]] that NMOS is **Q6** (the output stage the [[learning/notes/quick-context/comparator-specification|datasheet]] grades). A **"released" device** has its NMOS *off* — OUT is then an open circuit: high-impedance, floating (it can't pull HIGH — open-drain has no high-side transistor — and isn't pulling LOW). A device that *trips* turns its NMOS on, connecting OUT to GND.

The pull-up is *weak* (e.g. 4.7 kΩ); an NMOS turned on is a *strong* path to GND (tens of ohms), so one tripped device drags the WHOLE line near 0 V (~0.7 mA in the lopsided divider). Released devices supply no current and can't fight it. Below, three open-drain comparators share one FAULT line; **CMP A has tripped, B and C are released:**

```
          VCC
           │
       [ Rpull ]   weak pull-up — gently lifts the line HIGH
           │
   FAULT ──●───────────●───────────●───────────●──────►  to MCU input pin
                       │           │           │
                      OUT         OUT         OUT          ← each chip's output PIN
                       │           │           │
                   ┌───────┐   ┌───────┐   ┌───────┐
                   │NMOS=Q6│   │NMOS=Q6│   │NMOS=Q6│       ← internal output FET
                   └───┬───┘   └ ─ ─ ─ ┘   └ ─ ─ ─ ┘
                       │        (Q6 off)    (Q6 off)
                      GND        OUT open    OUT open
                   CMP A       CMP B       CMP C
                   TRIPPED     released    released
                   Q6 ON,      (high-Z)    (high-Z)
                   pulls LOW
```

Read one column top-to-bottom: the shared FAULT line → that comparator's **OUT** pin → its internal **NMOS (Q6)** → GND. CMP A's Q6 is ON (solid path to GND), so it pulls FAULT LOW; CMP B and C are released (Q6 off, OUT open) and just float with whatever the line does. Even if all three tripped, they'd be parallel paths to GND — still LOW, no short. **No number of released devices beats one that's pulling.** Only an *open-drain* comparator (LMC7221) can sit here — a push-pull part (LMC7211-N) has a high-side transistor too and would fight (contention). The leftmost `●` is just where the single pull-up taps the line, not a device.

Examples:
- **Fault/alarm bus** (the diagram above) — several open-drain comparators, each watching a different rail; any one tripping pulls FAULT LOW, so the MCU watches a single pin for "something's wrong."
- **I2C ACK bit** — the sender releases [[learning/notes/micro-context/i2c|SDA]]; the receiver yanks it LOW for one clock = "got your byte." One device, one pull, whole line LOW.
- **Buttons on a pulled-up pin** — wire several buttons-to-GND on one line; pressing *any* one makes the line LOW, so the MCU reads "a button is down" on a single pin.

### "Wired-AND" — the logic that fact implements

With *released* = 1 and *pulling LOW* = 0, the wire computes `line = A AND B AND C` — no gate, just the resistor and the NMOS transistors:

```
  A   B   C  │ line
  1   1   1  │  1   ← all released → pull-up wins → HIGH
  1   1   0  │  0   ← C pulls → LOW
  0   1   1  │  0   ← A pulls → LOW
  0   0   0  │  0
```

HIGH only when every input is 1 = the AND truth table.

Examples:
- **"All ready" barrier** — each board holds the line LOW while busy, releases when done. The line goes HIGH only when *every* board is done (`done_A AND done_B AND …`), so the CPU learns the whole system is ready from one pin.
- **I2C clock stretching** — SCL is wired-AND: the master pulses the clock, but any slow slave can *hold SCL LOW* to say "wait." SCL rises only when master **and** all slaves release — the slowest device gates the clock.

**Polarity footnote (why you'll also hear "wired-OR"):** same circuit, flipped labels. If the *signal* is active-LOW (LOW = "asserted"), then "any device pulls LOW" reads as "any device asserts" = **OR**. Voltage view → wired-AND (HIGH needs all releasing); active-low signal view → wired-OR (asserted if *any* device asserts). The FAULT bus above is exactly this: HIGH only while every comparator releases (wired-AND on voltage), but read as "fault if *any* comparator trips" (wired-OR on the active-low meaning). A shared `/INT` interrupt line works the same way.

This is exactly why [[learning/notes/micro-context/i2c|I2C]] and shared interrupt lines use open-drain: any chip can assert the line, and no combination of drivers can ever short the bus.

**What is "OUT" in the diagram?** It's the chip's single output pin — where the transistor structure meets the outside wire. Push-pull vs open-drain describes *how* that pin is driven.

In a [[learning/notes/quick-context/comparator|comparator]], OUT is the pin carrying the 1-bit decision "is V+ > V−?", driven by the output stage (Q6 in the LMC7211-N — see [[learning/notes/quick-context/comparator-specification|datasheet specs]]):

```
   V(+) ──┐
          ├──►  [ comparator guts ]  ──►  OUT   (HIGH if V+ > V−, else LOW)
   V(−) ──┘                                ▲
                                           │
                            driven by the OUTPUT STAGE (Q6)
```

- **Push-pull OUT** (LMC7211-N): actively driven HIGH *and* LOW — clean levels, drives an LED or logic gate directly, but can't share a wire.
- **Open-drain OUT** (its cousin the LMC7221): only pulls LOW, needs a pull-up to go HIGH — lets the pull-up set the HIGH level from a different rail (level-shifting) and lets many outputs share one line.

The spec rows `$V_{OH}$/$V_{OL}$` (how close OUT gets to each rail) and `$I_{SC}$` (how hard OUT drives) both grade this exact pin.

> **See also:** [[learning/notes/micro-context/mosfet]] | [[learning/notes/micro-context/i2c]] | [[learning/notes/small-context/pull-up-pull-down-resistors]]

**Definition:** Two ways a digital chip drives its output pin. A **push-pull** output uses two transistors to actively drive both HIGH and LOW. An **open-collector** (BJT) or **open-drain** (MOSFET) output uses a single transistor that can only pull LOW — going HIGH relies on an external pull-up resistor.

## How It Works

- **Push-pull:** a high-side transistor connects the pin to VCC (sources current, drives HIGH) and a low-side transistor connects it to GND (sinks current, drives LOW); only one is on at a time.
- Push-pull gives strong, fast drive in both directions, but two such outputs must never share a wire — one driving HIGH against another driving LOW is a near-short (bus contention).
- **Open-drain:** only the low-side transistor exists; turning it on sinks the pin LOW, turning it off lets the pin "float" so an external [[learning/notes/small-context/pull-up-pull-down-resistors|pull-up resistor]] raises it HIGH.
- This lets many outputs share one line safely (wired-AND: any device can pull LOW, none fight) and lets the pull-up set a different logic voltage — which is why [[learning/notes/micro-context/i2c|I2C]] buses and interrupt lines use open-drain.

```
   PUSH-PULL (totem-pole)            OPEN-DRAIN / OPEN-COLLECTOR
         VCC                           VCC
          │                             │
       ┌──┴──┐  high-side            ┌──┴──┐  external
       │ PMOS│  sources HIGH         │  R  │  pull-up
       └──┬──┘                       └──┬──┘
          ●──── OUT                     ●──── OUT
       ┌──┴──┐  low-side             ┌──┴──┐  low-side only
       │ NMOS│  sinks LOW            │ NMOS│  sinks LOW
       └──┬──┘                       └──┬──┘
          │                             │
         GND                           GND

   Drives HIGH and LOW                  Drives LOW; pull-up makes HIGH
   Never wire two together              Many share one line (wired-AND)
```

**Key insight:** Open-drain trades active drive strength for the ability to share a wire — that "weakness" (only pulling LOW) is exactly what stops multiple devices from short-circuiting each other on a shared bus.
