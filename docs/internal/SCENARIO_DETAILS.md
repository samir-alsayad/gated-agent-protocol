# Multi-Domain Excellence: Scenarios

## 🔬 Science: LLM Latency Quantization Study
**Goal**: Demonstrate "The Auditor" preventing drift in an LLM benchmark.

### 1. The Hypothesis (intent.md)
*   **H-01**: **IF** a 4-bit quantized model is used instead of 8-bit on M4 Pro, **THEN THE** inference latency **SHALL** decrease by at least 35%.
*   **H-02**: **THE** system **SHALL** maintain a standard deviation of <10ms across 100 runs to ensure statistical significance.

### 2. The Methodology (design.md)
*   **P-01: MLX-Inference-Layer**: Use the Apple MLX framework for local execution. *(Validates: H-01)*
*   **P-02: Deterministic-Sampling**: Fix seed=42 and temperature=0. *(Validates: H-02)*

### 3. The Audit Moment (Task Drift)
*   **User Proposal**: "Add a task to integrate stability-ai for image generation so we can see the benchmarks for that too."
*   **The Check**: Running `gap check traceability`
*   **The Result**: **BLOCK**. "Image generation" has no pedigree link to "LLM Latency Hypothesis (H-01/H-02)".

---

## 📖 The Pivot: Structural Domain Shift
**Goal**: Show that GAP changes the *Agent's Soul* via the Manifest, not the Prompt.

### 1. The Setup
*   The User is currently working on the **School of First Principles**.
*   The User performs a **Project Shift**: `cd ../the-silicon-heart` (which has a manifest `extends: [creative-writing]`).

### 2. The Realization
*   As soon as the TUI is launched, the Agent's "Structural Guardrails" are narratived-focused.
*   **User Action**: "Propose the Synopsis."
*   **Wow Moment**: The agent doesn't talk about NAND gates. It immediately uses the "Conflict-Goal" framework (R-01 as the Inciting Incident) because that is what the **Creative Writing Protocol** demands. 
