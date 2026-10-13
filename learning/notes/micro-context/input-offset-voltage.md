---
term: Input Offset Voltage (V_OS)
created: 2026-06-07
---
> **Related:** [[learning/notes/micro-context/offset-voltage-drift]] | [[learning/notes/micro-context/input-bias-current]] | [[learning/notes/micro-context/input-common-mode-range]] | [[learning/notes/micro-context/open-loop-voltage-gain]] | [[learning/notes/micro-context/output-voltage-swing]]


# Input Offset Voltage ($V_{OS}$)

> **[[learning/notes/micro-context/4-wire-kelvin-measurement|See also:]]** [[quick-context/comparator-specification]] | [[quick-context/differential-pair]] | [[quick-context/comparator]]

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Definition:]]** A small built-in [[learning/notes/quick-context/voltage|voltage]] error between a [[learning/notes/quick-context/comparator|comparator]]'s (or op-amp's) two inputs, caused by [[learning/notes/quick-context/transistor|transistor]] mismatch in the [[quick-context/differential-pair|differential input pair]]. It shifts the real switching [[learning/notes/quick-context/epson-rc-plus-programming|point]] to $V_{REF} \pm V_{OS}$ instead of exactly $V_{REF}$, so it sets [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] [[learning/notes/micro-context/capacitive-voltage-sensing|threshold]] [[learning/notes/quick-context/rc-oscillator|accuracy]].

## How It Works

- The input pair (Q1/Q2) is *drawn* [[learning/notes/quick-context/ram-addressing-decoder|identical]], but real [[learning/notes/quick-context/transistor|silicon]] etches slightly differently, so the two transistors don't split the [[learning/notes/micro-context/tail-current|tail current]] evenly at exactly $V(+) = V(-)$.
- The few millivolts of input difference needed to re-balance them *is* the offset voltage.
- It's a fixed DC error per part, not noise — so it stacks directly onto any [[learning/notes/quick-context/comparator|reference]]-divider [[learning/notes/quick-context/cnc-machining|tolerance]] to set [[learning/notes/quick-context/similarity-transform|total]] threshold accuracy.
- Datasheets list a *Typ* (statistical center at 25°C) and guaranteed *Limit* columns; the **boldface** limit [[learning/notes/quick-context/pupper-lab7-vision-tracking|holds]] over the [[learning/notes/quick-context/singular-value-decomposition|full]] temperature range.

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

**[[learning/notes/micro-context/4-wire-kelvin-measurement|Key insight:]]** $V_{OS}$ is not noise you can average away — it's a fixed error baked into each individual part, so the [[learning/notes/quick-context/comparator-specification|only]] honest design number is the guaranteed **boldface** limit (e.g. ≤8 mV over temperature), never the pretty "typical" 3 mV.
