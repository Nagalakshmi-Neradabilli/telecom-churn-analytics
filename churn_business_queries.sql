-- =====================================================================
-- TELECOM CHURN ANALYTICS — SQL BUSINESS ANALYSIS
-- Every query answers a specific executive question.
-- Run against: data/telecom_churn.db (table: customers)
-- =====================================================================

-- Q1. What is our overall churn rate and what does it cost us monthly?
-- BUSINESS QUESTION: How healthy is the customer base right now?
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(MonthlyCharges), 2) AS total_monthly_revenue,
    ROUND(SUM(CASE WHEN Churn='Yes' THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_lost_to_churn
FROM customers;

-- Q2. Which contract type is bleeding us customers?
-- BUSINESS QUESTION: Where should we focus contract-conversion campaigns?
SELECT
    Contract,
    COUNT(*) AS customers,
    SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- Q3. Which payment method correlates with the highest churn?
-- BUSINESS QUESTION: Should we push customers toward autopay?
SELECT
    PaymentMethod,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;

-- Q4. Which internet service type has the highest churn, and is it our
-- highest-revenue segment too? (identifies risk concentrated in premium customers)
-- BUSINESS QUESTION: Are we losing our most valuable customers?
SELECT
    InternetService,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge,
    ROUND(SUM(CASE WHEN Churn='Yes' THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_lost
FROM customers
GROUP BY InternetService
ORDER BY monthly_revenue_lost DESC;

-- Q5. Customer tenure cohorts — when are customers most likely to leave?
-- BUSINESS QUESTION: How long do we have to "hook" a new customer before risk drops?
SELECT
    CASE
        WHEN Tenure <= 6 THEN '0-6 months'
        WHEN Tenure <= 12 THEN '7-12 months'
        WHEN Tenure <= 24 THEN '13-24 months'
        WHEN Tenure <= 48 THEN '25-48 months'
        ELSE '48+ months'
    END AS tenure_cohort,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY tenure_cohort
ORDER BY MIN(Tenure);

-- Q6. Revenue-at-risk ranking of customers using a window function
-- BUSINESS QUESTION: Which specific high-value customers should Retention call TODAY?
SELECT
    CustomerID, City, Contract, PaymentMethod, MonthlyCharges, Tenure, SupportCallsLast6Months,
    RANK() OVER (ORDER BY MonthlyCharges DESC) AS revenue_rank
FROM customers
WHERE Churn = 'Yes'
ORDER BY MonthlyCharges DESC
LIMIT 20;

-- Q7. Support call frequency vs churn — is poor service driving churn?
-- BUSINESS QUESTION: Would investing in support reduce churn?
SELECT
    SupportCallsLast6Months,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY SupportCallsLast6Months
ORDER BY SupportCallsLast6Months;

-- Q8. City-wise revenue and churn (using CTE) — where should regional
-- retention teams focus?
-- BUSINESS QUESTION: Which cities need urgent regional retention campaigns?
WITH city_stats AS (
    SELECT
        City,
        COUNT(*) AS customers,
        SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned,
        SUM(MonthlyCharges) AS total_monthly_revenue
    FROM customers
    GROUP BY City
)
SELECT
    City,
    customers,
    churned,
    ROUND(100.0 * churned / customers, 2) AS churn_rate_pct,
    ROUND(total_monthly_revenue, 2) AS total_monthly_revenue,
    RANK() OVER (ORDER BY total_monthly_revenue DESC) AS revenue_rank
FROM city_stats
ORDER BY churn_rate_pct DESC;

-- Q9. Add-on services (TechSupport, OnlineSecurity) — do they reduce churn?
-- BUSINESS QUESTION: Should add-ons be bundled free to reduce churn?
SELECT
    TechSupport,
    OnlineSecurity,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
WHERE InternetService != 'No'
GROUP BY TechSupport, OnlineSecurity
ORDER BY churn_rate_pct DESC;

-- Q10. Customer Lifetime Value (CLV) by segment using CASE + subquery
-- BUSINESS QUESTION: Which segment generates the most long-term value, and is it safe?
SELECT
    Contract,
    ROUND(AVG(TotalCharges), 2) AS avg_lifetime_value,
    ROUND(AVG(Tenure), 1) AS avg_tenure_months,
    ROUND(100.0 * SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY avg_lifetime_value DESC;

-- Q11. Create a reusable VIEW for the Power-BI-style "Revenue at Risk" page
CREATE VIEW IF NOT EXISTS revenue_at_risk AS
SELECT
    CustomerID, City, Contract, PaymentMethod, InternetService,
    MonthlyCharges, Tenure, SupportCallsLast6Months,
    CASE
        WHEN Contract = 'Month-to-Month' AND SupportCallsLast6Months >= 3 THEN 'High Risk'
        WHEN Contract = 'Month-to-Month' THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_category
FROM customers
WHERE Churn = 'No';  -- still-active customers we could still lose

SELECT risk_category, COUNT(*) AS customers, ROUND(SUM(MonthlyCharges),2) AS revenue_at_risk
FROM revenue_at_risk
GROUP BY risk_category
ORDER BY revenue_at_risk DESC;
