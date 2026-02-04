# Data Audit: LLM Latency Benchmark

## Raw Data Integrity
- All measurements timestamped with NTP-synchronized clock
- Data stored in append-only Parquet format with SHA-256 checksums
- Each run tagged with hardware/software configuration snapshot

## Outlier Removal Protocol
1. Remove requests with HTTP errors (non-2xx status)
2. Remove requests during first 60 seconds (warm-up period)
3. Flag measurements beyond 3σ from rolling mean (manual review required)
4. Document all removals with justification

## Data Completeness
- Minimum 1000 successful requests per provider per token bucket
- Run duration: minimum 1 hour continuous operation

## Access Control
```yaml
allow_write:
  - "data/audit_log.md"
allow_exec:
  - "shasum -c checksums.sha256"
  - "du -rh data/"
```

---
*Trace: MET-01, MET-02*
