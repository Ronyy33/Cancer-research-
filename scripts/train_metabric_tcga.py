"""
Stage 9 (continued) - METABRIC and TCGA-BRCA as independent real-data
cross-checks.

Unlike Rotterdam/GBSG2 (a genuine train/external-validate PAIR with
comparable native features), METABRIC and TCGA-BRCA each have their own
different native feature set and no natural external-validation partner
in this project's current dataset lineup. So each is evaluated
independently here via WITHIN-cohort train/test split + CV, NOT treated
as an external validation of the Rotterdam-trained model - that would be
methodologically wrong given the different feature sets. This is
labeled clearly throughout, per the project's standard against
overstating validation rigor (Section 22).

METABRIC: the ~528-patient block-missingness batch found in Stage 8
(research/RESULTS/data_quality/SYNTHESIS.md) is excluded here, using the
EXACT reproducible rule from that investigation (rows missing in >=10 of
12 checked columns) rather than a cohort-number heuristic (COHORT=1
appears in BOTH the complete and incomplete groups, so filtering by
cohort number alone would be wrong - confirmed during Stage 8).

TCGA-BRCA: only 84 real recurrence events total (Stage 8 finding). A
further train/test split would leave too few test-set events for a
stable estimate, so only 5-fold CV is reported here - itself a
documented limitation of this cohort, not a shortcut taken silently.

Run: python scripts/train_metabric_tcga.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import KFold, train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sksurv.ensemble import GradientBoostingSurvivalAnalysis, RandomSurvivalForest
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.metrics import concordance_index_censored

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.loaders import load_metabric, load_tcga_brca  # noqa: E402

RESULTS_DIR = ROOT / "research" / "RESULTS" / "experiments"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
RANDOM_STATE = 42


def to_structured_y(time, event):
    return np.array(list(zip(event.astype(bool), time)), dtype=[("event", "?"), ("time", "<f8")])


def cv_concordance(model_factory, X, y, n_splits=5):
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    scores = []
    for tr, va in kf.split(X):
        m = model_factory()
        m.fit(X[tr], y[tr])
        pred = m.predict(X[va])
        scores.append(concordance_index_censored(y[va]["event"], y[va]["time"], pred)[0])
    return float(np.mean(scores)), float(np.std(scores))


def run_model_suite(X_train, y_train, X_test=None, y_test=None, label=""):
    models = {
        "Cox PH": lambda: CoxPHSurvivalAnalysis(),
        "Random Survival Forest": lambda: RandomSurvivalForest(
            n_estimators=300, min_samples_split=10, min_samples_leaf=15,
            n_jobs=-1, random_state=RANDOM_STATE,
        ),
        "Gradient Boosting Survival": lambda: GradientBoostingSurvivalAnalysis(
            n_estimators=200, learning_rate=0.05, max_depth=3, random_state=RANDOM_STATE,
        ),
    }
    rows = []
    for name, factory in models.items():
        model = factory()
        model.fit(X_train, y_train)
        train_c = concordance_index_censored(
            y_train["event"], y_train["time"], model.predict(X_train)
        )[0]
        cv_mean, cv_std = cv_concordance(factory, X_train, y_train)
        row = {"cohort": label, "model": name, "train_cindex": train_c,
               "cv_mean": cv_mean, "cv_std": cv_std}
        if X_test is not None:
            test_c = concordance_index_censored(
                y_test["event"], y_test["time"], model.predict(X_test)
            )[0]
            row["holdout_test_cindex"] = test_c
        rows.append(row)
    return rows


def metabric_experiment():
    print("=" * 70)
    print("METABRIC (within-cohort, incomplete batch excluded)")
    print("=" * 70)
    df = load_metabric()

    check_cols = [
        "CELLULARITY", "BREAST_SURGERY", "INFERRED_MENOPAUSAL_STATE",
        "CLAUDIN_SUBTYPE", "INTCLUST", "HER2_SNP6", "HORMONE_THERAPY",
        "CHEMOTHERAPY", "VITAL_STATUS", "RADIO_THERAPY", "OS_STATUS", "OS_MONTHS",
    ]
    incomplete_block = df[check_cols].isna().sum(axis=1) >= 10
    print(f"Excluding {incomplete_block.sum()} patients in the incomplete-batch block")
    df = df.loc[~incomplete_block].copy()

    df = df.dropna(subset=["RFS_MONTHS", "rfs_event"])
    print(f"After dropping missing outcome: N={len(df)}")

    numeric_cols = ["NPI", "AGE_AT_DIAGNOSIS", "LYMPH_NODES_EXAMINED_POSITIVE"]
    categorical_cols = ["ER_IHC", "HER2_SNP6", "HORMONE_THERAPY", "CHEMOTHERAPY",
                         "INFERRED_MENOPAUSAL_STATE"]
    df = df.dropna(subset=numeric_cols + categorical_cols)
    print(f"After complete-case on modeling features: N={len(df)}")
    print(f"Events: {int(df['rfs_event'].sum())} ({df['rfs_event'].mean()*100:.1f}%)")

    preproc = ColumnTransformer([
        ("num", StandardScaler(), numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", drop="first", sparse_output=False),
         categorical_cols),
    ])
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=RANDOM_STATE)
    X_train = preproc.fit_transform(train_df[numeric_cols + categorical_cols])
    X_test = preproc.transform(test_df[numeric_cols + categorical_cols])
    y_train = to_structured_y(train_df["RFS_MONTHS"].values, train_df["rfs_event"].values)
    y_test = to_structured_y(test_df["RFS_MONTHS"].values, test_df["rfs_event"].values)

    rows = run_model_suite(X_train, y_train, X_test, y_test, label="metabric")
    for r in rows:
        print(r)
    return rows


def tcga_experiment():
    print("\n" + "=" * 70)
    print("TCGA-BRCA (within-cohort, 5-fold CV only - too few events for a held-out split)")
    print("=" * 70)
    df = load_tcga_brca()
    df = df.dropna(subset=["DFS_MONTHS", "rfs_event"])
    print(f"After dropping missing outcome: N={len(df)}")

    numeric_cols = ["AGE"]
    categorical_cols = ["PATH_M_STAGE", "SUBTYPE", "RADIATION_THERAPY"]
    df = df.dropna(subset=numeric_cols + categorical_cols)
    print(f"After complete-case on modeling features: N={len(df)}")
    print(f"Events: {int(df['rfs_event'].sum())} ({df['rfs_event'].mean()*100:.1f}%)")

    preproc = ColumnTransformer([
        ("num", StandardScaler(), numeric_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", drop="first", sparse_output=False),
         categorical_cols),
    ])
    X = preproc.fit_transform(df[numeric_cols + categorical_cols])
    y = to_structured_y(df["DFS_MONTHS"].values, df["rfs_event"].values)

    rows = run_model_suite(X, y, label="tcga_brca")
    for r in rows:
        print(r)
    return rows


def main():
    rows = metabric_experiment() + tcga_experiment()
    out = pd.DataFrame(rows)
    print("\n" + "=" * 90)
    print(out.to_string(index=False))
    out_path = RESULTS_DIR / "experiment_0002_metabric_tcga.csv"
    out.to_csv(out_path, index=False)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
