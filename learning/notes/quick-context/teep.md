---
topic: TEEP (Total Effective Equipment Performance)
created: 2026-01-14
---

> **Related:** [[learning/notes/quick-context/isa-95-levels]]

> **TL;DR:** TEEP extends OEE by measuring against all calendar time (24/7/365), revealing the true utilization of capital assets and exposing capacity hidden in unscheduled shifts.

# TEEP (Total Effective Equipment Performance)

## The Core Problem: OEE Hides Unused Capacity

TEEP exists because OEE lies to you by omission. OEE measures how well you use equipment *during scheduled production time*, but says nothing about the other 8,760 hours in a year. A line running one shift with 85% OEE looks great on paper, but you're only using 28% of your theoretical capacity.

TEEP exposes this by measuring against *all calendar time*—24 hours a day, 365 days a year. The formula is simple: TEEP = OEE x Utilization, where Utilization is scheduled time divided by total calendar time.

If this metric doesn't exist, you get capital planning disasters: companies buy new equipment when they could run a second shift, or they benchmark facilities without accounting for different scheduling practices. A plant running two shifts at 70% OEE might actually be outperforming one running a single shift at 90% OEE, and without TEEP you'd never see it.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Utilization** | The percentage of calendar time that's actually scheduled for production—the multiplier that distinguishes TEEP from OEE |
| **Loading** | What the industry calls scheduled production time as a fraction of available time, sometimes used interchangeably with utilization |
| **Calendar Time** | The 8,760 hours per year (or 168 hours per week) that serves as TEEP's unforgiving denominator |
| **Hidden Capacity** | The gap between current scheduling and theoretical 24/7 operation, which TEEP quantifies in dollar terms |
| **Asset Intensity** | How much output you extract per unit of capital invested—what TEEP ultimately measures at the strategic level |

<details>
<summary><strong>How It Works</strong></summary>

**The TEEP Formula:**

```
TEEP = OEE x Utilization

Where:
- OEE = Availability x Performance x Quality (during scheduled time)
- Utilization = Scheduled Production Time / Total Calendar Time
```

**Example:**
- A line runs one 8-hour shift, 5 days per week
- Weekly calendar time: 168 hours
- Scheduled time: 40 hours
- OEE during scheduled time: 85%

Utilization = 40/168 = 23.8%
TEEP = 85% x 23.8% = **20.2%**

This reveals that despite "excellent" 85% OEE, the company uses only 20% of the equipment's theoretical capacity. Adding a second shift would nearly double output without capital investment.

**Comparison:**
| Scenario | OEE | Utilization | TEEP | Actual Output |
|----------|-----|-------------|------|---------------|
| Plant A: 1 shift, high OEE | 90% | 24% | 21.6% | 1,000 units/week |
| Plant B: 3 shifts, moderate OEE | 70% | 71% | 49.7% | 2,300 units/week |

Plant B produces 2.3x more despite "worse" OEE.

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The central tension is **demonstrated capacity vs. theoretical capacity** and what counts as "avoidable" downtime. Purists argue TEEP should be the primary metric because it reveals all hidden capacity—every holiday, every weekend, every maintenance window is time you *chose* not to produce.

Pragmatists counter that not all calendar time is actually available: you can't run during legally mandated shutdowns, market demand might not justify additional shifts, and some processes require cooldown periods. The debate gets contentious around planned downtime: if you schedule a maintenance day, does that represent lost capacity (TEEP says yes) or responsible asset management (operations says yes)?

Organizations fight about whether TEEP is a strategic planning tool showing where to invest, or a stick that makes every site look bad regardless of business context.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

**Capital Planning Decision:**

A medical device manufacturer needs 30% more capacity. Two options:
1. Buy a new $2M production line
2. Add shifts to existing equipment

**Current State Analysis:**
- Two production lines, each running single shift (40 hrs/week)
- Line 1 OEE: 82%, Line 2 OEE: 78%
- Average OEE: 80%
- Utilization: 40/168 = 23.8%
- TEEP: 80% x 23.8% = 19%

**TEEP reveals the answer:**
At 19% TEEP, the plant uses less than one-fifth of its theoretical capacity. Adding a second shift on both lines would:
- Double scheduled time: Utilization becomes 47.6%
- Even with slightly lower second-shift OEE (75%), TEEP = 75% x 47.6% = 35.7%
- Nearly doubles capacity with minimal capital investment

The new line isn't needed—the hidden capacity was always there. Without TEEP, leadership would have spent $2M solving a problem that required only hiring and training.

**The one thing most outsiders get wrong about this is...** thinking low TEEP is always bad. A single-shift operation with 20% TEEP has 80% of its capacity available for growth without capital investment—that's a strategic reserve, not a failure. TEEP becomes a problem only when you're buying new equipment while existing assets sit idle, or when you're benchmarking plants without accounting for scheduling differences.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/oee-overall-equipment-effectiveness]]** - The foundation metric that TEEP extends; must understand OEE's three factors before TEEP makes sense
- **[[quick-context/isa-95-levels]]** - Where capacity planning decisions (Level 4) meet production execution (Level 3)

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A plant manager boasts 92% OEE. Why might this be misleading without knowing the TEEP?
<details>
<summary>Answer</summary>
92% OEE only measures performance during scheduled production. If the plant runs one shift (24% utilization), TEEP is only 22%—meaning 78% of the capital asset sits idle. A competitor with 75% OEE running three shifts would have TEEP of 53% and produce more than twice as much from equivalent equipment.
</details>

**Q2:** Why do some practitioners argue TEEP is unfair to operations teams?
<details>
<summary>Answer</summary>
Operations teams control OEE—how well they execute during scheduled time. They don't control Utilization—that's a business decision about how many shifts to run, driven by demand, labor availability, and strategy. Judging operations on TEEP penalizes them for decisions made by leadership. TEEP is a capital efficiency metric, not an operational performance metric.
</details>

**Q3:** When would a low TEEP with high OEE be the *correct* business strategy?
<details>
<summary>Answer</summary>
When demand doesn't justify more production: niche products with limited markets, seasonal businesses, or when holding finished goods inventory is expensive or impossible (fresh food, custom products). Also valid during market downturns or when labor costs for additional shifts exceed the value of incremental production. Low TEEP means you have growth capacity without capital investment—that's an asset, not a problem.
</details>

**Q4:** How does TEEP change capital planning conversations compared to using OEE alone?
<details>
<summary>Answer</summary>
OEE shows how well you use scheduled time; TEEP shows how much theoretical capacity remains untapped. When a plant requests new equipment citing "high OEE," TEEP asks: "But are you using the equipment you have?" A plant at 85% OEE running one shift (TEEP ~20%) has four times more capacity available through scheduling changes than through operational improvements. TEEP forces the question: add shifts or add equipment?
</details>

**Q5:** What's the difference between "Utilization" and "Loading" in TEEP calculations?
<details>
<summary>Answer</summary>
They're often used interchangeably, but some practitioners distinguish them: Utilization is scheduled production time divided by total calendar time (what TEEP uses), while Loading might refer to scheduled time divided by available time (excluding known constraints like holidays or legally mandated shutdowns). The distinction matters when benchmarking across regions with different labor laws or cultural norms around operating schedules.
</details>

</details>
