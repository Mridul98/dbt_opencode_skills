# 🤖 AI Skills for Data Engineering

![Actively Maintained](https://img.shields.io/badge/Maintenance-Active-brightgreen.svg)
[![AI Native](https://img.shields.io/badge/AI-Native-blue.svg)](#)
[![Data Engineering](https://img.shields.io/badge/Domain-Data_Engineering-orange.svg)](#)

This repository is a collection of advanced, prompt-engineered AI "Skills" designed to empower autonomous coding agents (like OpenCode and Claude Code). 

The primary focus of this repository is providing structured workflows that allow AI agents to safely and intelligently interact with complex Data Engineering environments.

---

## 🧠 The `knowledge_base` Framework
The core feature of this repository is the **dbt Zettelkasten** framework, located in the [`knowledge_base/`](./knowledge_base/) directory.

This framework shifts dbt documentation away from scattered YAML files and into an interconnected "Second Brain" of Markdown notes, tracking column-level lineage, business context, and technical debt.

It includes two distinct agent skills:
1.  **`dbt-zettelkasten`**: Instructs the AI to act as a technical writer, autonomously traversing dbt SQL files and generating highly-structured documentation.
2.  **`query-second-brain`**: Instructs the AI to act as an analyst, using fast CLI search tools to read the generated documentation and answer complex questions about downstream impact and business logic.

👉 **[Click here to read the full Knowledge Base documentation](./knowledge_base/README.md)** for installation instructions and usage examples.

---

## 🛠️ Repository Structure

```text
.
├── knowledge_base/               # The dbt Zettelkasten framework
│   ├── README.md                 # Detailed instructions for the framework
│   ├── dbt_zettelkasten/         # The Writer AI Skill
│   └── query-second-brain/       # The Reader AI Skill
└── README.md                     # You are here
```