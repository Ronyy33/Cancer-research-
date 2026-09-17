# Conclusion

This study developed a recurrence-free survival prediction pipeline for
breast cancer using exclusively real, publicly accessible patient-level
data, with genuine external validation between independent cohorts as a
first-class design goal rather than an afterthought. Classical Cox
proportional hazards regression achieved external validation performance
within 0.013–0.018 concordance index of more complex tree-based
ensembles, while showing substantially better stability between training
and test performance — a pattern that replicated across two structurally
different real cohorts and independently reproduces a comparable finding
already present in the literature. On the evidence gathered, additional
model complexity is not currently justified for this problem at this
feature scale, and Cox PH is recommended as the primary model.

Explainability analysis found that the model's internal reasoning aligns
with established breast cancer prognostic factors (nodal status, tumor
size, grade), supporting confidence in the modeling pipeline. Subgroup
analysis identified a specific, actionable limitation: reduced
discrimination among patients with intermediate nodal burden, the
population in which improved risk stratification would plausibly be most
clinically useful.

This work does not close two gaps it set out, in its original framing, to
address: genuinely longitudinal EHR-based modeling, and assessment of
demographic equity — both blocked by real, documented data-access
constraints encountered during the project rather than by a change in
scientific priority. These remain the most direct paths for extending
this work, alongside targeted feature engineering for the intermediate-
nodal-burden subgroup identified here. The full record of decisions,
pivots, and their rationale is preserved in `research/DECISIONS.md` and
`research/RESEARCH_STATE.md`, so that this study's actual path —
including its constraints — remains legible rather than retrospectively
smoothed over.
