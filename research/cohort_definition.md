# Cohort Definition — Pathologic Complete Response (pCR) Prediction

**Status: DRAFT.** This is a conceptual design written before data access is
confirmed (Stage 6 is still partially blocked — see `RESEARCH_STATE.md`).
It will be revised once the All of Us feasibility check (in progress) and
Kevin's Registered Tier access are both available, and finalized only after
piloting against real data. Do not treat any inclusion/exclusion criterion
below as final until that revision.

## Clinical question

Among breast cancer patients who receive neoadjuvant (pre-surgical)
chemotherapy, can we predict — using only information available **before
treatment starts** — whether a patient will achieve a pathologic complete
response (pCR) at the time of surgery?

## Why this design (per Section 9 of the project brief)

This must be a genuine **PREDICTION** task, not detection: pCR is inherently
a future event relative to treatment initiation, so as long as features are
correctly restricted to the pre-treatment window, this design has structurally
lower leakage risk than recurrence-prediction tasks in the literature we
reviewed (see `RESEARCH_GAPS.md` Gap 1). This is a genuine strength of this
research question relative to the recurrence-prediction alternative.

## Proposed structure

```
Index date (neoadjuvant chemotherapy start)
  |
  |-- Baseline window: all information available BEFORE index date
  |   (demographics, comorbidities, baseline labs, biopsy pathology,
  |    receptor status [ER/PR/HER2], clinical stage, imaging findings
  |    at diagnosis)
  |
  v
Prediction time T = index date (chemotherapy start)
  |
  | (features must be locked here — nothing after this point may be used
  |  as a model input)
  v
Treatment period (neoadjuvant chemotherapy regimen, duration typically
  ~4-6 months) -- NOT used as a feature unless explicitly modeling
  "planned regimen" as a pre-treatment-known input (the planned regimen
  IS knowable at T and would be a legitimate feature; actual delivered
  doses/toxicities during treatment are NOT, since those postdate T)
  |
  v
Surgery date
  |
  v
Outcome ascertainment: pathologic complete response (pCR) = no residual
  invasive cancer in breast and axillary lymph nodes per surgical
  pathology report (ypT0/is ypN0, standard clinical definition — to be
  confirmed against whichever pCR definition variant the source data
  supports, as there are minor variants, e.g. with/without residual DCIS)
```

## Index date

Date of first administration of neoadjuvant chemotherapy for the current
breast cancer diagnosis.

## Prediction time (T)

Same as index date. All model features must be measurable and known as of
this date — this is the "hard requirement" the project brief specifies
(Section 14): the model must never see information after T.

## Observation window (baseline features)

Look-back period prior to T for extracting baseline covariates:
diagnosis date through T. Exact look-back bound for pre-existing conditions/
comorbidities (e.g., "any time prior" vs. "prior 1-2 years") to be decided
during Stage 7 based on what's actually queryable in the chosen data source.

## Outcome

Binary: pCR (yes/no) at surgical pathology, following completion of
neoadjuvant chemotherapy and definitive surgery.

## Censoring / attrition considerations

Patients who do not proceed to surgery (e.g., disease progression during
neoadjuvant treatment, patient declines surgery, loss to follow-up, death
before surgery) cannot have a pCR outcome ascertained and must be handled
explicitly — NOT silently dropped, since this could introduce a form of
outcome-dependent selection bias (patients who progress during treatment
are more likely to be excluded, which would bias the remaining cohort
toward treatment-responsive patients). This will be documented as a
specific limitation and, where feasible, reported as a secondary
"discontinued before surgery" category rather than simply excluded.

## Inclusion criteria (draft)

- Confirmed invasive breast cancer diagnosis
- Received neoadjuvant (pre-surgical) chemotherapy with documented start date
- Underwent definitive breast surgery following neoadjuvant treatment
- Surgical pathology report available for pCR ascertainment

## Exclusion criteria (draft)

- Metastatic disease at diagnosis (Stage IV) — neoadjuvant chemo intent and
  goals differ fundamentally in the metastatic setting
- Male breast cancer (extremely rare; would require separate stratified
  analysis if included at all, given very different population characteristics)
- Prior breast cancer treatment history that would confound baseline staging
- Insufficient baseline data to determine ER/PR/HER2 status (a core feature
  needed for any reasonable pCR model, per the literature — receptor status
  is consistently among the strongest predictors of pCR)

## Open questions to resolve once data access is confirmed

1. Can the chosen data source (All of Us, pending feasibility check; or
   I-SPY2 as fallback) reliably distinguish neoadjuvant from adjuvant
   chemotherapy administration via structured data, or does this require
   NLP over clinical notes?
2. Can pCR be ascertained from structured pathology codes, or does it
   require NLP extraction from free-text surgical pathology reports (as
   the broader recurrence literature suggests is often necessary for
   comparably granular outcomes — see Gap 2 in `RESEARCH_GAPS.md`)?
3. What is the realistic cohort size once inclusion/exclusion criteria are
   applied? (All of Us is a general-population program, not cancer-specific
   — realistic breast-cancer-plus-neoadjuvant-chemo subcohort size is
   currently unknown and is a focus of the ongoing feasibility check.)

*(This file will be finalized, with all UNKNOWNs above resolved, before
Stage 8 data quality analysis begins.)*
