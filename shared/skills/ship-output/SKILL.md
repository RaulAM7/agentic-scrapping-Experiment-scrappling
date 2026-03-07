---
name: ship-output
description: Produce the requested deliverable from the active spec and place it in 04_outputs with predictable naming. Use when a spec is approved and ready to execute.
---

# Goal
Ship a complete deliverable aligned with the active spec.

# Inputs
- `03_specs/now/*`
- `02_context/*`

# Output
- `04_outputs/YYYY-MM-DD_topic_v1.md` (or spec-defined file)

# Procedure
1. Read active spec and acceptance criteria.
2. Draft deliverable in final format.
3. Verify all criteria before finalizing.
4. Save only deliverable artifacts in `04_outputs/`.

# Anti-patterns
- Shipping from memory without reading the current spec.
- Writing final output into scratch folders.
