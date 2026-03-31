# Knowledge Quest -- Iteration 13 Design Specification

## Focus: Strategic Agency via Node Targeting + Topic-Aware Certifications

### Primary Feature: Clickable Node Targeting (Strategic Agency)

The #1 critique from iteration 12: "The interactive circuit board gives players strategic information (which nodes are powered/fading/dark) but no strategic action (cannot choose which node to target)."

#### What Changed

1. **Clicking a node on the circuit board starts a targeted encounter about that specific topic.**
   - Dark nodes: "Power Up" button -- harder encounter, expands capability
   - Fading nodes: "Repair" button -- easier encounter with memory hints, maintains the system
   - Powered nodes: "Review" button -- optional strengthening, extends half-life
   - Locked nodes: disabled button, shows unlock requirement

2. **Visual affordances for clickable nodes:**
   - Hover tooltip shows what clicking will do (e.g., "Fading! Click to repair", "Dark -- click to power up")
   - Hover effect: translateY(-1px) + accent glow to signal interactivity
   - Four visual states: powered (green), fading (red flicker), dark (gray), locked (dim gray, no-cursor)
   - Board legend added showing all four states

3. **Strategic tradeoffs between repair and explore:**
   - Repair (fading): easier -- player gets a memory hint from the topic's TL;DR. Rewards maintenance.
   - Explore (dark): harder -- no hint, sometimes uses diagnosis-style encounters. Rewards expansion.
   - Review (powered): optional -- strengthens half-life for long-term retention.

4. **Random encounters preserved as fallback:**
   - "Enter [Region] (random encounters)" option still available from world map
   - All 10 encounter types preserved: diagnosis, predict_behavior, component_choice, negotiate, decode, apply_knowledge, teach_apprentice, circuit_wiring, fault_tree, review_in_region
   - Node targeting is ADDITIONAL, not a replacement

5. **Board as primary navigation:**
   - Circuit board renders FIRST on the world map, before region cards
   - Board header text: "Click a node to target it"
   - Region buttons labeled "(random encounters)" to differentiate from targeting

6. **Targeted encounter API:**
   - Server's `/api/quiz/random` now supports `topic_id` parameter to fetch questions specific to a document
   - Targeted encounters try topic-specific questions first, fall back to category questions

### Secondary Feature: Topic-Aware Certifications

The remaining ~20% cosmetic gap: certification triggers were generic milestones with engineering names.

#### What Changed

1. **Six new subsystem-specific certifications:**
   - "Power Systems Engineer" -- fires when ALL Power Supply nodes are at signal strength > 80%
   - "Signal Integrity Specialist" -- fires when ALL Signal Bus nodes are at > 80%
   - "Analog Design Engineer" -- fires when ALL Logic Core nodes are at > 80%
   - "Manufacturing Process Engineer" -- fires when ALL Fabrication Bay nodes are at > 80%
   - "Firmware Architect" -- fires when ALL Control Center nodes are at > 80%
   - "Robotics Control Engineer" -- fires when ALL Motion Array nodes are at > 80%

2. **`checkSubsystemCerts()` function:**
   - Called after every `trackMastery()` correct answer
   - Iterates all subsystems, checks if every node has `correct >= 2` AND `getMasteryStrength() >= 0.8`
   - These certifications are genuinely topic-aware: "Licensed PCB Designer" now means something different from "Power Systems Engineer"

3. **New targeting certification:**
   - "Strategic Engineer" -- fires after targeting 10 specific nodes from the board
   - Tracked via `state.targetedNodeCount`

### POLISH Fixes from Iteration 12 Critique

#### POLISH-001: Prerequisite selection now sorted by relevance
- Before: `prereqs.find()` returned first alphabetical match (ADS1110 for Resistor)
- After: prerequisites sorted by (1) whether they appear in the region's `topics` array, (2) tier order (quick > small > micro)
- This surfaces foundational topics before specialized ones

#### POLISH-002: Boss mastery inflation capped
- Before: `trackMastery(true)` called per boss phase per node (up to 15 calls for 5-node subsystem)
- After: `trackMastery()` called ONCE per node at end of boss encounter, only if boss defeated
- This prevents tripling half-lives from a single boss fight

#### POLISH-003: System log accessible from HUD
- Before: log only visible from "Certifications and system log" menu option
- After: persistent [L] button in HUD opens a dedicated log panel overlay
- Log panel shows last 30 events (up from 15), stats summary, and certification count

### Preserved Features (No Regressions)

All 8 dimensions at their iteration 12 levels:

1. **Intrinsic Integration (deep):** All content from DB, prerequisite graph, Bloom scaffolding, circuit board metaphor
2. **Pedagogical Soundness (strong):** LLM evaluation, misconception matching, half-life decay, interleaving, category-scoped prerequisites
3. **Narrative & Structure (compelling):** Multi-phase bosses, NPC cascades, region descriptions, mysteries
4. **Motivation & Engagement (intrinsic):** Current flow animation, resonance LC analogy, maintenance rounds prefer fading, NOW with strategic agency
5. **Assessment Design (hybrid):** 18 boss phase questions, circuit wiring, fault trees, freeform + button encounters
6. **Accessibility (strong):** ARIA labels, keyboard support, theme/font/motion, mobile-responsive, node tooltips
7. **Freemium Monetisation (learning-first):** premiumFeatures.enabled = false, no ads, no paywalls
8. **RPG Mechanical Integrity (partially-functional → improved):** Node targeting adds genuine strategic depth

### New State Fields

- `targetedNode`: tracks which node the player chose to target (cleared after encounter)
- `targetedNodeCount`: cumulative count of nodes targeted from the board (for certification)
