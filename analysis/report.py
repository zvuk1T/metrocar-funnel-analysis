"""Write the Phase 1 data-quality report as Markdown.

This turns the raw profiling dicts from ``analysis.profile`` into a readable,
credential-free report under ``docs/``. It only formats numbers that are
already computed; it does not run new queries or derive funnel metrics.
"""

from __future__ import annotations

from pathlib import Path

from sqlalchemy.engine import Engine

from analysis import profile


def _fmt_ts(value) -> str:
    return "—" if value is None else str(value)


def render_report(results: dict) -> str:
    """Render the full profiling results as a Markdown string."""
    lines: list[str] = []
    add = lines.append

    add("# Metrocar Data-Quality Report — Phase 1 Structural Profile")
    add("")
    add("Credential-free structural profile of the source database. No funnel ")
    add("metrics, conversion rates, or business insights are computed here.")
    add("")

    # Schema comparison
    sc = results["schema_comparison"]
    add("## 1. Schema vs. plan (Section 6.2)")
    add("")
    problems = results.get("schema_problems") or []
    if problems:
        add("**Schema mismatches detected — profiling continued with partial data:**")
        add("")
        for p in problems:
            add(f"- {p}")
        add("")
    add(f"- Missing tables: {sc['missing_tables'] or 'none'}")
    add(f"- Extra tables: {sc['extra_tables'] or 'none'}")
    for table, cols in sc["columns"].items():
        add(f"- `{table}`: missing columns {cols['missing_columns'] or 'none'}, "
            f"extra columns {cols['extra_columns'] or 'none'}")
    add("")

    # Column detail
    add("## 2. Columns and data types")
    add("")
    for table, cols in results["columns"].items():
        add(f"### `{table}`")
        add("")
        add("| column | data_type | nullable |")
        add("|---|---|---|")
        for c in cols:
            add(f"| {c['column']} | {c['data_type']} | {c['is_nullable']} |")
        add("")

    # Table profiles
    add("## 3. Table profiles")
    add("")
    for table, p in results["tables"].items():
        if "error" in p:
            add(f"### `{table}` — {p['error']}")
            add("")
            continue
        add(f"### `{table}` — {p['row_count']} rows")
        add("")
        if p.get("skipped_columns"):
            add(f"- Skipped columns (not present): {p['skipped_columns']}")
        if p["key_stats"]:
            ks = p["key_stats"]
            unique = "yes" if ks["rows"] == ks["distinct_keys"] else "NO"
            add(f"- Key `{p['key']}`: {ks['distinct_keys']} distinct / "
                f"{ks['rows']} rows (unique: {unique}), null keys: {ks['null_keys']}")
        nulls = {k: v for k, v in p["null_counts"].items() if v}
        add(f"- Null counts (non-zero only): {nulls or 'none'}")
        for col, vals in p["categorical"].items():
            rendered = ", ".join(f"{v['value']}={v['n']}" for v in vals)
            add(f"- `{col}` values: {rendered}")
        for col, ts in p["timestamps"].items():
            add(f"- `{col}` range: {_fmt_ts(ts['min_ts'])} → {_fmt_ts(ts['max_ts'])}")
        add("")

    # Joins
    add("## 4. Join cardinality and coverage (Section 6.3)")
    add("")
    add("| join | left rows | right rows | joined rows | orphans | multiplies rows |")
    add("|---|---|---|---|---|---|")
    for j in results["joins"]:
        if "skipped" in j:
            add(f"| {j['left']}.{j['left_key']} → {j['right']}.{j['right_key']} "
                f"| — | — | — | — | {j['skipped']} |")
            continue
        add(f"| {j['left']}.{j['left_key']} → {j['right']}.{j['right_key']} "
            f"| {j['left_rows']} | {j['right_rows']} | {j['joined_rows']} "
            f"| {j['orphan_right_rows']} | {j['multiplies_rows']} |")
    add("")

    # Ride status patterns
    add("## 5. Ride status and null patterns")
    add("")
    rs = results["ride_status"]
    if "skipped" in rs:
        add(f"- {rs['skipped']}")
        add("")
    else:
        rf = rs["ride_flags"]
        add(f"- Total ride requests: {rf['total_requests']}")
        add(f"- With accept_ts: {rf['with_accept']}")
        add(f"- With pickup_ts: {rf['with_pickup']}")
        add(f"- With dropoff_ts: {rf['with_dropoff']}")
        add(f"- With cancel_ts: {rf['with_cancel']}")
        add("")
        add("Transactions by status:")
        add("")
        add("| charge_status | transactions | distinct rides |")
        add("|---|---|---|")
        for row in rs["transactions_by_status"]:
            add(f"| {row['charge_status']} | {row['transactions']} | {row['distinct_rides']} |")
        add("")
        rv = rs["reviews"]
        add(f"Reviews: {rv['total_reviews']} total across "
            f"{rv['distinct_rides_reviewed']} distinct rides.")
        add("")

    # Timestamp order
    add("## 6. Ride timestamp order checks")
    add("")
    rto = results["ride_timestamp_order"]
    if "skipped" in rto:
        add(f"- {rto['skipped']}")
    else:
        for key, value in rto.items():
            add(f"- {key}: {value}")
    add("")

    # Ride-stage inconsistencies
    add("## 7. Ride-stage inconsistency checks")
    add("")
    rsi = results["ride_stage_inconsistencies"]
    if "skipped" in rsi:
        add(f"- {rsi['skipped']}")
    else:
        add("Combinations that should be impossible or rare if the stage sequence is clean:")
        add("")
        for key, value in rsi.items():
            add(f"- {key}: {value}")
        add("")
        pwc = results["paid_without_completion"]
        if "skipped" in pwc:
            add(f"- {pwc['skipped']}")
        else:
            add(f"- approved payment without drop-off: {pwc['approved_payment_without_dropoff']}")
            add(f"- review without drop-off: {pwc['review_without_dropoff']}")
            add(f"- approved payment on cancelled ride: {pwc['approved_payment_on_cancelled_ride']}")
    add("")

    # Multiplicity
    add("## 8. Transaction and review multiplicity per ride")
    add("")
    tm = results["transaction_multiplicity"]
    add("Transactions per ride:")
    add("")
    if isinstance(tm, dict) and "skipped" in tm:
        add(f"- {tm['skipped']}")
        add("")
    else:
        add("| transactions | rides |")
        add("|---|---|")
        for row in tm:
            add(f"| {row['tx_count']} | {row['rides']} |")
        add("")
    rm = results["review_multiplicity"]
    add("Reviews per ride:")
    add("")
    if isinstance(rm, dict) and "skipped" in rm:
        add(f"- {rm['skipped']}")
        add("")
    else:
        add("| reviews | rides |")
        add("|---|---|")
        for row in rm:
            add(f"| {row['review_count']} | {row['rides']} |")
        add("")

    # Date ranges
    add("## 9. Date/cohort evidence")
    add("")
    dr = results["date_ranges"]
    if "skipped" in dr:
        add(f"- {dr['skipped']}")
    else:
        for name, ts in dr.items():
            add(f"- {name}: {_fmt_ts(ts['min_ts'])} → {_fmt_ts(ts['max_ts'])}")
    add("")

    return "\n".join(lines)


def write_report(engine: Engine, output_path: str | Path) -> Path:
    """Run the profile and write the Markdown report to ``output_path``."""
    results = profile.run_profile(engine)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_report(results), encoding="utf-8")
    return path
