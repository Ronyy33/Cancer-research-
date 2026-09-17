# Related Work

A structured literature review (`research/LITERATURE_MATRIX.csv`,
`research/RESEARCH_GAPS.md`) examined 32 papers spanning seed studies on
distant-recurrence identification from electronic health records
(`P0001`–`P0003`, `P0005`, `P0008`–`P0011`), systematic reviews and
meta-analyses of machine learning for breast cancer recurrence prediction
(`P0006`, `P0007`), recent (2024–2026) work on treatment-response
prediction, clinical NLP, and LLM-based information extraction, and
methodological comparisons between classical and deep survival models.
Literature discovery relied on web search rather than full-text retrieval
(an environment-level network restriction encountered throughout this
project), a limitation stated explicitly wherever it affects confidence
in a specific claim.

## Detection versus prediction

A recurring finding across the reviewed literature is the conflation of
recurrence *detection* (determining, from a full retrospective chart,
whether a documented recurrence event exists) with recurrence
*prediction* (forecasting a future event from information available only
up to a defined index time). Several influential papers in this space
(`P0001`, `P0005`, `P0009`–`P0011`) are, on close reading, detection or
information-extraction tools — valuable for cohort curation and registry
completeness, but not directly comparable to a genuine forecasting task.
This distinction, made explicit in project design (`research/
cohort_definition.md`), motivated restricting the present study to a
formally defined recurrence-free-survival endpoint with features locked
at a fixed index time.

## Label quality

Karimi et al. (`P0005`) found that natural-language-processing–derived
recurrence identification captured 11.1% of a breast cancer cohort as
recurrent, versus only 2.3% via ICD coding alone — independently
corroborated during this project's own literature synthesis. A directly
published critique of that same study (Ritzwoller, Hassett & Uno, `P0008`)
further noted that NLP-based recurrence cohorts are frequently pre-
enriched via structured high-risk codes, undermining claims of general-
population applicability and cross-institution portability. The present
study sidesteps the specific labeling problem these papers describe by
using trial-grade and tumor-registry-grade outcome ascertainment
(Rotterdam, GBSG2, METABRIC, TCGA-BRCA) rather than raw structured EHR
codes — though this substitution brings its own limitation, discussed
below and in `docs/limitations.md`.

## External validation

A pooled meta-analysis of 34 studies (Lu et al., `P0007`; 67,560 subjects,
8,695 recurrence events) reported strong aggregate discrimination
(pooled c-index estimates varied between the two independent literature-
review passes conducted for this project, in the range 0.77–0.86; this
discrepancy is flagged directly in `research/PAPERS/
P0007_lu_meta_analysis.md` as unresolved pending full-text verification).
Both that review and a separate systematic review of statistical and
machine-learning recurrence models (El Haji et al., `P0006`) note that
individual constituent studies are rarely validated outside their
development cohort, and that reported performance often degrades
substantially between training and validation splits even within a single
study. El Haji et al. additionally document a demographic generalizability
gap: existing models are predominantly trained and validated on Caucasian
and Asian populations, with African and Middle Eastern populations largely
absent from the literature.

## Model complexity versus classical methods

A directly relevant comparative study identified during the literature
review (unnamed authors, SEER cohort, HER2-positive/HR-negative subgroup)
found that classical Cox proportional hazards outperformed a deep
learning survival model (DeepSurv) on held-out test data, despite the
deep model's higher training-set discrimination
(`research/PAPERS/P0027_cox_beats_deepsurv.md`). This finding — that
model complexity does not reliably translate into better generalization
in this problem domain — is directly and independently reproduced in the
present study's own experiments (`research/EXPERIMENTS/experiment_0001.md`,
`experiment_0002.md`), strengthening confidence in the pattern beyond a
single external citation.

## Positioning of this study

Relative to this literature, the present study's contribution is
methodological rather than architectural: it does not introduce a novel
model, but instead constructs a genuine, real-data, multi-cohort external
validation design (train on Rotterdam, validate on GBSG2, cross-check on
two further independent cohorts) directly targeting the external-
validation gap identified above, while empirically testing — rather than
assuming — whether model complexity beyond Cox regression is warranted
for this specific feature set and data scale.
