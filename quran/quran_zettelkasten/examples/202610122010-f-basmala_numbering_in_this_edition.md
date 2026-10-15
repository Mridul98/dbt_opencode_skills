# Basmala is unnumbered in this edition except 1:1 — a numbering decision, not a neutral layout
**UID:** 202610122010
**Type:** Fleeting / Scratchpad
**Date:** 2026-10-13

## Context
Documenting the first passage [The Quran in miniature (1:1–7)](202610121930-p00101_fatihah_r1_the_quran_in_miniature.md) and noticing how the extracted corpus renders the basmala everywhere else.

## Observation / Question
In the corpus (Itani, ClearQuran edition A — Kufi/6236 numbering):

* `corpus/s001_al-fatihah.md` prints the basmala **as numbered ayah `[1:1]`**: "In the name of Allah, the Gracious, the Merciful."
* Every other surah file carries it as an **unnumbered header line** (`Basmala: In the name of Allah, the Gracious, the Merciful`), e.g., the header rows of `s002_al-baqarah.md`, `s027_an-naml.md`, `s055_ar-rahman.md` — a layout choice the extractor captured from the book's title pages.
* `s009_at-tawbah.md` has **no Basmala header at all** — matching the transmitted exception for surah 9.
* The single numbered place the phrase appears mid-surah is Solomon's letter: `[27:30]` "It is from Solomon, and it is, 'In the Name of Allah, the Gracious, the Merciful." (capital "Name" — a distinct rendering in quoted-letter context).

The question this raises: **the edition's numbering treats the basmala as an ayah only in al-Fatihah.** The widely cited legal positions are: Shafi'i — a numbered ayah at the head of every surah (except 9); Hanafi — an ayah in the Fatihah only (as here); Maliki/Hanbali narrations — not an ayah at all. If that is right, the corpus layout is exactly the Hanafi/Kufan position made typographic, which fits the 556-ruku (Idad-e-Quran) scheme we use for passage boundaries.

Consequences to watch:
* Quoting "verse counts" per surah from this corpus is the 6236 scheme; in mushaf editions that number the section-opening basmala as ayah 1, the first verse of every surah (except 9 and 1) shifts, and subsequent refs drift by one. Pin all `[s:a]` refs to this corpus's scheme.
* If a knowledge note ever treats "the basmala opens every surah" as a *verse*, it will be citing this edition's layout, not agreed ayah status. Keep the two claims separate.

## Next Steps
- [ ] Verify the madhhab positions against a primary tafsir source (Ibn Kathir / al-Qurtubi on 1:1 and on the "two surahs without basmala" question) before any Knowledge note restates them.
- [ ] Check where else this corpus's numbering could mislead: `rg -l "In the name of Allah" corpus/` (all headers) vs `rg "\[.*\] In the name" corpus/` (numbered occurrences only) — confirm 1:1 and 27:30 are the only numbered ones.
- [ ] Consider a Knowledge note "Basmala: status, placement, and what each reading changes" once verified — it would link Fatihah r1, an-Naml, and at-Tawbah indexes.

## Related Notes
* [The Quran in miniature (1:1–7)](202610121930-p00101_fatihah_r1_the_quran_in_miniature.md)
* [Guidance (hudan) and its conditions](202610122000-k-guidance_hudan_lil_muttaqin.md)
* [Surah al-Baqarah index](202610122020-s002_index_al-baqarah.md)
