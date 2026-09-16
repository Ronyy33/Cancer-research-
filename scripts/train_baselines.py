"""
Stage 9 - Baseline survival models.

Trains on Rotterdam (N=2,982), externally validates on GBSG2 (N=686) -
the real, citable train/external-validate pairing documented in
research/DATASETS/rotterdam_gbsg2.md (Royston & Altman 2013; the
standard DeepSurv/pycox benchmark split).

Models, in increasing complexity (per project brief Section 17 -
baselines first, simplest-sufficient-model philosophy):
  1. Kaplan-Meier (population-average baseline, no covariates - a
     sanity floor, not a real "model")
  2. Cox Proportional Hazards (standard)
  3. Elastic-Net Cox (regularized, alpha selected via 5-fold CV on
     the training set only - GBSG2 is never touched during model
     selection, only for final external evaluation)
  4. Random Survival Forest
  5. Gradient Boosting Survival Analysis

Metric: Harrell's concordance index (C-index), reported on:
  - Rotterdam in-sample (train)
  - Rotterdam 5-fold cross-validated (a more honest internal estimate)
  - GBSG2 (the real external validation - this is the number that
    matters most)

A large train-vs-external gap is itself an important, honestly-reported
finding (per project brief Section 28 - never manipulate experiments to
get better numbers; report the field's typical train->validation drop
if we see it too, per RESEARCH_GAPS.md Gap 3).

Run: python scripts/train_baselines.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sksurv.ensemble import GradientBoostingSurvivalAnalysis, RandomSurvivalForest
from sksurv.linear_model import CoxnetSurvivalAnalysis, CoxPHSurvivalAnalysis
from sksurv.metrics import concordance_index_censored
from sksurv.nonparametric import kaplan_meier_estimator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.harmonize import (  # noqa: E402
    COMMON_CATEGORICAL,
    COMMON_NUMERIC,
    harmonize_gbsg2,
    harmonize_rotterdam,
    to_structured_y,
)
from src.data.loaders import load_gbsg2, load_rotterdam_rfs  # noqa: E402

RESULTS_DIR = ROOT / "research" / "RESULTS" / "experiments"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42


def build_preprocessor() -> ColumnTransformer:
    # drop="first": with 4 one-hot-encoded categorical blocks and NO
    # intercept term (Cox models have none), leaving every block
    # un-reduced makes each block's dummies sum to a constant 1-vector -
    # those constants collide across blocks, producing an exactly
    # rank-deficient design matrix (confirmed: this crashed CoxPH's
    # Newton-Raphson solver with "ill-conditioned matrix" / NaN search
    # direction on the first run). Dropping one reference category per
    # categorical variable removes the redundancy.
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), COMMON_NUMERIC),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", drop="first", sparse_output=False),
                COMMON_CATEGORICAL,
            ),
        ]
    )


def cv_concordance(model_factory, X, y, n_splits=5, random_state=RANDOM_STATE):
    """Manual K-fold CV concordance index (sksurv models don't plug
    directly into sklearn's cross_val_score without a custom scorer)."""
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    scores = []
    for train_idx, val_idx in kf.split(X):
        model = model_factory()
        model.fit(X[train_idx], y[train_idx])
        pred = model.predict(X[val_idx])
        c_index = concordance_index_censored(
            y[val_idx]["event"], y[val_idx]["time"], pred
        )[0]
        scores.append(c_index)
    return float(np.mean(scores)), float(np.std(scores))


def select_coxnet_alpha(X, y, l1_ratio=0.5, n_splits=5):
    """Pick the Coxnet alpha with the best 5-fold CV concordance index,
    selected using ONLY the training data (Rotterdam) - GBSG2 is never
    touched during model selection."""
    path_model = CoxnetSurvivalAnalysis(
        l1_ratio=l1_ratio, alpha_min_ratio=0.01, n_alphas=20
    )
    path_model.fit(X, y)
    alphas = path_model.alphas_

    best_alpha, best_score = None, -np.inf
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    for alpha in alphas:
        fold_scores = []
        for train_idx, val_idx in kf.split(X):
            m = CoxnetSurvivalAnalysis(l1_ratio=l1_ratio, alphas=[alpha])
            try:
                m.fit(X[train_idx], y[train_idx])
                pred = m.predict(X[val_idx])
                c = concordance_index_censored(
                    y[val_idx]["event"], y[val_idx]["time"], pred
                )[0]
                fold_scores.append(c)
            except Exception:
                fold_scores.append(np.nan)
        mean_score = np.nanmean(fold_scores)
        if mean_score > best_score:
            best_score, best_alpha = mean_score, alpha
    return best_alpha, best_score


def main():
    print("Loading and harmonizing Rotterdam (train) + GBSG2 (external test)...")
    rot = harmonize_rotterdam(load_rotterdam_rfs())
    gbsg = harmonize_gbsg2(load_gbsg2())
    print(f"Rotterdam: N={len(rot)}, events={rot['rfs_event'].sum()}")
    print(f"GBSG2: N={len(gbsg)}, events={gbsg['rfs_event'].sum()}")

    grade1_in_gbsg2 = (gbsg["grade_cat"] == "1").sum()
    print(
        f"\nNOTE (documented limitation): GBSG2 has {grade1_in_gbsg2} grade-1 "
        f"patients; Rotterdam (training data) has none. These patients are "
        f"KEPT in the external validation set (not dropped to inflate "
        f"performance) but their grade feature is out-of-distribution for "
        f"the trained model."
    )

    preprocessor = build_preprocessor()
    X_train = preprocessor.fit_transform(rot[COMMON_NUMERIC + COMMON_CATEGORICAL])
    X_test = preprocessor.transform(gbsg[COMMON_NUMERIC + COMMON_CATEGORICAL])
    y_train = to_structured_y(rot)
    y_test = to_structured_y(gbsg)

    results = []

    # 1. Kaplan-Meier population baseline (no covariates - C-index is
    # undefined/meaningless for a model with no risk ordering, so we
    # report it separately as a descriptive sanity check, not in the
    # main comparison table)
    time_points, survival_prob = kaplan_meier_estimator(
        rot["rfs_event"].values, rot["rfstime_months"].values
    )
    print(
        f"\nKaplan-Meier (Rotterdam, population-average): "
        f"median follow-up ~{time_points[len(time_points)//2]:.1f} months, "
        f"survival at 60mo ~{survival_prob[np.searchsorted(time_points, 60)]:.2f}"
        if (time_points < 60).any()
        else ""
    )

    # 2. Cox Proportional Hazards
    print("\nFitting Cox Proportional Hazards...")
    cox = CoxPHSurvivalAnalysis()
    cox.fit(X_train, y_train)
    train_c = concordance_index_censored(
        y_train["event"], y_train["time"], cox.predict(X_train)
    )[0]
    cv_mean, cv_std = cv_concordance(lambda: CoxPHSurvivalAnalysis(), X_train, y_train)
    test_c = concordance_index_censored(
        y_test["event"], y_test["time"], cox.predict(X_test)
    )[0]
    results.append(
        {"model": "Cox PH", "train_cindex": train_c, "cv_mean": cv_mean,
         "cv_std": cv_std, "external_gbsg2_cindex": test_c}
    )

    # 3. Elastic-Net Cox (alpha selected via CV on training data only)
    print("Fitting Elastic-Net Cox (selecting alpha via 5-fold CV)...")
    best_alpha, best_cv_score = select_coxnet_alpha(X_train, y_train, l1_ratio=0.5)
    coxnet = CoxnetSurvivalAnalysis(l1_ratio=0.5, alphas=[best_alpha])
    coxnet.fit(X_train, y_train)
    train_c = concordance_index_censored(
        y_train["event"], y_train["time"], coxnet.predict(X_train)
    )[0]
    test_c = concordance_index_censored(
        y_test["event"], y_test["time"], coxnet.predict(X_test)
    )[0]
    results.append(
        {"model": f"Elastic-Net Cox (alpha={best_alpha:.4f})", "train_cindex": train_c,
         "cv_mean": best_cv_score, "cv_std": None, "external_gbsg2_cindex": test_c}
    )

    # 4. Random Survival Forest
    print("Fitting Random Survival Forest...")
    rsf = RandomSurvivalForest(
        n_estimators=300, min_samples_split=10, min_samples_leaf=15,
        n_jobs=-1, random_state=RANDOM_STATE,
    )
    rsf.fit(X_train, y_train)
    train_c = concordance_index_censored(
        y_train["event"], y_train["time"], rsf.predict(X_train)
    )[0]
    cv_mean, cv_std = cv_concordance(
        lambda: RandomSurvivalForest(
            n_estimators=300, min_samples_split=10, min_samples_leaf=15,
            n_jobs=-1, random_state=RANDOM_STATE,
        ),
        X_train, y_train,
    )
    test_c = concordance_index_censored(
        y_test["event"], y_test["time"], rsf.predict(X_test)
    )[0]
    results.append(
        {"model": "Random Survival Forest", "train_cindex": train_c, "cv_mean": cv_mean,
         "cv_std": cv_std, "external_gbsg2_cindex": test_c}
    )

    # 5. Gradient Boosting Survival Analysis
    print("Fitting Gradient Boosting Survival Analysis...")
    gbs = GradientBoostingSurvivalAnalysis(
        n_estimators=200, learning_rate=0.05, max_depth=3,
        random_state=RANDOM_STATE,
    )
    gbs.fit(X_train, y_train)
    train_c = concordance_index_censored(
        y_train["event"], y_train["time"], gbs.predict(X_train)
    )[0]
    cv_mean, cv_std = cv_concordance(
        lambda: GradientBoostingSurvivalAnalysis(
            n_estimators=200, learning_rate=0.05, max_depth=3,
            random_state=RANDOM_STATE,
        ),
        X_train, y_train,
    )
    test_c = concordance_index_censored(
        y_test["event"], y_test["time"], gbs.predict(X_test)
    )[0]
    results.append(
        {"model": "Gradient Boosting Survival", "train_cindex": train_c, "cv_mean": cv_mean,
         "cv_std": cv_std, "external_gbsg2_cindex": test_c}
    )

    df_results = pd.DataFrame(results)
    print("\n" + "=" * 90)
    print(df_results.to_string(index=False))
    print("=" * 90)

    out_path = RESULTS_DIR / "experiment_0001_baselines.csv"
    df_results.to_csv(out_path, index=False)
    print(f"\nSaved results to {out_path}")

    return df_results


if __name__ == "__main__":
    main()
