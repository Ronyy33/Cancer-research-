# Data Quality Report — rotterdam

**N rows (raw pull):** 2982

## Duplicates
- n_fully_duplicate_rows: 0
- n_duplicate_ids: 0

## Missingness (top 15 worst columns)

| column | n_missing | pct_missing |
|---|---|---|
| pid | 0 | 0.0% |
| year | 0 | 0.0% |
| age | 0 | 0.0% |
| meno | 0 | 0.0% |
| size | 0 | 0.0% |
| grade | 0 | 0.0% |
| nodes | 0 | 0.0% |
| pgr | 0 | 0.0% |
| er | 0 | 0.0% |
| hormon | 0 | 0.0% |
| chemo | 0 | 0.0% |
| rtime | 0 | 0.0% |
| recur | 0 | 0.0% |
| dtime | 0 | 0.0% |
| death | 0 | 0.0% |

## Numeric feature summary (+ IQR outlier flags)

| column | count | mean | std | min | 25% | 50% | 75% | max | extreme_outliers(>3xIQR) |
|---|---|---|---|---|---|---|---|---|---|
| age | 2982 | 55.06 | 12.95 | 24.00 | 45.00 | 54.00 | 65.00 | 90.00 | 0 |
| nodes | 2982 | 2.71 | 4.38 | 0.00 | 0.00 | 1.00 | 4.00 | 34.00 | 53 |
| pgr | 2982 | 161.83 | 291.31 | 0.00 | 4.00 | 41.00 | 198.00 | 5004.00 | 118 |
| er | 2982 | 166.59 | 272.47 | 0.00 | 11.00 | 61.00 | 202.75 | 3275.00 | 107 |
| year | 2982 | 1988.16 | 3.04 | 1978.00 | 1986.00 | 1988.00 | 1990.00 | 1993.00 | 0 |

## Categorical feature value counts

**meno** (cardinality=2):
- 1: 1670
- 0: 1312

**size** (cardinality=3):
- <=20: 1387
- 20-50: 1291
- >50: 304

**grade** (cardinality=2):
- 3: 2188
- 2: 794

**hormon** (cardinality=2):
- 0: 2643
- 1: 339

**chemo** (cardinality=2):
- 0: 2402
- 1: 580

## Implausible-value checks
- age: 0 implausible rows
- nodes: 0 implausible rows
- pgr: 0 implausible rows
- er: 0 implausible rows
- rfstime: 0 implausible rows
