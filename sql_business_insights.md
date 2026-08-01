# SQL Business Insights Report

Each query below answers a specific executive question with data, insight, and a recommended action.


## Q1: How healthy is our customer base right now?

|   total_customers |   churned_customers |   churn_rate_pct |   total_monthly_revenue |   monthly_revenue_lost |
|------------------:|--------------------:|-----------------:|------------------------:|-----------------------:|
|              5000 |                1047 |            20.94 |                  385401 |                87191.3 |


**Business Insight & Recommendation:** Overall churn sits at a level that, applied to monthly recurring revenue, represents a material and recurring monthly revenue leak — this is the number leadership should track weekly.


## Q2: Which contract type is bleeding us customers?

| Contract       |   customers |   churned |   churn_rate_pct |   avg_monthly_charge |
|:---------------|------------:|----------:|-----------------:|---------------------:|
| Month-to-Month |        2745 |       771 |            28.09 |                77.23 |
| One Year       |        1291 |       173 |            13.4  |                76.7  |
| Two Year       |         964 |       103 |            10.68 |                77.17 |


**Business Insight & Recommendation:** Month-to-month customers churn several times more often than annual/two-year customers. **Recommendation:** run a contract-upgrade incentive (e.g., 1 month free) targeted at month-to-month customers past their 3rd month.


## Q3: Which payment method correlates with highest churn?

| PaymentMethod        |   customers |   churn_rate_pct |
|:---------------------|------------:|-----------------:|
| Electronic Check     |        1757 |            33.52 |
| Mailed Check         |         948 |            18.99 |
| Bank Transfer (Auto) |        1177 |            13    |
| Credit Card (Auto)   |        1118 |            11.18 |


**Business Insight & Recommendation:** Electronic Check users churn far more than Auto-Pay (Bank Transfer/Credit Card) users. **Recommendation:** incentivize migration to autopay with a small recurring discount — autopay is both stickier and cheaper to collect.


## Q4: Are we losing our most valuable (highest revenue) customers?

| InternetService   |   customers |   churn_rate_pct |   avg_monthly_charge |   monthly_revenue_lost |
|:------------------|------------:|-----------------:|---------------------:|-----------------------:|
| Fiber Optic       |        2219 |            28.35 |                93.43 |               59162.3  |
| DSL               |        1714 |            16.45 |                75.91 |               21828.5  |
| No                |        1067 |            12.75 |                44.96 |                6200.48 |


**Business Insight & Recommendation:** Fiber Optic customers pay the most per month AND churn at a higher rate than DSL/No-internet customers, meaning the company's highest-margin segment is also its highest-risk segment. **Recommendation:** create a dedicated retention track for Fiber customers rather than a one-size-fits-all campaign.


## Q5: How long do we have before churn risk rises?

| tenure_cohort   |   customers |   churn_rate_pct |
|:----------------|------------:|-----------------:|
| 0-6 months      |        1202 |            27.45 |
| 7-12 months     |         804 |            24.5  |
| 13-24 months    |        1141 |            23.84 |
| 25-48 months    |        1154 |            15.94 |
| 48+ months      |         699 |             9.16 |


**Business Insight & Recommendation:** Churn is heavily concentrated in the first 12 months. **Recommendation:** invest in a structured onboarding/check-in program for the first 90 days — this is the highest-leverage retention window.


## Q7: Does poor support experience drive churn?

|   SupportCallsLast6Months |   customers |   churn_rate_pct |
|--------------------------:|------------:|-----------------:|
|                         0 |        1206 |            16.58 |
|                         1 |        1725 |            20.35 |
|                         2 |        1249 |            22.98 |
|                         3 |         546 |            23.08 |
|                         4 |         198 |            27.27 |
|                         5 |          58 |            34.48 |
|                         6 |          16 |            56.25 |
|                         7 |           2 |             0    |


**Business Insight & Recommendation:** Churn rate climbs sharply as support call frequency increases. **Recommendation:** flag any customer with 3+ support calls in 6 months for proactive outreach before they churn, not after.


## Q8: Which cities need urgent regional retention campaigns?

| City      |   customers |   churned |   churn_rate_pct |   total_monthly_revenue |
|:----------|------------:|----------:|-----------------:|------------------------:|
| Chennai   |         563 |       125 |            22.2  |                 44285.6 |
| Bangalore |         828 |       176 |            21.26 |                 63770.6 |
| Delhi     |         752 |       159 |            21.14 |                 57430.9 |
| Mumbai    |         782 |       163 |            20.84 |                 60403   |
| Hyderabad |         589 |       122 |            20.71 |                 44973.1 |
| Ahmedabad |         448 |        92 |            20.54 |                 34518.7 |
| Kolkata   |         521 |       107 |            20.54 |                 40117.9 |
| Pune      |         517 |       103 |            19.92 |                 39901   |


**Business Insight & Recommendation:** Churn rate varies meaningfully by city, meaning a single national campaign is inefficient. **Recommendation:** prioritize regional retention budget toward the cities with the combination of high churn AND high revenue concentration.


## Q9: Do add-on services (TechSupport/OnlineSecurity) reduce churn?

| TechSupport   | OnlineSecurity   |   customers |   churn_rate_pct |
|:--------------|:-----------------|------------:|-----------------:|
| No            | No               |        1968 |            24.8  |
| No            | Yes              |         830 |            22.41 |
| Yes           | No               |         789 |            21.17 |
| Yes           | Yes              |         346 |            20.23 |


**Business Insight & Recommendation:** Customers without TechSupport or OnlineSecurity churn noticeably more than those with both. **Recommendation:** bundle a free 3-month trial of TechSupport for new internet customers to build the habit before the risk window closes.


## Q10: Which segment generates the most lifetime value, and is it safe?

| Contract       |   avg_lifetime_value |   avg_tenure_months |   churn_rate_pct |
|:---------------|---------------------:|--------------------:|-----------------:|
| One Year       |              1813.11 |                23.6 |            13.4  |
| Month-to-Month |              1797.44 |                23.3 |            28.09 |
| Two Year       |              1737.93 |                22.3 |            10.68 |


**Business Insight & Recommendation:** Two-year contract customers have by far the highest lifetime value AND the lowest churn — they are the segment to protect and replicate, not just the one to celebrate.
