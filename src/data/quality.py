"""
Reusable data quality checks for Stage 8.

Per project brief Section 16: before modeling, generate missingness,
duplicate, class-distribution, feature-distribution, outlier, and
categorical-cardinality reports for every cohort. Nothing here modifies
data - it only reports on it, so findings can be reviewed before any
cleaning/imputation decision is made.
"""

from __future__ import annotations

import pandas as pd


def missingness_report(df: pd.DataFrame) -> pd.DataFrame:
    """Per-column missing count/percentage, sorted worst-first."""
    n = len(df)
    miss = df.isna().sum()
    out = pd.DataFrame(
        {"n_missing": miss, "pct_missing": (miss / n * 100).round(2)}
    )
    return out.sort_values("pct_missing", ascending=False)


def duplicate_report(df: pd.DataFrame, id_col: str | None) -> dict:
    """Full-row duplicates, and duplicate IDs if an ID column is given."""
    result = {"n_fully_duplicate_rows": int(df.duplicated().sum())}
    if id_col is not None and id_col in df.columns:
        result["n_duplicate_ids"] = int(df[id_col].duplicated().sum())
    return result


def numeric_summary(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Standard describe() plus an IQR-based outlier flag count per column."""
    present = [c for c in cols if c in df.columns]
    desc = df[present].describe().T
    outlier_counts = []
    for c in present:
        s = df[c].dropna()
        if len(s) == 0:
            outlier_counts.append(0)
            continue
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 3 * iqr, q3 + 3 * iqr
        outlier_counts.append(int(((s < lo) | (s > hi)).sum()))
    desc["n_extreme_outliers_3xIQR"] = outlier_counts
    return desc


def categorical_summary(df: pd.DataFrame, cols: list[str]) -> dict[str, pd.Series]:
    """Value counts (including NaN) per categorical column."""
    present = [c for c in cols if c in df.columns]
    return {c: df[c].value_counts(dropna=False) for c in present}


def implausible_value_checks(df: pd.DataFrame, checks: dict[str, str]) -> dict[str, int]:
    """Run a dict of {column: pandas query string} implausibility checks.

    Example: {"age": "age < 0 or age > 110", "nodes": "nodes < 0"}
    Returns count of rows failing each check (i.e. count of implausible
    values found), not a boolean pass/fail, so magnitude can be judged.
    """
    results = {}
    for col, condition in checks.items():
        if col not in df.columns:
            results[col] = None
            continue
        try:
            n_bad = len(df.query(condition))
        except Exception as e:  # pragma: no cover - defensive
            n_bad = f"CHECK_FAILED: {e}"
        results[col] = n_bad
    return results
