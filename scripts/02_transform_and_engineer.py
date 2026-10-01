import pandas as pd
import numpy as np
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
INPUT_FILE = PROCESSED_DIR / "clean_master_table_2001_2020.csv"
OUTPUT_FILE = PROCESSED_DIR / "transformed_master_table_2001_2020.csv"

def engineer_features():
    print(f"Loading cleaned master table from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    # Sort deterministically for temporal feature computation
    df = df.sort_values(["State", "Crop", "Year"]).reset_index(drop=True)
    groups = df.groupby(["State", "Crop"])
    
    print("Engineering temporal lag and momentum features...")
    for col in ["Production", "Yield", "Area", "avg_modal_price"]:
        df[f"{col}_lag_1"] = groups[col].shift(1)
        df[f"{col}_lag_2"] = groups[col].shift(2)
        
    df["price_change_yoy"] = (df["avg_modal_price_lag_1"] - df["avg_modal_price_lag_2"]) / (df["avg_modal_price_lag_2"] + 1e-5)
    df["production_change_yoy"] = (df["Production_lag_1"] - df["Production_lag_2"]) / (df["Production_lag_2"] + 1e-5)
    
    print("Engineering rolling window statistics...")
    df["avg_modal_price_roll_3_mean"] = groups["avg_modal_price"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean()
    )
    df["avg_modal_price_roll_3_std"] = groups["avg_modal_price"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).std()
    ).fillna(0)
    
    df["Production_roll_3_mean"] = groups["Production"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean()
    )
    df["Yield_roll_3_mean"] = groups["Yield"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean()
    )
    
    print("Engineering economic ratios & agricultural efficiency metrics...")
    df["price_volatility_index"] = df["modal_price_std"] / (df["avg_modal_price"] + 1e-5)
    df["price_spread_ratio"] = df["price_spread"] / (df["avg_modal_price"] + 1e-5)
    df["production_per_rainfall"] = df["Production"] / (df["Annual_Rainfall"] + 1.0)
    df["fertilizer_intensity"] = df["Fertilizer"] / (df["Area"] + 1e-5)
    df["pesticide_intensity"] = df["Pesticide"] / (df["Area"] + 1e-5)
    df["input_cost_index"] = (df["Fertilizer"] + df["Pesticide"]) / (df["Area"] + 1e-5)
    
    print("Computing log transformations...")
    df["log_Production"] = np.log1p(df["Production"])
    df["log_Area"] = np.log1p(df["Area"])
    df["log_avg_modal_price"] = np.log1p(df["avg_modal_price"])
    
    # Categorical IDs
    df["State_code"] = df["State"].astype("category").cat.codes
    df["Crop_code"] = df["Crop"].astype("category").cat.codes
    
    # Fill remaining lag NaNs resulting from group shifts using hierarchical medians
    lag_cols = [c for c in df.columns if "_lag_" in c or "_roll_" in c or "change_yoy" in c]
    for col in lag_cols:
        l1 = df.groupby(["State", "Crop"])[col].transform("bfill")
        l2 = df.groupby("Crop")[col].transform("median")
        df[col] = df[col].fillna(l1).fillna(l2).fillna(df[col].median())
        
    df = df.sort_values(["State", "Crop", "Year"]).reset_index(drop=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Transformed dataset saved successfully to {OUTPUT_FILE} with {df.shape[0]} rows and {df.shape[1]} columns.")
    print("Stage 2 Feature Engineering & Transformation completed successfully!\n")

if __name__ == "__main__":
    engineer_features()
