# 🧠 dbt Zettelkasten for AI Agents

![Actively Maintained](https://img.shields.io/badge/Maintenance-Active-brightgreen.svg)
[![AI Native](https://img.shields.io/badge/AI-Native-blue.svg)](#)
[![Data Engineering](https://img.shields.io/badge/Domain-Data_Engineering-orange.svg)](#)
[![dbt Framework](https://img.shields.io/badge/Framework-dbt-FF694B.svg)](#)

A specialized framework that empowers AI coding agents (like **OpenCode**, **Claude Code**, or **Claude Web**) to autonomously document, map, and query your dbt data warehouse using a Zettelkasten ("Second Brain") methodology.

Instead of relying on scattered `schema.yml` files, this system forces the AI to document your data pipeline by separating the technical lineage, the business context, and the technical debt into an interconnected, searchable web of Markdown files.

---

## 📖 Table of Contents
- [Why dbt Zettelkasten?](#-why-dbt-zettelkasten)
- [Core Features](#-core-features)
- [The "Triad" Architecture](#️-the-triad-architecture)
- [The AI Skills (Agents)](#-the-ai-skills-agents)
- [Installation & Integration](#-installation--integration)
- [Usage & Prompt Playbook](#-usage--prompt-playbook)
- [System Prerequisites](#-system-prerequisites)
- [Directory Structure](#-directory-structure)

---

## ❓ Why dbt Zettelkasten?

Standard dbt documentation (`schema.yml` and `dbt docs`) is excellent for technical metadata but struggles with capturing complex domain knowledge.
*   **The Problem:** Business logic, architectural decisions ("Why did we choose cash vs. accrual accounting here?"), and technical debt warnings are often lost in Slack threads or disconnected Notion pages.
*   **The Solution:** By applying the Zettelkasten method directly to the codebase, AI agents can read a SQL model and instantly generate documentation that explicitly links the *technical transformation* (the code) to the *enduring business concept* (the knowledge) and the *temporary observation* (the tech debt).

---

## 🌟 Core Features

This framework is built with strict, prompt-engineered directives to ensure AI agents behave predictably and reliably over long-term projects:

*   **Autonomous Directory Discovery:** The AI will scan your workspace to find your centralized Second Brain before writing, preventing folder fragmentation.
*   **Strict UID Event Tracking:** Every concept receives a unique `YYYYMMDDHHMM` timestamp identifier at the exact moment of its creation. The DAG is tracked via these immutable UIDs.
*   **Surviving CRUD Operations:** The framework explicitly handles evolving code.
    *   *In-Place Evolution:* Minor SQL updates trigger an update to the text and commit hash while preserving the original UID.
    *   *The Tombstone Pattern:* Major refactors or deletions trigger a rigorous Tombstone replacement. The AI renames the old note to `-DEPRECATED-` and establishes bi-directional links to the new V2 note, preserving historical lineage.
*   **Automated Link Validation:** The AI runs a bundled Python script (`check_links.py`) after every edit to guarantee 100% referential integrity across the Markdown web.
*   **Anti-Laziness Directives:** The AI is explicitly forced to read "perfect examples" bundled in the repo before generating new documentation. This completely eliminates empty placeholders or skeleton outputs.

---

## 🏗️ The "Triad" Architecture

The system instructs the AI to generate a "Triad" of interlinked notes for every complex dbt model.

1. **`03-repos/` (The What & Where):** The technical map. Contains column-level lineage, grain definitions, and upstream/downstream dependencies. These notes mirror your physical dbt DAG.
2. **`02-knowledge/` (The Why):** The domain context. Permanent notes explaining the underlying business logic, architectural patterns, and metric definitions.
3. **`01-fleeting/` (The How it Felt):** The tech debt tracker. Scratchpad notes capturing anomalies, hardcoded values, or architectural warnings the AI discovers while reading the raw SQL.

---

## 🤖 The AI Skills (Agents)

This repository contains two distinct AI "Skills" (system prompts and workflows):

### 1. `dbt-zettelkasten` (The Writer)
The documentation engine. When invoked, the AI reads a raw dbt SQL model, generates unique timestamped UIDs, fills out the mandatory templates, and automatically cross-links the Triad of notes.

### 2. `query-second-brain` (The Reader)
A specialized read-only mode for retrieval. It instructs the AI to use `ripgrep` (`rg`) via CLI tools to rapidly traverse the existing Zettelkasten to answer complex domain questions, trace column origins, and perform downstream impact analysis.

---

## 🚀 Installation & Integration

### Option 1: Integrating with OpenCode (CLI Agent)
OpenCode natively supports custom skills via its configuration directory.

1. Clone this repository.
2. Copy the skill folders into your OpenCode config directory:
   ```bash
   cp -r knowledge_base/dbt_zettelkasten ~/.config/opencode/skills/
   cp -r knowledge_base/query-second-brain ~/.config/opencode/skills/
   ```
3. OpenCode will automatically register them. Trigger the skill directly using the `/skill` slash command in your terminal:
   ```bash
   /skill dbt-zettelkasten Document the newly created int_monthly_revenue.sql model
   ```

### Option 2: Running with Claude Code (CLI Agent)
Anthropic's `claude code` CLI tool relies on inline system prompts. Navigate to the directory containing your dbt models and explicitly invoke the skill name:
```bash
claude "Use the dbt-zettelkasten skill to document the int_monthly_revenue.sql model in this directory."
```

### Option 3: Integrating with Claude Projects (Web UI)
You can inject these skills directly into a Claude Project to give the web interface the context needed to document your pipeline.

1. **Create a new Project** in Claude.
2. **Upload Knowledge:** Add the following files to the project's knowledge base so Claude can reference the templates, rules, and perfect examples:
   * `DBT-ZETTELKASTEN-GUIDE.md`
   * The entire `templates/` directory
   * The entire `examples/` directory
3. **Custom Instructions:** Open the `SKILL.md` file (from either skill folder) and copy the entire text directly into the "Custom Instructions" box for the Claude Project.

---

## 💬 Usage & Prompt Playbook

Once the skills are loaded, try these advanced prompts to drive the AI:

#### 📝 Documenting a New Model
> `/skill dbt-zettelkasten Please create a complete second brain triad for the stg_stripe_payments model. Ensure you run the link checker afterward.`

#### 🔍 Tracing Logic & Lineage
> `/skill query-second-brain Trace the origin of the opportunity_rsac column. Where does it come from, what upstream tables feed it, and what is the business logic behind it?`

#### 💥 Impact Analysis
> `/skill query-second-brain If I alter the 'Revenue Recognition' knowledge note to shift from cash to accrual accounting, what downstream reporting models in the repo might be impacted?`

#### 🚨 Finding Tech Debt
> `/skill query-second-brain Search the fleeting notes to find any documented anomalies, brittle logic, or hardcoded filters related to the pipe_generation models.`

---

## 📋 System Prerequisites
If you are using this locally via OpenCode or another CLI agent, ensure the following are installed:
*   **`ripgrep` (`rg`):** The `query-second-brain` skill heavily relies on `rg` for lightning-fast traversal of the Zettelkasten across thousands of files.
*   **`python3`:** Required for the `check_links.py` validation script executed by the AI after writing documentation.

---

## 📁 Directory Structure Overview

How the system maps to your environment:

```text
~/.config/opencode/skills/        # Your AI Agent Config
├── dbt_zettelkasten/             # The Writer Skill
│   ├── SKILL.md
│   ├── DBT-ZETTELKASTEN-GUIDE.md
│   ├── templates/
│   ├── examples/
│   └── scripts/check_links.py
└── query-second-brain/           # The Reader Skill
    └── SKILL.md

/path/to/your/dbt/project/        # Your Active Workspace
├── ds_dbt/                       # Raw SQL Models
└── second_brain/                 # The AI Generated Zettelkasten
    ├── 01-fleeting/              
    ├── 02-knowledge/             
    └── 03-repos/                 
        └── ds_dbt/               # Maps 1:1 with your dbt project
```
