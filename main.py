from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from collections.abc import Sequence
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
# Each source script emits Markdown bullets containing a call number and label.
ENTRY_PATTERN = re.compile(r"^- (\S+) (.+)$")


def read_entries_from_script(relative_path: str) -> dict[str, str]:
    script_path = SCRIPT_DIR / relative_path
    completed_process = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    entries: dict[str, str] = {}
    for line in completed_process.stdout.splitlines():
        match = ENTRY_PATTERN.match(line.strip())
        if match:
            entries[match.group(1)] = match.group(2).strip()
    return entries


def build_canonical_entries() -> dict[str, str]:
    oclc_entries = read_entries_from_script("lib/oclc.py")
    illinois_entries = read_entries_from_script("lib/illinois.py")
    canonical_entries: dict[str, str] = {}
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


def _entry_sort_key(number: str) -> tuple[int, str]:
    integer_value = _extract_integer_part(number)
    return integer_value, number


def _is_unassigned(description: str) -> bool:
    normalized = description.lower()
    return "unassigned" in normalized or "not assigned" in normalized


def build_markdown(entries: dict[str, str]) -> str:
    grouped: dict[int, list[tuple[str, str]]] = {}
    for number, description in entries.items():
        integer_value = _extract_integer_part(number)
        bucket = integer_value // 100
        grouped.setdefault(bucket, []).append((number, description))
    markdown_lines: list[str] = ["# Dewey Decimal System Call Numbers", ""]
    for bucket in range(10):
        markdown_lines.append(f"## The {bucket:01d}00s")
        bucket_entries = sorted(
            grouped.get(bucket, []), key=lambda entry: _entry_sort_key(entry[0])
        )
        for number, description in bucket_entries:
            markdown_lines.append(f"- {number} {description}")
        markdown_lines.append("")
    return "\n".join(markdown_lines).strip() + "\n"


def get_version() -> str:
    with (SCRIPT_DIR / "pyproject.toml").open("rb") as config_file:
        metadata = tomllib.load(config_file)
    project = metadata.get("project")
    if not isinstance(project, dict):
        raise TypeError("pyproject.toml must contain a project table")
    version = project.get("version")
    if not isinstance(version, str):
        raise TypeError("project.version must be a string")
    return version


def parse_args(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="dewey",
        description="Generate the canonical Dewey code index",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
    )
    parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    parse_args(argv)
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
