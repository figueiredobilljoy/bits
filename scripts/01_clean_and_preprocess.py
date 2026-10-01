import pandas as pd
import numpy as np
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
INPUT_FILE = PROCESSED_DIR / "master_table_2001_2020.csv"
OUTPUT_FILE = PROCESSED_DIR / "clean_master_table_2001_2020.csv"

def fill_hierarchical_median(df, col):
    """Fills missing values using hierarchical median: (State, Crop) -> (Crop) -> (State) -> Overall."""
    res = df[col].copy()
    
    # Level 1: State & Crop
    l1 = df.groupby(["State", "Crop"])[col].transform("median")
    res = res.fillna(l1)
    
    # Level 2: Crop
    l2 = df.groupby("Crop")[col].transform("median")
    res = res.fillna(l2)
    
    # Level 3: State
    l3 = df.groupby("State")[col].transform("median")
    res = res.fillna(l3)
    
    # Level 4: Overall
    res = res.fillna(df[col].median())
    return res

def clean_and_preprocess():
    print(f"Loading raw master table from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    initial_rows, initial_cols = df.shape
    print(f"Loaded {initial_rows} rows and {initial_cols} columns.")
    
    # 1. Standardize text & missing commodities
    df["Commodity"] = df["Commodity"].fillna(df["Crop"]).astype(str).str.strip()
    df["State"] = df["State"].astype(str).str.strip()
    df["Crop"] = df["Crop"].astype(str).str.strip()
    
    # 2. Track missing status before imputation
    price_cols = [
        "avg_modal_price", "median_modal_price", "min_price", 
        "max_price", "modal_price_std", "price_spread"
    ]
    
    for col in price_cols:
        df[f"{col}_was_missing"] = df[col].isna().astype(int)
        
    count_cols = ["price_record_count", "market_count", "district_count"]
    for col in count_cols:
        df[f"{col}_was_missing"] = df[col].isna().astype(int)
        df[col] = df[col].fillna(0)
        
    # 3. Hierarchical imputation for price metrics
    print("Imputing missing price columns with hierarchical medians...")
    for col in price_cols:
        df[col] = fill_hierarchical_median(df, col)
        
    # 4. Enforce non-negative constraint
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if "was_missing" not in col and col != "Year":
            df[col] = df[col].clip(lower=0)
            
    # 5. Capping extreme percentile outliers for price spread & std (upper 99.5 percentile)
    for col in ["modal_price_std", "price_spread"]:
        p995 = df[col].quantile(0.995)
        df[col] = np.minimum(df[col], p995)

    # 6. Sort deterministically
    df = df.sort_values(["State", "Crop", "Year"]).reset_index(drop=True)
    
    # Save cleaned file
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Cleaned dataset saved successfully to {OUTPUT_FILE} with {df.shape[0]} rows and {df.shape[1]} columns.")
    print("Stage 1 Data Cleaning & Preprocessing completed successfully!\n")

if __name__ == "__main__":
    clean_and_preprocess()
