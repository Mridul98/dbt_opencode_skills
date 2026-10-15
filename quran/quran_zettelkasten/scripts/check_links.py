#!/usr/bin/env python3
"""Link validator for the Quran Zettelkasten.

Usage:
    python3 check_links.py [root]   # root defaults to the current working directory
                                      # (run it from your Quran Second Brain root)

Traverses all .md files under root, verifies every relative markdown link
resolves to an existing file, and checks external URLs are reachable.
"""
import os
import sys
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse
from pathlib import Path
import concurrent.futures

IGNORED_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__"}
LINK_REGEX = re.compile(r"\[.*?\]\((.*?)\)")


def is_ignored(path):
    for part in path.parts:
        if part in IGNORED_DIRS:
            return True
    return False


def check_url(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        req = urllib.request.Request(url, method="HEAD", headers=headers)
        urllib.request.urlopen(req, timeout=5)
        return True, ""
    except urllib.error.HTTPError as e:
        if e.code in [403, 405, 400]:
            try:
                req = urllib.request.Request(url, method="GET", headers=headers)
                urllib.request.urlopen(req, timeout=5)
                return True, ""
            except Exception as e2:
                return False, f"HTTP Error: {e2}"
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def check_link(file_path, link):
    if link.startswith("mailto:"):
        return True, ""
    link_no_anchor = link.split("#")[0]
    if not link_no_anchor:
        return True, ""
    parsed = urlparse(link_no_anchor)
    if parsed.scheme in ("http", "https"):
        return check_url(link_no_anchor)
    try:
        target = (file_path.parent / link_no_anchor).resolve()
        if target.exists():
            return True, ""
        return False, "Local file not found"
    except Exception as e:
        return False, f"Invalid path: {e}"


def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    print(f"Scanning for markdown files under: {root}")
    markdown_files = [p for p in root.rglob("*.md") if not is_ignored(p)]

    all_links = []
    for mf in markdown_files:
        try:
            links = LINK_REGEX.findall(mf.read_text(encoding="utf-8"))
            for link in links:
                all_links.append((mf, link))
        except Exception as e:
            print(f"Error reading {mf}: {e}")

    if not all_links:
        print("No links found to check.")
        sys.exit(0)

    print(f"Checking {len(all_links)} links across {len(markdown_files)} files...")
    broken_links = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_link = {
            executor.submit(check_link, fp, link): (fp, link) for fp, link in all_links
        }
        for future in concurrent.futures.as_completed(future_to_link):
            fp, link = future_to_link[future]
            try:
                is_valid, error_msg = future.result()
                if not is_valid:
                    broken_links.append((fp, link, error_msg))
            except Exception as exc:
                broken_links.append((fp, link, str(exc)))

    if broken_links:
        print("\nBroken Links Found:")
        broken_by_file = {}
        for fp, link, err in broken_links:
            broken_by_file.setdefault(fp, []).append((link, err))
        for fp, links in broken_by_file.items():
            print(f"\n  {fp}")
            for link, err in links:
                print(f"    - {link} ({err})")
        sys.exit(1)
    else:
        print("\nAll links are healthy.")
        sys.exit(0)


if __name__ == "__main__":
    main()
