---
name: coverage-map
description: Generate a navigational index and coverage map for a domain, showing which quick-context files exist and where gaps remain
---

Generate a **coverage map** (navigational index) for the domain: **$ARGUMENTS**

A coverage map is a master document that organizes all sub-topics within a domain into a coherent hierarchy, shows which quick-context files already exist, identifies gaps, and serves as a navigational hub for the knowledge graph. Think of it as a "table of contents + gap analysis" for an entire subject area.

---

## Step 1: Discover Existing Coverage

**Before writing anything**, you MUST:

1. **Glob** `quick-context/*.md` to find all existing quick-context files.
2. **Glob** `micro-context/*.md` to find all existing micro-context files.
3. **Read every file** (at minimum the YAML frontmatter, TL;DR, and 5 Essential Terms table) to understand what's already covered.
4. **Identify which files fall within the domain** of `$ARGUMENTS`. Be inclusive — if a file is even partially relevant, note it.
5. **Build a mental inventory** of:
   - Files that are directly about this domain
   - Files that are adjacent/prerequisite to this domain
   - Obvious sub-topics that have NO file yet (gaps)

---

## Step 2: Design the Hierarchy

Organize the domain into **logical categories** (3–8 categories). Each category groups related sub-topics. The categories should:

- Flow from foundational → advanced (or simple → complex)
- Cover the domain comprehensively — a beginner should be able to look at the categories and understand the shape of the field
- Feel natural to a practitioner, not forced

For each sub-topic within a category, determine:
- ✅ = existing quick-context file covers this
- ❌ = no file exists yet (gap)

---

## Step 3: Write the Coverage Map

### Document Structure

```markdown
---
topic: [Domain Name] — Coverage Map
created: [today's date YYYY-MM-DD]
updated: [today's date YYYY-MM-DD]
---

> **Related:** [[quick-context/related-file-1]] | [[quick-context/related-file-2]]

> **TL;DR:** [1-2 sentences: what this domain is, and what this index helps you do — navigate the sub-topics and find gaps.]

# [Domain Name] — Coverage Map

## The Core Problem: [Why This Domain Needs a Map]

[2-4 sentences explaining why this domain is hard to hold in your head and why a navigational index helps. What span of concepts does it cover? How many distinct sub-topics are there?]

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Term 1** | One-sentence definition |
| **Term 2** | One-sentence definition |
| **Term 3** | One-sentence definition |
| **Term 4** | One-sentence definition |
| **Term 5** | One-sentence definition |
```

### Deep Dive Sections (all in `<details>` tags)

#### Section: "How It Works — The Full [Domain] Map"

For EACH category in your hierarchy, include:

1. **Category heading** (e.g., "## 1. Passive Components — Store or Dissipate Energy")
2. **Brief intro** (1-2 sentences explaining what this category covers)
3. **ASCII diagram** showing key relationships, hierarchy, or flow within the category (use box-drawing characters and clear labels)
4. **Sub-topic table:**

```markdown
| Part/Topic | Existing Quick-Context? | Key Concept |
|------------|------------------------|-------------|
| **[[quick-context/filename\|Display Name]]** | Yes | Brief description of what the file covers |
| **Topic Name** | ❌ No | What this file WOULD cover if created |
```

- For existing files: use `[[quick-context/filename\|Display Name]]` wiki links and note "Yes"
- For gaps: just use the topic name, mark "❌ No", and describe what the file would cover

#### Section: "The Key Tension — Coverage Map"

Include a full ASCII coverage map showing all categories and their sub-topics with ✅/❌ status:

```markdown
COVERAGE MAP
══════════════════════════════════════════════════════════════════════════════

  CATEGORY 1             CATEGORY 2             CATEGORY 3
  ────────────────       ────────────────       ─────────────────────
  ✅ Topic A             ✅ Topic D              ✅ Topic G
  ✅ Topic B             ❌ Topic E              ❌ Topic H
  ❌ Topic C             ✅ Topic F              ✅ Topic I
```

End with a summary line: "X of Y sub-topics have quick-context files. Gaps: [list the missing ones]."

#### Section: "Concrete Example"

Show a concrete scenario that traces through multiple sub-topics in the domain, demonstrating how they connect. Use an ASCII diagram showing a realistic workflow, signal path, process, or decision tree — and annotate each step with the relevant quick-context file.

#### Section: "Peripheral Knowledge"

Link to related quick-context files that are adjacent to but not core to this domain. Explain the connection for each.

#### Section: "Test Your Understanding"

5 questions (Q1-Q5, foundational → synthesis) that test understanding of the domain structure and how sub-topics relate. Each answer in a nested `<details>` tag.

---

## Step 4: Output

Save the coverage map to `quick-context/[domain-kebab-case]-coverage-map.md`.

**Filename examples:**
- Domain "Electronics" → `quick-context/electronics-coverage-map.md`
- Domain "Robotics Software" → `quick-context/robotics-software-coverage-map.md`
- Domain "Industrial Automation" → `quick-context/industrial-automation-coverage-map.md`

---

## Step 5: Back-link

After creating the coverage map:

1. For each existing quick-context file that is listed in the coverage map, add a back-link to the coverage map in that file's **Peripheral Knowledge** section (or Related header if it's highly relevant).
2. Only add back-links where they genuinely help navigation — the coverage map is a hub document, so most files in the domain should link back to it.

---

## Quality Checklist

Before finishing, verify:

- [ ] Every existing quick-context file relevant to the domain is listed
- [ ] Gaps are clearly identified with ❌ markers
- [ ] ASCII diagrams are present for each category AND the full coverage map
- [ ] The hierarchy flows logically (foundational → advanced)
- [ ] Wiki links use correct `[[quick-context/filename|Display Name]]` format
- [ ] The coverage summary accurately counts files vs. gaps
- [ ] Back-links have been added to existing files
