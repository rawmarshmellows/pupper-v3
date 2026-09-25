---
term: Input Common-Mode Range (CMVR)
created: 2026-06-07
---

# Input Common-Mode Range ($CMVR$)

> **Related:** [[micro-context/common-mode-rejection-ratio]] | [[micro-context/input-bias-current]] | [[micro-context/input-offset-voltage]] | [[micro-context/4-wire-kelvin-measurement]] | [[micro-context/ac-dc-current]]

**[[quick-context/capacitance|Definition]]:** The range of input [[quick-context/voltage|voltage]] (common to [[quick-context/bjt-specifications|both]] pins) over which a [[quick-context/comparator|comparator]] or op-amp still works correctly. "[[quick-context/op-amp|Rail-to-rail]]-[[micro-context/push-pull-vs-open-drain|and]]-beyond" parts accept inputs slightly *past* both supply rails.

## How It Works

- The input [[quick-context/differential-pair|differential pair]] only senses correctly while its transistors stay in their active region, which requires the input voltage to sit inside a usable window.
- Outside that window the pair stops steering current properly and the output becomes invalid — regardless of how good the offset or gain is.
- The [[quick-context/comparator-specification|LMC7211-N]]'s −0.3 to 3.0 V range on a 0–2.7 V supply means inputs work slightly below ground and slightly above $V^+$.
- That extra margin lets you sense a divider node sitting right at ground or right at the top rail without a dead zone.

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

**[[micro-context/4-wire-kelvin-measurement|Key insight:]]** CMVR is about *where the inputs are allowed to sit*, [[micro-context/can-bus-termination|not]] the difference between them — a part can have great offset and gain yet output garbage if [[quick-context/mcp6541-as-lmc7211-replacement|your]] signal sits outside its common-mode window.
