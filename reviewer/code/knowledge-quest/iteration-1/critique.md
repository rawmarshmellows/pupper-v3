# Critique: Knowledge Quest — Iteration 1

## Overview

Knowledge Quest is a text-based RPG built as a Docker Compose project (PostgreSQL+pgvector, Python importer, Node.js server). The knowledge base successfully imports 184 documents with 599 essential terms, 1113 document links, and full vector embeddings. The hybrid search (semantic + fulltext via RRF) works correctly. The game frontend is a single-page HTML app with character creation, region-based exploration, and multiple encounter types.

## API & Infrastructure Assessment

**Working well:**
- All core API endpoints respond correctly: `/api/health`, `/api/stats`, `/api/search`, `/api/topics`, `/api/terms`, `/api/similar`
- Semantic search returns relevant results (tested with "voltage", "capacitor", "PCB" queries)
- Embedding pipeline imported all 184 documents with 512-dimension vectors
- Docker Compose orchestration is solid (healthchecks, dependency ordering)

**Issues:**
- Quiz questions: 0 imported. The importer's regex for extracting Q&A pairs from "Test Your Understanding" sections doesn't match the actual note format. This means `/api/quiz/random` always returns 404, breaking guardian encounters and skill check encounters
- Route ordering bug fixed mid-build: `/api/topics/random` was being caught by `/api/topics/:id`

---

## Dimension 1: Intrinsic Integration

**Score: partial**

The game attempts to make knowledge the core mechanic: you must understand concepts to progress through regions, solve puzzles, and pass guardians. The region-based structure maps to the knowledge base tiers (micro/quick/small), and encounters pull real content from the database.

However, the integration is only partial:
- **Quiz-gating pattern persists.** Most encounters reduce to "here is some text, now answer a question about it." The learning content is displayed, then tested — this is chocolate-covered broccoli in narrative wrapping.
- **Understanding doesn't drive decisions.** The player doesn't need to *reason about* circuits to navigate the world. They read a knowledge panel and then type keywords back. The game would work identically with any subject matter.
- **Skill checks offer escape hatches.** Players can bypass knowledge challenges with stat checks (INT, WIS, CHA), making understanding optional.
- **The RPG mechanics (HP, combat, gold) are decorative.** Removing them wouldn't fundamentally change the learning experience.

**What would "deep" look like:** The player needs to *apply* circuit knowledge to solve puzzles — e.g., choosing the right component to complete a circuit, calculating a voltage divider to open a door, or debugging a circuit where the symptoms require understanding of how components interact.

## Dimension 2: Pedagogical Soundness

**Score: mixed**

**Strengths:**
- Content comes from the actual knowledge base (not hardcoded), ensuring accuracy
- The 6-region structure creates a natural learning progression from basic to advanced
- Spaced repetition is integrated (review every 5 turns)
- Wrong answers always show the correct answer (formative feedback)
- Multiple approach paths (answer directly, use skills, search for clues)

**Weaknesses:**
- **0 quiz questions imported.** The primary assessment mechanism (quiz/random) returns empty. Guardian encounters and skill checks that depend on quiz data fall back to exploration encounters, dramatically reducing challenge variety.
- **Keyword matching is crude.** The answer evaluation simply checks if the player's text contains keywords from the correct answer. This rewards copying fragments from the knowledge panel rather than demonstrating understanding.
- **Bloom's levels are only nominally targeted.** The code references Bloom's levels but all encounters functionally test at Remember/Understand level — no encounters require analysis, evaluation, or creation.
- **No misconception traps.** The game doesn't surface common misconceptions or use them as distractors.
- **Reading-before-testing pattern.** Players are shown the answer (in knowledge panels) before being asked the question, reducing retrieval practice to recognition.

## Dimension 3: Narrative & Structure

**Score: functional**

The Circuit Citadel metaphor works reasonably well. Each region has distinct flavor text, NPCs have personality, and the progression from Workshop to Motion Arena creates a natural learning arc. The encounter variety (puzzle, NPC dialogue, investigation, merchant, terminal, guardian) prevents monotony.

**Weaknesses:**
- Narrative text is generic — the descriptions could apply to any subject domain
- No persistent quest line or story arc; encounters are disconnected vignettes
- NPC interactions are one-shot; there's no relationship building
- The "Citadel" metaphor doesn't inherently connect to electronics/engineering

## Dimension 4: Motivation & Engagement

**Score: mixed**

**Positive:**
- Character creation with 6 classes gives initial investment
- XP and leveling provides progression feedback
- Region unlocking gates content naturally
- Gold rewards and inventory items provide tangible feedback

**Negative:**
- **External reward dominance.** The primary motivators are XP, gold, and leveling — all extrinsic. The learning itself isn't intrinsically rewarding through gameplay.
- **Low stakes.** Death merely costs 10 gold and teleports you back. There's no meaningful consequence for failure.
- **Repetitive loop.** Enter region → see knowledge panel → answer question → get XP → repeat. The core loop lacks variety.
- **No curiosity drivers.** There's nothing that makes the player *want* to explore the knowledge graph. No mysteries, secrets, or "I need to understand X to solve this specific problem."

## Dimension 5: Assessment Design

**Score: overt**

Assessment is essentially "answer this question" presented through various narrative wrappers. Despite the variety of encounter types (guardian, puzzle, merchant, terminal), they all reduce to the same mechanic: display correct information, then ask the player to reproduce keywords.

**Specific issues:**
- Quiz question extraction failed (0 questions), so the system relies entirely on term definitions for challenges
- No stealth assessment — the player always knows they're being tested
- Keyword matching can be gamed by including common domain words without understanding
- No performance analytics beyond simple correct/attempt counts

## Dimension 6: Accessibility & Inclusion

**Score: adequate**

**Strengths:**
- Dark theme with good base contrast
- Mobile-responsive layout (max-width 600px, touch-friendly 44px targets)
- Semantic HTML (role attributes, aria-labels)
- Keyboard shortcuts for choices (1-9 keys)
- `safe-area-inset` padding for notched phones
- localStorage persistence

**Weaknesses:**
- No light theme option
- No font size controls
- Screen reader experience untested but landmarks are present
- No reduced motion option
- Color coding without redundant indicators (success = green, danger = red)

## Dimension 7: Freemium Monetisation

**Score: balanced**

The free tier includes all 6 regions, full character creation, and complete learning objectives. Premium content (advanced classes, bonus regions, cosmetics, challenge modes) is defined but not implemented — it's just a JavaScript config object. This means the free experience IS the complete experience, which is correct for a prototype. No predatory patterns, no artificial friction.

---

## Biggest Risk

The game is fundamentally quiz-gated: knowledge panels display information, then the player is asked to reproduce it. This chocolate-covered-broccoli pattern means learning and gameplay are separate activities despite the narrative wrapping. Combined with 0 quiz questions actually imported, the challenge variety is severely limited.

## Priority Fixes

1. **Fix quiz question extraction** — The importer regex doesn't match the note format. Without quiz questions, half the encounter types don't work.
2. **Redesign encounters so understanding IS the mechanic** — Instead of "read panel → answer question," make encounters where the player must *apply* knowledge (e.g., choose components, diagnose circuits, predict behavior).
3. **Remove knowledge panels before questions** — Don't show the answer before asking. Force genuine retrieval practice.
4. **Add higher Bloom's level encounters** — Create analysis/evaluation tasks, not just recall.
5. **Add persistent narrative threads** — Give the player a reason to explore beyond XP accumulation.

---

<!-- SCORES
intrinsic_integration: partial
pedagogical_soundness: mixed
narrative_structure: functional
motivation_engagement: mixed
assessment_design: overt
accessibility: adequate
freemium_monetisation: balanced
biggest_risk: Learning content is quiz-gated (read panel then answer) rather than intrinsically integrated into gameplay decisions, and 0 quiz questions were imported so challenge variety is severely limited
SCORES -->
