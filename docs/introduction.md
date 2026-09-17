# Introduction

Breast cancer recurrence — the return of disease after primary treatment,
either locoregionally or at a distant site — remains one of the most
consequential uncertainties in survivorship care. Reliable, individualized
risk estimates could inform surveillance intensity, adjuvant treatment
duration, and patient counseling. Machine learning has been applied
extensively to this problem over the past decade, spanning classical
statistical models, tree-based ensembles, and, more recently, deep
learning and natural-language-processing approaches applied to clinical
text.

Despite this volume of work, a systematic review of the literature
conducted as part of this research program (32 papers reviewed;
`research/LITERATURE_MATRIX.csv`) identified a specific, recurring
methodological gap rather than a lack of activity: **models are rarely
validated on more than one institution or cohort**, and a substantial
fraction of studies described as predicting recurrence are, on inspection,
detecting recurrence that has already occurred and is documented
somewhere in the retrospective record — a materially different and easier
task than genuine forward prediction. A further, independently
corroborated finding from that review is that structured, billing-code-
derived recurrence labels substantially undercount true recurrence
relative to labels derived from clinical text or manual chart review
(one well-verified study found ICD-coded recurrence captured only 2.3%
of cases versus 11.1% confirmed by natural language processing).

This project set out to address the external-validation gap directly:
develop a recurrence-free survival model and validate it on data the
model never saw during training or model selection, using real patient
data throughout. The original intent was to use genuine longitudinal
electronic health record (EHR) data, reflecting the more clinically
realistic setting of repeated encounters over time rather than a single
diagnostic snapshot. That ambition was constrained by a concrete, real-
world access barrier encountered during the project (lack of
institutional sponsorship for the EHR resource initially targeted; see
`research/DECISIONS.md` entries D003–D007), which is documented here
rather than elided, since it materially shaped the final study design.

The study that resulted uses four independent, real, publicly accessible
patient cohorts, each a baseline-snapshot-plus-survival-time design rather
than a repeated-measures EHR timeline. Within that constraint, the study
asks two concrete questions: (1) can a model trained on one real cohort
generalize to another, previously unseen real cohort, at a level
consistent with (or exceeding) prior work that lacks such validation; and
(2) is additional model complexity — random survival forests, gradient
boosted survival models — empirically justified over classical Cox
regression for this problem, rather than assumed justified because more
complex methods exist in the literature.
