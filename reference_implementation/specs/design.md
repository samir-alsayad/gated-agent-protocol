# Design: GAP Native Implementation

## 1. System Architecture
The system replaces the legacy Python TUI (`ui/menu.py`) with a lightweight **Bootstrap -> Driver** architecture.

```mermaid
graph TD
    User[User] -->|Run| Bootstrap[Bootstrap Script (gap-gptme)]
    Bootstrap -->|Launch| Env[Environment Setup]
    Env -->|Execute| Gptme[gptme Driver]
    Gptme -->|Load| SysPrompt[System Prompt (gap_system_prompt.md)]
    Gptme <-->|Interact| User
    Gptme -->|Read/Write| Specs[./specs/*.md]
    Gptme -->|Form Tool| Policy[Policy Decision]
```

## 2. Component Design

### 2.1 The Bootstrap Script (`gap-gptme`)
*   **Path**: `/Users/Shared/Projects/Gated Agent Protocol/reference_implementation/gap-gptme`
*   **Language**: Bash (Shebang: `#!/bin/bash`)
*   **Execution Logic**:
    1.  **Resolve Paths**:
        *   `SCRIPT_DIR`: Directory of the script itself.
        *   `GPTME_BIN`: `$SCRIPT_DIR/.venv_reference/bin/gptme`
        *   `SYSTEM_PROMPT_FILE`: `$SCRIPT_DIR/gap_system_prompt.md`
    2.  **Environment Handover**:
        *   Export `OPENROUTER_API_KEY` from `$OPENROUTER_KEY` if not set.
        *   Fail fast if API key is missing.
    3.  **Project State Detection**:
        *   Check `if [ -f "$1/specs/requirements.md" ]`.
        *   If exists: Set `$INITIAL_PROMPT` to empty (resume mode).
        *   If new: Set `$INITIAL_PROMPT` to empty (user writes first, triggering "New Project" flow).
    4.  **Process Handover**:
        *   `exec "$GPTME_BIN" --system "$(cat $SYSTEM_PROMPT_FILE)" -m "$MODEL" -t save,form,read`
    *   **Reasoning**: Using `exec` replaces the shell process, ensuring signals (Ctrl+C) pass directly to `gptme`.

### 2.2 The System Prompt (`gap_system_prompt.md`)
*   **Role Definition**: "You are a helpful coding assistant. Chat naturally with the user."
*   **Trigger Logic**:
    *   Regex-like matching on user intent: `/(build|create|write|make).*/i`
    *   **Action**: `DECISIVE_MOVE -> DRAFT_REQ`
    *   *Note*: While the agent chats naturally, it acts decisively when intent is clear.
*   **Template Enforcement**:
    *   Requirements: EARS Syntax for Coding (Classic Markdown List).
    *   Design: Standard Markdown Headers.
        *   **Traceability Rule**: Every Design Component MUST reference a Requirement ID (e.g., `(Req-1)`).
    *   Tasks: Markdown Checkboxes (`- [ ]`).
*   **Policy Enforcement**:
    *   Instruction: "At step 3, YOU MUST call tool `form`."
    *   Form Schema:
        ```yaml
        acl: [src/ only, src/ and tests/, anywhere]
        tools: [safe, standard, sovereign]
        ```

### 2.3 The Deterministic Policy Form
*   **Tool**: `gptme.tools.form` (Native)
*   **Input**: Structured questions defined in the system prompt.
*   **Output**: JSON object injected back into the context.
*   **Flow**:
    1.  Agent calls `form`.
    2.  `gptme` halts generation, renders TUI form.
    3.  User selects options.
    4.  `gptme` injects JSON: `{"acl": "src/", "tools": "standard"}`.
    5.  Agent writes `specs/policy.md` using the JSON values.


### 2.4 Domain-Specific Syntax Injection (Context Swapping)
*   **Problem**: Different domains require different output formats (e.g., Coding -> EARS, Story -> Narrative Arc).
*   **Mechanism**: Conditional Logic in System Prompt.
*   **Implementation**:
    The generic system prompt contains "Reserved Slots" for domain rules that activate based on the User's choice in Step 1.

    ```markdown
    ## DOMAIN RULES (Conditional)
    
    ### IF DOMAIN == CODING
    **Syntax Rule**: "EARS" (Explicit, Atomic, Rigid, Structured)
    - Require strictly numbered lists.
    - No conversational filler in specs.
    
    ### IF DOMAIN == STORY
    **Syntax Rule**: "Narrative Flow"
    - Allow expressive descriptions.
    - Focus on Character/Setting/Plot.
    ```

*   **Trigger**: When the agent infers "Snake Game" (Coding), it implicitly loads the "EARS" rule set into its working context.


## 4. Security Model
*   **Bootstrap**: Sets the initial sandbox (Current Working Directory).
*   **Runtime**: `gptme` respects the tool allow-list passed via CLI args (`-t save,form,read` initially).
*   **Execution**: Tool allow-list is expanded only after Policy verification.

