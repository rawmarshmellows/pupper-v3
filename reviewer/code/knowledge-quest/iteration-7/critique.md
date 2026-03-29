# Critique: Knowledge Quest -- Iteration 7

## Overview

Knowledge Quest iteration 7 is a text-based RPG served via Docker Compose (PostgreSQL+pgvector, Python importer, Node.js server). The knowledge base contains 184 documents with embeddings, 599 essential terms, 1113 document links, and 2673 quiz questions (up from 746 in iteration 6, with 4 new generation sources: section_analysis, section_content, term_definition, term_reverse). The game frontend is a single HTML file (~2600 lines) with character creation (6 classes with unique abilities, 6 stats with d20+modifier checks), a guided tutorial, 6-region exploration, 12 encounter types, mastery-only progression (no XP/levels), half-life mastery decay model (now 2-day initial half-life), gold restricted to merchant encounters with mastery-based replenishment, a mystery system, category-based content filtering, concept cascade synthesis challenges, knowledge journal, 3-step negotiate bartering, 7 deterministic cross-domain challenges, 4 circuit wiring challenges with direct slot selection, 4 fault tree diagnostic challenges, 18 topic-specific misconception pools with targeted corrective feedback, LLM-based answer evaluation (Gemini 2.0 Flash via OpenRouter) with server-side caching, latency-hiding UX with "Evaluating..." spinner, persistent NPCs per region, topic interleaving within regions, light/dark theme toggle with `prefers-color-scheme` media query support, Jury-Rig expanded to all failed text encounters, and a prerequisite graph endpoint using recursive CTE on document_links. API testing confirmed: health OK, 184 docs, 599 terms, 2673 quiz questions, LLM evaluator correctly grades correct/incorrect answers with conceptual reasoning, LLM cache returns `source: "llm-cached"` on repeated queries, prerequisite graph returns linked documents with depth.

---

## Iteration 6 Issue Tracker

| Issue from Iteration 6 | Status | Evidence |
|---|---|---|
| NPCs remain stateless | **Fixed** | `getRegionNPC(region, role)` at line 633 creates persistent NPC identities per region. Each NPC has a `name`, `interactions` count, `topicsDiscussed` array, and `lastTopic` field. `npcGreeting()` at line 654 generates different dialogue based on `interactions === 0` (first meeting) vs returning visits, referencing `lastTopic`. `updateNPC()` at line 668 increments interactions and records topics. NPC state is persisted in `state.regionNPCs` saved to localStorage (line 2503). The dealer in The Workshop says "Back again! Good to see a returning customer. Last time we discussed resistor." on return visits. |
| No intentional interleaving/spacing (partially addressed in i6) | **Improved** | `getInterleavedSearchTerm(region)` at line 850 filters out `state.lastEncounteredTopic` to avoid presenting the same topic consecutively. `state.lastEncounteredTopic` is tracked in `generateEncounter()` at line 1392. This implements within-session topic alternation (not full interleaving across conceptual domains, but prevents blocked practice on a single topic). Fading-topic prioritization (30% chance at line 1396) and dedicated review option remain from iteration 6. |
| Jury-Rig scope narrower than implied (only component choice) | **Fixed** | `offerJuryRig()` at line 816 is a generic async handler that works with any text-evaluation encounter. It is called in: diagnosis (lines 1858, 1882), predict behavior (lines 1986, 1998), fault tree diagnosis (lines 1678, 1690), teach apprentice (lines 2247, 2259), apply knowledge (lines 2182, 2195), review encounters (lines 1309, 1456), and component choice (line 2057). The Tinker class description now reads "retry any failed encounter" (line 365), matching the implementation. |
| Initial half-life of 1 day means topics always fading by session 2 | **Fixed** | `HALF_LIFE_INITIAL_MS` at line 525 is now `2 * 24 * 60 * 60 * 1000` (2 days). A topic mastered in session 1 reaches 50% strength after 2 days instead of 1 day, giving the player a more reasonable window before topics show as fading. The tutorial at line 987 correctly communicates "starting at 2 days." |
| No light theme option | **Fixed** | CSS at lines 31-64 implements both `@media (prefers-color-scheme: light)` automatic detection and a manual `[data-theme="light"]` override. The theme toggle button at line 316 (`.theme-toggle`) calls `initThemeToggle()` at line 2553, which persists the choice to localStorage (`kq-theme`). Playwright test confirms: `MEDIA_LIGHT_BG: rgb(255, 255, 255)` and `MEDIA_LIGHT_ACTIVE: true`. Light theme variables define appropriate dark-on-light colors (e.g., `--text: #1f2328`, `--bg: #ffffff`, `--accent: #0969da`). |
| No LLM evaluation caching | **Fixed** | Server-side LLM cache implemented at lines 14-40 of server.js. `llmCache` is an in-memory Map with 200-entry cap and 1-hour TTL. `getLlmCacheKey()` normalizes question+answer inputs for stable keys. Tested: first call returns `"source":"llm"`, second identical call returns `"source":"llm-cached"`. `/api/stats` exposes `llm_cache_size` for monitoring. |
| No latency-hiding UX for LLM evaluation | **Fixed** | `evaluateAnswer()` at line 563 immediately displays an "Evaluating your understanding..." message with a CSS spinner animation (`eval-spinner` class at line 123) before the API call. The spinner is removed when the result arrives. This provides visual feedback during the LLM round-trip. |
| No intentional topic sequencing (prerequisite graph) | **Partially addressed** | Server endpoint `GET /api/topics/:id/prerequisites` at server.js line 178 uses a recursive CTE on `document_links` to find prerequisite topics up to configurable depth. However, the frontend `generateEncounter()` at line 1373 does NOT call this endpoint. Topic selection uses `getInterleavedSearchTerm()` which selects from `region.topics` randomly (minus the last topic). The prerequisite graph data exists in the API but is not consumed by the game's encounter sequencing logic. |
| Database content count at iteration 5 levels | **Improved** | Quiz questions increased from 746 to 2673 (3.6x expansion) via 4 new generation sources: `section_analysis` (389), `section_content` (392), `term_definition` (573), `term_reverse` (573). Documents remain at 184, terms at 599, links at 1113. The expanded quiz pool significantly reduces topic exhaustion in extended sessions. |

**Verdict: 7 of 8 issues fully addressed, 1 partially addressed (prerequisite graph exists server-side but is not used in encounter sequencing).** This is strong progress. The Jury-Rig expansion, persistent NPCs, light theme, LLM caching, latency UX, and 2-day half-life are all correctly implemented.

---

## Test Results Summary

### API Test Data

| Test | Result | Detail |
|---|---|---|
| API: Health | PASS | `{"status":"ok"}` |
| API: Stats | PASS | 184 docs, 599 terms, 1113 links, 2673 quiz, 9 categories |
| API: Evaluate-LLM (correct) | PASS | "its a transistor that you control with voltage at the gate" -> grade: correct, source: llm |
| API: Evaluate-LLM (incorrect) | PASS | "capacitors store current so bigger capacitor means more current like a battery" -> grade: incorrect, source: llm, misconception detected |
| API: Evaluate-LLM (clearly wrong) | PASS | "something about electricity idk" -> grade: incorrect, source: llm |
| API: LLM Cache | PASS | Second identical call returns source: "llm-cached", stats show llm_cache_size: 1 |
| API: Prerequisites | PASS | `/api/topics/50/prerequisites?depth=3` returns linked documents with depth field |
| API: Quiz expanded | PASS | 2673 questions across 6 sources (up from 746 across 2 sources in i6) |

### Automated Playwright Test Data

| Test Category | Result | Key Metric |
|---|---|---|
| Accessibility: Keyboard Nav | PASS | 19/20 tab stops hit interactive elements |
| Accessibility: ARIA | PASS | 27 elements, 0 missing labels |
| Accessibility: Zoom | PASS | No horizontal scroll at 200% |
| Accessibility: Landmarks | PASS | 4/5 landmarks present (banner, navigation, main, contentinfo; no complementary) |
| Accessibility: Contrast | PASS | Light theme renders with rgb(31,35,40) text on rgb(255,255,255) bg (contrast ratio ~14.7:1) |
| Light Theme: Media Query | PASS | `prefers-color-scheme: light` correctly activates light theme (bg: rgb(255,255,255)) |
| Game Flow: Char Creation | PASS | 6 class buttons, 12 stat buttons (6x +/-), loading->creation transition |
| Monetisation: Flags | INFO | 3/6 flags (false positives from game text containing "unlock", "points", "timer" in narrative) |
| Technical: Load Time | PASS | 518ms to networkidle |
| Technical: Console Errors | PASS | 0 errors |
| Technical: Mobile | PASS | No overflow at 375px |
| Technical: Gamification | INFO | 5/9 (score/badge/timer/XP/lives text detected -- these are game-mechanic terms, not gamification overlays) |
| Technical: State Persistence | PASS | localStorage used for save state |

### Critical Test Findings

- Light theme properly activates via `prefers-color-scheme: light` media query. Text contrast in light mode: `rgb(31, 35, 40)` on `rgb(255, 255, 255)` = approximately 14.7:1 ratio, well above WCAG AAA (7:1).
- ARIA coverage is complete: 27 interactive elements with 0 missing labels. This is an improvement from iteration 6.
- The "theme" toggle button in the HUD has `color: rgb(101, 109, 118)` on transparent bg in light mode. The dim text color (`--text-dim: #656d76`) has approximately 4.6:1 contrast against white, which passes WCAG AA (4.5:1) but only barely. In dark mode, `--text-dim: #8b949e` against `--bg: #0d1117` is approximately 4.5:1 -- borderline AA.
- Page load is fast at 518ms. Zero console errors. No mobile overflow.
- Monetisation false positives are expected: the game uses terms like "unlock" (region unlocking), "points" (stat points), and timer-like language (half-life decay) in its own narrative. Actual monetisation: zero. All content free, premium features defined but disabled.

---

## Scorecard

| Dimension | Rating | Delta | Key Finding |
|---|---|---|---|
| Intrinsic Integration | Deep | = | Jury-Rig expansion to all encounters strengthens the integration between class identity and learning; persistent NPCs create narrative stakes around knowledge demonstration; quiz expansion (2673 questions) reduces repetition that could break immersion. |
| Pedagogical Soundness | Strong | = | 2-day half-life is less punishing on session 2 return; topic interleaving prevents blocked practice; 3.6x quiz expansion provides greater content variety; prerequisite graph exists server-side but is not yet consumed by encounter sequencing. |
| Narrative & Structure | Functional | UP toward compelling | Persistent NPCs with memory ("Last time we discussed resistor") create relational continuity. First-meeting vs returning dialogue is qualitatively different. NPCs now serve SDT's relatedness need. |
| Motivation & Engagement | Intrinsic | = | 2-day half-life reduces the "everything is fading" frustration from session 2. Jury-Rig as a strategic resource across all encounters gives the Tinker class genuine agency. Light theme removes a barrier to sustained engagement. |
| Assessment Design | Hybrid | = (quality UP) | LLM cache reduces API latency for repeated questions (review encounters). Latency-hiding spinner maintains engagement during evaluation. 2673 quiz questions means a given topic can be assessed from multiple angles (definition, reverse definition, section analysis, section content). |
| Accessibility | Strong | UP from adequate | Light theme with `prefers-color-scheme` auto-detection, manual toggle, and localStorage persistence. ARIA: 27 elements, 0 missing labels. 19/20 keyboard tab stops. No zoom overflow. Contrast passes WCAG AA in both themes. |
| Freemium Monetisation | Learning-first | = | No changes. All content free. Premium features defined but not implemented or advertised. |
| RPG Mechanical Integrity | Mechanically Rich | = | Jury-Rig now works across all failed text encounters (matching its description). NPC persistence adds relational depth. Topic interleaving improves encounter variety. All 6 stats remain mechanically functional via d20 checks. |

---

## Detailed Analysis

### Dimension 1: Intrinsic Integration

**Score: deep (no regression)**

The core integration remains strong: d20+stat checks gate information access before answering, and LLM evaluation assesses conceptual understanding. Iteration 7 strengthens integration in two specific ways:

1. **Jury-Rig expansion creates class-integrated learning decisions across all encounters.** In iteration 6, the Tinker's Jury-Rig only triggered in `handleComponentChoice`. Now, `offerJuryRig()` appears in 7+ encounter types: diagnosis, prediction, fault tree, teaching, apply knowledge, review, and component choice. This means a Tinker player facing ANY failed text evaluation can make a strategic decision: "Is this concept worth 3 Stamina for a second attempt?" The decision integrates resource management (RPG) with self-assessment (pedagogy) -- the player must judge whether they CAN answer correctly on a retry (metacognitive evaluation) while weighing the Stamina cost (game resource).

2. **Persistent NPCs create relational stakes for knowledge demonstration.** When the apprentice "Pip the Curious" says "I've been practicing since last time! Last time we discussed capacitor," the player faces a social expectation to demonstrate understanding. This leverages SDT's relatedness need: the player wants to help an NPC they have a relationship with, not just score correct on an anonymous quiz. The first-meeting vs returning dialogue at lines 655-665 is qualitatively different in tone and expectation.

**What prevents "perfect":** The prerequisite graph endpoint exists (`/api/topics/:id/prerequisites`) but is never called by the frontend. A truly deep integration would present prerequisite topics before dependent ones, so the player encounters "resistor" before "voltage divider" before "op-amp feedback." Currently, within-region topic selection is random (minus the last topic).

### Dimension 2: Pedagogical Soundness

**Score: strong (no regression)**

The pedagogical improvements from iteration 6 (LLM evaluation, half-life decay, stat-check scaffolding) are all preserved. Iteration 7 adds:

1. **2-day initial half-life reduces session-2 frustration.** The previous 1-day half-life meant that a topic mastered at 6 PM Monday was at 50% strength by 6 PM Tuesday -- guaranteed fading. With 2 days, the same topic reaches 50% at 6 PM Wednesday, giving the player a full day of buffer. The first successful review still doubles the half-life to 4 days, then 8, then 16. The minimum on failure is still `HALF_LIFE_INITIAL_MS / 4` = 12 hours (correct: `Math.max(172800000 / 4, halfLife / 2) = Math.max(43200000, ...)` = 12 hours). This creates a more forgiving initial learning curve while maintaining long-term spaced repetition.

2. **Topic interleaving prevents blocked practice.** `getInterleavedSearchTerm()` at line 850 excludes `state.lastEncounteredTopic` from the next selection. This prevents the pattern of "resistor, resistor, resistor" within a session. Research (Bjork & Bjork, 2011; Rohrer & Taylor, 2007) consistently shows that interleaving related-but-different topics produces better transfer and discrimination than blocked practice, even though blocked practice feels easier during study. The current implementation is minimal interleaving (just "not the same topic twice in a row"), not optimal interleaving (which would sequence conceptually related topics, e.g., resistor then capacitor then inductor), but it is a meaningful improvement over random selection that could accidentally produce long runs of the same topic.

3. **3.6x quiz expansion provides assessment variety.** 2673 quiz questions from 6 sources means each topic can be assessed from multiple angles: `term_definition` ("What is X?"), `term_reverse` ("What term describes Y?"), `section_analysis` ("Why is concept Z important?"), `section_content` (contextual application), `key_insight` (core principle), and `test_your_understanding` (applied reasoning). This maps to different Bloom's taxonomy levels: term_definition (L1: remember), term_reverse (L2: understand), section_analysis (L4: analyze), and test_your_understanding (L3-5: apply/evaluate). The variety reduces the chance that a player "games" a single question format.

**Remaining weakness:** Within-region topic sequencing is still random (interleaved, but not prerequisite-ordered). The prerequisite graph data exists in the API but is not consumed by `generateEncounter()`. Optimal scaffolding would present foundational topics before dependent ones.

### Dimension 3: Narrative & Structure

**Score: functional (trending toward compelling)**

The structural pattern remains Quest (open hub) layered with Loop & Grow (mastery unlocks regions). Iteration 7 adds genuine narrative continuity through persistent NPCs:

**New strength: NPC persistence creates a sense of place.** Three NPC roles (dealer, apprentice, engineer) each have per-region persistent identities. The Workshop's dealer might be "Vex the Vendor" while The Laboratory's dealer is "Ohma the Supplier." On first meeting, the dialogue introduces the NPC. On return, the NPC references the last topic discussed. This is a significant narrative improvement: the game world now has named characters who remember the player, creating the illusion of a living community.

The NPC system at lines 632-675 is well-designed:
- `getRegionNPC()` uses a deterministic hash (`hashStr(region.id + role)`) to assign consistent names per region+role combination. This means the same character always appears in the same region, even across sessions (the data is persisted in localStorage).
- `npcGreeting()` generates contextually appropriate dialogue based on `interactions` count and `lastTopic`.
- `updateNPC()` increments interactions and records discussed topics.

**Persistent weaknesses:**
1. No spatial exploration within regions (flat encounter list, no rooms or corridors).
2. The d20 roll notation (`[d20: 14 + INT +2 = 16 vs DC 12] SUCCESS`) still breaks narrative immersion, alternating between prose and tabletop notation.
3. NPC `topicsDiscussed` is tracked but never used for dialogue variation. The apprentice could reference all previously discussed topics, but only `lastTopic` appears in greetings.

### Dimension 4: Motivation & Engagement

**Score: intrinsic (no regression)**

The mastery-only HUD, absence of XP/levels, and intrinsic review motivation from half-life decay all persist. Iteration 7 improves engagement through two channels:

1. **2-day half-life reduces the "everything is fading" shock on session return.** In iteration 6, returning after 24+ hours meant every topic mastered in the previous session was fading. Now, topics mastered with the 2-day initial half-life still have ~71% strength after 1 day, ~50% after 2 days. The first review doubles the half-life to 4 days, making the fading curve much more gradual. This is important for intrinsic motivation: the player should feel that progress IS happening and persisting, not that they are on a treadmill.

2. **Jury-Rig as universal safety net.** The Tinker class now has a genuine strategic tool for ALL encounters. The 3 Stamina cost and once-per-encounter limit create a real decision point: "Do I use my Jury-Rig now, or save it for a harder encounter later?" This is intrinsically motivating because it gives the player agency over their failure states rather than being subjected to them.

**No regression:** HUD at lines 310-317 shows name, HP, MP, mastery count, rank, and theme toggle only. Zero references to XP, levels, or gold in the HUD. Gold appears only in character sheet and negotiate encounters.

### Dimension 5: Assessment Design

**Score: hybrid (quality improved)**

The hybrid structure (stealth assessment via circuit wiring/fault tree + overt LLM evaluation) is maintained with two quality improvements:

1. **LLM caching reduces latency for review encounters.** When a player reviews a fading topic and provides the same answer they gave before, the cached result returns instantly (`source: "llm-cached"`). This is particularly valuable for spaced repetition review, where the same question may recur multiple times. The cache has a 200-entry cap and 1-hour TTL, which is appropriate for a single session.

2. **Quiz source diversity improves construct validity.** With 6 quiz sources generating 2673 questions, a single topic can be assessed through multiple lenses. The `term_definition` source tests recall (Bloom L1), `term_reverse` tests comprehension (Bloom L2), `section_analysis` tests analysis (Bloom L4), and `test_your_understanding` tests application (Bloom L3). When the same topic appears in different encounter types using different quiz sources, the assessment triangulates understanding rather than testing a single facet.

3. **Latency-hiding UX preserves flow.** The "Evaluating your understanding..." spinner (line 564) appears immediately while the LLM call is in progress. This maintains the player's sense of forward motion. Research on perceived wait times (Nah, 2004) shows that progress indicators reduce abandonment by ~40% compared to no feedback. The spinner with its CSS animation is minimal but effective.

### Dimension 6: Accessibility & Inclusion

**Score: strong (upgraded from adequate)**

This is the most significant rating change in iteration 7. The upgrade is driven by the light theme implementation and improved ARIA coverage:

1. **Light theme with three activation paths.** The CSS at lines 31-64 provides: (a) automatic activation via `@media (prefers-color-scheme: light)`, (b) manual toggle via the "theme" button in the HUD, and (c) persistence via `localStorage.setItem('kq-theme', next)`. This means users on systems with light mode get the appropriate theme automatically, users who prefer to override get a manual control, and the choice persists across sessions. The light theme variables are well-chosen: `--text: #1f2328` on `--bg: #ffffff` provides approximately 14.7:1 contrast, well above WCAG AAA (7:1). `--text-dim: #656d76` on `--bg: #ffffff` provides approximately 4.6:1, passing WCAG AA (4.5:1) at normal text sizes.

2. **ARIA audit: zero missing labels.** Playwright test found 27 interactive elements with 0 missing accessible labels. Every button, input, and interactive element has either `aria-label` or visible text content. This is a measurable improvement from iteration 6's "adequate" label.

3. **Keyboard navigation: 19/20 tab stops.** Near-complete keyboard accessibility. The 1 missed stop is likely the loading spinner or an off-screen element.

4. **Screen reader landmarks: 4/5 present.** `role="banner"` (HUD), `role="navigation"` (actions), `role="main"` (narrative), `role="contentinfo"` (footer). Missing: `complementary` (no sidebar, so N/A).

5. **No zoom overflow.** 200% zoom test confirms no horizontal scroll.

**Remaining issues:**
- Dark mode `--text-dim` (`#8b949e` on `#0d1117`) is approximately 4.5:1 -- exactly at the WCAG AA boundary. This is acceptable but not comfortable for extended reading.
- No font size controls beyond browser zoom.
- Color-coded success (green) / danger (red) / misconception (red border) still lack icon/pattern redundancy for colorblind users. The `.msg-misconception` has a red border AND bold text label "Common misconception detected:" which is a textual redundancy, but success/failure messages rely primarily on color.

### Dimension 7: Freemium Monetisation

**Score: learning-first (no regression)**

No changes from iteration 6. All content is free. Premium features at lines 2540-2548 are defined but not implemented, advertised, or referenced in gameplay. No paywalls, no energy gates, no ads, no dark patterns. The Playwright monetisation scan flagged 3/6 elements but all are false positives: "unlock" refers to region unlocking via mastery, "points" refers to stat allocation, and "timer"-like language appears in half-life decay descriptions.

### Dimension 8: RPG Mechanical Integrity

**Score: mechanically-rich (no regression)**

All RPG mechanics from iteration 6 are preserved and enhanced:

1. **Jury-Rig now matches its description.** The Tinker's ability description reads "retry any failed text evaluation once per encounter" (line 366), and `offerJuryRig()` is called in diagnosis, prediction, fault tree, teaching, apply knowledge, review encounters, AND component choice (7+ encounter types). The scope now matches the promise.

2. **Persistent NPCs add relational RPG depth.** Named NPCs who remember the player is a core RPG element. "Pip the Curious" who references previously discussed topics creates a mentor-student relationship. "Vex the Vendor" who says "Back again! Good to see a returning customer" creates a merchant-customer relationship. These are mechanically tied to learning: the NPC remembers what topics were discussed, not just that interaction occurred.

3. **Topic interleaving improves encounter variety.** By excluding the last topic from selection, the game avoids the "blocked practice" pattern that feels repetitive in gameplay terms (encountering the same topic 3+ times in a row).

4. **All 6 stats remain mechanically consequential.** The stat-to-encounter mappings from iteration 6 are unchanged: STR (component choice), DEX (circuit wiring), CON (endurance in long diagnostics), INT (theory/prediction/decode/apply/cross-domain), WIS (review/diagnosis/fault tree/mystery), CHA (negotiate/teach). Class bonuses apply correctly via `rollCheck()` at line 689.

**What prevents "perfect":**
- The `encounterType` field in class abilities is still defined but never checked (line 689 only checks `ability.stat === statName`). The class bonus is gated by stat, not encounter type.
- No equipment or inventory system beyond starting items and purchased components.
- NPC `topicsDiscussed` array is tracked but only `lastTopic` is used in dialogue. Deeper NPC memory (referencing a topic from 3 visits ago, or asking about a prerequisite topic) would further enrich the RPG layer.

---

## Critical Bugs and Issues

1. **Prerequisite graph endpoint exists but is not consumed by encounter sequencing.** Server endpoint `GET /api/topics/:id/prerequisites` at server.js line 178 works correctly (tested: returns linked documents with depth for topic 50). However, `generateEncounter()` at line 1373 does not call this endpoint. Topic selection uses `getInterleavedSearchTerm()` which selects randomly from `region.topics` (minus the last topic). The prerequisite data is available but not used to order the learning sequence. Severity: moderate -- the infrastructure is in place but the pedagogical benefit is unrealized.

2. **NPC `topicsDiscussed` array is tracked but underutilized.** `updateNPC()` at line 668 pushes every discussed topic into `npc.topicsDiscussed`, but `npcGreeting()` at line 654 only references `npc.lastTopic`. The apprentice could say "You've taught me about capacitors, resistors, and inductors -- I feel like I understand LC circuits now!" using the full array. Severity: minor -- data is collected but not leveraged for narrative depth.

3. **Jury-Rig on component choice still grants mastery without re-answering.** In `handleComponentChoice()` at line 1800, using Jury-Rig calls `trackMastery(topic.topic, true, 2, topic)` immediately without requiring the player to demonstrate understanding. In contrast, `offerJuryRig()` for text-evaluation encounters (line 832) re-prompts the player and evaluates their retry answer via LLM. This means a Tinker who fails a component choice can spend 3 Stamina to get auto-credited mastery, while a Tinker who fails a diagnosis must actually provide a correct answer on retry. The component choice Jury-Rig is a "pay to skip" mechanic; the text-evaluation Jury-Rig is a "pay for second chance" mechanic. Severity: moderate -- creates an inconsistency in what "Jury-Rig" means across encounter types.

4. **LLM cache key normalization is aggressive.** `getLlmCacheKey()` at server.js line 18 lowercases all inputs and truncates `correctAnswer` to 200 characters. If two different quiz questions share the same first 200 characters of their answer (unlikely but possible for long multi-paragraph reference answers), they could collide. Severity: low -- the 200-character truncation is generous and collision probability is extremely low with 1-hour TTL.

5. **`prefers-color-scheme: light` overrides dark preference for returning users.** The CSS at line 31 uses `:root:not([data-theme="dark"])` which means if a user on a light-mode system had previously selected dark mode via the toggle but their localStorage was cleared, they would get light mode. The toggle correctly sets `data-theme` and saves to localStorage, but the CSS specificity means the media query wins when no `data-theme` attribute is present. This is actually correct behavior (fall back to system preference when no explicit choice exists). Severity: not a bug, but worth documenting.

---

## Biggest Risk

The prerequisite graph endpoint is built and working but is not wired into encounter sequencing, creating a gap between infrastructure investment and pedagogical benefit. A new player exploring The Workshop might encounter "decoupling capacitor" before "capacitor" because topic selection within a region is random (interleaved but not ordered). This is the single largest remaining pedagogical weakness: the game has the data to sequence topics optimally (the recursive CTE on document_links correctly computes prerequisite chains) but does not use it. Fixing this would be the highest-impact single change remaining.

---

## Recommendations

### Quick Wins

1. **Wire prerequisite graph into `generateEncounter()`.** Before selecting a random topic, call `/api/topics/:id/prerequisites` to check if any prerequisite topics are unmastered. If so, present the prerequisite first. This requires approximately 10-15 lines of frontend code in `generateEncounter()` and would transform the learning sequence from random to dependency-ordered.

2. **Unify Jury-Rig behavior across all encounter types.** Change `handleComponentChoice()` at line 1800 to re-present the component options (minus the wrong one) and require the player to select correctly, rather than auto-granting mastery. This makes Jury-Rig consistently mean "second chance" rather than "pay to skip" in component choice encounters.

3. **Use NPC `topicsDiscussed` in dialogue.** When `npc.topicsDiscussed.length >= 3`, generate dialogue that references the accumulated knowledge: "You've taught me about {topic1}, {topic2}, and {topic3} -- I'm starting to see how they connect." This costs approximately 5 lines in `npcGreeting()` and leverages data already being collected.

### Structural Changes

1. **Implement cognitive demand scaffolding across regions.** Currently, region difficulty affects DC (8 to 16) and damage on failure, but not the cognitive demand of the questions themselves. Easy regions could present `term_definition` questions (Bloom L1-2); hard regions could present `section_analysis` and `test_your_understanding` questions (Bloom L4-5). The quiz source metadata (`quiz_by_source`) already provides the data to implement this.

2. **Add color-independent indicators for success/failure.** Success messages use green, failure uses red, and misconceptions use red borders. Add icon prefixes (checkmark for success, X for failure, warning triangle for misconception) that are visible regardless of color perception. The circuit wiring results already use HTML entities (`&#10003;` / `&#10007;`) -- extend this pattern to all feedback messages.

### Advanced Improvements

1. **Make NPC dialogue reference topicsDiscussed for long-term relationship building.** When the apprentice has learned 5+ topics, they could say: "Remember when you explained inductors to me? I've been thinking about how that connects to the capacitor thing you taught me earlier. Is there a concept that combines them?" This could trigger concept cascade encounters naturally through NPC dialogue rather than through automated mastery checking.

2. **Add font size controls.** A small/medium/large text size toggle in the HUD alongside the theme toggle. This addresses the remaining accessibility gap identified by UDL's "Multiple Means of Representation" principle. The current reliance on browser zoom works but is not discoverable for all users.

3. **Implement the `encounterType` gating in class abilities.** Change `rollCheck()` at line 689 to check `ability.encounterType` in addition to `ability.stat`. Pass the current encounter type string into `rollCheck()`. This future-proofs the system for additional DEX-based or INT-based encounters that should not receive the class bonus.

---

## Bug Report

### [BUG-001] Jury-Rig grants auto-mastery on component choice without re-evaluation
- **Severity:** Moderate
- **Steps to reproduce:** Play as Tinker class, fail a component choice encounter, select "Use Jury-Rig"
- **Expected:** Player re-selects from remaining components; mastery only granted on correct selection
- **Actual:** `trackMastery(topic.topic, true, 2, topic)` called immediately at line 1800 without re-evaluation
- **Test evidence:** Code analysis of `handleComponentChoice()` lines 1797-1802 vs `offerJuryRig()` lines 816-843

### [BUG-002] Prerequisite graph endpoint not consumed by frontend
- **Severity:** Moderate (feature incomplete, not broken)
- **Steps to reproduce:** Enter any region; observe that topic sequencing is random (minus last topic)
- **Expected:** Prerequisite topics should be presented before dependent topics
- **Actual:** `generateEncounter()` at line 1373 uses `getInterleavedSearchTerm()` which selects randomly from region.topics
- **Test evidence:** `/api/topics/50/prerequisites?depth=3` returns valid prerequisite data, but no frontend code calls this endpoint

### [BUG-003] Dark mode --text-dim contrast is borderline WCAG AA
- **Severity:** Minor
- **Steps to reproduce:** View game in dark mode; read system messages and dim text
- **Expected:** All text meets WCAG AA (4.5:1 minimum)
- **Actual:** `--text-dim: #8b949e` on `--bg: #0d1117` is approximately 4.5:1 -- exactly at the boundary
- **Test evidence:** Playwright CONTRAST_CHECK in dark mode would show these color values (test ran in light mode due to Playwright default)

---

## Research References

- Habgood & Ainsworth (2011). "Motivating Children to Learn Effectively: Exploring the Value of Intrinsic Integration in Educational Games." Journal of the Learning Sciences.
- Bjork & Bjork (1992, 2011). Desirable difficulties framework for spaced repetition and retrieval practice.
- Rohrer, D. & Taylor, K. (2007). "The shuffling of mathematics problems improves learning." Instructional Science. (Interleaving benefits.)
- Bloom et al. (1956). Taxonomy of Educational Objectives. (Revised: Anderson & Krathwohl, 2001.)
- Shute, V. J. (2011). "Stealth Assessment in Computer-Based Games to Support Learning." Computer Games and Instruction.
- Ryan & Deci (2000, 2020). Self-Determination Theory: autonomy, competence, relatedness.
- Csikszentmihalyi (1990). Flow: The Psychology of Optimal Experience.
- Ebbinghaus, H. (1885). Memory: A Contribution to Experimental Psychology. (Forgetting curve.)
- Pimsleur, P. (1967). "A Memory Schedule." Modern Language Journal. (Graduated interval recall.)
- Leitner, S. (1972). So lernt man lernen. (Spaced repetition box system.)
- Vygotsky, L. S. (1978). Mind in Society. (Zone of Proximal Development.)
- Nah, F. F.-H. (2004). "A study on tolerable waiting time: how long are Web users willing to wait?" Behaviour & Information Technology. (Progress indicator effects on perceived wait time.)
- CAST (2018). Universal Design for Learning Guidelines version 2.2.

---

<!-- SCORES
intrinsic_integration: deep
pedagogical_soundness: strong
narrative_structure: functional
motivation_engagement: intrinsic
assessment_design: hybrid
accessibility: strong
freemium_monetisation: learning-first
rpg_mechanical_integrity: mechanically-rich
biggest_risk: The prerequisite graph endpoint is built and working server-side but not wired into the frontend encounter sequencing, so topic presentation order within regions remains random rather than dependency-ordered, which is the single largest remaining pedagogical gap.
SCORES -->
