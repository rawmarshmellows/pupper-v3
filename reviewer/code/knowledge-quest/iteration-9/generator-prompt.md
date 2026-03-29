# Generator Prompt: Iteration 9

## Task
You are refining an existing educational game. This is iteration 9.

## Previous Game (full Docker project)
Read ALL files from: /Users/kevinlu/Documents/Learning/pupper-v3/reviewer/code/knowledge-quest/iteration-8/
- docker-compose.yml
- db/init.sql
- importer/import_notes.py, importer/Dockerfile, importer/requirements.txt
- server/server.js, server/package.json, server/Dockerfile
- server/public/index.html (the game frontend -- 2737 lines)

## Critique of Previous Iteration
Read the critique from: /Users/kevinlu/Documents/Learning/pupper-v3/reviewer/code/knowledge-quest/iteration-8/critique.md

## Structured Feedback -- What MUST Change

### PRIORITY 1 (CRITICAL): Full Interactive Tutorial / Onboarding
The game NEEDS a MUCH better tutorial. The user said "right now it's not clear what to do." A new player cannot figure out how to play. You MUST:

1. Add a dedicated, multi-step INTERACTIVE tutorial that walks the player through their FIRST encounter after character creation
2. The tutorial must include an actual practice encounter with guided annotations -- not just text explaining mechanics
3. Show an example of a good answer so players know what format/quality is expected
4. Explain what kind of input is expected: Is it freeform text? Buttons? What format? Make this CRYSTAL CLEAR
5. Explain EVERY core mechanic one at a time with progressive disclosure:
   - (Step 1) What this game is about and your goal
   - (Step 2) How encounters work: you see a question/challenge, you type your answer in the text box or click buttons
   - (Step 3) Walk through a REAL practice encounter with annotations
   - (Step 4) What mastery means, what the mastery bar shows, that it decays over time
   - (Step 5) Knowledge journal -- where to find it, what it records
   - (Step 6) Regions/zones and how to progress
   - (Step 7) Inventory, stats, and how they affect gameplay
6. The tutorial must take < 3 minutes and be skippable by returning players (Skip Tutorial button)
7. Add a PERSISTENT "Help" or "How to Play" button in the HUD that is accessible at ANY time during gameplay
8. The 30-second clarity test: within 30 seconds of starting, a brand new player must understand:
   (a) What this game IS
   (b) What they are supposed to DO
   (c) How to interact with it
9. Visual cues: interactive elements (buttons, text input) must be visually distinct from narrative text. The text input area should have a clear label like "Type your answer here..."
10. The very first encounter after the tutorial MUST be scaffolded differently -- tell the player exactly what to do

### PRIORITY 2: Bug Fixes from Iteration 8 Critique
1. BUG-001: Remove `summary` from REGION_QUIZ_SOURCES difficulty 3. Change line 547 from `'key_insight,summary,section_content'` to `'key_insight,section_content'`. The `summary` source does not exist in the quiz database, causing The Foundry to fall back to unfiltered questions.
2. BUG-002: Remove unused CSS icon classes `.icon-success`, `.icon-failure`, `.icon-warning`, `.icon-partial` (lines 312-315). These are dead code since inline unicode is used instead.
3. Make NPC cascade trigger DETERMINISTIC: track `cascadeEncountersSinceLastTrigger` per region in game state. After the apprentice has 5+ topics, trigger a cascade every 4th encounter in that region instead of the current 30% random probability. This makes it feel like a narrative milestone, not a dice roll.
4. Add logging when prerequisite check fails: change `catch(e){}` to `catch(e){ console.log('Prerequisite check failed:', e.message); }` for debugging.

### PRIORITY 3: Preserve EVERYTHING That Works
ALL passing dimensions must be preserved. Do NOT regress on ANY of these:
- Deep intrinsic integration: prerequisite graph ordering, cognitive demand scaffolding by region
- Strong pedagogy: Bloom-level scaffolding, prerequisite ordering, NPC cascades, 2-day half-life, topic interleaving, 2673 quiz pool, 18 misconception pools
- Compelling narrative: three-tier NPC greeting system, NPC-triggered cascades, persistent NPC identity (18 characters)
- Intrinsic motivation: mastery-only progression (no XP/levels in HUD), font size controls, NPC cascade payoffs
- Hybrid assessment: stealth assessment via circuit wiring/fault tree + LLM evaluation, Bloom filtering by region
- Strong accessibility: 28 ARIA elements, 19/20 keyboard tab stops, light/dark theme, font size toggle, 6.1:1+ contrast
- Learning-first monetisation: all content free, zero monetisation
- Mechanically-rich RPG: 6 stats with d20 checks, 6 classes with abilities, Jury-Rig consistent, mastery decay, negotiate bartering

## Output
Build the improved Docker project in: /Users/kevinlu/Documents/Learning/pupper-v3/reviewer/code/knowledge-quest/iteration-9/
Copy .env: cp /Users/kevinlu/Documents/Learning/pupper-v3/reviewer/code/knowledge-quest/.env.production /Users/kevinlu/Documents/Learning/pupper-v3/reviewer/code/knowledge-quest/iteration-9/.env

After writing all files, run:
```bash
cd /Users/kevinlu/Documents/Learning/pupper-v3/reviewer/code/knowledge-quest/iteration-9 && NOTES_PATH=/Users/kevinlu/Documents/Learning/pupper-v3/learning/notes docker compose up --build -d
```
Then verify: curl -s http://localhost:3000/api/health && curl -s http://localhost:3000/api/stats

Notes path: /Users/kevinlu/Documents/Learning/pupper-v3/learning/notes

Focus your effort on the tutorial/onboarding. This is the #1 priority. Do NOT regress on passing dimensions.
