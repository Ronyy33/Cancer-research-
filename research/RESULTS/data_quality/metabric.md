# Data Quality Report — metabric

**N rows (raw pull):** 2509

## Duplicates
- n_fully_duplicate_rows: 0
- n_duplicate_ids: 0

## Missingness (top 15 worst columns)

| column | n_missing | pct_missing |
|---|---|---|
| THREEGENE | 745 | 29.69% |
| LATERALITY | 639 | 25.47% |
| CELLULARITY | 592 | 23.6% |
| BREAST_SURGERY | 554 | 22.08% |
| INFERRED_MENOPAUSAL_STATE | 529 | 21.08% |
| CLAUDIN_SUBTYPE | 529 | 21.08% |
| INTCLUST | 529 | 21.08% |
| HER2_SNP6 | 529 | 21.08% |
| HORMONE_THERAPY | 529 | 21.08% |
| CHEMOTHERAPY | 529 | 21.08% |
| VITAL_STATUS | 529 | 21.08% |
| RADIO_THERAPY | 529 | 21.08% |
| OS_STATUS | 528 | 21.04% |
| OS_MONTHS | 528 | 21.04% |
| LYMPH_NODES_EXAMINED_POSITIVE | 266 | 10.6% |

## Numeric feature summary (+ IQR outlier flags)

| column | count | mean | std | min | 25% | 50% | 75% | max | extreme_outliers(>3xIQR) |
|---|---|---|---|---|---|---|---|---|---|
| LYMPH_NODES_EXAMINED_POSITIVE | 2243 | 1.95 | 4.02 | 0.00 | 0.00 | 0.00 | 2.00 | 45.00 | 137 |
| NPI | 2287 | 4.03 | 1.19 | 1.00 | 3.05 | 4.04 | 5.04 | 7.20 | 0 |
| AGE_AT_DIAGNOSIS | 2498 | 60.42 | 13.03 | 21.93 | 50.92 | 61.11 | 70.00 | 96.29 | 0 |
| OS_MONTHS | 1981 | 125.24 | 76.11 | 0.00 | 60.87 | 116.47 | 185.13 | 355.20 | 0 |
| RFS_MONTHS | 2388 | 110.29 | 77.54 | 0.00 | 41.10 | 100.42 | 169.87 | 389.33 | 0 |

## Categorical feature value counts

**CELLULARITY** (cardinality=4):
- High: 965
- Moderate: 737
- nan: 592
- Low: 215

**CHEMOTHERAPY** (cardinality=3):
- NO: 1568
- nan: 529
- YES: 412

**ER_IHC** (cardinality=3):
- Positve: 1817
- Negative: 609
- nan: 83

**HER2_SNP6** (cardinality=5):
- NEUTRAL: 1436
- nan: 529
- GAIN: 438
- LOSS: 101
- UNDEF: 5

**HORMONE_THERAPY** (cardinality=3):
- YES: 1216
- NO: 764
- nan: 529

**INFERRED_MENOPAUSAL_STATE** (cardinality=3):
- Post: 1556
- nan: 529
- Pre: 424

**CLAUDIN_SUBTYPE** (cardinality=8):
- LumA: 700
- nan: 529
- LumB: 475
- Her2: 224
- claudin-low: 218
- Basal: 209
- Normal: 148
- NC: 6

**RADIO_THERAPY** (cardinality=3):
- YES: 1173
- NO: 807
- nan: 529

**HISTOLOGICAL_SUBTYPE** (cardinality=9):
- Ductal/NST: 1810
- Mixed: 269
- Lobular: 192
- nan: 135
- Medullary: 32
- Mucinous: 25
- Tubular/ cribriform: 23
- Other: 21
- Metaplastic: 2

**BREAST_SURGERY** (cardinality=3):
- MASTECTOMY: 1170
- BREAST CONSERVING: 785
- nan: 554

## Implausible-value checks
- AGE_AT_DIAGNOSIS: 0 implausible rows
- LYMPH_NODES_EXAMINED_POSITIVE: 0 implausible rows
- RFS_MONTHS: 0 implausible rows
