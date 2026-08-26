-- Phase 1 structural profile of the Metrocar database (compact manual subset).
--
-- Business purpose: document the actual shape of the data (tables, keys,
-- nulls, categories, timestamp ranges, join cardinality, stage consistency)
-- before any metric is defined. Read-only.
--
-- Scope note: this is a deliberately compact, hand-runnable subset of the
-- canonical Python profiler in analysis/profile.py. It covers the same core
-- checks but not every derived section; when the two disagree,
-- analysis/profile.py is authoritative. Output grain: one summary block per
-- check.

-- 1. Columns and data types for the five expected tables.
SELECT table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('app_downloads', 'signups', 'ride_requests', 'transactions', 'reviews')
ORDER BY table_name, ordinal_position;

-- 1b. All public tables (so extra tables can be reported).
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- 2. Row counts and candidate-key uniqueness.
SELECT 'app_downloads' AS table_name, COUNT(*) AS rows,
       COUNT(DISTINCT app_download_key) AS distinct_keys,
       COUNT(*) FILTER (WHERE app_download_key IS NULL) AS null_keys
FROM app_downloads
UNION ALL
SELECT 'signups', COUNT(*), COUNT(DISTINCT user_id),
       COUNT(*) FILTER (WHERE user_id IS NULL)
FROM signups
UNION ALL
SELECT 'ride_requests', COUNT(*), COUNT(DISTINCT ride_id),
       COUNT(*) FILTER (WHERE ride_id IS NULL)
FROM ride_requests
UNION ALL
SELECT 'reviews', COUNT(*), COUNT(DISTINCT review_id),
       COUNT(*) FILTER (WHERE review_id IS NULL)
FROM reviews;

-- 3. Null counts on ride_requests outcome timestamps (defines ride stages).
SELECT
  COUNT(*) AS total_requests,
  COUNT(*) FILTER (WHERE accept_ts IS NOT NULL) AS with_accept,
  COUNT(*) FILTER (WHERE pickup_ts IS NOT NULL) AS with_pickup,
  COUNT(*) FILTER (WHERE dropoff_ts IS NOT NULL) AS with_dropoff,
  COUNT(*) FILTER (WHERE cancel_ts IS NOT NULL) AS with_cancel
FROM ride_requests;

-- 4. Categorical values.
SELECT 'platform' AS column_name, platform AS value, COUNT(*) AS n
FROM app_downloads GROUP BY platform
UNION ALL
SELECT 'age_range', age_range, COUNT(*) FROM signups GROUP BY age_range
UNION ALL
SELECT 'charge_status', charge_status, COUNT(*) FROM transactions GROUP BY charge_status
ORDER BY column_name, n DESC;

-- 5. Timestamp ranges (evidence for date/cohort rules).
SELECT 'download_ts' AS column_name, MIN(download_ts) AS min_ts, MAX(download_ts) AS max_ts
FROM app_downloads
UNION ALL
SELECT 'signup_ts', MIN(signup_ts), MAX(signup_ts) FROM signups
UNION ALL
SELECT 'request_ts', MIN(request_ts), MAX(request_ts) FROM ride_requests
UNION ALL
SELECT 'transaction_ts', MIN(transaction_ts), MAX(transaction_ts) FROM transactions;

-- 6. Join cardinality: does each join multiply rows?
--    joined_rows > right_rows signals a fan-out that would inflate metrics.
SELECT
  (SELECT COUNT(*) FROM signups) AS right_rows,
  (SELECT COUNT(*) FROM signups s
     LEFT JOIN app_downloads a ON a.app_download_key = s.session_id) AS joined_rows_signups_to_downloads,
  (SELECT COUNT(*) FROM ride_requests) AS ride_rows,
  (SELECT COUNT(*) FROM ride_requests r
     LEFT JOIN signups s ON s.user_id = r.user_id) AS joined_rows_rides_to_signups;

-- 7. Transaction and review multiplicity per ride (fan-out risk).
SELECT tx_count, COUNT(*) AS rides
FROM (
  SELECT r.ride_id, COUNT(t.ride_id) AS tx_count
  FROM ride_requests r
  LEFT JOIN transactions t ON t.ride_id = r.ride_id
  GROUP BY r.ride_id
) s
GROUP BY tx_count
ORDER BY tx_count;

SELECT review_count, COUNT(*) AS rides
FROM (
  SELECT r.ride_id, COUNT(rv.review_id) AS review_count
  FROM ride_requests r
  LEFT JOIN reviews rv ON rv.ride_id = r.ride_id
  GROUP BY r.ride_id
) s
GROUP BY review_count
ORDER BY review_count;

-- 7b. Ride-stage inconsistency checks (should be ~0 in a clean sequence).
SELECT
  COUNT(*) FILTER (WHERE pickup_ts IS NOT NULL AND accept_ts IS NULL) AS pickup_without_accept,
  COUNT(*) FILTER (WHERE dropoff_ts IS NOT NULL AND pickup_ts IS NULL) AS dropoff_without_pickup,
  COUNT(*) FILTER (WHERE dropoff_ts IS NOT NULL AND accept_ts IS NULL) AS dropoff_without_accept,
  COUNT(*) FILTER (WHERE cancel_ts IS NOT NULL AND accept_ts IS NOT NULL) AS cancelled_with_accept,
  COUNT(*) FILTER (WHERE cancel_ts IS NOT NULL AND pickup_ts IS NOT NULL) AS cancelled_with_pickup,
  COUNT(*) FILTER (WHERE cancel_ts IS NOT NULL AND dropoff_ts IS NOT NULL) AS cancelled_with_dropoff
FROM ride_requests;

-- 7c. Approved payment / review attached to an incomplete ride.
SELECT
  (SELECT COUNT(*) FROM transactions t
     JOIN ride_requests r ON r.ride_id = t.ride_id
    WHERE t.charge_status = 'approved' AND r.dropoff_ts IS NULL) AS approved_payment_without_dropoff,
  (SELECT COUNT(*) FROM reviews rv
     JOIN ride_requests r ON r.ride_id = rv.ride_id
    WHERE r.dropoff_ts IS NULL) AS review_without_dropoff;
