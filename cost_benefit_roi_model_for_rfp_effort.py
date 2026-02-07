# Cost-benefit ROI model for RFP effort

## Map Cost to Technical Complexity

import pandas as pd

complexity_hours = {
    1: 20,
    2: 30,
    3: 45,
    4: 60,
    5: 80
}

# re-create df to ensure 'win_probability' and 'estimated_deal_value_usd' are present.
df = pd.DataFrame({
    'technical_complexity': [1, 2, 3, 4, 5],
    'win_probability': [0.6, 0.5, 0.4, 0.3, 0.2], # Added for demonstration
    'estimated_deal_value_usd': [100000, 150000, 200000, 250000, 300000] # Added for demonstration
})

df["rfp_effort_hours"] = df["technical_complexity"].map(complexity_hours)

## Cost Calculation

engineer_cost = 120
sales_cost = 150
opportunity_cost_pct = 0.2

df["rfp_cost"] = (
    df["rfp_effort_hours"] * (engineer_cost + sales_cost)
)

df["total_rfp_cost"] = df["rfp_cost"] * (1 + opportunity_cost_pct)

## Expected Revenue

df["expected_revenue"] = (
    df["win_probability"] * df["estimated_deal_value_usd"]
)

## Expected Profit

df["expected_profit"] = (
    df["expected_revenue"] - df["total_rfp_cost"]
)

## ROI Calculation

df["roi"] = (
    df["expected_profit"] / df["total_rfp_cost"]
)

## Decision Policy

def rfp_decision(row):
    if row["roi"] >= 1:
        return "Go (High ROI)"
    elif row["roi"] >= 0:
        return "Conditional (Strategic)"
    else:
        return "No-Go"

df["rfp_decision"] = df.apply(rfp_decision, axis=1)

## Portfolio View

df.groupby("rfp_decision")[
    ["total_rfp_cost", "expected_revenue", "expected_profit"]
].sum()

## Optimize Decision Threshold

import numpy as np

thresholds = np.arange(0.1, 0.9, 0.05)
results = []

for t in thresholds:
    profit = (
        (df["win_probability"] >= t) * df["estimated_deal_value_usd"]
        - df["total_rfp_cost"]
    ).sum()
    results.append((t, profit))

pd.DataFrame(results, columns=["threshold","total_profit"])
