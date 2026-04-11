# stg_stripe_payments
**UID:** 202310270915
**Type:** Reference / dbt Model
**Last Verified Commit:** 8f7c9b2a

## 1. Grain & Core Purpose
* **Grain:** One row per `payment_id`.
* **Purpose:** This is the base staging model for Stripe payments. It cleans up raw JSON columns, standardizes timestamps to UTC, and casts monetary amounts from cents to dollars.

## 2. Column Lineage & Logic
### Note: you have to rely only on the DBT SQL model to determine column lineage and logic. DO NOT read schema.yml file
* **`payment_id`**: Primary key for the payment.
  * **Logic:** Passthrough. No functions or joins applied.
  * **Origin:** Raw Stripe Source -> `id`
* **`amount_usd`**: The total payment amount in dollars.
  * **Logic:** `amount / 100.0`. Applied division directly on the `amount` column from the base table. No joins involved.
  * **Origin:** Raw Stripe Source -> `amount`
* **`created_at_utc`**: The timestamp when the payment was initiated.
  * **Logic:** Applied `CONVERT_TIMEZONE('UTC', created)` function directly on the base table column.
  * **Origin:** Raw Stripe Source -> `created`

## 3. Transformation Evolution (Chronological)
### Note: You have to rely only on the DBT SQL model to deduce chronological transformation evolution. DO NOT read schema.yml file. 
1. **CTE `raw_payments`:** Selects directly from the raw Stripe source table.
2. **CTE `renamed_and_cast`:** 
    * Handles the basic casting of timestamps and division of cents to dollars. No complex joins or fan-outs occur at this layer.

## 4. Lineage (The DAG)
* **Depends On (Upstream):** 
  * Raw Source: `stripe.payment`
* **Used By (Downstream):** 
  * [int_monthly_revenue](202310270930-int_monthly_revenue.md)

## 5. Deprecation Notes (Tombstone Pattern)
*(Leave empty unless model is deprecated)*

## 6. Related Notes (The Zettelkasten)
* **Fleeting Notes:** [Stripe Timezone Anomaly](202310270945-fleeting_stripe_timezone.md)
* **Knowledge Notes:** None currently applicable.