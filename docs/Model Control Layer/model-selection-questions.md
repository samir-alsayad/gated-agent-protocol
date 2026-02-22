# Model Selection Questions

**Purpose**: Figure out which models are actually needed for each phase of work, and whether local models are sufficient or cloud is required.

---

## Phase 1: Alignment (Requirements, Design, Tasks)

### Writing Requirements from a User Conversation
- Can a local 14B–32B model distill a freeform user conversation into structured requirements?
- Or does this need a frontier model (Opus, GPT-4o) because it requires deep comprehension and ambiguity resolution?
- Does the domain matter? (e.g., simple CRUD app vs. distributed system architecture)
- What's the failure mode if a weaker model misses a requirement? Is that caught later or silently propagated?

### Writing Design from Requirements
- Design requires architectural reasoning — is a 14B coder model equipped for this?
- Does a reasoning model (DeepSeek-R1, QwQ) help here more than a general model?
- Can we split this: use a local model for the *structure* (headings, sections) and a cloud model for the *substance*?

### Writing Tasks from Design
- Tasks are more mechanical — decompose design into atomic steps. Can a small model (7B–14B) handle this?
- What about dependency ordering and traceability back to requirements — does that need stronger reasoning?

---

## Phase 2: Execution (Code, Writing, Data)

### Code Implementation
- Which coding models actually perform well locally? Qwen2.5-Coder-14B? DeepSeek-Coder-V2?
- At what complexity level does a local model start producing bugs that cost more time to fix than the cloud API would cost?
- Can IntentCoding / contrastive decoding techniques (from Inference_LLM_Lab research) close this gap?

### Code Review / Verification
- Can a local model reliably verify code against a task specification?
- Or is this a "trust but verify" situation where a second, stronger model should audit?

### Documentation / Writing
- For non-code artifacts (READMEs, reports, explanations) — is a local model sufficient?
- What about technical writing that requires domain expertise?

---

## Cross-Cutting Questions

### Model Size vs. Task Complexity
- Is there a rough heuristic? e.g.:
  - **< 7B**: Formatting, linting, simple transforms
  - **7B–14B**: Code completion, task decomposition, simple writing
  - **14B–32B**: Design, moderate reasoning, code generation
  - **70B+ / Cloud**: Complex architecture, ambiguity resolution, deep reasoning
- How does quantization affect this? Is a 4-bit 32B worse than an 8-bit 14B for reasoning?

### When Is Cloud Non-Negotiable?
- What tasks consistently fail with local models?
- Is there a measurable quality threshold (e.g., pass@1 on benchmarks) below which local is not viable?

### Specialization vs. Generalism
- Are niche models (code-specific, math-specific) meaningfully better than general models of the same size?
- Should the registry tag models by capability (`code`, `reasoning`, `chat`) and auto-suggest?

### Cost-Benefit
- What does a typical GAP session cost on OpenRouter vs. running locally?
- At what daily usage does buying more RAM pay for itself vs. cloud credits?

---

## Next Steps
- [ ] Benchmark local models on actual GAP phase artifacts (requirements, design, tasks)
- [ ] Create a scoring rubric for "good enough" output per phase
- [ ] Build a decision matrix: task type × model size × local/cloud
