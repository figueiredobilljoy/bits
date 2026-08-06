import pandas as pd

from pipeline_config import (
    END_YEAR,
    HORTICULTURE_CROPS,
    PROCESSED_DIR,
    PRODUCTION_FILE,
    SELECTED_STATES,
    START_YEAR,
)
from pipeline_utils import normalize_key, standardize_crop, standardize_state


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(PRODUCTION_FILE, sheet_name="crop_yield")
    df.columns = [str(col).strip() for col in df.columns]

    df = df.rename(
        columns={
            "Crop_Year": "Year",
            "Annual_Rainfall": "Annual_Rainfall",
        }
    )

    df["State"] = df["State"].map(standardize_state)
    df["Crop"] = df["Crop"].map(standardize_crop)
    df["crop_key"] = df["Crop"].map(normalize_key)

    numeric_cols = ["Year", "Area", "Production", "Annual_Rainfall", "Fertilizer", "Pesticide", "Yield"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df[
        df["State"].isin(SELECTED_STATES)
        & df["Crop"].isin(HORTICULTURE_CROPS)
        & df["Year"].between(START_YEAR, END_YEAR)
        & df["crop_key"].notna()
    ].copy()

    df["Year"] = df["Year"].astype(int)

    cols = [
        "State",
        "Crop",
        "crop_key",
        "Year",
        "Season",
        "Area",
        "Production",
        "Annual_Rainfall",
        "Fertilizer",
        "Pesticide",
        "Yield",
    ]
    df = df[cols].sort_values(["State", "Crop", "Year"])

    out = PROCESSED_DIR / "clean_production_2001_2020.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {out} with {len(df):,} rows")
    print(f"States: {df['State'].nunique():,}; crops: {df['Crop'].nunique():,}; years: {df['Year'].min()}-{df['Year'].max()}")


if __name__ == "__main__":
    main()
