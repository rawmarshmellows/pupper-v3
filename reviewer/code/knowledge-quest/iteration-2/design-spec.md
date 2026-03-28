# Knowledge Quest - Design Specification (Iteration 2)

## Changes from Iteration 1

### Fixed: Quiz Question Extraction
The importer now correctly parses the actual note format: `**Q1:**` question followed by `<details><summary>Answer</summary>` answer `</details>`.

### Redesigned: Intrinsic Integration
Encounters now require understanding as the gameplay mechanic:
- **Circuit Build**: Select the correct component from options — wrong choice causes circuit failure
- **Diagnosis**: Identify root cause from symptoms — no answer shown beforehand
- **Predict Behavior**: Forecast what happens when a parameter changes
- **Component Choice**: Stealth assessment — player picks a path without realizing it's a test
- **Negotiate**: Must define terms accurately to get good deals
- **Decode**: Name the term from its definition to unlock access
- **Teach Apprentice**: Explain concepts to an NPC (Bloom's Evaluate/Create level)

### Fixed: Retrieval Practice
Knowledge panels are NO LONGER shown before challenges. The player must recall/reason first. Correct information is revealed only AFTER the attempt (whether correct or not).

### Added: Semantic Answer Evaluation
New `/api/evaluate` endpoint uses embedding cosine similarity to score answers. Falls back to keyword matching if API fails.

### Added: Mystery System
Each region has an overarching mystery that requires understanding multiple topics to solve. Clues accumulate through successful encounters. Solving a mystery grants large bonus rewards.

### Added: Hint System with Cost
Players can request hints, but this reduces reward and increments a hint counter (tracked for assessment analytics).

## Encounter-Knowledge Integration

| Encounter | How Understanding IS the Mechanic | Bloom's Level |
|-----------|-----------------------------------|---------------|
| Circuit Build | Must identify correct component from description | Remember/Understand |
| Diagnosis | Must reason about cause from symptoms | Analyze |
| Predict Behavior | Must predict system behavior changes | Apply/Analyze |
| Component Choice | Implicit assessment through path selection | Understand |
| Negotiate | Must define terminology accurately | Remember |
| Decode | Must name concepts from definitions | Remember |
| Apply Knowledge | Must answer contextual quiz questions | Apply/Evaluate |
| Teach Apprentice | Must explain concepts to teach others | Evaluate/Create |

## Assessment Design
- **Stealth**: Component choice encounters assess understanding through gameplay decisions
- **Hybrid**: Diagnosis and prediction encounters require open-ended generation but evaluate via semantic similarity
- **Overt**: Quiz-based encounters are framed as system diagnostics rather than tests

## Preserved from Iteration 1
- 6-region structure with progressive difficulty
- Dark theme, mobile-responsive layout
- Character creation with 6 classes and stat allocation
- Keyboard shortcuts and touch-friendly targets
- localStorage persistence
- Freemium design (all learning free, premium is additive)
