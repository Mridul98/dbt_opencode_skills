# Revenue Recognition Rules (Cash vs Accrual)
**UID:** 202310271015
**Type:** Permanent / Domain Knowledge

## Concept
The business strictly recognizes revenue on a **Cash Basis** for dashboard reporting, meaning revenue is counted exactly when the credit card is successfully charged, NOT when the service is rendered. 

This architectural decision was made because our churn rate is high enough that accrual accounting creates massive discrepancies between "booked revenue" and actual cash in the bank, leading to cash flow crunches.

## Practical Implementation
In the dbt pipeline, this means we do not use the `subscription_start_date` or `invoice_period` to allocate revenue across months. 
Instead, models like `int_monthly_revenue` group strictly by the `created_at_utc` timestamp of the successful `payment` intent.

## Related Notes
* [int_monthly_revenue](202310270930-int_monthly_revenue.md)