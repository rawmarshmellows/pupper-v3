---
term: Input Offset Voltage (V_OS)
created: 2026-06-07
---

# Input Offset Voltage ($V_{OS}$)

> **Related:** [[micro-context/offset-voltage-drift]] | [[micro-context/capacitive-voltage-sensing]] | [[micro-context/input-bias-current]] | [[micro-context/input-common-mode-range]] | [[micro-context/open-loop-voltage-gain]]

**[[quick-context/capacitance|Definition]]:** A small built-in voltage error between a [[quick-context/comparator|comparator]]'s (or op-amp's) [[micro-context/schmitt-trigger-hysteresis|two]] inputs, caused by [[quick-context/transistor|transistor]] mismatch in the [[quick-context/differential-pair|differential input pair]]. It shifts the real switching point to $V_{REF} \pm V_{OS}$ instead of exactly $V_{REF}$, so it sets [[quick-context/mcp6541-as-lmc7211-replacement|your]] [[micro-context/capacitive-voltage-sensing|threshold]] [[quick-context/rc-oscillator|accuracy]].

## How It Works

- The input pair (Q1/Q2) is *drawn* identical, but real silicon etches slightly differently, so the two transistors don't split the [[micro-context/tail-current|tail current]] evenly at exactly $V(+) = V(-)$.
- The few millivolts of input difference needed to re-balance them *is* the offset voltage.
- It's a fixed DC error per part, [[micro-context/can-bus-termination|not]] noise — so it stacks directly onto any reference-divider tolerance to set total threshold accuracy.
- Datasheets list a *Typ* (statistical center at 25°C) [[micro-context/push-pull-vs-open-drain|and]] guaranteed *Limit* columns; the **boldface** limit holds over the full temperature range.

```
   ideal threshold        real threshold
        |                  |
        |   V_OS (a few mV)|
        v   |------------->v
  ------*------------------*------>  V(-) input voltage
     V_REF           V_REF + V_OS
                          |
   Output actually flips here, not at V_REF.

   Cause: Q1 and Q2 of the differential pair aren't
   perfectly matched, so they don't balance at V(+)=V(-).
```

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** $V_{OS}$ is not noise you can average away — it's a fixed error baked into each individual part, so the [[quick-context/comparator-specification|only]] honest design number is the guaranteed **boldface** limit (e.g. ≤8 mV over temperature), never the pretty "typical" 3 mV.
