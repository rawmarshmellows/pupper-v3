---
name: index-spine
description: Turn a brain dump of your current understanding into a navigational index-spine that links all related notes/code into one climbable ladder of abstraction, and fills the gaps by authoring the missing notes
---

Take the user's **brain dump** in **$ARGUMENTS** and build an **index-spine**: one
navigational document that stitches every relevant note and code artifact in the
repo into a single, climbable ladder of abstraction — readable top-to-bottom as ONE
continuous story — then **fill the gaps** by authoring the notes that are missing.

An index-spine is the marriage of three things:
- a **coverage map** (a navigational hub + gap analysis for a topic),
- a **narrative spine** (an ordered ladder where each layer flows into the next), and
- a **gap-filler** (it doesn't just mark gaps — it writes the missing notes).

The user's input is a *brain dump of their current understanding* — possibly messy,
partial, or out of order. Your job is to extract the implied ladder, ground it in
what already exists, and produce a spine that lets them (and a beginner) intuitively
grasp and explain the whole topic end to end.

---

## Input forms ($ARGUMENTS)

`$ARGUMENTS` may be any of:
- **Raw brain-dump text** — the user's freeform explanation of what they understand.
- **A path to a file** containing the brain dump or a seed note (e.g. a
  `quick-context` note that anchors the topic). If it's a path, read it.
- **A topic phrase** plus optional flags.

Optional flags the user may include:
- `--seed <path>` — the anchor note the spine is built around (its narrative is the
  backbone). Read it first and treat its arc as the spine's skeleton.
- `--code <dir>` — a directory of code/course material (e.g.
  `learning/references/courses/...`) to mine for **executable anchors**: real source
  files that *implement* a conceptual layer. Reference read-only; never edit them.

If the brain dump is ambiguous about the **bottom anchor** (the simplest concrete
starting point) or the **top anchor** (the end-to-end outcome the user wants to be
able to explain), ask ONE clarifying question before proceeding. Otherwise proceed.

---

## Phase 1: Parse the brain dump → extract the ladder

From the dump, extract:

1. **The narrative arc** — the "from X → Y" story (e.g. "from a switch → to a letter
   on screen"). Name the **bottom anchor** (simplest concrete thing) and the **top
   anchor** (the capability the user wants to be able to explain).
2. **The ordered layers** — break the arc into 6–14 layers, each climbing one rung of
   abstraction. Order them foundational → advanced. Each layer answers one question
   ("What is X?" / "How does X become Y?").
3. **What the user already understands** — note which layers the dump covers well,
   which are shaky or wrong (you'll gently correct these in the spine), and which the
   user didn't mention but the arc requires (silent gaps).

Output this skeleton to the user as a numbered layer list before building, so they
can correct the ordering:

```
SPINE: [bottom anchor] -> [top anchor]

  L0  [layer name] - [the question it answers]
  L1  [layer name] - [the question it answers]
  ...
  LN  [layer name] - [the question it answers]
```

---

## Phase 2: Discover existing coverage

**Before writing anything:**

1. **Glob** `learning/notes/quick-context/*.md`, `learning/notes/small-context/*.md`,
   and `learning/notes/micro-context/*.md`.
2. **Read** at least the frontmatter, TL;DR, and 5 Essential Terms of every plausibly
   relevant file. Be inclusive — partial relevance still counts.
3. For each layer from Phase 1, collect the note(s) that cover it.
4. (Optional — skip if the embedding DB isn't built) Run
   `python tools/embed.py related <path>` on the seed and each layer's primary note to
   surface related docs. If unavailable, fall back to Glob + Grep keyword sweeps.
5. If `--code <dir>` was given (or the brain dump points at code), map each layer to
   the **real source file(s)** that implement it — list the relative paths.
6. Run `/consolidate-context` thinking: if two existing notes overlap heavily on one
   layer, link both but don't duplicate them in the spine.

---

## Phase 3: Assign anchors + identify gaps

For each layer, assign up to **two anchors**:

- **Intuition anchor** — the repo note(s) that explain the concept. Use canonical
  wiki-links `[[learning/notes/<tier>/<slug>]]`.
- **Executable anchor** (when it exists) — the real code/artifact that *implements*
  the concept ("here is the idea as runnable code"), cited by relative path.

A reader should be able to see the SAME idea twice — as intuition and as artifact.

Mark every layer that has **no intuition anchor** as a **GAP**. Decide the tier for
each gap:
- `/quick-context` — a substantial topic (4-level progressive disclosure).
- `/small-context` — "how X works in this specific situation."
- `/micro-context` — a glossary term + one diagram.

---

## Phase 4: Fill the gaps (author the missing notes)

**Spawn parallel subagents** (Task tool, `subagent_type: "general-purpose"`), one per
gap, issued in a SINGLE response so they run concurrently. Each agent:

1. Runs the matching note-creation skill (`/quick-context`, `/small-context`, or
   `/micro-context`) for its gap.
2. Assumes the reader has ZERO background in the domain; uses ASCII/table diagrams.
3. Cites BOTH anchors where applicable — the intuition AND the executable artifact
   (real path) the concept maps to.
4. Adds `> **Related:** [[learning/notes/index/<spine-slug>]]` linking back to
   the spine (the spine's own slug — created in Phase 5).
5. Links to the adjacent layers' notes (the rung below and above it).

If there are more than ~8 gaps, list them and ask the user whether to fill all or a
subset. Never overwrite an existing note without confirmation.

---

## Phase 5: Write the index-spine

Save to `learning/notes/index/<topic-kebab>-index.md` (create the `index/` folder if
it does not exist). Follow the repo's index/coverage-map document structure exactly:

```markdown
---
topic: [Topic] — Index-Spine
created: [today's date YYYY-MM-DD]
updated: [today's date YYYY-MM-DD]
---

> **Related:** [[learning/notes/quick-context/anchor-1]] | [[learning/notes/quick-context/anchor-2]]

> **TL;DR:** [1-2 sentences: the arc (bottom -> top anchor) and what following this spine lets you do — climb from the simplest piece to explaining the whole thing.]

# [Topic] — Index-Spine

## The Core Problem: [Why this topic needs a spine]

[2-4 sentences: why the topic is hard to hold in your head, what span it covers, why a single climbable ladder helps.]

## 5 Essential Terms

| Term | Definition |
|------|------------|
| ... | ... |
```

Then, inside `<details>` sections (mirroring the other index files):

### Section: "The Ladder — climb it top to bottom"
The heart of the spine. For EACH layer, in order:

1. **Layer heading** — `### L[n] — [name]` and the one-line question it answers.
2. **Intuition** — 1–3 plain-English sentences. If the user's brain dump got this
   layer wrong or fuzzy, correct it here, plainly.
3. **Anchors** — the intuition note link(s) and, where it exists, the executable
   artifact path. Format: `Concept: [[...]]  ·  Code: path/to/file`.
4. **Bridge** — a short paragraph: "…and that is why we now need the next rung." This
   is what turns a list of links into ONE story. Every layer except the last has one.

### Section: "The Whole Ladder at a Glance"
A single ASCII diagram of the full ladder, bottom → top, with ✅ (note exists) / 🆕
(note created by this run) / ❌ (still a gap) status per rung. End with a summary
line: "X of Y rungs have notes; created N this run; remaining gaps: [...]."

### Section: "Concrete Example — one trace through every layer"
Trace a single concrete scenario (the arc's canonical example) from the bottom anchor
all the way to the top anchor, annotating each step with the rung it exercises. ASCII
diagram of the end-to-end path.

### Section: "Peripheral Knowledge"
Adjacent notes not on the main ladder; explain each connection.

### Section: "Test Your Understanding"
5 questions (Q1–Q5, foundational → synthesis) testing whether the reader can explain
the climb and how rungs connect. Each answer in a nested `<details>`.

---

## Phase 6: Back-link, verify, finish

1. **Back-link:** add a link to the spine in the **Peripheral Knowledge** (or Related)
   section of every existing note the spine references — it's a hub document.
2. **Verify every link/path resolves** (`ls` it) before finalizing. Canonical wiki-
   link form `[[learning/notes/<tier>/<slug>]]`; code cited by real relative path.
3. Run **`/ascii-fixer`** on the spine and every new note.
4. Run **`/fact-check`** on every NEW note (the PostToolUse hook will remind you).
5. Do NOT edit or move any `--code` reference files — read-only.

---

## Quality Checklist

- [ ] Phase-1 ladder skeleton was shown to the user before building
- [ ] Every rung that can have a note has ≥1 intuition anchor; executable anchors cited where they exist
- [ ] Every gap was either filled (🆕) or explicitly listed as remaining (❌)
- [ ] The spine reads top-to-bottom as ONE continuous story (bridges present)
- [ ] The "Whole Ladder at a Glance" status counts are accurate
- [ ] All wiki-links and code paths resolve; new notes pass `/fact-check`; ASCII passes `/ascii-fixer`
- [ ] Back-links added to referenced existing notes
- [ ] A reader following the spine in order can explain the topic from bottom anchor to top anchor

---

## Usage Examples

```
/index-spine I get that a switch makes a 1 or 0, and a flip-flop stores a bit, and
  registers are flip-flops in a row... but I lose the thread from there up to how a
  CPU runs code and a keypress becomes a letter on screen.
  --seed learning/notes/quick-context/switches-to-registers-storing-data.md
  --code learning/references/courses/python-nand-to-tetris-part-1

/index-spine learning/notes/quick-context/polymer-chemical-bonds.md

/index-spine "how a 3D printer turns a model into a physical part"
```
