# Limitations

Stated directly and specifically, per this project's standing requirement
to report limitations honestly rather than minimize them.

## Data shape

None of the four cohorts used in this study contains genuinely
longitudinal, repeated-measures clinical data. Every cohort is a
baseline-snapshot-plus-survival-time design: features are recorded once,
at or near diagnosis or surgery, and a single follow-up clock tracks time
to recurrence, death, or censoring. This was confirmed as a structural
property of the real, barrier-free public data landscape via three
independent searches during dataset selection (`research/DECISIONS.md`
D007), not a convenience choice. It means this study cannot speak to
whether models that exploit repeated encounters over time (e.g., the
landmark-time transformer architecture identified as the strongest
exemplar in this project's literature review, `research/PAPERS/
P0016_multimodal_behrt.md`) would outperform the classical approach used
here — that architecture requires data this study did not have access
to, and no claim is made about its relative performance.

## Demographic and socioeconomic equity could not be assessed

Rotterdam and GBSG2 (the primary train/external-test pair) are both
European cohorts from the 1980s–1990s with no race, ethnicity, or
socioeconomic variables recorded. METABRIC and TCGA-BRCA include some
demographic fields, but were not used for the primary predictive-
performance claims of this study. This means the demographic
generalizability gap directly identified in this project's own literature
review (existing recurrence models predominantly trained and validated on
Caucasian and Asian populations) is neither addressed nor newly
demonstrated by this study — it is a pre-existing gap in the available
data that this project's dataset-access constraints did not allow it to
close.

## Achieved discrimination is modest

The primary external validation C-index (0.654) indicates meaningful but
imperfect risk discrimination. This is not a calibration failure — model
calibration (whether predicted risk translates to correct absolute
probabilities, as distinct from correct relative ranking) was not
formally assessed in this study and should be evaluated before any
clinical-facing use of these results.

## Reduced feature set relative to native cohort data

The eight-feature harmonized schema used for the primary Rotterdam→GBSG2
comparison deliberately excludes variables available in one cohort but
not comparably available in the other (notably chemotherapy status,
present in Rotterdam but not released comparably in GBSG2's public data).
This benefits cross-cohort comparability at a direct cost to potential
predictive performance; a model using each cohort's full native feature
set would likely, though not necessarily, achieve higher in-sample
discrimination, at the cost of the cross-cohort validation this study
prioritized.

## Grade-1 patients are out-of-distribution for the trained model

Rotterdam, the training cohort, contains zero grade-1 tumors. The 81
grade-1 patients in the GBSG2 external test set were retained (not
excluded) and evaluated with a feature encoding the model was never
trained to represent for that category. Subgroup analysis found this
group's discrimination was not obviously worse than other subgroups
(C-index 0.660), which is reassuring but should not be read as
definitive given the subgroup's small size (N=81, 18 events) and the
fact that only discrimination, not calibration, was assessed for this
subgroup.

## TCGA-BRCA is not a reliable evaluation cohort at its current usable sample size

Only 74 of 799 complete-case TCGA-BRCA patients (9.3%) experienced a
recorded recurrence/progression event. Cross-validated performance for
every model class tested was statistically indistinguishable from chance
on this cohort. TCGA-BRCA results in this study should not be interpreted
as evidence about model performance; they are retained and reported as a
methodologically important negative finding (a genuine test of whether
this dataset can support reliable inference at its current filtered
sample size, which it cannot) rather than removed from the record.

## Reduced discrimination in a clinically important subgroup

Discrimination among patients with one to three positive lymph nodes
(C-index 0.564) was close to chance level, despite acceptable overall
external performance. Any application of this specific model to that
subgroup should account for its substantially reduced reliability there.

## Full-text literature verification was not possible

Literature review for this project relied on web search rather than
full-text retrieval, due to a network access restriction present
throughout the research environment used. Numeric claims sourced from the
literature are flagged as search-snippet-derived throughout `research/
LITERATURE_MATRIX.csv` and `research/PAPERS/`, including one specific,
unresolved discrepancy in a cited meta-analysis's pooled performance
figures (`research/PAPERS/P0007_lu_meta_analysis.md`).

## No prospective or real-world clinical validation

All validation in this study is retrospective. No claim is made, or
should be inferred, about this model's performance in prospective
clinical use, nor has any regulatory, IRB, or clinical-deployment
pathway been pursued or is implied by this work.
