# Temporal Leakage Audit

**Status:** Pre-emptive audit based on literature review findings. No cohort has been constructed yet (Stage 7 not started), so this file currently documents **leakage patterns observed in the reviewed literature** and the audit checklist our own pipeline must pass before any modeling begins. It will be updated with concrete per-feature findings once we build our own cohort.

## Leakage risks identified in the literature we reviewed

| Paper | Leakage risk observed |
|---|---|
| P0002 (Wang et al.) | Could not confirm whether input notes were restricted to a pre-prediction cutoff or spanned the full chart — real risk of detection mislabeled as prediction |
| P0003 (Sanyal et al.) | High AUROC (0.94) with unconfirmed input-text cutoff relative to the recurrence event — flagged for scrutiny |
| P0004 (González-Castro et al.) | High precision/recall (0.90/0.91) on N=823 without confirmed cross-validation or external validation — optimism-bias risk |
| P0012 (Sukhadia et al.) | AUC=1.0 on a 17-patient test set — a textbook small-sample overfitting red flag, not evidence of a leak-free robust model, but illustrates how easy it is to produce misleadingly perfect results without adequate validation |
| P0016 (Multimodal BEHRT) | Correct landmark-time design (a positive example), but outcome-label provenance (coded vs. NLP vs. manual) not specified — if the DFS label used post-cutoff information to retrospectively assign the label, that would itself be a leakage pathway even with correct feature timing |
| P0026 (SEER survival ML) | Large train (0.824) → internal-validation (0.689) C-index drop — consistent with overfitting/optimistic bias |

## Hard requirement for our own pipeline (once cohort construction begins)

For every feature we build, we will ask: **"Was this information genuinely available at prediction time?"** and check against:

- Future diagnoses, procedures, medications, treatment, notes, pathology, imaging
- Recurrence codes appearing before the clinically-confirmed recurrence date
- Retrospective statements in notes (e.g., a note written after recurrence that describes the pre-recurrence course)
- Duplicated encounters
- Future laboratory values
- Outcome-derived features (e.g., a "started palliative chemo" flag that is itself evidence of recurrence, if not carefully time-bounded)

**Given Gap 2 (structured/coded recurrence labels under-ascertain true recurrence by ~5x per P0005), our own outcome-label construction is itself a leakage-sensitive process**: if we build labels via NLP over the full chart, we must ensure the *label-assignment* process (which can look at the whole chart to determine ground truth) is kept strictly separate from the *feature-assignment* process (which must only see data up to the prediction time T). This is a distinct and easy-to-miss leakage pathway beyond ordinary feature leakage.

If leakage is found in our own pipeline: **STOP the relevant experiment, fix it, and document the fix here** before any results from that experiment are used elsewhere in the repository.

*(This file will be expanded with a concrete feature-by-feature audit table once Stage 7 cohort construction begins.)*
