"""
Stage 7 verification script - Rotterdam + GBSG2.

Loads the real Rotterdam and GBSG2 datasets via scikit-survival / lifelines
and prints their actual shape, columns, and event rates, so we can update
our documentation with numbers we've verified ourselves rather than
numbers sourced from search-engine snippets (which is all we had access
to earlier this session, since WebFetch was blocked).

Does not write any files - this is a verification/inspection script.
Run: python scripts/verify_rotterdam_gbsg2.py
"""

import sys


def verify_gbsg2():
    print("=" * 70)
    print("GBSG2 (German Breast Cancer Study Group 2)")
    print("=" * 70)
    try:
        from sksurv.datasets import load_gbsg2

        X, y = load_gbsg2()
        print(f"Loaded via sksurv.datasets.load_gbsg2()")
        print(f"N patients: {X.shape[0]}")
        print(f"Columns ({X.shape[1]}): {list(X.columns)}")
        print(f"Outcome dtype: {y.dtype}")
        event_field, time_field = y.dtype.names
        n_events = int(y[event_field].sum())
        print(f"Event field: '{event_field}', time field: '{time_field}'")
        print(f"N events (recurrence/death): {n_events} ({n_events / len(y) * 100:.1f}%)")
        print(f"Time field range: {y[time_field].min()} - {y[time_field].max()}")
        print()
        print("First 3 rows of X:")
        print(X.head(3))
        return X, y
    except Exception as e:
        print(f"FAILED to load GBSG2: {type(e).__name__}: {e}")
        return None, None


def verify_rotterdam():
    print()
    print("=" * 70)
    print("Rotterdam breast cancer dataset")
    print("=" * 70)
    # scikit-survival does not bundle Rotterdam directly as far as we
    # verified via search (unconfirmed). Try a few plausible sources.
    tried = []

    # Attempt 1: pycox (bundles a combined/derived "gbsg" dataset built
    # from Rotterdam+GBSG per Katzman et al. DeepSurv benchmark - need to
    # verify exactly what this contains, per our research agent's own
    # flagged ambiguity about this).
    try:
        import pycox.datasets as pycox_datasets

        df = pycox_datasets.gbsg.read_df()
        tried.append("pycox.datasets.gbsg")
        print(f"Loaded via pycox.datasets.gbsg.read_df()")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(df.head(3))
        print()
        print(
            "NOTE: pycox's 'gbsg' dataset is the Katzman et al. DeepSurv "
            "benchmark version - need to confirm whether this is Rotterdam "
            "(1546 subset), full GBSG2 (686), or a combined/different "
            "cohort before assuming it matches either of our documented "
            "sources. Do not assume - compare N and columns against the "
            "verified GBSG2 above."
        )
        return df
    except Exception as e:
        print(f"pycox.datasets.gbsg FAILED: {type(e).__name__}: {e}")

    # Attempt 2: R's survival::rotterdam dataset is not directly available
    # in Python. Check if there's a CSV mirror commonly used in tutorials.
    print(
        "\nRotterdam does not appear to have a direct Python package "
        "equivalent bundled the way GBSG2 does via scikit-survival. "
        "Options to get the REAL Rotterdam data:\n"
        "  1. Use rpy2 to pull survival::rotterdam directly from R (most "
        "     authoritative - it's R's own bundled dataset)\n"
        "  2. Find a verified CSV mirror (must verify provenance/checksum "
        "     against the R package, not just trust an arbitrary CSV)\n"
        "  3. Use the pycox 'gbsg' bundle if it turns out to BE the "
        "     Rotterdam-derived training set used in the DeepSurv paper "
        "     (needs verification, see above)"
    )
    return None


if __name__ == "__main__":
    X, y = verify_gbsg2()
    df_rotterdam_candidate = verify_rotterdam()
    print()
    print("=" * 70)
    print("Verification run complete.")
    print("=" * 70)
