"""
Cross-cohort harmonization for Rotterdam <-> GBSG2 (the primary
train/external-validate pair).

Handles two real issues found in Stage 8
(research/RESULTS/data_quality/SYNTHESIS.md):

1. Time units differ: Rotterdam/GBSG2 report survival time in DAYS.
   Everything is converted to MONTHS here (days / (365.25/12)) so it's
   on the same scale as METABRIC/TCGA-BRCA, should those be pooled later.

2. Column coding differs between the two cohorts even for conceptually
   identical variables (e.g. Rotterdam's categorical tumor-size bucket
   vs. GBSG2's continuous size in mm). A common feature schema is built
   here, with every mapping decision documented inline rather than
   silently guessed.

KNOWN, DOCUMENTED LIMITATION (not hidden): Rotterdam has zero grade-1
patients (see Stage 8 findings), so a model trained on Rotterdam has
never seen that category. GBSG2 has 81 grade-1 patients. Those patients
are NOT dropped from the external validation set (that would be
p-hacking the test set to look better) - instead they are encoded via
handle_unknown='ignore' in the one-hot encoder, which means the model
effectively cannot represent that category correctly for those patients.
This is reported as an explicit limitation of the external validation,
not swept under the rug.

Chemo is excluded from the common schema: GBSG2's publicly released
column set does not include a chemotherapy flag (all GBSG2 patients
received cytotoxic chemotherapy per the trial's own design - it was a
trial of chemo DURATION and hormonal therapy, not chemo vs. no chemo),
so there is no comparable variation to test against in the external set.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

DAYS_PER_MONTH = 365.25 / 12  # 30.4375 - standard conversion, documented

COMMON_NUMERIC = ["age", "nodes_positive", "er_value", "pr_value"]
COMMON_CATEGORICAL = ["menopause_post", "tumor_size_cat", "grade_cat", "hormone_therapy"]
COMMON_FEATURES = COMMON_NUMERIC + COMMON_CATEGORICAL


def _bucket_size_mm(size_mm: pd.Series) -> pd.Series:
    return pd.cut(
        size_mm,
        bins=[-np.inf, 20, 50, np.inf],
        labels=["<=20", "20-50", ">50"],
        right=True,
    )


def harmonize_rotterdam(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    out["age"] = df["age"]
    out["menopause_post"] = df["meno"].astype(int)  # already 1=post, 0=pre
    out["tumor_size_cat"] = df["size"].astype(str)  # already bucketed
    out["grade_cat"] = df["grade"].astype(str)  # "2" or "3" (no grade 1 - see module docstring)
    out["nodes_positive"] = df["nodes"]
    out["er_value"] = df["er"]
    out["pr_value"] = df["pgr"]
    out["hormone_therapy"] = df["hormon"].astype(int)
    out["rfstime_months"] = df["rfstime"] / DAYS_PER_MONTH
    out["rfs_event"] = df["rfs_event"].astype(bool)
    return out


def harmonize_gbsg2(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    out["age"] = df["age"]
    out["menopause_post"] = (df["menostat"] == "Post").astype(int)
    out["tumor_size_cat"] = _bucket_size_mm(df["tsize"]).astype(str)
    grade_map = {"I": "1", "II": "2", "III": "3"}
    out["grade_cat"] = df["tgrade"].map(grade_map)
    out["nodes_positive"] = df["pnodes"]
    out["er_value"] = df["estrec"]
    out["pr_value"] = df["progrec"]
    out["hormone_therapy"] = (df["horTh"] == "yes").astype(int)
    out["rfstime_months"] = df["rfstime"] / DAYS_PER_MONTH
    out["rfs_event"] = df["rfs_event"].astype(bool)
    return out


def to_structured_y(df: pd.DataFrame):
    """sksurv-style structured array: (event: bool, time: float)."""
    return np.array(
        list(zip(df["rfs_event"], df["rfstime_months"])),
        dtype=[("event", "?"), ("time", "<f8")],
    )
