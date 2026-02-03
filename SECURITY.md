# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in GAP, please report it responsibly:

1. **Email**: samir.alsayad@gmail.com
2. **Subject**: `[SECURITY] GAP Vulnerability Report`

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 7 days
- **Fix/Patch**: Depends on severity

## Scope

This policy covers:
- The GAP CLI (`gap` command)
- The core Python package (`gap/`)
- The security module (`gated_agent/`)

## Out of Scope

- Third-party dependencies (report to their maintainers)
- User-defined protocols and manifests

## Security Model

GAP's security model is based on:
- **Access Control Lists (ACLs)** embedded in approved artifacts
- **Immutable ledger** tracking all approvals
- **Gate enforcement** preventing unauthorized state transitions

GAP does **not** provide:
- Model-level AI safety (prompt injection prevention)
- Network security
- Encryption at rest

For details, see [docs/acl-specification.md](docs/acl-specification.md).
