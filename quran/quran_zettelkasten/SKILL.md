---
name: quran-zettelkasten
description: Document Quran passages (ruku) into an interconnected Second Brain, build thematic knowledge notes, or trace ayah cross-references.
---
# Skill: Quran Zettelkasten

## Core Directive
Before starting any documentation task, you MUST read and adhere to the project's official rulebook bundled with this skill.

*Note to Agent: The guide ([QURAN-ZETTELKASTEN-GUIDE.md](QURAN-ZETTELKASTEN-GUIDE.md)), the `templates/` directory, and the `data/` files (ruku_map.json, surah_manifest.json) are located in the exact same folder as this SKILL.md file. Use your knowledge of the skill's file path to locate and read them.*

## 0. Directory Discovery (MANDATORY FIRST STEP)
Before creating ANY notes or directories, you must locate the existing Quran Second Brain.
1. Search the workspace with `glob`/`bash` for the standard folders (`01-fleeting`, `02-knowledge`, `03-mushaf`, `corpus`) — check the user's home and the current working tree.
2. The corpus MUST exist (`corpus/sNNN_*.md`). If missing, run the bundled extractor: `python3 scripts/extract_pdf.py --pdf <path> --out <brain>/corpus` and report the validation line (must show 114 surahs / 6236 ayahs / 0 anomalies).
3. Prompt the user with the probable brain root(s) you found and ask them to confirm the target directory.
4. **DO NOT** proactively create top-level directories unless the user confirms this is a brand-new initialization.
5. **Dynamic Surah Folders:** If documenting a surah for the first time, you MAY create `03-mushaf/s<NNN>_<slug>/` inside an existing `03-mushaf/`.

## 1. Build-State Resume (check before any mass task)
If `BUILD_STATE.json` exists at the brain root, READ IT FIRST. Resume from the first pending surah; do not re-document completed ones (update them only if asked).

## Anti-Laziness Directive (CRITICAL)
When generating notes, you MUST NOT stop at creating skeletons. You must fully replace ALL `[Placeholder]` tags with actual, deeply researched content anchored to the local corpus.

Before writing a note, you MUST read its corresponding perfect example to understand the expected outcome and level of detail:
- For Passage Notes: Read [examples/202610121930-p00101_fatihah_r1_the_quran_in_miniature.md](examples/202610121930-p00101_fatihah_r1_the_quran_in_miniature.md)
- For Surah Index Notes: Read [examples/202610122020-s002_index_al-baqarah.md](examples/202610122020-s002_index_al-baqarah.md)
- For Knowledge Notes: Read [examples/202610122000-k-guidance_hudan_lil_muttaqin.md](examples/202610122000-k-guidance_hudan_lil_muttaqin.md)
- For Fleeting Notes: Read [examples/202610122010-f-basmala_numbering_in_this_edition.md](examples/202610122010-f-basmala_numbering_in_this_edition.md)

* **Source of Truth:** All verse text must be copied from `corpus/`, never from memory. Quote or excerpt using the exact `[s:a]` refs.
* **Triad Connectivity:** Link every new Passage note to its Surah Index row, and attach the Fleeting/Knowledge notes under `## 7. Related Notes`. Deduplicate Knowledge notes: link to an existing theme note instead of creating near-copies.
* **Tafsir Honesty:** Every interpretive claim in a Knowledge or Passage note carries a `Source:` label (named classical reference, consensus, observable corpus fact, or explicit agent inference). NEVER invent an attribution.
* **Handling Deprecation:** Ignore `-DEPRECATED-` files in standard search/linking. Exception: during a Tombstone replacement, cross-link old and new to preserve the study lineage.

## Quick Reference (Sourced from the Guide)
- **Templates:** [templates/template-passage.md](./templates/template-passage.md), [templates/template-surah-index.md](./templates/template-surah-index.md), [templates/template-knowledge.md](./templates/template-knowledge.md), [templates/template-fleeting.md](./templates/template-fleeting.md)
- **UIDs:** Generate a FRESH `YYYYMMDDHHMM` UID per file, even within one Triad. Format: `[UID]-[prefix]_descriptive_title.md` with prefixes `p<SSSSRR>_`, `s<NNN>_index_`, `k-`, `f-`.
- **Ayah refs:** Always `[surah:ayah]` (e.g., `[2:255]`) — the stable primary key for all searches.
- **Updating Existing Notes:** DO NOT change filename/UID on refinement. Update `Last Studied`, evolve content in place, and append any new Fleeting/Knowledge links.
- **Tombstone Pattern:** NEVER delete superseded notes; rename to `...-DEPRECATED-...`, fill `## 5. Superseded Notes`, and bi-directionally link the V2 note.

## CLI Query Engine (Sourced from the Guide)
Utilize these specific `rg` commands to navigate the Zettelkasten:
- **Trace Ayah Usage:** `rg -l "\[2:255\]" <brain>/`
- **Find Term Across Layers:** `rg -i "sirat|straight path" <brain>/03-mushaf/ <brain>/02-knowledge/`
- **Theme Impact:** `rg -l "<knowledge-note-uid-or-slug>" <brain>/03-mushaf/`
- **Ruku Boundaries:** `rg '"surah": 2' data/ruku_map.json -A 3`
- **Pull Passage Text:** `rg "^\[2:1\]" <brain>/corpus/s002_al-baqarah.md`

## Link Validation Post-Edit
After creating or modifying any notes, you MUST run [check_links.py](scripts/check_links.py) against the brain root (`python3 scripts/check_links.py <second_brain_root>`) to verify all relative file links resolve. If broken links are found, correct them immediately. During mass builds, run it per ~10-surah batch and once at full completion.
