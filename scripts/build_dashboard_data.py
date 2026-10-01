import json
import math
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DASHBOARD_DIR = ROOT_DIR / "dashboard"
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

RECORD_COLS = [
    "Year",
    "State",
    "Crop",
    "Production",
    "Yield",
    "Area",
    "Annual_Rainfall",
    "avg_modal_price",
    "price_volatility_index",
]


def sanitize_for_js(value):
    if isinstance(value, dict):
        return {key: sanitize_for_js(val) for key, val in value.items()}
    if isinstance(value, list):
        return [sanitize_for_js(item) for item in value]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value

def build_data_js():
    with open(PROCESSED_DIR / "eda_analytics_payload.json") as f:
        eda_data = json.load(f)
        
    with open(PROCESSED_DIR / "ml_modeling_results.json") as f:
        ml_data = json.load(f)

    records_df = pd.read_csv(PROCESSED_DIR / "transformed_master_table_2001_2020.csv", usecols=RECORD_COLS)
    records = records_df.round(4).where(pd.notna(records_df), None).to_dict(orient="records")
        
    compiled = {
        "eda": eda_data,
        "ml": ml_data,
        "records": records,
    }
    
    js_content = f"window.HORTICULTURE_DATA = {json.dumps(sanitize_for_js(compiled), indent=2, allow_nan=False)};"
    
    out_path = DASHBOARD_DIR / "data.js"
    with open(out_path, "w") as f:
        f.write(js_content)
        
    print(f"Compiled data written to {out_path}")

if __name__ == "__main__":
    build_data_js()
