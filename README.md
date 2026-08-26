# Metrocar Funnel Analysis — Phase 1

A portfolio rebuild of the Metrocar funnel analysis. This repository is
currently at **Phase 1: data access and structural profiling**. No funnel
metrics, insights, or frontend exist yet.

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

## What Phase 1 does

- `analysis/db.py` — safe, read-only SQLAlchemy 2.x + psycopg 3 connection.
- `analysis/schema.py` — expected tables/columns/keys from the plan.
- `analysis/profile.py` — read-only structural profiling queries.
- `analysis/report.py` — renders the credential-free data-quality report.
- `sql/production/01_structural_profile.sql` — the same checks as readable SQL.
- `docs/data_quality_report.md` — generated profiling output.

## Run

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

## Reading order for students

1. `analysis/schema.py` — what we expect the database to look like.
2. `analysis/db.py` — how we connect safely.
3. `analysis/profile.py` — what we check before trusting the data.
4. `docs/data_quality_report.md` — the findings.
