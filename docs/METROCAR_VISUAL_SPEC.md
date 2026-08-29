# Metrocar Visual and Interaction Specification

**Status:** Approved Phase 4 visual specification; frontend implementation remains separately gated

## 1. Purpose, authority, and boundary

This document defines the approved visual hierarchy, interaction model, project-specific identity,
Plotly presentation principles, responsive behavior, accessibility requirements, and later visual
acceptance criteria for Metrocar Phase 4. It translates the governed analysis into an interactive
recruiter-facing case study without changing the analysis.

The authority order for this specification is:

1. `METROCAR_PROJECT_EXECUTION_PLAN.md` for project scope, phase gates, product requirements, and
   approved deliverables;
2. `docs/METRIC_DEFINITION_CONTRACT.md` for analytical grain, stages, filters, attribution,
   formulas, caveats, and validation;
3. `docs/ANALYSIS_INSIGHT_LOG.md` for validated findings, interpretations, limitations, and
   recommendations;
4. the accepted canonical SQL, Python functions, tests, and source cutoff for executable evidence;
5. Job Pipeline's `docs/portfolio-architecture.md` for the hub-and-spoke and shared-shell model;
6. Job Pipeline's `docs/data-storytelling-and-visualization-philosophy.md` for universal
   storytelling and visual reasoning; and
7. Job Pipeline's `docs/portfolio-visual-identity.md` for the personal portfolio visual family.

If this specification conflicts with the Metric Contract, the Metric Contract governs and
implementation must stop. This document must not redefine an entity, counting grain, funnel stage,
filter, denominator, attribution rule, conversion, finding, or recommendation.

This is an implementation-facing specification, not implementation authority. It does not authorize
frontend scaffolding, dependencies, data regeneration, code changes, publication, deployment,
commit, or push. Historical dashboards, generated visual concepts, and external layout references
are not analytical sources.

## 2. Audience and product model

The primary audience is a recruiter or hiring manager who needs to understand the project's problem,
evidence, analytical judgment, and end-to-end quality quickly. A non-technical stakeholder is an
equally important primary reading mode. A deeper analytical or technical reader is the secondary
audience and should be able to inspect definitions, caveats, production SQL, reproducibility, and
validation without overwhelming the first view.

The approved product model is:

> an interactive analytical case study

It is not a generic admin dashboard. Dashboard components are acceptable when they support the
story, but admin conventions such as permanent CRUD navigation, equal card grids, account controls,
or purposeless filter density must not determine the experience.

The central business question is:

> Where does Metrocar lose users before a successful ride, and what should the company investigate
> or improve next?

The experience should demonstrate data analysis, validation, business reasoning, visualization,
product thinking, and reproducibility as one coherent analytical product. It must feel distinctive
and personal while remaining serious, calm, evidence-led, and understandable.

## 3. Story arc and hierarchy

The single-page analytical story follows this order:

```text
Business question and context
        ↓
Interactive funnel evidence
        ↓
Key observed loss
        ↓
First-ride diagnostic
        ↓
Supporting alternative-explanation evidence
        ↓
Interpretation
        ↓
Recommendation and next experiment
        ↓
Methodology, caveats, and reproducibility
```

This refines, rather than replaces, the execution plan's required single-page structure. The page
should contain:

1. hero and project context;
2. a concise executive takeaway and a small number of key performance indicators;
3. the shared interactive Funnel Explorer;
4. the key observed Requested-to-Completed and Requested-to-Finished loss;
5. the first-ride diagnostic as the narrative climax;
6. supporting platform, age, and request-hour evidence;
7. interpretation and the recommended instrumentation and experiment;
8. the review-without-Paid trust caveat;
9. methodology, data quality, calculation explanations, and production SQL; and
10. repository access and future Back to Portfolio navigation.

Visual weight must match analytical importance. The Funnel Explorer is the dominant analytical
object. The first-ride diagnostic receives the strongest weight after it. Platform, age, and
request-hour results test or narrow alternative explanations and must remain visually quieter. The
review anomaly is material to trust but must not displace the first-ride story.

The progressive-depth model is:

- **Five to ten seconds:** identify Metrocar, the funnel problem, and the principal observed loss.
- **Thirty to ninety seconds:** understand the canonical funnels, first-ride concentration, evidence
  boundary, and proposed next action.
- **Deeper exploration:** compare governed segments, inspect definitions and caveats, and follow the
  reproducibility path to SQL, Python, tests, and GitHub.

## 4. Analytical hero: shared Funnel Explorer

The analytical center is one dominant Funnel Explorer containing two labeled tabs. User Funnel and
Ride Funnel have equal conceptual importance and must not be presented as two unrelated long-form
sections. The selected tab changes the governed analytical grain and stage sequence; the interface
must make that state unmistakable.

### 4.1 User Funnel

The user funnel is entrant-level, using one distinct `app_download_key` as defined by the Metric
Contract. It must not be labeled as a count of uniquely identified physical people.

| Stage | Canonical count |
|---|---:|
| Downloaded | 23,608 |
| Signed Up | 17,623 |
| Requested | 12,406 |
| Completed | 6,233 |

| Adjacent transition | Canonical conversion |
|---|---:|
| Downloaded → Signed Up | 74.65% |
| Signed Up → Requested | 70.40% |
| Requested → Completed | 50.24% |

### 4.2 Ride Funnel

The ride funnel uses one distinct `ride_requests.ride_id` as defined by the Metric Contract.

| Stage | Canonical count |
|---|---:|
| Requested | 385,477 |
| Finished | 223,652 |
| Paid | 212,628 |
| Reviewed | 148,464 |

| Adjacent transition | Canonical conversion |
|---|---:|
| Requested → Finished | 58.02% |
| Finished → Paid | 95.07% |
| Paid → Reviewed | 69.82% |

These full-snapshot values use source cutoff `2022-04-24 20:00:00` with no cohort start or end
filter. Counts remain exact. Published rates use two decimals only in the presentation layer.

No stage may be added, removed, renamed in a way that changes meaning, or requalified for visual
convenience. Accepted and cancel-after-accept remain secondary diagnostics and are not main ride
funnel stages. Review evidence outside the canonical Paid subset must not increase Reviewed.

The funnels should make adjacent loss and conversion easy to read without implying that geometric
area proves a cause. Stage labels, exact values, denominators, and the current label mode must remain
available without relying exclusively on hover. The dominant visual may use related muted green and
teal-green shades, with selective semantic emphasis on the decision-relevant loss. Rainbow stages
are not appropriate.

## 5. Confirmed interaction requirements

The following are confirmed first-version requirements, not optional ideas:

- User Funnel and Ride Funnel tabs in one shared area;
- platform filtering and comparison;
- age-range filtering and comparison;
- date filtering;
- side-by-side comparison of two platforms or two age groups;
- `Absolute` stage counts;
- `Percent of Top`;
- `Percent of Previous`; and
- a clear reset or recovery action.

### 5.1 State and scope

The current funnel, date range, segment dimension, selected segment values, comparison state, and
label mode must be visible or readily understandable. Interaction must never create an unlabeled
scope change. Reset returns the explorer to a documented full-snapshot default rather than leaving
hidden filters active.

Controls must not mix the entrant and ride grains within one comparison. Side-by-side views compare
the same funnel, filters, stage sequence, label mode, and data cutoff. At most two platforms or two
age groups are compared in the confirmed comparison view. Unsupported dimensions must not appear
because a source column or UI control is convenient.

### 5.2 Label modes

`Absolute` shows exact stage counts. `Percent of Top` uses the selected funnel's first-stage count as
the presentation denominator. `Percent of Previous` shows governed adjacent-stage conversion.
Zero-denominator behavior, rounding, and `N/A` presentation follow the Metric Contract. A label-mode
change affects presentation, not membership or grain.

Essential values must remain legible at the stage or in an adjacent accessible summary. Hover may
add detail but cannot be the only place where the current count, rate, scope, or caveat can be found.

### 5.3 Date behavior

Date filtering follows cohort entry as governed by the Metric Contract: download timestamp for the
user funnel and request timestamp for the ride funnel. The user-facing start and end dates are
inclusive; the implementation uses the governed half-open boundary. Later outcomes remain
attributed to the selected entrant or ride cohort even when they occur after the selected end date.

The interface must disclose cohort-maturity risk for newer cohorts and the source-data cutoff. It
must not imply an equal observation window where none is defined.

### 5.4 Platform and age behavior

Platform and age attribution remain exactly as governed. Ride platform is the signup-linked
download platform, not proof of the device used for an individual request. Missing or conflicting
attribution must remain visible according to validation rules.

Age categories must preserve source `Unknown` separately from `Not available — no signup`. Because
known age is first observed at signup, known-age comparison is substantively interpretable from
Signed Up onward, not for Downloaded → Signed Up. The interface must prevent or clearly mark an
invalid known-age interpretation at that transition.

## 6. Key observed loss

The main funnels establish two connected observations:

- entrant Requested → Completed is the lowest-converting canonical user transition: 12,406 to
  6,233, or 50.24%, with 6,173 entrants not reaching Completed; and
- ride Requested → Finished is the corresponding large-volume operational loss: 385,477 to 223,652,
  or 58.02%, with a drop-off of 161,825 rides.

The page should state these as observed losses. It must not jump from the funnel shape to a causal
claim about drivers, waiting, ETA, matching, supply, pricing, or customer motivation. The purpose of
this transition is to motivate the deeper first-ride diagnostic.

## 7. First-ride diagnostic: narrative climax

The first-ride diagnostic covers all 12,406 registered requesting users in the accepted diagnostic
population. Every user has an unambiguous earliest request in the validated snapshot.

| Diagnostic stage | Canonical count |
|---|---:|
| Requested | 12,406 |
| Accepted | 7,205 |
| Picked Up | 6,233 |
| Finished | 6,233 |

There are 6,173 unfinished first rides:

| Failure category | Count | Share of failed first rides |
|---|---:|---:|
| Cancelled without recorded acceptance | 5,201 | 84.25% |
| Qualifying cancellation after acceptance | 972 | 15.75% |

Picked Up → Finished is 100% in the accepted snapshot. No failed first ride was followed by a later
Finished ride in the verified diagnostic population.

This section receives the strongest visual weight after the Funnel Explorer. It should make the
decomposition perceptually immediate: observed first-ride loss is concentrated before pickup and,
especially, before recorded acceptance. A focused stage progression, decomposition bar, or other
proportionate diagnostic may supplement the four-stage view if it keeps the two failure categories
and their common denominator explicit.

Approved language includes:

- observed loss;
- concentrated before recorded acceptance;
- concentrated before pickup;
- current data does not identify the cause; and
- additional instrumentation is required.

The design, annotations, icons, and color must not assert insufficient drivers, long waits, matching
latency, ETA problems, price sensitivity, or surge-pricing failure as facts. Those are hypotheses.
Warm exception color may emphasize the material loss, but the visual must pair it with calibrated
language and the missing-evidence boundary.

## 8. Supporting evidence

Supporting views help the audience test obvious alternative explanations. They are evidence, not a
second set of competing hero stories.

### 8.1 Platform

iOS supplies the largest volume: 14,290 of 23,608 entrants and 234,693 of 385,477 rides in the
accepted snapshot. Platform conversion spreads are modest: the widest user transition spread is
1.76 percentage points, and the ride Requested → Finished spread is 0.87 points.

The visual should use a subdued, honest comparison with shared scales or directly comparable values.
It must not exaggerate small differences through truncated axes, oversized color contrast, or
selective labels. The interpretation is that platform is not the primary observed fulfillment
driver. iOS volume may make it a practical test population, but funnel evidence alone does not
justify permanent marketing-budget allocation because CAC, LTV, retention, spend, and incremental
lift are unavailable.

### 8.2 Age

Among known ages, 35–44 is the strongest current primary-target hypothesis because it combines scale
and above-overall progression. It has 5,181 signups and 114,209 ride requests, with 70.68% Signed Up
→ Requested and 58.54% ride Requested → Finished. Age 18–24 is a possible secondary
high-progression hypothesis, including the strongest known-age Requested → Completed rate at 51.54%
and ride Requested → Finished rate at 59.20%.

The view should distinguish scale from rate and keep `Unknown` and unavailable attribution visible
where governed. It must not imply LTV, profitability, retention, or economically optimal targeting.
Different age groups lead different transitions, so one decorative winner badge would overstate the
evidence.

### 8.3 Request hour

Hours 08–09 and 16–19 contain 82.20% of ride requests. These are source-recorded hours; timezone is
unavailable. The three largest hours do not show materially worse Accepted, Finished, or
cancel-after-accept rates than overall.

Use a time-distribution form that preserves the ordered 24-hour structure and a zero baseline for
magnitude. A restrained annotation may identify the concentration window. The conclusion is that
peak hours offer experiment volume, not proof that peaks cause fulfillment failure or that surge
pricing is required. The unknown timezone must appear with the view or in immediately available
context.

## 9. Data-quality and trust layer

Exactly 7,747 rides have review evidence but do not qualify as Paid. All 7,747 Finished, all have
transaction evidence, and none has an Approved transaction. They represent 4.96% of the 156,211
rides with any review evidence.

This is a process or data anomaly, not an ordinary funnel stage loss. Raw review rows must not be
presented as canonical Reviewed. Canonical Paid → Reviewed remains 148,464 / 212,628 = 69.82%.

The anomaly should be visible in the trust or caveat layer and linked to its calculation explanation.
A compact warning, annotated decomposition, or methodology callout is appropriate. It should not
compete visually with the first-ride diagnostic. Possible review eligibility, payment workflow, or
synchronization explanations remain hypotheses requiring operational evidence.

## 10. Interpretation and recommendation

The resolution must preserve the distinction:

> We know where the loss is concentrated.

is not equivalent to:

> We know why it happens.

The primary evidence-backed next action is to instrument:

- request-to-accept latency;
- nearby or available driver supply;
- quoted ETA;
- cancellation initiator;
- cancellation reason; and
- price at the decision point where available.

Metrocar should then run a controlled first-ride matching or supply experiment. Peak hours may be
useful for sample volume, but current evidence does not prove peak-hour degradation. The
recommendation section should distinguish observed evidence, interpretation, hypotheses, proposed
instrumentation, and the experiment. It must not promise impact unsupported by the observational
dataset.

## 11. Metrocar visual identity

Metrocar uses the personal portfolio family in restrained analytical form. The foundation is
near-black or dark-neutral. Muted green, olive, teal-green, and neutral gray carry ordinary
analytical states and supporting context. Lime and warm exception colors are selective semantic
signals.

### 11.1 Color roles

- **Dark neutral:** page depth and analytical canvas; never so dark that panels and text lose
  separation.
- **Muted green, olive, and teal-green:** normal analytical series, stage relationships, controls,
  and calm structural continuity.
- **Neutral gray:** secondary context, inactive state, methodology, grid lines, and supporting
  evidence.
- **Lime:** rare emphasis for an active tab, selected state, key verified metric, controlled focus,
  or another deliberately prioritized signal.
- **Warm red, coral, or amber:** material loss, failure, risk, anomaly, or critical warning where the
  evidence warrants attention.

Lime must not flood headings, borders, KPIs, and charts. Warm color should attract attention because
it is rare and justified, not because every negative number needs decoration. Neither green nor red
may carry meaning alone; labels, position, annotations, shape, or text must provide a redundant cue.

Funnels should read as one coherent analytical system. Related muted green and teal shades are
preferred to unrelated stage colors. Stronger emphasis belongs on the selected state or
decision-relevant loss, not on every stage. The background remains dark and calm; panels must not
all glow.

### 11.2 Character and composition

The page should feel technical, data-native, modern, serious, and personally distinctive. It may
carry subtle terminal or computational character through typography details, small motifs, or
controlled motion, but the analytical page uses less glow and saturation than the portfolio
homepage. Literal Matrix imagery, falling code, cyberpunk cosplay, and ornamental effects that
compete with data are prohibited.

Composition should be information-rich but calm, with generous but not empty space. Card sizes and
section footprints should follow analytical importance rather than a uniform bento grid. Dark
surface variation, spacing, grouping, and type hierarchy should do most of the structural work.

The generated visual concept may inform general atmosphere—dark analytical surfaces, restrained
green/lime, selective warm loss signals, clear KPIs, prominent funnels, and serious analytical
density—but none of its numbers is evidence. Placeholder values such as the generated first-ride
counts must never enter copy, tests, data, or charts.

### 11.3 Approved Metrocar reference palette

These are Metrocar project-specific reference colors captured from Data's approved VS Code
screenshots. They are screenshot-derived references, not claims about official VS Code theme-token
values. They refine the existing semantic roles in Section 11.1 rather than replace them.

| Role | Reference HEX | Intent |
|---|---|---|
| Preferred primary analytical teal | `#71C6B1` | Data's strongest preference; inspired by the `pandas`, `sqlalchemy`, and `analysis` syntax color; candidate for important analytical accents, active analytical detail, selected structure, or restrained emphasis |
| Fresh secondary green | `#73C991` | Inspired by the active file/tab text; candidate for secondary active/status accents |
| Muted olive green | `#6A9955` | Inspired by explanatory comments; candidate for subdued structural/supporting context where contrast permits |
| Dark neutral reference | `#1F1F1F` | Screenshot-derived dark surface reference; candidate analytical background/surface, not automatically the final page background |

`#71C6B1` is the preferred Metrocar primary analytical teal reference. These colors do not replace
the Job Pipeline shared portfolio visual identity. That identity remains the higher shared visual
family, and the references are intended to help the Metrocar analytical page harmonize with the
future shared Portfolio / Career Hub shell. They should be evaluated together with that shared shell
rather than in isolation, with Metrocar remaining the calmer analytical member of the same visual
family.

The existing semantic roles remain unchanged: muted green, olive, and teal-green carry ordinary
analytical structure; lime provides rare stronger emphasis; warm red, coral, or amber communicate
justified exception, loss, or risk; and neutral gray provides secondary context. Do not use all
available greens simultaneously merely because they are available. Every color must continue to
have a semantic or hierarchical reason.

Each reference remains subject to actual foreground/background WCAG 2.2 AA contrast testing before
final implementation-token assignment. Exact final CSS and design tokens remain implementation-level
decisions after contrast testing, Plotly readability review, and full-page visual review.

## 12. Layout, navigation, and KPI treatment

The simplest approved orientation pattern is a slim sticky in-page navigation bar on wide screens,
positioned within the single-page project experience rather than as a permanent admin sidebar. It
may link to:

- Overview;
- Funnel Explorer;
- First Ride;
- Segments;
- Demand;
- Recommendation; and
- Methodology.

On smaller screens it should collapse into a compact, keyboard-accessible section menu or equivalent
anchor control. It must not introduce admin concepts such as Users, Settings, Billing, or
Authentication. The page remains usable as a linear story without navigation interaction.

The executive area may show no more than a small group of decision-relevant canonical KPIs. Useful
candidates are 23,608 download entrants, 50.24% Requested → Completed entrant conversion, 385,477
ride requests, 58.02% Requested → Finished ride conversion, and 6,173 unfinished first rides. They
must not all receive identical weight merely because they fit a card row. The first screen should
prioritize the problem and strongest observed result over metric inventory.

Every label must respect its definition. `23,608` means download entrants, not verified unique
people. `6,173` refers to unfinished first rides in the validated first-ride population. Context
should remain available without requiring technical knowledge.

## 13. Plotly presentation

Plotly must look native to the surrounding product rather than like an embedded notebook default.
The later implementation should define one shared Plotly theme or configuration layer with:

- transparent or dark-compatible plot and paper backgrounds;
- site-aligned typography and number formatting;
- restrained grid lines and dividers;
- accessible annotation, axis, tick, and legend text;
- the governed semantic color roles;
- readable hover cards that restate the active scope;
- controlled modebar visibility containing only useful actions;
- responsive sizing without clipped labels;
- stable state transitions that do not delay understanding; and
- clean comparison states for two selected platforms or age groups.

Essential values, current scope, main finding, and material caveats cannot exist only in hover.
Modebar tools should support inspection or export when justified; unnecessary controls should be
removed. Animation must not make stage geometry appear to prove a change that is only a state
transition.

Chart forms must follow the relationship. Funnels serve stage loss. Bars may serve categorical
comparison. An ordered bar or line-like distribution may serve source-recorded request hour. A
sentence, KPI, table, or annotated callout is preferable when it communicates a fact more honestly
than another chart. Three-dimensional charts, decorative gauges, rainbow palettes, and misleading
non-zero baselines are not approved.

## 14. Responsive behavior

On desktop, the Funnel Explorer remains visually dominant, controls stay compact, and supporting
evidence can use high analytical density without crowding. Side-by-side segment comparison should
preserve a common visual basis and sufficient annotation space.

On tablet and mobile:

- control groups may wrap or progressively collapse without hiding active state;
- the funnel and exact stage values remain readable;
- comparison views may stack while clearly identifying both selections;
- critical information must not depend on horizontal scrolling;
- the sticky navigation collapses to the approved compact section control;
- touch targets remain usable; and
- long labels, caveats, and calculation disclosures reflow without clipping.

Desktop density must not be preserved by shrinking text, annotations, or controls below readable
sizes. When a comparison stacks, shared scales or direct labels must preserve honest comparison.

## 15. Accessibility

Later implementation must provide:

- accessible contrast for the dark theme, including muted text and chart annotations;
- full keyboard access to tabs, filters, comparison selections, label modes, reset, navigation, and
  progressive disclosure;
- visible focus states that fit the semantic palette;
- labels and redundant encodings independent of color;
- reduced-motion support;
- readable typography and touch-friendly controls;
- meaningful chart descriptions or equivalent accessible summaries;
- a non-hover route to essential counts, rates, takeaways, and caveats; and
- logical reading and focus order when responsive layouts rearrange content.

Interactive charts should have nearby text that states their main purpose and result. An accessible
table or structured summary should expose material values where direct chart navigation cannot
provide an equivalent experience. The dark visual identity is invalid if it reduces legibility or
obscures state.

## 16. Methodology, caveats, and traceability

Technical depth uses progressive disclosure. The main recruiter story stays concise. Important
metrics provide a short `How was this calculated?` explanation and a path to complete production
SQL. The deeper layer records:

- analytical grain and stage meaning;
- current cohort and segment scope;
- source cutoff;
- date-filter and cohort-maturity behavior;
- source-recorded hour and unknown timezone;
- platform and age attribution limitations;
- review-without-Paid evidence;
- production SQL and canonical Python references;
- related Insight Log IDs; and
- validation and repository access.

Canonical reproducibility routes include:

- `analysis.funnel.run_funnel_analysis` in `analysis/funnel.py` and
  `sql/production/02_funnel_analysis.sql` for governed user and ride funnel results;
- `analysis.business_insights.run_business_insights` and
  `analysis.business_insights.first_ride_diagnostic` in `analysis/business_insights.py`, plus the
  named `first_ride_diagnostic` query in `sql/production/03_business_insights.sql`;
- `analysis.business_insights.platform_comparison`, `age_comparison`,
  `request_hour_summary`, and `review_without_paid_decomposition` for supporting evidence; and
- `tests/test_funnel.py` and `tests/test_business_insights.py` for accepted regression expectations.

The primary narrative and recommendation trace to validated records `INS-20260828-001` through
`INS-20260828-006`. Each published finding should link to the specific record and executable source
that supports it rather than cite this visual specification as analytical evidence.

Practice or exploratory SQL remains repository-only and must not be linked as authoritative
methodology. The public browser receives only validated, precomputed, non-sensitive analytical data
and never receives source database credentials or a live database connection.

## 17. Later implementation acceptance criteria

Phase 4 implementation is visually acceptable only when all applicable checks pass:

- only governed canonical counts and calculations are displayed;
- User Funnel and Ride Funnel are available as labeled tabs in one dominant shared explorer;
- platform, age, date, side-by-side comparison, `Absolute`, `Percent of Top`, `Percent of Previous`,
  and reset behavior work without changing grain or definitions;
- active analytical scope is understandable and recoverable;
- age and platform attribution limitations remain intact;
- the first-ride diagnostic is the narrative climax after the funnels;
- the 5,201 and 972 failure decomposition reconciles exactly to 6,173;
- platform, age, and request-hour evidence is present but visually secondary;
- the 7,747 review-without-Paid caveat is visible without reclassifying Reviewed;
- no unsupported causal claim appears in copy, annotation, iconography, or visual implication;
- the instrumentation and controlled-experiment recommendation cites validated evidence;
- the near-black, restrained green/olive/teal, selective lime, and semantic warm-exception identity
  is coherent with the personal portfolio family;
- color use remains restrained, semantic, and accessible;
- Plotly is integrated into the design system and exposes essential information beyond hover;
- desktop, tablet, and mobile layouts remain readable and preserve hierarchy;
- keyboard, focus, contrast, reduced-motion, touch, and accessible-chart requirements pass review;
- the single-page recruiter story is understandable at first-glance, executive, and deep-exploration
  levels;
- methodology, production SQL, Insight Log, data-quality, and GitHub routes are available;
- no generated-mockup placeholder value is treated as evidence;
- no Dash runtime is introduced;
- no public source-database access or secret is introduced; and
- all calculation, visual, interaction, narrative, responsive, accessibility, and security QA
  required by the execution plan is reported honestly as `PASS` or `FAIL`.

## 18. Anti-patterns and open implementation decisions

Reject:

- a generic admin sidebar or CRUD information architecture;
- equal visual weight for every KPI or finding;
- default notebook-like Plotly styling;
- fluorescent lime across the entire interface;
- every card glowing;
- warm exception colors used without analytical meaning;
- rainbow funnel stages;
- hidden active filters or irrecoverable state;
- mixed-grain or differently filtered comparisons;
- essential information available only on hover;
- exaggerated small platform differences;
- known-age claims at Downloaded → Signed Up;
- geographic interpretation of source-recorded hours;
- causal driver, latency, ETA, pricing, or supply claims unsupported by instrumentation;
- raw review counts presented as canonical Reviewed;
- placeholder values from generated visual concepts;
- visual effects that delay or compete with evidence; and
- copying, cloning, or installing a reference template without separate approval.

The following implementation-level decisions remain open:

- exact analytical-page HEX tokens and derived chart colors;
- typography families and final type scale;
- spacing, radius, border, shadow, and restrained-glow values;
- component library or decision to use project-native components;
- exact chart geometry, annotation placement, and hover-card design;
- exact breakpoint values and compact mobile comparison control;
- exact sticky-navigation height and scroll-state behavior;
- exact useful Plotly modebar actions;
- static fallback or social-preview treatment; and
- final motion values and transitions.

Those choices require a separately authorized implementation task, evidence from the actual layout,
accessibility testing, and later visual QA. They must remain within this specification rather than
reopening analytical semantics.
