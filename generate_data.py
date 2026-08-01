"""
Generate a realistic 5,000-row synthetic Telecom Customer dataset.
Churn probability is built from realistic business logic (contract type,
tenure, payment method, monthly charges, support calls) so the resulting
patterns are analyzable and the ML model has genuine signal to learn from.
"""

import numpy as np
import pandas as pd

np.random.seed(42)
N = 5000

customer_id = [f"CUST-{100000+i}" for i in range(N)]

genders = np.random.choice(["Male", "Female"], N)
senior_citizen = np.random.choice([0, 1], N, p=[0.84, 0.16])
partner = np.random.choice(["Yes", "No"], N, p=[0.48, 0.52])
dependents = np.random.choice(["Yes", "No"], N, p=[0.30, 0.70])

# Tenure in months (skewed - more newer customers, long tail of loyal ones)
tenure = np.random.exponential(scale=24, size=N).astype(int)
tenure = np.clip(tenure, 0, 72)

contract = np.random.choice(
    ["Month-to-Month", "One Year", "Two Year"], N, p=[0.55, 0.25, 0.20]
)

payment_method = np.random.choice(
    ["Electronic Check", "Mailed Check", "Bank Transfer (Auto)", "Credit Card (Auto)"],
    N, p=[0.34, 0.19, 0.24, 0.23]
)

internet_service = np.random.choice(
    ["Fiber Optic", "DSL", "No"], N, p=[0.44, 0.34, 0.22]
)

phone_service = np.random.choice(["Yes", "No"], N, p=[0.90, 0.10])

multiple_lines = np.where(
    phone_service == "No", "No Phone Service",
    np.random.choice(["Yes", "No"], N, p=[0.42, 0.58])
)

def addon(p_yes=0.35):
    return np.random.choice(["Yes", "No"], N, p=[p_yes, 1 - p_yes])

online_security = np.where(internet_service == "No", "No Internet Service", addon(0.30))
online_backup = np.where(internet_service == "No", "No Internet Service", addon(0.35))
device_protection = np.where(internet_service == "No", "No Internet Service", addon(0.34))
tech_support = np.where(internet_service == "No", "No Internet Service", addon(0.29))
streaming_tv = np.where(internet_service == "No", "No Internet Service", addon(0.38))
streaming_movies = np.where(internet_service == "No", "No Internet Service", addon(0.39))

paperless_billing = np.random.choice(["Yes", "No"], N, p=[0.59, 0.41])

# Monthly charges depend on services subscribed
base_charge = np.random.normal(45, 8, N)
internet_charge = np.where(internet_service == "Fiber Optic", 35,
                    np.where(internet_service == "DSL", 18, 0))
addon_count = (
    (online_security == "Yes").astype(int) + (online_backup == "Yes").astype(int) +
    (device_protection == "Yes").astype(int) + (tech_support == "Yes").astype(int) +
    (streaming_tv == "Yes").astype(int) + (streaming_movies == "Yes").astype(int)
)
monthly_charges = np.round(base_charge + internet_charge + addon_count * 6.5 + np.random.normal(0, 4, N), 2)
monthly_charges = np.clip(monthly_charges, 18, 145)

total_charges = np.round(monthly_charges * tenure + np.random.normal(0, 50, N), 2)
total_charges = np.clip(total_charges, 0, None)

city = np.random.choice(
    ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad"],
    N, p=[0.16, 0.15, 0.16, 0.12, 0.11, 0.11, 0.10, 0.09]
)

support_calls_last_6mo = np.random.poisson(1.4, N)
support_calls_last_6mo = np.clip(support_calls_last_6mo, 0, 12)

age_group = pd.cut(
    18 + np.random.exponential(15, N).astype(int),
    bins=[0, 25, 35, 45, 55, 65, 100],
    labels=["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
)

# ---- Build churn probability from realistic business drivers ----
logit = (
    -3.35
    + 1.35 * (contract == "Month-to-Month")
    + 0.35 * (contract == "One Year")
    + 0.00 * (contract == "Two Year")
    + 0.85 * (payment_method == "Electronic Check")
    - 0.55 * (payment_method == "Bank Transfer (Auto)")
    - 0.60 * (payment_method == "Credit Card (Auto)")
    + 0.55 * (internet_service == "Fiber Optic")
    - 0.30 * (internet_service == "No")
    - 0.028 * tenure
    + 0.014 * monthly_charges
    + 0.22 * support_calls_last_6mo
    - 0.45 * (tech_support == "Yes")
    - 0.35 * (online_security == "Yes")
    + 0.30 * (paperless_billing == "Yes")
    - 0.25 * (partner == "Yes")
    - 0.20 * (dependents == "Yes")
    + 0.20 * senior_citizen
    + np.random.normal(0, 0.55, N)
)
prob_churn = 1 / (1 + np.exp(-logit))
churn = (np.random.rand(N) < prob_churn).astype(int)
churn_label = np.where(churn == 1, "Yes", "No")

df = pd.DataFrame({
    "CustomerID": customer_id,
    "Gender": genders,
    "SeniorCitizen": senior_citizen,
    "Partner": partner,
    "Dependents": dependents,
    "AgeGroup": age_group.astype(str),
    "City": city,
    "Tenure": tenure,
    "PhoneService": phone_service,
    "MultipleLines": multiple_lines,
    "InternetService": internet_service,
    "OnlineSecurity": online_security,
    "OnlineBackup": online_backup,
    "DeviceProtection": device_protection,
    "TechSupport": tech_support,
    "StreamingTV": streaming_tv,
    "StreamingMovies": streaming_movies,
    "Contract": contract,
    "PaperlessBilling": paperless_billing,
    "PaymentMethod": payment_method,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges,
    "SupportCallsLast6Months": support_calls_last_6mo,
    "Churn": churn_label,
})

# Inject realistic data quality issues (so cleaning step is genuine, not fake)
missing_idx = np.random.choice(df.index, 45, replace=False)
df.loc[missing_idx, "TotalCharges"] = np.nan

dup_rows = df.sample(15, random_state=1)
df = pd.concat([df, dup_rows], ignore_index=True)

blank_idx = np.random.choice(df.index, 20, replace=False)
df.loc[blank_idx, "Gender"] = df.loc[blank_idx, "Gender"].replace({"Male": " Male ", "Female": "female"})

df.to_csv("/home/claude/telecom-churn-analytics/data/telecom_churn_raw.csv", index=False)
print(f"Generated {len(df)} rows. Churn rate: {(df['Churn']=='Yes').mean():.2%}")
print(df.head())
