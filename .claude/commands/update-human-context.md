---
name: update-human-context
description: Update an existing human-context file — refresh verification, add new claims, or append additional human understanding
---

Update the human-context file at **$ARGUMENTS**.

## Argument Format

The argument can be:
1. **Path only:** `learning/notes/human-context/concept-name.md` — re-verifies all claims, refreshes inline links, regenerates the Quick Reference and Corrections at a Glance sections
2. **Path + new explanation:** `learning/notes/human-context/concept-name.md "additional or revised understanding"` — appends/revises the user's understanding, then re-verifies the whole file

## What This Does

Human-context files are the user's own mental model, verified against authoritative sources. Updates differ from `/human-context` (the create flow) in three ways:

- The blockquoted `> **My understanding:**` original is **sacred** when refreshing — never edit it. New explanations get appended as a second blockquote, not merged into the first.
- Inline correction annotations stay as the audit trail. Don't silently fix old mistakes — keep the `[~~"wrong"~~ — why]` markup so the user can see what was learned.
- The **Quick Reference** and **Corrections at a Glance** sections (see `/human-context` Step 5) are always regenerated from the current verified prose.

## Instructions

1. **Read the existing file** at the specified path

2. **If the file doesn't exist**, inform the user and suggest using `/human-context [explanation]` to create a new one

3. **If a new explanation is provided** (path + quoted string):
   - Append a second blockquote **immediately below the existing `> **My understanding:**` block**, dated:
     ```markdown
     > **Update (YYYY-MM-DD):** [The user's new explanation, verbatim]
     ```
   - Treat its claims the same way `/human-context` Step 2 does (extract claims → check existing context files → check Obsidian vault → web-search anything still unverified)
   - Integrate the corrected version of the new claims into the existing verified prose. Prefer extending the existing prose paragraphs over appending a new section, unless the new explanation covers a clearly separate sub-topic
   - Use the same inline correction markup (`[~~"wrong"~~ — why]`) for any errors in the new explanation

4. **If only a path is given** (refresh mode):
   - Re-extract all claims from the verified prose
   - Re-check each claim against `learning/notes/micro-context/*.md`, `learning/notes/quick-context/*.md`, `brain/obsidian/`, and (only when those don't cover it) the web
   - If any claim is now contradicted by a more authoritative source, **add** a new inline correction annotation. Do not delete or rewrite existing annotations — they are the audit trail
   - Refresh broken or stale Obsidian wiki links (target files may have been renamed or split)

5. **Check Obsidian vault for additional material:**
   - Search `brain/obsidian/` for files matching the concept: `brain/obsidian/*concept*.md` (try Title Case, lowercase, abbreviations, synonyms)
   - Also check subdirectories: `brain/obsidian/**/*concept*.md`
   - If a matching note exists, use it as an extra verification source. Do **not** import its content into the human-context file — this is the user's understanding, not a tutorial

6. **Regenerate the digestible summary** (always, on every update):
   - Replace the entire `## Quick Reference` section with a fresh clean bullet-point version of the current verified prose (corrections silently applied, no annotations, inline links allowed)
   - Replace the entire `## Corrections at a Glance` table — one row per inline correction currently in the prose. If zero corrections remain, swap the table for a single line: `**No corrections needed — verified as written.**`

7. **Update frontmatter:**
   - Add or update an `updated: YYYY-MM-DD` field
   - Keep `created` unchanged
   - Keep `status: verified` unless new contradictions surfaced that you couldn't resolve, in which case set `status: needs-review` and add a one-line note to the Verification footer

8. **Update the Verification footer** at the bottom:
   - Recompute `X claims checked. Y correct, Z corrected.` based on the current state
   - Append any new sources consulted to the source list (don't delete old ones)

## Output Structure

```markdown
---
concept: Concept Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: verified
---

# Concept Name

> **Related:** [[learning/notes/quick-context/...]] | [[learning/notes/micro-context/...]]

> **My understanding:** [Original explanation — sacred, never edited]

> **Update (YYYY-MM-DD):** [Optional second blockquote, only present if a new explanation was added]

---

[Verified prose with inline links and inline correction annotations — extended, not rewritten]

---

## Quick Reference

- [Clean, atomic, corrected fact 1]
- [Clean, atomic, corrected fact 2]
- ...

## Corrections at a Glance

| What I said | What's actually correct | Why |
|---|---|---|
| ... | ... | ... |

---

**Verification:** X claims checked. Y correct, Z corrected. Sources: ...
```

## Guidelines

- **The blockquoted originals are sacred.** Never edit text inside any `> **My understanding:**` or `> **Update (...):**` blockquote.
- **Don't silently fix old mistakes.** If the user got something wrong on day 1 and now understands it, the inline `[~~"wrong"~~ — why]` annotation stays. Their growth is the point of the file.
- **Annotations should teach.** Each correction annotation should help the user understand *why* they were wrong, not just *that* they were wrong.
- **Don't add curriculum.** If the user didn't mention a concept, don't teach it to them here — even on update. The Quick Reference section can only contain points present in the verified prose.
- **Voice preservation is paramount.** Even when extending the prose, write in the user's existing register and use their existing analogies where they're valid.

---

## Post-Processing (REQUIRED)

After updating the human-context file, you MUST:

1. **Fact-check:** Run `/fact-check <output-file-path>` to verify all factual claims
2. **Update embeddings (manual):** Remind the user to run `python tools/embed.py sync` to update the embedding cache for semantic linking

## If File Doesn't Exist

Inform the user and suggest using `/human-context [explanation]` to create a new one instead.
