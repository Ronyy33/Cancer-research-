# Research State

**Last updated:** 2026-09-09
**Current stage:** Stage 4/5 complete (candidate questions ranked, datasets ranked) — **AWAITING HUMAN DECISION** before Stage 6 (dataset acquisition) begins.

## Stage status

| Stage | Status |
|---|---|
| 0. Project setup | COMPLETE |
| 1. Literature discovery | COMPLETE — 32 papers verified via WebSearch (WebFetch blocked all session; see caveats in each paper note), citation chaining performed topically |
| 2. Literature synthesis | COMPLETE — `LITERATURE_MATRIX.csv` (32 rows) + 8 detailed paper notes in `PAPERS/` for the highest-value sources |
| 3. Research gap identification | COMPLETE — `RESEARCH_GAPS.md`, 8 evidence-backed gaps, each with ≥2 supporting sources and confidence levels |
| 4. Candidate research questions | COMPLETE — `CANDIDATE_RESEARCH_QUESTIONS.md`, 4 candidates scored; recommendation prepared **pending human decision** |
| 5. Dataset discovery | COMPLETE — `DATASETS/` (SEER, MIMIC/eICU, TCGA-BRCA, METABRIC, I-SPY2, All of Us, + summary table of 9 more) |
| 6. Dataset acquisition | **BLOCKED — awaiting human decision** (see checkpoint) |
| 7. Cohort construction | NOT STARTED |
| 8. Data quality analysis | NOT STARTED |
| 9. Baseline modeling | NOT STARTED |
| 10. Proposed methodology | NOT STARTED |
| 11. Experiments | NOT STARTED |
| 12. Validation | NOT STARTED |
| 13. Explainability | NOT STARTED |
| 14. Robustness/fairness | NOT STARTED |
| 15. Research analysis | NOT STARTED |
| 16. Paper preparation | NOT STARTED |

## Key findings this session

1. **Structured/coded EHR recurrence labels badly under-ascertain true recurrence** (~2.31% coded vs. 11.1% NLP-confirmed, P0005) — independently confirmed by two research passes. This is the single most important finding for our eventual cohort/label design.
2. **Genuine external (cross-institution) validation of true PREDICTION models (not detection/extraction tools) is almost entirely absent** from the literature found — the field's clearest, most defensible open gap.
3. **Deep learning does not automatically beat classical models** in this domain (P0027: Cox beat DeepSurv on held-out SEER data) — directly supports our baselines-first, simplest-sufficient-model principle.
4. **No single dataset is a perfect fit.** SEER/NCDB cannot capture recurrence at all (structural gap, not missingness). METABRIC has a well-powered recurrence endpoint and is fully public but is not EHR-native (no labs/meds/notes/timeline). All of Us has the right longitudinal EHR structure but is unproven for this specific cohort/outcome and requires the human researcher's own identity verification to access.
5. Two systematic reviews/meta-analyses (P0006, P0007) confirm the aggregate field's benchmark performance is anchored on curated cohorts, not messy real-world EHR, and flag a demographic/geographic equity gap in existing models.

## Not yet decided (blocking Stage 6+)

- **The final prediction target** (recurrence/DFS vs. toxicity vs. treatment-response vs. survival) — see `CANDIDATE_RESEARCH_QUESTIONS.md` for the ranked options and recommendation.
- **The dataset to acquire first** — see `DATASETS/` for ranked options; several strong candidates (Flatiron, SEER-Medicare, TriNetX, All of Us Controlled Tier) require human-only action (credentials, payment, IRB, or identity verification) per project brief Section 33.

This is exactly the kind of decision the human-in-the-loop rule (project brief Section 34) reserves for Kevin. See the RESEARCH CHECKPOINT delivered in this session's chat for the concise summary and recommendation. **No dataset acquisition or modeling will proceed until this decision is made.**
