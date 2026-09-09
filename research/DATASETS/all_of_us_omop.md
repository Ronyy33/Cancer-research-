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

