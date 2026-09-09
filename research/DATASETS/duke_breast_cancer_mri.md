# Dataset: Duke-Breast-Cancer-MRI (Saha et al. 2018)

**Real or synthetic:** Real, single-institution (Duke University), biopsy-confirmed invasive breast cancer patients, Jan 2000–Mar 2014.

**N = 922** (verified across multiple independent sources: TCIA wiki, the original Saha et al. 2018 *British Journal of Cancer* paper, and multiple downstream ML papers). A widely-cited follow-up validation subset uses n=892 with "pertinent follow-up data" (Mazurowski et al. 2019, *JMRI*).

**Outcome variables — genuinely useful, confirmed present:** the clinical spreadsheet (~100 columns, sourced from oncology clinic notes in the EMR) includes "Days to last local recurrence-free assessment," "Days to last distant recurrence-free assessment," and "Days to last contact" — a real time-to-event structure for both local recurrence-free survival (LRFS) and distant recurrence-free survival (DRFS), not just imaging metadata.

**Other clinical/pathologic variables:** demographics, tumor stage/grade, ER/PR/HER2, molecular subtype, surgery/chemo/radiation treatment details, pathology, and genomic data (Oncotype DX/gene panel) for a subset. This is a genuinely richer clinical feature set than Rotterdam/GBSG2/METABRIC — closer in spirit to real EHR-derived clinical variables.

**⚠️ Open item — must verify before committing:** the exact recurrence event count/percentage could not be confirmed from search snippets despite repeated targeted searches. Several downstream papers build recurrence classifiers on this data (implying a workable event count exists), but the raw number is unconfirmed. **First action item: pull the actual clinical CSV/Excel from TCIA and count events directly before relying on this dataset for modeling** — if the event rate is very low, statistical power will be a real constraint despite N=922.

**Access:** Public TCIA/NBIA collection, Creative Commons Attribution license. Described consistently as downloadable via the free NBIA Data Retriever; an account may be needed for some download options but this is free self-registration, not institutional — same access tier as I-SPY2, which we already confirmed is autonomously accessible.

**Longitudinal depth:** Imaging is largely single pre-operative DCE-MRI timepoint (not serial like I-SPY1/I-SPY2). Clinical follow-up is a real time-to-event outcome, but not a repeated-measures EHR timeline.

**Usefulness for this project:** Can be used two ways — (a) as a pure structured-clinical dataset (ignore the MRI images entirely), giving a fourth independent real cohort with richer clinical covariates than the classic biostatistics datasets, or (b) as a genuine multimodal imaging+clinical dataset if we want to test whether imaging features add predictive value on top of clinical variables (echoes the structured-vs-unstructured ablation question from the literature review, Section 19 of the project brief).

**Ranking: ★★★★☆** — best-verified real recurrence outcome among the imaging-consortium datasets, largest usable N in that category, no institutional barrier. Held at 4 rather than 5 stars pending the event-rate verification above.
