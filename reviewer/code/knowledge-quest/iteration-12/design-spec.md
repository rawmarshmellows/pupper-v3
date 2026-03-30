# Knowledge Quest -- Iteration 12 Design Specification

## Focus: Bug Fixes + Gamification Deepening into Circuit Board Metaphor

### Bug Fixes (All 3 Mandatory)

#### BUG-001 FIX: Boss evaluation against real answers
- **Problem:** Boss encounters evaluated player answers against the boss QUESTION text concatenated with reward flavor text, not a correct answer. The `bossAnswer` field was missing from SUBSYSTEMS.
- **Fix:** Replaced single `bossPrompt` with `bossPhases` array. Each phase has its own `prompt` and `answer`. The `evaluateAnswer()` call now uses `phase.answer` as the correct answer, not `sub.bossPrompt + ' ' + sub.reward`.
- **Impact:** Boss assessment now correctly evaluates conceptual understanding against model answers.

#### BUG-002 FIX: Prerequisite redirect scoped to category
- **Problem:** The prerequisite lookup returned ALL linked documents from the database regardless of category. A Workshop player (electronics) could get redirected to "ADS1110 Battery ADC" (embedded) because the Resistor topic's wiki links include cross-category references.
- **Fix:** Added `regionCats.includes(p.category)` filter to the prerequisite selection. The code now only redirects to unmastered prerequisites that are in the same category as the current region. If no in-category prerequisite exists, no redirect occurs.
- **Impact:** First-time Workshop players now get redirected to foundational electronics topics only.

#### BUG-003 FIX: Multi-phase boss encounters with real HP bar
- **Problem:** Boss HP bar showed 100% but never changed -- boss was resolved in one answer attempt, creating false multi-phase expectations.
- **Fix:** Bosses now have 3 phases, each with a unique question and answer. HP bar starts at 100% and decreases by 33% for each correct phase. Player must pass at least 2/3 phases to defeat the boss. Each phase prompt targets a different aspect (diagnosis, component selection, protection/integration).
- **Impact:** HP bar is now meaningful. Boss encounters test breadth across all subsystem topics.

### Gamification Deepening: Circuit Board Metaphor Integration

All generic gamification elements have been fully integrated into the circuit board metaphor:

#### Streaks -> Current Flow
- Consecutive correct answers build "current" through the board
- Visual: HUD bar labeled "Current" with animated gradient that flows when current >= 3
- CSS animation `currentFlowAnim` simulates electrons moving along traces
- Narrative messages: "Current Flow: N -- electrons moving through the board"
- State field renamed from `streak` to `currentFlow`

#### Combos -> Resonance
- Quick consecutive answers (within 30 seconds) create "resonance"
- Tied to LC circuit resonance concept -- energy oscillating between L and C
- HUD shows `~Nx` resonance indicator with pulse animation
- Narrative messages: "Resonance xN -- LC oscillation amplifying learning"
- State field renamed from `combo` to `resonance`

#### Achievements -> Engineering Certifications
- All achievements reframed as engineering certifications/licenses
- Examples: "Licensed Technician" (not "First Light"), "Superconductor Class" (not "Streak Master"), "Licensed PCB Designer" (not "PCB Designer")
- Banner text says "Certification:" instead of "Achievement:"
- State field renamed from `achievements` to `certifications`

#### Daily Challenges -> Maintenance Rounds
- Daily challenge reframed as a "system check" / maintenance round
- Badge shows "MAINT" instead of "DAILY"
- Prefers fading topics (signal maintenance) over random questions
- Framed as maintaining circuit board signal integrity
- State field renamed from `dailyChallengesCompleted` to `maintenanceCompleted`

### New Features

#### Interactive Circuit Board
- Circuit board nodes are now clickable (mouse + keyboard accessible)
- Clicking a node shows a detail popup with: status (Powered/Fading/Dark), signal strength %, half-life, Bloom level, correct/incorrect counts, subsystem name
- Nodes have `tabindex="0"`, `role="button"`, and `aria-label` for accessibility
- Keyboard support: Enter/Space to activate node detail

#### System Log
- New "System Log" feature tracks the player's journey narratively
- Every significant event is logged: node powered, boss encountered, mystery solved, certifications earned, failures
- Log entries are timestamped and color-coded by type (success, fail, discovery, event)
- Displayed in the Certifications view with the last 15 entries
- Stored in localStorage (capped at 100 entries)

### Migration Compatibility

The `loadState()` function handles migration from iteration 11 state:
- `streak` -> `currentFlow`
- `bestStreak` -> `bestCurrentFlow`
- `achievements` -> `certifications`
- `dailyChallengesCompleted` -> `maintenanceCompleted`

### What Is Preserved (No Regressions)

- **Deep intrinsic integration**: Prerequisite graph (now properly scoped), Bloom scaffolding by region, all content from database
- **Strong pedagogical soundness**: LLM evaluator, quiz questions from all sources (no `summary`), misconception pools, half-life mastery decay, topic interleaving
- **Compelling narrative**: Three-tier NPC greetings, persistent NPC identity, NPC-triggered cascades, deterministic cascade counter
- **Hybrid assessment**: LLM evaluation, circuit wiring challenges, fault tree diagnosis, Bloom filtering, misconception matching
- **Strong accessibility**: ARIA labels, keyboard navigation, light/dark theme, font size toggle, prefers-reduced-motion, safe-area-inset
- **Learning-first monetisation**: All content free, premiumFeatures.enabled = false
- **Tutorial and help**: 5-step interactive tutorial with practice encounter, persistent help button, replay tutorial
- **No class system** (removed in i10, kept removed)

### Architecture

Same Docker Compose stack:
- PostgreSQL with pgvector for knowledge base
- Python importer for Obsidian markdown notes
- Node.js server with REST API + static file serving
- Single-page HTML/CSS/JS frontend
