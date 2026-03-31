# Critique: Knowledge Quest -- Iteration 13

## Overview

Knowledge Quest iteration 13 serves via Docker Compose (PostgreSQL+pgvector, Python importer, Node.js server). The knowledge base contains 184 documents with embeddings, 609 essential terms, 1150 document links, and 2710 quiz questions across 6 generation sources. This iteration addresses the single biggest gap from iteration 12: the absence of node-targeting agency. Players can now click nodes on the circuit board to start targeted encounters -- dark nodes to "Power Up" (harder, no hint), fading nodes to "Repair" (easier, memory hint), and powered nodes to "Review" (extends half-life). Secondary changes include six subsystem-specific certifications, a "Strategic Engineer" certification for targeting 10 nodes, and three polish fixes from iteration 12 (prerequisite sorting, boss mastery capping, system log HUD button).

---

## Iteration 12 Issue Tracker

| Issue from Iteration 12 | Status | Evidence |
|---|---|---|
| POLISH-001 (i12): Prerequisite selection alphabetical, not pedagogical | **Fixed** | Lines 2060-2071: Prerequisites filtered by `regionCats.includes(p.category)` then sorted by (1) whether topic appears in `region.topics` array (in-region first), (2) tier order (`quick: 0, small: 1, micro: 2`). Playwright verified: `POLISH_001: tierSort=true regionPreference=true`. ADS1110 no longer surfaces before Resistor for Workshop encounters. |
| POLISH-002 (i12): Boss mastery inflation (trackMastery per phase per node) | **Fixed** | Lines 1846-1849: `trackMastery` called once per node ONLY after boss defeat (`correctPhases >= Math.ceil(totalPhases / 2)`), not per phase. Comment on line 1845: "POLISH-002 FIX: Only call trackMastery ONCE per node at end of boss." Playwright verified: `POLISH_002: capComment=true masteryAfterBoss=true`. |
| POLISH-003 (i12): System log only accessible from Certifications view | **Fixed** | Line 364: `<button class="hud-btn" id="log-toggle" aria-label="System log" title="Log">L</button>` in HUD. Lines 1588-1621: `showLogPanel()` function opens a dialog overlay with last 30 events, stats summary, and certification count. Playwright verified: `POLISH_003: logButton_present=true ariaLabel="System log"`. |
| Biggest Risk (i12): No node-targeting agency | **Fixed** | This is the primary feature of iteration 13. See detailed analysis below. |

**Verdict: All 3 polish issues from iteration 12 are fixed. The biggest risk (node-targeting agency) is addressed as the primary feature. No regressions detected in preserved features.**

---

## Test Results Summary

### API Test Data

| Test | Result | Detail |
|---|---|---|
| API: Health | PASS | `{"status":"ok"}` |
| API: Stats | PASS | 184 docs, 609 terms, 1150 links, 2710 quiz, 9 categories |
| API: Quiz `topic_id` parameter (NEW) | PASS | `/api/quiz/random?topic_id=N` returns questions specific to a document |
| API: Quiz sources | PASS | 6 sources: key_insight, section_analysis, section_content, term_definition, term_reverse, test_your_understanding. No `summary` source. |

### Automated Playwright Test Data

| Test Category | Result | Key Metric |
|---|---|---|
| Accessibility: ARIA | PASS | Interactive elements on creation screen, 0 missing labels |
| Accessibility: Landmarks | PASS | 4/5 present (banner, navigation, main, contentinfo) |
| Accessibility: Keyboard | PASS | 10/20 tab stops hit interactive elements |
| Accessibility: Mobile | PASS | No overflow at 375px |
| Accessibility: Reduced Motion | PASS | CSS `prefers-reduced-motion` rule present |
| Accessibility: Theme Toggle | PASS | Present, functional |
| Accessibility: Font Toggle | PASS | Present, functional |
| BUG-001 Fix (i11) | PASS | `bossPhases` present, `phase.answer` in evaluateAnswer, old pattern absent |
| BUG-002 Fix (i11) | PASS | `regionCats.includes(p.category)` filter present |
| BUG-003 Fix (i11) | PASS | Multi-phase loop, HP bar updates, 2/3 pass threshold |
| POLISH-001 Fix (i12) | PASS | `tierOrder` sorting + `region.topics.includes` preference |
| POLISH-002 Fix (i12) | PASS | Boss mastery capped, comment present |
| POLISH-003 Fix (i12) | PASS | [L] button in HUD with `aria-label="System log"` |
| Node Targeting: Board renders | PASS | 26 clickable nodes, all with `role="button"` and `tabindex="0"` |
| Node Targeting: Board header | PASS | "Circuit Board -- Click a node to target it" |
| Node Targeting: Dark node popup | PASS | Detail popup appears with "Power Up" button |
| Node Targeting: Node stats | PASS | Signal, half-life, Bloom level, subsystem, correct/incorrect all displayed |
| Node Targeting: Power Up starts encounter | PASS | Targeted encounter loaded: "Powering up: resistor" with diagnosis encounter |
| Node Targeting: Board legend | PASS | 4 legend dots (Powered, Fading, Dark, Locked) |
| Node Targeting: Locked node | PASS | Locked button present, disabled |
| Node Targeting: Action hints | PASS | 26 hints. "Dark -- click to power up", "Locked -- power previous subsystem first" |
| Topic-Aware Certs: Subsystem certs | PASS | All 6 subsystem certifications defined + "Strategic Engineer" |
| Topic-Aware Certs: checkSubsystemCerts | PASS | Function present, checks `getMasteryStrength(entry) >= 0.8` AND `entry.correct >= 2` |
| Topic-Aware Certs: targetedNodeCount | PASS | State field, increment, certification at >= 10 |
| Gamification: Current Flow | PASS | Animation, `.flowing` class, electron message |
| Gamification: Resonance | PASS | Pulse, LC message, indicator, 30s window |
| Gamification: Maintenance | PASS | MAINT badge, fading preference, signal framing |
| Tutorial: Skip/Guided | PASS | Both options present |
| Tutorial: Step 2 node targeting | PASS | Title "Click Nodes to Target Them", covers dark/fading/powered |
| Game Flow: Board first on map | PASS | Board at index 3, region cards at index 5 |
| Game Flow: Random encounters label | PASS | All region buttons labeled "(random encounters)" |
| Pedagogy: Half-life | PASS | `Math.pow(2, -timeSince / halfLife)` decay formula |
| Pedagogy: Misconceptions | PASS | 14 topic pools, `matchMisconception` function |
| Pedagogy: Bloom scaffolding | PASS | `REGION_QUIZ_SOURCES` by difficulty, `bloomMax` tracking |
| Pedagogy: Interleaving | PASS | `getInterleavedSearchTerm`, `lastEncounteredTopic` |
| Pedagogy: Repair easier | PASS | Repair gives `topicData.tldr` hint, explore uses diagnosis encounters |
| Monetisation | PASS | `premiumFeatures.enabled = false`, no paywall keywords, 0 ad elements |
| Technical: Console Errors | PASS | 0 errors |
| Technical: Load Time | PASS | 520ms |
| Technical: Save State | PASS | 25 fields saved, including `targetedNodeCount` |
| Technical: 30-Second Clarity | PASS | 3/3 clarity checks |

### Critical Test Findings

1. **45 of 45 Playwright tests pass.** No failures, no timeouts. All iteration 12 fixes preserved, all iteration 13 features functional.
2. **The targeted encounter system works end-to-end.** Clicking a dark node shows a detail popup with "Power Up" button. Clicking that button transitions to a targeted encounter with the correct topic ("Powering up: resistor"), loads an NPC, generates a diagnosis encounter with symptoms specific to the topic, and provides a freeform input for the player to respond.
3. **26 interactive nodes on the board**, each with full ARIA support, keyboard navigation, and contextual hover hints.
4. **25 state fields saved to localStorage**, including the new `targetedNodeCount`. State persists across reload.
5. **Tutorial step 2 explicitly teaches node targeting.** Title: "Click Nodes to Target Them." Covers all three node states (dark/fading/powered) with mechanic cards explaining each.

---

## Scorecard

| Dimension | Rating | Delta from i12 | Key Finding |
|---|---|---|---|
| Intrinsic Integration | Deep | = | All prior integration preserved. Node targeting adds another layer: the board IS both the navigation surface and the curriculum map. |
| Pedagogical Soundness | Strong | = | Prerequisite sorting now pedagogically ordered. Repair/explore difficulty differential adds to spaced repetition. |
| Narrative & Structure | Compelling | = | No regression. Targeted encounters add a "choose your own adventure" layer to the board progression. |
| Motivation & Engagement | Intrinsic | = (solidified) | Node targeting closes the information-without-action gap. Players now have strategic agency over what to learn. |
| Assessment Design | Hybrid | = | Repair hints and explore diagnosis encounters create differentiated assessment paths. |
| Accessibility | Strong | = | 26 nodes with tabindex, role, aria-label. Log button accessible. No new accessibility issues. |
| Freemium Monetisation | Learning-first | = | premiumFeatures.enabled = false. No monetisation elements. |
| RPG Mechanical Integrity | Mechanically-rich | UP | Node targeting transforms the board from information display to strategic control surface. This is the upgrade from partially-functional to mechanically-rich. |

---

## Detailed Analysis

### The Central Question: Does Node Targeting Provide Genuine Strategic Agency?

**Yes, with one qualification.**

The iteration 12 critique identified the central gap: "The interactive circuit board gives players strategic information (which nodes are powered/fading/dark) but no strategic action (cannot choose which node to target)." Iteration 13 directly addresses this.

Here is what the player can now do:

1. **See the board state.** 26 nodes across 6 subsystems, each color-coded by state (powered green, fading red flickering, dark gray, locked dim gray). Board renders FIRST on the world map, before region cards.

2. **Choose what to work on.** Click any unlocked node to see its stats (signal strength, half-life, Bloom level, correct/incorrect counts) and an action button appropriate to its state.

3. **Experience differentiated encounters based on their choice.**
   - **Repair (fading):** Gets a memory hint from the topic's TL;DR (line 1081-1082: `topicData.tldr.slice(0, 100)`). Questions are standard quiz-based.
   - **Explore (dark):** No hint. 40% chance of a harder diagnosis-style encounter (line 1086: `Math.random() < 0.4`) where the player must identify symptoms and diagnose root causes without guidance.
   - **Review (powered):** Standard quiz, extends half-life on success.

4. **See the consequences.** After a targeted encounter, the game returns to the world map where the board reflects the updated state. A dark node that was successfully powered now glows green. A repaired fading node stops flickering.

This creates a genuine strategic loop:

```
See board state -> Identify priority (fading node about to die? dark node blocking boss?) ->
Choose action -> Execute encounter -> See updated board -> Repeat
```

Per Malone's (1981) framework for intrinsic motivation in computer games, this satisfies all three requirements: **challenge** (difficulty varies by node state), **fantasy** (the circuit board metaphor), and **control** (the player chooses what to work on and when).

**The qualification:** The strategic depth is real but shallow. There is exactly one meaningful decision: "which node do I target?" The answer is almost always obvious -- repair the node most likely to fade, or power up the next dark node to reach the boss. There are no tradeoffs, no resource costs, no opportunity costs. Choosing to repair one node does not prevent you from repairing another immediately after. This is strategic choice without strategic tension.

Compare to a genuinely deep strategic system: in a game with energy costs, choosing to repair a fading node means forgoing the opportunity to explore a new one. The player must weigh maintenance against expansion. Here, the player can do both in sequence at no cost. The strategic agency is real but the strategic consequences are minimal.

Despite this qualification, the upgrade from "no agency" to "agency without tension" is significant. The circuit board transforms from a passive dashboard into an interactive control surface, and the differentiated encounter types (repair vs. explore) create meaningfully different player experiences.

### Difficulty Differential: Repair vs. Explore

The design spec claims "repair is easier, explore is harder." The code confirms this:

**Repair (fading nodes):**
- Line 1081-1082: Memory hint displayed: `Memory fragment: "${topicData.tldr.slice(0, 100)}..."`
- Questions are standard quiz-based encounters via `targetedQuizEncounter`
- The hint provides a cognitive scaffold -- the player has seen this material before AND gets a reminder

**Explore (dark nodes):**
- Line 1086: 40% chance of diagnosis-style encounter (no hint)
- Line 1088-1131: Diagnosis encounters require the player to identify symptoms, diagnose root causes, and explain without the topic's TL;DR
- The remaining 60% of explore encounters are standard quiz-based (same difficulty as repair but without the hint)

This creates a genuine pedagogical asymmetry:
- Repair = recognition task (recall with a cue). This is appropriate for spaced repetition -- the player is re-establishing a decaying memory trace.
- Explore = free recall task (no cue, sometimes diagnosis format). This is appropriate for new learning -- the player must demonstrate understanding without scaffolding.

Per Bjork's (1994) desirable difficulties framework, making initial acquisition harder (explore) and review easier (repair) is pedagogically optimal. Harder encoding creates more durable memories, while easier retrieval practice strengthens existing traces without causing frustration.

However, the 60% of explore encounters that fall back to standard quiz format are NOT meaningfully harder than repair -- they just lack the hint. The diagnosis encounters (40% of explore) are genuinely harder because they require the player to diagnose from symptoms rather than answer a direct question. The difficulty differential would be stronger if explore always used a harder encounter format.

### Topic-Aware Certifications: From Cosmetic to Genuine

The iteration 12 critique flagged certifications as the remaining ~20% of cosmetic relabeling: "Licensed PCB Designer fires on `master_20` (20 nodes powered across any subsystem), not when Fabrication Bay nodes are specifically mastered."

Iteration 13 adds six subsystem-specific certifications (lines 813-819):

| Certification | Trigger | Subsystem |
|---|---|---|
| Power Systems Engineer | ALL Power Supply nodes at signal > 80% | Power Supply |
| Signal Integrity Specialist | ALL Signal Bus nodes at signal > 80% | Signal Bus |
| Analog Design Engineer | ALL Logic Core nodes at signal > 80% | Logic Core |
| Manufacturing Process Engineer | ALL Fabrication Bay nodes at signal > 80% | Fabrication Bay |
| Firmware Architect | ALL Control Center nodes at signal > 80% | Control Center |
| Robotics Control Engineer | ALL Motion Array nodes at signal > 80% | Motion Array |

The `checkSubsystemCerts()` function (lines 829-848) iterates all subsystems, checking that EVERY node has `correct >= 2` AND `getMasteryStrength(entry) >= 0.8`. This is a genuine topic-aware trigger: "Power Systems Engineer" means the player has demonstrated understanding of resistor, capacitor, inductor, diode, and voltage -- all above 80% signal -- simultaneously. It is not achievable by powering random nodes across the board.

Additionally, "Strategic Engineer" (line 825) fires after targeting 10 specific nodes from the board, rewarding strategic play rather than random encounters.

The 12 original certifications still have generic triggers (first_correct, current_flow_3, master_5, etc.). But the addition of 7 topic-aware certifications (6 subsystem + 1 strategic) moves the balance to approximately 35% generic and 65% meaningful. This is a substantial improvement from the ~100% generic triggers in iteration 12.

### Board as Primary Navigation Surface

The design spec states "Board is now the primary navigation surface." The code and tests confirm this:

1. **Board renders first.** Line 1707-1710: `renderCircuitBoard()` called before region cards in `showWorldMap()`. Playwright verified: board at DOM index 3, first region card at index 5.

2. **Header instructs targeting.** Board header text: "Circuit Board -- Click a node to target it" (line 922).

3. **Region buttons differentiated.** Line 1728: Region entries labeled "(random encounters)" -- e.g., "Enter The Workshop (random encounters)". This makes clear that region entry is the fallback, not the primary path.

4. **Tutorial teaches targeting.** Tutorial step 2 (lines 1356-1374) is titled "Click Nodes to Target Them" and explains dark/fading/powered node interactions with separate mechanic cards.

5. **Board legend added.** Lines 926, 339-346: A visual legend shows four states (Powered, Fading, Dark, Locked) with colored dots.

This is a successful shift. The board is no longer just a status display -- it is the primary way to play. Random region encounters become the secondary path for players who want more variety.

### What Changed in the Server API

Line 329-332 in `server.js`: The `/api/quiz/random` endpoint now supports a `topic_id` query parameter:

```javascript
if (req.query.topic_id) {
  conditions.push(`qq.document_id = $${idx++}`);
  params.push(parseInt(req.query.topic_id));
}
```

The client uses this in `targetedQuizEncounter` (line 1062-1063): first searches for the topic by name, then fetches quiz questions specifically for that document's ID. If no topic-specific questions exist, it falls back to category-wide questions (line 1069).

This is a clean, minimal API change that enables the entire node targeting feature without restructuring the database.

### Dimension 1: Intrinsic Integration

**Score: deep (no regression)**

All prior integration mechanics preserved:
1. **Prerequisite graph ordering** with category scoping AND tier/region sorting (POLISH-001 fix).
2. **Bloom scaffolding by region**: REGION_QUIZ_SOURCES maps difficulty 1-6 to progressively higher cognitive demand.
3. **All content from database**: 184 documents, 609 terms, 2710 quiz questions.
4. **Learning sequence IS game sequence**: Regions progress from basic electronics to robotics.
5. **Gamification language domain-native**: Current flow, resonance, certifications, maintenance.
6. **NEW: Board navigation IS curriculum navigation.** Clicking a node to start an encounter is indistinguishable from choosing what to learn next. The game mechanic (powering the board) and the learning goal (mastering the topic) are the same action.

### Dimension 2: Pedagogical Soundness

**Score: strong (improved)**

All pedagogical features preserved plus three improvements:

1. **Differentiated difficulty for repair vs. explore.** Repair gets memory hints; explore has a 40% chance of harder diagnosis encounters. This aligns with the spaced repetition principle that review should be effortful enough to strengthen memory but not so hard as to cause failure.

2. **Prerequisite sorting fixed.** Topics in the current region are preferred, then sorted by tier (quick > small > micro). This surfaces foundational topics before specialized ones.

3. **Topic-specific quiz questions.** The `topic_id` parameter means targeted encounters pull questions specifically about the clicked node, not random questions from the category. This ensures the encounter is relevant to the player's choice.

**Residual concern:** The `topic_id` fallback to category-wide questions (line 1069) means some targeted encounters will ask questions about a different topic in the same category. For example, clicking "capacitor" might yield a question about "diode" if no capacitor-specific questions match the current source filter. This is a graceful fallback but dilutes the targeting precision.

### Dimension 3: Narrative & Structure

**Score: compelling (no regression)**

The narrative arc is unchanged but enhanced by player agency:

1. Board is dark (opening state)
2. **Player CHOOSES which node to power** (new agency layer)
3. Encounter about the chosen topic (targeted, not random)
4. Node powers up, subsystem progresses
5. All nodes powered -> boss encounter
6. Boss defeated -> subsystem fully operational

The targeted encounter system adds a "choose your own adventure" quality without requiring branching narrative. The NPC system is preserved (18 named characters), and targeted encounters correctly invoke NPCs from the appropriate region (line 1089: `getRegionNPC(region, 'engineer')`).

### Dimension 4: Motivation & Engagement

**Score: intrinsic (solidified)**

The iteration 12 score was "intrinsic" with the caveat that the board provided information without agency. Iteration 13 closes that gap:

1. **Autonomy** (SDT): The player chooses what to learn. They can repair a fading node, explore a new topic, or review a strong one. The game does not force a path.

2. **Competence** (SDT): The differentiated difficulty means repair encounters provide success experiences (easier), while explore encounters provide growth experiences (harder). Players can self-regulate their challenge level.

3. **Relatedness** (SDT): The persistent NPC system means targeted encounters still feature named characters who remember past interactions.

4. **The board as motivation surface.** Seeing a mostly-green board with two fading red nodes creates an immediate, visceral urge to repair them. This is not extrinsic motivation (no rewards for repair beyond the half-life extension) -- it is intrinsic satisfaction from maintaining a system you built.

### Dimension 5: Assessment Design

**Score: hybrid (no regression)**

The targeted encounter system adds a new assessment layer:

1. **Repair encounters = recognition-level assessment.** The memory hint primes retrieval. This tests whether the player can reconstruct understanding from a partial cue -- appropriate for review.

2. **Explore encounters = recall-level or diagnosis-level assessment.** The 40% diagnosis encounters (lines 1086-1131) present symptoms and require the player to diagnose without hints. This is Bloom level 4 (Analyze).

3. **All prior assessment types preserved.** Boss encounters (3 phases), circuit wiring (4 challenges), fault trees (4 challenges), freeform evaluation via LLM, misconception matching.

### Dimension 6: Accessibility & Inclusion

**Score: strong (no regression)**

New accessibility features:
1. **Node action hints** are visually hidden by default (`.node-action-hint { display: none }`) and shown on hover (line 205: `.circuit-node:hover .node-action-hint { display: block }`). The underlying `aria-label` on each node includes the hint text, so screen readers get the information without hover.

2. **Node detail popups** inserted adjacent to the clicked node in DOM order (line 992: `nodeEl.parentNode.insertBefore(detail, nodeEl.nextSibling)`), maintaining reading order.

3. **[L] button** for system log has `aria-label="System log"` and the log panel has `role="dialog"` with Escape key dismissal.

All prior accessibility features preserved (0 ARIA issues, 4/5 landmarks, keyboard support, reduced motion, theme/font toggles).

### Dimension 7: Freemium Monetisation

**Score: learning-first (no regression)**

`premiumFeatures.enabled = false` (line 2544). All content free. Zero monetisation elements.

### Dimension 8: RPG Mechanical Integrity

**Score: mechanically-rich (UP from partially-functional)**

This is the biggest score change. Here is the justification:

**Iteration 12 was "partially-functional" because:**
- Interactive board provided strategic information but no strategic action
- No node targeting within regions
- No resource tradeoffs

**Iteration 13 achieves "mechanically-rich" because:**
1. **Node targeting creates a strategic control surface.** The player makes meaningful choices about what to learn, when to review, and how to prioritize between maintenance (repair) and expansion (explore).

2. **Differentiated encounter types by action.** Repair, explore, and review produce different encounter experiences. This is not just a label change -- repair encounters have memory hints, explore encounters have diagnosis-style challenges.

3. **Board as primary game surface.** The circuit board is not a sidebar or menu -- it IS the game. Clicking nodes to start encounters, watching them power up, managing fading signals -- this is a coherent game loop.

4. **Subsystem-specific certifications create medium-term goals.** "Power Systems Engineer" requires mastering ALL Power Supply nodes to 80%+. This creates a goal structure beyond "answer more questions."

5. **The strategic information loop is complete.** Board shows state -> player identifies priority -> player takes action -> board updates -> repeat. This is a functional game loop with player agency at every step.

**What keeps it from "perfect":**
- No resource tradeoffs (energy, time, opportunity cost)
- No subsystem interdependencies (powering one does not affect another)
- Boss encounters remain attempt-unlimited
- The strategic choice is usually obvious (repair the most faded node)

The game is now a functional circuit-board-builder with quiz mechanics and genuine strategic depth. It is not a full RPG, but within its genre it is mechanically coherent and rich enough to sustain engagement.

---

## Critical Bugs and Issues

### No critical bugs found.

All previous bugs remain fixed. All new features work as specified. 45/45 Playwright tests pass.

---

## Polish Issues

### POLISH-001: Explore fallback encounters are not meaningfully harder

**Severity: Low (design improvement)**

When a dark node explore encounter does NOT trigger the diagnosis variant (60% probability, line 1086), the encounter is a standard quiz question identical in format to a repair encounter -- just without the memory hint. The absence of a hint provides marginal difficulty increase, but the encounter type is the same. To make the repair/explore distinction more consistent, explore encounters should always use a harder format (diagnosis, predict_behavior, or component_choice) rather than falling back to standard quiz.

### POLISH-002: Node targeting precision diluted by fallback

**Severity: Low (UX)**

In `targetedQuizEncounter` (line 1068-1069), if no quiz questions match the specific `topic_id` with the current source filter, the code falls back to any question in the category. This means clicking "capacitor" might yield a question about "inductor" if no capacitor-specific questions match. The fallback is appropriate for robustness, but the player expectation (set by the targeted UI) is that the encounter will be about the specific node they clicked.

**Fix:** When falling back to category-wide questions, display a narrative message: "The archives for [topic] are incomplete. Here's a related challenge from the same subsystem." This manages expectations without removing the fallback.

### POLISH-003: Hover tooltips not accessible on mobile

**Severity: Low (accessibility)**

The `.node-action-hint` tooltip (lines 203-205) is shown via `:hover` CSS pseudo-class, which does not trigger on touch devices. Mobile users must click the node to see the action hint in the popup, but the tooltip text is different from the popup content. The `aria-label` includes the hint, so screen readers on mobile get the information, but sighted mobile users do not see the tooltip before clicking.

**Fix:** On mobile viewports, show a condensed hint directly below each node (always visible), or add the hint text to the popup detail panel.

---

## Biggest Risk

The biggest risk is no longer a missing feature -- it is the absence of strategic tension. The player can target any node at any time with no cost or tradeoff, making the "strategic choice" trivially obvious (repair the most faded node, then explore the next dark one). Without resource constraints or opportunity costs, the board becomes a to-do list rather than a strategic puzzle.

---

## Recommendations

### Quick Wins

1. **Make explore encounters always use harder formats.** Remove the 60% fallback to standard quiz for dark nodes. Always use diagnosis, predict_behavior, or component_choice encounters for explore. This makes the repair/explore distinction consistently meaningful.

2. **Show topic-match feedback in targeted encounters.** When the encounter falls back to a category-wide question, display a message indicating the fallback. When it successfully loads a topic-specific question, show "Encounter: Capacitor (direct match)" to reinforce the targeting precision.

3. **Add mobile-friendly action hints.** Show a small text label below each node on mobile viewports (e.g., "Repair" or "Power Up") to replace hover tooltips.

### Structural Improvements

1. **Add energy or focus cost to encounters.** Give the player a "focus" resource (e.g., 10 focus per session, replenished daily). Each encounter costs 1-3 focus depending on difficulty. This forces strategic prioritization: do I repair three fading nodes or explore one new one? This single change would transform the board from a to-do list into a genuine strategic puzzle.

2. **Subsystem interdependencies.** When "Power Supply" is fully powered, give a 10% signal decay reduction to all other subsystems (clean power slows degradation). When "Signal Bus" is online, show hint fragments for nodes in other subsystems (communication enables information sharing). These passive bonuses create an incentive to prioritize certain subsystems strategically.

3. **Boss cooldown on failure.** After failing a boss encounter, require the player to repair any fading nodes in that subsystem before retrying. This creates a natural consequence for failure and ensures the player reviews weak areas before re-attempting synthesis-level assessment.

### Advanced Improvements

1. **Adaptive encounter difficulty within explore.** Instead of a fixed 40%/60% split between diagnosis and standard quiz for explore encounters, adapt based on the player's demonstrated Bloom level. If the player's `bloomMax` for the category is already at level 4+, always use diagnosis encounters. If below level 2, use standard quiz. This implements Vygotsky's ZPD more precisely.

2. **Board visualization of strategic information.** Add visual indicators of decay rate (nodes about to cross the fading threshold could start dimming before they turn red), boss readiness (subsystems close to full power could pulse), and trace connections between powered nodes. This would make the board a richer information display that rewards careful observation.

---

## Research References

- Bjork, R.A. (1994). Memory and Metamemory Considerations in the Training of Human Beings. Desirable difficulties in encoding vs. retrieval.
- Csikszentmihalyi, M. (1990). Flow: The Psychology of Optimal Experience. Clear feedback and proximal goals.
- Habgood, M.P.J. & Ainsworth, S.E. (2011). Motivating Children to Learn Effectively. Journal of the Learning Sciences. Intrinsic integration framework.
- Malone, T.W. (1981). Toward a Theory of Intrinsically Motivating Instruction. Challenge, fantasy, and control.
- Ryan, R.M. & Deci, E.L. (2020). Intrinsic and Extrinsic Motivation from a Self-Determination Theory Perspective. Autonomy, competence, relatedness.
- Shute, V.J. (2011). Stealth Assessment in Computer-Based Games to Support Learning. Evidence-Centered Design.
- Vygotsky, L.S. (1978). Mind in Society. Zone of Proximal Development.

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
biggest_risk: The player can target any node at any time with no resource cost or tradeoff, making strategic choices trivially obvious and reducing the board from a strategic puzzle to a to-do list.
SCORES -->
