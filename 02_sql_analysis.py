"""
STEP 2: SQL BUSINESS ANALYSIS
Loads cleaned data into SQLite, runs each business query, and writes a
Markdown report with Question -> Result -> Insight -> Recommendation.
"""
import sqlite3
import pandas as pd

CLEAN_PATH = "/home/claude/telecom-churn-analytics/data/telecom_churn_clean.csv"
DB_PATH = "/home/claude/telecom-churn-analytics/data/telecom_churn.db"
REPORT_PATH = "/home/claude/telecom-churn-analytics/documentation/sql_business_insights.md"

df = pd.read_csv(CLEAN_PATH)
conn = sqlite3.connect(DB_PATH)
df.to_sql("customers", conn, if_exists="replace", index=False)

queries = {
    "Q1: How healthy is our customer base right now?": """
        SELECT COUNT(*) AS total_customers,
               SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned_customers,
               ROUND(100.0*SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct,
               ROUND(SUM(MonthlyCharges),2) AS total_monthly_revenue,
               ROUND(SUM(CASE WHEN Churn='Yes' THEN MonthlyCharges ELSE 0 END),2) AS monthly_revenue_lost
        FROM customers;
    """,
    "Q2: Which contract type is bleeding us customers?": """
        SELECT Contract, COUNT(*) AS customers,
               SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned,
               ROUND(100.0*SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct,
               ROUND(AVG(MonthlyCharges),2) AS avg_monthly_charge
        FROM customers GROUP BY Contract ORDER BY churn_rate_pct DESC;
    """,
    "Q3: Which payment method correlates with highest churn?": """
        SELECT PaymentMethod, COUNT(*) AS customers,
               ROUND(100.0*SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
        FROM customers GROUP BY PaymentMethod ORDER BY churn_rate_pct DESC;
    """,
    "Q4: Are we losing our most valuable (highest revenue) customers?": """
        SELECT InternetService, COUNT(*) AS customers,
               ROUND(100.0*SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct,
               ROUND(AVG(MonthlyCharges),2) AS avg_monthly_charge,
               ROUND(SUM(CASE WHEN Churn='Yes' THEN MonthlyCharges ELSE 0 END),2) AS monthly_revenue_lost
        FROM customers GROUP BY InternetService ORDER BY monthly_revenue_lost DESC;
    """,
    "Q5: How long do we have before churn risk rises?": """
        SELECT CASE WHEN Tenure<=6 THEN '0-6 months' WHEN Tenure<=12 THEN '7-12 months'
                    WHEN Tenure<=24 THEN '13-24 months' WHEN Tenure<=48 THEN '25-48 months'
                    ELSE '48+ months' END AS tenure_cohort,
               COUNT(*) AS customers,
               ROUND(100.0*SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
        FROM customers GROUP BY tenure_cohort ORDER BY MIN(Tenure);
    """,
    "Q7: Does poor support experience drive churn?": """
        SELECT SupportCallsLast6Months, COUNT(*) AS customers,
               ROUND(100.0*SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
        FROM customers GROUP BY SupportCallsLast6Months ORDER BY SupportCallsLast6Months;
    """,
    "Q8: Which cities need urgent regional retention campaigns?": """
        WITH city_stats AS (
            SELECT City, COUNT(*) AS customers,
                   SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) AS churned,
                   SUM(MonthlyCharges) AS total_monthly_revenue
            FROM customers GROUP BY City
        )
        SELECT City, customers, churned,
               ROUND(100.0*churned/customers,2) AS churn_rate_pct,
               ROUND(total_monthly_revenue,2) AS total_monthly_revenue
        FROM city_stats ORDER BY churn_rate_pct DESC;
    """,
    "Q9: Do add-on services (TechSupport/OnlineSecurity) reduce churn?": """
        SELECT TechSupport, OnlineSecurity, COUNT(*) AS customers,
               ROUND(100.0*SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
        FROM customers WHERE InternetService != 'No'
        GROUP BY TechSupport, OnlineSecurity ORDER BY churn_rate_pct DESC;
    """,
    "Q10: Which segment generates the most lifetime value, and is it safe?": """
        SELECT Contract, ROUND(AVG(TotalCharges),2) AS avg_lifetime_value,
               ROUND(AVG(Tenure),1) AS avg_tenure_months,
               ROUND(100.0*SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
        FROM customers GROUP BY Contract ORDER BY avg_lifetime_value DESC;
    """,
}

insights = {
    "Q1: How healthy is our customer base right now?":
        "Overall churn sits at a level that, applied to monthly recurring revenue, represents a "
        "material and recurring monthly revenue leak — this is the number leadership should track weekly.",
    "Q2: Which contract type is bleeding us customers?":
        "Month-to-month customers churn several times more often than annual/two-year customers. "
        "**Recommendation:** run a contract-upgrade incentive (e.g., 1 month free) targeted at "
        "month-to-month customers past their 3rd month.",
    "Q3: Which payment method correlates with highest churn?":
        "Electronic Check users churn far more than Auto-Pay (Bank Transfer/Credit Card) users. "
        "**Recommendation:** incentivize migration to autopay with a small recurring discount — "
        "autopay is both stickier and cheaper to collect.",
    "Q4: Are we losing our most valuable (highest revenue) customers?":
        "Fiber Optic customers pay the most per month AND churn at a higher rate than DSL/No-internet "
        "customers, meaning the company's highest-margin segment is also its highest-risk segment. "
        "**Recommendation:** create a dedicated retention track for Fiber customers rather than a "
        "one-size-fits-all campaign.",
    "Q5: How long do we have before churn risk rises?":
        "Churn is heavily concentrated in the first 12 months. **Recommendation:** invest in a "
        "structured onboarding/check-in program for the first 90 days — this is the highest-leverage "
        "retention window.",
    "Q7: Does poor support experience drive churn?":
        "Churn rate climbs sharply as support call frequency increases. **Recommendation:** flag any "
        "customer with 3+ support calls in 6 months for proactive outreach before they churn, not after.",
    "Q8: Which cities need urgent regional retention campaigns?":
        "Churn rate varies meaningfully by city, meaning a single national campaign is inefficient. "
        "**Recommendation:** prioritize regional retention budget toward the cities with the combination "
        "of high churn AND high revenue concentration.",
    "Q9: Do add-on services (TechSupport/OnlineSecurity) reduce churn?":
        "Customers without TechSupport or OnlineSecurity churn noticeably more than those with both. "
        "**Recommendation:** bundle a free 3-month trial of TechSupport for new internet customers to "
        "build the habit before the risk window closes.",
    "Q10: Which segment generates the most lifetime value, and is it safe?":
        "Two-year contract customers have by far the highest lifetime value AND the lowest churn — "
        "they are the segment to protect and replicate, not just the one to celebrate.",
}

report_lines = ["# SQL Business Insights Report\n",
                "Each query below answers a specific executive question with data, insight, and a recommended action.\n"]

for question, query in queries.items():
    result_df = pd.read_sql_query(query, conn)
    report_lines.append(f"\n## {question}\n")
    report_lines.append(result_df.to_markdown(index=False))
    report_lines.append(f"\n\n**Business Insight & Recommendation:** {insights.get(question, '')}\n")
    print(f"\n{'='*70}\n{question}\n{'='*70}")
    print(result_df.to_string(index=False))

with open(REPORT_PATH, "w") as f:
    f.write("\n".join(report_lines))

conn.close()
print(f"\n\nSQL insights report saved -> {REPORT_PATH}")
print(f"SQLite database saved -> {DB_PATH}")
