---
name: update-quick-context
description: Update an existing quick-context file with refreshed or expanded information
---

Update the quick-context file at **$ARGUMENTS**.

## Instructions

1. **Read the existing file** at the specified path (e.g., `quick-context/3d-printer-hotends.md`)

2. **Analyze the current content** to understand:
   - The topic being covered
   - The existing structure and sections
   - Any related document links
   - The current depth and focus areas

3. **Research and refresh** the content:
   - Use web search if needed to find current/updated information
   - Look for new developments, corrections, or additional context
   - Check if any technical details need updating

4. **Update the file** while preserving:
   - The YAML frontmatter (update `created` to today's date, or add an `updated` field)
   - The overall structure (core problem, key tension, 5 terms, concrete example, "outsiders get wrong")
   - Any existing related document links (add new ones if relevant)
   - The dense, practical style

5. **Improvements to consider:**
   - Add more concrete examples if the original is light on them
   - Expand the 5 essential terms if some were too brief
   - Update code examples to current best practices
   - Add links to related quick-context files that now exist — but only if the link helps understanding (ask: "would reading THAT document help someone understand THIS concept?"). Prefer inline links where concepts naturally appear over listing links in headers
   - **Revise test questions** to follow a simple → complex progression:
     - Q1-Q2: Foundational (answers directly in document)
     - Q3-Q4: Applied understanding (connecting ideas, "why" questions, misconception challenges)
     - Q5: Synthesis (connecting to other concepts, novel scenarios, reasoning beyond the text)
     - Avoid calculation-heavy questions — test mental models, not formula application

## Output

Overwrite the existing file with the updated content. Add an `updated: YYYY-MM-DD` field to the frontmatter to track when it was refreshed.

If the file doesn't exist or the path is invalid, inform the user and suggest using `/quick-context [topic]` to create a new one instead.
