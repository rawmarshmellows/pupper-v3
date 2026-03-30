# Knowledge Quest -- Iteration 10 Design Specification

## Focus: Remove Classes, Simplify Entry, Better Gamification

### User Directives (Override Standard Feedback)

1. **Remove the class system entirely** -- no more Warrior/Mage/Rogue class selection
2. **Make it easier** -- lower barrier to entry, reduce cognitive load on mechanics
3. **Better gamification** -- lighter but more rewarding than the RPG system

### What Changed

#### 1. Class System Removed

**Before (iteration 9):** Character creation required:
- Name input
- Class selection (6 classes with abilities)
- Stat allocation (20 points across 6 stats)
- Derived HP/MP calculations
- Starting inventory based on class

**After (iteration 10):** Character creation requires:
- Name input only
- One click to start

This reduces the character creation from ~60 seconds with 20+ decisions to ~5 seconds with 1 decision.

#### 2. Stat Checks and d20 Rolls Removed

**Before:** Every encounter included a d20 + stat modifier roll that affected the outcome (hints revealed, damage amounts, etc.). This added mechanical complexity that competed with the educational content for cognitive resources.

**After:** Encounters focus purely on the knowledge challenge. Hints are given based on topic context data (tldr, key_insight) without gating behind dice rolls. This follows the cognitive load principle (Plass et al., 2015): every game element that doesn't support learning is extraneous load.

#### 3. HP/MP/Gold/Inventory Removed

**Before:** HP loss on wrong answers, MP cost for hints/retries, gold economy, inventory system, class abilities (Jury-Rig). These were mechanically interesting but added cognitive overhead.

**After:** Wrong answers reset the streak but never punish with HP loss. Hints are freely available (the point is learning, not resource management). This follows the anti-pattern guidance: "Make errors informative, not punitive."

#### 4. Title System Replaces Classes

**Before:** Static class identity (e.g., "Engineer") chosen at start.

**After:** Evolving title that reflects actual mastery progress:
- Newcomer (0%) -> Curious (5%) -> Apprentice (15%) -> Journeyman (30%) -> Adept (50%) -> Expert (70%) -> Master (85%) -> Grandmaster (95%)

The title is earned through learning, not selected at character creation. This is more intrinsically motivating because it reflects actual achievement.

#### 5. Better Gamification Systems

**Streaks:** Consecutive correct answers build a visible streak counter in the HUD. Streak milestones (3, 5, 10) trigger achievements. Wrong answers reset the streak. This provides moment-to-moment feedback on performance.

**Combos:** Correct answers within 30 seconds of each other build a combo multiplier (x2, x3, etc.) displayed in the HUD with a pulse animation. This rewards flow states and sustained engagement.

**Achievements (20 total):** Unlockable milestones with names and descriptions:
- Streak achievements (3, 5, 10 in a row)
- Mastery milestones (5, 20, 50 topics)
- Exploration (visit all regions)
- Mystery solving (first mystery, all mysteries)
- Concept cascades (1, 5 discovered)
- Encounter types (circuit wiring, fault tree)
- Daily challenges (first, 7 days)
- Collections (first complete set)
- Teaching (teach apprentice 5 times)
- Bloom depth (reach level 4)
- Memory keeper (review a fading topic)

**Knowledge Collections (6 sets):** Complete sets of related topics to collect:
- Circuit Fundamentals (resistor, capacitor, inductor, diode, voltage)
- Signal Path (I2C, SPI, CAN bus, PWM)
- Semiconductor Journey (transistor, MOSFET, BJT, op-amp)
- Robot Builder (PID, kinematics, gait)
- Maker Toolkit (PCB, soldering, SMD, 3D printing, CNC)
- Embedded Master (STM32, clock, ADC, IMU)

Each collection shows progress bars and highlights which topics are mastered.

**Daily Challenges:** One quiz question per day. Completing it earns a daily badge and works toward the daily challenge achievement streak.

**Progress Visualization:** Every region shows a mastery progress bar. The mastery progress screen shows per-topic strength bars (strong/medium/fading).

#### 6. Polish Items from Iteration 9 Feedback

- **POLISH-001 (Replay Tutorial):** Added "Replay Tutorial" button at the bottom of the help panel.
- **POLISH-002 (Input consistency):** Both tutorial and main game now use consistent input elements.
- **POLISH-003 (First encounter scaffold):** When the player enters their first region for the first time, a brief guided annotation bridges the tutorial and gameplay.

### What is Preserved

All 8 dimensions from iteration 9 are preserved:

- **Deep intrinsic integration:** Prerequisite graph ordering, Bloom scaffolding by region, all content from database
- **Strong pedagogical soundness:** LLM evaluator, 5420 quiz questions, 18 misconception pools, half-life mastery decay, topic interleaving
- **Compelling narrative:** Three-tier NPC greetings, persistent NPC identity, NPC-triggered cascades, deterministic cascade counter
- **Hybrid assessment:** LLM evaluation, circuit wiring challenges, fault tree diagnosis, Bloom filtering, misconception matching
- **Strong accessibility:** ARIA labels, keyboard navigation, light/dark theme, font size toggle, prefers-reduced-motion, safe-area-inset
- **Learning-first monetisation:** All content free
- **Tutorial and help:** 5-step interactive tutorial with practice encounter, persistent help button, replay tutorial button

### Architecture

Unchanged from iteration 9:
- Docker Compose: pgvector/pg16 + Python importer + Node.js server
- 184 documents, 1218 terms, 1150 links, 5420 quiz questions (all with embeddings)
- LLM evaluation via Gemini 2.0 Flash (OpenRouter)
- Hybrid search: pgvector cosine + full-text RRF

### Migration

The `loadState()` function includes migration logic: if a save from iteration 9 has a class system (`state.char.class`), it strips it and keeps only the name. Existing mastery progress, achievements, and journal entries are preserved.
