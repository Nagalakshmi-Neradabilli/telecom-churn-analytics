# Executive Action Center — Business Recommendations

**Overall churn rate: ~21%** | **Revenue currently exposed (active month-to-month customers): ~$148,000/month**

| # | Finding | Evidence | Recommended Action | KPI to Monitor | Estimated Impact |
|---|---|---|---|---|---|
| 1 | Month-to-Month customers churn far more than committed customers | 28.1% churn vs. 13.4% (One Year) and 10.7% (Two Year) | Launch a contract-upgrade incentive (e.g., 1 month free) for month-to-month customers past month 3 | % of M2M customers converted to annual | Converting 15% of M2M base could cut overall churn by ~4-5 pts |
| 2 | Electronic Check payers churn 3x more than autopay users | 33.5% churn vs. 11.2% (Credit Card Auto) / 13.0% (Bank Transfer Auto) | Offer a small recurring bill credit for enrolling in autopay | Autopay adoption rate | Est. $15K-20K/month in retained revenue if 20% of Electronic Check users switch |
| 3 | Fiber Optic customers are highest-revenue AND highest-churn segment | 28.4% churn, $93.43 avg monthly charge — losing ~$59K/month in fiber revenue alone | Create a dedicated white-glove retention track for Fiber customers (proactive check-ins, priority support) | Fiber churn rate, Fiber revenue retained | Largest single revenue-protection opportunity in the dataset |
| 4 | Churn is concentrated in the first 12 months | 27.5% (0-6mo) and 24.5% (7-12mo) vs. 9.2% (48+mo) | Build a structured 90-day onboarding program with proactive check-ins at day 30/60/90 | New-customer churn rate | Reducing early churn by 5 pts protects a disproportionate share of future CLV |
| 5 | Churn rises sharply with support call volume | 16.6% (0 calls) → 56.3% (6 calls) | Auto-flag any customer with 3+ support calls in 6 months for proactive retention outreach before they churn | Escalation-to-save rate | Early intervention on ~750 flagged customers |
| 6 | Two-Year contract customers have the highest lifetime value and lowest churn | $1,738 avg CLV, 10.7% churn — the "gold standard" segment | Study and replicate what keeps 2-year customers loyal (bundle mix, engagement) in retention offers for other segments | CLV by contract type | Informs which behaviors to incentivize company-wide |
| 7 | Model can rank customers by real-time churn risk | Logistic Regression: 63% recall, 0.74 ROC-AUC on held-out test data | Route the "High Risk" and "Critical Risk" customer list (163 of 1,000 test customers) directly to the retention team weekly | Save rate on contacted high-risk customers | Turns a reactive process into a proactive, prioritized one |

**Model selection note:** Logistic Regression was selected over Random Forest despite slightly lower accuracy (67% vs 72%) because it has meaningfully higher **recall** (63.2% vs 56.0%) — in churn prediction, missing an actual churner (false negative) costs the company a lost customer's full lifetime value, while a false positive only costs a discretionary retention offer to a loyal customer. Recall is the metric that matters here, not accuracy.

**Top 3 churn drivers (Random Forest feature importance):** Payment Method, Monthly Charges, Contract Type — together these three explain the majority of the model's predictive power, and all three are levers the business can directly influence.
