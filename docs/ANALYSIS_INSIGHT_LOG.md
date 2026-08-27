# Metrocar Analysis Insight Log

**Status:** Planning-owned structure; no Phase 2 insight records yet  
**Last reviewed:** 2026-08-27

## 1. Purpose

This document is the durable evidence register for analytical findings.

It records:

- what was observed;
- which population, segment, or cohort it applies to;
- how the observation can be reproduced and validated;
- what business meaning the evidence can support;
- which limitations remain;
- what next step is justified;
- how the finding’s status changed over time.

This document does not define metrics. Metric definitions remain governed exclusively by `docs/METRIC_DEFINITION_CONTRACT.md`.

An entry in this log does not authorize implementation, a scope change, a new metric, or a new business assumption.

## 2. Status Definitions

| Status | Meaning |
|---|---|
| `Candidate` | A reproducible pattern has been observed, but required validation, interpretation review, or limitation review is incomplete. It must not support a final recommendation. |
| `Validated` | The pattern has been reproduced, required checks have passed, limitations are recorded, and the business interpretation does not exceed the evidence. |
| `Rejected` | The candidate did not survive validation or relied on incorrect logic, insufficient evidence, or an unsupported interpretation. |
| `Superseded` | A newer record replaced this record because the evidence, scope, definition, or interpretation changed. The replacement record must be identified. |

## 3. Reproducibility Standard

Every insight record must identify at least one executable, canonical source of truth:

1. the exact SQL used to produce the result; and/or
2. a canonical Python module and function that reproduces the result.

A reproducibility reference must include enough information to locate and run the relevant logic:

- repository-relative SQL file and named query, statement, CTE, or output;
- and/or repository-relative Python file, fully qualified module/function name, material parameters, and named output;
- the data-source cutoff;
- cohort or filter parameters;
- the analytical grain;
- the validation output relevant to the claim.

A notebook may provide the student-facing narrative, show intermediate reasoning, and reference the canonical SQL or Python implementation. It must not be the only source of truth for a published metric or finding.

If both SQL and Python implementations exist, the record must identify which one is canonical and explain any role played by the other.

A screenshot, copied result table, chart, manual calculation, notebook display output, or prose-only description may supplement evidence but cannot replace exact SQL or a canonical Python module/function.

## 4. Maintenance Rules

- Use one record for one distinct claim.
- Assign an immutable ID in the form `INS-YYYYMMDD-NNN`.
- Record dates in ISO `YYYY-MM-DD` format.
- Never reuse an ID.
- Do not delete a record because its status changes.
- Append every status transition to the record’s status history.
- Reference the applicable section of `docs/METRIC_DEFINITION_CONTRACT.md`.
- Separate the observed pattern, business interpretation, and recommendation.
- Do not state causation unless the analytical design supports causation.
- Only `Validated` records may directly support final business recommendations.
- A `Candidate` record may recommend further validation but not a final business action.
- `Rejected` and `Superseded` records must remain visible for auditability.
- A `Superseded` record must identify its replacement.
- Material Metric Contract validation failures prevent promotion to `Validated`.
- Editing rights are controlled by `AGENTS.md`, `METROCAR_PROJECT_EXECUTION_PLAN.md`, and explicit task authorization. This document grants no write authority by itself.

## 5. Insight Index

No Phase 2 insight records exist at document creation because Phase 2 analytical implementation has not begun.

Add one index row for every future record.

| ID | Created | Current status | Short title | Related or replacement record |
|---|---|---|---|---|
| — | — | — | No Phase 2 records yet | — |

## 6. Record Template

### `INS-YYYYMMDD-NNN` — Short descriptive title

- **Created:** `YYYY-MM-DD`
- **Last updated:** `YYYY-MM-DD`
- **Status:** `Candidate | Validated | Rejected | Superseded`

- **Business question:**  
  State the specific decision, uncertainty, or approved analytical question being investigated.

- **Observed pattern:**  
  Describe the observed result factually and neutrally. Do not include an unsupported explanation or imply causation.

- **Segment or cohort:**  
  Identify the population, cohort-entry period, platform, age group, or other approved segment to which the pattern applies.

- **Contract reference:**  
  Cite the relevant section or sections of `docs/METRIC_DEFINITION_CONTRACT.md`.

- **Evidence:**  
  Record the relevant result, comparison, population size, analytical grain, data-source cutoff, filter parameters, and validation checks.

- **Canonical reproducibility reference:**  
  Provide at least one of the following:

  - **Exact SQL:** `path/to/query.sql` — named query, statement, CTE, or output
  - **Canonical Python:** `package.module.function` in `path/to/module.py` — material inputs, parameters, and named output

  If both exist, identify the canonical result producer.

- **Notebook narrative reference:**  
  Enter `None` or cite `path/to/notebook.ipynb` and its section or stable cell label. The notebook reference is supplementary and cannot replace the canonical reproducibility reference.

- **Business meaning:**  
  Explain what the pattern may mean for the approved business question. Do not make a stronger claim than the evidence permits.

- **Limitations:**  
  Record relevant data limitations, cohort-maturity effects, missing dimensions, uncertainty, alternative explanations, platform or age attribution limitations, timezone limitations, and scope boundaries.

- **Recommended next step:**  
  State the smallest evidence-based validation, analysis, decision, or action that should follow. A `Candidate` may recommend further validation but must not present a final business recommendation.

- **Related records:**  
  Enter `None` or list related, rejected, superseded, or replacement insight IDs.

#### Status History

| Date | Previous status | New status | Reason and supporting evidence | Changed by |
|---|---|---|---|---|
| `YYYY-MM-DD` | `—` | `Candidate` | Initial observation recorded. | `[authorized editor]` |

## 7. Initial Confirmed Phase 1 Context

The following statements are accepted Phase 1 baseline facts. They are not Phase 2 insight records and do not constitute new analytical results:

- Phase 1 is complete and independently accepted.
- `docs/data_quality_report.md` is the accepted Phase 1 evidence.
- The accepted live-schema comparison reported zero mismatches.
- The accepted validation suite reported 32 passed tests and zero failed tests.
- In the accepted Phase 1 snapshot, no ride had more than one transaction or more than one review.
- The accepted Phase 1 evidence found `dropoff_ts` structurally consistent as the completion marker.
- In the accepted Phase 1 snapshot, 24,727 records had both `accept_ts` and `cancel_ts` non-null. This is only the candidate population for the cancel-after-accept diagnostic. The records must not be described as cancel-after-accept unless the required condition `cancel_ts >= accept_ts` is confirmed.
- The accepted Phase 1 evidence reported no cancellations after pickup or drop-off in that snapshot. This is an observed validation result, not an inference derived from the presence of `cancel_ts` alone.

These baseline facts are snapshot-specific. They must not be treated as permanent source constraints.

They must not be promoted into Phase 2 findings or recommendations without a complete insight record containing canonical reproducibility evidence and all required validation.
