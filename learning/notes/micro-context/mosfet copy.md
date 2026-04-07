---
term: MOSFET
created: 2026-04-02
---
> **See also:** [[learning/notes/micro-context/mosfet|MOSFET]] | [[learning/notes/quick-context/transistor|Transistor]] | [[learning/notes/quick-context/doped-silicon|Doped Silicon]]


# MOSFET

**Definition:** A [[learning/notes/quick-context/voltage|voltage]]-controlled switch/valve for [[learning/notes/quick-context/electric-current|electric current]]. It has three terminals — **gate**, **drain**, and **source** — and the voltage applied to the gate controls how much current flows between drain and source. "M1", "M2", etc. are just labels for individual MOSFETs in a circuit (like naming resistors R1, R2).

## How It Works

- The **gate** is the control input — it's electrically insulated from the channel by a thin oxide layer, so no current flows into it; only voltage matters.
- When $V_{gs}$ (gate-to-source voltage) exceeds a threshold $V_{th}$, an electric field through the oxide creates a conductive channel between drain and source, allowing current to flow.
- More $V_{gs}$ above threshold = more conductive channel = more current — this is how a [[learning/notes/micro-context/mosfet|MOSFET]] acts as a variable valve, not just an on/off switch.
- In **saturation** (the region used for amplification), drain current depends mainly on $V_{gs}$ and is nearly independent of drain voltage — this is why MOSFETs make good current sources in circuits like [[micro-context/current-mirror|current mirrors]].

```
         drain (D)
           |
           |  current flows
           |  (controlled by gate)
           |
  gate ----+  <- oxide insulator between
  (G)      |     gate and channel
           |     (no current into gate)
           |
           |
         source (S)

  Vgs > Vth  -->  channel ON, current D to S
  Vgs < Vth  -->  channel OFF, no current
```

**Key insight:** The gate never carries current — it's a pure voltage sensor. This makes MOSFETs extremely efficient to control (nearly zero input power) and is why billions of them can sit on a single chip without overheating just from their control signals.
