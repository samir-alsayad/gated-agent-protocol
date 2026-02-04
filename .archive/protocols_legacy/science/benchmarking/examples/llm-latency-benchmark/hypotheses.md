# Hypotheses: LLM Latency Benchmark

## Research Questions
What is the true latency distribution of various LLM providers under controlled conditions?

## Null Hypotheses

### HYP-01: Provider Variance
- **Claim**: WHEN comparing providers A, B, and C, THE p50 latency differences SHALL be statistically significant.
- **Null**: No significant difference exists between providers (p > 0.05).
- **Predicted Effect Size**: >100ms difference in p50.

### HYP-02: Token Scaling
- **Claim**: IF output token count doubles, THEN THE latency SHALL increase sublinearly (< 2x).
- **Null**: Latency scales linearly or superlinearly with token count.
