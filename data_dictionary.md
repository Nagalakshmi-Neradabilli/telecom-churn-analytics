# Data Dictionary — Telecom Customer Churn Dataset

| Column | Business Meaning | Type | Possible Values | Business Importance |
|---|---|---|---|---|
| CustomerID | Unique customer identifier (Primary Key) | Text | CUST-100000... | Joins across all tables/queries |
| Gender | Customer gender | Text | Male, Female | Demographic segmentation |
| SeniorCitizen | Whether customer is 65+ | Binary | 0, 1 | Age-based retention targeting |
| Partner | Has a partner/spouse | Text | Yes, No | Household stability signal, correlates with churn |
| Dependents | Has dependents | Text | Yes, No | Household stability signal |
| AgeGroup | Age bracket | Text | 18-25 ... 65+ | Campaign targeting |
| City | Customer's city | Text | 8 major cities | Regional retention planning |
| Tenure | Months as a customer | Integer | 0-72 | Strongest lifecycle/loyalty signal |
| PhoneService | Has phone service | Text | Yes, No | Product mix |
| MultipleLines | Has multiple phone lines | Text | Yes, No, No Phone Service | Product mix |
| InternetService | Internet plan type | Text | Fiber Optic, DSL, No | Major revenue and churn driver |
| OnlineSecurity / OnlineBackup / DeviceProtection / TechSupport | Add-on services | Text | Yes, No, No Internet Service | Engagement/stickiness signal |
| StreamingTV / StreamingMovies | Entertainment add-ons | Text | Yes, No, No Internet Service | Engagement signal |
| Contract | Contract commitment | Text | Month-to-Month, One Year, Two Year | **Top churn driver** |
| PaperlessBilling | Billing format | Text | Yes, No | Minor churn correlation |
| PaymentMethod | How customer pays | Text | Electronic Check, Mailed Check, Bank Transfer (Auto), Credit Card (Auto) | **Top churn driver** |
| MonthlyCharges | Current monthly bill ($) | Float | 18-145 | Revenue + risk sizing |
| TotalCharges | Lifetime billed amount ($) | Float | 0+ | CLV calculation |
| SupportCallsLast6Months | Support call volume | Integer | 0-12 | Service-quality churn signal |
| Churn | Did the customer leave? (Target variable) | Text | Yes, No | What we are predicting |

**Data Quality Issues Found & Fixed:** duplicate CustomerIDs, missing TotalCharges (new customers), inconsistent Gender text casing/whitespace — see `data_cleaning_log.md` for full documentation.
