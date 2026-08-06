# Modeling CSV Files Documentation

This document explains the two prepared CSV files used after building the horticulture master table.

```text
data/processed/modeling_table_2001_2020.csv
data/processed/price_modeling_train_2001_2020.csv
```

They are related, but they should be used for different purposes.

## 1. modeling_table_2001_2020.csv

### Purpose

This is the full prepared modeling table.

It keeps every available `State + Crop + Year` row from the 12-crop horticulture master table, including rows where the target price is missing.

Use this file for:

```text
Full data analysis
Missing-value checking
EDA
Understanding state-crop-year coverage
Future prediction rows
Checking where price data is unavailable
```

### Shape

```text
Rows: 1,444
Columns: 59
Crops: 12
States: 11
Years: 2001-2019
```

### Important Point

This file includes both:

```text
Rows where avg_modal_price exists
Rows where avg_modal_price is missing
```

The column `target_available` tells you whether the target price exists:

```text
target_available = 1 means avg_modal_price exists
target_available = 0 means avg_modal_price is missing
```

So this file is useful for analysis, but it is not the best file for directly training a supervised price prediction model.

### Column Meanings for modeling_table_2001_2020.csv

| Column | Meaning |
|---|---|
| `State` | State where the crop was produced and where price data was matched |
| `Crop` | Standardized crop name from the production dataset |
| `Commodity` | Standardized commodity name from the price dataset; may be blank when price was not matched |
| `crop_key` | Normalized crop key used internally for merging crop and commodity names |
| `Year` | Year of the production and annual price record |
| `Season` | Crop season from production data |
| `Area` | Cultivated area for the crop |
| `Production` | Total production for the crop |
| `Yield` | Yield value for the crop |
| `Annual_Rainfall` | Annual rainfall associated with the crop/state/year row |
| `Fertilizer` | Fertilizer input estimate |
| `Pesticide` | Pesticide input estimate |
| `avg_modal_price` | Average annual modal market price; may be missing in this file |
| `median_modal_price` | Median annual modal market price; may be missing |
| `min_price` | Lowest observed market price after yearly aggregation; may be missing |
| `max_price` | Highest observed market price after yearly aggregation; may be missing |
| `modal_price_std` | Standard deviation of modal prices; may be missing |
| `price_spread` | Difference between `max_price` and `min_price`; may be missing |
| `price_record_count` | Number of price records used for aggregation; may be missing |
| `market_count` | Number of unique markets contributing price data; may be missing |
| `district_count` | Number of unique districts contributing price data; may be missing |
| `price_available` | `1` if price data was matched, otherwise `0` |
| `Production_lag_1` | Previous available year's production for same state and crop; may be missing for first years |
| `Yield_lag_1` | Previous available year's yield for same state and crop; may be missing for first years |
| `Area_lag_1` | Previous available year's area for same state and crop; may be missing for first years |
| `avg_modal_price_lag_1` | Previous available year's average modal price; may be missing |
| `avg_modal_price_roll_3` | Previous 3-year rolling average of `avg_modal_price`; may be missing |
| `Production_roll_3` | Previous 3-year rolling average of `Production`; may be missing |
| `target_available` | `1` if `avg_modal_price` exists, otherwise `0` |
| `avg_modal_price_was_missing` | `1` if `avg_modal_price` was originally missing before filling |
| `avg_modal_price_filled` | Filled version of `avg_modal_price` |
| `median_modal_price_was_missing` | `1` if `median_modal_price` was originally missing before filling |
| `median_modal_price_filled` | Filled version of `median_modal_price` |
| `min_price_was_missing` | `1` if `min_price` was originally missing before filling |
| `min_price_filled` | Filled version of `min_price` |
| `max_price_was_missing` | `1` if `max_price` was originally missing before filling |
| `max_price_filled` | Filled version of `max_price` |
| `modal_price_std_was_missing` | `1` if `modal_price_std` was originally missing before filling |
| `modal_price_std_filled` | Filled version of `modal_price_std` |
| `price_spread_was_missing` | `1` if `price_spread` was originally missing before filling |
| `price_spread_filled` | Filled version of `price_spread` |
| `Production_lag_1_was_missing` | `1` if `Production_lag_1` was originally missing before filling |
| `Production_lag_1_filled` | Filled version of `Production_lag_1` |
| `Yield_lag_1_was_missing` | `1` if `Yield_lag_1` was originally missing before filling |
| `Yield_lag_1_filled` | Filled version of `Yield_lag_1` |
| `Area_lag_1_was_missing` | `1` if `Area_lag_1` was originally missing before filling |
| `Area_lag_1_filled` | Filled version of `Area_lag_1` |
| `avg_modal_price_lag_1_was_missing` | `1` if `avg_modal_price_lag_1` was originally missing before filling |
| `avg_modal_price_lag_1_filled` | Filled version of `avg_modal_price_lag_1` |
| `avg_modal_price_roll_3_was_missing` | `1` if `avg_modal_price_roll_3` was originally missing before filling |
| `avg_modal_price_roll_3_filled` | Filled version of `avg_modal_price_roll_3` |
| `Production_roll_3_was_missing` | `1` if `Production_roll_3` was originally missing before filling |
| `Production_roll_3_filled` | Filled version of `Production_roll_3` |
| `price_record_count_was_missing` | `1` if `price_record_count` was originally missing before filling |
| `price_record_count_filled` | Filled version of `price_record_count`; missing values filled with `0` |
| `market_count_was_missing` | `1` if `market_count` was originally missing before filling |
| `market_count_filled` | Filled version of `market_count`; missing values filled with `0` |
| `district_count_was_missing` | `1` if `district_count` was originally missing before filling |
| `district_count_filled` | Filled version of `district_count`; missing values filled with `0` |

## 2. price_modeling_train_2001_2020.csv

### Purpose

This is the training-only CSV for price prediction.

It is created from `modeling_table_2001_2020.csv` by keeping only rows where the target price exists:

```text
target_available = 1
avg_modal_price is not missing
```

Use this file for:

```text
Training machine learning models
Testing machine learning models
Predicting avg_modal_price
Regression experiments
Feature importance analysis
```

### Shape

```text
Rows: 1,199
Columns: 59
Crops: 12
States: 11
Years: 2001-2019
```

### Important Point

In this file, every row has a real target value:

```text
avg_modal_price is available for every row
target_available = 1 for every row
```

This is the file to use for supervised machine learning.

### Column Meanings for price_modeling_train_2001_2020.csv

Most columns mean the same thing as in the full modeling table, but in this file the target price is always available.

| Column | Meaning |
|---|---|
| `State` | State used as an input feature; should be encoded as categorical data |
| `Crop` | Crop used as an input feature; should be encoded as categorical data |
| `Commodity` | Matched price commodity name; usually not needed if `Crop` is already used |
| `crop_key` | Internal merge key; usually not used as a model feature |
| `Year` | Year of observation; can be used as a time feature |
| `Season` | Crop season; can be used as a categorical feature |
| `Area` | Cultivated area; model input feature |
| `Production` | Total production; model input feature |
| `Yield` | Yield; model input feature |
| `Annual_Rainfall` | Annual rainfall; model input feature |
| `Fertilizer` | Fertilizer input estimate; model input feature |
| `Pesticide` | Pesticide input estimate; model input feature |
| `avg_modal_price` | Main target column to predict |
| `median_modal_price` | Same-year price summary; avoid as predictor when target is `avg_modal_price` |
| `min_price` | Same-year price summary; avoid as predictor for first price model |
| `max_price` | Same-year price summary; avoid as predictor for first price model |
| `modal_price_std` | Same-year price volatility; avoid as predictor for first price model |
| `price_spread` | Same-year price spread; avoid as predictor for first price model |
| `price_record_count` | Number of records used to calculate price; optional control feature |
| `market_count` | Number of markets contributing price data; optional control feature |
| `district_count` | Number of districts contributing price data; optional control feature |
| `price_available` | Always `1` in this training file |
| `Production_lag_1` | Previous available year's production; original version may contain blanks |
| `Yield_lag_1` | Previous available year's yield; original version may contain blanks |
| `Area_lag_1` | Previous available year's area; original version may contain blanks |
| `avg_modal_price_lag_1` | Previous available year's average modal price; original version may contain blanks |
| `avg_modal_price_roll_3` | Previous 3-year rolling average price; original version may contain blanks |
| `Production_roll_3` | Previous 3-year rolling average production; original version may contain blanks |
| `target_available` | Always `1` in this training file |
| `avg_modal_price_was_missing` | Always `0` in this training file because target rows were filtered |
| `avg_modal_price_filled` | Filled version of target; avoid using as predictor for `avg_modal_price` |
| `median_modal_price_was_missing` | Flag showing whether `median_modal_price` was originally missing |
| `median_modal_price_filled` | Filled version of `median_modal_price`; avoid as predictor for first model |
| `min_price_was_missing` | Flag showing whether `min_price` was originally missing |
| `min_price_filled` | Filled version of `min_price`; avoid as predictor for first model |
| `max_price_was_missing` | Flag showing whether `max_price` was originally missing |
| `max_price_filled` | Filled version of `max_price`; avoid as predictor for first model |
| `modal_price_std_was_missing` | Flag showing whether `modal_price_std` was originally missing |
| `modal_price_std_filled` | Filled version of `modal_price_std`; avoid as predictor for first model |
| `price_spread_was_missing` | Flag showing whether `price_spread` was originally missing |
| `price_spread_filled` | Filled version of `price_spread`; avoid as predictor for first model |
| `Production_lag_1_was_missing` | Useful model feature indicating whether lagged production was imputed |
| `Production_lag_1_filled` | Use this instead of `Production_lag_1` for modeling |
| `Yield_lag_1_was_missing` | Useful model feature indicating whether lagged yield was imputed |
| `Yield_lag_1_filled` | Use this instead of `Yield_lag_1` for modeling |
| `Area_lag_1_was_missing` | Useful model feature indicating whether lagged area was imputed |
| `Area_lag_1_filled` | Use this instead of `Area_lag_1` for modeling |
| `avg_modal_price_lag_1_was_missing` | Useful model feature indicating whether lagged price was imputed |
| `avg_modal_price_lag_1_filled` | Use this as previous-year price feature |
| `avg_modal_price_roll_3_was_missing` | Useful model feature indicating whether rolling price was imputed |
| `avg_modal_price_roll_3_filled` | Use this as previous-price-trend feature |
| `Production_roll_3_was_missing` | Useful model feature indicating whether rolling production was imputed |
| `Production_roll_3_filled` | Use this as previous-production-trend feature |
| `price_record_count_was_missing` | Flag showing whether record count was originally missing |
| `price_record_count_filled` | Optional control feature; missing values filled with `0` |
| `market_count_was_missing` | Flag showing whether market count was originally missing |
| `market_count_filled` | Optional control feature; missing values filled with `0` |
| `district_count_was_missing` | Flag showing whether district count was originally missing |
| `district_count_filled` | Optional control feature; missing values filled with `0` |

## Source Data

The files were built from:

```text
datasets/production/Horticulture.xlsx
datasets/price/2001.csv through datasets/price/2020.csv
```

Production data was yearly crop-level data. Price data was daily market-level data, so price records were aggregated to annual level before merging.

## Crop Coverage

Both files include these 12 horticulture crops:

```text
Banana
Black pepper
Coconut
Coriander
Dry Chillies
Garlic
Ginger
Onion
Potato
Sweet potato
Tapioca
Turmeric
```

These crops were removed because they had no matched price records:

```text
Arecanut
Cardamom
Cashewnut
```

## Merge Level

The data was merged at:

```text
State + crop_key + Year
```

`crop_key` standardizes crop names from production and commodity names from price data.

## Missing Value Treatment

Missing values were handled in:

```text
scripts/05_prepare_modeling_table.py
```

For price and lag features, missing values were filled in this order:

```text
1. Median of same State + Crop
2. Median of same Crop
3. Median of same State
4. Overall median
```

For count columns:

```text
price_record_count
market_count
district_count
```

missing values were filled with:

```text
0
```

Original columns were kept. Filled columns were added separately with `_filled`.

## Recommended Training Setup

Use this file:

```text
price_modeling_train_2001_2020.csv
```

Target:

```text
avg_modal_price
```

Recommended first model features:

```text
State
Crop
Year
Season
Area
Production
Yield
Annual_Rainfall
Fertilizer
Pesticide
Production_lag_1_filled
Yield_lag_1_filled
Area_lag_1_filled
avg_modal_price_lag_1_filled
avg_modal_price_roll_3_filled
Production_roll_3_filled
Production_lag_1_was_missing
Yield_lag_1_was_missing
Area_lag_1_was_missing
avg_modal_price_lag_1_was_missing
avg_modal_price_roll_3_was_missing
Production_roll_3_was_missing
```

Avoid these as predictors when predicting `avg_modal_price`:

```text
median_modal_price
min_price
max_price
modal_price_std
price_spread
avg_modal_price_filled
median_modal_price_filled
min_price_filled
max_price_filled
modal_price_std_filled
price_spread_filled
```

Reason: these are same-year price summaries and can cause data leakage.

## Assumptions

1. `avg_modal_price` is treated as the annual representative price.
2. Daily mandi prices were aggregated to yearly state-crop level.
3. Crop and commodity names represent the same crop after standardization.
4. The dataset is state-level annual data, not district-level forecasting data.
5. Previous-year lag features are valid because they are known before the current year.
6. Same-year production features are included. For strict future forecasting, use only features known before prediction time.

## Suggested Models

Start with:

```text
Linear Regression
Random Forest Regressor
Gradient Boosting Regressor
```

Evaluation metrics:

```text
MAE
RMSE
R2 score
```

