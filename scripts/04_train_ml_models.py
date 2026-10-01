import pandas as pd
import numpy as np
import json
import joblib
from pathlib import Path
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Paths
ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
MODELS_DIR = ROOT_DIR / "models"
INPUT_FILE = PROCESSED_DIR / "transformed_master_table_2001_2020.csv"
OUTPUT_JSON = PROCESSED_DIR / "ml_modeling_results.json"

def calculate_mape(y_true, y_pred):
    return float(np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1.0))) * 100)

def train_and_evaluate():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Loading transformed dataset from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    target_col = "avg_modal_price"
    
    # Predictor columns
    feature_cols = [
        "Production", "Yield", "Area", "Annual_Rainfall", "Fertilizer", "Pesticide",
        "Production_lag_1", "Yield_lag_1", "Area_lag_1", "avg_modal_price_lag_1", "avg_modal_price_lag_2",
        "avg_modal_price_roll_3_mean", "avg_modal_price_roll_3_std", "Production_roll_3_mean", "Yield_roll_3_mean",
        "price_volatility_index", "price_spread_ratio", "production_per_rainfall", "fertilizer_intensity",
        "pesticide_intensity", "input_cost_index", "log_Production", "log_Area"
    ]
    
    # Add One-Hot Encoding for State and Crop
    df_encoded = pd.get_dummies(df, columns=["State", "Crop"], drop_first=False)
    state_crop_dummy_cols = [c for c in df_encoded.columns if c.startswith("State_") or c.startswith("Crop_")]
    all_feature_cols = feature_cols + state_crop_dummy_cols
    
    # Temporal Train/Test Split (Train: 2001-2016, Test: 2017 onward)
    train_mask = df_encoded["Year"] <= 2016
    test_mask = df_encoded["Year"] >= 2017
    
    X_train = df_encoded.loc[train_mask, all_feature_cols]
    y_train = df_encoded.loc[train_mask, target_col]
    X_test = df_encoded.loc[test_mask, all_feature_cols]
    y_test = df_encoded.loc[test_mask, target_col]
    
    print(f"Training set: {X_train.shape[0]} samples (2001-2016)")
    print(f"Test set: {X_test.shape[0]} samples (2017-{int(df_encoded.loc[test_mask, 'Year'].max())})")
    
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=10.0),
        "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=120, learning_rate=0.08, max_depth=5, random_state=42)
    }
    
    results = {}
    best_model_name = None
    best_r2 = -float("inf")
    trained_model_objs = {}
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        mae = float(mean_absolute_error(y_test, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mape = calculate_mape(y_test, y_pred)
        r2 = float(r2_score(y_test, y_pred))
        
        results[name] = {
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "MAPE": round(mape, 2),
            "R2": round(r2, 4)
        }
        
        print(f"[{name}] MAE: {mae:.2f} | RMSE: {rmse:.2f} | MAPE: {mape:.2f}% | R2: {r2:.4f}")
        trained_model_objs[name] = model
        
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            
    print(f"\nBest Performing Model: {best_model_name} (R2 = {best_r2:.4f})")
    best_model = trained_model_objs[best_model_name]
    
    # Save best model to disk
    joblib.dump(best_model, MODELS_DIR / "best_horticulture_price_model.pkl")
    
    # Feature Importances (from best ensemble model)
    if hasattr(best_model, "feature_importances_"):
        importances = best_model.feature_importances_
        feature_imp_df = pd.DataFrame({
            "feature": all_feature_cols,
            "importance": importances
        }).sort_values("importance", ascending=False)
        top_importances = feature_imp_df.head(15).to_dict(orient="records")
    else:
        top_importances = []
        
    # Store predictions on test set for visualization
    test_df_results = df.loc[test_mask, ["Year", "State", "Crop", "avg_modal_price"]].copy()
    test_df_results["predicted_price"] = best_model.predict(X_test).round(2)
    sample_predictions = test_df_results.head(50).to_dict(orient="records")
    
    # Package final JSON results
    output_data = {
        "best_model": best_model_name,
        "metrics": results,
        "feature_importances": top_importances,
        "sample_predictions": sample_predictions,
        "features_list": feature_cols
    }
    
    with open(OUTPUT_JSON, "w") as f:
        json.dump(output_data, f, indent=2)
        
    print(f"ML Modeling Results saved to {OUTPUT_JSON}.")
    print("Stage 4 Machine Learning Predictive Modeling completed successfully!\n")

if __name__ == "__main__":
    train_and_evaluate()
