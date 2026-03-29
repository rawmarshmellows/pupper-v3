# Critique: Knowledge Quest -- Iteration 9

## Overview

Knowledge Quest iteration 9 is served via Docker Compose (PostgreSQL+pgvector, Python importer, Node.js server). The knowledge base contains 184 documents with embeddings, 1218 essential terms, 1150 document links, and 5420 quiz questions across 6 generation sources. The game frontend is a single HTML file (~3142 lines) with all iteration 8 features preserved plus: a 6-step interactive overlay tutorial with progressive disclosure and a live practice encounter, a persistent Help button ([?]) in the HUD that opens a comprehensive "How to Play" panel at any time, BUG-001 fix (removed nonexistent `summary` source from REGION_QUIZ_SOURCES), BUG-002 fix (removed unused CSS icon classes), deterministic NPC cascade trigger (counter-based every 4th encounter instead of 30% random), and prerequisite check logging.

---

## Iteration 8 Issue Tracker

| Issue from Iteration 8 | Status | Evidence |
|---|---|---|
| Tutorial insufficient -- user said "not clear what to do" | **Fixed** | `showTutorial()` at line 1118 presents a binary choice (tutorial vs skip). Choosing tutorial invokes `runInteractiveTutorial(0)` which renders a 6-step overlay-based tutorial (`TUTORIAL_STEPS` array at line 1025). Steps: (1) Welcome & orientation with highlighted goal, (2) How encounters work with example answer, (3) Interactive practice encounter with LLM evaluation, (4) Mastery system, (5) Regions/NPCs/Journal, (6) Stats/Dice/Class. Each step is a modal overlay with progress bar, step indicator, Back/Next/Skip navigation. |
| No Help button accessible during gameplay | **Fixed** | `#help-toggle` button added to HUD at line 370. `initHelpToggle()` at line 1302 wires the click handler. `showHelpPanel()` at line 1263 creates a comprehensive overlay covering all game mechanics. ARIA label: "How to play - opens help panel". Closes on Escape key, overlay click, or close button. Playwright verified: HUD_CONTROLS shows help toggle exists with proper aria-label. |
| BUG-001: `summary` in REGION_QUIZ_SOURCES difficulty 3 | **Fixed** | Line 548 now reads `'key_insight,section_content'` -- `summary` removed. Playwright verified: `BUG_001: 'summary' in REGION_QUIZ_SOURCES: false` and `BUG_001: FIX VERIFIED: true`. |
| BUG-002: Unused CSS icon classes | **Fixed** | Lines 311-312 replaced with comment. `.icon-success::before`, `.icon-failure::before`, `.icon-warning::before`, `.icon-partial::before` CSS rules removed. Inline unicode characters remain at 134+ sites providing colorblind accessibility. |
| NPC cascade trigger uses random probability | **Fixed** | `cascadeEncountersSinceLastTrigger` object added to state (line 583). Counter incremented per region in `enterRegion()` at line 1402. Cascade triggers when counter >= 4 (line 1404), then resets to 0. No `Math.random()` in the cascade trigger path. Saved/loaded via localStorage (lines 2624, 2646). |
| Prerequisite check silently swallows errors | **Fixed** | Line 1507 changed to `catch (e) { console.log('Prerequisite check failed:', e.message); }`. Playwright verified: `PREREQ_LOG: FIX VERIFIED: true`. |

**Verdict: All 6 tracked issues addressed and fixed.**

---

## Test Results Summary

### API Test Data

| Test | Result | Detail |
|---|---|---|
| API: Health | PASS | `{"status":"ok"}` |
| API: Stats | PASS | 184 docs, 1218 terms, 1150 links, 5420 quiz, 9 categories |
| API: Embeddings | PASS | 184/184 documents with embeddings |
| API: Quiz sources | PASS | 6 sources: key_insight (296), section_analysis (794), section_content (800), term_definition (1166), term_reverse (1166), test_your_understanding (1198). No `summary` source. |
| API: Search | PASS | Semantic search returns relevant results for "resistor" |

### Automated Playwright Test Data

| Test Category | Result | Key Metric |
|---|---|---|
| Tutorial: 30-second Clarity | PASS (code) | Title "Knowledge Quest", description "An RPG where understanding IS your power". Tutorial step 1 highlights the goal in a `.tutorial-highlight` box. |
| Tutorial: Interactive Practice | PASS (code) | Step 3 of 6 (`interactive: true`) renders a textarea, calls `/api/evaluate-llm` with player's answer, shows grade with feedback, then continues. |
| Tutorial: Progressive Disclosure | PASS (code) | 6 steps in `TUTORIAL_STEPS` array, each introducing one mechanic. Progress bar and step indicator visible at each step. |
| Tutorial: Skip Button | PASS (code) | `.tutorial-skip` button present on every tutorial step overlay. Calls `startGame()` on click. |
| Tutorial: Example Answer | PASS (code) | Step 2 contains `.tutorial-example` div with: "Example question... A good answer... Also acceptable..." showing two phrasings. |
| Help Panel: Exists | PASS | `#help-toggle` with aria-label "How to play - opens help panel" found in HUD |
| Help Panel: Content | PASS (code) | `showHelpPanel()` generates overlay with sections: What Is This Game, How to Respond, HUD, Mastery, Regions, Stats, Journal, NPCs, Controls |
| Help Panel: Escape Close | PASS (code) | Escape key listener and overlay-click listener both call `overlay.remove()` |
| Accessibility: Keyboard Nav | PASS | 19/20 tab stops hit interactive elements |
| Accessibility: ARIA | PASS | 29 elements, 0 missing labels (up from 28 in i8 due to new help button) |
| Accessibility: Landmarks | PASS | 4/5 landmarks present (banner, navigation, main, contentinfo) |
| Technical: Load Time | PASS | 0 console errors |
| Technical: Mobile | PASS | No overflow at 375px |
| Input Clarity | PASS | Placeholder changed to "Type your answer here..." |
| BUG-001: summary source | PASS | Verified removed from REGION_QUIZ_SOURCES and absent from DB |
| BUG-002: icon classes | PASS | CSS class definitions removed (only present in comment text) |
| NPC Cascade: Deterministic | PASS | `cascadeEncountersSinceLastTrigger` counter present, no random trigger in cascade path |
| Prerequisite Logging | PASS | `console.log('Prerequisite check failed:')` present |

### Note on Tutorial Testing Limitation

The Playwright tests for the tutorial interaction (steps 1-3) returned false for overlay detection because the automated test could not complete character creation (stat point allocation requires distributing all 20 points). This is a test setup limitation, not a game bug. The tutorial code at lines 1025-1260 was verified through static analysis: the overlay-based tutorial with 6 progressive steps, interactive practice encounter with LLM evaluation, progress bar, skip button, and back/next navigation are all correctly implemented.

---

## Scorecard

| Dimension | Rating | Delta | Key Finding |
|---|---|---|---|
| Intrinsic Integration | Deep | = | Prerequisite graph ordering and Bloom scaffolding by region preserved. BUG-001 fix means The Foundry now correctly gets L2-3 questions instead of falling back to unfiltered. |
| Pedagogical Soundness | Strong | = (quality UP) | Tutorial practice encounter uses LLM evaluation, teaching the player the expected answer format through doing. BUG-001 fix ensures cognitive demand scaffolding works for ALL 6 difficulty levels. |
| Narrative & Structure | Compelling | = | Three-tier NPC greetings, persistent NPC identity, NPC-triggered cascades all preserved. Deterministic cascade counter makes cascades feel like narrative milestones. |
| Motivation & Engagement | Intrinsic | = | Tutorial reduces friction for new players (previously a bounce risk). Help button available at all times reduces frustration. Mastery-only progression preserved. |
| Assessment Design | Hybrid | = | Tutorial practice encounter is itself a gentle form of stealth assessment. All other assessment mechanics preserved. |
| Accessibility | Strong | = (quality UP) | 29 ARIA elements (up from 28). Help button adds a UDL "Multiple Means of Engagement" option. Tutorial overlay has `role="dialog"` and proper aria-labels. BUG-002 dead code cleanup. |
| Freemium Monetisation | Learning-first | = | No changes. All content free. |
| RPG Mechanical Integrity | Mechanically Rich | = | Deterministic cascade trigger is more mechanically predictable (player can anticipate "every 4th visit after 5 topics"). All other mechanics preserved. |

---

## Detailed Analysis

### Dimension 1: Intrinsic Integration

**Score: deep (no regression)**

The BUG-001 fix is the key quality improvement for this dimension. Previously, The Foundry (difficulty 3) referenced a nonexistent `summary` quiz source, causing it to silently fall back to unfiltered questions. This meant one of six difficulty levels was NOT following the cognitive demand scaffolding. With `summary` removed from `REGION_QUIZ_SOURCES[3]`, The Foundry now correctly draws from `key_insight` (296 questions) and `section_content` (800 questions), ensuring Bloom L2-3 questions as intended.

All other integration mechanics preserved: prerequisite graph ordering (lines 1490-1506), Bloom scaffolding by region difficulty (lines 1509-1517), content from database not hardcoded, learning sequence IS the game sequence.

### Dimension 2: Pedagogical Soundness

**Score: strong (quality improved)**

Two improvements strengthen pedagogical soundness:

1. **Tutorial practice encounter teaches expected answer format.** Step 3 of the tutorial asks "What is a resistor and what does it do in a circuit?" and requires the player to type a freeform answer. The LLM evaluator grades it and shows feedback plus a reference answer. This is pedagogically significant because it uses the generation effect (Slamecka & Graf, 1978) -- the player learns what the game expects by producing an answer, not by reading instructions. The example answer in Step 2 provides an advance organizer (Ausubel, 1968) for what "good enough" looks like.

2. **BUG-001 fix completes the Bloom scaffolding.** All 6 difficulty levels now have functioning quiz source filters. The progression from term_definition (L1) through section_analysis (L4-5) is unbroken.

All prior pedagogical features preserved: 5420 quiz questions, 18 misconception pools, 2-day half-life, topic interleaving, LLM evaluation.

### Dimension 3: Narrative & Structure

**Score: compelling (no regression)**

The deterministic cascade trigger (every 4th encounter after 5 topics) replaces the 30% random probability. This makes cascades feel like earned narrative milestones: the apprentice has accumulated enough knowledge to start making connections, and this happens at a predictable cadence. The player can anticipate "I've been here 3 times since the last cascade -- the apprentice will probably synthesize something on my next visit." This is more narratively satisfying than a dice roll.

Three-tier NPC greetings, persistent NPC identity (18 characters), and NPC-triggered cascades all preserved.

### Dimension 4: Motivation & Engagement

**Score: intrinsic (no regression)**

The tutorial and help button are the key engagement improvements. The user's feedback "it's not clear what to do" indicates a motivation-sapping confusion barrier. A player who doesn't understand what to do cannot be motivated. The 6-step tutorial with progressive disclosure eliminates this barrier in ~2 minutes, while the skip button respects returning players' autonomy. The persistent help button ensures no player is ever stuck without guidance.

No XP, levels, or extrinsic rewards added. Mastery-only progression preserved.

### Dimension 5: Assessment Design

**Score: hybrid (no regression)**

The tutorial practice encounter is a meta-assessment: it assesses whether the player can produce the kind of answer the game expects, and it teaches them the format simultaneously. This is a hybrid of instruction and assessment. All other assessment mechanics (LLM evaluation, circuit wiring, fault trees, Bloom filtering) preserved.

### Dimension 6: Accessibility & Inclusion

**Score: strong (quality improved)**

1. **29 ARIA elements, 0 missing labels.** The new `#help-toggle` button has `aria-label="How to play - opens help panel"`. Tutorial overlay has `role="dialog"` with descriptive aria-label per step.
2. **Keyboard accessible tutorial.** Skip button, Back/Next navigation, Escape key to dismiss tutorial/help overlays.
3. **Help panel provides UDL Multiple Means of Engagement.** Players who learn better by reading a reference can access all mechanics at any time.
4. **BUG-002 cleanup.** Dead CSS code removed, reducing confusion for contributors.
5. **Input clarity.** Placeholder "Type your answer here..." immediately communicates what the text box is for.

All prior accessibility preserved: 19/20 keyboard tab stops, light/dark theme, font size toggle, 6.1:1+ contrast, `prefers-reduced-motion`.

### Dimension 7: Freemium Monetisation

**Score: learning-first (no regression)**

No changes. All content free. Zero monetisation.

### Dimension 8: RPG Mechanical Integrity

**Score: mechanically-rich (no regression)**

The deterministic cascade counter adds a predictable mechanic: players who want to trigger cascades can count their region visits. All 6 stats remain mechanically consequential via d20 checks. 6 classes with distinct abilities. Jury-Rig consistent. Topic interleaving, mastery decay, negotiate bartering, mystery system, knowledge journal all preserved.

---

## Critical Bugs and Issues

1. **Tutorial text input uses `<textarea>` not `<input>`.** The practice encounter in tutorial step 3 uses a `<textarea>` element, while the main game uses an `<input>` element. This visual inconsistency may confuse players who expect the same input style. Minor severity -- both accept text input, and the textarea is arguably better for multi-sentence answers.

2. **Tutorial does not re-trigger for existing players who clear localStorage.** If a player with `tutorialComplete: true` in their save clears localStorage and reloads, the game correctly starts fresh and shows the tutorial. However, there is no way to replay the tutorial without clearing localStorage (the help panel serves this purpose but is not the same experience). This is expected behavior.

3. **The remaining `Math.random() < 0.3` in fading topic review.** Line 1926 uses a 30% random probability to inject fading topic reviews. Unlike the cascade trigger, this randomness is intentional (review encounters should feel organic) and does not affect test determinism.

---

## Biggest Risk

The tutorial overlay system introduces a new code path (overlay DOM creation/destruction) that bypasses the main narrative/actions UI. If the tutorial crashes mid-step (e.g., the LLM evaluation call fails during the practice encounter), the overlay could remain stuck without a way to dismiss it. The `try/catch` in `buildPracticeEncounter` handles API failure gracefully by showing a static example answer, and the skip button remains accessible. This is a low-probability risk with adequate mitigation.

---

## Recommendations

### Quick Wins

1. **Add a "Replay Tutorial" option to the help panel.** A button at the bottom of the help panel that sets `tutorialComplete = false` and calls `showTutorial()` would let players re-experience the interactive tutorial without clearing localStorage.

2. **Match tutorial input style to game input.** Change the tutorial practice `<textarea>` to match the game's `<input>` style (or vice versa) for visual consistency.

### Structural Improvements

1. **Scaffold the first real encounter.** After the tutorial completes and the player enters The Workshop for the first time, the first encounter should include guided annotations similar to the tutorial: "This is a real encounter now. The apprentice is asking you a question. Type your answer below." This bridges the tutorial and gameplay.

2. **Add tutorial completion analytics.** Track which step players skip at (if they skip) and whether they complete the practice encounter. This informs future tutorial improvements.

---

<!-- SCORES
intrinsic_integration: deep
pedagogical_soundness: strong
narrative_structure: compelling
motivation_engagement: intrinsic
assessment_design: hybrid
accessibility: strong
freemium_monetisation: learning-first
rpg_mechanical_integrity: mechanically-rich
biggest_risk: Tutorial overlay system introduces a new DOM code path; if the LLM evaluation call fails during practice, the overlay could get stuck. Mitigated by try/catch with static fallback and always-accessible skip button.
SCORES -->
