# GAP Core Modules Audit

This document explains what every file in `src/gap/core/` does in plain English.
We want to figure out if these files are actually useful, or if they are "Agentic Hallucinations" (over-engineering that we should delete to keep the protocol pure and simple).

Please read through these sections.
If you think a file is over-engineered or not needed for our "simple ledger" philosophy, mark it for **DELETE**. If it's useful, mark it for **KEEP**. You can just edit this file directly and tell me when you are done.

---

## 1. `manifest.py`
**What it does:** Reads your `manifest.yaml` file (e.g. `software-engineering.yaml`) and loads it into memory. It figures out what the steps are (Requirements -> Design -> Tasks -> Plan -> Implementation) and which ones require a human gate.
**Why it exists:** Without this, the CLI wouldn't know what workflow you are trying to follow.
**Verdict:** [ ] KEEP / [ ] DELETE

## 2. `ledger.py`
**What it does:** Reads and writes the `.gap/status.yaml` file. When you type `gap gate approve`, this is the file that actually writes `status: complete` to the ledger.
**Why it exists:** It is the "database" logic for the protocol. It remembers where you are in the project.
**Verdict:** [ ] KEEP / [ ] DELETE

## 3. `state.py`
**What it does:** A tiny file that just lists the 5 possible states a step can be in: `locked`, `unlocked`, `pending`, `complete`, or `invalid`.
**Why it exists:** It makes sure the code doesn't misspell "complete" as "completed" by standardizing the names.
**Verdict:** [ ] KEEP / [ ] DELETE

## 4. `models.py`
**What it does:** Defines the structure of the new Task and Plan rules we just made. It says "A task must have an ID" and "A plan must have an ACL and a Cognition strategy".
**Why it exists:** So that when reading `.gap/plan.yaml`, python can verify all the correct fields are actually there.
**Verdict:** [ ] KEEP / [ ] DELETE

## 5. `scope_manifest.py` (Formerly `security.py`)
**What it does:** Reads the `.gap/plan.yaml` file and extracts just the `acl` block (the allowed filesystem and shell commands).
**Why it exists:** Originally built to enforce security, we renamed/neutered it. Now it just grabs the rules so that `gap check` or the Runner can read them.
**Verdict:** [ ] KEEP / [ ] DELETE

---

## The Suspicious Files (Potential Hallucinations)

These files might be over-engineering. Read carefully:

### 6. `auditor.py`
**What it does:** The "Traceability Auditor". It opens your markdown and YAML files, uses regex to hunt for things like `R-01` (Requirements IDs) and `D-01` (Design IDs), and then crosses-checks them to make sure every task connects to a design, and every design connects to a requirement.
**The Problem:** It is incredibly fragile. If the AI formats a markdown file slightly wrong, or forgets the exact regex string `(Traces to: R-01)`, the auditor throws massive errors and blocks the project.
**Verdict:** [ ] KEEP / [ ] DELETE

### 7. `validator.py`
**What it does:** Looks at `manifest.yaml` and runs a complex algorithm ("Topological Sort") to make sure you didn't accidentally create an infinite loop (e.g. Step A needs Step B, but Step B needs Step A).
**The Problem:** The manifests are extremely simple, static 6-step YAML files written by us, not dynamically generated code. We are never going to accidentally write an infinite loop in a hardcoded 20-line YAML file. This is classic computer-science over-engineering.
**Verdict:** [ ] KEEP / [ ] DELETE

### 8. `path.py`
**What it does:** A complex "Path Resolution Manager" that tries to figure out where template files (like `requirements.md`) live by doing 4 layers of fallback logic and checking arbitrary magic folders.
**The Problem:** `manifest.yaml` already has a `templates:` section at the bottom that explicitly states the exact path to the file. We don't need a massive fallback engine to find a file path.
**Verdict:** [ ] KEEP / [ ] DELETE

### 9. `factory.py`
**What it does:** A file with exactly one function: `return YamlLedger()`.
**The Problem:** Originally, this is where it decided between using the `YamlLedger` or the heavy `SQLAlchemy` database ledger. Since we deleted the SQL database because GAP is just a simple YAML ledger, this file is now just a useless middleman. We can just use `YamlLedger()` directly.
**Verdict:** [ ] KEEP / [ ] DELETE
