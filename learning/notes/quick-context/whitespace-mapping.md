---
topic: Whitespace Mapping
created: 2026-02-10
---

# Whitespace Mapping

> **Related:** [[micro-context/can-bus-termination]] | [[micro-context/can-bus-transceiver]] | [[quick-context/can-bus]] | [[quick-context/meddpicc-qualification-framework]]

> **TL;DR:** Whitespace mapping is a visual framework (often a matrix) that plots customer buying centers (divisions, regions, departments) against your product offerings to identify untapped expansion opportunities—cells that are neither won nor lost represent revenue potential hiding inside existing accounts.

## The Core Problem

Account teams often know they should "expand" but lack a systematic way to see where opportunities exist. Without a structured view, expansion becomes opportunistic (waiting for inbound requests) rather than strategic (proactively targeting high-potential gaps). The whitespace map makes invisible revenue visible by showing exactly which products could be sold to which buying centers within an account.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **Buying Center** | A distinct decision-making unit within a customer organization—could be a division, department, region, site, or business unit with its own budget and authority |
| **Whitespace** | Product/buying-center combinations where you have neither won nor lost—unexplored opportunity territory |
| **Heat Map** | A color-coded whitespace grid showing status: Won (green), Pipeline (yellow), Opportunity (blue), N/A (gray), Lost to Competitor (red) |
| **Cell Revenue** | Estimated ARR potential for each whitespace cell—used to prioritize which opportunities to pursue first |
| **Penetration Rate** | The percentage of total addressable whitespace cells that have been won—a measure of account development maturity |

<details>
<summary><strong>How It Works</strong> — Building and using the whitespace matrix</summary>

The whitespace map is a simple 2D grid:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      WHITESPACE MAP: Acme Corp                          │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                   YOUR PRODUCT OFFERINGS (Columns)                      │
│            ┌─────────┬─────────┬─────────┬─────────┬─────────┐         │
│            │ Core    │ Premium │ Security│ Mobile  │ Analytics│         │
│ BUYING     │ Platform│ Support │ Module  │ App     │ Add-on  │         │
│ CENTERS    ├─────────┼─────────┼─────────┼─────────┼─────────┤         │
│ (Rows)     │         │         │         │         │         │         │
│ ───────────┼─────────┼─────────┼─────────┼─────────┼─────────┤         │
│ Engineering│   ██    │   ██    │   ░░    │   ░░    │   ──    │         │
│ Dept       │  WON    │  WON    │ PIPELINE│ OPPTY   │  N/A    │         │
│            │  $45K   │  $15K   │  $20K   │  $12K   │         │         │
│ ───────────┼─────────┼─────────┼─────────┼─────────┼─────────┤         │
│ Operations │   ░░    │   ──    │   ░░    │   ██    │   ░░    │         │
│ Team       │ OPPTY   │  N/A    │ OPPTY   │  WON    │ OPPTY   │         │
│            │  $35K   │         │  $15K   │  $8K    │  $25K   │         │
│ ───────────┼─────────┼─────────┼─────────┼─────────┼─────────┤         │
│ Sales Div  │   ▓▓    │   ░░    │   ──    │   ░░    │   ██    │         │
│            │  LOST   │ OPPTY   │  N/A    │ PIPELINE│  WON    │         │
│            │ (Rival) │  $12K   │         │  $10K   │  $30K   │         │
│ ───────────┼─────────┼─────────┼─────────┼─────────┼─────────┤         │
│ APAC       │   ░░    │   ░░    │   ░░    │   ░░    │   ░░    │         │
│ Region     │ OPPTY   │ OPPTY   │ OPPTY   │ OPPTY   │ OPPTY   │         │
│            │  $50K   │  $18K   │  $22K   │  $15K   │  $28K   │         │
│            └─────────┴─────────┴─────────┴─────────┴─────────┘         │
│                                                                         │
│ LEGEND:  ██ = Won    ░░ = Whitespace    ▓▓ = Lost    ── = N/A         │
│          Yellow border = Active Pipeline                                │
│                                                                         │
│ SUMMARY:                                                                │
│ Current ARR: $98K (5 cells won)                                        │
│ Pipeline: $42K (3 cells in motion)                                     │
│ Whitespace: $232K (11 cells untapped)                                  │
│ Lost: $45K (1 cell, Sales Div Core Platform)                           │
│ Penetration: 5/20 = 25%                                                │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

**The DemandFarm/ARPEDIO Framework:**

These are popular software tools that operationalize whitespace mapping:

```
┌────────────────────────────────────────────────────────────────────────┐
│               WHITESPACE MAP STATUS CODES                               │
├────────────────┬───────────────────────────────────────────────────────┤
│ Status         │ Meaning & Action                                      │
├────────────────┼───────────────────────────────────────────────────────┤
│ WON (Green)    │ Active customer for this product/buying center combo  │
│                │ Action: Protect, deepen, potential reference          │
├────────────────┼───────────────────────────────────────────────────────┤
│ PIPELINE       │ Active deal in progress                               │
│ (Yellow)       │ Action: Standard deal management, MEDDPICC tracking   │
├────────────────┼───────────────────────────────────────────────────────┤
│ WHITESPACE     │ No activity yet—unexplored opportunity                │
│ (Blue)         │ Action: Prioritize by cell revenue, create outreach   │
├────────────────┼───────────────────────────────────────────────────────┤
│ N/A (Gray)     │ Not applicable—product doesn't fit this buying center │
│                │ Action: None (removes from TAM calculation)           │
├────────────────┼───────────────────────────────────────────────────────┤
│ LOST (Red)     │ Tried and lost—competitor entrenched or rejected      │
│                │ Action: Monitor for displacement triggers             │
└────────────────┴───────────────────────────────────────────────────────┘
```

**Building the Map — Step by Step:**

1. **List Buying Centers (Rows):**
   - Organizational units with budget authority
   - May be: Departments, Divisions, Regions, Sites, Business Units
   - Ask: "Where are the separate decision-makers?"

2. **List Product Offerings (Columns):**
   - Your products, modules, tiers, or service lines
   - Include: Upsells (higher tiers) and cross-sells (different products)
   - Ask: "What else could we sell here?"

3. **Code Each Cell:**
   - Interview the account team
   - Mark current status (Won/Pipeline/Whitespace/N/A/Lost)
   - Note competitor if Lost

4. **Estimate Cell Revenue:**
   - Use comparable deals or pricing models
   - Prioritize cells by potential × probability

5. **Prioritize Whitespace:**
   - Overlay with [[quick-context/sandler-kare-segmentation|KARE]] thinking
   - Which cells align with [[quick-context/miller-heiman-strategic-selling-lamp|LAMP]] account goals?
   - Where do we have champions?

</details>

<details>
<summary><strong>The Key Tension</strong> — Breadth vs. depth of expansion</summary>

Whitespace mapping creates a choice: go wide (many buying centers, few products each) or go deep (few buying centers, full product suite).

| Go Wide | Go Deep |
|---------|---------|
| More stakeholder relationships | Deeper relationships with fewer |
| Diversified risk (losing one BC doesn't kill account) | Higher product lock-in per BC |
| Harder to service many small deployments | Easier to deliver excellence in fewer places |
| Lower switching costs per cell | Higher switching costs (full suite) |
| May trigger enterprise agreement conversation | May miss cross-department synergies |

**The practitioner debate:**

- **"Land wide, then deepen"**: Get a footprint in multiple buying centers first. Each one is a beachhead for expansion. Diversification protects against reorgs and champion departures.
- **"Land deep, then expand"**: Become indispensable to one buying center first. Reference success drives internal expansion. Shallow deployments get ripped out.

**Prioritization Factors:**

| Factor | Go Wide | Go Deep |
|--------|---------|---------|
| Product complexity | Low (easy to deploy anywhere) | High (needs investment to work) |
| Support capacity | High ([[micro-context/can-bus-termination|can]] service many) | Limited (focus required) |
| Champion strength | Strong in multiple BCs | Strong in one BC |
| Competitive threat | High (need to block land-grabs) | Low (time to develop) |
| Account maturity | Early (exploring fit) | Established (expanding success) |

</details>

<details>
<summary><strong>Concrete Example</strong> — Whitespace analysis driving expansion strategy</summary>

**Scenario:** CSM at a construction project management SaaS company analyzing a large civil contractor account.

```
WHITESPACE MAP: Hawkins Construction Group
═══════════════════════════════════════════════════════════════════════════

                    PROJECT    DOCUMENT   SAFETY    EQUIPMENT  BIM
                    MGMT       CONTROL    MODULE    TRACKING   INTEGRATION
                    ─────────  ─────────  ─────────  ─────────  ─────────
Commercial          ██ WON     ██ WON     ░░ OPPTY   ── N/A     ░░ OPPTY
Division            $85K       $25K       $18K                  $35K
(Auckland HQ)

Infrastructure      ░░ OPPTY   ░░ OPPTY   ░░ OPPTY   ██ WON     ░░ OPPTY
Division            $120K      $35K       $22K       $45K       $50K
(Wellington)

Residential         ▓▓ LOST    ░░ OPPTY   ░░ OPPTY   ░░ OPPTY   ── N/A
Division            (Procore)  $15K       $12K       $20K
(Christchurch)

Australia           ░░ OPPTY   ░░ OPPTY   ░░ OPPTY   ░░ OPPTY   ░░ OPPTY
Expansion           $90K       $28K       $20K       $35K       $40K
(Sydney—new)

─────────────────────────────────────────────────────────────────────────
CURRENT: $155K ARR (4 cells)
PIPELINE: $0 (nothing actively working!)
WHITESPACE: $540K (14 cells)
LOST: ~$80K (Residential, Project Mgmt—Procore entrenched)
PENETRATION: 4/18 = 22%
```

**Analysis:**

```
PRIORITY 1: Infrastructure Division — Full Suite
──────────────────────────────────────────────────────────────────────────
Why: Already using Equipment Tracking ($45K). They know us.
Opportunity: $227K across remaining products
Champion: Diane Foster (Operations Manager) loves Equipment module
Risk: Competitor could land Project Mgmt before we do

Action Plan:
• Week 1: Diane intro to their Project Director
• Week 2: Project Mgmt demo tailored to infrastructure workflows
• Week 3: Bundle proposal—Infrastructure Suite at volume discount
• Target: $175K expansion this quarter

PRIORITY 2: Australia Expansion — Land Project Mgmt
──────────────────────────────────────────────────────────────────────────
Why: Greenfield. No competitor entrenched. $213K total potential.
Opportunity: Land with Core ($90K), expand from there
Champion: None yet—need to develop
Risk: They might evaluate independently without HQ influence

Action Plan:
• Week 1: Ask Jennings (our Exec Sponsor) for Sydney intro
• Week 2: Discovery call with AU leadership
• Week 4: Land proposal for Project Mgmt only
• Target: $90K new ARR, creates beachhead for cross-sell

PRIORITY 3: Commercial Division — Cross-Sell Safety + BIM
──────────────────────────────────────────────────────────────────────────
Why: Our strongest relationship. $53K expansion potential.
Opportunity: They already love Project Mgmt + Docs
Champion: Marcus Chen (Commercial Director) is our best reference
Risk: Low priority for them—nice-to-have, not must-have

Action Plan:
• Week 1: Safety module demo during next QBR
• Week 2: BIM integration ROI case study (similar contractor)
• Week 6: Bundle at renewal in Q3
• Target: $53K at renewal

DE-PRIORITIZE: Residential Division
──────────────────────────────────────────────────────────────────────────
Why: Procore entrenched. Lost core product. Only $47K remaining potential.
Status: Mark as RECAPTURE trigger monitoring
Action: Wait for: Procore contract renewal, buyer turnover, or delivery failure
```

**The one thing most outsiders get wrong about this is...** they treat whitespace mapping as a one-time exercise. It's not—the map changes constantly. Buying centers reorganize, new ones form (Australia expansion), products evolve, competitors win or lose cells. Quarterly map refreshes are as important as the initial build.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong> — Related topics to explore</summary>

- **[[quick-context/sandler-kare-segmentation]]** — KARE's EXPAND bucket identifies accounts with whitespace worth pursuing; the whitespace map shows *where* within those accounts
- **[[quick-context/miller-heiman-strategic-selling-lamp]]** — LAMP account planning uses whitespace analysis as a key input to strategy; the Gold Sheet's "Field of Play Opportunities" draws from whitespace
- **[[quick-context/post-sale-account-engagement]]** — Post-sale expansion playbooks are triggered by whitespace analysis
- **[[quick-context/mcdonald-kam-model]]** — Relationship maturity affects which whitespace cells are accessible; Cooperative+ accounts enable cross-BC selling
- **[[quick-context/meddpicc-qualification-framework]]** — Each whitespace cell becoming Pipeline needs MEDDPICC qualification
- **Total Addressable Market (TAM)** — Whitespace map shows account-level TAM; sum across accounts = expansion TAM
- **Land-and-Expand** — The go-to-market strategy that whitespace mapping operationalizes

</details>

<details>
<summary><strong>Test Your Understanding</strong> — 5 progressive questions</summary>

**Q1:** What's the difference between a "Pipeline" cell and a "Whitespace" cell?
<details>
<summary>Answer</summary>
Pipeline means there's an active deal in motion—you've initiated a sales process for that product/buying-center combination. Whitespace means the opportunity exists but no action has been taken yet. Pipeline is yellow (work in progress); Whitespace is blue (unexplored opportunity). See: How It Works.
</details>

**Q2:** Why would a cell be marked "N/A" instead of "Whitespace"?
<details>
<summary>Answer</summary>
N/A means the product doesn't fit that buying center—there's no opportunity there. Example: an "Equipment Tracking" module for a buying center that doesn't use heavy equipment. Marking it N/A removes it from TAM calculations and prevents wasted effort. Not every product fits every buying center.
</details>

**Q3:** An account has 20 whitespace cells but only 1 champion. How should you prioritize?
<details>
<summary>Answer</summary>
Prioritize cells where the champion has influence. If they're in the Engineering department, start with Engineering whitespace even if other cells have higher revenue potential. Champions enable access; without internal support, high-value cells remain theoretical. Expand from strength—use early wins to build credibility for harder cells.
</details>

**Q4:** A cell is marked "Lost to Competitor." Should it be removed from the whitespace map?
<details>
<summary>Answer</summary>
No—keep it visible but coded red. Lost cells [[micro-context/can-bus-transceiver|can]] become RECAPTURE opportunities when triggers occur: competitor contract renewal, delivery failure, buyer turnover, or your product evolving to address the gap. Removing lost cells hides account history and prevents systematic re-engagement when circumstances change.
</details>

**Q5:** How does [[quick-context/mcdonald-kam-model|relationship maturity]] affect whitespace strategy?
<details>
<summary>Answer</summary>
Relationship maturity determines *which* whitespace is accessible. At Basic/Exploratory stages, you're often limited to single buying centers (bow-tie relationship). At Cooperative/Interdependent stages, multi-threading enables cross-BC expansion—your champions [[quick-context/can-bus|can]] introduce you to other divisions. Trying to pursue whitespace in buying centers you can't access wastes resources. Match whitespace prioritization to relationship reach.
</details>

</details>
