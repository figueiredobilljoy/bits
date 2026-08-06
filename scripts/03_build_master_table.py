import pandas as pd

from pipeline_config import PROCESSED_DIR


def add_lag_features(df):
    df = df.sort_values(["State", "Crop", "Year"]).copy()
    groups = df.groupby(["State", "Crop"], dropna=False)

    for col in ["Production", "Yield", "Area", "avg_modal_price"]:
        df[f"{col}_lag_1"] = groups[col].shift(1)

    df["avg_modal_price_roll_3"] = groups["avg_modal_price"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean()
    )
    df["Production_roll_3"] = groups["Production"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean()
    )
    return df


def main():
    production = pd.read_csv(PROCESSED_DIR / "clean_production_2001_2020.csv")
    prices = pd.read_csv(PROCESSED_DIR / "annual_prices_2001_2020.csv")

    master = production.merge(
        prices,
        on=["State", "crop_key", "Year"],
        how="left",
        validate="many_to_one",
    )

    master["price_available"] = master["avg_modal_price"].notna().astype(int)
    master = add_lag_features(master)

    ordered_cols = [
        "State",
        "Crop",
        "Commodity",
        "crop_key",
        "Year",
        "Season",
        "Area",
        "Production",
        "Yield",
        "Annual_Rainfall",
        "Fertilizer",
        "Pesticide",
        "avg_modal_price",
        "median_modal_price",
        "min_price",
        "max_price",
        "modal_price_std",
        "price_spread",
        "price_record_count",
        "market_count",
        "district_count",
        "price_available",
        "Production_lag_1",
        "Yield_lag_1",
        "Area_lag_1",
        "avg_modal_price_lag_1",
        "avg_modal_price_roll_3",
        "Production_roll_3",
    ]
    master = master[ordered_cols].sort_values(["State", "Crop", "Year"])

    out = PROCESSED_DIR / "master_table_2001_2020.csv"
    master.to_csv(out, index=False)
    print(f"Wrote {out} with {len(master):,} rows")
    print(f"Rows with price match: {master['price_available'].sum():,} ({master['price_available'].mean():.1%})")
    print(f"States: {master['State'].nunique():,}; crops: {master['Crop'].nunique():,}; years: {master['Year'].min()}-{master['Year'].max()}")


if __name__ == "__main__":
    main()

