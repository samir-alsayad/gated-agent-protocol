# Protocol: Empirical Research (Empirical-Flow)

This protocol governs the `science` domain (Experimental Research, Data Analysis, and Technical Evaluation). It defends **Reproducibility** by enforcing "Pre-Registration" of intent.

## Philosophy: Pre-Registration
In this domain, the biggest risk is "p-hacking" or post-hoc rationalization. This protocol prevents this by gating the research lifecycle—ensuring that the method is locked before the first data point is collected.

## Rule: No Exploration During Registration
**You MUST NOT access the raw dataset or run benchmarks while in the Pre-Registration phases.**
The only exception is running diagnostic commands to verify environment readiness.

## Operational Gates

| Gate | Artifact | Verification Rule |
|:-----|:---------|:------------------|
| `gate_pre_registration` | `hypotheses.md` | Every hypothesis MUST be falsifiable and defined with measurable EARS logic. |
| `gate_invariant` | `invariants.md` | Analytical Invariants MUST be locked before data collection begins. |
| `gate_synthesis` | `report.md` | Research report MUST be reproducible and address all pre-registered hypotheses. |

### Gate I: Hypothesis Registration (`hypotheses.md`)
- **Action**: Define falsifiable hypotheses using EARS syntax.
- **Sections**: Introduction, Hypotheses, Variables.
- **Mandatory**: Every claim must be measurable with predicted outcomes.

### Gate II: Analytical Locking (`invariants.md`)
- **Action**: Define the statistical bounds, invariants, and execution protocol.
- **Sections**: Overview, Analytical Invariants, Success Criteria, Data Sanitization, Execution Protocol.
- **ACL**: Embedded Access Control block defines allowed writes/execs.
- **Mandatory**: Lockdown of p-value thresholds or confidence intervals.

### Gate III: Synthesis (`report.md`)
- **Action**: Execute the protocol and produce the research report.
- **Sections**: Introduction, Statistical Results, Falsification Check, Conclusion.
- **Mandatory**: Report must address all pre-registered hypotheses.

## Metadata Standard
- **ID Prefixes**: `HYP-` (Hypothesis), `INV-` (Invariant), `STEP-` (Execution Step).
- **Format**: `_Trace: HYP-01, INV-01_` footer for every step.

---
*Governed by GAP - 2026*
