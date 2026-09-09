# P0016 — Multimodal BEHRT (2024/2025) — Transformer for Breast Cancer Prognosis

**Citation:** "Multimodal BEHRT: Transformers for Multimodal Electronic Health Records to predict breast cancer prognosis." medRxiv preprint 2024.09.18.24312984 → published *Frontiers in Oncology* 2025;15:1496215.
**Link:** PubMed 41179659 · PMC12575146 · https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2025.1496215/full

**Clinical problem:** Predict 3-year disease-free survival using only the first year of post-surgery EHR trajectory (a genuine landmark-time design).

**Dataset/cohort:** ~15,000 breast cancer patients on adjuvant chemotherapy, real EHR (source institution not confirmed from available sources).

**Features:** Sequential patient trajectories up to 1 year post-surgery — labs, medical department/procedure codes, structured features ("Tabular BEHRT"), and free-text report content ("Text BEHRT"), fused into "M-BEHRT."

**Target/prediction design:** Disease-free survival status at 3 years, predicted from information available only through 1 year post-surgery — **this is one of the few genuinely correct landmark/prediction-time designs found across both literature searches** (features locked before the outcome window, not mixed with post-outcome information).

**Methodology:** BEHRT-style transformer, pretrained with a masked-trajectory objective on censored+uncensored patients, fine-tuned for classification. Baselines: Nottingham Prognostic Index (NPI), Random Forest.

**Results:** M-BEHRT AUC-ROC 0.77 [0.70–0.84] vs. NPI/RF 0.67 [0.58–0.75] (p<0.05); unimodal Tabular-BEHRT and Text-BEHRT each ~0.75 individually.

**Limitations:** Single AUC point estimate with wide confidence intervals; **no external-site validation reported**; DFS ground-truth ascertainment method (manual review vs. ICD-coded vs. NLP-derived) not specified — this matters enormously given P0005's finding that coded recurrence under-counts true recurrence by ~5x. If the DFS label here is coded rather than NLP/manually verified, the reported AUC could be optimistic or biased in an unknown direction.

**Reproducibility:** Not assessed (code/data availability not verified).

**Research gap it leaves open:** Combines correct temporal design + multimodal fusion + beats a validated clinical baseline, but lacks external validation and label-provenance transparency — precisely the two things a follow-up study should add.

**Relevance to our project:** ★★★★★ — **the single strongest architectural exemplar found in this literature search.** If we pursue longitudinal/multimodal modeling (project brief Section 20), this is the closest published template to replicate and extend (adding external validation + a verified NLP-derived label).
