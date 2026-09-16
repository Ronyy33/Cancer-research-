# Dataset: TCGA-BRCA (The Cancer Genome Atlas — Breast Cancer) / GDC

## ✅ VERIFIED DIRECTLY — 2026-09-16

Actually pulled and inspected this session (`scripts/pull_metabric_tcga.sh`,
PanCancer Atlas 2018 study, via cBioPortal's GitHub datahub mirror):
- **N = 1,084** confirmed exactly (resolves the earlier ~1,084-1,098
  ambiguity across secondhand sources — this is the real, current count).
- **DFS_STATUS** (Disease Free Status): 858 disease-free, **84
  recurred/progressed**, 142 missing → event rate **8.9%** of valid
  records — **much lower than Rotterdam (57.4%), GBSG2 (43.6%), or
  METABRIC (40.3%)**. This matters: with only 84 real events, statistical
  power for TCGA-BRCA alone is limited; best used as a smaller
  cross-validation/robustness check rather than a primary training set.
- **PFS_STATUS** (Progression Free Status): 145 progression events/1083
  valid (13.4%) — a somewhat larger event pool if progression (rather
  than strict recurrence) is used as the outcome instead.
- **OS_STATUS**: 933 living, 151 deceased.
- Real columns confirmed present: AJCC stage (T/N/M), subtype, ethnicity,
  race, radiation therapy, new tumor event indicator, genetic ancestry
  label — genomic data available separately via the same datahub source
  if a molecular-augmentation arm is pursued later.

**Real or synthetic:** Real, NCI/NHGRI (Genomic Data Commons), mirrored at cBioPortal.

**Patient count:** Reported as ~1,084–1,098 patients depending on cohort release (original Nature 2012 publication ~1,098 with a comparable count for PanCancer Atlas; GDC recompute figures vary slightly across sources) — exact current figure has minor discrepancies across sources; best-available consensus ≈1,098 cases in the current GDC TCGA-BRCA project.

**Variables:** Primarily genomic (whole-exome sequencing, RNA-seq, methylation, copy-number variation, RPPA proteomics) + whole-slide pathology images. Clinical data is comparatively thin: AJCC stage, histologic subtype, grade, ER/PR/HER2 (as originally reported, not uniformly re-verified against current standards), demographics, vital status.

**Outcome/follow-up:** The **TCGA Pan-Cancer Clinical Data Resource (TCGA-CDR, Liu et al. 2018, Cell)** harmonizes overall survival (OS), disease-specific survival (DSS), disease-free interval (DFI), and progression-free interval (PFI) endpoints across TCGA cohorts including BRCA — a real recurrence-adjacent endpoint (DFI/new-tumor-event), better than base SEER in this one respect. However, TCGA enrollment/follow-up largely concluded ~2013–2015, so follow-up is comparatively short and BRCA event counts (recurrences, deaths) are small given the cohort skews toward earlier-stage disease.

**No structured labs, medications, or clinical notes** — not EHR-like; a genomics/pathology-centric snapshot with limited baseline clinical covariates, not a longitudinal EHR trajectory.

**Longitudinal structure:** Limited — index date (diagnosis/surgery) + time-to-event outcome via TCGA-CDR, but small N and low event counts limit statistical power for a robust recurrence classifier.

**Access:** Clinical + most molecular data = **open tier, no login required**, freely downloadable (GDC Portal, cBioPortal). Raw sequence-level files (BAMs) = controlled tier requiring dbGaP authorization (Data Access Committee) — **not needed** for a clinical/expression-only prediction task.

**License:** NIH Genomic Data Sharing Policy; open tier freely reusable with citation; controlled tier governed by NIH Genomic Data User Code of Conduct.

**IRB:** Not required for open-tier data use.

**Usefulness for this project:** Has DFI/PFI recurrence-adjacent endpoints and real follow-up via TCGA-CDR, but small N (~1,098), few events, short follow-up, genomics-centric with thin clinical variables. Could serve as a genomics-augmentation arm alongside a primarily-clinical/EHR dataset, but is not sufficient alone for a well-powered EHR-native prediction study.

**Ranking: ★★★☆☆** — realistically and immediately accessible (no STOP point for the open tier), but structurally limited by small N and thin clinical covariates.
