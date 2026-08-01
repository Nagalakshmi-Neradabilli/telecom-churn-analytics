"""
STEP 4: FEATURE ENGINEERING + MACHINE LEARNING
Builds business-driven features, trains Logistic Regression + Random Forest,
and translates model output into business action (not just metrics).
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, roc_auc_score, confusion_matrix, roc_curve)

df = pd.read_csv("/home/claude/telecom-churn-analytics/data/telecom_churn_clean.csv")

# ---------------- FEATURE ENGINEERING ----------------
# Tenure Group: business-readable lifecycle stage
df["TenureGroup"] = pd.cut(df["Tenure"], bins=[-1, 6, 12, 24, 48, 100],
                            labels=["0-6mo", "7-12mo", "13-24mo", "25-48mo", "48+mo"])

# Revenue Tier: segments customers by spend for targeted campaigns
df["RevenueTier"] = pd.cut(df["MonthlyCharges"], bins=[0, 40, 70, 100, 200],
                            labels=["Low", "Medium", "High", "Premium"])

# Customer Lifetime Value proxy
df["CLV"] = df["MonthlyCharges"] * df["Tenure"]

# Revenue at Risk flag: still-active month-to-month customers = exposed revenue
df["RevenueAtRisk"] = np.where(
    (df["Contract"] == "Month-to-Month") & (df["Churn"] == "No"), df["MonthlyCharges"], 0
)

# Engagement Score: proxy for how "locked in" a customer is (more services = higher engagement)
service_cols = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
df["EngagementScore"] = df[service_cols].apply(lambda row: sum(v == "Yes" for v in row), axis=1)

# Contract Renewal Risk Indicator
df["HighRiskFlag"] = np.where(
    (df["Contract"] == "Month-to-Month") & (df["SupportCallsLast6Months"] >= 3), 1, 0
)

print("Engineered features: TenureGroup, RevenueTier, CLV, RevenueAtRisk, EngagementScore, HighRiskFlag")
print(f"Total revenue at risk (active month-to-month customers): ${df['RevenueAtRisk'].sum():,.2f}/month")

# ---------------- MODEL PREP ----------------
model_df = df.copy()
model_df["ChurnFlag"] = (model_df["Churn"] == "Yes").astype(int)

categorical_cols = ["Gender", "Partner", "Dependents", "PhoneService", "MultipleLines",
                     "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
                     "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
                     "PaperlessBilling", "PaymentMethod", "AgeGroup", "City",
                     "TenureGroup", "RevenueTier"]

le_dict = {}
for col in categorical_cols:
    le = LabelEncoder()
    model_df[col] = le.fit_transform(model_df[col].astype(str))
    le_dict[col] = le

feature_cols = categorical_cols + ["SeniorCitizen", "Tenure", "MonthlyCharges", "TotalCharges",
                                    "SupportCallsLast6Months", "CLV", "EngagementScore", "HighRiskFlag"]

X = model_df[feature_cols]
y = model_df["ChurnFlag"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ---------------- LOGISTIC REGRESSION ----------------
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logreg = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
logreg.fit(X_train_scaled, y_train)
logreg_pred = logreg.predict(X_test_scaled)
logreg_proba = logreg.predict_proba(X_test_scaled)[:, 1]

# ---------------- RANDOM FOREST ----------------
rf = RandomForestClassifier(n_estimators=300, max_depth=8, class_weight="balanced",
                             random_state=42, min_samples_leaf=10)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_proba = rf.predict_proba(X_test)[:, 1]

# ---------------- EVALUATION ----------------
def evaluate(y_true, y_pred, y_proba, name):
    return {
        "Model": name,
        "Accuracy": round(accuracy_score(y_true, y_pred), 3),
        "Precision": round(precision_score(y_true, y_pred), 3),
        "Recall": round(recall_score(y_true, y_pred), 3),
        "F1": round(f1_score(y_true, y_pred), 3),
        "ROC_AUC": round(roc_auc_score(y_true, y_proba), 3),
    }

results = pd.DataFrame([
    evaluate(y_test, logreg_pred, logreg_proba, "Logistic Regression"),
    evaluate(y_test, rf_pred, rf_proba, "Random Forest"),
])
print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)
print(results.to_string(index=False))

# Choose Random Forest as final model (better recall typically) - check
final_model_name = "Random Forest" if results.loc[1, "Recall"] >= results.loc[0, "Recall"] else "Logistic Regression"
print(f"\nSelected model: {final_model_name}")
print("Business rationale: Recall is prioritized over Accuracy because failing to identify a "
      "customer who WILL churn (false negative) costs the company a lost customer and their full "
      "lifetime value. A false positive only costs a discretionary retention offer to a loyal "
      "customer — a much cheaper mistake.")

# ---------------- FEATURE IMPORTANCE ----------------
importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)
print("\nTop 10 Churn Drivers (Random Forest Feature Importance):")
print(importances.head(10).to_string())

plt.figure(figsize=(8, 6))
importances.head(10).sort_values().plot(kind="barh", color="#2ca02c")
plt.title("What's Actually Causing the Churn? (Top 10 Drivers)", fontsize=12, fontweight="bold")
plt.xlabel("Feature Importance")
plt.tight_layout()
plt.savefig("/home/claude/telecom-churn-analytics/charts/07_feature_importance.png")
plt.close()

# Confusion matrix chart
import seaborn as sns
plt.figure(figsize=(5.5, 5))
cm = confusion_matrix(y_test, rf_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["No Churn", "Churn"], yticklabels=["No Churn", "Churn"])
plt.title("Random Forest: Predicted vs Actual Churn", fontsize=12, fontweight="bold")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.tight_layout()
plt.savefig("/home/claude/telecom-churn-analytics/charts/08_confusion_matrix.png")
plt.close()

# ROC curve
plt.figure(figsize=(6, 5))
fpr, tpr, _ = roc_curve(y_test, rf_proba)
plt.plot(fpr, tpr, label=f"Random Forest (AUC = {roc_auc_score(y_test, rf_proba):.3f})", linewidth=2, color="#d62728")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.title("Model Discrimination: ROC Curve", fontsize=12, fontweight="bold")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.tight_layout()
plt.savefig("/home/claude/telecom-churn-analytics/charts/09_roc_curve.png")
plt.close()

# ---------------- RISK-SCORED CUSTOMER LIST (for dashboard Page 4) ----------------
test_customers = df.loc[X_test.index, ["CustomerID", "City", "Contract", "MonthlyCharges", "Tenure"]].copy()
test_customers["ChurnProbability"] = rf_proba
test_customers["RiskCategory"] = pd.cut(
    test_customers["ChurnProbability"], bins=[-0.01, 0.3, 0.6, 0.8, 1.01],
    labels=["Low Risk", "Medium Risk", "High Risk", "Critical Risk"]
)
test_customers = test_customers.sort_values("ChurnProbability", ascending=False)
test_customers.to_csv("/home/claude/telecom-churn-analytics/data/churn_risk_scores.csv", index=False)

results.to_csv("/home/claude/telecom-churn-analytics/documentation/model_comparison_results.csv", index=False)
importances.to_csv("/home/claude/telecom-churn-analytics/documentation/feature_importance.csv")

print(f"\nRisk-scored customer list saved: {len(test_customers)} customers")
print(f"High/Critical risk customers to prioritize for outreach: "
      f"{(test_customers['RiskCategory'].isin(['High Risk','Critical Risk'])).sum()}")
print("\nAll model outputs, charts, and CSVs saved.")
