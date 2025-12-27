# Dewey Decimal Skill

A Claude agent to organize ebooks by the [Dewey Decimal](https://en.wikipedia.org/wiki/Dewey_decimal_classification) system with OCD renaming rules through three distinct Skills. Codex Skills are brand new; supporting Codex would likely require some rework. See https://developers.openai.com/codex/skills for adapting these skills to Codex's format.

| skill                | description                                                             |
|:---------------------|:------------------------------------------------------------------------|
| metadata-extraction  | unzips .epub files and inspects metadata for author, contributors, year |
| filename-formatting  | OCD filename rules for translators, edition, ancient authors, etc.      |
| dewey-classification | organizes files by inferring Dewey Decimal codes from OCLC index        |

## Setup

1. Copy `config.example.ini` to `config.ini` and edit the paths. [^1]
2. Ensure your `arrivals_dir` and `books_dir` paths exist.
3. Run `./install` to install the agents/skills into `~/.claude`.

## Usage

Run the agent:
```bash
claude --agent rename-books
```

For single-file processing, specify the file path. For batch processing, point it at your arrivals directory.

### History File

The agent will store a history file documenting the before and after filenames, paths, and hash of each book it touches at `$arrivals_dir/renames.jsonl`.

### Regenerating `data/codes.md`

If you want to rebuild the Dewey code index:
```bash
python main.py > data/codes.md
```

The Classification codes are indexed and cross-compared by these sources:
- `lib/illinois.py` - https://www.library.illinois.edu/infosci/research/guides/dewey/
- `lib/oclc.py` - https://www.oclc.org/content/dam/oclc/dewey/ddc23-summaries.pdf

These are orchestrated together by `main.py` to create `data/codes.md`, which is provided in this repo.

> [!NOTE]
> DDC is proprietary and maintained by OCLC. [OpenLibrary](https://openlibrary.org/)
> exposes `dewey_decimal_class` in its Books API, but coverage appears uneven; I couldn’t find
> a public, comprehensive ISBN↔DDC mapping. [WorldCat](https://www.worldcat.org/) doesn’t
> provide a free bulk ISBN <-> DDC mapping.

Having already learned the topology of DDC codes with respect to library shelving, categorizing by [Library of Congress](https://www.loc.gov/standards) coding is unnatural to me, as much as I would prefer myself and all libraries to adopt it.

## License

- Code - [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
- Text - [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

[^1]: The `[permissions]` section is currently unused; agent runs appeared to ignore a local `~/.claude/settings.local.json`.

