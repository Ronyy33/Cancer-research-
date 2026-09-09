# Cohort Definition — Breast Cancer Recurrence Prediction (Multi-Dataset Real-Data Design)

**Status: DRAFT v3.** Supersedes the All of Us-based v2 draft after D007
(All of Us abandoned — institutional access barrier confirmed unresolvable;
switched to a multi-dataset real-data design using Rotterdam+GBSG2 as the
primary pair, METABRIC and TCGA-BRCA as secondary cohorts, Duke-Breast-
Cancer-MRI as an optional richer-feature/multimodal arm).

## Clinical question (unchanged from v2)

Among breast cancer patients treated with curative intent, can we predict
— using only information available at the end of primary treatment (or, in
these registry-style datasets, at diagnosis/surgery, which is when their
baseline variables are recorded) — the future risk of recurrence
(locoregional or distant), and does this generalize across independent
real-world cohorts?

## Why a multi-dataset design (see D007 in `DECISIONS.md`)

Three independent deep searches confirmed that no real, publicly-
downloadable, genuinely longitudinal (multi-visit) EHR dataset for breast
cancer recurrence is accessible without institutional backing. Rather than
treat this as a dead end, the design leans into what IS available: several
independent real cohorts, each with a genuine time-to-event recurrence
outcome and zero access barrier. Modeling across multiple real cohorts
gives genuine external validation — the single most consistently
documented gap in this field (`RESEARCH_GAPS.md` Gap 3) — using an
established methodology (Royston & Altman 2013) rather than an invented
split.

## Datasets in the design

| Role | Dataset | N | Outcome field | Access |
|---|---|---|---|---|
| Primary training | Rotterdam | 2,982 | `rfstime`/`recur` (recurrence-free survival) | Built into R `survival` package |
| Primary external validation | GBSG2 | 686 (43.6% event rate) | recurrence-free survival + censoring | CRAN / scikit-survival |
| Secondary cross-validation cohort | METABRIC | ~2,509 | Relapse-Free Survival status + months | cBioPortal, public |
| Secondary cross-validation cohort | TCGA-BRCA | ~1,098 | DFI (disease-free interval), DSS, PFI | cBioPortal/GDC, public |
| Optional richer-feature / multimodal arm | Duke-Breast-Cancer-MRI | 922 (event rate TBD) | LRFS/DRFS time-to-event | TCIA, public |

## Proposed structure (per dataset)

```
Index date = surgery / diagnosis (varies slightly by dataset - each
  dataset's own definition will be used and documented, not forced into
  an artificial common definition that the source data doesn't support)
  |
  |-- Baseline features: everything recorded at/before index date
  |   (age, tumor size/grade, nodal status, receptor status [ER/PR/
  |    HER2 where available], treatment received)
  |
  v
Prediction time T = index date
  |
  | (features locked here - standard for these datasets since they are
  |  baseline-snapshot-plus-outcome by design, so leakage risk here is
  |  LOW as long as we don't accidentally include any post-baseline
  |  variable, e.g. treatment received AFTER the recorded baseline -
  |  to be double-checked per dataset during Stage 8)
  v
Follow-up period (years, varies by cohort - Rotterdam/GBSG2 have long
  follow-up given 1980s-90s origin; METABRIC/TCGA vary)
  |
  v
Outcome: recurrence-free survival time + event indicator (time-to-event,
  NOT binary classification - censoring is handled properly since these
  datasets were built for survival analysis from the start, unlike our
  earlier noisy-proxy design for All of Us)
```

## Why this is actually a leakage-safer design than the All of Us plan

These datasets were purpose-built for survival analysis by their original
authors — the outcome fields already properly separate "recorded at
baseline" from "observed over follow-up," and censoring is handled by
design rather than needing to be reconstructed from noisy multi-signal
proxies (contrast with the All of Us design in the superseded v2 draft,
which needed the elaborate noisy-label mitigation strategy). This is a
genuine methodological upgrade, not just a fallback.

## Modeling plan sketch (to be refined at Stage 9/10)

1. **Baselines first** (per project brief Section 17): Kaplan-Meier, Cox
   Proportional Hazards, Elastic-Net Cox on Rotterdam, tested on GBSG2.
2. **Stronger baselines:** Random Survival Forest, gradient-boosted
   survival models (matching what the literature review found — P0027
   showed Cox can beat DeepSurv, so we test this ourselves rather than
   assuming deep learning wins).
3. **Cross-cohort generalization check:** train on Rotterdam, test on
   GBSG2 (the established pairing); separately check performance on
   METABRIC and TCGA-BRCA as further independent real-world checks —
   this is a genuinely multi-cohort external validation study, which is
   rare in this literature per our own review.
4. Only after baselines are established and cross-cohort generalization is
   characterized would a more complex model (e.g., a landmark-time neural
   architecture inspired by P0016/Multimodal BEHRT) be considered, and
   only if it demonstrably beats the simpler baselines — per the project's
   core principle of preferring simpler models when sufficient.

## Inclusion/exclusion criteria

Will follow each dataset's own established cohort definition (documented
in the original publications) rather than imposing an artificial common
filter that doesn't match what the source data supports. Cross-cohort
harmonization of variable definitions (e.g., what counts as "positive
nodes," receptor-status cutoffs) will be documented explicitly during
Stage 7/8 data quality analysis, since different eras/institutions may
define these slightly differently — a known real risk when combining
cohorts, to be checked rather than assumed away.

## Open questions for Stage 7/8

1. Exact Duke-Breast-Cancer-MRI recurrence event count/rate (flagged as
   unverified in `DATASETS/duke_breast_cancer_mri.md` — must confirm
   before relying on it for primary modeling).
2. Harmonizing variable definitions across cohorts from different eras
   (1978-1993 Rotterdam vs. 2000s+ Duke/TCGA/METABRIC) — treatment
   patterns and receptor-testing methods have evolved; this must be
   documented as a limitation, not glossed over.
3. Whether to pursue Duke's imaging data as a genuine multimodal arm, or
   use it purely as a fourth structured-clinical cohort.

*(This file will be finalized once Stage 7 cohort construction actually
begins against the real downloaded data.)*
