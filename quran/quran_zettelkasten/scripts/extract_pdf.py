#!/usr/bin/env python3
"""Extract the Clear Quran (Talal Itani) PDF into a rg-searchable corpus.

One markdown file per surah under <out>/, every ayah line prefixed with its
stable primary key [surah:ayah] (standard Kufi numbering, total 6236).

Usage:
  python3 extract_pdf.py [--pdf PATH] [--out DIR] [--manifest PATH]
"""
import argparse
import json
import re
import sys
from pathlib import Path

import pymupdf

BODY_START_PAGE = 11  # 0-indexed PDF page where surah 1 begins

# Surah titles in the book may span "N. ALL CAPS TITLE" + "(translit)" lines,
# or a single "N. ALL CAPS TITLE (translit)" page header.
PAREN_RE = re.compile(r"^(\d{1,3})\.\s+([A-Z][A-Z '\"\u2019\u201c-]+)\s+\(([^)]+)\)\s*$")
INLINE_RE = re.compile(r"^(\d{1,3})\.\s+([A-Z][A-Z '\"\u2019\u201c-]+)\s*$")
TRANSLIT_RE = re.compile(r"^\(([^)]+)\)\s*$")
FOOTER_RE = re.compile(r"^\d{1,3}\s*$")
AYAH_RE = re.compile(r"^(\d{1,4})\.\s+(.*)$")
BASMALA_1 = re.compile(r"^In the name of Allah,?(\s+the Gracious,?)?(\s+the Merciful)?\.?$", re.I)
BASMALA_2 = re.compile(r"^(\s*the Gracious,\s+)?the Merciful\.?$", re.I)
DOT_LEADER = re.compile(r"\.{4,}")
ALLCAPS_TEXT = re.compile(r"^[A-Z][A-Z '\"\u2019\u201c-]*$")


def slugify(name: str) -> str:
    s = name.replace("‘", "'").replace("’", "'")
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s


def process_lines(doc, manifest_counts):
    """Ayah-number-driven segmentation.

    Truth: ayah numbers restart at 1 exactly when a new surah starts. Page
    headers/titles are annotations captured as metadata (a page header can
    announce the surah that begins later on the same page).
    """
    surahs = {}
    cur = None            # current surah number
    exp_ayah = 1          # next expected ayah number in current surah
    pending_title = None  # (num, name, translit) awaiting its "1." ayah
    pending_basmala = []  # basmala line fragments awaiting the "1." ayah
    anomalies = []

    def open_surah(num):
        nonlocal cur, exp_ayah, pending_title, pending_basmala
        cur = num
        exp_ayah = 1
        title = pending_title if pending_title and pending_title[0] == num else None
        pending_title = None
        surahs[num] = {
            "name": title[1] if title else "",
            "translit": title[2] if title else "",
            "basmala": " ".join(pending_basmala).strip(),
            "ayahs": {},
        }
        pending_basmala = []

    def note_title(num, name, translit):
        nonlocal pending_title
        if cur is not None and num == cur:
            if name and not surahs[num]["name"]:
                surahs[num]["name"] = name
            if translit and not surahs[num]["translit"]:
                surahs[num]["translit"] = translit
        elif num == (cur + 1 if cur is not None else 1):
            if pending_title is None:
                pending_title = (num, name, translit)
            else:
                pending_title = (num, name or pending_title[1], translit or pending_title[2])
        elif cur is None or num > cur:
            pass  # header announcing a surah that begins further down the page
        else:
            anomalies.append(f"p{pno}: title num {num} regression (cur={cur})")

    for pno in range(BODY_START_PAGE, doc.page_count):
        lines = []
        for ln in doc[pno].get_text().splitlines():
            s = ln.strip()
            if not s or FOOTER_RE.match(s) or DOT_LEADER.search(s):
                continue
            lines.append(s)

        for s in lines:
            m = PAREN_RE.match(s)
            if m:
                note_title(int(m.group(1)), m.group(2).strip(), m.group(3).strip())
                continue
            m = INLINE_RE.match(s)
            if m and (cur is None or int(m.group(1)) in (cur, cur + 1)):
                num = int(m.group(1))
                note_title(num, m.group(2).strip(), "")
                continue
            if s.startswith("(") and s.endswith(")"):
                t = TRANSLIT_RE.match(s)
                if t and pending_title:
                    pending_title = (pending_title[0], pending_title[1], t.group(1).strip())
                    continue
            if BASMALA_1.match(s) or BASMALA_2.match(s):
                pending_basmala.append(s)
                continue

            m = AYAH_RE.match(s)
            if m:
                n = int(m.group(1))
                if n != exp_ayah:
                    if n == 1:
                        new_num = 1 if cur is None else cur + 1
                        if new_num != n and cur is not None and new_num != cur + 1:
                            anomalies.append(f"p{pno}: suspicious restart at surah {new_num}")
                        open_surah(new_num)
                        surahs[cur]["ayahs"][1] = m.group(2)
                        exp_ayah = 2
                        continue
                    anomalies.append(
                        f"p{pno}: ayah start {n} out of sync (surah={cur} exp={exp_ayah}) text={m.group(2)[:40]!r}"
                    )
                else:
                    if cur is None:
                        open_surah(1)
                    surahs[cur]["ayahs"][n] = m.group(2)
                    exp_ayah += 1
                    continue
            # continuation of previous ayah (dehyphenate)
            if cur is None:
                anomalies.append(f"p{pno}: orphan before first surah: {s[:60]!r}")
                continue
            prev = surahs[cur]["ayahs"].get(exp_ayah - 1)
            if prev is None:
                anomalies.append(f"p{pno}: no previous ayah for continuation: {s[:60]!r}")
                continue
            if ALLCAPS_TEXT.match(s):
                continue  # stray all-caps title echo
            hyphen_compounds = {"a", "an", "one", "two", "three", "four", "five",
                                "six", "seven", "eight", "nine", "ten", "half"}
            prev_word = prev[:-1].rsplit(" ", 1)[-1].lower() if prev.endswith("-") else ""
            if prev.endswith("-") and s[:1].islower():
                if prev_word in hyphen_compounds:
                    surahs[cur]["ayahs"][exp_ayah - 1] = prev + s  # keep hyphen: "one-" + "third"
                else:
                    surahs[cur]["ayahs"][exp_ayah - 1] = prev[:-1] + s  # true wrap: "Mer-" + "ciful"
            else:
                surahs[cur]["ayahs"][exp_ayah - 1] = prev + " " + s
    return surahs, anomalies


def validate(surahs, manifest_counts):
    errors = []
    total = 0
    for num in range(1, 115):
        if num not in surahs:
            errors.append(f"surah {num} never detected")
            continue
        got = surahs[num]["ayahs"]
        seen_max = max(got) if got else 0
        expected = manifest_counts.get(num)
        missing = [n for n in range(1, seen_max + 1) if n not in got]
        if missing:
            errors.append(f"surah {num}: gaps at {missing[:10]}")
        if expected is not None and seen_max != expected:
            errors.append(f"surah {num}: pdf max ayah {seen_max} != manifest {expected}")
        total += seen_max
    return errors, total


def write_corpus(surahs, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    for num in sorted(surahs):
        info = surahs[num]
        fname = out_dir / f"s{num:03d}_{slugify(info['translit'] or info['name'])}.md"
        lines = [
            f"# Surah {num}: {info['name']} ({info['translit']})",
            "Source: The Clear Quran, English translation by Talal Itani "
            "(ClearQuran edition A; 'Allah' rendering)",
        ]
        if info["basmala"]:
            lines.append(f"Basmala: {info['basmala']}")
        lines.append("")
        for a in sorted(info["ayahs"]):
            text = info["ayahs"][a]
            lines.append(f"[{num}:{a}] {text}")
        fname.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(surahs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default="/mnt/e/quran-english-translation-clearquran-edition-allah.pdf")
    ap.add_argument("--out", default=str(Path.home() / "quran_second_brain" / "corpus"))
    ap.add_argument("--manifest", default=str(Path(__file__).resolve().parent.parent / "data" / "surah_manifest.json"))
    ap.add_argument("--emit-manifest", action="store_true",
                    help="overwrite the manifest from counts observed in the PDF")
    args = ap.parse_args()

    doc = pymupdf.open(args.pdf)
    manifest = json.loads(Path(args.manifest).read_text()) if Path(args.manifest).exists() else []
    manifest_counts = {m["number"]: m["ayahs"] for m in manifest}

    surahs, anomalies = process_lines(doc, manifest_counts)
    errors, total = validate(surahs, manifest_counts)

    n = write_corpus(surahs, Path(args.out))
    print(f"surahs written: {n} | total ayahs (max per surah): {total} | anomalies: {len(anomalies)}")
    for a in anomalies[:20]:
        print("  WARN:", a)
    for e in errors[:40]:
        print("  ERR:", e)

    if args.emit_manifest:
        data = [
            {"number": num, "ayahs": max(surahs[num]["ayahs"]), "name_en": surahs[num]["name"],
             "translit": surahs[num]["translit"]}
            for num in sorted(surahs)
        ]
        Path(args.manifest).write_text(json.dumps(data, indent=1) + "\n")
        print(f"manifest emitted from PDF -> {args.manifest}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
