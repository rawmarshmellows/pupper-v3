---
name: update-small-context
description: Update an existing small-context file, optionally adding human notes
---

Update the small-context file at **$ARGUMENTS**.

## Argument Format

The argument can be:
1. **Path only:** `learning/notes/small-context/use-case-name.md` — refreshes the file
2. **Path + notes:** `learning/notes/small-context/use-case-name.md "my notes to add"` — adds/updates Human notes section

## Instructions

1. **Read the existing file** at the specified path

2. **If human notes are provided:**
   - Add or update a `## Human notes` section **immediately after the `# Case: Title` heading** (before the component links)
   - Place the user's notes there verbatim
   - Scan the notes for concepts that match existing files in `learning/notes/quick-context/` or `learning/notes/micro-context/`
   - Add inline Obsidian links `[[folder/filename|display text]]` where concepts naturally appear
   - Don't force links—only add them where they genuinely help understanding

3. **Check Obsidian vault for additional material:**
   - Search `brain/obsidian/` for files matching the use case and its components: `brain/obsidian/*topic*.md` (try Title Case, lowercase, abbreviations, synonyms)
   - Also check subdirectories: `brain/obsidian/**/*topic*.md`
   - If matching files exist, read them and incorporate any unique content, examples, or explanations that are missing from the current small-context

4. **Refresh the content:**
   - Verify the step-by-step walkthrough is still accurate
   - Check if diagrams accurately represent each step
   - Update component links if related files now exist
   - Ensure the "Go Deeper" section has current links

4. **Preserve the small-context format:**
   - Keep it 80-150 lines
   - Maintain: The Situation, The Pieces, Step by Step, The Result, Why Each Piece Matters, Go Deeper
   - Keep focus on ONE use case
   - **Math notation:** Use LaTeX for all mathematical expressions (`$V = IR$` for inline, `$$P = IV$$` for display)

5. **Update frontmatter:** Add `updated: YYYY-MM-DD` field

## Output Structure

```markdown
---
case: Descriptive Case Name
components: [component-1, component-2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Case: [Descriptive Name]

## Human notes

[User's notes here, with inline links to related concepts]

> **Components:** [[learning/notes/quick-context/component-1]] | [[learning/notes/quick-context/component-2]]
> **Micro-context:** [[learning/notes/micro-context/related-term]] | ...

> **In brief:** [Summary...]

## The Situation
[...]

## The Pieces
[...]

## Step by Step: What Happens
[...]

## The Result
[...]

## Why Each Piece Matters
[...]

## Go Deeper
[...]
```

## Linking Human Notes

When processing the user's notes:

1. **Search for related files:**
   - `learning/notes/quick-context/*.md` for full treatments of components
   - `learning/notes/micro-context/*.md` for quick definitions of terms

2. **Add inline links where concepts appear:**
   - Example: User writes "I didn't realize the capacitor smooths the ripple"
   - Becomes: "I didn't realize the [[learning/notes/quick-context/capacitor|capacitor]] smooths the ripple"

3. **Don't over-link:**
   - One link per concept is enough
   - Only link if the target file actually helps understanding
   - Prefer inline links over listing them separately

---

## Post-Processing (REQUIRED)

After updating the small-context file, you MUST:

1. **Fact-check:** Run `/fact-check <output-file-path>` to verify all factual claims
2. **ASCII-fixer:** Run `/ascii-fixer <output-file-path>` to fix any diagram alignment issues
3. **Update embeddings (manual):** Remind the user to run `python tools/embed.py sync` to update the embedding cache for semantic linking

## If File Doesn't Exist

Inform the user and suggest using `/small-context [use case]` to create a new one instead.
