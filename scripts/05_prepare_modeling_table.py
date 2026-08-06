import pandas as pd

from pipeline_config import PROCESSED_DIR


PRICE_FEATURES = [
    "avg_modal_price",
    "median_modal_price",
    "min_price",
    "max_price",
    "modal_price_std",
    "price_spread",
]

COUNT_FEATURES = [
    "price_record_count",
    "market_count",
    "district_count",
]

LAG_FEATURES = [
    "Production_lag_1",
    "Yield_lag_1",
    "Area_lag_1",
    "avg_modal_price_lag_1",
    "avg_modal_price_roll_3",
    "Production_roll_3",
]


def fill_by_groups(df, source_col):
    filled = df[source_col].copy()
    for groups in [["State", "Crop"], ["Crop"], ["State"]]:
        group_values = df.groupby(groups)[source_col].transform("median")
        filled = filled.fillna(group_values)
    return filled.fillna(df[source_col].median())


def main():
    master_path = PROCESSED_DIR / "master_table_2001_2020.csv"
    df = pd.read_csv(master_path)

    df["target_available"] = df["avg_modal_price"].notna().astype(int)
    df["Commodity"] = df["Commodity"].fillna(df["Crop"])

    for col in PRICE_FEATURES + LAG_FEATURES:
        df[f"{col}_was_missing"] = df[col].isna().astype(int)
        df[f"{col}_filled"] = fill_by_groups(df, col)

    for col in COUNT_FEATURES:
        df[f"{col}_was_missing"] = df[col].isna().astype(int)
        df[f"{col}_filled"] = df[col].fillna(0)

    modeling_path = PROCESSED_DIR / "modeling_table_2001_2020.csv"
    df.to_csv(modeling_path, index=False)

    train_df = df[df["target_available"].eq(1)].copy()
    train_path = PROCESSED_DIR / "price_modeling_train_2001_2020.csv"
    train_df.to_csv(train_path, index=False)

    print(f"Wrote {modeling_path} with {len(df):,} rows and {len(df.columns):,} columns")
    print(f"Wrote {train_path} with {len(train_df):,} rows and {len(train_df.columns):,} columns")
    print(f"Training rows kept because target price is available: {len(train_df):,} ({len(train_df) / len(df):.1%})")
    print("\nFilled feature missing counts after preparation:")
    filled_cols = [f"{col}_filled" for col in PRICE_FEATURES + COUNT_FEATURES + LAG_FEATURES]
    print(df[filled_cols].isna().sum().sort_values(ascending=False).to_string())


if __name__ == "__main__":
    main()

