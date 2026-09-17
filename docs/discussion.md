# Discussion

## Model complexity was not empirically justified for this problem

The central empirical finding of this study is negative in the most
useful sense: across three independent real cohorts, evaluated under two
different validation designs (genuine external test, independent
within-cohort holdout), classical Cox regression achieved external
performance within 0.013–0.018 C-index of the best-performing tree-based
ensemble, while showing 3–5 times less degradation between training and
test performance. This is not a marginal or ambiguous result — it
replicated in both structurally different validation settings used in
this study, and it independently reproduces a comparison already present
in the literature reviewed for this project (Cox outperforming DeepSurv
on held-out SEER data). Taken together, this constitutes a reasonably
strong basis for recommending Cox PH as the default model for this
feature set and data scale, rather than a more complex architecture
selected because it is available in the literature or because it achieves
marginally higher in-sample performance.

This finding should not be over-generalized to breast cancer prediction
problems broadly. It applies specifically to the feature scale examined
here (eight harmonized clinical variables) and to cohorts of the size and
composition studied. A materially larger feature set — particularly one
incorporating genomic, imaging, or genuinely longitudinal treatment-
response data — could plausibly shift this balance toward models capable
of capturing higher-order interactions. The point is not that complex
models are never warranted, but that their use should be justified by
demonstrated performance on held-out data specific to the problem at
hand, which is the standard this study attempted to apply to itself.

## The model reproduces known clinical knowledge, which is reassuring but limited

That two independent explainability methods, applied to two different
model classes, converge on positive lymph node count, tumor size, and
histologic grade as dominant predictors is a meaningful internal
consistency check: these are the established core components of breast
cancer staging, and their emergence from a model that had no access to
staging labels directly is evidence the pipeline is capturing real
clinical signal rather than artifacts of the harmonization or
preprocessing steps. This should be read as validation of the modeling
process, not as a novel clinical finding — the prognostic importance of
nodal status, size, and grade is long established and is not a
contribution of this study.

## The subgroup finding is the most clinically actionable result of this study

Reduced discrimination among patients with one to three positive lymph
nodes (C-index 0.564) is a more specific and more actionable finding than
the model's aggregate performance. Patients with heavy nodal involvement
are already recognized as high-risk on clinical grounds largely
independent of a statistical model; patients with minimal nodal
involvement are comparatively low-risk without much ambiguity. It is the
intermediate group — one to three positive nodes — where individualized
risk stratification could most plausibly influence a treatment or
surveillance decision, and it is exactly this group where the present
model is least discriminating. A plausible explanation, consistent with
the permutation-importance findings, is that nodal count itself carries
most of this model's predictive weight; within a narrow nodal-count band,
the remaining seven features provide comparatively little additional
separation. Testing this explanation, and identifying features that
specifically improve discrimination within this subgroup, is a natural
direction for follow-up work rather than a conclusion supported by the
present analysis.

## Achieved discrimination is modest relative to some published work, by design

The C-index values obtained here (approximately 0.65 for the primary
external validation) are lower than pooled or single-study estimates
reported elsewhere in the literature (up to 0.77–0.86 in the meta-
analysis reviewed for this project). This is an expected consequence of
methodological choices made deliberately in this study: an eight-feature
schema constructed specifically for cross-cohort comparability, rather
than each cohort's full native feature set, and genuine external
validation rather than in-sample or single-cohort evaluation, which this
project's own literature review found to be rare in comparable published
work. Higher published discrimination figures should not be read as
directly comparable without accounting for whether they reflect the same
validation rigor.

## What this study does not establish

This study makes no claim about genuinely longitudinal, repeated-measures
electronic health record data, since none was available within its
scope — the original, more ambitious framing of this research program
(see `research/README.md` and the decision log in `research/
DECISIONS.md`) targeted exactly that kind of data, and the pivot to
registry/trial-grade cohorts was a response to a specific, documented
access constraint rather than a methodological preference. Nor does this
study assess demographic or socioeconomic equity, since no available
cohort contained the relevant variables — a limitation inherited from
both the dataset-access constraint encountered in this project and a
gap already documented in the broader literature. Both limitations are
discussed further in `docs/limitations.md`.
