# Knowledge Quest -- Iteration 4 Design Specification

## Fundamental Redesign Summary

Iteration 4 makes three structural changes to break out of the score plateau:

### 1. XP/Level System Removed -- Mastery Milestones Only
- **Before**: XP accumulates, levels grant +5 HP/+3 MP, gold earned universally, de-emphasized but functional
- **After**: XP and level-up system completely removed from code. No `state.char.level`, no `state.char.xp`, no `grantReward()` function. Progression is purely through mastery milestones: Novice -> Apprentice -> Journeyman -> Master per region. Gold exists ONLY for merchant encounters (Negotiate), not as a universal reward.

### 2. Intrinsic Integration Deepened
- **Cross-domain challenges**: Reference answers now built from actual document `key_insight` and `tldr` fields fetched via `/api/topics/insights`, not topic name lists
- **Negotiate redesigned**: 3-step bartering encounter where Step 1 = identify the component by specs, Step 2 = evaluate quality by understanding what specs matter, Step 3 = price determined by demonstrated understanding. Understanding directly determines the gold price.
- **Symptom generation**: For topics that don't match keyword detection, uses TL;DR/key_insight content to construct contextual failure scenario instead of generic fallback
- **Concept cascades**: When a player masters two related topics (e.g., capacitors + inductors), a cascade encounter fires that challenges them to explain the combined concept (LC resonance). The learning IS the reward.

### 3. Pedagogical Soundness Strengthened
- **Topic-specific misconceptions**: `generateWrongAttempt()` has 20+ domain-specific misconception pools (capacitors store current, resistors in parallel add like series, etc.) instead of 5 generic templates
- **Fallback threshold raised**: Keyword fallback requires 50% match for "correct" (was 30%)
- **Quiz variety increased**: Importer now extracts questions from Summary and Key Insight sections in addition to Test Your Understanding. Each document with summary/insight generates 2-4 additional questions.

## Knowledge Journal
A new persistent structure that records mastered concepts with their key insights and connections to other topics. Players can review their journal from the world map to see their growing web of understanding.

## Concept Cascade System
Pre-defined pairs of topics that combine into higher-order concepts:
- capacitor + inductor -> LC Resonance
- resistor + capacitor -> RC Time Constant
- PID + IMU -> Sensor-Driven Control
- ADC + voltage -> Signal Digitization
- MOSFET + PWM -> Power Switching
- SPI + STM32 -> Peripheral Communication
- CAN bus + PID -> Distributed Control

When both topics in a pair are mastered, the cascade fires automatically, presenting a challenge that requires understanding the combined concept.

## What Was Preserved (Passing Dimensions)
- Narrative structure: Circuit Citadel, 6 regions, mystery system, category filtering
- Assessment design: Component Choice, Circuit Build stealth assessment, semantic eval via OpenRouter
- Accessibility: Dark theme, mobile-responsive, ARIA labels, reduced-motion media query added
- Freemium monetisation: All content free, premium features defined but not gated
