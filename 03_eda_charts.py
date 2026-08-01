"""
STEP 3: EDA VISUALIZATIONS
Each chart answers a specific business question (not decoration).
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 130

df = pd.read_csv("/home/claude/telecom-churn-analytics/data/telecom_churn_clean.csv")
OUT = "/home/claude/telecom-churn-analytics/charts/"

# Chart 1: Churn by Contract Type
plt.figure(figsize=(7, 5))
rate = df.groupby("Contract")["Churn"].apply(lambda x: (x == "Yes").mean() * 100).sort_values(ascending=False)
ax = rate.plot(kind="bar", color=["#d62728", "#ff7f0e", "#2ca02c"])
plt.title("Which Contract Type Is Bleeding Us Customers?", fontsize=12, fontweight="bold")
plt.ylabel("Churn Rate (%)")
plt.xlabel("")
plt.xticks(rotation=0)
for i, v in enumerate(rate):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(OUT + "01_churn_by_contract.png")
plt.close()

# Chart 2: Churn by Payment Method
plt.figure(figsize=(8, 5))
rate2 = df.groupby("PaymentMethod")["Churn"].apply(lambda x: (x == "Yes").mean() * 100).sort_values(ascending=False)
ax = rate2.plot(kind="barh", color="#1f77b4")
plt.title("Does Payment Method Predict Who Leaves?", fontsize=12, fontweight="bold")
plt.xlabel("Churn Rate (%)")
for i, v in enumerate(rate2):
    ax.text(v + 0.3, i, f"{v:.1f}%", va="center", fontweight="bold")
plt.tight_layout()
plt.savefig(OUT + "02_churn_by_payment.png")
plt.close()

# Chart 3: Revenue Lost by Internet Service (dual insight: revenue AND churn)
plt.figure(figsize=(7, 5))
rev_lost = df[df["Churn"] == "Yes"].groupby("InternetService")["MonthlyCharges"].sum().sort_values(ascending=False)
ax = rev_lost.plot(kind="bar", color="#9467bd")
plt.title("Where Are We Losing the Most Monthly Revenue?", fontsize=12, fontweight="bold")
plt.ylabel("Monthly Revenue Lost ($)")
plt.xlabel("")
plt.xticks(rotation=0)
for i, v in enumerate(rev_lost):
    ax.text(i, v + 500, f"${v:,.0f}", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(OUT + "03_revenue_lost_by_internet.png")
plt.close()

# Chart 4: Churn by Tenure Cohort
plt.figure(figsize=(7, 5))
df["TenureCohort"] = pd.cut(df["Tenure"], bins=[-1, 6, 12, 24, 48, 100],
                             labels=["0-6mo", "7-12mo", "13-24mo", "25-48mo", "48+mo"])
rate3 = df.groupby("TenureCohort", observed=True)["Churn"].apply(lambda x: (x == "Yes").mean() * 100)
ax = rate3.plot(kind="line", marker="o", linewidth=2.5, color="#d62728")
plt.title("How Long Until a New Customer Is 'Safe'?", fontsize=12, fontweight="bold")
plt.ylabel("Churn Rate (%)")
plt.xlabel("Tenure Cohort")
for i, v in enumerate(rate3):
    ax.text(i, v + 0.7, f"{v:.1f}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(OUT + "04_churn_by_tenure.png")
plt.close()

# Chart 5: Support Calls vs Churn
plt.figure(figsize=(7, 5))
support = df[df["SupportCallsLast6Months"] <= 6].groupby("SupportCallsLast6Months")["Churn"].apply(lambda x: (x == "Yes").mean() * 100)
ax = support.plot(kind="bar", color="#ff7f0e")
plt.title("Does Poor Support Experience Drive Churn?", fontsize=12, fontweight="bold")
plt.ylabel("Churn Rate (%)")
plt.xlabel("Support Calls (last 6 months)")
plt.xticks(rotation=0)
for i, v in enumerate(support):
    ax.text(i, v + 0.7, f"{v:.1f}%", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(OUT + "05_churn_by_support_calls.png")
plt.close()

# Chart 6: Correlation heatmap (numeric drivers)
plt.figure(figsize=(7, 5))
num_df = df.copy()
num_df["ChurnFlag"] = (num_df["Churn"] == "Yes").astype(int)
corr_cols = ["Tenure", "MonthlyCharges", "TotalCharges", "SupportCallsLast6Months", "ChurnFlag"]
corr = num_df[corr_cols].corr()
sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f")
plt.title("What Actually Correlates With Churn?", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig(OUT + "06_correlation_heatmap.png")
plt.close()

print("6 business-question charts saved to /charts")
