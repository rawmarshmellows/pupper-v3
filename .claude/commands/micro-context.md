---
name: micro-context
description: Ultra-brief glossary-style definition with one diagram and links
---

Create an ultra-concise reference entry for **$ARGUMENTS**.

## Format

A micro-context is a **30-second read** - just enough to understand what something is without a full deep-dive. Think "glossary entry with a diagram."

```markdown
---
term: Term Name
created: YYYY-MM-DD
---

# Term Name

> **See also:** [[quick-context/related-topic]] | [[quick-context/another-topic]]

**Definition:** [1-2 sentences max. What is it? What does it do?]

```
[ONE small ASCII diagram that captures the core concept visually - 10-15 lines max]
```

**Key insight:** [One sentence - the "aha" moment or common misconception]
```

## Guidelines

1. **Maximum length:** ~15-20 lines total (excluding diagram)
2. **One diagram only:** Small, focused, captures the essence
3. **No sections:** No "How It Works", no "Key Tension", no questions - that's what quick-context is for
4. **Link inline, not just at top:** Only include links where they naturally fit in the text and help understanding. Don't list unrelated topics in "See also" just because they're tangentially related—every link should have a clear reason the reader would want to follow it from this context
5. **Glossary tone:** Neutral, factual, definitional
6. **Verify ASCII diagrams:** After creating any ASCII diagram, carefully review it to ensure:
   - Lines connect properly and don't have gaps or misalignments
   - Waveforms (sine waves, square waves, etc.) show the correct shape above AND below the baseline
   - Labels align with what they're pointing to
   - The diagram accurately represents the concept (e.g., AC current must show alternating positive/negative values)

## Output

Save to `micro-context/` folder with kebab-case filename (e.g., `micro-context/clock-edges.md`). Create the folder if it doesn't exist.

## Required: Link to Existing Files

Before writing:
1. Search `quick-context/*.md` for related topics
2. **Only add "See also" links if there's a clear, direct relationship** that the reader would want to explore
3. **Prefer inline links** within the definition or key insight where they naturally fit (e.g., "...used in [[quick-context/pcb-printed-circuit-board|PCB]] assembly...")
4. If a quick-context file mentions this term, add a back-link: `[[micro-context/term-name|term]]`

**Bad:** Listing 3 topics in "See also" that are vaguely related but don't help understanding
**Good:** One inline link where the concept naturally appears in the definition

## Example

```markdown
---
term: Clock Edge
created: 2026-01-26
---

# Clock Edge

> **See also:** [[quick-context/transistor-analog-to-digital]]

**Definition:** The precise moment when a clock signal transitions between states - either rising (0→1) or falling (1→0). Digital circuits sample data only at clock edges to avoid reading signals while they're in transition.

```
Clock:  ───┐   ┌───┐   ┌───┐   ┌───
           └───┘   └───┘   └───┘
           ↑   ↑   ↑   ↑
        RISING  FALLING
         EDGE    EDGE

        Data is sampled HERE,
        after signals have settled.
```

**Key insight:** Clock edges are why billions of imperfect analog transistors can coordinate as perfect digital switches - they all agree to only "look" at signals at the same precise moments.
```
