---
name: icp-definer
description: >
  Generate a smart, minimal ICP (Ideal Customer Profile) from any input —
  messy notes, product descriptions, founder hypotheses, or existing context.
  Produces a dual-render artifact (human-readable + machine-structured YAML)
  with observable signals for agentic scraping. Use when the user mentions ICP,
  ideal customer, target customer, who to sell to, customer profile, buyer
  persona, target market, or needs to define who they're going after
  commercially — even if they don't use the term "ICP" explicitly.
---

# Goal

Transform fuzzy strategic input into a compact, actionable ICP artifact consumable by both humans and downstream agents (scraping, offer design, outbound, CRM).

# Inputs

- `00_inbox/` — raw materials
- `02_context/` — distilled context if available
- Direct user input (free text, notes, hypotheses)
- Any combination of the above

# Output

- `04_outputs/icp-[segment-name].md` — ICP artifact in markdown with embedded YAML block
- If multiple segments: one file per segment + `04_outputs/icp-index.md` with ranking

# Core Principles

Three rules that govern the entire execution:

1. **Extract-first.** Parse all available input before asking a single question. Infer aggressively. Only ask what cannot be deduced and is critical to continue. Maximum 3 questions per iteration. Prefer multiple-choice over open-ended.

2. **Signals over descriptions.** Every strategic attribute must translate to at least one observable signal. If you cannot derive a signal, the attribute is decorative — mark it as such or remove it.

3. **Confidence, not certainty.** Every field carries a tag: `stated` (user said it), `inferred` (you deduced it), `hypothesis` (plausible but unconfirmed). Downstream agents use this to weigh decisions.

# Procedure

## Phase 1 — Absorption

1. Read all available input (inbox, context, direct text).
2. Extract: what is being sold, who it seems aimed at, what pains are mentioned, what market context is implied.
3. Identify critical gaps vs gaps you can reasonably infer.
4. If critical gaps block progress (you cannot even infer what is being sold), ask — maximum 3 questions, multiple-choice format when possible.

## Phase 2 — Segment Hypotheses

5. Generate 1-3 candidate segments. Each segment is an ICP hypothesis, not a certainty.
6. For each segment, articulate in one sentence: who + what pain + why now.
7. If more than one segment, rank by: accessibility x pain intensity x ability to pay.
8. Present to user for selection/confirmation of beachhead. If only one clear segment exists, skip selection.

## Phase 3 — ICP Construction

9. For the selected segment (or the only one), build the 6 blocks of the artifact (see Output Format below).
10. For each attribute in blocks 1-3, derive at least one observable signal and populate block 4. Consult `references/signal-patterns.md` for patterns by org type and data source.
11. Build the anti-ICP (block 5) from logical inversions + explicit exclusions from input.
12. Build the scoring heuristic (block 6) combining signals from block 4 with weights.

## Phase 4 — Validation

13. Apply the **concreteness test**: could you name 10 real companies that fit? If not, the ICP is too vague — tighten it.
14. Apply the **scrapeability test**: can each signal in block 4 be looked up in a real data source? If not, reformulate the signal or mark it as `manual_check`.
15. Mark the overall ICP status: `[draft]`, `[refined]`, or `[validated]`.

# Output Format

The artifact has two renders of the same content in a single file.

## Human render (markdown) — top of file

```markdown
# ICP: [Segment Name]
> Status: draft | refined | validated
> Generated: YYYY-MM-DD
> Beachhead: yes | no
> Confidence: low | medium | high

## 1. Target Org
| Attribute | Value | Confidence |
|-----------|-------|------------|
| ... | ... | stated/inferred/hypothesis |

## 2. Trigger Events
| Event | Time Window | Confidence |
|-------|-------------|------------|
| ... | ... | ... |

## 3. Decision Unit

**Buyer** — [Role]: [pain] / [motivator]
**User** — [Role]: [pain]
**Blocker** — [Role]: [objection]
(Omit blocker if it cannot be inferred — do not invent.)

## 4. Observable Signals

### LinkedIn / Sales Navigator
| Signal | Query Hint | Confidence | Check Type |
|--------|-----------|------------|------------|
| ... | ... | ... | automated/manual_check |

### Web / Tech Stack
| Signal | Query Hint | Confidence | Check Type |
|--------|-----------|------------|------------|

### Job Boards
| Signal | Query Hint | Confidence | Check Type |
|--------|-----------|------------|------------|

### Databases / Registries
| Signal | Query Hint | Confidence | Check Type |
|--------|-----------|------------|------------|

(Only include source categories with actual signals. Do not add empty sections.)

## 5. Anti-ICP
| Exclusion | Reason |
|-----------|--------|
| ... | ... |

## 6. Scoring Heuristic
| Signal (or combination) | Weight (1-5) | Source |
|------------------------|--------------|--------|
| ... | ... | ... |

## Changelog
| Date | Change | Reason |
|------|--------|--------|
| YYYY-MM-DD | Initial generation | — |
```

## Machine render (YAML) — bottom of file, fenced

Append this block at the very end of the file. Downstream agents parse this block directly without reading the markdown above.

```yaml
---
# machine-readable ICP — do not edit manually, generated from content above
icp:
  segment: ""
  status: draft|refined|validated
  confidence: low|medium|high
  beachhead: true|false
  generated: "YYYY-MM-DD"

  target_org:
    - attribute: ""
      value: ""
      confidence: stated|inferred|hypothesis

  triggers:
    - event: ""
      window: ""
      confidence: stated|inferred|hypothesis

  decision_unit:
    buyer:
      role: ""
      pain: ""
      motivator: ""
    user:
      role: ""
      pain: ""
    blocker:
      role: ""
      objection: ""

  signals:
    - signal: ""
      source: ""
      query_hint: ""
      confidence: stated|inferred|hypothesis
      check_type: automated|manual_check

  anti_icp:
    - exclusion: ""
      reason: ""

  scoring:
    - signal_ref: ""
      weight: 1-5
      source: ""
---
```

# About the 6 Blocks

## Block 1 — Target Org
Maximum 5 attributes. Prioritize the ones that discriminate most. Use ranges, not point values (e.g. "50-200 employees", not "100 employees"). Typical attributes: vertical sector, size (employees/revenue), stage (startup/scaleup/enterprise), geography, business model, tech stack.

## Block 2 — Trigger Events
What is happening **now** in the organization that creates urgency. Without triggers, there is no buying timing. Examples: recent funding round, aggressive hiring in a specific area, regulatory change, tool migration, loss of a key competitor, new C-level hire. Each trigger has an estimated relevance time window.

## Block 3 — Decision Unit
Not an extensive buyer persona. Three roles maximum:
- **Buyer**: who signs. Their pain and their motivator.
- **User**: who uses it daily. Their operational pain.
- **Blocker**: who can veto. Their typical objection.
If a blocker cannot be inferred, omit it — do not fabricate.

## Block 4 — Observable Signals
The differentiating block. Each signal must answer: "what could a scraping agent look for to detect this type of organization or person?"

Organize by data source (LinkedIn, Web, Job Boards, Databases, Activity Signals). Each signal includes a `query_hint` — a hint on how to search for it (e.g. "LinkedIn Sales Nav filter: headcount growth > 20% last 6mo").

Consult `references/signal-patterns.md` for patterns by org type and data source.

## Block 5 — Anti-ICP
Exclusions that save time for the pipeline. Must be verifiable. Examples: "Companies with fewer than 10 employees — no budget or decision structure", "Public sector — incompatible buying cycles".

## Block 6 — Scoring Heuristic
Combines signals from block 4 with weights (1-5). Enables automatic ranking:
- **Weight 5**: signal that nearly confirms fit (e.g. "uses [competitor tool] + posted a [relevant area] role")
- **Weight 1**: weak signal that only adds context
Signal combinations can have compound weights (e.g. "signal A + signal B together = weight 8").

# Multi-segment

When multiple segments are generated, create:
- One file per segment: `icp-[segment-name].md`
- An index: `icp-index.md` with ranking, one-line summary per segment, and beachhead recommendation

# Refinement Mode

When invoked on an existing ICP:
1. Read the current artifact.
2. Integrate new input (scraping data, sales feedback, new hypothesis).
3. Update affected fields, adjust confidence levels.
4. Log what changed and why in the `## Changelog` block.
5. Bump status if warranted (draft → refined → validated).

# Anti-patterns

- Filling all 6 blocks with weak inferences when input is poor. Better to have 3 solid blocks and 3 marked as `[pending input]`.
- Signals that cannot be looked up in any real data source. If it is not scrapeable or verifiable, it is not a signal.
- Confusing the ICP with the offer. This artifact defines who to target, not what to sell them.
- ICPs that fail the concreteness test — if you cannot name companies, it is too abstract.
- Output exceeding ~120 lines (human render + YAML). Compress or downstream agent context windows will saturate.
- Inventing blocker roles or trigger events without evidence. Omit what you do not know.
