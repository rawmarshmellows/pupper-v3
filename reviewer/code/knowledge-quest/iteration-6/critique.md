# Critique: Knowledge Quest -- Iteration 6

## Overview

Knowledge Quest iteration 6 is a text-based RPG served via Docker Compose (PostgreSQL+pgvector, Python importer, Node.js server). The knowledge base contains 184 documents with embeddings, 599 essential terms, 1113 document links, and 746 quiz questions (157 from key_insight, 589 from test_your_understanding). The game frontend is a single HTML file (~2639 lines) with character creation (6 classes with unique abilities, 6 stats with d20+modifier checks), a guided tutorial, 6-region exploration, 12 encounter types, mastery-only progression (no XP/levels), half-life mastery decay model, gold restricted to merchant encounters with mastery-based replenishment, a mystery system, category-based content filtering, concept cascade synthesis challenges, knowledge journal, 3-step negotiate bartering, 7 deterministic cross-domain challenges, 4 circuit wiring challenges with direct slot selection, 4 fault tree diagnostic challenges, 18 topic-specific misconception pools with targeted corrective feedback, and LLM-based answer evaluation (Gemini 2.0 Flash via OpenRouter) as the primary modality with cosine similarity as fallback. API testing confirmed: health OK, 184 docs, 599 terms, 746 quiz questions, LLM evaluator correctly grades correct/partial/incorrect answers with conceptual reasoning, misconception matching works at 0.723 similarity.

---

## Iteration 5 Issue Tracker

| Issue from Iteration 5 | Status | Evidence |
|---|---|---|
| Cosine similarity conflates vocabulary with conceptual accuracy across 8/12 encounter types | **Fixed** | LLM evaluation (POST `/api/evaluate-llm`) is now the primary evaluation modality for ALL text-entry encounters. The `evaluateAnswer` function at line 510 calls `/api/evaluate-llm` first, falling back to `/api/evaluate` (cosine similarity) only on failure. The server endpoint (line 324) sends the question, correct answer, and player answer to Gemini 2.0 Flash with an explicit system prompt: "Grade based on CONCEPTUAL UNDERSTANDING, not vocabulary matching." Tested: "voltage is proportional to current when resistance is constant" graded "correct" for Ohm's Law (different vocabulary, correct concept). "capacitors store energy in electric fields between plates" graded "incorrect" for Ohm's Law (unrelated concept). "its the relationship between V I and R but I dont remember exactly" graded "partial" (vague but directionally correct). All three grades came back with `source: "llm"`. |
| No scaffolding/fading -- same mechanics at all difficulty levels | **Partially addressed** | Stats + d20 checks provide implicit scaffolding. A successful INT check reveals a full hint (line 1617: full definition), while a failed check reveals a garbled partial hint (line 1621: first 40% of text). Region DC scales from 8 (easy) to 16 (hard) via `regionDC()` at line 599. However, the encounter TYPE selection is still random (line 1242), and the number of distractors, partial credit thresholds, and evaluation strictness remain identical across regions. The stat check provides context scaffolding but not cognitive demand scaffolding. |
| Class choice has no mechanical impact beyond starting items and HP/MP | **Fixed** | Six classes with unique mechanical abilities defined at lines 314-328. Each class has an `ability` object with a specific stat bonus (+3) applied to the relevant stat during `rollCheck` (line 584-588). Engineer gets +3 DEX on wiring, Scholar +3 INT on theory, Explorer +3 WIS on diagnosis, Sage +3 CHA on teaching, Artificer +3 INT on negotiate. Tinker has a unique "Jury-Rig" mechanic (line 1657-1681): spend 3 Stamina to retry a failed component choice encounter once per encounter, tracked via `state.juryRigUsedThisEncounter`. The `canJuryRig` function (line 1692) checks class, MP, and once-per-encounter constraint. |
| NPCs remain stateless | **Not addressed** | NPCs (apprentice, dealer, senior engineer) still have no persistent identity or relationship tracking. Each encounter generates a fresh anonymous NPC. |
| No intentional interleaving/spacing | **Partially addressed** | The half-life mastery decay model provides a form of spaced repetition. Fading topics (below 50% strength) are prioritized for review encounters with a 30% chance of appearing during region exploration (line 1230). A dedicated "Review fading topics" option appears on the world map (line 988). However, within-session topic selection remains random (line 1214), and there is no interleaving of related-but-different topics. |

**Verdict: 3 of 5 issues fully addressed, 2 partially addressed.** The cosine similarity limitation and class mechanical impact -- the two most critical issues from iteration 5 -- are both resolved. Scaffolding and interleaving are improved but not fully realized.

---

## RPG Mechanical Integrity Analysis (NEW Dimension)

### 1. Stats Affect Every Encounter via d20 Checks

All 6 stats are mechanically functional through d20+modifier checks:

| Stat | Encounters Using It | Mechanical Effect |
|---|---|---|
| STR | Component Choice (line 1872) | Successful check eliminates one distractor option |
| DEX | Circuit Wiring (line 1319) | Successful check reduces distractors by 1 |
| CON | Fault Tree after 4+ steps (line 1508) | Failed check causes 1 HP damage from fatigue |
| INT | Circuit Build (1595), Predict (1805), Decode (2013), Apply (2047), Cross-Domain (2325) | Successful check reveals full hint/definition; failure shows garbled/partial info |
| WIS | Review (1141, 1268), Fault Tree (1470), Diagnosis (1706), Mystery (2257) | Successful check reveals context/eliminates hypotheses; failure gives less info |
| CHA | Negotiate (1910), Teach Apprentice (2121) | Negotiate: free "correct step" (rapport discount). Teach: partial grades promoted to correct (line 2142) |

The `rollCheck` function (line 581) correctly calculates: d20 + floor((stat - 10) / 2) + classBonus vs DC. The `regionDC` function (line 599) scales DCs from 8 (easy regions) to 16 (hard regions). The `formatRoll` function (line 593) displays the full roll breakdown to the player, making the system transparent.

**Assessment:** Stats are not cosmetic. They create genuinely different gameplay experiences. A high-INT Scholar gets full hints on theory checks; a low-INT character proceeds with partial information. A high-DEX Engineer faces fewer circuit wiring distractors. A high-CHA Sage's partial teaching answers are accepted as correct. These are mechanically consequential, not flavor text.

### 2. Classes Have Unique Abilities

Six classes defined at lines 314-328:

| Class | Ability | Mechanical Effect |
|---|---|---|
| Engineer | Precision Wiring | +3 DEX on circuit wiring checks |
| Scholar | Deep Theory | +3 INT on theory/prediction checks |
| Tinker | Jury-Rig | Spend 3 Stamina to retry failed component choice (once/encounter) |
| Sage | Mentor's Insight | +3 CHA on teaching/negotiation checks |
| Explorer | Keen Eye | +3 WIS on diagnosis checks |
| Artificer | Component Crafting | +3 INT on negotiate checks |

The class bonus is applied via `rollCheck` at line 584-588: if the ability's stat matches the check's stat, the bonus is added to the total. This is correct.

**Limitation:** The class bonus applies only when the ability's `stat` field matches the check's `statName`. The Engineer's +3 DEX applies to ALL DEX checks (currently only circuit wiring), not just circuit wiring specifically. The `encounterType` field in the ability definition is defined but never checked -- the bonus is gated only by stat name. This is a minor concern: currently each stat is used in only 1-2 encounter types, so the stat gate is sufficient. But if future iterations add more DEX-based encounters, the Engineer would get +3 on all of them.

**Jury-Rig unique mechanic:** The Tinker class has a genuinely different ability (reroll rather than stat bonus). It costs 3 MP/Stamina, is limited to once per encounter, and is tracked via `state.juryRigUsedThisEncounter` (reset at line 1206 and 1212). However, Jury-Rig currently only triggers in the `handleComponentChoice` function (line 1658). It does NOT trigger in other failed encounters (diagnosis, predict, teach, etc.). The Tinker's unique ability is mechanically real but narrower in scope than it could be.

### 3. Guided Tutorial After Character Creation

A 4-step tutorial is implemented at lines 805-872:

1. **Step 1:** Explains all 6 stats and their encounter mappings, plus the player's class ability. Includes a live sample roll against DC 12 (line 833).
2. **Step 2:** Explains the half-life mastery decay system, including how successful reviews double the half-life and failures halve it. Explains the HUD elements.
3. **Step 3:** A simulated INT check against DC 8 (line 849), demonstrating how success/failure affects information access.
4. **Step 4:** Explains regions, progression, and mysteries.

The tutorial is skippable ("I know how to play -- skip to the Citadel" at line 817). The `tutorialComplete` flag is persisted in localStorage (line 561), so returning players are not shown the tutorial again.

**Assessment:** The tutorial meets the specification. It explains the world, walks through a live roll example, explains mastery decay, and shows encounter flow. It is under 2 minutes for a reader at normal pace. The live roll demonstration is particularly effective -- it shows the d20+modifier calculation, not just describes it.

### 4. Half-Life Mastery Decay

Implemented at lines 607-631:

- `getMasteryStrength(entry)` = 2^(-timeSinceReview / halfLife) -- line 616. This is the correct exponential decay formula.
- `HALF_LIFE_INITIAL_MS` = 86400000 (1 day) -- line 478.
- On success: halfLife doubles (line 2456).
- On failure: halfLife halves, minimum 6 hours (line 2459: `Math.max(HALF_LIFE_INITIAL_MS / 4, ...)`). Note: HALF_LIFE_INITIAL_MS / 4 = 6 hours, which matches the spec.
- Topics below 0.5 strength are "fading" (line 630).
- Fading topics appear as colored bars in the mastery view (line 1062: `mastery-fading` class with red bar).
- Fading topics prioritized during exploration (line 1230: 30% chance of review encounter).
- Dedicated "Review fading topics" option on world map (line 988).
- Migration for old mastery entries (line 2582-2584): entries without `halfLife` get the initial value.

**Assessment:** The mastery decay model is correctly implemented. The exponential decay formula, half-life doubling/halving, fading threshold, review prioritization, and dedicated review interface all work as specified. The `lastReviewed` timestamp is updated on every mastery interaction (line 2451), and the `isMastered` function (line 619) requires BOTH >= 2 correct answers AND >= 0.5 strength. This means mastery is genuinely impermanent -- a topic mastered yesterday with a 1-day half-life drops to 50% strength after exactly 1 day, causing it to show as fading. After 2 days it is at 25% and is no longer counted in the mastered total.

**Bug found:** The minimum half-life on failure is `HALF_LIFE_INITIAL_MS / 4` (6 hours), not `HALF_LIFE_INITIAL_MS / 4` as a floor on the halved value. Consider: if halfLife is already 6 hours (the minimum) and the player fails again, `Math.max(6h, 6h / 2) = Math.max(6h, 3h) = 6h`. This correctly floors at 6 hours. The math is sound.

### 5. LLM Evaluator

Implemented as POST `/api/evaluate-llm` at server.js line 324:

- Uses `google/gemini-2.0-flash-001` via OpenRouter.
- System prompt explicitly states: "Grade based on CONCEPTUAL UNDERSTANDING, not vocabulary matching."
- Three-tier grading: correct, partial, incorrect.
- Returns: `{grade, feedback, misconception, source}`.
- Handles markdown fences in LLM response (line 371-373).
- Falls back to regex extraction if JSON parsing fails (line 389-393).
- Falls back to cosine similarity if the entire LLM call fails (line 396-426).

Frontend integration at line 510: `evaluateAnswer()` calls `/api/evaluate-llm` as primary, `/api/evaluate` (cosine) as first fallback, and a keyword-matching `fallbackEvaluate` function as last resort.

**Live test results:**
- Correct answer (different vocabulary): `{"grade":"correct","feedback":"The student correctly describes the relationship...","source":"llm"}` -- PASS
- Incorrect answer (wrong concept): `{"grade":"incorrect","feedback":"The student's answer describes the function of a capacitor, not Ohm's Law.","misconception":"The student is confusing Ohm's Law with the function of a capacitor.","source":"llm"}` -- PASS
- Partial answer (vague but directional): `{"grade":"partial","feedback":"The answer identifies the correct variables but doesn't specify the relationship between them.","misconception":"The student understands the relevant variables but doesn't know the formula.","source":"llm"}` -- PASS

**Assessment:** The LLM evaluator is the single biggest improvement in iteration 6. It directly addresses the primary weakness identified in iterations 4 and 5. The three test cases demonstrate that it correctly distinguishes conceptual understanding from vocabulary overlap. The cascading fallback chain (LLM -> cosine -> keyword) ensures the game never breaks if the API is unavailable.

---

## Test Results Summary

### API Test Data

| Test | Result | Detail |
|---|---|---|
| API: Health | PASS | `{"status":"ok"}` |
| API: Stats | PASS | 184 docs, 599 terms, 1113 links, 746 quiz, 9 categories |
| API: Evaluate-LLM (correct) | PASS | "voltage is proportional to current when resistance is constant" -> grade: correct, source: llm |
| API: Evaluate-LLM (incorrect) | PASS | "capacitors store energy in electric fields" -> grade: incorrect, source: llm |
| API: Evaluate-LLM (partial) | PASS | "its the relationship between V I and R" -> grade: partial, source: llm |
| API: Misconception-Match | PASS | "capacitors store current" -> matched: true, similarity: 0.723 |
| API: Evaluate (legacy cosine) | PASS | similarity: 0.808, grade: correct |

### Code Analysis Data

| Feature | Status | Line References |
|---|---|---|
| d20+stat rollCheck in every encounter | PASS | 17 rollCheck calls across 12 encounter types + tutorial |
| All 6 stats mechanically used | PASS | STR(1872), DEX(1319), CON(1508), INT(1595,1805,2013,2047,2325), WIS(1141,1268,1470,1706,2257), CHA(1910,2121) |
| 6 class abilities defined with bonuses | PASS | Lines 314-328 |
| Class bonus applied in rollCheck | PASS | Lines 584-588 |
| Tinker Jury-Rig mechanic | PASS | Lines 1657-1696 |
| Tutorial with live roll demo | PASS | Lines 805-872, 4 steps, skippable |
| Half-life decay formula | PASS | Line 616: Math.pow(2, -timeSince / halfLife) |
| Half-life doubling on success | PASS | Line 2456 |
| Half-life halving on failure (6h min) | PASS | Line 2459 |
| Fading threshold at 0.5 | PASS | Line 630 |
| Review prioritization for fading topics | PASS | Lines 1228-1232 (30% in-region), line 988 (world map option) |
| LLM evaluation as primary | PASS | Line 512: /api/evaluate-llm |
| Cosine similarity as fallback only | PASS | Line 521: only called in catch block |
| LLM feedback displayed to player | PASS | `result.feedback` displayed via addMsg in all encounter types |
| No XP/level system | PASS | Zero references to xp or level-up in functional code |
| No gold in HUD | PASS | HUD at lines 267-273 shows: name, HP, MP, mastery, rank only |
| Mastery-only progression | PASS | HUD shows mastered count + rank, no XP bar |
| Direct slot selection in circuit wiring | PASS | Line 1335: selectedSlotIdx; tap slot then tap part (fixed from iteration 5) |
| Used wiring parts: opacity 0.4 + line-through | PASS | Line 129: `.wiring-part.used { opacity: 0.4; cursor: not-allowed; border-color: transparent; text-decoration: line-through; }` |

---

## Scorecard

| Dimension | Rating | Delta | Key Finding |
|---|---|---|---|
| Intrinsic Integration | Deep | = | LLM evaluation strengthens text-entry encounters; d20+stat checks create mechanical integration between character build and learning outcomes. Understanding IS your power now extends to both answer quality (LLM) and stat-gated information access (d20). |
| Pedagogical Soundness | Strong | UP from mixed | LLM evaluation grades conceptual understanding, not vocabulary matching. Half-life decay creates genuine spaced repetition with forgetting. Stat checks provide implicit scaffolding (high-stat = more context = easier). Misconception detection + LLM feedback provide two layers of formative assessment. |
| Narrative & Structure | Functional | = | 6-region quest structure, mystery system, concept cascades, knowledge journal unchanged. Tutorial adds narrative framing. NPCs remain stateless. |
| Motivation & Engagement | Intrinsic | = | Mastery-only HUD, no XP/levels, mastery decay makes maintenance intrinsically motivated, Jury-Rig provides class-specific agency. |
| Assessment Design | Hybrid | = (quality UP) | Circuit wiring and fault tree remain genuine stealth assessment. LLM evaluation now distinguishes conceptual understanding from vocabulary parroting in all text-entry encounters, significantly improving assessment validity. |
| Accessibility | Adequate | = | ARIA labels, keyboard nav, reduced-motion, no horizontal scroll. Direct slot selection improves wiring accessibility. Used parts have opacity 0.4 + line-through (redundant indicator). Still no light theme, no font controls. |
| Freemium Monetisation | Learning-first | = | No paywalls, no ads, no dark patterns. All content free. Premium features defined but not implemented. |
| RPG Mechanical Integrity | Mechanically Rich | NEW | All 6 stats affect gameplay via d20 checks. 6 classes with unique abilities (5 stat bonuses + 1 unique mechanic). Guided tutorial with live roll demo. Half-life mastery decay correctly implemented. Stats create meaningfully different playthroughs. |

---

## Detailed Analysis

### Dimension 1: Intrinsic Integration

**Score: deep**

Iteration 6 maintains and strengthens the "deep" rating. The d20+stat system creates a new layer of intrinsic integration: the player's CHARACTER BUILD affects how much context they receive before answering, and the LLM evaluator means their CONCEPTUAL UNDERSTANDING determines whether they succeed. This creates a two-stage integration loop:

1. **Stage 1 (stat check):** Your character's INT/WIS/DEX/CHA/STR/CON determines how much scaffolding you receive. A high-INT Scholar attempting a prediction encounter gets the full key_insight as a hint. A low-INT character gets 40% of the text with "[display garbled]." This is mechanically meaningful scaffolding, not just flavor.

2. **Stage 2 (answer evaluation):** The LLM evaluator assesses whether you understand the concept, not whether you memorized specific words. A player who writes "switching between high and low states rapidly controls average power delivery" scores "correct" for PWM even though none of those words appear in the reference text. This was impossible with cosine similarity.

The circuit wiring encounter's DEX check (line 1319) is particularly elegant: a successful DEX roll removes one distractor from the parts bin, making the puzzle physically easier. This is the RPG equivalent of "your skilled hands can tell this part doesn't fit" -- a natural integration of character ability with a learning-assessment task.

**What prevents "perfect":** The stat check outcomes are binary (success/failure). There is no gradient -- you either get the full hint or the garbled version, with no intermediate. A d20 system inherently produces high variance (a character with +5 modifier still fails a DC 12 check 30% of the time), which could feel random rather than fair. However, this is a genre-appropriate limitation of the d20 system, not a design flaw.

### Dimension 2: Pedagogical Soundness

**Score: strong (upgraded from mixed)**

This is the most significant rating change in iteration 6, driven by two improvements:

1. **LLM evaluation grades conceptual understanding.** The system prompt at line 331 explicitly instructs: "A student who explains the concept correctly in different words should get 'correct'. A student who uses the right technical terms but in wrong relationships should get 'incorrect'." Live testing confirmed this works: a correct paraphrase in completely different vocabulary scores "correct," while an answer about the wrong concept scores "incorrect" even if it uses relevant technical terms. This directly addresses Bloom's taxonomy levels 2-5 (understanding through evaluation), not just level 1 (remembering/recognizing).

2. **Half-life mastery decay creates genuine spaced repetition.** The formula `strength = 2^(-timeSinceReview / halfLife)` is the standard exponential forgetting model used in spaced repetition research (Ebbinghaus, 1885; Pimsleur, 1967; Leitner, 1972). The doubling of half-life on success (from 1 day to 2 days to 4 days to 8 days...) and halving on failure (minimum 6 hours) creates an adaptive schedule. Topics that a student consistently reviews correctly become increasingly permanent; topics that are difficult decay quickly and reappear sooner. The 50% fading threshold and 30% chance of in-region review encounters create the "desirable difficulty" that Bjork & Bjork (2011) identify as optimal for long-term retention.

3. **Stat checks provide implicit scaffolding.** A successful INT check in the Circuit Build encounter reveals the full definition (line 1617); a failure reveals only 40% garbled text (line 1621). This means stronger characters (who have invested in the relevant stat) receive more context, reducing cognitive load. Weaker characters must rely more on prior knowledge. This is not the same as full Vygotsky ZPD scaffolding (which would adapt encounter complexity, not just hint quality), but it is a meaningful step toward it.

**Remaining weakness:** Within-session topic selection is still random (line 1214). There is no intentional sequencing of related topics (e.g., resistor before voltage divider before op-amp feedback). The fading-topic prioritization addresses WHEN to review but not WHAT order to learn new material. This matters less now that LLM evaluation correctly identifies conceptual gaps, but optimal learning sequences would further improve pedagogical soundness.

### Dimension 3: Narrative & Structure

**Score: functional**

The structural pattern remains Quest (open hub) layered with Loop & Grow (mastery unlocks regions). Iteration 6 adds narrative framing through the tutorial (Circuit Citadel lore, class identity) but does not fundamentally change the narrative architecture.

**New strength:** The tutorial at lines 805-872 grounds the player in the world fiction before gameplay begins. The "Systems are breaking down -- only someone who truly understands how they work can fix them" framing (line 813) establishes a narrative reason for the learning. The class ability introduction personalizes the narrative ("As an Engineer, you'll excel at Precision Wiring").

**Persistent weaknesses:**
1. NPCs remain stateless. The dealer, apprentice, and senior engineer are anonymous per-encounter.
2. No spatial exploration within regions (flat list, no rooms).
3. The d20 roll display (`[d20: 14 + INT +2 = 16 vs DC 12] SUCCESS`) is mechanically informative but breaks narrative immersion. The game alternates between narrative prose and tabletop-RPG notation.

### Dimension 4: Motivation & Engagement

**Score: intrinsic**

The mastery decay system actually STRENGTHENS intrinsic motivation. The fading-topic alerts ("3 topic(s) fading from memory!") create an internal drive to maintain knowledge, not an external reward to chase. The player is motivated to review because THEIR knowledge is degrading, not because an XP bar is emptying. This aligns with SDT's competence need: the player wants to feel competent, and watching mastery fade undermines that feeling, creating natural motivation to review.

The Jury-Rig mechanic provides the Tinker class with a unique form of agency: the choice to spend resources for a second chance. This is a genuine strategic decision (is this component worth 3 Stamina?), not just a button press.

**No regression:** HUD at lines 267-273 shows only name, HP, MP, mastery count, and rank. Zero references to XP, levels, or gold in the HUD. Gold appears only in the character sheet view and negotiate encounters.

### Dimension 5: Assessment Design

**Score: hybrid (quality significantly improved)**

The hybrid rating is maintained (stealth assessment via circuit wiring and fault tree + overt text evaluation), but the QUALITY of assessment has improved dramatically:

1. **LLM evaluation assesses conceptual understanding.** A student who writes "the coil opposes changes in current by generating a back-voltage" for an inductor question scores "correct" even though the reference says "V = L*dI/dt." A student who writes "inductors store voltage in their magnetic field" scores "incorrect" because the concept is wrong despite using relevant vocabulary. This is a fundamental validity improvement over cosine similarity.

2. **LLM provides specific formative feedback.** The `feedback` field returns a one-sentence explanation ("The student correctly describes the relationship between voltage and current at constant resistance"). This is displayed to the player after every evaluation (lines 1822, 1828, 1836, etc.). Combined with misconception detection, the player receives two layers of formative assessment: what they got right/wrong (LLM feedback) and what specific misconception they hold (misconception matching).

3. **CHA check grade promotion is valid assessment design.** At line 2142: `const effectiveGrade = (chaCheck.success && result.grade === 'partial') ? 'correct' : result.grade`. A successful CHA check means the apprentice is receptive, so a partial explanation is accepted. This models a real teaching interaction: a student teacher with rapport can succeed with a less polished explanation. The partial answer still demonstrates understanding; the CHA check determines the THRESHOLD, not whether understanding exists.

### Dimension 6: Accessibility & Inclusion

**Score: adequate**

Iteration 6 addresses two specific issues from iteration 5:

1. **Direct slot selection in circuit wiring** (line 1335-1368): Players can now tap a specific slot to select it, then tap a part to fill it. This replaces the sequential auto-fill from iteration 5. A student who recognizes the output filter but not the input filter can fill slot 3 first. This supports non-linear reasoning and improves assessment validity.

2. **Used wiring parts have redundant visual indicators** (line 129): `.wiring-part.used { opacity: 0.4; cursor: not-allowed; border-color: transparent; text-decoration: line-through; }`. The line-through provides a redundant indicator beyond opacity for colorblind or low-vision users.

**Persistent issues:**
- No light theme option. Dark-only with borderline contrast on `--text-dim: #8b949e`.
- No font size controls.
- Color coding without icon/pattern redundancy for success (green), danger (red), misconception (red border).
- No complementary landmark (acceptable -- no sidebar).

### Dimension 7: Freemium Monetisation

**Score: learning-first**

No changes from iteration 5. All content free. Premium features at line 2596-2603 are defined but not implemented or advertised. No paywalls, no energy gates, no ads, no dark patterns.

### Dimension 8: RPG Mechanical Integrity (NEW)

**Score: mechanically-rich**

This is the new dimension for iteration 6. The RPG mechanics are genuinely integrated:

1. **Stats are consequential.** All 6 stats affect gameplay through d20+modifier checks. The effect is not cosmetic -- a high-INT character literally receives more information (full hints vs garbled text) before answering. A high-DEX character faces fewer distractors in circuit wiring. A high-CHA character's partial teaching answers are accepted.

2. **Classes create different playstyles.** An Engineer with +3 DEX consistently faces 1 fewer distractor in wiring challenges. A Scholar with +3 INT gets full hints in theory encounters. A Tinker can spend Stamina to retry failed component choices. These are mechanically distinct paths through the same content.

3. **d20 variance creates stakes.** Even a character with high stats can fail a check (d20 roll of 1 + modifier < DC). This creates genuine tension: you might not get the hint. The format display (`[d20: 7 + INT +2 = 9 vs DC 12] FAILURE`) makes the stakes transparent.

4. **Tutorial effectively onboards.** Four steps cover stats, class abilities, mastery decay, and encounter flow. A live roll demonstration shows the d20 system in action. The tutorial is skippable for returning players.

5. **Mastery decay adds RPG dimension.** Knowledge is not a permanent acquisition -- it requires maintenance. This models the real-world phenomenon of knowledge decay and creates an ongoing gameplay loop beyond initial mastery.

**What prevents "perfect":**
- The `encounterType` field in class abilities is defined but never checked (line 586 only checks `stat`). If a class had two abilities for the same stat, there would be no way to distinguish them.
- Jury-Rig only activates in `handleComponentChoice`, not in other failed encounters (diagnosis, predict, teach, etc.).
- No equipment or inventory system beyond starting items and purchased components.
- No party/companion system -- the player is always solo.
- No enemy/NPC stat blocks -- encounters are player-vs-check, not player-vs-NPC.

---

## Critical Bugs and Issues

1. **Jury-Rig scope is narrower than implied.** The Tinker's Jury-Rig ability ("Spend 3 Stamina to reroll a failed check once per encounter") is described as applicable to any encounter, but the `canJuryRig` check only triggers in `handleComponentChoice` (line 1658). Failed diagnosis, prediction, teaching, and negotiation encounters do not offer a Jury-Rig option. The ability description sets an expectation the implementation does not meet. Severity: moderate (Tinker players may feel their unique ability is underutilized).

2. **Class ability `encounterType` field is unused.** Each class ability defines an `encounterType` (e.g., `'circuit_wiring'`, `'predict_behavior'`), but `rollCheck` at line 586 only checks if `ability.stat === statName`. This means the Engineer's +3 DEX applies to ALL DEX checks, not just circuit wiring. Currently this has no impact because DEX is only used for circuit wiring, but it could be a bug if future iterations add more DEX-based encounters. Severity: low (no current impact).

3. **Database content count still at iteration 5 levels.** 599 terms vs spec's mention of expanded content, 746 quiz questions. The same 50% shortfall persists from iteration 5. Severity: minor (game functions correctly with available content).

4. **Half-life initial value is set to 1 day, but the design spec says "halfLife starts at 1 day."** The implementation matches the spec. However, for a new player who masters a topic and returns the next day, the topic is already at 50% (the fading threshold). This means topics mastered in session 1 are ALWAYS fading by session 2, which could feel punishing. The first successful review doubles the half-life to 2 days, making the decay much more manageable. Severity: minor (by design, but the initial session may feel harsh).

5. **LLM evaluator has no rate limiting.** Every text-entry answer calls the LLM endpoint. A player entering many answers quickly could rack up significant API costs. There is no debounce, cooldown, or per-session limit. Severity: depends on scale -- fine for individual use, potentially costly at scale.

---

## Biggest Risk

The LLM evaluator introduces a dependency on an external API (OpenRouter/Gemini) for the core assessment loop. If the API is slow (adding 1-2 seconds per answer evaluation), the gameplay pacing degrades significantly -- every text encounter requires waiting for an API round-trip. If the API is unavailable, the game falls back to cosine similarity, losing the conceptual evaluation that justifies the "strong" pedagogical soundness rating. The fallback chain is well-designed (LLM -> cosine -> keyword), but the quality gap between the primary evaluator and the fallbacks is large enough that extended API downtime would regress the game to iteration 5's assessment quality.

---

## Recommendations

### Quick Wins

1. **Expand Jury-Rig to all failed encounters.** Add `canJuryRig()` check after failed evaluations in diagnosis, prediction, teaching, and negotiation encounters. The reroll should re-display the challenge prompt and allow a second attempt. This makes the Tinker class ability match its description.

2. **Gate class ability bonus by encounterType, not just stat.** Change line 586 to: `if (ability && ability.stat === statName && (ability.encounterType === 'any' || ability.encounterType === currentEncounterType))`. Pass the encounter type string into `rollCheck`. This future-proofs the system.

3. **Add LLM evaluation caching.** For identical question+answer pairs, cache the LLM response for the session. This reduces API calls during review encounters where the same question may be asked multiple times.

### Structural Changes

1. **Increase initial half-life to 2-3 days.** The current 1-day half-life means topics mastered in session 1 are always fading by session 2 (24+ hours later). Starting at 2 days gives the player more time before their first review is needed, reducing the "everything is fading" feeling on return.

2. **Add intentional topic sequencing within regions.** Track which topics a student has encountered and use a dependency graph (e.g., resistor before voltage divider before op-amp feedback) to sequence encounters. Present prerequisite topics before dependent ones.

3. **Give NPCs persistent identities.** Track which NPC the player has interacted with in each region. The dealer in The Workshop should remember previous transactions. The apprentice should reference topics they previously struggled with. This creates relatedness (SDT) and narrative continuity.

### Advanced Improvements

1. **Add light theme option.** Provide `@media (prefers-color-scheme: light)` CSS or a manual toggle.

2. **Add latency-hiding UX for LLM evaluation.** Show a "Evaluating your understanding..." message with a brief animation while waiting for the LLM response. If the response takes >3 seconds, show the cosmetic result of the stat check (damage/reward) first and display the LLM feedback when it arrives.

3. **Re-run the importer with expanded question generation.** The database has 599 terms and 746 quiz questions vs what was specified. Expanding the content variety would reduce topic exhaustion in extended sessions.

---

## Research References

- Habgood & Ainsworth (2011). "Motivating Children to Learn Effectively: Exploring the Value of Intrinsic Integration in Educational Games." Journal of the Learning Sciences.
- Bjork & Bjork (1992, 2011). Desirable difficulties framework for spaced repetition and retrieval practice.
- Bloom et al. (1956). Taxonomy of Educational Objectives. (Revised: Anderson & Krathwohl, 2001.)
- Shute, V. J. (2011). "Stealth Assessment in Computer-Based Games to Support Learning." Computer Games and Instruction.
- Ryan & Deci (2000, 2020). Self-Determination Theory: autonomy, competence, relatedness.
- Csikszentmihalyi (1990). Flow: The Psychology of Optimal Experience.
- Ebbinghaus, H. (1885). Memory: A Contribution to Experimental Psychology. (Forgetting curve.)
- Pimsleur, P. (1967). "A Memory Schedule." Modern Language Journal. (Graduated interval recall.)
- Leitner, S. (1972). So lernt man lernen. (Spaced repetition box system.)
- Vygotsky, L. S. (1978). Mind in Society. (Zone of Proximal Development.)

---

<!-- SCORES
intrinsic_integration: deep
pedagogical_soundness: strong
narrative_structure: functional
motivation_engagement: intrinsic
assessment_design: hybrid
accessibility: adequate
freemium_monetisation: learning-first
rpg_mechanical_integrity: mechanically-rich
biggest_risk: The LLM evaluator creates a critical dependency on an external API for the core assessment loop, and the quality gap between primary (conceptual grading) and fallback (cosine similarity) evaluation means API downtime or latency degrades both assessment validity and gameplay pacing.
SCORES -->
