---
name: update-quick-context
description: Update an existing quick-context file, optionally adding human notes
---

Update the quick-context file at **$ARGUMENTS**.

## Argument Format

The argument can be:
1. **Path only:** `learning/notes/quick-context/topic-name.md` — refreshes the file
2. **Path + notes:** `learning/notes/quick-context/topic-name.md "my notes to add"` — adds/updates Human notes section

## Instructions

1. **Read the existing file** at the specified path (e.g., `learning/notes/quick-context/3d-printer-hotends.md`)

2. **If human notes are provided:**
   - Add or update a `## Human notes` section **immediately after the `# Title` heading** (before "The Core Problem")
   - Place the user's notes there verbatim
   - Scan the notes for concepts that match existing files in `learning/notes/quick-context/` or `learning/notes/micro-context/`
   - Add inline Obsidian links `[[folder/filename|display text]]` where concepts naturally appear
   - Don't force links—only add them where they genuinely help understanding

3. **Analyze the current content** to understand:
   - The topic being covered
   - The existing structure and sections
   - Any related document links
   - The current depth and focus areas

4. **Check Obsidian vault for additional material:**
   - Search `brain/obsidian/` for files matching the topic: `brain/obsidian/*topic*.md` (try Title Case, lowercase, abbreviations, synonyms)
   - Also check subdirectories: `brain/obsidian/**/*topic*.md`
   - If a matching file exists, read it and incorporate any unique content, examples, or explanations that are missing from the current context file

5. **Research and refresh** the content:
   - Use web search if needed to find current/updated information
   - Look for new developments, corrections, or additional context
   - Check if any technical details need updating

5. **Update the file** while preserving:
   - The YAML frontmatter (update `created` to today's date, or add an `updated` field)
   - The overall structure (core problem, key tension, 5 terms, concrete example, "outsiders get wrong")
   - Any existing related document links (add new ones if relevant)
   - The dense, practical style
   - **Human notes section** (if present—never remove user's notes)

6. **Improvements to consider:**
   - Add more concrete examples if the original is light on them
   - Expand the 5 essential terms if some were too brief
   - Update code examples to current best practices
   - Add links to related quick-context files that now exist — but only if the link helps understanding (ask: "would reading THAT document help someone understand THIS concept?"). Prefer inline links where concepts naturally appear over listing links in headers
   - **Revise test questions** to follow a simple → complex progression:
     - Q1-Q2: Foundational (answers directly in document)
     - Q3-Q4: Applied understanding (connecting ideas, "why" questions, misconception challenges)
     - Q5: Synthesis (connecting to other concepts, novel scenarios, reasoning beyond the text)
     - Avoid calculation-heavy questions — test mental models, not formula application
   - **Verify ASCII diagrams:** After creating or modifying any ASCII diagram, carefully review it to ensure:
     - Lines connect properly and don't have gaps or misalignments
     - Waveforms (sine waves, square waves, etc.) show the correct shape above AND below the baseline where applicable
     - Labels align with what they're pointing to
     - Flow arrows point in the correct direction
     - The diagram accurately represents the concept being explained
   - **Math notation:** Use LaTeX for all mathematical expressions:
     - Inline math: `$V = IR$` renders as $V = IR$
     - Display math: `$$P = IV$$` renders on its own line
     - Use LaTeX for variables, equations, units with exponents, and formulas

## Output

Overwrite the existing file with the updated content. Add an `updated: YYYY-MM-DD` field to the frontmatter to track when it was refreshed.

If the file doesn't exist or the path is invalid, inform the user and suggest using `/quick-context [topic]` to create a new one instead.

## Linking Human Notes

When processing the user's notes:

1. **Search for related files:**
   - `learning/notes/quick-context/*.md` for full treatments
   - `learning/notes/micro-context/*.md` for quick definitions

2. **Add inline links where concepts appear:**
   - Example: User writes "I found this helpful for understanding capacitor behavior"
   - Becomes: "I found this helpful for understanding [[learning/notes/quick-context/capacitor|capacitor]] behavior"

3. **Don't over-link:**
   - One link per concept is enough
   - Only link if the target file actually helps understanding
   - Prefer inline links over listing them separately

## Output Structure with Human Notes

```markdown
---
topic: Topic Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

> **Related:** [[learning/notes/quick-context/related-topic]] | ...

> **TL;DR:** [Summary...]

# Topic Name

## Human notes

[User's notes here, with inline links to related concepts]

## The Core Problem: [...]

[Rest of document...]
```

---

## Post-Processing (REQUIRED)

After updating the quick-context file, you MUST:

1. **Fact-check:** Run `/fact-check <output-file-path>` to verify all factual claims
2. **ASCII-fixer:** Run `/ascii-fixer <output-file-path>` to fix any diagram alignment issues
3. **Update embeddings (manual):** Remind the user to run `python tools/embed.py sync` to update the embedding cache for semantic linking
