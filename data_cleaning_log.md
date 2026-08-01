# Data Cleaning Log
**Raw records loaded:** 5015
## 1. Duplicate Records
- Found 15 duplicate CustomerIDs.
- **Why it matters:** duplicate customers would double-count revenue and churn in every downstream KPI (e.g. inflating 'customers lost' and skewing churn rate), causing leadership to over- or under-react.
- Action: kept first occurrence, dropped rest.
## 2. Missing Values
- Total missing cells found: 66
- `TotalCharges` missing in 45 rows (mostly customers with 0 tenure — i.e. brand-new customers billed for a partial first month).
- **Why it matters:** leaving these blank would silently exclude new customers from revenue analysis, understating recent revenue trends.
- Action: imputed as `MonthlyCharges x Tenure`, a standard, explainable business estimate.
## 3. Inconsistent Categories
- `Gender` had inconsistent casing/whitespace: ['Male', 'Female', ' Male ', 'female']
- **Why it matters:** inconsistent labels (`' Male '`, `'female'`) fragment groupby aggregations — e.g. 'Male' and ' Male ' would be counted as two different segments, silently corrupting gender-based churn analysis.
- Action: standardized to trimmed Title Case: ['Male', 'Female']
## 4. Data Types
- Enforced numeric types on `SeniorCitizen`, `Tenure`, `MonthlyCharges`, `TotalCharges`.
- **Why it matters:** if these load as text/object, SQL aggregations (SUM, AVG) and ML models fail silently or produce wrong results.
## 5. Outlier Check (MonthlyCharges)
- IQR bounds: [17.46, 138.16]
- Outliers detected: 0
- **Why it matters:** telecom monthly charges legitimately range widely by plan (basic phone-only vs. full fiber+streaming bundle), so these are real customers, not data errors. Action: **kept** — removing them would hide our highest-value customers, exactly the segment leadership cares most about protecting.

**Final clean record count:** 5000
