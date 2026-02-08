# Scenario analysis

## Baseline

import pandas as pd
df = pd.read_csv('/data/sales_lead_rfp_dataset.csv')

# Display columns to identify the correct one for grouping
print(df.columns)

baseline = df.copy()

# The following line will still cause an error until 'rfp_decision' is replaced with a valid column
# baseline_summary = baseline.groupby("rfp_decision")[["total_rfp_cost", "expected_revenue", "expected_profit"]].sum()


## Scenario 1: 20% Budget Cut

budget_cut = df.copy()

# Assign 'estimated_deal_value_usd' to 'expected_revenue'
budget_cut["expected_revenue"] = budget_cut["estimated_deal_value_usd"]

# Define a base RFP cost as 10% of the estimated deal value
# Then, calculate total_rfp_cost using the original multiplier (1.35)
budget_cut["rfp_cost_base"] = budget_cut["estimated_deal_value_usd"] * 0.10
budget_cut["total_rfp_cost"] = budget_cut["rfp_cost_base"] * 1.35

budget_cut["expected_profit"] = (
    budget_cut["expected_revenue"] - budget_cut["total_rfp_cost"]
)
budget_cut["roi"] = (
    budget_cut["expected_profit"] / budget_cut["total_rfp_cost"]
)

budget_cut["rfp_decision"] = budget_cut["roi"].apply(
    lambda x: "Go" if x >= 1.5 else "No-Go"
)

budget_cut.groupby("rfp_decision")[
    ["total_rfp_cost","expected_profit"]
].sum()

## Scenario 2: Hiring Freeze

capacity_limit_hours = budget_cut["response_time_hours"].sum() * 0.7

df_sorted = budget_cut.sort_values(
    by=["roi", "expected_profit"],
    ascending=False
)

df_sorted["cumulative_hours"] = df_sorted["response_time_hours"].cumsum()

hiring_freeze = df_sorted[
    df_sorted["cumulative_hours"] <= capacity_limit_hours
]

hiring_freeze[[
    "response_time_hours",
    "total_rfp_cost",
    "expected_profit"
]].sum()

## Scenario 3: Combined Shock (Budget Cut + Hiring Freeze)

## Executive Reality Mode


combined = df.copy()

# Assign 'estimated_deal_value_usd' to 'expected_revenue'
combined["expected_revenue"] = combined["estimated_deal_value_usd"]

# Define a base RFP cost as 10% of the estimated deal value
# Then, calculate total_rfp_cost using a multiplier (e.g., 1.4 for this scenario)
combined["rfp_cost_base"] = combined["estimated_deal_value_usd"] * 0.10
combined["total_rfp_cost"] = combined["rfp_cost_base"] * 1.4

combined["expected_profit"] = (
    combined["expected_revenue"] - combined["total_rfp_cost"]
)
combined["roi"] = (
    combined["expected_profit"] / combined["total_rfp_cost"]
)

combined = combined[
    combined["roi"] >= 1.8
].sort_values(
    by="expected_profit",
    ascending=False
)

# Use 'response_time_hours' as a proxy for 'rfp_effort_hours'
combined["cumulative_hours"] = combined["response_time_hours"].cumsum()

combined = combined[
    combined["cumulative_hours"] <= capacity_limit_hours
]

## Compare All Scenarios

# Calculate expected_profit for baseline before comparison
baseline_expected_revenue = baseline["estimated_deal_value_usd"]
baseline_total_rfp_cost = baseline["estimated_deal_value_usd"] * 0.10
baseline_expected_profit = baseline_expected_revenue - baseline_total_rfp_cost

comparison = pd.DataFrame({
    "Baseline Profit": [baseline_expected_profit.sum()],
    "Budget Cut Profit": [budget_cut["expected_profit"].sum()],
    "Hiring Freeze Profit": [hiring_freeze["expected_profit"].sum()],
    "Combined Shock Profit": [combined["expected_profit"].sum()]
})

comparison

## ROI per hour

# Calculate expected_profit for df
df["expected_revenue"] = df["estimated_deal_value_usd"]
df["total_rfp_cost"] = df["estimated_deal_value_usd"] * 0.10
df["expected_profit"] = df["expected_revenue"] - df["total_rfp_cost"]

# Use response_time_hours as a proxy for rfp_effort_hours
df["rfp_effort_hours"] = df["response_time_hours"]

df["roi_per_hour"] = df["expected_profit"] / df["rfp_effort_hours"]

df["roi_per_hour"]