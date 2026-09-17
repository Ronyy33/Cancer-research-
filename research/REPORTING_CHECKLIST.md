# Reporting Checklist

## Which guideline applies

This is a **multivariable prediction model development and external
validation study** (recurrence-free survival prediction from clinical
variables), not a diagnostic accuracy study, not a clinical trial, and
not a study of an AI system embedded in a clinical workflow. The
applicable guideline is therefore **TRIPOD+AI** (Transparent Reporting of
a multivariable prediction model for Individual Prognosis Or Diagnosis —
AI extension). PROBAST-AI (risk of bias assessment for AI-based
prediction models) is used as a secondary self-assessment. STROBE,
CONSORT-AI, SPIRIT-AI, and CLAIM are not applicable (no diagnostic
accuracy comparison against a reference standard test, no clinical
trial, no image-based diagnostic classification).

## TRIPOD+AI self-assessment

| Item | Status | Where addressed |
|---|---|---|
| Title identifies it as a prediction model development/validation study | Done | This repository's framing throughout |
| Structured abstract | Done | `docs/abstract.md` |
| Background/rationale, including existing models | Done | `docs/introduction.md`, `docs/related_work.md` |
| Objectives | Done | `docs/introduction.md` |
| Source of data (registry/cohort/trial), dates | Done | `docs/methods.md`, `research/DATASETS/` |
| Eligibility criteria for participants | Done | `research/cohort_definition.md` (note: harmonized to each cohort's native inclusion criteria, not independently re-derived — stated as such) |
| Outcome definition and how/when determined | Done | `docs/methods.md` — recurrence-free survival, cohort-native ascertainment |
| Predictors: definition and measurement | Done | `docs/methods.md`, `src/data/harmonize.py` (every mapping decision documented inline) |
| Sample size rationale | Partial | Used all available patients per cohort after documented exclusions; no formal a priori power calculation was performed — stated as a limitation here rather than omitted |
| Missing data handling | Done | `research/RESULTS/data_quality/SYNTHESIS.md`, `docs/methods.md` (METABRIC block-exclusion rule documented and reproducible) |
| Statistical/ML methods for model development | Done | `docs/methods.md`, `research/EXPERIMENTS/experiment_0001.md` |
| Model-building procedures (variable selection etc.) | Done | Fixed 8-feature schema, no post-hoc feature selection performed — stated explicitly |
| Internal validation method | Done | 5-fold CV within Rotterdam/METABRIC |
| External validation method | Done | Rotterdam→GBSG2, genuinely held out |
| Performance measures (discrimination, calibration) | **Partial** | **Discrimination (C-index) reported throughout; calibration was explicitly NOT assessed — stated directly as a limitation in `docs/limitations.md`, not silently omitted** |
| Model presentation (equation/coefficients) | Done | `research/EXPERIMENTS/experiment_0003.md` (Cox hazard ratios) |
| Participant flow / numbers at each stage | Done | `docs/methods.md`, `research/RESULTS/data_quality/*.md` (exact N at each exclusion step) |
| Baseline characteristics of participants | Partial | Feature distributions reported in `research/RESULTS/data_quality/` per-dataset reports; not compiled into a single Table 1-style summary — noted as a gap for future work |
| Model performance results with confidence/uncertainty | Partial | CV standard deviations reported; formal confidence intervals on external C-index not computed — noted as a gap |
| Subgroup/fairness analysis | Done | `research/EXPERIMENTS/experiment_0004.md`, with explicit statement of what could NOT be assessed (demographic equity) |
| Limitations | Done | `docs/limitations.md` |
| Interpretation, including comparison to existing models | Done | `docs/discussion.md` |
| Implications for practice | Done | `docs/discussion.md`, `docs/conclusion.md` — explicitly scoped, no clinical deployment claim made |
| Funding/conflicts of interest | N/A | No external funding; autonomous research program, stated in project context |
| Availability of data/code/model | Done | Code in this repository; raw data not redistributed (per each source's own license — see `research/DATASETS/`), pull scripts provided to regenerate from original public sources |
| AI-specific: description of AI/ML component | Done | `docs/methods.md` — explicit model list, hyperparameters, software versions |
| AI-specific: human-AI interaction / deployment context | N/A | No deployment; explicitly research-stage only |
| AI-specific: handling of missing predictors at prediction time | Partial | One-hot encoding uses `handle_unknown="ignore"` for out-of-distribution categories (documented for the grade-1 case); no broader missing-predictor-at-inference strategy defined, since this is a research study, not a deployed system |

## PROBAST-AI self-assessment (risk of bias, high-level)

- **Participants domain:** Low-to-moderate concern — real, well-documented
  trial/registry cohorts, but era differences (Rotterdam/GBSG2 from the
  1980s–90s vs. METABRIC/TCGA-BRCA from the 2000s+) mean treatment
  patterns and receptor-testing methods are not perfectly comparable
  across cohorts — stated directly in `research/RESULTS/data_quality/
  SYNTHESIS.md`.
- **Predictors domain:** Low concern for the harmonized pair (documented,
  reproducible mapping); moderate concern for cross-cohort comparability
  given differing native codings across all four cohorts.
- **Outcome domain:** Low concern — genuine time-to-event outcomes with
  documented censoring, not proxy-derived labels (a deliberate design
  choice specifically to avoid the label-quality problem identified in
  the literature review, Gap 2).
- **Analysis domain:** Low-to-moderate concern — appropriate
  discrimination metrics and genuine external validation used; moderate
  concern from the absence of calibration assessment and formal
  confidence intervals (see TRIPOD+AI table above).

## What this checklist is, and isn't

This is a self-assessment performed as part of this research program, not
an independent or peer review. It is intended to make gaps in reporting
rigor visible and explicit (per this project's standing principle of
honest limitation reporting) rather than to certify the study as complete
or publication-ready as-is.
