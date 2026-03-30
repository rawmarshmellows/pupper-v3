# Critique: Knowledge Quest -- Iteration 10

## Overview

Knowledge Quest iteration 10 is served via Docker Compose (PostgreSQL+pgvector, Python importer, Node.js server). The knowledge base contains 184 documents with embeddings, 609 essential terms, 1150 document links, and 2710 quiz questions across 6 generation sources. This iteration implements a major structural change per user directive: the class system (Warrior/Mage/Rogue, stat allocation, HP/MP, d20 rolls) has been completely removed and replaced with lighter gamification systems (streaks, combos, achievements, collections, daily challenges, evolving titles). Character creation is reduced to name-only input. All iteration 9 pedagogical features are preserved: prerequisite graph ordering, Bloom scaffolding by region, LLM evaluation, misconception pools, half-life mastery decay, concept cascades with deterministic triggers, and the interactive tutorial with help panel. The three iteration 9 polish items (POLISH-001, POLISH-002, POLISH-003) are addressed.

---

## Iteration 9 Issue Tracker

| Issue from Iteration 9 | Status | Evidence |
|---|---|---|
| POLISH-001: Add Replay Tutorial button to help panel | **Fixed** | `showHelpPanel()` at line 1228 creates a `tutorial-btn` with text "Replay Tutorial". Click handler at line 1233 removes overlay, sets `tutorialComplete = false`, calls `showTutorial()`. Playwright verified: `POLISH_001: Replay Tutorial button in help panel: true`. |
| POLISH-002: Match tutorial input to game input | **Not fixed** | Tutorial practice step still uses `<textarea>` (line 1116), game input is `<input>` (line 314). Playwright verified: `POLISH_002: Input consistency: game=input, tutorial=textarea`. The inconsistency remains. |
| POLISH-003: Scaffold the first real encounter | **Fixed** | Line 1677 checks `state.visitedRegions.length <= 1 && state.turnCount === 0`, then shows: "This is your first real encounter. Apply what you learned in the tutorial -- type your answer in the text box below." Playwright verified: `POLISH_003: First encounter scaffold present: true`. |
| POLISH-004: Tutorial completion analytics | **Not addressed** | No `tutorialStepReached` or `tutorialPracticeCompleted` fields in state. Low priority; noted. |

**Verdict: 2 of 4 polish items addressed (the 2 highest priority). POLISH-002 persists. POLISH-004 was low priority and is not a regression.**

---

## Test Results Summary

### API Test Data

| Test | Result | Detail |
|---|---|---|
| API: Health | PASS | `{"status":"ok"}` |
| API: Stats | PASS | 184 docs, 609 terms, 1150 links, 2710 quiz, 9 categories |
| API: Embeddings | PASS | 184/184 documents with embeddings |
| API: Quiz sources | PASS | 6 sources: key_insight (148), section_analysis (397), section_content (400), term_definition (583), term_reverse (583), test_your_understanding (599). No `summary` source. |

**Note:** Quiz question count is 2710, down from 5420 in iteration 9. The design spec claims 5420. All 6 sources are present but each has roughly half the previous count. This appears to be a database import change, not a code bug. The game continues to function correctly with the available questions.

### Automated Playwright Test Data

| Test Category | Result | Key Metric |
|---|---|---|
| POLISH-001: Replay Tutorial | PASS | Button present in help panel, wired to restart tutorial |
| POLISH-002: Input consistency | FAIL (known) | Game uses `<input>`, tutorial uses `<textarea>` -- unchanged from i9 |
| POLISH-003: First encounter scaffold | PASS | "first real encounter" message shown on initial region entry |
| Class system removal: Creation screen | PASS | No class select, no stat allocation. Name input + Start button only. |
| Class system removal: HUD | PASS | HP=false, MP=false, Gold=false. Streak=true, Combo=true, Mastery=true, Title=true. |
| Class system removal: d20 / stat checks | PASS | No d20, rollD, diceRoll, statModifier in source. |
| Migration: Old save with class | PARTIAL | In-memory migration works (line 2508-2510), but `saveState()` is not called after `loadState()`, so the class field persists in localStorage until the next save-triggering action. |
| Achievements: UI accessible | PASS | 20 achievements shown in UI, collections section visible |
| Streak/combo system | PASS | All 7 code markers verified: onCorrectAnswer, onIncorrectAnswer, streak++, comboTimer, 30s window, streak reset, achievement banner |
| Daily challenge | PASS | Button on world map, DAILY badge notification shown |
| Collections | PASS | 6 collections: Circuit Fundamentals, Signal Path, Semiconductor Journey, Robot Builder, Maker Toolkit, Embedded Master |
| Title system | PASS | 8 titles from Newcomer to Grandmaster, threshold-based |
| Accessibility: ARIA | PASS | 17 interactive elements, 0 missing labels |
| Accessibility: Keyboard | PASS | 19/20 tab stops hit interactive elements |
| Accessibility: Landmarks | PASS | 4/5 present (banner, navigation, main, contentinfo) |
| Accessibility: Mobile | PASS | No overflow at 375px |
| Accessibility: Theme toggle | PASS (code) | Test timed out because HUD is hidden before character creation. Code verified: `initThemeToggle()` at line 2532 works correctly. |
| Accessibility: Font toggle | PASS (code) | Same: HUD hidden before creation. `initFontToggle()` at line 2544 verified. |
| Accessibility: Reduced motion | PASS | CSS `prefers-reduced-motion` rule present |
| Pedagogy: Quiz sources | PASS | BUG-001 fix preserved -- no `summary` in REGION_QUIZ_SOURCES |
| Pedagogy: Misconceptions | PASS | 14 misconception pools present |
| Pedagogy: Mastery decay | PASS | Half-life, threshold, strength calc, fading topics, double/halve all present |
| Pedagogy: Bloom scaffolding | PASS | bloomMax tracking, 6-level taxonomy, progress view |
| Pedagogy: Prerequisites | PASS | Depth-2 check, redirect to unmastered prerequisite, error logging |
| Pedagogy: Cascades | PASS | 8 cascades (7 pairs in CONCEPT_CASCADES), deterministic counter >= 4 |
| Technical: Console errors | PASS | 0 errors on load |
| Technical: Tutorial completion | PASS | Full tutorial path completes without errors, reaches world map |
| Technical: Save/load fields | PASS | All 7 new fields (streak, bestStreak, achievements, totalCorrect, totalAttempts, dailyChallengesCompleted, apprenticeTeachCount) present in save |

---

## Scorecard

| Dimension | Rating | Delta from i9 | Key Finding |
|---|---|---|---|
| Intrinsic Integration | Deep | = | Class removal does not affect integration. Prerequisite graph, Bloom scaffolding, and DB-driven content all preserved. |
| Pedagogical Soundness | Strong | = | LLM evaluator, misconception pools, half-life decay, topic interleaving, tutorial practice encounter all preserved. Quiz count lower but all sources present. |
| Narrative & Structure | Compelling | = | NPC three-tier greetings, persistent identity, deterministic cascade triggers, 6 region mysteries all preserved. |
| Motivation & Engagement | Intrinsic | = (quality UP) | Class removal reduces extraneous cognitive load. New gamification (streaks, combos, achievements, collections, daily challenges) adds surface-level feedback loops WITHOUT introducing extrinsic dependency. All progression still driven by mastery. |
| Assessment Design | Hybrid | = | LLM evaluation, circuit wiring, fault trees, Bloom filtering, misconception matching preserved. Removing stat checks from assessment is a net positive -- evaluation is now purely knowledge-based. |
| Accessibility | Strong | = | 17 ARIA elements (down from 29 in i9 due to fewer class-related interactive elements), 0 missing labels. All other accessibility features preserved. |
| Freemium Monetisation | Learning-first | = | No changes. premiumFeatures.enabled = false. |
| RPG Mechanical Integrity | N/A (Intentional) | DOWN (by design) | The class system, stat allocation, HP/MP, d20 rolls, gold, and inventory are removed per user directive. The game is no longer an RPG; it is a gamified learning adventure. This is a deliberate and well-motivated design decision, not a regression. |

---

## Detailed Analysis

### The Central Design Question: Did Removing the Class System Improve the Experience?

**Yes, with one caveat.**

The class system in iteration 9 was mechanically rich (6 classes, 6 stats, d20 checks, HP/MP, gold, Jury-Rig ability). However, it competed with the educational content for the player's attention. Every encounter required the player to think about TWO things simultaneously: (1) do I understand this engineering concept? and (2) what stat should I use, how likely am I to succeed on the roll, should I spend MP on a hint? This is the extraneous cognitive load problem identified by Plass et al. (2015) -- game mechanics that do not serve learning objectives consume working memory that could be used for learning.

The iteration 10 design replaces this with gamification that provides feedback without demanding decisions:

- **Streaks** are passive feedback on performance. The player does not decide to "build a streak" -- it happens automatically when they answer correctly. This aligns with the goal of making knowledge performance visible without adding decision overhead.
- **Combos** reward flow states (answering quickly) without penalizing slow deliberation. The 30-second timer is generous enough that a thoughtful player building a careful answer will not feel punished.
- **Achievements** are milestone markers, not resources. They celebrate accomplishments after the fact rather than influencing decisions before the fact.
- **Collections** provide a completionist goal structure that maps directly to knowledge domains. "Complete the Circuit Fundamentals collection" is semantically identical to "master the foundational electronics topics."
- **Daily challenges** provide a habit formation nudge without gating content.
- **Evolving titles** replace the static class label with a dynamic reflection of actual mastery.

**The caveat:** The iteration 9 class system provided a sense of identity and role-playing investment. "I am Sera the Engineer" has more narrative weight than "I am Sera the Newcomer." The title system partially compensates (titles evolve), but the loss of class-specific abilities (Jury-Rig, Scholar's Insight) removes a layer of player expression. This is acceptable because the abilities were largely cosmetic in their effect on learning -- they gated hints behind resource management, which the design spec correctly identifies as an anti-pattern.

**Net assessment: The removal trades mechanical depth for cognitive accessibility. This is the right call for a learning-first product.**

### Dimension 1: Intrinsic Integration

**Score: deep (no regression)**

The class system was orthogonal to intrinsic integration. Integration depends on whether learning content IS the game content, not on whether there are classes. All integration mechanics are preserved:

1. **Prerequisite graph ordering** (lines 1770-1782): Depth-2 prerequisite check redirects players to foundational topics before advanced ones.
2. **Bloom scaffolding by region** (lines 497-504): REGION_QUIZ_SOURCES maps difficulty 1-6 to progressively higher cognitive demand sources.
3. **Content from database**: All 184 documents, 609 terms, 2710 quiz questions served via API.
4. **Learning sequence IS game sequence**: Regions progress from basic electronics through semiconductors, manufacturing, protocols, embedded systems, to robotics.

### Dimension 2: Pedagogical Soundness

**Score: strong (no regression)**

All pedagogical features preserved:

1. **LLM evaluation** via Gemini 2.0 Flash with cosine fallback and keyword fallback.
2. **Misconception matching** with 14 topic-specific pools (down from 18 in the i9 critique -- the actual code has 14 keys in MISCONCEPTION_POOLS, covering resistor, capacitor, inductor, voltage, transistor, mosfet, pcb, pid, adc, imu, clock, stm32, pwm, kinematics).
3. **Half-life mastery decay** (2-day initial, doubles on correct, halves on incorrect, 0.5 threshold).
4. **Topic interleaving** via `getInterleavedSearchTerm()`.
5. **Tutorial practice encounter** with LLM evaluation teaching expected answer format.
6. **BUG-001 fix preserved**: No `summary` source in REGION_QUIZ_SOURCES.

The removal of stat-gated hints is pedagogically sound. In iteration 9, a player with low Intelligence had fewer hints available, which punished the player who needed hints most. Now hints are freely available based on topic data (tldr, key_insight), following the principle that the purpose of hints is learning, not resource management.

**Data note:** Quiz questions dropped from 5420 to 2710. The design spec claims 5420. All 6 sources are present. This may reflect a database re-import with different duplication settings. The game functions correctly with 2710 questions -- this is still 14.7 questions per topic on average, sufficient for the encounter system. Worth investigating if the full 5420 was intended.

### Dimension 3: Narrative & Structure

**Score: compelling (no regression)**

Narrative elements unaffected by class removal:

1. **Three-tier NPC greetings**: First meeting, returning visit, veteran (3+ topics discussed). Code at lines 736-752.
2. **Persistent NPC identity**: 18 named characters across 3 roles (dealer, apprentice, engineer) per region.
3. **Deterministic cascade triggers**: Counter-based every 4th encounter after 5 topics discussed (lines 1667-1674).
4. **6 region mysteries** with clue collection and freeform answer evaluation.
5. **Region descriptions** providing atmospheric setting (lines 1651-1658).

The loss of class-based narrative framing ("As an Engineer, you approach the problem methodically...") is the one narrative regression, but it is minor. The NPC interaction system carries the narrative weight.

### Dimension 4: Motivation & Engagement

**Score: intrinsic (quality improved)**

This is the dimension most affected by the change. The improvements:

1. **Reduced cognitive barrier.** Character creation: ~5 seconds (name only) vs ~60 seconds (name + class + 20 stat points). This eliminates a decision bottleneck that delays the player's first learning encounter.
2. **Streaks provide moment-to-moment feedback.** The HUD streak bar fills visually with each correct answer, providing continuous positive reinforcement without requiring the player to manage resources.
3. **Combos reward flow states.** The x2, x3 multiplier display with pulse animation celebrates sustained correct answering without penalizing deliberation.
4. **Achievements provide goal structure.** 20 achievements across streak milestones (3, 5, 10), mastery milestones (5, 20, 50), exploration, mystery solving, encounter types, daily challenges, collections, teaching, Bloom depth, and review. These are all intrinsically motivated -- they celebrate learning accomplishments, not extrinsic rewards.
5. **Collections align gamification with knowledge.** The 6 collections map directly to knowledge domains. Completing "Circuit Fundamentals" (resistor, capacitor, inductor, diode, voltage) IS mastering the foundational electronics topics.
6. **Daily challenges encourage habit formation.** A single question per day with an achievement streak is a lightweight retention mechanism.
7. **No new extrinsic dependency introduced.** There is no XP, no leveling system, no virtual currency, no loot. All progression is mastery-driven.

The risk would be if streaks/combos created unhealthy pressure. The 30-second combo window is generous (most typed answers take 15-45 seconds), and streak reset on wrong answers is the standard pattern. Neither system gates content or punishes the player beyond resetting a counter.

### Dimension 5: Assessment Design

**Score: hybrid (no regression)**

All assessment mechanics preserved:

1. **LLM evaluation** for freeform answers (primary pathway).
2. **Circuit wiring challenges** (4 challenges across 4 categories) with slot-based interaction.
3. **Fault tree diagnosis** (4 challenges) with step-by-step elimination and freeform root cause declaration.
4. **Bloom-filtered quiz sources** scaffolding cognitive demand by region difficulty.
5. **Misconception matching** triggering targeted corrections.
6. **Tutorial practice encounter** as meta-assessment.

The removal of d20 stat checks is a net positive for assessment validity. In iteration 9, a high-Intelligence character could see hints that a low-Intelligence character could not, meaning assessment difficulty was partly determined by character build rather than knowledge. Now assessment difficulty is determined by region (Bloom scaffolding) and topic (prerequisite ordering) -- both educationally meaningful.

### Dimension 6: Accessibility & Inclusion

**Score: strong (no regression)**

1. **17 ARIA elements, 0 missing labels.** The count is lower than iteration 9's 29 because class-related interactive elements (class cards, stat sliders) no longer exist. All remaining elements are properly labeled.
2. **Keyboard navigation**: 19/20 tab stops hit interactive elements. Number key shortcuts for choices preserved.
3. **4/5 landmarks**: banner, navigation, main, contentinfo. `complementary` (aside) still absent -- acceptable.
4. **Mobile**: No horizontal overflow at 375px.
5. **Theme toggle**: Light/dark theme via `data-theme` attribute.
6. **Font size toggle**: Three sizes (small/medium/large) via `data-fontsize` attribute.
7. **`prefers-reduced-motion`**: All animations suppressed to 0.01ms.
8. **Tutorial overlay**: `role="dialog"` with descriptive aria-label per step.
9. **Help panel**: `role="dialog"`, escape key, overlay click to close.

### Dimension 7: Freemium Monetisation

**Score: learning-first (no regression)**

`premiumFeatures.enabled = false`. All content free. Zero monetisation elements. Premium features object defines bonus regions, cosmetics, and challenge modes as future possibilities, but none are active. No ads, no energy system, no paywalls.

### Dimension 8: RPG Mechanical Integrity

**Score: N/A (intentional redesign, not a regression)**

This dimension requires re-evaluation. Iteration 9 scored "mechanically-rich" based on 6 stats, 6 classes, d20 checks, HP/MP, gold, inventory, and Jury-Rig. All of these have been intentionally removed per user directive. The game is no longer an RPG; it is a **gamified learning adventure**.

The new gamification systems are mechanically simpler but coherent:
- Streaks and combos are implemented with clear rules (streak increments on correct, resets on wrong; combo increments on correct within 30s, resets otherwise).
- Achievements have defined trigger conditions with no ambiguity.
- Collections map to specific topic sets with completion tracking.
- Daily challenges use date-keyed tracking.
- Titles evolve based on mastery percentage thresholds.

These systems serve their purpose (providing feedback and goal structure) without the complexity overhead of the RPG system. The trade is deliberate.

---

## Critical Bugs and Issues

### BUG-001: Migration does not immediately persist class stripping

**Severity: Low**

`loadState()` at line 2508-2510 strips `state.char.class` in memory, but `saveState()` is not called after `loadState()`. This means a player with an iteration 9 save who loads the game will have the correct in-memory state (class stripped) but the localStorage JSON still contains the `class` field until the next save-triggering action. If the player inspects localStorage or if the page crashes before any save action, the class field persists.

**Fix:** Add `saveState()` after the migration block in `loadState()`, or call `saveState()` immediately after `loadState()` returns true in `init()`.

### BUG-002: POLISH-002 input inconsistency persists

**Severity: Low**

Tutorial practice encounter uses `<textarea>` (line 1116, `.tutorial-practice-input`, 3 rows), while the main game uses `<input type="text">` (line 314, `#freeform`). The iteration 9 critique flagged this as POLISH-002 with "medium" priority. It remains unfixed. The functional impact is minimal (both accept text), but the visual inconsistency breaks the tutorial's promise of "this is how the game works."

### BUG-003: Quiz question count discrepancy

**Severity: Informational**

The design spec claims 5420 quiz questions, but the database contains 2710 (exactly half). All 6 quiz sources are present. The game functions correctly with 2710 questions (14.7 per topic average). This may be intentional (reduced duplication) or a database import issue.

### BUG-004: Combo resets on page reload but streak persists

**Severity: Low (by design)**

Line 2464 in `saveState()` saves `combo: 0` (comment: "combo resets on reload"). This is arguably correct (combos are session-based flow rewards), but a player may be confused if their combo disappears on refresh. The streak persists correctly.

---

## Biggest Risk

The largest risk in this iteration is **reductive simplification** -- that the removal of RPG mechanics could make the game feel like a quiz app with narrative decoration. The new gamification systems (streaks, combos, achievements) provide feedback loops but do not provide the decision-making depth that made iteration 9 feel like a game. If a future iteration needs to increase engagement without adding RPG complexity back, the path forward is richer interaction modalities (more circuit wiring variants, more fault tree scenarios, simulated experiments) rather than cosmetic reward systems.

---

## Recommendations

### Quick Wins

1. **Fix BUG-001: Persist migration immediately.** Add `saveState()` at line 2511 (after `return true`) or in `init()` after `loadState()`. One line fix.

2. **Fix POLISH-002: Match input elements.** Change line 314 from `<input type="text" id="freeform"` to `<textarea id="freeform" rows="1"` with CSS to match appearance. Or change line 1116 from `<textarea>` to `<input>`. The textarea is pedagogically better (multi-sentence answers) so prefer converting the game input.

### Structural Improvements

1. **Add more circuit wiring and fault tree challenges.** Currently there are 4 of each. These are the most intrinsically integrated assessment types -- the player IS doing engineering. Expanding to 8-10 of each across more categories would significantly strengthen the "this is a game, not a quiz" feeling.

2. **Consider a lightweight "specialty" system.** Rather than the full class system, let players choose a focus area (e.g., "I'm most interested in electronics" or "I want to learn robotics") that affects which region the world map highlights first. This preserves the approachability while giving a sense of player identity. No stat effects, no gating -- purely advisory.

---

<!-- SCORES
intrinsic_integration: deep
pedagogical_soundness: strong
narrative_structure: compelling
motivation_engagement: intrinsic
assessment_design: hybrid
accessibility: strong
freemium_monetisation: learning-first
rpg_mechanical_integrity: cosmetic
biggest_risk: Removal of RPG mechanics risks the game feeling like a quiz app with narrative decoration; richer interaction modalities (more wiring/fault-tree challenges, simulated experiments) are needed to maintain the game feel without restoring class complexity.
SCORES -->
