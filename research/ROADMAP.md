# Research Roadmap — Stage Definitions

Each stage below defines what "complete" means. A stage is never marked
complete unless its exit criteria are actually met — see `RESEARCH_STATE.md`
for the live status of each.

| # | Stage | Exit criteria |
|---|---|---|
| 0 | Project setup | Repo structure created; tracking files initialized |
| 1 | Literature discovery | Seed papers verified; citation chaining performed forward and backward; recent (2024–2026) work found |
| 2 | Literature synthesis | LITERATURE_MATRIX.csv populated; high-value papers have individual notes in `PAPERS/` |
| 3 | Research gap identification | Each gap in `RESEARCH_GAPS.md` supported by ≥2 papers with recorded evidence |
| 4 | Candidate research questions | ≥3 candidate questions ranked on clinical importance, novelty, data feasibility, label quality, technical feasibility, validation feasibility, interpretability, publication potential |
| 5 | Dataset discovery | Candidate datasets investigated and ranked; variables verified against primary sources, not assumed |
| 6 | Dataset acquisition | Chosen dataset obtained or access path documented; **requires human approval if credentials/IRB/payment needed** |
| 7 | Cohort construction | `cohort_definition.md` complete: index date, prediction time, observation window, horizon, outcome, censoring, inclusion/exclusion criteria |
| 8 | Data quality analysis | Missingness, duplicates, class balance, temporal coverage, outliers documented in `RESULTS/data_quality/` |
| 9 | Baseline modeling | Majority baseline + at least Logistic Regression + one tree ensemble (or Cox equivalents for survival) run and recorded as experiments |
| 10 | Proposed methodology | Documented rationale: what limitation from Stage 3 does this design address, why not a simpler model |
| 11 | Experiments | All experiments recorded in `EXPERIMENTS/experiment_####.md`, reproducible via `scripts/` |
| 12 | Validation | Strongest realistic validation strategy applied (temporal split at minimum; external if available) |
| 13 | Explainability | SHAP/permutation importance + calibration plots produced; associations not overstated as causal |
| 14 | Robustness/fairness | Subgroup analysis where sample size permits |
| 15 | Research analysis | Honest synthesis, including negative results |
| 16 | Paper preparation | `docs/` sections drafted from completed experiments only |

## Process (do not skip stages)

```
RESEARCH EXPLORATION
  -> LITERATURE REVIEW
  -> RESEARCH GAP
  -> DATASET DISCOVERY
  -> DATA ACQUISITION
  -> COHORT DEFINITION
  -> EHR PREPROCESSING
  -> BASELINES
  -> MODEL DEVELOPMENT
  -> EXPERIMENTS
  -> VALIDATION
  -> EXPLAINABILITY
  -> RESEARCH ANALYSIS
  -> PAPER-READY RESULTS
```

## Human-in-the-loop checkpoints

Per the operating rules, autonomous work proceeds through routine engineering
and research steps without asking permission. Work STOPS for human decision
at:

1. Choosing between fundamentally different research questions
2. Selecting a dataset that requires credentials
3. IRB / ethics approval needs
4. Institutional data access
5. Paying for a dataset/API
6. Committing to the final research hypothesis
7. Choosing between substantially different study designs
8. Clinically consequential assumptions that cannot be verified

The first such checkpoint is expected after Stage 5 (dataset ranking) /
Stage 4 (candidate question ranking) — see `PROGRESS.md` for the live
"decision required" flag.
