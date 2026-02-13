# Monte Carlo Stress Testing for Sales Pipeline Volatility

import numpy as np
import pandas as pd

def monte_carlo_pipeline(df, n_simulations=10000):
    results = []

    for _ in range(n_simulations):
        # Random shocks
        win_shock = np.random.normal(1, 0.2, len(df))
        value_shock = np.random.normal(1, 0.25, len(df))
        cost_shock = np.random.normal(1, 0.15, len(df))

        sim_win_prob = np.clip(
            df["win_probability"] * win_shock, 0, 1
        )
        sim_value = df["estimated_deal_value_usd"] * value_shock
        sim_cost = df["total_rfp_cost"] * cost_shock

        sim_expected_profit = (
            sim_win_prob * sim_value - sim_cost
        ).sum()

        results.append(sim_expected_profit)

    return np.array(results)

df = pd.read_csv('/content/data/sales_lead_rfp_dataset.csv')
simulated_profits = monte_carlo_pipeline(df, n_simulations=10000)

## Simulation Function

def monte_carlo_pipeline(df, n_simulations=10000):
    results = []

    for _ in range(n_simulations):
        # Random shocks
        win_shock = np.random.normal(1, 0.2, len(df))
        value_shock = np.random.normal(1, 0.25, len(df))

        sim_win_prob = np.clip(
            df["rfp_win"] * win_shock, 0, 1
        )
        sim_value = df["estimated_deal_value_usd"] * value_shock
        # 'total_rfp_cost' column not found, assuming costs are zero for this simulation
        sim_cost = 0

        sim_expected_profit = (
            sim_win_prob * sim_value - sim_cost
        ).sum()

        results.append(sim_expected_profit)

    return np.array(results)

print(df.columns)

## Risk Metrics

summary = {
    "Mean Profit": np.mean(simulated_profits),
    "Median Profit": np.median(simulated_profits),
    "5th Percentile (Worst Case)": np.percentile(simulated_profits, 5),
    "95th Percentile (Best Case)": np.percentile(simulated_profits, 95),
    "Probability of Loss": np.mean(simulated_profits < 0)
}

summary

## Visualize Distribution

import matplotlib.pyplot as plt

plt.hist(simulated_profits, bins=50)
plt.axvline(np.mean(simulated_profits), linestyle="--")
plt.axvline(np.percentile(simulated_profits, 5), linestyle=":")
plt.show()

## Specific Stress Tests

### Budget Cut Shock


df_budget = df.copy()

budget_sim = monte_carlo_pipeline(df_budget)

budget_summary = {
    "Mean Profit (Budget)": np.mean(budget_sim),
    "Median Profit (Budget)": np.median(budget_sim),
    "5th Percentile (Worst Case, Budget)": np.percentile(budget_sim, 5),
    "95th Percentile (Best Case, Budget)": np.percentile(budget_sim, 95),
    "Probability of Loss (Budget)": np.mean(budget_sim < 0)
}

budget_summary

### Hiring Freeze Shock (Win Rate Impact)

df_freeze = df.copy()
df_freeze["rfp_win"] *= 0.85

freeze_sim = monte_carlo_pipeline(df_freeze)

freeze_summary = {
    "Mean Profit (Freeze)": np.mean(freeze_sim),
    "Median Profit (Freeze)": np.median(freeze_sim),
    "5th Percentile (Worst Case, Freeze)": np.percentile(freeze_sim, 5),
    "95th Percentile (Best Case, Freeze)": np.percentile(freeze_sim, 95),
    "Probability of Loss (Freeze)": np.mean(freeze_sim < 0)
}

freeze_summary

## Compare Outcomes

pd.DataFrame({
    "Baseline": simulated_profits,
    "Budget Cut": budget_sim,
    "Hiring Freeze": freeze_sim
}).describe(percentiles=[0.05, 0.5, 0.95])

## Risk-Adjusted ROI

risk_adjusted_profit = (
    np.mean(simulated_profits)
    - 0.5 * np.std(simulated_profits)
)
risk_adjusted_profit
