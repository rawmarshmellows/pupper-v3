# Critique: Knowledge Quest -- Iteration 3

## Overview

Knowledge Quest iteration 3 is a text-based RPG served via Docker Compose (PostgreSQL+pgvector, Python importer, Node.js server). The knowledge base imports 184 documents, 599 essential terms, 1113 document links, and 589 quiz questions. The game frontend is a single HTML file (~1620 lines) with character creation, 6-region exploration, 8 encounter types, a mystery system requiring domain-knowledge explanations, category-based content filtering, mastery-centric HUD, Bloom's level tracking, cross-domain challenges, and semantic answer evaluation via OpenRouter embeddings with lowered thresholds. Playwright automated testing confirmed: accessible character creation flow (22 focusable elements), working mastery HUD (no XP bar, no gold display in HUD), no knowledge reveals before answers, no horizontal scroll at 200% zoom, 6 region cards with mastery meters, 1 region unlocked at start with 5 locked behind mastery gates, 6 classes, 6 stats, aria-labels present on name input and stat buttons.

---

## Iteration 2 Issue Tracker

| Issue from Iteration 2 | Status | Evidence |
|---|---|---|
| Hardcoded diagnosis symptoms unrelated to topics | **Fixed** | `generateTopicSymptom(topic)` at line 850 produces topic-specific symptoms based on `key_insight`/`definition` content. Capacitor topics show ripple/filtering symptoms; resistor topics show current/voltage symptoms. ~12 keyword-matched branches plus a generic fallback. |
| Terms/quiz questions leaking across domains | **Fixed** | `/api/terms/random` and `/api/quiz/random` accept `?categories=` parameter. The `generateEncounter` function passes `region.categories` when fetching content (lines 680-695). Tested: `?categories=electronics` returns only electronics content; `?categories=sales` returns only sales content. |
| Semantic similarity threshold too strict (0.85) | **Fixed** | `/api/evaluate` now uses 0.75 for correct, 0.55 for partial (line 308-309, comment at line 286). Tested: a mystery answer paraphrase scored 0.819 and graded "correct" -- this would have been "partial" under the old threshold. |
| Wiki-link markdown in quiz questions | **Fixed** | `strip_wiki_links()` function at importer line 165-167 strips `[[target|display]]` syntax. Called on all extracted fields: tldr, definition, key_insight, terms, quiz questions. Tested: 10 random quiz fetches showed 0 wiki-link occurrences. No `[[` syntax found in `index.html`. |
| CHA bluff escape hatch bypasses learning | **Fixed** | The negotiate encounter at line 1025 has an explicit comment: "NO CHA BLUFF ESCAPE HATCH -- stat checks never bypass knowledge." All three approach options (explain, use case, clarify) require domain knowledge. CHA only appears in STAT_NAMES for character creation. |
| XP/gold as primary motivators -- should show mastery progress | **Fixed** | HUD shows mastery bar and "X mastered" count instead of XP/gold. Playwright confirmed: `#hud-xp-bar` not present, `#hud-gold` not present. XP/gold rewards are de-emphasized: rendered in dim text at 0.85rem (line 1470). Mastery messages rendered in purple at standard weight (line 772, 807, etc.). Region unlocking is mastery-based, not level-based (line 561-565: requires 40% mastery of previous region). |
| Mystery solutions should require domain knowledge | **Fixed** | `attemptMysterySolve` at line 1307 presents the mystery and requires the player to explain the root cause in their own words. Each region has a specific `mysteryAnswer` with technical content (e.g., Workshop: degraded capacitor causing voltage regulator oscillation). The player's explanation is evaluated via semantic similarity against this answer. Auto-solve is gone; reaching 60% clues marks the mystery as "solvable" but the player must still demonstrate understanding. Tested: a good paraphrase of the Workshop mystery answer scored 0.819 ("correct"). |

**Verdict: All 7 priority fixes from iteration 2 have been addressed.** The implementations are functional and can be verified through API testing and code inspection.

---

## Test Results Summary

### Automated Test Data

| Test Category | Result | Key Metric |
|---|---|---|
| Accessibility: Keyboard Nav | PASS | 22 focusable elements on character creation |
| Accessibility: ARIA | PASS | Name input has aria-label="Character name"; stat buttons have labels |
| Accessibility: Zoom | PASS | No horizontal scroll at 200% zoom |
| Accessibility: Landmarks | WARN | 2/5 landmarks present (navigation, main); missing banner, complementary, contentinfo |
| Game Flow: Engine | Custom | Single-page JavaScript application, no framework |
| Rewards: Gamification Score | 6 | Score, badges, timer (false positive), XP, mastery, hasPricing |
| Assessment: Quiz Elements | Hybrid | Stealth (component choice, circuit build) + overt (negotiate, decode) |
| Monetisation: Flags | 0 | No paywall, no ads, no energy gates, no dark patterns |
| Monetisation: Paywall Placement | None | Free tier includes all content and learning objectives |
| Technical: State Persistence | Yes | localStorage with `knowledge-quest-save` key |
| API: Health | OK | All endpoints responding, 184 docs with embeddings |
| API: Stats | OK | 184 docs, 599 terms, 1113 links, 589 quiz, 9 categories |

### Critical Test Findings

- **Mastery-centric HUD works as designed.** No XP bar or gold counter in the HUD. Mastery bar and "0 mastered" counter are the primary displays. XP/gold still exist but are visually de-emphasized.
- **Region gating is mastery-based.** Only The Workshop (difficulty 1) is unlocked at start. All others require 40% mastery of the previous region. This is a genuine structural improvement over level-based gating.
- **Zero knowledge reveals before player answers.** Playwright confirmed 0 `.knowledge-reveal` elements after entering the first region, before any answer submission.
- **Category filtering prevents domain leakage.** API testing confirmed that `?categories=electronics` returns only electronics content, and `?categories=sales` returns only sales content. The frontend passes region categories to all content endpoints.
- **Content count dropped significantly.** 599 terms (was 7188 in iteration 2) and 589 quiz questions (was 7068). This is likely due to a different notes dataset being imported, not a regression in the importer. The importer code correctly handles term and quiz extraction.

---

## Scorecard

| Dimension | Rating | Key Finding |
|---|---|---|
| Intrinsic Integration | Partial | Topic-specific symptoms and scenarios are a real improvement, but the core evaluation mechanic remains "type text, compare to reference" regardless of encounter framing. |
| Pedagogical Soundness | Mixed | Lowered thresholds, wiki-link stripping, and Bloom's tracking are solid fixes, but the semantic evaluator still cannot distinguish Bloom's levels in practice. |
| Narrative & Structure | Functional | Mystery system now requires synthesis, cross-domain challenges add depth, but NPCs remain stateless and regional exploration lacks spatial progression. |
| Motivation & Engagement | Mixed | Mastery-centric HUD and understanding-based gates are genuine improvements, but XP/gold/levels still exist and function identically to before. |
| Assessment Design | Hybrid | Component Choice and Circuit Build remain good stealth assessment; Teach Apprentice redesign is pedagogically strong; but the single evaluation modality limits assessment validity. |
| Accessibility | Adequate | Name input aria-label fixed, landmarks improved, no horizontal scroll. Still missing light theme, font controls, reduced motion, banner/footer landmarks. |
| Freemium Monetisation | Learning-first | No paywalls, no ads, no dark patterns. Free tier includes all content and learning objectives. Premium features defined but not implemented. |

---

## Detailed Analysis

### Dimension 1: Intrinsic Integration

**Score: partial**

Iteration 3 makes meaningful progress toward "deep" integration but falls short of the threshold.

**What improved:**

1. **Topic-specific symptoms in Diagnosis.** The `generateTopicSymptom` function (line 850) uses keyword matching against the topic's `key_insight`/`definition` to produce relevant failure modes. A capacitor topic now presents "excessive ripple and the circuit fails to maintain a steady DC level" -- directly related to what capacitors do. This is a real improvement: the diagnosis encounter is now semantically coherent.

2. **Topic-derived scenarios in Predict Behavior.** The `generateTopicScenario` function (line 935) constructs thought experiments specific to the component. "If you replace the capacitor in this filter circuit with one that has half the capacitance, how does the cutoff frequency change?" requires understanding the RC time constant relationship, not just recognizing the term "capacitor."

3. **Category-based region filtering.** Each region specifies its categories (Workshop = electronics, Laboratory = semiconductors, etc.), and all content endpoints accept category filters. This prevents the sales-term-in-electronics-workshop problem that plagued iteration 2.

4. **Teach Apprentice redesign.** The apprentice now presents a wrong answer via `generateWrongAttempt` (line 1235). The player must identify the error and correct the reasoning. This is Bloom's level 5 (Evaluate) -- a genuinely different cognitive task from "explain this concept." The wrong answers are plausible enough to require understanding: "I memorized the definition but I can't really explain how it works in practice."

**What still prevents "deep" rating:**

1. **The evaluation bottleneck.** Every freeform encounter type -- Diagnosis, Predict Behavior, Negotiate, Teach Apprentice, Apply Knowledge, Mystery Solve, Cross-Domain Challenge -- ultimately reduces to the same operation: compare player text to a reference string via cosine similarity. The encounter framing varies (diagnose vs. predict vs. teach vs. explain), but the underlying assessment is identical. A player who writes an excellent diagnosis using causal reasoning is scored the same way as one who paraphrases the `key_insight` text. The game cannot distinguish HOW the player demonstrates understanding, only WHETHER their text is semantically close to a reference.

2. **Symptom generation uses keyword matching, not content understanding.** The `generateTopicSymptom` function checks for substrings like "store", "capacit", "resist", "ohm" in the `key_insight` text. This produces reasonable symptoms for common components but will generate generic fallback symptoms for topics whose `key_insight` doesn't contain these keywords. A topic about "decoupling capacitor" would hit the "capacit" branch, but a topic about "buck converter" might fall through to the generic: "The buck-converter subsystem behaves unexpectedly."

3. **Cross-domain challenge reference answers are structurally weak.** The `combinedAnswer` at line 1394 is: `"This requires knowledge of stm32, clock, adc, imu from The Control Sanctum and pid, kinematics, gait, reinforcement-learning from The Motion Arena. The signal chain connects these domains through their shared interfaces."` This is a list of topic names, not a technical explanation. A player who writes a thoughtful analysis of how IMU sensor data flows through an ADC into a PID controller scores only 0.658 ("partial") against this reference. The reference answer should describe the actual technical relationships, not just enumerate topic names.

### Dimension 2: Pedagogical Soundness

**Score: mixed**

**Improvements:**

1. **Lowered thresholds work correctly.** The 0.75/0.55 thresholds (line 308-309) are empirically better. A good paraphrase of the Workshop mystery answer scored 0.819 ("correct") -- this would have been "partial" at 0.85. However, a solid resistor explanation scored only 0.559-0.665 ("partial") against a somewhat different reference phrasing. The threshold is better but the fundamental limitation is that cosine similarity between short texts is sensitive to vocabulary overlap, not conceptual accuracy.

2. **Wiki-link markdown stripped.** The `strip_wiki_links` function is called on all extracted content (tldr, definition, key_insight, terms, quiz Q&A). Tested: 0/10 random quiz questions contained `[[` syntax.

3. **Bloom's Level removed from encounter UI.** The Apply Knowledge encounter at line 1111 has a comment confirming removal. Bloom's level is now only visible in the character sheet's mastery progress section (line 611), which is the appropriate place for meta-cognitive reflection.

4. **Distractors from document_links.** The `/api/distractors/:id` endpoint (line 337) prefers linked documents over semantically similar ones. Tested: capacitor (id 67) returns Impedance and Reactance, PWM, and Op-Amp as distractors -- all conceptually related through the knowledge graph. This is pedagogically stronger than purely embedding-based similarity.

5. **Bloom's level tracking per topic.** `trackMastery` (line 1495) records the highest Bloom's level achieved, and the character sheet shows the Bloom's depth distribution. This gives players meta-cognitive visibility into the quality of their understanding.

**Persistent weaknesses:**

1. **Single evaluation modality cannot distinguish Bloom's levels.** A player who paraphrases a definition (Bloom's 1-2) and a player who synthesizes a causal explanation (Bloom's 4-5) are both compared to the same reference string via the same cosine similarity. The game tracks Bloom's level based on encounter type (Diagnosis = 4, Teach Apprentice = 5), but this is an assumption about what the encounter requires, not evidence of what the player demonstrated. A player could pass a Diagnosis encounter by reproducing the key_insight text (Bloom's 1) and be credited with Bloom's 4.

2. **Wrong-answer generation is generic.** The `generateWrongAttempt` function (line 1235) produces 5 templated wrong answers based on question keywords ("why" -> "I think it's just because that's how it was designed," "calculate" -> "I tried plugging in the numbers but I keep getting a different answer"). These don't target specific misconceptions for the domain. A capacitor question and a PID question that both start with "why" get the same wrong answer. Misconception-based distractors require domain-specific wrong reasoning, not generic expressions of confusion.

3. **No scaffolding or fading.** Encounters at difficulty 1 and difficulty 6 use the same mechanics. There is no progression from supported (hints provided, partial credit generous) to independent (fewer hints, stricter evaluation). The difficulty scaling affects only reward multipliers and damage amounts, not cognitive demand.

### Dimension 3: Narrative & Structure

**Score: functional**

The structural pattern is **Quest** (open hub with available tasks) layered with **Loop & Grow** (mastery unlocks new regions). This is the right pattern for self-directed topic exploration with spaced repetition.

**Improvements:**

1. **Mystery system requires synthesis.** Each region's `mysteryAnswer` is a specific technical explanation. The Workshop mystery answer: "The capacitor in the power supply has degraded, reducing its capacitance. Without proper filtering, the voltage regulator oscillates and draws excessive current through the inductor, causing thermal shutdown." The player must explain this in their own words, evaluated via semantic similarity. Tested: a good paraphrase scored 0.819 ("correct"). This is genuine synthesis -- the player must combine understanding of capacitors, voltage regulators, and inductors.

2. **Cross-domain challenges.** When players have clues in 2+ regions, they can attempt challenges that span domains (e.g., "A system requires converting raw sensor data from The Control Sanctum into a control signal for The Motion Arena"). This targets Bloom's level 6 (Create) and rewards connecting knowledge across silos.

3. **Region-specific mystery answers.** All 6 regions have detailed technical mystery answers that connect multiple concepts within the domain. The CAN bus mystery involves termination resistors, signal reflections, differential signals, and bit errors. Solving requires understanding the whole subsystem, not a single component.

**Persistent weaknesses:**

1. **NPCs remain stateless.** The apprentice in Teach Apprentice, the dealer in Negotiate, and the "senior engineer" in Predict Behavior have no persistent identity. Each encounter creates a new anonymous NPC. There is no relationship arc, no recurring characters, no sense of community within the Citadel.

2. **No spatial exploration.** Regions are entered and exited from a flat list. There is no sense of physical space, no rooms to navigate, no corridors to explore. The "explore" encounter type (line 1254) provides brief flavor text but no actual spatial choices.

3. **Class choice has no mechanical impact on narrative.** An Engineer and a Sage see identical encounters, identical mysteries, and identical dialogue. The class affects only starting items and HP/MP calculation. The stat system (STR/DEX/CON/INT/WIS/CHA) has minimal gameplay impact since the CHA bluff was correctly removed and stat checks don't bypass knowledge challenges.

### Dimension 4: Motivation & Engagement

**Score: mixed**

**Improvements:**

1. **Mastery-centric HUD.** The HUD shows "X mastered" and a mastery bar. Playwright confirmed no XP bar or gold counter in the HUD. This makes understanding the primary visible metric.

2. **Understanding-based gates.** Region unlocking requires 40% mastery of the previous region (line 561-565). This means players advance by demonstrating understanding, not by grinding encounters for XP. This is a genuine structural improvement aligned with SDT's competence need.

3. **Mastery progress on region cards.** Each region card shows a mastery meter (line 537), making understanding visible across the world map. The player sees their knowledge growing spatially.

4. **XP/gold de-emphasized.** Rewards display in dim text at 0.85rem (line 1470), while mastery messages display in purple at standard weight. This correctly inverts the visual hierarchy.

**Persistent problems:**

1. **XP/gold/levels still fully functional.** Despite de-emphasizing the display, the XP/gold/level system still operates identically: XP accumulates, level-ups grant +5 Max HP and +3 Max MP, gold is earned on every encounter. The level-up message at line 1479 is rendered in success color at bold weight. Players still experience the operant conditioning loop of numerical rewards on every encounter -- the numbers are just smaller and dimmer. A player focused on XP could still grind easy encounters in The Workshop indefinitely.

2. **Death remains trivially punished.** HP drops to 0, player revives at 25% HP and loses 10 gold (line 1487-1490). Since gold has no meaningful use (no shop, no purchases, no expenditure system), death has zero consequence. This undermines any sense of stakes.

3. **No competence escalation within regions.** The encounter difficulty is determined by the region (Workshop = 1, Arena = 6), not by the player's demonstrated understanding. A player who has mastered all capacitor topics still faces the same encounter complexity as a first-time visitor. There is no adaptive difficulty.

4. **The mystery reward is still partially extrinsic.** Solving a mystery grants `region.difficulty * 30` XP and `region.difficulty * 15` gold (line 1324). While the mastery message "This is what mastery looks like" emphasizes the intrinsic aspect, the XP/gold reward still accompanies it. Full intrinsic motivation would mean the mystery reward is purely the satisfaction of synthesis and the narrative resolution.

### Dimension 5: Assessment Design

**Score: hybrid**

**Improvements:**

1. **Teach Apprentice is now genuine evaluation.** The player must identify what's wrong with a plausible wrong answer and correct it. This is a fundamentally different cognitive task from restating correct information. It requires understanding not just the right answer but why a specific wrong answer is wrong. This is the closest the game gets to assessing higher-order thinking through its mechanics.

2. **Distractors from the knowledge graph.** Circuit Build and Component Choice encounters now use `/api/distractors/:id`, which prefers linked documents. Tested: capacitor distractors included Impedance/Reactance, PWM, and Op-Amp -- all topics that a student might confuse with capacitor functions. This is structurally better than random similarity.

3. **Mystery solve as synthesis assessment.** Requiring the player to explain the root cause and fix (evaluated against a detailed technical reference) is a valid assessment of knowledge integration. The mystery answers are specific enough that vague hand-waving would fail.

**Persistent weakness:**

The fundamental limitation remains: **semantic similarity is a single-modality evaluator.** It can detect whether the player's text is semantically close to a reference, but it cannot evaluate:
- Causal reasoning quality (did the player explain WHY, or just state WHAT)
- Specificity of examples (did the player cite concrete values/scenarios)
- Error identification accuracy (in Teach Apprentice, did the player correctly identify the specific error)
- Cross-domain connection quality (in Cross-Domain Challenges, did the player actually connect the domains or just name concepts from each)

This means the Bloom's level tracking is aspirational rather than empirical. The game assigns Bloom's level 5 to Teach Apprentice encounters (line 1193), but the evaluation would grade a Bloom's level 2 response (paraphrasing the correct answer) identically to a Bloom's level 5 response (analyzing the specific error in the wrong answer) if both are semantically similar to the reference.

### Dimension 6: Accessibility & Inclusion

**Score: adequate**

**Improvements from iteration 2:**
- Name input now has `aria-label="Character name"` (line 209) -- previously missing
- Narrative div has `role="main"` and `aria-label="Game narrative"` (line 217)
- Actions div has `role="navigation"` and `aria-label="Game actions"` (line 219)

**Playwright results:**
- 22 focusable elements on character creation, all keyboard accessible
- No horizontal scroll at 200% zoom
- 2/5 landmarks present (navigation, main)

**Persistent issues:**
- Missing `banner` (header), `complementary` (aside), `contentinfo` (footer) landmarks
- No light theme option
- No font size controls
- No reduced motion option (CSS animations present: `fadeIn`, `spin`, `scale(0.98)`)
- Color coding without redundant indicators: success = green (#3fb950), danger = red (#f85149), with no icons or patterns for colorblind users
- Dim text `rgb(139,148,158)` on dark background (#0d1117) is borderline for WCAG AA contrast ratio
- `autocomplete="off"` on freeform input may interfere with assistive technology
- Keyboard number shortcuts (1-9) may conflict with screen reader navigation

### Dimension 7: Freemium Monetisation

**Score: learning-first**

No changes from iteration 2. Free tier includes all 6 regions, all 8 encounter types, mystery system, library, spaced repetition, cross-domain challenges, and the full knowledge base. Premium features (advanced classes, bonus regions, cosmetics, challenge modes) are defined in a config object (line 1583-1591) but not implemented or advertised. No paywalls, no energy gates, no ads, no dark patterns.

---

## Critical Bugs and Issues

1. **Cross-domain challenge reference answers are topic name lists, not technical explanations.** The `combinedAnswer` (line 1394) is constructed by concatenating topic names: "This requires knowledge of stm32, clock, adc, imu from The Control Sanctum and pid, kinematics, gait, reinforcement-learning from The Motion Arena." A player who writes a substantive technical analysis of the signal chain between these domains scores only 0.658 ("partial") because the reference is a list of keywords, not a technical explanation. This means the cross-domain challenge -- the game's highest-order assessment -- rewards listing topic names over demonstrating understanding.

2. **`/api/topics/random` parameter inconsistency.** The endpoint uses `req.query.category` (singular, line 85), while `/api/terms/random` and `/api/quiz/random` use `req.query.categories` (plural, comma-separated). The design spec lists `?categories=` for topics. The frontend's `explore` encounter calls `?category=` (line 1276), which works. But if the frontend ever needs to pass multiple categories to the topics endpoint, it will silently fail. The API surface should be consistent.

3. **Content count dropped significantly.** 599 essential terms (was 7188 in iteration 2) and 589 quiz questions (was 7068). This appears to be a dataset change rather than an importer bug, but it means significantly less content variety. With 53 electronics documents sharing 589 quiz questions across all categories, the Workshop could exhaust unique questions relatively quickly during extended play.

4. **`generateWrongAttempt` produces identical wrong answers for different topics.** Any question starting with "why" gets "I think it's just because that's how it was designed." Any calculation question gets "I tried plugging in the numbers but I keep getting a different answer." The Teach Apprentice encounter's pedagogical strength depends on the wrong answer being plausible and topic-specific. Generic confusion expressions don't create a meaningful error-identification task.

5. **Fallback evaluation is overly generous.** When the OpenRouter API fails, `fallbackEvaluate` (line 316) uses keyword matching with a 30% threshold for "correct" (similarity 0.8). This means a player who mentions 3 out of 10 keywords gets full credit. The semantic evaluation threshold was carefully lowered to 0.75, but the fallback has no equivalent calibration.

---

## Biggest Risk

The cross-domain challenge -- the game's highest cognitive demand and the crown jewel of the Bloom's taxonomy progression -- evaluates against a reference answer that is a list of topic names, not a technical explanation. This means the single mechanic intended to assess synthesis (Bloom's 6) actually rewards keyword listing (Bloom's 1). A player who writes "stm32, clock, adc, imu, pid, kinematics, gait, reinforcement learning" would likely score higher than one who writes a detailed explanation of how IMU data flows through an SPI bus to an STM32's DMA controller, gets processed by a Kalman filter, and feeds a PID loop that generates PWM signals for servos. The assessment is inverted: it rewards shallow breadth over deep connection. This should be the top priority fix because it is the game's most prominent claim to deep integration.

## Priority Fixes for Iteration 4

1. **Write real reference answers for cross-domain challenges.** Replace the topic-name-list `combinedAnswer` with pre-authored technical explanations that describe the actual signal chain, interfaces, and concepts that connect the two domains. Alternatively, construct the reference dynamically by concatenating the `key_insight` or `tldr` fields from topics in both regions.

2. **Generate topic-specific wrong attempts for Teach Apprentice.** Instead of 5 generic confusion templates, derive wrong answers from common misconceptions about the specific topic. For a capacitor question, the wrong answer should confuse capacitors with batteries or mix up series/parallel capacitance formulas. Use the topic's `key_insight` to generate a plausible but specifically wrong variation.

3. **Harmonize API parameter naming.** Make `/api/topics/random` accept `?categories=` (plural, comma-separated) to match `/api/terms/random` and `/api/quiz/random`.

4. **Add adaptive difficulty within regions.** Track per-topic mastery and adjust encounter complexity: new topics get more scaffolding (hints offered proactively, partial credit generous); mastered topics get harder variants (higher Bloom's level quiz questions, fewer hints).

5. **Remove XP/gold/level system entirely, or give gold a meaningful use.** The de-emphasis is a good half-step, but the system still runs in parallel with mastery. Either remove it completely (let mastery be the only progression) or give gold a meaningful purpose (purchase hint tokens, unlock optional lore, fund equipment upgrades that change encounter mechanics). Currently gold accumulates with no expenditure, making both earning and losing it meaningless.

6. **Improve the fallback evaluator calibration.** If the OpenRouter API fails, the keyword-matching fallback should use thresholds comparable to the semantic evaluation. A 30% keyword match granting "correct" (similarity 0.8) is far more generous than the 0.75 cosine threshold.

7. **Add reduced-motion CSS media query.** Wrap `fadeIn`, `spin`, and `scale(0.98)` animations in `@media (prefers-reduced-motion: no-preference)` so users who prefer reduced motion get a static experience.

---

## Research References

- Habgood & Ainsworth (2011). "Motivating Children to Learn Effectively: Exploring the Value of Intrinsic Integration in Educational Games." Journal of the Learning Sciences.
- Bjork & Bjork (1992, 2011). Desirable difficulties framework for spaced repetition and retrieval practice.
- Bloom et al. (1956). Taxonomy of Educational Objectives. (Revised: Anderson & Krathwohl, 2001.)
- Shute, V. J. (2011). "Stealth Assessment in Computer-Based Games to Support Learning." Computer Games and Instruction.
- Ryan & Deci (2000, 2020). Self-Determination Theory: autonomy, competence, relatedness.
- Csikszentmihalyi (1990). Flow: The Psychology of Optimal Experience.
- Sweller (1988). Cognitive Load Theory.
- Ashwell, S. K. (2015). Standard Patterns in Choice-Based Games.

---

<!-- SCORES
intrinsic_integration: partial
pedagogical_soundness: mixed
narrative_structure: functional
motivation_engagement: mixed
assessment_design: hybrid
accessibility: adequate
freemium_monetisation: learning-first
biggest_risk: The cross-domain challenge evaluates against a reference that is a list of topic names rather than a technical explanation, so the highest-order assessment rewards keyword listing over genuine synthesis.
SCORES -->
