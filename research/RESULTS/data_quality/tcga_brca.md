# Data Quality Report — tcga_brca

**N rows (raw pull):** 1084

## Duplicates
- n_fully_duplicate_rows: 0
- n_duplicate_ids: 0

## Missingness (top 15 worst columns)

| column | n_missing | pct_missing |
|---|---|---|
| WEIGHT | 1084 | 100.0% |
| PRIMARY_LYMPH_NODE_PRESENTATION_ASSESSMENT | 364 | 33.58% |
| NEW_TUMOR_EVENT_AFTER_INITIAL_TREATMENT | 199 | 18.36% |
| ETHNICITY | 169 | 15.59% |
| rfstime | 143 | 13.19% |
| DFS_MONTHS | 143 | 13.19% |
| DFS_STATUS | 142 | 13.1% |
| rfs_event | 142 | 13.1% |
| AJCC_STAGING_EDITION | 140 | 12.92% |
| PERSON_NEOPLASM_CANCER_STATUS | 123 | 11.35% |
| DAYS_LAST_FOLLOWUP | 104 | 9.59% |
| SUBTYPE | 103 | 9.5% |
| RADIATION_THERAPY | 101 | 9.32% |
| RACE | 90 | 8.3% |
| DSS_STATUS | 20 | 1.85% |

## Numeric feature summary (+ IQR outlier flags)

| column | count | mean | std | min | 25% | 50% | 75% | max | extreme_outliers(>3xIQR) |
|---|---|---|---|---|---|---|---|---|---|
| AGE | 1084 | 58.42 | 13.22 | 26.00 | 49.00 | 58.00 | 67.00 | 90.00 | 0 |
| OS_MONTHS | 1084 | 40.83 | 39.36 | 0.00 | 14.72 | 27.01 | 55.00 | 282.90 | 12 |
| DFS_MONTHS | 941 | 37.94 | 36.19 | 0.00 | 14.27 | 24.99 | 50.96 | 281.29 | 11 |
| PFS_MONTHS | 1082 | 37.91 | 35.62 | 0.00 | 14.09 | 25.12 | 51.37 | 281.29 | 8 |

## Categorical feature value counts

**SEX** (cardinality=2):
- Female: 1072
- Male: 12

**AJCC_PATHOLOGIC_TUMOR_STAGE** (cardinality=13):
- STAGE IIA: 355
- STAGE IIB: 255
- STAGE IIIA: 155
- STAGE I: 89
- STAGE IA: 86
- STAGE IIIC: 64
- STAGE IIIB: 28
- STAGE IV: 19
- STAGE X: 14
- STAGE IB: 6
- STAGE II: 6
- nan: 5
- STAGE III: 2

**PATH_M_STAGE** (cardinality=4):
- M0: 895
- MX: 162
- M1: 21
- CM0 (I+): 6

**PATH_N_STAGE** (cardinality=16):
- N0: 329
- N1A: 164
- N0 (I-): 154
- N1: 123
- N2A: 64
- N2: 55
- N3A: 46
- N1MI: 36
- N1B: 32
- N0 (I+): 28
- N3: 26
- NX: 20
- N3B: 3
- N1C: 2
- N3C: 1
- N0 (MOL+): 1

**PATH_T_STAGE** (cardinality=13):
- T2: 626
- T1C: 219
- T3: 136
- T1: 40
- T4B: 27
- T1B: 16
- T4: 9
- TX: 3
- T4D: 3
- T1A: 2
- T2B: 1
- T3A: 1
- T2A: 1

**RACE** (cardinality=5):
- White: 751
- Black or African American: 182
- nan: 90
- Asian: 60
- American Indian or Alaska Native: 1

**RADIATION_THERAPY** (cardinality=3):
- Yes: 549
- No: 434
- nan: 101

**SUBTYPE** (cardinality=6):
- BRCA_LumA: 499
- BRCA_LumB: 197
- BRCA_Basal: 171
- nan: 103
- BRCA_Her2: 78
- BRCA_Normal: 36

## Implausible-value checks
- AGE: 0 implausible rows
- DFS_MONTHS: 0 implausible rows
