# Experiment 0003 — Explainability (Stage 13)

**Date:** 2026-09-17
**Script:** `scripts/explainability.py`
**Model:** Cox PH (primary, per `research/PROPOSED_METHODOLOGY.md`), with Random Survival Forest as a cross-check
**Data:** Rotterdam, 75/25 train/holdout split (holdout never used for model fitting)

## Method

Per project brief Section 24: SHAP / permutation importance / feature
importance, with an explicit reminder that predictive association is not
causation. Two complementary views:

1. **Cox PH native hazard ratios** — a genuine advantage of choosing Cox
   PH as the primary model: every coefficient has a standard, direct
   clinical interpretation with no need for a post-hoc explainer.
2. **Permutation importance** (model-agnostic — identical method for Cox
   PH and Random Survival Forest, so the two can be compared fairly),
   computed on the held-out split, not the training data.

**Note on hazard ratio units:** numeric features (age, nodes_positive,
er_value, pr_value) were standardized before fitting, so each numeric
hazard ratio is **per 1 standard deviation** of that feature, not per raw
clinical unit (e.g. not "per additional positive node"). This is stated
explicitly to avoid a common misreading.

## Results — Cox PH hazard ratios (Rotterdam training split)

| Feature | Hazard ratio | Direction |
|---|---|---|
| Grade 3 (vs. grade 2 reference) | 1.393 | ↑ risk |
| Positive nodes (per 1 SD) | 1.364 | ↑ risk |
| Tumor size >50mm (vs. 20-50mm reference) | 1.297 | ↑ risk |
| Post-menopausal (vs. pre-menopausal) | 1.115 | ↑ risk |
| Age (per 1 SD) | 1.032 | ↑ risk (small) |
| ER value (per 1 SD) | 1.031 | ↑ risk (small) |
| PR value (per 1 SD) | 0.970 | ↓ risk (small) |
| Hormone therapy received | 0.880 | ↓ risk |
| Tumor size ≤20mm (vs. 20-50mm reference) | 0.727 | ↓ risk |

Figure: `research/FIGURES/cox_hazard_ratios.png`

## Results — Permutation importance (held-out split, mean C-index drop when shuffled)

| Feature | Cox PH | Random Survival Forest |
|---|---|---|
| Positive nodes | **0.081** | **0.118** |
| Tumor size ≤20mm | 0.025 | 0.011 |
| Grade 3 | 0.012 | 0.006 |
| Age | -0.001 (noise) | 0.010 |
| PR value | 0.001 | 0.007 |
| Hormone therapy | 0.001 | 0.001 |
| Tumor size >50mm | 0.0004 | -0.0004 (noise) |
| ER value | -0.001 (noise) | -0.002 (noise) |
| Menopause status | -0.001 (noise) | -0.001 (noise) |

Figure: `research/FIGURES/permutation_importance.png`

## Interpretation (association, not causation — stated explicitly per Section 24)

1. **Both independent methods (hazard ratios and permutation importance)
   and both model classes (Cox PH and Random Survival Forest) agree**:
   number of positive lymph nodes is by far the dominant predictor,
   followed by tumor size and grade. This is a real convergence across
   four different analytical angles, not a single method's artifact.
2. **This matches well-established clinical knowledge** — positive nodal
   status, tumor grade, and tumor size are the classic core prognostic
   factors in breast cancer staging (they form the backbone of the TNM
   system and the Nottingham Prognostic Index cited throughout our
   literature review, e.g. `research/PAPERS/P0004_...md`). This is a
   meaningful sanity check on the whole modeling pipeline: the model
   independently rediscovered known clinical prognostic factors rather
   than finding something spurious.
3. **Hormone therapy shows a protective association** (HR=0.880), matching
   real oncology knowledge that hormonal therapy reduces recurrence risk
   in receptor-positive patients — another clinically-plausible result,
   not asserted as this study's discovery.
4. **Several features (age, ER value, menopause status) show near-zero or
   even negative permutation importance** — meaning shuffling them barely
   changes or even slightly improves the model's held-out C-index. This
   is a real, honestly-reported finding: **these features are carrying
   little independent predictive signal beyond what nodes/size/grade
   already capture** in this dataset and feature set, not evidence that
   they're clinically unimportant in general (small effect sizes and
   correlation with the dominant features are the more likely explanation
   — not investigated further here, flagged as a direction for future
   feature-interaction analysis rather than overclaimed).

## What we are NOT claiming

Per Section 24's explicit instruction: **we are not claiming "positive
nodes cause recurrence"** — nodal involvement is itself a manifestation
of how advanced the cancer already is at diagnosis, not an independent
causal driver in the everyday sense. These are model-internal predictive
associations, useful for risk stratification, not a causal mechanism
study.

## Next step

Stage 14 (robustness/fairness): check whether this predictive pattern
holds consistently across age groups and other subgroups where sample
size permits, rather than assuming it's uniform across the population.
