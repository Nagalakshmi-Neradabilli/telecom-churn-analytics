# Telecom Customer Churn Analytics — End-to-End Business Solution

## Business Summary

A telecom provider is experiencing a **~21% customer churn rate**, translating to significant recurring
monthly revenue loss. Leadership needed to know which customers were most likely to leave, why they
were leaving, and what specific retention actions would protect the most revenue. This project builds
an end-to-end analytics solution — **SQL → Python → Machine Learning → Business Recommendations** —
to answer those questions with data, not guesswork.

**Bottom line finding:** Churn is concentrated in month-to-month contract customers who pay by
Electronic Check and are within their first 12 months — and it's disproportionately hitting the
company's highest-revenue Fiber Optic customers. Three specific, actionable levers (contract
conversion, autopay migration, and early-tenure onboarding) could meaningfully reduce it.

## Business Questions Answered

1. How healthy is our customer base right now? *(Executive Summary)*
2. Which contract type is bleeding us customers? *(Segmentation)*
3. Where are we losing the most revenue? *(Revenue at Risk)*
4. Who is likely to leave next, and how confident are we? *(Prediction)*
5. What's actually causing the churn? *(Driver Analysis)*
6. What should leadership do next, and what will it save? *(Action Center)*

## Methodology

| Stage | Tool | Output |
|---|---|---|
| Data generation (5,000 records, realistic business logic + intentional data quality issues) | Python (pandas, numpy) | `data/telecom_churn_raw.csv` |
| Data cleaning (duplicates, missing values, inconsistent categories, type fixes) | Python | `data/telecom_churn_clean.csv`, `documentation/data_cleaning_log.md` |
| SQL business analysis (10 queries: CTEs, window functions, views, CASE logic) | SQLite | `sql/churn_business_queries.sql`, `documentation/sql_business_insights.md` |
| EDA (6 business-question-driven charts) | Python (matplotlib/seaborn) | `charts/01-06*.png` |
| Feature engineering (CLV, Revenue at Risk, Engagement Score, Risk Flags) | Python | Embedded in model script |
| Machine Learning (Logistic Regression + Random Forest, compared on Recall) | scikit-learn | `documentation/model_comparison_results.csv`, `charts/07-09*.png` |
| Risk-scored customer list | Python | `data/churn_risk_scores.csv` |
| Business recommendations with estimated revenue impact | — | `documentation/business_recommendations.md` |

## Key Findings

- **Contract type is the strongest lever:** Month-to-Month churn (28.1%) is 2.6x higher than Two-Year (10.7%)
- **Payment method matters almost as much:** Electronic Check churn (33.5%) is 3x higher than autopay methods (~11-13%)
- **Fiber Optic is highest revenue AND highest risk:** $59K/month in lost fiber revenue alone
- **The first 12 months are the danger zone:** churn drops from ~27% to ~9% after month 48
- **Support call volume is a leading indicator:** churn rate more than triples between 0 and 5+ support calls

## Model Performance

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression (selected) | 0.67 | 0.343 | **0.632** | 0.444 | 0.739 |
| Random Forest | 0.72 | 0.384 | 0.560 | 0.455 | 0.751 |

**Why Logistic Regression was selected despite lower accuracy:** Recall matters more than accuracy in
churn prediction — missing a real churner (false negative) costs the company a lost customer's full
lifetime value, while a false positive only costs a discretionary retention offer to a loyal customer.

## Top Churn Drivers (Feature Importance)

1. Payment Method
2. Monthly Charges
3. Contract Type
4. Tenure
5. Total Charges (CLV proxy)

## Project Structure

```
telecom-churn-analytics/
├── data/
│   ├── telecom_churn_raw.csv
│   ├── telecom_churn_clean.csv
│   ├── telecom_churn.db
│   └── churn_risk_scores.csv
├── sql/
│   └── churn_business_queries.sql
├── python/
│   ├── generate_data.py
│   ├── 01_data_cleaning.py
│   ├── 02_sql_analysis.py
│   ├── 03_eda_charts.py
│   └── 04_feature_engineering_and_model.py
├── charts/
│   └── 01-09 business-question PNG charts
├── documentation/
│   ├── data_dictionary.md
│   ├── data_cleaning_log.md
│   ├── sql_business_insights.md
│   ├── business_recommendations.md
│   ├── model_comparison_results.csv
│   └── feature_importance.csv
├── README.md
└── requirements.txt
```

## Limitations

- Dataset is synthetically generated with realistic business logic, not live production data — patterns
  are directional and demonstrate methodology, not literal company figures
- Model uses only structured account/service data; no external factors (competitor promotions, macro
  conditions) are included
- Recall of 63% means ~37% of actual churners are still missed — in production this model would be a
  prioritization tool for the retention team, not a fully automated decision system

## Future Improvements

- Add a customer sentiment/NPS feature if survey data becomes available
- Test XGBoost/LightGBM for potential recall improvement
- Build a live Power BI dashboard connected directly to the SQLite/production database with the
  6-page structure outlined in `documentation/business_recommendations.md`
- A/B test the recommended retention interventions and measure actual save rate

## Resume Bullets

- Built an end-to-end telecom customer churn analytics solution (SQL, Python, Machine Learning)
  on 5,000 customer records, identifying Payment Method, Contract Type, and Tenure as primary
  churn drivers
- Designed a recall-optimized Logistic Regression model (63.2% recall, 0.74 ROC-AUC) to
  proactively flag high-risk customers for retention outreach
- Quantified ~$148K/month in exposed revenue among active month-to-month customers and delivered
  6 data-backed retention recommendations with estimated business impact
