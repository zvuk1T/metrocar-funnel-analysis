"""Expected Metrocar schema, reconciled with the live database (Phase 1).

This is the single source of truth for what Phase 1 validates against. The
profiler compares the live database to these expectations and reports any
mismatch instead of failing silently.

Reconciliation note: the live database is authoritative. Column names and
status values below reflect the verified live schema, which differs from the
original plan (Section 6.2) in three ways:
  - ride_requests uses ``dropoff_location`` (plan said ``destination_location``)
  - reviews uses ``review`` (plan said ``free_response``)
  - transactions has an extra candidate key ``transaction_id``
  - transactions.charge_status values are exactly ``Approved`` / ``Decline``
All timestamps are source-local ``timestamp without time zone`` (timezone
unknown).
"""

# Expected columns per table, matching the verified live schema.
EXPECTED_TABLES: dict[str, list[str]] = {
    "app_downloads": ["app_download_key", "platform", "download_ts"],
    "signups": ["user_id", "session_id", "signup_ts", "age_range"],
    "ride_requests": [
        "ride_id",
        "user_id",
        "driver_id",
        "request_ts",
        "accept_ts",
        "pickup_location",
        "dropoff_location",
        "pickup_ts",
        "dropoff_ts",
        "cancel_ts",
    ],
    "transactions": [
        "transaction_id",
        "ride_id",
        "purchase_amount_usd",
        "charge_status",
        "transaction_ts",
    ],
    "reviews": ["review_id", "ride_id", "driver_id", "user_id", "rating", "review"],
}

# Columns that must be unique and non-null (candidate primary keys).
UNIQUE_KEYS: dict[str, str] = {
    "app_downloads": "app_download_key",
    "signups": "user_id",
    "ride_requests": "ride_id",
    "transactions": "transaction_id",
    "reviews": "review_id",
}

# Exact charge_status values present in the live database.
CHARGE_STATUSES: tuple[str, str] = ("Approved", "Decline")

# Provisional relationships from Section 6.3 to validate.
# Each entry: (left_table, left_key, right_table, right_key, description).
PROVISIONAL_JOINS: list[tuple[str, str, str, str, str]] = [
    ("app_downloads", "app_download_key", "signups", "session_id",
     "each signup links to one app download"),
    ("signups", "user_id", "ride_requests", "user_id",
     "each ride request links to one signed-up user"),
    ("ride_requests", "ride_id", "transactions", "ride_id",
     "each transaction links to one ride"),
    ("ride_requests", "ride_id", "reviews", "ride_id",
     "each review links to one ride"),
]
