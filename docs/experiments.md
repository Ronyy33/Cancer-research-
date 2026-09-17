# Experiments

Four experiments were conducted, each documented individually with full
methodological detail in `research/EXPERIMENTS/`. This section summarizes
their design; results are reported in `docs/results.md`.

## Experiment 0001 — Baseline models, Rotterdam → GBSG2 external validation

Cox PH, elastic-net Cox, random survival forest, and gradient boosting
survival models were trained on the full Rotterdam cohort (N=2,982) using
the harmonized eight-feature schema, and evaluated without refitting on
the full GBSG2 cohort (N=686) — a genuine external test the models never
saw during training or hyperparameter selection. During development, a
numerical fault was identified and resolved: un-reduced one-hot encoding
across four categorical feature blocks produced an exactly rank-deficient
design matrix for the Cox model (each encoded block's dummy variables sum
to a constant vector, and with no intercept term to absorb the resulting
redundancy across multiple such blocks, the model's optimizer failed).
This was corrected by dropping one reference category per categorical
variable, and a regression test was added
(`tests/test_harmonize.py::test_onehot_encoding_does_not_crash_coxph`) to
prevent recurrence.

## Experiment 0002 — METABRIC and TCGA-BRCA independent cross-checks

METABRIC (post-exclusion N=1,873) and TCGA-BRCA (N=799) were each
evaluated independently via within-cohort train/test procedures — not as
external validations of the Rotterdam-trained model, since their native
feature sets differ and direct harmonization across all four cohorts was
not attempted. METABRIC used an 80/20 holdout split plus five-fold
cross-validation; TCGA-BRCA, given its small usable event count (74),
used five-fold cross-validation only, without a further holdout split.

## Experiment 0003 — Explainability

Cox PH (fit on a 75/25 Rotterdam train/holdout split, held-out portion
never used for fitting) was analyzed via its native hazard ratios and via
permutation feature importance; the same permutation-importance procedure
was applied to a random survival forest fit on the identical split,
allowing direct, method-matched comparison between the two model classes.

## Experiment 0004 — Subgroup robustness analysis

The Cox PH model fit on the full Rotterdam cohort (as used for external
validation in Experiment 0001) was evaluated for discrimination
separately within six clinically motivated subgroups of the GBSG2 test
set: three age bands, menopausal status (pre/post), histologic grade
(including the grade-1 stratum entirely absent from Rotterdam training
data), hormone therapy receipt, and nodal burden (1–3 vs. ≥4 positive
nodes). A minimum sample threshold (N≥30 patients, ≥10 events) was
applied before reporting any subgroup estimate.
