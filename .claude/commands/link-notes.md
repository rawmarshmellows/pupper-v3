---
name: link-notes
description: Analyze markdown files and create Obsidian wiki links (related docs + inline term linking)
---

Analyze all markdown files in the following folders and propose links between them: **$ARGUMENTS**

If no folders specified, scan both: `micro-context` and `quick-context`

## Two Types of Linking

### Type 1: Related Documents Header

Add/update the `> **Related:**` line after YAML frontmatter linking to topically related files.

```markdown
> **Related:** [[quick-context/file-one]] | [[quick-context/file-two]]
```

### Type 2: Inline Term Linking

Find terms/concepts in the document body that match other document topics, and convert them to inline wiki links.

**Before:**
```markdown
The tensile strength of PLA depends on layer adhesion and hotend temperature.
```

**After:**
```markdown
The [[quick-context/tensile-strength-materials|tensile strength]] of PLA depends on [[quick-context/3d-printing-filament-types|layer adhesion]] and [[quick-context/3d-printer-hotends|hotend]] temperature.
```

## Instructions

1. **Read all `.md` files** in `micro-context` and `quick-context` folders
2. **Build a term map** from each file's:
   - Frontmatter `topic` field
   - Main heading (H1)
   - Key terms defined in the document (from "words to know" sections, bolded terms, etc.)
3. **Create a proposal** listing all proposed links (do NOT modify files yet):
   - Group by target file
   - Show proposed `> **Related:**` links for each file
   - Show proposed inline term links with context (the sentence where they'd appear)
4. **Wait for user approval** before making any changes

## Rules

- **Related header**: 1-5 genuinely related links, bidirectional when appropriate
- **Inline links**:
  - Only link first occurrence of each term per file (don't over-link)
  - Don't link terms inside headings, code blocks, or existing links
  - Don't link a file to itself
  - Use the original word's casing in the display text: `[[path|Tensile Strength]]` not `[[path|tensile strength]]`
  - Be conservative - only link clear matches, not vague associations
- Preserve all other formatting exactly

## Output

Present the proposal in this format:

### Proposed Links

For each file that would be modified:

```
📄 quick-context/example-file.md
  Related docs to add:
    - [[micro-context/related-topic]]
    - [[quick-context/another-topic]]

  Inline terms to link:
    - "tensile strength" → [[micro-context/tensile-strength|tensile strength]]
      Context: "The tensile strength of the material..."
    - "servo motor" → [[quick-context/servo-motors|servo motor]]
      Context: "...controlled by a servo motor that..."
```

After presenting the full proposal, ask: "Apply these changes? (all / select specific files / none)"
