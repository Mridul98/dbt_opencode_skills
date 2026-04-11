---
name: query-second-brain
description: Trace data lineage, understand business logic, and assess downstream impact in the dbt Zettelkasten
---
# Skill: Query Second Brain

## Core Directive
This skill is designed for **read-only retrieval and synthesis**. When loaded, you must use the CLI tools provided below to deeply interrogate the dbt Zettelkasten. Your primary objective is to trace data lineage, understand business logic, and assess downstream impact by synthesizing information across the three note layers (Fleeting, Knowledge, and Repos).

**CRITICAL RULE:** Always cite your sources. When providing an answer, reference the specific UIDs or file names of the notes you derived the information from.

## The "Triad" Traversal Protocol
The Zettelkasten is built on a Triad structure. When you find a relevant Repo note (`03-repos`) containing technical column lineage, you **MUST** look for its corresponding Knowledge (`02-knowledge`) and Fleeting (`01-fleeting`) notes using the identical UID. 
*   **Repos (`03-repos`):** Contains the "What" and "Where" (Column lineage, grain, dependencies).
*   **Knowledge (`02-knowledge`):** Contains the "Why" (Core business concepts, architectural decisions).
*   **Fleeting (`01-fleeting`):** Contains the "How it felt" (Observations, tech debt warnings).
*Synthesis requires reading all three to provide a complete answer.*

## CLI Query Playbook
Utilize these specific `rg` (ripgrep) commands via your Bash tool to navigate and extract answers from the Zettelkasten:

### 1. Tracing Column Logic and Origin
To find exactly how a specific column is calculated and where it comes from:
```bash
rg -A 5 "\*\*\`[column_name]\`\*\*" dbt_zettelkasten/03-repos/
```

### 2. Impact Analysis (Downstream Dependencies)
To find all models that depend on a specific upstream model (replace `[UID]` with the 12-digit ID):
```bash
rg -l "[UID]" dbt_zettelkasten/03-repos/
```

### 3. Concept Discovery (Business Logic)
To search exclusively in the knowledge layer to understand how business concepts (e.g., "ARR", "EAV") are defined:
```bash
rg -i -l "search_term" dbt_zettelkasten/02-knowledge/
```

### 4. Domain / Tag Filtering
To find all models associated with a specific domain or tag (e.g., `zendesk`, `arr_sst`):
```bash
rg -l "tags:.*\[.*[tag_name].*\]" dbt_zettelkasten/
```

### 5. Finding Deprecated Models
To find models that have been marked as deprecated (Tombstone Pattern):
```bash
rg -l "DEPRECATED" dbt_zettelkasten/03-repos/
```

## Synthesis Guidelines
When answering the user based on your queries:
1.  **Understand First:** Run the necessary `rg` commands in parallel. If you find a UID, run `cat` on the Repo, Knowledge, and Fleeting notes for that UID.
2.  **Synthesize:** Combine the technical lineage from the Repo note with the business context from the Knowledge note.
3.  **Answer:** Provide a clear, concise answer.
4.  **Cite:** Mention the UIDs or model names you used to formulate your answer.