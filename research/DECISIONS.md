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

*(Further entries appended as decisions are made. Entries requiring human
sign-off will be flagged **DECISION REQUIRED** in `PROGRESS.md` before being
finalized here.)*
