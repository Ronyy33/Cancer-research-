"""
Stage 14 - Robustness / fairness subgroup analysis.

Per project brief Section 23: evaluate performance, calibration, and
error differences across subgroups WHERE DATA PERMITS - explicitly do
NOT manufacture subgroup analyses when sample sizes are inadequate.

Model: Cox PH fit on the FULL Rotterdam training cohort (N=2,982, not
the 75/25 explainability split), evaluated on GBSG2 (the genuine
external test set, N=686) - consistent with experiment_0001's primary
model.

Subgroups tested (clinically motivated, not arbitrary): age band,
menopausal status, tumor grade (including the grade-1 patients flagged
as out-of-distribution for this model in experiment_0001/harmonize.py),
hormone therapy status, nodal burden. A subgroup is only reported if it
has >= MIN_N patients AND >= MIN_EVENTS events; otherwise it is listed
as "insufficient sample" rather than silently reported with an unstable
estimate.

HONEST LIMITATION, stated directly: Rotterdam and GBSG2 are both
European cohorts (Netherlands / Germany) with no race, ethnicity, or
socioeconomic variables available. This means the demographic/equity
gap documented in research/RESEARCH_GAPS.md (Gap 4 - existing models
predominantly trained/validated on Caucasian/Asian populations) CANNOT
be assessed or addressed with this dataset. This is reported as a real,
unaddressed limitation, not silently skipped.

Run: python scripts/subgroup_analysis.py
"""

import sys
from pathlib import Path

import pandas as pd
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.metrics import concordance_index_censored

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.train_baselines import build_preprocessor  # noqa: E402
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

MIN_N = 30
MIN_EVENTS = 10


def define_subgroups(gbsg_raw: pd.DataFrame, gbsg_harm: pd.DataFrame) -> dict:
    subgroups = {}

    age = gbsg_harm["age"]
    subgroups["age <50"] = age < 50
    subgroups["age 50-64"] = (age >= 50) & (age < 65)
    subgroups["age 65+"] = age >= 65

    subgroups["menopause: pre"] = gbsg_harm["menopause_post"] == 0
    subgroups["menopause: post"] = gbsg_harm["menopause_post"] == 1

    subgroups["grade 1 (out-of-distribution - see limitation)"] = gbsg_harm["grade_cat"] == "1"
    subgroups["grade 2"] = gbsg_harm["grade_cat"] == "2"
    subgroups["grade 3"] = gbsg_harm["grade_cat"] == "3"

    subgroups["hormone therapy: no"] = gbsg_harm["hormone_therapy"] == 0
    subgroups["hormone therapy: yes"] = gbsg_harm["hormone_therapy"] == 1

    nodes = gbsg_harm["nodes_positive"]
    subgroups["nodes 1-3"] = (nodes >= 1) & (nodes <= 3)
    subgroups["nodes 4+"] = nodes >= 4

    return subgroups


def main():
    print("Fitting Cox PH on FULL Rotterdam (N=2,982) - primary model from experiment_0001")
    rot = harmonize_rotterdam(load_rotterdam_rfs())
    gbsg = harmonize_gbsg2(load_gbsg2())

    preprocessor = build_preprocessor()
    X_train = preprocessor.fit_transform(rot[COMMON_NUMERIC + COMMON_CATEGORICAL])
    X_test = preprocessor.transform(gbsg[COMMON_NUMERIC + COMMON_CATEGORICAL])
    y_train = to_structured_y(rot)
    y_test = to_structured_y(gbsg)

    cox = CoxPHSurvivalAnalysis()
    cox.fit(X_train, y_train)
    risk_scores = cox.predict(X_test)  # higher = higher predicted risk

    overall_c = concordance_index_censored(y_test["event"], y_test["time"], risk_scores)[0]
    print(f"Overall external C-index (all GBSG2, N={len(gbsg)}): {overall_c:.3f}")

    subgroups = define_subgroups(load_gbsg2(), gbsg)

    rows = []
    for name, mask in subgroups.items():
        n = int(mask.sum())
        n_events = int(y_test["event"][mask.values].sum())
        if n < MIN_N or n_events < MIN_EVENTS:
            rows.append(
                {"subgroup": name, "n": n, "n_events": n_events,
                 "cindex": None, "mean_predicted_risk": None,
                 "observed_event_rate": None,
                 "status": f"INSUFFICIENT SAMPLE (need n>={MIN_N}, events>={MIN_EVENTS})"}
            )
            continue

        y_sub = y_test[mask.values]
        risk_sub = risk_scores[mask.values]
        c_index = concordance_index_censored(y_sub["event"], y_sub["time"], risk_sub)[0]
        rows.append(
            {
                "subgroup": name,
                "n": n,
                "n_events": n_events,
                "cindex": round(c_index, 3),
                "mean_predicted_risk": round(float(risk_sub.mean()), 3),
                "observed_event_rate": round(float(y_sub["event"].mean()), 3),
                "status": "OK",
            }
        )

    df = pd.DataFrame(rows)
    print("\n" + "=" * 100)
    print(df.to_string(index=False))
    print("=" * 100)

    out_path = RESULTS_DIR / "experiment_0004_subgroup_analysis.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved to {out_path}")

    print(
        "\nHONEST LIMITATION: Rotterdam and GBSG2 are both European cohorts with no "
        "race/ethnicity/socioeconomic data. The demographic equity gap documented in "
        "RESEARCH_GAPS.md Gap 4 cannot be assessed with this dataset - stated directly, "
        "not silently skipped."
    )


if __name__ == "__main__":
    main()
