# [Metric Name] (e.g., Monthly Recurring Revenue - MRR)
**UID:** [YYYYMMDDHHMM]
**Type:** Permanent / Metric Definition
**Business Owner:** [Name / Department]

## 1. Business Definition
[Plain English definition of the metric. What does it measure and why does the business care?]

## 2. Calculation Logic
[Formula or high-level logical steps to calculate this metric. e.g., "Sum of all active subscription amounts excluding one-time fees."]

## 3. Related dbt Models
* **Calculated in:** [monthly_revenue_report](../reporting/YYYYMMDDHHMM-monthly_revenue_report.md)
* **Underlying sources:** [stg_stripe_subscriptions](../staging/YYYYMMDDHHMM-stg_stripe_subscriptions.md)

## 4. Known Gotchas & Quirks
* [e.g., "MRR does not account for mid-month prorations until the invoice is fully settled."]

## 5. Related Notes
* [Related Knowledge Concept](../knowledge/YYYYMMDDHHMM-business_concept.md)
