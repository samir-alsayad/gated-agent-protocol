# Contributing to GAP

Thank you for your interest in contributing to the **Gated Agent Protocol**!

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/samir-alsayad/gated-agent-protocol.git
cd gated-agent-protocol

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e .

# Run tests
pytest tests/ -v
```

## 📋 Ways to Contribute

### 1. Submit a Protocol
GAP is extensible through **Protocols** — domain-specific workflows.

To contribute a new protocol:
1. Create a folder in `src/gap/protocols/your-protocol/`
2. Add a `manifest.yaml` following the [Protocol Schema](docs/SCHEMA_PROTOCOL.md)
3. Add templates in `templates/`
4. Submit a PR

**Example domains we'd love to see:**
- Research (Hypothesis → Pre-Registration → Experiment → Analysis)
- Legal (Intake → Research → Draft → Review)
- Design (Brief → Wireframe → Mockup → Handoff)

### 2. Improve Documentation
- Fix typos or clarify existing docs
- Add examples to the `examples/` folder
- Improve the [Integration Guide](docs/integration_guide.md)

### 3. Add Tests
We're always looking for better test coverage:
- CLI integration tests
- ACL validation tests
- Edge case handling

### 4. Report Issues
Found a bug? Open an issue with:
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)

## 🧪 Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_manifest.py -v

# With coverage
pytest tests/ --cov=gap --cov-report=html
```

## 📐 Code Style

- Use type hints for all function signatures
- Follow PEP 8
- Keep functions focused and small
- Add docstrings for public APIs

## 🔒 The Golden Rule

Every contribution should respect the core principle:

> **Agents propose. Humans approve. The Ledger remembers.**

If your change weakens this guarantee, it won't be merged.

---

*Built with <3 by the Open Agent Community.*
