---
name: link-notes-auto
description: Automatically add Obsidian wiki links to markdown files, apply changes without confirmation, and open a PR
---

Analyze all markdown files in `learning/notes/micro-context` and `learning/notes/quick-context` folders, add Obsidian wiki links, apply changes directly, then open a PR.

## Two Types of Linking

### Type 1: Related Documents Header

Add/update the `> **Related:**` line after YAML frontmatter linking to topically related files.

```markdown
> **Related:** [[learning/notes/quick-context/file-one]] | [[learning/notes/quick-context/file-two]]
```

### Type 2: Inline Term Linking

Find terms/concepts in the document body that match other document topics, and convert them to inline wiki links.

**Before:**
```markdown
The tensile strength of PLA depends on layer adhesion and hotend temperature.
```

**After:**
```markdown
The [[learning/notes/quick-context/tensile-strength-materials|tensile strength]] of PLA depends on [[learning/notes/quick-context/3d-printing-filament-types|layer adhesion]] and [[learning/notes/quick-context/3d-printer-hotends|hotend]] temperature.
```

## Instructions

### Semantic search path (preferred)

If `learning/.embeddings/embeddings.db` exists:

1. Run `python tools/link_semantic.py propose` to get semantic link proposals (JSON)
2. Parse the JSON output — each file entry has `related` (docs by TLDR similarity) and `inline_links` (terms by embedding match)
3. **Apply all link changes directly** to each file (do NOT wait for approval):
   - Add/update `> **Related:**` headers from `related` array (top 5)
   - Add inline wiki links from `inline_links` array (first occurrence only)
4. **If any files were modified**, create a new branch named `auto/link-notes-YYYY-MM-DD` and open a pull request with:
   - Title: "Auto link-notes: update Obsidian wiki links"
   - Body listing which files were modified and a summary of links added
5. **If no files needed changes**, do nothing

### Fallback path (no embeddings)

If the embeddings database does not exist, fall back to string matching:

1. **Read all `.md` files** in `learning/notes/micro-context` and `learning/notes/quick-context` folders
2. **Build a term map** from each file's:
   - Frontmatter `topic` field
   - Main heading (H1)
   - Key terms defined in the document (from "words to know" sections, bolded terms, etc.)
3. **Apply all link changes directly** to each file (do NOT wait for approval)
4. **If any files were modified**, create a new branch named `auto/link-notes-YYYY-MM-DD` and open a pull request with:
   - Title: "Auto link-notes: update Obsidian wiki links"
   - Body listing which files were modified and a summary of links added
5. **If no files needed changes**, do nothing

## Rules

- **Related header**: 1-5 genuinely related links, bidirectional when appropriate
- **Inline links**:
  - Only link first occurrence of each term per file (don't over-link)
  - Don't link terms inside headings, code blocks, or existing links
  - Don't link a file to itself
  - Use the original word's casing in the display text: `[[path|Tensile Strength]]` not `[[path|tensile strength]]`
  - Be conservative - only link clear matches, not vague associations
- Preserve all other formatting exactly

## Post-Linking: Dangling Reference Check

After all link changes are applied, run a **dangling reference scan** before opening the PR:

1. **Extract all wiki link targets** from every `.md` file in `learning/notes/micro-context/` and `learning/notes/quick-context/` — parse `[[path/file|...]]` and `[[path/file]]` patterns
2. **Check each target exists** — verify the referenced `.md` file is present on disk (strip display text, check `path/file.md` exists)
3. **Report any dangling references** — links pointing to files that don't exist. For each:
   - File containing the broken link
   - The broken link target
   - Suggested fix: closest matching filename (fuzzy match), or remove the link
4. **Fix all dangling references** before committing — either update the link target to the correct file, or remove the link if no match exists
5. Include the dangling reference fix count in the PR body
