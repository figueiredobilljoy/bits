import pandas as pd
import numpy as np
import json
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
INPUT_FILE = PROCESSED_DIR / "transformed_master_table_2001_2020.csv"
OUTPUT_JSON = PROCESSED_DIR / "eda_analytics_payload.json"
OUTPUT_CORR_CSV = PROCESSED_DIR / "correlation_matrix.csv"

def run_eda():
    print(f"Loading transformed dataset from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    # 1. Key Columns for Correlation Analysis
    corr_cols = [
        "avg_modal_price", "Production", "Yield", "Area", "Annual_Rainfall",
        "Fertilizer", "Pesticide", "modal_price_std", "price_spread",
        "Production_lag_1", "avg_modal_price_lag_1", "price_volatility_index",
        "input_cost_index", "production_per_rainfall"
    ]
    
    # Compute Pearson & Spearman Correlations
    pearson_corr = df[corr_cols].corr(method="pearson").round(4)
    spearman_corr = df[corr_cols].corr(method="spearman").round(4)
    
    pearson_corr.to_csv(OUTPUT_CORR_CSV)
    print(f"Pearson correlation matrix saved to {OUTPUT_CORR_CSV}.")
    
    # 2. Temporal Trends (Annual Aggregations)
    yearly_agg = df.groupby("Year").agg({
        "avg_modal_price": "mean",
        "Production": "sum",
        "Yield": "mean",
        "Annual_Rainfall": "mean",
        "Area": "sum"
    }).reset_index().round(2)
    
    # Crop-wise annual price trends
    crop_yearly_price = df.pivot_table(
        index="Year", columns="Crop", values="avg_modal_price", aggfunc="mean"
    ).round(2).reset_index()
    
    # State-wise annual production trends
    state_yearly_prod = df.pivot_table(
        index="Year", columns="State", values="Production", aggfunc="sum"
    ).round(2).reset_index()
    
    # 3. Summary Metrics by State
    state_summary = df.groupby("State").agg({
        "Production": "sum",
        "Area": "mean",
        "avg_modal_price": "mean",
        "Yield": "mean",
        "price_volatility_index": "mean"
    }).reset_index().round(2)
    
    # 4. Summary Metrics by Crop
    crop_summary = df.groupby("Crop").agg({
        "Production": "sum",
        "Area": "mean",
        "avg_modal_price": "mean",
        "min_price": "min",
        "max_price": "max",
        "Yield": "mean",
        "price_volatility_index": "mean"
    }).reset_index().round(2)
    
    # 5. Key Correlation Highlights
    key_correlations = {
        "price_vs_production": float(df["avg_modal_price"].corr(df["Production"])),
        "price_vs_lag_price": float(df["avg_modal_price"].corr(df["avg_modal_price_lag_1"])),
        "price_vs_rainfall": float(df["avg_modal_price"].corr(df["Annual_Rainfall"])),
        "yield_vs_fertilizer": float(df["Yield"].corr(df["Fertilizer"])),
        "yield_vs_pesticide": float(df["Yield"].corr(df["Pesticide"])),
        "yield_vs_rainfall": float(df["Yield"].corr(df["Annual_Rainfall"])),
        "price_vs_volatility": float(df["avg_modal_price"].corr(df["price_volatility_index"])),
        "production_vs_area": float(df["Production"].corr(df["Area"])),
    }
    
    # Format EDA payload for dashboard JSON
    eda_payload = {
        "metadata": {
            "total_records": len(df),
            "years": sorted(df["Year"].unique().tolist()),
            "states": sorted(df["State"].unique().tolist()),
            "crops": sorted(df["Crop"].unique().tolist()),
        },
        "key_correlations": {k: round(v, 4) for k, v in key_correlations.items()},
        "corr_matrix_pearson": {
            "columns": corr_cols,
            "data": pearson_corr.values.tolist()
        },
        "corr_matrix_spearman": {
            "columns": corr_cols,
            "data": spearman_corr.values.tolist()
        },
        "yearly_national_trends": yearly_agg.to_dict(orient="records"),
        "crop_yearly_prices": crop_yearly_price.to_dict(orient="records"),
        "state_yearly_production": state_yearly_prod.to_dict(orient="records"),
        "state_summary": state_summary.to_dict(orient="records"),
        "crop_summary": crop_summary.to_dict(orient="records"),
    }
    
    with open(OUTPUT_JSON, "w") as f:
        json.dump(eda_payload, f, indent=2)
        
    print(f"EDA Analytics Payload saved to {OUTPUT_JSON}.")
    print("Stage 3 Exploratory Data Analysis & Correlation Analysis completed successfully!\n")

if __name__ == "__main__":
    run_eda()
