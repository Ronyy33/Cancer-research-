# Experiment 0004 — Robustness / Fairness Subgroup Analysis (Stage 14)

**Date:** 2026-09-17
**Script:** `scripts/subgroup_analysis.py`
**Model:** Cox PH fit on full Rotterdam (N=2,982), evaluated on GBSG2 (external test, N=686) — the primary model from `research/PROPOSED_METHODOLOGY.md`

## Method

Per project brief Section 23: evaluate performance across subgroups
**where sample size permits** (minimum N=30 and minimum 10 events per
subgroup — subgroups failing this threshold are reported as
"insufficient sample," not silently included with an unstable estimate).
All defined subgroups met this threshold this time — none were excluded.

## Results

| Subgroup | N | Events | C-index | Mean predicted risk | Observed event rate |
|---|---|---|---|---|---|
| Age <50 | 268 | 106 | 0.644 | 0.109 | 0.396 |
| Age 50-64 | 326 | 157 | 0.648 | 0.177 | 0.482 |
| Age 65+ | 92 | 36 | 0.714 | 0.216 | 0.391 |
| Menopause: pre | 290 | 119 | 0.647 | 0.101 | 0.410 |
| Menopause: post | 396 | 180 | 0.658 | 0.196 | 0.455 |
| **Grade 1 (out-of-distribution for training)** | 81 | 18 | **0.660** | -0.095 | 0.222 |
| Grade 2 | 444 | 202 | 0.620 | 0.071 | 0.455 |
| Grade 3 | 161 | 79 | 0.694 | 0.517 | 0.491 |
| Hormone therapy: no | 440 | 205 | 0.631 | 0.196 | 0.466 |
| Hormone therapy: yes | 246 | 94 | 0.686 | 0.084 | 0.382 |
| **Nodes 1-3** | 376 | 119 | **0.564** | -0.125 | 0.316 |
| Nodes 4+ | 310 | 180 | 0.608 | 0.496 | 0.581 |

(Overall external C-index, whole GBSG2 cohort: 0.654 — matches experiment_0001.)

## Two findings worth flagging directly, not glossed over

### 1. The model performs notably WORSE for patients with lower nodal burden (1-3 positive nodes)

C-index **0.564** for the 1-3-node subgroup vs. **0.608** for the 4+-node
subgroup, both below the overall 0.654. This is the most clinically
important finding in this analysis: **discrimination is weakest in
exactly the population where risk stratification arguably matters most**
— patients with heavy nodal involvement (4+ nodes) are already understood
clinically to be higher-risk almost regardless of a model's output, while
patients with only 1-3 positive nodes are a genuinely more clinically
ambiguous group where a good risk model could change management
decisions. The likely mechanism (not independently verified further
here): per `experiment_0003.md`'s permutation importance findings, nodal
count dominates this model's predictions; within a narrower nodal-count
band, the model has comparatively less other discriminating information
to work with. **This is reported as a real limitation of the current
feature set for exactly the subgroup where it matters most, not
downplayed.**

### 2. The grade-1 subgroup (flagged as out-of-distribution in experiment_0001) performed reasonably well

C-index 0.660 for grade-1 patients — comparable to, even slightly better
than, grade-2 (0.620), despite Rotterdam (the training data) containing
zero grade-1 patients. This is a genuinely reassuring finding given the
limitation flagged earlier (`src/data/harmonize.py` docstring,
`experiment_0001.md`): the model's inability to have learned a specific
grade-1 coefficient did not translate into materially worse
discrimination for those patients in practice, at least on this measure.
This should NOT be over-read as "the limitation doesn't matter" — the
sample is small (N=81, 18 events, right at this analysis's minimum
threshold) and calibration (not just ranking/discrimination) for this
subgroup was not separately assessed.

## Other subgroup observations (smaller effects, noted for completeness)

- Age 65+ shows the highest subgroup C-index (0.714), though this is also
  the smallest subgroup (N=92) — noted, not over-interpreted given the
  smaller sample.
- Patients who received hormone therapy show better discrimination
  (0.686) than those who did not (0.631) — a modest difference.

## ⚠️ Honest limitation stated directly, not silently skipped

**Rotterdam and GBSG2 are both European cohorts (Netherlands, Germany)
with no race, ethnicity, or socioeconomic variables available at all.**
This means the demographic/equity gap directly documented in our own
literature review (`research/RESEARCH_GAPS.md` Gap 4 — El Haji et al.
2023's systematic review found existing recurrence models are
predominantly trained/validated on Caucasian and Asian populations, with
African and Middle Eastern populations largely absent) **cannot be
assessed or addressed at all with the datasets currently in this
project.** This is a real, structural limitation of the current dataset
choice, not an oversight in this analysis — flagged here explicitly so
it isn't quietly forgotten by the time of any eventual paper-stage
writeup.

## Next step

Stage 15: honest research synthesis pulling together experiments 0001-0004
into a single coherent narrative — including the nodal-subgroup weakness
and the demographic-data gap as explicit limitations, not just the
headline external-validation C-index numbers.
