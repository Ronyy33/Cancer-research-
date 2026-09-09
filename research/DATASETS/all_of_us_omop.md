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
