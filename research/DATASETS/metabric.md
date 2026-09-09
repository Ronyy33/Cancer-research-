# Dataset: METABRIC (Molecular Taxonomy of Breast Cancer International Consortium)

**Real or synthetic:** Real, UK + Canada breast cancer molecular cohort (5 hospitals/centers), ~2,509 patients with clinical observations, 1,980 with gene expression profiles.

**Variables confirmed:** age at diagnosis, tumor size/grade/stage, lymph node status, ER/PR/HER2 status, PAM50 molecular subtype, Nottingham Prognostic Index, type of breast surgery (mastectomy vs. breast-conserving), treatment flags (chemo/hormone/radiotherapy), **overall survival (OS) time+status**, and **relapse-free survival (RFS) time+status — 1,403 of 2,509 patients (55.9%) experienced a recurrence event** (directly confirmed via search — a genuinely well-powered recurrence-type endpoint, notably better than SEER or TCGA in this respect).

**No structured labs, medication dosing, vitals, or clinical notes** — baseline-covariates-plus-outcome design, not a multi-timepoint EHR trajectory.

**Longitudinal structure:** Single baseline index (diagnosis/surgery) + real elapsed time-to-event follow-up (reportedly up to decades for some patients) — supports a genuine "predict future event from information available at diagnosis" design (classic survival/ML time-to-event modeling), though NOT a dynamic multi-timepoint feature stream like a true EHR.

**Missingness:** Not independently characterized this session.

**Access:** Processed clinical + genomic summary data — **fully public via cBioPortal, no login/registration required**, direct TSV/tarball download (confirmed). Raw sequencing/genotyping data is separately hosted at **EGA under controlled access** (Data Access Committee application) — **not needed** if only using the cBioPortal curated clinical+expression data.

**License:** Reuse per original publication terms (Curtis et al. 2012 *Nature*; Pereira et al. 2016 *Nat Commun*) — generally permissive for research with citation; EGA raw data governed by a formal Data Access Agreement.

**IRB:** Not required for the public cBioPortal clinical+expression data.

**Usefulness for this project:** The strongest **immediately, fully autonomously accessible** dataset with a genuine, well-powered recurrence endpoint found in this search. Well suited to classic survival/ML time-to-event modeling and baseline-feature ablations, but not to true longitudinal/dynamic EHR modeling (no multi-timepoint clinical trajectory, no notes, no labs).

**Limitations:** Not EHR-native (no labs/meds/notes); single-baseline design; UK/Canada 1990s–2000s cohort — dated relative to current treatment standards (may limit clinical relevance of the treatment variables to current practice).

**Ranking: ★★★★☆** — real, well-powered recurrence/OS endpoints, fully public, moderate size; best combination of access-ease and label quality found.
