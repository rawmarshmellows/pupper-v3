---
name: obsidian-links
description: Generate Obsidian wiki links for all markdown files in specified folders
---

Generate Obsidian-style wiki links for all `.md` files in the following folders: **$ARGUMENTS**

## Instructions

1. For each folder specified, find all markdown files recursively
2. Output them as Obsidian wiki links in this format: `[[folder/filename|display-name]]`
   - Remove the `.md` extension from the link path
   - Use the filename (without extension) as the display name
3. Group the links by folder with a heading for each
4. Sort files alphabetically within each folder

## Output Format

```markdown
## folder-name

- [[folder-name/file-one|file-one]]
- [[folder-name/file-two|file-two]]
- [[folder-name/subfolder/file-three|file-three]]
```

If no folders are specified, default to: `learning/notes/quick-context`

Output the links directly to the chat so I can copy them. Do not create a file unless I ask.
