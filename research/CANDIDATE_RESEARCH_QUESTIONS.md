# Candidate Research Questions — Ranked

Per the project brief's mandate not to assume recurrence is automatically correct (Section 0), the following candidates were evaluated on: clinical importance, research novelty, real-data availability, label quality, technical feasibility, validation feasibility, interpretability, and publication potential. Scores are 1–5 (5 = strongest), assigned qualitatively from the evidence gathered — not from a formal weighted model.

| Criterion | Q1: Recurrence/DFS prediction (structured+NLP EHR, landmark design) | Q2: Treatment-related toxicity prediction | Q3: pCR / treatment-response prediction | Q4: Overall survival prediction (SEER-based) |
|---|---|---|---|---|
| Clinical importance | 5 | 4 | 5 | 3 |
| Research novelty / gap size | 5 (Gaps 1,2,3,8) | 4 (Gap 7) | 3 (external validation precedent already exists: P0017) | 1 (heavily saturated per P0007 meta-analysis) |
| Real-data availability (autonomous) | 3 (best fit is METABRIC/All of Us, neither perfect) | 2 (no public dataset with the right label found) | 4 (I-SPY2/TCIA is public and well-suited) | 5 (SEER is trivially accessible) |
| Label quality achievable | 2 (Gap 2: coded labels badly biased; NLP labeling is a real sub-project) | 4 (lab/dose-modification-based labels are more objective) | 4 (pCR is a clean, objectively-defined pathology outcome) | 5 (vital status is unambiguous) |
| Technical feasibility | 3 (multimodal fusion + correct landmark design is nontrivial, though P0016 provides a template) | 4 | 4 | 5 |
| Validation feasibility | 3 (external EHR validation is hard to arrange without institutional access) | 2 (no obvious external dataset identified) | 4 (I-SPY2 + potential NCDB-style comparison) | 5 (SEER + external registry comparison, per P0026 template) |
| Interpretability | 4 (SHAP over structured+NLP features is standard) | 4 | 4 | 4 |
| Publication potential | 5 (fills the field's most cited weakness — see RESEARCH_GAPS.md Gap 3) | 3 (smaller, more niche contribution) | 3 (already has decent published external validation precedent, P0017/P0018) | 1 (would not be novel per P0007) |
| **Rough total (unweighted, out of 40)** | **30** | **27** | **31** | **29** |

## Important caveat on this scoring

These totals are close enough (27–31) that **the numeric score alone should not decide this** — the real differentiator is what a defensible, fundable, publishable study actually requires:

- **Q4 (SEER-based OS prediction)** scores well on feasibility but is explicitly ruled out as *novel* by our own meta-analysis review (P0007) — this would be "another breast cancer ML model," which the project brief explicitly says we are not trying to build (Section 36). **Recommend deprioritizing.**
- **Q3 (pCR/treatment-response)** has the best out-of-the-box public dataset (I-SPY2) and real precedent for external validation (P0017, P0018), making it the **lowest-execution-risk option** for a genuinely novel, well-validated study — but the "genuine EHR longitudinality" angle is weaker here (I-SPY2 is trial-derived, not routine-care EHR).
- **Q1 (Recurrence/DFS)** is the highest-novelty, highest-clinical-importance option and is what the literature synthesis (RESEARCH_GAPS.md) converges on independently from two different search agents — but it carries real execution risk on the label-quality problem (Gap 2) and lacks a single "ideal" autonomously-accessible dataset (METABRIC is close but not EHR-native; All of Us is EHR-native but unproven for this cohort and requires a human identity-verification step).
- **Q2 (Toxicity)** is a credible, lower-hype, well-scoped complementary or fallback target if Q1's label-engineering proves too costly, but no clearly identified public dataset supports it directly (would likely require All of Us or an institutional dataset).

## Recommendation for the checkpoint

Given the convergent literature evidence, propose **Q1 (recurrence/DFS prediction) as the primary target, using METABRIC as the initial fully-public dataset for baseline/methodology development** (real recurrence endpoint, no access barrier), with **All of Us investigated in parallel as a path to a more EHR-native version of the same question** (requires Kevin's one-time identity verification to unlock). If Q1's label/data engineering proves infeasible at the METABRIC/All of Us stage, **Q3 (pCR via I-SPY2) is the recommended fallback** given its lower execution risk and existing external-validation precedent.

This is exactly the kind of "choosing between fundamentally different research questions" decision the project brief reserves for the human researcher (Section 33, item 1) — presented in the checkpoint below for Kevin's decision, not decided autonomously.
