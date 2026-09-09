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

---

### D006 — 2026-09-09 — All of Us recurrence feasibility: MEDIUM confidence, proceed as gated pilot (autonomous, routine methodology work)
The narrower feasibility check launched after D005 found recurrence
detection from All of Us structured data is **not structurally blocked**
(unlike pCR/D004), but carries a real, specific risk: a 2026 claims-linkage
study found All of Us EHR-only data undercounts real procedures by a wide
margin relative to insurance claims for the same patients over the same
months — meaning care happening outside a participant's AoU-linked health
system is invisible to any structured recurrence-proxy algorithm. General
claims-based recurrence-proxy methods are well-validated elsewhere
(SEER-Medicare, Kaiser Permanente: 92-94% sensitivity when combining
multiple structured signals), but that validation was done in
closed/near-complete care-capture settings that All of Us is not.

**Resulting methodological adjustments** (documented in `cohort_definition.md`
v2 and `LEAKAGE_AUDIT.md`): treat the recurrence label as noisy rather than
ground truth; require a combined multi-signal proxy algorithm rather than
any single indicator; frame the outcome as recurrence-free survival with
censoring rather than binary classification; run a mandatory manual
validation gate on a small sample before any cohort-scale modeling; keep
METABRIC documented as a fallback if the validation gate shows the label
is too unreliable.

**Type:** routine research/methodology work — proceeding autonomously per
project brief Section 33 (this refines methodology within the
already-approved question+dataset from D005; it does not change the
research question or dataset, so it does not require a further stop-and-ask).
Kevin was informed of the finding and rationale in chat.

---

---

### D007 — 2026-09-09 — All of Us abandoned (institutional barrier confirmed); switched to multi-dataset real-data plan
Kevin reported his institute is not registered with All of Us, blocking
Workbench access regardless of his own identity verification. Rather than
keep pursuing a single blocked dataset, he asked for a deep, multi-hour
search for a real (not synthetic), ideally-longitudinal dataset with no
institutional access requirement.

Three parallel deep-research passes (classic public survival datasets;
TCIA imaging+outcome datasets; newer open EHR datasets + All of Us
individual-access recheck) independently converged on the same structural
finding: **All of Us, NSABP/NCTN (via dbGaP), and UK Biobank are all
institution-gated in practice** (each requires an institutional
Signing-Official/DURA co-signature or affiliated-email verification), and
**no real, publicly-downloadable, genuinely multi-visit EHR-timeline
dataset for breast cancer recurrence exists** that is accessible to an
unaffiliated individual. This was checked independently three times and
is treated as a real constraint of the current public data landscape, not
a search failure.

**Decision: adopt a multi-dataset real-data research design** rather than
seeking one large EHR dataset:
- **Primary training + external validation:** Rotterdam (n=2,982, train) +
  GBSG2 (n=686, external validation) — both real, zero-barrier, genuine
  time-to-event recurrence-free survival data, and this exact pairing is
  a citable, established methodology (Royston & Altman 2013; the standard
  DeepSurv/pycox benchmark split) — directly answering Gap 3 (lack of
  external validation) from `RESEARCH_GAPS.md`.
- **Secondary real cohorts for cross-validation/robustness:** METABRIC
  (n≈2,509, already investigated, real RFS outcome) and TCGA-BRCA
  (n≈1,098, DFI/DSS/PFI fields) as additional independent real datasets.
- **Optional richer-feature / multimodal arm:** Duke-Breast-Cancer-MRI
  (n=922, real LRFS/DRFS time-to-event fields, richer clinical covariates,
  optional imaging) — pending direct verification of its recurrence event
  rate before relying on it for primary modeling.

This turns the access constraint into a design strength: using multiple
independent real cohorts together gives genuine external/cross-cohort
validation from day one — the exact thing most published studies in this
field lack (per `RESEARCH_GAPS.md` Gap 3), achieved via real, freely
accessible data rather than one large gated EHR source.

**Explicitly not achieved and stated honestly:** true multi-visit,
repeated-measures EHR time-series data. All real, zero-barrier datasets
found across three independent deep searches share the same baseline-
snapshot-plus-survival-time structure. This is documented as a known,
searched-for-and-confirmed-absent limitation, not an oversight.

**Type:** consequential dataset/design decision — treated as within the
scope of Kevin's explicit instruction ("get a perfect dataset which we can
work on... take hours no problem") rather than requiring a further
stop-and-ask, since the research question (recurrence prediction) is
unchanged and Kevin delegated the final dataset selection itself.

---

*(Further entries appended as decisions are made. Entries requiring human
sign-off will be flagged **DECISION REQUIRED** in `PROGRESS.md` before being
finalized here.)*
