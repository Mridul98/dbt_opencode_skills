# Stripe Timezone Casting Anomaly
**UID:** 202310270945
**Type:** Fleeting / Scratchpad

## Context
While reviewing [stg_stripe_payments](202310270915-stg_stripe_payments.md), I noticed how we are handling the `created` column.

## Observation / Question
Stripe supposedly sends all webhook payloads in UTC by default, but the raw database ingestion seems to be defaulting to the server's local time (PST) before we cast it in dbt. 
If we migrate our Fivetran/Airbyte ingestion server to a new region, `CONVERT_TIMEZONE('UTC', created)` might double-shift the timezone and break downstream daily revenue metrics.

## Next Steps
- [ ] Verify Fivetran connector timezone settings.
- [ ] Check if `created` should just be cast directly to `TIMESTAMP` without the explicit shift.

## Related Notes
* [stg_stripe_payments](202310270915-stg_stripe_payments.md)
* [Revenue Recognition Rules](202310271015-knowledge_revenue_recognition.md)