---
name: filename-formatting
description: Format ebook filenames using citation format with author, title, year, and optional translator/editor. Use when constructing standardized filenames for library catalog.
---

# Filename Formatting

Format: `Author Last, First [Contributors] - Title (Year).ext`

## Author Field

### Single Author

Convert to citation format: `Last, First`

| Input | Output |
|-------|--------|
| Charles Bukowski | Bukowski, Charles |
| Simone de Beauvoir | de Beauvoir, Simone |
| Aristotle | Aristotle |

Name particles (de, van, von) stay lowercase with last name.
Single names (Aristotle, Plato) have no comma.

### Two Authors

Format: `Last1, First1 and Last2, First2`

| Input | Output |
|-------|--------|
| Andrew Dornenburg, Karen Page | Dornenburg, Andrew and Page, Karen |
| Brian Kernighan, Dennis Ritchie | Kernighan, Brian W. and Ritchie, Dennis |

### Three or More Authors

Format: `Last, First et al`

| Input | Output |
|-------|--------|
| William H. Press, Saul A. Teukolsky, ... | Press, William H. et al |

## Contributors

Square brackets with role abbreviation, after author:

| Role | Format |
|------|--------|
| Translator | `[tr. Last, First]` |
| Editor | `[ed. Last, First]` |
| Multiple | `[tr. Last1, First1; ed. Last2, First2]` |

Examples:
- `Aristotle [tr. Irwin, Terence] - Nicomachean Ethics (2019).pdf`
- `de Beauvoir, Simone [tr. Border, C., Malovany-Chevallier, S.] - The Second Sex (2010).epub`

## Title Field

Exact title as published. Subtitles: convert colon to space-dash-space.

| Original | Filename |
|----------|----------|
| Salt: A World History | Salt - A World History |
| Capital: A Critique of Political Economy | Capital - A Critique of Political Economy |

## Edition Field

Include only for non-first editions, in square brackets before year:

- `Press, William H. et al - Numerical Recipes [3rd Edition] (2007).pdf`
- `Kernighan, Brian W. and Ritchie, Dennis - C Programming Language [2nd Edition] (1988).pdf`

Omit for first editions.

## Year Field

Parentheses: `(YYYY)`

Use publication year of THIS edition/translation.

## File Extension

Preserve original: `.epub`, `.pdf`, `.mobi`, `.djvu`

## Complete Examples

```
Bukowski, Charles - Love Is A Dog From Hell (2007).epub
Kernighan, Brian W. and Ritchie, Dennis - C Programming Language (1988).pdf
Aristotle [tr. Irwin, Terence] - Nicomachean Ethics (2019).pdf
Marx, Karl [tr. Fowkes, Ben] - Capital - A Critique of Political Economy, Volume 1 (1867).epub
Hippo, St. Augustine of [tr. Chadwick, Henry] - The Confessions (2008).epub
Hegel, Georg W. F. [tr. Miller, A.V.] - Phenomenology of Spirit (1977).mobi
```

## Edge Cases

### Nobility/Religious Titles

Convert to citation form:
- St. Augustine of Hippo: `Hippo, St. Augustine of`
- Saint Thomas Aquinas: `Aquinas, Thomas`

### Multi-Volume Works

Include volume in title:
- `Capital - Volume 1: A Critique of Political Economy`

### Solutions Manuals

Include type in title:
- `Griffiths, David Jeffrey - Solutions Manual for Introduction to Quantum Mechanics (1995).pdf`

## Forbidden Characters

Do not use these characters in filenames:
- `:` (colon) – convert to space-dash-space in titles (see Title Field rules above)
- `\` (backslash)
- `*` (asterisk)
- `?` (question mark)
- `"` (quote)
- `<` `>` (angle brackets)
- `|` (pipe)
- ASCII control characters (U+0000–U+001F)
- Trailing space
- Trailing dot

Remove forbidden characters from titles and other fields (except colons, which convert to ` - `).

Examples:
- `How Should a Person Be?` → `How Should a Person Be`
- `Salt: A World History` → `Salt - A World History` (colon converts to dash)
- `What's the "Real" Point*` → `What's the Real Point`
