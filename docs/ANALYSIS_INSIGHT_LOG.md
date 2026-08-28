# Metrocar Analysis Insight Log

**Status:** Six validated Phase 3 insight records registered
**Last reviewed:** 2026-08-28

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

No separate Phase 2 insight records were created. The first durable findings
were approved through the Phase 3 business-analysis evidence pass.

| ID | Created | Current status | Short title | Related or replacement record |
|---|---|---|---|---|
| `INS-20260828-001` | 2026-08-28 | `Validated` | First-ride fulfillment is the principal funnel priority | `INS-20260828-006` |
| `INS-20260828-002` | 2026-08-28 | `Validated` | Platform is not the primary fulfillment driver | `INS-20260828-001`, `INS-20260828-006` |
| `INS-20260828-003` | 2026-08-28 | `Validated` | Age groups support targeting hypotheses, not economic conclusions | `INS-20260828-006` |
| `INS-20260828-004` | 2026-08-28 | `Validated` | Demand concentration does not demonstrate peak fulfillment failure | `INS-20260828-006` |
| `INS-20260828-005` | 2026-08-28 | `Validated` | Review-without-Paid is a process or data anomaly | None |
| `INS-20260828-006` | 2026-08-28 | `Validated` | Instrument and test first-ride matching and supply | `INS-20260828-001`–`INS-20260828-004` |

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

## 8. Validated Phase 3 Insight Records

### `INS-20260828-001` — First-ride fulfillment is the principal funnel priority

- **Created:** `2026-08-28`
- **Last updated:** `2026-08-28`
- **Status:** `Validated`

- **Business question:**
  Which funnel steps should Metrocar research and improve, are specific
  drop-offs preventing first-ride completion, and which transition has the
  lowest conversion?

- **Observed pattern:**
  Entrant-level Requested → Completed is the lowest-converting canonical
  transition. In the separate first-ride diagnostic, the loss is concentrated
  before the ride starts: 5,201 first rides have cancellation evidence without
  recorded acceptance, and 972 have qualifying cancel-after-accept evidence
  before pickup. All picked-up first rides Finished in the accepted snapshot.

- **Segment or cohort:**
  Full observed source snapshot; no cohort start or end filter; registered
  users with at least one ride in the accepted ride base.

- **Contract reference:**
  Sections 3, 4, 5.2, 6, 7, 10, 12, and 13 of
  `docs/METRIC_DEFINITION_CONTRACT.md`.

- **Evidence:**
  At source cutoff `2022-04-24 20:00:00`, User Requested → Completed is
  12,406 → 6,233: 50.24% conversion, 6,173 drop-off, and 49.76% drop-off.
  All 12,406 requesting registered users had an unambiguous earliest request:
  7,205 first rides were Accepted, 6,233 were Picked Up, and 6,233 Finished.
  The observed pre-acceptance diagnostic population is 5,201; another 972
  first rides qualify as cancel-after-accept. Missing request timestamps,
  conflicting request timestamps, and tied earliest requests each affected
  zero users. SQL and Pandas first-ride totals reconciled exactly.

- **Canonical reproducibility reference:**
  - **Canonical Python:** `analysis.business_insights.run_business_insights`
    and `analysis.business_insights.first_ride_diagnostic` in
    `analysis/business_insights.py` — inputs are the accepted Phase 2 result
    from `analysis.funnel.run_funnel_analysis`, no cohort bounds, and cutoff
    `2022-04-24 20:00:00`; named outputs `overall_transitions.user` and
    `first_ride`.
  - **Exact SQL:** `sql/production/03_business_insights.sql` — named query
    `first_ride_diagnostic`, using `:cohort_start`,
    `:cohort_end_exclusive`, and `:source_cutoff`.

- **Notebook narrative reference:**
  None.

- **Business meaning:**
  The first-ride path before pickup is the strongest research priority. The
  evidence localizes the observed loss but does not establish its cause.

- **Limitations:**
  The source does not contain request-to-accept latency, nearby or available
  driver supply, quoted ETA, cancellation initiator or reason, or price at the
  decision point. Matching latency, driver supply, ETA, and cancellation
  motivation are leading hypotheses requiring instrumentation, not observed
  explanations. Timestamps are source-local and have no known timezone.

- **Recommended next step:**
  Instrument the missing operational variables and validate which factors are
  associated with the observed pre-acceptance diagnostic population before
  selecting a permanent product or operations change.

- **Related records:**
  `INS-20260828-002`, `INS-20260828-004`, `INS-20260828-006`.

#### Status History

| Date | Previous status | New status | Reason and supporting evidence | Changed by |
|---|---|---|---|---|
| 2026-08-28 | `—` | `Validated` | Approved Phase 3 evidence; exact SQL/Pandas first-ride reconciliation and accepted Phase 2 invariants passed. | Spock, under task-specific Insight Log authority |

### `INS-20260828-002` — Platform is not the primary fulfillment driver

- **Created:** `2026-08-28`
- **Last updated:** `2026-08-28`
- **Status:** `Validated`

- **Business question:**
  How does funnel performance differ across ios, android, and web, and what can
  that evidence support about next year's marketing budget?

- **Observed pattern:**
  Platform conversion spreads are modest compared with the common
  Requested/Finished loss. ios supplies the majority of entrant and ride
  volume while converting close to the overall rates.

- **Segment or cohort:**
  Full observed source snapshot, segmented using the accepted signup-linked
  platform attribution; no cohort start or end filter.

- **Contract reference:**
  Sections 3, 7, 8, 10, 12.7, and 13 of
  `docs/METRIC_DEFINITION_CONTRACT.md`.

- **Evidence:**
  At cutoff `2022-04-24 20:00:00`, ios contributes 14,290 of 23,608
  entrants (60.53%) and 234,693 of 385,477 rides (60.88%). The widest user
  transition spread is 1.76 percentage points and the platform spread for
  ride Requested → Finished is 0.87 points. All platform stage totals
  reconcile to the corresponding accepted Phase 2 base.

- **Canonical reproducibility reference:**
  - **Canonical Python:** `analysis.business_insights.platform_comparison` in
    `analysis/business_insights.py` — accepted Phase 2 user and ride bases;
    named outputs `user_stage_counts`, `user_transitions`,
    `ride_stage_counts`, and `ride_transitions` within
    `run_business_insights(...)["platform"]`.

- **Notebook narrative reference:**
  None.

- **Business meaning:**
  The principal fulfillment problem appears cross-platform. ios is the
  largest available test population, but similar conversion does not prove
  superior marketing economics.

- **Limitations:**
  Ride platform is the signup-linked download platform, not proof of the
  device used for a particular request. Marketing spend, CAC, LTV, retention,
  revenue attribution, and incremental lift are unavailable, so funnel
  results do not establish marketing ROI.

- **Recommended next step:**
  Address common fulfillment evidence first. If acquisition testing is
  pursued, measure ios and android CAC and downstream value before any
  permanent budget allocation; do not redistribute budget from funnel results
  alone.

- **Related records:**
  `INS-20260828-001`, `INS-20260828-006`.

#### Status History

| Date | Previous status | New status | Reason and supporting evidence | Changed by |
|---|---|---|---|---|
| 2026-08-28 | `—` | `Validated` | Approved Phase 3 platform evidence reconciled to both accepted Phase 2 bases. | Spock, under task-specific Insight Log authority |

### `INS-20260828-003` — Age groups support targeting hypotheses, not economic conclusions

- **Created:** `2026-08-28`
- **Last updated:** `2026-08-28`
- **Status:** `Validated`

- **Business question:**
  Which age groups perform best from signup onward, and which groups most
  likely contain Metrocar's target customers?

- **Observed pattern:**
  Among known ages, 35–44 combines the largest scale with above-overall
  progression. The 18–24 group shows especially strong early first-ride and
  ride progression. Different known-age groups lead different transitions.

- **Segment or cohort:**
  Full observed source snapshot using accepted signup age attribution. Source
  `Unknown`, `Not available — no signup`, and any explicit unavailable values
  remain separate.

- **Contract reference:**
  Sections 3, 7, 9, 10, 12.7, and 13 of
  `docs/METRIC_DEFINITION_CONTRACT.md`.

- **Evidence:**
  At cutoff `2022-04-24 20:00:00`, age 35–44 has 5,181 signups and
  114,209 ride requests, with 70.68% Signed Up → Requested and 58.54% ride
  Requested → Finished. Age 18–24 has the highest known-age Requested →
  Completed rate (51.54%) and ride Requested → Finished rate (59.20%). Age
  45–54 has the highest known-age Paid → Reviewed rate (71.73%). Age segment
  totals reconcile to the accepted bases.

- **Canonical reproducibility reference:**
  - **Canonical Python:** `analysis.business_insights.age_comparison` in
    `analysis/business_insights.py` — accepted Phase 2 user and ride bases;
    named outputs `user_stage_counts`, `user_transitions`,
    `ride_stage_counts`, and `ride_transitions` within
    `run_business_insights(...)["age"]`.

- **Notebook narrative reference:**
  None.

- **Business meaning:**
  Age 35–44 is a primary target-customer hypothesis based on scale and
  progression; age 18–24 is a secondary growth hypothesis based on strong
  early progression.

- **Limitations:**
  Age is first observed at signup, so Downloaded → Signed Up is not an
  interpretable known-age comparison. The funnel dataset cannot establish
  LTV, profitability, retention, or economically optimal targeting.

- **Recommended next step:**
  Test the two audience hypotheses against repeat usage, retention, revenue,
  and contribution-margin evidence before formal targeting decisions.

- **Related records:**
  `INS-20260828-006`.

#### Status History

| Date | Previous status | New status | Reason and supporting evidence | Changed by |
|---|---|---|---|---|
| 2026-08-28 | `—` | `Validated` | Approved Phase 3 age evidence preserved all governed categories and reconciled to both bases. | Spock, under task-specific Insight Log authority |

### `INS-20260828-004` — Demand concentration does not demonstrate peak fulfillment failure

- **Created:** `2026-08-28`
- **Last updated:** `2026-08-28`
- **Status:** `Validated`

- **Business question:**
  How are ride requests distributed throughout the day, and what can the
  observed pattern support about a potential surge-pricing strategy?

- **Observed pattern:**
  Demand is strongly concentrated at source-recorded hours 8–9 and 16–19,
  but the three largest hours do not have materially worse Accepted, Finished,
  or cancel-after-accept rates than overall.

- **Segment or cohort:**
  Full accepted ride population; source-recorded hour; timezone unavailable;
  no cohort start or end filter.

- **Contract reference:**
  Sections 7, 10, 12.6, and 13 of
  `docs/METRIC_DEFINITION_CONTRACT.md`.

- **Evidence:**
  At cutoff `2022-04-24 20:00:00`, source-recorded hours 8–9 and 16–19
  contain 82.20% of 385,477 requests. The three largest hours are 9, 8, and
  16. Their request-weighted rates differ from overall by +0.04 percentage
  points for Accepted, +0.10 points for Finished, and −0.05 points for
  cancel-after-accept. All 24 hourly counts reconcile exactly to the accepted
  ride population, with zero missing request timestamps in this snapshot.

- **Canonical reproducibility reference:**
  - **Canonical Python:** `analysis.business_insights.request_hour_summary` in
    `analysis/business_insights.py` — accepted Phase 2 ride base; named output
    `run_business_insights(...)["request_hour"]`, including `hourly`,
    `top_six_hours`, `top_six_request_share_pct`, and
    `top_three_minus_overall_pp`.

- **Notebook narrative reference:**
  None.

- **Business meaning:**
  Peak periods are useful candidates for controlled supply, pricing, or
  incentive experiments because they provide sample volume. Current evidence
  does not prove that surge pricing is necessary or that peaks cause worse
  fulfillment.

- **Limitations:**
  The source timezone, driver supply, wait time, quoted price, elasticity, and
  experimental lift are unavailable. Recorded hours cannot be assigned to UTC,
  German time, or another geographic timezone.

- **Recommended next step:**
  Measure supply-demand imbalance and run a controlled experiment with
  completion, cancellation, customer-cost, and driver-supply guardrails. Use
  peak hours for sample volume, not because degradation is already proven.

- **Related records:**
  `INS-20260828-001`, `INS-20260828-006`.

#### Status History

| Date | Previous status | New status | Reason and supporting evidence | Changed by |
|---|---|---|---|---|
| 2026-08-28 | `—` | `Validated` | Approved Phase 3 hourly evidence reconciled to the ride base and retained the timezone limitation. | Spock, under task-specific Insight Log authority |

### `INS-20260828-005` — Review-without-Paid is a process or data anomaly

- **Created:** `2026-08-28`
- **Last updated:** `2026-08-28`
- **Status:** `Validated`

- **Business question:**
  How should stakeholders interpret review evidence that falls outside the
  canonical Paid → Reviewed subset?

- **Observed pattern:**
  Exactly 7,747 rides have review evidence but do not qualify as Paid. All
  7,747 Finished, all have transaction evidence, and none has an Approved
  transaction.

- **Segment or cohort:**
  Full accepted ride population; review-without-Paid diagnostic population;
  no cohort start or end filter.

- **Contract reference:**
  Sections 5.2, 11.3, 12.5, and 13 of
  `docs/METRIC_DEFINITION_CONTRACT.md`.

- **Evidence:**
  At cutoff `2022-04-24 20:00:00`, the 7,747 anomalous rides represent
  4.96% of all 156,211 rides with review evidence. The mutually exclusive
  decomposition is 100% Finished, with transaction evidence, and with no
  Approved transaction. The categories reconcile exactly to 7,747. Canonical
  Paid → Reviewed remains 148,464 / 212,628 = 69.82%.

- **Canonical reproducibility reference:**
  - **Canonical Python:**
    `analysis.business_insights.review_without_paid_decomposition` in
    `analysis/business_insights.py` — accepted Phase 2 ride base; named output
    `run_business_insights(...)["review_without_paid"]`, including
    `population_count`, `decomposition`,
    `anomaly_share_of_all_review_evidence_pct`, and
    `canonical_paid_to_reviewed_pct`.

- **Notebook narrative reference:**
  None.

- **Business meaning:**
  This is a material warning for raw review analysis. Possible workflow,
  payment, or integration explanations remain hypotheses. The anomaly is not
  an ordinary funnel drop-off and does not change canonical Paid or Reviewed
  membership.

- **Limitations:**
  The available tables do not establish whether the pattern comes from review
  access rules, payment processing outside the snapshot, transaction-state
  synchronization, or another integration process.

- **Recommended next step:**
  Audit review eligibility and payment-state synchronization using operational
  system evidence. Continue using the canonical Paid-subset definition for
  published conversion.

- **Related records:**
  None.

#### Status History

| Date | Previous status | New status | Reason and supporting evidence | Changed by |
|---|---|---|---|---|
| 2026-08-28 | `—` | `Validated` | Approved anomaly decomposition reconciled exactly without reclassifying Paid or Reviewed. | Spock, under task-specific Insight Log authority |

### `INS-20260828-006` — Instrument and test first-ride matching and supply

- **Created:** `2026-08-28`
- **Last updated:** `2026-08-28`
- **Status:** `Validated`

- **Business question:**
  What evidence-backed next step could improve the lowest-converting part of
  the funnel?

- **Observed pattern:**
  The lowest canonical conversion is entrant Requested → Completed; ride
  Requested → Finished is the corresponding large-volume operational loss.
  First-ride failures are concentrated before pickup. Platform and age
  differences do not explain the overall magnitude, and demand peaks do not
  show worse fulfillment.

- **Segment or cohort:**
  Full observed source snapshot across the accepted user and ride bases; no
  cohort start or end filter.

- **Contract reference:**
  Sections 3–10, 12, and 13 of
  `docs/METRIC_DEFINITION_CONTRACT.md`.

- **Evidence:**
  At cutoff `2022-04-24 20:00:00`, User Requested → Completed converts at
  50.24% with 6,173 entrant drop-off. Ride Requested → Finished converts at
  58.02% with 161,825 ride drop-off. First-ride diagnostics identify 5,201
  cancellations without recorded acceptance and 972 cancel-after-accept
  first rides. Platform spreads are modest, age leaders vary by transition,
  and top request hours perform close to overall.

- **Canonical reproducibility reference:**
  - **Canonical Python:** `analysis.business_insights.run_business_insights`
    in `analysis/business_insights.py` — accepted Phase 2 result, no cohort
    bounds, cutoff `2022-04-24 20:00:00`; named outputs
    `overall_transitions`, `first_ride`, `platform`, `age`, and `request_hour`.
  - **Exact SQL:** `sql/production/03_business_insights.sql` — named query
    `first_ride_diagnostic` independently validates the genuinely new
    first-ride evidence.

- **Notebook narrative reference:**
  None.

- **Business meaning:**
  The combined evidence supports a controlled first-ride matching or supply
  experiment rather than an immediate permanent pricing, marketing, or
  platform-specific change.

- **Limitations:**
  The dataset lacks request-to-accept latency, nearby or available driver
  supply, quoted ETA, cancellation initiator and reason, and request-level
  price. The evidence is observational and cannot establish causation.

- **Recommended next step:**
  Instrument request-to-accept latency, nearby or available driver supply,
  quoted ETA, cancellation initiator and reason, and price where available;
  then run a controlled first-ride matching/supply experiment. Peak hours may
  provide experimental sample volume, but the current evidence does not prove
  peak-hour degradation.

- **Related records:**
  `INS-20260828-001`, `INS-20260828-002`, `INS-20260828-003`,
  `INS-20260828-004`.

#### Status History

| Date | Previous status | New status | Reason and supporting evidence | Changed by |
|---|---|---|---|---|
| 2026-08-28 | `—` | `Validated` | Data approved the Phase 3 synthesis after the read-only evidence pass; canonicalization preserves all stated limitations. | Spock, under task-specific Insight Log authority |
