# Research State

**Last updated:** 2026-09-17
**Current stage:** Stage 14 (robustness/fairness) COMPLETE → Stage 15 (research analysis/synthesis) next.

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
| 8. Data quality analysis | COMPLETE — `scripts/data_quality_analysis.py` run on all 4 cohorts; reports in `research/RESULTS/data_quality/`, figures in `research/FIGURES/data_quality/`. Key findings: Rotterdam/GBSG2 are clean trial-quality data (zero missingness/duplicates/implausible values); METABRIC has a real, structured (non-random) missingness block of ~528 patients tied to specific internal sub-cohort batches — needs an explicit handling decision before modeling; TCGA-BRCA has an empty `WEIGHT` column and a real 13.1% DFS censoring gap on top of its already-low 8.9% event rate; **critical cross-cohort issue found: Rotterdam/GBSG2 report time in days, METABRIC/TCGA-BRCA in months — must be harmonized before any cross-cohort comparison**. Full synthesis in `research/RESULTS/data_quality/SYNTHESIS.md` |
| 9. Baseline modeling | **COMPLETE.** `experiment_0001` (Rotterdam→GBSG2 external validation): Cox PH 0.654, Elastic-Net 0.646, RSF 0.672 (best raw, most overfitting), GBS 0.669. `experiment_0002` (METABRIC + TCGA-BRCA within-cohort): METABRIC shows the same pattern as Rotterdam/GBSG2 (Cox PH 0.653 holdout vs RSF 0.666, much smaller train/test gap) — a second independent cohort confirming the finding. **TCGA-BRCA's CV-mean C-index (0.49-0.53) is essentially random chance** despite deceptively high training scores — confirms it as unreliable for drawing conclusions given only 74 real events, an honest negative result, not swept under the rug. Found/fixed a real one-hot-encoding collinearity bug along the way (regression-tested). See `research/EXPERIMENTS/experiment_0001.md` and `experiment_0002.md` |
| 10. Proposed methodology | **COMPLETE** — `research/PROPOSED_METHODOLOGY.md`: Cox PH selected as primary model. Evidence: 3 independent real cohorts show tree ensembles beat Cox PH by only 0.013-0.018 C-index while overfitting 3-5x more; a landmark-time neural architecture (P0016) was explicitly considered and rejected as unsuitable given our data's baseline-snapshot (not multi-visit) structure. Conditions for revisiting this decision stated explicitly (genuine longitudinal EHR access, larger performance gap, or a specific nonlinear sub-question) |
| 11. Experiments | Substantially covered by experiment_0001-0003 (tracked, reproducible, not post-hoc-tuned) |
| 12. Validation | Genuine external validation (Rotterdam→GBSG2) + independent within-cohort validation (METABRIC) both done — satisfies the project's validation hierarchy at the external-validation level for the primary pair |
| 13. Explainability | **COMPLETE** — `research/EXPERIMENTS/experiment_0003.md`: Cox PH hazard ratios + permutation importance (Cox PH vs RSF) on held-out Rotterdam split. Finding: positive lymph nodes, tumor size, and grade dominate across both methods and both model classes — matches established clinical prognostic factors (a real sanity check on the pipeline). Explicit association-not-causation framing throughout, per Section 24 |
| 14. Robustness/fairness | **COMPLETE** — `research/EXPERIMENTS/experiment_0004.md`: subgroup analysis (Cox PH on GBSG2 external test), all subgroups met the minimum sample threshold. **Key finding: model discriminates notably worse for patients with 1-3 positive nodes (C-index 0.564, near chance) than 4+ nodes (0.608)** — weakest exactly where risk stratification matters most clinically. Grade-1 patients (out-of-distribution for training, per experiment_0001) performed reasonably (0.660) — a reassuring but not over-interpreted finding given small N. **Honest limitation stated directly: Rotterdam/GBSG2 have no race/ethnicity/socioeconomic data, so the equity gap from Gap 4 in RESEARCH_GAPS.md cannot be assessed with current datasets** |
| 15. Research analysis | NOT STARTED — next step |
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
