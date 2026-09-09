# Research Gaps — Breast Cancer + Real-World EHR + AI/ML

Evidence-backed gaps identified from the literature reviewed in `LITERATURE_MATRIX.csv` and `PAPERS/`. Each gap below is supported by ≥2 independently-found sources, per the project brief's requirement not to call something a gap merely because one paper didn't investigate it. Where evidence is thin, that is stated explicitly.

**Session-wide caveat:** WebFetch (full-text retrieval) was blocked in this environment for all three research passes; findings are built from WebSearch result snippets, which frequently quote abstracts but do not allow independent verification of methods sections. Every gap below is flagged with its confidence level given this constraint.

---

## GAP 1 — "Prediction" papers are frequently actually detection/extraction papers, and this is under-scrutinized

**Evidence:** Of the core distant-recurrence-from-EHR cluster, only P0004 (González-Castro, explicit 5-year horizon) and arguably P0003 (Sanyal, "in advance" framing) have a clearly defensible PREDICTION design. P0001 (Zeng) is squarely DETECTION. P0002 (Wang)'s status is genuinely unresolved. P0005 (Karimi), P0009 (Banerjee 2019), P0010/P0011 (Lee et al. 2024/2025), and P0031 (Ling et al.) are explicitly extraction/detection tools for registry curation, not forecasting, despite titles that sometimes use "prediction"-adjacent language.

**Confidence:** HIGH — directly observed across ~15 papers in this specific sub-literature by an independent agent, cross-checked by a second agent's parallel search.

**Implication for our program:** Any claim of "predicting recurrence" in the literature must be checked against whether the model genuinely restricts input features/text to a pre-specified time point before the outcome, or classifies over the full chart (which is detection). Section 9 of the project brief's DETECTION/EXTRACTION/PREDICTION distinction is not a hypothetical concern — it is the single most common conflation in this literature.

---

## GAP 2 — Structured/coded EHR fields severely under-ascertain recurrence

**Evidence:** P0005 (Karimi et al. 2021) found NLP identified recurrence in 11.1% of a breast cancer database vs. only 2.31% via ICD coding alone — a ~5x gap. This exact finding was independently surfaced by two separate research agents searching different query sets, which is strong convergent evidence, not a single-source claim.

**Confidence:** HIGH (convergent, independently replicated finding).

**Implication:** Any project — including ours — that constructs a recurrence label purely from structured/coded EHR fields (ICD codes, registry flags) will have a badly biased, under-ascertained outcome label. A credible label needs NLP-derived or manually-abstracted recurrence ascertainment, which is itself a nontrivial sub-project (see P0005, P0008, P0010, P0020, P0024 for methods precedent).

---

## GAP 3 — Near-total absence of genuine external (cross-institution) validation for true PREDICTION models specifically

**Evidence:** Genuine external validation exists in this literature — but almost exclusively for detection/extraction tools (P0020: DFCI model tested at Kaiser NorCal, 90% accuracy) or for cross-institution studies with severely inadequate sample sizes (P0012/Sukhadia et al.: external validation n=9, AUC=1.0 on a 17-patient internal test — a methodological red flag, not a robust result). P0017 (Zhao et al., NCDB→UChicago) and P0025 (NSABP B-42→TAILORx) are rare genuine external-validation PREDICTION studies, but the latter uses clinical-trial cohorts, not routine-care EHR. The two systematic reviews (P0006, P0007) both note the pooled literature's evident train→validation performance drop as an implicit generalization-gap signal.

**Confidence:** HIGH — this is the most consistently repeated observation across both literature-search agents' independent syntheses.

**Implication:** A well-powered, EHR-native (not registry, not trial-cohort), externally-validated true prediction model for a breast cancer outcome is essentially absent from what this search could find. This is the clearest, most defensible open research gap for this program.

---

## GAP 4 — Demographic/geographic equity gap in existing recurrence models

**Evidence:** Directly confirmed by a systematic review (P0006, El Haji et al. 2023): existing recurrence-prediction models are trained/validated predominantly on Caucasian and Asian populations, with African and Middle Eastern populations largely absent.

**Confidence:** HIGH (stated directly in a systematic review, not inferred by us).

**Implication:** If we get to choose among candidate datasets, cohort diversity should be an explicit selection criterion, and any eventual subgroup/fairness analysis (project brief Section 23) should treat this as a known field-wide weakness to test for, not just a generic checkbox.

---

## GAP 5 — Deep learning is not automatically superior to classical models in this domain, and this is under-reported relative to positive results

**Evidence:** P0027 found classical Cox Proportional Hazards outperformed DeepSurv on held-out SEER data despite DeepSurv's higher training C-index — an honest negative result. P0030 (Stratipath) found an AI risk-stratification model performed only "similarly" to the existing Nottingham Histologic Grade system, not clearly better. Both are real, findable negative/neutral results, but they are outnumbered by positive-result papers in the broader search, consistent with typical publication bias.

**Confidence:** MODERATE — two clear examples found; broader prevalence of publication bias in this specific sub-field was not directly quantified (would require a dedicated bias-focused review).

**Implication:** Directly supports the project brief's First Principle (Section 1): baselines-first, simplest-sufficient-model. Our own experiments should be designed and reported to surface a negative result honestly if the proposed model doesn't beat XGBoost/Cox, per Section 28.

---

## GAP 6 — OMOP-based breast cancer *outcome prediction* studies (as distinct from data-infrastructure papers) appear scarce

**Evidence:** Searches for "OMOP breast cancer machine learning" surfaced only infrastructure/data-mapping papers (P0029: pathology-report-to-OMOP mapping; general OMOP-CDM-for-cancer-research extension papers) and general-cancer systematic reviews (not breast-specific), not a network study predicting a breast cancer outcome on OMOP-harmonized multi-site data.

**Confidence:** MODERATE — absence-of-evidence is weaker than a directly-stated gap; the research agent explicitly flagged this could reflect search limitations rather than a true absence.

**Implication:** If All of Us / OMOP is pursued as the eventual data source, this would be a genuinely novel angle — but the feasibility of constructing a reliable breast-cancer cohort + outcome from raw OMOP codes has not been piloted or verified in the literature we found, so this carries real execution risk.

---

## GAP 7 — Toxicity prediction is comparatively neglected relative to recurrence/survival, despite more objectively ascertainable labels

**Evidence:** Only P0019 (neoadjuvant toxicity, N=590) was found addressing treatment toxicity directly, versus dozens of papers on recurrence/survival. Toxicity grades (lab-based, e.g. CTCAE criteria) are more objectively and consistently documented in structured EHR fields (labs, dose-modification codes) than recurrence is in free text — meaning GAP 2's label-quality problem is much less severe for toxicity than for recurrence.

**Confidence:** MODERATE — based on relative paper counts found in a bounded search, not a formal bibliometric analysis.

**Implication:** A strong secondary/complementary candidate research question with a cleaner label-engineering path than recurrence prediction.

---

## GAP 8 — Landmark-time (correct prediction-time-cutoff) multimodal architectures exist but are not yet externally validated

**Evidence:** P0016 (Multimodal BEHRT) is the strongest example found of a genuinely correct landmark-time design (features from year 1 post-surgery predicting 3-year DFS) combined with structured+text fusion, beating a validated clinical baseline (NPI). But it reports no external-site validation and does not specify whether its outcome label is coded, NLP-derived, or manually verified (directly relevant to Gap 2).

**Confidence:** HIGH for the architecture's existence and reported result; MODERATE for generalizability given the unaddressed external-validation and label-provenance gaps.

**Implication:** This is the closest published template to build on. A follow-up study that (a) verifies/upgrades the outcome label per Gap 2, and (b) adds genuine external validation per Gap 3, would directly answer two of this program's most important open questions at once.

---

## Synthesis

The single most defensible, evidence-backed research gap combining clinical importance, novelty, and feasibility is:

> **A breast cancer recurrence/disease-free-survival prediction model using structured + NLP-extracted longitudinal EHR data, with a correctly-designed landmark/prediction-time cutoff, an NLP-derived (not ICD-coded) outcome label, and genuine external (cross-institution or strong temporal) validation from the start.**

This synthesis is echoed independently by both literature-search agents' own concluding recommendations (see agent transcripts referenced in `PROGRESS.md`), which is a meaningful convergence signal.

A close secondary candidate is **treatment-related toxicity prediction**, which is comparatively under-studied and has a more objectively ascertainable label, making it lower-risk from a label-engineering standpoint — see `RESEARCH_STATE.md` and the upcoming checkpoint for how these compare against dataset feasibility.
