---
name: dewey-classification
description: Assign Dewey Decimal categories to books and determine correct shelf location in __BOOKS_DIR__/. Handles directory leafing rules for when to create subcategories. Use when cataloging books or reorganizing library structure.
---

# Dewey Classification

Assign Dewey codes and determine shelf location in __BOOKS_DIR__/.

## Assignment Process

1. Identify primary subject matter
2. Look up code in data/codes.md
3. Check existing __BOOKS_DIR__/ directory structure
4. Apply leafing rules to determine final path

## Leafing Rules

Directories stay flat until thresholds trigger subdivision.

### Rule: When to Create Subdirectory

Create XY0 subdirectory under X00 when BOTH conditions met:
1. X00 contains 6+ books total
2. 3+ books share the same Y value (would belong in XY0)

Same rule applies recursively: create XYZ under XY0 when XY0 has 6+ books and 3+ share same Z.

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

### Promoted Categories

Some frequently-used categories exist at root level (not nested under parent):

| Category | Why |
|----------|-----|
| 150 - Psychology | High volume, distinct from philosophy |
| 640 - Home Economics & Cooking | High volume, distinct from technology |
| 920 - Biography | High volume, distinct from history |

When assigning to these categories, place directly in root-level directory.

## Current Structure

Check __BOOKS_DIR__/ before placing. Respect existing organization:

```
__BOOKS_DIR__/
  000 - General Works/
  100 - Philosophy/
  150 - Psychology/          (promoted)
  300 - Social Sciences/
  500 - Natural Sciences and Mathematics/
    510 - Mathematics/
    520 - Astronomy and Applied Sciences/
    530 - Physics/
  600 - Technology/
  640 - Home Economics & Cooking/   (promoted)
  700 - Arts/
  800 - Literature/
    810 - N. American Literature/
    811 - N. American Poetry/
    820 - English Literature/
    890 - Literature of other languages/
  900 - History/
  920 - Biography/           (promoted)
```

## Category Guidelines

### 100 - Philosophy
Logic, ethics, metaphysics, epistemology, social philosophy.
- Critique of Pure Reason: 100
- Being and Time: 100
- Gender Trouble: 100 (philosophical social theory)

### 150 - Psychology
Psychology, cognitive science, neuroscience, self-help.
- Maps of Meaning: 150

### 300 - Social Sciences
Economics, politics, law, sociology.
- Capital (Marx): 300

### 500 - Natural Sciences
Math (510), astronomy (520), physics (530), chemistry (540), biology (570).
- Understanding Linear Algebra: 510
- Black Holes & Time Warps: 530
- The Hidden Reality (cosmology): 520

### 600 - Technology
Engineering, medicine, manufacturing.

### 640 - Cooking
Cookbooks, food preparation, foraging.
- The Pizza Bible: 640
- Edible Wild Plants: 640

### 700 - Arts
Art, music, film, design, photography.

### 800 - Literature
Fiction, poetry, drama, essays.
- 810: North American prose
- 811: North American poetry
- 820: English/British literature
- 890: Other languages

Bukowski prose (Factotum, Ham On Rye): 810
Bukowski poetry: 811

### 900 - History
History, geography, travel.

### 920 - Biography
Pure biography of individuals.
Philosophy about a person (Louis C.K. and Philosophy): 100, not 920.

## Code Reference

Full Dewey codes in data/codes.md.

## When to Ask User

- Book spans multiple primary subjects equally
- Subject is specialized and code unclear
- Purpose ambiguous (philosophy about X vs history of X)
- New directory creation uncertain
