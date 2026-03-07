---
name: write-spec
description: Create or refine one active SDD-light spec in 03_specs/now from distilled context. Use when execution is unclear, drifting, or missing acceptance criteria.
---

# Goal
Create an execution-ready single spec.

# Inputs
- `02_context/*`
- `03_specs/backlog.md`
- `03_specs/decisions.md`

# Output
- One file in `03_specs/now/`.

# Procedure
1. Define outcome and exact deliverable path.
2. Set scope and no-scope.
3. Add acceptance checklist with objective checks.
4. Capture risks, edge cases, and open questions.
5. Keep one active spec only.

# Anti-patterns
- Multi-spec execution in parallel.
- Acceptance criteria that cannot be verified.
