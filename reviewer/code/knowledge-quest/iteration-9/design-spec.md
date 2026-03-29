# Knowledge Quest -- Iteration 9 Design Specification

## Focus: Full Interactive Tutorial / Onboarding Overhaul

### Problem Statement
User feedback from iteration 8: "right now it's not clear what to do." The previous tutorial was a series of text walls explaining mechanics, with no interactive practice and no example of what a good answer looks like. New players could not understand within 30 seconds what the game is, what they should do, or how to interact.

### Changes in Iteration 9

#### Priority 1: Interactive Tutorial System

**Architecture:** Replaced the old `showTutorial()` function (which used in-narrative text blocks) with a dedicated **overlay-based tutorial system** using 6 progressive disclosure steps:

1. **Welcome & Orientation** (Step 1/6): Tells the player who they are, what the game is about, and their goal. The "30-second clarity test" answer is delivered in a highlighted box.

2. **How Encounters Work** (Step 2/6): Explains the two input methods (click buttons OR type in text box), that most encounters ask for freeform text explanations, and shows a concrete example of a good answer with an alternative acceptable phrasing.

3. **Interactive Practice Encounter** (Step 3/6): The player actually types an answer to "What is a resistor and what does it do in a circuit?" The answer is evaluated by the LLM evaluator in real-time. The player sees their grade (correct/partial/incorrect) with feedback and a reference answer. This teaches them the expected format by doing, not reading.

4. **Mastery System** (Step 4/6): Explains the half-life decay model, what the HUD elements mean, and how mastery tracking works.

5. **Regions, NPCs, and Journal** (Step 5/6): Covers the 6 regions, NPC persistence, mystery system, and knowledge journal.

6. **Stats, Dice, and Class Ability** (Step 6/6): Explains the d20+stat system and the player's specific class ability.

**UI Features:**
- Progress bar and step indicator ("Step 3 of 6")
- Skip Tutorial button accessible at every step
- Back/Next navigation between steps
- Distinct visual style (overlay panel, not inline narrative text)
- Keyboard accessible (Escape to skip, focus management)
- Takes ~2 minutes to complete

**Persistent Help Panel:**
- A [?] button added to the HUD, always visible during gameplay
- Opens an overlay with a comprehensive "How to Play" reference covering all mechanics
- Closeable with Escape key or close button
- Available at any time, even mid-encounter

**Input Clarity:**
- Freeform input placeholder changed from "Or type a custom action..." to "Type your answer here..."
- ARIA label updated to "Type your answer or action here"

#### Priority 2: Bug Fixes

1. **BUG-001 Fixed:** Removed `summary` from `REGION_QUIZ_SOURCES` difficulty 3. Changed from `'key_insight,summary,section_content'` to `'key_insight,section_content'`. The `summary` quiz source does not exist in the database, so The Foundry was silently falling back to unfiltered questions.

2. **BUG-002 Fixed:** Removed unused CSS icon classes (`.icon-success`, `.icon-failure`, `.icon-warning`, `.icon-partial`). Inline unicode characters provide the same colorblind accessibility benefit.

3. **Deterministic NPC Cascade Trigger:** Replaced the 30% random probability with a deterministic counter. Added `cascadeEncountersSinceLastTrigger` per region to state (saved/loaded via localStorage). After the apprentice has 5+ discussed topics, a cascade triggers every 4th encounter in that region.

4. **Prerequisite Check Logging:** Changed `catch(e){}` to `catch(e){ console.log('Prerequisite check failed:', e.message); }` for debugging.

#### Priority 3: Preserved Features

All 8 dimensions from iteration 8 are fully preserved:
- Deep intrinsic integration (prerequisite graph, Bloom scaffolding)
- Strong pedagogical soundness (5420 quiz questions, 18 misconception pools, interleaving)
- Compelling narrative (3-tier NPC greetings, persistent NPCs, cascade triggers)
- Intrinsic motivation (mastery-only progression, no XP/levels)
- Hybrid assessment (LLM evaluator, circuit wiring, fault trees)
- Strong accessibility (ARIA, keyboard nav, light/dark theme, font sizes)
- Learning-first monetisation (all free, zero monetisation)
- Mechanically-rich RPG (6 stats, 6 classes, d20 checks, Jury-Rig)

## Architecture

Unchanged from iteration 8:
- Docker Compose: pgvector/pg16 + Python importer + Node.js server
- 184 documents, 1218 terms, 1150 links, 5420 quiz questions (all with embeddings)
- LLM evaluation via Gemini 2.0 Flash (OpenRouter)
- Hybrid search: pgvector cosine + full-text RRF
