# Data Directory

## ⚠️ Policy update — 2026-09-18

The original policy here was "no raw data is ever committed." That has
been **deliberately overridden for four specific files** at Kevin's
explicit request, so the real datasets can be shown directly (e.g. in a
meeting) without anyone needing to clone the repo and run the pull
scripts. This override is scoped narrowly — see below — not a blanket
policy change.

## What's actually committed, and why it's an acceptable exception

`data/raw/rotterdam_raw.csv`, `data/raw/gbsg2_raw.csv`,
`data/raw/metabric_clinical_patient.txt`, and
`data/raw/tcga_brca_clinical_patient.txt` are committed to this
repository. This is a narrow, explicit exception to the general rule
below, justified because:

- All four are **de-identified public research cohorts**, not real
  hospital records or identifiable patient data — Rotterdam (Rotterdam
  Tumour Bank, 1978–1993), GBSG2 (German Breast Cancer Study Group trial),
  METABRIC, and TCGA-BRCA (PanCancer Atlas 2018).
- Rotterdam and GBSG2 are already freely redistributed as part of
  standard, widely-used software packages (R's `survival` package;
  Python's `scikit-survival`), so committing them here adds no new
  exposure.

**⚠️ Unverified caveat, stated honestly:** METABRIC and TCGA-BRCA were
pulled from cBioPortal's public GitHub data mirror
(`github.com/cBioPortal/datahub`). Their specific redistribution terms
(as opposed to terms for *using* the data in analysis) were **not
independently verified** before committing them here. If this repository
is or becomes public, and strict redistribution compliance matters,
this should be checked against cBioPortal's data usage policy before
relying on it further.

## Everything else in `data/` remains excluded from version control

`data/interim/`, `data/processed/`, and any other file under `data/`
besides the four named above are still gitignored, per the general rule
below. This exception covers exactly the four raw source files, nothing
derived from them.

## Directory structure

```
data/
  raw/            # as-pulled source data (4 files committed, see above; anything else here stays untracked)
  interim/        # intermediate cleaning steps (never committed)
  processed/      # model-ready cohort files (never committed)
```

## How each file was obtained (reproducible from scratch)

- `rotterdam_raw.csv` — `Rscript scripts/pull_rotterdam.R` (pulls directly
  from R's `survival` package)
- `gbsg2_raw.csv` — `sksurv.datasets.load_gbsg2()` (scikit-survival)
- `metabric_clinical_patient.txt`, `tcga_brca_clinical_patient.txt` —
  `bash scripts/pull_metabric_tcga.sh` (cBioPortal's public GitHub mirror)

## General hard rules (still in force for everything not named above)

- Never commit identifiable patient information.
- Never commit raw clinical datasets sourced from real hospital
  EHR/institutional access, even de-identified ones — the exception above
  applies only to the four named public research-cohort files.
- Never bypass access restrictions (registration, DUA, IRB).
