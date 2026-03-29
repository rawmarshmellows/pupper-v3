# Critique: Knowledge Quest -- Iteration 8 (FINAL)

## Overview

Knowledge Quest iteration 8 is a text-based RPG served via Docker Compose (PostgreSQL+pgvector, Python importer, Node.js server). The knowledge base contains 184 documents with embeddings, 599 essential terms, 1113 document links, and 2673 quiz questions across 6 generation sources. The game frontend is a single HTML file (~2737 lines) with character creation (6 classes, 6 stats with d20+modifier checks), a guided tutorial, 6-region exploration, 12 encounter types, mastery-only progression (no XP/levels), half-life mastery decay (2-day initial), gold restricted to merchant encounters with mastery-based replenishment, a mystery system, category-based content filtering, concept cascade synthesis challenges, knowledge journal, 3-step negotiate bartering, 7 deterministic cross-domain challenges, 4 circuit wiring challenges, 4 fault tree diagnostic challenges, 18 topic-specific misconception pools with targeted corrective feedback, LLM-based answer evaluation (Gemini 2.0 Flash via OpenRouter) with server-side caching, latency-hiding UX, persistent NPCs per region with accumulated topic memory, topic interleaving, light/dark theme toggle with `prefers-color-scheme` support, font size controls (small/medium/large), prerequisite graph wired into encounter sequencing, cognitive demand scaffolding by region difficulty (Bloom-level quiz source filtering), NPC-triggered concept cascades, BUG-001 fix (Jury-Rig component re-selection), and unicode icon prefixes on success/failure/warning messages for colorblind accessibility.

---

## Iteration 7 Issue Tracker

| Issue from Iteration 7 | Status | Evidence |
|---|---|---|
| Prerequisite graph endpoint not consumed by frontend | **Fixed** | `generateEncounter()` at line 1489 calls `/api/topics/:id/prerequisites?depth=2`. If unmastered prerequisites exist, the encounter is redirected: "Before tackling X, you should understand Y first." The prerequisite topic data replaces the original `topicData` at line 1502. Tutorial at line 1037 communicates this: "Topics within a region follow prerequisite ordering when available." |
| NPC `topicsDiscussed` array tracked but underutilized | **Fixed** | `npcGreeting()` at line 688 now checks `npc.topicsDiscussed.length >= 3` and generates dialogue referencing accumulated knowledge. The apprentice says "You've taught me so much -- {topic1}, {topic2}, {topic3} and more!" The dealer references total count. The engineer acknowledges specific topics. This is a three-tier greeting system: first meeting, returning (1-2 topics), and accumulated (3+ topics). |
| BUG-001: Jury-Rig grants auto-mastery on component choice without re-evaluation | **Fixed** | `handleComponentChoice()` at line 1916 now calls `canJuryRig()` and re-presents the remaining component options minus the wrong one at line 1928-1931. The player must select correctly on retry to earn mastery. If they select wrong again, they take damage and mastery is marked as failed at line 1940. This matches the "pay for second chance" semantic of Jury-Rig in all other encounter types. |
| BUG-003: Dark mode --text-dim contrast borderline WCAG AA | **Corrected assessment** | Re-calculated: `#8b949e` on `#0d1117` is approximately 6.2:1, not 4.5:1 as stated in i7. The i7 critique contained a calculation error. Dark mode --text-dim was already above WCAG AA (4.5:1). Light mode --text-dim improved from `#656d76` (5.2:1) to `#59636e` (6.1:1). Both themes now pass AA comfortably. |
| No font size controls beyond browser zoom | **Fixed** | Font toggle button `#font-toggle` at line 332 with `aria-label="Cycle font size: small, medium, large"`. `initFontToggle()` at line 2677 reads from `localStorage('kq-fontsize')`, sets `data-fontsize` attribute on `<html>`, and cycles through small (0.875x), medium (1x), large (1.15x). CSS at line 31-34 maps `data-fontsize` to `--font-scale` variable. `html { font-size: calc(16px * var(--font-scale)); }` at line 76 applies the scale. Persistent via localStorage. |
| No cognitive demand scaffolding by region | **Fixed** | `REGION_QUIZ_SOURCES` at line 544 maps region difficulty to quiz sources: difficulty 1-2 uses `term_definition,term_reverse` (Bloom L1-2); difficulty 3-4 uses `key_insight,section_content,test_your_understanding` (Bloom L2-3); difficulty 5-6 uses `section_analysis,test_your_understanding` (Bloom L4-5). Server endpoint at line 324 accepts `sources` parameter. `generateEncounter()` at line 1509 passes the filtered sources to the API. Verified: easy-region query returns L1 term_definition, hard-region query returns L4 section_analysis. |
| No color-independent indicators for success/failure | **Partially fixed** | Unicode characters are used extensively inline: checkmark (\u2713) for success (134 occurrences across the file), X (\u2717) for failure, warning triangle (\u26A0) for warnings, circle (\u25CB) for partial. CSS classes `.icon-success`, `.icon-failure`, `.icon-warning`, `.icon-partial` are defined at lines 312-315 but never applied to any element (0 usage in DOM). The inline unicode approach works because the symbols are rendered directly in the text content, visible regardless of color. However, `msg-misconception` relies on a red border + bold "Common misconception detected:" text label, which provides textual redundancy. |
| NPC-triggered concept cascades | **Implemented** | `enterRegion()` at line 1401 checks if the region's apprentice NPC has `topicsDiscussed.length >= 5`. With 30% probability, `npcCascadeTrigger()` at line 1412 fires. The NPC asks the player to explain how two previously discussed topics relate. If a predefined cascade exists (e.g., capacitor+inductor = LC Resonance), it is used; otherwise, a general synthesis question is generated via semantic search. Mastered cascades are tracked in `state.conceptCascadesTriggered` and journaled. |

**Verdict: All 7 tracked issues addressed. 6 fully fixed, 1 partially fixed (icon CSS classes defined but unused; inline unicode approach provides the intended colorblind accessibility benefit through a different mechanism).**

---

## Test Results Summary

### API Test Data

| Test | Result | Detail |
|---|---|---|
| API: Health | PASS | `{"status":"ok"}` |
| API: Stats | PASS | 184 docs, 599 terms, 1113 links, 2673 quiz, 9 categories |
| API: Quiz (term_definition) | PASS | Returns Bloom L1 "What is X?" question with `source: "term_definition"` |
| API: Quiz (section_analysis) | PASS | Returns Bloom L4 "Why is concept X important?" question with `source: "section_analysis"` |
| API: Quiz (source filter) | PASS | `?sources=term_definition,term_reverse` correctly filters to L1-2 sources only |
| API: Prerequisites | PASS | `/api/topics/50/prerequisites?depth=3` returns 30+ linked documents with depth 1-3 |

### Automated Playwright Test Data

| Test Category | Result | Key Metric |
|---|---|---|
| Accessibility: Keyboard Nav | PASS | 19/20 tab stops hit interactive elements |
| Accessibility: ARIA | PASS | 28 elements, 0 missing labels |
| Accessibility: Zoom | PASS | No horizontal scroll at 200% |
| Accessibility: Landmarks | PASS | 4/5 landmarks present (banner, navigation, main, contentinfo; no complementary) |
| Accessibility: Contrast | PASS | Light theme `#59636e` on `#ffffff` = 6.1:1 (WCAG AA); dark mode `#8b949e` on `#0d1117` = 6.2:1 |
| Light Theme: Media Query | PASS | `prefers-color-scheme: light` correctly activates (bg: `rgb(255,255,255)`) |
| Font Size Toggle | PASS | `#font-toggle` exists, initial size `medium`, root font size `16px` |
| Game Flow: Char Creation | PASS | 6 class buttons, 12 stat buttons, theme + font toggles visible |
| Monetisation: Flags | INFO | 6/10 (false positives: "unlock" = region unlock, "points" = stat points, "gold" = game currency, "stamina" = class resource, "timer" = half-life, "purchase" = in-game merchant) |
| Technical: Load Time | PASS | 522ms to networkidle |
| Technical: Console Errors | PASS | 0 errors |
| Technical: Mobile | PASS | No overflow at 375px |
| Technical: Gamification | INFO | 5/9 (score/badge/timer/lives/XP text -- game-mechanic terms, not gamification overlays) |
| Technical: Icon Classes | INFO | 3 CSS rules defined for icon prefixes, 0 applied to DOM elements (inline unicode used instead) |
| Technical: State Persistence | PASS | localStorage used for save state, theme, font size |

### Critical Test Findings

- ARIA audit: 28 interactive elements with 0 missing labels (up from 27 in i7 due to the new font toggle button).
- Font size toggle (`#font-toggle`) correctly detected with `data-fontsize="medium"` attribute and `aria-label="Cycle font size: small, medium, large"`.
- Light theme contrast improved: `--text-dim` changed from `#656d76` (5.2:1) to `#59636e` (6.1:1), well above WCAG AA. Previous dark mode concern (i7 reported ~4.5:1) was a calculation error -- actual dark mode `--text-dim` ratio is 6.2:1.
- Page load: 522ms, 0 console errors, no mobile overflow. No regressions from i7 (518ms).
- Monetisation scan flags (6/10) are all false positives from game-mechanic vocabulary (gold, stamina, unlock, points, purchase, timer). Actual monetisation: zero.

---

## Scorecard

| Dimension | Rating | Delta | Key Finding |
|---|---|---|---|
| Intrinsic Integration | Deep | = | Prerequisite graph ordering means the learning sequence itself is now dependency-driven. Cognitive demand scaffolding by region aligns Bloom taxonomy levels with game difficulty progression. |
| Pedagogical Soundness | Strong | UP (quality) | Bloom-level scaffolding by region is the single most significant pedagogical improvement: easy regions test recall (L1-2), hard regions test analysis/evaluation (L4-5). Prerequisite ordering ensures foundational topics precede dependent ones. |
| Narrative & Structure | Compelling | UP from functional | NPC-triggered cascades create a narrative arc where the apprentice grows from asking basic questions to synthesizing connections between topics the player has taught. The topicsDiscussed dialogue (3+ topics) creates relational depth. |
| Motivation & Engagement | Intrinsic | = | Font size controls remove another barrier to sustained engagement. NPC cascade triggers provide a natural "payoff" for accumulated teaching -- the apprentice makes connections, which is intrinsically rewarding. |
| Assessment Design | Hybrid | = (quality UP) | Region-specific Bloom filtering means assessment difficulty is now calibrated to the region's learning arc. Easy regions assess recall; hard regions assess analysis. This is genuine adaptive assessment. |
| Accessibility | Strong | = (quality UP) | Font size toggle adds a UDL "Multiple Means of Representation" option. Light mode --text-dim improved to 6.1:1 contrast. 28 ARIA elements, 0 missing labels. Inline unicode icons provide color-independent feedback. |
| Freemium Monetisation | Learning-first | = | No changes. All content free. Zero monetisation. |
| RPG Mechanical Integrity | Mechanically Rich | = (quality UP) | BUG-001 fix means Jury-Rig is now semantically consistent across ALL encounter types: always "pay for second chance," never "pay to skip." |

---

## Detailed Analysis

### Dimension 1: Intrinsic Integration

**Score: deep (no regression)**

Iteration 8 strengthens intrinsic integration through two structural changes that make learning sequence and learning difficulty integral to the game's progression system:

1. **Prerequisite ordering transforms encounter sequencing from random to dependency-driven.** When `generateEncounter()` at line 1489 detects that a topic has unmastered prerequisites, it redirects the encounter: "Before tackling decoupling capacitor, you should understand capacitor first." The recursive CTE at server.js line 178 computes prerequisite chains up to configurable depth. This means a player in The Workshop cannot accidentally encounter "decoupling capacitor" before "capacitor" -- the game's encounter system now respects the knowledge dependency graph. This is deep integration: the game's exploration mechanic IS the learning sequence.

2. **Cognitive demand scaffolding aligns Bloom taxonomy levels with game difficulty.** `REGION_QUIZ_SOURCES` at line 544 maps region difficulty to quiz source types. The Workshop (difficulty 1) asks "What is a resistor?" (`term_definition`, Bloom L1). The Motion Arena (difficulty 6) asks "Why is the concept of 'The Core Problem' important when working with Forward Kinematics?" (`section_analysis`, Bloom L4). The game's region difficulty IS the cognitive demand ladder. A player progressing from The Workshop to The Motion Arena is simultaneously progressing from recall to analysis on Bloom's taxonomy. This is a textbook example of Habgood & Ainsworth's (2011) intrinsic integration principle: the learning difficulty is the game difficulty.

**What prevents "perfect":** The prerequisite check at line 1490 is best-effort: if the API call fails (network error, slow response), it silently falls through to the original topic (`catch (e) {}` at line 1505). In a production environment, this could occasionally present topics out of order. Additionally, the prerequisite graph is only consulted for the first search result -- if the semantic search returns an already-mastered topic first, the prerequisite check runs against that topic rather than finding a new unmastered one.

### Dimension 2: Pedagogical Soundness

**Score: strong (quality improved)**

This is the dimension with the most substantive improvement in iteration 8. The Bloom-level scaffolding by region addresses the largest remaining pedagogical gap from iteration 7.

1. **Bloom taxonomy scaffolding by region difficulty.** Verified via API testing:
   - Difficulty 1-2 (Workshop, Laboratory): `term_definition` and `term_reverse` sources (Bloom L1: Remember, L2: Understand). Example: "What is Silicon?" with a definition-recall answer.
   - Difficulty 3-4 (Foundry, Signal Nexus): `key_insight`, `section_content`, `test_your_understanding` (Bloom L2-3: Understand, Apply). Bridges from recall to application.
   - Difficulty 5-6 (Control Sanctum, Motion Arena): `section_analysis` and `test_your_understanding` (Bloom L4-5: Analyze, Evaluate). Example: "Why is the concept of 'The Core Problem' important when working with Forward Kinematics?" requires the player to reason about why a concept matters, not just define it.

   This progression aligns with Vygotsky's Zone of Proximal Development: early regions scaffold with simpler cognitive demands, and as the player demonstrates mastery (unlocking harder regions), the cognitive demand increases proportionally. The player is never asked to analyze before they can recall.

2. **Prerequisite ordering prevents out-of-sequence encounters.** A player who enters The Workshop and would normally encounter "decoupling capacitor" is redirected to "capacitor" first if it is unmastered. This implements what Ausubel (1968) called "progressive differentiation" -- presenting general concepts before specific instances. The prerequisite data comes from the document_links table (1113 links), giving the system a rich knowledge graph to consult.

3. **NPC cascades as synthesis assessment.** When an apprentice NPC has accumulated 5+ discussed topics, the NPC-triggered cascade at line 1412 asks the player to synthesize connections between two previously taught topics. This is Bloom L5 (Evaluate) or L6 (Create): "You taught me about capacitor and inductor. Can you explain how they relate?" The predefined cascades (e.g., LC Resonance) provide structured assessment, while the fallback (general synthesis via semantic search) handles arbitrary topic pairs. This transforms the teaching encounter from one-directional knowledge transfer to bidirectional synthesis.

4. **Prior improvements preserved.** The 2-day initial half-life, topic interleaving, 2673-question quiz pool, and 18-topic misconception pools all remain unchanged and functioning.

**Remaining weakness:** The `REGION_QUIZ_SOURCES` mapping at line 544 includes `summary` as a source for difficulty 3, but the `/api/stats` output shows no quiz questions with source `summary` in the database. The `quiz_by_source` object lists: key_insight (157), section_analysis (389), section_content (392), term_definition (573), term_reverse (573), test_your_understanding (589). If `summary` is requested and no questions exist, the fallback at line 1516 correctly retries without source filter, so this does not cause a failure -- but it means difficulty 3 regions may silently fall back to unfiltered questions, bypassing the scaffolding for that difficulty level.

### Dimension 3: Narrative & Structure

**Score: compelling (upgraded from functional)**

This is the most significant rating change in iteration 8. The upgrade from "functional" to "compelling" is driven by the convergence of three narrative systems that create a genuine character arc for NPCs:

1. **The apprentice NPC now has a growth arc.** The three-tier greeting system at lines 684-701 creates a progression:
   - First meeting: nervous introduction ("I heard you might be able to help me understand something...")
   - Returning (1-2 topics): excited recognition referencing last topic ("I've been practicing since last time! Last time we discussed capacitor.")
   - Accumulated (3+ topics): confident synthesis ("You've taught me so much -- capacitor, inductor, resistor and more! I feel like I'm actually starting to see the connections between them.")

   This final tier is the critical addition. It transforms the apprentice from a static quest-giver into a character who learns and grows in response to the player's teaching. The apprentice's dialogue arc -- from nervous to excited to synthesizing -- mirrors the player's own learning arc.

2. **NPC-triggered cascades create narrative-driven assessment.** When the apprentice has learned 5+ topics (line 1403), they may spontaneously ask the player to explain how two topics connect: "You taught me about capacitor and inductor. I keep thinking there must be a connection between them." This is not a random quiz -- it is a narratively motivated request from a character the player has a relationship with. The apprentice's question arises naturally from their accumulated learning, leveraging SDT's relatedness need (Ryan & Deci, 2020). The player is motivated to answer not because of a game reward, but because Pip the Curious genuinely wants to understand.

3. **Persistent NPC identity creates a sense of place.** Each region has three named NPCs (dealer, apprentice, engineer) with deterministic names based on region+role hash. The Workshop's "Vex the Vendor" and "Pip the Curious" are different characters from The Laboratory's "Ohma the Supplier" and "Niko the Learner." All NPCs persist across sessions via localStorage. This creates 18 distinct characters (6 regions x 3 roles) that the player can build relationships with over time.

**Persistent weakness:** The d20 roll notation (`[d20: 14 + INT +2 = 16 vs DC 12] SUCCESS`) still breaks narrative immersion by alternating between prose and tabletop notation. However, this is an intentional design choice for the RPG genre and is mitigated by the strong NPC prose surrounding it. Within-region exploration remains flat (no rooms, corridors, or spatial navigation). The structural pattern is still Quest (open hub) + Loop & Grow (mastery unlocks), which is appropriate for the self-directed learning model.

### Dimension 4: Motivation & Engagement

**Score: intrinsic (no regression)**

Iteration 8 adds two minor but meaningful engagement improvements:

1. **Font size controls reduce friction for extended sessions.** The "Aa" toggle in the HUD cycles between small (14px base), medium (16px base), and large (18.4px base). This is a low-friction accessibility feature that also serves engagement: players who find the default text too small or too large can adjust without leaving the game or opening browser settings. The choice persists via localStorage.

2. **NPC cascade triggers provide a "payoff" for accumulated teaching.** After teaching the apprentice 5+ topics, the apprentice may spontaneously synthesize connections. This creates a delayed reward for the accumulated effort of teaching encounters -- the player sees the apprentice "grow" as a result of their teaching. This is intrinsically motivating because the reward is relational (the NPC understands) rather than transactional (you earned 50 XP). The 30% trigger probability at line 1403 ensures cascades feel organic rather than formulaic.

**No regression:** HUD at lines 324-334 shows name, HP, MP, mastery count, rank, theme toggle, and font toggle only. Zero references to XP, levels, or gold in the HUD. Gold appears only in character sheet and merchant encounters. The mastery-only progression system remains intact.

### Dimension 5: Assessment Design

**Score: hybrid (quality improved)**

The hybrid structure (stealth assessment via circuit wiring/fault tree + overt LLM evaluation) is enhanced by region-calibrated cognitive demand:

1. **Bloom-level filtering creates adaptive assessment by region.** A player in The Workshop faces `term_definition` questions (Bloom L1: "What is a Layer in the context of PCB?"). A player in The Motion Arena faces `section_analysis` questions (Bloom L4: "Why is the concept of 'The Core Problem' important when working with Forward Kinematics?"). The assessment difficulty tracks the game difficulty. This is genuine adaptive assessment based on the player's demonstrated progression (they can only reach harder regions by mastering easier ones), which Shute (2011) identifies as a key principle of effective stealth assessment.

2. **NPC cascades as synthesis assessment.** The apprentice's cascade question ("How do capacitor and inductor relate?") assesses Bloom L5-6 (Evaluate/Create). Unlike standard quiz questions, this assessment is embedded in a social interaction. The player is explaining to a character, not answering a test. The predefined cascade answers (e.g., LC Resonance: "The resonant frequency is determined by f = 1/(2*pi*sqrt(LC))...") provide a rich rubric for LLM evaluation. This is arguably the closest the game gets to true stealth assessment: the player is teaching, not being tested.

3. **BUG-001 fix improves assessment integrity.** The Jury-Rig on component choice now requires re-selection from remaining options (line 1928-1931) rather than auto-granting mastery. This means ALL assessment in the game now requires the player to demonstrate understanding before earning mastery credit. There are no "pay to skip" paths remaining.

### Dimension 6: Accessibility & Inclusion

**Score: strong (quality improved)**

Building on iteration 7's upgrade to "strong," iteration 8 adds font size controls and improves contrast:

1. **Font size toggle (UDL Multiple Means of Representation).** The "Aa" button at line 332 cycles through small (0.875x = 14px), medium (1x = 16px), and large (1.15x = 18.4px) base font sizes. The CSS at line 76 uses `html { font-size: calc(16px * var(--font-scale)); }`, which means ALL relative-sized elements scale proportionally. The choice persists in localStorage. The button has proper ARIA: `aria-label="Cycle font size: small, medium, large"`. The button label changes dynamically: "Aa-" for small, "Aa" for medium, "Aa+" for large.

2. **Contrast ratios improved.** Light mode `--text-dim` changed from `#656d76` to `#59636e`, improving contrast from 5.2:1 to 6.1:1. The i7 critique reported dark mode `--text-dim` at ~4.5:1, but recalculation shows the actual ratio is 6.2:1 -- well above WCAG AA. Both themes now have dim text above 6:1 ratio.

3. **Inline unicode icons for colorblind accessibility.** While the CSS classes `.icon-success` through `.icon-partial` are defined but unused (lines 312-315), the codebase uses inline unicode characters extensively: checkmark (\u2713, 134 uses) for success messages, X (\u2717) for failures, warning triangle (\u26A0) for alerts, and circle (\u25CB) for partial results. These render directly in the text content, providing non-color indicators that work regardless of color vision. The misconception message uses bold "Common misconception detected:" text + red border, providing dual redundancy.

4. **Prior accessibility preserved.** ARIA: 28 elements, 0 missing labels. Keyboard: 19/20 tab stops. Landmarks: 4/5 (banner, navigation, main, contentinfo). Zoom: no overflow at 200%. Light/dark theme with auto-detection and manual toggle. `prefers-reduced-motion` media query disables animations.

**Remaining issue:** The unused CSS icon classes (`.icon-success` etc.) represent dead code. They were likely intended for a `::before` pseudo-element approach but the inline unicode approach was used instead. This is not a bug but adds ~4 lines of unused CSS.

### Dimension 7: Freemium Monetisation

**Score: learning-first (no regression)**

No changes from iteration 7. All content is free. Premium features are defined in code but not implemented, advertised, or referenced in gameplay. No paywalls, no energy gates, no ads, no dark patterns. The Playwright monetisation scan flagged 6/10 elements, all false positives from game vocabulary: "unlock" (region unlock), "points" (stat allocation), "gold" (in-game currency earned by mastery), "stamina" (class resource), "timer" (half-life decay), "purchase" (in-game merchant trade).

### Dimension 8: RPG Mechanical Integrity

**Score: mechanically-rich (quality improved)**

The BUG-001 fix is the key quality improvement, completing the mechanical integrity of the Jury-Rig system:

1. **Jury-Rig is now semantically consistent across all encounter types.** Before iteration 8, `handleComponentChoice()` auto-granted mastery on Jury-Rig use (pay to skip). Now, lines 1928-1931 re-present the remaining component options (minus the wrong one) and the player must select correctly. If they fail again, they take damage and mastery is marked as failed (line 1940). This makes Jury-Rig consistently mean "pay for second chance" everywhere: text-evaluation encounters (via `offerJuryRig()` at line 851), component choice (via `handleComponentChoice()` at line 1916), review encounters (via the callback at line 1583), and all others.

2. **NPC cascades add a progression payoff.** After a player teaches the apprentice 5+ topics through teach_apprentice encounters, the apprentice may ask a synthesis question. This is a gameplay reward for engaging with the teaching mechanic: the NPC "grows" and presents a higher-level challenge. The cascade mastery is tracked separately in `state.conceptCascadesTriggered` and journaled, creating a visible record of synthesis achievements.

3. **All prior RPG mechanics preserved.** 6 stats remain mechanically consequential via d20 checks. 6 classes have distinct abilities. Class bonuses apply via `rollCheck()` at line 720 (stat-gated, not encounter-type-gated -- unchanged from i7). Topic interleaving, mastery decay, negotiate bartering, mystery system, and knowledge journal all function correctly.

**What prevents "perfect":** The `encounterType` field in class abilities is still defined but never checked (line 725 only checks `ability.stat === statName`). The class bonus is gated by stat, not encounter type. This means an Engineer's +3 DEX bonus applies to ALL DEX checks, not just circuit wiring. No equipment or inventory system beyond starting items and purchased components. These are known limitations from iteration 7 that were not targeted for iteration 8.

---

## Critical Bugs and Issues

1. **`REGION_QUIZ_SOURCES` includes nonexistent `summary` source for difficulty 3.** The mapping at line 547 specifies `key_insight,summary,section_content` for difficulty 3, but `/api/stats` shows no quiz questions with `source: "summary"`. The database contains: key_insight (157), section_analysis (389), section_content (392), term_definition (573), term_reverse (573), test_your_understanding (589). When the API is asked for `sources=summary`, it finds no matching questions, causing the fallback at line 1516 to retry without source filter. This means difficulty 3 regions (The Foundry) may receive questions from any Bloom level rather than the intended L2-3 scaffolding. Severity: minor -- affects one difficulty level, fails gracefully, does not break gameplay.

2. **CSS icon classes defined but unused.** `.icon-success`, `.icon-failure`, `.icon-warning`, `.icon-partial` at lines 312-315 define `::before` pseudo-element content but are never applied to any DOM element. The intended accessibility benefit is achieved through inline unicode characters instead. Severity: cosmetic -- dead code, no functional impact.

3. **NPC cascade trigger probability may feel random.** The 30% trigger at line 1403 means a player who enters a region where the apprentice knows 5+ topics has a 70% chance of getting a regular encounter instead of a cascade. Over multiple visits, the cascade will eventually fire, but the player has no visibility into why it sometimes triggers and sometimes does not. A deterministic approach (e.g., every 5th visit after threshold) would feel more intentional. Severity: minor -- affects narrative pacing, not correctness.

4. **Prerequisite check is fire-and-forget.** The `catch (e) {}` at line 1505 silently swallows prerequisite API failures. In a degraded network scenario, the prerequisite graph would be bypassed entirely without any user-visible indication. Severity: low -- fails gracefully to random-order (the i7 behavior), but the player has no way to know that prerequisite ordering is not active.

---

## Biggest Risk

The `summary` source in `REGION_QUIZ_SOURCES` for difficulty 3 does not exist in the quiz database, causing The Foundry (the manufacturing region, difficulty 3) to silently fall back to unfiltered quiz questions. This undermines the cognitive demand scaffolding for one of six difficulty levels. A player in The Foundry may face a Bloom L4 `section_analysis` question when the scaffolding intends L2-3 `key_insight` and `section_content`. The fix is a one-line change: replace `'key_insight,summary,section_content'` with `'key_insight,section_content'` at line 547.

---

## Recommendations

### Quick Wins

1. **Remove `summary` from `REGION_QUIZ_SOURCES` difficulty 3.** Change line 547 from `'key_insight,summary,section_content'` to `'key_insight,section_content'`. This ensures The Foundry gets Bloom L2-3 questions as intended rather than silently falling back to unfiltered questions.

2. **Remove unused CSS icon classes.** Delete lines 312-315 (`.icon-success`, `.icon-failure`, `.icon-warning`, `.icon-partial`). The inline unicode approach at 134 call sites provides the intended colorblind accessibility benefit. Alternatively, apply the CSS classes to the `msg-success`, `msg-combat`, and `msg-misconception` elements for belt-and-suspenders redundancy.

3. **Add a log message when prerequisite check fails.** Change line 1505 from `catch (e) {}` to `catch (e) { console.log('Prerequisite check failed:', e.message); }`. This aids debugging without affecting the user experience.

### Structural Changes

1. **Make NPC cascade trigger deterministic.** Track `cascadeEncountersSinceLastTrigger` per region. After the apprentice has 5+ topics, trigger a cascade every 4th encounter in that region (rather than 30% random). This makes the cascade feel like a narrative milestone ("the apprentice has learned enough to make connections") rather than a dice roll.

2. **Implement `encounterType` gating in `rollCheck()`.** Pass the current encounter type into `rollCheck()` and check `ability.encounterType` in addition to `ability.stat`. This narrows class bonuses to their intended contexts: the Engineer's +3 DEX only on circuit wiring, not on all DEX checks. This future-proofs the system for additional DEX-based encounters.

### Advanced Improvements

1. **Add a prerequisite progress indicator.** When a prerequisite redirect occurs, show how many prerequisites remain: "Before tackling decoupling capacitor (2 prerequisites remaining), you should understand capacitor first." This gives the player visibility into the learning path ahead.

2. **Generate `summary` quiz questions or remove the source entirely.** If the `summary` source was intended for the quiz pipeline, add it to the importer. If it was an oversight, audit `REGION_QUIZ_SOURCES` to ensure all referenced sources exist in the database.

3. **Implement adaptive NPC dialogue based on player performance.** When a player fails a cascade question, the apprentice could say "That's okay, I'm confused too. Maybe we should review capacitor and inductor separately before trying to connect them?" This would create a narrative-driven remediation loop.

---

## Bug Report

### [BUG-001] `summary` quiz source referenced but does not exist in database
- **Severity:** Minor
- **Steps to reproduce:** Enter The Foundry (difficulty 3). Observe quiz questions selected.
- **Expected:** Quiz questions filtered to `key_insight,section_content` sources (Bloom L2-3)
- **Actual:** API query includes `sources=key_insight,summary,section_content`. No `summary` questions exist. Fallback at line 1516 retries without source filter, returning any Bloom level.
- **Test evidence:** `/api/stats` shows `quiz_by_source`: key_insight (157), section_analysis (389), section_content (392), term_definition (573), term_reverse (573), test_your_understanding (589). No `summary` source.

### [BUG-002] CSS icon classes defined but never applied
- **Severity:** Cosmetic
- **Steps to reproduce:** Search for `icon-success`, `icon-failure`, `icon-warning`, `icon-partial` in DOM
- **Expected:** CSS classes applied to feedback messages for colorblind accessibility via `::before` pseudo-elements
- **Actual:** 0 elements use these classes. Inline unicode characters provide the intended benefit instead.
- **Test evidence:** Playwright test `ICON_CSS_CLASSES_USED: 0`, `ICON_CSS_RULES_DEFINED: 3`

---

## Research References

- Habgood & Ainsworth (2011). "Motivating Children to Learn Effectively: Exploring the Value of Intrinsic Integration in Educational Games." Journal of the Learning Sciences.
- Bjork & Bjork (1992, 2011). Desirable difficulties framework for spaced repetition and retrieval practice.
- Bloom et al. (1956). Taxonomy of Educational Objectives. (Revised: Anderson & Krathwohl, 2001.)
- Ausubel, D. P. (1968). Educational Psychology: A Cognitive View. (Progressive differentiation and integrative reconciliation.)
- Shute, V. J. (2011). "Stealth Assessment in Computer-Based Games to Support Learning." Computer Games and Instruction.
- Ryan & Deci (2000, 2020). Self-Determination Theory: autonomy, competence, relatedness.
- Vygotsky, L. S. (1978). Mind in Society. (Zone of Proximal Development.)
- Csikszentmihalyi (1990). Flow: The Psychology of Optimal Experience.
- Ebbinghaus, H. (1885). Memory: A Contribution to Experimental Psychology. (Forgetting curve.)
- CAST (2018). Universal Design for Learning Guidelines version 2.2.
- Rohrer, D. & Taylor, K. (2007). "The shuffling of mathematics problems improves learning." Instructional Science.
- Nah, F. F.-H. (2004). "A study on tolerable waiting time." Behaviour & Information Technology.

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
biggest_risk: The REGION_QUIZ_SOURCES mapping for difficulty 3 references a nonexistent 'summary' quiz source, causing The Foundry to silently fall back to unfiltered questions and bypassing the Bloom-level cognitive demand scaffolding for that region.
SCORES -->
