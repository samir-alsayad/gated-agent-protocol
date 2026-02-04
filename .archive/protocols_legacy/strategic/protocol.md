# Strategic Protocol: The Art of the Pivot

## Objective
To ensure that the high-level goals of the **School of First Principles** (Roadmaps and Campaign READMEs) are modified only with explicit human intent and technical justification.

## The Roles
- **Strategist (The Optimizer)**: Analyzes the current progress and proposes a shift in direction.
- **Human Steward (The User)**: The final authority who signs off on the strategic change.

## The Workflow
### 1. Identify the Need
A strategic pivot is usually triggered by a **Diagnosis** (Analytical Mode). 
Example: "The Council is struggling with Inference; we need to pivot Campaign 10 from 'Selection' to 'Optimization'."

### 2. Draft the Proposal
The Strategist writes a `pivot_proposal.md`. 
- **Requirement**: Must list every file that will be impacted by the change.
- **Requirement**: Must define the "Cascade Audit" parameters.

### 3. Human Approval (The Master Gate)
The User reviews the proposal.
- **Action**: Use the `/sign` command (or manual edit) to authorize the change.
- **Constraint**: No agent can touch `roadmap.md` or `README.md` without this signature.

### 4. Direct Update
Once signed, the files are updated. This triggers a follow-up **Cascade Audit** in the `analytical` domain to ensure all sub-atoms are still aligned.
