# Results

## Primary external validation: Rotterdam → GBSG2

| Model | Train C-index | 5-fold CV (train cohort) | External (GBSG2) C-index |
|---|---|---|---|
| Cox PH | 0.667 | 0.663 (±0.012) | **0.654** |
| Elastic-net Cox | 0.670 | 0.669 (selection score) | 0.646 |
| Random survival forest | 0.733 | 0.679 (±0.010) | **0.672** |
| Gradient boosting survival | 0.706 | 0.678 (±0.009) | 0.669 |

Random survival forest achieved the highest external C-index, but with
substantially greater train-to-external performance degradation (0.733 →
0.672, a 0.061 drop) than Cox PH (0.667 → 0.654, a 0.013 drop) — a
4.5-fold difference in apparent overfitting between the two model
classes on identical data and features.

## Independent cross-checks: METABRIC and TCGA-BRCA

| Cohort | Model | Train C-index | CV mean | Holdout/CV C-index |
|---|---|---|---|---|
| METABRIC (N=1,873) | Cox PH | 0.645 | 0.634 (±0.033) | 0.653 (holdout) |
| METABRIC | Random survival forest | 0.709 | 0.633 (±0.016) | 0.666 (holdout) |
| METABRIC | Gradient boosting survival | 0.699 | 0.631 (±0.018) | 0.665 (holdout) |
| TCGA-BRCA (N=799, 74 events) | Cox PH | 0.579 | **0.494 (±0.073)** | — |
| TCGA-BRCA | Random survival forest | 0.730 | **0.531 (±0.069)** | — |
| TCGA-BRCA | Gradient boosting survival | 0.693 | **0.534 (±0.051)** | — |

METABRIC reproduces the qualitative pattern observed in the primary
Rotterdam→GBSG2 experiment. TCGA-BRCA's cross-validated performance is
statistically indistinguishable from chance (0.5) across all three model
classes, despite apparently strong training-set discrimination for the
tree-based models (0.69–0.73) — a within-cohort overfitting signature
attributable to the small usable event count (74) rather than to any
particular model choice.

## Explainability

**Cox PH hazard ratios** (standardized numeric features; categorical
features relative to a reference category), fit on a Rotterdam training
split:

| Feature | Hazard ratio |
|---|---|
| Grade 3 (vs. grade 2) | 1.393 |
| Positive nodes (per 1 SD) | 1.364 |
| Tumor size >50mm (vs. 20–50mm) | 1.297 |
| Post-menopausal (vs. pre) | 1.115 |
| Age (per 1 SD) | 1.032 |
| Estrogen receptor value (per 1 SD) | 1.031 |
| Progesterone receptor value (per 1 SD) | 0.970 |
| Hormone therapy received | 0.880 |
| Tumor size ≤20mm (vs. 20–50mm) | 0.727 |

**Permutation importance** (mean C-index drop on a held-out split when a
feature is shuffled) identified positive lymph node count as the
dominant feature for both Cox PH (0.081) and random survival forest
(0.118), with tumor size and grade as secondary contributors for both
model classes; several features (age, estrogen receptor value,
menopausal status) showed near-zero or negative importance for Cox PH
specifically, indicating limited independent contribution beyond the
dominant features in this model.

## Subgroup robustness (GBSG2 external test set, Cox PH)

| Subgroup | N | Events | C-index |
|---|---|---|---|
| Age <50 | 268 | 106 | 0.644 |
| Age 50–64 | 326 | 157 | 0.648 |
| Age 65+ | 92 | 36 | 0.714 |
| Pre-menopausal | 290 | 119 | 0.647 |
| Post-menopausal | 396 | 180 | 0.658 |
| Grade 1 (absent from training data) | 81 | 18 | 0.660 |
| Grade 2 | 444 | 202 | 0.620 |
| Grade 3 | 161 | 79 | 0.694 |
| No hormone therapy | 440 | 205 | 0.631 |
| Hormone therapy | 246 | 94 | 0.686 |
| **1–3 positive nodes** | 376 | 119 | **0.564** |
| **4+ positive nodes** | 310 | 180 | **0.608** |

All subgroups met the pre-specified minimum sample threshold (N≥30,
≥10 events). Discrimination was lowest in the 1–3-positive-node subgroup
(0.564) — below both the 4+-node subgroup (0.608) and the overall
external C-index (0.654) — identifying a specific population in which
this model's clinical utility is most limited. The grade-1 subgroup,
entirely unseen during model training, showed discrimination (0.660)
comparable to or exceeding the grade-2 subgroup (0.620), despite the
documented absence of that category from training data.
