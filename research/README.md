# Breast Cancer + Real-World EHR/Clinical Data + AI/ML — Research Program

This directory is the single source of truth for an ongoing research program.
It is organized so that at any point, anyone (including a future session of
this same agent) can answer:

- What are we doing, and why?
- What has already been tested?
- What failed? What succeeded?
- What remains?
- What decision is currently pending from the human researcher (Kevin)?

## Directory Map

| Path | Purpose |
|---|---|
| `RESEARCH_STATE.md` | Current stage in the research state machine (Stage 0–16), updated continuously |
| `ROADMAP.md` | The full stage plan and what each stage requires to be considered complete |
| `DECISIONS.md` | Log of every consequential decision, with rationale and date |
| `RESEARCH_GAPS.md` | Evidence-backed gaps in the existing literature, each supported by cited papers |
| `LITERATURE_MATRIX.csv` | Structured table of every paper reviewed |
| `PAPERS/` | One Markdown note per high-value paper (`P####_<short_name>.md`) |
| `DATASETS/` | One Markdown note per candidate dataset, with verified (not assumed) contents |
| `EXPERIMENTS/` | One Markdown file per experiment run, append-only (never overwritten) |
| `RESULTS/` | Analysis outputs (data quality, evaluation results) |
| `FIGURES/` | Generated plots |
| `NOTES/` | Scratch/working notes that don't belong elsewhere yet |
| `cohort_definition.md` | Index date, prediction time, observation window, horizon, in/exclusion criteria |
| `LEAKAGE_AUDIT.md` | Temporal leakage audit — every feature checked against "was this known at prediction time?" |
| `REPORTING_CHECKLIST.md` | Applicable reporting guideline (TRIPOD+AI / STROBE / PROBAST-AI) checklist |
| `PROGRESS.md` | Running log: completed / in progress / failed / blocked / next step / decisions needed |

## Guiding Principle

We are not building "another breast cancer ML model." We are trying to answer:

> What clinically meaningful problem in breast cancer can be addressed using
> real-world EHR data, where existing AI approaches have a demonstrable
> limitation, and where we can produce a scientifically defensible
> improvement?

Everything in this repository supports that question. Be skeptical, be
evidence-driven, be reproducible. Prefer simple models when they are
sufficient. Never fabricate papers, datasets, results, or gaps. Never use
future information in a prediction feature. Never optimize for
impressive-looking metrics at the expense of validity.

See `ROADMAP.md` for the current stage and `RESEARCH_STATE.md` for live status.
