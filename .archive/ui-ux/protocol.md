---
protocol_id: software-ui-ux-v1
variant: aesthetic-flow
meta:
  pillar: Visual Excellence
  philosophy: User-Centric Synthesis
  prefixes:
    intent: "USER-REQ-"
    guardrail: "UI-PROP-"
    step: "DESIGN-STEP-"

roles:
  - id: scout
    capability: "Thinking/Persona Analysis"
    focus: ["User Journeys", "Accessibility Standards", "Vibe/Aesthetic Direction"]
  - id: architect
    capability: "System Design/Layout"
    focus: ["Wireframing", "Component Hierarchy", "Color/Typography Theory"]
  - id: craft
    capability: "Implementation/Synthesis"
    focus: ["CSS/HTML Synthesis", "Micro-animations", "Responsiveness"]

gates:
  - id: gate_intent
    pillar: user_research.md
    responsible_roles: [scout, architect]
    logic:
      persona_driven: true
      mandatory_sections:
        - Introduction
        - User Personas
        - User Stories:
            grammar: "EARS Syntax"
        - Success Criteria:
            focus: ["Universal Access", "Performance"]
    verification_rule: "Every user story MUST be paired with a specific persona and success metric."

  - id: gate_aesthetic_bounds
    pillar: design_system.md
    depends_on: gate_intent
    responsible_roles: [architect, scout]
    logic:
      token_enforcement: true
      mandatory_sections:
        - Overview
        - Visual Tokens:
            subsections: ["Color Palette", "Typography", "Spacing"]
        - Component Blueprints:
            format: "Mermaid Blueprint"
        - Correctness Properties:
            definition: "Aesthetic Invariants (e.g., 'Contrast shall always be >= 4.5:1')"
    verification_rule: "Design System MUST define concrete tokens for all UI elements."

  - id: gate_interaction_path
    pillar: tasks.md
    depends_on: gate_aesthetic_bounds
    responsible_roles: [craft, architect]
    logic:
      traceable_interactivity: true
      mandatory_sections:
        - Overview
        - Interactive Steps:
            metadata: ["User Req ID", "UI Property ID"]
            formatting: "Traceability Footer Required"
    verification_rule: "The task list MUST account for 100% of defined Accessibility Properties."

final_execution:
  responsible_role: craft
  objective: "Synthesize high-fidelity UI that satisfies all Aesthetic Invariants."
  output_format: "Frontend Code (HTML/CSS/JS)"
---
# Protocol: UI-UX Design (Aesthetic-Flow)

This protocol governs the design and implementation of high-fidelity user interfaces. It defends the pillar of **Visual Excellence** by ensuring that design is never "ad-hoc" but is derived from a rigorous mapping of user persona and design tokens.

## 1. The Operational Philosophy: User-Centric Synthesis
In UI design, the biggest risk is "Interface Bloat" or "Accessibility Debt." This protocol prevents this by enforcing a formal "token-first" design architecture.

## 2. The Operational Gates

### Gate I: Persona Alignment (`user_research.md`)
- **Action**: Define the human users and their critical journeys using EARS syntax.
- **Mandatory**: Identification of personas and success metrics.

### Gate II: Token Lockdown (`design_system.md`)
- **Action**: Define the color palette, typography, and component blueprints.
- **Mandatory**: Define **Aesthetic Invariants** (e.g., contrast ratios, responsive break-points).

### Gate III: Interaction Mapping (`tasks.md`)
- **Action**: Break the high-fidelity design into atomic implementation steps.
- **Traceability**: Every task MUST link back to a User Requirement and a UI Property.

---
*Governed by the Bureau of Standards - 2026*
