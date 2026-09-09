# Dataset: All of Us Research Program (OMOP CDM)

**Real or synthetic:** Real, NIH program, built natively on OMOP Common Data Model v5.

**Access tiers (confirmed):** Public (no login) → **Registered Tier** (free registration + required identity verification + ethics/training modules; gives access to a cloud Researcher Workbench with de-identified individual-level longitudinal EHR, surveys, physical measurements, wearables) → **Controlled Tier** (additional Data Access Committee approval; genomic data, unsuppressed dates).

**Breast cancer relevance:** One study found in search compared a mastectomy cohort vs. controls using OMOP-coded concepts (mammography, biopsy, endocrine therapy, chemotherapy prevalence) — confirms breast-cancer-relevant structured EHR concepts exist. However, this is derived from raw diagnosis/procedure codes, not a pre-built, curated oncology outcomes registry like SEER/METABRIC. Whether structured recurrence/staging/receptor-status fields analogous to a cancer registry exist reliably: **UNKNOWN — not verified**; would require substantial cohort-construction effort from raw EHR codes and possibly clinical notes.

**Longitudinal structure:** This is the one resource confirmed to have genuine **multi-year timestamped EHR data per participant** (Registered Tier includes longitudinal EHR data with relative-interval-preserved dates) — structurally the best fit for a proper index-date + prediction-window + follow-up design, *if* a reliable breast-cancer cohort and outcome can actually be constructed from it (not verified/piloted this session).

**Key practical constraint:** Analysis is workbench-only — no bulk raw-row export off-platform without a formal egress review process.

**Access:** Free Registered Tier requires **a real human's identity verification** (photo ID proofing) — this step cannot be completed by an AI agent.

**License:** All of Us Data Use and Registration Agreement (workbench-based analysis, no raw bulk export).

**IRB:** All of Us itself operates under its own IRB/consent framework for participants; researcher-side IRB requirements depend on the researcher's institution and the specific study — **not fully verified this session, flag for confirmation before use.**

**Usefulness for this project:** Promising but unproven — the right structural shape (genuine longitudinal multi-year EHR) but breast-cancer cohort/outcome construction from raw codes has not been piloted or verified, and it inherits the same "coded recurrence under-captures true recurrence" risk documented in the literature review (P0005) unless supplemented with NLP over available clinical text.

**⚠️ STOP POINT — requires human researcher action:** Registered Tier requires the human researcher's own identity verification (photo ID) — this is a step only Kevin can complete, not something the agent can do autonomously. Controlled Tier additionally requires Data Access Committee approval.

**Ranking: ★★★☆☆** — right structural shape, unproven cohort/outcome feasibility, and requires human-only registration step.

---

## STATUS UPDATE — 2026-09-09 (D003): Selected as first dataset target, paired with pCR/treatment-response question

Kevin selected All of Us as the first dataset to pursue, paired with the
pCR/treatment-response prediction question (see `DECISIONS.md` D003 and
`CANDIDATE_RESEARCH_QUESTIONS.md`). **This specific pairing was not
verified in the original dataset-discovery research pass** — that pass
only confirmed general breast-cancer-relevant OMOP concepts (mammography,
biopsy, endocrine therapy, chemotherapy prevalence) via one unrelated
mastectomy-cohort study, not specifically neoadjuvant chemotherapy regimen
identification or post-treatment pathologic response ascertainment.

### What Kevin needs to do (cannot be automated)

1. Go to the All of Us Research Hub (researchallofus.org) and create a
   researcher account.
2. Complete the required ethics/training modules (typically an approx.
   1-2 hour online training on responsible conduct of research with
   All of Us data).
3. Complete **identity verification** (photo ID proofing) — this is the
   hard blocker; it must be Kevin's own government ID, not something the
   agent can supply or complete on his behalf.
4. Request/activate Registered Tier access to the Researcher Workbench.
5. Once Registered Tier access is active, share Workbench access
   credentials/workspace details back with this project so cohort-building
   notebooks can be developed against it (analysis happens on-platform;
   no bulk raw-data export off-platform without a separate egress review).

### Feasibility investigation results — 2026-09-09

**Conclusion: NOT FEASIBLE as specified. Confidence: HIGH.**

- **No published study has used All of Us for neoadjuvant chemotherapy
  identification or pCR ascertainment.** Six All of Us breast-cancer papers
  were found (mastectomy data-quality, surgical-oncology data-quality,
  CVD-risk in survivors, pain-management prediction, survival disparities,
  pharmacogenomics) — none touch treatment-response phenotyping.
- **Two of All of Us's own investigator groups have published dedicated
  data-quality papers on breast-cancer-surgery cohorts specifically
  because structured data completeness is a known open problem**: the
  mastectomy cohort paper (JMIR Cancer 2025, PMC11918980) found
  chemotherapy exposure data limited to anthracycline-based drugs only
  (other regimen components e.g. taxanes not confirmed captured), and
  radiation data miscoded into the wrong OMOP table. The surgical-oncology
  data-quality paper (JCO CCI 2025, PMC12240465) found low concept
  prevalence and completeness problems across five surgical cohort types.
- **Registered Tier provides NO free-text access to clinical notes or
  pathology reports.** pCR is intrinsically a pathology-report-level
  judgment (no residual invasive tumor, ypT0/ypN0). Instead, All of Us
  exposes only NLP-derived structured concept codes covering roughly
  99,000 of >883,000 enrolled participants (~11%), with no confirmed
  pathology-response granularity.
- Neoadjuvant-vs-adjuvant sequencing has been done from OMOP-like data
  elsewhere (JMIR Med Inform 2021, e25035), but that approach relied on
  pathology staging fields (ypT/ypN) and explicit "neoadjuvant" text terms
  that All of Us does not expose to researchers.
- **I-SPY2 re-confirmed as the purpose-built alternative**: 624 patients,
  pCR is the trial's pre-adjudicated primary endpoint (not something to be
  reconstructed), linked imaging + clinical covariates already public via
  TCIA.

**Recommendation from the investigation:** fall back to I-SPY2 as the
primary dataset for pCR prediction, OR keep All of Us but change the
outcome to something structurally supportable (e.g., chemo-regimen
exposure/cardiotoxicity risk, or treatment-sequencing patterns as a
process measure rather than a clinical-response measure).

**This is a research-design-level finding, not a routine engineering
result** — see `DECISIONS.md` D004 and the follow-up checkpoint presented
to Kevin.

---

## Feasibility investigation #2 — 2026-09-09: RECURRENCE detection (different question)

Following D005 (Kevin reverted to recurrence/relapse prediction, explicitly
requiring an EHR dataset), a second, narrower feasibility check was run:
**can recurrence be detected from All of Us structured data alone**
(diagnosis codes, treatment-restart timing), without needing the free-text
pathology reports that specifically ruled out pCR above?

**Conclusion: MEDIUM confidence — feasible as a gated pilot, not a clean
guaranteed endpoint.** This is meaningfully different from the pCR
verdict (which was a hard structural block).

**Key findings:**
- Only one published All of Us breast-cancer-outcome study was found —
  and tellingly, it had to use tamoxifen medication exposure as a crude
  proxy for "remission" because "the All of Us Research Program database
  lacks an indicator for remission from breast cancer" (Quality Management
  in Health Care, PubMed 40167483). No validated recurrence study exists
  in All of Us yet.
- **General claims-based recurrence-proxy algorithms are well-validated
  elsewhere** — combining multiple structured signals (new secondary-
  malignancy code + new/restarted systemic therapy after a gap + new
  radiation + cause of death) achieves 92-94% sensitivity / 93-98%
  specificity against manual chart review in SEER-Medicare and integrated
  systems like Kaiser Permanente. A single signal alone (e.g. just "new
  therapy") misses ~40%+ of even near-certain recurrences (Warren et al.
  2016) — the algorithm MUST be multi-signal.
- **The critical risk specific to All of Us**: a new 2026 claims-linkage
  study (PMC12829818) found that for the same patients in the same
  months, insurance claims show ~75% more procedure codes and ~16% more
  service dates than All of Us EHR data alone. All of Us is a federated,
  partial-capture network — care that happens outside a participant's
  AoU-linked health system is simply invisible. This is a different and
  additional risk on top of the already-known problem that coded
  recurrence generally undercounts true recurrence (see Gap 2 in
  `RESEARCH_GAPS.md`).
- Unconfirmed whether All of Us populates the OMOP Oncology Module
  (`episode`/`episode_event` tables built for exactly this purpose) — this
  is the first thing to check directly in the Workbench.
- Rough (unverified) cohort size estimate: low thousands to ~15,000 total
  breast cancer cases in All of Us before filtering; a published Mastectomy
  phenotype gives a concrete starting cohort of n=4,175.
- Follow-up duration is adequate for a meaningful subset (~25% of the
  >287,000 participants with EHR data have 10 years of it) — this favors
  recurrence prediction over pCR, since recurrence risk extends years
  post-treatment.

**Resulting methodological decision (not requiring a further stop, since
the question/dataset choice itself is unchanged from D005):**
1. Treat the recurrence-proxy label as **noisy, not ground truth**.
2. Use a **combined multi-signal algorithm**, never a single indicator.
3. Frame the outcome as **recurrence-free survival with censoring**, not
   binary classification — "no signal observed" means unknown, not
   confirmed disease-free.
4. Run a **mandatory validation gate** (manual chart-timeline review on a
   small stratified sample) before any cohort-scale modeling, to get a
   local, honest precision/recall estimate rather than assuming the
   Medicare/Kaiser performance figures transfer.
5. Keep METABRIC as an explicit fallback/benchmarking dataset (clean,
   validated recurrence label, but not full EHR) if the validation gate
   shows unacceptable label quality.

See the revised `cohort_definition.md` for the full design incorporating
these points.

