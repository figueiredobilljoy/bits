# Comprehensive Data Science Internship Report: Indian Horticulture Price & Production Analytics Pipeline

**Internship Role**: Data Science & Machine Learning Engineering Intern  
**Project Title**: End-to-End Horticulture Production & Price Modeling Pipeline and Analytics Dashboard  
**Domain**: Agricultural Economics, Time-Series Modeling & Predictive Analytics  
**Target Variable**: Annual Mandi Average Modal Price (`avg_modal_price` in ₹/Quintal)  
**Dataset Scope**: 1,444 State-Crop-Year Observations across 11 Major Indian States & 12 Horticulture Commodities (2001–2019)  
**Status**: Completed & Verified  

---

## 1. Overview of the Data Science Process Lifecycle

The project followed the standard 8-phase **Data Science Process Lifecycle** (CRISP-DM / OMNI methodology), spanning problem definition down to model deployment and web dashboard implementation.

```
                    ┌─────────────────────────────────────────┐
                    │ 1. Problem Definition & Data Acquisition │
                    └────────────────────┬────────────────────┘
                                         │
                    ┌────────────────────▼────────────────────┐
                    │ 2. Data Cleaning & Standardization      │
                    └────────────────────┬────────────────────┘
                                         │
                    ┌────────────────────▼────────────────────┐
                    │ 3. Panel Construction & Data Merging    │
                    └────────────────────┬────────────────────┘
                                         │
                    ┌────────────────────▼────────────────────┐
                    │ 4. Feature Engineering & Ratio Creation │
                    └────────────────────┬────────────────────┘
                                         │
                    ┌────────────────────▼────────────────────┐
                    │ 5. Exploratory Data Analysis (EDA)      │
                    └────────────────────┬────────────────────┘
                                         │
                    ┌────────────────────▼────────────────────┐
                    │ 6. Machine Learning Predictive Modeling │
                    └────────────────────┬────────────────────┘
                                         │
                    ┌────────────────────▼────────────────────┐
                    │ 7. Business Intelligence & Web Deployment│
                    └────────────────────┬────────────────────┘
                                         │
                    ┌────────────────────▼────────────────────┐
                    │ 8. Documentation & Knowledge Transfer   │
                    └─────────────────────────────────────────┘
```

---

## 2. Exhaustive File-by-File Technical Breakdown

Below is the detailed specification of **every single file** in the codebase, explaining what it does, its location in the data science pipeline, its inputs, outputs, and internal code logic.

---

### Pipeline Configuration & Utility Modules (Foundation Layer)

#### 1. [`scripts/pipeline_config.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/pipeline_config.py)
* **Data Science Phase**: Foundation / Pipeline Setup & Configuration
* **Description**: Central configuration module establishing filesystem paths, time horizons, selected state/crop filters, and dictionary mapping rules for data normalization.
* **Inputs**: Filesystem environment.
* **Outputs**: Python constants (`ROOT`, `PRODUCTION_FILE`, `PRICE_DIR`, `PROCESSED_DIR`, `START_YEAR`, `END_YEAR`, `SELECTED_STATES`, `HORTICULTURE_CROPS`, `STATE_ALIASES`, `CROP_ALIASES`).
* **Detailed Logic & Key Operations**:
  - Uses `pathlib.Path` to dynamically compute project root (`ROOT`) and target subdirectories (`datasets/`, `data/processed/`, `models/`).
  - Sets timeline bounds: `START_YEAR = 2001`, `END_YEAR = 2020`.
  - Defines the 11 targeted Indian states (*Uttar Pradesh, Tamil Nadu, Madhya Pradesh, Maharashtra, Gujarat, West Bengal, Karnataka, Haryana, Himachal Pradesh, Odisha, Kerala, Punjab*).
  - Defines the 12 targeted price-supported horticulture crops (*Banana, Black pepper, Coconut, Coriander, Dry Chillies, Garlic, Ginger, Onion, Potato, Sweet potato, Tapioca, Turmeric*).
  - Maintains `STATE_ALIASES` map to standardize state name variations (e.g., `"Orissa"` $\rightarrow$ `"Odisha"`, `"Uttrakhand"` $\rightarrow$ `"Uttarakhand"`).
  - Maintains `CROP_ALIASES` dictionary mapping over 35 raw commodity string variations (e.g., `"Dry chillies"` $\rightarrow$ `"Dry Chillies"`, `"Ginger (Green)"` $\rightarrow$ `"Ginger"`, `"Black Pepper"` $\rightarrow$ `"Black pepper"`).

#### 2. [`scripts/pipeline_utils.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/pipeline_utils.py)
* **Data Science Phase**: Foundation / Data Text Standardization
* **Description**: Utility module providing string cleaning, normalization, and text standardization helper functions imported by data ingestion scripts.
* **Inputs**: Raw string values from dataset columns.
* **Outputs**: Normalized and standardized text strings.
* **Detailed Logic & Key Operations**:
  - `clean_text(value)`: Trims leading/trailing whitespace, converts multiple spaces into single spaces using regex `\s+`, and handles `None`/null cases.
  - `normalize_key(value)`: Converts text to lowercase, replaces `&` with `" and "`, removes non-alphanumeric characters (`[^a-z0-9]+`), and trims whitespace to produce clean join keys (`crop_key`).
  - `standardize_state(value)`: Cleans input state string and replaces historical/alternate state names using `STATE_ALIASES`.
  - `standardize_crop(value)`: Cleans crop string and standardizes commodity names using `CROP_ALIASES`.

---

### Data Ingestion, Cleaning & Merging Pipeline (Phases 1–3)

#### 3. [`scripts/01_clean_production.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/01_clean_production.py)
* **Data Science Phase**: Data Ingestion & Preprocessing (Production Data)
* **Description**: Reads raw Excel production sheets, standardizes text attributes, casts numerical columns, filters to target states/crops/years, and exports clean production data.
* **Inputs**: [`datasets/production/Horticulture.xlsx`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/datasets/production/Horticulture.xlsx) (sheet: `crop_yield`).
* **Outputs**: [`data/processed/clean_production_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/clean_production_2001_2020.csv).
* **Detailed Logic & Key Operations**:
  - Uses `pd.read_excel` to read crop yield worksheets.
  - Renames `Crop_Year` to `Year`.
  - Standardizes `State` and `Crop` columns using `standardize_state` and `standardize_crop`.
  - Generates normalized `crop_key` column for dataset joining.
  - Casts `Year`, `Area`, `Production`, `Annual_Rainfall`, `Fertilizer`, `Pesticide`, `Yield` to numeric formats (`errors="coerce"`).
  - Filters records strictly to `SELECTED_STATES`, `HORTICULTURE_CROPS`, and years `2001–2020`.
  - Sorts by `State`, `Crop`, `Year` and writes to CSV.

#### 4. [`scripts/02_aggregate_prices.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/02_aggregate_prices.py)
* **Data Science Phase**: Data Ingestion & Aggregation (Price Mandi Transactions)
* **Description**: Processes large multi-year daily wholesale mandi transaction price CSVs in chunked batches, standardizes text, aggregates daily records to state-crop-year annual price features, and calculates statistical metrics.
* **Inputs**: [`datasets/price/{2001..2020}.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/datasets/price/) daily transaction files.
* **Outputs**: [`data/processed/annual_prices_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/annual_prices_2001_2020.csv).
* **Detailed Logic & Key Operations**:
  - Reads matching `crop_key` values from `clean_production_2001_2020.csv` to establish join targets.
  - Processes annual CSV files in chunks of `500,000` rows using `pd.read_csv(..., chunksize=CHUNKSIZE)` to manage memory efficiently.
  - Filters chunks by state, derives `Year` from `Arrival_Date`, maps `Commodity` to `standardize_crop`, and keeps valid positive modal prices (`Modal_Price > 0`).
  - Computes chunk-level intermediate aggregates: `modal_price_sum`, `modal_price_sq_sum`, `min_price`, `max_price`, `median_modal_price`, and `price_record_count`.
  - Tracks unique mandi markets (`Market`) and districts (`District`) per `(State, crop_key, Year)`.
  - Aggregates chunks into final annual metrics:
    $$\text{avg\_modal\_price} = \frac{\sum \text{Modal\_Price}}{N}$$
    $$\text{modal\_price\_std} = \sqrt{\frac{\sum \text{Modal\_Price}^2}{N} - (\text{avg\_modal\_price})^2}$$
    $$\text{price\_spread} = \text{max\_price} - \text{min\_price}$$
  - Exports clean annual price panel to CSV.

#### 5. [`scripts/03_build_master_table.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/03_build_master_table.py)
* **Data Science Phase**: Dataset Integration & Panel Construction
* **Description**: Merges clean annual production data with aggregated annual mandi price features on `(State, crop_key, Year)` using a left-join, adds initial lag features, and creates a master dataset panel.
* **Inputs**: [`clean_production_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/clean_production_2001_2020.csv), [`annual_prices_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/annual_prices_2001_2020.csv).
* **Outputs**: [`data/processed/master_table_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/master_table_2001_2020.csv).
* **Detailed Logic & Key Operations**:
  - Performs `left_join` of production and price datasets.
  - Adds binary indicator column `price_available` (1 if price matched, 0 if missing).
  - Computes initial 1-year lag features (`Production_lag_1`, `Yield_lag_1`, `Area_lag_1`, `avg_modal_price_lag_1`) grouped by `(State, Crop)`.
  - Computes 3-year rolling means (`avg_modal_price_roll_3`, `Production_roll_3`).
  - Exports unified master table containing 1,444 records across 28 columns.

#### 6. [`scripts/04_missing_value_audit.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/04_missing_value_audit.py)
* **Data Science Phase**: Data Quality Audit & Diagnostics
* **Description**: Performs a comprehensive audit of missing values across all attributes in the master table, categorizing missingness overall, by crop, and by state.
* **Inputs**: [`data/processed/master_table_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/master_table_2001_2020.csv).
* **Outputs**: [`missing_summary.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/missing_summary.csv), [`missing_by_crop.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/missing_by_crop.csv), [`missing_by_state.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/missing_by_state.csv).
* **Detailed Logic & Key Operations**:
  - `missing_summary(df)`: Calculates missing count and percentage for every column.
  - `grouped_missing(df, group_col)`: Groups missing price statistics by `State` and `Crop`, calculating match rates and column-wise missing percentages.
  - Identifies crops and states with lowest price coverage to guide imputation logic.

#### 7. [`scripts/05_prepare_modeling_table.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/05_prepare_modeling_table.py)
* **Data Science Phase**: Missing Value Imputation & Preliminary Dataset Preparation
* **Description**: Constructs missingness indicator flags (`_was_missing`) and fills missing values using a multi-tiered hierarchical median fallback imputation strategy.
* **Inputs**: [`data/processed/master_table_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/master_table_2001_2020.csv).
* **Outputs**: [`modeling_table_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/modeling_table_2001_2020.csv), [`price_modeling_train_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/price_modeling_train_2001_2020.csv).
* **Detailed Logic & Key Operations**:
  - Implements `fill_by_groups(df, source_col)`:
    $$\text{Impute Priority: } (\text{State}, \text{Crop}) \text{ median} \rightarrow (\text{Crop}) \text{ median} \rightarrow (\text{State}) \text{ median} \rightarrow \text{Global median}$$
  - Creates explicit binary tracking columns for missing attributes (e.g. `avg_modal_price_was_missing`).
  - Filters target-available rows (`target_available == 1`) to produce dedicated training set `price_modeling_train_2001_2020.csv`.

#### 8. [`scripts/01_clean_and_preprocess.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/01_clean_and_preprocess.py)
* **Data Science Phase**: Second-Phase Data Preprocessing & Outlier Capping
* **Description**: Refines the master table by enforcing strict non-negative constraints, standardizing state/crop strings, performing hierarchical median imputation, and capping top 99.5th percentile price outliers.
* **Inputs**: [`data/processed/master_table_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/master_table_2001_2020.csv).
* **Outputs**: [`data/processed/clean_master_table_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/clean_master_table_2001_2020.csv).
* **Detailed Logic & Key Operations**:
  - Strips whitespace and standardizes column names.
  - Applies hierarchical imputation across numerical price attributes (`avg_modal_price`, `min_price`, `max_price`, `modal_price_std`, `price_spread`).
  - Outlier Capping: Computes 99.5th percentile thresholds for `modal_price_std` and `price_spread` and caps extreme upper values to reduce skewness.
  - Enforces non-negative bounds: `df[col] = df[col].clip(lower=0)`.

---

### Feature Engineering, EDA & Modeling Pipeline (Phases 4–6)

#### 9. [`scripts/02_transform_and_engineer.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/02_transform_and_engineer.py)
* **Data Science Phase**: Feature Engineering, Economic Ratio Creation & Transformation
* **Description**: Computes temporal lag features ($t-1, t-2$), YoY price/production momentum changes, rolling window statistics, agricultural efficiency ratios, log transformations, and categorical encoding.
* **Inputs**: [`clean_master_table_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/clean_master_table_2001_2020.csv).
* **Outputs**: [`transformed_master_table_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/transformed_master_table_2001_2020.csv).
* **Detailed Logic & Key Operations**:
  - Sorts deterministically by `State`, `Crop`, `Year`.
  - Computes 1-year and 2-year lags: `Production_lag_1`, `Production_lag_2`, `Yield_lag_1`, `Area_lag_1`, `avg_modal_price_lag_1`, `avg_modal_price_lag_2`.
  - Computes YoY Rates of Change:
    $$\text{price\_change\_yoy} = \frac{\text{avg\_modal\_price\_lag\_1} - \text{avg\_modal\_price\_lag\_2}}{\text{avg\_modal\_price\_lag\_2} + 1e-5}$$
    $$\text{production\_change\_yoy} = \frac{\text{Production\_lag\_1} - \text{Production\_lag\_2}}{\text{Production\_lag\_2} + 1e-5}$$
  - Computes 3-year rolling window statistics: `avg_modal_price_roll_3_mean`, `avg_modal_price_roll_3_std`, `Production_roll_3_mean`, `Yield_roll_3_mean`.
  - Computes domain-specific economic & input ratios:
    - `price_volatility_index` = `modal_price_std` / `avg_modal_price`
    - `price_spread_ratio` = `price_spread` / `avg_modal_price`
    - `production_per_rainfall` = `Production` / (`Annual_Rainfall` + 1.0)
    - `fertilizer_intensity` = `Fertilizer` / `Area`
    - `pesticide_intensity` = `Pesticide` / `Area`
    - `input_cost_index` = (`Fertilizer` + `Pesticide`) / `Area`
  - Applies logarithmic transformations: `log_Production` = $\ln(1 + \text{Production})$, `log_Area` = $\ln(1 + \text{Area})$, `log_avg_modal_price` = $\ln(1 + \text{avg\_modal\_price})$.
  - Encodes categorical IDs: `State_code`, `Crop_code`.
  - Fills edge-case NaNs from group shifting using backward fill and crop median fallback.
  - Outputs transformed master table (1,444 rows, 58 features).

#### 10. [`scripts/03_exploratory_data_analysis.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/03_exploratory_data_analysis.py)
* **Data Science Phase**: Exploratory Data Analysis & Statistical Payload Generation
* **Description**: Performs correlation analysis (Pearson and Spearman), calculates multi-year national trends, computes state and crop level aggregations, and packages results into JSON analytics payloads.
* **Inputs**: [`transformed_master_table_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/transformed_master_table_2001_2020.csv).
* **Outputs**: [`correlation_matrix.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/correlation_matrix.csv), [`eda_analytics_payload.json`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/eda_analytics_payload.json).
* **Detailed Logic & Key Operations**:
  - Computes full Pearson ($r$) and Spearman ($\rho$) correlation matrices across numerical attributes.
  - Extracts key statistical relationship pairs (e.g. `avg_modal_price` vs `avg_modal_price_lag_1` Spearman $\rho = 0.9094$; `Yield` vs `Fertilizer` Pearson $r = 0.4850$).
  - Calculates 20-year national time series trends for price, production, area, yield, and rainfall.
  - Generates state-wise and crop-wise summary benchmarks (mean price, price volatility, total output volume).
  - Serializes analytics structure to JSON for web dashboard consumption.

#### 11. [`scripts/04_train_ml_models.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/04_train_ml_models.py)
* **Data Science Phase**: Machine Learning Predictive Modeling & Out-of-Sample Evaluation
* **Description**: Prepares training data via One-Hot Encoding, enforces a temporal out-of-sample train/test split, trains four regression algorithms, evaluates performance metrics ($R^2$, MAE, RMSE, MAPE), extracts feature importances, serializes the best model weights, and saves results to JSON.
* **Inputs**: [`transformed_master_table_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/transformed_master_table_2001_2020.csv).
* **Outputs**: [`models/best_horticulture_price_model.pkl`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/models/best_horticulture_price_model.pkl), [`data/processed/ml_modeling_results.json`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/ml_modeling_results.json).
* **Detailed Logic & Key Operations**:
  - Defines target column: `avg_modal_price`.
  - Feature set selection: 23 numerical engineered features + One-Hot Encoded `State` and `Crop` dummy variables (46 total predictors).
  - **Temporal Train/Test Split**:
    - Training Set: `Year <= 2016` (1,191 records, 2001–2016)
    - Test Set: `Year >= 2017` (253 records, 2017–2019 out-of-sample holdout)
  - Evaluates 4 Machine Learning Algorithms:
    1. `LinearRegression()`
    2. `Ridge(alpha=10.0)`
    3. `RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42)`
    4. `GradientBoostingRegressor(n_estimators=120, learning_rate=0.08, max_depth=5, random_state=42)`
  - Calculates out-of-sample evaluation metrics:
    $$\text{MAE} = \frac{1}{n} \sum |y - \hat{y}|, \quad \text{RMSE} = \sqrt{\frac{1}{n} \sum (y - \hat{y})^2}, \quad R^2 = 1 - \frac{\sum (y - \hat{y})^2}{\sum (y - \bar{y})^2}$$
    $$\text{MAPE} = \frac{100\%}{n} \sum \left| \frac{y - \hat{y}}{\max(y, 1.0)} \right|$$
  - Results achieved: **Random Forest Regressor** won with **$R^2 = 0.6529$**, **MAE = ₹1,264.92/Quintal**, and **MAPE = 34.8%**.
  - Extracts top feature importances (`Area_lag_1`: 34.9%, `avg_modal_price_lag_2`: 13.7%, `avg_modal_price_lag_1`: 10.1%).
  - Serializes best model object using `joblib.dump` to `models/best_horticulture_price_model.pkl`.
  - Writes sample predictions and model benchmarks to `ml_modeling_results.json`.

---

### Dashboard Compilation & Deployment Layer (Phase 7)

#### 12. [`scripts/build_dashboard_data.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/build_dashboard_data.py)
* **Data Science Phase**: Dashboard Data Assembly & Pre-compilation
* **Description**: Merges EDA JSON payloads, ML model evaluation results, and historical observation records into a single sanitized JavaScript variable file for CORS-free browser execution.
* **Inputs**: [`eda_analytics_payload.json`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/eda_analytics_payload.json), [`ml_modeling_results.json`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/ml_modeling_results.json), [`transformed_master_table_2001_2020.csv`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/data/processed/transformed_master_table_2001_2020.csv).
* **Outputs**: [`dashboard/data.js`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/dashboard/data.js).
* **Detailed Logic & Key Operations**:
  - Reads `eda_analytics_payload.json` and `ml_modeling_results.json`.
  - Reads essential record columns from transformed master table (`Year`, `State`, `Crop`, `Production`, `Yield`, `Area`, `Annual_Rainfall`, `avg_modal_price`, `price_volatility_index`).
  - `sanitize_for_js(value)`: Replaces `NaN` and `Infinity` values with `null` to ensure strict JSON / JavaScript compatibility.
  - Generates JavaScript payload file: `window.HORTICULTURE_DATA = { ... };`.
  - Writes `dashboard/data.js` to enable zero-CORS local file viewing without needing a complex backend server.

#### 13. [`dashboard/index.html`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/dashboard/index.html)
* **Data Science Phase**: User Interface / Front-End Web Application
* **Description**: Responsive HTML5 user interface featuring glassmorphic navigation header, executive KPI overview cards, interactive multi-select filter controls, canvas containers for Chart.js charts, Spearman correlation grid, and an interactive What-If price simulator.
* **Inputs**: User browser interactions.
* **Outputs**: Rendered Web Dashboard UI.
* **Key Components**:
  - Filter Bar: State Selector (`#state-filter`), Crop Selector (`#crop-filter`), Horizon Selector (`#horizon-filter`).
  - KPI Cards: Displaying Average Price, Annual Production Volume, Price Volatility Index, and Out-of-Sample Model $R^2$ Score.
  - Chart Elements: Out-of-Sample Actual vs Predicted Price chart, YoY Production vs Price Trend chart, Feature Importance horizontal bar chart.
  - Correlation Heatmap Grid: Container (`#heatmap-grid`) for rendering interactive pairwise correlation cells.
  - Interactive What-If Price Simulator: Interactive sliders/inputs for Lagged Price, Acreage, Fertilizer, and Rainfall to compute predicted price in real time.

#### 14. [`dashboard/styles.css`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/dashboard/styles.css)
* **Data Science Phase**: Web Application Styling & UX Design
* **Description**: Custom CSS stylesheet introducing a modern dark theme, neon accents, CSS glassmorphism, responsive grid layouts, and animated card transitions.
* **Key Visual Specifications**:
  - Color Palette: Deep Slate background (`#0f172a`), Card Background (`rgba(30, 41, 59, 0.7)`), Accent Cyan (`#06b6d4`), Neon Green (`#10b981`), Warning Gold (`#f59e0b`).
  - Styling Techniques: CSS `backdrop-filter: blur(12px)`, CSS Grid (`grid-template-columns: repeat(auto-fit, minmax(...))`), custom scrollbars, responsive media queries for mobile viewports.

#### 15. [`dashboard/app.js`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/dashboard/app.js)
* **Data Science Phase**: Dashboard Dynamic Controller & Client-Side Simulator Logic
* **Description**: Vanilla JavaScript application script that binds `window.HORTICULTURE_DATA` to the HTML UI, updates KPI cards dynamically based on filter changes, renders interactive Chart.js charts, constructs the correlation matrix heatmap, and executes client-side What-If price predictions.
* **Inputs**: [`dashboard/data.js`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/dashboard/data.js), User filter inputs.
* **Outputs**: Interactive DOM updates, rendered charts, and dynamic simulation results.
* **Detailed Logic & Key Operations**:
  - Listens for `DOMContentLoaded` event.
  - Population of Dropdowns: Extracts unique `State` and `Crop` options from `HORTICULTURE_DATA.records`.
  - Event Listeners: Attaches `change` listeners to dropdown filters to trigger re-rendering of KPI cards and time-series charts.
  - Chart Rendering Functions: Instantiates Chart.js line and bar instances (`renderPriceChart`, `renderTrendChart`, `renderImportanceChart`).
  - Heatmap Generator (`renderHeatmap`): Iterates over Spearman correlation matrix, computing background color dynamically using cyan/magenta color scaling.
  - **What-If Price Simulator Controller**: Reads user input values for `Lagged Price`, `Cultivated Area`, `Fertilizer Intensity`, and `Rainfall`, applies trained model weight multipliers, and updates predicted price output in real time.

#### 16. [`dashboard/data.js`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/dashboard/data.js)
* **Data Science Phase**: Web Application Data Store
* **Description**: Pre-compiled standalone JavaScript data store exposing global variable `window.HORTICULTURE_DATA`.
* **Inputs**: Auto-generated by `build_dashboard_data.py`.
* **Outputs**: In-memory JavaScript object containing `eda`, `ml`, and historical `records`.

---

### Documentation & Reporting Layer (Phase 8)

#### 17. [`HORTICULTURE_ANALYSIS_REPORT.md`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/HORTICULTURE_ANALYSIS_REPORT.md)
* **Data Science Phase**: Analytical Documentation & Policy Reporting
* **Description**: Executive-level data science report summarizing project scope, statistical correlation findings, state and crop commodity dynamics, machine learning benchmark comparisons, top feature drivers, and strategic policy recommendations.

#### 18. [`PROJECT_OCCURRENCES_LOG.md`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/PROJECT_OCCURRENCES_LOG.md)
* **Data Science Phase**: Technical Project Execution Log
* **Description**: Detailed chronological record logging all 6 main pipeline stages, script execution commands, output row/column counts, missingness audit results, and verification milestones.

#### 19. [`README.md`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/README.md)
* **Data Science Phase**: Project Documentation & User Guide
* **Description**: Main project landing page containing setup instructions, step-by-step PowerShell pipeline execution order, description of key output files, and data folder storage notes.

#### 20. [`links.txt`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/links.txt)
* **Data Science Phase**: Raw Data Provenance Tracking
* **Description**: Plain text file storing external Google Drive cloud storage links for the raw horticulture production Excel files and raw daily mandi price transaction CSV datasets.

---

## 3. Summary Matrix of Every File in the Project

| File Path | Data Science Phase | Key Responsibility / Function | Output / Artifact Generated |
| :--- | :--- | :--- | :--- |
| [`scripts/pipeline_config.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/pipeline_config.py) | Configuration | Constants, paths, state/crop lists, alias maps | Configuration constants |
| [`scripts/pipeline_utils.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/pipeline_utils.py) | Utility / Text | String cleaning, key normalization, alias mapping | Normalized string values |
| [`scripts/01_clean_production.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/01_clean_production.py) | Preprocessing | Excel parsing, state/crop filtering, numeric casting | `clean_production_2001_2020.csv` |
| [`scripts/02_aggregate_prices.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/02_aggregate_prices.py) | Aggregation | Daily mandi CSV chunked reading & annual feature aggregation | `annual_prices_2001_2020.csv` |
| [`scripts/03_build_master_table.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/03_build_master_table.py) | Dataset Integration | Merges production & prices into master panel, initial lags | `master_table_2001_2020.csv` |
| [`scripts/04_missing_value_audit.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/04_missing_value_audit.py) | Quality Audit | Missingness summary overall, by crop, and by state | 3 missing audit CSV reports |
| [`scripts/05_prepare_modeling_table.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/05_prepare_modeling_table.py) | Imputation | Hierarchical median imputation & indicator flags | `modeling_table_2001_2020.csv` |
| [`scripts/01_clean_and_preprocess.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/01_clean_and_preprocess.py) | Cleaning / Outliers | Outlier capping (99.5th percentile) & non-negative bounds | `clean_master_table_2001_2020.csv` |
| [`scripts/02_transform_and_engineer.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/02_transform_and_engineer.py) | Feature Engineering | Lags, YoY momentum, rolling stats, ratio metrics, log scaling | `transformed_master_table_2001_2020.csv` |
| [`scripts/03_exploratory_data_analysis.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/03_exploratory_data_analysis.py) | EDA / Statistics | Pearson & Spearman correlation matrices, 20-year trends | `eda_analytics_payload.json` |
| [`scripts/04_train_ml_models.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/04_train_ml_models.py) | ML Modeling | OHE, Temporal split, trains 4 models, feature importance | `best_horticulture_price_model.pkl` |
| [`scripts/build_dashboard_data.py`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/scripts/build_dashboard_data.py) | Assembly | Compiles JSON payloads & records into JS file | `dashboard/data.js` |
| [`dashboard/index.html`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/dashboard/index.html) | Front-End UI | Layout, filters, KPI cards, chart canvases, simulator | Interactive Web UI |
| [`dashboard/styles.css`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/dashboard/styles.css) | UX / Styling | Glassmorphism dark theme, grid layouts, responsive rules | Custom CSS design |
| [`dashboard/app.js`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/dashboard/app.js) | Dynamic Logic | Chart.js rendering, filter event handling, What-If simulator | Live UI interactions |
| [`dashboard/data.js`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/dashboard/data.js) | Data Store | Precompiled JavaScript object containing all analytical data | `window.HORTICULTURE_DATA` |
| [`HORTICULTURE_ANALYSIS_REPORT.md`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/HORTICULTURE_ANALYSIS_REPORT.md) | Reporting | Analytical executive report, statistical insights & policies | Analytical report document |
| [`PROJECT_OCCURRENCES_LOG.md`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/PROJECT_OCCURRENCES_LOG.md) | Execution Log | Chronological pipeline execution and verification log | Process log document |
| [`README.md`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/README.md) | Documentation | Project overview, execution steps, output file guide | Readme file |
| [`links.txt`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/links.txt) | Provenance | External raw dataset Google Drive storage links | External link references |
| [`internship.md`](file:///C:/Users/Billjoy%20Figueiredo/Desktop/bits/internship.md) | Internship Report | **This Document**: Exhaustive file-by-file data science report | Full Internship Document |
