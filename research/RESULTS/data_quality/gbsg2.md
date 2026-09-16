# Data Quality Report — gbsg2

**N rows (raw pull):** 686

## Duplicates
- n_fully_duplicate_rows: 0

## Missingness (top 15 worst columns)

| column | n_missing | pct_missing |
|---|---|---|
| age | 0 | 0.0% |
| estrec | 0 | 0.0% |
| horTh | 0 | 0.0% |
| menostat | 0 | 0.0% |
| pnodes | 0 | 0.0% |
| progrec | 0 | 0.0% |
| tgrade | 0 | 0.0% |
| tsize | 0 | 0.0% |
| rfstime | 0 | 0.0% |
| rfs_event | 0 | 0.0% |

## Numeric feature summary (+ IQR outlier flags)

| column | count | mean | std | min | 25% | 50% | 75% | max | extreme_outliers(>3xIQR) |
|---|---|---|---|---|---|---|---|---|---|
| age | 686 | 53.05 | 10.12 | 21.00 | 46.00 | 53.00 | 61.00 | 80.00 | 0 |
| estrec | 686 | 96.25 | 153.08 | 0.00 | 8.00 | 36.00 | 114.00 | 1144.00 | 28 |
| pnodes | 686 | 5.01 | 5.48 | 1.00 | 1.00 | 3.00 | 7.00 | 51.00 | 7 |
| progrec | 686 | 110.00 | 202.33 | 0.00 | 7.00 | 32.50 | 131.75 | 2380.00 | 23 |
| tsize | 686 | 29.33 | 14.30 | 3.00 | 20.00 | 25.00 | 35.00 | 120.00 | 4 |

## Categorical feature value counts

**horTh** (cardinality=2):
- no: 440
- yes: 246

**menostat** (cardinality=2):
- Post: 396
- Pre: 290

**tgrade** (cardinality=3):
- II: 444
- III: 161
- I: 81

## Implausible-value checks
- age: 0 implausible rows
- pnodes: 0 implausible rows
- estrec: 0 implausible rows
- progrec: 0 implausible rows
- tsize: 0 implausible rows
- rfstime: 0 implausible rows
