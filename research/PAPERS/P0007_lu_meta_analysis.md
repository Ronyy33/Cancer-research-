# P0007 — Lu et al. (2023) — Meta-Analysis of ML for Breast Cancer Recurrence

**Citation:** Lu Y, Long J, Fu C, Zhou X, et al. "Predictive value of machine learning for breast cancer recurrence: a systematic review and meta-analysis." *Journal of Cancer Research and Clinical Oncology* 2023;149:10659–10674.
**Link:** DOI 10.1007/s00432-023-04967-w · PubMed 37302114 · PMC11796809

**Scope:** PRISMA-style systematic review + meta-analysis, 34 studies, 67,560 subjects pooled, 8,695 recurrence events.

**Key findings:** Random forest was the most common top-performing model across included studies.

**⚠️ DATA DISCREPANCY — FLAGGED, NOT RESOLVED:** Two independent research passes on this same paper reported different pooled metrics from search snippets:
- Pass 1: pooled c-index (training) 0.863 (95% CI 0.834–0.892); pooled sensitivity/specificity ≈0.82.
- Pass 2: pooled c-index 0.814 (train) / 0.770 (validation); sensitivity/specificity 0.69/0.89 (train), 0.64/0.88 (validation).

Both passes agree on N=34 studies, 67,560 subjects, 8,695 events, and PROBAST bias assessment, so this is very likely the same paper — the metric discrepancy is most likely due to different search snippets quoting different tables/subgroups of the paper (e.g., different outcome definitions or model subsets), not two different papers. **This must be resolved against the actual full text before citing a specific pooled c-index number in any downstream writing.** WebFetch was blocked for both research passes this session.

**Interpretation regardless of which numbers are exact:** If the train→validation drop reported in Pass 2 is accurate (0.814→0.770), it is itself an honest signal of overfitting/generalization gap across the pooled field — consistent with our program's broader finding that few studies validate rigorously.

**Research gap it leaves open:** Aggregate literature has real volume (67,560 subjects across 34 studies) but individual studies mostly rely on curated clinicopathologic variables rather than messy real-world longitudinal EHR — benchmark performance is anchored on relatively clean cohorts.

**Relevance to our project:** ★★★★★ — primary quantitative benchmark for framing "what's already been achieved" in a future paper. **ACTION ITEM before citing:** verify the exact pooled c-index directly from the published paper (full-text access was blocked this session for both search passes).
