# Knowledge Quest - Design Specification

## Topic
Electronics, electrical engineering, robotics, manufacturing, and applied physics.

## Learning Objectives (Bloom's-Mapped)

| Objective | Bloom's Level | Game Mechanic |
|-----------|--------------|---------------|
| Define fundamental components (resistor, capacitor, etc.) | Remember (1) | Term challenges at merchant NPCs and terminals |
| Explain how components work and interact | Understand (2) | NPC dialogue encounters with knowledge panels |
| Apply circuit analysis to diagnose problems | Apply (3) | Investigation encounters with skill checks |
| Analyze relationships between concepts | Analyze (4) | Puzzle chambers requiring concept connections |
| Evaluate design tradeoffs | Evaluate (5) | Guardian encounters with higher-level questions |
| Design solutions to novel problems | Create (6) | Freeform input encounters in advanced regions |

## Content Map & Prerequisites
```
Workshop (Tier 1: Micro-context)
  └─ Resistors, Capacitors, Inductors, Diodes, Voltage
      └─ Laboratory (Tier 2: Micro-context)
          └─ Transistors, MOSFETs, BJTs, Op-Amps
              └─ Foundry (Tier 3: Quick-context)
                  └─ PCB Design, Soldering, SMD, 3D Printing
                      └─ Signal Nexus (Tier 4: Quick-context)
                          └─ I2C, SPI, CAN Bus, PWM
                              └─ Control Sanctum (Tier 5: Quick-context)
                                  └─ STM32, Clock Systems, ADC, IMU
                                      └─ Motion Arena (Tier 6: Small-context)
                                          └─ PID, Kinematics, Gait Control, RL
```

## LM-GM Framework Mapping

| Learning Mechanic | Game Mechanic | Integration Check |
|-------------------|---------------|-------------------|
| Recall definitions | Merchant/terminal encounters demand terminology | Removing definitions breaks merchant interaction |
| Explain concepts | NPC dialogues require articulating understanding | NPCs only share knowledge when player demonstrates comprehension |
| Apply knowledge | Investigation encounters require diagnosing devices | Diagnosis IS the gameplay - can't fix without understanding |
| Analyze connections | Puzzle chambers link concepts together | Puzzles are unsolvable without connecting topics |
| Evaluate tradeoffs | Guardian encounters pose higher-order questions | Wrong evaluations have combat consequences |

## Spaced Repetition Design
- Every 5 turns, a review opportunity appears naturally in gameplay
- Previously seen but not-mastered topics resurface as encounters
- The mastery system tracks correct answers per topic
- Topics with low mastery scores appear more frequently in encounters
- Review encounters grant bonus XP (positive reinforcement, not punishment)

## Difficulty Curve & ZPD
- Workshop: DC 12, Bloom's Level 1-2 (Remember/Understand)
- Laboratory: DC 14, Bloom's Level 2-3 (Understand/Apply)
- Foundry: DC 16, Bloom's Level 3-4 (Apply/Analyze)
- Signal Nexus: DC 18, Bloom's Level 4-5 (Analyze/Evaluate)
- Control Sanctum: DC 20, Bloom's Level 5 (Evaluate)
- Motion Arena: DC 22, Bloom's Level 5-6 (Evaluate/Create)

## Assessment Design
- Open-ended text input is primary (generation > recognition)
- Keyword matching evaluates understanding, not exact wording
- Multiple paths to demonstrate knowledge (answer, skill check, investigation)
- Wrong answers always reveal correct information (formative, not punitive)
- Mastery tracked per topic with correct/attempt ratio

## Freemium Design
- **Free**: All 6 regions, full character creation, complete learning objectives, core quest line
- **Premium**: Advanced classes (Quantum Sage, etc.), bonus regions, cosmetics, challenge modes
- Core learning is never gated behind premium content

## Architecture
- Docker Compose: PostgreSQL (pgvector) + Python importer + Node.js server
- 185 Obsidian notes imported with vector embeddings
- Hybrid search (semantic + full-text) via RRF
- Single-page HTML frontend with localStorage persistence
- Mobile-responsive, dark theme, touch-friendly
