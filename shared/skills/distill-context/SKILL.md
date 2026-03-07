---
name: distill-context
description: Distill raw materials from 00_inbox into concise context files in 02_context and prepare 03_specs inputs. Use when inbox is noisy, long, duplicated, or unstructured.
---

# Goal
Turn raw context into a 5-minute context pack.

# Inputs
- `00_inbox/`

# Outputs
- `02_context/BRIEF.md`
- `02_context/FACTS.md`
- `02_context/CONSTRAINTS.md`
- `02_context/LINKS.md`
- `02_context/GLOSSARY.md` when needed

# Procedure
1. Read all inbox files and cluster by topic.
2. Extract facts with source reference.
3. Separate assumptions and unknowns.
4. Write concise context files with no duplication.
5. Propose candidate scope for next spec.

# Anti-patterns
- Copying inbox dumps into context files.
- Mixing facts and opinions without labels.
