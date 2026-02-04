# Invariants: Prompt Caching Study

## Overview
This document defines the analytical invariants and execution protocol for the prompt caching study.

## Analytical Invariants

### INV-01: Latency Measurement
- **Bound**: Latency measurements SHALL be taken at the application layer, excluding network RTT.
- **Precision**: Measurements SHALL use monotonic clocks with microsecond resolution.

### INV-02: Quality Scoring
- **Bound**: BLEU scores SHALL be computed against fresh responses generated with identical parameters.
- **Validation**: A minimum of 100 paired samples required for statistical significance.

## Success Criteria
- **p-value threshold**: p < 0.01 for latency claims
- **Confidence interval**: 95% CI for BLEU score comparison
- **Error margin**: ±5% for latency measurements

## Data Sanitization
- Exclude cold-start requests (first 10 per session)
- Remove outliers beyond 3σ from mean latency

## Execution Protocol

- [ ] **STEP-01**: Set up test harness with cache enabled/disabled toggle. — *Trace: HYP-01, INV-01*
- [ ] **STEP-02**: Generate 500 semantically similar prompt pairs. — *Trace: HYP-01*
- [ ] **STEP-03**: Run baseline (no cache) to establish control latencies. — *Trace: HYP-01, INV-01*
- [ ] **STEP-04**: Run experiment (cache enabled) with same prompts. — *Trace: HYP-01*
- [ ] **STEP-05**: Compute BLEU scores for all cached responses. — *Trace: HYP-02, INV-02*
- [ ] **STEP-06**: Perform statistical analysis (t-test for latency, equivalence test for BLEU). — *Trace: HYP-01, HYP-02*

## Access Control
```yaml
allow_write:
  - "results/experiment_log.csv"
  - "results/analysis_report.md"
  - "data/processed/**"
allow_exec:
  - "python scripts/run_experiment.py"
  - "python scripts/analyze.py"
```

---
*Trace: HYP-01, INV-01, INV-02*
