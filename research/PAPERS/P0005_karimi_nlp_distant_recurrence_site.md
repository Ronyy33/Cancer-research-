# P0005 — Karimi et al. (2021) — NLP for Distant Recurrence Status + Site

**Citation:** Karimi YH, Blayney DW, Kurian AW, Shen J, Yamashita R, Rubin D, Banerjee I. "Development and Use of Natural Language Processing for Identification of Distant Cancer Recurrence and Sites of Distant Recurrence Using Unstructured Electronic Health Record Data." *JCO Clinical Cancer Informatics* 2021;5:469-478.
**Link:** DOI 10.1200/CCI.20.00165 · PubMed 33929889

**Clinical problem:** Structured EHR/claims fields don't reliably capture recurrence status or site; builds an NLP framework to classify both from unstructured EHR text.

**Dataset/cohort:** Stanford EHR, breast cancer + hepatocellular carcinoma cohorts, N≈1,273 (breast+HCC combined, per independent verification).

**Target:** Recurrence status + specific anatomic site (multi-class), retrospective — this is INFORMATION EXTRACTION/DETECTION, not prediction.

**Results:** Breast distant-recurrence detection AUC=0.98 (95% CI 0.96–0.99); site-of-recurrence mean accuracy ≈0.90.

**⭐ MOST IMPORTANT FINDING FOR THE WHOLE PROGRAM:** NLP identified recurrence in **11.1%** of the breast database vs. only **2.31%** via ICD coding alone. This ~5x gap, independently confirmed by two separate research passes, means **any project that builds a recurrence label purely from structured/coded EHR fields will have a badly under-ascertained, biased label.** A credible EHR-based recurrence-prediction project needs an NLP- or manually-abstracted outcome label, not a coded one.

**Limitations / critique:** Directly critiqued by Ritzwoller, Hassett & Uno (P0008) — the cohort was pre-selected for high recurrence likelihood using structured codes before NLP was applied, so the sample is enriched/non-representative, and reported performance may not generalize to an unselected population. NLP models are also less portable across institutions (documentation style varies).

**Reproducibility:** Not assessed.

**Research gap it leaves open:** Cohort-enrichment bias in NLP recurrence studies is under-scrutinized; label quality for "recurrence" from EHR remains a first-order methodological risk for any downstream prediction study.

**Relevance to our project:** ★★★★ — critical for cohort/label design (Stage 7–8), not for modeling architecture. Read alongside P0008 before finalizing an outcome-label strategy.
