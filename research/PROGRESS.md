# Progress Log

## 2026-09-09 — Session 1

**COMPLETED**
- Repository scaffold: directory structure, `.gitignore` (no raw clinical data/secrets ever committed), core tracking files
- Literature discovery + synthesis: 3 parallel research passes (seed-paper citation chaining; recent 2024-2026 landscape scan across all candidate problem areas; dataset feasibility investigation), yielding:
  - `LITERATURE_MATRIX.csv` — 32 verified papers with structured fields (dataset, N, target, validation, metrics, leakage risk, research gap, star rating)
  - 8 detailed paper notes in `PAPERS/` for the highest-value sources, including one flagged internal metric discrepancy (P0007) left unresolved rather than silently picking a number
  - `RESEARCH_GAPS.md` — 8 evidence-backed gaps, each with supporting sources and a stated confidence level
  - `DATASETS/` — 6 individual dataset files (SEER, MIMIC/eICU, TCGA-BRCA, METABRIC, I-SPY2, All of Us) + 1 summary table covering 9 more candidates (NCDB, Flatiron, BCSC, curatedBreastData, SCAN-B, TriNetX, UCI sets, CPRD)
  - `CANDIDATE_RESEARCH_QUESTIONS.md` — 4 candidate research questions scored across 8 criteria, with an explicit recommendation
  - `LEAKAGE_AUDIT.md` — pre-emptive audit of leakage patterns observed in the literature + hard requirements for our own future pipeline

**IN PROGRESS**
- Nothing actively running; session paused at the Stage 4/5 → Stage 6 human-decision checkpoint, as required by the project brief.

**FAILED**
- WebFetch (full-text retrieval) was blocked for the entire session across all three research agents and every domain tested (PubMed, PMC, journal publishers, arXiv, Google Scholar, even Wikipedia as a control). All literature findings are therefore built from WebSearch result snippets, not independently-read full text. This is flagged in every paper note and dataset file where it affects confidence. If a future session has WebFetch access, prioritize re-verifying: the P0007 metric discrepancy, exact validation methodology for P0002/P0005/P0013, and full-text read of P0023 (the longitudinal-EHR scoping review, content not retrieved this session).

**BLOCKED**
- Stage 6 (dataset acquisition) cannot proceed until the human researcher decides: (1) which candidate research question to commit to, and (2) which dataset to pursue first — several of the strongest-fit datasets (Flatiron, SEER-Medicare, TriNetX, All of Us Controlled Tier) require human-only action (payment, IRB, institutional membership, or identity verification) that cannot be completed autonomously.

**NEXT STEP**
- Await Kevin's decision from the RESEARCH CHECKPOINT (delivered in chat this session). Once a research question + dataset are approved, proceed autonomously to Stage 7 (cohort construction) without further stop-and-ask, per the routine-work autonomy rule (Section 33).

**DECISION MADE (D003, 2026-09-09):** Kevin selected treatment response/pCR
prediction as the research question, and All of Us as the first dataset —
see `DECISIONS.md` D003. This was a deliberate, more ambitious pairing than
the checkpoint's matched recommendation (pCR+I-SPY2, recurrence+All of Us),
flagged accordingly.

## 2026-09-09 — Session 2 (continued)

**COMPLETED**
- Logged decision D003 in `DECISIONS.md`
- Updated `RESEARCH_STATE.md` to Stage 6, with a clear split between what's
  blocked on Kevin (All of Us identity verification) vs. what proceeds
  autonomously
- Added explicit "what Kevin needs to do" access instructions to
  `DATASETS/all_of_us_omop.md`
- Drafted `cohort_definition.md` for the pCR prediction task (index date,
  prediction time, observation window, outcome, censoring, inclusion/
  exclusion) — conceptual, pending data-access confirmation

**IN PROGRESS**
- Feasibility investigation (background agent) into whether All of Us can
  actually support (a) identifying a neoadjuvant-chemotherapy cohort and
  (b) ascertaining pCR/treatment response — this specific pairing was not
  verified in the original dataset-discovery pass and carries real risk

**BLOCKED**
- All of Us data access itself — requires Kevin's personal photo-ID identity
  verification (see `DATASETS/all_of_us_omop.md` for exact steps). No
  cohort can be built against real All of Us data until this is done.

**NEXT STEP**
- Once the feasibility check returns: if All of Us + pCR looks viable,
  finalize `cohort_definition.md` and prepare pilot query/cohort-building
  notebooks for Kevin to run once his Workbench access is active. If not
  viable as-is, present a revised recommendation (e.g., fall back to I-SPY2,
  or keep All of Us but change the specific outcome) before proceeding
  further, since this would be a research-design change significant enough
  to warrant checking back in.

**DECISION REQUIRED FROM KEVIN (superseded below by D004 — see updated ask)**

## 2026-09-09 — Session 2 (continued further): feasibility check returned NOT FEASIBLE

**COMPLETED**
- Feasibility investigation completed: All of Us cannot support pCR
  ascertainment as specified (HIGH confidence). Full findings appended to
  `DATASETS/all_of_us_omop.md`; decision logged as D004 in `DECISIONS.md`.

**BLOCKED**
- Study design decision: whether to (a) fall back to I-SPY2 for pCR
  prediction as originally recommended, (b) keep All of Us but change the
  outcome to something structurally supportable, or (c) pursue a hybrid.
  This is a consequential research-design change and is being put back to
  Kevin rather than decided autonomously, per project brief Section 33.
- All of Us Registered Tier registration + identity verification is STILL
  a live action item for Kevin regardless of which option is chosen, since
  option (b) and the hybrid option (c) both still need it; only pure
  option (a) would make it unnecessary for now.

**NEXT STEP**
- Present revised checkpoint to Kevin with the three options above and a
  recommendation (fall back to I-SPY2). Await his decision before any
  further cohort-design or data-engineering work specific to a dataset.

## 2026-09-09 — Session 2 (continued): reverted to recurrence, EHR required (D005)

**COMPLETED**
- Kevin redirected the research question back to recurrence/relapse
  prediction with an explicit EHR-native dataset requirement. Logged as
  D005 in `DECISIONS.md`. All of Us remains the only free, EHR-native
  candidate (Flatiron is commercial, SEER-Medicare needs DUA+IRB+fee).

**IN PROGRESS**
- Feasibility check (background agent) on the narrower question: can
  recurrence be detected from All of Us STRUCTURED data alone (diagnosis
  codes, treatment-restart patterns), without needing free-text pathology
  reports (the specific thing that ruled out pCR in D004). This is a
  different, more tractable signal than pCR and has precedent elsewhere
  (SEER-Medicare claims-based recurrence-proxy algorithms).

**NEXT STEP**
- Await feasibility check; update `cohort_definition.md` for a recurrence
  target once confirmed, and revise `DATASETS/all_of_us_omop.md` and
  `RESEARCH_STATE.md` accordingly.

## 2026-09-09 — Session 2 (continued further): recurrence feasibility confirmed MEDIUM, cohort v2 drafted (D006)

**COMPLETED**
- Feasibility check returned: recurrence detection from All of Us
  structured data is feasible as a gated pilot (MEDIUM confidence), not
  blocked like pCR was, but with a real care-capture-completeness risk
  (quantified via a 2026 claims-linkage comparison study). Logged as D006.
- Rewrote `cohort_definition.md` (v2) around a time-to-event/censored
  design with a combined multi-signal recurrence-proxy algorithm and a
  mandatory manual validation gate before cohort-scale modeling.
- Updated `DATASETS/all_of_us_omop.md` and `LEAKAGE_AUDIT.md` with the
  full findings and the resulting label-noise mitigation strategy.
- This was treated as routine methodology work (same question, same
  dataset as D005) and completed autonomously; Kevin was informed of the
  finding directly in chat rather than stopped for another decision.

**BLOCKED**
- All of Us Registered Tier access (Kevin's identity verification) — still
  the only real blocker. Once active, the concrete pilot steps in
  `DATASETS/all_of_us_omop.md` are ready to run (check Oncology Module
  population, C77-C79 code completeness, pilot the proxy algorithm, run
  the manual validation gate).

**NEXT STEP**
- Nothing further can proceed on this dataset until Kevin's All of Us
  access is active. In the meantime, could start Stage-9-adjacent prep
  work (baseline model scaffolding in `scripts/`/`configs/`) that doesn't
  require real data, if useful — otherwise session is idle pending Kevin's
  access or further direction.

## 2026-09-09 — Session 2 (continued further): All of Us abandoned, multi-dataset real-data plan adopted (D007)

**COMPLETED**
- Kevin reported his institute isn't registered with All of Us — access
  blocked regardless of his own ID verification. Redirected to a deep,
  multi-hour, 3-agent parallel search for a real, barrier-free dataset.
- All three searches independently confirmed: All of Us, NSABP/dbGaP, and
  UK Biobank are all institution-gated in practice, and no real,
  barrier-free, genuinely multi-visit EHR dataset exists publicly for
  this task. Treated as a confirmed structural constraint, not a search
  failure.
- **Adopted a multi-dataset real-data design (D007):** Rotterdam (n=2,982,
  train) + GBSG2 (n=686, external validation, 43.6% event rate) as the
  primary pair — a citable, established train/external-validate
  methodology (Royston & Altman 2013; standard DeepSurv/pycox benchmark
  split). METABRIC (~2,509) and TCGA-BRCA (~1,098) as secondary
  cross-validation cohorts. Duke-Breast-Cancer-MRI (922, event rate TBD)
  as an optional richer-feature/multimodal arm.
- All five datasets are immediately, freely accessible — no registration,
  institution, fee, or IRB required.
- Wrote `DATASETS/rotterdam_gbsg2.md` and `DATASETS/duke_breast_cancer_mri.md`.
- Rewrote `cohort_definition.md` (v3) around the multi-dataset design —
  genuinely lower leakage risk than the All of Us plan, since these
  datasets were purpose-built for survival analysis with proper censoring.
- Updated `RESEARCH_STATE.md`: **nothing is currently blocked.**

**NEXT STEP**
- Begin Stage 7: actually load/verify the real data (Rotterdam via R
  `survival` package, GBSG2 via CRAN/scikit-survival, METABRIC/TCGA-BRCA
  via cBioPortal, Duke via TCIA), confirm fields match documentation,
  verify Duke's exact recurrence event rate, then proceed to Stage 8 data
  quality analysis. This can proceed autonomously as routine engineering
  work per project brief Section 33.

**DECISION REQUIRED FROM KEVIN**
- None currently blocking. Kevin should sanity-check the multi-dataset
  design (rather than one big EHR source) matches what he wants before
  Stage 7 engineering goes deep — flagged in chat, proceeding unless
  redirected.

## 2026-09-16 — Session 3: Stage 7 data loading, all datasets directly verified

**COMPLETED**
- Kevin confirmed the multi-dataset plan and asked to continue.
- Set up Python environment (`.venv`, `requirements.txt`: pandas, numpy,
  scikit-survival, lifelines, scikit-learn, xgboost, shap, matplotlib,
  seaborn, pyyaml, requests, pytest) and installed R (`r-base-core`) for
  authoritative access to Rotterdam.
- **All 4 real datasets pulled from authoritative sources and directly
  verified** - a genuine upgrade from every earlier dataset claim this
  session, which was necessarily sourced from WebSearch snippets since
  WebFetch was blocked all session:
  - Rotterdam: pulled directly from R's `survival` package
    (`scripts/pull_rotterdam.R`). N=2,982 confirmed exactly. Recurrence-
    free-survival event rate = 1,713/2,982 = 57.4%.
  - GBSG2: loaded via `sksurv.datasets.load_gbsg2()`. N=686 confirmed.
    Event rate = 299/686 = 43.6% (matches earlier search-sourced figure
    exactly).
  - METABRIC: pulled from cBioPortal's public GitHub datahub mirror
    (main cBioPortal site is blocked by this environment's network
    policy; the GitHub mirror serves identical authoritative files) via
    `scripts/pull_metabric_tcga.sh`. N=2,509 confirmed. RFS event rate =
    1,002/2,488 valid = 40.3%.
  - TCGA-BRCA (PanCancer Atlas 2018): same mirror. N=1,084 confirmed
    (resolves earlier ~1,084-1,098 ambiguity). DFS event rate =
    84/942 valid = **8.9% — notably lower than the other three**,
    flagged clearly in `DATASETS/tcga_brca.md` as a real limitation
    (best used as a smaller cross-check, not primary training data).
- Built `src/data/loaders.py` with a loader per dataset, all standardized
  to `rfstime`/`rfs_event` columns for interchangeable use.
- Built `tests/test_loaders.py` - 5/5 passing, checks real shapes and
  sane event-rate ranges (not brittle exact-match assertions), plus a
  placeholder leakage-awareness check ahead of the full Stage 8 audit.
- Updated `DATASETS/rotterdam_gbsg2.md`, `DATASETS/metabric.md`,
  `DATASETS/tcga_brca.md` with "VERIFIED DIRECTLY" sections.
- Raw data files confirmed NOT tracked by git (`.gitignore` working as
  intended) - only code, tests, and docs are committed.

**NEXT STEP**
- Stage 8: real data quality analysis (missingness, distributions,
  outliers, cross-cohort variable harmonization e.g. receptor-status
  cutoffs across eras) on all 4 cohorts, output to
  `research/RESULTS/data_quality/` and `research/FIGURES/data_quality/`.
- Then Stage 9: baseline models (majority class, Cox/Elastic-Net Cox,
  Random Survival Forest, XGBoost-survival) trained on Rotterdam,
  externally validated on GBSG2, cross-checked on METABRIC/TCGA-BRCA.

## 2026-09-16 — Session 3 (continued): Stage 8 data quality analysis complete

**COMPLETED**
- Kevin confirmed Python stack and "verify before trust," asked to
  continue to next stage.
- Built `src/data/quality.py` (reusable missingness/duplicate/numeric/
  categorical/implausible-value checks) and
  `scripts/data_quality_analysis.py` (runs all checks + KM survival
  curves on all 4 cohorts).
- Ran it for real. Key findings:
  - **Rotterdam + GBSG2**: zero missingness, zero duplicates, zero
    implausible values — clean trial-quality data as expected. Rotterdam
    has no grade-1 patients at all (real cohort characteristic).
  - **METABRIC**: found a real, structured (non-random) missingness
    block of ~528-529 patients simultaneously missing across ~12
    columns. Investigated directly and confirmed this traces to
    specific internal `COHORT` batches (1, 7, 8, 9) — a genuine MNAR
    pattern requiring an explicit handling decision before modeling,
    not naive imputation. Documented options in `SYNTHESIS.md`.
  - **TCGA-BRCA**: `WEIGHT` column 100% empty (drop it); real 13.1% DFS
    censoring gap on top of the already-low 8.9% event rate — reinforces
    treating it as a secondary cross-check cohort.
  - **CRITICAL cross-cohort issue found**: Rotterdam/GBSG2 report
    survival time in **days**, METABRIC/TCGA-BRCA in **months** — flagged
    clearly before any pooled/cross-cohort comparison happens; the KM
    overlay plot is explicitly labeled as not-yet-harmonized to avoid
    a misleading chart.
  - Also flagged: cross-cohort variable coding differences (grade,
    receptor status, nodal status) that need documented harmonization
    rules before Stage 9's cross-cohort validation.
- Wrote `research/RESULTS/data_quality/{rotterdam,gbsg2,metabric,
  tcga_brca,SYNTHESIS}.md` and 7 figures in
  `research/FIGURES/data_quality/`. Sent key figures to Kevin.

**NEXT STEP**
- Stage 9: baseline models. First resolve the METABRIC batch-missingness
  decision and the cross-cohort time-unit harmonization (both required
  before cross-cohort validation, not optional polish), then build
  Kaplan-Meier baseline, Cox/Elastic-Net Cox, Random Survival Forest, and
  XGBoost-survival models trained on Rotterdam, externally validated on
  GBSG2, cross-checked on METABRIC and TCGA-BRCA (secondary weight).

## 2026-09-16 — Session 3 (continued): Stage 9 baselines, experiment_0001

**COMPLETED**
- Kevin confirmed both pending decisions (exclude METABRIC's incomplete
  batch; harmonize time units to months) and asked to continue.
- Built `src/data/harmonize.py`: converts Rotterdam/GBSG2 time from days
  to months, and maps their differently-coded columns to a common
  8-feature schema (age, nodes, ER/PR values, menopause, tumor-size
  bucket, grade, hormone therapy). Documented every mapping decision
  inline, including the deliberate exclusion of chemo (not comparably
  available in GBSG2's released columns) and the honest handling of
  GBSG2's 81 grade-1 patients (kept in the test set, not dropped to
  inflate performance, since Rotterdam has none to train on).
- Built `scripts/train_baselines.py` and ran it for real.
  **Found and fixed a genuine bug along the way**: un-reduced one-hot
  encoding across 4 categorical blocks made the Cox PH design matrix
  exactly rank-deficient (each block's dummies sum to a constant
  1-vector; with no intercept term to absorb it, multiple such blocks
  collide) - crashed with "ill-conditioned matrix" / NaN search
  direction. Fixed with `drop="first"`, added a regression test
  (`tests/test_harmonize.py::test_onehot_encoding_does_not_crash_coxph`)
  so it can't silently recur.
- **Results (experiment_0001, Rotterdam train → GBSG2 external test,
  Harrell's C-index):** Cox PH 0.654, Elastic-Net Cox 0.646, Random
  Survival Forest 0.672 (best raw score), Gradient Boosting Survival
  0.669.
- **Key honest finding:** RSF's higher raw score comes with 4.5x more
  overfitting than Cox PH (train→external gap 0.061 vs 0.013) - a
  direct, self-generated instance of the same pattern found in our own
  literature review (P0027: Cox beat DeepSurv on held-out data). Written
  up as a real argument for preferring the simpler, more stable model
  per the project's First Principle, not just noted in passing.
- Added `tests/test_harmonize.py` (5 new tests, all passing; 10/10 total
  across the test suite).
- Documented the full run in `research/EXPERIMENTS/experiment_0001.md`
  per the project's experiment-tracking requirement (Section 25) -
  dataset version, features, hyperparameters, seed, validation strategy,
  results, and explicit limitations of this first baseline pass.

**NEXT STEP**
- Add METABRIC (own within-cohort baseline, since its native features
  differ from Rotterdam/GBSG2's harmonized schema) and TCGA-BRCA
  (secondary, low-event-rate cross-check) as further real-data
  validation points.
- Then Stage 10: given how close Cox PH already comes to the tree-based
  models with far better stability, assess whether a more complex
  proposed methodology is actually justified before building one for
  its own sake (per Section 1's core principle).

## 2026-09-16 — Session 3 (continued): experiment_0002, Stage 9 complete

**COMPLETED**
- Built `scripts/train_metabric_tcga.py`: METABRIC evaluated within-cohort
  (80/20 holdout + 5-fold CV) after excluding the Stage-8-identified
  incomplete batch using the exact reproducible missingness rule (not a
  COHORT-number heuristic, since COHORT=1 spans both complete and
  incomplete groups). TCGA-BRCA evaluated via 5-fold CV only (too few
  events for a further holdout split).
- **METABRIC (N=1,873, 40.7% events):** Cox PH 0.653 holdout, RSF 0.666,
  GBS 0.665 — a second independent real cohort showing the same pattern
  as Rotterdam/GBSG2 (tree models modestly ahead, Cox PH close behind
  with far less train/test divergence).
- **TCGA-BRCA (N=799, only 74 events/9.3%): CV-mean C-index 0.49-0.53
  across all three models — essentially indistinguishable from random
  chance**, despite deceptively high training scores (0.58-0.73) from
  the tree-based models on this same small cohort. Reported plainly as
  an honest negative result (project brief Section 28) confirming the
  earlier decision to treat TCGA-BRCA as secondary/exploratory only.
- Documented in `research/EXPERIMENTS/experiment_0002.md`, explicitly
  scoped as within-cohort evaluation, NOT external validation of the
  Rotterdam-trained model (different feature sets - would be
  methodologically wrong to conflate the two).
- **Stage 9 (baseline modeling) is now complete** across all 4 real
  cohorts.

**NEXT STEP**
- Stage 10: three independent real cohorts (Rotterdam/GBSG2 pair +
  METABRIC) now converge on the same finding - Cox PH is competitive
  with tree ensembles and substantially more stable. Assess honestly
  whether this means a more complex proposed methodology (e.g. a
  landmark-time neural architecture per P0016/Multimodal BEHRT) is
  actually justified, or whether a well-specified Cox model is the
  right, defensible answer for this feature set and these cohort sizes
  - per the project's core principle (Section 1) of preferring simpler
  models when they're sufficient.

## 2026-09-17 — Session 3 (continued): Stage 10 methodology decision + Stage 13 explainability

**COMPLETED**
- **Stage 10:** Wrote `research/PROPOSED_METHODOLOGY.md`. Decision: Cox
  PH is the primary model. Evidence table across 3 cohorts shows a
  consistent, small (0.013-0.018) performance gap vs. tree ensembles
  with 3-5x less overfitting each time - not a one-off result. Explicitly
  considered and rejected a landmark-time neural architecture (the
  strongest exemplar from our own literature review, P0016/Multimodal
  BEHRT) because it requires genuine multi-visit EHR trajectories that
  none of our real, barrier-free datasets have - a data-shape constraint,
  stated as such, not a modeling-effort shortcut. Conditions that would
  justify revisiting this decision are stated explicitly (institutional
  EHR access, larger gap under future feature engineering, or a specific
  nonlinear sub-question), so this isn't a permanent, unexamined default.
- **Stage 13:** Built `scripts/explainability.py`. Two complementary,
  model-agnostic-comparable methods on Rotterdam (75/25 held-out split):
  Cox PH's native hazard ratios, and permutation importance (Cox PH vs
  RSF, same method for both so they're fairly comparable).
  **Finding: positive lymph nodes, tumor size, and grade dominate across
  BOTH methods AND both model classes** - four independent analytical
  angles converging on the same answer. This matches real, established
  breast cancer prognostic factors (the TNM/Nottingham Prognostic Index
  backbone cited throughout our own literature review) - a genuine
  sanity check that the pipeline found real clinical signal, not
  spurious correlations. Hormone therapy showed a protective association
  (HR=0.880), also clinically consistent. Explicit
  association-not-causation framing throughout (Section 24).
  Documented in `research/EXPERIMENTS/experiment_0003.md`, sent 2
  figures to Kevin.

**NEXT STEP**
- Stage 14: robustness/fairness - check whether the predictive pattern
  holds consistently across age groups and other subgroups where sample
  size permits (project brief Section 23 - do not manufacture subgroup
  analyses when sample sizes are inadequate).
- Then Stage 15 (research analysis / honest synthesis) and Stage 16
  (paper-ready output) to close out the modeling arc.
