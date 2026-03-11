# Execution Policy: {{ project_name }}

## 1. Governance Overview
This document defines the **Authority** (Venue and Model Selection) and **Gates** (Checkpoints) for the implementation phases defined in [.gap/tasks.md](file://./tasks.md).

## 2. Resource Assignment (Authority)
Define the execution venue (Cloud Provider vs Local Inference) and authorized models for each phase inherited from the approved task list.

| Task Phase | Locality (Provider/Local) | Cognition (Model ID) |
| :--- | :--- | :--- |
| **Phase 1: Setup** | {{ setup_locality }} | {{ setup_model }} |
| **Phase 2: Foundation** | {{ foundation_locality }} | {{ foundation_model }} |
| **Phase 3: Implementation** | {{ implementation_locality }} | {{ implementation_model }} |

## 3. Global Policy Overrides
*   **Max Budget**: {{ total_budget }}
*   **Safety Level**: {{ safety_tier }} (e.g., Strict, Permissive)
*   **Model Tier**: {{ model_tier }} (e.g., Performance, Efficiency)

---
**Protocol Note:** This document ensures the agent stays within the approved venue and model tier for each specific phase of the project, as defined in the approved `tasks.md`.
