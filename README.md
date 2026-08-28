# Metrocar Funnel Analysis

Metrocar is a ride-sharing funnel-analysis portfolio project demonstrating:

- reproducible SQL/Pandas analysis;
- governed user and ride funnels;
- validated business insights;
- evidence-backed recommendations; and
- a planned Astro + React + TypeScript + Plotly.js interactive analytical case study.

## Current status

- Phases 1–3 are complete and accepted.
- The Phase 4 visual specification is approved.
- Phase 4 frontend implementation has **not** started.
- This is a portfolio rebuild, not a MasterSchool resubmission.

No frontend, live demo, or Render deployment is claimed by this README.

## Canonical high-level funnels

These accepted full-snapshot counts follow `docs/METRIC_DEFINITION_CONTRACT.md` and the canonical
SQL/Pandas analysis. The two funnels retain their separate governed grains.

### User funnel

```text
Downloaded 23,608
→ Signed Up 17,623
→ Requested 12,406
→ Completed 6,233
```

### Ride funnel

```text
Requested 385,477
→ Finished 223,652
→ Paid 212,628
→ Reviewed 148,464
```

## Setup

1. Create the environment and install dependencies:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure the database credential locally (never commit it):

   ```bash
   cp .env.example .env
   # edit .env and set METROCAR_DATABASE_URL to the PostgreSQL connection URL
   ```

   `.env` is listed in `.gitignore` and must stay out of version control.

## Existing structural-profile command

- `analysis/db.py` — safe, read-only SQLAlchemy 2.x + psycopg 3 connection.
- `analysis/schema.py` — expected tables/columns/keys from the plan.
- `analysis/profile.py` — read-only structural profiling queries.
- `analysis/report.py` — renders the credential-free data-quality report.
- `sql/production/01_structural_profile.sql` — the same checks as readable SQL.
- `docs/data_quality_report.md` — generated profiling output.

## Run existing checks

```bash
# regenerate the data-quality report (requires METROCAR_DATABASE_URL)
# single safe entry point: checks the connection and exits with a
# credential-free message on any failure
python -m analysis.run

# run tests (database tests skip if the credential is not set)
pytest
```

The database connection is enforced read-only at the connection level, and no
error path prints the URL or a chained traceback.

`python -m analysis.run` regenerates the Phase 1 structural data-quality report. It is not a Phase 4
build command. Canonical Phase 2 and Phase 3 logic is available through the modules and production
SQL listed below.

## Current reading order

1. [`AGENTS.md`](AGENTS.md)
2. [`METROCAR_PROJECT_EXECUTION_PLAN.md`](METROCAR_PROJECT_EXECUTION_PLAN.md)
3. [`docs/METRIC_DEFINITION_CONTRACT.md`](docs/METRIC_DEFINITION_CONTRACT.md)
4. [`docs/data_quality_report.md`](docs/data_quality_report.md)
5. [`analysis/funnel.py`](analysis/funnel.py) +
   [`sql/production/02_funnel_analysis.sql`](sql/production/02_funnel_analysis.sql)
6. [`analysis/business_insights.py`](analysis/business_insights.py) +
   [`sql/production/03_business_insights.sql`](sql/production/03_business_insights.sql)
7. [`docs/ANALYSIS_INSIGHT_LOG.md`](docs/ANALYSIS_INSIGHT_LOG.md)
8. [`docs/METROCAR_VISUAL_SPEC.md`](docs/METROCAR_VISUAL_SPEC.md)
