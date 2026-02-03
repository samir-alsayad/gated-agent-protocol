# Standard: PostgreSQL Backend Ledger

## 1. Objective
To provide an **Immutable Ledger** for all Decision Records and Execution States in a GAP Project.

## 2. Schema
The GAP Ledger is a relational schema that mirrors the `manifest.yaml` structure.

```sql
CREATE TABLE decision_records (
    id UUID PRIMARY KEY,
    project_id TEXT,
    phase TEXT CHECK (phase IN ('requirements', 'design', 'policy', 'task')),
    status TEXT CHECK (status IN ('draft', 'proposed', 'approved')),
    content_hash TEXT,
    approver_id TEXT,
    approved_at TIMESTAMP
);

CREATE TABLE execution_log (
    id UUID PRIMARY KEY,
    task_id UUID REFERENCES decision_records(id),
    checkpoint_id TEXT,
    acl_fingerprint TEXT,
    output_hash TEXT,
    verified BOOLEAN DEFAULT FALSE
);
```

## 3. Integration Logic
1.  **Scribe**: When an Artifact is scribed, a `draft` record is inserted.
2.  **Gate**: When a Gate is passed (`gate: true`), the record is updated to `approved`.
3.  **Harness**: The Harness checks `approver_id` before allowing downstream execution.
