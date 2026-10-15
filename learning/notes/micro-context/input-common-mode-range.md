---
term: Input Common-Mode Range (CMVR)
created: 2026-06-07
---

> **Related:** [[learning/notes/micro-context/common-mode-rejection-ratio]] | [[learning/notes/micro-context/input-bias-current]] | [[learning/notes/micro-context/input-offset-voltage]] | [[learning/notes/quick-context/common-ic-packages]]

# Input Common-Mode Range ($CMVR$)

> **[[learning/notes/quick-context/tensile-strength-materials|]]See also:** [[quick-context/comparator-specification]] | [[quick-context/differential-pair]] | [[quick-context/comparator]]

**[[learning/notes/quick-context/capacitance|Definition]]:** [[learning/notes/quick-context/capacitance|The]] range of input [[learning/notes/quick-context/voltage|voltage]] (common to [[learning/notes/quick-context/bjt-specifications|both]] pins) over which [[learning/notes/quick-context/anions-and-oxidation|a]] [[learning/notes/quick-context/comparator|comparator]] [[learning/notes/micro-context/push-pull-vs-open-drain|or]] op-amp still works correctly. "[[learning/notes/quick-context/op-amp|Rail-to-rail]]-[[learning/notes/micro-context/push-pull-vs-open-drain|and]]-beyond" parts accept inputs slightly *past* both supply rails.

## How It Works

- The input [[quick-context/differential-pair|differential pair]] [[learning/notes/quick-context/comparator-specification|only]] senses correctly while its transistors stay in their active region, which requires the input voltage to sit inside a usable window.
- Outside that window the pair stops steering [[learning/notes/quick-context/capacitance|current]] properly and the output becomes invalid — regardless of how good the offset or gain is.
- The [[learning/notes/quick-context/comparator-specification|LMC7211-N]]'s −[[learning/notes/quick-context/meddpicc-qualification-framework|0]].[[learning/notes/quick-context/meddpicc-qualification-framework|3]] to 3.0 [[learning/notes/quick-context/capacitor|V]] range on a 0–[[learning/notes/quick-context/meddpicc-qualification-framework|2]].[[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|7 V]] supply means inputs work slightly below ground and slightly above $V^+$.
- That extra margin lets you sense a divider [[learning/notes/quick-context/ros2-architecture|node]] sitting right at ground or right at the [[learning/notes/quick-context/keypress-to-pixel-pipeline|top]] rail without a dead zone.

```
        +--- +0.3 V beyond top rail
   V+ --+==================+   <- inputs valid up to here
        |  usable input    |
        |  common-mode     |   CMVR
        |  window          |
   V- --+==================+   <- and down to here
        +--- -0.3 V below bottom rail  (rail-to-rail-and-beyond)

   Inputs sitting OUTSIDE this window -> invalid output.
```

**Key insight:** CMVR is about *where the inputs are allowed to sit*, [[learning/notes/micro-context/can-bus-termination|not]] the difference between them — a part [[learning/notes/quick-context/embedded-communication-protocols|can]] have great offset and gain yet output garbage if [[learning/notes/quick-context/mcp6541-as-lmc7211-replacement|your]] [[learning/notes/quick-context/comparator|signal]] sits outside its common-mode window.
