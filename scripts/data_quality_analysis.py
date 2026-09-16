"""
Stage 8 - Data Quality Analysis.

Runs missingness, duplicate, numeric/categorical distribution, and
implausible-value checks on all four real cohorts (Rotterdam, GBSG2,
METABRIC, TCGA-BRCA), and plots a Kaplan-Meier recurrence-free-survival
curve per cohort. Writes:
  - research/RESULTS/data_quality/<dataset>.md   (text report)
  - research/FIGURES/data_quality/<dataset>_km.png
  - research/FIGURES/data_quality/<dataset>_missingness.png
  - research/FIGURES/data_quality/cross_cohort_km_overlay.png

Run: python scripts/data_quality_analysis.py
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from lifelines import KaplanMeierFitter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.loaders import (  # noqa: E402
    load_gbsg2,
    load_metabric,
    load_rotterdam_rfs,
    load_tcga_brca,
)
from src.data.quality import (  # noqa: E402
    categorical_summary,
    duplicate_report,
    implausible_value_checks,
    missingness_report,
    numeric_summary,
)

RESULTS_DIR = ROOT / "research" / "RESULTS" / "data_quality"
FIGURES_DIR = ROOT / "research" / "FIGURES" / "data_quality"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = {
    "rotterdam": {
        "loader": load_rotterdam_rfs,
        "id_col": "pid",
        "numeric_cols": ["age", "nodes", "pgr", "er", "year"],
        "categorical_cols": ["meno", "size", "grade", "hormon", "chemo"],
        "implausible_checks": {
            "age": "age < 0 or age > 110",
            "nodes": "nodes < 0",
            "pgr": "pgr < 0",
            "er": "er < 0",
            "rfstime": "rfstime < 0",
        },
    },
    "gbsg2": {
        "loader": load_gbsg2,
        "id_col": None,
        "numeric_cols": ["age", "estrec", "pnodes", "progrec", "tsize"],
        "categorical_cols": ["horTh", "menostat", "tgrade"],
        "implausible_checks": {
            "age": "age < 0 or age > 110",
            "pnodes": "pnodes < 0",
            "estrec": "estrec < 0",
            "progrec": "progrec < 0",
            "tsize": "tsize < 0",
            "rfstime": "rfstime < 0",
        },
    },
    "metabric": {
        "loader": load_metabric,
        "id_col": "PATIENT_ID",
        "numeric_cols": [
            "LYMPH_NODES_EXAMINED_POSITIVE",
            "NPI",
            "AGE_AT_DIAGNOSIS",
            "OS_MONTHS",
            "RFS_MONTHS",
        ],
        "categorical_cols": [
            "CELLULARITY",
            "CHEMOTHERAPY",
            "ER_IHC",
            "HER2_SNP6",
            "HORMONE_THERAPY",
            "INFERRED_MENOPAUSAL_STATE",
            "CLAUDIN_SUBTYPE",
            "RADIO_THERAPY",
            "HISTOLOGICAL_SUBTYPE",
            "BREAST_SURGERY",
        ],
        "implausible_checks": {
            "AGE_AT_DIAGNOSIS": "AGE_AT_DIAGNOSIS < 0 or AGE_AT_DIAGNOSIS > 110",
            "LYMPH_NODES_EXAMINED_POSITIVE": "LYMPH_NODES_EXAMINED_POSITIVE < 0",
            "RFS_MONTHS": "RFS_MONTHS < 0",
        },
    },
    "tcga_brca": {
        "loader": load_tcga_brca,
        "id_col": "PATIENT_ID",
        "numeric_cols": ["AGE", "OS_MONTHS", "DFS_MONTHS", "PFS_MONTHS"],
        "categorical_cols": [
            "SEX",
            "AJCC_PATHOLOGIC_TUMOR_STAGE",
            "PATH_M_STAGE",
            "PATH_N_STAGE",
            "PATH_T_STAGE",
            "RACE",
            "RADIATION_THERAPY",
            "SUBTYPE",
        ],
        "implausible_checks": {
            "AGE": "AGE < 0 or AGE > 110",
            "DFS_MONTHS": "DFS_MONTHS < 0",
        },
    },
}


def write_report(name: str, df: pd.DataFrame, cfg: dict) -> None:
    lines = [f"# Data Quality Report — {name}", ""]
    lines.append(f"**N rows (raw pull):** {len(df)}")
    lines.append("")

    lines.append("## Duplicates")
    dup = duplicate_report(df, cfg["id_col"])
    for k, v in dup.items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("## Missingness (top 15 worst columns)")
    miss = missingness_report(df)
    lines.append("")
    lines.append("| column | n_missing | pct_missing |")
    lines.append("|---|---|---|")
    for col, row in miss.head(15).iterrows():
        lines.append(f"| {col} | {int(row['n_missing'])} | {row['pct_missing']}% |")
    lines.append("")

    lines.append("## Numeric feature summary (+ IQR outlier flags)")
    num_summary = numeric_summary(df, cfg["numeric_cols"])
    lines.append("")
    lines.append("| column | count | mean | std | min | 25% | 50% | 75% | max | extreme_outliers(>3xIQR) |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for col, row in num_summary.iterrows():
        lines.append(
            f"| {col} | {row['count']:.0f} | {row['mean']:.2f} | {row['std']:.2f} | "
            f"{row['min']:.2f} | {row['25%']:.2f} | {row['50%']:.2f} | {row['75%']:.2f} | "
            f"{row['max']:.2f} | {int(row['n_extreme_outliers_3xIQR'])} |"
        )
    lines.append("")

    lines.append("## Categorical feature value counts")
    cat_summary = categorical_summary(df, cfg["categorical_cols"])
    for col, vc in cat_summary.items():
        lines.append(f"\n**{col}** (cardinality={vc.shape[0]}):")
        for val, count in vc.items():
            lines.append(f"- {val}: {count}")
    lines.append("")

    lines.append("## Implausible-value checks")
    implausible = implausible_value_checks(df, cfg["implausible_checks"])
    for col, n_bad in implausible.items():
        flag = "⚠️ " if isinstance(n_bad, int) and n_bad > 0 else ""
        lines.append(f"- {flag}{col}: {n_bad} implausible rows")
    lines.append("")

    out_path = RESULTS_DIR / f"{name}.md"
    out_path.write_text("\n".join(lines))
    print(f"Wrote {out_path}")


def plot_km(name: str, df: pd.DataFrame) -> KaplanMeierFitter:
    kmf = KaplanMeierFitter()
    valid = df["rfstime"].notna() & df["rfs_event"].notna()
    kmf.fit(df.loc[valid, "rfstime"], df.loc[valid, "rfs_event"], label=name)

    fig, ax = plt.subplots(figsize=(6, 4))
    kmf.plot_survival_function(ax=ax)
    ax.set_title(f"{name}: recurrence-free survival (N={valid.sum()})")
    ax.set_xlabel("Time (dataset-native units - months or days, see report)")
    ax.set_ylabel("Recurrence-free survival probability")
    fig.tight_layout()
    out_path = FIGURES_DIR / f"{name}_km.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    print(f"Wrote {out_path}")
    return kmf


def plot_missingness(name: str, df: pd.DataFrame) -> None:
    miss = missingness_report(df)
    miss = miss[miss["pct_missing"] > 0].head(20)
    if miss.empty:
        print(f"{name}: no missing values to plot")
        return
    fig, ax = plt.subplots(figsize=(7, max(3, 0.3 * len(miss))))
    ax.barh(miss.index[::-1], miss["pct_missing"][::-1])
    ax.set_xlabel("% missing")
    ax.set_title(f"{name}: missingness by column")
    fig.tight_layout()
    out_path = FIGURES_DIR / f"{name}_missingness.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    print(f"Wrote {out_path}")


def main():
    kmfs = {}
    for name, cfg in DATASETS.items():
        print(f"\n{'=' * 60}\n{name}\n{'=' * 60}")
        df = cfg["loader"]()
        write_report(name, df, cfg)
        plot_missingness(name, df)
        kmfs[name] = plot_km(name, df)

    # Cross-cohort overlay - note: Rotterdam/GBSG2 rfstime is in DAYS,
    # METABRIC/TCGA-BRCA RFS/DFS_MONTHS is in MONTHS. This is a real
    # cross-cohort unit mismatch that must be harmonized before any
    # cross-cohort modeling - flagged explicitly rather than plotted
    # misleadingly on a shared raw time axis.
    fig, ax = plt.subplots(figsize=(7, 5))
    for name, kmf in kmfs.items():
        kmf.plot_survival_function(ax=ax)
    ax.set_title(
        "Cross-cohort KM overlay (⚠️ time units differ - see report, "
        "NOT yet harmonized)"
    )
    ax.set_xlabel("Time (native units per cohort - NOT harmonized)")
    ax.set_ylabel("Recurrence-free survival probability")
    fig.tight_layout()
    out_path = FIGURES_DIR / "cross_cohort_km_overlay.png"
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
