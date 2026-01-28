---
name: deep-dive
description: Comprehensive research for deeply understanding a new field from first principles to practitioner-level intuition
---

**Output Instructions:** Save this research to a markdown file at `research/$ARGUMENTS.md` (sanitize the filename by replacing spaces with hyphens and removing special characters). Create the `research/` directory if it doesn't exist. Write the complete research document to the file, then confirm the file path to the user.

**Source Document Linking:** If $ARGUMENTS references or builds upon an existing document in this vault (e.g., "the robotic arm API document", "my notes on PLCs", or a specific filename), add a "Related Documents" section at the top of the output (after the frontmatter) with Obsidian-style wiki links to those source documents. Use the format `[[folder/filename]]` for cross-folder links or `[[filename]]` for same-folder links. Example:
```
> **Related:** [[quick-context/robotic-arm-api-levels]]
```

---

I want to understand **$ARGUMENTS** well enough to have informed conversations with practitioners and identify non-obvious opportunities or problems.

Help me build understanding in layers:

---

## 1. First Principles

- What problem does this field exist to solve?
- What would the world look like without it?
- What are the core constraints and tradeoffs practitioners navigate daily?

---

## 2. Vocabulary and Mental Models

- What are the 15-20 terms I'd need to not sound like an outsider?
- What are the dominant frameworks people use to think about problems here?
- Are there competing vocabularies between subgroups or schools of thought?

---

## 3. The Landscape

- Who are the key players (companies, researchers, institutions)?
- What are the major "schools of thought" or competing approaches?
- Where is there genuine disagreement vs. settled consensus?
- What's the relationship between academia and industry in this field?

---

## 4. History and Trajectory

- What were the major inflection points that shaped current practice?
- What's the "received wisdom" that's starting to be questioned?
- Where does the field seem to be heading?
- What external forces (technology, regulation, market shifts) are changing the game?

---

## 5. The Dirty Secrets

- What do practitioners complain about privately?
- What are the known hard problems everyone's stuck on?
- What are the "obvious" solutions that don't actually work, and why?
- What does the field get wrong about itself or oversell to outsiders?

---

## 6. Entry Points (With Synthesis)

For each of the following, identify the most respected source AND provide a substantive summary of its core arguments/contributions:

### a) The Foundational Text

- What's the book or paper that shaped how the field thinks today?
- Summarize its core thesis, key frameworks, and why it became canonical
- What critiques or limitations have emerged since?

### b) The Current State-of-the-Art

- What's the most cited recent work (last 3-5 years) that practitioners actually reference?
- Summarize what it advances beyond previous understanding
- What questions does it open up or leave unresolved?

### c) The Best "Outsider-to-Insider" Bridge

- What resource do practitioners recommend to smart people entering from adjacent fields?
- Summarize its key lessons and what makes it effective for building intuition

### d) The Contrarian or Revisionist Take

- What's a well-argued piece that challenges mainstream thinking in the field?
- Summarize its argument and how the field has responded
- Is it gaining traction or still fringe?

### e) The Practitioners' Watering Holes

- What podcasts, newsletters, forums, or conferences do serious people actually pay attention to?
- For the top 2-3, summarize the general perspective or bias they represent
- What recurring debates or themes show up?

### f) The "If You Only Read One Thing" Synthesis

Given everything above, write a 500-word synthesis that captures the essential knowledge—the thing I could read before walking into a room of practitioners and hold my own in conversation.

---

## 7. My Learning Path

Based on my background in AI agent architecture, spatial data applications, and infrastructure asset management, suggest:
- Which sections of the field I'll grasp quickly due to transferable knowledge
- Where my existing mental models might mislead me
- A prioritized sequence for going deeper (what to learn first, second, third)
- One small project or exercise that would force me to apply this knowledge
