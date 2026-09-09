# Cohort Definition — Breast Cancer Recurrence / Relapse Prediction

**Status: DRAFT, v2.** Superseded from the earlier pCR-focused draft after
D005 (revert to recurrence, EHR-required) and D006 (All of Us recurrence
feasibility findings — MEDIUM confidence, proceed as a gated pilot). Will
be finalized only after real piloting in the All of Us Researcher
Workbench.

## Clinical question

Among breast cancer patients treated with curative intent, can we predict
— using only information available at the end of primary treatment — the
future risk of recurrence (locoregional or distant)?

## Why the design looks the way it does

Two things this design must account for, both surfaced directly by our own
research this session:

1. **Structured/coded recurrence labels are known to undercount true
   recurrence** (Gap 2 in `RESEARCH_GAPS.md`: ICD-coded recurrence caught
   only 2.3% vs. 11.1% true recurrence in one well-verified study). All of
   Us adds a *second* layer of the same risk: even a good multi-signal
   structured algorithm can only see care that happens within the health
   systems feeding data into All of Us — a new 2026 claims-linkage study
   found real-world care events undercounted by a wide margin relative to
   insurance claims for the same patients.
2. Because of (1), **we cannot treat "no recurrence signal observed" as
   equivalent to "confirmed disease-free."** It must be treated as
   **censored** (unknown), not as a negative label. This pushes the study
   toward a **time-to-event / survival framing** (recurrence-free survival
   with censoring) rather than simple binary classification — which is
   also more clinically standard and more defensible statistically when
   labels are known to be imperfect.

## Proposed structure

```
Index date = end of primary treatment
  (surgery + adjuvant chemo/radiation/endocrine therapy initiation,
   whichever marks the point "active initial treatment" is considered
   complete - exact operational definition to be finalized once we can
   see what the data actually supports)
  |
  |-- Baseline window: diagnosis through index date
  |   (staging, receptor status [ER/PR/HER2], grade, nodal status,
  |    treatment received, demographics, comorbidities)
  |
  v
Prediction time T = index date
  |
  | (features locked here - nothing after T may be used as model input)
  v
Follow-up / observation period (multi-year - recurrence risk extends
  2-10+ years post-treatment, unlike pCR which resolves in months)
  |
  v
Outcome ascertainment via a COMBINED multi-signal proxy algorithm
  (not any single signal alone - see Methodology below), applied over
  the full follow-up period:
    - new secondary-malignancy diagnosis code (ICD-10 C77-C79) after
      index date
    - restarted or changed systemic anticancer therapy after a
      treatment-free gap (proposed threshold: 6-12 months, per
      published convention - to be validated against our own pilot)
    - new radiation therapy to a site inconsistent with initial
      locoregional treatment
    - death with breast cancer as underlying/contributing cause
  |
  v
Each patient's follow-up ends at: recurrence-proxy-positive event,
  death, loss of continuous engagement with the AoU-linked health
  system (a proxy for "we can no longer see this patient's care"),
  or end of available data - whichever comes first. This is the
  censoring point.
```

## Outcome label — explicitly treated as NOISY, not ground truth

Per the feasibility investigation: general claims-based recurrence-proxy
algorithms achieve 86-94% sensitivity / 93-99% specificity **only when
validated in closed or near-complete care-capture settings** (Medicare
fee-for-service claims nationally, or single integrated health systems
like Kaiser Permanente/Geisinger where patients get nearly all care in
one system). All of Us is neither — it is a federated, partial-capture
network. **We should not assume those published performance figures
transfer**, and must establish our own estimate before trusting the
label for modeling. See Validation Gate below.

## Inclusion criteria (draft)

- Confirmed invasive breast cancer diagnosis, structured procedure/diagnosis
  evidence of primary treatment (surgery with or without adjuvant therapy)
- Sufficient continuous engagement with the AoU-linked health system across
  the intended follow-up window (operational definition of "continuous
  engagement" — e.g. minimum visit density — to be set during piloting;
  this is a deliberate mitigation for the care-outside-network blind spot)
- No evidence of metastatic (Stage IV) disease at initial diagnosis

## Exclusion criteria (draft)

- Stage IV at diagnosis (different clinical question — already metastatic,
  not at risk of a first recurrence)
- Male breast cancer (separate stratified analysis if pursued at all, per
  same reasoning as the earlier pCR draft)
- Insufficient baseline receptor-status/staging data
- Patients with no follow-up time after index date (cannot contribute
  information to a time-to-event outcome)

## MANDATORY VALIDATION GATE before any cohort-scale modeling

Per the feasibility investigation's explicit recommendation, before
building the full cohort:

1. Pull a small stratified sample (proxy-positive and proxy-negative
   patients) from a pilot query.
2. Manually inspect each patient's structured timeline (and the ~11%
   NLP-note-derived layer where available) to get an honest, local
   estimate of the proxy algorithm's precision/recall in All of Us
   specifically — do not import the Medicare/Kaiser performance figures
   as an assumption.
3. If local concordance is unacceptably poor, the options are (in order
   of preference): (a) tighten the multi-signal algorithm and/or the
   continuous-engagement filter, (b) fall back to METABRIC for a
   methods-development/benchmarking arm while treating the All of Us
   effort as exploratory, (c) revisit whether SEER-Medicare's
   DUA/IRB/fee-gated but validated approach is worth the access cost —
   this would be a consequential decision requiring Kevin's sign-off, not
   an autonomous pivot.

## Open questions to resolve once Workbench access is active

1. Does All of Us populate the OMOP Oncology Module (`episode`/
   `episode_event` tables)? If yes, this may shortcut much of the manual
   cohort-building work below. (First query to run — see
   `DATASETS/all_of_us_omop.md` pilot steps.)
2. What is the actual completeness of ICD-10 C77-C79 codes and
   antineoplastic drug_exposure records in the breast cancer cohort?
3. What is the realistic final cohort size after inclusion/exclusion and
   the continuous-engagement filter? (Rough, unverified extrapolation
   suggests low thousands to ~15,000 total breast cancer cases in All of
   Us before any filtering — to be confirmed, not assumed.)

*(This file will be finalized, with all UNKNOWNs above resolved and the
Validation Gate results documented, before Stage 8 data quality analysis
begins.)*
