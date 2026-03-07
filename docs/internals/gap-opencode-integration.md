# GAP & OpenCode Architecture Decision Record

## The Core Invariant
Before deciding how to integrate GAP and OpenCode, we must establish the single non-negotiable rule of the Gated Agent Protocol:

**The Agent must NEVER be aware of, author, or modify the Execution Plan (`.gap/plan.yaml`).**

The Execution Plan is the "Powers Granted" contract signed by the Human Supervisor. It defines exactly what models can be used and where the checkpoints are. If the AI can read or write the plan, it can grant itself more power or bypass checkpoints, breaking the entire premise of the Consent Ledger.

## The Question: Plugin vs. Wrapper

Should GAP be an OpenCode Plugin, or should GAP wrap OpenCode as a first-class citizen?

To answer this, we must look at who boots up first.

### Option A: OpenCode as the Host (GAP as a Plugin)
In this model, you run `opencode` in your terminal. OpenCode boots up its AI session. As it runs, it occasionally calls a custom "GAP Tool" we write in TypeScript (e.g., `packages/plugin/src/gap.ts`).

*   **How it works:** OpenCode says to the LLM: *"You have a tool called `gap_verify_checkpoint`. Call this before moving to the next task."*
*   **The Flaw:** This violates the Core Invariant. We are relying on the LLM to *choose* to call the checkpoint tool. If the LLM is confused or goes rogue, it simply stops calling the tool and edits files directly using its native `write_file` tool.
*   **Architectural Verdict:** A strict security ledger cannot be an optional tool inside the sandbox it's trying to securely govern.

### Option B: GAP as the Host (OpenCode as the Engine)
In this model, GAP is the primary CLI tool. You run `gap execute tasks`. GAP boots up, reads `.gap/plan.yaml`, and firmly dictates the parameters of the environment *before* OpenCode ever starts.

*   **How it works:** GAP reads `.gap/plan.yaml`. It sees "Model: Qwen, Checkpoint: Phase 1". GAP programmatically launches a sandboxed instance of OpenCode from the outside (e.g., using `subprocess.run(["opencode", "--model", "qwen", "Do Task 1"])`). OpenCode does exactly Task 1 and exits. GAP logs the checkpoint, asks the supervisor for permission, and then launches OpenCode *again* for Task 2.
*   **The Advantage:** The AI has absolutely zero awareness that GAP exists. It is just repeatedly woken up by an invisible God, told to do one tiny task, and then put back to sleep. There is no way for the LLM to bypass checkpoints because the LLM process is literally terminated at every checkpoint.

## Conclusion

**GAP must be a first-class citizen that wraps OpenCode.** 

If GAP is just a plugin *inside* OpenCode, we are asking the prisoner to lock their own cell door. By making GAP the parent process, GAP becomes the warden that opens and closes the OpenCode execution sandbox based on the rules strictly enforced in the human-authored `.gap/plan.yaml`.

---
*Drafted based on conversation regarding OpenCode architecture and GAP invariants.*
