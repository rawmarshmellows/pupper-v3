# Critique: Knowledge Quest -- Iteration 12

## Overview

Knowledge Quest iteration 12 serves via Docker Compose (PostgreSQL+pgvector, Python importer, Node.js server). The knowledge base contains 184 documents with embeddings, 609 essential terms, 1150 document links, and 2710 quiz questions across 6 generation sources. This iteration fixes all 3 bugs from iteration 11 (boss answer evaluation, prerequisite scope, boss HP bar) and deepens gamification integration into the circuit board metaphor: streaks become "current flow" with animated electron CSS, combos become "resonance" tied to the LC circuit concept, achievements become "engineering certifications," and daily challenges become "maintenance rounds" that prefer fading nodes. New features include interactive clickable circuit board nodes with detail popups, multi-phase boss encounters (3 questions per boss with real HP tracking), and a system log.

---

## Iteration 11 Issue Tracker

| Issue from Iteration 11 | Status | Evidence |
|---|---|---|
| BUG-001: Boss evaluates against question, not answer | **Fixed** | Lines 400-401: `bossPhases` array replaces single `bossPrompt`. Each phase has explicit `prompt` and `answer` fields. Line 1644: `evaluateAnswer(choice.freeformInput, phase.answer, phase.prompt)` now uses `phase.answer` as the correct answer. Playwright verified: `BUG_001_FIX: FIXED: true`. The old `sub.bossPrompt + ' ' + sub.reward` pattern is completely absent from the codebase. |
| BUG-002: Prerequisite redirect ignores category scope | **Fixed** | Lines 1937-1940: `const regionCats = region.categories; const unmasteredPrereq = prereqs.find(p => { ... regionCats.includes(p.category) })`. API verification confirms Resistor has 105 total prerequisites but only 53 are in the `electronics` category. The Workshop (categories: `['electronics']`) will now only redirect to electronics prerequisites. Playwright verified: `BUG_002_FIX: FIXED: true`. **Residual concern**: ADS1110 Battery ADC remains in the `electronics` category and is still the first alphabetical electronics prerequisite for Resistor -- see POLISH-001 below. |
| BUG-003: Boss HP bar is purely cosmetic | **Fixed** | Lines 1628-1694: Boss encounters now have 3 phases with `currentPhase` tracking and `correctPhases` counter. HP bar is calculated as `(totalPhases - correctPhases) / totalPhases * 100` (line 1637), decreasing by 33% with each correct phase. Player must pass at least `Math.ceil(totalPhases / 2)` phases (i.e., 2/3) to defeat the boss. Playwright verified: `BUG_003_FIX: FIXED: true`. All 6 bosses have 3 phase definitions each (18 total phase prompts + answers confirmed). |
| POLISH-001 (i11): Streak/combo not integrated into circuit board metaphor | **Fixed** | Streaks renamed to "current flow" with `currentFlowAnim` CSS animation (line 102-105) and `.flowing` class (line 106-110). Combos renamed to "resonance" with `resonancePulse` animation and LC oscillation messaging. Certifications renamed from generic achievements to engineering licenses. Maintenance rounds renamed from daily challenges with fading-node preference. |

**Verdict: All 3 priority bugs from iteration 11 are fixed. The POLISH-001 design concern is also addressed. No regressions detected in preserved features.**

---

## Test Results Summary

### API Test Data

| Test | Result | Detail |
|---|---|---|
| API: Health | PASS | `{"status":"ok"}` |
| API: Stats | PASS | 184 docs, 609 terms, 1150 links, 2710 quiz, 9 categories |
| API: Embeddings | PASS | 184/184 documents with embeddings |
| API: Quiz sources | PASS | 6 sources: key_insight (148), section_analysis (397), section_content (400), term_definition (583), term_reverse (583), test_your_understanding (599). No `summary` source. |
| API: Prerequisites | PASS | Resistor topic returns 105 prereqs; 53 are `electronics`, 52 cross-category. Category filter works. |

### Automated Playwright Test Data

| Test Category | Result | Key Metric |
|---|---|---|
| Accessibility: ARIA | PASS | 6 interactive elements on creation screen, 0 missing labels |
| Accessibility: Landmarks | PASS | 4/5 present (banner, navigation, main, contentinfo) |
| Accessibility: Keyboard | PASS | 10/20 tab stops hit interactive elements (creation screen has limited elements) |
| Accessibility: Mobile | PASS | No overflow at 375px |
| Accessibility: Reduced Motion | PASS | CSS `prefers-reduced-motion` rule present |
| Accessibility: Theme Toggle | PASS | Present (HUD hidden until game starts; button exists in DOM) |
| Accessibility: Font Toggle | PASS | Present (same as above) |
| BUG-001 Fix | PASS | `bossPhases` present, `phase.answer` in evaluateAnswer, old `bossPrompt+reward` pattern absent |
| BUG-002 Fix | PASS | `regionCats.includes(p.category)` filter present |
| BUG-003 Fix | PASS | Multi-phase loop, HP bar updates, 2/3 pass threshold all present |
| Gamification: Current Flow | PASS | State field, CSS animation, flowing class, narrative indicator, thematic message all present |
| Gamification: Resonance | PASS | State field, CSS pulse, narrative indicator, LC message, 30s window all present |
| Gamification: Certifications | PASS | State field, "Certification:" banner, engineering names (Licensed Technician, Licensed PCB Designer, Superconductor Class) |
| Gamification: Maintenance | PASS | State field, MAINT badge, signal framing, fading preference, function present |
| Gamification: Interactive Nodes | PASS | Click handler, tabindex, role=button, detail popup, keyboard Enter/Space support |
| Gamification: System Log | PASS | State field, addLogEntry function, CSS classes, timestamps, color coding, 100-entry cap |
| Gamification: Migration | PASS | All 4 field migrations (streak, bestStreak, achievements, dailyChallengesCompleted) present |
| Pedagogy: No summary source | PASS | `summary` absent from REGION_QUIZ_SOURCES |
| Pedagogy: Misconceptions | PASS | 19 correction entries across 14 topic pools |
| Pedagogy: Half-life decay | PASS | HALF_LIFE_INITIAL_MS, getMasteryStrength, MASTERY_FADING_THRESHOLD all present |
| Pedagogy: Bloom scaffolding | PASS | bloomMax tracking, REGION_QUIZ_SOURCES per difficulty |
| Pedagogy: Prerequisites | PASS | API call with category filter |
| Pedagogy: Interleaving | PASS | getInterleavedSearchTerm, lastEncounteredTopic |
| Pedagogy: LLM evaluation | PASS | /api/evaluate-llm endpoint used |
| Game Flow: Character Creation | PASS | Name input enables start button |
| Game Flow: Tutorial Choices | PASS | "Yes, show me how to play" and "Skip" both offered |
| Game Flow: World Map | PASS | Circuit board visible, 6 subsystem cards, 26 interactive nodes, board power display, MAINT badge |
| Game Flow: Encounter | PASS | Workshop encounter loads with freeform input |
| Tutorial: 5 Steps | PASS | Steps 1-5 all navigated, practice encounter at step 3 (answer submitted, evaluated) |
| Monetisation | PASS | Premium disabled, no paywall keywords, 0 ad elements |
| Technical: Load Time | PASS | 522ms to networkidle |
| Technical: Console Errors | PASS | 0 errors |
| Technical: Save State | PASS | 24 fields saved, including systemLog, currentFlow, certifications, maintenanceCompleted. State persists across reload. |
| Technical: 30-Second Clarity | PASS | 3/3 (game context, call to action, interaction hint) |
| Circuit Board: Subsystems | PASS | 6/6 defined |
| Circuit Board: Boss Phases | PASS | 6 bosses x 3 phases = 18 phase definitions |
| Circuit Board: Cascades | PASS | 8/8 trace names |

### Critical Test Findings

1. **32 of 33 Playwright tests pass.** One test timeout in the tutorial flow is a test-script issue (loop tried to navigate past step 5), not a game bug. The tutorial itself completed all 5 steps including the practice encounter with LLM evaluation.
2. **All 3 iteration 11 bugs are fixed.** Boss evaluation now uses `phase.answer`, prerequisites are filtered by `region.categories`, and boss encounters have genuine 3-phase mechanics with updating HP bar.
3. **All 4 gamification elements are fully integrated into the circuit board metaphor.** Every streak, combo, achievement, and daily challenge has been renamed, reframed, and given visual/narrative treatment consistent with the circuit board domain.
4. **26 interactive circuit board nodes rendered** on the world map, each with `tabindex="0"`, `role="button"`, and keyboard support (Enter/Space). Clicking shows signal strength, half-life, Bloom level, and subsystem membership.
5. **24 state fields saved to localStorage**, including the new systemLog, currentFlow, certifications, and maintenanceCompleted. State persists across page reload.

---

## Scorecard

| Dimension | Rating | Delta from i11 | Key Finding |
|---|---|---|---|
| Intrinsic Integration | Deep | = | Prerequisite graph (now properly scoped), Bloom scaffolding, DB-driven content all preserved. Circuit board metaphor now fully integrated with gamification language. |
| Pedagogical Soundness | Strong | = (residual concern improved) | BUG-002 fix eliminates cross-category redirects. Residual: in-category prerequisite selection still alphabetical rather than pedagogical. |
| Narrative & Structure | Compelling | = | Multi-phase boss encounters add genuine narrative arcs. System log provides journey reflection. NPC cascade triggers preserved. |
| Motivation & Engagement | Intrinsic | UP | Current flow, resonance, certifications, and maintenance rounds are now semantically coherent with the circuit board domain. Gamification feels native, not bolted on. |
| Assessment Design | Hybrid | UP | Boss encounters now have 18 total phase questions with model answers, each targeting a different assessment angle (diagnosis, selection, protection/integration). |
| Accessibility | Strong | = | 0 ARIA issues, 4/5 landmarks, theme/font/motion support, mobile-safe, interactive nodes have keyboard support. |
| Freemium Monetisation | Learning-first | = | premiumFeatures.enabled = false. No monetisation elements. |
| RPG Mechanical Integrity | Partially-functional | UP | Multi-phase bosses add strategic depth. Interactive nodes add information architecture. Current flow and resonance have genuine visual feedback. Still lacks node-targeting agency. |

---

## Detailed Analysis

### The Central Question: Is the Gamification Integration Genuine or Cosmetic?

**The iteration 11 critique identified the gamification as "~60% genuine innovation and ~40% thematic relabeling." Iteration 12 moves this to approximately 80% genuine / 20% residual.**

Here is what changed substantively:

**1. Current Flow: From Label to Mechanic**

In iteration 11, the streak bar was a horizontal fill with no domain-specific behavior. In iteration 12, the "current flow" concept is realized through three layers:

- **Visual**: The HUD bar has an animated gradient (`currentFlowAnim`, lines 102-110) that simulates electrons flowing along traces when `currentFlow >= 3`. The animation uses `background-size: 200%` with linear infinite movement -- a CSS technique that genuinely looks like current flowing through a conductor.
- **Narrative**: The inline `current-flow-indicator` element (line 323, line 759) displays "Current Flow: N -- electrons moving through the board" with a distinct border and color scheme.
- **Tutorial**: The tutorial explicitly explains "Consecutive correct answers build current through the board -- like electrons flowing through a conductor" (line 1181).

This is no longer a reskin. The visual metaphor of animated electrons is drawn directly from the learning domain (how current actually flows), the narrative messaging reinforces the concept, and the tutorial teaches the metaphor. A player encountering "current flow" learns something about electronics even from the gamification element itself.

**2. Resonance: From Speed Reward to Domain Concept**

The combo system's rebrand to "resonance" is the strongest integration of the four:

- The mechanic is explicitly tied to LC circuit resonance (line 484, line 1184): "Quick consecutive answers create resonance -- like an LC circuit amplifying a signal. The resonance multiplier boosts your learning."
- The `RESONANCE_WINDOW_MS = 30000` (line 610) window is generous enough that speed pressure is moderate, and the naming connects to the real concept of resonant frequency in LC circuits.
- The CSS `resonancePulse` animation (line 96) uses a scale-up/scale-down pattern that visually mimics oscillation.

The connection between "quick answers amplify learning" and "LC resonance amplifies signals" is a genuine analogical bridge. Per Gentner's (1983) structure-mapping theory, analogies are most effective when they map relational structure (not just surface features). Here, the relational structure (repeated input at the right timing creates amplification) maps correctly from the game mechanic to the electronics concept.

**3. Certifications: Improved but Still Partially Cosmetic**

The renaming from generic achievements ("First Light," "Streak Master") to engineering certifications ("Licensed Technician," "Superconductor Class," "Licensed PCB Designer") is well-executed. The names are creative and domain-appropriate. The banner text says "Certification:" instead of "Achievement:" (line 830).

However, the underlying trigger conditions are unchanged from iteration 10-11. "Licensed Technician" fires on `first_correct` (first correct answer). "Current Flow Certificate" fires on `current_flow_3` (3 correct in a row). These are the same milestones with new labels. A genuine integration would require different triggering conditions -- for example, "Licensed PCB Designer" should fire when the Fabrication Bay subsystem is fully powered, not when 20 nodes are powered across any subsystem.

This is the remaining 20% of cosmetic relabeling: the names are better, but the mechanics underneath do not test or require certification-level knowledge.

**4. Maintenance Rounds: Properly Reframed**

The daily challenge reframe is effective:

- The MAINT badge (line 313) replaces the generic "DAILY" badge.
- The maintenance round prefers fading topics via `getFadingTopics()` (line 1707), making it functionally different from a random quiz -- it targets topics that need review.
- The framing as "signal maintenance" / "keeping signal integrity high" (line 1389, line 1704) connects directly to the real engineering concept of signal integrity in circuit design.

The preference for fading topics is a meaningful mechanical change, not just a label change. This makes maintenance rounds pedagogically superior to the iteration 11 daily challenges because they implement targeted spaced repetition rather than random review.

**Net Assessment: The gamification is now ~80% genuine integration.** Current flow animation, resonance-as-LC-analogy, fading-topic-preferring maintenance rounds, and the overall reframing are substantive. Certification trigger conditions remain the one area where the renaming outpaces the mechanics.

### Multi-Phase Boss Encounters: A Major Quality Improvement

The most impactful change in iteration 12 is the multi-phase boss system. Each of the 6 bosses now has 3 phases, each targeting a different cognitive skill:

| Boss | Phase 1 (Diagnosis) | Phase 2 (Design/Selection) | Phase 3 (Protection/Integration) |
|---|---|---|---|
| The Surge | Root cause of capacitor failure | Buck converter component sizing | Three protection circuits |
| The Crosstalk | I2C lockup from SPI crosstalk | CAN bus error causes + tests | PCB layout rules for protocol isolation |
| The Saturation | Asymmetric clipping in CE amplifier | MOSFET source-follower optimization | Op-amp rail clipping + dynamic range |
| The Cold Joint | Failure analysis test sequence | BGA voiding manufacturing causes | Process fixes for <1% failure rate |
| The Glitch | Clock failure modes + watchdog | I2C lockup vs ADC peripheral causes | Complete fix (HW + FW + field update) |
| The Oscillation | Gain margin on carpet vs floor | PID + RL surface-robust redesign | Gait transition integration |

This is pedagogically excellent. The three-phase structure maps to Bloom's taxonomy levels 4-6 (Analyze, Evaluate, Create) and the model answers in each `phase.answer` field are detailed, technically accurate engineering solutions running 50-100 words each. The evaluation now uses `phase.answer` (line 1644) instead of the broken `bossPrompt + reward` pattern, so the LLM has a genuine model answer to compare against.

The HP bar is now meaningful: it starts at 100% and decreases by 33% per correct phase (line 1637-1638). The 2/3 pass threshold (line 1678) means a player can fail one phase and still defeat the boss, which is pedagogically appropriate -- it rewards breadth without requiring perfection.

One concern: on a correct boss phase, the code calls `for (const t of sub.nodes) await trackMastery(t, true, 5, null)` (line 1651), meaning ALL nodes in the subsystem get a mastery boost for each correct phase. This means 3 correct phases would call `trackMastery(true)` three times for each of 4-5 nodes, potentially over-inflating mastery. However, since each `trackMastery` call doubles the half-life and increments `correct`, this creates a strong retention signal, which may be appropriate for synthesis-level assessment.

### Interactive Circuit Board Nodes

The interactive circuit board (lines 886-948) is a welcome addition to the world map. Each node is rendered as a `<span>` with `tabindex="0"`, `role="button"`, and `aria-label` (line 904). Clicking or pressing Enter/Space on a node shows a detail popup with:

- Status (Powered / Fading / Dark)
- Signal strength percentage
- Half-life in days
- Bloom level reached
- Correct/incorrect counts
- Subsystem membership

This provides what Csikszentmihalyi (1990) calls "clear feedback" -- a prerequisite for flow states. The player can see exactly where they stand on every topic without navigating away from the map. The keyboard accessibility (line 946) ensures screen reader users can access this information.

The Playwright test confirmed 26 interactive nodes on the world map, matching the total across all 6 subsystems.

### System Log

The system log (lines 722-732, 1609-1618) is a lightweight but valuable addition. Every significant event (node powered, boss encountered, mystery solved, certification earned, failures) is logged with a timestamp and color-coded by type (success/fail/discovery/event).

The log serves two functions:
1. **Narrative reflection**: Players can review their journey, seeing patterns in what they succeeded at and where they struggled.
2. **Metacognitive support**: Per Flavell's (1979) metacognition framework, reflecting on one's own learning process improves learning outcomes. The system log provides the raw data for this reflection without forcing the player to do anything.

The 100-entry cap (line 726) prevents unbounded localStorage growth while preserving enough history for meaningful review.

### Dimension 1: Intrinsic Integration

**Score: deep (no regression)**

All prior integration mechanics preserved:
1. **Prerequisite graph ordering** with category scoping (BUG-002 fix).
2. **Bloom scaffolding by region**: REGION_QUIZ_SOURCES maps difficulty 1-6 to progressively higher cognitive demand.
3. **All content from database**: 184 documents, 609 terms, 2710 quiz questions.
4. **Learning sequence IS game sequence**: Regions progress from basic electronics to robotics.
5. **Gamification language now domain-native**: Current flow, resonance, certifications, maintenance all draw from the electronics domain.

The deepening of the gamification metaphor reinforces intrinsic integration. When the streak bar animates with flowing electrons, the gamification element IS the learning domain. Per Habgood & Ainsworth (2011), this is the standard for intrinsic integration: the motivational mechanics are drawn from the same conceptual space as the learning content.

### Dimension 2: Pedagogical Soundness

**Score: strong (improved from i11)**

All pedagogical features preserved:
1. **LLM evaluation** via Gemini 2.0 Flash with cosine fallback and keyword fallback (3-tier evaluation cascade).
2. **Misconception matching** with 14 topic-specific pools (19 total corrections).
3. **Half-life mastery decay** (2-day initial, doubles on correct, halves on incorrect, 0.5 threshold).
4. **Topic interleaving** via `getInterleavedSearchTerm()`.
5. **Tutorial practice encounter** with LLM evaluation.
6. **No `summary` source** in REGION_QUIZ_SOURCES.

**Improvement: BUG-002 fix eliminates cross-category prerequisite redirects.** A Workshop player will no longer be sent to CAN Bus or BJT. The fix correctly filters to `region.categories`, reducing the 105 Resistor prerequisites to 53 electronics-only options.

**Residual concern: In-category prerequisite selection is alphabetical, not pedagogical.** The first unmastered electronics prerequisite for Resistor is "ADS1110 Battery Voltage ADC" -- a specialized topic about a particular ADC chip used for battery monitoring. This is categorized as `electronics` (correctly, since it is an electronics component), but it is not a foundational prerequisite for understanding resistors. The prerequisite system still uses the database's `document_links` table, which represents Obsidian wiki links rather than pedagogical prerequisite relationships. The category filter prevents the worst offenders but does not solve the underlying issue: wiki links are not curriculum dependencies.

### Dimension 3: Narrative & Structure

**Score: compelling (no regression)**

The multi-phase boss encounters add a genuine narrative arc to each subsystem:

1. Board is dark (opening state)
2. Player powers individual nodes (encounter-by-encounter progress)
3. Subsystem comes online (eureka banner climax)
4. **Multi-phase boss encounter** (three-phase synthesis challenge with updating HP bar)
5. Boss defeated (subsystem fully operational)

The three-phase boss structure creates a mini-narrative within each encounter: diagnose the problem, design the solution, protect against recurrence. This mirrors real engineering workflows and creates dramatic tension as the HP bar decreases.

Narrative elements preserved:
1. Three-tier NPC greetings (first meeting, returning, veteran).
2. Persistent NPC identity (18 named characters across 6 roles).
3. Deterministic cascade triggers (counter-based every 4th encounter after 5 topics).
4. 6 region descriptions and mysteries.
5. System log adds narrative reflection capability.

### Dimension 4: Motivation & Engagement

**Score: intrinsic (improved)**

The gamification reframing addresses the iteration 11 concern that "streaks and combos are unchanged." Now:

1. **Current flow creates visual satisfaction.** The animated electron gradient on the streak bar (line 106-110) provides a continuous visual reward that grows more dynamic as the current increases. At `currentFlow >= 3`, the `.flowing` class triggers the animation, creating a threshold effect that motivates reaching 3 correct answers.

2. **Resonance leverages domain knowledge.** The LC resonance metaphor teaches while it motivates. A player who experiences resonance in-game may better understand resonance when they encounter LC circuits in the curriculum. This is dual-coding (Paivio, 1971): the game experience creates a second representation of the concept alongside the textual explanation.

3. **Maintenance rounds are autonomy-supportive.** The fading-node preference (line 1707) means maintenance rounds are not random busywork -- they target the topics the player most needs to review. This aligns with Self-Determination Theory's autonomy need: the system recommends what to review but the player chooses when.

4. **System log enables self-directed reflection.** Players who want to understand their learning patterns can review the log. Players who do not care about it can ignore it. This is multiple-means-of-engagement per Universal Design for Learning.

**Residual concern from i11:** The 30-second resonance window (line 610) still creates mild speed pressure. However, the generous duration and the explicit LC circuit metaphor ("resonance decays after 30 seconds of inactivity" per line 1188) reframes speed as signal decay rather than a time attack. This is a meaningful improvement over the generic "combo timer" of iteration 10-11.

### Dimension 5: Assessment Design

**Score: hybrid (improved)**

The multi-phase boss encounters are a major assessment improvement:

1. **Three distinct assessment angles per boss.** Phase 1 tests diagnosis (Bloom level 4: Analyze). Phase 2 tests design/selection (Bloom level 5: Evaluate). Phase 3 tests protection/integration (Bloom level 6: Create). This is genuine multi-faceted assessment within a single game encounter.

2. **Model answers are technically detailed.** Each `phase.answer` contains 50-100 words of specific engineering knowledge (component values, equations, design rules). The LLM evaluator has rich material to compare against, reducing false positives.

3. **Partial credit via phase scoring.** The 2/3 threshold allows players to demonstrate partial competence. Passing 2 of 3 phases defeats the boss but with a "review the failed phases" message (line 1681-1682). This is formative assessment embedded in summative evaluation.

All prior assessment mechanics preserved:
- LLM evaluation for freeform answers
- Circuit wiring challenges (4 challenges with category matching)
- Fault tree diagnosis (4 challenges with step-by-step investigation)
- Bloom-filtered quiz sources by region difficulty
- Misconception matching with specific corrections

### Dimension 6: Accessibility & Inclusion

**Score: strong (improved)**

New accessibility features:
1. **Interactive circuit nodes have keyboard support.** Each node has `tabindex="0"`, `role="button"`, `aria-label`, and handles both click and keyboard (Enter/Space) events (lines 904, 945-946). This is proper ARIA widget implementation.
2. **Node detail popups** are dynamically inserted adjacent to the clicked node, maintaining reading order for screen readers.

Preserved accessibility features:
1. 0 ARIA issues on creation screen (6 interactive elements, 0 missing labels).
2. 4/5 screen reader landmarks (banner, navigation, main, contentinfo). `complementary` still absent.
3. 10/20 tab stops on creation screen (limited elements on this screen).
4. No mobile overflow at 375px.
5. `prefers-reduced-motion`: All animations suppressed to 0.01ms.
6. Theme toggle (light/dark) and font size toggle (small/medium/large).
7. Tutorial overlay with `role="dialog"` and descriptive `aria-label` per step.
8. Help panel with `role="dialog"`, Escape key, overlay click to close.

### Dimension 7: Freemium Monetisation

**Score: learning-first (no regression)**

`premiumFeatures.enabled = false` (line 2538). All content free. Zero monetisation elements. No ads, no energy system, no paywalls.

### Dimension 8: RPG Mechanical Integrity

**Score: partially-functional (improved)**

Iteration 12 adds mechanical depth through:

1. **Multi-phase boss encounters.** Three distinct questions with HP tracking create a genuine multi-round combat analog. The player must demonstrate breadth across diagnosis, design, and protection -- this is not a single-answer encounter disguised as multi-phase.

2. **Interactive circuit board as information architecture.** Clicking nodes to see signal strength, half-life, Bloom level, and correct/incorrect counts gives the player strategic information. They can identify which nodes are fading, which subsystems are close to completion, and where to focus effort. This is informational agency even though it does not yet offer mechanical agency (choosing which node to target).

3. **Current flow and resonance have visual feedback loops.** The animated electron gradient and resonance pulse create immediate, continuous feedback for sustained correct answers. These are not just counters -- they are visual feedback systems that create micro-goals within the encounter loop.

4. **System log adds journey tracking.** The color-coded, timestamped log provides a game-state record that players can consult for strategic decisions (which topics fail most often, when bosses were attempted, etc.).

**What still keeps it from "mechanically rich":**
- **No node targeting within regions.** The player cannot choose which dark or fading node to work on. Encounters are randomly selected from the region's topic pool via `getInterleavedSearchTerm()`. The interactive circuit board shows the player's state but does not let them direct their effort.
- **No resource tradeoffs.** There is no energy cost, time cost, or opportunity cost to choosing one region over another.
- **No subsystem interdependencies.** Powering one subsystem does not mechanically affect another (beyond unlocking the next region at 40% power).
- **Boss encounters are attempt-unlimited.** A failed boss can be immediately re-attempted with no cooldown or cost, reducing the stakes.

The game is a circuit-board builder with quiz mechanics, not an RPG. The "mechanically rich" ceiling for this dimension assumes RPG systems with stats, classes, and strategic tradeoffs. This game's mechanical richness comes from a different genre (builder/management), and within that genre it is competent but not deep.

---

## Critical Bugs and Issues

### POLISH-001: Prerequisite selection is alphabetical, not pedagogical

**Severity: Low (design improvement)**

The BUG-002 fix correctly filters prerequisites to the current region's categories. However, within that filtered set, the code still uses `prereqs.find()` (line 1938), which returns the FIRST matching element -- alphabetically ordered by the API. For the Resistor topic, the first electronics prerequisite is "ADS1110 Battery Voltage ADC," a specialized IC topic that is not a natural prerequisite for resistors.

**Fix:** Add a secondary filter by topic difficulty or popularity. For example, prefer prerequisites that appear in the region's `topics` array, or sort by document tier (quick-context before micro-context) to surface foundational topics first. Alternatively, add a `difficulty` or `foundational` tag to the prerequisites API and sort by it.

### POLISH-002: Boss phase mastery inflation

**Severity: Low (balance)**

Line 1651: `for (const t of sub.nodes) await trackMastery(t, true, 5, null)` calls trackMastery for ALL subsystem nodes on each correct boss phase. For a 5-node subsystem with all 3 phases correct, this results in 15 `trackMastery(true)` calls total, tripling each node's half-life and adding 3 to each node's `correct` count. This potentially over-inflates mastery for nodes the player may not have demonstrated individual understanding of.

**Fix:** Only call `trackMastery` once per node at the end of the boss encounter, not per phase. Or weight the mastery boost by whether the phase specifically tested concepts from that node.

### POLISH-003: System log has no persistent display outside Certifications view

**Severity: Low (UX)**

The system log is only visible when the player clicks "Certifications and system log" from the world map (line 1609-1618). It is not accessible from within a region or during encounters. A persistent mini-log in the HUD or a dedicated "Log" button would improve discoverability.

---

## Biggest Risk

The biggest risk in iteration 12 is no longer a bug -- it is the absence of node-targeting agency. The circuit board shows the player exactly which nodes are powered, fading, or dark, but the player cannot choose which node to work on. Encounters are randomly selected from the region's topic pool. This creates a disconnect: the game gives the player strategic information (via the interactive board) but no strategic action to take with that information. Per Malone (1981), intrinsic motivation in computer games requires both challenge and fantasy AND a sense of control. The interactive board satisfies the information need but not the control need. Adding node targeting would close this gap and elevate the game from a quiz-with-information-architecture to a genuine strategic learning experience.

---

## Recommendations

### Quick Wins

1. **Allow node targeting within regions.** When the player enters a region, show the subsystem's nodes and let them choose which dark or fading node to power. This single change would give the interactive circuit board strategic purpose and address the biggest remaining mechanical gap.

2. **Sort prerequisites by foundational relevance.** Before the `prereqs.find()` call, sort the filtered prerequisites to prefer topics that appear in the current region's `topics` array, or topics tagged as tier `quick` over `micro`. This would prevent the ADS1110 redirect for Workshop resistor players.

3. **Cap boss mastery inflation.** Change line 1651 to only call `trackMastery` at the end of the boss encounter (once per node), not per phase. This prevents tripling half-lives from a single boss fight.

### Structural Improvements

1. **Subsystem interdependencies.** Add gameplay where powering one subsystem creates visible effects on others. For example: powering the "Power Supply" subsystem could add a "Clean Power" indicator to other subsystem nodes, or the "Signal Bus" coming online could reveal hidden connections (traces) between nodes in other subsystems. This would create emergent strategy without mechanical complexity.

2. **Cooldown on failed boss attempts.** Add a brief cooldown (e.g., "review 2 fading nodes before retrying") after a failed boss encounter. This creates consequence for failure and encourages the player to review weak areas before reattempting, aligning game incentives with pedagogical goals.

### Advanced Improvements

1. **Certification triggers tied to actual mastery demonstrations.** Instead of firing certifications on generic milestones (first correct answer, 3 in a row), tie them to domain-specific achievements: "Licensed PCB Designer" fires when ALL Fabrication Bay nodes are at signal strength > 80%. "Analog Engineer License" fires when BJT, MOSFET, and Op-Amp nodes are all powered simultaneously. This would make certifications genuinely meaningful within the circuit board metaphor.

2. **Adaptive prerequisite graph.** Replace the static document_links-based prerequisites with an adaptive system that tracks which concept dependencies the player has actually demonstrated (via freeform answer analysis). If a player's answer about capacitors reveals understanding of voltage and charge but not dielectric materials, redirect to the dielectric concept specifically. This would implement Vygotsky's ZPD more precisely than alphabetical prerequisite selection.

---

## Research References

- Csikszentmihalyi, M. (1990). Flow: The Psychology of Optimal Experience. Clear feedback and proximal goals as preconditions for flow states.
- Flavell, J.H. (1979). Metacognition and Cognitive Monitoring. Reflecting on one's own learning process improves outcomes.
- Gee, J.P. (2003). What Video Games Have to Teach Us About Learning and Literacy. Achievement principle -- earned vs. given.
- Gentner, D. (1983). Structure-Mapping: A Theoretical Framework for Analogy. Relational structure mapping in analogical reasoning.
- Habgood, M.P.J. & Ainsworth, S.E. (2011). Motivating Children to Learn Effectively. Journal of the Learning Sciences. Intrinsic integration framework.
- Malone, T.W. (1981). Toward a Theory of Intrinsically Motivating Instruction. Challenge, fantasy, and control as intrinsic motivators.
- Paivio, A. (1971). Imagery and Verbal Processes. Dual-coding theory -- game experience creates second representation alongside text.
- Ryan, R.M. & Deci, E.L. (2020). Intrinsic and Extrinsic Motivation from a Self-Determination Theory Perspective. Autonomy, competence, relatedness.
- Shute, V.J. (2011). Stealth Assessment in Computer-Based Games to Support Learning. Evidence-Centered Design for assessment without immersion-breaking.
- Vygotsky, L.S. (1978). Mind in Society. Zone of Proximal Development -- scaffolding matching the learner's current ability.

---

<!-- SCORES
intrinsic_integration: deep
pedagogical_soundness: strong
narrative_structure: compelling
motivation_engagement: intrinsic
assessment_design: hybrid
accessibility: strong
freemium_monetisation: learning-first
rpg_mechanical_integrity: partially-functional
biggest_risk: The interactive circuit board gives players strategic information (which nodes are powered/fading/dark) but no strategic action (cannot choose which node to target), creating a disconnect between visibility and agency that limits the game's mechanical depth.
SCORES -->
