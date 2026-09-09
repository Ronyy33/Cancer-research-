# Decision Log

Record of consequential decisions made during this research program, with
date, rationale, and who made the call (autonomous engineering decision vs.
human-approved research decision).

---

### D001 — 2026-09-09 — Repository structure adopted (autonomous)
Adopted the directory structure specified in the project brief
(`/research`, `/src`, `/configs`, `/scripts`, `/tests`, `/docs`, `/data`)
as-is, since it already matches sound research-repo practice. No deviation
needed at this time.

**Type:** routine engineering — no human approval required.

---

### D002 — 2026-09-09 — Raw data will never be committed (autonomous)
`.gitignore` configured to exclude `data/`, `*.csv`, `*.parquet`, `*.json`,
`*.sqlite`, `*.db` etc. by default, with explicit exceptions carved out
for known-safe files (e.g. `research/LITERATURE_MATRIX.csv`, JSON configs).
This is a hard safety requirement from the project brief, not open to
autonomous override.

**Type:** routine engineering — no human approval required.

---

---

### D003 — 2026-09-09 — Primary research question and first dataset chosen (human-approved)
Per the RESEARCH CHECKPOINT presented after Stage 1-5 (literature review +
dataset discovery), Kevin selected:

- **Research question:** Q3 — treatment response / pathologic complete
  response (pCR) prediction to neoadjuvant chemotherapy. Rationale from
  `CANDIDATE_RESEARCH_QUESTIONS.md`: objectively-defined outcome (pCR at
  surgery), real external-validation precedent in the literature (P0017,
  P0018), lower label-engineering risk than recurrence (which requires
  NLP-derived labels per Gap 2 in `RESEARCH_GAPS.md`).
- **Dataset (first target):** All of Us Research Program (OMOP CDM),
  pursued in parallel with Kevin's own Registered Tier registration.

**Important deviation flagged:** the checkpoint's matched recommendation
paired pCR with I-SPY2 (public, trial-derived, imaging-centric) and paired
All of Us with the *recurrence* question, not pCR. Kevin instead chose
pCR + All of Us — a more ambitious, more EHR-native combination, but
**neither research pass in this session verified that All of Us reliably
captures neoadjuvant chemotherapy regimens or pathologic treatment
response.** This pairing has real, unquantified feasibility risk and
must be piloted before committing further engineering effort. A targeted
feasibility investigation was launched immediately following this decision
(see `PROGRESS.md`).

**Type:** consequential research decision — human-approved, per project
brief Section 33 item 1 (choosing between fundamentally different research
questions) and item 6 (committing to a research hypothesis/dataset pairing).

**Access blocker:** All of Us Registered Tier requires Kevin's own identity
verification (photo ID proofing) — this cannot be completed by the agent.
See `DATASETS/all_of_us_omop.md` and the access instructions added there.

---

---

### D004 — 2026-09-09 — All of Us + pCR pairing found infeasible; awaiting revised decision
The feasibility investigation launched immediately after D003 returned a
high-confidence NOT FEASIBLE finding: All of Us Registered Tier does not
expose the free-text pathology reports that pCR is defined from, its
NLP-derived concept layer covers only ~11% of participants with no
demonstrated pathology-response granularity, and no prior study has
attempted neoadjuvant-chemo or pCR work using All of Us. Full evidence in
`DATASETS/all_of_us_omop.md` (feasibility investigation results section).

This is NOT treated as a routine engineering finding to route around
autonomously — it materially affects the study design chosen in D003
(project brief Section 33 items 1, 6, 7: choosing between research
questions/datasets, committing to a hypothesis, choosing between study
designs). A revised checkpoint was presented to Kevin rather than
unilaterally switching to a fallback.

**Type:** consequential — human decision required, not yet made at time of
this entry.

---

---

### D005 — 2026-09-09 — Reverted to recurrence/relapse prediction, EHR-native dataset required (human-approved)
Following D004's finding that All of Us cannot support pCR, Kevin redirected
the research question back to **recurrence/relapse prediction** (the
originally top-ranked candidate, Q1 in `CANDIDATE_RESEARCH_QUESTIONS.md`,
and the strongest evidence-backed gap in `RESEARCH_GAPS.md`), with an
explicit requirement for a **genuine EHR dataset** (not a registry snapshot
like METABRIC/SEER/TCGA).

Given the dataset landscape from Stage 5, the only dataset that is both (a)
genuinely EHR-native/longitudinal and (b) free of a cost/IRB/institutional
barrier is **All of Us** (requires only Kevin's one-time identity
verification, already a pending action item from D003). Flatiron
(commercial license) and SEER-Medicare (DUA+IRB+fee) remain structurally
strong but access-gated.

**Important distinction from the D004 finding:** pCR strictly requires
free-text pathology reports, which All of Us does not expose — that
specific outcome was ruled out. Recurrence/relapse is a different signal
with structurally-supportable proxies (new metastatic-disease diagnosis
codes, restarted/changed systemic therapy after a treatment-free interval,
claims-based recurrence-proxy methodologies precedented in the SEER-Medicare
literature) that were NOT tested in the D004 investigation. A dedicated
feasibility check was launched immediately following this decision.

**Type:** consequential research decision — human-approved, per project
brief Section 33.

---

*(Further entries appended as decisions are made. Entries requiring human
sign-off will be flagged **DECISION REQUIRED** in `PROGRESS.md` before being
finalized here.)*
