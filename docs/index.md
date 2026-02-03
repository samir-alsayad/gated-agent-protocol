# Gated Agent Protocol (GAP)

**The Sovereign Standard for Human-AI Collaboration.**

GAP is a protocol engine that enforces **Structure**, **Security**, and **Traceability** in agentic workflows. It prevents AI from hallucinating requirements or skipping safety checks by strictly enforcing a "State Machine of Work".

## 📚 Documentation Structure

### Core Concepts (Immutable)
*   **[Board of Decisions](DECISIONS.md)**: The Constitution.
*   **[Logic](LOGIC.md)**: The Rules of State.
*   **[Taxonomy](taxonomy.md)**: The Language.
*   **[Protocol Schema](SCHEMA_PROTOCOL.md)**: The "DNA" & Traceability Standard.
*   **[Project Schema](SCHEMA_PROJECT.md)**: The "Law" (Manifest).
*   **[Session Schema](SCHEMA_SESSION.md)**: The "Exception" (Tool Config).
*   **[Access Control](acl-specification.md)**: The Plan-Derived Security Model.

### Guides
*   **[Integration Guide](integration_guide.md)**: How to add GAP to your project.
*   **[Postgres Backend](postgres_spec.md)**: Setting up the SQL Ledger.

### API Reference
*   **[CLI](cli.md)**: `gap check`, `gap scribe`, `gap gate`, `gap migrate`.

## 🚀 Getting Started

```bash
pip install git+https://github.com/samir-alsayad/gated-agent-protocol.git
gap --help
```
