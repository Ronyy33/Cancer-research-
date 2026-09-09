# Research State

**Last updated:** 2026-09-09
**Current stage:** Stage 6/7 — dataset+question confirmed, cohort design (v2) drafted, awaiting Kevin's All of Us access to begin real piloting.

## Stage status

| Stage | Status |
|---|---|
| 0. Project setup | COMPLETE |
| 1. Literature discovery | COMPLETE |
| 2. Literature synthesis | COMPLETE |
| 3. Research gap identification | COMPLETE |
| 4. Candidate research questions | COMPLETE — **DECIDED (D005):** recurrence/relapse prediction (reverted from pCR after D004) |
| 5. Dataset discovery | COMPLETE — **DECIDED (D005):** All of Us (OMOP CDM) |
| 6. Dataset acquisition | IN PROGRESS — feasibility confirmed MEDIUM confidence (D006, gated pilot, not a clean guarantee); **BLOCKED on Kevin's All of Us identity verification** for actual Workbench access |
| 7. Cohort construction | DRAFT v2 written (`cohort_definition.md`) — time-to-event/censored design incorporating label-noise mitigations from D006; will be piloted and finalized once Workbench access is active |
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
- **D004:** pCR ruled out — All of Us has no free-text pathology report access, which pCR strictly requires. HIGH confidence block.
- **D005:** Kevin reverted to recurrence/relapse prediction, explicitly requiring a real EHR dataset. All of Us remains the only free, EHR-native option (Flatiron commercial-only, SEER-Medicare needs DUA+IRB+fee).
- **D006:** Recurrence detection from All of Us structured data assessed as MEDIUM confidence — not blocked like pCR, but real risk that care happening outside All of Us's linked health systems is invisible (a 2026 claims-linkage study found EHR-only data undercounts real procedures by a wide margin vs. claims for the same patients). Resulting design: treat the recurrence label as noisy, use a combined multi-signal proxy algorithm (not one indicator), frame as recurrence-free survival with censoring rather than binary classification, and run a mandatory manual validation gate before any cohort-scale modeling.

## What's blocked vs. not blocked

**Blocked on Kevin:** All of Us Registered Tier requires his own photo-ID identity verification (see `DATASETS/all_of_us_omop.md`). Nothing about real data access can proceed until this is done.

**Not blocked — proceeding autonomously:**
- `cohort_definition.md` v2 is drafted and ready to pilot the moment Workbench access is live.
- Once access is active, the first concrete steps are listed in `DATASETS/all_of_us_omop.md` (check whether the OMOP Oncology Module is populated, query C77-C79 code completeness, pilot the multi-signal proxy algorithm, run the manual validation gate on a small sample).
- METABRIC remains documented as a fallback/benchmarking dataset if the validation gate shows the All of Us proxy label is too unreliable.
