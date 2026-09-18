"""
Generates a per-patient prediction file for the GBSG2 external test set -
one row per patient, showing their real features, real outcome, and the
risk score each of the 4 models assigned them. This did not exist before
(only the aggregate summary CSV did) - built on request to make the
model's actual output visible at the individual-patient level.

Run: python scripts/generate_predictions_csv.py
"""

import sys
from pathlib import Path

import pandas as pd
from sksurv.ensemble import GradientBoostingSurvivalAnalysis, RandomSurvivalForest
from sksurv.linear_model import CoxnetSurvivalAnalysis, CoxPHSurvivalAnalysis

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.train_baselines import RANDOM_STATE, build_preprocessor, select_coxnet_alpha  # noqa: E402
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


def main():
    rot = harmonize_rotterdam(load_rotterdam_rfs())
    gbsg = harmonize_gbsg2(load_gbsg2())

    preprocessor = build_preprocessor()
    X_train = preprocessor.fit_transform(rot[COMMON_NUMERIC + COMMON_CATEGORICAL])
    X_test = preprocessor.transform(gbsg[COMMON_NUMERIC + COMMON_CATEGORICAL])
    y_train = to_structured_y(rot)

    # Fit all 4 models on Rotterdam (identical to train_baselines.py)
    cox = CoxPHSurvivalAnalysis().fit(X_train, y_train)
    best_alpha, _ = select_coxnet_alpha(X_train, y_train, l1_ratio=0.5)
    coxnet = CoxnetSurvivalAnalysis(l1_ratio=0.5, alphas=[best_alpha]).fit(X_train, y_train)
    rsf = RandomSurvivalForest(
        n_estimators=300, min_samples_split=10, min_samples_leaf=15,
        n_jobs=-1, random_state=RANDOM_STATE,
    ).fit(X_train, y_train)
    gbs = GradientBoostingSurvivalAnalysis(
        n_estimators=200, learning_rate=0.05, max_depth=3, random_state=RANDOM_STATE,
    ).fit(X_train, y_train)

    # Build the output table: original features + actual outcome + each
    # model's predicted risk score, one row per GBSG2 patient
    out = gbsg[COMMON_NUMERIC + COMMON_CATEGORICAL].copy()
    out["actual_rfstime_months"] = gbsg["rfstime_months"].round(2)
    out["actual_event"] = gbsg["rfs_event"].astype(int)
    out["predicted_risk_CoxPH"] = cox.predict(X_test).round(4)
    out["predicted_risk_ElasticNetCox"] = coxnet.predict(X_test).round(4)
    out["predicted_risk_RandomSurvivalForest"] = rsf.predict(X_test).round(4)
    out["predicted_risk_GradientBoosting"] = gbs.predict(X_test).round(4)

    out_path = RESULTS_DIR / "gbsg2_per_patient_predictions.csv"
    out.to_csv(out_path, index=True, index_label="patient_row")
    print(f"Saved {len(out)} patient predictions to {out_path}")
    print("\nFirst 5 rows:")
    print(out.head().to_string())


if __name__ == "__main__":
    main()
