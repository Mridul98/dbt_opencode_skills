# CLI Zettelkasten for Quran Study

Welcome to your Second Brain for reading, understanding, and retaining the Quran. This system blends the atomic, linked nature of a Zettelkasten with a hierarchical directory structure that mirrors the physical Mushaf (114 surahs, 6,236 ayahs, 556 ruku). Instead of scattered highlights and bookmarks, every passage you study becomes a node in an interconnected, searchable web of Markdown notes.

## 1. Core Principles

### The Source of Truth
The AI never "quotes from memory." All translation text MUST come from the local corpus:

* **`corpus/sNNN_<surah-slug>.md`** — one file per surah, extracted from the user's English PDF (The Clear Quran, Talal Itani). Every line is keyed with a stable primary reference: **`[surah:ayah]`** (e.g., `[2:255]`).
* **`data/ruku_map.json`** (in this skill folder) — the 556-ruku (Hanafi/Idad-e-Quran) thematic partition: `{ruku_global, surah, ruku_in_surah, start, end, ayah_count}`. A **passage** is one ruku; its canonical ref is `surah:ruku` (e.g., `2:1`).

### File Naming (The UID System)
Every file must start with a timestamp **Unique Identifier (UID)**.
* **Format:** `YYYYMMDDHHMM-[prefix]_descriptive_title.md`
* **Unique Events:** Every file receives a fresh, unique timestamp at the exact moment of its creation. Do not share UIDs across a Triad.
* **Conventions (prefixes):**
  * Passage notes: `p<SSSSRR>_` — SSS = zero-padded surah, RR = zero-padded ruku-in-surah (e.g., `202610132100-p00201_baqarah_r1_the_book_as_guidance.md`)
  * Surah index notes: `s<NNN>_index_` (e.g., `202610132140-s002_index_al-baqarah.md`)
  * Knowledge notes: `k-` (e.g., `202610132115-k-guidance_hudan_lil_muttaqin.md`)
  * Fleeting notes: `f-` (e.g., `202610132120-f-basmala_numbering_in_this_edition.md`)
* **Why:** UIDs prevent naming collisions and mark the birth of the concept; strict prefixes allow instant identification of note type and lightning-fast global searches (e.g., `rg -g "*_index_*.md"`).

### Ayah References (The Primary Keys)
Unlike dbt models, the Quran's structure is immutable. **The `[s:a]` reference — never the UID — is the stable identity of revelation text.**
* Always write ayah references in bracketed numeric form: `[7:171]`. This exact token is what `rg` searches across the whole brain.
* Quote text by pasting the full `[s:a]` line from the corpus, or a short excerpt followed by `[s:a]`. NEVER paraphrase a verse and present it as a quote.

### Markdown Linking (The Web)
Links between notes represent thematic and structural relationships.
* **Format:** Standard Markdown — link text in square brackets, target in parentheses immediately after, with a relative path inside the parentheses.
* **Example shape:** `[Hudan lil-Muttaqin]` + `(../02-knowledge/UID-k-guidance_hudan_lil_muttaqin.md)` joined — the UID written at authoring time.
* **Why:** Standard links work everywhere (GitHub, VSCode, Neovim) and force consciousness of the physical hierarchy.
* **Assurance:** Make sure the links between notes are not broken (see Link Validation, Section 4).

---

## 2. The Hybrid Directory Structure (Schema)

**Note on Location:** A workspace should only have *one* centralized Quran Second Brain. Before adding notes, always verify the location of these core directories rather than blindly creating new ones in your current working path.

```text
<second_brain_root>/             # e.g., ~/quran_second_brain/
├── 01-fleeting/                 # Reflections, questions, memorization snags, tensions noticed
├── 02-knowledge/                # Permanent thematic notes: the "why" (creed, law, narrative patterns)
├── 03-mushaf/                   # The structural map, 1:1 with the Mushaf
│   └── s<NNN>_<surah-slug>/     # One folder per surah
│       ├── <UID>-s<NNN>_index_*.md          # Surah-level index note (114 total)
│       └── <UID>-p<SSSSRR>_*.md             # One passage note per ruku (~556 total)
├── corpus/                      # READ-ONLY source text (extracted from the PDF). Never edit.
└── templates/                   # (optional mirror) DO NOT modify.
```

* `03-mushaf/` is the "What & Where": what the text says (translation-anchored), how it is structured, where it connects.
* `02-knowledge/` is the "Why": enduring concepts that transcend a single passage (tawhid, sabr, covenant, riba, prophetic narrative cycles...).
* `01-fleeting/` is the "How it felt / what I noticed": open questions, apparent tensions, memorization trouble spots, action items for deeper study.

---

## 3. Adapting Notes for Quran Study

Do not just copy translation text. Use the Zettelkasten to explain the **structure**, the **theme**, and the **context**. Focus on meaningful ruku; a passage note exists to make the unit *understandable and retrievable*, not to re-typeset the surah.

### A. Document the Unit & Its Arc
The most critical part of a passage note is its **range and one-sentence thesis**.
* *Example:* "2:1–7 — The Book declares itself as guidance, then sorts humanity into three reactions to it."

### B. Capture Key Terms (the Lineage Analogue)
Every significant Arabic term gets `Term:`, `Rendering:`, and `Elsewhere:` details:
*Format:*
* **`muttaqin`** (Those conscious of God)
  * **Rendering:** "the righteous" in 2:2–3; "believers" context in 8:34.
  * **Elsewhere:** [2:197], [3:133], [49:13] — trace via `rg "\[49:13\]"` / term search.

### C. Record Cross-References
Parallel themes, echo-backs (e.g., Fatihah's "sirat" answered in Baqarah 1–7), Meccan↔Medinan resonances. Each as `[s:a]` refs with a one-line "why this link."

### D. Knowledge-Note Integrity (Tafsir Honesty)
Knowledge notes extract the "business logic" — but here the source is revelation, not code. Because the local corpus is a *translation only*, any interpretive claim MUST be labeled:
* **`Source:`** field — name the classical reference the point comes from (e.g., "Tafsir Ibn Kathir on 1:5", "al-Tabari on 2:5"), or state `Source: consensus of classical tafsir` / `Source: translator's term choice (observable in corpus)` / `Source: agent inference — verify`.
* Never fabricate a tafsir attribution. If in doubt, `Source: agent inference — verify` and raise a Fleeting note to check it.

---

## 4. Lifecycle Management (Surviving CRUD Operations)

A static Second Brain for an evolving understanding will fail. Treat notes like code: they change as your study deepens.

### Create
* Follow the Mandatory Triad Documentation rules (Section 6). Generate fresh UIDs for every new file.

### Update (In-Place Evolution)
When a note needs refinement (better theme summary, new cross-reference):
1. **DO NOT change the file's UID or filename.** The UID marks the birth of the note.
2. **Update the `Last Studied` metadata** to the current date.
3. **Evolve the Content:** add/remove Key Terms, Cross-References; keep the quote lines faithful to the corpus.
4. **Capture New Thoughts:** new observations spawn *new* Fleeting or Knowledge notes (fresh UIDs) linked at the bottom of the existing passage note.

### Reinterpret (The Tombstone Pattern)
When a note's understanding is fundamentally superseded (e.g., you re-read a passage and the thesis changes):
1. Rename the file to include `-DEPRECATED-`.
2. Fill out `## 5. Superseded Notes`: date, reason, and a link to the new V2 note.
3. Do NOT delete its existing links — they preserve the historical study lineage.
4. Create the V2 note (fresh UID) and link *backward* to the `-DEPRECATED-` note.

### Link Validation
After any batch of edits, run the bundled checker from the brain root:
```bash
python3 <skill_dir>/scripts/check_links.py <second_brain_root>
```
It traverses all `.md` files and fails on broken internal links. Fix any broken links immediately.

---

## 5. CLI Query Engine Mastery

The terminal is the search engine. Use `ripgrep` (`rg`).

### 🔍 Find an ayah reference everywhere
```bash
rg -l "\[2:255\]" <brain>/   # which notes discuss the Throne verse
```

### 🔍 Trace a key term across the brain
```bash
rg -i "sirat|straight path" <brain>/03-mushaf/ <brain>/02-knowledge/
```

### 🔍 Pull a passage's actual text (from the immutable corpus)
```bash
rg "^\[2:1\]|^\[2:7\]" <brain>/corpus/s002_al-baqarah.md
```

### 🔍 Which passages feed a theme? (downstream impact)
```bash
rg -l "k-guidance_hudan_lil_muttaqin" <brain>/03-mushaf/
```

### 🔍 List a surah's passage notes in order
```bash
ls <brain>/03-mushaf/s002_al-baqarah/ | rg "^.*-p002\d\d_"
```

### 🔍 Ruku boundaries for a surah
```bash
rg '"surah": 2' <skill_dir>/data/ruku_map.json -A 3
```

### 🔍 Find superseded understandings
```bash
rg -l "DEPRECATED" <brain>/03-mushaf/
```

---

## 6. Mandatory Triad Documentation

When documenting a passage (ruku) of the Quran, you must create a triad of interlinked notes:

*   **Passage Note (`03-mushaf/sNNN_<slug>/`)**: the structural map of one ruku — range, thesis, verse-by-verse arc (quoting the corpus faithfully), key terms, cross-references, and links to its Knowledge and Fleeting notes.
    *   **🎯 Expected Outcome:** A reader can re-learn the passage from your note alone and find every ayah ref instantly. No bare quotes without explanation.
    *   **📄 Reference Example:** `examples/202610121930-p00101_fatihah_r1_the_quran_in_miniature.md`
*   **Surah Index Note (same folder)**: one per surah (114 total). Revelation context (Meccan/Medinan by classical order), total ayahs/ruku, the ruku table with links to each passage note, the surah's central theme and structure.
    *   **🎯 Expected Outcome:** A table of contents + 3-sentence orientation for the surah, every row linked.
    *   **📄 Reference Example:** `examples/202610122020-s002_index_al-baqarah.md`
*   **Knowledge Note (`02-knowledge/`)**: an enduring thematic concept extracted from one or more passages, with the tafsir-honesty `Source:` discipline from Section 3D.
    *   **🎯 Expected Outcome:** A distilled, stable explanation of a concept (creed, law, motif, narrative pattern) that transcends any single ruku and links back to supporting passages.
    *   **📄 Reference Example:** `examples/202610122000-k-guidance_hudan_lil_muttaqin.md`
*   **Fleeting Note (`01-fleeting/`)**: an honest observation — a tension, a question, a memorization snag, a term-choice quirk visible in this specific edition.
    *   **🎯 Expected Outcome:** An actionable brain-dump with concrete "Next Steps."
    *   **📄 Reference Example:** `examples/202610122010-f-basmala_numbering_in_this_edition.md`

### 🛑 Anti-Skeleton Policy
Notes consisting only of template placeholders (e.g., leaving `[One-sentence thesis]` in the file) are INVALID. All fields must be filled with real, corpus-anchored content. Review the four `examples/` before writing anything.

### 🛑 Mass-Documentation Discipline (the build pipeline)
When asked to document the whole Quran (or many surahs at once):
1. Work strictly in **Mushaf order** (surah 1 → 114), one surah at a time: index note first, then passage notes in ruku order.
2. Update `BUILD_STATE.json` at the brain root after EACH surah completes: `{"completed_surahs": [...], "last_updated": "YYYY-MM-DD", "pending": [...]}`. On session start, READ IT FIRST and resume from the first pending surah.
3. Deduplicate knowledge notes: one canonical note per theme; new passages LINK to it rather than creating near-copies.
4. Fleeting notes only for genuine observations — do not manufacture filler.
5. Run the link checker at the end of every ~10-surah batch, and once on full completion.

Your Second Brain is now ready. Start by copying `templates/template-passage.md` into `03-mushaf/s001_al-fatihah/` and document the first ruku!
