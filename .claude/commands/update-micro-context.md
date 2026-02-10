---
name: update-micro-context
description: Update an existing micro-context file, optionally adding human notes
---

Update the micro-context file at **$ARGUMENTS**.

## Argument Format

The argument can be:
1. **Path only:** `micro-context/term-name.md` — refreshes the file
2. **Path + notes:** `micro-context/term-name.md "my notes to add"` — adds/updates Human notes section

## Instructions

1. **Read the existing file** at the specified path

2. **If human notes are provided:**
   - Add or update a `## Human notes` section **immediately after the `# Title` heading**
   - Place the user's notes there verbatim
   - Scan the notes for concepts that match existing files in `quick-context/` or `micro-context/`
   - Add inline Obsidian links `[[folder/filename|display text]]` where concepts naturally appear
   - Don't force links—only add them where they genuinely help understanding

3. **Refresh the content:**
   - Verify the definition is still accurate
   - Check if the diagram accurately represents the concept
   - Update links if related files now exist

4. **Preserve the micro-context format:**
   - Keep it ~15-20 lines (excluding diagram and Human notes)
   - One diagram only
   - No additional sections beyond: Definition, diagram, Key insight, and Human notes

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

> **See also:** [[quick-context/related-topic]]

**Definition:** [1-2 sentences]

```
[ASCII diagram]
```

**Key insight:** [One sentence]
```

## Linking Human Notes

When processing the user's notes:

1. **Search for related files:**
   - `quick-context/*.md` for full treatments
   - `micro-context/*.md` for quick definitions

2. **Add inline links where concepts appear:**
   - Example: User writes "this relates to how transistors switch"
   - Becomes: "this relates to how [[quick-context/transistor|transistors]] switch"

3. **Don't over-link:**
   - One link per concept is enough
   - Only link if the target file actually helps understanding
   - Prefer inline links over listing them separately

## If File Doesn't Exist

Inform the user and suggest using `/micro-context [topic]` to create a new one instead.
