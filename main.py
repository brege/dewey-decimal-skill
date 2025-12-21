from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
ENTRY_PATTERN = re.compile(r"^- (\S+) (.+)$")


def read_entries_from_script(relative_path: str) -> Dict[str, str]:
    script_path = SCRIPT_DIR / relative_path
    completed_process = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    entries: Dict[str, str] = {}
    for line in completed_process.stdout.splitlines():
        match = ENTRY_PATTERN.match(line.strip())
        if match:
            entries[match.group(1)] = match.group(2).strip()
    return entries


def build_canonical_entries() -> Dict[str, str]:
    oclc_entries = read_entries_from_script("lib/oclc.py")
    illinois_entries = read_entries_from_script("lib/illinois.py")
    canonical_entries: Dict[str, str] = {}
    for number in sorted(oclc_entries, key=_entry_sort_key):
        description = oclc_entries[number]
        if _is_unassigned(description):
            continue
        canonical_entries[number] = description
    for number in sorted(illinois_entries, key=_entry_sort_key):
        if number in canonical_entries:
            continue
        description = illinois_entries[number]
        if _is_unassigned(description):
            continue
        canonical_entries[number] = description
    return canonical_entries


def _entry_sort_key(number: str) -> Tuple[int, str]:
    integer_value = _extract_integer_part(number)
    return integer_value, number


def _is_unassigned(description: str) -> bool:
    normalized = description.lower()
    return "unassigned" in normalized or "not assigned" in normalized


def build_markdown(entries: Dict[str, str]) -> str:
    grouped: Dict[int, List[Tuple[str, str]]] = {}
    for number, description in entries.items():
        integer_value = _extract_integer_part(number)
        bucket = integer_value // 100
        grouped.setdefault(bucket, []).append((number, description))
    markdown_lines: List[str] = ["# Dewey Decimal System Call Numbers", ""]
    for bucket in range(10):
        markdown_lines.append(f"## The {bucket:01d}00s")
        bucket_entries = sorted(grouped.get(bucket, []), key=lambda entry: _entry_sort_key(entry[0]))
        for number, description in bucket_entries:
            markdown_lines.append(f"- {number} {description}")
        markdown_lines.append("")
    return "\n".join(markdown_lines).strip() + "\n"


def main() -> None:
    canonical_entries = build_canonical_entries()
    markdown_output = build_markdown(canonical_entries)
    print(markdown_output)


def _extract_integer_part(number: str) -> int:
    hyphen_split = number.split("-", 1)[0]
    integer_part, _, _ = hyphen_split.partition(".")
    try:
        integer_value = int(integer_part)
    except ValueError:
        integer_value = 0
    return integer_value


if __name__ == "__main__":
    main()
