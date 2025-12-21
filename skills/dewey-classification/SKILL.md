---
name: dewey-classification
description: Assign Dewey Decimal categories to books and determine correct shelf location in __BOOKS_DIR__/. Handles directory leafing rules for when to create subcategories. Use when cataloging books or reorganizing library structure.
---

# Dewey Classification

Assign Dewey codes and determine shelf location in __BOOKS_DIR__/.

## Assignment Process

1. Identify primary subject matter
2. **ALWAYS read data/codes.md** to find the correct code and category name
3. Check existing __BOOKS_DIR__/ directory structure
4. Apply leafing rules to determine final path

## CRITICAL: Directory Naming

**NEVER invent or guess category names.** Before creating any directory:

1. Read data/codes.md
2. Find the exact line matching the code (e.g., `- 130 Parapsychology and occultism`)
3. Use the EXACT name from that file: `130 - Parapsychology and occultism`

Format: `XXX - [exact name from codes.md]`

Examples from data/codes.md:
- `- 110 Metaphysics` → directory: `110 - Metaphysics`
- `- 130 Parapsychology and occultism` → directory: `130 - Parapsychology and occultism`
- `- 160 Philosophical logic` → directory: `160 - Philosophical logic`

**If you cannot find a code in data/codes.md, ask the user.**

## Leafing Rules

Directories stay flat until thresholds trigger subdivision. **Do not create empty directories.**

Hierarchy: centennials (X00) → decades (XY0) → integrals (XYZ)

### Rule: When to Create Subdirectory

Create XY0 subdirectory under X00 **ONLY** when BOTH conditions met:
1. X00 contains 6+ books total
2. 3+ books share the same Y value (would belong in XY0)

Same rule applies recursively: create XYZ under XY0 when XY0 has 6+ books and 3+ share same Z.

### Rule: Do NOT Create Preemptively

- **Never create empty directories**
- **Never create a subdivision with fewer than 3 books**
- Keep books at the parent level until the threshold is reached
- Example: If you have 2 ethics books in 100/, leave them in 100/. Do not create 170/ until you have 3+ ethics books AND 6+ total in 100/.

The goal is minimal bureaucratic structure. Only subdivide when the volume justifies separating material from the pack.

### Example

```
500 - Natural Sciences and Mathematics/
  (5 physics books, 2 math books, 1 astronomy book)
```

Total: 8 books. Physics has 5 (3+ threshold met). Create 530 subdirectory:

```
500 - Natural Sciences and Mathematics/
  530 - Physics/
    (5 physics books)
  (2 math books, 1 astronomy book remain in 500)
```

When math reaches 3+ books, create 510 subdirectory.

## Current Structure

Check __BOOKS_DIR__/ before placing. Always verify directory names against data/codes.md.

Subdirectories are created dynamically based on leafing rules. Do not assume a fixed structure - scan the actual directory and cross-reference with data/codes.md.

## Category Guidelines

Always look up the exact code and name in data/codes.md. Common top-level categories:

- **000** - Computer science, information, general works
- **100** - Philosophy & psychology (includes 150 Psychology)
- **300** - Social sciences (economics, politics, law)
- **500** - Natural sciences and mathematics
- **600** - Technology (includes 640 Home economics)
- **700** - Arts
- **800** - Literature (810 N. American, 820 English, 890 other languages)
- **900** - History & geography (includes 920 Biography)

### Classification Examples

When classifying, find the most specific applicable code:
- Philosophy of mind → look up 12X codes in data/codes.md
- Ethics → 170 Ethics (Moral philosophy)
- Psychology → 150 Psychology
- Cooking → 641 Food & drink (check data/codes.md for exact name)

**Always verify against data/codes.md before creating directories.**

## Code Reference

The authoritative source is data/codes.md. Read it before every classification decision.

## When to Ask User

- Book spans multiple primary subjects equally
- Subject is specialized and code unclear
- Purpose ambiguous (philosophy about X vs history of X)
- New directory creation uncertain
