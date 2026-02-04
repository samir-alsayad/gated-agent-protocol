# Requirements: GAP Native Implementation ("gap-gptme")

## 1. Intent & Scope
**Intent**: Create a deterministic, native command-line implementation of the Gated Agent Protocol using `gptme` as the core driver, replacing the legacy Python TUI.
**Scope**: The `gap-gptme` bootstrap script and its associated system prompt (`gap_system_prompt.md`).

## 2. Core Behavior: Decisive Action
The Agent must act as a **Workflow Engine**, not a Conversational Assistant.
*   **No Chat Overhead**: When the user states an intent (e.g., "Build a snake game"), the Agent must **IMMEDIATELY** draft the full `specs/requirements.md` file.
*   **No Clarifying Questions**: The Agent must infer reasonable defaults (language, priority, etc.) rather than asking the user.
*   **Implicit Confirmation**: The specific content of the drafted file serves as the confirmation mechanism. The user approves or rejects the *file*, not the *idea*.

## 3. Protocol: The State Machine
The Agent must enforce the following strict sequence for new projects:

1.  **Requirements**: Drafted immediately upon intent. Saved upon user approval.
2.  **Design**: Drafted immediately upon Requirements approval. Saved upon user approval.
3.  **Policy (Deterministic)**: The Agent **MUST** use the native `form` tool to capture security settings (ACL, Tools). It is **FORBIDDEN** from generating this file via LLM.
4.  **Tasks**: Drafted immediately upon Policy confirmation. Saved upon user approval.
5.  **Execution**: Begins only after Tasks are saved.

## 4. Protocol: Existing Projects
If valid specs (`specs/requirements.md`) exist in the workspace, the Agent must:
*   **Skip Initialization**: Do not ask "What do you want to build?".
*   **Contextual Awareness**: Read existing specs and immediately offer assistance relevant to the current phase.

## 5. Technical Stack
*   **Driver**: `gptme` (Python package).
*   **Bootstrap**: Bash script (`gap-gptme`) setting environment and system prompt.
*   **Model**: Configurable via CLI, default `openrouter/qwen/qwen-2.5-coder-32b-instruct`.
*   **Tools**: `save`, `read`, `form` (strict usage).

## 6. Domain Specificity & Syntax
*   **Coding Domain**: MUST adhere to **EARS** syntax (Explicit, Atomic, Rigid, Structured) for all Specs.
*   **Traceability**: Every Design decision MUST link back to a specific Requirement ID.
*   **Context Swapping**: The Agent must dynamically adopt the correct Syntax Rule based on the inferred domain.

