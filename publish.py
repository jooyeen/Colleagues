#!/usr/bin/env python3
"""
Scans all .md files in the Obsidian vault for frontmatter with 'publish: true'
and copies them to the PUBLISH folder.
"""

import os
import shutil
import re
from pathlib import Path

VAULT_PATH = Path(__file__).parent
PUBLISH_PATH = VAULT_PATH / "PUBLISH"

def has_publish_frontmatter(filepath: Path) -> bool:
    """Check if a markdown file has 'publish: true' in its frontmatter."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return False

    # Check for YAML frontmatter (starts and ends with ---)
    if not content.startswith('---'):
        return False

    # Find the closing ---
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return False

    frontmatter = content[3:3 + end_match.start()]

    # Check for publish: true (handles various YAML formats)
    publish_pattern = r'^\s*publish\s*:\s*(true|yes|on)\s*$'
    return bool(re.search(publish_pattern, frontmatter, re.MULTILINE | re.IGNORECASE))

def main():
    # Ensure PUBLISH folder exists
    PUBLISH_PATH.mkdir(exist_ok=True)

    # Clear existing files in PUBLISH folder
    for item in PUBLISH_PATH.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

    # Find all markdown files (excluding PUBLISH folder and hidden directories)
    published_count = 0
    scanned_count = 0

    for md_file in VAULT_PATH.rglob('*.md'):
        # Skip files in PUBLISH folder, hidden folders, and .git
        relative = md_file.relative_to(VAULT_PATH)
        parts = relative.parts

        if any(part.startswith('.') or part == 'PUBLISH' for part in parts):
            continue

        scanned_count += 1

        if has_publish_frontmatter(md_file):
            dest = PUBLISH_PATH / md_file.name

            # Handle duplicate filenames by adding a suffix
            if dest.exists():
                stem = md_file.stem
                suffix = md_file.suffix
                counter = 1
                while dest.exists():
                    dest = PUBLISH_PATH / f"{stem}_{counter}{suffix}"
                    counter += 1

            shutil.copy2(md_file, dest)
            print(f"Published: {relative}")
            published_count += 1

    print(f"\nScanned {scanned_count} files, published {published_count} to PUBLISH/")

if __name__ == "__main__":
    main()
