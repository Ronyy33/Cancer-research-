"""
Tests for src/data/harmonize.py - the cross-cohort Rotterdam/GBSG2
harmonization logic (time-unit conversion, categorical mapping).

Also exercises the exact one-hot-encoding + Cox PH combination that
crashed with an "ill-conditioned matrix" error during Stage 9 (see
research/EXPERIMENTS/experiment_0001.md) until drop="first" was added -
this is a regression test for that specific bug, not just a smoke test.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data.harmonize import (  # noqa: E402
    DAYS_PER_MONTH,
    harmonize_gbsg2,
    harmonize_rotterdam,
    to_structured_y,
)
from src.data.loaders import DATA_RAW, load_gbsg2, load_rotterdam_rfs  # noqa: E402

pytestmark = pytest.mark.skipif(
    not (DATA_RAW / "rotterdam_raw.csv").exists(),
    reason="raw data not pulled - run scripts/pull_rotterdam.R first",
)


def test_time_conversion_sane():
    # Rotterdam rfstime max is ~7043 days -> should become ~231 months,
    # not something wildly off (catches a unit-conversion sign/factor bug)
    rot = harmonize_rotterdam(load_rotterdam_rfs())
    assert rot["rfstime_months"].max() == pytest.approx(7043 / DAYS_PER_MONTH, rel=0.01)
    assert 0 < rot["rfstime_months"].min()


def test_rotterdam_has_no_grade_1():
    rot = harmonize_rotterdam(load_rotterdam_rfs())
    assert "1" not in rot["grade_cat"].unique()


def test_gbsg2_grade_mapping_produces_all_three_grades():
    gbsg = harmonize_gbsg2(load_gbsg2())
    assert set(gbsg["grade_cat"].unique()) == {"1", "2", "3"}


def test_no_missing_values_in_harmonized_common_schema():
    from src.data.harmonize import COMMON_FEATURES

    rot = harmonize_rotterdam(load_rotterdam_rfs())
    gbsg = harmonize_gbsg2(load_gbsg2())
    for df, name in [(rot, "rotterdam"), (gbsg, "gbsg2")]:
        for col in COMMON_FEATURES:
            assert df[col].isna().sum() == 0, f"{name}.{col} has unexpected NaNs"


def test_onehot_encoding_does_not_crash_coxph():
    """Regression test for the exact bug found in experiment_0001: full
    (non-reduced) one-hot encoding across multiple categorical blocks
    made the Cox PH design matrix exactly rank-deficient (no intercept
    term to absorb the redundant all-ones combination), crashing with
    'ill-conditioned matrix' / NaN search direction. Fixed with
    drop='first'. This test fits a real CoxPH model end-to-end to make
    sure that fix holds."""
    from sksurv.linear_model import CoxPHSurvivalAnalysis

    from scripts.train_baselines import build_preprocessor  # noqa: E402

    rot = harmonize_rotterdam(load_rotterdam_rfs())
    from src.data.harmonize import COMMON_CATEGORICAL, COMMON_NUMERIC

    X = build_preprocessor().fit_transform(rot[COMMON_NUMERIC + COMMON_CATEGORICAL])
    y = to_structured_y(rot)

    model = CoxPHSurvivalAnalysis()
    model.fit(X, y)  # must not raise
    preds = model.predict(X)
    assert np.isfinite(preds).all()
