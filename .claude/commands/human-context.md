---
name: human-context
description: Save a human's explanation of a concept, fact-check it, correct errors, and link to existing context files
---

Save, fact-check, and link a human explanation: **$ARGUMENTS**

## What This Does

The user is explaining a concept in their own words. Your job is to:

1. Save their explanation to `learning/notes/human-context/`
2. Fact-check every claim against web sources AND existing context files
3. Fix inaccuracies directly in the text, annotating what changed
4. Link terms to existing `learning/notes/micro-context/` and `learning/notes/quick-context/` files
5. Produce a digestible summary (clean bullet-point reference + corrections-at-a-glance table) so the user can quickly re-absorb the right model

The goal is a **verified, linked version of the human's own understanding** — not a rewrite. Preserve their voice and framing. Only change what's factually wrong.

---

## Step 1: Save the Raw Explanation

Create a file in `learning/notes/human-context/` with kebab-case filename based on the concept.

```markdown
---
concept: [Concept Name — inferred from the explanation]
created: YYYY-MM-DD
status: verified
---

# [Concept Name]

> **My understanding:** [The user's original explanation, preserved as-is in this blockquote]

---

[The verified, corrected, and linked version goes below — see Steps 2-4]
```

Create the `learning/notes/human-context/` folder if it doesn't exist.

---

## Step 1b: Check Obsidian Vault

Before fact-checking, check if a relevant note already exists in the Obsidian vault at `brain/obsidian/`:

1. **Search** for files matching the concept:
   - Use `Glob` with patterns like `brain/obsidian/*concept*.md` (try Title Case, lowercase, abbreviations, synonyms)
   - Also check subdirectories: `brain/obsidian/**/*concept*.md`
2. **If a matching file exists**, read it fully
3. **Use it as an additional verification source** in Step 2 — compare the user's claims against the Obsidian note as well as existing context files and web sources. If the Obsidian note has additional context or examples not in the user's explanation, note them but don't add them (this is the user's understanding, not a tutorial)
4. **If no match is found**, proceed to Step 2 as normal

---

## Step 2: Fact-Check Against All Sources

### 2a: Extract Claims

Read the user's explanation and identify every verifiable claim:
- Definitions ("X is...")
- Causal relationships ("X causes Y")
- Numerical values (measurements, thresholds, ratios)
- Mechanisms ("X works by...")
- Comparisons ("X is better/faster/stronger than Y")

### 2b: Check Against Existing Context Files

1. **Glob** `learning/notes/micro-context/*.md` and `learning/notes/quick-context/*.md`
2. **Read files** related to the topic
3. Compare the user's claims against what the existing context files say
4. Note any contradictions between the user's explanation and the verified context files

### 2c: Check Against Web Sources

For claims not covered by existing context files, or where extra verification is needed:
1. **WebSearch** for authoritative sources
2. Compare and note discrepancies

---

## Step 3: Write the Verified Version

Below the blockquoted original, write the corrected version. Rules:

### Corrections
- **Fix errors inline** — don't leave wrong information standing
- **Annotate every correction** with a bracketed note explaining what changed and why:

```markdown
The MOSFET switches by applying voltage to the gate, which creates an electric field
that allows current to flow between source and drain [~~"pushes electrons through the
channel"~~ — current flows due to the electric field creating a conductive channel, not
direct electron pushing].
```

- Keep annotations short — one sentence max
- If the user's explanation is correct but imprecise, leave it unless the imprecision could cause confusion

### Preservation
- **Keep the user's sentence structure and phrasing** wherever correct
- **Keep their analogies and mental models** if they're valid (even if non-standard)
- **Don't add new information** the user didn't mention — this is their understanding, verified, not a tutorial
- **Don't restructure** into sections, tables, or progressive disclosure — keep it as prose

---

## Step 4: Add Obsidian Links

### Inline Links
Link terms in the verified version to existing context files:

```markdown
The [[learning/notes/quick-context/mosfet|MOSFET]] switches by applying voltage to the
[[learning/notes/micro-context/gate-terminal|gate]], which creates an
[[learning/notes/micro-context/electric-field|electric field]]...
```

Rules:
- Only link **first occurrence** of each term
- Don't link terms inside the blockquoted original (that stays untouched)
- Don't link inside correction annotations
- Only link to files that **actually exist** — glob first
- Be conservative — only link clear, direct matches

### Related Header
Add a Related line after the frontmatter linking to the most relevant context files (2-5 max):

```markdown
> **Related:** [[learning/notes/quick-context/mosfet]] | [[learning/notes/micro-context/gate-terminal]]
```

### Back-Links
For each context file linked from the human-context file, consider whether a back-link is warranted. Add back-links in the Peripheral Knowledge section of quick-context files if the human-context file adds a useful perspective. Don't force back-links — human-context files are personal notes, not reference material.

---

## Step 5: Digestible Summary

After the verified prose (which contains inline correction annotations and is dense to read), add a **digestible summary** that lets the user quickly re-absorb the corrected mental model without parsing the inline `[~~...~~]` markup.

This summary has two parts:

### 5a: Quick Reference

A clean bullet-point version of the verified concept — corrections silently applied, no annotations, no blockquote markers. Each bullet is one atomic fact or step. Aim for 5–10 bullets that together cover the same ground as the verified prose.

```markdown
## Quick Reference

- [Atomic, corrected fact 1]
- [Atomic, corrected fact 2]
- ...
```

Rules:
- **No correction markup** in this section — it's the clean, "as it should be understood" version
- **Match the user's mental order** — don't reorganize unless their order was confusing
- **Stay concrete** — keep specific values, names, and chip/term references the user used (corrected if needed)
- Inline links are still allowed (and encouraged) where they help

### 5b: Corrections at a Glance

A table summarizing every correction so the user can scan their misconceptions at speed:

```markdown
## Corrections at a Glance

| What I said | What's actually correct | Why |
|---|---|---|
| [Original claim, brief] | [Corrected claim, brief] | [One-clause reason] |
| ... | ... | ... |
```

Rules:
- One row per inline correction in the verified prose
- Keep each cell short — long explanations stay in the inline annotation
- If there are zero corrections, omit the table entirely and add a single line: `**No corrections needed — verified as written.**`

---

## Step 6: Summary Footer

At the bottom of the file, add a verification summary:

```markdown
---

**Verification:** X claims checked. Y correct, Z corrected. [Sources consulted: brief list]
```

---

## Complete Example

Input: `/human-context I think capacitors work by storing charge on two plates separated by an insulator. When you connect them to a circuit, they charge up exponentially and then discharge exponentially. The time constant is R times C. Bigger capacitors store more energy because E = CV.`

Output file `learning/notes/human-context/how-capacitors-work.md`:

```markdown
---
concept: How Capacitors Work
created: 2026-03-26
status: verified
---

# How Capacitors Work

> **Related:** [[learning/notes/quick-context/capacitor]] | [[learning/notes/micro-context/rc-time-constant]]

> **My understanding:** I think capacitors work by storing charge on two plates separated by an insulator. When you connect them to a circuit, they charge up exponentially and then discharge exponentially. The time constant is R times C. Bigger capacitors store more energy because E = CV.

---

[[learning/notes/quick-context/capacitor|Capacitors]] work by storing charge on two plates separated by an insulator (the [[learning/notes/micro-context/dielectric|dielectric]]). When connected to a circuit, they charge up exponentially and then discharge exponentially. The [[learning/notes/micro-context/rc-time-constant|time constant]] is $\tau = RC$. Bigger capacitors store more energy because $E = \frac{1}{2}CV^2$ [~~"E = CV"~~ — energy stored is $\frac{1}{2}CV^2$, not $CV$; the $\frac{1}{2}$ comes from integrating the voltage as the capacitor charges].

---

## Quick Reference

- A [[learning/notes/quick-context/capacitor|capacitor]] is two conductive plates separated by an insulator (the [[learning/notes/micro-context/dielectric|dielectric]])
- It stores charge on the plates when a voltage is applied across them
- In a circuit it charges and discharges **exponentially**
- The [[learning/notes/micro-context/rc-time-constant|time constant]] is $\tau = RC$
- Energy stored is $E = \tfrac{1}{2}CV^2$ — the $\tfrac{1}{2}$ comes from integrating $V$ as the cap charges

## Corrections at a Glance

| What I said | What's actually correct | Why |
|---|---|---|
| $E = CV$ | $E = \tfrac{1}{2}CV^2$ | Voltage rises linearly as the cap charges, so energy is the integral, not the product |

---

**Verification:** 4 claims checked. 3 correct, 1 corrected. Sources: learning/notes/quick-context/capacitor.md, Wikipedia (capacitor energy formula)
```

---

## Guidelines

- **Voice preservation is paramount.** This is the user's mental model. Don't rewrite it into textbook prose.
- **Correct errors, don't add curriculum.** If they didn't mention a concept, don't teach it to them here.
- **Annotations should teach.** Each correction annotation should help the user understand *why* they were wrong, not just *that* they were wrong.
- **Link generously but accurately.** The linking transforms a personal note into a connected node in the knowledge graph.
- **The blockquoted original is sacred.** Never modify the text inside the `> **My understanding:**` blockquote.

---

## Post-Processing (REQUIRED)

After creating or updating the human-context file, you MUST:

1. **Fact-check:** Run `/fact-check <output-file-path>` to verify all factual claims
2. **Update embeddings (manual):** Remind the user to run `python tools/embed.py sync` to update the embedding cache for semantic linking
