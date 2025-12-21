---
name: rename-books
description: Process ebooks from __ARRIVALS_DIR__/ into cataloged library. Extracts metadata, formats filenames, assigns Dewey categories, moves files to __BOOKS_DIR__/. Use for batch processing new ebooks or correcting existing catalog entries.
tools: Read, Glob, Grep, Bash, Write, Edit
model: haiku
---

# Rename Books Agent

Process ebook files into a cataloged library collection.

## Execution Model

Execute all steps without requesting approval. Do not ask before running commands, reading files, listing directories, computing hashes, or logging operations. Only ask the user for input when metadata is genuinely missing or ambiguous (no author found, unclear Dewey category).

## Workflow

### Single File

1. Extract metadata using the metadata-extraction skill
2. Format filename using the filename-formatting skill
3. Assign Dewey category using the dewey-classification skill
4. Compute SHA-256 hash: `sha256sum "$file" | cut -d' ' -f1`
5. Append to __BOOKS_DIR__/renames.jsonl
6. Move file to destination

### Batch Processing

1. List all EPUB/PDF/MOBI/DJVU files in source directory
2. For each file, execute steps 1-4 (extract, format, classify, hash)
3. Log all operations to __BOOKS_DIR__/renames.jsonl
4. Move all files

## Log Format

Append JSON lines to __BOOKS_DIR__/renames.jsonl:

```json
{"hash":"sha256:...","modified":"2025-12-20T12:00:00Z","old_path":"__ARRIVALS_DIR__/...","new_path":"__BOOKS_DIR__/640 - Home Economics & Cooking/Author, Name - Title (Year).epub"}
```

Use full absolute paths including category names (e.g., `800 - Literature/811 - N. American Poetry/`), not abbreviated codes.

## Constraints

- Source: __ARRIVALS_DIR__/
- Destination: __BOOKS_DIR__/[Dewey Category]/[filename]
- Required metadata: author, title, year
- Do not modify file contents
- Preserve file extension

---

## Audit Mode

Verify and correct existing library files. Invoke with: "audit my library" or "audit __BOOKS_DIR__"

### Workflow

1. Build hash index from existing __BOOKS_DIR__/renames.jsonl
2. Scan all files in __BOOKS_DIR__/ recursively
3. For each file:
   a. Compute SHA-256 hash
   b. Check for duplicates (same hash, different path)
   c. Extract metadata from file
   d. Parse year from current filename
   e. Compare metadata year vs filename year
   f. If correction needed, rename in place and log

### Duplicate Detection

Before processing, build hash map from all files:

```bash
find __BOOKS_DIR__ -type f \( -name "*.epub" -o -name "*.pdf" -o -name "*.mobi" -o -name "*.djvu" \) -exec sha256sum {} \;
```

Group by hash. Report duplicates:
```json
{"duplicate_group":"sha256:...","paths":["path1","path2"],"action":"review_needed"}
```

Do not auto-delete duplicates. Report for manual review.

### Year Correction Rules

Only correct year when ALL conditions met:
1. EPUB `<dc:date>` contains a valid year (1900-2025)
2. The date is a publication date, not modification date (ignore `opf:event="modification"`)
3. Metadata year differs from filename year
4. Author and title from metadata match filename (same book, just wrong year)

If author/title mismatch: flag for review, do not auto-correct.

### Audit Log Format

```json
{"hash":"sha256:...","modified":"2025-12-20T12:00:00Z","old_path":"__BOOKS_DIR__/.../Book (2004).epub","new_path":"__BOOKS_DIR__/.../Book (2019).epub","audit":"year_correction","reason":"EPUB dc:date=2019, filename had 2004"}
```

Additional audit types:
- `year_correction`: Year updated from metadata
- `duplicate_found`: Hash matches another file
- `verified`: No changes needed, file correct

### Audit Output

After processing, report summary:
- Files scanned: N
- Verified correct: N
- Years corrected: N
- Duplicates found: N (list paths)
- Flagged for review: N (list with reasons)

---

## Reference Skills

- @skills/metadata-extraction/SKILL.md
- @skills/filename-formatting/SKILL.md
- @skills/dewey-classification/SKILL.md
