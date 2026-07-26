---
topic: Miller Heiman Strategic Selling / LAMP
created: 2026-02-10
updated: 2026-02-10
---

# Miller Heiman Strategic Selling / LAMP

> **Related:** [[learning/notes/quick-context/strategic-selling-buyer-roles]] | [[learning/notes/micro-context/push-pull-vs-open-drain|Push-Pull vs Open-Collector / Open-Drain]] | [[learning/notes/quick-context/inside-the-triangle|Inside the Triangle — Complete Op-Amp / Comparator Signal Path]] | [[learning/notes/quick-context/qwiic-stemma-qt-i2c|Qwiic / STEMMA QT — Plug-and-Play I2C Connector Ecosystem]] | [[learning/notes/quick-context/tlv7211-as-lmc7211-replacement|TLV7211 / TLV7211A as an LMC7211-N Replacement]]

> **TL;DR:** Miller Heiman Strategic Selling is an account planning methodology that maps stakeholder roles and builds 1-3 year strategic plans through its LAMP (Large Account Management Process) framework, using the "Gold Sheet" to systematically research, strategize, and execute complex B2B deals.

## Human notes

Give a more in-depth dive for what a Gold Sheet summary will look like.

## The Core Problem

Complex B2B sales involve multiple stakeholders with different priorities, and reps often lose deals because they fail to identify all decision-makers or misunderstand who actually controls the budget. Without a systematic approach to account planning, sales teams rely on relationship luck rather than strategic positioning, leading to unpredictable revenue and wasted effort on accounts that were never winnable.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Gold Sheet** | A structured multi-page document that captures the complete strategic picture of a large account—situation appraisal, charter statement, stakeholder map, goals, focus/stop investments, and revenue targets |
| **Economic Buyer** | The person with final authority to release funds and approve the purchase; they can say "yes" when everyone else says "no" |
| **User Buyer** | The person(s) who will actually use your product day-to-day and judge success based on job impact |
| **Technical Buyer** | The gatekeeper who screens vendors against specifications, compliance, or technical requirements—they can't approve but can veto |
| **Coach** | An internal advocate who provides intelligence about the organization's decision process and guides your strategy |

<details>
<summary><strong>How It Works</strong> — The LAMP three-phase process</summary>

LAMP (Large Account Management Process) structures account planning into three distinct phases executed over 1-3 year horizons:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         LAMP PLANNING CYCLE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   PHASE 1: RESEARCH              PHASE 2: STRATEGY         PHASE 3: EXECUTE
│   ══════════════════             ═════════════════         ═══════════════
│                                                                          │
│   ┌─────────────────┐           ┌─────────────────┐       ┌─────────────┐
│   │ Map the Account │           │ Define Objectives│       │ Implement   │
│   │   Ecosystem     │    ──►    │ Aligned to Their │  ──►  │ & Refine    │
│   │                 │           │     Goals        │       │             │
│   └─────────────────┘           └─────────────────┘       └─────────────┘
│                                                                          │
│   • Who are the buyers?         • What do THEY need?      • Execute plays│
│   • What's the org chart?       • Where's whitespace?     • Track metrics│
│   • Who influences whom?        • What's our unique fit?  • Adjust course│
│   • What's their buying         • 90-day action items     • Review health│
│     history?                                                             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**The Four Buyer Roles**

Every significant deal has these four roles (sometimes one person fills multiple):

```
                    ┌─────────────────────┐
                    │   ECONOMIC BUYER    │
                    │   "The Wallet"      │
                    │   Final yes/no on $ │
                    └──────────┬──────────┘
                               │ approves
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
   │  USER BUYER   │   │TECHNICAL BUYER│   │    COACH      │
   │ "Day-to-day"  │   │ "The Filter"  │   │ "The Guide"   │
   │               │   │               │   │               │
   │ Judges by job │   │ Screens specs │   │ Gives intel   │
   │ impact        │   │ Can veto      │   │ on process    │
   └───────────────┘   └───────────────┘   └───────────────┘
```

The Gold Sheet captures all four roles plus their current stance (growth, trouble, even keel, overconfident) and your coverage strategy for each.

</details>

<details>
<summary><strong>The Key Tension</strong> — Depth vs. scalability</summary>

LAMP's comprehensive approach creates an inherent tension:

| Deep LAMP | Lightweight Adaptation |
|-----------|----------------------|
| Full Gold Sheets per account | Simplified templates |
| Quarterly strategic reviews | Monthly check-ins |
| 3+ hours per account plan | 30-60 minutes |
| Works for 10-20 accounts | Scales to 50+ |
| Maximum strategic insight | Good-enough coverage |

**The practitioner debate:** Purists argue the Gold Sheet's depth is the whole point—shortcuts lose the strategic value. Pragmatists counter that most B2B teams can't afford that depth for every account and need tiered approaches (full LAMP for top 10, simplified for the rest).

Modern adaptations often digitize the Gold Sheet into CRM fields, losing some nuance but gaining scalability and consistency.

</details>

<details>
<summary><strong>Concrete Example</strong> — A complete Gold Sheet walkthrough</summary>

**Scenario:** You're selling infrastructure monitoring software to a 500-person manufacturing company. Below is a complete Gold Sheet demonstrating all major sections.

---

### GOLD SHEET: Precision Manufacturing Inc.

---

#### SECTION 1: ACCOUNT OVERVIEW

```
┌────────────────────────────────────────────────────────────────────────┐
│ ACCOUNT IDENTIFICATION                                                 │
├────────────────────────────────────────────────────────────────────────┤
│ Account Name:     Precision Manufacturing Inc.                         │
│ Industry:         Industrial Manufacturing (Aerospace Components)      │
│ Employees:        500                                                  │
│ Annual Revenue:   $120M                                                │
│ Fiscal Year End:  December                                             │
│ HQ Location:      Cleveland, OH                                        │
│ Account Owner:    Sarah Chen (Sr. AE)                                  │
│ Last Review:      2025-11-15                                           │
└────────────────────────────────────────────────────────────────────────┘

CURRENT RELATIONSHIP STATUS
───────────────────────────
Current Revenue:     $0 (New Logo)
Target Revenue:      $85K ARR (Year 1) → $180K ARR (Year 3)
Relationship Stage:  Prospect → Active Evaluation
Buy-Sell Hierarchy:  Vendor (we perceive Partner; they see us as Vendor)
```

---

#### SECTION 2: SITUATION APPRAISAL

The fundamental question: *"What are we here to do for this customer?"*

```
┌────────────────────────────────────────────────────────────────────────┐
│ CUSTOMER'S BUSINESS CONTEXT                                             │
├────────────────────────────────────────────────────────────────────────┤
│ • Aerospace supply chain tightening; customers demanding 99.9% uptime   │
│ • Lost $340K in Q2 from unplanned production line downtime              │
│ • Aging monitoring infrastructure (10+ year-old SCADA integration)      │
│ • New CTO hired 8 months ago, mandated "digital transformation"         │
│ • Competitor (Apex Controls) installed at 2 of their 5 plants           │
└────────────────────────────────────────────────────────────────────────┘

FIELD OF PLAY TRENDS (Industry + Account-Specific)
──────────────────────────────────────────────────
[+] Aerospace OEMs requiring supply chain visibility → vendors must prove uptime
[+] Regulatory push for predictive maintenance documentation (FAA audit trail)
[+] Remote monitoring adoption accelerated post-2020 → their plants are ready
[-] Capex budgets under scrutiny; CFO favoring opex/subscription models
[-] IT team stretched thin; complex implementations get deprioritized

FIELD OF PLAY OPPORTUNITIES
───────────────────────────
1. Plants 3, 4, 5 have NO monitoring solution → greenfield opportunity
2. CTO's digital transformation initiative needs early wins → we can be that win
3. Apex Controls contract renewal in 14 months → displacement opportunity
4. Upcoming FAA audit (Q3) → compliance urgency creates timeline pressure
```

---

#### SECTION 3: CHARTER STATEMENT

*A Charter Statement defines what you're committing to achieve FOR the customer—not your sales quota.*

```
┌────────────────────────────────────────────────────────────────────────┐
│ CHARTER STATEMENT                                                      │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│ "Precision Manufacturing's Operations Division will achieve 99.5%      │
│  production uptime across all five plants within 24 months by          │
│  deploying unified infrastructure monitoring that enables predictive   │
│  maintenance, reduces mean-time-to-resolution from 4 hours to under    │
│  30 minutes, and provides the audit-ready compliance documentation     │
│  required for FAA Tier-1 supplier certification."                      │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

WHY THIS CHARTER WORKS:
• Specific outcome (99.5% uptime) not vague "improve operations"
• Tied to THEIR strategic need (FAA certification, not our quota)
• Quantified improvement (4 hrs → 30 min MTTR)
• Timeline alignment with their fiscal planning (24 months)
• Customer could present this to their board as their initiative
```

**Bad Charter Example (for contrast):**
> "We will sell Precision Manufacturing $180K of monitoring software that will transform their operations and help us exceed Q4 quota."

This fails because it's about *us*, not *them*.

---

#### SECTION 4: STRATEGIC PLAYERS MAP

```
┌────────────────────────────────────────────────────────────────────────┐
│ ECONOMIC BUYER                                                          │
├────────────────────────────────────────────────────────────────────────┤
│ Name:       Maria Chen, CFO                                             │
│ Stance:     EVEN KEEL — Not feeling acute pain yet                      │
│ Priority:   Cost avoidance > cost reduction; ROI proof required         │
│ Access:     Limited (2 meetings to date, via CTO introduction)          │
│ Win Theme:  "Prevent the $340K downtime losses from recurring"          │
│ Red Flags:  Prefers capex; we're subscription. Needs finance packaging. │
│ Action:     Build ROI model showing 14-month payback; present Q1        │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ USER BUYERS                                                             │
├────────────────────────────────────────────────────────────────────────┤
│ Name:       James Wu, VP Operations (Primary)                           │
│ Stance:     TROUBLE — Current tools failing; 3AM pages weekly           │
│ Priority:   Sleep. Fewer false alarms. Protect his team's sanity.       │
│ Access:     Strong (weekly calls, toured their Plant 3 facility)        │
│ Win Theme:  "You'll stop being the 3AM firefighter"                     │
│ Red Flags:  Burned by last vendor; needs proof of onboarding support    │
│ Action:     Reference call with similar manufacturing customer          │
│                                                                         │
│ Name:       Diane Foster, Plant 3 Manager (Secondary)                   │
│ Stance:     GROWTH — Sees opportunity to be the "model plant"           │
│ Priority:   Be first to deploy; career visibility with new CTO          │
│ Access:     Moderate (met twice; James's direct report)                 │
│ Win Theme:  "Your plant becomes the template for the other four"        │
│ Action:     Position pilot as her initiative; give her the spotlight    │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ TECHNICAL BUYER                                                         │
├────────────────────────────────────────────────────────────────────────┤
│ Name:       Priya Patel, Director of IT Security                        │
│ Stance:     EVEN KEEL — Will screen; not emotionally invested           │
│ Priority:   SOC2, on-prem option, no new attack surface                 │
│ Access:     Moderate (1 deep-dive; scheduled follow-up)                 │
│ Win Theme:  "This passes your audit without you babysitting it"         │
│ Red Flags:  Previous vendor failed security review; she's skeptical     │
│ Action:     Provide SOC2 Type II report + architecture review session   │
│                                                                         │
│ Name:       Tom Bradley, IT Infrastructure Manager                      │
│ Stance:     EVEN KEEL — Cares about integration complexity              │
│ Priority:   No weekend deployments; clean API; minimal handholding      │
│ Access:     Limited (1 call; defers to Priya on decisions)              │
│ Action:     Technical POC with their existing stack; prove easy setup   │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│ COACH                                                                   │
├────────────────────────────────────────────────────────────────────────┤
│ Name:       Alex Rivera, IT Manager (reports to James)                  │
│ Relationship: Former customer at previous company (strong trust)        │
│ Intel Provided:                                                         │
│   • Budget cycle in Q4; must get on CTO's priority list by October      │
│   • James has CFO's ear after Q2 downtime incident                      │
│   • Apex Controls renewal is NOT a done deal; CTO unhappy with them     │
│   • Maria (CFO) listens to compliance/audit angles more than ROI        │
│                                                                         │
│ Coach Development:                                                      │
│   • Currently: Provides intel informally                                │
│   • Goal: Gets him to actively advocate in internal meetings            │
│   • Action: Prep him with talking points for CTO's October planning     │
└────────────────────────────────────────────────────────────────────────┘
```

---

#### SECTION 5: STRENGTHS, VULNERABILITIES & COMPETITION

```
OUR STRATEGIC STRENGTHS (Why We Can Win)
────────────────────────────────────────
✓ Manufacturing-specific monitoring (vs. generic IT tools)
✓ SOC2 Type II certified; meets their compliance bar
✓ Alex Rivera as internal coach with credibility
✓ Subscription model aligns with CTO's opex preference
✓ 30-day POC program reduces perceived risk

OUR CRITICAL VULNERABILITIES (What Could Kill the Deal)
───────────────────────────────────────────────────────
✗ CFO prefers capex; our subscription model is friction
✗ Limited brand recognition vs. Apex Controls
✗ No current reference customer in aerospace manufacturing
✗ Priya skeptical after previous vendor security failure

COMPETITIVE LANDSCAPE
─────────────────────
┌──────────────────┬───────────────────────────────────────────────────┐
│ Apex Controls    │ Incumbent at Plants 1, 2. Renewal in 14 months.   │
│ (Primary)        │ CTO unhappy with support response times.          │
│                  │ Our angle: "We respond in hours, not days"        │
├──────────────────┼───────────────────────────────────────────────────┤
│ DataDog          │ Generic IT monitoring. Not manufacturing-aware.   │
│ (Secondary)      │ Tom evaluated; rejected for OT/IT gap.            │
│                  │ Our angle: We speak their operational language    │
├──────────────────┼───────────────────────────────────────────────────┤
│ Status Quo       │ Spreadsheets + tribal knowledge + 3AM pages       │
│ (Real enemy)     │ The real risk: they do nothing for another year   │
└──────────────────┴───────────────────────────────────────────────────┘
```

---

#### SECTION 6: GOALS & INVESTMENT PRIORITIES

```
RELATIONSHIP GOALS (Qualitative)
────────────────────────────────
Year 1: Establish as trusted advisor to Operations team
Year 2: Expand relationship to CTO-level strategic partner
Year 3: Become preferred vendor; displace Apex Controls entirely

FOCUS INVESTMENTS (Where We Will Invest Resources)
──────────────────────────────────────────────────
1. Executive Sponsor Program — Assign our VP Ops to build CFO relationship
2. Reference Development — Get aerospace manufacturer case study by Q2
3. Technical Enablement — Custom integration docs for their SCADA stack
4. Coach Development — Enable Alex to advocate in internal meetings

STOP INVESTMENTS (What We Will NOT Do)
──────────────────────────────────────
✗ Don't pursue Plants 1, 2 until Apex renewal window (resource waste)
✗ Don't discount aggressively; it signals desperation to CFO
✗ Don't engage Procurement until Economic Buyer is committed
```

---

#### SECTION 7: REVENUE TARGETS & 90-DAY ACTION PLAN

```
REVENUE TARGETS
───────────────
                    Year 1         Year 2         Year 3
                    ──────         ──────         ──────
Base Platform:      $65,000        $65,000        $65,000
Expansion (Plants): —              $75,000        $115,000
Premium Support:    $20,000        $40,000        $45,000
                    ───────        ───────        ────────
Total ARR:          $85,000        $180,000       $225,000
```

```
90-DAY ACTION PLAN (October → December)
───────────────────────────────────────
┌──────────┬─────────────────────────────────────────────┬──────────────┐
│ Week     │ Action                                      │ Owner        │
├──────────┼─────────────────────────────────────────────┼──────────────┤
│ Week 2   │ Technical deep-dive with Priya (SOC2 focus) │ SE Team      │
│ Week 3   │ Deliver ROI model to James for internal use │ Sarah Chen   │
│ Week 4   │ Reference call: James ↔ Similar customer    │ CSM Team     │
│ Week 5   │ Prep Alex with October planning talking pts │ Sarah Chen   │
│ Week 6   │ Business case workshop with James           │ Sarah + Mgr  │
│ Week 8   │ Alex warm-intro to Maria (CFO)              │ Alex Rivera  │
│ Week 10  │ Executive sponsor dinner (our VP + Maria)   │ VP Sales     │
│ Week 12  │ Proposal to Maria; James presents internal  │ Sarah Chen   │
└──────────┴─────────────────────────────────────────────┴──────────────┘

SUCCESS METRICS
───────────────
□ James verbally commits to pilot by Week 8
□ Maria agrees to proposal meeting by Week 10
□ SOC2 review passed (Priya approval) by Week 6
□ Pilot contract signed by December 15
```

---

#### SECTION 8: ACCOUNT HEALTH INDICATORS

```
RED FLAGS (Current)                    GREEN FLAGS (Current)
───────────────────                    ─────────────────────
⚠ CFO capex preference                 ✓ Strong coach in Alex
⚠ No aerospace reference yet           ✓ User Buyer (James) in TROUBLE stance
⚠ Priya skeptical from past burn       ✓ CTO mandated digital transformation
                                       ✓ Apex Controls relationship weakening

NEXT REVIEW: January 15, 2026
ACCOUNT HEALTH: YELLOW (Winnable but requires active management)
```

---

**The one thing most outsiders get wrong about this is...** they think the four buyer roles are job titles. They're not—they're *functions*. A single person can be both Economic and User Buyer in a small company. In large enterprises, you might have three User Buyers across different departments. The roles describe decision-making power, not org chart positions.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[quick-context/meddpicc-qualification-framework]]** — MEDDPICC is a qualification complement to LAMP; use MEDDPICC to validate deal viability, LAMP to plan account strategy
- **[[quick-context/challenger-sale-methodology]]** — Challenger provides the *how* of customer interactions; LAMP provides the *who* and *when*
- **[[quick-context/mcdonald-kam-model]]** — McDonald's relationship maturity model adds a diagnostic layer to LAMP's stakeholder mapping
- **[[quick-context/sandler-kare-segmentation]]** — KARE helps decide which accounts deserve full LAMP treatment vs. lighter touch
- **[[quick-context/whitespace-mapping]]** — Visual tool for identifying expansion opportunities; feeds into LAMP's situation appraisal
- **Value Selling** — Complementary methodology for quantifying the business case LAMP identifies

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** What's the difference between a Technical Buyer and an Economic Buyer?
<details>
<summary>Answer</summary>
Technical Buyer screens for specifications and can veto but cannot approve. Economic Buyer has final authority to release funds—they can say yes when everyone else says no. See: 5 Essential Terms.
</details>

**Q2:** Why does the Charter Statement focus on the customer's outcomes rather than your sales targets?
<details>
<summary>Answer</summary>
A Charter Statement that reads like a sales goal ("sell $180K") can't be shared with the customer or used internally by your champion. A customer-centric charter ("achieve 99.5% uptime") becomes something the customer's team can present to their leadership as *their* initiative. It also forces you to understand what success looks like from their perspective, which shapes your entire strategy.
</details>

**Q3:** In the example Gold Sheet, why is "Status Quo" listed as a competitor alongside Apex Controls?
<details>
<summary>Answer</summary>
The real competition is often inaction, not another vendor. Even if you beat Apex Controls in every evaluation, the customer might decide "we'll revisit this next year" or "we'll make do with spreadsheets." Treating status quo as a competitor forces you to address the *cost of doing nothing*—in this case, the $340K downtime losses.
</details>

**Q4:** The example shows Alex Rivera (Coach) providing intel but not yet actively advocating. What's the strategic value of developing him further?
<details>
<summary>Answer</summary>
A coach who only provides information is useful but limited—you still have to do all the selling. A coach who actively advocates speaks on your behalf in meetings you're not in. The difference: Alex telling you "budget cycle is in Q4" vs. Alex saying to the CTO "we should prioritize this monitoring initiative for October planning." The Gold Sheet's "Coach Development" section tracks this progression.
</details>

**Q5:** If Precision Manufacturing's CFO (Maria) strongly prefers capex purchases but your product is subscription-only, how would you adjust the strategy using the Gold Sheet framework?
<details>
<summary>Answer</summary>
The Gold Sheet reveals Maria listens to "compliance/audit angles more than ROI" (per Coach intel). The strategy adjustment: (1) Reframe the subscription as a compliance advantage—"always current = audit-ready" vs. capex software that ages, (2) Use the FAA audit timeline (Q3) to create urgency that bypasses the capex preference, (3) Have your Executive Sponsor (VP Ops) speak to Maria about how other aerospace suppliers handle this. The Gold Sheet's "Focus Investments" section should add "Finance packaging—explore annual prepay or capex-like structuring" as a resource priority.
</details>

</details>

## Sources

- [Korn Ferry LAMP® Overview](https://www.kornferry.com/capabilities/leadership-professional-development/training-certification/sales/large-account-management-process)
- [Miller Heiman LAMP Methodology](https://www.sybill.ai/blogs/miller-heiman-lamp)
- [Book Review: The New Successful Large Account Management](https://kimtasso.com/book-review-the-new-successful-large-account-management-by-robert-b-miller-and-stephen-e-heiman-with-tad-tuleja-kam-key-account-management/)
- [bdm Sales Training LAMP Courses](https://bdmsalestraining.co.uk/courses/large-account-management-process)
- [Growing Strategic Accounts - Charter Statement Examples](https://www.linkedin.com/pulse/growing-strategic-accounts-what-really-matters-david-gogolkiewicz)
