# Full Project Occurrences & Execution Documentation

## Overview

- **Project Title**: End-to-End Horticulture Production & Price Data Science Project
- **Target Variable**: Annual Mandi Average Modal Price (`avg_modal_price` in ₹/Quintal)
- **Dataset Scope**: 1,444 records across 11 States & 12 Horticulture Crops (2001-2019)
- **Status**: Fully Completed

---

## Chronological Project Stages & Occurrences Log

### Stage 1: Data Cleaning & Preprocessing
- **Script Executed**: `scripts/01_clean_and_preprocess.py`
- **Actions Taken**:
  - Audited `data/processed/master_table_2001_2020.csv` (1,444 rows, 28 columns).
  - Standardized text strings across `State`, `Crop`, and `Commodity` attributes.
  - Tracked missingness flags for all price metrics (`avg_modal_price_was_missing`, `min_price_was_missing`, etc.).
  - Implemented hierarchical median imputation: `(State, Crop)` -> `(Crop)` -> `(State)` -> Overall median.
  - Treated extreme outliers by capping top 99.5 percentile for price variance and spread.
  - Enforced non-negative numerical constraints across production and price attributes.
- **Output File**: `data/processed/clean_master_table_2001_2020.csv` (1,444 rows, 37 columns).

---

### Stage 2: Feature Engineering & Transformation
- **Script Executed**: `scripts/02_transform_and_engineer.py`
- **Actions Taken**:
  - Computed 1-year and 2-year temporal lag features: `Production_lag_1`, `Production_lag_2`, `Yield_lag_1`, `Area_lag_1`, `avg_modal_price_lag_1`, `avg_modal_price_lag_2`.
  - Computed Year-over-Year price change (`price_change_yoy`) and production momentum (`production_change_yoy`).
  - Computed 3-year rolling mean and standard deviation: `avg_modal_price_roll_3_mean`, `avg_modal_price_roll_3_std`, `Production_roll_3_mean`.
  - Engineered economic & agricultural ratio metrics:
    - `price_volatility_index` (`modal_price_std` / `avg_modal_price`)
    - `price_spread_ratio` (`price_spread` / `avg_modal_price`)
    - `production_per_rainfall` (`Production` / `Annual_Rainfall`)
    - `fertilizer_intensity` (`Fertilizer` / `Area`)
    - `pesticide_intensity` (`Pesticide` / `Area`)
    - `input_cost_index` (`Fertilizer` + `Pesticide`) / `Area`
  - Created log-transformed numerical attributes (`log_Production`, `log_Area`, `log_avg_modal_price`) and categorical codes (`State_code`, `Crop_code`).
- **Output File**: `data/processed/transformed_master_table_2001_2020.csv` (1,444 rows, 58 columns).

---

### Stage 3: Exploratory Data Analysis & Statistical Correlations
- **Script Executed**: `scripts/03_exploratory_data_analysis.py`
- **Actions Taken**:
  - Generated full Pearson and Spearman correlation matrices for key features.
  - Calculated 20-year national trends for prices, production, yields, and rainfall.
  - Computed state-wise and crop-wise multi-year summaries.
  - Extracted key correlation highlights (e.g. Spearman `avg_modal_price` vs `avg_modal_price_lag_1` $\rho = 0.9094$; Pearson `Yield` vs `Fertilizer` $r = 0.4850$).
- **Output Files**:
  - `data/processed/correlation_matrix.csv`
  - `data/processed/eda_analytics_payload.json`

---

### Stage 4: Machine Learning Predictive Modeling
- **Script Executed**: `scripts/04_train_ml_models.py`
- **Actions Taken**:
  - Applied One-Hot Encoding for State and Crop categorical variables.
  - Configured a temporal train/test split: Train (2001-2016, 1,191 samples) and Test (2017-2019, 253 out-of-sample samples).
  - Trained 4 Machine Learning Regression models: Linear Regression, Ridge Regression ($\alpha=10$), Random Forest Regressor ($n=100$), Gradient Boosting Regressor ($n=120$).
  - Evaluated out-of-sample test metrics ($R^2$, MAE, RMSE, MAPE).
  - Best model achieved: **Random Forest Regressor** with **$R^2 = 0.6529$** (out-of-sample) and **MAE = ₹1,264.92 / Quintal**.
  - Serialized best model weights to `models/best_horticulture_price_model.pkl`.
- **Output File**: `data/processed/ml_modeling_results.json`

---

### Stage 5: Interactive Web Analytics Dashboard
- **Script Executed**: `scripts/build_dashboard_data.py` -> Compiled `dashboard/data.js`
- **Files Built**:
  - `dashboard/index.html` (Glassmorphic layout, KPI Cards, Filter Bar, Chart.js canvases, Heatmap grid, Simulator interface)
  - `dashboard/styles.css` (Dark theme, neon accents, CSS glassmorphism, responsive grid)
  - `dashboard/app.js` (Dynamic state/crop filter handling, chart updates, correlation color scale, interactive what-if simulator logic)
  - `dashboard/data.js` (Standalone JSON bundle for zero-CORS browser execution)
- **Local Server Verification**: Started `python -m http.server 8080 --directory dashboard` and verified active serving at `http://localhost:8080/index.html`.

---

### Stage 6: Documentation & Deliverables Generation
- **Files Created**:
  - `HORTICULTURE_ANALYSIS_REPORT.md` (Analytical insights, correlation findings, state/crop trends, ML model evaluation)
  - `PROJECT_OCCURRENCES_LOG.md` (This file, logging all project occurrences, transformations, and milestones)

---

## Pipeline Execution Commands Summary

To re-run the entire pipeline end-to-end:

```powershell
# 1. Clean & Preprocess
python scripts/01_clean_and_preprocess.py

# 2. Feature Engineering & Transformation
python scripts/02_transform_and_engineer.py

# 3. Exploratory Data Analysis & Correlations
python scripts/03_exploratory_data_analysis.py

# 4. Train Machine Learning Models
python scripts/04_train_ml_models.py

# 5. Build Dashboard Payload & Run Local Server
python scripts/build_dashboard_data.py
python -m http.server 8080 --directory dashboard
```
