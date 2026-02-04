---
protocol_id: strategic-planning-v1
variant: strategic-flow
meta:
  pillar: Strategic Alignment
  philosophy: Intent-Driven Operations
  prefixes:
    objective: "OBJ-"
    guardrail: "GRD-STRAT-"
    step: "STEP-"

roles:
  - id: strategist
    capability: "Thinking/Strategic Abstraction"
    focus: ["OKRs", "Market/Resource Analysis", "KPI Definition"]
  - id: critic
    capability: "Verification/Risk Audit"
    focus: ["Operational Guardrails", "Conflict Detection", "Constraint Analysis"]
  - id: craft
    capability: "Action/Roadmap Synthesis"
    focus: ["Milestone Sequencing", "Resource Allocation", "Traceability Mapping"]

gates:
  - id: gate_objectives
    pillar: objectives.md
    responsible_roles: [strategist, critic]
    logic:
      ears_enforcement: true
      mandatory_sections:
        - Introduction
        - Strategic Objectives (OKRs):
            grammar: "EARS Syntax (UNLESS..THE SHALL / IF..THE SHALL)"
        - Target Metrics (KPIs)
    verification_rule: "Every objective MUST be defined with a non-ambiguous EARS condition and a measurable KPI."

  - id: gate_operational_guardrails
    pillar: guardrails.md
    depends_on: gate_objectives
    responsible_roles: [critic, strategist]
    logic:
      risk_verification: true
      mandatory_sections:
        - Operational Guardrails:
            definition: "Constraints on Resource/Risk"
        - Conflict Matrix:
            definition: "Handling of competing objectives"
    verification_rule: "Every Guardrail MUST bound a specific strategic risk identified in the objectives."

  - id: gate_roadmap
    pillar: roadmap.md
    depends_on: gate_operational_guardrails
    responsible_roles: [craft, critic]
    logic:
      traceable_sequencing: true
      mandatory_sections:
        - Overview
        - Milestone Sequence:
            metadata: ["Objective ID", "Guardrail ID"]
            formatting: "Traceability Footer Required"
    verification_rule: "The roadmap MUST account for 100% of defined Strategic Objectives."

final_execution:
  responsible_role: craft
  objective: "Synthesize the final Strategic Roadmap and Operational Brief."
  output_format: "Strategic Roadmap (.md)"
---
# Protocol: Strategic Planning (Strategic-Flow)

This protocol governs the `meta` domain's strategic operations. It defends the pillar of **Strategic Alignment** by ensuring that high-level objectives are quantifiable and traceably linked to operational milestones.

## 1. The Operational Philosophy: Intent-Driven Operations
In strategic planning, the biggest risk is "Vague Ambition". This protocol prevents this by enforcing EARS-style OKRs—ensuring that every dream is grounded in a measurable, conditional reality.

## 2. Rule 1: No Implementation During Planning
**You MUST NOT start executing projects while in the Strategic Planning phases.**
The focus is on defining the *What* and the *Bound*, not the *How*.

## 3. The Operational Gates

### Gate I: Objective Registration (`objectives.md`)
- **Action**: Define strategic OKRs using EARS syntax.
- **Mandatory**: Every objective must be paired with a measurable KPI.

### Gate II: Risk Guardrails (`guardrails.md`)
- **Action**: Identify the operational constraints that bound the strategic intent.
- **Mandatory**: Identification of conflicts between objectives (e.g., "Speed vs. Quality").

### Gate III: Milestone Sequencing (`roadmap.md`)
- **Action**: Break the objectives into a traceable timeline of milestones.
- **Traceability**: Every milestone MUST link back to an Objective or Guardrail.

## 4. Metadata Standard
- **ID Prefixes**: `OBJ-` (Objective), `GRD-STRAT-` (Guardrail), `STEP-` (Milestone).
- **Format**: `_Objectives: [ID], Guardrails: [ID]_` footer for every milestone.

---
*Governed by the Bureau of Standards - 2026*
