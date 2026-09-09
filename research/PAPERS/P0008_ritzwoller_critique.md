# P0008 — Ritzwoller, Hassett & Uno (2022) — Critique of NLP-Based Recurrence Identification

**Citation:** Ritzwoller DP, Hassett MJ, Uno H. "Regarding the Utility of Unstructured Data and Natural Language Processing for Identification of Breast Cancer Recurrence." *JCO Clinical Cancer Informatics* 2022.
**Link:** DOI 10.1200/CCI.21.00091 · PMC9848577

**What this is:** An invited commentary/letter responding directly to Karimi et al. 2021 (P0005), published in the same venue — a rare, direct, named methodological critique within this literature.

**Core arguments (directly complicating the "unstructured NLP is the way forward" framing common in this literature):**
1. The Karimi et al. (P0005) cohort was **not a general breast cancer population** — patients were pre-selected for high likelihood of recurrence using structured-data codes before NLP was applied, meaning the NLP system was validated on an enriched, non-representative sample rather than deployed on an unselected real-world population.
2. NLP-based recurrence-identification approaches have practical deployment shortcomings: unstructured text and sufficient computing resources may not be uniformly available across health systems, and NLP models are **less portable across institutions** because clinician documentation style varies (a "domain shift" problem).
3. Conclusion: the authors argue EHR- or claims-based structured recurrence-detection algorithms will likely remain the more practical tool for population-level research for the foreseeable future — a direct pushback against assuming unstructured/NLP data is automatically superior.

**Why this matters for our program:** This is exactly the kind of contradicting evidence the research process is supposed to surface (project brief Section 4: "find newer and contradictory studies"). It tempers any plan to lean entirely on NLP-derived labels/features without also validating portability across sites, and argues for testing model performance on an *unselected* population, not just a curated high-risk subset.

**Relevance to our project:** ★★★★★ — critical counter-evidence; should be weighed directly against P0005's finding (ICD coding badly under-captures recurrence) when designing our own label strategy. The synthesis is not "NLP is better" or "structured is better" — it's that **cohort selection and cross-site portability must be explicitly tested**, not assumed.
