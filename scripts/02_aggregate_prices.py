from collections import defaultdict

import pandas as pd

from pipeline_config import END_YEAR, PRICE_DIR, PROCESSED_DIR, SELECTED_STATES, START_YEAR
from pipeline_utils import normalize_key, standardize_crop, standardize_state


CHUNKSIZE = 500_000
PRICE_COLUMNS = [
    "State",
    "District",
    "Market",
    "Commodity",
    "Arrival_Date",
    "Min_Price",
    "Max_Price",
    "Modal_Price",
]


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    production = pd.read_csv(PROCESSED_DIR / "clean_production_2001_2020.csv", usecols=["crop_key"])
    production_crop_keys = set(production["crop_key"].dropna().unique())

    numeric_parts = []
    markets = defaultdict(set)
    districts = defaultdict(set)

    for year in range(START_YEAR, END_YEAR + 1):
        path = PRICE_DIR / f"{year}.csv"
        if not path.exists():
            print(f"Skipping missing file: {path}")
            continue

        print(f"Reading {path.name}")
        for chunk in pd.read_csv(path, usecols=PRICE_COLUMNS, chunksize=CHUNKSIZE):
            chunk["State"] = chunk["State"].map(standardize_state)
            chunk = chunk[chunk["State"].isin(SELECTED_STATES)].copy()
            if chunk.empty:
                continue

            chunk["Year"] = pd.to_datetime(chunk["Arrival_Date"], errors="coerce").dt.year
            chunk = chunk[chunk["Year"].eq(year)]
            if chunk.empty:
                continue

            chunk["Commodity"] = chunk["Commodity"].map(standardize_crop)
            chunk["crop_key"] = chunk["Commodity"].map(normalize_key)
            chunk = chunk[chunk["crop_key"].isin(production_crop_keys)].copy()
            if chunk.empty:
                continue

            for col in ["Min_Price", "Max_Price", "Modal_Price"]:
                chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

            chunk = chunk[chunk["Modal_Price"].gt(0)]
            if chunk.empty:
                continue

            chunk["modal_price_sq"] = chunk["Modal_Price"] ** 2
            keys = ["State", "crop_key", "Year"]

            grouped = chunk.groupby(keys, dropna=False).agg(
                Commodity=("Commodity", "first"),
                price_record_count=("Modal_Price", "size"),
                modal_price_sum=("Modal_Price", "sum"),
                modal_price_sq_sum=("modal_price_sq", "sum"),
                min_price=("Min_Price", "min"),
                max_price=("Max_Price", "max"),
                median_modal_price=("Modal_Price", "median"),
            )
            numeric_parts.append(grouped.reset_index())

            small = chunk[keys + ["Market", "District"]].dropna(subset=keys)
            for row in small.itertuples(index=False):
                key = (row.State, row.crop_key, int(row.Year))
                if pd.notna(row.Market):
                    markets[key].add(row.Market)
                if pd.notna(row.District):
                    districts[key].add(row.District)

    if not numeric_parts:
        raise RuntimeError("No matching price rows found. Check state and crop mappings.")

    combined = pd.concat(numeric_parts, ignore_index=True)
    keys = ["State", "crop_key", "Year"]
    annual = combined.groupby(keys, as_index=False).agg(
        Commodity=("Commodity", "first"),
        price_record_count=("price_record_count", "sum"),
        modal_price_sum=("modal_price_sum", "sum"),
        modal_price_sq_sum=("modal_price_sq_sum", "sum"),
        min_price=("min_price", "min"),
        max_price=("max_price", "max"),
        median_modal_price=("median_modal_price", "median"),
    )

    annual["avg_modal_price"] = annual["modal_price_sum"] / annual["price_record_count"]
    variance = (annual["modal_price_sq_sum"] / annual["price_record_count"]) - (annual["avg_modal_price"] ** 2)
    annual["modal_price_std"] = variance.clip(lower=0).pow(0.5)
    annual["price_spread"] = annual["max_price"] - annual["min_price"]
    annual["market_count"] = annual.apply(
        lambda r: len(markets.get((r["State"], r["crop_key"], int(r["Year"])), set())), axis=1
    )
    annual["district_count"] = annual.apply(
        lambda r: len(districts.get((r["State"], r["crop_key"], int(r["Year"])), set())), axis=1
    )

    annual = annual[
        [
            "State",
            "Commodity",
            "crop_key",
            "Year",
            "avg_modal_price",
            "median_modal_price",
            "min_price",
            "max_price",
            "modal_price_std",
            "price_spread",
            "price_record_count",
            "market_count",
            "district_count",
        ]
    ].sort_values(["State", "Commodity", "Year"])

    out = PROCESSED_DIR / "annual_prices_2001_2020.csv"
    annual.to_csv(out, index=False)
    print(f"Wrote {out} with {len(annual):,} rows")
    print(f"States: {annual['State'].nunique():,}; commodities: {annual['Commodity'].nunique():,}")


if __name__ == "__main__":
    main()

