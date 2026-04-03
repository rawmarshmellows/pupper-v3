---
name: update-micro-context
description: Update an existing micro-context file, optionally adding human notes
---

Update the micro-context file at **$ARGUMENTS**.

## Argument Format

The argument can be:
1. **Path only:** `learning/notes/micro-context/term-name.md` — refreshes the file
2. **Path + notes:** `learning/notes/micro-context/term-name.md "my notes to add"` — adds/updates Human notes section

## Instructions

1. **Read the existing file** at the specified path

2. **If human notes are provided:**
   - Add or update a `## Human notes` section **immediately after the `# Title` heading**
   - Place the user's notes there verbatim
   - Scan the notes for concepts that match existing files in `learning/notes/quick-context/` or `learning/notes/micro-context/`
   - Add inline Obsidian links `[[folder/filename|display text]]` where concepts naturally appear
   - Don't force links—only add them where they genuinely help understanding

3. **Check Obsidian vault for additional material:**
   - Search `brain/obsidian/` for files matching the term: `brain/obsidian/*term*.md` (try Title Case, lowercase, abbreviations, synonyms)
   - Also check subdirectories: `brain/obsidian/**/*term*.md`
   - If a matching file exists, read it and incorporate any unique content or explanations that are missing from the current micro-context

4. **Refresh the content:**
   - Verify the definition is still accurate
   - Check if the diagram accurately represents the concept
   - Update links if related files now exist

4. **Preserve the micro-context format:**
   - Keep it ~15-20 lines (excluding diagram and Human notes)
   - One diagram only
   - No additional sections beyond: Definition, How It Works, diagram, Key insight, and Human notes
   - **Math notation:** Use LaTeX for all mathematical expressions (`$V = IR$` for inline, `$$P = IV$$` for display)

5. **Update frontmatter:** Add `updated: YYYY-MM-DD` field

## Output Structure

```markdown
---
term: Term Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Term Name

## Human notes

[User's notes here, with inline links to related concepts]

> **See also:** [[learning/notes/quick-context/related-topic]]

**Definition:** [1-2 sentences]

## How It Works

- [2-4 concise bullet points explaining the mechanism/process]

```
[ASCII diagram]
```

**Key insight:** [One sentence]
```

## Linking Human Notes

When processing the user's notes:

1. **Search for related files:**
   - `learning/notes/quick-context/*.md` for full treatments
   - `learning/notes/micro-context/*.md` for quick definitions

2. **Add inline links where concepts appear:**
   - Example: User writes "this relates to how transistors switch"
   - Becomes: "this relates to how [[learning/notes/quick-context/transistor|transistors]] switch"

3. **Don't over-link:**
   - One link per concept is enough
   - Only link if the target file actually helps understanding
   - Prefer inline links over listing them separately

## If File Doesn't Exist

Inform the user and suggest using `/micro-context [topic]` to create a new one instead.
