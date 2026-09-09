# P0020 — DFCI Shareable AI Model (2025) — Genuine Cross-Institution External Validation

**Citation:** "Integrating a Shareable Artificial Intelligence Model Into Clinical Research for Cancer Recurrence in Patients With Breast and Colorectal Cancer." *JCO Clinical Cancer Informatics* 2025.
**Link:** DOI 10.1200/CCI-25-00143 · PMC12700351

**What this is:** A Dana-Farber Cancer Institute (DFCI)-developed NLP recurrence-identification model ("DFCI-imaging-student"), shared and deployed at an **entirely independent health system** — Kaiser Permanente Northern California — and re-validated there.

**Cohort:** 200 breast + 200 colorectal cancer patients at the external site.

**Task:** Recurrence identification + time-to-recurrence estimation from EHR text (INFORMATION EXTRACTION/DETECTION, not forward prediction).

**Results:** 90% accuracy for recurrence identification at the external site; median time-to-recurrence error <2 weeks vs. manual chart review.

**Why this matters:** This is one of the only papers found in either literature search that actually tests **model portability across genuinely different health systems** — directly addressing the field's dominant weak spot (near-total absence of true external validation, as documented across the systematic reviews P0006/P0007 and echoed by the Ritzwoller critique P0008 about NLP portability concerns). It is direct empirical evidence that portability is achievable, at least for this extraction task, when explicitly engineered and tested for.

**Limitations:** Small external test set (200+200); detection/extraction task, not a predictive model; single external site (not a multi-site network validation).

**Relevance to our project:** ★★★★★ — a template for how we should validate any label-generation or prediction tool: budget for genuine external-site testing from the start rather than treating it as a stretch goal.
