# P0004 — González-Castro et al. (2023) — Structured vs. Unstructured EHR for 5-Year Recurrence

**Citation:** González-Castro L, et al. "Machine Learning Algorithms to Predict Breast Cancer Recurrence Using Structured and Unstructured Sources from Electronic Health Records." *Cancers* 2023;15(10):2741.
**Link:** DOI 10.3390/cancers15102741 · https://www.mdpi.com/2072-6694/15/10/2741 · PMC10216131

**Clinical problem:** Predict 5-year breast cancer recurrence, comparing structured registry/EHR fields, NLP-derived features from unstructured clinical reports, and their combination.

**Dataset/cohort:** Hospital EHR cohort (Spain, GRADIANT/University of Vigo research group; source hospital not named in available sources), N=823 after preprocessing.

**Features:** Structured/semi-structured EHR fields + NLP-extracted features (TNM/biomarker fields recovered from free text).

**Target:** 5-year recurrence (binary). Exact operational definition/index point not confirmed.

**Methodology:** 5 ML algorithms compared; XGBoost best.

**Results:** XGB precision 0.900, recall 0.907, F1 0.897 (best modality combination). Combined structured+unstructured beat either single modality.

**Limitations:** Small N (823) for a rare outcome; validation strategy (CV vs. held-out vs. external) not confirmed from available sources — the high precision/recall without confirmed cross-validation is a genuine optimism-bias risk; fragmented EHR data and systematic missingness noted.

**Leakage concerns:** Cannot rule out leakage without confirming exact prediction-time cutoff relative to the 5-year outcome window.

**Reproducibility:** Not assessed (code/data availability not verified).

**Research gap it leaves open:** The clearest explicit-horizon design found in this search, but on a small single-institution cohort with unconfirmed validation rigor — exactly the kind of study that needs replication at scale with proper external/temporal validation.

**Relevance to our project:** ★★★★★ — most directly on-point paper to the structured-vs-unstructured EHR ablation question in the project brief (Section 19). Should inform our own ablation design (Models A–F).
