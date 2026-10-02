# Actual Files, Datasets, Scripts and Artifacts Used

## Internship Project

**Project:** End-to-End Horticulture Production & Price Modeling
Pipeline and Analytics Dashboard\
**Role:** Data Science & Machine Learning Engineering Intern\
**Domain:** Agricultural Economics, Time-Series Modeling & Predictive
Analytics\
**Internship period:** 3 August 2026 -- 3 October 2026

This document records the actual files, datasets, scripts, processed
datasets, models, dashboard files and documentation artifacts described
in the internship technical documentation.

------------------------------------------------------------------------

# 1. Raw Data Sources

## 1.1 Horticulture Production Dataset

### `datasets/production/Horticulture.xlsx`

**Type:** Excel workbook\
**Role:** Primary production/agricultural dataset\
**Used by:** `scripts/01_clean_production.py`

The production workbook contained the crop-yield information used as the
base agricultural dataset.

Relevant fields included:

-   Crop
-   Year
-   State
-   Area
-   Production
-   Annual Rainfall
-   Fertilizer
-   Pesticide
-   Yield

The production-cleaning script read the `crop_yield` worksheet and
converted the required fields into analysis-ready formats.

------------------------------------------------------------------------

## 1.2 Raw Mandi Price Datasets

### `datasets/price/{2001..2020}.csv`

**Type:** Multiple yearly CSV files\
**Role:** Raw daily wholesale mandi transaction-price data\
**Used by:** `scripts/02_aggregate_prices.py`

The price data consisted of daily transaction records across multiple
years.

The processing pipeline:

-   Read the yearly files in chunks.
-   Filtered relevant states.
-   Derived year information from `Arrival_Date`.
-   Standardized commodity names.
-   Retained valid positive `Modal_Price` values.
-   Aggregated daily transactions into annual state-crop-year
    statistics.

The project used chunked processing with a chunk size of **500,000
rows** to manage large files.

------------------------------------------------------------------------

## 1.3 Raw Data Provenance

### `links.txt`

**Role:** Raw-data provenance tracking

This file stored external Google Drive links associated with the raw
horticulture production Excel files and daily mandi price CSV datasets.

It provided a record of where the source datasets were stored.

------------------------------------------------------------------------

# 2. Configuration and Utility Scripts

## 2.1 `scripts/pipeline_config.py`

**Pipeline role:** Foundation / configuration

This script defined project-wide constants and configuration.

It contained:

-   Project root paths
-   Production-data path
-   Price-data path
-   Processed-data path
-   Model path
-   Start year
-   End year
-   Selected states
-   Selected horticulture crops
-   State aliases
-   Crop aliases

### Important configuration

-   `START_YEAR = 2001`
-   `END_YEAR = 2020`

The configuration also defined the selected states and target
horticulture commodities.

------------------------------------------------------------------------

## 2.2 `scripts/pipeline_utils.py`

**Pipeline role:** Text cleaning and standardization utility module

Functions included:

### `clean_text(value)`

-   Removed leading/trailing whitespace.
-   Collapsed repeated whitespace.
-   Handled null/empty values.

### `normalize_key(value)`

-   Converted text to lowercase.
-   Replaced `&` with `"and"`.
-   Removed non-alphanumeric characters.
-   Generated normalized join keys such as `crop_key`.

### `standardize_state(value)`

-   Cleaned state names.
-   Applied state aliases.
-   Standardized alternate/historical names.

### `standardize_crop(value)`

-   Cleaned crop names.
-   Applied crop aliases.
-   Standardized commodity names between datasets.

------------------------------------------------------------------------

# 3. Production-Data Processing

## 3.1 `scripts/01_clean_production.py`

**Pipeline stage:** Data ingestion and preprocessing

### Input

`datasets/production/Horticulture.xlsx`

### Output

`data/processed/clean_production_2001_2020.csv`

### Operations

-   Read the `crop_yield` worksheet.
-   Renamed `Crop_Year` to `Year`.
-   Standardized state names.
-   Standardized crop names.
-   Created `crop_key`.
-   Converted numerical columns.
-   Filtered the selected states.
-   Filtered the selected crops.
-   Restricted the data to 2001--2020.
-   Sorted records by State, Crop and Year.
-   Exported the cleaned production dataset.

------------------------------------------------------------------------

# 4. Mandi Price Aggregation

## 4.1 `scripts/02_aggregate_prices.py`

**Pipeline stage:** Price-data ingestion and aggregation

### Inputs

`datasets/price/{2001..2020}.csv`

### Output

`data/processed/annual_prices_2001_2020.csv`

### Operations

-   Read large CSV files in chunks.
-   Used `crop_key` values from the cleaned production data as join
    targets.
-   Filtered price records by state.
-   Derived Year from `Arrival_Date`.
-   Standardized Commodity values.
-   Removed invalid/non-positive modal prices.
-   Aggregated daily records into annual state-crop-year features.

### Generated price variables

-   `avg_modal_price`
-   `modal_price_std`
-   `min_price`
-   `max_price`
-   `price_spread`
-   `price_record_count`
-   Unique market count
-   Unique district count

### Core calculations

Average modal price:

`sum(Modal_Price) / number_of_records`

Price standard deviation:

Based on the aggregated sum and squared-sum statistics.

Price spread:

`max_price - min_price`

------------------------------------------------------------------------

# 5. Master Dataset Construction

## 5.1 `scripts/03_build_master_table.py`

**Pipeline stage:** Dataset integration / panel construction

### Inputs

-   `clean_production_2001_2020.csv`
-   `annual_prices_2001_2020.csv`

### Output

`data/processed/master_table_2001_2020.csv`

### Operations

-   Performed a left join.
-   Joined using State, `crop_key` and Year.
-   Added `price_available`.
-   Added initial one-year lag features.
-   Generated:
    -   `Production_lag_1`
    -   `Yield_lag_1`
    -   `Area_lag_1`
    -   `avg_modal_price_lag_1`
-   Generated initial three-year rolling variables.
-   Produced the unified master panel.

### Master-table size

The technical report documents:

-   **1,444 records**
-   **28 columns**

------------------------------------------------------------------------

# 6. Missing-Value Audit

## 6.1 `scripts/04_missing_value_audit.py`

**Pipeline stage:** Data-quality audit

### Input

`data/processed/master_table_2001_2020.csv`

### Outputs

-   `data/processed/missing_summary.csv`
-   `data/processed/missing_by_crop.csv`
-   `data/processed/missing_by_state.csv`

### Operations

-   Counted missing values in every column.
-   Calculated missing percentages.
-   Examined missingness by crop.
-   Examined missingness by state.
-   Identified areas with weaker price coverage.
-   Produced diagnostic reports for subsequent imputation.

------------------------------------------------------------------------

# 7. Modeling-Table Preparation

## 7.1 `scripts/05_prepare_modeling_table.py`

**Pipeline stage:** Missing-value preparation

### Input

`data/processed/master_table_2001_2020.csv`

### Outputs

-   `data/processed/modeling_table_2001_2020.csv`
-   `data/processed/price_modeling_train_2001_2020.csv`

### Operations

Created missingness indicators such as:

`avg_modal_price_was_missing`

Used hierarchical median imputation:

1.  State + Crop median
2.  Crop median
3.  State median
4.  Global median

Then created a dedicated training dataset containing observations where
the target variable was available.

------------------------------------------------------------------------

# 8. Second-Stage Cleaning and Outlier Processing

## 8.1 `scripts/01_clean_and_preprocess.py`

**Pipeline stage:** Cleaning / outlier treatment

### Input

`data/processed/master_table_2001_2020.csv`

### Output

`data/processed/clean_master_table_2001_2020.csv`

### Operations

-   Standardized column names.
-   Removed/handled unnecessary whitespace.
-   Applied hierarchical imputation to numerical price attributes.
-   Enforced non-negative bounds.
-   Capped selected extreme values at the 99.5th percentile.

Variables treated included:

-   `avg_modal_price`
-   `min_price`
-   `max_price`
-   `modal_price_std`
-   `price_spread`

------------------------------------------------------------------------

# 9. Feature Engineering Dataset

## 9.1 `scripts/02_transform_and_engineer.py`

**Pipeline stage:** Feature engineering

### Input

`data/processed/clean_master_table_2001_2020.csv`

### Output

`data/processed/transformed_master_table_2001_2020.csv`

### Operations

The script created the expanded analytical dataset.

### Temporal features

-   `Production_lag_1`
-   `Production_lag_2`
-   `Yield_lag_1`
-   `Area_lag_1`
-   `avg_modal_price_lag_1`
-   `avg_modal_price_lag_2`

### Year-over-year features

-   `price_change_yoy`
-   `production_change_yoy`

### Rolling features

-   `avg_modal_price_roll_3_mean`
-   `avg_modal_price_roll_3_std`
-   `Production_roll_3_mean`
-   `Yield_roll_3_mean`

### Agricultural/economic ratios

-   `price_volatility_index`
-   `price_spread_ratio`
-   `production_per_rainfall`
-   `fertilizer_intensity`
-   `pesticide_intensity`
-   `input_cost_index`

### Transformations

-   `log_Production`
-   `log_Area`
-   `log_avg_modal_price`

### Encodings

-   `State_code`
-   `Crop_code`

### Final transformed dataset

The technical report documents:

-   **1,444 rows**
-   **58 features**

------------------------------------------------------------------------

# 10. Exploratory Data Analysis

## 10.1 `scripts/03_exploratory_data_analysis.py`

**Pipeline stage:** EDA and statistical analysis

### Input

`data/processed/transformed_master_table_2001_2020.csv`

### Outputs

-   `data/processed/correlation_matrix.csv`
-   `data/processed/eda_analytics_payload.json`

### Operations

-   Pearson correlation analysis.
-   Spearman correlation analysis.
-   Multi-year national trends.
-   State-level aggregation.
-   Crop-level aggregation.
-   Price analysis.
-   Production analysis.
-   Area analysis.
-   Yield analysis.
-   Rainfall analysis.
-   Price-volatility analysis.
-   Dashboard-ready analytical payload generation.

The documented analysis included relationships such as:

-   `avg_modal_price` vs `avg_modal_price_lag_1`
-   `Yield` vs `Fertilizer`

------------------------------------------------------------------------

# 11. Machine-Learning Model Training

## 11.1 `scripts/04_train_ml_models.py`

**Pipeline stage:** Predictive modeling

### Input

`data/processed/transformed_master_table_2001_2020.csv`

### Outputs

-   `models/best_horticulture_price_model.pkl`
-   `data/processed/ml_modeling_results.json`

### Target

`avg_modal_price`

### Predictors

The documented model used:

-   23 numerical engineered features
-   One-hot encoded State
-   One-hot encoded Crop
-   46 total predictors after encoding

### Temporal split

Training:

-   2001--2016
-   1,191 records

Testing:

-   2017 onward in the documented out-of-sample period
-   253 records

### Models trained

1.  Linear Regression
2.  Ridge Regression
3.  Random Forest Regressor
4.  Gradient Boosting Regressor

### Evaluation metrics

-   R²
-   MAE
-   RMSE
-   MAPE

### Reported Random Forest result

-   R²: **0.6529**
-   MAE: **₹1,264.92/quintal**
-   MAPE: **34.8%**

### Important feature-importance outputs

The documented leading features included:

-   `Area_lag_1`
-   `avg_modal_price_lag_2`
-   `avg_modal_price_lag_1`

------------------------------------------------------------------------

# 12. Saved Price-Prediction Model

## `models/best_horticulture_price_model.pkl`

**Type:** Serialized Python model artifact

**Purpose:** Stores the trained best-performing horticulture
price-prediction model for reuse.

It was produced using `joblib.dump`.

------------------------------------------------------------------------

# 13. Machine-Learning Results File

## `data/processed/ml_modeling_results.json`

Contains model-related outputs such as:

-   Model benchmarks
-   Evaluation metrics
-   Sample predictions
-   Model comparison results

This file was later consumed by the dashboard-generation workflow.

------------------------------------------------------------------------

# 14. Dashboard Data Compilation

## 14.1 `scripts/build_dashboard_data.py`

**Pipeline stage:** Dashboard data assembly

### Inputs

-   `eda_analytics_payload.json`
-   `ml_modeling_results.json`
-   `transformed_master_table_2001_2020.csv`

### Output

`dashboard/data.js`

### Operations

-   Combined EDA results.
-   Combined ML results.
-   Selected historical records.
-   Included variables such as:
    -   Year
    -   State
    -   Crop
    -   Production
    -   Yield
    -   Area
    -   Annual Rainfall
    -   Average modal price
    -   Price volatility index
-   Replaced NaN and Infinity values with `null`.
-   Generated a browser-readable `window.HORTICULTURE_DATA` object.

------------------------------------------------------------------------

# 15. Dashboard Frontend

## 15.1 `dashboard/index.html`

**Role:** Main dashboard user interface

### Components

-   State filter
-   Crop filter
-   Time-horizon filter
-   KPI cards
-   Average price display
-   Annual production display
-   Price-volatility display
-   Out-of-sample R² display
-   Actual vs predicted price chart
-   Production vs price trend chart
-   Feature-importance chart
-   Correlation heatmap
-   What-If price simulator

------------------------------------------------------------------------

## 15.2 `dashboard/styles.css`

**Role:** Dashboard styling

Included:

-   Responsive layout
-   Grid-based interface
-   Dark visual theme
-   Card layouts
-   Glassmorphism effects
-   Responsive behavior
-   Animated interface elements
-   Custom styling for dashboard components

------------------------------------------------------------------------

## 15.3 `dashboard/app.js`

**Role:** Dashboard dynamic logic

### Operations

-   Loaded `window.HORTICULTURE_DATA`.
-   Populated state and crop filters.
-   Responded to filter changes.
-   Updated KPI cards.
-   Rendered Chart.js charts.
-   Rendered the correlation heatmap.
-   Rendered feature-importance visualization.
-   Implemented the What-If price simulator.
-   Updated predicted price values from user-controlled inputs.

------------------------------------------------------------------------

## 15.4 `dashboard/data.js`

**Role:** Precompiled dashboard data store

Contains:

`window.HORTICULTURE_DATA`

The object contains:

-   EDA information
-   ML results
-   Historical records

It allows the dashboard to operate without requiring a complex backend
for the prepared analytical data.

------------------------------------------------------------------------

# 16. Crop Recognition Dataset and Model

This was a separate crop-recognition component from the horticulture
price-prediction model.

## 16.1 Dataset

### Kaggle Agriculture Crop Images

**Source:** Kaggle Agriculture Crop Images

**Total images:** 999

### Dataset structure

-   `crop_images/` --- 201 base field photos
-   `kag2/` --- 798 augmented variations

### Crop classes

-   Jute
-   Maize
-   Rice
-   Sugarcane
-   Wheat

------------------------------------------------------------------------

# 17. Crop Recognition Training Artifacts

## 17.1 `crop_model.pth`

**Role:** Trained MobileNetV2 crop-recognition model weights.

------------------------------------------------------------------------

## 17.2 `class_indices.json`

**Role:** Mapping between model class indices and crop labels.

------------------------------------------------------------------------

## 17.3 `model_metrics.json`

**Role:** Stores crop-recognition evaluation metrics.

------------------------------------------------------------------------

## 17.4 `training_evaluation.png`

**Role:** Training/evaluation visualization.

Contains the training curve and confusion-matrix visualization described
in the model report.

------------------------------------------------------------------------

# 18. Crop Recognition Training Method

## Model Architecture

### MobileNetV2

Used as the pretrained image-classification backbone.

The documented architecture included:

-   Input: 224 × 224 × 3
-   MobileNetV2 ImageNet-pretrained backbone
-   1280-dimensional feature output
-   Dropout
-   Dense layer: 1280 → 128
-   Batch normalization
-   ReLU
-   Dropout
-   Output layer: 128 → 5
-   Softmax

## Training

### Phase 1

-   MobileNetV2 backbone frozen.
-   Classification head trained.
-   Adam optimizer.
-   Learning rate: `1e-3`.
-   ReduceLROnPlateau scheduler.

### Phase 2

-   Top six convolutional feature blocks unfrozen.
-   Fine-tuned with learning rate `1e-4`.

### Dataset splitting

Used grouped splitting to prevent augmented variants of the same
original image from appearing across training and evaluation sets.

Documented split:

-   Train: 793 images
-   Validation: 107 images
-   Test: 99 images

### Reported validation performance

**75.7% validation accuracy**

------------------------------------------------------------------------

# 19. Crop Recognition Web Application

## `app.py`

**Role:** Backend inference application

Technologies documented:

-   Python
-   Flask
-   PyTorch

### Operations

-   Loads `crop_model.pth`.
-   Loads `class_indices.json`.
-   Receives uploaded crop images.
-   Performs image preprocessing.
-   Runs model inference.
-   Produces top crop prediction.
-   Produces confidence percentage.
-   Produces the full probability distribution.

### Endpoints documented

-   `/predict`
-   `/sample_images`

------------------------------------------------------------------------

# 20. Crop Recognition Frontend

## `templates/index.html`

**Role:** Web interface for crop recognition

Included:

-   Drag-and-drop image upload
-   File browsing
-   Image preview
-   Loading indicator
-   Predicted crop badge
-   Confidence percentage
-   Probability bars for all five crops
-   Interactive sample-image gallery

------------------------------------------------------------------------

# 21. Satellite / Remote-Sensing Work

The internship also included a satellite-based crop-detection/validation
component.

## Data and tools

-   Sentinel-2 satellite imagery
-   Google Earth Engine
-   Python
-   Geographic coordinates
-   NDVI
-   Other vegetation/spectral indicators

## Workflow

1.  Selected reference geographic coordinates.
2.  Located agricultural areas around the coordinates.
3.  Retrieved/inspected Sentinel-2 imagery.
4.  Used Google Earth Engine for satellite-data access and processing.
5.  Used Python for additional data handling.
6.  Calculated NDVI and other spectral/vegetation indicators.
7.  Retrieved crop imagery from selected areas.
8.  Used the satellite information to investigate crop detectability.

## Validation status

The satellite component achieved **partial crop detection/validation in
selected areas**.

It did **not** achieve complete quantitative validation of the entire
horticulture dataset.

------------------------------------------------------------------------

# 22. Internship Documentation Files

## `HORTICULTURE_ANALYSIS_REPORT.md`

**Role:** Analytical report

Contained:

-   Project scope
-   Statistical findings
-   Correlation analysis
-   State/crop analysis
-   Machine-learning benchmarks
-   Feature drivers
-   Analytical conclusions/recommendations

------------------------------------------------------------------------

## `PROJECT_OCCURRENCES_LOG.md`

**Role:** Technical execution log

Contained:

-   Chronological project execution
-   Pipeline stages
-   Script execution records
-   Output row/column counts
-   Missingness-audit results
-   Verification milestones

------------------------------------------------------------------------

## `README.md`

**Role:** Main project guide

Contained:

-   Project overview
-   Setup instructions
-   PowerShell execution order
-   Description of important outputs
-   Data-directory organization
-   Project workflow

------------------------------------------------------------------------

## `links.txt`

**Role:** Data provenance

Contained external links for the raw production and mandi-price
datasets.

------------------------------------------------------------------------

## `internship.md`

**Role:** Comprehensive internship technical report

Documented:

-   Data-science lifecycle
-   File-by-file technical breakdown
-   Inputs and outputs
-   Processing logic
-   Feature engineering
-   EDA
-   Machine learning
-   Dashboard
-   Documentation
-   Project file structure

------------------------------------------------------------------------

# 23. Complete Processing Chain

The actual project files form the following pipeline:

``` text
Raw Production Excel
        │
        ▼
01_clean_production.py
        │
        ▼
clean_production_2001_2020.csv
        │
        │
Raw Mandi Price CSVs
        │
        ▼
02_aggregate_prices.py
        │
        ▼
annual_prices_2001_2020.csv
        │
        └──────────────┐
                       ▼
              03_build_master_table.py
                       │
                       ▼
              master_table_2001_2020.csv
                       │
          ┌────────────┴─────────────┐
          ▼                          ▼
04_missing_value_audit.py    05_prepare_modeling_table.py
          │                          │
          ▼                          ▼
Missingness reports          modeling datasets
                                     │
                                     ▼
                         01_clean_and_preprocess.py
                                     │
                                     ▼
                         clean_master_table_2001_2020.csv
                                     │
                                     ▼
                         02_transform_and_engineer.py
                                     │
                                     ▼
                       transformed_master_table_2001_2020.csv
                                     │
                     ┌───────────────┴───────────────┐
                     ▼                               ▼
          03_exploratory_data_analysis.py    04_train_ml_models.py
                     │                               │
                     ▼                               ▼
          correlation_matrix.csv          best_horticulture_price_model.pkl
          eda_analytics_payload.json      ml_modeling_results.json
                     │                               │
                     └───────────────┬───────────────┘
                                     ▼
                         build_dashboard_data.py
                                     │
                                     ▼
                              dashboard/data.js
                                     │
                  ┌──────────────────┼──────────────────┐
                  ▼                  ▼                  ▼
             index.html         styles.css           app.js
                                     │
                                     ▼
                           Interactive Dashboard
```

------------------------------------------------------------------------

# 24. Main Dataset/Artifact Inventory

  ----------------------------------------------------------------------------------------------
  Category                File / Dataset                             Purpose
  ----------------------- ------------------------------------------ ---------------------------
  Raw data                `Horticulture.xlsx`                        Production data

  Raw data                `datasets/price/{2001..2020}.csv`          Daily mandi price
                                                                     transactions

  Configuration           `pipeline_config.py`                       Pipeline configuration

  Utilities               `pipeline_utils.py`                        Text normalization

  Processing              `01_clean_production.py`                   Production preprocessing

  Processing              `02_aggregate_prices.py`                   Annual price aggregation

  Integration             `03_build_master_table.py`                 Production-price merge

  Quality                 `04_missing_value_audit.py`                Missing-data analysis

  Imputation              `05_prepare_modeling_table.py`             Missing-value preparation

  Cleaning                `01_clean_and_preprocess.py`               Outlier
                                                                     treatment/refinement

  Features                `02_transform_and_engineer.py`             Feature engineering

  EDA                     `03_exploratory_data_analysis.py`          Statistical/EDA outputs

  ML                      `04_train_ml_models.py`                    Price prediction

  Processed data          `clean_production_2001_2020.csv`           Clean production data

  Processed data          `annual_prices_2001_2020.csv`              Annual price data

  Processed data          `master_table_2001_2020.csv`               Integrated master table

  Processed data          `modeling_table_2001_2020.csv`             Imputed modeling table

  Processed data          `price_modeling_train_2001_2020.csv`       Price-model training data

  Processed data          `clean_master_table_2001_2020.csv`         Refined master table

  Processed data          `transformed_master_table_2001_2020.csv`   Feature-engineered dataset

  EDA output              `correlation_matrix.csv`                   Correlation results

  EDA output              `eda_analytics_payload.json`               Dashboard analytics

  ML output               `ml_modeling_results.json`                 Model metrics/results

  Model                   `best_horticulture_price_model.pkl`        Best price model

  Dashboard               `build_dashboard_data.py`                  Dashboard data compilation

  Dashboard               `index.html`                               Dashboard UI

  Dashboard               `styles.css`                               Dashboard styling

  Dashboard               `app.js`                                   Dashboard logic

  Dashboard               `data.js`                                  Dashboard data store

  Crop ML                 `crop_model.pth`                           MobileNetV2 crop model

  Crop ML                 `class_indices.json`                       Crop class mapping

  Crop ML                 `model_metrics.json`                       Crop-model metrics

  Crop ML                 `training_evaluation.png`                  Training/confusion-matrix
                                                                     output

  Crop app                `app.py`                                   Crop-model inference
                                                                     backend

  Crop app                `templates/index.html`                     Crop-recognition frontend

  Documentation           `HORTICULTURE_ANALYSIS_REPORT.md`          Analytical report

  Documentation           `PROJECT_OCCURRENCES_LOG.md`               Execution log

  Documentation           `README.md`                                Project guide

  Provenance              `links.txt`                                Raw-data links

  Internship              `internship.md`                            Comprehensive technical
                                                                     report
  ----------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 25. Overall File-Based Data-Science Workflow

The project therefore involved more than simply analyzing one CSV. It
consisted of a sequence of **raw datasets → cleaning scripts →
aggregated datasets → integrated master table → quality audits →
imputation → refined dataset → engineered dataset → EDA outputs → ML
outputs → dashboard data → web dashboard**, together with a separate
**crop-recognition model and application** and a
**satellite/remote-sensing crop-detection workflow**.

The major persistent analytical dataset was the production-price master
table, while the major derived datasets were the cleaned, modeling and
feature-engineered versions. The major model artifacts were the
horticulture price model and the MobileNetV2 crop-recognition model. The
major presentation artifact was the interactive analytics dashboard.
