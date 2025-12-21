from __future__ import annotations

import re
from typing import List, Optional, Sequence, Tuple

import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString

SOURCE_URL = "https://www.library.illinois.edu/infosci/research/guides/dewey/"


def fetch_html_document() -> str:
    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()
    return response.text


def extract_panel_sections(html_document: str) -> List[Tuple[str, List[Tuple[str, bool]]]]:
    soup = BeautifulSoup(html_document, "html.parser")
    panels = soup.select("div#ui_lib_panel")
    if not panels:
        raise RuntimeError("Unable to locate Dewey panels in source document")
    extracted_sections: List[Tuple[str, List[Tuple[str, bool]]]] = []
    for panel in panels:
        heading_element = panel.select_one("span.sh-font-semibold")
        if heading_element is None:
            raise RuntimeError("Missing panel heading text")
        heading_text = heading_element.get_text(strip=True)
        content_division = _find_panel_content(panel)
        panel_lines = _extract_lines_from_panel(content_division)
        extracted_sections.append((heading_text, panel_lines))
    return extracted_sections


def _find_panel_content(panel: Tag) -> Tag:
    for element in panel.select("div"):
        if _is_panel_content_division(element):
            return element
    raise RuntimeError("Missing panel content division")


def _is_panel_content_division(element: Tag) -> bool:
    for class_name in element.get("class", []):
        if class_name.startswith("ui-lib-coll-pan-id") and "_" not in class_name:
            return True
    return False


def _extract_lines_from_panel(content_division: Tag) -> List[Tuple[str, bool]]:
    collected_entries: List[Tuple[str, bool]] = []
    current_parts: List[str] = []

    def flush_current_entry(context: Optional[dict[str, int]]) -> None:
        if not current_parts:
            return
        combined_text = " ".join(current_parts)
        normalized_text = _normalize_text(combined_text)
        if normalized_text:
            is_footnote = context is not None and context.get("line_index", 0) == 0
            collected_entries.append((normalized_text, is_footnote))
            if context is not None:
                context["line_index"] = context.get("line_index", 0) + 1
        current_parts.clear()

    def feed_fragment(fragment: str) -> None:
        current_parts.append(fragment)

    def traverse(node, context: Optional[dict[str, int]]) -> None:
        if isinstance(node, NavigableString):
            normalized_fragment = _normalize_text(str(node))
            if normalized_fragment:
                feed_fragment(normalized_fragment)
        elif isinstance(node, Tag):
            tag_name = node.name.lower()
            if tag_name == "br":
                flush_current_entry(context)
            elif tag_name == "p":
                flush_current_entry(context)
                paragraph_context: dict[str, int] = {"line_index": 0}
                for child in node.children:
                    traverse(child, paragraph_context)
                flush_current_entry(paragraph_context)
            else:
                for child in node.children:
                    traverse(child, context)

    for child in content_division.children:
        traverse(child, None)
    flush_current_entry(None)
    if not collected_entries:
        raise RuntimeError("Panel contained no Dewey entries")
    return collected_entries


def _normalize_text(value: str) -> str:
    sanitized_value = value.replace("\xa0", " ")
    collapsed_whitespace = " ".join(sanitized_value.split())
    without_punctuation_gaps = re.sub(r"\s+([,.;:])", r"\1", collapsed_whitespace)
    without_ordinal_gaps = re.sub(r"(\d+)\s+(st|nd|rd|th)\b", r"\1\2", without_punctuation_gaps, flags=re.IGNORECASE)
    return without_ordinal_gaps


def _slugify(value: str) -> str:
    lowered = value.lower()
    replaced = re.sub(r"[^a-z0-9]+", "-", lowered)
    condensed = re.sub(r"-{2,}", "-", replaced)
    return condensed.strip("-")


def build_markdown(sections: Sequence[Tuple[str, Sequence[Tuple[str, bool]]]]) -> str:
    markdown_lines: List[str] = ["# Dewey Decimal System Call Numbers", ""]
    footnote_definitions: List[str] = []
    identifier_counts: dict[str, int] = {}
    for heading_text, entries in sections:
        markdown_lines.append(f"## {heading_text}")
        last_bullet_line_index: Optional[int] = None
        last_bullet_text: Optional[str] = None
        for entry_text, is_footnote in entries:
            if is_footnote:
                if last_bullet_line_index is None or last_bullet_text is None:
                    raise RuntimeError("Footnote text appeared before any call number entry")
                identifier = _derive_footnote_identifier(heading_text, last_bullet_text, identifier_counts)
                reference_label = f"cite:{identifier}"
                markdown_lines[last_bullet_line_index] = f"{markdown_lines[last_bullet_line_index]} [^{reference_label}]"
                footnote_definitions.append(f"[^{reference_label}]: cite: {entry_text}")
            else:
                markdown_lines.append(f"- {entry_text}")
                last_bullet_line_index = len(markdown_lines) - 1
                last_bullet_text = entry_text
        markdown_lines.append("")
    if footnote_definitions:
        markdown_lines.extend(footnote_definitions)
        markdown_lines.append("")
    return "\n".join(markdown_lines).strip() + "\n"


def _derive_footnote_identifier(
    heading_text: str,
    entry_text: str,
    identifier_counts: dict[str, int],
) -> str:
    heading_slug = _slugify(heading_text)
    entry_slug = _slugify(entry_text)
    base_identifier = f"{heading_slug}-{entry_slug}".strip("-")
    count = identifier_counts.get(base_identifier, 0) + 1
    identifier_counts[base_identifier] = count
    if count == 1:
        return base_identifier
    return f"{base_identifier}-{count}"


def main() -> None:
    html_document = fetch_html_document()
    sections = extract_panel_sections(html_document)
    markdown_output = build_markdown(sections)
    print(markdown_output)


if __name__ == "__main__":
    main()
