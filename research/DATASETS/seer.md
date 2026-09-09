# Dataset: SEER (Surveillance, Epidemiology, and End Results)

**Real or synthetic:** Real, population-based cancer registry (NCI).
**Source:** seer.cancer.gov (official; primary source not directly fetchable this session — findings via WebSearch snippets of the official documentation).

**Coverage:** Registries covering ~47.9% of the US population. Breast cancer is the most common cancer type in SEER; exact breast-cancer-specific case count UNKNOWN — not independently verified.

**Variables confirmed:** demographics, stage at diagnosis, tumor morphology/grade, ER/PR status (since 1990), HER2 status (since 2010, "Breast Subtype 2010+" derived variable), first course of treatment (surgery, radiation), vital status, cause-specific death classification, follow-up time to death/last contact.

**CRITICAL VERIFIED LIMITATION:** SEER does **not** capture surgery/radiation beyond ~4 months post-diagnosis, and does **not** capture recurrence or metastasis detected after initial diagnosis at all (confirmed directly from official SEER documentation snippets). Chemotherapy variables are also substantially undercaptured in registry data generally.

**Longitudinal structure:** Yes for survival (diagnosis = index date, follow-up to death/last contact via registry linkage) — good for overall-survival prediction. **No** for recurrence/metastasis — the outcome is not collected in base SEER.

**Missingness:** Not independently characterized this session beyond the structural gaps above.

**Access:** SEER Research Data (SEER*Stat) — public, free, self-service click-through Data Use Agreement, no IRB required, no fee. **Realistically autonomously accessible.**

**License:** NCI SEER Research Data Use Agreement (custom terms; restricts re-identification attempts and unauthorized linkage to outside data).

**IRB:** Not required for the standard research data files.

**Usefulness for this project:** Cannot support recurrence/metastasis prediction directly (structural gap, not missingness). Usable only if the eventual target is narrowed to **overall survival / vital status** prediction from baseline covariates — and even then, it is registry data (no labs, meds, or clinical notes), not full longitudinal EHR.

**Limitations for this use case:** No recurrence field at all; no labs/meds/notes; treatment capture truncated at ~4 months.

---

## SEER-Medicare (linkage)

**Real**, adds Medicare Part A/B (and more recent Part D) claims longitudinally for patients aged 65+.

Enables **claims-based recurrence-proxy algorithms** (published methodology exists, e.g. treatment-pattern-based imputation) — the closest thing to a genuine longitudinal EHR-like recurrence signal among the registry options, but recurrence is *inferred* from claims patterns, not a ground-truth labeled field.

**Access:** Requires formal application, signed **Data Use Agreement**, **documented IRB approval**, and a **processing fee** (amount depends on files requested). Per a new NCI-CMS agreement, by March 1, 2027 access shifts to a secure enclave with a per-seat fee.

**Selection bias:** Restricted to Medicare-eligible (mostly 65+) population — not representative of the general breast cancer population.

**★★★★☆ (structural fit)** — real longitudinal claims timeline enabling validated recurrence-proxy algorithms at scale.

**⚠️ STOP POINT — requires human researcher action:** formal DUA, documented IRB approval, and a processing fee. This cannot proceed autonomously.
