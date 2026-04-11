# [Model Name] (e.g., int_payments_pivoted)
**UID:** [YYYYMMDDHHMM]
**Type:** Reference / dbt Model
**Last Verified Commit:** [Git Commit Hash or "N/A"]

## 1. Grain & Core Purpose
* **Grain:** One row per `[grain_column]`.
* **Purpose:** [1-2 sentences explaining the core objective of this model in the pipeline.]

## 2. Column Lineage & Logic
### Note: you have to rely only on the DBT SQL model to determine column lineage and logic. DO NOT read schema.yml file
* **`[column_1]`**: [Primary key / Business description]
  * **Logic:** [The exact SQL snippet or plain English explanation of the transformation, e.g., `COALESCE(amount, 0) * exchange_rate`]. It should be complete with proper mentions of joins as well as the functions applied if applicable.
  * **Origin:** [Upstream Model Name](../staging/YYYYMMDDHHMM-stg_upstream_model.md) -> `[upstream_column_name]`
* **`[column_2]`**: [Description]
  * **Logic:** Passthrough.
  * **Origin:** [Upstream Model Name](../staging/YYYYMMDDHHMM-stg_upstream_model.md) -> `[column_2]`

## 3. Transformation Evolution (Chronological)
### Note: You have to rely only on the DBT SQL model to deduce chronological transformation evolution. DO NOT read schema.yml file. 
1. **CTE `[name]`:** Reads from [Upstream Model Name](../staging/YYYYMMDDHHMM-stg_upstream_model.md).
2. **CTE `[name]`:** 
    * [Explain overall logical architecture, e.g., complex joins, fan-outs, or window functions. Column specific math goes in Section 2. Do not miss out any logic]

## 4. Lineage (The DAG)
* **Depends On (Upstream):** 
  * [Upstream Model Name](../staging/YYYYMMDDHHMM-stg_upstream_model.md)
* **Used By (Downstream):** 
  * [Downstream Model Name](../reporting/YYYYMMDDHHMM-downstream_model_report.md)

## 5. Deprecation Notes (Tombstone Pattern)
*(Leave empty unless model is deprecated)*
* **Deprecated On:** [Date]
* **Reason:** [Why was this removed? If replaced by a V2 model, you MUST provide a link to the new model here.]

## 6. Related Notes (The Zettelkasten)
* **Fleeting Notes:** [[Link to related Fleeting Notes (e.g., anomalies, questions)]]
* **Knowledge Notes:** [[Link to related Knowledge Notes (e.g., core business logic)]]