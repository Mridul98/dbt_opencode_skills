# dbt Zettelkasten for OpenCode & Claude

A specialized framework that empowers AI coding agents (like OpenCode or Claude) to autonomously document, map, and query your dbt data warehouse using a Zettelkasten ("Second Brain") methodology.

Instead of relying on scattered `schema.yml` files, this system forces the AI to document your data pipeline by separating the technical lineage, the business context, and the technical debt into an interconnected web of Markdown files.

## 🧠 The "Triad" Methodology
This system instructs the AI to generate a "Triad" of notes for every complex dbt model. This separates concerns and makes the knowledge base highly searchable:

1. **`03-repos/` (The What & Where):** The technical map. Contains column-level lineage, grain definitions, and upstream/downstream dependencies. These notes mirror your dbt DAG.
2. **`02-knowledge/` (The Why):** The domain context. Permanent notes explaining the underlying business logic, architectural patterns, and metric definitions (e.g., "Why do we calculate Revenue Recognition this way?").
3. **`01-fleeting/` (The How it Felt):** The tech debt tracker. Scratchpad notes capturing anomalies, hardcoded values, or architectural warnings the AI discovers while reading the raw SQL.

## 🛠️ The Included AI Skills

This repository contains two distinct AI "Skills" (system prompts and workflows):

*   **`dbt-zettelkasten` (The Documentation Engine):** When invoked, the AI reads a raw dbt SQL model, generates unique timestamped UIDs, fills out the mandatory templates, and automatically cross-links the Triad of notes. It utilizes a bundled Python script (`check_links.py`) to guarantee no broken Markdown links exist in your Second Brain.
*   **`query-second-brain` (The Retrieval Engine):** A specialized read-only mode. It instructs the AI to use `ripgrep` (`rg`) to traverse the existing Zettelkasten to answer complex domain questions, trace column origins, and perform downstream impact analysis.

## 🔄 Recent Enhancements
To make the AI more autonomous, historically accurate, and robust against "lazy" generation, several major updates have been introduced to the framework:

*   **Strict Unique Event UIDs:** Moved from shared session UIDs to **Unique Event UIDs**. Every file now receives a fresh `YYYYMMDDHHMM` timestamp at its exact moment of creation to strictly adhere to pure Zettelkasten philosophy.
*   **Surviving CRUD Operations (The Tombstone Pattern):** The framework now explicitly instructs the AI on how to handle evolving code. Minor updates trigger an **In-Place Evolution** (updating the text and commit hash while preserving the UID). Major refactors trigger a rigorous **Tombstone replacement**, establishing bi-directional links between the `-DEPRECATED-` legacy note and the new V2 note to preserve the historical DAG.
*   **Anti-Laziness Directive & Verified Examples:** Added a bundled `examples/` directory containing a perfectly interlinked Triad. The AI is now bound by a "CRITICAL" prompt directive to read these examples before generating documentation, completely eliminating placeholder/skeleton outputs.
*   **Mandatory Triad Connectivity:** The AI is now explicitly forced to link the generated Fleeting and Knowledge notes at the bottom of the Model note (`## 6. Related Notes`), guaranteeing the Triad is never disconnected.
*   **Directory Discovery Protocol:** Added a "Step 0" check. The AI will actively search your workspace for the centralized Zettelkasten (`01-fleeting`, `02-knowledge`, `03-repos`) and ask for your confirmation before proactively running `mkdir` to prevent folder fragmentation.

---

## 🚀 Integration Guide

### Option 1: Integrating & Running with OpenCode (CLI Agent)
OpenCode natively supports custom skills.

1. Clone this repository.
2. Copy the skill folders into your OpenCode config directory:
   ```bash
   cp -r skills/dbt_zettelkasten ~/.config/opencode/skills/
   cp -r skills/query-second-brain ~/.config/opencode/skills/
   ```
3. Trigger the skill directly using the `/skill` slash command in your terminal:
   ```bash
   /skill dbt-zettelkasten Document the newly created int_monthly_revenue.sql model
   ```

### Option 2: Running with Claude Code (CLI Agent)
If you are using Anthropic's `claude code` CLI tool, it relies on system prompts. Navigate to the directory containing your dbt models and explicitly call the skill name in your inline prompt:
```bash
claude "Use the dbt-zettelkasten skill to document the int_monthly_revenue.sql model in this directory."
```

### Option 3: Integrating with Claude Projects (Web UI)
You can inject these skills directly into a Claude Project to give it the context needed to document your pipeline.

1. **Create a new Project** in Claude.
2. **Upload Knowledge:** Add the following files to the project's knowledge base so Claude can reference the templates and rules:
   * `DBT-ZETTELKASTEN-GUIDE.md`
   * The entire `templates/` directory
   * The entire `examples/` directory
3. **Custom Instructions:** Open the `SKILL.md` file (from either skill folder) and copy the entire text directly into the "Custom Instructions" box for the Claude Project.

---

## 📋 System Prerequisites (For CLI Usage)
If you are using this locally via OpenCode or another CLI agent, ensure the following are installed:
*   **`ripgrep` (`rg`):** The `query-second-brain` skill heavily relies on `rg` for lightning-fast traversal of the Zettelkasten.
*   **`python3`:** Required for the `check_links.py` validation script executed by the AI after writing documentation.

---

## 💬 Usage Examples (Prompting the AI)

Once the skills are loaded, try these prompts:

**Documenting a New Model:**
> `/skill dbt-zettelkasten Please create a second brain triad for the stg_stripe_payments model.`

**Tracing Logic & Lineage:**
> `/skill query-second-brain Trace the origin of the opportunity_rsac column. Where does it come from, and what is the business logic behind it?`

**Impact Analysis:**
> `/skill query-second-brain If I alter the 'Revenue Recognition' knowledge note, what downstream models in the repo might be impacted?`

**Finding Tech Debt:**
> `/skill query-second-brain Search the fleeting notes to find any documented anomalies or hardcoded filters related to the pipe_generation models.`
