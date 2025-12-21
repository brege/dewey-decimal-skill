---
name: metadata-extraction
description: Extract author, title, year, and contributor metadata from ebook files (EPUB, PDF). Use when you need to identify a book's bibliographic information from its embedded metadata or filename.
---

# Metadata Extraction

Extract bibliographic metadata from ebook files.

## Priority Order

1. EPUB OPF metadata (most authoritative)
2. PDF document properties
3. Filename parsing (least reliable)
4. User input (for disambiguation only)

## EPUB Extraction

### Step 1: Find OPF Path

```bash
unzip -p "$file" META-INF/container.xml | grep -oP 'full-path="\K[^"]*'
```

Returns path like `OEBPS/content.opf` or `content.opf`.

### Step 2: Extract Metadata

```bash
unzip -p "$file" "$opf_path" | grep -E '<dc:(creator|title|date|contributor)'
```

### Fields

| Tag | Content |
|-----|---------|
| `<dc:creator>` | Author name(s) |
| `<dc:title>` | Book title |
| `<dc:date>` | Publication date (extract YYYY) |
| `<dc:contributor opf:role="trn">` | Translator |
| `<dc:contributor opf:role="edt">` | Editor |

## PDF Extraction

```bash
pdfinfo "$file" 2>/dev/null | grep -E '^(Title|Author|CreationDate|ModDate):'
```

Extract:
- Title field
- Author field
- CreationDate year (format: D:YYYYMMDDhhmmss)

## Filename Parsing

Parse for hints when metadata insufficient:
- Author: Often at start, before dash or title
- Title: Main text
- Year: Four digits in parentheses or at end

Example: `Charles.Bukowski.-.Love.Is.A.Dog.From.Hell.2007.RETAIL.EPUB.eBook-CTO.epub`
- Author: Charles Bukowski
- Title: Love Is A Dog From Hell
- Year: 2007

## Year Rules

Use publication year of THIS edition, not original work.

- Aristotle's Nicomachean Ethics (ancient) with Irwin translation (2019): use 2019
- Marx's Capital originally 1867: use edition's publication year
- If EPUB date differs from original work date, prefer EPUB date

## Useless Metadata

Some EPUBs have placeholder or garbage metadata. Treat these as missing:
- Title: `[No data]`, `Unknown`, `Untitled`, empty
- Author: `Unknown`, `Anonymous` (unless actually anonymous work), empty
- Date: Only modification date present, no publication date

When OPF metadata is useless, fall back to filename parsing immediately.

## Author Name Normalization

Fix common capitalization issues from metadata:
- `Harold Mcgee` → `Harold McGee` (fix surname caps)
- `CHARLES BUKOWSKI` → `Charles Bukowski` (fix all-caps)
- Preserve intentional lowercase particles: `de Beauvoir`, `van Gogh`

Use `opf:file-as` attribute if present - it often has correct citation format:
```xml
<dc:creator opf:file-as="McGee, Harold">Harold Mcgee</dc:creator>
```

## Translator Verification

Translator info in filenames is often wrong or refers to different editions.
- Verify translator matches publisher/edition (e.g., Penguin 2004 Marx = Fowkes, not Guyer-Wood)
- If translator not in metadata, check ISBN against known editions
- When uncertain, ask user

## Missing Data

When metadata genuinely unavailable:
- No author: Ask user
- No year: Ask user for "publication year of this edition"
- Ambiguous title: Ask user
- No translator but work is translated: Ask user or look up by ISBN/publisher

Do not guess. Do not proceed without author and title.
