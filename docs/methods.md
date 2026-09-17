# Methods

## Data sources

Four real, publicly accessible patient-level cohorts were used, each
pulled directly from its authoritative source and independently verified
against the raw data rather than trusted from secondary description
(`research/DATASETS/`, `src/data/loaders.py`):

- **Rotterdam** (N=2,982): breast cancer surgical patients, 1978–1993,
  Rotterdam Tumour Bank, pulled directly from R's `survival` package
  (`survival::rotterdam`).
- **GBSG2** (N=686): German Breast Cancer Study Group randomized trial of
  hormonal treatment and chemotherapy duration in node-positive breast
  cancer, loaded via `sksurv.datasets.load_gbsg2()`.
- **METABRIC** (N=2,509 before exclusions): Molecular Taxonomy of Breast
  Cancer International Consortium, clinical data pulled from cBioPortal's
  public data mirror.
- **TCGA-BRCA** (N=1,084 before exclusions): The Cancer Genome Atlas
  breast cancer cohort, PanCancer Atlas 2018 release, same source.

Rotterdam and GBSG2 form the study's primary train/external-test pair,
selected for their combination of a genuine time-to-event recurrence-
free-survival endpoint, zero access barrier, and — specifically for this
pairing — precedent as an established external-validation design in the
biostatistics literature (Royston & Altman, 2013) and as a standard
benchmark split in the deep-survival-modeling literature. METABRIC and
TCGA-BRCA served as independent, structurally different cross-checks
rather than a second external-validation pair, since their native feature
sets differ from Rotterdam/GBSG2's and no direct harmonization was
attempted between all four simultaneously.

## Outcome definition

The primary outcome was recurrence-free survival: time from the cohort's
native index point (surgery or trial enrollment) to the first of
recurrence or death, with patients alive and recurrence-free at last
follow-up treated as censored. Rotterdam and GBSG2 report follow-up time
in days; METABRIC and TCGA-BRCA report in months. This unit discrepancy
was identified during data quality review and harmonized (days converted
to months) prior to any cross-cohort comparison (`research/RESULTS/
data_quality/SYNTHESIS.md`).

## Cohort construction and exclusions

METABRIC data quality review identified a block of 528–529 patients
simultaneously missing across approximately 12 clinical variables,
traced to specific internal sub-cohort batches within METABRIC rather
than random missingness. These patients were excluded from METABRIC
analyses using a reproducible, data-driven rule (rows missing in ≥10 of
12 checked columns), rather than filtering by an internal cohort-number
field, which was found not to separate complete from incomplete records
cleanly. TCGA-BRCA retained only 799 patients with complete outcome and
covariate data, of whom 74 (9.3%) had a recorded recurrence/progression
event.

## Feature harmonization (Rotterdam/GBSG2)

Because Rotterdam and GBSG2 encode conceptually similar variables
differently (e.g., a categorical tumor-size bucket versus a continuous
millimeter measurement), a common eight-feature schema was constructed
(`src/data/harmonize.py`): age, positive lymph node count, estrogen and
progesterone receptor values (standardized numeric); menopausal status,
tumor size category, histologic grade, and hormone therapy receipt
(categorical, one-hot encoded with a reference category dropped). A
chemotherapy indicator, present in Rotterdam, was excluded from the
common schema because it is not released as a comparable field in
GBSG2's public data. Rotterdam contains no grade-1 patients; the 81
grade-1 patients present in GBSG2 were retained in the external test set
rather than excluded, since removing them would constitute test-set
curation favorable to the reported result.

## Models

Four survival models were fit on Rotterdam and evaluated on GBSG2: Cox
proportional hazards, elastic-net-penalized Cox (regularization strength
selected via five-fold cross-validation on Rotterdam only), random
survival forest (300 trees), and gradient boosting survival analysis (200
boosting stages). The same model family (excluding elastic-net Cox) was
fit independently within METABRIC (80/20 train/holdout split) and within
TCGA-BRCA (five-fold cross-validation only, given its small usable event
count). All models used a fixed random seed (42) for reproducibility.

## Evaluation

The primary metric was Harrell's concordance index (C-index), computed
on: (a) the training set (in-sample, expected optimistic), (b) five-fold
cross-validation within the training cohort, and (c) the held-out
external or within-cohort test set. Model selection (elastic-net
regularization strength) used only training-cohort cross-validation; the
external test set was never used for any model-selection decision.

## Explainability and robustness

For the selected primary model (Cox PH, trained on the full Rotterdam
cohort), two complementary explainability analyses were performed on a
held-out Rotterdam split: native Cox hazard ratios, and permutation
feature importance (computed identically for Cox PH and random survival
forest to allow direct comparison). Subgroup robustness analysis
evaluated the same model's discrimination on the GBSG2 external test set
across six clinically motivated subgroups (age band, menopausal status,
histologic grade, hormone therapy status, nodal burden), reporting a
subgroup only where it met a minimum sample threshold (N≥30, ≥10 events)
to avoid reporting unstable estimates from small strata.

## Software and reproducibility

All analyses used Python 3.11 with scikit-survival, lifelines, and
scikit-learn; Rotterdam was retrieved via R 4.3 (`survival` package).
Code is organized under `src/` (reusable modules) and `scripts/`
(experiment entry points), with raw data excluded from version control
per data governance policy (`data/README.md`) and pull scripts provided
to regenerate it from source. Each experiment is documented individually
in `research/EXPERIMENTS/` with dataset version, features, hyperparameters,
random seed, and results, per this project's experiment-tracking standard.
