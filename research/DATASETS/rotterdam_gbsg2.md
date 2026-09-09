# Dataset: Rotterdam Breast Cancer Cohort + GBSG2 (paired train/external-validate)

**Real or synthetic:** Both REAL patient cohorts.

## Rotterdam (Rotterdam Tumour Bank)

- **N = 2,982** real patients who had surgery for primary breast cancer, 1978–1993 (verified across multiple independent CRAN/package sources).
- **Variables:** age, tumor size, tumor grade, number of positive lymph nodes, hormonal treatment, ER/PR receptor status.
- **Outcome:** Genuine time-to-event structure — `rfstime` (days to first of recurrence/death/last follow-up) and `recur` (1=relapse, 0=no relapse), separately `dtime`/`death` for overall survival. Standard practice combines these into a recurrence-free survival endpoint (`rfstime = pmin(rtime, dtime)`, `status = pmax(recur, death)`).
- **Access: zero barrier.** Ships built directly into R's core `survival` package (`survival::rotterdam`) — no download, no registration, no DUA. Also via the `OncoDataSets` CRAN package.
- **License:** Standard R core package license (GPL), freely redistributable for research.
- **Longitudinal depth:** Baseline snapshot at surgery + one follow-up survival-time clock. NOT multi-visit repeated-measures EHR data — this is an honest structural limitation shared by every real, zero-barrier dataset found in this search.

## GBSG2 (German Breast Cancer Study Group 2)

- **N = 686** real patients, node-positive breast cancer, from a randomized 2×2 trial of hormonal treatment and chemo duration (Schumacher et al., J Clin Oncol 1994).
- **Variables:** age, menopausal status, tumor size, tumor grade, number of positive nodes, hormonal therapy, progesterone receptor, estrogen receptor.
- **Outcome:** Recurrence-free survival time + censoring indicator. **299/686 (43.6%) experienced the event** — a healthy, well-balanced event rate for modeling.
- **Access: zero barrier.** CRAN packages `TH.data`, `pec`, `casebase`, `LongCART`; also `sksurv.datasets.load_gbsg2` in Python's scikit-survival, and bundled in `pycox`/DeepSurv benchmark code.
- **License:** Freely redistributable via CRAN/scikit-survival.
- **Longitudinal depth:** Same baseline-snapshot-plus-survival-time structure as Rotterdam.

## Why this pairing is unusually strong for our purposes

This exact **train-on-Rotterdam, externally-validate-on-GBSG2** split is not something we'd be inventing — it is a **named, citable methodology** in the biostatistics literature:

- Royston & Altman, "External validation of a Cox prognostic model: principles and methods," *BMC Medical Research Methodology* 2013;13:33 — develops a prognostic model on Rotterdam and externally validates on GBSG2, with a reproducible CRAN vignette.
- It is also the standard benchmark split in modern deep-survival-model literature: Katzman et al.'s DeepSurv paper (2018) and its descendants (`pycox`, `DeepSurvK`) use a 1,546-patient node-positive Rotterdam subset for training and the full 686-patient GBSG2 as the external test set.

This directly answers the single most repeated finding across our entire literature review (`RESEARCH_GAPS.md` Gap 3): the field's biggest, most consistent weakness is the near-total absence of genuine external validation. Using this pairing means our project has real external validation built in from day one, using an established, citable design rather than an ad hoc split.

## Usefulness for this project

Combined N = 3,668 across two independent real cohorts, both with genuine time-to-event recurrence-free survival data and healthy event rates, zero access barrier, and a built-in external-validation story. This is the strongest real, immediately-usable option found across all three deep-search passes.

**Limitation to carry forward honestly:** both cohorts are 1980s–1990s era (treatment patterns and receptor-status testing methods have evolved since); neither is genuinely longitudinal/multi-visit EHR data — it's baseline-plus-outcome, same limitation as METABRIC and every other real, zero-barrier dataset examined in this research program.

**Ranking: ★★★★★** — for a real, zero-barrier, well-powered, methodologically-precedented recurrence prediction + external validation study.
