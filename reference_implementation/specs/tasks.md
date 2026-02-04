# Tasks: GAP Native Implementation

## Phase 1: Bootstrap Implementation
- [x] Create `gap-gptme` bootstrap script in `reference_implementation/` (Design: 2.1)
    - [x] Implement environment path resolution
    - [x] Implement API key shim (`OPENROUTER_KEY` -> `OPENROUTER_API_KEY`)
    - [x] Implement `gptme` launch command with `exec`
- [x] Make `gap-gptme` executable (Design: 2.1)

## Phase 2: System Prompt Engineering
- [x] Finalize `gap_system_prompt.md` content (Design: 2.2)
    - [x] Implement "Decisive Action" trigger (`DECISIVE_MOVE`)
    - [x] Implement "Context Swapping" placeholder (Design: 2.4)
    - [x] Implement State Machine instructions (Req -> Design -> Policy -> Tasks)
    - [x] Implement Policy Form enforcement instruction

## Phase 3: Integration & Testing
- [ ] Verify `gap-gptme` launches successfully in `.venv_reference` (Req: 5)
- [ ] Verify "New Project" flow triggers correctly on intent (Req: 2)
- [ ] Verify "Existing Project" flow skips q&a (Req: 4)
- [ ] Verify Policy Form works purely via `gptme` native tool (Req: 3)
