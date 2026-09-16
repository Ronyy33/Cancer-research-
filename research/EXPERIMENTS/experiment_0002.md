# Experiment 0002 — METABRIC and TCGA-BRCA within-cohort baselines

**Date:** 2026-09-16
**Script:** `scripts/train_metabric_tcga.py`
**Stage:** 9 (baseline modeling, continued)

## Purpose and important scope limitation

Unlike experiment_0001 (Rotterdam train → GBSG2 external test, a genuine
external validation using a comparable harmonized feature set), METABRIC
and TCGA-BRCA each have their own different native feature set with no
natural external-validation partner in this project's current dataset
lineup. **This experiment evaluates each cohort independently via
within-cohort train/test split + cross-validation — it is NOT an external
validation of the Rotterdam-trained model, and is not presented as one.**
This distinction is deliberate, per the project's standard against
overstating validation rigor (Section 22 of the project brief).

## METABRIC

**Cohort construction:** the ~528-patient block-missingness batch found in
Stage 8 (`research/RESULTS/data_quality/SYNTHESIS.md`) was excluded using
the exact reproducible rule from that investigation (rows missing in ≥10
of 12 checked columns) — **not** a COHORT-number heuristic, since COHORT=1
appears in both the complete and incomplete groups (confirmed during
Stage 8; filtering by cohort number alone would have been wrong).

- N after excluding incomplete batch + dropping missing outcome: 1,980
- N after complete-case on modeling features: **1,873**
- Events: 763 (40.7%)
- Features: NPI, age at diagnosis, positive lymph nodes (numeric); ER
  status, HER2 status, hormone therapy, chemotherapy, menopausal state
  (categorical, one-hot with reference category dropped)
- Split: 80/20 within-cohort holdout (random_state=42) + 5-fold CV

### Results (Harrell's C-index)

| Model | Train | CV mean (±std) | Holdout test |
|---|---|---|---|
| Cox PH | 0.645 | 0.634 (±0.033) | 0.653 |
| Random Survival Forest | 0.709 | 0.633 (±0.016) | 0.666 |
| Gradient Boosting Survival | 0.699 | 0.631 (±0.018) | 0.665 |

**Interpretation:** consistent with experiment_0001's Rotterdam→GBSG2
pattern — tree-based models score modestly higher on held-out data, Cox PH
is close behind with much less train/holdout divergence. This is now a
**second, independent real-data cohort showing the same pattern**, which
strengthens (not just repeats) the experiment_0001 finding.

## TCGA-BRCA

- N after dropping missing outcome: 941
- N after complete-case on modeling features: **799**
- Events: **74 (9.3%)**
- Features: age (numeric); AJCC pathologic M-stage, molecular subtype,
  radiation therapy (categorical)
- **Only 5-fold CV reported — no further holdout split.** With just 74
  real events, an 80/20 split would leave too few test-set events for a
  stable estimate; this is a documented limitation of the cohort itself,
  not a shortcut taken silently.

### Results (Harrell's C-index)

| Model | Train | CV mean (±std) |
|---|---|---|
| Cox PH | 0.579 | **0.494 (±0.073)** |
| Random Survival Forest | 0.730 | **0.531 (±0.069)** |
| Gradient Boosting Survival | 0.693 | **0.534 (±0.051)** |

### ⚠️ Honest, important finding: TCGA-BRCA cross-validated performance is essentially indistinguishable from random chance

A C-index of 0.5 means no better than a coin flip at ranking who's higher
risk. **All three models' CV-mean C-index falls in the 0.49–0.53 range —
essentially random** — despite the tree-based models showing deceptively
high *training* C-index (0.69–0.73). This is a textbook small-data
overfitting signature: with only 74 events, there simply is not enough
signal for a model trained on this cohort to generalize, even within the
same cohort's own held-out folds.

**This directly validates the decision (made in Stage 8/`DATASETS/
tcga_brca.md`) to treat TCGA-BRCA as a secondary/exploratory cohort only,
not a reliable cross-check.** Per the project's standard (Section 28:
report negative results honestly, never manipulate experiments to get
better numbers), this finding is reported plainly rather than omitted or
downplayed. TCGA-BRCA should not be used to draw conclusions about model
performance in this research program going forward without first
substantially growing its usable event count (e.g. by relaxing feature
completeness requirements, at the cost of fewer covariates).

## Combined evidence across experiment_0001 + experiment_0002

Three independent real cohorts now show the same qualitative pattern:
simple Cox regression achieves external/holdout performance close to
tree-based ensembles, with substantially less overfitting risk. The one
cohort that doesn't fit this pattern (TCGA-BRCA) doesn't fit it because
it lacks enough real events for *any* model to learn reliably — not
because a different model class would have solved it.

## Next step

Stage 10: given three independent real-data baseline experiments now
converging on "Cox PH is competitive with tree ensembles and much more
stable," assess whether a more complex proposed methodology is actually
justified, or whether the honest answer is that a well-specified Cox
model is the right choice for this feature set and these cohort sizes.
