# P0027 — RSF/DeepSurv/CoxPH Comparison (2025) — Negative Result for Deep Survival Modeling

**Citation:** "Comparison of Random Survival Forest Based-Overall Survival With Deep Learning and Cox Proportional Hazard Models in HER2-Positive HR-Negative Breast Cancer." 2025.
**Link:** PMC12234386 · PubMed 40624807

**Clinical problem:** Compare Random Survival Forest, DeepSurv, and classical Cox Proportional Hazards for overall survival prediction in a specific molecular subtype.

**Dataset:** SEER registry, N=8,119 HER2+/HR− patients.

**Result — the key finding:** DeepSurv achieved a training C-index >0.8, but **classical CoxPH outperformed DeepSurv on the held-out test set.** RSF performed best overall (AUC 0.876/0.861/0.845 for 1/3/5-year OS in the test group).

**Why this matters for our program:** This is a directly relevant, honestly-reported negative result for deep learning over a simpler, classical model — exactly the caution the project brief emphasizes in its First Principle (Section 1): *"If the best solution is Logistic Regression/XGBoost/Cox instead of a deep neural network, use the simpler model. Do NOT use deep learning merely because it sounds impressive."* This paper is direct empirical evidence supporting that principle, not just a stated philosophy.

**Limitations:** SEER-only (registry data, no labs/meds/notes — not full real-world EHU); single molecular subtype, limiting generalizability of the specific finding.

**Relevance to our project:** ★★★★ (methodological signal), ★★★ (data relevance since SEER-only) — should be cited directly when justifying a baselines-first, simplest-sufficient-model development process (project brief Section 17–18).
