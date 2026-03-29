# Knowledge Quest -- Iteration 5 Design Spec (FINAL)

## Changes from Iteration 4

### Intrinsic Integration Fixes (partial -> deep)

**A. Deterministic Cross-Domain Challenges**
- 7 pre-authored challenges in `CROSS_DOMAIN_CHALLENGES` with fixed technical reference answers
- Each has: id, title, regions, prompt, and a detailed technical reference
- Examples: "Design a Motor Driver Circuit", "Build a Sensor-to-Display Pipeline", "Design Power Regulation for a Robot"
- References are ~100 words of specific technical content (topology, component selection, parameter values)
- No random topic insight assembly -- same answer evaluates the same way every time

**B. Circuit Wiring Encounter (action-based)**
- 4 challenges in `CIRCUIT_WIRING_CHALLENGES`
- Player sees named circuit slots (e.g., "Input filter", "Voltage conversion", "Output filter", "Load decoupling")
- Selects components from a mixed pool of correct parts + distractors
- Taps parts to fill slots, taps slots to remove parts
- Submit grades each slot against the fixed correct order
- No text entry -- understanding demonstrated through component selection and ordering
- Full explanation revealed after submission

**C. Fault Tree Encounter (action-based)**
- 4 challenges in `FAULT_TREE_CHALLENGES` (Motor Not Spinning, I2C Bus Lockup, Robot Drifts Left, ADC Readings Noisy)
- Player sees symptoms and chooses diagnostic steps from a menu
- Each step reveals information: either eliminates a hypothesis or reveals a clue
- After minimum steps, player can declare root cause (text entry to name it)
- Stealth assessment: the PATH the player takes through diagnostic steps reveals their reasoning
- Steps track "used" state, preventing re-selection

### Pedagogical Soundness Fixes (mixed -> strong)

**A. Diagnostic Branching with Misconception Matching**
- `MISCONCEPTION_POOLS` object: 18 topic keys, each with 1-3 misconceptions, each with specific corrective text
- Server endpoint `POST /api/misconception-match`: embeds player answer + all misconceptions, finds best semantic match above 0.60 threshold
- On wrong answers in Diagnosis, Predict Behavior, Apply Knowledge, Teach Apprentice, Fault Tree, Cross-Domain, and Mystery encounters: calls misconception matching
- If matched: shows targeted feedback in `.msg-misconception` styled box with the specific misconception text and its correction
- If no match: falls back to generic "incorrect" feedback
- Keyword fallback in frontend if API fails

**B. Gold Replenishment via Mastery**
- `GOLD_PER_RANK` defines gold earned per rank milestone: Apprentice=10, Journeyman=15, Master=25
- `checkGoldReplenishment()` fires on each topic mastery, checking if region rank advanced
- `goldRanksEarned` state tracks highest rank that earned gold per region
- Total possible gold from mastery: 6 regions * (10 + 15 + 25) = 300 gold
- Negotiate encounter: if player has no gold but passed steps 1-2, dealer accepts "knowledge in trade"
- Gold depletion is no longer a permanent dead end

### Preserved from Iteration 4 (5 passing dimensions)
- motivation_engagement: intrinsic -- no XP/level, mastery milestones only
- narrative_structure: functional -- Circuit Citadel, 6 regions, mystery system
- assessment_design: hybrid -- Component Choice/Circuit Build stealth + text evaluation
- accessibility: adequate -- dark theme, mobile-responsive, ARIA labels, prefers-reduced-motion
- freemium_monetisation: learning-first -- all content free, premium config defined but not gated

### Bug Fixes
- Concept cascade detection: exact key match (`k === a`) instead of `k.includes(a)` to prevent premature triggering from partial matches like "decoupling-capacitor" matching "capacitor"
