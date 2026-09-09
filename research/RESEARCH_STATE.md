# Research State

**Last updated:** 2026-09-09
**Current stage:** Stage 6 (dataset acquisition) — IN PROGRESS, partially blocked on human action.

## Stage status

| Stage | Status |
|---|---|
| 0. Project setup | COMPLETE |
| 1. Literature discovery | COMPLETE |
| 2. Literature synthesis | COMPLETE |
| 3. Research gap identification | COMPLETE |
| 4. Candidate research questions | COMPLETE — **DECIDED (D003):** treatment response / pCR prediction |
| 5. Dataset discovery | COMPLETE — **DECIDED (D003):** All of Us (OMOP CDM), first target |
| 6. Dataset acquisition | IN PROGRESS — feasibility check running (agent); **BLOCKED on Kevin's personal All of Us identity verification** for actual data access |
| 7. Cohort construction | NOT STARTED — conceptual cohort design for pCR prediction can begin now (no data access required for the design itself) |
| 8. Data quality analysis | NOT STARTED |
| 9. Baseline modeling | NOT STARTED |
| 10. Proposed methodology | NOT STARTED |
| 11. Experiments | NOT STARTED |
| 12. Validation | NOT STARTED |
| 13. Explainability | NOT STARTED |
| 14. Robustness/fairness | NOT STARTED |
| 15. Research analysis | NOT STARTED |
| 16. Paper preparation | NOT STARTED |

## Decision D003 (human-approved, 2026-09-09)

- **Research question:** treatment response / pathologic complete response (pCR) to neoadjuvant chemotherapy.
- **First dataset:** All of Us Research Program (OMOP CDM).
- **Flagged deviation:** this pairing (pCR + All of Us) was not the matched recommendation from the checkpoint (which paired pCR with I-SPY2, and All of Us with recurrence). It is more ambitious/EHR-native but unverified — see `DATASETS/all_of_us_omop.md` status update and the feasibility investigation now running.

## What's blocked vs. not blocked

**Blocked on Kevin (cannot be automated):** All of Us Registered Tier requires Kevin's own photo-ID identity verification. See `DATASETS/all_of_us_omop.md` for the exact steps. No All of Us data can be accessed until this is complete.

**Not blocked — proceeding autonomously:**
- Feasibility investigation into whether All of Us structured/OMOP data can plausibly support neoadjuvant-chemo cohort identification + pCR/treatment-response ascertainment (routine research work, no approval needed).
- Conceptual cohort design (`cohort_definition.md`) for the pCR prediction task — index date, prediction time, observation window, outcome definition, inclusion/exclusion criteria — can be drafted now independent of data access, then refined once the feasibility check and Kevin's access are both in hand.
- Scaffolding of `scripts/`, `configs/` for the eventual data pipeline.

I-SPY2 (the originally-recommended pCR dataset) remains fully public and immediately accessible with no blocker, and is documented as a fallback/comparison dataset if All of Us proves infeasible for this specific outcome.
