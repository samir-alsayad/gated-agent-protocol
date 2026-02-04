# GAP Integration Guide: Building a Protocol-Aware Tool

**Target Audience:** IDE Developers (OpenCode, Cursor), Agent Framework Builders (LangChain, AutoGen).

---

## 1. The Practical Flow

“Supporting GAP” means your tool stops being a passive executor and becomes a **Protocol Enforcer**.

### Step A: Detection (The "Is this a GAP Project?" Check)
When your tool opens a folder, it must check for `.gap/gap.yaml`.

**The Session Registry:**
Instead of a single global mode, the tool manages **Sessions**.
- Reads `.gap/gap.yaml` -> `active_session`.
- Loads session state from `.gap/sessions/[active_session]/`.

---

### Step B: Resolution (Law + Declared Exceptions)

The Tool MUST construct the **Effective Policy** by applying **explicit, declared Session exceptions** to immutable Project Law.

**Sources of Truth (in order):**
1.  **Project Manifest (`.gap/manifest.yaml`)**:
    - Canonical, versioned, immutable defaults.
    - Represents the **Law of the Repository**.
2.  **Session Configuration (`.gap/sessions/[id]/config.yaml` OR CLI flags)**:
    - Explicit, temporary **Exception Declarations**.
    - Must be named and scoped to the active session.
3.  **Ledger (Execution Log)**:
    - Records the resolution outcome.
    - Preserves traceability (“what changed and why”).

**Invariant:**
> **Session configuration MUST NOT silently override Project Law.**
> **All deviations MUST be explicit, scoped, and recorded in the Ledger.**

```python
def load_context(root_path):
    # 1. Load Project Law (Immutable)
    with open(os.path.join(root_path, ".gap/manifest.yaml")) as f:
        project_manifest = yaml.safe_load(f)

    # 2. Load Active Session (Declared Exceptions)
    with open(os.path.join(root_path, ".gap/gap.yaml")) as f:
        global_config = yaml.safe_load(f)
        session_id = global_config['active_session']

    session_config = load_session_config(session_id)

    # 3. Apply Declared Exceptions (NOT silent overrides)
    effective_policy = apply_exceptions(
        base_policy=project_manifest['execution'],
        exceptions=session_config.get('execution_exceptions', {}),
        ledger=execution_ledger,
        session_id=session_id
    )

    return effective_policy
```

---

### Step C: The Enforcement Loop (The "Main Loop")
The Harness enforces the **Decision Chain of Custody**.

**The GAP State Machine:**
1.  **Phase 1: Requirements**
    - Gate: `true` (Manual / Supervisor).
2.  **Phase 2: Design**
    - Gate: `true` (Manual / Supervisor).
3.  **Phase 3: Execution Policy**
    - Gate: `true` (Manual / Supervisor).
    - Defines: Execution mode, Task granularity, Checkpoint strategy.
4.  **Phase 4: Tasks**
    - Gate: `true` (Manual / Supervisor).
    - Tasks are decomposed **in accordance with the Execution Policy**.
    - **ACLs are derived here**, from approved Tasks.
5.  **Phase 5: Execution**
    - Gates: **Execution Gates (Checkpoints)**.
    - Enforced strictly by the Harness.

**Note on "True" Gates:**
> A `true` gate means **explicit approval is required**.
> The approver MAY be a Human User or a designated Supervisor Agent.
> GAP is agnostic to *who* approves, but **not** to *whether* approval occurs.

---

### Session-Based Exception Declarations (Mission Control)
These allow a user to temporarily deviate from Project Law for a specific mission **without mutating the Manifest**.

**Examples:**
- “Tonight, run autonomous.” -> Exception: `execution.mode = autonomous`
- “Strict audit mode.” -> Exception: `checkpoints.strategy = every`

**Mandatory Logging Rule:**
> **Every Session Exception MUST produce a Ledger entry recording:**
> - Project default
> - Declared exception
> - Effective policy
> - Session ID
> - Approving authority

---

### Pseudo-Code Logic
```python
def run_protocol(project):
    # 1. Authority Check
    if not project.has_approved("design"):
        halt("Must approve Design first")

    # 2. Resolve Effective Policy (Law + Exceptions)
    policy = project.effective_execution_policy()

    # 3. Execution Loop (Task-Bound, Deterministic)
    for task in project.tasks:
        # A. Checkpoint Transition
        if policy.requires_checkpoint_after(task.id):
            pause_for_approval("Execution checkpoint reached")

        # B. ACL Enforcement (Derived from Task)
        acl = extract_acl(task)
        sandbox.apply_rules(acl)

        # C. Execute (via Harness)
        agent.execute(task)
        
        # D. Completion Declaration
        project.record_task_completion(task.id)
```

## 2. What this feels like to the User
1.  **Safety**: They see the IDE say *"Agent Restricted: Planning Mode"*.
2.  **Trust**: They see the Agent ask *"I need write access to `src/main.py`. Approve?"*
3.  **Control**: They know the Agent *cannot* touch `database.db` because it wasn't in the plan.
4.  **Flexibility**: *"Execution is autonomous for this session only."*

## 3. The Harness Responsibility
Your tool acts as the **Harness**. You are the "Container" that holds the "Contextual Drift" in check.
The Harness is dumb, explicit, and unforgiving.
