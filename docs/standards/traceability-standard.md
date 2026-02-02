# Standard: Traceability and Justification

This standard defines the metadata required to bridge the gap between human intent and agentic work across all domains in the Protocol Library.

## 1. Domain Sovereignty in Identification
Each Protocol is responsible for defining its own identification prefixes to match the natural language of its domain.

**Common Examples:**
- **Intent**: `REQ-` (Systems), `HYP-` (Science), `OBJ-` (Strategy).
- **Invariant**: `PROP-` (Code), `INV-` (Data), `GRD-` (Operational).
- **Execution**: `TASK-` (Action), `STEP-` (Protocol), `ACT-` (Activity).

## 2. The Traceability Footer
Regardless of naming conventions, every actionable item in an execution document MUST be accompanied by a traceability footer. This footer serves as the **Justification** for why an agent is performing an action.

**Mandatory Format:**
- `[ ] Action Description`
    - `_Intent: [ID1], [ID2]_`
    - `_Invariant: [ID3], [ID4]_`

## 3. Evidence and Proof
When an agent completes an execution item, it must provide evidence that the related **Invariants** have been verified. 
- In **Software**, this is often passing Property-Based Tests.
- In **Science**, this is often a statistical significance report.

## 4. Integrity Constraints
Audit tools SHALL flag the following as violations of the library's rigor:
- **Orphan Actions**: Actions with no traceability footer.
- **Untracked Intents**: Intent items that are never addressed by an action.
- **Fringe Work**: Code or analysis that exists outside the scope of a ratified intent.

---
*Governed by GAP - 2026*
