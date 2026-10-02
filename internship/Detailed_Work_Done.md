# Detailed Internship Work Log

## Internship Period

**3 August 2026 -- 3 October 2026**

**Working pattern:** Monday--Saturday\
**Weekly off:** Sunday\
**Declared holidays:** 15 August 2026 (Independence Day), 14 September
2026 (Ganesh Chaturthi)

## Project

**End-to-End Horticulture Production & Price Modeling Pipeline and
Analytics Dashboard**

**Role:** Data Science & Machine Learning Engineering Intern

**Domain:** Agricultural Economics, Time-Series Modeling & Predictive
Analytics

**Target variable:** Annual Mandi Average Modal Price
(`avg_modal_price`)

**Dataset scope:** 1,444 state-crop-year observations across the
selected Indian states and horticulture commodities, covering the
2001--2020 processing window in the project pipeline. The internship
report describes 1,444 records and 28 columns in the master table.

------------------------------------------------------------------------

# Week 1 --- 3--8 August 2026

## Project Orientation, Data Acquisition and Production-Data Preparation

### Monday, 3 August --- Project Orientation

-   Reviewed the horticulture data-science problem and project
    objectives.
-   Understood the intended end-to-end workflow from raw agricultural
    datasets through preprocessing, analysis, modeling and presentation.
-   Identified the major data sources: horticulture production data and
    mandi price transaction data.
-   Reviewed the main analytical dimensions: state, crop and year.
-   Established the initial project structure and Python-based workflow.

### Tuesday, 4 August --- Production Dataset Inspection

-   Set up the Python working environment for data processing.
-   Inspected the raw horticulture production data.
-   Reviewed the available columns and their data types.
-   Examined variables including year, area, production, annual
    rainfall, fertilizer, pesticide and yield.
-   Reviewed the available state, crop and year coverage.
-   Identified the need for text standardization and numeric conversion
    before analysis.

### Wednesday, 5 August --- State and Crop Standardization

-   Examined inconsistent representations of state and crop names.
-   Established standardized state names for reliable joining and
    filtering.
-   Standardized commodity/crop names across source data.
-   Created normalized crop keys for later dataset integration.
-   Prepared reusable Python utility functions for text cleaning and
    normalization.

### Thursday, 6 August --- Production Data Cleaning

-   Read the production worksheet using Python/Pandas.
-   Renamed the year field into a consistent `Year` representation.
-   Standardized the `State` and `Crop` columns.
-   Generated normalized crop keys.
-   Converted `Year`, `Area`, `Production`, `Annual_Rainfall`,
    `Fertilizer`, `Pesticide` and `Yield` to numeric formats.
-   Applied the selected state, crop and year filters.
-   Sorted the resulting production records and generated the cleaned
    production dataset.

### Friday, 7 August --- Initial Python/NumPy Development

-   Studied Python concepts needed for data-processing scripts.
-   Practiced variables, collections, functions and reusable code.
-   Worked with NumPy arrays and numerical operations.
-   Practiced basic vectorized calculations.
-   Related the programming concepts to the requirements of the
    agricultural dataset.

### Saturday, 8 August --- Pandas Foundations

-   Practiced Pandas Series and DataFrames.
-   Worked with CSV and Excel files.
-   Practiced inspecting rows, columns, dimensions and data types.
-   Practiced selecting columns and filtering rows.
-   Generated basic summaries of datasets.

------------------------------------------------------------------------

# Week 2 --- 10--15 August 2026

## Mandi Price Processing and Annual Aggregation

### Monday, 10 August --- Clean Production Dataset

-   Completed the production-data preprocessing workflow.
-   Verified standardized crop and state values.
-   Verified the selected year range and target state/crop scope.
-   Produced the clean production dataset used by later pipeline stages.

### Tuesday, 11 August --- Large Mandi Transaction Processing

-   Began processing multi-year daily mandi transaction files.
-   Used chunked CSV reading to manage large files efficiently.
-   Filtered transactions by relevant states.
-   Derived the year from arrival dates.
-   Standardized raw commodity names.
-   Retained valid positive modal-price observations.

### Wednesday, 12 August --- Annual Price Feature Aggregation

-   Aggregated daily mandi transactions to annual state-crop-year
    records.
-   Calculated average modal price.
-   Calculated minimum and maximum prices.
-   Calculated modal-price standard deviation.
-   Calculated price spread.
-   Counted price records.
-   Prepared annual price statistics for joining with production data.

### Thursday, 13 August --- Market and District Coverage

-   Tracked unique mandi markets for each state-crop-year group.
-   Tracked unique districts represented in the price data.
-   Consolidated chunk-level aggregates into final annual price
    statistics.
-   Exported the annual price panel.
-   Checked price coverage before integration.

### Friday, 14 August --- Pandas Cleaning and Aggregation

-   Practiced Pandas sorting and filtering.
-   Practiced `groupby()` and aggregation operations.
-   Worked with grouped numerical summaries.
-   Practiced selecting and transforming columns.
-   Applied the concepts to data-processing tasks relevant to the
    project.

### Saturday, 15 August --- Independence Day

**Holiday --- No internship work.**

------------------------------------------------------------------------

# Week 3 --- 17--22 August 2026

## Master Table Construction and Data Quality

### Monday, 17 August --- Production and Price Integration

-   Loaded the cleaned production and annual price datasets.
-   Joined production and price information using state, normalized crop
    key and year.
-   Used the production dataset as the base of the integrated panel.
-   Checked whether price information matched the production
    observations.

### Tuesday, 18 August --- Master Table Construction

-   Created the unified horticulture master table.
-   Added the `price_available` indicator.
-   Created initial one-year lag variables.
-   Added lagged production, yield, area and price variables grouped by
    state and crop.
-   Generated the integrated master dataset.

### Wednesday, 19 August --- Missing-Value Audit

-   Audited missing values across all master-table attributes.
-   Calculated missing counts and percentages.
-   Examined missingness by crop.
-   Examined missingness by state.
-   Identified crops and states with weaker price coverage.
-   Generated missing-value summary outputs.

### Thursday, 20 August --- Missing-Value Preparation

-   Created a modeling-ready dataset.
-   Implemented hierarchical median imputation.
-   Used state-crop median first.
-   Used crop median as the next fallback.
-   Used state median as the next fallback.
-   Used global median when necessary.
-   Created binary indicators showing whether values had originally been
    missing.
-   Prepared the dedicated price-modeling training dataset.

### Friday, 21 August --- Pandas Grouping, Joins and Missing Data

-   Practiced grouped transformations using Pandas.
-   Practiced joins and merges between datasets.
-   Practiced sorting and group-wise calculations.
-   Practiced missing-value detection and replacement.
-   Related these operations to the master-table and data-quality
    workflow.

### Saturday, 22 August --- Descriptive Statistics

-   Practiced descriptive statistical summaries in Python.
-   Reviewed count, mean, median and spread.
-   Examined distributions of numerical variables.
-   Practiced using summary statistics to understand dataset quality.
-   Connected descriptive statistics to the initial exploratory
    analysis.

------------------------------------------------------------------------

# Week 4 --- 24--29 August 2026

## Data Refinement and Feature Engineering

### Monday, 24 August --- Data Quality Refinement

-   Refined the master table after the missing-value stage.
-   Standardized column values.
-   Enforced non-negative constraints on applicable numerical variables.
-   Prepared price-related variables for further analysis.

### Tuesday, 25 August --- Outlier Handling

-   Applied percentile-based outlier treatment to price-related
    variability measures.
-   Used the 99.5th percentile as the upper capping threshold for
    selected extreme variables.
-   Reduced the influence of extreme observations while retaining the
    observations in the dataset.
-   Generated the cleaned master table.

### Wednesday, 26 August --- Temporal Lag Features

-   Created one-year lag features.
-   Created two-year lag features where required.
-   Generated lagged production, yield, area and price variables.
-   Calculated lag values within state-crop groups.
-   Preserved the temporal structure of the panel.

### Thursday, 27 August --- Rolling Statistics and Domain Features

-   Created three-year rolling price statistics.
-   Created three-year rolling production and yield statistics.
-   Created price volatility index.
-   Created price spread ratio.
-   Created production-per-rainfall measure.
-   Created fertilizer intensity.
-   Created pesticide intensity.
-   Created input cost index.
-   Applied logarithmic transformations to production, area and price.
-   Created categorical state and crop codes.
-   Handled edge-case missing values caused by lag and rolling
    operations.

### Friday, 28 August --- Advanced Pandas Transformations

-   Practiced group-wise transformations.
-   Practiced creating multiple derived columns.
-   Worked with temporal ordering and grouped calculations.
-   Practiced operations needed for lagged and rolling features.
-   Improved familiarity with reusable data-transformation workflows.

### Saturday, 29 August --- NumPy Numerical Processing

-   Practiced NumPy vectorized calculations.
-   Worked with numerical arrays and mathematical transformations.
-   Practiced logarithmic transformations.
-   Reviewed efficient numerical processing for large datasets.
-   Connected NumPy operations with feature-generation tasks.

------------------------------------------------------------------------

# Week 5 --- 31 August--5 September 2026

## Exploratory Data Analysis and Statistical Analysis

### Monday, 31 August --- Analytical Dataset Finalization

-   Finalized the transformed analytical dataset.
-   Verified engineered features.
-   Verified categorical encodings.
-   Addressed edge cases created by shifting and rolling calculations.
-   Prepared the dataset for EDA and modeling.

### Tuesday, 1 September --- Exploratory Data Analysis

-   Examined production, area, yield, rainfall and price variables.
-   Investigated distributions across the multi-year dataset.
-   Compared observations across states and crops.
-   Reviewed summary statistics and major analytical patterns.

### Wednesday, 2 September --- Correlation Analysis

-   Calculated Pearson correlation coefficients.
-   Calculated Spearman correlation coefficients.
-   Generated the correlation matrix.
-   Examined relationships between price and lagged price.
-   Examined relationships between yield and fertilizer.
-   Extracted relevant statistical relationship pairs.

### Thursday, 3 September --- Trend and Group-Level Analysis

-   Calculated multi-year national trends.
-   Examined price trends.
-   Examined production trends.
-   Examined cultivated-area trends.
-   Examined yield trends.
-   Examined rainfall trends.
-   Generated state-level summaries.
-   Generated crop-level summaries.
-   Prepared analytical outputs for dashboard use.

### Friday, 4 September --- Python Analytical Workflows

-   Practiced combining Pandas and NumPy operations.
-   Worked on repeatable data-analysis workflows.
-   Practiced producing summary tables.
-   Practiced transforming data for analysis.
-   Organized analytical outputs into reusable structures.

### Saturday, 5 September --- Data Visualization

-   Practiced visualizing analytical data with Python.
-   Worked with time-based trends.
-   Worked with category comparisons.
-   Reviewed distribution plots.
-   Practiced visualizing numerical relationships.
-   Focused on presenting analytical findings clearly.

------------------------------------------------------------------------

# Week 6 --- 7--12 September 2026

## Predictive Price Modeling

### Monday, 7 September --- Modeling Dataset Preparation

-   Prepared the transformed dataset for machine learning.
-   Selected engineered numerical predictors.
-   Selected categorical state and crop information.
-   Applied one-hot encoding to categorical variables.
-   Prepared the final predictor matrix.

### Tuesday, 8 September --- Temporal Validation Setup

-   Implemented a chronological train/test split.
-   Used records through 2016 for training.
-   Used later years as the out-of-sample test period.
-   Preserved temporal ordering rather than randomly mixing years.
-   Prepared the evaluation framework.

### Wednesday, 9 September --- Regression Model Training

-   Trained Linear Regression.
-   Trained Ridge Regression.
-   Trained Random Forest Regressor.
-   Trained Gradient Boosting Regressor.
-   Compared the models using the same target and evaluation framework.

### Thursday, 10 September --- Model Evaluation

-   Calculated R².
-   Calculated MAE.
-   Calculated RMSE.
-   Calculated MAPE.
-   Compared out-of-sample performance.
-   Examined feature importance.
-   Saved the selected model as a reusable model artifact.
-   Generated machine-learning evaluation results and sample
    predictions.

### Friday, 11 September --- Python Script and Workflow Organization

-   Practiced organizing data-science scripts into separate processing
    stages.
-   Practiced input/output file handling.
-   Practiced reusable functions.
-   Reviewed how intermediate datasets can be passed from one processing
    stage to another.
-   Focused on reproducible Python workflows.

### Saturday, 12 September --- SQL for Data Analysis

-   Practiced SQL `SELECT` queries.
-   Practiced filtering with `WHERE`.
-   Practiced aggregation and `GROUP BY`.
-   Practiced sorting and selecting analytical results.
-   Practiced joins for combining related data.
-   Related relational-data concepts to the integrated horticulture
    dataset.

------------------------------------------------------------------------

# Week 7 --- 14--19 September 2026

## Satellite Data, NDVI and Crop Detection

### Monday, 14 September --- Ganesh Chaturthi

**Holiday --- No internship work.**

### Tuesday, 15 September --- Coordinate-Based Satellite Workflow

-   Began the satellite crop-detection workflow using geographic
    coordinates.
-   Selected specific agricultural locations for examination.
-   Used coordinates as reference points for obtaining imagery.
-   Established the connection between geographic locations and
    crop-detection analysis.

### Wednesday, 16 September --- Sentinel-2 Data Retrieval

-   Worked with Sentinel-2 satellite imagery.
-   Used Google Earth Engine for satellite-data access and processing.
-   Also used Python for parts of the satellite-data workflow.
-   Retrieved and examined imagery for selected coordinate-based
    agricultural locations.

### Thursday, 17 September --- NDVI and Spectral Analysis

-   Calculated NDVI.
-   Calculated other vegetation/spectral indicators used in the
    analysis.
-   Examined vegetation characteristics around selected coordinates.
-   Used the satellite-derived indicators to investigate crop
    detectability.
-   Used the satellite work as a partial validation/detection step
    rather than claiming complete dataset-wide validation.

### Friday, 18 September --- Python for Satellite Data Processing

-   Practiced Python-based processing of extracted numerical
    observations.
-   Organized satellite-derived values into structured records.
-   Worked with numerical feature values associated with geographic
    locations.
-   Prepared feature information for crop-detection work.

### Saturday, 19 September --- Satellite Feature Organization

-   Organized coordinate-based satellite observations.
-   Maintained consistent geographic references.
-   Structured extracted vegetation/spectral features.
-   Prepared the information needed for crop-detection experiments.

------------------------------------------------------------------------

# Week 8 --- 21--26 September 2026

## Crop Recognition Model

### Monday, 21 September --- Crop Image Dataset Preparation

-   Prepared the crop-image dataset used for crop recognition.
-   Worked with the five target classes: jute, maize, rice, sugarcane
    and wheat.
-   Reviewed the dataset structure.
-   Prepared image data for model training and evaluation.

### Tuesday, 22 September --- MobileNetV2 Transfer Learning

-   Built the crop-recognition model using MobileNetV2.
-   Used a pretrained ImageNet MobileNetV2 backbone.
-   Prepared the custom classification head.
-   Configured image input size and classification outputs.
-   Set up the model-training workflow.

### Wednesday, 23 September --- Leak-Free Dataset Splitting

-   Identified groups corresponding to original images and their
    augmented variants.
-   Used grouped splitting to avoid augmented versions of the same
    original image appearing in different evaluation sets.
-   Prepared training, validation and test partitions.
-   Maintained separation between training and evaluation data.

### Thursday, 24 September --- Model Fine-Tuning and Evaluation

-   Trained the classification head during the initial warm-up phase.
-   Fine-tuned the upper MobileNetV2 layers using a lower learning rate.
-   Reviewed validation performance.
-   Generated trained model weights.
-   Generated class mapping.
-   Generated evaluation metrics.
-   Generated training-curve and confusion-matrix artifacts.
-   Prepared the model for inference.

### Friday, 25 September --- Python Project Organization

-   Practiced organizing Python code, datasets and model artifacts.
-   Reviewed file paths and output management.
-   Practiced keeping processing, modeling and application components
    separated.
-   Focused on making the project easier to reproduce and explain.

### Saturday, 26 September --- Python Model Inference Application

-   Worked with Python application logic for image input.
-   Connected the trained model to inference code.
-   Prepared image preprocessing before prediction.
-   Prepared probability outputs and predicted crop labels.
-   Integrated the model into the crop-recognition application workflow.

------------------------------------------------------------------------

# Week 9 --- 28 September--3 October 2026

## Dashboard, Integration, Testing and Finalization

### Monday, 28 September --- Dashboard Data Assembly

-   Combined EDA results with machine-learning results.
-   Included selected historical records from the transformed master
    table.
-   Prepared a dashboard-ready data structure.
-   Sanitized invalid numerical values such as NaN and Infinity before
    JavaScript use.
-   Generated the dashboard data store.

### Tuesday, 29 September --- Interactive Dashboard Development

-   Built the dashboard interface.
-   Added state filtering.
-   Added crop filtering.
-   Added time-horizon filtering.
-   Added KPI cards for average price, annual production, price
    volatility and model R².
-   Added analytical charts.
-   Added the correlation heatmap.

### Wednesday, 30 September --- What-If Price Simulator

-   Integrated model outputs into the dashboard.
-   Implemented the interactive price simulator.
-   Added inputs for lagged price, cultivated area, fertilizer intensity
    and rainfall.
-   Connected user inputs to model-based price prediction.
-   Displayed predicted results interactively.

### Thursday, 1 October --- Testing and Verification

-   Tested dashboard filters.
-   Checked chart rendering.
-   Checked analytical data flow.
-   Verified model-result integration.
-   Checked the correlation visualization.
-   Tested the What-If simulator.
-   Corrected presentation and integration issues identified during
    testing.

### Friday, 2 October --- Documentation and Reproducibility

-   Reviewed the Python pipeline and execution order.
-   Organized project scripts and generated outputs.
-   Reviewed the analytical workflow from raw data to final dashboard.
-   Consolidated technical explanations of the processing stages.
-   Prepared the project documentation and supporting records.

### Saturday, 3 October --- Final Completion

-   Completed final project verification.
-   Consolidated datasets and analytical outputs.
-   Organized model artifacts.
-   Organized dashboard files.
-   Consolidated technical documentation.
-   Finalized the internship work and report.
