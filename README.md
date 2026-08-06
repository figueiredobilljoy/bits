# Horticulture Price Modeling Project

This project builds a state-crop-year modeling dataset for Indian horticulture crop price prediction.

## What The Pipeline Does

The pipeline:

1. Cleans horticulture production data.
2. Aggregates daily mandi price CSVs to annual state-crop price features.
3. Merges production and price data into a master table.
4. Filters to price-supported horticulture crops.
5. Creates modeling-ready tables with filled features and missing-value flags.

## Main Outputs

```text
data/processed/master_table_2001_2020.csv
data/processed/modeling_table_2001_2020.csv
data/processed/price_modeling_train_2001_2020.csv
data/processed/price_modeling_train_2001_2020.md
```

Use this file for model training:

```text
data/processed/price_modeling_train_2001_2020.csv
```

Target column:

```text
avg_modal_price
```

## Scripts

Run the pipeline in this order:

```powershell
python scripts/01_clean_production.py
python scripts/02_aggregate_prices.py
python scripts/03_build_master_table.py
python scripts/04_missing_value_audit.py
python scripts/05_prepare_modeling_table.py
```

## Data Note

The raw `datasets/` folder is ignored by Git because the source files are large. Keep raw data locally or store it externally.

