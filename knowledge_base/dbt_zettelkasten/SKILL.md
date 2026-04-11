---
name: dbt-zettelkasten
description: Document dbt models, trace data lineage, or query the Data Engineering knowledge base.
---
# Skill: dbt Zettelkasten

## Core Directive
Before starting any documentation task, you MUST read and adhere to the project's official rulebook bundled with this skill. 

*Note to Agent: The guide ([DBT-ZETTELKASTEN-GUIDE.md](DBT-ZETTELKASTEN-GUIDE.md)) and the `templates/` directory are located in the exact same folder as this SKILL.md file. Use your knowledge of the skill's file path to locate and read them.*

## 0. Directory Discovery (MANDATORY FIRST STEP)
Before creating ANY notes or directories, you must locate the existing Zettelkasten (Second Brain).
1. Search the workspace using `glob` or `bash` to look for existing standard Zettelkasten folders (e.g., `01-fleeting`, `02-knowledge`, `03-repos`).
2. Prompt the user with a list of the probable directories you found.
3. Ask the user to explicitly confirm the correct target root directory for the new notes.
4. **DO NOT** proactively create new top-level directories (`01-fleeting`, `02-knowledge`, `03-repos`) using `mkdir` unless the user explicitly instructs you that this is a brand-new initialization. 
5. **Dynamic Repo Folders:** If you are documenting a new dbt project, you MAY create the dynamic `<actual_dbt_project_name>` subfolder inside an existing `03-repos/` directory (e.g., `mkdir 03-repos/new_project_name/staging`).

## Anti-Laziness Directive (CRITICAL)
When generating notes, you MUST NOT stop at creating skeletons. You must fully replace ALL `[Placeholder]` tags with actual, deeply researched analytical content. 

Before writing a note, you MUST read its corresponding perfect example to understand the expected outcome and level of detail:
- For Model/Repo Notes: Read [examples/202310270930-int_monthly_revenue.md](examples/202310270930-int_monthly_revenue.md)
- For Fleeting Notes: Read [examples/202310270945-fleeting_stripe_timezone.md](examples/202310270945-fleeting_stripe_timezone.md)
- For Knowledge Notes: Read [examples/202310271015-knowledge_revenue_recognition.md](examples/202310271015-knowledge_revenue_recognition.md)

* **Triad Connectivity:** You MUST explicitly link the newly generated Fleeting and Knowledge notes into the bottom of the Model note under the `## 6. Related Notes` section. Do not leave the triad disconnected.
* **Handling Deprecation:** Actively ignore `-DEPRECATED-` files during standard searches/linking to prevent polluting active models. **Exception:** When executing a Major Refactor/Tombstone replacement, you MUST cross-link the new V2 model and the old `-DEPRECATED-` model to preserve historical lineage, as defined in the Guide.

## Quick Reference (Sourced from the Guide)
- **Examples:** Always review the files in the [examples/](examples/) directory to see the expected standard of completeness.
- **Templates:** Always use [templates/template-dbt-model.md](./templates/template-dbt-model.md) for new repo notes.
- **UIDs:** Generate a FRESH, unique timestamp UID (`YYYYMMDDHHMM`) for EVERY individual file created, even if they belong to the same Triad. Do not share UIDs. Strict naming format: `[UID]-[prefix]_descriptive_title_[suffix].md`.
- **Updating Existing Notes (In-Place Evolution):** If asked to update an existing model's documentation, DO NOT change its filename or UID. Update the `Last Verified Commit`, modify the column logic to match the new SQL, and append new Fleeting/Knowledge links if necessary.
- **Column Lineage:** EVERY column must have `Logic:` and `Origin:` details linking to upstream models.
- **Tombstone Pattern:** NEVER delete deprecated notes. Rename to `...-DEPRECATED-...` and fill out the deprecation section.

## CLI Query Engine (Sourced from the Guide)
Utilize these specific `rg` commands to navigate the Zettelkasten:
- **Trace Column Origin:** `rg -A 2 "\*\*\`[column_name]\`\*\*" 03-repos/`
- **Find Dependencies (1st Degree):** `rg "[UID]"`
- **Scope to Layer:** `rg "search_term" 03-repos/sales-analytics/reporting/`

## Link Validation Post-Edit
After creating or modifying any notes in the Zettelkasten, you MUST run [check_links.py](scripts/check_links.py) from the root directory by running `./dbt_zettelkasten/scripts/check_links.py` to verify that all relative file links and external URLs are intact. If broken links are found, correct them immediately.
