#!/usr/bin/env python3
import os
import sys
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse
from pathlib import Path
import concurrent.futures

IGNORED_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__"}
# Regex to match markdown links: [text](link)
LINK_REGEX = re.compile(r"\[.*?\]\((.*?)\)")


def is_ignored(path):
    """Check if the path contains any ignored directories."""
    for part in path.parts:
        if part in IGNORED_DIRS:
            return True
    return False


def check_url(url):
    """Check if an external URL is reachable."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        # Try a fast HEAD request first
        req = urllib.request.Request(url, method="HEAD", headers=headers)
        urllib.request.urlopen(req, timeout=5)
        return True, ""
    except urllib.error.HTTPError as e:
        # Some servers block HEAD requests, fallback to GET
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
    """Determine link type and check its validity."""
    # Ignore mailto links
    if link.startswith("mailto:"):
        return True, ""

    # Strip URL anchors (e.g., #section-name)
    link_no_anchor = link.split("#")[0]

    # If the link was ONLY an anchor (e.g., [text](#anchor))
    if not link_no_anchor:
        return True, ""

    parsed = urlparse(link_no_anchor)

    # External HTTP/HTTPS link
    if parsed.scheme in ("http", "https"):
        is_valid, error = check_url(link_no_anchor)
        return is_valid, error
    else:
        # Internal file link
        try:
            # Resolve relative to the markdown file's parent directory
            target = (file_path.parent / link_no_anchor).resolve()
            if target.exists():
                return True, ""
            else:
                return False, "Local file not found"
        except Exception as e:
            return False, f"Invalid path: {e}"


def main():
    print("Scanning for markdown files...")
    # Determine the repository root dynamically based on the script's location
    # Since script is in dbt_zettelkasten/scripts/, we go up two levels to the root
    repo_root = Path(__file__).resolve().parent.parent.parent
    markdown_files = [p for p in repo_root.rglob("*.md") if not is_ignored(p)]

    all_links = []

    for mf in markdown_files:
        try:
            content = mf.read_text(encoding="utf-8")
            links = LINK_REGEX.findall(content)
            for link in links:
                all_links.append((mf, link))
        except Exception as e:
            print(f"Error reading {mf}: {e}")

    if not all_links:
        print("No links found to check.")
        sys.exit(0)

    print(f"Checking {len(all_links)} links across {len(markdown_files)} files...")

    broken_links = []

    # Use a thread pool to execute network requests in parallel for speed
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
        print("\n❌ Broken Links Found:")

        # Group broken links by file for cleaner output
        broken_by_file = {}
        for fp, link, err in broken_links:
            broken_by_file.setdefault(fp, []).append((link, err))

        for fp, links in broken_by_file.items():
            print(f"\n📄 {fp}:")
            for link, err in links:
                print(f"  - {link} ({err})")

        sys.exit(1)
    else:
        print("\n✅ All links are healthy!")
        sys.exit(0)


if __name__ == "__main__":
    main()
