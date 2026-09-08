# Metrocar Metric Definition Contract

**Status:** Current analytical definitions; implementation requires separate authorization

**Final substantive authority:** Data

**Last reviewed:** 2026-09-08

## 1. Purpose and Authority

This document is the binding definition contract for current Metrocar funnel analysis.

It defines:

- analytical grain;
- funnel-stage membership;
- approved funnel calculations;
- cohort-entry filtering;
- platform and age attribution;
- timestamp treatment;
- join direction and row preservation;
- multiplicity handling;
- validation and monotonicity requirements;
- reproducibility and learner-facing analytical-document requirements.

All future SQL, Python analytical artifacts, datasets, visualizations, findings, and recommendations must follow this contract.

`docs/MASTERSCHOOL_METROCAR_SOURCE_BRIEF.md` governs reconstruction of the original curriculum. This contract governs current analytical meaning. Current precision that goes beyond the historical curriculum must not be attributed to MasterSchool.

This document contains no final analytical result and does not authorize implementation. It must not be interpreted as permission to add metrics, alter business definitions, or progress into another analytical task.

If implementation conflicts with this contract, implementation must stop until Data resolves the conflict.

## 2. General Counting Principle

Every funnel stage is evaluated at its declared analytical grain.

Stage membership is boolean at that grain:

- an entity either qualifies for a stage or does not;
- multiple downstream records must not multiply the entity count;
- every later main-funnel stage must be a subset of the preceding stage.

Use existence flags, grain-level pre-aggregation, `EXISTS`, or equivalent reproducible logic. Raw joined-row counts must not be used as funnel counts.

For any stage `S`:

```text
N(S) = count of distinct grain identifiers that qualify for S
```

Conceptually:

```text
N(S) = COUNT(DISTINCT grain_identifier) where stage_S = TRUE
```

Counts are exact integers and must not be rounded.

## 3. Funnel Calculations and Presentation Rules

The conversion and drop-off formulas in Sections 3.1–3.3 apply only to adjacent stages of the two approved main funnels:

```text
User funnel:
Downloaded → Signed Up → Requested → Completed

Ride funnel:
Requested → Finished → Paid → Reviewed
```

Accepted and cancel-after-accept are secondary diagnostics and are not included in main-funnel conversion or drop-off calculations.

For adjacent stages `A → B`:

### 3.1 Conversion Rate / Percent of Previous

The historical curriculum label `Percent of Previous` and the current contract term `adjacent-stage conversion rate` refer to the same analytical measure.

```text
conversion_rate_pct(A → B)
    = 100 × N(B) / N(A)
```

Equivalent SQL calculation:

```text
100.0 * N(B) / NULLIF(N(A), 0)
```

### 3.2 Drop-Off Count

```text
dropoff_count(A → B)
    = N(A) - N(B)
```

### 3.3 Drop-Off Rate

```text
dropoff_rate_pct(A → B)
    = 100 × (N(A) - N(B)) / N(A)
```

Equivalent SQL calculation:

```text
100.0 * (N(A) - N(B)) / NULLIF(N(A), 0)
```

The drop-off rate must be calculated directly from unrounded counts. It must not be derived by subtracting a previously rounded conversion rate from `100`.

### 3.4 Zero-Denominator Rule

If:

```text
N(A) = 0
```

then:

- conversion rate is `NULL`;
- drop-off rate is `NULL`;
- the presentation label must be `N/A`, not `0%`, `100%`, or infinity;
- drop-off count remains the exact arithmetic difference;
- any later-stage count greater than zero is a subset and monotonicity failure that must be resolved before publication.

### 3.5 Rounding Rule

- Counts remain exact integers.
- Rates must be calculated and validated at full available precision.
- Rounding occurs only in the final presentation layer.
- Published percentage rates must be rounded to two decimal places.
- Intermediate values must not be rounded.
- Reconciliation and monotonicity checks must use unrounded counts and rates.
- All results within the same table or visualization must use the same percentage precision.

When results are segmented, numerator and denominator must belong to the same selected cohort, segment, and approved source snapshot.

### 3.6 Percent of Top — Descriptive Stage Context

Percent of Top is approved as a descriptive funnel-context measure for every
stage of each approved main funnel. It is not an adjacent-stage conversion
rate, does not add a funnel stage, and must not replace Percent of Previous.

For any stage `S`, let `T` be the funnel's top stage:

| Funnel | Top stage `T` |
|---|---|
| User Funnel | Downloaded |
| Ride Funnel | Requested |

“Top” is scope-dependent: it means the first stage of the selected approved funnel. `Downloaded` is therefore not a universal denominator. A new sub-funnel and its top stage require separate approval under the scope-change rule in Section 15.

```text
percent_of_top_pct(S)
    = 100 × N(S) / N(T)
```

The numerator and top-stage denominator must use the same selected cohort,
segment, and approved source snapshot.

Percent of Top must be calculated from exact unrounded stage counts at full
available precision. Section 3.5 governs presentation rounding.

If `N(T) = 0`, Percent of Top is `NULL` for every stage and the presentation
label is `N/A`. It must not be displayed as `0%`, `100%`, or infinity.

When `N(T) > 0`, Percent of Top for the top stage is `100%`. A later stage may
also equal `100%` when its exact stage count equals `N(T)`; this indicates no
loss from the top population and does not make Percent of Top an adjacent-stage
conversion rate.

No non-adjacent or additional conversion metric is approved by Sections 3.1–3.5. Section 3.6 approves only the named descriptive Percent of Top context measure.

## 4. User Funnel

### 4.1 Analytical Grain

The user-funnel grain is one distinct:

```text
app_downloads.app_download_key
```

`app_download_key` is an analytical entrant and proxy for one recorded app download. It is not evidence of a uniquely identified physical person.

User-funnel results must therefore be described as entrant-level or download-level results, not as counts of unique people.

Duplicate source rows for the same `app_download_key`, if encountered, are a data-quality finding. They must not silently create additional entrants.

### 4.2 Main Stages

The main user funnel is:

```text
Downloaded → Signed Up → Requested → Completed
```

#### Downloaded

An entrant is Downloaded when its distinct `app_download_key` exists in `app_downloads`.

#### Signed Up

An entrant is Signed Up when it is Downloaded and at least one matching signup exists through:

```text
app_downloads.app_download_key = signups.session_id
```

A download without a matching signup remains in Downloaded and must not be removed from the funnel.

#### Requested

An entrant is Requested when it is Signed Up and the linked signup user has at least one ride request through:

```text
signups.user_id = ride_requests.user_id
```

Multiple ride requests by the same entrant must not multiply the entrant count.

#### Completed

An entrant is Completed when it is Requested and the linked signup user has at least one ride satisfying the Finished definition in this contract.

Multiple Finished rides by the same entrant must not multiply the entrant count.

## 5. Ride Funnel

### 5.1 Analytical Grain

The ride-funnel grain is one distinct:

```text
ride_requests.ride_id
```

Duplicate source rows for the same `ride_id`, if encountered, are a data-quality finding. They must not silently create additional rides.

### 5.2 Main Stages

The main ride funnel is:

```text
Requested → Finished → Paid → Reviewed
```

#### Requested

A ride is Requested when its distinct `ride_id` exists in `ride_requests`.

#### Finished

A ride is Finished when:

```text
ride_requests.dropoff_ts IS NOT NULL
```

`pickup_ts`, lifecycle chronology, and the presence or absence of `cancel_ts` are validation checks. They are not additional filters in the Finished definition.

A record containing any of the following must be surfaced as a data-quality issue before publication:

- `dropoff_ts` without `pickup_ts`;
- incompatible lifecycle timestamp order;
- both completion and cancellation evidence.

Such records must not be silently removed or reclassified by adding an unapproved filter.

#### Paid

A ride is Paid when:

1. it is Finished; and
2. it has at least one linked transaction satisfying:

```text
transactions.charge_status = 'Approved'
```

The join key is:

```text
ride_requests.ride_id = transactions.ride_id
```

The existence of a transaction alone is not sufficient.

A transaction with:

```text
charge_status = 'Decline'
```

does not qualify the ride as Paid.

The condition:

```text
purchase_amount_usd > 0
```

is not part of the approved Paid definition.

Paid membership remains boolean at the `ride_id` grain. Multiple transaction rows or multiple Approved transaction rows for the same `ride_id` must not increase the Paid ride count.

Either form of transaction multiplicity is a data-quality finding that must be reported and validated.

A ride with an Approved transaction but without Finished status does not qualify as Paid and must be reported through the Approved-without-Finished validation.

#### Reviewed

A ride is Reviewed when:

1. it is Paid; and
2. it has at least one linked row in `reviews`.

The join key is:

```text
ride_requests.ride_id = reviews.ride_id
```

A non-empty value in a review-text field is not an additional requirement. The existence of a linked review row is sufficient.

Reviewed membership remains boolean at the `ride_id` grain. Multiple review rows for the same `ride_id` must not increase the Reviewed ride count and must be reported as a data-quality finding.

A ride with a review row but without Paid status does not qualify as Reviewed and must be reported through the review-without-Paid validation.

## 6. Accepted and Cancel-After-Accept Treatment

Accepted is a secondary diagnostic metric. It is not a stage in the main ride funnel.

A ride is Accepted when:

```text
ride_requests.accept_ts IS NOT NULL
```

A ride containing both `accept_ts` and `cancel_ts` remains Accepted for this diagnostic.

A ride qualifies for the cancel-after-accept diagnostic only when all three conditions are true:

```text
accept_ts IS NOT NULL
AND cancel_ts IS NOT NULL
AND cancel_ts >= accept_ts
```

Timestamp equality is included by the approved rule.

A ride with both timestamps present but:

```text
cancel_ts < accept_ts
```

must:

- remain Accepted if `accept_ts` is present;
- not be described or counted as cancel-after-accept;
- be reported as a lifecycle timestamp anomaly.

`cancel_ts` alone does not establish whether a ride started.

Evidence that a ride started comes from:

```text
pickup_ts
```

Evidence that a ride finished comes from:

```text
dropoff_ts
```

Therefore:

- a qualifying cancel-after-accept ride remains Accepted;
- a cancelled ride without `dropoff_ts` remains only in Requested within the main ride funnel;
- the presence of `cancel_ts` must not be used to claim that the ride never started without checking `pickup_ts`;
- a record containing both `cancel_ts` and `dropoff_ts` follows the Finished definition but must be surfaced as contradictory lifecycle evidence before publication.

Cancellation does not independently add, remove, or reorder a main-funnel stage.

## 7. Source Snapshot, Cohort Entry, and Downstream Timing

### 7.1 Approved Source Snapshot / Provenance Boundary

The approved Metrocar source snapshot is the default evidence boundary. The source-data cutoff is primarily provenance metadata that identifies the evidence state reproducibly. It is not, by default, an independent event-time eligibility filter applied to every downstream record.

For the default full-snapshot analysis:

```text
approved source snapshot
→ rows present in that snapshot are available evidence
→ cohort filters select entrants when a question defines a cohort
→ downstream outcomes are evaluated from the rows present in the approved snapshot
```

Each run must record enough existing source-cutoff metadata to identify the approved source snapshot reproducibly. Where an approved source-cutoff value already exists, use that value. Do not invent or substitute a new timestamp or snapshot ID.

### 7.2 Cohort-Entry Date Filtering

Date filters select entities by the timestamp at which they enter their respective funnel:

| Funnel | Cohort-entry timestamp |
|---|---|
| User funnel | `app_downloads.download_ts` |
| Ride funnel | `ride_requests.request_ts` |

The selected start date and end calendar date are inclusive from the user’s perspective.

The technical predicate must use a half-open interval:

```text
entry_timestamp >= start_date
AND entry_timestamp < day_after_end_date
```

### 7.3 Downstream Outcome Membership

Later-stage events remain attributed to the selected entry cohort even if they occur after the selected end date.

Downstream stage timestamps must not be independently restricted to the cohort-entry date range.

Under the default snapshot-as-observed model, downstream membership is established from qualifying rows present in the approved source snapshot according to the governed stage rules. This includes qualifying signup, ride, transaction, and review rows. No additional per-event timestamp cutoff is applied unless a separately approved metric explicitly requires one.

Newer entry cohorts have had less time to reach later stages. Every relevant report must therefore state the cohort-maturity caveat.

### 7.4 Review Timing Limitation

The current reviewed source does not provide a reliable review-event timestamp. Reviewed membership may therefore establish only that a qualifying review record was present in the approved source snapshot. It must not be used to claim that the review occurred before a particular event-time cutoff.

Review time must not be inferred from a drop-off timestamp, transaction timestamp, request timestamp, or another ride timestamp.

### 7.5 Future Event-Time Metrics

No arbitrary conversion window is part of this contract.

An equal-window comparison, event-time “as of” analysis, within-N-days lifecycle measure, or other time-bounded downstream measure requires a separate Data-approved metric and cohort design under Section 15. Such a measure must not silently redefine the default snapshot funnel.

## 8. Platform Attribution

### 8.1 User Funnel

User-funnel platform is taken from:

```text
app_downloads.platform
```

on the `app_downloads` record that supplies the entrant’s `app_download_key`.

It represents the platform recorded for that download entrant.

### 8.2 Ride Funnel

Ride-funnel platform is the signup-linked download platform.

It is the value of:

```text
app_downloads.platform
```

on the app-download record reached through the exact relationship path:

```text
ride_requests.user_id = signups.user_id
signups.session_id = app_downloads.app_download_key
```

It is therefore an attribute of the app-download record linked to the ride through the matching signup record.

It is not:

- a ride-event attribute;
- proof of the device or platform used to request the individual ride;
- permission to infer a platform when the signup or app-download link is missing.

Missing or unexpected platform values must:

- remain visible;
- not be silently discarded;
- not be reassigned to a named platform;
- be included in join and attribution validation.

If one analytical entity reaches multiple conflicting platform values through the approved relationship path:

- the base entity must remain counted once;
- the attribution conflict must be reported;
- segmented platform results must not be published until the conflict is resolved through an approved planning decision.

## 9. Age Attribution

Age segmentation uses only:

```text
signups.age_range
```

No age value may be:

- imputed;
- converted into an exact age;
- inferred from another field;
- assumed to change during the observed period.

### 9.1 `Unknown`

If a matching signup exists and its source `age_range` value is:

```text
Unknown
```

the category must remain:

```text
Unknown
```

This means that a signup exists, but its age range is unknown.

### 9.2 `Not available — no signup`

For a download entrant without a matching signup, the age category must be:

```text
Not available — no signup
```

This means that the entrant never reached the point at which signup age information was available.

The two categories must never be combined:

```text
Unknown
```

is not equivalent to:

```text
Not available — no signup
```

A null, invalid, or unexpected age value on an existing signup must remain explicit and be treated as a data-quality or attribution issue. It must not be silently converted to `Not available — no signup`.

### 9.3 Interpretive Limitation

Age is first observed at signup.

Comparisons among known age groups are therefore not reliable for the:

```text
Downloaded → Signed Up
```

transition because assignment to a known age group already depends on reaching signup.

Age-based funnel analysis is substantively interpretable from Signed Up onward.

### 9.4 Ride-Funnel Age

Ride-funnel age is attributed through:

```text
ride_requests.user_id = signups.user_id
```

A ride without a matching signup must remain in the ride funnel under `LEFT JOIN` protection.

Its age attribution must remain explicitly unavailable and must not be merged with the source `Unknown` category.

## 10. Timestamp and Timezone Limitation

All source timestamps must be treated as source-local naive timestamps.

The source does not establish a timezone. Therefore:

- timestamps must not be converted to UTC;
- timestamps must not be converted to German time or another assumed timezone;
- calendar-date filters operate on values exactly as recorded in the source;
- hour-of-day results must be described as:

```text
source-recorded hour; timezone unavailable
```

- no recorded hour may be attributed to a specific geographic timezone;
- interpretations requiring a known timezone must be reported as unavailable rather than inferred.

## 11. Required Join Keys, Direction, and Preservation

### 11.1 User Funnel

The user funnel must be anchored on `app_downloads`.

The required relationship path is:

```text
app_downloads
LEFT JOIN signups
    ON signups.session_id = app_downloads.app_download_key
LEFT JOIN ride_requests
    ON ride_requests.user_id = signups.user_id
```

This direction preserves:

- downloads without signup;
- signups without ride requests;
- entrants that do not reach later stages.

Later-stage membership must be calculated using existence flags, grain-level pre-aggregation, or equivalent distinct-grain logic.

Multiple signups or ride requests must not multiply an `app_download_key`.

#### 11.1.1 Multiple-Entrant User-Link Ambiguity

Repeated or otherwise duplicate signup rows that preserve the same non-null
(`user_id`, `session_id`) pair do not by themselves satisfy this ambiguity
predicate. They contribute one distinct relationship to this check and remain
separately reportable as source multiplicity.

For a selected User Funnel cohort, a material ambiguity exists only when one
non-null `signups.user_id` is linked through signup rows present in the
approved source snapshot to more than one distinct non-null
`signups.session_id`, and those session IDs match more than one distinct
`app_downloads.app_download_key` in the selected download-entry cohort.

`app_downloads.download_ts` defines User Funnel cohort entry. Signup evidence
comes from the same approved source snapshot identified by the recorded
source-cutoff metadata. A signup session activates this predicate only when it
matches a download entrant inside the selected cohort.

This rule defines a validation predicate. It does not assert that the source
data contains such a relationship.

Any positive predicate result must be detected, retained as diagnostic
evidence, and reported. It must not be resolved by row order, arbitrary first
or last selection, earliest or latest session, collapsing distinct entrant
keys, or automatically assigning one user's downstream ride activity to one
or every linked entrant.

If the predicate returns any user, User Funnel acceptance for the selected
cohort, canonical promotion, and publication must STOP until Data explicitly
approves a contract-level attribution rule. Diagnostic inspection does not
grant acceptance or publication authority.

### 11.2 Ride-Funnel Attribution

The ride funnel must be anchored on `ride_requests`.

The attribution path is:

```text
ride_requests
LEFT JOIN signups
    ON signups.user_id = ride_requests.user_id
LEFT JOIN app_downloads
    ON app_downloads.app_download_key = signups.session_id
```

This direction preserves every Requested ride even when signup, download, platform, or age attribution is missing.

### 11.3 Ride Outcomes

Ride outcomes use:

```text
ride_requests.ride_id = transactions.ride_id
ride_requests.ride_id = reviews.ride_id
```

Transactions and reviews must be reduced to ride-level existence and multiplicity indicators before, or as part of, the final ride-grain calculation.

The implementation must preserve every Requested ride through `LEFT JOIN`, `EXISTS`, or equivalent grain-preserving logic.

Conditions on right-side tables must not be placed in a way that unintentionally converts a preserving join into an inner join.

Missing signup, download, transaction, or review records must affect attribution or stage membership according to this contract. They must not cause the base entrant or ride to disappear.

## 12. Validation Requirements

Before any governed analytical result is accepted, the implementation must demonstrate the following.

### 12.1 Grain Preservation

- User-funnel output contains no more than one analytical record per distinct `app_download_key`.
- Ride-funnel output contains no more than one analytical record per distinct `ride_id`.
- Joined-row multiplication does not alter entrant or ride counts.
- Base-cohort counts remain unchanged after enrichment joins.

### 12.2 Main-Funnel Monotonicity

User-funnel stage populations must satisfy:

```text
Downloaded >= Signed Up >= Requested >= Completed
```

Ride-funnel stage populations must satisfy:

```text
Requested >= Finished >= Paid >= Reviewed
```

Every later-stage identifier set must also be a subset of the preceding-stage identifier set. Count-level monotonicity alone is not sufficient.

Accepted and cancel-after-accept are excluded from the ride-funnel monotonicity sequence because they are secondary diagnostics.

A negative drop-off count is a validation failure.

### 12.3 Formula Validation

Validation must confirm that:

- every stage count uses the declared distinct grain;
- adjacent-stage conversion and drop-off calculations use the formulas in Section 3;
- Percent of Top uses the applicable funnel's top-stage count for the same cohort, segment, and approved source snapshot, sets the top-stage value to `100%` when the top-stage count is nonzero, returns `NULL` and displays as `N/A` for every stage when the top-stage count is zero, allows a later stage to equal `100%` when its count equals the top-stage count, and is not labeled as adjacent-stage conversion;
- segmented numerators and denominators use the same cohort, segment, and approved source snapshot;
- zero denominators return `NULL` and display as `N/A`;
- rounding occurs only after full-precision calculation;
- drop-off rates are not calculated from rounded conversion rates.

### 12.4 Join and Multiplicity Checks

Validation must report:

- unmatched records along the required relationship paths;
- any join cardinality capable of duplicating the declared grain;
- any non-null `signups.user_id` satisfying the multiple-entrant predicate in Section 11.1.1, reported separately from repeated rows preserving the same (`user_id`, `session_id`) relationship;
- duplicate `app_download_key` or `ride_id` source records;
- multiple transaction rows for one `ride_id`;
- multiple Approved transaction rows for one `ride_id`;
- multiple review rows for one `ride_id`;
- missing, unexpected, or conflicting platform attribution;
- missing, unexpected, or invalid age attribution.

These findings must not silently alter stage definitions.

### 12.5 Lifecycle and Outcome-Integrity Checks

Validation must inspect and report:

- the chronological order of available lifecycle timestamps;
- `dropoff_ts` without `pickup_ts`;
- `cancel_ts` together with `pickup_ts`;
- `cancel_ts` together with `dropoff_ts`;
- records with both `accept_ts` and `cancel_ts` where `cancel_ts < accept_ts`;
- other contradictions among available lifecycle timestamps;
- Approved-without-Finished records;
- review-without-Paid records.

Approved-without-Finished means:

```text
at least one linked transaction has charge_status = 'Approved'
AND the ride does not satisfy Finished
```

Such a ride is not Paid under this contract.

Review-without-Paid means:

```text
at least one linked review row exists
AND the ride does not satisfy Paid
```

Such a ride is not Reviewed under this contract.

`cancel_ts` alone must never be treated as proof that pickup did not occur.

Timestamp and outcome anomalies must be surfaced before publication and must not be resolved through an unapproved business assumption.

### 12.6 Cohort and Filter Checks

Validation must confirm that:

- user cohorts are selected only by `download_ts`;
- ride cohorts are selected only by `request_ts`;
- the half-open date boundary is applied correctly;
- downstream outcomes are not removed merely because they occur after the selected end date;
- the approved source snapshot and its source-cutoff provenance metadata are recorded;
- downstream membership uses qualifying rows present in that snapshot without an additional per-event timestamp cutoff;
- Reviewed timing claims comply with the limitation in Section 7.4;
- reporting carries the required cohort-maturity and timezone caveats.

### 12.7 Segment Reconciliation

Segmented outputs must reconcile to the corresponding overall population when all explicit missing, unknown, and unavailable categories are included.

Unmatched or ambiguous attribution must not be hidden by excluding it from segment totals.

### 12.8 Checkpoint Rule

A failed material contract validation is a checkpoint stop.

It is not permission to revise the metric definition inside SQL, Python, or a notebook.

## 13. Canonical Reproducibility and Traceability

The Metric Contract defines business meaning. The executable source of each calculation must also be canonical and reproducible.

Every published metric must be traceable to one or both of the following version-controlled artifacts:

1. **Exact SQL**
   - repository-relative `.sql` file path;
   - named query, CTE, statement, or output;
   - material input parameters;
   - cohort and filter values;
   - approved source snapshot and source-cutoff provenance metadata.

2. **Approved canonical Python implementation**
   - approved artifact form: learner-facing notebook, learner-facing cell-based `.py` analytical document, supporting importable Python module/function, or an approved combination;
   - repository-relative artifact path;
   - durable locator appropriate to the artifact, such as a stable named section, `# %%` analytical section, named output, or importable module/function when applicable;
   - material inputs and parameters;
   - cohort and filter values;
   - approved source snapshot and source-cutoff provenance metadata;
   - validation evidence.

A generic file path, screenshot, copied result table, manual calculation, or display-only result is not canonical evidence. A notebook display is not sufficient by itself, but the executable notebook containing the governed logic may itself be an approved canonical Python implementation.

If both SQL and Python implementations exist for the same result, their outputs at the declared grain and parameters must reconcile.

If multiple canonical paths exist for the same governed result, the reproducibility record must identify their roles and reconcile them where required.

Each reproducibility reference must identify:

- the applicable section of this contract;
- the exact executable artifact;
- the artifact form and durable locator;
- the analytical grain;
- the material inputs and parameters;
- the cohort and filter values;
- the approved source snapshot and source-cutoff provenance metadata;
- the named output or returned object;
- the related validation evidence;
- related Insight Log IDs, where applicable.

Every finding in `docs/ANALYSIS_INSIGHT_LOG.md` must reference the exact SQL and/or approved canonical Python reference that reproduces its evidence.

Every recommendation must identify the `Validated` Insight Log record or records that support it.

Observations, interpretations, and recommendations must remain clearly distinguished.

If a value cannot be reproduced from the documented source, parameters, and canonical executable logic, it must not be presented as an accepted project result.

## 14. Learner-Facing Analytical Document Role and Documentation

The primary learner-facing analytical document combines the real analytical work with its explanation. A learner-facing analytical document may be approved in Jupyter/Colab notebook form or as a cell-based `.py` analytical document using `# %%` sections. `AGENTS.md`, `HOW-WE-WORK.md`, and the authorized analytical task govern which approved artifact serves as the primary learning path.

When the learner-facing document is the approved canonical Python implementation, its material calculations may live directly in that executable artifact. A separate supporting module or function is not required merely to satisfy architecture.

When a learner-facing document is supplementary rather than canonical, it must reuse, execute, clearly reference, or explicitly reconcile to the approved canonical implementation. Any reconciliation must use the same analytical grain, material inputs and parameters, cohort and filter values, and approved source snapshot/cutoff metadata. The supplementary document must not become a second independent implementation or metric authority.

Canonical analytical meaning remains governed by this contract. No learner-facing artifact may redefine it.

Before every significant code cell, `# %%` section, or coherent group of closely related steps, an explanatory learning block appropriate to the artifact must explain, in proportion to the operation’s complexity:

- why the step is needed;
- the business question;
- the analytical grain;
- the applicable stage or formula definition;
- the source tables and exact join keys;
- the cohort-entry filter and approved source snapshot/cutoff metadata;
- the exact SQL and/or approved canonical Python reference being executed or implemented;
- the expected output;
- the required validation or monotonicity condition;
- relevant maturity, attribution, or timezone limitations.

For `.ipynb`, the learning block may be a Markdown cell. For a cell-based `.py` analytical document, it may be a `# %% [markdown]` section or clearly separated teaching block. Import-only, configuration-only, or simple display steps may share a short introductory block.

The learner-facing analytical document must record or expose:

- filter parameters;
- the approved source snapshot and source-cutoff provenance metadata;
- canonical executable references;
- validation outputs;
- related Insight Log IDs where findings are discussed.

The learner-facing analytical document may explain this contract for learning, but it may not redefine it.

Any change to grain, stages, attribution, filtering, formulas, validation treatment, or business meaning still requires explicit planning approval.

## 15. Scope Protection

No additional metric, funnel stage, non-adjacent conversion, observation window, segmentation rule, or business interpretation is approved merely because it can be derived from the available data.

Any such addition requires a separate planning decision and explicit contract amendment.
