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

> **See also:** [[learning/notes/quick-context/related-topic]] | [[learning/notes/quick-context/another-topic]]

**Definition:** [1-2 sentences max. What is it? What does it do?]

## How It Works

[2-4 concise bullet points explaining the mechanism/process step by step. Each bullet should be 1 sentence. Focus on the causal chain — what happens and why.]

```
[ONE small ASCII diagram that captures the core concept visually - 10-15 lines max]
```

**Key insight:** [One sentence - the "aha" moment or common misconception]
```

## Guidelines

1. **Maximum length:** ~15-20 lines total (excluding diagram)
2. **One diagram only:** Small, focused, captures the essence
3. **"How It Works" section:** 2-4 bullet points max, each one sentence. Explains the causal chain — no deep dives (that's what quick-context is for)
4. **Link inline, not just at top:** Only include links where they naturally fit in the text and help understanding. Don't list unrelated topics in "See also" just because they're tangentially related—every link should have a clear reason the reader would want to follow it from this context
5. **Glossary tone:** Neutral, factual, definitional
6. **Verify ASCII diagrams:** After creating any ASCII diagram, carefully review it to ensure:
   - Lines connect properly and don't have gaps or misalignments
   - Waveforms (sine waves, square waves, etc.) show the correct shape above AND below the baseline
   - Labels align with what they're pointing to
   - The diagram accurately represents the concept (e.g., AC current must show alternating positive/negative values)
7. **Math notation:** Use LaTeX for all mathematical expressions:
   - Inline math: `$V = IR$` renders as $V = IR$
   - Display math: `$$P = IV$$` renders on its own line
   - Use LaTeX for variables, equations, units with exponents, and formulas

## REQUIRED: Check Obsidian Vault First

Before creating the context file, you MUST check if a relevant note already exists in the Obsidian vault at `brain/obsidian/`:

1. **Search** for files matching the topic:
   - Use `Glob` with patterns like `brain/obsidian/*topic*.md` (try Title Case, lowercase, abbreviations, synonyms)
   - Also check subdirectories: `brain/obsidian/**/*topic*.md`
   - Try alternative names — e.g., for "clock edges" also try "Clock Edge", "Clock Signal", etc.
2. **If a matching file exists**, read it fully
3. **Use it as a foundation** — incorporate the Obsidian note's content, structure, and insights into the new micro-context file. Reformat to match the micro-context template, but preserve the substance and any unique explanations from the original
4. **If no match is found**, proceed with web research as normal

---

## Output

Save to `learning/notes/micro-context/` folder with kebab-case filename (e.g., `learning/notes/micro-context/clock-edges.md`). Create the folder if it doesn't exist.

## Required: Link to Existing Files

Before writing:
1. Search `learning/notes/quick-context/*.md` for related topics
2. **Only add "See also" links if there's a clear, direct relationship** that the reader would want to explore
3. **Prefer inline links** within the definition or key insight where they naturally fit (e.g., "...used in [[learning/notes/quick-context/pcb-printed-circuit-board|PCB]] assembly...")
4. If a quick-context file mentions this term, add a back-link: `[[learning/notes/micro-context/term-name|term]]`

**Bad:** Listing 3 topics in "See also" that are vaguely related but don't help understanding
**Good:** One inline link where the concept naturally appears in the definition

---

## Post-Processing (REQUIRED)

After creating or updating the micro-context file, you MUST run these skills in order:

1. **Fact-check:** Run `/fact-check <output-file-path>` to verify all factual claims
2. **ASCII-fixer:** Run `/ascii-fixer <output-file-path>` to fix any diagram alignment issues

Do not consider the task complete until both post-processing steps have been run.

3. **Consolidation check:** Run `/consolidate-context` to check for overlapping or redundant context files

## Example

```markdown
---
term: Clock Edge
created: 2026-01-26
---

# Clock Edge

> **See also:** [[learning/notes/quick-context/transistor-analog-to-digital]]

**Definition:** The precise moment when a clock signal transitions between states - either rising (0→1) or falling (1→0). Digital circuits sample data only at clock edges to avoid reading signals while they're in transition.

## How It Works

- The clock oscillator generates a continuous square wave that alternates between high (1) and low (0).
- On each rising or falling transition, flip-flops and registers "snapshot" their input signals.
- Between edges, signals are free to change and settle — the circuit ignores this intermediate noise.
- By the next edge, all signals have stabilized, so every component reads consistent, valid data.

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
