# Research State

**Last updated:** 2026-09-16
**Current stage:** Stage 7 (cohort construction) — data loading complete and directly verified; cohort/feature definition finalization next.

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
| 7. Cohort construction | IN PROGRESS — all 4 datasets pulled from authoritative sources and directly verified (not search-snippet sourced): Rotterdam (N=2,982, R `survival` package), GBSG2 (N=686, scikit-survival), METABRIC (N=2,509, cBioPortal GitHub mirror), TCGA-BRCA (N=1,084, same mirror). `src/data/loaders.py` + `tests/test_loaders.py` (5/5 passing) built. Real event rates confirmed: Rotterdam 57.4%, GBSG2 43.6%, METABRIC 40.3%, TCGA-BRCA 8.9% (notably lower — flagged) |
| 8. Data quality analysis | NOT STARTED — next step |
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
