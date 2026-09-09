# Dataset: MIMIC-III / MIMIC-IV / eICU (PhysioNet)

**Real or synthetic:** Real, MIT/PhysioNet, Beth Israel Deaconess Medical Center (MIMIC); 208 US hospitals (eICU).

**Coverage:** MIMIC-III: ICU stays 2001–2012. MIMIC-IV: hospital/ICU data 2008–2019; reported figures vary by version/snapshot (roughly 300–500K admissions) — exact current count UNKNOWN, not independently pinned down. eICU: >200,000 ICU admissions, 2014–2015.

**Breast cancer relevance: confirmed minimal to none.**
- MIMIC captures patients only during acute ICU/hospital episodes. Cancer-related MIMIC studies found in search all concern general ICU mortality in cancer patients (e.g., lung cancer ICU mortality, neutropenia studies) — **no evidence of a designed, longitudinal breast-cancer oncology cohort.** No staging/receptor-status/treatment-line/recurrence structure exists; patients appear incidentally (e.g., post-op complications, sepsis).
- eICU: confirmed general-purpose critical-care database (vitals, labs, meds, structured problem-list diagnoses, treatments, 31-table schema) with **no dedicated oncology or breast-cancer content found.**

**Longitudinal structure:** Only within single hospitalizations/ICU stays — not a multi-year oncology follow-up structure. Not suitable for defining an index date + prediction time + long follow-up window for a cancer outcome.

**Access:** PhysioNet Credentialed Health Data License 1.5.0 + Data Use Agreement; requires completing CITI "Data or Specimens Only Research" training + a credentialing application (real-identity review) per PhysioNet, plus accepting each dataset's own DUA. Free, no fee. Technically autonomously completable (documented steps), but identity verification requires a real named individual (the human researcher, not the agent).

**License:** PhysioNet Credentialed Health Data License 1.5.0.

**Verdict: NOT SUITABLE for a breast cancer outcome-prediction project.** Confirmed via targeted search, not merely presumed. Included here for completeness per the research brief's instruction to investigate MIMIC/PhysioNet, but ranked unsuitable (✩) and not recommended for further pursuit.
