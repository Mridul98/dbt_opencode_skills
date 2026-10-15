---
name: quran-query
description: Trace ayah cross-references, understand Quranic themes, and assess which passages feed a concept — via the Quran Zettelkasten.
---
# Skill: Query Quran Brain

## Core Directive
This skill is designed for **read-only retrieval and synthesis**. When loaded, you must use the CLI tools provided below to deeply interrogate the Quran Second Brain (and its `corpus/`). Your primary objective is to trace themes, locate passages, explain business-of-revelation logic (creed, law, narrative patterns), and assess "what connects to what" by synthesizing information across the note layers (Fleeting, Knowledge, Mushaf) and the immutable corpus.

**CRITICAL RULE:** Always cite your sources. Reference the specific `[surah:ayah]` refs and note UIDs/filenames you derived the answer from. When quoting translation text, quote the `corpus/` line verbatim — never from memory.

## The Layer Traversal Protocol
1. **Passage notes (`03-mushaf/sNNN_*/`):** the "What & Where" — verse arcs, key terms, cross-references, per-ruku thesis.
2. **Surah index (`...sNNN_index_*.md`):** the table of contents and structural arc of each surah.
3. **Knowledge (`02-knowledge/`):** the "Why" — enduring thematic concepts with `Source:` labels.
4. **Fleeting (`01-fleeting/`):** the honest caveats — open questions, numbering/edition warnings, unverified inferences.
*Synthesis requires reading all layers that surface, and surfacing a Knowledge note's `Source:` label in your answer.*

## CLI Query Playbook
Use `rg` (ripgrep) via your Bash tool. The brain root defaults to the location the user confirms (e.g., `~/quran_second_brain`).

### 1. "Where does the Quran say X?" (concept discovery)
```bash
rg -i -l "search_term" <brain>/02-knowledge/
rg -i "search_term" <brain>/corpus/ -l        # raw text hits
```

### 2. "What does this passage mean?" (passage lookup)
```bash
rg -l "\[2:255\]" <brain>/03-mushaf/ <brain>/02-knowledge/
rg "^\[2:254\]|^\[2:255\]|^\[2:256\]|^\[2:257\]" <brain>/corpus/s002_al-baqarah.md
```

### 3. Which passages feed a theme? (impact analysis)
```bash
rg -l "k-guidance_hudan" <brain>/03-mushaf/
```

### 4. Trace an ayah ref across the whole brain (lineage)
```bash
rg -c "\[1:6\]" <brain>/            # which notes and how often
```

### 5. Ruku boundary lookup (what passage contains this ayah?)
```bash
rg '"surah": 2' <skill_dir>/data/ruku_map.json -A 3   # then match the containing range
```

### 6. Key-term map within a surah
```bash
rg -i "righteous|piety" <brain>/03-mushaf/s002_al-baqarah/ -l
```

### 7. Superseded understanding / open caveats
```bash
rg -l "DEPRECATED" <brain>/03-mushaf/
rg -i "unverified|agent inference" <brain>/02-knowledge/
```

## Synthesis Guidelines
When answering the user based on your queries:
1. **Understand First:** Run the necessary `rg` commands in parallel. When a passage note surfaces, follow its links: surah index row, Knowledge notes, Fleeting notes.
2. **Ground the Quote:** Pull the actual line from `corpus/` for anything you present as translated text.
3. **Synthesize:** Combine the verse arc (Mushaf layer) with the theme (`Source:`-labeled knowledge) and honor any Fleeting caveat relevant to the refs.
4. **Answer:** Provide a clear, concise answer.
5. **Cite:** Mention the `[s:a]` refs, passage UIDs, and note names used. If the brain has no relevant notes yet, say so and answer from corpus lines directly, marked as un-documented.
