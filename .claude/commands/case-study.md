---
name: case-study
description: Focused walkthrough of how things work together in a specific use case
---

Walk me through **$ARGUMENTS** step by step.

## Purpose

A case-study sits between micro-context and quick-context:

| Level | Length | Question |
|-------|--------|----------|
| micro-context | ~20 lines | "What is X?" |
| **case-study** | ~80-150 lines | "How does X work in this situation?" |
| quick-context | ~200-500 lines | "Tell me everything about X" |

Case studies are for understanding **how things work together in a specific application**. They include just enough about each piece to understand the use case—readers can follow links to quick-context for the full treatment.

---

## Document Template

```markdown
---
case: Descriptive Case Name
components: [component-1, component-2, ...]
created: YYYY-MM-DD
---

# Case: [Descriptive Name]

> **Components:** [[quick-context/component-1]] | [[quick-context/component-2]] | ...
> **Micro-context:** [[micro-context/related-term]] | [[micro-context/another-term]] | ...

> **In brief:** [2-3 sentences describing what we're trying to accomplish and how the pieces work together to achieve it. Link to micro-context inline for key terms.]

## The Situation

[What problem are we solving? What are we trying to achieve? 2-3 sentences max.]

## The Pieces

[Brief intro to each component—just enough context to follow the walkthrough. Each piece gets 2-3 sentences focused on its role in THIS use case, not a full explanation.]

**Piece A:** [What it is and what it does for this use case. Link to [[quick-context/piece-a]] for full treatment.]

**Piece B:** [What it is and what it does for this use case. Link to [[quick-context/piece-b]] for full treatment.]

## Step by Step: What Happens

[The core of the case study. Walk through the process chronologically or logically. Use numbered steps or clear phases. Include ASCII diagrams showing the state at each step.]

```
[ASCII diagram showing the process, with annotations]
```

### Step 1: [Description]
[What happens in this step. Why does it happen? What's the state after?]

### Step 2: [Description]
[Continue the walkthrough...]

### Step 3: [Description]
[...]

## The Result

[What do we end up with? How does the output compare to the input? Include a before/after diagram if helpful.]

```
[Final state diagram or comparison]
```

## Why Each Piece Matters

[Brief summary connecting each component's role to the outcome. This reinforces understanding without repeating the walkthrough.]

- **Piece A:** [Its essential contribution]
- **Piece B:** [Its essential contribution]

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/term-1]] — Ultra-brief definition
- [[micro-context/term-2]] — Ultra-brief definition

**Full treatment (10 minutes):**
- [[quick-context/component-1]] — Full treatment of [component 1]
- [[quick-context/component-2]] — Full treatment of [component 2]
```

---

## Guidelines

1. **Focus on ONE use case:** Don't try to cover all applications—that's what quick-context is for
2. **Assume no prior knowledge:** But don't teach everything—just enough for this case
3. **Show the process:** Use step-by-step structure with diagrams at key stages
4. **Link liberally to quick-context:** For readers who want depth on any component
5. **Keep it scannable:** Someone should be able to skim the headers and diagrams and get the gist
6. **80-150 lines:** Long enough to explain the mechanics, short enough to stay focused

## ASCII Diagram Guidelines

After creating any ASCII diagram, verify:
- Lines connect properly without gaps
- Waveforms show correct shapes (AC goes above AND below baseline)
- Labels align with what they're pointing to
- Flow arrows point in the correct direction
- State changes between steps are visually clear

## Math Notation

Use LaTeX for all mathematical expressions:
- Inline math: `$V = IR$` renders as $V = IR$
- Display math: `$$P = IV$$` renders on its own line
- Use LaTeX for variables, equations, units with exponents, and formulas throughout the document

---

## Output

Save to `case-study/` folder with kebab-case filename describing the use case (e.g., `case-study/ac-to-dc-conversion.md`). Create the folder if it doesn't exist.

Include YAML frontmatter with:
- `case`: Descriptive case name
- `components`: List of main components involved
- `created`: Today's date in YYYY-MM-DD format

---

## Required: Link to Existing Files

Before writing:
1. Search `quick-context/*.md` AND `micro-context/*.md` for related topics
2. Read relevant files to understand what's already covered
3. Link to quick-context files for each component in the "Components" header
4. Link to micro-context files for key terms in the "Micro-context" header
5. Add inline links where concepts naturally appear in the text (prefer micro-context for quick definitions, quick-context for deeper dives)
6. In "Go Deeper" section, organize links by depth level (micro-context first, then quick-context)
7. After creating the case study, add back-links from related files (Peripheral Knowledge sections in quick-context, See also in micro-context)

---

## Example: Good Case Study Structure

```markdown
---
case: AC to DC Power Conversion
components: [diode, capacitor]
created: 2026-02-08
---

# Case: AC to DC Power Conversion

> **Components:** [[quick-context/diode]] | [[quick-context/capacitor]]
> **Micro-context:** [[micro-context/ac-dc-current]] | [[micro-context/diode-rectification]]

> **In brief:** Wall power is [[micro-context/ac-dc-current|AC]] but electronics need [[micro-context/ac-dc-current|DC]]. Diodes act as one-way valves ([[micro-context/diode-rectification|rectification]]), then capacitors smooth out the bumps into steady DC.

## The Situation
[...]

## The Pieces
**Diodes:** [Role in this case...]
**Capacitors:** [Role in this case...]

## Step by Step: What Happens
### Step 1: AC Input
[...]

## The Result
[...]

## Go Deeper

**Quick definitions (30 seconds):**
- [[micro-context/ac-dc-current]] — What AC and DC mean
- [[micro-context/diode-rectification]] — Ultra-brief definition of rectification

**Full treatment (10 minutes):**
- [[quick-context/diode]] — PN junction physics, LEDs, Zeners, breakdown voltage
- [[quick-context/capacitor]] — Decoupling, supercapacitors, RC time constants
```

---

## Post-Processing (REQUIRED)

After creating or updating the case-study file, you MUST run these skills in order:

1. **Fact-check:** Run `/fact-check <output-file-path>` to verify all factual claims
2. **ASCII-fixer:** Run `/ascii-fixer <output-file-path>` to fix any diagram alignment issues

Do not consider the task complete until both post-processing steps have been run.
