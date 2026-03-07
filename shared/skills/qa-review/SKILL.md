---
name: qa-review
description: Review a deliverable against the active spec and QA gate, then produce a pass/fail verdict with gaps and fixes. Use before closing any task.
---

# Goal
Prevent false-done closure.

# Inputs
- Deliverable in `04_outputs/`
- Active spec in `03_specs/now/`

# Output
- QA summary with pass/fail, gaps, and required fixes.

# Procedure
1. Check each acceptance criterion explicitly.
2. Validate naming, location, and completeness.
3. List unknowns and unresolved risks.
4. Return pass/fail with shortest fix path.

# Anti-patterns
- Subjective approval without checklist traceability.
- Declaring done with unresolved blockers.
