# Research State

**Last updated:** 2026-09-09
**Current stage:** Stage 6 COMPLETE (dataset confirmed, no institutional barrier) → Stage 7 (cohort construction) ready to begin.

## Stage status

| Stage | Status |
|---|---|
| 0. Project setup | COMPLETE |
| 1. Literature discovery | COMPLETE |
| 2. Literature synthesis | COMPLETE |
| 3. Research gap identification | COMPLETE |
| 4. Candidate research questions | COMPLETE — recurrence/relapse prediction (D005) |
| 5. Dataset discovery | COMPLETE (expanded) — see D007 |
| 6. Dataset acquisition | **COMPLETE** — **DECIDED (D007):** multi-dataset real-data design: Rotterdam (train) + GBSG2 (external validation) as primary pair, METABRIC + TCGA-BRCA as secondary cross-validation cohorts, Duke-Breast-Cancer-MRI as optional richer-feature arm. **All zero-barrier, no institution or credentials required — nothing blocking us now.** |
| 7. Cohort construction | READY TO BEGIN — `cohort_definition.md` v3 drafted around the multi-dataset design |
| 8. Data quality analysis | NOT STARTED |
| 9. Baseline modeling | NOT STARTED |
| 10. Proposed methodology | NOT STARTED |
| 11. Experiments | NOT STARTED |
| 12. Validation | NOT STARTED |
| 13. Explainability | NOT STARTED |
| 14. Robustness/fairness | NOT STARTED |
| 15. Research analysis | NOT STARTED |
| 16. Paper preparation | NOT STARTED |

## Decision history (see `DECISIONS.md` for full detail)

- **D003:** pCR prediction + All of Us chosen.
- **D004:** pCR ruled out — All of Us has no pathology-report text access.
- **D005:** Reverted to recurrence/relapse prediction, EHR dataset required.
- **D006:** All of Us recurrence detection assessed MEDIUM confidence (structured proxy, gated pilot).
- **D007:** All of Us abandoned entirely — institute not registered, confirmed unresolvable. Deep multi-hour, 3-agent search found All of Us/NSABP/UK Biobank are all institution-gated, and no real, barrier-free, genuinely multi-visit EHR dataset exists publicly. **Switched to a multi-dataset real-data design** (Rotterdam+GBSG2 primary pair, METABRIC+TCGA-BRCA secondary, Duke-Breast-Cancer-MRI optional) — turns the access constraint into a strength by providing genuine cross-cohort external validation from day one, the field's most-cited weakness.

## What's blocked vs. not blocked

**Nothing is currently blocked.** Every dataset in the D007 design is immediately, freely accessible with no registration, no institutional affiliation, no fee, no IRB (Rotterdam ships in R's `survival` package; GBSG2 via CRAN/scikit-survival; METABRIC and TCGA-BRCA via cBioPortal; Duke-Breast-Cancer-MRI via public TCIA).

**Next step:** begin Stage 7 (real cohort construction) — download/load the actual data, verify the fields match what was documented in `DATASETS/`, confirm Duke's exact recurrence event rate, and start the data quality analysis (Stage 8).
