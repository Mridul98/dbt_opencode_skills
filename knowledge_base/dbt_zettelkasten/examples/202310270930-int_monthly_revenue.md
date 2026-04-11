# int_monthly_revenue
**UID:** 202310270930
**Type:** Reference / dbt Model
**Last Verified Commit:** 8f7c9b2a

## 1. Grain & Core Purpose
* **Grain:** One row per `customer_id` per `billing_month`.
* **Purpose:** Aggregates all valid Stripe payments into a monthly revenue grain per customer. This intermediate model resolves complexities around refunded payments and prorations before hitting the final reporting layer.

## 2. Column Lineage & Logic
### Note: you have to rely only on the DBT SQL model to determine column lineage and logic. DO NOT read schema.yml file
* **`customer_id`**: The unique identifier for the customer.
  * **Logic:** Passthrough from the `GROUP BY` clause in the `aggregated_months` CTE.
  * **Origin:** [stg_stripe_payments](202310270915-stg_stripe_payments.md) -> `customer_id`
* **`billing_month`**: The month the revenue is recognized for.
  * **Logic:** Applied `DATE_TRUNC('month', created_at_utc)` function within the `aggregated_months` CTE. No joins involved.
  * **Origin:** [stg_stripe_payments](202310270915-stg_stripe_payments.md) -> `created_at_utc`
* **`net_revenue_usd`**: Total revenue after subtracting refunds.
  * **Logic:** Applied the aggregate function `SUM(amount_usd)` combined with a `FILTER (WHERE status = 'succeeded')` clause.
  * **Origin:** [stg_stripe_payments](202310270915-stg_stripe_payments.md) -> `amount_usd`

## 3. Transformation Evolution (Chronological)
### Note: You have to rely only on the DBT SQL model to deduce chronological transformation evolution. DO NOT read schema.yml file. 
1. **CTE `successful_payments`:** Filters the staging model strictly for payments where `status = 'succeeded'`.
2. **CTE `aggregated_months`:** 
    * Truncates the dates to the month level and aggregates the `amount_usd` using a `GROUP BY` on customer and month.

## 4. Lineage (The DAG)
* **Depends On (Upstream):** 
  * [stg_stripe_payments](202310270915-stg_stripe_payments.md)
* **Used By (Downstream):** 
  * (Final Reporting Models)

## 5. Deprecation Notes (Tombstone Pattern)
*(Leave empty unless model is deprecated)*

## 6. Related Notes (The Zettelkasten)
* **Fleeting Notes:** None currently applicable.
* **Knowledge Notes:** [Revenue Recognition Rules (Cash vs Accrual)](202310271015-knowledge_revenue_recognition.md)