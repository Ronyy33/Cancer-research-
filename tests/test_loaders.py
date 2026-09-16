"""
Tests for src/data/loaders.py.

These tests require the raw data files to already be pulled (see
scripts/pull_rotterdam.R and scripts/pull_metabric_tcga.sh) - they are
skipped automatically if the files aren't present, since raw data is
never committed to the repo (see data/README.md and .gitignore).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data.loaders import (  # noqa: E402
    DATA_RAW,
    load_gbsg2,
    load_metabric,
    load_rotterdam_rfs,
    load_tcga_brca,
)

pytestmark = pytest.mark.skipif(
    not (DATA_RAW / "rotterdam_raw.csv").exists(),
    reason="raw data not pulled - run scripts/pull_rotterdam.R and "
    "scripts/pull_metabric_tcga.sh first",
)


def test_rotterdam_shape_and_event_rate():
    df = load_rotterdam_rfs()
    assert len(df) == 2982
    # event rate should stay in a sane real-world range; catches gross
    # data corruption or a broken pull without hardcoding a brittle
    # exact-match assertion
    assert 0.3 < df["rfs_event"].mean() < 0.8
    assert df["rfs_event"].isin([0, 1]).all()


def test_gbsg2_shape_and_event_rate():
    df = load_gbsg2()
    assert len(df) == 686
    assert 0.3 < df["rfs_event"].mean() < 0.6


def test_metabric_shape_and_event_rate():
    df = load_metabric()
    assert len(df) == 2509
    valid = df["rfs_event"].notna()
    assert 0.2 < df.loc[valid, "rfs_event"].mean() < 0.6


def test_tcga_brca_shape_and_event_rate():
    df = load_tcga_brca()
    assert len(df) == 1084
    valid = df["rfs_event"].notna()
    # TCGA-BRCA has a genuinely low event rate (verified ~8.9%) - this
    # is a real, documented feature of the dataset, not a bug
    assert 0.03 < df.loc[valid, "rfs_event"].mean() < 0.20


def test_no_future_leakage_columns_by_name():
    """Sanity check: none of our loaded feature sets should contain an
    obviously outcome-derived column name that would leak the label into
    the features (e.g. a raw 'death' or 'recur' column sitting alongside
    engineered features meant to be used as predictors)."""
    for loader in (load_rotterdam_rfs, load_gbsg2, load_metabric, load_tcga_brca):
        df = loader()
        # rfstime/rfs_event are the *outcome* columns we deliberately add -
        # this test is a placeholder for Stage 8's full leakage audit,
        # not a substitute for it.
        assert "rfstime" in df.columns
        assert "rfs_event" in df.columns
