# Critique: Knowledge Quest -- Iteration 5 (FINAL)

## Overview

Knowledge Quest iteration 5 is a text-based RPG served via Docker Compose (PostgreSQL+pgvector, Python importer, Node.js server). The knowledge base contains 184 documents with embeddings, 599 essential terms, 1113 document links, and 746 quiz questions (157 from key_insight, 589 from test_your_understanding). The game frontend is a single HTML file (~2257 lines) with character creation, 6-region exploration, 12 encounter types (including 2 new action-based encounters), mastery-only progression (no XP/levels), gold restricted to merchant encounters with mastery-based replenishment, a mystery system, category-based content filtering, concept cascade synthesis challenges, knowledge journal, 3-step negotiate bartering, 7 deterministic cross-domain challenges, 4 circuit wiring challenges, 4 fault tree diagnostic challenges, 18 topic-specific misconception pools with targeted corrective feedback via `/api/misconception-match`, and semantic answer evaluation via OpenRouter embeddings. Playwright automated testing confirmed: accessible character creation flow (22 focusable elements, 19/20 tab stops), mastery-only HUD (no XP bar, no gold display, rank and mastery count displayed), 26 interactive elements with 0 missing ARIA labels, 4/5 landmarks present (banner, navigation, main, contentinfo), reduced-motion CSS media query present, no horizontal scroll at 200% zoom.

---

## Iteration 4 Issue Tracker

| Issue from Iteration 4 | Status | Evidence |
|---|---|---|
| Cross-domain challenge references were non-deterministic (random insights) | **Fixed** | The `crossTopicChallenge` function at line 1973 now selects from `CROSS_DOMAIN_CHALLENGES` -- a hardcoded array of 7 challenges with fixed `reference` strings. No call to `/api/topics/insights` exists in the frontend (confirmed via grep). Tested: evaluating "An H-bridge uses four MOSFETs to control motor direction. PWM controls speed via duty cycle. Flyback diodes protect against back-EMF." against the motor driver reference scored 0.852 ("correct"). The same answer would score 0.852 on every attempt because the reference is fixed. |
| No action-based encounters (all text entry) | **Fixed** | Two new encounter types implemented: (1) `circuitWiringEncounter` (line 1169) presents named circuit slots and a mixed pool of correct parts + distractors. Player taps parts to fill slots. No text entry. 4 challenges defined in `CIRCUIT_WIRING_CHALLENGES`. (2) `faultTreeEncounter` (line 1296) presents symptoms and diagnostic step buttons. Player clicks steps to reveal information, then optionally declares root cause (only this final step uses text). 4 challenges in `FAULT_TREE_CHALLENGES`. Both use custom CSS classes (`.wiring-slot`, `.wiring-part`, `.fault-step-btn`, `.fault-info`) with full ARIA labels. |
| Wrong answers get generic feedback (no diagnostic branching) | **Fixed** | The `matchMisconception` function (line 653) sends the player's wrong answer plus the relevant misconception pool to `POST /api/misconception-match`. The server embeds both and returns the best-matching misconception above 0.60 similarity threshold. Misconception matching is integrated into 7 encounter types: Diagnosis (line 1497), Predict Behavior (line 1581), Apply Knowledge (line 1775), Teach Apprentice (line 1838), Fault Tree (line 1361), Cross-Domain (line 2017), and Mystery Solve (line 1954). Tested: `{"playerAnswer":"capacitors store current","misconceptions":[...]}` returned `{"matched":true,"similarity":0.723}` with the correct capacitor/current misconception. Non-matching answer ("a resistor limits current flow") returned `{"matched":false,"similarity":0.31}`. Keyword fallback (line 678) activates if the API fails. 18 topic keys with 1-3 misconceptions each, totaling 37 individual misconceptions with specific corrective text. |
| Gold has no replenishment mechanism | **Fixed** | `GOLD_PER_RANK` (line 597) defines gold per rank: Apprentice=10, Journeyman=15, Master=25. `checkGoldReplenishment` (line 736) fires on each topic mastery (line 2110), checks if region rank advanced, and awards cumulative gold for all new ranks reached. `goldRanksEarned` state (line 613) tracks highest rank that earned gold per region. Total possible gold from mastery: 6 regions * (10 + 15 + 25) = 300 gold. Additionally, the negotiate encounter (line 1683) detects when a player has no gold but passed steps 1-2, and the dealer accepts "knowledge in trade" -- giving the component free. Gold depletion is no longer a dead end. |
| Concept cascade detection used includes() for partial matches | **Fixed** | Line 769: `const hasA = masteredKeys.some(k => k === a);` uses strict equality instead of `.includes()`. Comment at line 767 documents the fix: "ITERATION 5 FIX: exact key match, not includes()". Mastering "decoupling-capacitor" no longer triggers the capacitor+inductor cascade. |

**Verdict: 5 of 5 issues fully addressed.** All four priority fixes from iteration 4 are implemented and verified through both code review and live API testing.

---

## Test Results Summary

### Automated Test Data

| Test Category | Result | Key Metric |
|---|---|---|
| Accessibility: Keyboard Nav | PASS | 19/20 tab stops hit interactive elements, 22 focusable elements |
| Accessibility: ARIA | PASS | 26 interactive elements, 0 missing labels |
| Accessibility: Zoom | PASS | No horizontal scroll at 200% zoom |
| Accessibility: Landmarks | PASS | 4/5 landmarks present (banner, navigation, main, contentinfo); missing: complementary |
| Accessibility: Reduced Motion | PASS | `@media (prefers-reduced-motion: reduce)` present at line 29 |
| Game Flow: Engine | Custom | Single-page JavaScript application, no framework, ~2257 lines |
| Game Flow: Regions | 6 total | 1 unlocked at start, 5 locked behind mastery gates |
| Rewards: Gamification | Mastery-only | No XP bar, no gold display in HUD. Mastery count + rank shown |
| Assessment: Quiz Elements | Hybrid | Stealth (component choice, circuit wiring, fault tree) + text evaluation (negotiate, decode, diagnosis, predict, teach, cross-domain, cascade) |
| Monetisation: Flags | 0 actual | Paywall/pricing false positives from "unlock" (region gating), "points remaining" (stat allocation), "crystal" (in context of crystal oscillator content), and "mystery" (gameplay mechanic). No real paywalls. |
| API: Health | OK | All endpoints responding, 184 docs with embeddings |
| API: Stats | OK | 184 docs, 599 terms, 1113 links, 746 quiz, 9 categories |
| API: Evaluate | OK | Similarity 0.852 for motor driver answer against fixed reference |
| API: Misconception-Match | OK | 0.723 similarity for matching misconception, 0.31 for non-matching (threshold 0.60 works correctly) |
| Technical: State Persistence | Yes | localStorage with `knowledge-quest-save` key, saves goldRanksEarned |

### Critical Test Findings

- **All 4 iteration 4 fixes verified through live API testing.** Cross-domain challenge evaluation is now deterministic (fixed reference, 0.852 for accurate answer). Misconception matching works server-side with correct threshold behavior. Gold replenishment code is present and structurally correct. Circuit wiring and fault tree encounters have full DOM structures with ARIA labels.
- **XP/level system remains completely removed.** 0 references to `state.char.xp`, `state.char.level`, or `grantReward` in functional code. The HUD contains only: name, HP bar, MP bar, mastery count, and rank.
- **Database stats are lower than design spec claims.** The spec says 1198 terms and 1492 quiz questions; the live database has 599 terms and 746 quiz questions. This suggests the importer may not have been re-run with the expanded question generation. The game still functions correctly with the available content, but content variety is half of what was specified.
- **No gold display in HUD.** Gold appears only in the character sheet / mastery progress view (line 1036: `Gold: ${c.gold}`) and during negotiate encounters. This is correct per the design intent -- gold is not a visible progression metric.
- **The `/api/misconception-match` endpoint requires the frontend to pass the misconception array.** The API does not look up misconceptions by topic name -- the frontend is responsible for selecting the relevant pool from `MISCONCEPTION_POOLS` and sending it. The endpoint signature is `{playerAnswer, misconceptions[]}`, not `{answer, topic}`. This is architecturally sound (keeps misconception definitions in the frontend for zero-latency pool selection) but means the endpoint cannot be tested with just a topic name.

---

## Scorecard

| Dimension | Rating | Key Finding |
|---|---|---|
| Intrinsic Integration | Deep | Action-based encounters (circuit wiring, fault tree) make understanding the core mechanic; deterministic cross-domain references give the capstone assessment validity; misconception-targeted feedback turns wrong answers into learning events; gold earned through mastery ranks closes the economic loop. |
| Pedagogical Soundness | Mixed | Diagnostic branching with 37 misconceptions is strong formative assessment, but no scaffolding/fading (all difficulty levels use identical mechanics) and single evaluation modality (cosine similarity) cannot distinguish reasoning quality from vocabulary overlap. |
| Narrative & Structure | Functional | 6-region quest structure with mystery system works; concept cascades create synthesis moments; knowledge journal tracks growth; but NPCs remain stateless and class choice has no mechanical impact. |
| Motivation & Engagement | Intrinsic | Mastery is the sole visible progression; gold earned through understanding, not grinding; concept cascades and mystery solves are intrinsically rewarding; death penalty is proportional (25% HP, no gold loss). |
| Assessment Design | Hybrid | Circuit wiring and fault tree are genuine stealth assessment (actions reveal understanding); misconception matching provides diagnostic branching; cross-domain references are now valid; but cosine similarity still conflates vocabulary proximity with conceptual accuracy. |
| Accessibility | Adequate | 19/20 tab stops, 0 missing ARIA labels, 4/5 landmarks, reduced-motion present, no zoom overflow; still missing light theme, font controls, and visual redundancy for color-coded feedback. |
| Freemium Monetisation | Learning-first | No paywalls, no ads, no dark patterns. All content free. Premium features defined but not implemented or advertised. |

---

## Detailed Analysis

### Dimension 1: Intrinsic Integration

**Score: deep**

This is the most significant upgrade from iteration 4's "partial" rating. Four changes converge to make understanding the core gameplay mechanic:

1. **Circuit wiring is genuine stealth assessment.** The player sees slots labeled "Input filter", "Voltage conversion", "Output filter", "Load decoupling" and must select the correct component from a pool that includes both correct answers and plausible distractors (e.g., "Zener diode" and "Crystal oscillator" alongside "Buck converter IC"). No text is typed. The act of placing "Bulk capacitor" in the "Input filter" slot IS the demonstration of understanding -- the player cannot succeed without knowing what each circuit stage does. This fulfills Habgood & Ainsworth's criterion: the learning content rides on the most engaging part of gameplay (building/solving), not on a separate quiz layer.

2. **Fault tree diagnosis assesses reasoning process, not just final answer.** The player sees "Motor Not Spinning" with symptoms and chooses diagnostic steps from a menu. Each step reveals information: "Measure supply voltage at motor driver input" returns "12.1V present -- power supply is good" and eliminates "power supply failure." The PATH the player takes through diagnostic steps reveals their reasoning strategy -- a student who checks the power supply first demonstrates different understanding than one who jumps to the bootstrap capacitor. This is stealth assessment per Shute (2011): the game observes behavioral evidence of competency without interrupting the experience.

3. **Deterministic cross-domain references make the capstone assessment valid.** The motor driver challenge reference is a fixed 80-word technical description specifying H-bridge topology, N-channel MOSFETs, bootstrap capacitors, PWM frequency range, Schottky flyback diodes, gate resistors, and current-sense resistors. A player who understands motor driver design will match this reference; one who doesn't will score low. The same answer evaluates the same way every time. Tested: a concise motor driver description scored 0.852 ("correct") against this reference.

4. **Gold earned through mastery completes the economic integration.** The negotiate encounter's "knowledge in trade" fallback (line 1683) means a player with zero gold but demonstrated understanding (steps 1-2 correct) still gets the component. Gold replenishment via rank milestones (10+15+25 = 50 gold per region, 300 total) ensures the economic subsystem rewards understanding, not grinding. The gold system is now fully intrinsically integrated: you earn gold by mastering topics, and you spend gold more efficiently by demonstrating understanding.

**What prevents a "perfect" rating:**

The semantic similarity bottleneck remains for all text-entry encounters. A player who paraphrases the reference text (Bloom's level 1) scores the same as one who constructs a causal explanation (Bloom's level 4-5). The circuit wiring and fault tree encounters sidestep this limitation (actions rather than text), but 8 of 12 encounter types still evaluate via cosine similarity. This is a fundamental constraint of the current architecture, not a design choice that can be easily fixed.

### Dimension 2: Pedagogical Soundness

**Score: mixed**

**Improvements:**

1. **Diagnostic branching with 37 misconceptions is strong formative assessment.** When a student writes "capacitors store current" in a capacitor-related encounter, the system identifies the specific misconception (0.723 similarity match) and returns targeted corrective text: "Capacitors store energy in an electric field between two plates, not current." This is textbook formative assessment: identifying the specific error in the student's mental model and providing a correction that addresses that exact error, not a generic "try again." The corrective text is detailed (50-100 words) and explains WHY the misconception is wrong, not just what the right answer is.

2. **Fault tree diagnosis targets Bloom's level 4 (Analyze) through action.** The student must analyze symptoms, form hypotheses, select tests, interpret results, and synthesize a diagnosis. The "eliminate hypothesis" vs "reveal clue" distinction in step results teaches systematic debugging methodology. The `minStepsToSolve` parameter (3 for all challenges) sets a lower bound on investigation before declaring root cause, preventing guessing.

3. **Circuit wiring targets Bloom's level 3 (Apply) through action.** Selecting components for specific circuit positions requires applying knowledge of component function to a specific design context. The distractors are plausible but incorrect (e.g., "Crystal oscillator" in a voltage regulator circuit), requiring understanding of why they don't fit, not just recognition.

**Persistent weaknesses:**

1. **No scaffolding or fading.** A first-time player in The Workshop (difficulty 1) faces the same circuit wiring mechanics with the same number of distractors and the same evaluation thresholds as a mastery-level player in The Motion Arena (difficulty 6). The difficulty scaling affects only damage amounts, not cognitive demand. There is no progression from supported (fewer distractors, partial credit, recognition tasks) to independent (more distractors, strict evaluation, recall tasks). This violates Vygotsky's ZPD: the game does not adapt to the student's current ability boundary.

2. **Single evaluation modality for text encounters.** Cosine similarity measures vocabulary overlap, not reasoning quality. A student who writes "MOSFET switches with PWM for motor control, flyback diodes protect" (paraphrasing keywords) may score higher than one who writes "The H-bridge alternates current direction through the motor by activating diagonal switch pairs, and the inductive kick when switches turn off requires clamping paths" (genuine causal reasoning with different vocabulary). The misconception matching partially addresses this for wrong answers, but correct-answer evaluation remains vocabulary-dependent.

3. **Interleaving is incidental.** Encounter types are selected randomly (line 1147: `types[Math.floor(Math.random() * types.length)]`), and topics within a region are selected via search against a random topic from the region's list (line 1125). There is no intentional spacing, no progressive topic sequencing, and no mechanism to ensure a student sees all topics before repeating any.

4. **Quiz question count is half the spec.** The live database has 746 quiz questions vs the design spec's 1492. This means topic exhaustion will occur sooner in extended play sessions, particularly in regions with fewer topics.

### Dimension 3: Narrative & Structure

**Score: functional**

The structural pattern remains Quest (open hub) layered with Loop & Grow (mastery unlocks regions). Iteration 5 does not add new narrative elements beyond what iteration 4 established (concept cascades, knowledge journal, mystery system). The narrative improvements are indirect: the circuit wiring and fault tree encounters create more varied gameplay moments within the existing structure.

**Strengths carried forward:**

1. Knowledge journal creates narrative continuity and visible evidence of growth (SDT competence).
2. Concept cascades create "aha moments" where two topics synthesize into a higher principle.
3. Mystery answers require genuine multi-concept technical synthesis.
4. Six regional narratives provide thematic context for different knowledge domains.

**Persistent weaknesses:**

1. NPCs remain stateless (apprentice, dealer, senior engineer have no persistent identity).
2. Class choice has no mechanical impact beyond starting items and HP/MP calculation.
3. No spatial exploration within regions (flat list, no rooms/corridors).
4. The circuit wiring and fault tree encounters, while mechanically distinct, do not expand the narrative (no story context for why you're wiring a circuit or debugging a fault -- they appear as abstract challenges).

### Dimension 4: Motivation & Engagement

**Score: intrinsic**

This dimension remains strong from iteration 4 and is further reinforced by the gold replenishment system:

1. **Mastery is the only visible progression.** HUD shows: name, HP, MP, mastered count, rank. No XP, no gold counter, no level indicator. Playwright confirmed: `#hud-xp-bar` not present, `#hud-gold` not present.

2. **Gold is now intrinsically integrated.** Players earn gold through mastery milestones (rank advances), not through encounter completion. The negotiate encounter accepts "knowledge in trade" when the player has no gold but demonstrates understanding. This closes the loop: understanding earns gold, gold enables more learning encounters (negotiate), and understanding reduces gold cost. Gold is a consequence of learning, not a substitute for it.

3. **Action-based encounters provide autonomy.** In circuit wiring, the player chooses which component to place in which slot -- genuine decision-making, not quiz-answer selection. In fault tree, the player chooses which diagnostic steps to take and in what order -- genuine investigative autonomy. These are much closer to SDT's autonomy requirement than "type your answer below."

4. **Death penalty remains proportional.** Revive at 25% HP, no gold loss (line 2080-2081). This is less punishing than losing gold would be, especially now that gold is earned through mastery milestones rather than encounters.

**Remaining concern:** The circuit wiring encounter auto-fills the next empty slot when a part is tapped (line 1226: `const emptyIdx = slotFills.indexOf(null)`). This means the player cannot directly choose WHICH slot to fill -- they must fill in order 1-2-3-4. This reduces autonomy: a student who recognizes the output filter but not the input filter must still fill the input slot first. Allowing direct slot selection (tap slot, then tap part) would better support non-linear reasoning.

### Dimension 5: Assessment Design

**Score: hybrid**

**Improvements:**

1. **Circuit wiring is genuine stealth assessment.** The student's component selections directly reveal their understanding of circuit topology. No quiz framing, no explicit "test your knowledge" prompt. The student is building a circuit; the game is assessing their understanding. Per Shute (2011), the assessment is invisible within the gameplay.

2. **Fault tree assesses reasoning process.** The sequence of diagnostic steps chosen reveals the student's mental model of the system. A student who checks power supply first, then signal path, then gate drive demonstrates systematic top-down debugging. One who jumps to "Inspect bootstrap capacitor" without checking upstream signals may be guessing. The game tracks steps used and distinguishes "optimal" (minimum steps) from "thorough" (all steps) paths.

3. **Misconception matching provides diagnostic branching.** When a student's wrong answer matches a known misconception (above 0.60 cosine similarity), they receive a targeted correction. When it doesn't match, they get generic feedback. This creates two remediation paths: specific (addressing the identified error) and general (showing the correct answer). The 0.60 threshold was tested and works correctly: a capacitor-current misconception matched at 0.723, while an unrelated resistor answer scored 0.31.

4. **Cross-domain assessment is now valid.** The fixed reference for "Design a Motor Driver Circuit" tests whether the student can describe H-bridge topology, MOSFET selection, PWM parameters, back-EMF protection, and gate drive requirements. A student who can do this has genuinely cross-domain understanding. The same answer evaluates identically every time -- this is a basic assessment validity requirement that was missing in iteration 4.

**Persistent weakness:**

The cosine similarity evaluation fundamentally measures vocabulary proximity, not conceptual accuracy. A student could score "correct" by stringing together the right technical terms in the wrong relationships ("Bootstrap capacitors protect against back-EMF while flyback diodes charge the high-side gate drivers") because the embeddings capture term co-occurrence, not logical structure. The action-based encounters (circuit wiring, fault tree) sidestep this limitation, which is precisely why they represent the most valid assessment in the game.

### Dimension 6: Accessibility & Inclusion

**Score: adequate**

Playwright test results:

- 19/20 tab stops hit interactive elements (PASS)
- 22 focusable elements on character creation (PASS)
- 26 interactive elements, 0 missing ARIA labels (PASS)
- 4/5 landmarks present: banner, navigation, main, contentinfo (PASS; complementary missing but acceptable -- no sidebar element)
- No horizontal scroll at 200% zoom (PASS)
- `@media (prefers-reduced-motion: reduce)` present (PASS)
- New circuit wiring and fault tree elements have ARIA labels: `.wiring-slot` has `aria-label="Slot N: name, component/empty"`, `.wiring-part` has `aria-label="Component: name (already placed/not)"`, `.fault-step-btn` has `aria-label="Diagnostic step: action (already performed/not)"`

**Persistent issues (unchanged from iteration 4):**

- No light theme option. Dark-only theme with `--text-dim: #8b949e` on `--bg: #0d1117` is borderline WCAG AA (~4.1:1 contrast ratio for normal text).
- No font size controls.
- Color coding without redundant indicators: success = green, danger = red, misconception = red border, with no icons or patterns for colorblind users. The new `.msg-misconception` style uses only a red border and red bold text for the "Common misconception detected" label.
- New wiring encounter uses `.used { opacity: 0.3 }` for placed parts, which could be difficult to distinguish from active parts for users with low vision. The opacity-based distinction provides no alternative indicator.

### Dimension 7: Freemium Monetisation

**Score: learning-first**

No changes from iteration 4. Free tier includes all 6 regions, all 12 encounter types, mystery system, library, spaced repetition, cross-domain challenges, concept cascades, knowledge journal, circuit wiring challenges, fault tree challenges, and the full knowledge base. Premium features (line 2217-2225: advanced classes, bonus regions, cosmetics, challenge modes) are defined but not implemented or advertised. No paywalls, no energy gates, no ads, no dark patterns, no loot boxes. The Playwright monetisation detector flagged false positives from game content terms ("crystal" in crystal oscillator, "mystery" in mystery system, "unlock" in region gating, "points remaining" in stat allocation).

---

## Critical Bugs and Issues

1. **Database content count mismatch.** The design spec claims 1198 essential terms and 1492 quiz questions. The live database contains 599 terms and 746 quiz questions. This is a 50% shortfall in content that affects encounter variety and potential for topic exhaustion. The importer may not have been re-run with the expanded generation pipeline. Severity: minor (game works correctly with available content, but variety suffers in extended play).

2. **Circuit wiring auto-fills sequential slots.** When a player taps a component, it fills the FIRST empty slot (line 1226: `slotFills.indexOf(null)`). The player cannot choose to fill slot 3 before slot 1. This constrains assessment validity: a student who recognizes the output filter but not the input filter is forced to guess at slot 1 first. Severity: minor (the clear-all button provides a workaround, but the interaction model is less flexible than it could be).

3. **`/api/misconception-match` endpoint signature mismatch with task specification.** The endpoint expects `{playerAnswer, misconceptions[]}` but the task testing instructions used `{answer, topic}`. The endpoint works correctly with its actual signature. This is a documentation issue, not a bug.

4. **Fault tree hides freeform input during diagnostic steps.** Line 1385: `document.getElementById('input-row').style.display = 'none';`. This prevents the player from typing custom actions during the fault tree encounter. It is correctly restored at line 1389 when the encounter ends. Not a bug per se, but it breaks the game's general expectation that freeform input is always available.

---

## Biggest Risk

The semantic similarity evaluation modality remains the single largest threat to assessment validity across 8 of 12 encounter types. While iteration 5 successfully mitigates this for cross-domain challenges (deterministic references), wrong answers (misconception matching), and adds two encounter types that bypass it entirely (circuit wiring, fault tree), the fundamental limitation persists: cosine similarity between text embeddings measures vocabulary overlap, not conceptual accuracy. A student who assembles the right technical terms without understanding their relationships will pass text-entry encounters; a student who understands deeply but uses different vocabulary may fail. The game's most valid assessments are now the action-based encounters (circuit wiring and fault tree) precisely because they assess behavior, not text. The recommendation for any future work is to expand the proportion of action-based encounters and reduce reliance on freeform text evaluation.

---

## Recommendations

### Quick Wins

1. **Allow direct slot selection in circuit wiring.** Change the click handler so tapping a slot marks it as the target, then tapping a part fills that specific slot. This supports non-linear reasoning and improves assessment validity.

2. **Add visual redundancy for color-coded feedback.** Prefix success messages with a checkmark character, danger messages with a warning character, and misconception messages with a lightbulb or question mark. This makes the feedback accessible to colorblind users without requiring icons or images.

3. **Increase opacity floor for used wiring parts.** Change `.wiring-part.used { opacity: 0.3 }` to `opacity: 0.4` and add `text-decoration: line-through` for a redundant visual indicator that a part has been placed.

### Structural Changes

1. **Add scaffolding within regions.** Track per-topic correct/attempt ratio and adjust encounter complexity. New topics get recognition tasks (Component Choice, Decode) with generous partial credit. Partially mastered topics get application tasks (Diagnosis, Predict Behavior, Circuit Wiring). Mastered topics get evaluation tasks (Teach Apprentice, Fault Tree) with strict thresholds. This creates fading per Vygotsky's ZPD.

2. **Expand action-based encounters.** The circuit wiring and fault tree formats bypass the cosine similarity limitation. Adding more variants (signal routing challenge, timing diagram interpretation, PCB layout review) would increase the proportion of valid stealth assessment.

3. **Add intentional interleaving.** Track which topics a student has encountered and ensure related-but-different topics are presented in sequence (e.g., capacitor followed by inductor, then LC resonance cascade) rather than random selection. Research (Rohrer, 2012) shows interleaving improves discrimination learning.

### Advanced Improvements

1. **Add light theme option.** Provide `@media (prefers-color-scheme: light)` CSS or a manual toggle. The current dark theme with borderline contrast ratios is an accessibility concern.

2. **Re-run importer with expanded question generation.** The database has 599 terms vs the spec's 1198, and 746 quiz questions vs the spec's 1492. Running the importer with the key_insight and summary question generators would double the content variety.

3. **Add adaptive evaluation for text encounters.** Instead of pure cosine similarity, use a two-stage evaluation: (1) cosine similarity for initial screening, then (2) if the answer is borderline (0.55-0.75), extract key concepts from both answer and reference and check whether the causal relationships between concepts match. This would better distinguish paraphrasing from genuine understanding.

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
- Vygotsky, L. S. (1978). Mind in Society: The Development of Higher Psychological Processes. (Zone of Proximal Development.)
- Rohrer, D. (2012). "Interleaving Helps Students Distinguish Among Similar Concepts." Educational Psychology Review.

---

<!-- SCORES
intrinsic_integration: deep
pedagogical_soundness: mixed
narrative_structure: functional
motivation_engagement: intrinsic
assessment_design: hybrid
accessibility: adequate
freemium_monetisation: learning-first
biggest_risk: Cosine similarity evaluation across 8 of 12 encounter types measures vocabulary overlap rather than conceptual accuracy, so students who assemble correct terms without understanding pass while students with deep understanding but different vocabulary may fail.
SCORES -->
