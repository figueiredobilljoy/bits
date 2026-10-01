# Horticulture Price & Production Analytics Report (2001-2019)

## Executive Summary

This study presents a multi-dimensional data science investigation into Indian horticulture economics across 11 primary agricultural states and 12 price-supported horticulture crops over a 19-year processed timeline (2001-2019). By integrating agricultural production data with mandi modal market prices, we analyze supply-demand elasticity, spatial-temporal price variations, environmental input impacts, and machine learning price predictability.

---

## 1. Scope & Dataset Overview

- **Time Horizon**: 2001 to 2019 (19 Annual Cycles)
- **Geographic Coverage**: 11 Major States (*Uttar Pradesh, Tamil Nadu, Madhya Pradesh, Maharashtra, Gujarat, West Bengal, Karnataka, Haryana, Himachal Pradesh, Odisha, Kerala*)
- **Crop Categories**: 12 Horticulture Commodities (*Banana, Black pepper, Coconut, Coriander, Dry Chillies, Garlic, Ginger, Onion, Potato, Sweet potato, Tapioca, Turmeric*)
- **Total Master Observations**: 1,444 state-crop-year records across 58 engineered features.

---

## 2. Statistical Correlation & Key Drivers Analysis

The correlation analysis uncovers strong relationships among price trajectories, temporal lags, yield efficiency, and agricultural input factors:

| Feature Pair | Pearson Correlation ($r$) | Spearman Correlation ($\rho$) | Analytical Insight |
| :--- | :---: | :---: | :--- |
| `avg_modal_price` vs `avg_modal_price_lag_1` | **+0.0415** | **+0.9094** | Rank-order price persistence is strong, while the Pearson relationship is weakened by commodity-level scale differences and outliers. |
| `avg_modal_price` vs `modal_price_std` | **+0.3442** | **+0.7208** | High-value crops generally experience higher absolute intra-year price dispersion. |
| `Yield` vs `Fertilizer` | **+0.4850** | **+0.3114** | Fertilizer input has a positive association with yield in the processed panel. |
| `Yield` vs `Pesticide` | **+0.4605** | **+0.3113** | Crop protection input is positively associated with yield. |
| `avg_modal_price` vs `Production` | **+0.1690** | **-0.3800** | Volume and price move differently depending on whether absolute levels or rank-order comparisons are used. |
| `avg_modal_price` vs `Annual_Rainfall` | **+0.0940** | **+0.1495** | Rainfall has only a weak direct association with modal market prices. |

---

## 3. State & Crop Dynamics

### Crop Price & Volatility Spectrum
1. **High-Value / High-Volatility Commodities**:
   - **Black Pepper & Garlic**: Display average modal prices exceeding ₹5,000–₹12,000 / Quintal with price volatility indices exceeding 0.35.
   - **Onion & Dry Chillies**: High price sensitivity due to seasonal storage constraints and extreme climate sensitivity.
2. **Bulk Production Commodities**:
   - **Potato & Banana**: Consistently lower modal price bounds (₹800 – ₹1,800 / Quintal) with massive annual production volume (exceeding 25 Million Tonnes combined).

### Regional Production Dominance
- **Uttar Pradesh & West Bengal**: Lead total volume output driven by massive Potato and Banana acreage.
- **Tamil Nadu & Kerala**: Lead perennial plantation crops (Coconut, Black Pepper, Tapioca) with distinct price stability metrics.

---

## 4. Machine Learning Predictive Modeling Results

Four regression algorithms were evaluated using a strict **temporal train/test split** (Train: 2001-2016, 1,191 samples; Test: 2017-2019 out-of-sample holdout, 253 samples).

| Model Algorithm | Out-of-Sample $R^2$ | MAE (₹/Quintal) | RMSE (₹/Quintal) | MAPE (%) | Performance Evaluation |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Linear Regression** | -1.9055 | ₹5,767 | ₹10,181 | 344.8% | Underperforms due to extreme non-linear price scale differences across crops. |
| **Ridge Regression ($\alpha=10$)** | -1.5519 | ₹5,501 | ₹9,541 | 328.9% | Penalization reduces variance but fails to model non-linear crop interactions. |
| **Gradient Boosting** | **0.5593** | ₹1,399 | ₹3,965 | 37.7% | Strong out-of-sample generalizability across diverse crop regimes. |
| **Random Forest Regressor** | **0.6529** | **₹1,264** | **₹3,519** | **34.8%** | **Best Overall Model**; captures complex crop-state interaction splits. |

### Top 5 Price Importance Drivers
1. **`Area_lag_1`** (34.9% Importance Weight)
2. **`avg_modal_price_lag_2`** (13.7% Importance Weight)
3. **`avg_modal_price_lag_1`** (10.1% Importance Weight)
4. **`Area`** (7.5% Importance Weight)
5. **`log_Area`** (6.4% Importance Weight)

---

## 5. Strategic Recommendations

1. **Price Stabilization Reserves**: Establish regional buffer stocks for high-volatility commodities (Garlic, Onion) during forecasted high-rainfall anomaly years.
2. **Predictive Mandi Intelligence**: Deploy the real-time ML Price Simulator at state mandi boards to advise farmers on expected harvest prices 1-2 seasons in advance.
3. **Precision Input Support**: Enhance targeted fertilizer and pesticide distribution in low-yield states (e.g. Odisha, Himachal Pradesh) to boost overall horticulture productivity.
