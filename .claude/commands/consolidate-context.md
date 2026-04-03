---
name: consolidate-context
description: Scan all context files and propose articles to consolidate (merge overlapping learning/notes/micro-context/quick-context entries)
---

Scan all context files and propose consolidation opportunities.

## What This Does

This skill analyzes the full set of `learning/notes/micro-context/` and `learning/notes/quick-context/` files to find:

1. **Overlapping micro-contexts** — Two or more micro-context files covering nearly the same concept (e.g., `voltage-divider.md` and `resistive-divider.md`)
2. **Micro-context clusters ready for promotion** — A cluster of 3+ closely related micro-contexts that would be better served by a single quick-context file
3. **Overlapping quick-contexts** — Two quick-context files with significant content overlap that should be merged
4. **Micro-contexts absorbed by quick-contexts** — A micro-context whose content is fully covered by an existing quick-context (the micro-context adds no unique value)

---

## Step 1: Inventory All Files

1. **Glob** `learning/notes/micro-context/*.md` and `learning/notes/quick-context/*.md`
2. **Read every file** — at minimum the frontmatter, definition/TL;DR, and key terms
3. Build a list of `(filename, type, core-concept, key-terms[])` for each file

---

## Step 2: Detect Consolidation Candidates

For each pair/group of files, check:

### A. Near-Duplicates (same concept, different names)
- Do two files define essentially the same thing?
- Would a reader be confused about which file to read?
- **Signal:** >80% term overlap in definitions, or one is just a synonym/alias of the other

### B. Promotable Clusters (micro-contexts → quick-context)
- Are there 3+ micro-contexts that all relate to the same parent concept?
- Would a single quick-context with an "Essential Terms" table replace them all while adding structure?
- **Signal:** A group of micro-contexts that would all logically appear in one quick-context's "5 Essential Terms" table

### C. Overlapping Quick-Contexts
- Do two quick-context files cover substantially the same ground?
- Could one be absorbed into the other, or should they be restructured with clearer boundaries?
- **Signal:** >3 shared terms in their "5 Essential Terms" tables, or the "How It Works" sections describe the same mechanism

### D. Absorbed Micro-Contexts
- Does a quick-context file already cover everything a micro-context says (and more)?
- Would deleting the micro-context lose any unique information?
- **Signal:** The micro-context's definition is a strict subset of the quick-context's TL;DR + Core Problem

---

## Step 3: Present Proposals

Output a markdown report with this structure:

```markdown
# Context Consolidation Report

**Scanned:** X micro-context files, Y quick-context files
**Proposals:** N consolidation opportunities found

---

## Near-Duplicates

### Proposal 1: Merge `learning/notes/micro-context/a.md` + `learning/notes/micro-context/b.md`
- **Why:** Both define [concept]. File A focuses on [X], File B on [Y], but 90% of content overlaps.
- **Action:** Keep `a.md`, merge unique content from `b.md`, delete `b.md`, update all links.

---

## Promotable Clusters

### Proposal 2: Promote cluster → `learning/notes/quick-context/new-topic.md`
- **Files:** `learning/notes/micro-context/x.md`, `learning/notes/micro-context/y.md`, `learning/notes/micro-context/z.md`
- **Why:** These three micro-contexts all describe aspects of [parent concept]. A single quick-context would give better structure and context.
- **Action:** Create `learning/notes/quick-context/new-topic.md` incorporating all three as Essential Terms. Keep micro-contexts as glossary stubs pointing to the quick-context.

---

## Overlapping Quick-Contexts

### Proposal 3: Restructure `learning/notes/quick-context/a.md` and `learning/notes/quick-context/b.md`
- **Why:** Both files explain [mechanism]. File A approaches from [angle], File B from [angle].
- **Action:** [Merge into one / Split along clearer boundary / Keep both but deduplicate shared sections]

---

## Absorbed Micro-Contexts

### Proposal 4: Retire `learning/notes/micro-context/a.md`
- **Why:** `learning/notes/quick-context/b.md` fully covers this concept in its [section]. The micro-context adds no unique information.
- **Action:** Delete `learning/notes/micro-context/a.md`, redirect any incoming links to `learning/notes/quick-context/b.md`.

---

## No Action Needed

[List any files that were close calls but don't warrant consolidation, with a brief reason why they should stay separate.]
```

---

## Step 4: Wait for User Approval

After presenting the report, **do not take any action**. Ask the user which proposals (if any) they want to execute. Only proceed with explicit approval.

When the user approves a proposal:
1. Perform the merge/promotion/deletion
2. Update all wiki links (`[[...]]`) across the entire context corpus that pointed to removed/renamed files
3. Run `/fact-check` and `/ascii-fixer` on any newly created or modified files
4. Run the **Dangling Reference Check** (see below)

---

## Step 5: Dangling Reference Check (REQUIRED after execution)

After executing any consolidation (deletions, renames, merges), run a full dangling reference scan:

1. **Extract all wiki link targets** from every `.md` file in `learning/notes/micro-context/` and `learning/notes/quick-context/` — parse `[[path/file|...]]` and `[[path/file]]` patterns
2. **Check each target exists** — verify the referenced `.md` file is present on disk (strip display text, check `path/file.md` exists)
3. **Report any dangling references** — links pointing to files that don't exist. For each:
   - File containing the broken link
   - The broken link target
   - Suggested fix: closest matching filename (fuzzy match), or remove the link
4. **Fix all dangling references** — either update the link target to the correct file, or remove the link if no match exists
5. **Present a summary** to the user:
   ```
   ## Dangling Reference Check
   - **Total links scanned:** X
   - **Dangling references found:** X
   - **Fixed:** X
   - [list of fixes applied]
   ```

This step catches links broken by file deletions, renames, or typos introduced during consolidation.

---

## Guidelines

- **Conservative by default:** When in doubt, propose "keep separate" rather than "merge." False merges lose nuance; false separations are harmless.
- **Preserve unique perspectives:** If two files cover the same topic but from genuinely different angles (e.g., a physics perspective vs. a circuit design perspective), note this and recommend keeping both.
- **Micro-contexts are cheap:** Don't propose retiring a micro-context just because a quick-context exists on a related topic. Only propose retirement when the micro-context is truly redundant (adds zero unique information).
- **Link, don't merge, when in doubt:** Sometimes the right fix is just better cross-linking, not consolidation.

## Optional: Scope Filter

If `$ARGUMENTS` is provided, only analyze files related to that domain/topic. Otherwise, analyze everything.
