# P0006 — El Haji et al. (2023) — Systematic Review of Recurrence Risk Prediction Models

**Citation:** El Haji H, Souadka A, Patel BK, Sbihi N, Ramasamy G, Patel B, Ghogho M, Banerjee I. "Evolution of Breast Cancer Recurrence Risk Prediction: A Systematic Review of Statistical and Machine Learning–Based Models." *JCO Clinical Cancer Informatics* 2023.
**Link:** DOI 10.1200/CCI.23.00049 · PubMed 37566789 · PMC11771520

**Scope:** Systematic review of statistical + ML breast cancer recurrence risk prediction models published 2008–2022.

**Key findings:**
- ML models show strong performance but limited interpretability and reduced generalizability.
- Predictive models often use a narrow feature set (tumor/treatment/molecular/clinical), rarely full longitudinal EHR.
- Imbalanced classes and lack of open-source datasets impede development/validation.
- **Explicit, citable equity gap:** existing models are predominantly trained/validated on Caucasian and Asian populations; African and Middle Eastern populations are largely overlooked.

**Notable lineage:** Co-authored by Imon Banerjee, also a co-author on P0003 (Sanyal) and P0005 (Karimi) — this reviewing group has direct hands-on experience building the exact type of model it is reviewing.

**Research gap it leaves open (evidence for RESEARCH_GAPS.md):**
1. Demographic/geographic generalizability gap (confirmed directly, not inferred).
2. Narrow feature sets vs. full longitudinal EHR — an opportunity for a study using richer data.
3. Interpretability limitations of ML models in this space.

**Relevance to our project:** ★★★★★ — primary landscape-mapping reference; the equity gap finding should directly inform subgroup/fairness analysis planning (Stage 14) and cohort diversity considerations if we get to choose our data source.
