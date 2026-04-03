---
name: mental-model-loop
description: Find cross-domain connections where different fields share the same underlying mental model
---

Analyze the file at **$ARGUMENTS** and identify a mental model that connects it to a seemingly unrelated field.

## What is a Mental Model Loop?

A mental model loop is when the same underlying pattern, principle, or structure appears across completely different domains. Examples:

- **Abstraction layers**: Software stacks (app → OS → hardware) mirror chip design (application → RTL → transistors) mirror organizational hierarchies (strategy → management → execution)
- **Conway's Law**: Software interfaces reflect communication structures in organizations—the way modules talk mirrors how teams talk
- **Impedance matching**: In electronics (source/load impedance), in APIs (data format translation), in management (translating executive vision to engineering tasks)
- **Caching**: CPU caches, CDNs, human memory, inventory warehouses—all solve "expensive fetch, frequent access"
- **Feedback loops**: Control systems, agile retrospectives, thermostat regulation, market price discovery

## Process

### Step 1: Read and Understand the Source File

Read the file provided. Identify:
- The core mechanism or principle it explains
- The key tensions or tradeoffs
- The essential vocabulary

### Step 2: Abstract the Mental Model

Strip away domain-specific details. Ask:
- What is the **underlying pattern**? (e.g., "layered indirection", "feedback control", "resource pooling")
- What **problem shape** does it solve? (e.g., "too expensive to do every time", "too complex to handle at once", "need coordination without direct coupling")
- What are the **structural relationships**? (e.g., "many-to-one", "hierarchical", "bidirectional flow")

### Step 3: Find the Cross-Domain Match

Search existing quick-context and micro-context files for a concept from a **different field** that shares this mental model.

Use Glob to find all existing files:
```
learning/notes/quick-context/*.md
learning/notes/micro-context/*.md
learning/notes/small-context/*.md
```

Look for matches where:
- The problem shape is identical but the domain is different
- The tradeoffs rhyme (e.g., "latency vs throughput" appears in both)
- The vocabulary maps surprisingly well

**Prioritize surprising connections** over obvious ones:
- Software ↔ Biology (good)
- Software ↔ Another software concept (less interesting)
- Hardware ↔ Organizational design (good)
- Two hardware concepts (less interesting)

### Step 4: Propose the Connection (REQUIRES HUMAN APPROVAL)

Present the proposed mental model loop to the user in this format:

```
## Proposed Mental Model Loop

**Source:** [[path/to/source-file]]
**Target:** [[path/to/target-file]]

### The Shared Mental Model

[Name the pattern in 2-4 words, e.g., "Layered Abstraction", "Impedance Matching", "Cached Indirection"]

### Why These Connect

[2-3 sentences explaining the structural similarity. Be specific about what maps to what.]

**Source domain:** [Concept A] → [Concept B] → [Concept C]
**Target domain:** [Concept X] → [Concept Y] → [Concept Z]

### Why This Matters

[1-2 sentences on why recognizing this connection is useful. What can you now reason about by analogy?]

### The Limits of the Analogy

[1-2 sentences on where the mapping breaks down. Every analogy has limits—name them.]
```

**STOP HERE AND ASK FOR APPROVAL.**

Do not create any files until the user confirms:
- The connection makes sense
- They want to proceed with documenting it

## Step 5: After Approval — Create the Mental Model Loop File

Only after user approval, create the file in `learning/notes/mental-model-loop/` folder.

### File Template

```markdown
---
mental-model: [Pattern Name]
source: [[path/to/source]]
target: [[path/to/target]]
created: YYYY-MM-DD
---

# [Pattern Name]: [Source Domain] ↔ [Target Domain]

> **TL;DR:** [One sentence explaining the shared pattern across both domains]

## The Pattern

[2-3 paragraphs explaining the abstract mental model, independent of either domain]

## How It Appears

### In [Source Domain]

[Brief explanation with link to source file. Show how the pattern manifests here.]

### In [Target Domain]

[Brief explanation with link to target file. Show how the pattern manifests here.]

## The Mapping

| Source Domain | ↔ | Target Domain |
|---------------|---|---------------|
| [Concept A]   |   | [Concept X]   |
| [Concept B]   |   | [Concept Y]   |
| [Concept C]   |   | [Concept Z]   |

## Why This Connection Matters

[What can you now reason about by analogy? What insights transfer?]

## Where the Analogy Breaks

[Every analogy has limits. Name the specific ways these domains diverge despite the shared pattern.]

## Other Instances

[Optional: List other domains where this same mental model appears]

- **[Domain 3]** — [Brief note on how it appears]
- **[Domain 4]** — [Brief note on how it appears]
```

### Step 6: Add Cross-Links

After creating the mental model loop file:

1. **Update the source file**: Add a link in the Peripheral Knowledge section:
   ```markdown
   - **[[learning/notes/mental-model-loop/pattern-name]]** — Shares the "[Pattern Name]" mental model with [Target Domain]
   ```

2. **Update the target file**: Add a similar link:
   ```markdown
   - **[[learning/notes/mental-model-loop/pattern-name]]** — Shares the "[Pattern Name]" mental model with [Source Domain]
   ```

## Output

- **Filename:** `learning/notes/mental-model-loop/[pattern-name]-[source]-[target].md` (kebab-case)
- **Folder:** Create `learning/notes/mental-model-loop/` if it doesn't exist
- **Only create after explicit user approval**

## Examples of Good Mental Model Loops

| Pattern | Domain A | Domain B | Why it's interesting |
|---------|----------|----------|---------------------|
| Layered Abstraction | Software architecture | Chip fabrication | Both hide complexity through stable interfaces between layers |
| Conway's Law | API design | Org charts | System boundaries mirror team boundaries |
| Caching | CPU memory hierarchy | Retail inventory | Both solve "expensive to fetch, frequently needed" |
| Impedance Matching | Electronics | Data format translation | Both handle mismatched interfaces between systems |
| Feedback Control | PID controllers | Agile retrospectives | Both use measurement → adjustment loops to converge on target |
| Single Source of Truth | Database normalization | Legal contracts | Both avoid inconsistency by having one authoritative version |
