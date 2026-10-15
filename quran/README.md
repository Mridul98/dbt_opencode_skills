# 🧠 Quran Zettelkasten for AI Agents

![Actively Maintained](https://img.shields.io/badge/Maintenance-Active-brightgreen.svg)
[![AI Native](https://img.shields.io/badge/AI-Native-blue.svg)](#)
[![Domain](https://img.shields.io/badge/Domain-Quran_Study-2E8B57.svg)](#)

A specialized framework that empowers AI coding agents (**OpenCode**, **Claude Code**, **Claude Web**) to autonomously document, interlink, and query your study of the Quran using the same Zettelkasten ("Second Brain") mechanics as the [dbt framework](../knowledge_base/) — retooled for revelation instead of warehouses.

Your source of truth is a **local corpus** extracted from your own English PDF (here: *The Clear Quran*, Talal Itani), keyed by immutable `[surah:ayah]` refs. Every passage (ruku) you study becomes an atomic, linked, searchable note.

---

## 🏗️ The "Triad" Architecture (adapted)

1. **`03-mushaf/` (The What & Where):** one folder per surah (1:1 with the Mushaf). Holds the **surah index** (ruku table + arc) and **passage notes** — verse arcs, key terms, cross-references.
2. **`02-knowledge/` (The Why):** permanent thematic notes (guidance, covenant, charity vs usury...). Every interpretive claim carries a `Source:` label — named classical reference, consensus, observable corpus fact, or explicit agent inference.
3. **`01-fleeting/` (The Observations):** questions, edition/numbering caveats, memorization snags, tensions — with concrete Next Steps.
4. **`corpus/` (read-only):** `sNNN_surah.md` files extracted from the PDF; each ayah line starts with its `[s:a]` primary key. Never edited; it is the "SQL" of this brain.

## 🤖 The Two Skills

* **`quran-zettelkasten`** (Writer): discovers the brain, reads the perfect examples first (anti-skeleton policy), documents ruku passages into the Triad with fresh UIDs (`YYYYMMDDHHMM-p00201_...`), and validates links after every batch.
* **`quran-query`** (Reader): read-only synthesis over the brain via `rg` — find where the Quran says X, which passages feed a theme, what a ruku covers, and what is still unverified.

## 🚀 Installation

```bash
cp -r quran/quran_zettelkasten ~/.config/opencode/skills/
cp -r quran/quran_query ~/.config/opencode/skills/
```

Prerequisites: `ripgrep` (`rg`), `python3`, and for corpus extraction the `pypdf`/`pymupdf` pip packages.

**First time — extract the corpus from your PDF:**
```bash
python3 ~/.config/opencode/skills/quran_zettelkasten/scripts/extract_pdf.py \
  --pdf /path/to/your-quran.pdf --out ~/quran_second_brain/corpus
```
Validation line must report `surahs written: 114 | total ayahs: 6236 | anomalies: 0`.

## 💬 Prompt Playbook

> `/skill quran-zettelkasten Initialize the second brain at ~/quran_second_brain and document Surah 1.`

> `/skill quran-zettelkasten Continue the full-Quran build from BUILD_STATE.json.`

> `/skill quran-query Where does the Quran discuss the people of the Book vs the hypocrites, and how are they characterized?`

> `/skill quran-query Which knowledge note covers guidance, and which passages feed it?`

## 📋 What carries over from the dbt framework

Strict UID birth-timestamps; directory-as-tag hierarchy; anti-laziness/anti-skeleton with mandatory perfect examples; in-place evolution (never change a UID); the Tombstone pattern for superseded understanding (`-DEPRECATED-` + bi-directional link); link validation post-edit; Writer/Reader skill split; and a resumable batch pipeline (`BUILD_STATE.json`) for mass documentation.
