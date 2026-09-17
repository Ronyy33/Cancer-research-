"""
Stage 13 - Explainability.

Per project brief Section 24: use appropriate methods (SHAP, permutation
importance, feature importance), clearly distinguish predictive
association from causality, and never claim "X causes recurrence" just
because X has high importance.

Two complementary views on the PRIMARY model (Cox PH, per
research/PROPOSED_METHODOLOGY.md), trained on Rotterdam:

1. Cox PH's NATIVE interpretability - hazard ratios (exp(coefficient)).
   This is a genuine advantage of choosing Cox PH as the primary model:
   unlike a black-box ensemble needing a post-hoc explainer, every
   coefficient has a direct, standard clinical interpretation (a hazard
   ratio > 1 means higher instantaneous recurrence/death risk per unit
   increase in that feature, holding other features fixed - an
   ASSOCIATION within this model, not a causal claim).

2. Permutation importance (model-agnostic, works identically for Cox PH
   and Random Survival Forest, so the two can be compared on the same
   footing) - shuffles one feature at a time and measures the drop in
   concordance index, computed on Rotterdam's held-out CV folds so
   importance isn't measured on the same data the model was fit on.

Run: python scripts/explainability.py
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sksurv.ensemble import RandomSurvivalForest
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.metrics import concordance_index_censored

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.train_baselines import build_preprocessor, RANDOM_STATE  # noqa: E402
from src.data.harmonize import (  # noqa: E402
    COMMON_CATEGORICAL,
    COMMON_NUMERIC,
    harmonize_rotterdam,
    to_structured_y,
)
from src.data.loaders import load_rotterdam_rfs  # noqa: E402

RESULTS_DIR = ROOT / "research" / "RESULTS" / "experiments"
FIGURES_DIR = ROOT / "research" / "FIGURES"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


class ConcordanceScorer:
    """Wraps a fitted sksurv model so sklearn's permutation_importance
    (which expects a .score(X, y) -> higher-is-better float) can call it."""

    def __call__(self, estimator, X, y):
        pred = estimator.predict(X)
        return concordance_index_censored(y["event"], y["time"], pred)[0]


def get_feature_names(preprocessor) -> list[str]:
    num_names = COMMON_NUMERIC
    cat_names = list(
        preprocessor.named_transformers_["cat"].get_feature_names_out(COMMON_CATEGORICAL)
    )
    return num_names + cat_names


def main():
    rot = harmonize_rotterdam(load_rotterdam_rfs())
    preprocessor = build_preprocessor()

    # Held-out split so importance isn't measured on training data
    train_df, holdout_df = train_test_split(rot, test_size=0.25, random_state=RANDOM_STATE)
    X_train = preprocessor.fit_transform(train_df[COMMON_NUMERIC + COMMON_CATEGORICAL])
    X_holdout = preprocessor.transform(holdout_df[COMMON_NUMERIC + COMMON_CATEGORICAL])
    y_train = to_structured_y(train_df)
    y_holdout = to_structured_y(holdout_df)
    feature_names = get_feature_names(preprocessor)

    # --- 1. Cox PH native hazard ratios ---
    print("=" * 70)
    print("Cox PH hazard ratios (fit on training split)")
    print("=" * 70)
    cox = CoxPHSurvivalAnalysis()
    cox.fit(X_train, y_train)
    hr = np.exp(cox.coef_)
    hr_table = pd.DataFrame(
        {"feature": feature_names, "coef": cox.coef_, "hazard_ratio": hr}
    ).sort_values("hazard_ratio", ascending=False)
    print(hr_table.to_string(index=False))
    hr_table.to_csv(RESULTS_DIR / "experiment_0003_cox_hazard_ratios.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#c0392b" if h > 1 else "#2980b9" for h in hr_table["hazard_ratio"]]
    ax.barh(hr_table["feature"][::-1], hr_table["hazard_ratio"][::-1], color=colors[::-1])
    ax.axvline(1.0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Hazard ratio (>1 = higher recurrence/death risk; <1 = protective)")
    ax.set_title("Cox PH hazard ratios (Rotterdam training split)\nAssociation within this model, NOT a causal claim")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "cox_hazard_ratios.png", dpi=120)
    plt.close(fig)
    print(f"\nSaved plot to {FIGURES_DIR / 'cox_hazard_ratios.png'}")

    # --- 2. Permutation importance: Cox PH vs Random Survival Forest ---
    print("\n" + "=" * 70)
    print("Permutation importance on held-out split (25% of Rotterdam)")
    print("=" * 70)

    rsf = RandomSurvivalForest(
        n_estimators=300, min_samples_split=10, min_samples_leaf=15,
        n_jobs=-1, random_state=RANDOM_STATE,
    )
    rsf.fit(X_train, y_train)

    scorer = ConcordanceScorer()
    results_rows = []
    for name, model in [("Cox PH", cox), ("Random Survival Forest", rsf)]:
        pi = permutation_importance(
            model, X_holdout, y_holdout, scoring=scorer,
            n_repeats=20, random_state=RANDOM_STATE,
        )
        for i, feat in enumerate(feature_names):
            results_rows.append(
                {
                    "model": name,
                    "feature": feat,
                    "importance_mean_cindex_drop": pi.importances_mean[i],
                    "importance_std": pi.importances_std[i],
                }
            )

    pi_df = pd.DataFrame(results_rows)
    print(
        pi_df.sort_values(["model", "importance_mean_cindex_drop"], ascending=[True, False])
        .to_string(index=False)
    )
    pi_df.to_csv(RESULTS_DIR / "experiment_0003_permutation_importance.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for ax, name in zip(axes, ["Cox PH", "Random Survival Forest"]):
        sub = pi_df[pi_df["model"] == name].sort_values("importance_mean_cindex_drop")
        ax.barh(sub["feature"], sub["importance_mean_cindex_drop"],
                xerr=sub["importance_std"], color="#5d6d7e")
        ax.set_title(name)
        ax.set_xlabel("Mean C-index drop when shuffled")
        ax.axvline(0, color="black", linewidth=0.8)
    fig.suptitle("Permutation importance, held-out Rotterdam split (higher = more important)")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "permutation_importance.png", dpi=120)
    plt.close(fig)
    print(f"\nSaved plot to {FIGURES_DIR / 'permutation_importance.png'}")


if __name__ == "__main__":
    main()
