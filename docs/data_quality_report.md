# Metrocar Data-Quality Report — Phase 1 Structural Profile

Credential-free structural profile of the source database. No funnel 
metrics, conversion rates, or business insights are computed here.

## 1. Schema vs. plan (Section 6.2)

- Missing tables: none
- Extra tables: none
- `app_downloads`: missing columns none, extra columns none
- `reviews`: missing columns none, extra columns none
- `ride_requests`: missing columns none, extra columns none
- `signups`: missing columns none, extra columns none
- `transactions`: missing columns none, extra columns none

## 2. Columns and data types

### `app_downloads`

| column | data_type | nullable |
|---|---|---|
| app_download_key | text | NO |
| platform | text | YES |
| download_ts | timestamp without time zone | YES |

### `reviews`

| column | data_type | nullable |
|---|---|---|
| review_id | bigint | NO |
| ride_id | bigint | YES |
| user_id | bigint | YES |
| driver_id | bigint | YES |
| rating | bigint | YES |
| review | text | YES |

### `ride_requests`

| column | data_type | nullable |
|---|---|---|
| ride_id | bigint | NO |
| user_id | bigint | YES |
| driver_id | integer | YES |
| request_ts | timestamp without time zone | YES |
| accept_ts | timestamp without time zone | YES |
| pickup_location | text | YES |
| dropoff_location | text | YES |
| pickup_ts | timestamp without time zone | YES |
| dropoff_ts | timestamp without time zone | YES |
| cancel_ts | timestamp without time zone | YES |

### `signups`

| column | data_type | nullable |
|---|---|---|
| user_id | bigint | NO |
| session_id | text | YES |
| signup_ts | timestamp without time zone | YES |
| age_range | text | YES |

### `transactions`

| column | data_type | nullable |
|---|---|---|
| transaction_id | bigint | NO |
| ride_id | bigint | YES |
| purchase_amount_usd | double precision | YES |
| charge_status | text | YES |
| transaction_ts | timestamp without time zone | YES |

## 3. Table profiles

### `app_downloads` — 23608 rows

- Key `app_download_key`: 23608 distinct / 23608 rows (unique: yes), null keys: 0
- Null counts (non-zero only): none
- `platform` values: ios=14290, android=6935, web=2383
- `download_ts` range: 2021-01-01 00:05:59 → 2021-12-31 23:52:27

### `signups` — 17623 rows

- Key `user_id`: 17623 distinct / 17623 rows (unique: yes), null keys: 0
- Null counts (non-zero only): none
- `age_range` values: Unknown=5304, 35-44=5181, 25-34=3447, 18-24=1865, 45-54=1826
- `signup_ts` range: 2021-01-01 05:23:30 → 2022-01-02 15:22:15

### `ride_requests` — 385477 rows

- Key `ride_id`: 385477 distinct / 385477 rows (unique: yes), null keys: 0
- Null counts (non-zero only): {'driver_id': 137098, 'accept_ts': 137098, 'pickup_ts': 161825, 'dropoff_ts': 161825, 'cancel_ts': 223652}
- `request_ts` range: 2021-01-02 08:19:00 → 2022-04-24 18:27:00
- `accept_ts` range: 2021-01-04 09:25:00 → 2022-04-24 18:37:00
- `pickup_ts` range: 2021-01-05 14:25:00 → 2022-04-24 18:50:00
- `dropoff_ts` range: 2021-01-05 15:30:00 → 2022-04-24 20:00:00
- `cancel_ts` range: 2021-01-02 08:37:00 → 2022-03-18 09:28:00

### `transactions` — 223652 rows

- Key `transaction_id`: 223652 distinct / 223652 rows (unique: yes), null keys: 0
- Null counts (non-zero only): none
- `charge_status` values: Approved=212628, Decline=11024
- `transaction_ts` range: 2021-01-05 15:30:00 → 2022-04-24 20:00:00

### `reviews` — 156211 rows

- Key `review_id`: 156211 distinct / 156211 rows (unique: yes), null keys: 0
- Null counts (non-zero only): none
- `rating` values: 1=46458, 4=39571, 5=39252, 3=15659, 2=15271

## 4. Join cardinality and coverage (Section 6.3)

| join | left rows | right rows | joined rows | orphans | multiplies rows |
|---|---|---|---|---|---|
| app_downloads.app_download_key → signups.session_id | 23608 | 17623 | 17623 | 0 | False |
| signups.user_id → ride_requests.user_id | 17623 | 385477 | 385477 | 0 | False |
| ride_requests.ride_id → transactions.ride_id | 385477 | 223652 | 223652 | 0 | False |
| ride_requests.ride_id → reviews.ride_id | 385477 | 156211 | 156211 | 0 | False |

## 5. Ride status and null patterns

- Total ride requests: 385477
- With accept_ts: 248379
- With pickup_ts: 223652
- With dropoff_ts: 223652
- With cancel_ts: 161825

Transactions by status:

| charge_status | transactions | distinct rides |
|---|---|---|
| Approved | 212628 | 212628 |
| Decline | 11024 | 11024 |

Reviews: 156211 total across 156211 distinct rides.

## 6. Ride timestamp order checks

- accept_before_request: 0
- pickup_before_accept: 0
- dropoff_before_pickup: 0
- cancelled_and_dropped_off: 0

## 7. Ride-stage inconsistency checks

Combinations that should be impossible or rare if the stage sequence is clean:

- pickup_without_accept: 0
- dropoff_without_pickup: 0
- dropoff_without_accept: 0
- cancelled_with_accept: 24727
- cancelled_with_pickup: 0
- cancelled_with_dropoff: 0

- approved payment without drop-off: 0
- review without drop-off: 0
- approved payment on cancelled ride: 0

## 8. Transaction and review multiplicity per ride

Transactions per ride:

| transactions | rides |
|---|---|
| 0 | 161825 |
| 1 | 223652 |

Reviews per ride:

| reviews | rides |
|---|---|
| 0 | 229266 |
| 1 | 156211 |

## 9. Date/cohort evidence

- downloads: 2021-01-01 00:05:59 → 2021-12-31 23:52:27
- signups: 2021-01-01 05:23:30 → 2022-01-02 15:22:15
- requests: 2021-01-02 08:19:00 → 2022-04-24 18:27:00
