---
term: Input Common-Mode Range (CMVR)
created: 2026-06-07
---

> **Related:** [[learning/notes/micro-context/common-mode-rejection-ratio]]

# Input Common-Mode Range ($CMVR$)

> **See also:** [[quick-context/comparator-specification]] | [[quick-context/differential-pair]] | [[quick-context/comparator]]

**Definition:** The range of input voltage (common to both pins) over which a [[learning/notes/quick-context/comparator|comparator]] or [[learning/notes/quick-context/op-amp|op-amp]] still works correctly. "Rail-to-rail-and-beyond" parts accept inputs slightly *past* both supply rails.

## How It Works

- The input [[quick-context/differential-pair|differential pair]] only senses correctly while its transistors stay in their active region, which requires the input voltage to sit inside a usable window.
- Outside that window the pair stops steering current properly and the output becomes invalid — regardless of how good the offset or gain is.
- The LMC7211-N's −0.3 to 3.0 V range on a 0–2.7 V supply means inputs work slightly below ground and slightly above $V^+$.
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

**Key insight:** CMVR is about *where the inputs are allowed to sit*, not the difference between them — a part can have great offset and gain yet output garbage if your signal sits outside its common-mode window.
