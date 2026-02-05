import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/sales_lead_rfp_dataset.csv")

df.info()
df.describe()

sns.countplot(x="rfp_win", data=df)
plt.show()

df["lead_score"] = (
    df["solution_fit_score"] * 40 +
    df["past_vendor_experience"] * 20 +
    (df["technical_complexity"] <= 3).astype(int) * 15 +
    (df["response_time_hours"] <= 24).astype(int) * 15 +
    (df["estimated_deal_value_usd"] > 100000).astype(int) * 10
)

df["lead_category"] = pd.cut(
    df["lead_score"],
    bins=[0,40,70,100],
    labels=["Low Priority","Medium Priority","High Priority"]
)

df[["lead_score","lead_category"]].head()

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

features = [
    "technical_complexity",
    "response_time_hours",
    "solution_fit_score",
    "estimated_deal_value_usd",
    "past_vendor_experience"
]

X = df[features]
y = df["rfp_win"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train, y_train)

pred_prob = model.predict_proba(X_test)[:,1]
roc_auc_score(y_test, pred_prob)

importance = pd.DataFrame({
    "feature": features,
    "coef": model.coef_[0]
}).sort_values(by="coef", ascending=False)

importance

sns.boxplot(
    x="rfp_win",
    y="sales_cycle_days",
    data=df[df["rfp_received"]==1]
)
plt.show()