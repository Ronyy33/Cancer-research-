# Abstract

**Background.** Machine learning models for breast cancer recurrence
prediction are rarely validated across more than one institution or
cohort, and studies claiming to "predict" recurrence frequently instead
detect recurrence already documented in retrospective records — a
distinction that matters for clinical utility but is often not made
explicit.

**Objective.** To develop and externally validate a recurrence-free
survival prediction model for breast cancer using exclusively real,
publicly accessible patient-level data, and to determine empirically
whether model complexity beyond classical survival regression is
justified for this problem.

**Methods.** We trained Cox proportional hazards, elastic-net Cox, random
survival forest, and gradient boosting survival models on the Rotterdam
tumor bank cohort (N=2,982) and externally validated on the GBSG2 cohort
(N=686) — a train/external-test pairing with precedent in the
biostatistics literature. Two further independent real cohorts, METABRIC
(N=1,873) and TCGA-BRCA (N=799), were used as additional within-cohort
cross-checks. A harmonized 8-feature schema was constructed across
cohorts with differing native variable coding, with every mapping
decision documented. Explainability (hazard ratios, permutation
importance) and subgroup robustness analyses were performed on the
selected primary model.

**Results.** External validation (Rotterdam→GBSG2) concordance index was
0.654 for Cox PH versus 0.672 for random survival forest — a small
margin achieved at the cost of 4.5-times greater train-to-test
performance degradation for the ensemble model. This pattern replicated
independently on METABRIC (Cox PH 0.653 vs. RSF 0.666). TCGA-BRCA, with
only 74 real recurrence events, showed cross-validated performance
indistinguishable from chance (C-index 0.49–0.53) across all model
classes, confirming it as unsuitable for reliable inference at its
current usable sample size. Explainability analysis identified positive
lymph node count, tumor size, and histologic grade as the dominant
predictors across both hazard-ratio and permutation-importance methods
and both model classes — consistent with established breast cancer
prognostic factors. Subgroup analysis identified reduced discrimination
(C-index 0.564) specifically among patients with 1–3 positive lymph
nodes, the clinically intermediate-risk group in which risk
stratification is arguably most consequential.

**Conclusions.** For this feature set and cohort scale, classical Cox
regression achieved external validation performance close to more
complex alternatives while showing substantially better stability,
supporting its use as the primary model rather than defaulting to a more
complex architecture. Demographic and socioeconomic equity could not be
assessed, as no cohort used in this study included such variables — a
limitation directly traceable to a dataset-access constraint encountered
during this research program (see Limitations) and inherited from the
broader field. No genuinely longitudinal electronic health record data
was available within the scope of this program; all four cohorts are
baseline-snapshot-plus-survival-time designs, which bounds the
applicability of these findings to more dynamic, repeated-measures
clinical data.
