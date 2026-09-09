# Dataset: I-SPY2 (via TCIA / The Cancer Imaging Archive)

**Real or synthetic:** Real, adaptive platform trial (NCT01042379), neoadjuvant treatment for stage 2/3 breast cancer.

**Important distinction:** The full trial enrolled 2,118 patients (2010–2022) with follow-up on 2,005 as of Jan 2024, but the **publicly released TCIA imaging dataset is a sub-cohort**: "I-SPY2 Imaging Cohort 1" = 985 patients (719 + 266 from the ISPY2/ACRIN-6698 collections) with serial DCE-MRI + pathologic complete response (pCR) outcome.

**Content:** Serial breast MRI (DCE-MRI, DWI) acquired at **4 timepoints before/during/after neoadjuvant chemotherapy**, plus pCR at surgery as the primary outcome; limited accompanying clinical/pathologic covariates (receptor subtype, stage). No detailed medications/labs/notes.

**Longitudinal structure:** Yes — genuinely one of the strongest datasets found for **true multi-timepoint, treatment-response** prediction (index = pre-treatment baseline, features can include early on-treatment imaging, outcome = pCR). Some associated publications report 3-year event-free/distant-recurrence-free survival, but this is **not confirmed to be bundled into the base public TCIA file release** — would need separate per-file verification.

**Access:** Public TCIA collection; typically requires a **free TCIA/NBIA account** for bulk download via the Data Retriever tool, but no DUA/fee/IRB for de-identified public collections. Realistically autonomously accessible.

**License:** TCIA collections are generally released under a Creative Commons license (commonly CC BY 3.0/4.0, sometimes CC BY-NC) — exact license for this specific collection UNKNOWN, not verified this session; TCIA requires citation regardless.

**IRB:** Not required for the public de-identified collection.

**Usefulness for this project:** Excellent fit specifically for a **treatment-response prediction** research question (neoadjuvant chemo → pCR), which is one of the candidate problem areas in the project brief. Narrow scope otherwise (imaging-centric, ~985 patients, limited clinical covariates, no broad EHR variables).

**Limitations:** Moderate N for deep learning; imaging-centric (not a general EHR dataset); longer-term outcome (distant recurrence) not confirmed bundled in the public release.

**Ranking: ★★★★☆** — genuine multi-timepoint temporal structure tied to a defined outcome; fully public; best fit if the research question narrows specifically to treatment-response prediction rather than recurrence/survival broadly.
