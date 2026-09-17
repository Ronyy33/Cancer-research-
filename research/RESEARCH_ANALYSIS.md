# Stage 15 — Research Analysis (Honest Synthesis)

**Date:** 2026-09-17
**Covers:** the full arc from Stage 1 (literature discovery) through Stage 14 (robustness/fairness), synthesized into one coherent narrative rather than left scattered across individual stage files.

## 1. What we set out to do, and what actually happened

The mandate (see chat history and `research/README.md`) was to find a
clinically meaningful, evidence-backed breast cancer problem where
existing AI approaches have a demonstrable limitation, and produce a
scientifically defensible improvement using real-world data. The process
was not linear, and that's worth recording honestly rather than
retconning a clean story:

1. **Literature review** (32 real papers, `research/LITERATURE_MATRIX.csv`)
   converged independently, via two separate research passes, on
   **recurrence/disease-free-survival prediction with genuine external
   validation** as the field's clearest gap (`RESEARCH_GAPS.md` Gap 3) —
   almost no published study validates a true prediction model (as
   opposed to a detection/extraction tool) across more than one
   institution or cohort.
2. **First dataset plan** (All of Us + pathologic complete response) was
   investigated and found infeasible — All of Us doesn't expose the
   pathology-report text pCR requires (D004).
3. **Second dataset plan** (All of Us + recurrence, via structured-data
   proxies) was assessed as feasible-but-risky (D006), then **abandoned
   entirely** when the human researcher's institution turned out not to
   be registered with All of Us (D007) — a real-world access constraint,
   not a modeling problem.
4. **Final dataset plan**: a deep, three-way parallel search for real,
   barrier-free alternatives converged on **Rotterdam (train) + GBSG2
   (external test)** as the primary pair, with **METABRIC** and
   **TCGA-BRCA** as independent secondary cohorts (D007). All four are
   real patient data, zero registration/cost/IRB barrier, and — critically
   — were then **actually pulled and directly verified** (not just cited
   from search snippets) in Stage 7.

This pivot history matters for interpreting everything downstream: the
project ended up studying recurrence-free survival using classic,
well-characterized clinical-trial/tumor-registry cohorts rather than a
genuine multi-visit EHR system. That's a real scope change from the
original ambition, driven by actual access constraints encountered along
the way, and it shapes every limitation discussed below.

## 2. What the data actually is (and isn't)

| Cohort | N | Real events | Role |
|---|---|---|---|
| Rotterdam | 2,982 | 1,713 (57.4%) | Primary training |
| GBSG2 | 686 | 299 (43.6%) | Primary external test |
| METABRIC | 1,873 (after excluding a documented incomplete batch) | 763 (40.7%) | Independent within-cohort cross-check |
| TCGA-BRCA | 799 | 74 (9.3%) | Secondary/exploratory only — confirmed unreliable in Stage 9 |

All four are **baseline-snapshot-plus-survival-time** datasets (features
recorded once at diagnosis/surgery, one follow-up clock to recurrence or
death), not genuine longitudinal multi-visit EHR data. This was
established as a structural fact about the public data landscape (three
independent searches in Stage 5/D007 confirmed no real, barrier-free,
truly longitudinal EHR dataset for this problem exists), not a shortcut
taken for convenience.

## 3. Key methodological findings, in the order they were discovered

1. **Structured recurrence labels are known to be unreliable in EHR
   settings generally** (Gap 2, from the literature: ICD-coded recurrence
   caught only 2.3% vs. 11.1% true recurrence in one well-verified study).
   Our chosen datasets sidestep this specific problem because Rotterdam/
   GBSG2/METABRIC/TCGA-BRCA all use trial-grade or registry-grade outcome
   ascertainment (not raw billing codes) — a genuine advantage of the
   final dataset choice, discovered as a side effect of the pivot away
   from EHR-code-based labels.
2. **A real .gitignore bug** was found and fixed during Stage 7 (an
   unanchored `data/` rule was silently excluding our own `src/data/`
   source code) — a reminder that infrastructure bugs can silently and
   invisibly compromise a project's actual state.
3. **A real cross-cohort unit mismatch** was found in Stage 8: Rotterdam/
   GBSG2 report survival time in days, METABRIC/TCGA-BRCA in months. Had
   this gone unnoticed, any cross-cohort comparison would have been
   silently wrong by a factor of ~30.
4. **A real, structured (non-random) missingness pattern** was found in
   METABRIC (Stage 8): ~528 patients simultaneously missing across ~12
   columns, traced directly to specific internal sub-cohort batches — not
   random dropout. Handled by explicit, documented exclusion using a
   reproducible rule, not silent imputation.
5. **A real numerical bug** was found and fixed in Stage 9: un-reduced
   one-hot encoding across multiple categorical blocks made the Cox
   model's design matrix exactly rank-deficient, crashing the solver.
   Fixed with `drop="first"`, and a regression test was added so it
   cannot silently recur.

Five real bugs/data-quality issues caught and fixed across the pipeline —
this is itself evidence that "verify before trust" (the standard set
early in this project) was substantively applied, not just stated as a
principle.

## 4. Modeling results, synthesized

**Cox Proportional Hazards is the recommended primary model**
(`research/PROPOSED_METHODOLOGY.md`), based on convergent evidence from
three independent real cohorts:

| Cohort | Cox PH | Best tree ensemble | Gap | Overfitting (train→test drop) |
|---|---|---|---|---|
| GBSG2 (genuine external test) | 0.654 | 0.672 (RSF) | 0.018 | Cox: 0.013 / RSF: 0.061 |
| METABRIC (within-cohort holdout) | 0.653 | 0.666 (RSF) | 0.013 | Cox: 0.008 / RSF: 0.043 |
| TCGA-BRCA (5-fold CV) | 0.494 | 0.534 (GBS) | both ≈ random | not a model-class issue — too few events (74) for any model |

Tree-based ensembles win by a small margin on raw discrimination but
overfit substantially more. This is not a one-off — it replicated across
two structurally different real cohorts (a genuine external test and an
independent within-cohort holdout), and it **independently reproduces a
finding already present in our own literature review**
(`research/PAPERS/P0027_cox_beats_deepsurv.md`: Cox beat DeepSurv on held-
out SEER data). That convergence — a pattern found in someone else's
published work, then independently rediscovered on our own data with our
own pipeline — is a meaningfully stronger form of evidence than either
result alone.

**Explainability** (Stage 13) reinforces confidence in the pipeline
rather than just decorating it: two independent methods (hazard ratios,
permutation importance) on two model classes (Cox PH, RSF) all converged
on the same three dominant predictors — positive lymph nodes, tumor size,
and grade — which are exactly the classic core prognostic factors in
breast cancer staging. The model rediscovered known clinical reality
rather than finding something spurious. Hormone therapy showed a
protective association (HR=0.880), also clinically consistent.

**Subgroup analysis** (Stage 14) found a genuinely important, non-trivial
weakness: discrimination is notably worse for patients with 1–3 positive
nodes (C-index 0.564, near chance) than for those with 4+ nodes (0.608) —
worse exactly in the clinically ambiguous population where a risk model
would matter most, since heavy nodal burden is already obviously
high-risk without one. This is the single most important limitation of
the current model, and it's a specific, actionable one (more/better
features for lower-nodal-burden patients specifically), not a vague
"more data would help."

## 5. How this compares to the field (per our own literature review)

- The pooled meta-analysis in our review (`P0007_lu_meta_analysis.md`)
  reported pooled c-index figures in the 0.77–0.86 range (with an
  internally-flagged discrepancy between two search passes) — noticeably
  higher than our 0.65–0.67. This is an honest, expected trade-off: our
  harmonized common feature schema deliberately strips both cohorts down
  to 8 mutually-comparable variables so genuine cross-cohort external
  validation is possible, whereas most published single-cohort studies
  use each cohort's full native feature set (often 10–20+ variables,
  sometimes including genomic/pathology-derived features) and are largely
  **not** externally validated at all (Gap 3). We are trading some raw
  discrimination for a real, honest external-validation story — exactly
  the trade the literature review identified as the field's biggest gap.
- The demographic/equity gap identified directly in a systematic review
  in our literature (`P0006_el_haji_systematic_review.md` — models
  predominantly validated on Caucasian/Asian populations) **could not be
  assessed at all** with our final dataset choice, since Rotterdam and
  GBSG2 are both European cohorts with zero race/ethnicity data. This is
  a real, structural limitation carried forward from the dataset-access
  pivot, not a new finding — but it means this project does not close
  that particular gap, and says so plainly.

## 6. Overall, honest conclusion

This research program produced a **real, externally-validated, honestly-
characterized recurrence-free-survival prediction pipeline** on real
patient data, built and verified end-to-end by directly touching the
data rather than trusting secondhand summaries. Its core positive
findings — (a) simple Cox regression is competitive with more complex
models here and far more stable, replicated across independent cohorts,
and (b) the model's internal reasoning matches known clinical prognostic
factors — are genuine, defensible contributions consistent with (and
independently reproducing) patterns already noted in the literature.

Its core limitations are equally real and are not being minimized: (1)
the achieved discrimination (C-index ~0.65) is modest and lower than some
richer-feature published models, a direct consequence of prioritizing
genuine cross-cohort comparability; (2) the model is weakest in the most
clinically useful subgroup (moderate nodal burden); (3) demographic
equity cannot be assessed with the current data; (4) none of the
datasets are genuinely longitudinal EHR data, so this does not yet
address the project's original, more ambitious framing of "real-world EHR
timeline modeling" — that remains blocked on institutional data access
that was not available during this research program.

## 7. What would be needed to go further

Stated explicitly, not left implicit:
1. Institutional access to a genuine longitudinal EHR resource (Flatiron,
   SEER-Medicare, or All of Us with institutional backing) to test whether
   the landmark-time multimodal architecture identified in the literature
   review (P0016) actually adds value over Cox PH once real timeline data
   is available — this project's evidence base does not yet support that
   architecture, precisely because the necessary data was never available
   to test it against.
2. Feature engineering specifically targeted at the moderate-nodal-burden
   subgroup identified as the model's weak point in Stage 14.
3. A dataset with demographic/socioeconomic variables to actually test
   (not just note the absence of a test for) the equity gap identified in
   the literature review.
