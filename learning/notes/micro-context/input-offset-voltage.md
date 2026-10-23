---
term: Input Offset Voltage (V_OS)
created: 2026-06-07
---

> **Related:** [[learning/notes/micro-context/offset-voltage-drift]] | [[learning/notes/micro-context/ads1110-battery-adc]] | [[learning/notes/micro-context/buck-converter]] | [[learning/notes/micro-context/capacitive-voltage-sensing]] | [[learning/notes/micro-context/input-bias-current]]

# Input Offset Voltage ($V_{OS}$)

> **See also:** [[quick-context/comparator-specification]] | [[quick-context/differential-pair]] | [[quick-context/comparator]]

**[[learning/notes/quick-context/capacitance|Definition]]:** A small built-in [[learning/notes/quick-context/voltage|voltage]] error between a [[learning/notes/quick-context/comparator|comparator]]'s (or op-amp's) [[learning/notes/micro-context/schmitt-trigger-hysteresis|two]] inputs, caused by [[learning/notes/quick-context/silicon-die|transistor]] mismatch in [[learning/notes/quick-context/capacitance|the]] [[quick-context/differential-pair|differential input pair]]. It shifts the real switching [[learning/notes/quick-context/epson-rc-plus-programming|point]] to $V_{REF} \pm V_{OS}$ instead of exactly $V_{REF}$, so it sets [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] threshold [[learning/notes/quick-context/rc-oscillator|accuracy]].

## How It Works

- The input pair (Q1/Q2) is *drawn* [[learning/notes/quick-context/ram-addressing-decoder|identical]], but real [[learning/notes/quick-context/transistor|silicon]] etches slightly differently, so the two transistors don't split the [[learning/notes/micro-context/tail-current|tail current]] evenly at exactly $V(+) = V(-)$.
- The few millivolts of input difference needed to re-balance them *is* the offset voltage.
- It's a fixed DC error per part, [[learning/notes/micro-context/can-bus-termination|not]] noise — so it stacks directly onto any [[learning/notes/quick-context/comparator|reference]]-divider [[learning/notes/quick-context/cnc-machining|tolerance]] to set [[learning/notes/quick-context/similarity-transform|total]] threshold accuracy.
- Datasheets list a *Typ* (statistical center at 25°C) [[learning/notes/micro-context/push-pull-vs-open-drain|and]] guaranteed *Limit* columns; the **[[learning/notes/quick-context/comparator-specification|boldface]]** limit [[learning/notes/quick-context/pupper-lab7-vision-tracking|holds]] over the [[learning/notes/quick-context/singular-value-decomposition|full]] temperature range.

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

**Key insight:** $V_{OS}$ is not noise you [[learning/notes/quick-context/embedded-communication-protocols|can]] average away — it's a fixed error baked into each individual part, so the [[learning/notes/quick-context/comparator-specification|only]] honest design number is the guaranteed **boldface** limit (e.g. ≤8 mV over temperature), never the pretty "typical" 3 mV.
