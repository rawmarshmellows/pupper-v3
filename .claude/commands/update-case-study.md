---
name: update-case-study
description: Update an existing case-study file, optionally adding human notes
---

Update the case-study file at **$ARGUMENTS**.

## Argument Format

The argument can be:
1. **Path only:** `case-study/use-case-name.md` — refreshes the file
2. **Path + notes:** `case-study/use-case-name.md "my notes to add"` — adds/updates Human notes section

## Instructions

1. **Read the existing file** at the specified path

2. **If human notes are provided:**
   - Add or update a `## Human notes` section **immediately after the `# Case: Title` heading** (before the component links)
   - Place the user's notes there verbatim
   - Scan the notes for concepts that match existing files in `quick-context/` or `micro-context/`
   - Add inline Obsidian links `[[folder/filename|display text]]` where concepts naturally appear
   - Don't force links—only add them where they genuinely help understanding

3. **Refresh the content:**
   - Verify the step-by-step walkthrough is still accurate
   - Check if diagrams accurately represent each step
   - Update component links if related files now exist
   - Ensure the "Go Deeper" section has current links

4. **Preserve the case-study format:**
   - Keep it 80-150 lines
   - Maintain: The Situation, The Pieces, Step by Step, The Result, Why Each Piece Matters, Go Deeper
   - Keep focus on ONE use case

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

> **Components:** [[quick-context/component-1]] | [[quick-context/component-2]]
> **Micro-context:** [[micro-context/related-term]] | ...

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
   - `quick-context/*.md` for full treatments of components
   - `micro-context/*.md` for quick definitions of terms

2. **Add inline links where concepts appear:**
   - Example: User writes "I didn't realize the capacitor smooths the ripple"
   - Becomes: "I didn't realize the [[quick-context/capacitor|capacitor]] smooths the ripple"

3. **Don't over-link:**
   - One link per concept is enough
   - Only link if the target file actually helps understanding
   - Prefer inline links over listing them separately

## If File Doesn't Exist

Inform the user and suggest using `/case-study [use case]` to create a new one instead.
