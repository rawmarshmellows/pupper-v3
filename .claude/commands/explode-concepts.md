---
name: explode-concepts
description: Extract core concepts from a document and spawn parallel quick-context agents for each
---

Analyze the document at **$ARGUMENTS** and create quick-context explainers for every core concept.

## Phase 1: Document Analysis

1. Read the document at the specified path
2. Identify **all core concepts, terminology, and technical terms** that would benefit from deeper explanation
3. For each concept, note:
   - The term itself
   - Brief context from the source document (how it's used)
   - Whether it's foundational (must understand first) or advanced (builds on other concepts)

## Phase 2: Concept Extraction Output

Present the extracted concepts to the user in a numbered list:

```
Found [N] concepts in [document-name]:

FOUNDATIONAL (explain these first):
1. [concept-1] - [one-line context from document]
2. [concept-2] - [one-line context from document]

INTERMEDIATE:
3. [concept-3] - [one-line context from document]
...

ADVANCED (builds on above):
N. [concept-N] - [one-line context from document]
```

## Phase 3: Parallel Agent Spawning

After presenting the concepts, spawn **parallel subagents** using the Task tool. Each subagent should:

1. Run the `/quick-context` skill for its assigned concept
2. Tailor the explanation assuming **zero background knowledge** in the subject domain
3. Include **diagrams using ASCII art or markdown tables** wherever visual representation would help understanding
4. Add a `> **Related:** [[path/to/source-document]]` link back to the original document

**CRITICAL: Spawn all agents in parallel** by issuing multiple Task tool calls in a single response. Do not wait for one to complete before starting the next.

Example agent prompt for each concept:
```
Run /quick-context for "[concept-name]" with these requirements:
- Assume the reader has ZERO background in [domain inferred from source document]
- Use diagrams (ASCII art, markdown tables, or text-based visuals) wherever possible to illustrate the concept
- At the top of the file, add: > **Related:** [[source-document-path]]
- The context is: this concept appears in [source-document-name] where it's used to describe [context from document]
- Make explanations accessible to complete beginners while remaining technically accurate
```

## Phase 4: Summary

After all agents complete, provide a summary:

```
Created [N] quick-context files:
- [[learning/notes/quick-context/concept-1]] - [status]
- [[learning/notes/quick-context/concept-2]] - [status]
...

These are all linked back to: [[source-document-path]]
```

## Usage Examples

```
/explode-concepts learning/notes/quick-context/polymer-chemical-bonds.md
/explode-concepts lectures/robotics-intro.md
/explode-concepts building/servo-motor-basics.md
```

## Notes

- Use `subagent_type: "general-purpose"` for each Task agent since they need to run skills
- If the document contains more than 10 concepts, ask the user if they want to proceed with all or select a subset
- Preserve any existing quick-context files; don't overwrite unless the user confirms
