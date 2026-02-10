---
name: quick-context
description: Fast 2-3 paragraph primer to orient on a topic quickly
---

Give me a fast orientation on **$ARGUMENTS**.

## Progressive Disclosure Structure

All quick-context files follow a **4-level progressive disclosure** format. Readers can stop at any level and have a complete (if shallow) understanding. Each level adds depth.

```
LEVEL 1: TL;DR (5 seconds)
    ↓
LEVEL 2: Core Concepts (2 minutes)
    ↓
LEVEL 3: Deep Dive (10 minutes)
    ↓
LEVEL 4: Reference (as needed)
```

---

## Document Template

### LEVEL 1: TL;DR (Always Visible)

```markdown
# Topic Name

> **Related:** [[quick-context/parent-topic]] | [[quick-context/sibling-topic]]

> **TL;DR:** [1-2 sentence summary that captures the essence. Someone should be able to read ONLY this and understand what the topic is about at a cocktail-party level.]
```

### LEVEL 2: Core Concepts (Always Visible)

**The Core Problem** — What breaks if this doesn't exist? Why does anyone care? (2-3 sentences max)

**5 Essential Terms** — Table format, always visible:

```markdown
| Term | Definition |
|------|------------|
| **Term 1** | One-sentence definition |
| **Term 2** | One-sentence definition |
| ... | ... |
```

### LEVEL 3: Deep Dive (Collapsible Sections)

Each deep-dive section is wrapped in `<details>` for progressive disclosure:

```markdown
<details>
<summary><strong>How It Works</strong> — The essential mechanism</summary>

[Walk through the core concept step-by-step in plain language. Use ASCII diagrams to visualize key relationships, flow, or structure. This gives someone a mental model they can reason with.]

**ASCII Diagram Verification:** After creating any ASCII diagram, carefully review it to ensure:
- Lines connect properly and don't have gaps or misalignments
- Waveforms (sine waves, square waves, etc.) show the correct shape above AND below the baseline where applicable
- Labels align with what they're pointing to
- Flow arrows point in the correct direction
- The diagram accurately represents the concept being explained

</details>

<details>
<summary><strong>The Key Tension</strong> — What practitioners argue about</summary>

[The core tradeoff at the heart of the field. What do practitioners optimize between? Include a comparison table if applicable.]

</details>

<details>
<summary><strong>Concrete Example</strong> — What this looks like in practice</summary>

[Show tangible examples:
- Code snippets (with syntax highlighting and comments)
- Real-world configurations, message formats, or data structures
- Specific scenarios walked through step-by-step
- Before/after comparisons

If there's code, show actual runnable or realistic code, not pseudocode.]

**The one thing most outsiders get wrong about this is...** [misconception and correction]

</details>
```

### LEVEL 4: Reference (Collapsible)

```markdown
<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[quick-context/related-topic-1]]** — How it connects to this topic
- **[[quick-context/related-topic-2]]** — How it connects to this topic
- **Topic without file yet** — How it connects to this topic

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** [Foundational - answer directly in document]
<details>
<summary>Answer</summary>
[Answer with reference: "See: The Key Tension"]
</details>

**Q2:** [Foundational - answer directly in document]
<details>
<summary>Answer</summary>
[Answer]
</details>

**Q3:** [Applied - requires connecting ideas within document]
<details>
<summary>Answer</summary>
[Answer]
</details>

**Q4:** [Applied - "Why can't you do X?" or "What's wrong with this claim?"]
<details>
<summary>Answer</summary>
[Answer]
</details>

**Q5:** [Synthesis - requires reasoning beyond the text or connecting to other concepts]
<details>
<summary>Answer</summary>
[Answer]
</details>

</details>
```

---

## Complete Example Structure

```markdown
---
topic: Example Topic
created: 2026-01-26
---

# Example Topic

> **Related:** [[quick-context/parent]] | [[quick-context/sibling]]

> **TL;DR:** Example topic is X that does Y, solving the problem of Z.

## The Core Problem

[2-3 sentences on why this matters]

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Term 1** | Definition |
| **Term 2** | Definition |
| **Term 3** | Definition |
| **Term 4** | Definition |
| **Term 5** | Definition |

<details>
<summary><strong>How It Works</strong></summary>

[Detailed explanation with ASCII diagrams]

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

[Tradeoffs and debates]

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

[Tangible example with code/diagrams]

**The one thing most outsiders get wrong about this is...** [misconception]

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/related-1]]** — Connection explanation
- **[[quick-context/related-2]]** — Connection explanation

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

[5 questions with nested <details> for answers]

</details>
```

---

## Output

Save the response to a markdown file in the `quick-context/` folder. Use a kebab-case filename based on the topic (e.g., `quick-context/industrial-plcs.md`). Create the folder if it doesn't exist. The file should include a YAML frontmatter with:
- `topic`: The topic name
- `created`: Today's date in YYYY-MM-DD format

---

## REQUIRED: Search and Link Existing Quick-Context Files

**Before writing the new document**, you MUST:

1. **Search all existing quick-context files** using `Glob` with pattern `quick-context/*.md`

2. **Read all existing files** to identify related topics. When reading files with progressive disclosure structure:
   - **TL;DR and Core sections** (always visible) give you the topic summary and key terms
   - **Collapsible sections** (`<details>`) contain deeper content — read these to find:
     - Related concepts mentioned in "How It Works"
     - Tradeoffs and comparisons in "The Key Tension"
     - Concrete examples that might reference your new topic
     - Existing links in "Peripheral Knowledge"

   **Structure-aware search pattern:**
   ```
   - YAML frontmatter → topic name
   - TL;DR line → one-sentence summary
   - 5 Essential Terms table → key vocabulary to cross-link
   - <details> sections → deeper content for contextual linking
   - Peripheral Knowledge → existing link graph
   ```

3. **Build a link map** of:
   - Which existing files should be linked FROM the new document (as Related or inline links)
   - Which existing files should be linked TO the new document (back-links to add)
   - Which terms from the new topic appear in existing files' 5 Essential Terms tables (high-value link targets)

4. **Create links in the new document**:
   - Add a `> **Related:**` header with links to the most closely related existing documents (2-5 max)
   - **Every link must have a clear reason** — don't list topics just because they're tangentially related. Ask: "Would a reader of THIS document want to follow this link?"
   - **Prefer inline links** `[[quick-context/filename|display text]]` within prose where concepts naturally appear, rather than listing links at the top without context
   - Prioritize linking terms that appear in the 5 Essential Terms tables of existing files

5. **Add back-links to existing documents**:
   - For each existing file that relates to the new topic, find where the new concept is mentioned (or should be mentioned) in the prose
   - Add inline wiki links pointing back to the new document
   - **Best places to add back-links in progressive disclosure files:**
     - The "5 Essential Terms" table (if the new topic IS a term)
     - Inside `<details>` sections where the concept is discussed
     - The "Peripheral Knowledge" section (add as a new related topic)
   - Focus on natural, contextual linking within body text, not just headers

**Example workflow:**
```
1. Glob: quick-context/*.md → finds 15 existing files
2. Read all 15 files:
   - transistor.md: TL;DR mentions "switching", Terms table has "Gate, Source, Drain"
   - silicon-die.md: "How It Works" section mentions MOSFETs
   - doped-silicon.md: Peripheral Knowledge links to transistor
3. New topic "MOSFET" relates to: transistor (parent), doped-silicon (prerequisite)
4. In new MOSFET file:
   - Related header: [[quick-context/transistor]] | [[quick-context/doped-silicon]]
   - Inline: "...the [[quick-context/doped-silicon|doped silicon]] regions form..."
5. Back-link updates:
   - transistor.md: Add "MOSFET" to Terms table → [[quick-context/mosfet|MOSFET]]
   - silicon-die.md: In <details> How It Works, link "MOSFET" → [[quick-context/mosfet|MOSFET]]
   - doped-silicon.md: Add to Peripheral Knowledge section
```

This ensures every new quick-context file is woven into the existing knowledge graph.

---

**Inline Links:** Throughout the document, link key terms to existing quick-context files using `[[quick-context/filename|display text]]` format. This creates a connected knowledge graph. Prioritize linking:
- Terms in the 5 essential vocabulary
- Related concepts mentioned in the text

**Link quality over quantity:** Only include links where they help understanding. Every link in "Related" or inline should have a clear reason—ask "would reading THAT document help someone understand THIS concept?" If not, don't link it.

**Back-linking:** After creating the new file, update any existing quick-context files that were linked to in the new document. Add **inline** reciprocal links where the new topic is mentioned in the body text. When working with progressive disclosure files:
- **Visible sections** (TL;DR, Core Problem, Terms table): High-visibility links
- **Collapsible sections** (`<details>`): Contextual links within deeper content
- **Peripheral Knowledge section**: Add to the related topics list

The goal is contextual linking where concepts naturally appear throughout all disclosure levels.
