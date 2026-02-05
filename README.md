# RFP ROI & Sales Decision Intelligence Project
Analytics project that mirrors how B2B sales + pre-sales / solution engineering teams qualify leads and manage technical sales cycles, including RFP/RFI responses.

## Executive Summary
This project builds a **decision intelligence system** for qualifying B2B sales leads, managing RFP/RFI efforts, and maximizing revenue under real-world constraints such as **budget cuts, hiring freezes, and pipeline volatility**.

It combines **machine learning**, **cost–benefit ROI modeling**, **SHAP explainability**, **Monte Carlo stress testing**, and an **interactive Power BI dashboard** to support data-driven sales and finance decisions.

---

## Business Problem
Enterprise sales teams face three persistent challenges:

- Too many low-quality leads and RFPs
- High pre-sales engineering cost with unclear ROI
- Revenue volatility due to uncertain win rates and deal sizes

**Responding to every RFP destroys value.**

This project answers:
> *Which RFPs should we pursue, under what conditions, and why?*

---

## Dataset

**File:** `sales_lead_rfp_dataset.csv`

**Records:** 1,200 realistic B2B sales leads

### Key Fields
| Column | Description |
|------|-----------|
| lead_id | Unique lead identifier |
| industry | Client industry |
| company_size | Small / Mid / Enterprise |
| region | Geography |
| lead_source | Website, Referral, Partner, etc. |
| rfp_received | Whether RFP/RFI was issued |
| technical_complexity | 1 (Low) – 5 (High) |
| estimated_deal_value_usd | Deal size |
| response_time_hours | Time to respond |
| solution_fit_score | Technical fit (0–1) |
| past_vendor_experience | Prior relationship |
| rfp_win | Target variable (won/lost) |

---
