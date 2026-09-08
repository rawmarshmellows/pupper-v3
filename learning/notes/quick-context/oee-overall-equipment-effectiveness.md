---
topic: OEE (Overall Equipment Effectiveness)
created: 2026-01-14
---

> **Related:** [[quick-context/integration-failure-modes-solutions]]

> **TL;DR:** OEE decomposes equipment losses into Availability, Performance, and Quality—multiplied together—revealing whether you're losing capacity to breakdowns, slow cycles, or defects.

# OEE (Overall Equipment Effectiveness)

## The Core Problem

OEE exists because manufacturing plants are black boxes of lost capacity, and without a structured way to decompose losses, everyone argues about symptoms instead of root causes. A machine might run 24/7 and still only deliver 40% of its theoretical output—but *why*?

OEE forces you to answer by splitting losses into three buckets: **Availability** (was the machine running when it should have been, or was it down for changeovers, breakdowns, or waiting for materials?), **Performance** (when running, was it at full speed, or did it slow-cycle due to jams, operator hesitation, or worn components?), and **Quality** (of what it produced, how much was good first-pass versus scrapped or reworked?). You multiply these three percentages together—so 90% availability x 85% performance x 95% quality = 72.7% OEE.

The brilliance is the decomposition: when OEE drops, you immediately know which bucket to investigate. Without this, plant managers chase ghosts—blaming maintenance for downtime when the real issue is micro-stops tanking performance, or congratulating themselves on uptime while quality losses quietly bleed margin. OEE gives everyone a common scoreboard that reveals whether you're losing capacity to breakdowns (maintenance problem), slow cycles (process engineering problem), or defects (quality problem).

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Six Big Losses** | The canonical taxonomy: breakdowns, setup/changeover, minor stops, slow cycles, startup rejects, and production rejects—OEE exists to quantify these |
| **Ideal Cycle Time** | The theoretical minimum time to produce one unit, against which actual cycle times are compared for Performance calculation |
| **Planned Production Time** | The scheduled hours minus planned downtime like meals or maintenance windows—your denominator for Availability |
| **TEEP** | Total Effective Equipment Performance—OEE's bigger sibling that measures against *all* calendar time, exposing capacity hidden in unscheduled shifts |
| **Pareto of Losses** | The analysis technique of ranking losses by impact to focus improvement efforts—"we're losing 12% to changeovers and 3% to breakdowns, so attack changeovers first" |

<details>
<summary><strong>How It Works</strong></summary>

**The OEE Formula:**

```
OEE = Availability x Performance x Quality
```

**Availability** = Run Time / Planned Production Time
- Losses: Breakdowns, setup/changeover, material shortages, operator unavailability

**Performance** = (Ideal Cycle Time x Total Count) / Run Time
- Losses: Minor stops, reduced speed, jams, operator hesitation

**Quality** = Good Count / Total Count
- Losses: Startup rejects, production defects, rework

**Example Calculation:**
- Planned Production Time: 480 minutes (8-hour shift)
- Downtime: 48 minutes (breakdown + changeover)
- Run Time: 432 minutes
- Ideal Cycle Time: 1 minute per unit
- Total Units Produced: 400
- Good Units: 380

Availability = 432/480 = 90%
Performance = (1 x 400)/432 = 92.6%
Quality = 380/400 = 95%
OEE = 90% x 92.6% x 95% = **79.2%**

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The central tension is between OEE as a diagnostic tool versus OEE as a target to be gamed. When you tie bonuses or plant rankings to OEE numbers, Goodhart's Law kicks in hard. Operators learn to run slightly under ideal cycle time to avoid jams (sacrificing performance to protect availability), maintenance teams classify changeovers as "planned downtime" to exclude them from availability losses, and quality inspectors get pressure to pass borderline product.

The other perennial argument is about what "ideal cycle time" means—the theoretical maximum on the nameplate, the best sustained performance ever achieved, or something in between? Set it too aggressive and you're chasing a fantasy; set it too loose and you've baked waste into your baseline.

World-class OEE is often cited as 85%, but this is nearly meaningless across industries: a continuous chemical process might hit 95% easily while a high-mix job shop with constant changeovers struggles to break 60%, and both could be performing excellently for their context. Practitioners who actually use OEE well treat it as a conversation starter ("why did Line 3 drop from 78% to 71% this week?") rather than a leaderboard.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

**Bottling Line Analysis:**

A beverage company's bottling line shows 68% OEE. Breaking it down:
- Availability: 85% (15% lost to changeovers between SKUs and two breakdown events)
- Performance: 88% (minor jams causing micro-stops, running 10% under ideal speed)
- Quality: 91% (startup losses after each changeover, occasional fill-level rejects)

**The Pareto reveals priorities:**
1. Changeovers: 8% of total losses (SMED project to reduce changeover time)
2. Micro-stops: 6% of total losses (investigate jam root causes at infeed)
3. Startup rejects: 4% of total losses (tune fill parameters for faster startup)
4. Breakdowns: 3% of total losses (preventive maintenance on the problematic filler valve)

Without OEE decomposition, management might have blamed "old equipment" and requested capital for a new line. The data showed the existing line could reach 80%+ OEE with changeover reduction and jam elimination—no capital required.

**The one thing most outsiders get wrong about this is...** thinking 85% OEE is a universal target. World-class for a dedicated single-product line might be 95%; world-class for a high-mix job shop with 50 changeovers per day might be 55%. The number is meaningless without context—OEE is a diagnostic tool for identifying loss categories, not a leaderboard for comparing dissimilar operations.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/teep]]** - Extends OEE to measure against all calendar time, revealing hidden capacity in unscheduled hours
- **[[quick-context/isa-95-levels]]** - Level 3 MES systems are where OEE calculations typically live and get reported

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A line has 95% Availability, 70% Performance, and 98% Quality. What's the OEE, and which factor should the team focus on improving?
<details>
<summary>Answer</summary>
OEE = 95% x 70% x 98% = 65.2%. Focus on Performance—it's the weakest factor at 70%. Investigate why the line runs 30% below ideal cycle time: minor stops, slow cycles, or operators running conservatively to avoid jams.
</details>

**Q2:** Why might a plant with 60% OEE actually be performing well, while one at 80% OEE is underperforming?
<details>
<summary>Answer</summary>
Context matters enormously. A high-mix job shop with 200 SKUs and constant changeovers at 60% OEE might be excellent—changeovers are inherent to the business model. A dedicated single-product line at 80% OEE might be underperforming if similar lines in the industry achieve 90%+. OEE must be benchmarked against comparable operations, not arbitrary targets.
</details>

**Q3:** How does Goodhart's Law manifest when OEE is tied to bonuses?
<details>
<summary>Answer</summary>
People optimize the metric, not the underlying performance. Examples: operators run slower to avoid jams (protecting availability at the cost of performance), maintenance reclassifies breakdowns as "planned downtime," quality passes borderline product, and changeovers get scheduled during breaks to exclude them from availability calculations. The number improves while actual productivity stagnates.
</details>

**Q4:** What are the "Six Big Losses" and how do they map to OEE's three factors?
<details>
<summary>Answer</summary>
The Six Big Losses are: (1) Breakdowns and (2) Setup/Changeover, which reduce Availability; (3) Minor Stops and (4) Slow Cycles, which reduce Performance; (5) Startup Rejects and (6) Production Rejects, which reduce Quality. This taxonomy helps teams categorize losses and assign ownership—maintenance owns breakdowns, process engineering owns slow cycles, quality owns defects.
</details>

**Q5:** Why is "Ideal Cycle Time" such a contentious parameter in OEE calculations?
<details>
<summary>Answer</summary>
Ideal Cycle Time is the denominator for Performance calculation, so its definition directly affects the OEE number. Options include: nameplate maximum (often unrealistic), best-ever sustained performance (hard to verify), or engineering estimate (potentially sandbagged). Set it too aggressive and you're chasing fantasy numbers; set it too loose and you've baked waste into your baseline. Different stakeholders have incentives to manipulate this number in different directions.
</details>

</details>
