# Critique: Knowledge Quest -- Iteration 2

## Overview

Knowledge Quest iteration 2 is a text-based RPG served via Docker Compose (PostgreSQL+pgvector, Python importer, Node.js server). The knowledge base imports 184 documents, 7188 essential terms, 1118 document links, and 7068 quiz questions (up from 0 in iteration 1). The game frontend is a single HTML file (~1250 lines) with character creation, 6-region exploration, 8 encounter types, a mystery system, hint tracking, and semantic answer evaluation via OpenRouter embeddings. Playwright automated testing confirmed: accessible character creation flow, working HUD, no knowledge reveals before answers, no horizontal scroll at 200% zoom, 9/9 gamification elements detected, 6 classes, 6 stats, 6 regions (2 unlocked at level 1, 4 gated).

---

## Iteration 1 Issue Tracker

| Issue from Iteration 1 | Status | Evidence |
|---|---|---|
| Chocolate-covered-broccoli (learning and gameplay separate) | **Partially addressed** | New encounter types (circuit_build, diagnosis, predict_behavior, component_choice) embed knowledge into the decision. However, several encounters still reduce to "type your answer" with a narrative frame. |
| 0 quiz questions imported | **Fixed** | 7068 quiz questions imported across all Bloom's levels. Quiz-based encounters now function. |
| Keyword matching instead of semantic evaluation | **Fixed** | `/api/evaluate` uses embedding cosine similarity. Keyword matching remains as fallback only. Tested: identical answer = 1.0 (correct), good paraphrase = 0.815 (partial), keyword-only = 0.579 (incorrect), irrelevant = 0.076 (incorrect). |
| Knowledge panels shown BEFORE questions | **Fixed** | Playwright confirmed 0 `knowledge-reveal` elements before player answers. Reveals happen only AFTER attempts. |
| All encounters test at Remember/Understand level | **Partially addressed** | Diagnosis (Analyze), Predict Behavior (Apply/Analyze), and Teach Apprentice (Evaluate/Create) aim at higher Bloom's levels. However, diagnosis uses hardcoded generic symptoms disconnected from the actual topic, and Teach Apprentice evaluates output the same way as all other encounters (semantic similarity to a reference answer, not actual pedagogical quality). |
| No stealth assessment | **Partially addressed** | Component Choice encounter is labeled as stealth assessment, and it does assess through implicit path selection. Circuit Build is also effectively stealth (pick component from options). However, most encounters still begin with explicit challenge framing: "Diagnose the problem," "Define this term." |
| Extrinsic motivators only (XP, gold) | **Partially addressed** | Mystery system adds intrinsic curiosity (accumulate clues to solve a regional mystery). But XP and gold remain the primary feedback signals on every encounter. The mystery reward is also extrinsic: +50*difficulty XP and +25*difficulty gold. |

---

## Dimension 1: Intrinsic Integration

**Score: partial**

Iteration 2 makes genuine progress. The design spec correctly identifies that "understanding IS the mechanic" -- and several encounters deliver on this:

- **Circuit Build** asks the player to identify the right component from 4 options, using the topic's definition as a clue. The correct answer requires recognizing what the description refers to. This is real integration: the gameplay action (selecting a component) requires domain knowledge.
- **Component Choice** works similarly with 3 paths branching from a requirement description. The player's choice reveals understanding without explicit questioning.
- **Decode** requires naming a term from its definition -- essentially a reverse flashcard, but wrapped as password entry.

However, integration breaks down in key areas:

1. **Diagnosis encounters use hardcoded generic symptoms.** There are exactly 5 symptom strings (line 694-700) that are randomly selected regardless of the topic. A "diagnosis" of `capacitor` could present "The output is stuck at the supply rail" -- a symptom unrelated to capacitors. The player's "diagnosis" is then evaluated against the topic's `key_insight` or `definition`, not against the symptom's actual cause. This means the diagnosis encounter is semantically incoherent: symptoms don't match the topic, and the "correct answer" doesn't match the symptoms.

2. **Predict Behavior uses hardcoded scenarios.** The 5 prediction scenarios (line 766-771) are randomly selected regardless of the actual topic. A prediction about `CAN bus` might ask "If you double the resistance in this circuit, what happens to the current?" The scenario has nothing to do with CAN bus. The "correct" answer is then the topic's `key_insight`, which also has nothing to do with the scenario. This encounter type is deeply broken.

3. **Negotiate and Teach Apprentice are still "type the answer" encounters** with narrative dressing. The player types text, it's compared to a reference answer via cosine similarity. The game mechanic is identical to a quiz -- the narrative wrapper doesn't change the underlying task.

4. **The term/quiz pools leak across domains.** `api/terms/random` returns terms from ALL documents, including sales methodology (Sandler KARE, Miller Heiman, MEDDPICC). A negotiate encounter in The Workshop (electronics basics) may ask the player to define "Gold Sheet" (a sales strategy document). This breaks the thematic integration of region-to-content mapping.

**What "deep" would require:** The diagnosis symptoms must be generated from or matched to the actual topic. The prediction scenarios must relate to the actual component being discussed. Region-specific term filtering (not global random) would prevent domain leakage.

## Dimension 2: Pedagogical Soundness

**Score: mixed**

**Strengths:**
- 7068 quiz questions across Bloom's levels 1-6 provide excellent content depth. Tested examples include calculation problems (L3: "What resistor value for 5V supply, 20mA LED at 2V drop?"), analysis questions (L4: "Why is the Bow-Tie model fragile compared to the Diamond?"), and design challenges (L6: capacitive touch button design).
- Knowledge reveals happen AFTER attempts, enforcing genuine retrieval practice.
- Spaced repetition surfaces weak topics for review every 6 turns.
- The hint system tracks usage (`state.hintsUsed`), providing assessment metadata.
- Wrong answers always show the correct information with formative feedback.

**Weaknesses:**

1. **Semantic similarity threshold is too strict.** Testing shows a well-constructed paraphrase ("A resistor is a component in a circuit that resists electric current flow. Ohm's law says V=IR, so it creates a voltage drop proportional to current") scores only 0.815 -- graded as "partial." The 0.85 threshold for "correct" means the player must nearly reproduce the exact reference wording. This punishes genuine understanding expressed in different words and rewards rote memorization.

2. **Quiz questions contain raw wiki-link markdown.** Level 5 questions were observed containing `[[quick-context/mcdonald-kam-model|KAM relationship maturity]]` -- unrendered markdown syntax presented directly to the player. This creates confusion and breaks immersion.

3. **Bloom's level classification is keyword-based and often inaccurate.** The `estimate_bloom_level()` function (importer line 213-228) checks for keywords like "define" -> L1, "explain" -> L2, etc. A question like "Why can't you produce sodium metal by electrolyzing water?" contains "why" which maps to L2, but this question requires analysis (L4). The default level is 2, so questions without trigger keywords are all classified as Understand.

4. **No misconception-based distractors.** Circuit Build and Component Choice encounters generate distractors from semantically similar topics (via `/api/similar`). While this is better than random options, it doesn't target common misconceptions. For example, a capacitor question won't specifically offer "resistor" as a distractor because students confuse energy storage with energy dissipation -- it'll offer whatever happens to be semantically nearby in the embedding space.

5. **The CHA bluff escape hatch in Negotiate undermines learning.** A player can roll CHA DC 16 to bypass defining a term entirely (line 884-893). The game even explicitly states "But you didn't actually learn anything." This explicitly acknowledges the escape hatch undermines learning, yet keeps it. The stat system should never bypass knowledge-based challenges.

## Dimension 3: Narrative & Structure

**Score: functional**

The Circuit Citadel metaphor works better in iteration 2. Each region has a persistent mystery ("A power supply keeps failing. Something is drawing too much current..."), creating a through-line that connects encounters. The mystery progress tracking (`state.mysteryProgress[region.id]`) and clue accumulation system give exploration purpose beyond individual encounters.

**Strengths:**
- Region descriptions are domain-specific and evocative (Workshop smells of burnt components, Signal Nexus pulses with data streams)
- Mystery text ties directly to the domain (power supply failures in the Workshop, corrupted bus data in Signal Nexus)
- The 60% clue threshold for mystery solving is well-calibrated -- players must engage with most topics in a region but don't need perfection

**Weaknesses:**
- NPCs remain one-shot interactions. The "apprentice" in Teach Apprentice encounters has no persistent identity or relationship arc.
- The mystery "solution" is purely mechanical: accumulate enough correct answers in a region. There's no actual mystery-solving moment where the player synthesizes clues. The game just announces "MYSTERY SOLVED" when the clue count hits the threshold.
- No branching narrative based on class choice. An Engineer and a Sage see identical encounters and stories.
- Region transitions are abrupt: select from map -> enter -> encounter -> back to map. No exploration, no spatial navigation, no sense of place beyond the opening description.

## Dimension 4: Motivation & Engagement

**Score: mixed**

**Positive developments:**
- The mystery system creates genuine curiosity ("what's actually causing the power supply failures?") -- but undermines it with mechanical resolution.
- Encounter variety (8 types) prevents the monotonous loop of iteration 1.
- Hint cost mechanics (reduced XP, tracked usage) create meaningful decision points.
- Clue progress notifications ("[Mystery clue 3/5: capacitor]") provide progress feedback tied to understanding.

**Persistent problems:**
- **XP and gold dominate every reward signal.** Every successful encounter ends with "+15 XP +5 gold" in bright gold text. The mystery system's reward is also XP+gold. There is no moment where the reward IS the knowledge itself (e.g., unlocking a new capability based on what you learned, seeing a simulation change based on your understanding).
- **No competence escalation.** The encounters at difficulty 6 work identically to difficulty 1 -- the same mechanics with bigger numbers. The difficulty scaling is purely in reward/damage multipliers, not in cognitive demand. There's no scaffolding from recall to transfer to creation.
- **Death is trivially punished.** HP drops to 0, player revives at 25% HP and loses 10 gold (line 1143-1147). Since gold has no meaningful use beyond accumulation, death is nearly costless.
- **No flow state support.** Encounters require an API round-trip for semantic evaluation (~1-2 seconds), and the core loop always returns to a choice screen. There's no momentum, no escalating challenge, no "one more encounter" pull.

## Dimension 5: Assessment Design

**Score: hybrid**

This is the dimension with the most genuine improvement.

**Stealth elements:**
- Component Choice encounters assess understanding through path selection without framing the action as a test.
- Circuit Build encounters present the task as "fix the mechanism" rather than "answer this question."
- The hint system tracks `hintsUsed` as a signal of knowledge gaps.

**Hybrid elements:**
- Diagnosis and Predict Behavior encounters require open-ended text generation evaluated via semantic similarity. The framing is "diagnose this" or "predict what happens," not "answer this quiz question." However, the semantic evaluation is the same regardless of encounter type.
- Apply Knowledge encounters are framed as "system diagnostic" rather than a quiz, but explicitly show "Bloom's Level" in the UI (line 929), breaking the stealth frame entirely.

**Remaining overt elements:**
- Decode encounters are explicitly "name the term" -- a flashcard in disguise.
- Negotiate encounters ask "define this term" with no ambiguity about what's being assessed.
- The spaced repetition system in the Library is purely overt review.

**Critical assessment issue:** The semantic evaluation has a single modality: cosine similarity between player text and reference text. This works for recall and comprehension but cannot assess higher-order thinking. A player who explains causation (analysis), evaluates tradeoffs (evaluation), or proposes a design (creation) is scored the same way as one who paraphrases the reference answer. The assessment cannot distinguish Bloom's levels in practice, even though the quiz questions themselves span all 6 levels.

## Dimension 6: Accessibility & Inclusion

**Score: adequate**

**Playwright test results:**
- 22 focusable elements on character creation, all keyboard accessible
- Stat buttons have proper aria-labels ("Decrease STR", "Increase STR")
- 1 ARIA issue: name input missing explicit label (has placeholder but no `aria-label`)
- Landmarks present: `navigation` (actions div), `main` (narrative div)
- Missing landmarks: `banner`, `complementary`, `contentinfo`
- No horizontal scroll at 200% zoom
- Color contrast: primary text rgb(230,237,243) on dark backgrounds provides adequate contrast; dim text rgb(139,148,158) on dark background is borderline

**Same issues from iteration 1 persist:**
- No light theme option
- No font size controls
- No reduced motion option (CSS animations are present: `fadeIn`, `spin`, `scale(0.98)`)
- Color coding without redundant indicators: success = green (#3fb950), danger = red (#f85149), with no icons or patterns

**New issue:**
- The freeform text input has `autocomplete="off"`, which may interfere with assistive technology
- Keyboard number shortcuts (1-9) conflict with screen reader navigation in some readers

## Dimension 7: Freemium Monetisation

**Score: balanced**

Playwright detected: `hasPremiumBadges: 4`, `hasPaywall: false`, `hasPricing: true`, `premiumMentions: 5`. These correspond to the premium config object in JavaScript (line 1215-1223) and the `premium-badge` CSS class, which exists but is not actively used in the DOM during normal gameplay.

The free tier includes all 6 regions, all 8 encounter types, the mystery system, the library, spaced repetition, and the full knowledge base. Premium features (advanced classes, bonus regions, cosmetics, challenge modes) are defined in a config object but not implemented or advertised. No paywalls, no energy gates, no ad interruptions, no confirmshaming.

This is correct for a prototype: the complete learning experience is free. The premium config suggests future monetisation but doesn't specify how it would gate content.

---

## Critical Bugs and Issues

1. **Domain leakage in encounters.** `/api/terms/random` and `/api/quiz/random` return content from ALL documents globally, including sales methodology, polymer science, and other non-electronics domains. A Workshop encounter (electronics basics) may ask about "Portfolio Velocity" (Sandler KARE sales framework). This is disorienting and pedagogically unsound.

2. **Hardcoded symptoms/scenarios ignore topic context.** `diagnosisEncounter` has 5 generic symptom strings. `predictBehaviorEncounter` has 5 generic scenario strings. Neither is connected to the actual topic fetched from the API. The player may be asked to diagnose "capacitor" but see symptoms about an output stuck at the supply rail, then their explanation of capacitors is compared to the capacitor's definition regardless of the symptom.

3. **Encounter loading race condition.** Playwright testing showed that after clicking "Enter The Workshop," the encounter content sometimes wasn't loaded within 3 seconds -- the old map choices were still visible. The `generateEncounter` function makes 3 sequential API calls (`/api/search`, `/api/terms/random`, `/api/quiz/random`) before rendering, and the first call requires an OpenRouter embedding round-trip. On a cold path, this could take 5+ seconds.

4. **Raw markdown in quiz questions.** Some quiz questions contain unrendered wiki-link syntax: `[[quick-context/mcdonald-kam-model|KAM relationship maturity]]` presented directly in the UI.

5. **Semantic similarity too strict at 0.85 threshold.** A correct paraphrase scores 0.815 and gets "partial." This threshold penalizes genuine understanding expressed in different words.

---

## Biggest Risk

The encounter system is thematically incoherent: diagnosis symptoms, prediction scenarios, terms, and quiz questions are not matched to the topic being discussed or the region being explored. This makes encounters feel like random quizzes in costume rather than integrated investigations of a coherent domain.

## Priority Fixes for Iteration 3

1. **Filter terms and quiz questions by region.** Use the region's topics list to filter `/api/terms/random` and `/api/quiz/random` to terms/questions belonging to documents that match the region's domain. This prevents sales methodology questions in the electronics workshop.

2. **Generate topic-specific symptoms and scenarios.** Replace hardcoded arrays with dynamically generated content. At minimum, use the topic's `key_insight` or `tldr` to construct symptoms that relate to the actual subject matter. Better: store symptom/scenario data alongside quiz questions.

3. **Lower semantic similarity threshold to 0.75 for "correct."** Current 0.85 penalizes valid paraphrases. Testing shows a good paraphrase scores ~0.80. Lower to 0.75 for correct, 0.55 for partial.

4. **Strip wiki-link markdown from quiz question text** before displaying to the player. Add a cleanup step: `question.replace(/\[\[.*?\|?(.*?)\]\]/g, '$1')`.

5. **Remove the CHA bluff escape hatch** from Negotiate encounters. Stat checks should never bypass knowledge-based challenges.

6. **Make mystery resolution require synthesis.** Instead of auto-solving at 60% clue count, present the accumulated clues and ask the player to explain the root cause. Evaluate their explanation against the mystery description.

7. **Remove the "Bloom's Level" display** from Apply Knowledge encounters (line 929). This meta-information breaks immersion and serves no player-facing purpose.

---

<!-- SCORES
intrinsic_integration: partial
pedagogical_soundness: mixed
narrative_structure: functional
motivation_engagement: mixed
assessment_design: hybrid
accessibility: adequate
freemium_monetisation: balanced
biggest_risk: Encounters are thematically incoherent -- diagnosis symptoms, prediction scenarios, and terms are not matched to the topic or region, making the game feel like random quizzes in narrative costume rather than integrated domain investigations.
SCORES -->
