# Knowledge Quest -- Iteration 6 Design Specification

## Key Changes from Iteration 5

### 1. RPG Mechanical Integrity (NEW dimension)
- **Stats affect every encounter** via d20+stat modifier checks:
  - INT: theory, prediction, decode, cross-domain synthesis, circuit build diagnostics
  - WIS: diagnosis, fault tree initial assessment, fading topic recall, mystery insight
  - DEX: circuit wiring (fewer distractors on success)
  - CHA: negotiation (rapport discount), teaching (lower bar for partial answers)
  - STR: component choice (brute-force eliminates wrong options)
  - CON: endurance in long fault tree diagnostic chains (4+ steps)
- **Class abilities** (each class has a unique mechanical bonus):
  - Engineer: +3 DEX on wiring checks
  - Scholar: +3 INT on theory/prediction checks
  - Tinker: Jury-Rig -- spend 3 Stamina to retry a failed check (once per encounter)
  - Sage: +3 CHA on teaching/negotiation checks
  - Explorer: +3 WIS on diagnosis checks
  - Artificer: +3 INT on negotiate checks (craft components)
- **Guided tutorial** after character creation:
  - Explains the world (Circuit Citadel, regions, purpose)
  - Walks through stat checks with a live example roll
  - Explains mastery decay system
  - Shows a sample encounter flow
  - Skippable by experienced players
  - Takes under 2 minutes
- **Half-life mastery decay**:
  - strength = 2^(-timeSinceReview / halfLife)
  - halfLife starts at 1 day (86400000ms)
  - Doubles on each successful review
  - Halves on failure (minimum 6 hours)
  - Topics below 0.5 strength are "fading" -- shown as colored bars
  - Fading topics prioritized for spaced repetition encounters
  - In-region review encounters for fading topics (30% chance)
  - Dedicated "Review fading topics" option on world map

### 2. Pedagogical Soundness (mixed -> targeting strong)
- **LLM-based evaluation** replaces cosine similarity as primary:
  - POST /api/evaluate-llm using google/gemini-2.0-flash-001 via OpenRouter
  - Sends question + correct answer + player answer + rubric
  - Returns {grade, feedback, misconception, source}
  - Grades on CONCEPTUAL UNDERSTANDING, not vocabulary matching
  - Cosine similarity kept only as fallback if LLM call fails
  - Every text evaluation now uses LLM (diagnosis, predict, teach, negotiate, apply, cross-domain, cascade, mystery, review)
  - LLM feedback displayed to player after each evaluation
- **Misconception detection** via LLM response field
- **Stat checks provide scaffolding**: successful checks reveal hints, failed checks give less context

### 3. Preserved Dimensions (must not regress)
- **Intrinsic Integration: deep** -- All mechanics unchanged
- **Motivation & Engagement: intrinsic** -- NO XP/level, mastery-only progression, no gold in HUD
- **Narrative & Structure: functional** -- 6 regions, mystery system, concept cascades, knowledge journal
- **Assessment Design: hybrid** -- Circuit wiring, fault tree, text evaluation (now LLM-based)
- **Accessibility: adequate** -- ARIA labels, keyboard nav, reduced-motion, no horizontal scroll
- **Freemium Monetisation: learning-first** -- All content free, premium defined but not gated

## Architecture

### Frontend (index.html)
- Single self-contained HTML file with embedded CSS and vanilla JavaScript
- Mobile-responsive, dark theme, touch-friendly (44px targets)
- localStorage for state persistence with migration for old mastery entries
- All content from API (no hardcoded educational content)

### Server (server.js)
- Express.js REST API
- NEW endpoint: POST /api/evaluate-llm (Gemini via OpenRouter)
- Preserved: all existing endpoints unchanged
- Cosine similarity endpoints kept as fallback

### Database (init.sql)
- pgvector/pgvector:pg16
- Schema unchanged from iteration 5
- HNSW indexes for semantic search

### Importer (import_notes.py)
- Unchanged from iteration 5
- Reads Obsidian markdown notes, generates embeddings via OpenRouter
