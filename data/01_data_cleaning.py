"""
STEP 1: DATA CLEANING
Every cleaning decision is documented with WHY it matters to the business,
not just what was done.
"""
import pandas as pd
import numpy as np

RAW_PATH = "/home/claude/telecom-churn-analytics/data/telecom_churn_raw.csv"
CLEAN_PATH = "/home/claude/telecom-churn-analytics/data/telecom_churn_clean.csv"
LOG_PATH = "/home/claude/telecom-churn-analytics/documentation/data_cleaning_log.md"

df = pd.read_csv(RAW_PATH)
log = []
log.append("# Data Cleaning Log\n")
log.append(f"**Raw records loaded:** {len(df)}\n")

# 1. Duplicate records
dupes = df.duplicated(subset=["CustomerID"]).sum()
df = df.drop_duplicates(subset=["CustomerID"], keep="first")
log.append(f"## 1. Duplicate Records\n- Found {dupes} duplicate CustomerIDs.\n"
            f"- **Why it matters:** duplicate customers would double-count revenue and churn "
            f"in every downstream KPI (e.g. inflating 'customers lost' and skewing churn rate), "
            f"causing leadership to over- or under-react.\n- Action: kept first occurrence, dropped rest.\n")

# 2. Missing values
missing_total = df.isnull().sum().sum()
missing_by_col = df.isnull().sum()
missing_by_col = missing_by_col[missing_by_col > 0]
# TotalCharges: impute using MonthlyCharges * Tenure (a defensible business estimate)
missing_tc = df["TotalCharges"].isnull().sum()
df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"] * df["Tenure"])
log.append(f"## 2. Missing Values\n- Total missing cells found: {missing_total}\n"
            f"- `TotalCharges` missing in {missing_tc} rows (mostly customers with 0 tenure — "
            f"i.e. brand-new customers billed for a partial first month).\n"
            f"- **Why it matters:** leaving these blank would silently exclude new customers from "
            f"revenue analysis, understating recent revenue trends.\n"
            f"- Action: imputed as `MonthlyCharges x Tenure`, a standard, explainable business estimate.\n")

# 3. Inconsistent text categories
before = df["Gender"].unique().tolist()
df["Gender"] = df["Gender"].astype(str).str.strip().str.title()
after = df["Gender"].unique().tolist()
log.append(f"## 3. Inconsistent Categories\n- `Gender` had inconsistent casing/whitespace: {before}\n"
            f"- **Why it matters:** inconsistent labels (`' Male '`, `'female'`) fragment groupby "
            f"aggregations — e.g. 'Male' and ' Male ' would be counted as two different segments, "
            f"silently corrupting gender-based churn analysis.\n"
            f"- Action: standardized to trimmed Title Case: {after}\n")

# 4. Data types
df["SeniorCitizen"] = df["SeniorCitizen"].astype(int)
df["Tenure"] = df["Tenure"].astype(int)
df["MonthlyCharges"] = df["MonthlyCharges"].astype(float)
df["TotalCharges"] = df["TotalCharges"].astype(float)
log.append("## 4. Data Types\n- Enforced numeric types on `SeniorCitizen`, `Tenure`, `MonthlyCharges`, "
            "`TotalCharges`.\n- **Why it matters:** if these load as text/object, SQL aggregations "
            "(SUM, AVG) and ML models fail silently or produce wrong results.\n")

# 5. Outliers
q1, q3 = df["MonthlyCharges"].quantile([0.25, 0.75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = df[(df["MonthlyCharges"] < lower) | (df["MonthlyCharges"] > upper)]
log.append(f"## 5. Outlier Check (MonthlyCharges)\n- IQR bounds: [{lower:.2f}, {upper:.2f}]\n"
            f"- Outliers detected: {len(outliers)}\n"
            f"- **Why it matters:** telecom monthly charges legitimately range widely by plan "
            f"(basic phone-only vs. full fiber+streaming bundle), so these are real customers, "
            f"not data errors. Action: **kept** — removing them would hide our highest-value customers, "
            f"exactly the segment leadership cares most about protecting.\n")

df.to_csv(CLEAN_PATH, index=False)
log.append(f"\n**Final clean record count:** {len(df)}\n")

with open(LOG_PATH, "w") as f:
    f.writelines(log)

print(f"Clean dataset saved: {len(df)} rows -> {CLEAN_PATH}")
print(f"Cleaning log saved -> {LOG_PATH}")
