


from pathlib import Path

import pandas as pd

DATA_RAW = Path(__file__).resolve().parents[2] / "data" / "raw"
DATA_PROCESSED = Path(__file__).resolve().parents[2] / "data" / "processed"


def load_rotterdam_raw() -> pd.DataFrame:

    path = DATA_RAW / "rotterdam_raw.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run: Rscript scripts/pull_rotterdam.R"
        )
    return pd.read_csv(path)


def load_rotterdam_rfs() -> pd.DataFrame:

    df = load_rotterdam_raw()
    df = df.copy()
    df["rfstime"] = df[["rtime", "dtime"]].min(axis=1)
    df["rfs_event"] = ((df["recur"] == 1) | (df["death"] == 1)).astype(int)
    return df


def load_gbsg2() -> pd.DataFrame:

    from sksurv.datasets import load_gbsg2

    X, y = load_gbsg2()
    df = X.copy()
    df["rfstime"] = y["time"]
    df["rfs_event"] = y["cens"].astype(int)
    return df


def load_metabric() -> pd.DataFrame:

    path = DATA_RAW / "metabric_clinical_patient.txt"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run: bash scripts/pull_metabric_tcga.sh"
        )
    df = pd.read_csv(path, sep="\t", comment="#")
    df["rfstime"] = df["RFS_MONTHS"]
    df["rfs_event"] = df["RFS_STATUS"].str.startswith("1").astype("Int64")
    return df


def load_tcga_brca() -> pd.DataFrame:
 
    path = DATA_RAW / "tcga_brca_clinical_patient.txt"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run: bash scripts/pull_metabric_tcga.sh"
        )
    df = pd.read_csv(path, sep="\t", comment="#")
    df["rfstime"] = df["DFS_MONTHS"]
    df["rfs_event"] = df["DFS_STATUS"].str.startswith("1").astype("Int64")
    return df


if __name__ == "__main__":
    rotterdam = load_rotterdam_rfs()
    gbsg2 = load_gbsg2()

    print("Rotterdam (recurrence-free survival):")
    print(f"  N = {len(rotterdam)}")
    print(
        f"  Events = {rotterdam['rfs_event'].sum()} "
        f"({rotterdam['rfs_event'].mean() * 100:.1f}%)"
    )
    print()
    print("GBSG2 (recurrence-free survival):")
    print(f"  N = {len(gbsg2)}")
    print(
        f"  Events = {gbsg2['rfs_event'].sum()} "
        f"({gbsg2['rfs_event'].mean() * 100:.1f}%)"
    )

    metabric = load_metabric()
    print()
    print("METABRIC (relapse-free survival):")
    print(f"  N = {len(metabric)}")
    valid = metabric["rfs_event"].notna()
    print(
        f"  Events = {int(metabric.loc[valid, 'rfs_event'].sum())} "
        f"/ {valid.sum()} valid ({metabric.loc[valid, 'rfs_event'].mean() * 100:.1f}%)"
    )

    tcga = load_tcga_brca()
    print()
    print("TCGA-BRCA (disease-free survival):")
    print(f"  N = {len(tcga)}")
    valid = tcga["rfs_event"].notna()
    print(
        f"  Events = {int(tcga.loc[valid, 'rfs_event'].sum())} "
        f"/ {valid.sum()} valid ({tcga.loc[valid, 'rfs_event'].mean() * 100:.1f}%)"
    )
