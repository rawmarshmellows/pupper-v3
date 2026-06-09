# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

A personal learning knowledge base + tooling around it. The domain is electronics, electrical engineering, robotics, manufacturing, and applied physics (with the Stanford Pupper quadruped project as one of the reference courses). Two halves:

1. **`learning/`** — markdown notes organized into context tiers, plus reference course material.
2. **`tools/`** — Python embedding pipeline that indexes the notes into a local SQLite database for similarity search and inline link proposals.

There is no top-level build, package manager, or test runner — each subproject has its own.

## Indexing scope

When indexing this repo (e.g. via `mcp__claude-context__index_codebase` or any other indexer), restrict to **markdown (`.md`) and code files** (Python, JS/TS, JSON, YAML, shell, etc.). Explicitly **exclude**:

- Images: `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`, `.heic`
- Spreadsheets / office docs: `.xlsx`, `.xls`, `.csv`, `.docx`, `.pdf`
- CAD / EE artifacts under `learning/references/`: Gerber files, `.step`, `.stl`, `.f3d`, `.dxf`, `.kicad_*`, `.sch`, `.brd`, `.zip`
- Binary / build artifacts: `.DS_Store`, `__pycache__/`, `.mypy_cache/`, `learning/.embeddings/`

The `learning/references/courses/` tree in particular contains large binary course materials that should never be indexed.

## The notes (`learning/notes/`) — tiered structure

Every `.md` file under `learning/notes/<tier>/` follows a templated format defined by the matching slash command in `.claude/commands/`. The Python parser in `tools/note_parser.py` and the embedding pipeline depend on these conventions, so deviating breaks downstream tooling.

| Tier | Length | Question it answers | Template command |
|---|---|---|---|
| `micro-context/` | ~20 lines | "What is X?" (glossary entry + one diagram) | `/micro-context` |
| `quick-context/` | 200–500 lines | "Tell me everything about X" (4-level progressive disclosure) | `/quick-context` |
| `small-context/` | 80–150 lines | "How does X work in this situation?" | `/small-context` |
| `human-context/` | varies | User's own explanation, fact-checked and corrected in place | `/human-context` |

Required fields the parser extracts: YAML frontmatter (`topic`/`term`/`case`, `created`), a `> **TL;DR:**` or `**Definition:**` blockquote, a `5 Essential Terms` table (quick-context), `## Test Your Understanding` Q&A blocks, and `[[learning/notes/<tier>/<slug>]]` wiki-links. Filenames are kebab-case slugs.

After creating a `quick-context`, `micro-context`, or `small-context` note, the PostToolUse hook reminds Claude to run `/fact-check` and `/ascii-fixer` on the output — do this.

## Slash commands

`.claude/commands/` holds the project's authoring workflow. The note-creation commands (`micro-context`, `quick-context`, `small-context`, `human-context`) define the templates the parsers expect — read the relevant command before authoring or editing notes in a tier. Other useful commands: `/link-notes` (propose links interactively), `/link-notes-auto` (apply + open PR), `/consolidate-context` (find overlapping notes), `/coverage-map` (gap analysis for a domain), `/explode-concepts` (spawn parallel quick-contexts from a source doc), `/fact-check`, `/ascii-fixer`.
