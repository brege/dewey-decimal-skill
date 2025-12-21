from __future__ import annotations

import io
import os
import re
import subprocess
import tempfile
from typing import Dict, List, Sequence, Tuple

import requests

SOURCE_URL = "https://www.oclc.org/content/dam/oclc/dewey/ddc23-summaries.pdf"
ENTRY_PATTERN = re.compile(r"(\d{3}(?:\.\d+)?)\s+(.+?)(?=(?:\s{2,}\d{3}(?:\.\d+)?\b)|$)")


def fetch_pdf_bytes() -> bytes:
    response = requests.get(SOURCE_URL, timeout=60)
    response.raise_for_status()
    return response.content


def extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError:
        return _extract_text_with_pdftotext(pdf_bytes)
    reader = PdfReader(io.BytesIO(pdf_bytes))
    page_texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            page_texts.append(text)
    if not page_texts:
        raise RuntimeError("Unable to extract text from PDF via pypdf")
    return "\n".join(page_texts)


def _extract_text_with_pdftotext(pdf_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        pdf_file.write(pdf_bytes)
        pdf_path = pdf_file.name
    try:
        completed_process = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            check=True,
            text=True,
            capture_output=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError(
            "Neither pypdf nor the pdftotext command are available for PDF extraction"
        ) from error
    finally:
        os.remove(pdf_path)
    return completed_process.stdout


def extract_third_summary_text(full_text: str) -> str:
    normalized = full_text.replace("\r\n", "\n").replace("\r", "\n")
    marker = "Third Summary"
    start_index = normalized.find(marker)
    if start_index == -1:
        raise RuntimeError("Unable to locate Third Summary section in PDF text")
    return normalized[start_index:]


def parse_third_summary_entries(summary_text: str) -> List[Tuple[str, str]]:
    entries: List[Tuple[str, str]] = []
    for raw_line in summary_text.splitlines():
        cleaned_line = raw_line.replace("\x0c", "").rstrip()
        if not cleaned_line.strip():
            continue
        stripped_line = cleaned_line.strip()
        if stripped_line.startswith("Third Summary"):
            continue
        if stripped_line.startswith("Thousand Sections"):
            continue
        if stripped_line.startswith("Consult schedules"):
            continue
        for number, description in ENTRY_PATTERN.findall(cleaned_line):
            normalized_description = description.strip()
            if normalized_description:
                entries.append((number, normalized_description))
    if not entries:
        raise RuntimeError("No entries could be parsed from the third summary text")
    return entries


def build_markdown(entries: Sequence[Tuple[str, str]]) -> str:
    grouped: Dict[int, List[Tuple[str, str]]] = {index: [] for index in range(10)}
    for number, description in entries:
        bucket_index = _bucket_for_number(number)
        grouped[bucket_index].append((number, description))
    markdown_lines: List[str] = ["# Dewey Decimal System Call Numbers", ""]
    for index in range(10):
        markdown_lines.append(f"## The {index:01d}00s")
        bucket_entries = grouped.get(index, [])
        bucket_entries.sort(key=lambda entry: _entry_sort_key(entry[0]))
        for number, description in bucket_entries:
            markdown_lines.append(f"- {number} {description}")
        markdown_lines.append("")
    return "\n".join(markdown_lines).strip() + "\n"


def _bucket_for_number(number: str) -> int:
    normalized = number.split(".", 1)[0]
    padded = normalized.zfill(3)
    return int(padded) // 100


def _entry_sort_key(number: str) -> Tuple[int, str]:
    integer_part, _, fractional_part = number.partition(".")
    return int(integer_part), fractional_part


def main() -> None:
    pdf_bytes = fetch_pdf_bytes()
    pdf_text = extract_pdf_text(pdf_bytes)
    summary_text = extract_third_summary_text(pdf_text)
    entries = parse_third_summary_entries(summary_text)
    markdown_output = build_markdown(entries)
    print(markdown_output)


if __name__ == "__main__":
    main()
