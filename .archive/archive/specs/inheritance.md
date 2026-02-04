# GAP Technical Spec: Domain Inheritance

This credential defines the resolution logic for `manifest.yaml` files that utilize the `extends` key.

## 1. The Inheritance Chain
A manifest can extend exactly **one** parent manifest.
- **Child**: The specific Project Domain (e.g., `sovereign/school-of-first-principles`). It anchors abstract logic to concrete disk paths and identities.
- **Parent**: The abstract Core Domain (e.g., `core/instructional`). It defines the workflow methodology and capability requirements.

## 2. Separation of Concerns (Taxonomy)
- **Core (Parent)**: Defines **HOW** (Process). MUST NOT contain specific paths.
- **Sovereign (Child)**: Defines **WHERE** (Paths) and **WHO** (Personas). MUST inherit Process.

## 3. Merge Logic (The "Nitty Gritty")
When resolving a Child manifest, the `gap` CLI applies the following rules:

### A. Meta & Invariants (Union)
The `meta` block is merged. Invariants (`guards`) are **Additive**.
- Parent: `[Determinism]`
- Child: `[Reflective Locking]`
- **Result**: `[Determinism, Reflective Locking]`

### B. Roles (Patch & Add)
Roles are matched by `id`.
- If Child defines a Role `id` that exists in Parent -> **Child Patches Parent**.
- If Child defines a Role `id` not in Parent -> **Child Adds Role**.

### C. Permissions (Replacement)
**CRITICAL**: `permissions` blocks are **NOT merged**. They are **REPLACED**.
- **Reasoning**: Security. A Child domain acts in a specific context (disk path). Unintentionally inheriting Parent paths (which might be generic wildcards) creates leakage.
- **Rule**: If a Child Gate defines `permissions`, it **completely overwrites** the Parent Gate's permissions.

### D. Gates (Patch by ID)
Gates are matched by `id`.
- **Logic**:
    - `verification_rule`: Child **Overwrites** Parent.
    - `mandatory_sections`: Child **Appends** to Parent.
    - `permissions`: Child **Overwrites** Parent (as per Rule C).

## 3. Example: The School

### Parent (`core/instructional`)
```yaml
gates:
  - id: gate_draft
    permissions:
      write: [${WORKSPACE}/drafts/*.md]
    mandatory_sections:
      - Concept
```

### Child (`sovereign/school`)
```yaml
extends: core/instructional
gates:
  - id: gate_draft
    permissions:
      write: [/Users/Shared/Projects/school/curriculum/**/*.md] # <--- REPLACES PARENT
    mandatory_sections:
      - Reflection # <--- APPENDS TO PARENT
```

### Resolved Manifest
```yaml
gates:
  - id: gate_draft
    permissions:
      write: [/Users/Shared/Projects/school/curriculum/**/*.md]
    mandatory_sections:
      - Concept
      - Reflection
```
