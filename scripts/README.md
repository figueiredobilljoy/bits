# Master Table Pipeline

This pipeline builds the first master table from:

- `datasets/production/Horticulture.xlsx`
- `datasets/price/2001.csv` through `datasets/price/2020.csv`

The merge level is:

```text
State + crop/commodity + Year
```

Run in order:

```powershell
python scripts/01_clean_production.py
python scripts/02_aggregate_prices.py
python scripts/03_build_master_table.py
python scripts/04_missing_value_audit.py
python scripts/05_prepare_modeling_table.py
```

Outputs:

```text
data/processed/clean_production_2001_2020.csv
data/processed/annual_prices_2001_2020.csv
data/processed/master_table_2001_2020.csv
data/processed/missing_summary.csv
data/processed/missing_by_crop.csv
data/processed/missing_by_state.csv
data/processed/modeling_table_2001_2020.csv
data/processed/price_modeling_train_2001_2020.csv
```

The master table is filtered to these price-supported horticulture crops:

```text
Banana, Black pepper, Coconut, Coriander, Dry Chillies, Garlic,
Ginger, Onion, Potato, Sweet potato, Tapioca, Turmeric
```

The current processed table uses these states:

```text
Uttar Pradesh, Tamil Nadu, Madhya Pradesh, Maharashtra, Gujarat,
West Bengal, Karnataka, Haryana, Himachal Pradesh, Odisha,
Kerala
```

Extended analytics and dashboard steps:

```powershell
python scripts/01_clean_and_preprocess.py
python scripts/02_transform_and_engineer.py
python scripts/03_exploratory_data_analysis.py
python scripts/04_train_ml_models.py
python scripts/build_dashboard_data.py
```
