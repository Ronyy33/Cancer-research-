# Other Candidate Datasets — Summary Table

Investigated but each either has a hard access barrier requiring human/institutional action, or a structural limitation ruling it out for this project's current stage. Full detail available in the dataset-discovery agent transcript; key facts summarized here.

| Dataset | Real/Synth | Key facts (verified via search) | Longitudinal? | Access | Verdict |
|---|---|---|---|---|---|
| **NCDB** (National Cancer Database, ACS/CoC) | Real | Large US hospital-based registry; Participant User Files have stage, receptor status, granular treatment, comorbidity (Charlson-Deyo), vital status/survival. **Same core limitation as SEER: does not capture recurrence.** | Diagnosis + follow-up to death only (no recurrence) | Requires investigator affiliation with a CoC-accredited cancer program + formal annual PUF application | ★★☆☆☆ — STOP POINT (institutional access) |
| **Flatiron Health** | Real | Large (~3.4–6M+ patient records, ~220+ oncology practices), genuine longitudinal EHR-derived + chart-abstracted data: staging, biomarkers, treatment lines, labs, ECOG, real-world OS, **real-world PFS**. Structurally probably the best fit of anything found. | Yes — likely the most EHR-realistic longitudinal structure available | **Commercial licensing/partnership required**, pricing not public | ★★★★★ (structural fit) — STOP POINT (cost/commercial, likely prohibitive without institutional deal) |
| **Breast Cancer Surveillance Consortium (BCSC)** | Real | Mammography-screening registries; public-use datasets free, instant, no-login. But: no dates, no patient IDs, **no diagnosis/treatment/recurrence/survival-after-diagnosis data**. | No (screening events only, not post-diagnosis follow-up) | Fully public | ★☆☆☆☆ — accessible but wrong data shape |
| **curatedBreastData** (Bioconductor R package) | Real | Pooled/harmonized ~2,700 samples across 34 GEO microarray studies; harmonized survival/treatment-response variables (pCR, ER/HER2 status, stage). | Baseline covariates + single outcome per patient only | Fully public, free R/Bioconductor install | ★☆☆☆☆ — accessible but not a real timeline |
| **SCAN-B** (Sweden Cancerome Analysis Network-Breast) | Real | Large prospective population-based Swedish cohort (~12,000+ enrolled, 7,743–8,000+ RNA-seq profiled), integrated with Swedish national quality registries. RNA-seq public on GEO. Full clinical/outcome linkage does NOT appear openly public. | Structurally yes, but usable outcome linkage unconfirmed as public | Genomic data public; full clinical linkage likely requires formal collaboration with Lund University | ★★☆☆☆ — STOP POINT for the clinically useful part |
| **TriNetX** | Real | Federated real-world EHR network, ~70 healthcare orgs / 100M+ patients; built-in temporal cohort-definition and outcome tools. No dataset exported — analysis happens on-platform. | Structurally yes, on-platform only | Requires researcher's institution to be a TriNetX network member (subscription/contract) | ★★☆☆☆ — STOP POINT (institutional membership) |
| **UCI/Wisconsin Breast Cancer datasets** | Real | Well-known small diagnostic/cytology datasets; classic set has no follow-up; older small Prognostic set (~198 patients) has limited time-to-recurrence but dated/single-institution. | No (single timepoint or trivially small/dated) | Fully public | ✩ Unsuitable |
| **CPRD** (UK Clinical Practice Research Datalink) | Real (known to exist) | Longitudinal UK primary+secondary care EHR including cancer patients. **Not independently verified this session** — no dedicated search run. | UNKNOWN — not verified this session | Known generally to require a formal, paid protocol-approval (ISAC) process | UNKNOWN ranking — flag for future investigation if needed |

## Explicit STOP-and-ask list (requires human decision: credentials, IRB, payment, or institutional access)

- **SEER-Medicare** — formal DUA + documented IRB approval + processing fee.
- **NCDB** — requires investigator affiliation with a CoC-accredited cancer program.
- **Flatiron Health** — commercial licensing/partnership agreement, no public pricing.
- **TriNetX** — requires the researcher's institution to be a network member.
- **SCAN-B** (full clinical linkage) — requires formal collaboration with Lund University-led consortium.
- **METABRIC raw sequencing data (EGA)** — controlled access, only needed if raw sequence data required (not needed for the curated clinical+expression data, which is public).
- **TCGA controlled-tier raw sequence files (dbGaP)** — only needed if raw BAMs required (not needed for open-tier clinical/expression data).
- **All of Us Registered/Controlled Tier** — requires a real human's personal identity verification (photo ID), which an AI agent cannot perform.
- **CPRD** — known generally to require a paid, formal protocol/ISAC approval process.

## Realistically autonomously accessible (no human-only step beyond routine account creation)

- **SEER Research Data** (SEER*Stat) — self-service click-through DUA, no IRB, no fee.
- **TCGA-BRCA open tier** (GDC Portal / cBioPortal) — no login required.
- **METABRIC via cBioPortal** (clinical + expression) — fully public, no login.
- **I-SPY2 via TCIA** — public collection; free self-service TCIA/NBIA account.
- **curatedBreastData** (Bioconductor) — straightforward package install.
- **BCSC public-use datasets** — free, instant download (limited use for this project per ranking above).
