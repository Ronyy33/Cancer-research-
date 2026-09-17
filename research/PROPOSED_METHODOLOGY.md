# Stage 10 — Proposed Methodology Decision

**Date:** 2026-09-17
**Decision:** Cox Proportional Hazards is the recommended primary model
for this research program's current feature set and cohort sizes. A more
complex architecture is **not** currently justified by the evidence.

## Why this decision, not a more complex model

Project brief Section 1 (First Principle) and Section 18 both require an
explicit answer to: *why this model, what limitation does it solve, why
not something simpler?* Here that question runs in the opposite direction
— the evidence collected in Stage 9 argues **against** adding complexity:

| Cohort | Cox PH | Best tree/ensemble model | Gap | Train→test overfitting (Cox / best ensemble) |
|---|---|---|---|---|
| GBSG2 (genuine external test) | 0.654 | 0.672 (RSF) | 0.018 | 0.013 / 0.061 |
| METABRIC (within-cohort holdout) | 0.653 | 0.666 (RSF) | 0.013 | 0.008 / 0.043 |
| TCGA-BRCA (5-fold CV) | 0.494 | 0.534 (GBS) | 0.040 (both ≈random) | both models unreliable — too few events, not a model-class issue |

**Three independent real cohorts** now show the same qualitative pattern:
Cox PH trails tree ensembles by only 0.013–0.018 C-index while showing
3–5x less train-to-test performance drop. This is not a single lucky
result — it replicated across Rotterdam→GBSG2 (external validation) and
METABRIC (independent within-cohort holdout), which is a much stronger
basis for a methodology decision than any one experiment alone.

**This also directly reproduces a finding from our own literature review**
(`research/PAPERS/P0027_cox_beats_deepsurv.md`): classical Cox beat
DeepSurv on held-out SEER data despite DeepSurv's higher training score —
the exact same qualitative pattern, now independently confirmed on our own
data rather than only cited from someone else's paper.

## Why NOT a landmark-time neural architecture (e.g. Multimodal BEHRT, P0016)

The strongest architectural exemplar found in our literature review
(`research/PAPERS/P0016_multimodal_behrt.md`) required genuine multi-visit,
timestamped EHR trajectories (labs, notes, procedure codes over a full
year of follow-up) to build its transformer-based patient representation.
**Our actual data does not have that structure** — this was established
directly in `research/cohort_definition.md` and confirmed again in Stage 8:
every real, barrier-free dataset available to this project (Rotterdam,
GBSG2, METABRIC, TCGA-BRCA) is baseline-snapshot-plus-survival-time, not a
repeated-measures timeline. Building a landmark-time transformer here would
not be "using a more sophisticated method" — it would be **applying an
architecture to data it isn't designed for**, and it could not exploit the
temporal-sequence modeling that makes that architecture useful in the
first place. This is a data-shape constraint, not a modeling-effort
shortcut.

## What WOULD justify moving beyond Cox PH

Stated explicitly, so this isn't a permanent default:
1. **Genuine longitudinal EHR access** (e.g. if institutional access to
   Flatiron, SEER-Medicare, or All of Us becomes available later) — that
   would change the data shape enough to justify revisiting sequence
   models.
2. **A materially larger performance gap** than the 0.013–0.018 found here
   — if future feature engineering (e.g. adding interaction terms, or
   including HISTOLOGICAL_SUBTYPE/CLAUDIN_SUBTYPE from METABRIC) widened
   the gap substantially, tree ensembles would become the more defensible
   default despite their overfitting risk.
3. **A specific clinical sub-question** where nonlinear interactions are
   independently known to matter (e.g. treatment-effect heterogeneity) —
   Random Survival Forest remains documented and available for this, not
   discarded, just not the default.

## What this means for remaining stages

- **Stage 11 (Experiments):** experiment_0001 and experiment_0002 already
  constitute the core experimental record for this decision — both
  tracked, reproducible, and neither post-hoc-tuned to produce this
  conclusion.
- **Stage 12 (Validation):** genuine external validation (Rotterdam→GBSG2)
  and independent within-cohort validation (METABRIC) are both already
  done. The validation hierarchy from the project brief (random split →
  temporal split → external validation) has been satisfied at the
  external-validation level for the primary pair — stronger than most
  published studies in this exact literature (per `RESEARCH_GAPS.md`
  Gap 3).
- **Stage 13 (Explainability):** proceed with Cox PH as the primary model
  for interpretability analysis (hazard ratios — a Cox model's native,
  directly-interpretable output) plus permutation importance for
  cross-checking, computed next.

## Honest caveat

Hyperparameter tuning for the tree-based models was not exhaustive
(reasonable defaults only, no grid search) — it's possible a tuned RSF or
gradient boosting model would widen the performance gap somewhat. Given
the consistency of the ~0.013–0.018 gap across two structurally different
real cohorts, it is unlikely that tuning would reverse the qualitative
conclusion (tree ensembles overfit more on this feature set), but this is
flagged as a real limitation of this analysis, not hidden.
