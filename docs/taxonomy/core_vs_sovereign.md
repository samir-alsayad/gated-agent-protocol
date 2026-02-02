# Taxonomy: Core vs. Sovereign Responsibilities

This document defines the strict **Separation of Concerns** between Parent (Core) and Child (Sovereign) domains in the GAP inheritance model.

## 1. Core Domain (The "HOW")
**Scope**: Abstract capability and methodology. It defines *how* work is done, regardless of *where* it happens.
- **Defines**:
    - **Methodology**: "We draft, then we review." (The Gate Sequence).
    - **Roles (Abstract)**: "Author", "Reviewer" (Capabilities, not Personas).
    - **Invariants (Universal)**: "No broken links", "No placeholder text."
    - **Grammar**: The required headers in markdown files (e.g., EARS syntax).
- **Does NOT Define**:
    - **Paths**: Never hardcodes specific disk locations.
    - **Personas**: Does not know about "The Librarian" or "The Smith."
    - **Project Logic**: Does not know about "Atoms" or "Campaigns."

## 2. Sovereign Domain (The "WHERE" & "WHO")
**Scope**: Concrete context and identity. It defines *where* work happens and *who* does it.
- **Defines**:
    - **Context (Paths)**: The specific `/Users/Shared/Projects/...` directories.
    - **Identity (Personas)**: Maps "Author" -> "The Smith", "Reviewer" -> "The Critic."
    - **Project Logic**: "Atoms", "Foundry", "The Cast."
    - **Invariants (Contextual)**: "Reflective Locking", "Zero-Execution."
- **Does NOT Define**:
    - **Methodology**: Should inherit the workflow from Core.

## 3. The Litmus Test
If you are asking **"How do I write a good spec?"** -> Look at **Core**.
If you are asking **"Where do I save this file?"** -> Look at **Sovereign**.
