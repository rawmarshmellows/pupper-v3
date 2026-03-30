# Knowledge Quest -- Iteration 11 Design Specification

## Focus: Fundamentally Rethought Gamification

### The Central Concept: Knowledge Circuit Board

The generic gamification from iteration 10 (streaks, combos, achievements, collections) has been replaced with a unified metaphor: **you are powering up a circuit board**. Every gamification element now maps to an electronics concept:

- **Nodes** = topics. Each topic is a node on the circuit board. Mastered topics glow green. Fading topics flicker red (like a capacitor discharging).
- **Subsystems** = collections of nodes that form a functional unit (Power Supply, Signal Bus, Logic Core, etc.). When all nodes in a subsystem are powered, it "comes online."
- **Traces** = connections between topics. Discovering concept cascades lights up traces on the board.
- **Boss encounters** = synthesis challenges unlocked when a subsystem is fully powered.
- **Signal degradation** = mastery decay, reframed as nodes losing power. Review is "signal maintenance."
- **Board power %** = overall progress, shown in HUD.

### Why This Is Better Than Generic Gamification

1. **Domain-integrated**: The gamification IS the learning domain. Powering nodes on a circuit board is not just metaphor -- it mirrors how actual electronics work. The player internalizes the idea that components are interconnected.

2. **Visible progress**: The circuit board visualization on the world map shows every node's status at a glance. Green = mastered, red/flickering = fading, dark = unlearned. This is more informative than a single progress bar.

3. **Decay feels meaningful**: "Your resistor node is losing power" is more compelling than "Your mastery bar went down." It connects to the real concept that circuits need maintenance.

4. **Boss encounters reward synthesis**: Generic achievements reward volume. Boss encounters require combining knowledge from ALL topics in a subsystem. This targets Bloom's Evaluate/Create levels.

5. **Eureka moments**: Discovering traces (concept cascades) gets a special "eureka" animation and banner. The player literally sees their board becoming more connected.

6. **Subsystem completion is satisfying**: When all nodes power up and the subsystem comes online, it feels like building something real -- not just checking boxes.

### Bug Fixes from Iteration 10

1. **BUG-001 FIXED**: `saveState()` is now called immediately inside `loadState()` after the migration block, persisting the class data strip to localStorage.

2. **POLISH-002 FIXED**: Both the tutorial practice encounter and the main game now use `<textarea>` elements for text input, providing consistent multi-line input capability.

### What Is Preserved (No Regressions)

- **Deep intrinsic integration**: Prerequisite graph, Bloom scaffolding by region, all content from database
- **Strong pedagogical soundness**: LLM evaluator, quiz questions from all sources, misconception pools, half-life mastery decay, topic interleaving
- **Compelling narrative**: Three-tier NPC greetings, persistent NPC identity, NPC-triggered cascades, deterministic cascade counter
- **Hybrid assessment**: LLM evaluation, circuit wiring challenges, fault tree diagnosis, Bloom filtering, misconception matching
- **Strong accessibility**: ARIA labels, keyboard navigation, light/dark theme, font size toggle, prefers-reduced-motion, safe-area-inset
- **Learning-first monetisation**: All content free
- **Tutorial and help**: 5-step interactive tutorial with practice encounter, persistent help button, replay tutorial
- **No class system** (removed in iteration 10, kept removed)

### New Features

1. **Circuit Board visualization** on world map showing all subsystem nodes with power state
2. **Subsystem power tracking** replacing generic collections
3. **Boss encounters** for fully powered subsystems (6 unique multi-topic synthesis challenges)
4. **Signal degradation alerts** replacing generic "fading topics" warnings
5. **Eureka banners** for trace discoveries (concept cascades)
6. **Board power %** in HUD
7. **Subsystem-aware region cards** showing power indicators

### Architecture

Same Docker Compose stack as iteration 10:
- PostgreSQL with pgvector for knowledge base
- Python importer for Obsidian markdown notes
- Node.js server with REST API + static file serving
- Single-page HTML/CSS/JS frontend

New API endpoint: `GET /api/graph` returns all nodes and edges for potential future graph visualization.
