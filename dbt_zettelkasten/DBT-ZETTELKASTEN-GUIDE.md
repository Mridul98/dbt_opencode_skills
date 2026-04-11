# CLI Zettelkasten for Data Engineering & dbt

Welcome to your Second Brain, optimized for Data Engineering and mapping out dbt repositories. This system blends the atomic, linked nature of a Zettelkasten with a hierarchical directory structure to ensure your notes mirror your data architecture.

## 1. Core Principles

### File Naming (The UID System)
Every file must start with a timestamp **Unique Identifier (UID)**.
* **Format:** `YYYYMMDDHHMM-[prefix]_descriptive_title_[suffix].md`
* **Unique Events:** Every file receives a fresh, unique timestamp at the exact moment of its creation. Do not share UIDs across a Triad (e.g., the Model, Fleeting, and Knowledge notes will have slightly different timestamp prefixes representing when you authored them).
* **Conventions:**
  * Staging: `stg_` prefix (e.g., `202310270915-stg_stripe_payments.md`)
  * Intermediate: `int_` prefix (e.g., `202310271030-int_sales_pivoted.md`)
  * Reporting: `_report` suffix (e.g., `202310271400-monthly_revenue_report.md`)
* **Why:** UIDs prevent naming collisions. Strict prefixes/suffixes allow you to instantly identify the model's layer and enable lightning-fast global searches using wildcards (e.g., `*_report.md`).

### Markdown Linking (The DAG)
Links between notes represent your dbt DAG (Directed Acyclic Graph).
* **Format:** Standard Markdown `[Visible Text](./relative/path/to/file.md)`
* **Example:** `Depends on: [stg_stripe_payments](../staging/202310270915-stg-stripe-payments.md)`
* **Why:** Standard links work everywhere (GitHub, VSCode, Neovim, standard markdown renderers) and force you to be conscious of the physical directory hierarchy.
* **Assurance:** Make sure the links between notes are not broken.

---

## 2. The Hybrid Directory Structure (Schema)

Unlike traditional flat Zettelkastens, we leverage directories to mirror data layers. This provides "free tagging" and scoped searches.

**Note on Location:** A project should only have *one* centralized Second Brain. Before adding notes, always verify the location of these core directories rather than blindly creating new ones in your current working path.

The Second Brain must strictly adhere to the following schema. AI Agents must dynamically replace `<variables>` based on the active project context.

* **`01-fleeting/`** -> Model-centric scratchpad for anomalies and questions.
* **`02-knowledge/`** -> Permanent notes distilling core business rules.
* **`03-repos/`** -> The root for all dbt model documentation.
    * **`03-repos/<actual_dbt_project_name>/`** -> You MUST create a subfolder matching the exact name of the dbt project you are documenting.
        * **`staging/`** -> For `stg_` models.
        * **`intermediate/`** -> For `int_` models.
        * **`reporting/`** -> For final `_report` or `_marts` models.
        * **`macros/`** -> For reusable Jinja snippets.
        * **`metrics/`** -> For core business definitions.
* **`templates/`** -> Contains the `.md` templates. DO NOT modify these.

---

## 3. Adapting Notes for Data Engineering

Do not just copy and paste SQL. Use your Zettelkasten to explain the **Why** and **How**. Focus on complex `intermediate` and `reporting` models; avoid documenting trivial 1:1 staging models unless they contain tricky logic.

### A. Documenting Grain & Purpose
The most critical part of a data model is its grain. Every model note must define its row-level identity.
* *Example:* "One row per `user_id` per `month`."

### B. Capturing Column Lineage & Logic
Never write a column description without explaining *how* it is calculated and *where* it came from. Use standard markdown links to point directly to the upstream model.

*Format:*
* **`[column_name]`**: [Business description]
  * **Logic:** [The exact SQL or explanation, e.g., `COUNT(DISTINCT deal_id)`]
  * **Origin:** [[Link to upstream model]] -> `[upstream_column_name]`

---

## 4. Lifecycle Management (Surviving CRUD Operations)

A static Second Brain for a dynamic dbt codebase will fail. You must treat notes like code, evolving them as the dbt models experience CRUD (Create, Read, Update, Delete) operations.

### Create (New Models)
* Follow the Mandatory Triad Documentation rules (Section 6). Generate fresh UIDs for every new file.

### Update (In-Place Evolution)
When an existing dbt model is modified (e.g., a column is added, logic is tweaked, but the core grain remains the same), the Zettelkasten must sync:
1. **DO NOT change the file's UID or filename.** The UID marks the birth of the concept.
2. **Update the `Last Verified Commit`:** Change the metadata tag at the top of the note to the new Git hash.
3. **Evolve the Content:** Add/remove columns in the `Lineage & Logic` section. Update the SQL logic explanations to reflect reality.
4. **Capture New Thoughts:** If the update introduces technical debt or new business rules, create *new* Fleeting or Knowledge notes (with fresh UIDs) and link them to the bottom of the existing Model note.

### Delete / Major Refactor (The Tombstone Pattern)
When a model is completely deleted or fundamentally rewritten (e.g., the grain changes so much it requires a V2), you must execute a strict Tombstone procedure to preserve the historical DAG.

**Step 1: Tombstone the Old Note**
1. Rename the old file to include `-DEPRECATED-` (e.g., `202310270930-DEPRECATED-int_monthly_revenue.md`).
2. Fill out `## 5. Deprecation Notes`: Record the date, the reason for deprecation, and explicitly link to the *new* model replacing it (if applicable).
3. **CRITICAL:** Do NOT delete or modify its existing upstream/downstream links in Section 4. They must remain intact to preserve the historical lineage.

**Step 2: Create the V2 Triad (If Replaced)**
1. Generate a brand new Model Note for the new dbt model using the standard template (with a fresh UID).
2. Document its new logic and new lineage.
3. **CRITICAL:** In the new model's `## 3. Transformation Evolution` or `## 6. Related Notes` section, you MUST add a link pointing backward to the `-DEPRECATED-` note. (e.g., `* **Legacy Logic:** This model replaces [DEPRECATED-int_monthly_revenue](...)`).

### Link Validation
To ensure the integrity of the Zettelkasten, all Markdown links must point to valid files. Run the provided Python link checker script after making changes to the notes:
```bash
./dbt_zettelkasten/scripts/check_links.py
```
This script traverses all `.md` files, ensuring internal file links resolve correctly and external URLs are reachable. If you add or rename files, you must fix any broken links this script surfaces.

---

## 5. CLI Query Engine Mastery

Because we use standard text and folders, your terminal is the ultimate search engine. Use `ripgrep` (`rg`) or `grep` for lightning-fast lookups.

### 🔍 Search by Model Dependencies (1st-Degree Lineage)
*Scenario: What models rely on this staging model?*
1. Get the UID of the staging model (e.g., `202310270915`).
2. Search the repo for that UID:
   ```bash
   rg "202310270915" 03-repos/sales-analytics/
   ```

### 🔍 Scoped Searches via Directories
*Scenario: What is the final business logic for the `amount` column?*
Instead of searching everywhere, scope your search strictly to the `reporting/` directory to filter out intermediate noise.
```bash
rg "amount" 03-repos/sales-analytics/reporting/
```

### 🔍 Find by Naming Convention (Prefix/Suffix)
*Scenario: List every reporting model across all repositories.*
```bash
rg -g "*_report.md" --files 03-repos/
```
*Scenario: Find where a staging model is first used in intermediate logic.*
```bash
rg "stg_stripe_payments" 03-repos/sales-analytics/intermediate/
```

### 🔍 Trace Column Origin
*Scenario: What upstream file provides the data for `deals_in_stage`?*
```bash
rg -A 2 "\*\*\`deals_in_stage\`\*\*" 03-repos/
```
*(This command finds the column name and prints the next 2 lines, instantly revealing its Logic and Origin).*

### 🔍 Find all "User" grained models
```bash
rg -A 1 "\*\*Grain:\*\*" 03-repos/ | rg -i "user"
```
*(Finds the Grain header and searches the subsequent line for 'user')*

---

Your Second Brain is now ready. Start by copying `templates/template-dbt-model.md` into one of the `03-repos` subdirectories and trace your first dbt model!

---

## 6. Mandatory Triad Documentation
When documenting a dbt repository, you must create a triad of notes for **every** model:

*   **Repository Note (`03-repos/`)**: The standard lineage and column definition. All the notes should contain valid links to fleeting and knowledge notes.
    *   **🎯 Expected Outcome:** A complete map of the model's grain, column-level transformation logic, upstream origins, and its place in the DAG. No raw SQL dumps without plain-English explanation.
    *   **📄 Reference Examples:** `examples/202310270915-stg_stripe_payments.md` and `examples/202310270930-int_monthly_revenue.md`
*   **Fleeting Note (`01-fleeting/`)**: Immediate observations, anomalies, or technical debt spotted in the SQL. Use `template-fleeting.md`. All the fleeting notes should contain valid parent notes link. All the fleeting notes should be complete with proper contents, not only scaffolding.
    *   **🎯 Expected Outcome:** A clear, actionable brain dump regarding an anomaly or question discovered during the modeling process, culminating in concrete "Next Steps".
    *   **📄 Reference Example:** `examples/202310270945-fleeting_stripe_timezone.md`
*   **Knowledge Note (`02-knowledge/`)**: The extracted, abstracted business logic or architectural pattern behind the model. Use `template-knowledge.md`. All the knowledges notes should contain valid parent notes link. All the fleeting notes should be complete with proper contents, not only scaffolding.
    *   **🎯 Expected Outcome:** A distilled, enduring explanation of a core business rule, architectural decision, or metric definition (e.g., cash vs. accrual accounting) that transcends specific dbt syntax.
    *   **📄 Reference Example:** `examples/202310271015-knowledge_revenue_recognition.md`

### 🛑 Anti-Skeleton Policy (Examples)
Documentation that consists only of template placeholders (e.g., leaving `[Explain overall logical architecture]` in the file) is considered invalid. All fields must be comprehensively filled out with real business context. 
To see what a fully fleshed-out Zettelkasten triad looks like, review the `examples/` directory bundled with this skill.
