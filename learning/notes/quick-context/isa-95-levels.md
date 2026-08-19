---
topic: ISA-95 Levels
created: 2026-01-14
---

> **Related:** [[micro-context/plc-programmable-logic-controller]] | [[quick-context/oee-overall-equipment-effectiveness]] | [[quick-context/plc-vs-software-control]] | [[quick-context/plc-vs-software]] | [[micro-context/can-bus-termination]]

> **TL;DR:** ISA-95 defines a five-level hierarchy that standardizes communication between factory floor systems and business systems, solving the integration chaos between ERPs and manufacturing equipment.

# ISA-95 Levels

## The Core Problem

ISA-95 exists to solve the communication chaos between the factory floor and business systems. Before this standard, every integration between an ERP system (think SAP tracking inventory and orders) and the actual machines making products was a custom, brittle nightmare.

The standard defines a five-level hierarchy: **Level 0** is the physical process itself—chemical reactions, material flow, the actual physics. **Level 1** is sensing and manipulating that process: temperature sensors, motor drives, valves opening and closing. **Level 2** is control and monitoring—your PLCs and DCS systems running logic like "if tank level exceeds 80%, close inlet valve." **Level 3** is Manufacturing Operations Management (MOM/MES)—scheduling which batch runs when, tracking work orders, managing recipes, capturing quality data. **Level 4** is business planning and logistics—your ERP deciding you need to make 10,000 widgets this month based on demand forecasts and available inventory.

A real example: in a brewery, Level 0 is the wort fermenting, Level 1 is the temperature probe and cooling jacket, Level 2 is the [[micro-context/plc-programmable-logic-controller|PLC]] maintaining fermentation at 18C, Level 3 is the MES system scheduling this batch as "IPA Batch 2847" and recording its actual fermentation curve, Level 4 is SAP knowing this batch will fulfill a customer order shipping next Tuesday.

## 5 Essential Terms

| Term | Definition |
|------|------------|
| **MES** | Manufacturing Execution System—the Level 3 software that orchestrates production and captures what actually happened |
| **B2MML** | Business to Manufacturing Markup Language—the XML schema that implements ISA-95's data models for actual system integration |
| **OEE** | Overall Equipment Effectiveness—the holy trinity metric of availability x performance x quality that Level 3 systems exist to calculate |
| **Work Order** | The instruction from Level 4 to Level 3 saying "make this thing" |
| **Genealogy** | The ability to trace every input lot, process parameter, and operator that touched a finished product—critical for recalls and regulated industries |

<details>
<summary><strong>How It Works</strong></summary>

The ISA-95 hierarchy creates clear boundaries for what each system level should handle:

- **Level 0 (Physical Process):** The actual physics—chemical reactions, material transformations, thermal processes
- **Level 1 (Sensing/Manipulation):** Sensors reading the process, actuators affecting it—temperature probes, valves, motor drives
- **Level 2 (Control):** PLCs and DCS systems running real-time logic—"if pressure > 150 PSI, open relief valve"
- **Level 3 (MOM/MES):** Production scheduling, recipe management, quality tracking, work order execution—minutes to days timescale
- **Level 4 (Business/ERP):** Demand planning, inventory management, order fulfillment—days to months timescale

Data flows up (actual production results) and down (production orders), with ISA-95 defining the standard objects and relationships at the Level 3/4 boundary.

</details>

<details>
<summary><strong>The Key Tension</strong></summary>

The central tension practitioners navigate is where to draw the Level 3/Level 4 boundary—and this is where religious wars happen. Purists want a clean separation: ERP should never talk directly to machines, everything flows through MES as an intermediary that handles the translation between "make 10,000 units" (business-speak) and "run recipe R-47 on Line 3 for 6 hours" (operations-speak).

But MES systems are expensive, complex, and often overkill for simpler operations. So you see constant pressure to let ERP reach further down, or to let automation systems reach further up, collapsing the layers. The standard itself is intentionally vague about exactly what lives where because real plants vary wildly—a semiconductor fab and a craft brewery both "manufacture" but have radically different Level 3 needs.

The other perpetual argument is about the data model: ISA-95 defines standard objects like "Material Lot" and "Equipment" with relationships between them, but mapping your actual plant's messy reality onto these pristine abstractions is where implementations die.

</details>

<details>
<summary><strong>Concrete Example</strong></summary>

**Brewery Production Flow:**

- **Level 4 (SAP):** Receives customer order for 500 cases of IPA, checks inventory, determines need to brew, creates production order
- **Level 3 (MES):** Receives work order, schedules "IPA Batch 2847" on Fermenter 3, loads recipe parameters, tracks actual fermentation curve, records quality samples
- **Level 2 ([[quick-context/plc-vs-software|PLC]]):** Executes fermentation control—maintains 18C setpoint, controls cooling jacket, monitors pressure
- **Level 1 (Sensors/Actuators):** Temperature probe reads 18.2C, cooling valve position at 35%, pressure transducer reads 12 PSI
- **Level 0 (Process):** Yeast converting sugars to alcohol, CO2 off-gassing, flavor compounds developing

When the batch completes, data flows back up: actual temperatures, durations, and quality results recorded in MES, production confirmation sent to SAP to update inventory and mark the order ready for fulfillment.

**The one thing most outsiders get wrong about this is...** thinking ISA-95 prescribes specific software products or architectures. It doesn't—it's a vocabulary and conceptual framework. The levels aren't about which vendor's system you buy; they're about creating a shared language so automation engineers, IT architects, and business analysts [[micro-context/can-bus-termination|can]] actually communicate about integration boundaries without talking past each other.

</details>

<details>
<summary><strong>Peripheral Knowledge</strong></summary>

- **[[quick-context/oee-overall-equipment-effectiveness]]** - The key metric that Level 3 MES systems calculate from production data
- **[[quick-context/plc-vs-software-control]]** - Understanding what happens at Level 2 and the tradeoffs in control architectures

</details>

<details>
<summary><strong>Test Your Understanding</strong></summary>

**Q1:** A plant manager wants to connect SAP directly to PLCs to avoid buying MES software. What ISA-95 levels would this bypass, and what problems might arise?
<details>
<summary>Answer</summary>
This bypasses Level 3 (MOM/MES). Problems include: ERP systems operate on different timescales (days) than PLCs (milliseconds), no translation layer between business language ("make 10,000 units") and machine language ("run recipe R-47"), loss of production genealogy and quality tracking, difficulty handling the real-time data volumes PLCs generate, and no place to manage shop floor exceptions that don't belong in ERP.
</details>

**Q2:** Why does ISA-95 intentionally avoid prescribing specific system architectures?
<details>
<summary>Answer</summary>
Because manufacturing contexts vary enormously—a semiconductor fab with thousands of process steps needs different Level 3 capabilities than a craft brewery or a packaging line. The standard provides vocabulary and conceptual frameworks so different stakeholders (automation engineers, IT architects, ERP consultants) [[micro-context/can-bus-transceiver|can]] communicate, not a one-size-fits-all blueprint.
</details>

**Q3:** What's the difference between a "Work Order" and a "Recipe" in ISA-95 terms?
<details>
<summary>Answer</summary>
A Work Order is the instruction from Level 4 to Level 3 saying "make this thing" (what and how much). A Recipe is the Level 3 knowledge of "how to make this thing" (process parameters, steps, equipment settings). The MES combines them: Work Order says "make 1000 units of Product X" and the Recipe says "run at 180C for 45 minutes with ingredient ratios A:B:C."
</details>

**Q4:** What is B2MML and why does it matter for ISA-95 implementations?
<details>
<summary>Answer</summary>
B2MML (Business to Manufacturing Markup Language) is the XML schema that implements ISA-95's abstract data models for actual system integration. While ISA-95 defines concepts like "Material Lot" and "Equipment" and their relationships, B2MML provides the concrete XML structures that ERP and MES systems use to exchange this data. Without B2MML, every integration would require custom data mapping.
</details>

**Q5:** Why is genealogy tracking a critical function of Level 3 systems in regulated industries?
<details>
<summary>Answer</summary>
Genealogy tracks every input lot, process parameter, operator, and equipment that touched a finished product. In regulated industries (pharma, food, medical devices), this enables targeted recalls—if a contaminated ingredient lot is discovered, you [[quick-context/can-bus|can]] trace forward to find exactly which finished products were affected. Without genealogy, you'd have to recall everything produced during a broad time window, costing far more and eroding customer trust.
</details>

</details>
