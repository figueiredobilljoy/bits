import pandas as pd

from pipeline_config import PROCESSED_DIR


def missing_summary(df):
    rows = len(df)
    summary = (
        df.isna()
        .sum()
        .rename("missing_count")
        .reset_index()
        .rename(columns={"index": "column"})
    )
    summary["missing_pct"] = (summary["missing_count"] / rows * 100).round(2)
    return summary.sort_values(["missing_count", "column"], ascending=[False, True])


def grouped_missing(df, group_col):
    numeric_price_cols = [
        "avg_modal_price",
        "median_modal_price",
        "min_price",
        "max_price",
        "modal_price_std",
        "price_spread",
    ]
    grouped = (
        df.groupby(group_col)
        .agg(
            rows=("State", "size"),
            price_matched_rows=("price_available", "sum"),
            price_match_pct=("price_available", "mean"),
            avg_modal_price_missing=("avg_modal_price", lambda s: s.isna().sum()),
        )
        .reset_index()
    )
    grouped["price_match_pct"] = (grouped["price_match_pct"] * 100).round(2)

    for col in numeric_price_cols:
        grouped[f"{col}_missing_pct"] = (
            df.groupby(group_col)[col].apply(lambda s: s.isna().mean() * 100).round(2).values
        )

    return grouped.sort_values(["price_match_pct", "rows"], ascending=[True, False])


def main():
    master_path = PROCESSED_DIR / "master_table_2001_2020.csv"
    df = pd.read_csv(master_path)

    overall = missing_summary(df)
    crop = grouped_missing(df, "Crop")
    state = grouped_missing(df, "State")

    overall_path = PROCESSED_DIR / "missing_summary.csv"
    crop_path = PROCESSED_DIR / "missing_by_crop.csv"
    state_path = PROCESSED_DIR / "missing_by_state.csv"

    overall.to_csv(overall_path, index=False)
    crop.to_csv(crop_path, index=False)
    state.to_csv(state_path, index=False)

    print(f"Wrote {overall_path}")
    print(f"Wrote {crop_path}")
    print(f"Wrote {state_path}")
    print("\nHighest missing columns:")
    print(overall.head(12).to_string(index=False))
    print("\nLowest price-match crops:")
    print(crop[["Crop", "rows", "price_matched_rows", "price_match_pct"]].head(12).to_string(index=False))
    print("\nLowest price-match states:")
    print(state[["State", "rows", "price_matched_rows", "price_match_pct"]].head(12).to_string(index=False))


if __name__ == "__main__":
    main()

