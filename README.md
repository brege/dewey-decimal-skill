# Dewey Decimal Skill

A Claude/Codex agent to organize ebooks by the [Dewey Decimal](https://en.wikipedia.org/wiki/Dewey_decimal_classification) system with OCD renaming rules through three distinct Skills:

| skill                | description                                                             |
|:---------------------|:------------------------------------------------------------------------|
| metadata-extraction  | unzips .epub files and inspects metadata for author, contributors, year |
| filename-formatting  | OCD filename rules for translators, edition, ancient authors, etc.      |
| dewey-classification | organizes files by inferring Dewey Decimal codes from OCLC index        |

## Setup

1. Copy `config.example.ini` to `config.ini` and edit the paths.

2. Run `./install` to install the agents/skills into `~/.claude`.

The Classification codes are indexed and cross-compared by these sources:
- `lib/illinois.py` - https://www.library.illinois.edu/infosci/research/guides/dewey/
- `lib/oclc.py` - https://www.oclc.org/content/dam/oclc/dewey/ddc23-summaries.pdf

These are orchestrated together by `main.py` to create `data/codes.md`, which is provided in this repo.

> [!NOTE] It's surprising to learn that the Dewey Decimal system is proprietary. 

[Worldcat](https://www.worldcat.org/) does not index DDC, nor does [OpenLibrary](https://openlibrary.org/). To my knowledge, there is no public repository linking ISBN <-> DDC.  

Having already learned the topology of DDC codes with respect to library shelving, categorizing by [Library of Congress](https://www.loc.gov/standards) coding is unnatural to me, as much as I would prefer myself and all libraries to adopt it.

## License

Code - [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)

Text -  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
