# Metrocar Analysis Insight Log

**Status:** Active rebuild register — no current findings accepted  
**Reset date:** 2026-09-02

## 1. Purpose and Authority

This document is the active evidence register for findings established by the current Metrocar analytical rebuild.

It records:

- what was observed;
- the population, cohort, segment, grain, and cutoff;
- how the result is reproduced and validated;
- what the evidence supports;
- what remains uncertain;
- the interpretation or hypothesis, when appropriate;
- the smallest justified recommendation or next question; and
- the finding’s status history.

This document does not define metrics.

Current analytical meaning remains governed by `docs/METRIC_DEFINITION_CONTRACT.md`.

An entry does not authorize implementation, a new metric, a scope change, publication, or business action.

## 2. Current Rebuild State

There are no current accepted findings at this reset checkpoint.

Earlier analytical work contained six records marked `Validated` at source cutoff `2022-04-24 20:00:00`.

Those records are preserved:

- locally at `.local_archive/docs/docs/ANALYSIS_INSIGHT_LOG.md`; and
- in Git history, including file-changing commit `4d3269117cd258a443c138aa8d3b0ce10c3564af`.

The documentation reset does not change or revoke their historical statuses.

However, those records are not current rebuild findings and must not:

- select the first business question;
- preselect the recruiter-facing story;
- support a new public recommendation without reconciliation;
- substitute for current Technical PASS or Learning PASS; or
- silently regain active authority because old code or outputs still exist.

When the current rebuild independently re-establishes a related claim, create a new record with a new ID and identify the historical record under `Related historical records`.

Do not copy, rewrite, or update the archived record as if the new evidence had existed at its original review date.

## 3. Status Definitions

| Status | Meaning |
|---|---|
| `Candidate` | A reproducible pattern has been observed, but required validation, interpretation review, limitation review, or Learning PASS is incomplete. It cannot support a final recommendation. |
| `Validated` | The pattern has been reproduced, required technical checks passed, Data granted Learning PASS for the relevant analytical slice, limitations are recorded, and the interpretation does not exceed the evidence. |
| `Rejected` | The candidate did not survive validation or depended on incorrect logic, insufficient evidence, or an unsupported interpretation. |
| `Superseded` | A newer active record replaced this record because the evidence, scope, definition, or interpretation changed. The replacement record must be identified. |

Archival location is not a finding status.

## 4. Admission Gate

Before a current record is added, the authorized evidence package must identify:

1. the approved business and analytical question;
2. source tables and required fields;
3. analytical grain;
4. cohort, cutoff, filters, and assumptions;
5. applicable Metric Contract sections;
6. exact SQL and/or canonical Python/Pandas implementation;
7. the named output containing the evidence;
8. join, grain, formula, and reconciliation checks as applicable;
9. the evidence ceiling and material limitations;
10. Troi’s interpretation review;
11. Data’s Learning PASS decision; and
12. the explicit authority to modify this file.

A failed material validation prevents promotion to `Validated`.

A result from a fixture or candidate implementation must not be recorded as a real Metrocar business finding.

## 5. Maintenance Rules

- Use one record for one distinct claim.
- Assign an immutable ID in the form `INS-YYYYMMDD-NNN`.
- Record dates in ISO `YYYY-MM-DD` format.
- Never reuse an ID, including an ID present only in the historical archive.
- Do not delete an active record because its status changes.
- Append every active status transition to the record’s status history.
- Reference the applicable Metric Contract sections.
- Keep the observed fact separate from interpretation, hypothesis, judgment, and recommendation.
- Do not state causation unless the analytical design supports it.
- Only `Validated` current records may directly support a current final business recommendation.
- A `Candidate` may recommend additional validation but not a final business action.
- `Rejected` and `Superseded` active records remain visible for auditability.
- A `Superseded` record must identify its replacement.
- Historical findings require new current evidence and a new current ID before use.
- Editing rights remain controlled by `AGENTS.md`, `METROCAR_PROJECT_EXECUTION_PLAN.md`, and explicit task authorization.

## 6. Current Record Index

No current records.

| ID | Created | Current status | Short title | Related historical or replacement record |
|---|---|---|---|---|
| — | — | — | No current findings accepted | — |

## 7. Record Template

### `INS-YYYYMMDD-NNN` — Short descriptive title

- **Created:** `YYYY-MM-DD`
- **Last updated:** `YYYY-MM-DD`
- **Status:** `Candidate | Validated | Rejected | Superseded`

- **Business question:**  
  State the approved decision or uncertainty being investigated.

- **Analytical question:**  
  State the measurable question answered by this record.

- **Observed fact:**  
  Describe the directly observed result without explanation or causal language.

- **Population, cohort, and grain:**  
  Identify the entity counted, population, cohort bounds, filters, segment, and source-data cutoff.

- **Contract reference:**  
  Cite the relevant sections of `docs/METRIC_DEFINITION_CONTRACT.md`.

- **Evidence:**  
  Record the material values, comparisons, denominators, and validation checks.

- **Canonical reproducibility reference:**  
  Provide at least one exact executable reference:

  - **Exact SQL:** `path/to/query.sql` — named query, statement, CTE, or output
  - **Canonical learner-facing Python:** `path/to/file.py` or `path/to/notebook.ipynb` — stable named section, `# %%` analytical section, named output, or other durable locator; include material inputs, parameters, and source cutoff
  - **Canonical Python module/function:** `package.module.function` in `path/to/file.py` — material inputs, parameters, and named output

  Use whichever canonical form or approved combination actually governs the analytical slice. A learner-facing Python artifact does not require a separate supporting module merely to satisfy architecture.

  If multiple canonical paths exist, identify their roles and reconciliation result.

- **Technical PASS:**  
  Record the exact reviewed artifact, validation scope, commands or evidence, and decision date.

- **Learning PASS:**  
  Record Data’s decision, reviewed analytical slice, and decision date.

- **Interpretation:**  
  Explain what the observed fact may mean without presenting the interpretation as another fact.

- **Alternative explanations or hypotheses:**  
  Record material possibilities the available evidence cannot distinguish.

- **Judgment:**  
  State what the evidence currently supports and does not support.

- **Limitations:**  
  Record material uncertainty, missing dimensions, attribution limits, maturity effects, or scope constraints.

- **Recommended action or next question:**  
  State the smallest justified action, validation, experiment, deliberate non-action, or next analytical question.

- **Related current records:**  
  Enter `None` or list current IDs.

- **Related historical records:**  
  Enter `None` or list immutable IDs from the archived register.

### Status History

| Date | Previous status | New status | Reason and supporting evidence | Changed by |
|---|---|---|---|---|
| `YYYY-MM-DD` | `—` | `Candidate` | Initial current-rebuild observation recorded. | `[authorized editor]` |
