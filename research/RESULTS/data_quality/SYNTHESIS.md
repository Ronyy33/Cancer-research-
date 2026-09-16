# Stage 8 — Data Quality Synthesis (across all 4 cohorts)

**Date:** 2026-09-16. See per-dataset reports (`rotterdam.md`, `gbsg2.md`,
`metabric.md`, `tcga_brca.md`) for full detail. This file summarizes the
findings that actually matter for how we build the cohort and model in
Stage 9+.

## 1. Rotterdam + GBSG2: clean, trial-quality data

Both have **zero missingness, zero duplicates, zero implausible values**
across every checked column. This is expected — both are curated trial/
tumor-bank datasets with mandatory field completion, unlike routine-care
EHR data. Some numeric columns (nodes, pgr, er, estrec, progrec, tsize)
have IQR-flagged "outliers," but these are real, expected right-skew in
clinical concentration/count variables (e.g. receptor fmol values,
positive-node counts), not data errors — confirmed by inspecting the
actual max values (e.g. Rotterdam `pgr` max=5004, `er` max=3275 — high
but clinically plausible receptor concentrations, not impossible values).

**Real cohort characteristic to note:** Rotterdam's `grade` column only
contains values 2 and 3 (no grade 1 patients at all) — not a data error,
just how this cohort was assembled. Any model trained on Rotterdam alone
will have zero training signal for grade-1 tumors.

## 2. METABRIC: real, structured (non-random) missingness tied to sub-cohort batch

**This is the most important finding of Stage 8.** ~528-529 patients are
simultaneously missing across ~12 different columns (CELLULARITY,
BREAST_SURGERY, menopausal state, molecular subtype, HER2 status, hormone/
chemo/radio therapy flags, vital status, OS_MONTHS). This is **not random
missingness (MCAR)** — we confirmed it directly: these missing rows cluster
almost entirely in METABRIC's internal `COHORT` batches 1, 7, 8, and 9,
while batches 2, 3, 4, 5 are essentially complete. METABRIC pooled multiple
sub-studies/sequencing batches with different levels of clinical annotation,
and this shows up as a real, structural missingness pattern, not noise.

**Action required before Stage 9 modeling:** do not impute these columns
as if missingness were random - that would introduce bias. Options to
decide before baseline modeling:
(a) restrict primary METABRIC analysis to the well-annotated cohort
    batches only, documenting the resulting smaller N, or
(b) keep all patients but treat "missing due to batch" as its own
    informative category for categorical features (valid, since the
    missingness itself may correlate with era/protocol, which can
    matter clinically) rather than imputing a point estimate, or
(c) use only the columns/patients that are complete for the specific
    comparison being made.
Recommendation for Stage 9: start with (a) for baseline modeling
simplicity, explicitly report the excluded batch's size and outcome
distribution (188 recur / 309 not-recur within the block, which is NOT
wildly different from the overall 40.3% rate — so excluding the block is
unlikely to introduce large outcome-distribution bias, though it may
still bias the *feature* distributions if those batches differ
systematically in other ways not yet checked).

**Also noted, lower severity:** `ER_IHC` category is spelled "Positve"
(typo) in the source data — real source-data quirk, must be matched
exactly when filtering/encoding, not "corrected" silently in a way that
diverges from the source file.

## 3. TCGA-BRCA: empty column + real DFS censoring gap

- **`WEIGHT` column is 100% missing (1084/1084)** — completely unusable,
  should simply be dropped rather than imputed.
- **DFS_STATUS/DFS_MONTHS missing for 142/1084 (13.1%)** — a real
  censoring/follow-up gap on top of the already-low 8.9% event rate
  documented in `DATASETS/tcga_brca.md`. Combined, this reinforces the
  earlier recommendation to treat TCGA-BRCA as a secondary cross-check
  cohort, not a primary training set.
- 12 male patients present (SEX=Male) — consistent with
  `cohort_definition.md`'s planned exclusion criterion (male breast
  cancer excluded as a separate clinical question).
- `PATH_N_STAGE` has one occurrence of a nonstandard code
  (`N0 (MOL+)`) — a minor source-coding quirk to be aware of during
  categorical encoding, not an error requiring correction.

## 4. ⚠️ CRITICAL cross-cohort issue: time units are NOT the same

- **Rotterdam and GBSG2** report survival time in **days**
  (`rfstime`/`rtime`/`dtime` — e.g. Rotterdam max ~7043, GBSG2 max
  ~2659).
- **METABRIC and TCGA-BRCA** report survival time in **months**
  (`RFS_MONTHS` max ~389, `DFS_MONTHS` max ~281).

**This must be harmonized (e.g. convert Rotterdam/GBSG2 days → months, or
everything → a common unit) before any cross-cohort comparison or pooled
analysis.** The Stage 8 KM overlay plot
(`FIGURES/data_quality/cross_cohort_km_overlay.png`) is explicitly
labeled as NOT yet harmonized for exactly this reason — do not interpret
that plot's x-axis as comparable across cohorts as currently rendered.
This will be fixed in the Stage 7/9 feature-engineering step before any
modeling.

## 5. Cross-cohort variable harmonization needed (Stage 9 prerequisite)

Beyond time units, the four cohorts use different codings for
conceptually similar variables that will need explicit mapping before a
pooled or cross-validated model can use them consistently:
- Grade: Rotterdam/GBSG2 use numeric 1/2/3 (Rotterdam has no grade 1);
  no direct grade field confirmed yet checked in METABRIC/TCGA in this
  pass (histologic grade may need to be sourced from a different column
  or may not be directly comparable — flagged for Stage 9 feature
  engineering, not assumed compatible).
- Receptor status: Rotterdam/GBSG2 give continuous fmol values (pgr/er,
  estrec/progrec) with no explicit positive/negative cutoff applied;
  METABRIC gives categorical ER_IHC (Positive/Negative); TCGA gives
  receptor status via its SUBTYPE field (BRCA_LumA/LumB/Her2/Basal/
  Normal) rather than a direct ER/PR/HER2 binary. These are NOT
  trivially interchangeable and will need a documented harmonization
  rule, not a naive rename.
- Nodal status: Rotterdam/GBSG2 give a raw positive-node count; TCGA
  gives AJCC pathologic N-stage (a categorical bucket, e.g. N0/N1A/N2...).
  Converting between these requires a documented, defensible mapping.

## Summary table

| Cohort | N | Missingness | Duplicates | Implausible values | Time unit | Primary quality concern |
|---|---|---|---|---|---|---|
| Rotterdam | 2,982 | None | None | None | days | Grade 1 absent from cohort |
| GBSG2 | 686 | None | None | None | days | None significant |
| METABRIC | 2,509 | ~21% block-missing (batch-dependent) | None | None | months | MNAR missingness tied to sub-cohort batch — needs explicit handling |
| TCGA-BRCA | 1,084 | WEIGHT 100%, DFS 13.1% | None | None | months | Low event rate (8.9%) + real censoring gap — secondary cohort only |

**Bottom line for Stage 9:** Rotterdam/GBSG2 are ready to model as-is.
METABRIC needs a documented decision on the batch-missingness block before
inclusion. TCGA-BRCA should proceed as a secondary/robustness cohort, not
weighted equally with the other three, given its much lower event count.
All cross-cohort time units must be harmonized before any pooled or
cross-validated comparison.
